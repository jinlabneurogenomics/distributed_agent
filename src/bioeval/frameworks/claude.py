"""Claude Code framework command, environment, and execution adapter."""

from __future__ import annotations

import json
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
    ANALYSIS_ENV,
    ANALYSIS_ENV_BIN,
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

DEFAULT_CLAUDE_MODEL = "claude-opus-4-8"
DEFAULT_CLAUDE_FAIRNESS_SANDBOX = True
DEFAULT_CLAUDE_WEB_TOOLS = "Bash,Read,Write,Edit,WebSearch,WebFetch,Glob,Grep"
DEFAULT_CLAUDE_SHELL_TOOLS = "Bash,Read,Write,Edit,Glob,Grep"
CLAUDE_WEB_MODES = ("off", "tools", "shell")
DEFAULT_CLAUDE_INPUT_ROOTS = DEFAULT_INPUT_ROOTS
DEFAULT_CLAUDE_PERMISSION_MODE = "auto"
CLAUDE_PERMISSION_MODES = (
    "default",
    "acceptEdits",
    "auto",
    "dontAsk",
    "bypassPermissions",
    "plan",
)
DEFAULT_CLAUDE_MAX_TURNS = 200
DEFAULT_CLAUDE_OUTPUT_FORMAT = "json"
CLAUDE_OUTPUT_FORMATS = ("text", "json", "stream-json")


def claude_command(
    *,
    model: str = DEFAULT_CLAUDE_MODEL,
    permission_mode: str = DEFAULT_CLAUDE_PERMISSION_MODE,
    max_turns: int = DEFAULT_CLAUDE_MAX_TURNS,
    output_format: str = DEFAULT_CLAUDE_OUTPUT_FORMAT,
    claude_executable: str = "claude",
    web: str = "off",
    allowed_tools: str | None = None,
    literature_mcp_url: str | None = None,
) -> list[str]:
    """Build the hermetic Claude Code command used for prompt eval runs.

    ``web="off"`` (default): ``--bare`` disables Claude's own context sources —
    CLAUDE.md (all scopes), auto-memory, hooks, LSP, plugins, attribution — and
    forces ``ANTHROPIC_API_KEY``-only auth. Fully hermetic, but ``--bare`` also
    disables the built-in WebSearch/WebFetch tools (and no network use).

    ``web="tools"``/``"shell"``: keep web access. ``--bare`` is dropped (it strips
    web tools) and isolation is re-provided by ``--setting-sources ""`` (no
    CLAUDE.md/settings/hooks), ``--strict-mcp-config`` (no MCP),
    ``CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`` (set in :func:`claude_env`), and the
    sandbox's tmpfs ``$HOME``. The two differ only in the tool allowlist:

    * ``tools`` — grants built-in ``WebSearch``/``WebFetch`` (which route through a
      fast auxiliary model, e.g. haiku, that fetches + condenses web content).
    * ``shell`` — withholds those tools; the agent reaches the web via ``Bash``
      (curl/python) with its own model, so the run stays single-model (no haiku
      helper). Network is open in the sandbox either way.
    """
    model = runtime_model_name(model)
    mcp_config = {"mcpServers": {}}
    if literature_mcp_url:
        mcp_config["mcpServers"]["bioeval_literature"] = {
            "type": "http",
            "url": literature_mcp_url,
        }
    mcp_json = json.dumps(mcp_config, separators=(",", ":"))
    cmd = [claude_executable]
    if web in ("tools", "shell"):
        default_tools = (
            DEFAULT_CLAUDE_WEB_TOOLS if web == "tools" else DEFAULT_CLAUDE_SHELL_TOOLS
        )
        cmd += [
            "-p",
            "--setting-sources",
            "",
            "--strict-mcp-config",
            "--mcp-config",
            mcp_json,
            "--allowedTools",
            allowed_tools or default_tools,
        ]
        if web == "shell":
            # --allowedTools is an auto-approve list, NOT a restriction: under a
            # permissive mode the built-in WebSearch/WebFetch run regardless. Hard-
            # block them so web access goes only through Bash (agent's own model,
            # no auxiliary web-tool model).
            cmd += ["--disallowedTools", "WebSearch,WebFetch"]
    else:
        cmd += ["--bare", "-p", "--strict-mcp-config", "--mcp-config", mcp_json]
        if literature_mcp_url:
            cmd += [
                "--allowedTools",
                (
                    "Bash,Read,Write,Edit,Glob,Grep,"
                    "mcp__bioeval_literature__search_pubmed,"
                    "mcp__bioeval_literature__fetch_pubmed"
                ),
            ]
    if model:
        cmd.extend(["--model", model])
    if permission_mode:
        cmd.extend(["--permission-mode", permission_mode])
    if output_format:
        cmd.extend(["--output-format", output_format])
    if max_turns:
        cmd.extend(["--max-turns", str(max_turns)])
    return cmd


def claude_run_command(
    run_dir: Path,
    *,
    model: str = DEFAULT_CLAUDE_MODEL,
    permission_mode: str = DEFAULT_CLAUDE_PERMISSION_MODE,
    max_turns: int = DEFAULT_CLAUDE_MAX_TURNS,
    output_format: str = DEFAULT_CLAUDE_OUTPUT_FORMAT,
    claude_executable: str = "claude",
    fairness_sandbox: bool = DEFAULT_CLAUDE_FAIRNESS_SANDBOX,
    input_roots: Iterable[Path] = DEFAULT_CLAUDE_INPUT_ROOTS,
    web: str = "off",
    allowed_tools: str | None = None,
    network_isolated: bool = False,
    model_gate_host_dir: Path | None = None,
    literature_gate_host_dir: Path | None = None,
    tls_egress_gate_host_dir: Path | None = None,
    literature_mcp_url: str | None = None,
) -> list[str]:
    """Full argv for a Claude run, wrapped in the allowlist fairness sandbox.

    The sandbox mounts only the declared ``input_roots`` and the Claude toolchain
    read-only and ``run_dir`` read-write; ``$HOME`` is a fresh tmpfs, so the
    operator's ``~/.claude`` auto-memory, global/project ``CLAUDE.md``, MCP
    servers, skills, and ``.agent`` context cannot leak, and ``debug/``,
    ``src/bioeval``, ``outputs/``, and the results tree are simply absent. The
    agent's working dir is ``run_dir``, so its deliverables land there.

    ``fairness_sandbox=False`` is a debug escape hatch that returns the bare
    (still ``--bare``-hermetic) command with no filesystem sandbox.
    """
    if network_isolated and not fairness_sandbox:
        raise ValueError("network-isolated Claude requires the fairness sandbox")
    if network_isolated and model_gate_host_dir is None:
        raise ValueError("network-isolated Claude requires a model gateway")

    cmd = claude_command(
        model=model,
        permission_mode=permission_mode,
        max_turns=max_turns,
        output_format=output_format,
        claude_executable=claude_executable,
        web=web,
        allowed_tools=allowed_tools,
        literature_mcp_url=literature_mcp_url,
    )
    if not fairness_sandbox:
        return cmd
    extra_binds: list[tuple[str, str, bool]] = []
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
    toolchain = sandbox.claude_toolchain_paths(claude_executable)
    bin_dir = str(toolchain[0]) if toolchain else None
    # (B1) analysis env first on PATH so `python` has the pandas/duckdb stack.
    parts = (
        [str(ANALYSIS_ENV_BIN)] + ([bin_dir] if bin_dir else []) + ["/usr/bin", "/bin"]
    )
    return sandbox.bwrap_allowlist_command(
        cmd,
        chdir=str(run_dir),
        allow_ro=[
            ANALYSIS_ENV,
            DEFAULT_MODEL_PROXY_BRIDGE,
            *input_roots,
            *toolchain,
        ],
        allow_rw=[run_dir],
        path=":".join(parts),
        share_net=not network_isolated,
        extra_binds=extra_binds,
    )


def claude_env(
    *,
    cwd: Path | None = None,
    fairness_sandbox: bool = DEFAULT_CLAUDE_FAIRNESS_SANDBOX,
    web: str = "off",
    proxy: "ProxyHandle | None" = None,
    tls_egress_proxy_url: str | None = None,
) -> dict[str, str]:
    """Environment for Claude runs.

    Sandboxed (default): a scrubbed env carrying only ``ANTHROPIC_API_KEY``
    (backfilled from the repo ``.env`` when not already exported, mirroring
    ``codex_env``), so no host env hints or stray secrets enter the sandbox. In
    ``web`` mode (which drops ``--bare``) it also sets
    ``CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`` so auto-memory stays off even though
    ``--bare`` is not in play. Unsandboxed escape hatch: inherit the parent env.
    """
    if not fairness_sandbox:
        env = os.environ.copy()
        if proxy is not None:
            apply_proxy_env(env, proxy)
        if tls_egress_proxy_url:
            apply_tls_egress_env(env, proxy_url=tls_egress_proxy_url)
        return env
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        from dotenv import dotenv_values

        env_path = (cwd or REPO_ROOT) / ".env"
        if env_path.exists():
            key = dotenv_values(env_path).get("ANTHROPIC_API_KEY")
    extra = {"ANTHROPIC_API_KEY": key} if key else {}
    if web != "off":
        extra["CLAUDE_CODE_DISABLE_AUTO_MEMORY"] = "1"
    env = sandbox.clean_env(extra=extra)
    if proxy is not None:
        apply_proxy_env(env, proxy)
    if tls_egress_proxy_url:
        apply_tls_egress_env(env, proxy_url=tls_egress_proxy_url)
    return env


def parse_claude_usage(stdout_path: Path) -> dict | None:
    """Extract token/cost usage from a Claude Code ``--output-format json`` result.

    Claude Code emits its own per-run accounting (``total_cost_usd``, ``usage``,
    ``num_turns``) in the single JSON result object printed to stdout. We mirror
    that stdout to ``claude_result.json`` and parse it into the same usage shape
    used for the proxy-tracked frameworks.
    """
    try:
        text = stdout_path.read_text().strip()
    except OSError:
        return None
    if not text:
        return None
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict):
        return None
    usage = payload.get("usage") or {}
    token_keys = (
        "input_tokens",
        "output_tokens",
        "cache_creation_input_tokens",
        "cache_read_input_tokens",
    )
    tokens = {key: int(usage.get(key, 0) or 0) for key in token_keys}
    cost = payload.get("total_cost_usd")
    return {
        "total_tokens": sum(tokens.values()),
        "requests": int(payload.get("num_turns", 0) or 0),
        "cost_usd": float(cost) if cost is not None else 0.0,
        "cost_unconfigured": cost is None,
        "duration_ms": payload.get("duration_ms"),
        "by_model": payload.get("modelUsage") or {},
        **tokens,
    }


def write_claude_last_message(result_path: Path, output_path: Path) -> bool:
    """Extract Claude's final text while retaining the raw accounting payload."""
    try:
        payload = json.loads(result_path.read_text())
    except (OSError, json.JSONDecodeError):
        return False
    if not isinstance(payload, dict) or not isinstance(payload.get("result"), str):
        return False
    output_path.write_text(payload["result"])
    return True


def run_claude_prompt(
    framework_prompt: FrameworkPrompt,
    *,
    model: str = DEFAULT_CLAUDE_MODEL,
    permission_mode: str = DEFAULT_CLAUDE_PERMISSION_MODE,
    max_turns: int = DEFAULT_CLAUDE_MAX_TURNS,
    output_format: str = DEFAULT_CLAUDE_OUTPUT_FORMAT,
    claude_executable: str = "claude",
    fairness_sandbox: bool = DEFAULT_CLAUDE_FAIRNESS_SANDBOX,
    input_roots: Iterable[Path] = DEFAULT_CLAUDE_INPUT_ROOTS,
    web: str = "off",
    allowed_tools: str | None = None,
    cwd: Path | None = None,
    proxy: "ProxyHandle | None" = None,
    source_policy: SourcePolicy | None = None,
    filtered_search_image: Path | None = None,
    apptainer_executable: str = "apptainer",
    track_cost: bool = True,
) -> FrameworkRunResult:
    """Run one rendered prompt through Claude Code non-interactively.

    Defaults to the allowlist fairness sandbox (see ``claude_run_command``):
    ``~/.claude`` auto-memory/config/MCP and the repo's answer paths are absent,
    the env is scrubbed to just ``ANTHROPIC_API_KEY``, and the agent's cwd is its
    own ``run_dir``. The prompt is still fed on stdin (inherited through bwrap).
    ``web=True`` enables WebSearch/WebFetch (drops ``--bare``; isolation preserved
    by the sandbox + strict MCP + CLAUDE_CODE_DISABLE_AUTO_MEMORY).
    A protected run keeps hosted web tools off but gives ordinary HTTP clients
    access only through the TLS-intercepting loopback gateway.
    """
    log_path = framework_prompt.run_dir / "runner.log"
    model = runtime_model_name(model)
    last_message_path = framework_prompt.run_dir / "last_message.txt"
    stdout_path = (
        framework_prompt.run_dir / "claude_result.json"
        if output_format == "json"
        else last_message_path
    )
    policy_enabled = bool(source_policy and source_policy.enabled)
    if policy_enabled and not fairness_sandbox:
        raise ValueError("protected Claude runs require --claude-fairness-sandbox")
    if policy_enabled and web != "off":
        raise ValueError("protected Claude runs require --claude-web off")
    proxy_context = model_proxy_context(
        framework_prompt=framework_prompt,
        model=model,
        proxy=proxy,
        enabled=policy_enabled or (track_cost and output_format != "json"),
    )
    with framework_gateways(
        run_dir=framework_prompt.run_dir,
        source_policy=source_policy,
        filtered_search_image=filtered_search_image,
        apptainer_executable=apptainer_executable,
        proxy_context=proxy_context,
    ) as gateways:
        cmd = claude_run_command(
            framework_prompt.run_dir,
            model=model,
            permission_mode=permission_mode,
            max_turns=max_turns,
            output_format=output_format,
            claude_executable=claude_executable,
            fairness_sandbox=fairness_sandbox,
            input_roots=input_roots,
            web=web,
            allowed_tools=allowed_tools,
            network_isolated=policy_enabled,
            model_gate_host_dir=gateways.model_gate_host_dir,
            literature_gate_host_dir=gateways.literature_gate_host_dir,
            tls_egress_gate_host_dir=gateways.tls_egress_gate_host_dir,
            literature_mcp_url=gateways.filtered_mcp_url,
        )
        # Under the sandbox the inner cwd is set by bwrap (--chdir run_dir); the
        # outer launch dir only needs to resolve .env, so use the repo root.
        outer_cwd = REPO_ROOT if fairness_sandbox else cwd
        t0 = time.time()
        returncode = run_subprocess_with_log(
            cmd,
            log_path=log_path,
            cwd=outer_cwd,
            env=claude_env(
                cwd=cwd,
                fairness_sandbox=fairness_sandbox,
                web=web,
                proxy=gateways.sandbox_proxy,
                tls_egress_proxy_url=gateways.tls_egress_proxy_url,
            ),
            stdin_path=framework_prompt.prompt_path,
            stdout_path=stdout_path,
        )
        t1 = time.time()
        proxy_usage = collect_usage(gateways.active_proxy, t0, t1)
        filtered_proxy = gateways.filtered_proxy
        tls_egress = gateways.tls_egress

    if output_format == "json":
        write_claude_last_message(stdout_path, last_message_path)

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
    raw_usage = (
        parse_claude_usage(stdout_path) if output_format == "json" else proxy_usage
    )
    usage = finalize_usage(
        raw_usage,
        model=model,
        cost_source="provider" if output_format == "json" else "litellm",
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
