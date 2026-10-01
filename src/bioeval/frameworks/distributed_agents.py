"""DistributedAgents framework command, environment, and execution adapter."""

from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path
from typing import TYPE_CHECKING, Iterable

from ..accounting.pricing import finalize_usage
from ..artifacts.results import write_framework_result
from ..models import FrameworkPrompt, FrameworkRunResult
from ..runtime import sandbox
from ..runtime.gateways import framework_gateways
from ..runtime.paths import REPO_ROOT
from ..runtime.policy import SourcePolicy, write_source_filtered_copy
from ..runtime.source_policy import (
    audit_protected_run,
    filtered_codex_config,
)
from .codex import parse_distributed_agents_codex_usage
from .common import (
    ANALYSIS_ENV,
    DEFAULT_INPUT_ROOTS,
    apply_proxy_env,
    apply_tls_egress_env,
    check_expected_outputs,
    model_proxy_context,
    run_subprocess_with_log,
)

if TYPE_CHECKING:
    from ..accounting import ProxyHandle

DEFAULT_DISTRIBUTED_AGENTS_MODEL = "gpt-rosalind-5.5"
DISTRIBUTED_AGENTS_BACKENDS = ("codex", "api")
DEFAULT_DISTRIBUTED_AGENTS_BACKEND = "codex"
DISTRIBUTED_AGENTS_QUERY_MODES = ("adaptive", "direct")
DEFAULT_DISTRIBUTED_AGENTS_QUERY_MODE = "adaptive"
DISTRIBUTED_AGENTS_CODEX_LAUNCHER = Path(__file__).resolve().with_name("distributed_agents_launcher.py")
DISTRIBUTED_AGENTS_CODEX_SANDBOX_ENV = "BIOEVAL_DISTRIBUTED_AGENTS_CODEX_SANDBOX"


def distributed_agents_command(
    prompt_path: Path,
    run_dir: Path,
    *,
    model: str = DEFAULT_DISTRIBUTED_AGENTS_MODEL,
    pixi_executable: str = "pixi",
    backend: str = DEFAULT_DISTRIBUTED_AGENTS_BACKEND,
    query_mode: str = DEFAULT_DISTRIBUTED_AGENTS_QUERY_MODE,
    corpus_release: str | None = None,
    codex_input_roots: Iterable[Path] | None = None,
    codex_executable: str = "codex",
    codex_bwrap: bool = True,
    codex_config_overrides: Iterable[str] = (),
) -> list[str]:
    """Build the DistributedAgents query command used for prompt eval runs."""

    if backend not in DISTRIBUTED_AGENTS_BACKENDS:
        raise ValueError(f"unsupported DistributedAgents backend: {backend!r}")
    if query_mode not in DISTRIBUTED_AGENTS_QUERY_MODES:
        raise ValueError(f"unsupported DistributedAgents query mode: {query_mode!r}")
    cmd = [
        pixi_executable,
        "run",
        "distributed_agents",
        "query",
        "--task-file",
        str(prompt_path),
        "--out-dir",
        str(run_dir),
        "--backend",
        backend,
        "--model",
        model,
    ]
    if query_mode != DEFAULT_DISTRIBUTED_AGENTS_QUERY_MODE:
        cmd.extend(["--mode", query_mode])
    if corpus_release is not None:
        cmd.extend(["--corpus-release", corpus_release])
    if backend == "codex":
        if codex_executable != "codex":
            cmd.extend(["--codex-executable", codex_executable])
        if not codex_bwrap:
            cmd.append("--no-codex-bwrap")
        for root in codex_input_roots or ():
            cmd.extend(["--codex-input-root", str(root)])
        for override in codex_config_overrides:
            cmd.extend(["--codex-config-override", override])
    else:
        for root in codex_input_roots or ():
            cmd.extend(["--api-input-root", str(root)])
    return cmd


def distributed_agents_run_command(
    prompt_path: Path,
    run_dir: Path,
    *,
    model: str = DEFAULT_DISTRIBUTED_AGENTS_MODEL,
    pixi_executable: str = "pixi",
    fairness_sandbox: bool = False,
    input_roots: Iterable[Path] = DEFAULT_INPUT_ROOTS,
    backend: str = DEFAULT_DISTRIBUTED_AGENTS_BACKEND,
    query_mode: str = DEFAULT_DISTRIBUTED_AGENTS_QUERY_MODE,
    corpus_release: str | None = None,
    network_isolated: bool = False,
    filtered_mcp_url: str | None = None,
) -> list[str]:
    """Build DistributedAgents argv with an optional BioEval-owned Codex launcher."""

    eval_enclosure = fairness_sandbox or network_isolated
    if eval_enclosure and backend != "codex":
        raise ValueError("BioEval-owned fairness/protected enclosures require codex")
    config_overrides = (
        filtered_codex_config(filtered_mcp_url) if filtered_mcp_url is not None else ()
    )
    return distributed_agents_command(
        prompt_path,
        run_dir,
        model=model,
        pixi_executable=pixi_executable,
        backend=backend,
        query_mode=query_mode,
        corpus_release=corpus_release,
        codex_input_roots=input_roots,
        codex_executable=(str(DISTRIBUTED_AGENTS_CODEX_LAUNCHER) if eval_enclosure else "codex"),
        codex_bwrap=not eval_enclosure,
        codex_config_overrides=config_overrides,
    )


def distributed_agents_codex_sandbox_config(
    *,
    run_dir: Path,
    input_roots: Iterable[Path],
    corpus_release: str | None,
    runtime_env: dict[str, str],
    network_isolated: bool,
    literature_gate_host_dir: Path | None,
    tls_egress_gate_host_dir: Path | None,
    biokg_gate_host_dir: Path | None,
    codex_executable: str = "codex",
) -> str:
    """Serialize the BioEval-owned enclosure for the injected Codex launcher."""

    from distributed_agents.corpus.registry import get_release

    release = get_release(corpus_release)
    artifact_overrides = {
        artifact: Path(runtime_env[env_key]).expanduser().absolute()
        for artifact, env_key in (
            ("reports", "BIOKG_REPORTS_PATH"),
            ("findings", "DISTRIBUTED_AGENTS_FINDINGS_LEDGER"),
        )
        if runtime_env.get(env_key)
    }
    package_root = REPO_ROOT / "src" / "distributed_agents"
    candidates = [
        *input_roots,
        *release.runtime_roots(artifact_overrides=artifact_overrides),
        package_root / "skills",
        package_root / "corpus" / "mcp_server.py",
    ]
    gene_store = runtime_env.get("DISTRIBUTED_AGENTS_GENE_STORE")
    if gene_store:
        candidates.append(Path(gene_store))
    allow_ro = [
        str(path.expanduser().absolute())
        for path in dict.fromkeys(candidates)
        if path.expanduser().absolute().exists()
    ]
    return json.dumps(
        {
            "schema_version": "bioeval-distributed_agents-codex-sandbox-v1",
            "run_dir": str(run_dir.expanduser().absolute()),
            "analysis_env": str(ANALYSIS_ENV.expanduser().absolute()),
            "codex_executable": codex_executable,
            "allow_ro": allow_ro,
            "network_isolated": network_isolated,
            "literature_gate_host_dir": (
                str(literature_gate_host_dir)
                if literature_gate_host_dir is not None
                else None
            ),
            "tls_egress_gate_host_dir": (
                str(tls_egress_gate_host_dir)
                if tls_egress_gate_host_dir is not None
                else None
            ),
            "biokg_gate_host_dir": (
                str(biokg_gate_host_dir) if biokg_gate_host_dir is not None else None
            ),
        },
        sort_keys=True,
    )


def distributed_agents_env(
    *,
    proxy: "ProxyHandle | None" = None,
    fairness_sandbox: bool = False,
) -> dict[str, str]:
    """Environment for the trusted DistributedAgents coordinator process.

    With the BioEval enclosure enabled, the trusted DistributedAgents coordinator gets
    a scrubbed host environment but retains its real HOME long enough to stage
    Codex authentication. The injected launcher then gives the model a fresh
    HOME and the evaluation allowlist.
    """
    if fairness_sandbox:
        extra = {
            "DISTRIBUTED_AGENTS_SANDBOX": "0",
            "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        }
        for key in (
            "DISTRIBUTED_AGENTS_CORPUS_RELEASE",
            "DISTRIBUTED_AGENTS_CORPUS_ROOTS",
            "DISTRIBUTED_AGENTS_FINDINGS_LEDGER",
            "DISTRIBUTED_AGENTS_GENE_STORE",
            "BIOKG_REPORTS_PATH",
            "BIOKG_NEO4J_HTTP_URL",
            "BIOKG_NEO4J_DATABASE",
            "BIOKG_NEO4J_URI",
            "BIOKG_NEO4J_USER",
            "BIOKG_NEO4J_PASSWORD",
            "DISTRIBUTED_AGENTS_SUBAGENT_MAX",
            "DISTRIBUTED_AGENTS_SUBAGENT_CONCURRENCY",
            "DISTRIBUTED_AGENTS_SUBAGENT_MAX_TURNS",
            "DISTRIBUTED_AGENTS_SUBAGENT_LANE",
            "DISTRIBUTED_AGENTS_SYNTH_SLICE",
        ):
            val = os.environ.get(key)
            if val:
                extra[key] = val
        env = sandbox.clean_env(fake_home=str(Path.home()), extra=extra)
        if proxy is not None:
            apply_proxy_env(env, proxy)
        return env
    env = os.environ.copy()
    env["DISTRIBUTED_AGENTS_SANDBOX"] = "0"
    if proxy is not None:
        apply_proxy_env(env, proxy)
    return env


def run_distributed_agents_prompt(
    framework_prompt: FrameworkPrompt,
    *,
    model: str = DEFAULT_DISTRIBUTED_AGENTS_MODEL,
    fairness_sandbox: bool = False,
    pixi_executable: str = "pixi",
    cwd: Path | None = None,
    proxy: "ProxyHandle | None" = None,
    input_roots: Iterable[Path] = DEFAULT_INPUT_ROOTS,
    backend: str = DEFAULT_DISTRIBUTED_AGENTS_BACKEND,
    query_mode: str = DEFAULT_DISTRIBUTED_AGENTS_QUERY_MODE,
    corpus_release: str | None = None,
    source_policy: SourcePolicy | None = None,
    filtered_search_image: Path | None = None,
    apptainer_executable: str = "apptainer",
    track_cost: bool = True,
) -> FrameworkRunResult:
    """Run one rendered prompt through the DistributedAgents query agent."""
    log_path = framework_prompt.run_dir / "runner.log"
    input_roots = tuple(input_roots)
    policy_enabled = bool(source_policy and source_policy.enabled)
    eval_enclosure = fairness_sandbox or policy_enabled
    if eval_enclosure and backend != "codex":
        raise ValueError("fairness/protected DistributedAgents runs require the codex backend")
    proxy_context = model_proxy_context(
        framework_prompt=framework_prompt,
        model=model,
        proxy=proxy,
        enabled=False,
    )
    run_env = distributed_agents_env(
        proxy=None,
        fairness_sandbox=eval_enclosure,
    )
    filtered_reports: Path | None = None
    if policy_enabled:
        from distributed_agents.corpus.registry import get_release

        filtered_reports = write_source_filtered_copy(
            get_release(corpus_release).artifact("reports"),
            (
                framework_prompt.run_dir
                / "codex_runtime"
                / "protected_inputs"
                / "findings_reports.filtered.jsonl"
            ),
            policy=source_policy,
        )
        run_env["BIOKG_REPORTS_PATH"] = str(filtered_reports)
    biokg_preflight_http_url = (
        os.environ.get("BIOKG_NEO4J_HTTP_URL", "http://127.0.0.1:7474")
        if policy_enabled
        else None
    )
    with framework_gateways(
        run_dir=framework_prompt.run_dir,
        source_policy=source_policy,
        filtered_search_image=filtered_search_image,
        apptainer_executable=apptainer_executable,
        proxy_context=proxy_context,
        require_model_gateway=False,
        biokg_base_url=biokg_preflight_http_url,
    ) as gateways:
        if gateways.tls_egress_proxy_url is not None:
            apply_tls_egress_env(
                run_env,
                proxy_url=gateways.tls_egress_proxy_url,
            )
        if gateways.biokg_http_url is not None:
            run_env["BIOKG_NEO4J_HTTP_URL"] = gateways.biokg_http_url
        if biokg_preflight_http_url is not None:
            run_env["DISTRIBUTED_AGENTS_BIOKG_PREFLIGHT_HTTP_URL"] = biokg_preflight_http_url
        if eval_enclosure:
            run_env[DISTRIBUTED_AGENTS_CODEX_SANDBOX_ENV] = distributed_agents_codex_sandbox_config(
                run_dir=framework_prompt.run_dir,
                input_roots=input_roots,
                corpus_release=corpus_release,
                runtime_env=run_env,
                network_isolated=policy_enabled,
                literature_gate_host_dir=gateways.literature_gate_host_dir,
                tls_egress_gate_host_dir=gateways.tls_egress_gate_host_dir,
                biokg_gate_host_dir=gateways.biokg_gate_host_dir,
            )
        cmd = distributed_agents_run_command(
            framework_prompt.prompt_path,
            framework_prompt.run_dir,
            model=model,
            pixi_executable=pixi_executable,
            fairness_sandbox=eval_enclosure,
            input_roots=input_roots,
            backend=backend,
            query_mode=query_mode,
            corpus_release=corpus_release,
            network_isolated=policy_enabled,
            filtered_mcp_url=gateways.filtered_mcp_url,
        )
        t0 = time.time()
        if gateways.active_proxy is not None:
            apply_proxy_env(run_env, gateways.active_proxy)
        returncode = run_subprocess_with_log(
            cmd,
            log_path=log_path,
            cwd=cwd,
            env=run_env,
        )
        t1 = time.time()
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
    raw_usage, native_model = parse_distributed_agents_codex_usage(framework_prompt.run_dir)
    usage_model = native_model or model
    cost_source = "tokens"
    usage = finalize_usage(
        raw_usage,
        model=usage_model,
        cost_source=cost_source,
        pricing_enabled=track_cost,
    )
    result = FrameworkRunResult(
        framework=framework_prompt.framework,
        run_dir=framework_prompt.run_dir,
        prompt_path=framework_prompt.prompt_path,
        expected_outputs=framework_prompt.expected_outputs,
        model=usage_model,
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
