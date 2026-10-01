"""Biomni framework command, environment, and execution adapter."""

from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path
from typing import TYPE_CHECKING, Iterable

from ..accounting.pricing import finalize_usage, runtime_model_name
from ..artifacts.results import write_framework_result
from ..models import FrameworkPrompt, FrameworkRunResult
from ..runtime import sandbox
from ..runtime.gateways import framework_gateways
from ..runtime.paths import REPO_ROOT
from ..runtime.policy import SourcePolicy
from ..runtime.source_policy import audit_protected_run
from .common import (
    DEFAULT_INPUT_ROOTS,
    DEFAULT_MODEL_PROXY_BRIDGE,
    apply_proxy_env,
    apply_tls_egress_env,
    check_expected_outputs,
    collect_usage,
    model_proxy_context,
    run_subprocess_with_log,
)

if TYPE_CHECKING:
    from ..accounting import ProxyHandle

DEFAULT_BIOMNI_MODEL = "claude-opus-4-5"
DEFAULT_BIOMNI_ENV = "biomni_e1"
DEFAULT_BIOMNI_RUNNER = Path(__file__).resolve().with_name("biomni_runner.py")
DEFAULT_BIOMNI_DATA_PATH = "modules/Biomni/data"
SANDBOX_BIOMNI_DATA_PATH = "/tmp/biomni-data"

BIOMNI_KEY_NAMES = ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "BIOMNI_ANTHROPIC_API_KEY")


def biomni_env_vars(
    *,
    proxy: "ProxyHandle | None" = None,
    fairness_sandbox: bool = False,
    cwd: Path | None = None,
    filtered_mcp_url: str | None = None,
    tls_egress_proxy_url: str | None = None,
) -> dict[str, str]:
    """Environment for Biomni runs.

    Sandboxed: a scrubbed env carrying only the LLM API keys (backfilled from the
    repo ``.env`` when not exported), since Biomni's runner reads keys from the
    environment (it does not load ``.env`` itself). Unsandboxed: inherit the
    parent env. A proxy, when supplied, redirects Biomni's LLM client through it.
    """
    if fairness_sandbox:
        extra: dict[str, str] = {}
        dotenv = None
        for key in BIOMNI_KEY_NAMES:
            val = os.environ.get(key)
            if not val:
                if dotenv is None:
                    from dotenv import dotenv_values

                    env_path = (cwd or REPO_ROOT) / ".env"
                    dotenv = dotenv_values(env_path) if env_path.exists() else {}
                val = dotenv.get(key)
            if val:
                extra[key] = val
        if filtered_mcp_url:
            extra["BIOEVAL_FILTERED_MCP_URL"] = filtered_mcp_url
        env = sandbox.clean_env(extra=extra)
        if proxy is not None:
            apply_proxy_env(env, proxy)
        if tls_egress_proxy_url:
            apply_tls_egress_env(env, proxy_url=tls_egress_proxy_url)
        return env
    env = os.environ.copy()
    if filtered_mcp_url:
        env["BIOEVAL_FILTERED_MCP_URL"] = filtered_mcp_url
    if proxy is not None:
        apply_proxy_env(env, proxy)
    if tls_egress_proxy_url:
        apply_tls_egress_env(env, proxy_url=tls_egress_proxy_url)
    return env


def biomni_command(
    prompt_path: Path,
    run_dir: Path,
    *,
    model: str = DEFAULT_BIOMNI_MODEL,
    data_path: str = DEFAULT_BIOMNI_DATA_PATH,
    biomni_repo: Path | None = Path("modules/Biomni"),
    biomni_env: str = DEFAULT_BIOMNI_ENV,
    mamba_executable: str = "mamba",
    runner_script: Path = DEFAULT_BIOMNI_RUNNER,
) -> list[str]:
    """Build the Biomni command, running in its own mamba environment."""
    model = runtime_model_name(model)
    python_cmd = [
        "python",
        str(runner_script),
        "--prompt-path",
        str(prompt_path),
        "--run-dir",
        str(run_dir),
        "--model",
        model,
        "--data-path",
        data_path,
    ]
    if biomni_repo is not None:
        python_cmd.extend(["--biomni-repo", str(biomni_repo)])
    if biomni_env:
        return [mamba_executable, "run", "-n", biomni_env, *python_cmd]
    return python_cmd


def biomni_allow_ro(
    *,
    biomni_repo: Path | None = Path("modules/Biomni"),
    runner_script: Path = DEFAULT_BIOMNI_RUNNER,
    data_path: str | None = None,
) -> list[Path]:
    """Read-only paths Biomni needs under the allowlist sandbox.

    Mounts the Biomni repo and just the single runner file (it lives under
    ``src/bioeval``, which is otherwise absent so graders/specs stay hidden).
    Task inputs are mounted separately through ``input_roots``. ``data_path`` is
    optional for backwards-compatible callers, but protected runs deliberately
    use a fresh tmpfs data directory rather than exposing the repository's
    shared ``data/`` tree.
    """
    paths = [
        runner_script,  # src/bioeval/frameworks/biomni_runner.py (file only)
    ]
    if data_path is not None:
        data = Path(data_path)
        paths.append(data if data.is_absolute() else (REPO_ROOT / data).resolve())
    if biomni_repo is not None:
        repo = biomni_repo if biomni_repo.is_absolute() else REPO_ROOT / biomni_repo
        paths.append(repo)
    return paths


def biomni_run_command(
    prompt_path: Path,
    run_dir: Path,
    *,
    model: str = DEFAULT_BIOMNI_MODEL,
    data_path: str = DEFAULT_BIOMNI_DATA_PATH,
    biomni_repo: Path | None = Path("modules/Biomni"),
    biomni_env: str = DEFAULT_BIOMNI_ENV,
    mamba_executable: str = "mamba",
    runner_script: Path = DEFAULT_BIOMNI_RUNNER,
    fairness_sandbox: bool = False,
    input_roots: Iterable[Path] = DEFAULT_INPUT_ROOTS,
    network_isolated: bool = False,
    model_gate_host_dir: Path | None = None,
    literature_gate_host_dir: Path | None = None,
    tls_egress_gate_host_dir: Path | None = None,
) -> list[str]:
    """Biomni argv, optionally wrapped in the allowlist fairness sandbox.

    Relative pipeline inputs are resolved before the sandbox changes into
    ``run_dir`` so task-relative deliverables land in the correct directory.
    mamba is invoked by absolute path (``~/miniforge3/bin/mamba``) since the shell
    ``mamba`` function is unavailable to a bare subprocess. The env dir may need
    to write conda-meta/history, so the miniforge tree is mounted read-write.
    """
    if network_isolated and not fairness_sandbox:
        raise ValueError("network-isolated Biomni requires the fairness sandbox")
    if network_isolated and model_gate_host_dir is None:
        raise ValueError("network-isolated Biomni requires a model gateway")

    exe = mamba_executable
    command_data_path = data_path
    command_biomni_repo = biomni_repo
    command_runner_script = runner_script
    command_biomni_env = biomni_env
    biomni_prefix: Path | None = None
    host_data_lake: Path | None = None
    if fairness_sandbox:
        # BioMNI creates ``biomni_data/`` below this path. Keep that mutable
        # framework scratch state in the sandbox tmpfs; the task's declared
        # inputs are mounted independently and read-only through ``input_roots``.
        # The framework's own data lake is bind-mounted read-only *into* that
        # tmpfs below, so A1 can still makedirs around it.
        host = Path(data_path)
        host = host if host.is_absolute() else (REPO_ROOT / host)
        candidate = (host / "biomni_data" / "data_lake").resolve()
        if candidate.is_dir() and any(candidate.iterdir()):
            host_data_lake = candidate
        command_data_path = SANDBOX_BIOMNI_DATA_PATH
        if biomni_repo is not None and not biomni_repo.is_absolute():
            command_biomni_repo = (REPO_ROOT / biomni_repo).resolve()
        if not runner_script.is_absolute():
            command_runner_script = (REPO_ROOT / runner_script).resolve()
        if biomni_env:
            # Invoke the environment's interpreter directly. Mounting the whole
            # miniforge installation read-write allowed cross-run persistence
            # and exposed unrelated environments/caches to the evaluated model.
            biomni_prefix = Path.home() / "miniforge3" / "envs" / biomni_env
            if not (biomni_prefix / "bin" / "python").exists():
                raise FileNotFoundError(
                    f"Biomni environment Python not found: "
                    f"{biomni_prefix / 'bin' / 'python'}"
                )
            command_biomni_env = ""
    cmd = biomni_command(
        prompt_path,
        run_dir,
        model=model,
        data_path=command_data_path,
        biomni_repo=command_biomni_repo,
        biomni_env=command_biomni_env,
        mamba_executable=exe,
        runner_script=command_runner_script,
    )
    if not fairness_sandbox:
        return cmd
    extra_binds: list[tuple[str, str, bool]] = []
    if host_data_lake is not None:
        # Read-only lake inside the writable tmpfs root; bwrap creates parents.
        extra_binds.append(
            (
                str(host_data_lake),
                f"{SANDBOX_BIOMNI_DATA_PATH}/biomni_data/data_lake",
                True,
            )
        )
    if network_isolated:
        inner_cmd = cmd
        cmd = [
            "/usr/bin/python3",
            str(DEFAULT_MODEL_PROXY_BRIDGE),
            "--socket",
            sandbox.MODEL_GATE_SOCKET,
            "--port",
            str(sandbox.MODEL_GATE_PORT),
        ]
        if literature_gate_host_dir is not None:
            cmd.extend(
                [
                    "--relay",
                    (
                        f"{sandbox.LITERATURE_GATE_PORT}:"
                        f"{sandbox.LITERATURE_GATE_SOCKET}"
                    ),
                ]
            )
        if tls_egress_gate_host_dir is not None:
            cmd.extend(
                [
                    "--relay",
                    (
                        f"{sandbox.TLS_EGRESS_GATE_PORT}:"
                        f"{sandbox.TLS_EGRESS_GATE_SOCKET}"
                    ),
                ]
            )
        cmd.extend(["--", *inner_cmd])
        extra_binds.append((str(model_gate_host_dir), sandbox.MODEL_GATE_DIR, False))
        if literature_gate_host_dir is not None:
            extra_binds.append(
                (
                    str(literature_gate_host_dir),
                    sandbox.LITERATURE_GATE_DIR,
                    False,
                )
            )
        if tls_egress_gate_host_dir is not None:
            extra_binds.append(
                (
                    str(tls_egress_gate_host_dir),
                    sandbox.TLS_EGRESS_GATE_DIR,
                    False,
                )
            )
    toolchain_ro = [biomni_prefix] if biomni_prefix is not None else []
    toolchain_path = (
        f"{biomni_prefix / 'bin'}:/usr/bin:/bin"
        if biomni_prefix is not None
        else "/usr/bin:/bin"
    )
    return sandbox.bwrap_allowlist_command(
        cmd,
        chdir=str(run_dir),
        allow_ro=[
            *biomni_allow_ro(
                biomni_repo=biomni_repo,
                runner_script=command_runner_script,
            ),
            DEFAULT_MODEL_PROXY_BRIDGE,
            *toolchain_ro,
            *input_roots,
        ],
        allow_rw=[run_dir],
        path=toolchain_path,
        share_net=not network_isolated,
        extra_binds=extra_binds,
    )


def run_biomni_prompt(
    framework_prompt: FrameworkPrompt,
    *,
    model: str = DEFAULT_BIOMNI_MODEL,
    data_path: str = DEFAULT_BIOMNI_DATA_PATH,
    biomni_repo: Path | None = Path("modules/Biomni"),
    biomni_env: str = DEFAULT_BIOMNI_ENV,
    mamba_executable: str = "mamba",
    runner_script: Path = DEFAULT_BIOMNI_RUNNER,
    cwd: Path | None = None,
    proxy: "ProxyHandle | None" = None,
    fairness_sandbox: bool = False,
    input_roots: Iterable[Path] = DEFAULT_INPUT_ROOTS,
    source_policy: SourcePolicy | None = None,
    filtered_search_image: Path | None = None,
    apptainer_executable: str = "apptainer",
    track_cost: bool = True,
) -> FrameworkRunResult:
    """Run one rendered prompt through Biomni A1 in Biomni's own environment."""
    log_path = framework_prompt.run_dir / "runner.log"
    model = runtime_model_name(model)
    policy_enabled = bool(source_policy and source_policy.enabled)
    if policy_enabled and not fairness_sandbox:
        raise ValueError("protected Biomni runs require --biomni-fairness-sandbox")
    proxy_context = model_proxy_context(
        framework_prompt=framework_prompt,
        model=model,
        proxy=proxy,
        enabled=track_cost or policy_enabled,
    )
    with framework_gateways(
        run_dir=framework_prompt.run_dir,
        source_policy=source_policy,
        filtered_search_image=filtered_search_image,
        apptainer_executable=apptainer_executable,
        proxy_context=proxy_context,
    ) as gateways:
        cmd = biomni_run_command(
            framework_prompt.prompt_path,
            framework_prompt.run_dir,
            model=model,
            data_path=data_path,
            biomni_repo=biomni_repo,
            biomni_env=biomni_env,
            mamba_executable=mamba_executable,
            runner_script=runner_script,
            fairness_sandbox=fairness_sandbox,
            input_roots=input_roots,
            network_isolated=policy_enabled,
            model_gate_host_dir=gateways.model_gate_host_dir,
            literature_gate_host_dir=gateways.literature_gate_host_dir,
            tls_egress_gate_host_dir=gateways.tls_egress_gate_host_dir,
        )
        t0 = time.time()
        returncode = run_subprocess_with_log(
            cmd,
            log_path=log_path,
            cwd=cwd,
            env=biomni_env_vars(
                proxy=gateways.sandbox_proxy,
                fairness_sandbox=fairness_sandbox,
                cwd=cwd,
                filtered_mcp_url=gateways.filtered_mcp_base_url,
                tls_egress_proxy_url=gateways.tls_egress_proxy_url,
            ),
        )
        t1 = time.time()
        proxy_usage = collect_usage(gateways.active_proxy, t0, t1)
        filtered_proxy = gateways.filtered_proxy
        tls_egress = gateways.tls_egress

    source_audit = None
    if policy_enabled:
        source_audit = audit_protected_run(
            run_dir=framework_prompt.run_dir,
            output_paths=framework_prompt.expected_outputs,
            policy=source_policy,
            broker=filtered_proxy,
            tls_audit_path=(tls_egress.audit_path if tls_egress is not None else None),
        )
        if source_audit["status"] != "passed" and returncode == 0:
            returncode = 86
    usage = finalize_usage(
        proxy_usage,
        model=model,
        cost_source="litellm",
        pricing_enabled=track_cost,
    )
    result = FrameworkRunResult(
        framework=framework_prompt.framework,
        run_dir=framework_prompt.run_dir,
        prompt_path=framework_prompt.prompt_path,
        expected_outputs=framework_prompt.expected_outputs,
        model=model,
        returncode=returncode,
        command=cmd,
        log_path=log_path,
        output_status=check_expected_outputs(framework_prompt.expected_outputs),
        duration_s=round(t1 - t0, 2),
        usage=usage,
        source_policy_audit=source_audit,
    )
    write_framework_result(result)
    if returncode:
        raise subprocess.CalledProcessError(returncode, cmd)
    return result
