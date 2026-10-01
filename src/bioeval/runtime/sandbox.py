"""Hardened allowlist sandbox for BioEval framework runs (HPC-native).

The eval fairness model is an *allowlist*, not a blocklist: mount ONLY what a
task legitimately needs (OS toolchain trees + declared inputs), give the agent a
tmpfs ``$HOME`` and ``/tmp``, and hand it a minimal scrubbed environment.
Everything else — held-out ground truth, graders, references, other runs,
``~/.claude`` auto-memory + config + MCP, ``~/.codex``, host env hints — is
simply absent, not enumerated-and-masked. A blocklist can never be proven
complete; an allowlist can.

Two backends share one ``allow_ro``/``allow_rw`` interface:
  * bwrap  — works with the installed bubblewrap 0.4.1 (no ``--clearenv``; the
             parent supplies the scrubbed env dict instead).
  * apptainer — reproducible path for a pinned ``.sif`` image
             (``--containall --cleanenv --no-home``), the HPC-native analogue of
             a Docker-based eval sandbox.

The command builders are side-effect free.  The Unix-socket bridge context
manager near the bottom starts only a local ``socat`` relay; it never opens a
remote connection itself.
"""

from __future__ import annotations

import contextlib
import os
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence
from urllib.parse import urlparse

# Read-only OS trees needed for a from-scratch mount to run interpreters and
# common toolchains. Extend per framework (e.g. a conda/pixi prefix) via
# ``allow_ro``.
DEFAULT_OS_ROOTS: tuple[str, ...] = (
    "/usr",
    "/bin",
    "/sbin",
    "/lib",
    "/lib64",
    "/etc",
    "/opt",
)

FAKE_HOME = "/sandbox-home"
MODEL_GATE_DIR = f"{FAKE_HOME}/.bioeval-model-gate"
MODEL_GATE_SOCKET = f"{MODEL_GATE_DIR}/proxy.sock"
MODEL_GATE_PORT = 43191
LITERATURE_GATE_DIR = f"{FAKE_HOME}/.bioeval-literature-gate"
LITERATURE_GATE_SOCKET = f"{LITERATURE_GATE_DIR}/proxy.sock"
LITERATURE_GATE_PORT = 43192
TLS_EGRESS_GATE_DIR = f"{FAKE_HOME}/.bioeval-tls-egress-gate"
TLS_EGRESS_GATE_SOCKET = f"{TLS_EGRESS_GATE_DIR}/proxy.sock"
TLS_EGRESS_GATE_CA_CERT = f"{TLS_EGRESS_GATE_DIR}/mitmproxy-ca-cert.pem"
TLS_EGRESS_GATE_PORT = 43193
BIOKG_GATE_DIR = f"{FAKE_HOME}/.bioeval-biokg-gate"
BIOKG_GATE_SOCKET = f"{BIOKG_GATE_DIR}/proxy.sock"
BIOKG_GATE_PORT = 43194


def clean_env(
    *,
    fake_home: str = FAKE_HOME,
    passthrough_keys: Iterable[str] = (),
    extra: dict[str, str] | None = None,
) -> dict[str, str]:
    """Minimal scrubbed environment for a sandboxed run.

    Starts from nothing (no host env hints, no stray secrets), sets a neutral
    locale + PATH + tmpfs HOME, then copies ONLY the explicitly named
    ``passthrough_keys`` (e.g. the one API key the run must bill to) from the
    real environment. ``extra`` overrides/adds literal values last.
    """
    env = {
        "PATH": "/usr/bin:/bin",
        "HOME": fake_home,
        "TMPDIR": "/tmp",
        "LC_ALL": "C.UTF-8",
        "LANG": "C.UTF-8",
    }
    for key in passthrough_keys:
        val = os.environ.get(key)
        if val is not None:
            env[key] = val
    if extra:
        env.update(extra)
    return env


def bwrap_allowlist_command(
    inner_cmd: Sequence[str],
    *,
    chdir: str = FAKE_HOME,
    allow_ro: Iterable[Path] = (),
    allow_rw: Iterable[Path] = (),
    os_roots: Iterable[str] = DEFAULT_OS_ROOTS,
    share_net: bool = True,
    fake_home: str = FAKE_HOME,
    path: str = "/usr/bin:/bin",
    extra_binds: Iterable[tuple[str, str, bool]] = (),
    bwrap_executable: str = "bwrap",
) -> list[str]:
    """Build an allowlist bwrap argv.

    Only ``os_roots`` (read-only), ``allow_ro`` (read-only inputs), and
    ``allow_rw`` (the run's own writable out-dir) are visible; ``$HOME`` and
    ``/tmp`` are fresh tmpfs. Pair with :func:`clean_env` for the env. ``path``
    is the sandbox ``PATH`` — include a toolchain's bin dir when its launcher is
    not under ``/usr/bin``. ``extra_binds`` are ``(src, dest, read_only)`` triples
    bound at an explicit ``dest`` (e.g. a single credential file placed into the
    tmpfs HOME) — bwrap creates the tmpfs parent dirs as needed.
    """
    if shutil.which(bwrap_executable) is None:
        raise RuntimeError(
            f"{bwrap_executable} not found on PATH; install bubblewrap or run "
            "with the fairness sandbox disabled (this drops eval isolation)."
        )
    args = [bwrap_executable, "--unshare-all"]
    if share_net:
        args.append("--share-net")
    args += [
        "--dev",
        "/dev",
        "--proc",
        "/proc",
        "--tmpfs",
        "/tmp",
        "--tmpfs",
        fake_home,
        "--die-with-parent",
    ]
    for root in os_roots:
        if Path(root).exists():
            args += ["--ro-bind", root, root]
    # Bind each path at its LITERAL (absolutised, not symlink-resolved) location:
    # bwrap resolves the source to the real inode, but the mountpoint keeps the
    # name the prompt/agent uses — so a literal path through a symlinked parent
    # (e.g. the jin_lab -> group data alias) resolves inside the sandbox. Dedup
    # by destination so aliases that canonicalise together aren't bound twice.
    seen: set[str] = set()
    for p in allow_ro:
        dest = str(Path(p).absolute())
        if dest in seen or not Path(dest).exists():
            continue
        seen.add(dest)
        args += ["--ro-bind", dest, dest]
    for p in allow_rw:
        rp = Path(p).absolute()
        if str(rp) in seen:
            continue
        seen.add(str(rp))
        rp.mkdir(parents=True, exist_ok=True)
        args += ["--bind", str(rp), str(rp)]
    for src, dest, ro in extra_binds:
        if Path(src).exists():
            args += ["--ro-bind", src, dest] if ro else ["--bind", src, dest]
    args += [
        "--setenv",
        "HOME",
        fake_home,
        "--setenv",
        "PATH",
        path,
        "--chdir",
        chdir,
        "--",
    ]
    args += list(inner_cmd)
    return args


@dataclass(frozen=True)
class UnixSocketBridge:
    """Host-side half of a networkless sandbox's HTTP gateway tunnel."""

    host_dir: Path
    host_socket: Path
    target_host: str
    target_port: int
    command: tuple[str, ...]


@contextlib.contextmanager
def unix_socket_tcp_bridge(
    target_base_url: str,
    *,
    log_path: Path,
    socat_executable: str = "socat",
) -> Iterable[UnixSocketBridge]:
    """Relay a private Unix socket to a loopback-only HTTP gateway.

    The peer inside the sandbox has no network interface except loopback.  A
    second ``socat`` process (started by ``model_proxy_bridge.py`` inside that
    namespace) maps loopback TCP to this Unix socket.  Consequently the agent
    can reach the explicitly mounted local gateways but cannot make direct
    outbound connections or bypass them by clearing environment variables.
    """
    parsed = urlparse(target_base_url)
    host = parsed.hostname or ""
    if parsed.scheme != "http" or host not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError(
            f"gateway target must be loopback HTTP, got {target_base_url!r}"
        )
    if parsed.port is None:
        raise ValueError(f"gateway target has no explicit port: {target_base_url!r}")
    if shutil.which(socat_executable) is None:
        raise RuntimeError(f"{socat_executable} not found on PATH")

    log_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="bioeval-gateway-", dir="/tmp") as tmp:
        host_dir = Path(tmp)
        host_socket = host_dir / "proxy.sock"
        command = [
            socat_executable,
            f"UNIX-LISTEN:{host_socket},fork,mode=600",
            f"TCP:{host}:{parsed.port}",
        ]
        with log_path.open("w") as log_handle:
            process = subprocess.Popen(
                command,
                stdin=subprocess.DEVNULL,
                stdout=log_handle,
                stderr=subprocess.STDOUT,
                text=True,
            )
            try:
                deadline = time.monotonic() + 10
                while not host_socket.exists():
                    if process.poll() is not None:
                        tail = log_path.read_text(errors="replace")[-2000:]
                        raise RuntimeError(
                            f"gateway relay exited with {process.returncode}: {tail}"
                        )
                    if time.monotonic() >= deadline:
                        raise TimeoutError(
                            f"gateway relay did not create {host_socket}"
                        )
                    time.sleep(0.05)
                yield UnixSocketBridge(
                    host_dir=host_dir,
                    host_socket=host_socket,
                    target_host=host,
                    target_port=parsed.port,
                    command=tuple(command),
                )
            finally:
                if process.poll() is None:
                    process.terminate()
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait(timeout=5)


def codex_toolchain_paths(codex_executable: str = "codex") -> list[Path]:
    """Read-only paths to mount so the ``codex`` binary runs in the sandbox.

    Codex ships as a self-contained binary under ``~/.codex/packages/.../bin``;
    mount the launcher's bin dir and the release dir (binary + siblings). We do
    NOT mount the rest of ``~/.codex`` (auth.json, memories, history, sessions) —
    the tmpfs ``$HOME`` already denies those, closing codex's own cross-session
    memory leak the same way it closes Claude's auto-memory.
    """
    which = shutil.which(codex_executable)
    if which is None:
        return []
    launcher = Path(which)
    real = launcher.resolve()
    paths = [launcher.parent]
    # real = ~/.codex/packages/.../releases/<v>/bin/codex; parents[1] = release dir
    if len(real.parents) > 1:
        paths.append(real.parents[1])
    return paths


def claude_toolchain_paths(claude_executable: str = "claude") -> list[Path]:
    """Read-only paths to mount so the ``claude`` launcher runs in the sandbox.

    Resolved at runtime (not hardcoded) so version bumps under
    ``~/.local/share/claude/versions/<v>`` are picked up automatically: mount the
    launcher's bin dir and the versions parent (``.../share/claude``).
    """
    which = shutil.which(claude_executable)
    if which is None:
        return []
    launcher = Path(which)
    real = launcher.resolve()
    paths = [launcher.parent]
    # real = .../share/claude/versions/<v>; parents[1] = .../share/claude
    if len(real.parents) > 1:
        paths.append(real.parents[1])
    return paths
