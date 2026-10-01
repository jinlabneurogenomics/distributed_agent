"""DistributedAgents-owned mechanics for launching and observing Codex.

This module deliberately contains no evaluation policy.  It builds a normal
Codex command, stages the minimum ChatGPT authentication state, executes the
process, and parses raw token usage.  Callers such as BioEval may inject an
alternate ``codex`` executable or config overrides to provide an external
sandbox, filtered services, or other policy without becoming a DistributedAgents
runtime dependency.
"""

from __future__ import annotations

import json
import os
import shutil
import signal
import subprocess
import sys
import threading
from pathlib import Path
from typing import Iterable

from . import sandbox as sandbox_runtime


CODEX_CHATGPT_CACHE_FILES = (
    "cloud-config-bundle-cache.json",
    "cloud-requirements-cache.json",
    "models_cache.json",
    "installation_id",
)


def codex_command(
    run_dir: Path,
    *,
    model: str,
    sandbox: str,
    codex_executable: str,
    auth: str,
    config_overrides: Iterable[str] = (),
    ephemeral: bool = False,
    strict_config: bool = True,
    ignore_rules: bool = True,
    network_access: bool = True,
    resume_session_id: str | None = None,
    last_message_path: Path | None = None,
) -> list[str]:
    """Build the ordinary Codex CLI command for one DistributedAgents turn."""

    if resume_session_id:
        cmd = [
            codex_executable,
            "exec",
            "resume",
            "--json",
            "--skip-git-repo-check",
        ]
    else:
        cmd = [
            codex_executable,
            "exec",
            "--json",
            "--skip-git-repo-check",
            "--cd",
            str(run_dir),
        ]
    if ephemeral:
        cmd.append("--ephemeral")
    if strict_config:
        cmd.append("--strict-config")
    if ignore_rules:
        cmd.append("--ignore-rules")
    if sandbox == "workspace-write":
        value = "true" if network_access else "false"
        cmd.extend(["--config", f"sandbox_workspace_write.network_access={value}"])
    if auth == "apikey":
        cmd.extend(
            [
                "--config",
                "model_providers.oaikey.name=openai-apikey",
                "--config",
                "model_providers.oaikey.base_url=https://api.openai.com/v1",
                "--config",
                "model_providers.oaikey.env_key=OPENAI_API_KEY",
                "--config",
                "model_providers.oaikey.wire_api=responses",
                "--config",
                "model_provider=oaikey",
            ]
        )
    for override in config_overrides:
        cmd.extend(["--config", override])
    if model:
        cmd.extend(["--model", model])
    if sandbox and not resume_session_id:
        cmd.extend(["--sandbox", sandbox])
    elif sandbox and resume_session_id:
        cmd.extend(["--config", f"sandbox_mode={json.dumps(sandbox)}"])
    message_path = last_message_path or (run_dir / "last_message.txt")
    cmd.extend(["--output-last-message", str(message_path)])
    if resume_session_id:
        cmd.extend([resume_session_id, "-"])
    else:
        cmd.append("-")
    return cmd


def codex_run_command(
    run_dir: Path,
    *,
    model: str,
    sandbox: str,
    codex_executable: str,
    auth: str,
    bwrap: bool,
    input_roots: Iterable[Path] = (),
    config_overrides: Iterable[str] = (),
    ephemeral: bool = False,
    strict_config: bool = True,
    ignore_rules: bool = True,
    sandbox_binds: Iterable[tuple[str, str, bool]] = (),
    network_access: bool = True,
    resume_session_id: str | None = None,
) -> list[str]:
    """Build a Codex command with DistributedAgents' baseline allowlist enclosure."""

    executable = codex_executable
    if bwrap:
        which = shutil.which(codex_executable)
        executable = str(Path(which).resolve()) if which else codex_executable
    cmd = codex_command(
        run_dir,
        model=model,
        sandbox=sandbox,
        codex_executable=executable,
        auth=auth,
        config_overrides=config_overrides,
        ephemeral=ephemeral,
        strict_config=strict_config,
        ignore_rules=ignore_rules,
        network_access=network_access,
        resume_session_id=resume_session_id,
    )
    if not bwrap:
        return cmd
    toolchain = sandbox_runtime.codex_toolchain_paths(codex_executable)
    bin_dir = str(toolchain[0]) if toolchain else None
    python_bin = Path(sys.executable).resolve().parent
    path_parts = [str(python_bin)] + ([bin_dir] if bin_dir else []) + [
        "/usr/bin",
        "/bin",
    ]
    return sandbox_runtime.bwrap_allowlist_command(
        cmd,
        chdir=str(run_dir),
        allow_ro=[Path(sys.prefix), *input_roots, *toolchain],
        allow_rw=[run_dir],
        path=":".join(path_parts),
        extra_binds=sandbox_binds,
    )


def stage_chatgpt_codex_state(
    destination: Path,
    *,
    source: Path | None = None,
) -> tuple[Path, ...]:
    """Copy only authentication and control-plane caches into a run-local home."""

    source = source or (Path.home() / ".codex")
    auth_source = source / "auth.json"
    if not auth_source.is_file():
        raise FileNotFoundError("ChatGPT Codex auth not found; run `codex login` first")
    destination.mkdir(parents=True, exist_ok=True)
    copied: list[Path] = []
    for name in ("auth.json", *CODEX_CHATGPT_CACHE_FILES):
        source_path = source / name
        if not source_path.is_file():
            continue
        destination_path = destination / name
        shutil.copy2(source_path, destination_path)
        copied.append(destination_path)
    (destination / "auth.json").chmod(0o600)
    return tuple(copied)


def codex_env(
    *,
    auth: str,
    cwd: Path,
    fairness_sandbox: bool = True,
    extra: dict[str, str] | None = None,
) -> dict[str, str]:
    """Return a scrubbed sandbox env or the inherited external-runner env."""

    key = os.environ.get("OPENAI_API_KEY")
    if auth == "apikey" and not key:
        from dotenv import dotenv_values

        env_path = cwd / ".env"
        if env_path.exists():
            key = dotenv_values(env_path).get("OPENAI_API_KEY")
    if fairness_sandbox:
        clean_extra = dict(extra or {})
        if auth == "apikey" and key:
            clean_extra["OPENAI_API_KEY"] = str(key)
        env = sandbox_runtime.clean_env(extra=clean_extra)
    else:
        env = os.environ.copy()
        if extra:
            env.update(extra)
        if auth == "apikey" and key:
            env["OPENAI_API_KEY"] = str(key)
    if auth == "chatgpt":
        env.pop("OPENAI_API_KEY", None)
    return env


def parse_codex_usage(events_path: Path) -> dict[str, int] | None:
    """Aggregate raw token counts from a Codex JSONL event stream."""

    try:
        text = events_path.read_text()
    except OSError:
        return None
    input_tokens = cached_tokens = output_tokens = reasoning_tokens = 0
    turns = 0
    for line in text.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict) or event.get("type") != "turn.completed":
            continue
        usage = event.get("usage") or {}
        input_tokens += int(usage.get("input_tokens", 0) or 0)
        cached_tokens += int(usage.get("cached_input_tokens", 0) or 0)
        output_tokens += int(usage.get("output_tokens", 0) or 0)
        reasoning_tokens += int(usage.get("reasoning_output_tokens", 0) or 0)
        turns += 1
    if turns == 0:
        return None
    return {
        "total_tokens": input_tokens + output_tokens,
        "requests": turns,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cache_read_input_tokens": cached_tokens,
        "reasoning_output_tokens": reasoning_tokens,
    }


def run_subprocess_with_log(
    cmd: list[str],
    *,
    log_path: Path,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    stdin_path: Path | None = None,
    stdout_path: Path | None = None,
    timeout_seconds: float | None = None,
) -> int:
    """Run a process while mirroring combined output to a log and JSONL file."""

    log_path.parent.mkdir(parents=True, exist_ok=True)
    if stdout_path is not None:
        stdout_path.parent.mkdir(parents=True, exist_ok=True)
    stdin_file = stdin_path.open() if stdin_path is not None else None
    stdout_file = stdout_path.open("w") if stdout_path is not None else None
    timer: threading.Timer | None = None
    kill_timer: threading.Timer | None = None
    timed_out = False
    try:
        with log_path.open("w") as log:
            log.write("$ " + " ".join(cmd) + "\n")
            if stdin_path is not None:
                log.write(f"# stdin: {stdin_path}\n")
            if stdout_path is not None:
                log.write(f"# stdout mirror: {stdout_path}\n")
            log.write("\n")
            log.flush()
            process = subprocess.Popen(
                cmd,
                cwd=str(cwd) if cwd else None,
                env=env,
                stdin=stdin_file,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                start_new_session=bool(timeout_seconds),
            )
            if timeout_seconds:

                def terminate_on_timeout() -> None:
                    nonlocal kill_timer, timed_out
                    timed_out = True
                    try:
                        os.killpg(process.pid, signal.SIGTERM)
                    except (ProcessLookupError, PermissionError):
                        try:
                            process.terminate()
                        except ProcessLookupError:
                            pass

                    def kill_after_grace() -> None:
                        try:
                            os.killpg(process.pid, signal.SIGKILL)
                        except (ProcessLookupError, PermissionError):
                            try:
                                process.kill()
                            except ProcessLookupError:
                                pass

                    kill_timer = threading.Timer(5.0, kill_after_grace)
                    kill_timer.daemon = True
                    kill_timer.start()

                timer = threading.Timer(timeout_seconds, terminate_on_timeout)
                timer.daemon = True
                timer.start()
            assert process.stdout is not None
            for line in process.stdout:
                sys.stdout.write(line)
                sys.stdout.flush()
                log.write(line)
                log.flush()
                if stdout_file is not None:
                    stdout_file.write(line)
                    stdout_file.flush()
            returncode = process.wait()
            return 124 if timed_out else returncode
    finally:
        if timer is not None:
            timer.cancel()
        if kill_timer is not None:
            kill_timer.cancel()
        if stdin_file is not None:
            stdin_file.close()
        if stdout_file is not None:
            stdout_file.close()
