"""Sandboxed shell executor shared by direct API-backed agents."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import venv
from collections.abc import Callable, Iterable
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import sandbox
from .paths import user_cache_dir


SANDBOX_ROOT = Path(
    os.environ.get("DISTRIBUTED_AGENTS_SANDBOX_ROOT", user_cache_dir() / "shell-sandbox")
).resolve()
SANDBOX_VENV = SANDBOX_ROOT / "venv"
SANDBOX_BOOTSTRAP_PACKAGES = (
    "pyarrow",
    "duckdb",
    "polars",
    "pandas",
    "numpy",
    "scipy",
    "requests",
    "httpx",
)
SANDBOX_BOOTSTRAP_MARKER = SANDBOX_VENV / ".bootstrap-packages.json"
_SHELL_ENV_PREFIXES = ("DISTRIBUTED_AGENTS_", "BIOKG_")
_SHELL_ENV_KEYS = {
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "http_proxy",
    "https_proxy",
    "NO_PROXY",
    "no_proxy",
    "SSL_CERT_FILE",
    "REQUESTS_CA_BUNDLE",
    "CURL_CA_BUNDLE",
}


def _sandbox_disabled() -> bool:
    return os.environ.get("DISTRIBUTED_AGENTS_SANDBOX", "1").lower() in (
        "0",
        "false",
        "no",
        "off",
    )


def ensure_sandbox_venv() -> Path:
    """Create or update the isolated shell environment used by API agents."""

    python = SANDBOX_VENV / "bin" / "python"
    wanted = sorted(SANDBOX_BOOTSTRAP_PACKAGES)
    if python.exists():
        try:
            installed = json.loads(SANDBOX_BOOTSTRAP_MARKER.read_text())
        except (OSError, ValueError):
            installed = []
        missing = [package for package in wanted if package not in installed]
        if missing:
            pip = SANDBOX_VENV / "bin" / "pip"
            print(
                f"[distributed_agents] installing sandbox packages: {missing}",
                file=sys.stderr,
            )
            subprocess.run([str(pip), "install", *missing], check=True)
            SANDBOX_BOOTSTRAP_MARKER.write_text(json.dumps(wanted))
        return SANDBOX_VENV
    if shutil.which("bwrap") is None:
        raise RuntimeError(
            "bwrap not found on PATH; install bubblewrap or run with "
            "DISTRIBUTED_AGENTS_SANDBOX=0"
        )
    SANDBOX_ROOT.mkdir(parents=True, exist_ok=True)
    print(f"[distributed_agents] creating sandbox venv at {SANDBOX_VENV}", file=sys.stderr)
    venv.EnvBuilder(with_pip=True, symlinks=True, clear=False).create(SANDBOX_VENV)
    pip = SANDBOX_VENV / "bin" / "pip"
    subprocess.run([str(pip), "install", "--upgrade", "pip"], check=True)
    subprocess.run([str(pip), "install", *SANDBOX_BOOTSTRAP_PACKAGES], check=True)
    SANDBOX_BOOTSTRAP_MARKER.write_text(json.dumps(wanted))
    print("[distributed_agents] sandbox venv ready", file=sys.stderr)
    return SANDBOX_VENV


def _bwrap_command(
    command: str,
    *,
    writable_dir: Path | None = None,
    readable_roots: Iterable[Path] = (),
) -> list[str]:
    ensure_sandbox_venv()
    writable = writable_dir.expanduser().resolve() if writable_dir else None
    if writable is not None:
        writable.mkdir(parents=True, exist_ok=True)
    extra_binds: list[tuple[str, str, bool]] = []
    empty_mask = SANDBOX_ROOT / ".empty_mask"
    for hidden in filter(None, os.environ.get("DISTRIBUTED_AGENTS_SANDBOX_HIDE", "").split(":")):
        if os.path.isfile(hidden):
            empty_mask.parent.mkdir(parents=True, exist_ok=True)
            empty_mask.touch(exist_ok=True)
            extra_binds.append((str(empty_mask), hidden, True))
    inner_env = {
        "VIRTUAL_ENV": str(SANDBOX_VENV),
        "TMPDIR": "/tmp",
    }
    for key, value in sorted(os.environ.items()):
        if key in _SHELL_ENV_KEYS or key.startswith(_SHELL_ENV_PREFIXES):
            inner_env[key] = value
    return sandbox.bwrap_allowlist_command(
        ["/bin/sh", "-c", command],
        chdir=str(writable or Path("/tmp")),
        allow_ro=(SANDBOX_VENV, *readable_roots),
        allow_rw=(writable,) if writable is not None else (),
        path=f"{SANDBOX_VENV}/bin:/usr/bin:/bin",
        extra_binds=extra_binds,
        setenv=inner_env,
    )


def _append_tool_log(
    command: str,
    stdout: str,
    stderr: str,
    outcome: str,
    exit_code: int | None = None,
    *,
    path: str | None = None,
) -> None:
    path = path or os.environ.get("DISTRIBUTED_AGENTS_TOOLLOG")
    if not path or path.lower() in ("0", "false", "off"):
        return
    try:
        record = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "command": command,
            "outcome": outcome,
            "exit_code": exit_code,
            "stdout_head": (stdout or "")[:4000],
            "stderr_head": (stderr or "")[:2000],
        }
        with open(path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(record) + "\n")
    except Exception:
        pass


def execute_shell_commands(
    commands: list[str],
    timeout: float | None,
    max_output_length: Any,
    *,
    cwd: str | None = None,
    tool_log_path: str | None = None,
    readable_roots: Iterable[Path] = (),
    writable_dir: Path | None = None,
) -> Any:
    """Run a batch of shell commands through the configured sandbox."""

    from agents.tool import ShellCallOutcome, ShellCommandOutput, ShellResult

    sandboxed = not _sandbox_disabled()
    outputs: list[ShellCommandOutput] = []
    for command in commands:
        if sandboxed:
            effective_writable = (
                Path(cwd).expanduser().resolve()
                if cwd
                else writable_dir
                or (
                    Path(os.environ["DISTRIBUTED_AGENTS_OUTPUT_DIR"]).expanduser().resolve()
                    if os.environ.get("DISTRIBUTED_AGENTS_OUTPUT_DIR")
                    else None
                )
            )
            popen_args: str | list[str] = _bwrap_command(
                command,
                writable_dir=effective_writable,
                readable_roots=readable_roots,
            )
            popen_shell = False
            popen_env: dict[str, str] | None = {"PATH": "/usr/bin:/bin"}
            run_cwd: str | None = None
        else:
            popen_args = command
            popen_shell = True
            popen_env = None
            run_cwd = cwd or (str(writable_dir) if writable_dir else None)
        try:
            process = subprocess.run(
                popen_args,
                shell=popen_shell,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=popen_env,
                cwd=run_cwd,
            )
            outputs.append(
                ShellCommandOutput(
                    stdout=process.stdout,
                    stderr=process.stderr,
                    outcome=ShellCallOutcome(
                        type="exit",
                        exit_code=process.returncode,
                    ),
                    command=command,
                )
            )
            _append_tool_log(
                command,
                process.stdout,
                process.stderr,
                "exit",
                process.returncode,
                path=tool_log_path,
            )
        except subprocess.TimeoutExpired as exc:
            stdout = (
                exc.stdout.decode()
                if isinstance(exc.stdout, bytes)
                else (exc.stdout or "")
            )
            stderr = (
                exc.stderr.decode()
                if isinstance(exc.stderr, bytes)
                else (exc.stderr or "")
            )
            outputs.append(
                ShellCommandOutput(
                    stdout=stdout,
                    stderr=stderr,
                    outcome=ShellCallOutcome(type="timeout"),
                    command=command,
                )
            )
            _append_tool_log(
                command,
                stdout,
                stderr,
                "timeout",
                path=tool_log_path,
            )
    return ShellResult(output=outputs, max_output_length=max_output_length)


def make_local_shell_executor(
    *,
    readable_roots: Iterable[Path] = (),
    writable_dir: Path | None = None,
) -> Callable[[Any], Any]:
    """Bind an Agents SDK shell executor to explicit filesystem roots."""

    roots = tuple(Path(path).expanduser().resolve() for path in readable_roots)
    writable = writable_dir.expanduser().resolve() if writable_dir else None

    def execute(request: Any) -> Any:
        action = request.data.action
        timeout = (action.timeout_ms / 1000.0) if action.timeout_ms else None
        return execute_shell_commands(
            list(action.commands),
            timeout,
            action.max_output_length,
            readable_roots=roots,
            writable_dir=writable,
        )

    return execute
