"""Shared command execution, environment, and proxy helpers."""

from __future__ import annotations

import contextlib
import os
import signal
import subprocess
import sys
import threading
from pathlib import Path
from typing import TYPE_CHECKING, Iterable

from ..models import FrameworkPrompt
from ..runtime import sandbox
from ..runtime.paths import REPO_ROOT

if TYPE_CHECKING:
    from ..accounting import ProxyHandle

DEFAULT_INPUT_ROOTS = (
    REPO_ROOT / "data",
    Path("/gpfs/home/asun/jin_lab/distributed_agents/data"),
)
ANALYSIS_ENV = REPO_ROOT / ".pixi" / "envs" / "default"
ANALYSIS_ENV_BIN = ANALYSIS_ENV / "bin"
DEFAULT_MODEL_PROXY_BRIDGE = (
    Path(__file__).resolve().parents[1] / "runtime" / "model_proxy_bridge.py"
)


def apply_proxy_env(env: dict[str, str], proxy: "ProxyHandle") -> None:
    """Point a subprocess's OpenAI and Anthropic clients at the cost-tracking proxy.

    Sets both ``OPENAI_BASE_URL`` (read by openai-python / the Agents SDK) and
    ``OPENAI_API_BASE`` (read by langchain_openai, which Biomni uses). The real
    ``OPENAI_API_KEY`` is left untouched: the proxy runs without a master key and
    forwards using its own upstream key, and keeping the real key in the
    subprocess means the Agents SDK trace exporter (which talks to OpenAI
    directly, not through the proxy) still authenticates.

    For Biomni runs on Anthropic models (``--biomni-model claude-*``) the same
    must happen for the Anthropic client, or its traffic goes straight to
    api.anthropic.com and is never tracked. ``ChatAnthropic`` resolves its base
    URL from ``ANTHROPIC_API_URL`` then ``ANTHROPIC_BASE_URL`` and hands it to
    the anthropic SDK, which appends ``/v1/messages`` — the route LiteLLM serves
    at the proxy *root* — so strip the ``/v1`` suffix. Both vars are set (the
    API_URL one wins) so a stale value in the environment can't silently bypass
    the proxy. The real ``ANTHROPIC_API_KEY`` is likewise left untouched.
    """
    env["OPENAI_BASE_URL"] = proxy.base_url
    env["OPENAI_API_BASE"] = proxy.base_url
    anthropic_base = proxy.base_url.rsplit("/v1", 1)[0]
    env["ANTHROPIC_BASE_URL"] = anthropic_base
    env["ANTHROPIC_API_URL"] = anthropic_base


def apply_tls_egress_env(
    env: dict[str, str],
    *,
    proxy_url: str,
    ca_cert_path: str = sandbox.TLS_EGRESS_GATE_CA_CERT,
) -> None:
    """Force ordinary HTTP clients through the protected-run TLS gateway."""
    for key in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"):
        env[key] = proxy_url
    no_proxy = "127.0.0.1,localhost,::1"
    env["NO_PROXY"] = no_proxy
    env["no_proxy"] = no_proxy
    # Cover the common Python, curl/OpenSSL, Node, and git trust hooks.
    env["SSL_CERT_FILE"] = ca_cert_path
    env["REQUESTS_CA_BUNDLE"] = ca_cert_path
    env["CURL_CA_BUNDLE"] = ca_cert_path
    env["NODE_EXTRA_CA_CERTS"] = ca_cert_path
    env["GIT_SSL_CAINFO"] = ca_cert_path


def collect_usage(proxy: "ProxyHandle | None", t0: float, t1: float) -> dict | None:
    """Aggregate proxy usage rows for the request window ``[t0, t1]``."""
    if proxy is None:
        return None
    from ..accounting import aggregate_usage, wait_for_log_settle

    wait_for_log_settle(proxy.usage_log)
    return aggregate_usage(proxy.usage_log, t0, t1)


def model_proxy_context(
    *,
    framework_prompt: FrameworkPrompt,
    model: str,
    proxy: "ProxyHandle | None",
    enabled: bool,
):
    """Return a caller-owned proxy or a framework-local single-model proxy."""
    if proxy is not None:
        return contextlib.nullcontext(proxy)
    if not enabled:
        return contextlib.nullcontext(None)
    from ..accounting import scoped_model_proxy

    return scoped_model_proxy(
        framework=framework_prompt.framework,
        model=model,
        run_dir=framework_prompt.run_dir,
    )


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
    """Run a command, teeing combined stdout/stderr to terminal and a log file."""
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
            proc = subprocess.Popen(
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

                def _terminate_on_timeout() -> None:
                    nonlocal kill_timer, timed_out
                    timed_out = True
                    try:
                        os.killpg(proc.pid, signal.SIGTERM)
                    except (ProcessLookupError, PermissionError):
                        try:
                            proc.terminate()
                        except ProcessLookupError:
                            pass

                    def _kill_after_grace() -> None:
                        try:
                            os.killpg(proc.pid, signal.SIGKILL)
                        except (ProcessLookupError, PermissionError):
                            try:
                                proc.kill()
                            except ProcessLookupError:
                                pass

                    kill_timer = threading.Timer(5.0, _kill_after_grace)
                    kill_timer.daemon = True
                    kill_timer.start()

                timer = threading.Timer(timeout_seconds, _terminate_on_timeout)
                timer.daemon = True
                timer.start()
            assert proc.stdout is not None
            for line in proc.stdout:
                sys.stdout.write(line)
                sys.stdout.flush()
                log.write(line)
                log.flush()
                if stdout_file is not None:
                    stdout_file.write(line)
                    stdout_file.flush()
            returncode = proc.wait()
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


def check_expected_outputs(expected_outputs: Iterable[Path]) -> dict[str, bool]:
    """Return existence status for each expected output path."""
    return {str(path): path.exists() for path in expected_outputs}
