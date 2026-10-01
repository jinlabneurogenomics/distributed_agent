"""Launch the LiteLLM proxy and attribute usage to framework runs.

Runs in the *eval* environment (stdlib + python-dotenv only — never imports
``litellm``). Responsibilities:

* start the proxy from the isolated ``litellm-proxy`` pixi env as a subprocess,
  injecting the real upstream key, the usage-log path, and PYTHONPATH so the
  callback module loads;
* hand back the local base URL + master key for bioeval to inject into framework
  subprocess environments;
* after a framework subprocess finishes, bucket the proxy's JSONL usage rows into
  that run by wall-clock window and aggregate tokens + cost.
"""

from __future__ import annotations

import atexit
import contextlib
import json
import os
import shutil
import socket
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from dotenv import dotenv_values

from .pricing import model_provider, pricing_model_name, runtime_model_name

_THIS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _THIS_DIR.parents[2]
_PROXY_BIN = _REPO_ROOT / ".pixi" / "envs" / "litellm-proxy" / "bin" / "litellm"


@dataclass(frozen=True)
class ProxyHandle:
    """Connection details for a running proxy."""

    base_url: str
    usage_log: Path


@dataclass(frozen=True)
class ProxyModelConfig:
    """One model route and its framework-scoped upstream credential."""

    client_model: str
    upstream_model: str
    credential_candidates: tuple[str, ...]
    base_model: str


def proxy_model_config(framework: str, model: str) -> ProxyModelConfig:
    """Build the only model route exposed to one framework subprocess."""
    client_model = runtime_model_name(model)
    provider = model_provider(client_model)
    if framework == "distributed_agents":
        if provider != "openai":
            raise ValueError("DistributedAgents cost tracking currently requires a gpt-* model")
        credentials = ("DISTRIBUTED_AGENTS_OPENAI_API_KEY", "OPENAI_API_KEY")
    elif framework == "biomni":
        credentials = (
            ("BIOMNI_ANTHROPIC_API_KEY", "ANTHROPIC_API_KEY")
            if provider == "anthropic"
            else ("BIOMNI_OPENAI_API_KEY", "OPENAI_API_KEY")
        )
    elif framework == "claude-code":
        if provider != "anthropic":
            raise ValueError("Claude Code cost tracking requires a claude-* model")
        credentials = ("ANTHROPIC_API_KEY",)
    else:
        raise ValueError(f"no scoped LiteLLM route for framework {framework!r}")
    return ProxyModelConfig(
        client_model=client_model,
        upstream_model=f"{provider}/{client_model}",
        credential_candidates=credentials,
        base_model=pricing_model_name(client_model),
    )


def _free_port(host: str) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, 0))
        return sock.getsockname()[1]


def _populate_credentials(
    env: dict[str, str],
    *,
    required: tuple[str, ...],
) -> str:
    """Backfill the proxy env with API keys from the repo .env, then sanity-check."""
    repo_env = dotenv_values(_REPO_ROOT / ".env")
    for name, value in repo_env.items():
        if value and not env.get(name):
            env[name] = value
    for name in required:
        if env.get(name):
            return name
    raise RuntimeError(
        "No upstream credential found for this framework/model route "
        f"(checked {', '.join(required)} in the environment and repo .env)."
    )


def _scoped_config(path: Path, model: ProxyModelConfig, credential: str) -> None:
    """Write a secret-free, single-model LiteLLM config for one eval run."""
    payload = {
        "model_list": [
            {
                "model_name": model.client_model,
                "litellm_params": {
                    "model": model.upstream_model,
                    "api_key": f"os.environ/{credential}",
                },
                "model_info": {"base_model": model.base_model},
            }
        ],
        "litellm_settings": {
            "callbacks": "usage_callback.usage_logger",
            "drop_params": False,
            "num_retries": 8,
            "retry_after": 30,
            "request_timeout": 600,
        },
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def _wait_until_ready(base_url: str, timeout: float, proc: subprocess.Popen) -> None:
    deadline = time.time() + timeout
    health = base_url.rsplit("/v1", 1)[0] + "/health/readiness"
    while time.time() < deadline:
        if proc.poll() is not None:
            raise RuntimeError(f"litellm proxy exited early (code {proc.returncode})")
        try:
            with urllib.request.urlopen(health, timeout=2) as resp:
                if resp.status == 200:
                    return
        except (urllib.error.URLError, OSError):
            pass
        time.sleep(0.5)
    raise TimeoutError(f"litellm proxy not ready within {timeout}s at {health}")


@contextlib.contextmanager
def litellm_proxy(
    usage_log_path: Path,
    *,
    model_config: ProxyModelConfig,
    host: str = "127.0.0.1",
    port: int | None = None,
    readiness_timeout: float = 120.0,
    log_path: Path | None = None,
):
    """Start a single-model proxy and tear it down on context exit."""
    if not _PROXY_BIN.exists():
        raise RuntimeError(
            f"litellm proxy binary not found at {_PROXY_BIN}. "
            "Run `pixi install -e litellm-proxy` first."
        )
    usage_log_path = Path(usage_log_path)
    usage_log_path.parent.mkdir(parents=True, exist_ok=True)
    usage_log_path.touch(exist_ok=True)

    port = port or _free_port(host)
    base_url = f"http://{host}:{port}/v1"

    env = os.environ.copy()
    credential = _populate_credentials(
        env,
        required=model_config.credential_candidates,
    )
    env["BIOEVAL_USAGE_LOG"] = str(usage_log_path)
    # Pricing must stay tied to the pixi-locked catalog recorded by pricing.py,
    # not whatever happens to be on LiteLLM's main branch at run time.
    env["LITELLM_LOCAL_MODEL_COST_MAP"] = "True"
    env["PYTHONPATH"] = os.pathsep.join(
        [str(_THIS_DIR), env.get("PYTHONPATH", "")]
    ).rstrip(os.pathsep)

    with tempfile.TemporaryDirectory(
        prefix="bioeval-litellm-config-",
        dir="/tmp",
    ) as config_dir:
        config_path = Path(config_dir) / "config.json"
        # LiteLLM resolves custom callback modules relative to the config file,
        # even when PYTHONPATH contains the source directory.
        shutil.copy2(
            _THIS_DIR / "usage_callback.py",
            Path(config_dir) / "usage_callback.py",
        )
        _scoped_config(config_path, model_config, credential)
        cmd = [
            str(_PROXY_BIN),
            "--config",
            str(config_path),
            "--host",
            host,
            "--port",
            str(port),
        ]
        log_handle = open(log_path, "w") if log_path else subprocess.DEVNULL
        proc = subprocess.Popen(
            cmd,
            env=env,
            stdout=log_handle,
            stderr=subprocess.STDOUT,
        )

        def _terminate() -> None:
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    proc.kill()
            if log_handle not in (None, subprocess.DEVNULL):
                log_handle.close()

        atexit.register(_terminate)
        try:
            _wait_until_ready(base_url, readiness_timeout, proc)
            yield ProxyHandle(base_url=base_url, usage_log=usage_log_path)
        finally:
            _terminate()
            with contextlib.suppress(ValueError):
                atexit.unregister(_terminate)


def scoped_model_proxy(
    *,
    framework: str,
    model: str,
    run_dir: Path,
):
    """Start a per-run proxy that cannot route to a different configured model."""
    return litellm_proxy(
        run_dir / "model_usage.jsonl",
        log_path=run_dir / "model_proxy.log",
        model_config=proxy_model_config(framework, model),
    )


def wait_for_log_settle(
    path: Path, *, idle: float = 1.5, timeout: float = 15.0
) -> None:
    """Wait until the usage log stops growing.

    The proxy logs each request asynchronously, slightly after it returns the
    response to the client, so the last rows for a just-finished subprocess may
    not be on disk yet. Poll until the file size is stable for ``idle`` seconds.
    """
    path = Path(path)
    deadline = time.time() + timeout
    last_size = -1
    stable_since = time.time()
    while time.time() < deadline:
        size = path.stat().st_size if path.exists() else 0
        if size != last_size:
            last_size = size
            stable_since = time.time()
        elif time.time() - stable_since >= idle:
            return
        time.sleep(0.25)


def _num(value) -> float:
    return float(value) if isinstance(value, (int, float)) else 0.0


def aggregate_usage(usage_log_path: Path, t0: float, t1: float) -> dict:
    """Sum usage rows whose request start falls within ``[t0, t1]``.

    Framework subprocesses run sequentially, so a wall-clock window uniquely
    identifies one run's requests without per-request tagging.
    """
    path = Path(usage_log_path)
    summary = {
        "requests": 0,
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "cache_read_input_tokens": 0,
        "cache_creation_input_tokens": 0,
        "total_tokens": 0,
        "cost_usd": 0.0,
        "cost_unconfigured": False,
        "by_model": {},
        "window": {"start": t0, "end": t1},
    }
    if not path.exists():
        return summary

    seen_call_ids: set[str] = set()
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        ts = row.get("ts_start")
        if ts is None or not (t0 <= ts <= t1):
            continue
        # The Responses API logs each call twice under one litellm_call_id; keep
        # only the first. Rows without an id (shouldn't happen) are kept as-is.
        call_id = row.get("litellm_call_id")
        if call_id is not None:
            if call_id in seen_call_ids:
                continue
            seen_call_ids.add(call_id)

        model = row.get("model") or "unknown"
        prompt = _num(row.get("prompt_tokens"))
        completion = _num(row.get("completion_tokens"))
        cache_read = _num(row.get("cache_read_input_tokens"))
        cache_creation = _num(row.get("cache_creation_input_tokens"))
        total = _num(row.get("total_tokens")) or (prompt + completion)
        cost = _num(row.get("response_cost"))

        summary["requests"] += 1
        summary["prompt_tokens"] += int(prompt)
        summary["completion_tokens"] += int(completion)
        summary["cache_read_input_tokens"] += int(cache_read)
        summary["cache_creation_input_tokens"] += int(cache_creation)
        summary["total_tokens"] += int(total)
        summary["cost_usd"] += cost
        if row.get("cost_unconfigured"):
            summary["cost_unconfigured"] = True

        bucket = summary["by_model"].setdefault(
            model,
            {
                "requests": 0,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "cache_read_input_tokens": 0,
                "cache_creation_input_tokens": 0,
                "total_tokens": 0,
                "cost_usd": 0.0,
            },
        )
        bucket["requests"] += 1
        bucket["prompt_tokens"] += int(prompt)
        bucket["completion_tokens"] += int(completion)
        bucket["cache_read_input_tokens"] += int(cache_read)
        bucket["cache_creation_input_tokens"] += int(cache_creation)
        bucket["total_tokens"] += int(total)
        bucket["cost_usd"] += cost

    summary["cost_usd"] = round(summary["cost_usd"], 6)
    for bucket in summary["by_model"].values():
        bucket["cost_usd"] = round(bucket["cost_usd"], 6)
    return summary
