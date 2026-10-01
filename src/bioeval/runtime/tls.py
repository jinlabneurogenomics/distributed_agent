"""Supervise TLS-intercepting egress for protected BioEval runs."""

from __future__ import annotations

import atexit
import contextlib
import hashlib
import json
import os
import secrets
import shutil
import socket
import subprocess
import tempfile
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Iterator
from urllib.parse import quote, unquote, urlsplit

from .paths import REPO_ROOT
from .policy import SourcePolicy


DEFAULT_MITMDUMP_EXECUTABLE = (
    REPO_ROOT / ".pixi" / "envs" / "tls-proxy" / "bin" / "mitmdump"
)
DEFAULT_TLS_FILTER_ADDON = Path(__file__).resolve().with_name("tls_filter_addon.py")
TLS_EGRESS_AUDIT_FILENAME = "tls_egress_audit.jsonl"
TLS_EGRESS_LOG_FILENAME = "tls_egress_proxy.log"
TLS_EGRESS_READINESS_TIMEOUT_S = 120
TLS_EGRESS_START_ATTEMPTS = 2
TLS_EGRESS_SHARED_ENV = "BIOEVAL_SHARED_TLS_EGRESS"


def normalized_filter_text(parts: Iterable[str | bytes | None]) -> str:
    """Normalize URL/body material without losing exact-path matching."""
    decoded: list[str] = []
    for part in parts:
        if part is None:
            continue
        if isinstance(part, bytes):
            value = part.decode("utf-8", errors="replace")
        else:
            value = str(part)
        # Decode nested URL encoding (common in search and redirect URLs).
        for _ in range(2):
            expanded = unquote(value)
            if expanded == value:
                break
            value = expanded
        decoded.append(value)
    return "\n".join(decoded)


def request_filter_text(
    *,
    url: str,
    method: str = "",
    headers: Iterable[tuple[str, str]] = (),
    body: bytes | str | None = None,
) -> str:
    """Build the text inspected before an HTTP request leaves the proxy."""
    parsed = urlsplit(url)
    header_text = "\n".join(f"{key}: {value}" for key, value in headers)
    return normalized_filter_text(
        (
            method,
            url,
            parsed.hostname,
            parsed.path,
            parsed.query,
            header_text,
            body,
        )
    )


def response_filter_text(
    *,
    headers: Iterable[tuple[str, str]] = (),
    body: bytes | str | None = None,
) -> str:
    """Build the text inspected before an HTTP response reaches the agent."""
    header_text = "\n".join(f"{key}: {value}" for key, value in headers)
    return normalized_filter_text((header_text, body))


def url_sha256(url: str) -> str:
    """Return an audit-safe identifier without persisting attempted URLs."""
    return hashlib.sha256(url.encode()).hexdigest()


@dataclass(frozen=True)
class TlsEgressHandle:
    """Metadata for one running TLS egress proxy."""

    base_url: str
    ca_cert_path: Path
    audit_path: Path
    log_path: Path
    command: tuple[str, ...]
    lease_id: str | None = None
    supervisor_pid: int | None = None
    _proxy_auth: tuple[str, str] | None = field(default=None, repr=False)

    def proxy_url(self, *, host: str, port: int) -> str:
        """Return a lease-authenticated proxy URL at a bridged endpoint."""
        if self._proxy_auth is None:
            return f"http://{host}:{port}"
        username, password = self._proxy_auth
        return (
            f"http://{quote(username, safe='')}:{quote(password, safe='')}"
            f"@{host}:{port}"
        )


def _free_loopback_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _wait_ready(
    *,
    process: subprocess.Popen,
    port: int,
    ca_cert_path: Path,
    log_path: Path,
    timeout_s: float = TLS_EGRESS_READINESS_TIMEOUT_S,
) -> None:
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        if process.poll() is not None:
            tail = log_path.read_text(errors="replace")[-4000:]
            raise RuntimeError(
                f"TLS egress proxy exited with {process.returncode}: {tail}"
            )
        if ca_cert_path.is_file():
            try:
                with socket.create_connection(("127.0.0.1", port), timeout=0.1):
                    return
            except OSError:
                pass
        time.sleep(0.05)
    raise TimeoutError(
        f"TLS egress proxy did not listen on 127.0.0.1:{port} or create its CA"
    )


def _terminate_process(process: subprocess.Popen[object]) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def _resolve_executable(value: str | Path) -> Path:
    executable = Path(value)
    if executable.is_file():
        return executable.resolve()
    resolved = shutil.which(str(value))
    if resolved is None:
        raise RuntimeError(
            f"mitmdump not found at {value}; run `pixi install -e tls-proxy`"
        )
    return Path(resolved).resolve()


def _write_json_atomic(path: Path, value: dict[str, object]) -> None:
    temporary = path.with_suffix(f"{path.suffix}.{secrets.token_hex(4)}.tmp")
    temporary.write_text(json.dumps(value, sort_keys=True) + "\n")
    os.replace(temporary, path)


class TlsEgressSupervisor:
    """Process-scoped mitmproxy supervisor with isolated per-run leases."""

    def __init__(
        self,
        *,
        policy: SourcePolicy,
        mitmdump_executable: str | Path = DEFAULT_MITMDUMP_EXECUTABLE,
        addon_path: Path = DEFAULT_TLS_FILTER_ADDON,
        readiness_timeout_s: float = TLS_EGRESS_READINESS_TIMEOUT_S,
        start_attempts: int = TLS_EGRESS_START_ATTEMPTS,
    ) -> None:
        if not policy.enabled:
            raise ValueError("TLS egress supervisor requires an enabled source policy")
        if start_attempts < 1:
            raise ValueError("start_attempts must be at least one")
        self.policy = policy
        self.executable = _resolve_executable(mitmdump_executable)
        self.addon_path = addon_path.resolve()
        if not self.addon_path.is_file():
            raise FileNotFoundError(f"TLS filter addon not found: {self.addon_path}")
        self.readiness_timeout_s = readiness_timeout_s
        self.start_attempts = start_attempts
        self._root = Path(
            tempfile.mkdtemp(prefix=f"bioeval-tls-{policy.digest[:12]}-", dir="/tmp")
        )
        self._lease_dir = self._root / "leases"
        self._audit_dir = self._root / "audits"
        self._lease_dir.mkdir()
        self._audit_dir.mkdir()
        self._policy_path = self._root / "policy.json"
        self._policy_path.write_text(json.dumps(policy.broker_payload()))
        self._process: subprocess.Popen[str] | None = None
        self._command: tuple[str, ...] = ()
        self._ca_cert_path: Path | None = None
        self._log_path: Path | None = None
        self._port: int | None = None
        self._active_leases: set[str] = set()
        self._start_attempts_used = 0
        self._closed = False
        self._lock = threading.RLock()

    @property
    def pid(self) -> int | None:
        with self._lock:
            if self._process is None or self._process.poll() is not None:
                return None
            return self._process.pid

    @property
    def active_lease_count(self) -> int:
        with self._lock:
            return len(self._active_leases)

    @property
    def start_attempts_used(self) -> int:
        with self._lock:
            return self._start_attempts_used

    def _start_locked(self) -> None:
        if self._closed:
            raise RuntimeError("TLS egress supervisor is closed")
        if self._process is not None and self._process.poll() is None:
            return

        failures: list[str] = []
        for attempt in range(1, self.start_attempts + 1):
            attempt_dir = self._root / f"attempt-{attempt}-{secrets.token_hex(4)}"
            conf_dir = attempt_dir / "mitmproxy"
            conf_dir.mkdir(parents=True)
            log_path = attempt_dir / "supervisor.log"
            port = _free_loopback_port()
            command = (
                str(self.executable),
                "--listen-host",
                "127.0.0.1",
                "--listen-port",
                str(port),
                "--set",
                f"confdir={conf_dir}",
                "--set",
                "connection_strategy=lazy",
                "--set",
                "block_global=false",
                "--set",
                "proxyauth=any",
                "--set",
                "termlog_verbosity=warn",
                "--scripts",
                str(self.addon_path),
            )
            env = {
                "PATH": f"{self.executable.parent}:/usr/bin:/bin",
                "HOME": str(attempt_dir),
                "TMPDIR": str(attempt_dir),
                "LC_ALL": "C.UTF-8",
                "LANG": "C.UTF-8",
                "PYTHONPATH": str(REPO_ROOT / "src"),
                "BIOEVAL_TLS_POLICY": str(self._policy_path),
                "BIOEVAL_TLS_LEASE_DIR": str(self._lease_dir),
                "BIOEVAL_TLS_AUDIT_DIR": str(self._audit_dir),
            }
            linker_path = os.environ.get("LD_LIBRARY_PATH")
            if linker_path:
                env["LD_LIBRARY_PATH"] = linker_path

            with log_path.open("w") as log_handle:
                process = subprocess.Popen(
                    command,
                    stdin=subprocess.DEVNULL,
                    stdout=log_handle,
                    stderr=subprocess.STDOUT,
                    env=env,
                    text=True,
                )
            ca_cert_path = conf_dir / "mitmproxy-ca-cert.pem"
            try:
                _wait_ready(
                    process=process,
                    port=port,
                    ca_cert_path=ca_cert_path,
                    log_path=log_path,
                    timeout_s=self.readiness_timeout_s,
                )
            except (RuntimeError, TimeoutError) as exc:
                _terminate_process(process)
                tail = (
                    log_path.read_text(errors="replace")[-4000:]
                    if log_path.is_file()
                    else ""
                )
                failures.append(f"attempt {attempt}: {exc}; log tail: {tail}")
                continue

            self._process = process
            self._command = command
            self._ca_cert_path = ca_cert_path
            self._log_path = log_path
            self._port = port
            self._start_attempts_used = attempt
            return

        raise RuntimeError(
            "TLS egress supervisor failed to start after "
            f"{self.start_attempts} attempts: {' | '.join(failures)}"
        )

    @contextlib.contextmanager
    def lease(self, *, run_dir: Path) -> Iterator[TlsEgressHandle]:
        """Lease the shared proxy while writing only this run's audit stream."""
        run_dir.mkdir(parents=True, exist_ok=True)
        final_audit_path = run_dir / TLS_EGRESS_AUDIT_FILENAME
        run_log_path = run_dir / TLS_EGRESS_LOG_FILENAME
        token = secrets.token_hex(24)
        password = secrets.token_urlsafe(32)
        temporary_audit_path = self._audit_dir / f"{token}.jsonl"
        lease_path = self._lease_dir / f"{token}.json"

        with self._lock:
            self._start_locked()
            assert self._process is not None
            assert self._ca_cert_path is not None
            assert self._log_path is not None
            assert self._port is not None
            _write_json_atomic(
                lease_path,
                {
                    "password_sha256": hashlib.sha256(password.encode()).hexdigest(),
                    "policy_sha256": self.policy.digest,
                },
            )
            self._active_leases.add(token)
            run_log_path.write_text(
                json.dumps(
                    {
                        "status": "leased",
                        "lease_id": token,
                        "policy_sha256": self.policy.digest,
                        "start_attempts": self._start_attempts_used,
                        "supervisor_pid": self._process.pid,
                        "supervisor_log": str(self._log_path),
                    },
                    sort_keys=True,
                )
                + "\n"
            )
            handle = TlsEgressHandle(
                base_url=f"http://127.0.0.1:{self._port}",
                ca_cert_path=self._ca_cert_path,
                audit_path=final_audit_path,
                log_path=run_log_path,
                command=self._command,
                lease_id=token,
                supervisor_pid=self._process.pid,
                _proxy_auth=(token, password),
            )

        try:
            yield handle
        finally:
            with self._lock:
                lease_path.unlink(missing_ok=True)
                if temporary_audit_path.is_file():
                    shutil.copyfile(temporary_audit_path, final_audit_path)
                    temporary_audit_path.unlink()
                elif not final_audit_path.exists():
                    final_audit_path.write_text("")
                self._active_leases.discard(token)
                with run_log_path.open("a") as handle_log:
                    handle_log.write(
                        json.dumps(
                            {
                                "status": "released",
                                "lease_id": token,
                                "supervisor_pid": handle.supervisor_pid,
                            },
                            sort_keys=True,
                        )
                        + "\n"
                    )

    def close(self, *, force: bool = False) -> None:
        """Stop the shared proxy and remove its private state."""
        with self._lock:
            if self._closed:
                return
            if self._active_leases and not force:
                raise RuntimeError(
                    "cannot close TLS egress supervisor with active leases"
                )
            for lease_path in self._lease_dir.glob("*.json"):
                lease_path.unlink(missing_ok=True)
            if self._process is not None:
                _terminate_process(self._process)
            self._process = None
            self._closed = True
            shutil.rmtree(self._root, ignore_errors=True)


_SUPERVISOR_LOCK = threading.RLock()
_SUPERVISORS: dict[tuple[str, str, str], TlsEgressSupervisor] = {}


def _shared_supervisor(
    *,
    policy: SourcePolicy,
    mitmdump_executable: str | Path,
    addon_path: Path,
) -> TlsEgressSupervisor:
    executable = _resolve_executable(mitmdump_executable)
    resolved_addon = addon_path.resolve()
    key = (policy.digest, str(executable), str(resolved_addon))
    with _SUPERVISOR_LOCK:
        supervisor = _SUPERVISORS.get(key)
        if supervisor is None:
            supervisor = TlsEgressSupervisor(
                policy=policy,
                mitmdump_executable=executable,
                addon_path=resolved_addon,
            )
            _SUPERVISORS[key] = supervisor
        return supervisor


def shutdown_tls_egress_supervisors() -> None:
    """Stop all process-scoped TLS supervisors."""
    with _SUPERVISOR_LOCK:
        supervisors = list(_SUPERVISORS.values())
        _SUPERVISORS.clear()
    for supervisor in supervisors:
        supervisor.close(force=True)


atexit.register(shutdown_tls_egress_supervisors)


@contextlib.contextmanager
def _ephemeral_tls_egress_proxy(
    *,
    policy: SourcePolicy,
    run_dir: Path,
    mitmdump_executable: str | Path,
    addon_path: Path,
) -> Iterator[TlsEgressHandle]:
    """Compatibility path that starts one proxy and CA for one run."""
    executable = _resolve_executable(mitmdump_executable)
    if not addon_path.is_file():
        raise FileNotFoundError(f"TLS filter addon not found: {addon_path}")

    run_dir.mkdir(parents=True, exist_ok=True)
    final_audit_path = run_dir / TLS_EGRESS_AUDIT_FILENAME
    log_path = run_dir / TLS_EGRESS_LOG_FILENAME
    with tempfile.TemporaryDirectory(prefix="bioeval-tls-egress-", dir="/tmp") as tmp:
        tmp_dir = Path(tmp)
        conf_dir = tmp_dir / "mitmproxy"
        conf_dir.mkdir()
        policy_path = tmp_dir / "policy.json"
        temporary_audit_path = tmp_dir / TLS_EGRESS_AUDIT_FILENAME
        policy_path.write_text(json.dumps(policy.broker_payload()))
        port = _free_loopback_port()
        command = [
            str(executable),
            "--quiet",
            "--listen-host",
            "127.0.0.1",
            "--listen-port",
            str(port),
            "--set",
            f"confdir={conf_dir}",
            "--set",
            "connection_strategy=lazy",
            "--set",
            "block_global=false",
            "--scripts",
            str(addon_path),
        ]
        env = {
            "PATH": f"{executable.parent}:/usr/bin:/bin",
            "HOME": str(tmp_dir),
            "TMPDIR": str(tmp_dir),
            "LC_ALL": "C.UTF-8",
            "LANG": "C.UTF-8",
            "PYTHONPATH": str(REPO_ROOT / "src"),
            "BIOEVAL_TLS_POLICY": str(policy_path),
            "BIOEVAL_TLS_AUDIT": str(temporary_audit_path),
        }
        linker_path = os.environ.get("LD_LIBRARY_PATH")
        if linker_path:
            env["LD_LIBRARY_PATH"] = linker_path

        with log_path.open("w") as log_handle:
            process = subprocess.Popen(
                command,
                stdin=subprocess.DEVNULL,
                stdout=log_handle,
                stderr=subprocess.STDOUT,
                env=env,
                text=True,
            )
            try:
                ca_cert_path = conf_dir / "mitmproxy-ca-cert.pem"
                _wait_ready(
                    process=process,
                    port=port,
                    ca_cert_path=ca_cert_path,
                    log_path=log_path,
                )
                yield TlsEgressHandle(
                    base_url=f"http://127.0.0.1:{port}",
                    ca_cert_path=ca_cert_path,
                    audit_path=final_audit_path,
                    log_path=log_path,
                    command=tuple(command),
                )
            finally:
                _terminate_process(process)
                if temporary_audit_path.is_file():
                    shutil.copyfile(temporary_audit_path, final_audit_path)
                elif not final_audit_path.exists():
                    final_audit_path.write_text("")


@contextlib.contextmanager
def tls_egress_proxy(
    *,
    policy: SourcePolicy,
    run_dir: Path,
    mitmdump_executable: str | Path = DEFAULT_MITMDUMP_EXECUTABLE,
    addon_path: Path = DEFAULT_TLS_FILTER_ADDON,
    shared: bool | None = None,
) -> Iterator[TlsEgressHandle]:
    """Lease a process-scoped proxy, or start an explicit per-run fallback."""
    if not policy.enabled:
        raise ValueError("TLS egress proxy requires an enabled source policy")
    if shared is None:
        shared = os.environ.get(TLS_EGRESS_SHARED_ENV, "1").strip().lower() not in {
            "0",
            "false",
            "no",
        }
    if shared:
        supervisor = _shared_supervisor(
            policy=policy,
            mitmdump_executable=mitmdump_executable,
            addon_path=addon_path,
        )
        with supervisor.lease(run_dir=run_dir) as handle:
            yield handle
        return
    with _ephemeral_tls_egress_proxy(
        policy=policy,
        run_dir=run_dir,
        mitmdump_executable=mitmdump_executable,
        addon_path=addon_path,
    ) as handle:
        yield handle
