"""Enforce and audit a task's protected-source policy."""

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
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Iterator

from .policy import SourcePolicy

DEFAULT_FILTERED_SEARCH_TIMEOUT_S = 30.0
FILTERED_SEARCH_START_ATTEMPTS = 2
FILTERED_SEARCH_SHARED_ENV = "BIOEVAL_SHARED_FILTERED_SEARCH"
PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FILTERED_SEARCH_IMAGE = (
    PACKAGE_ROOT / "containers" / "bioeval-filtered-search.sif"
)


@dataclass(frozen=True)
class FilteredSearchHandle:
    mcp_url: str
    command: tuple[str, ...]
    policy_sha256: str
    image_path: Path
    image_sha256: str
    audit_path: Path
    log_path: Path
    lease_id: str | None = None
    supervisor_pid: int | None = None
    _live_audit_path: Path | None = field(default=None, repr=False, compare=False)
    _live_audit_offset: int = field(default=0, repr=False, compare=False)

    def snapshot_audit(self) -> Path:
        """Materialize this lease's broker audit while the lease is active."""
        source_path = self._live_audit_path
        if source_path is None or not source_path.is_file():
            if self.audit_path.is_file():
                return self.audit_path
            payload = b""
        else:
            with source_path.open("rb") as source:
                source.seek(self._live_audit_offset)
                payload = source.read()

        temp_path = self.audit_path.with_name(
            f".{self.audit_path.name}.{secrets.token_hex(8)}.tmp"
        )
        try:
            temp_path.write_bytes(payload)
            os.replace(temp_path, self.audit_path)
        finally:
            temp_path.unlink(missing_ok=True)
        return self.audit_path


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _free_local_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def filtered_codex_config(mcp_url: str) -> tuple[str, ...]:
    return (
        'approval_policy="never"',
        'web_search="disabled"',
        "tools.web_search=false",
        f'mcp_servers.bioeval_literature.url="{mcp_url}"',
        "mcp_servers.bioeval_literature.required=true",
        (
            "mcp_servers.bioeval_literature.enabled_tools="
            '["search_pubmed","fetch_pubmed"]'
        ),
        ('mcp_servers.bioeval_literature.default_tools_approval_mode="approve"'),
        "mcp_servers.bioeval_literature.startup_timeout_sec=30",
        "mcp_servers.bioeval_literature.tool_timeout_sec=60",
    )


def filtered_search_command(
    *,
    image: Path,
    runtime_dir: Path,
    port: int,
    apptainer_executable: str = "apptainer",
    ncbi_api_key_file: Path | None = None,
) -> list[str]:
    command = [
        apptainer_executable,
        "exec",
        "--containall",
        "--cleanenv",
        "--no-home",
        "--writable-tmpfs",
        "--pwd",
        "/",
        "--bind",
        f"{runtime_dir}:/run/bioeval:rw",
        str(image),
        "python3",
        "/opt/bioeval/filtered_search_server.py",
        "--host",
        "127.0.0.1",
        "--port",
        str(port),
        "--policy",
        "/run/bioeval/policy.json",
        "--audit-log",
        "/run/bioeval/search-audit.jsonl",
    ]
    if ncbi_api_key_file is not None:
        command.extend(["--ncbi-api-key-file", "/run/bioeval/ncbi-api-key"])
    return command


def _stage_ncbi_api_key(runtime_dir: Path, api_key: str | None) -> Path | None:
    """Stage a broker-only key file without exposing the secret in argv."""
    if api_key is None or not api_key.strip():
        return None
    path = runtime_dir / "ncbi-api-key"
    path.write_text(api_key.strip() + "\n", encoding="utf-8")
    path.chmod(0o600)
    return path


def _wait_ready(
    url: str,
    process: subprocess.Popen,
    log_path: Path,
    *,
    timeout_s: float = DEFAULT_FILTERED_SEARCH_TIMEOUT_S,
) -> None:
    deadline = time.monotonic() + timeout_s
    health = url.removesuffix("/mcp") + "/health"
    while time.monotonic() < deadline:
        if process.poll() is not None:
            tail = ""
            if log_path.exists():
                tail = log_path.read_text(errors="replace")[-2000:]
            raise RuntimeError(
                f"filtered-search SIF exited with {process.returncode}: {tail}"
            )
        try:
            with urllib.request.urlopen(health, timeout=1.0) as response:
                if response.status == 200:
                    return
        except (OSError, urllib.error.URLError):
            time.sleep(0.1)
    raise TimeoutError(f"filtered-search SIF did not become ready at {health}")


def _terminate_process(process: subprocess.Popen[object]) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


@dataclass
class _FilteredSearchWorker:
    process: subprocess.Popen[str]
    mcp_url: str
    command: tuple[str, ...]
    audit_path: Path
    log_path: Path
    runtime_dir: Path
    active: bool = False


class FilteredSearchSupervisor:
    """Reuse filtered-search SIF workers while keeping run audits separate."""

    def __init__(
        self,
        *,
        policy: SourcePolicy,
        image: Path,
        apptainer_executable: str = "apptainer",
        readiness_timeout_s: float = DEFAULT_FILTERED_SEARCH_TIMEOUT_S,
        start_attempts: int = FILTERED_SEARCH_START_ATTEMPTS,
        ncbi_api_key: str | None = None,
    ) -> None:
        if not policy.enabled:
            raise ValueError(
                "filtered-search supervisor requires an enabled source policy"
            )
        if start_attempts < 1:
            raise ValueError("start_attempts must be at least one")
        self.policy = policy
        self.image = image.expanduser().resolve()
        if not self.image.is_file():
            raise FileNotFoundError(
                f"filtered-search SIF not found: {self.image}; build it with "
                "`bioeval build-search-sif`"
            )
        resolved_apptainer = shutil.which(apptainer_executable)
        if resolved_apptainer is None:
            raise FileNotFoundError(f"{apptainer_executable} not found on PATH")
        self.apptainer_executable = resolved_apptainer
        self.image_sha256 = _file_sha256(self.image)
        self.readiness_timeout_s = readiness_timeout_s
        self.start_attempts = start_attempts
        self.ncbi_api_key = ncbi_api_key.strip() if ncbi_api_key else None
        self._root = Path(
            tempfile.mkdtemp(
                prefix=f"bioeval-filtered-{policy.digest[:12]}-",
                dir="/tmp",
            )
        )
        self._workers: list[_FilteredSearchWorker] = []
        self._closed = False
        self._condition = threading.Condition(threading.RLock())

    @property
    def worker_count(self) -> int:
        with self._condition:
            return sum(worker.process.poll() is None for worker in self._workers)

    @property
    def active_lease_count(self) -> int:
        with self._condition:
            return sum(worker.active for worker in self._workers)

    def _start_worker_locked(self) -> _FilteredSearchWorker:
        failures: list[str] = []
        for attempt in range(1, self.start_attempts + 1):
            runtime_dir = self._root / (
                f"worker-{len(self._workers) + 1}-attempt-{attempt}-"
                f"{secrets.token_hex(4)}"
            )
            runtime_dir.mkdir()
            (runtime_dir / "policy.json").write_text(
                json.dumps(self.policy.broker_payload(), indent=2) + "\n"
            )
            audit_path = runtime_dir / "search-audit.jsonl"
            log_path = runtime_dir / "filtered-search.log"
            api_key_file = _stage_ncbi_api_key(runtime_dir, self.ncbi_api_key)
            port = _free_local_port()
            command = filtered_search_command(
                image=self.image,
                runtime_dir=runtime_dir,
                port=port,
                apptainer_executable=self.apptainer_executable,
                ncbi_api_key_file=api_key_file,
            )
            mcp_url = f"http://127.0.0.1:{port}/mcp"
            with log_path.open("w") as log_handle:
                process = subprocess.Popen(
                    command,
                    cwd=self._root,
                    stdin=subprocess.DEVNULL,
                    stdout=log_handle,
                    stderr=subprocess.STDOUT,
                    text=True,
                )
            try:
                _wait_ready(
                    mcp_url,
                    process,
                    log_path,
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
            worker = _FilteredSearchWorker(
                process=process,
                mcp_url=mcp_url,
                command=tuple(command),
                audit_path=audit_path,
                log_path=log_path,
                runtime_dir=runtime_dir,
            )
            self._workers.append(worker)
            return worker
        raise RuntimeError(
            "filtered-search supervisor failed to start after "
            f"{self.start_attempts} attempts: {' | '.join(failures)}"
        )

    def _available_worker_locked(self) -> _FilteredSearchWorker:
        if self._closed:
            raise RuntimeError("filtered-search supervisor is closed")
        self._workers = [
            worker for worker in self._workers if worker.process.poll() is None
        ]
        for worker in self._workers:
            if not worker.active:
                return worker
        return self._start_worker_locked()

    @contextlib.contextmanager
    def lease(self, *, run_dir: Path) -> Iterator[FilteredSearchHandle]:
        run_dir.mkdir(parents=True, exist_ok=True)
        final_audit_path = run_dir / "filtered_search_audit.jsonl"
        run_log_path = run_dir / "filtered_search_proxy.log"
        lease_id = secrets.token_hex(24)
        with self._condition:
            worker = self._available_worker_locked()
            worker.active = True
            audit_offset = (
                worker.audit_path.stat().st_size if worker.audit_path.is_file() else 0
            )
            run_log_path.write_text(
                json.dumps(
                    {
                        "status": "leased",
                        "lease_id": lease_id,
                        "policy_sha256": self.policy.digest,
                        "supervisor_pid": worker.process.pid,
                        "supervisor_log": str(worker.log_path),
                    },
                    sort_keys=True,
                )
                + "\n"
            )
            handle = FilteredSearchHandle(
                mcp_url=worker.mcp_url,
                command=worker.command,
                policy_sha256=self.policy.digest,
                image_path=self.image,
                image_sha256=self.image_sha256,
                audit_path=final_audit_path,
                log_path=run_log_path,
                lease_id=lease_id,
                supervisor_pid=worker.process.pid,
                _live_audit_path=worker.audit_path,
                _live_audit_offset=audit_offset,
            )
        try:
            yield handle
        finally:
            with self._condition:
                if worker.audit_path.is_file():
                    with worker.audit_path.open("rb") as source:
                        source.seek(audit_offset)
                        final_audit_path.write_bytes(source.read())
                elif not final_audit_path.exists():
                    final_audit_path.write_text("")
                worker.active = False
                with run_log_path.open("a") as handle_log:
                    handle_log.write(
                        json.dumps(
                            {
                                "status": "released",
                                "lease_id": lease_id,
                                "supervisor_pid": worker.process.pid,
                            },
                            sort_keys=True,
                        )
                        + "\n"
                    )
                self._condition.notify_all()

    def close(self, *, force: bool = False) -> None:
        with self._condition:
            if self._closed:
                return
            active = [worker for worker in self._workers if worker.active]
            if active and not force:
                raise RuntimeError(
                    "cannot close filtered-search supervisor with active leases"
                )
            for worker in self._workers:
                _terminate_process(worker.process)
            self._workers.clear()
            self._closed = True
            shutil.rmtree(self._root, ignore_errors=True)


_SUPERVISOR_LOCK = threading.RLock()
_SUPERVISORS: dict[tuple[str, str, str, str], FilteredSearchSupervisor] = {}


def _shared_supervisor(
    *,
    policy: SourcePolicy,
    image: Path,
    apptainer_executable: str,
    ncbi_api_key: str | None,
) -> FilteredSearchSupervisor:
    resolved_image = image.expanduser().resolve()
    resolved_apptainer = shutil.which(apptainer_executable)
    if resolved_apptainer is None:
        raise FileNotFoundError(f"{apptainer_executable} not found on PATH")
    api_key_digest = (
        hashlib.sha256(ncbi_api_key.strip().encode()).hexdigest()
        if ncbi_api_key and ncbi_api_key.strip()
        else "none"
    )
    key = (
        policy.digest,
        str(resolved_image),
        resolved_apptainer,
        api_key_digest,
    )
    with _SUPERVISOR_LOCK:
        supervisor = _SUPERVISORS.get(key)
        if supervisor is None:
            supervisor = FilteredSearchSupervisor(
                policy=policy,
                image=resolved_image,
                apptainer_executable=resolved_apptainer,
                ncbi_api_key=ncbi_api_key,
            )
            _SUPERVISORS[key] = supervisor
        return supervisor


def shutdown_filtered_search_supervisors() -> None:
    """Stop every process-scoped filtered-search worker pool."""
    with _SUPERVISOR_LOCK:
        supervisors = list(_SUPERVISORS.values())
        _SUPERVISORS.clear()
    for supervisor in supervisors:
        supervisor.close(force=True)


atexit.register(shutdown_filtered_search_supervisors)


@contextlib.contextmanager
def _ephemeral_filtered_search_proxy(
    *,
    policy: SourcePolicy,
    image: Path,
    run_dir: Path,
    apptainer_executable: str,
    ncbi_api_key: str | None,
) -> Iterator[FilteredSearchHandle]:
    """Compatibility path that launches one filtered-search SIF per run."""
    image = image.expanduser().resolve()
    if not image.is_file():
        raise FileNotFoundError(
            f"filtered-search SIF not found: {image}; build it with "
            "`bioeval build-search-sif`"
        )
    if shutil.which(apptainer_executable) is None:
        raise FileNotFoundError(f"{apptainer_executable} not found on PATH")
    image_sha256 = _file_sha256(image)

    run_dir.mkdir(parents=True, exist_ok=True)
    log_path = run_dir / "filtered_search_proxy.log"
    final_audit = run_dir / "filtered_search_audit.jsonl"
    with tempfile.TemporaryDirectory(prefix="bioeval-filtered-search-") as tmp:
        runtime_dir = Path(tmp)
        (runtime_dir / "policy.json").write_text(
            json.dumps(policy.broker_payload(), indent=2) + "\n"
        )
        temp_audit = runtime_dir / "search-audit.jsonl"
        api_key_file = _stage_ncbi_api_key(runtime_dir, ncbi_api_key)
        port = _free_local_port()
        mcp_url = f"http://127.0.0.1:{port}/mcp"
        command = filtered_search_command(
            image=image,
            runtime_dir=runtime_dir,
            port=port,
            apptainer_executable=apptainer_executable,
            ncbi_api_key_file=api_key_file,
        )
        with log_path.open("w") as log_handle:
            process = subprocess.Popen(
                command,
                cwd=run_dir,
                stdin=subprocess.DEVNULL,
                stdout=log_handle,
                stderr=subprocess.STDOUT,
                text=True,
            )
            try:
                _wait_ready(mcp_url, process, log_path)
                yield FilteredSearchHandle(
                    mcp_url=mcp_url,
                    command=tuple(command),
                    policy_sha256=policy.digest,
                    image_path=image,
                    image_sha256=image_sha256,
                    audit_path=final_audit,
                    log_path=log_path,
                    _live_audit_path=temp_audit,
                )
            finally:
                _terminate_process(process)
        if temp_audit.exists():
            shutil.copyfile(temp_audit, final_audit)
        else:
            final_audit.write_text("")


@contextlib.contextmanager
def filtered_search_proxy(
    *,
    policy: SourcePolicy,
    image: Path,
    run_dir: Path,
    apptainer_executable: str = "apptainer",
    shared: bool | None = None,
    ncbi_api_key: str | None = None,
) -> Iterator[FilteredSearchHandle]:
    if not policy.enabled:
        raise ValueError("filtered_search_proxy requires an enabled source policy")
    if shared is None:
        shared = os.environ.get(
            FILTERED_SEARCH_SHARED_ENV,
            "1",
        ).strip().lower() not in {"0", "false", "no"}
    if shared:
        supervisor = _shared_supervisor(
            policy=policy,
            image=image,
            apptainer_executable=apptainer_executable,
            ncbi_api_key=ncbi_api_key,
        )
        with supervisor.lease(run_dir=run_dir) as handle:
            yield handle
        return
    with _ephemeral_filtered_search_proxy(
        policy=policy,
        image=image,
        run_dir=run_dir,
        apptainer_executable=apptainer_executable,
        ncbi_api_key=ncbi_api_key,
    ) as handle:
        yield handle


def audit_protected_run(
    *,
    run_dir: Path,
    output_paths: Iterable[Path],
    policy: SourcePolicy,
    broker: FilteredSearchHandle | None = None,
    tls_audit_path: Path | None = None,
) -> dict:
    violations: list[dict] = []
    scanned: list[str] = []

    text_paths = [*output_paths, run_dir / "last_message.txt"]
    for path in dict.fromkeys(text_paths):
        if not path.is_file():
            continue
        scanned.append(str(path))
        pattern_hashes = policy.matches(path.read_text(errors="replace"))
        if pattern_hashes:
            violations.append(
                {
                    "kind": "forbidden_identifier_in_output",
                    "path": str(path),
                    "pattern_hashes": pattern_hashes,
                }
            )

    combined_events_path = run_dir / "events.jsonl"
    events_paths = (
        [combined_events_path]
        if combined_events_path.is_file()
        else sorted(run_dir.glob("events.segment-*.jsonl"))
    )
    for events_path in events_paths:
        scanned.append(str(events_path))
        for line_number, line in enumerate(
            events_path.read_text(errors="replace").splitlines(), start=1
        ):
            pattern_hashes = policy.matches(line)
            if pattern_hashes:
                violations.append(
                    {
                        "kind": "forbidden_identifier_in_event",
                        "path": str(events_path),
                        "line": line_number,
                        "pattern_hashes": pattern_hashes,
                    }
                )
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            item = event.get("item") if isinstance(event, dict) else None
            if not isinstance(item, dict):
                continue
            item_type = item.get("type")
            if item_type == "web_search":
                violations.append(
                    {
                        "kind": "hosted_web_search_used",
                        "path": str(events_path),
                        "line": line_number,
                    }
                )

    broker_audit = run_dir / "filtered_search_audit.jsonl"
    broker_counts = {"allowed": 0, "denied": 0, "upstream_errors": 0}
    if broker_audit.is_file():
        scanned.append(str(broker_audit))
        for line in broker_audit.read_text(errors="replace").splitlines():
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            decision = str(record.get("decision") or "")
            if decision == "allow":
                broker_counts["allowed"] += 1
            elif decision.startswith("deny"):
                broker_counts["denied"] += 1
            elif decision == "upstream_error":
                broker_counts["upstream_errors"] += 1

    tls_counts = {"allowed": 0, "denied": 0, "upstream_errors": 0}
    if tls_audit_path is not None and tls_audit_path.is_file():
        scanned.append(str(tls_audit_path))
        for line in tls_audit_path.read_text(errors="replace").splitlines():
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            decision = str(record.get("decision") or "")
            if decision == "allow":
                tls_counts["allowed"] += 1
            elif decision.startswith("deny"):
                tls_counts["denied"] += 1
            elif decision == "upstream_error":
                tls_counts["upstream_errors"] += 1

    if not policy.literature_access and any(broker_counts.values()):
        violations.append(
            {
                "kind": "literature_access_used_in_disabled_arm",
                "broker_requests": broker_counts,
            }
        )

    result = {
        "status": "passed" if not violations else "failed",
        "mode": policy.mode,
        "literature_access": policy.literature_access,
        "policy_sha256": policy.digest,
        "broker": (
            {
                "image": str(broker.image_path),
                "image_sha256": broker.image_sha256,
            }
            if broker is not None
            else None
        ),
        "scanned_paths": scanned,
        "broker_requests": broker_counts,
        "tls_egress_requests": tls_counts,
        "violations": violations,
    }
    (run_dir / "source_policy_audit.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    return result
