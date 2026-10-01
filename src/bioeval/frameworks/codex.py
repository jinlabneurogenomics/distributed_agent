"""Direct Codex framework command, authentication, and execution adapter."""

from __future__ import annotations

import contextlib
import json
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Iterable

from ..accounting.pricing import finalize_usage
from ..artifacts.results import write_framework_result
from ..models import FrameworkPrompt, FrameworkRunResult
from ..runtime import sandbox as runtime_sandbox
from ..runtime.gateways import framework_gateways
from ..runtime.paths import REPO_ROOT
from ..runtime.policy import SourcePolicy
from ..runtime.source_policy import audit_protected_run, filtered_codex_config
from .common import (
    ANALYSIS_ENV,
    ANALYSIS_ENV_BIN,
    DEFAULT_INPUT_ROOTS,
    DEFAULT_MODEL_PROXY_BRIDGE,
    apply_tls_egress_env,
    check_expected_outputs,
    run_subprocess_with_log,
)

DEFAULT_CODEX_MODEL = "gpt-rosalind-5.5"
DEFAULT_CODEX_SANDBOX = "workspace-write"
CODEX_SANDBOXES = ("read-only", "workspace-write", "danger-full-access")
DEFAULT_CODEX_AUTH = "chatgpt"
CODEX_AUTHS = ("chatgpt", "apikey")
DEFAULT_CODEX_BWRAP = True
CODEX_CHATGPT_CACHE_FILES = (
    "cloud-config-bundle-cache.json",
    "cloud-requirements-cache.json",
    "models_cache.json",
    "installation_id",
)
CODEX_PROTECTED_DISABLED_FEATURES = (
    "standalone_web_search",
    "browser_use",
    "browser_use_external",
    "browser_use_full_cdp_access",
    "computer_use",
    "in_app_browser",
    "apps",
    "plugins",
    "remote_plugin",
)
PROTECTED_SHELL_ENV_KEYS = (
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "http_proxy",
    "https_proxy",
    "NO_PROXY",
    "no_proxy",
    "SSL_CERT_FILE",
    "REQUESTS_CA_BUNDLE",
    "CURL_CA_BUNDLE",
    "NODE_EXTRA_CA_CERTS",
    "GIT_SSL_CAINFO",
)
BASE_SHELL_ENV_KEYS = ("PATH", "HOME", "TMPDIR", "LANG", "LC_ALL")


def codex_command(
    run_dir: Path,
    *,
    model: str = DEFAULT_CODEX_MODEL,
    sandbox: str = DEFAULT_CODEX_SANDBOX,
    codex_executable: str = "codex",
    auth: str = DEFAULT_CODEX_AUTH,
    network_access: bool = True,
    config_overrides: Iterable[str] = (),
    enable_features: Iterable[str] = (),
    disable_features: Iterable[str] = (),
    ephemeral: bool = False,
    strict_config: bool = False,
    ignore_rules: bool = False,
    resume_session_id: str | None = None,
    last_message_path: Path | None = None,
) -> list[str]:
    """Build the Codex CLI command used for prompt eval runs.

    ``--json`` is always emitted so the per-run token usage is recoverable from
    the JSONL ``turn.completed`` events (see ``parse_codex_usage``); the final
    agent message still lands in ``last_message.txt`` via ``--output-last-message``.

    ``--cd run_dir`` makes the agent's working directory the clean per-run output
    dir rather than the repo root, so a bare ``ls`` no longer surfaces the eval's
    own source tree. Under ``workspace-write`` this also scopes Codex's writable
    root to ``run_dir``. (Read isolation from the GT/graders is enforced
    separately by the bwrap fairness wrapper — Codex's own sandbox never
    restricts reads.)

    ``network_access=True`` lets shell commands reach the network under
    ``workspace-write`` (off by default in that mode); other sandbox modes ignore
    the flag.

    ``auth='apikey'`` injects a scoped OpenAI ``model_provider`` that authenticates
    with ``OPENAI_API_KEY`` instead of the codex ChatGPT login. This is required
    for restricted models (e.g. ``gpt-rosalind-260428``) that a ChatGPT account
    cannot call, and it bills the run to that API key. The override is passed
    only on this invocation; the user's global codex auth is untouched.
    """
    # --skip-git-repo-check: under the allowlist sandbox run_dir is not a git repo
    # (the repo's .git is not mounted), so codex's trusted-dir check must be
    # bypassed; harmless for unsandboxed runs too.
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
    for feature in enable_features:
        cmd.extend(["--enable", feature])
    for feature in disable_features:
        cmd.extend(["--disable", feature])
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
        # ``codex exec resume`` has no --sandbox flag. Preserve the original
        # session policy explicitly through the equivalent config key; the
        # outer fairness bwrap remains the authoritative filesystem boundary.
        cmd.extend(["--config", f"sandbox_mode={json.dumps(sandbox)}"])
    message_path = last_message_path or (run_dir / "last_message.txt")
    cmd.extend(["--output-last-message", str(message_path)])
    if resume_session_id:
        cmd.extend([resume_session_id, "-"])
    else:
        cmd.append("-")
    return cmd


def stage_chatgpt_codex_state(
    destination: Path,
    *,
    source: Path | None = None,
) -> tuple[Path, ...]:
    """Copy the minimal ChatGPT Codex state into an isolated writable home.

    The live ``~/.codex`` directory is never mounted. Codex may refresh signed
    policy and model metadata during startup, so each process receives its own
    writable snapshot containing only authentication and control-plane caches.
    Sessions, history, memories, plugins, and user configuration stay absent.
    """

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


@contextlib.contextmanager
def temporary_codex_home(
    *,
    auth: str,
    prefix: str = "bioeval-codex-home-",
):
    """Yield an isolated writable Codex home for one process."""

    with tempfile.TemporaryDirectory(prefix=prefix) as raw:
        destination = Path(raw)
        if auth == "chatgpt":
            stage_chatgpt_codex_state(destination)
        yield destination


def codex_env(
    *,
    auth: str = DEFAULT_CODEX_AUTH,
    cwd: Path | None = None,
    fairness_sandbox: bool = DEFAULT_CODEX_BWRAP,
    extra: dict[str, str] | None = None,
    tls_egress_proxy_url: str | None = None,
) -> dict[str, str]:
    """Environment for Codex runs.

    Sandboxed + ``apikey``: a scrubbed env carrying only ``OPENAI_API_KEY``
    (backfilled from the repo ``.env`` when not exported). Sandboxed + ``chatgpt``:
    a scrubbed env with NO ``OPENAI_API_KEY`` (so codex uses the ChatGPT token from
    the mounted ``~/.codex/auth.json`` rather than falling into apikey mode).
    Unsandboxed escape hatch: inherit the parent env and backfill sibling keys from
    ``.env`` for apikey auth.
    """
    if not fairness_sandbox:
        env = os.environ.copy()
        if auth == "apikey" and not env.get("OPENAI_API_KEY"):
            from dotenv import dotenv_values

            env_path = (cwd or Path.cwd()) / ".env"
            if env_path.exists():
                for key, value in dotenv_values(env_path).items():
                    if value is not None and not env.get(key):
                        env[key] = value
        if extra:
            env.update(extra)
        if tls_egress_proxy_url:
            apply_tls_egress_env(env, proxy_url=tls_egress_proxy_url)
        return env
    if auth == "chatgpt":
        # ChatGPT auth uses the token in the mounted auth.json; an OPENAI_API_KEY
        # in the env would flip codex into apikey mode, so leave it out.
        env = runtime_sandbox.clean_env(extra=extra)
        if tls_egress_proxy_url:
            apply_tls_egress_env(env, proxy_url=tls_egress_proxy_url)
        return env
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        from dotenv import dotenv_values

        env_path = (cwd or REPO_ROOT) / ".env"
        if env_path.exists():
            key = dotenv_values(env_path).get("OPENAI_API_KEY")
    clean_extra = {"OPENAI_API_KEY": key} if key else {}
    if extra:
        clean_extra.update(extra)
    env = runtime_sandbox.clean_env(extra=clean_extra)
    if tls_egress_proxy_url:
        apply_tls_egress_env(env, proxy_url=tls_egress_proxy_url)
    return env


def parse_codex_usage(events_path: Path) -> dict | None:
    """Aggregate token usage from a Codex ``--json`` JSONL event stream.

    Codex emits one ``turn.completed`` event per turn carrying a ``usage`` object
    (``input_tokens``, ``cached_input_tokens``, ``output_tokens``,
    ``reasoning_output_tokens``). Summed across turns this mirrors the usage shape
    ``_print_prompt_result`` / ``runner_result.json`` use for the other
    frameworks. Codex reports no dollar cost in the stream, so ``cost_usd`` is 0
    and the row is flagged ``cost_unconfigured``.
    """
    try:
        text = events_path.read_text()
    except OSError:
        return None
    input_tokens = cached_tokens = output_tokens = reasoning_tokens = 0
    turns = 0
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
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
        "cost_usd": 0.0,
        "cost_unconfigured": True,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cache_read_input_tokens": cached_tokens,
        "reasoning_output_tokens": reasoning_tokens,
    }


def parse_distributed_agents_codex_usage(run_dir: Path) -> tuple[dict | None, str | None]:
    """Read native backend usage/model recorded by DistributedAgents' own pipeline."""
    try:
        payload = json.loads((run_dir / "run.json").read_text())
    except (OSError, json.JSONDecodeError):
        return None, None
    if not isinstance(payload, dict) or payload.get("backend") not in {"codex", "api"}:
        return None, None
    usage = payload.get("usage")
    return (
        usage if isinstance(usage, dict) else None,
        str(payload["model"]) if payload.get("model") else None,
    )


def codex_run_command(
    run_dir: Path,
    *,
    model: str = DEFAULT_CODEX_MODEL,
    sandbox: str = DEFAULT_CODEX_SANDBOX,
    codex_executable: str = "codex",
    auth: str = DEFAULT_CODEX_AUTH,
    bwrap: bool = DEFAULT_CODEX_BWRAP,
    input_roots: Iterable[Path] = DEFAULT_INPUT_ROOTS,
    config_overrides: Iterable[str] = (),
    enable_features: Iterable[str] = (),
    disable_features: Iterable[str] = (),
    ephemeral: bool = False,
    strict_config: bool = False,
    ignore_rules: bool = False,
    sandbox_binds: Iterable[tuple[str, str, bool]] = (),
    mount_chatgpt_auth: bool = True,
    network_access: bool = True,
    network_isolated: bool = False,
    literature_gate_host_dir: Path | None = None,
    tls_egress_gate_host_dir: Path | None = None,
    biokg_gate_host_dir: Path | None = None,
    resume_session_id: str | None = None,
    last_message_path: Path | None = None,
) -> list[str]:
    """Full argv for a Codex run, wrapped in the allowlist fairness sandbox.

    Mounts only the declared ``input_roots`` + the codex binary read-only and
    ``run_dir`` read-write; the tmpfs ``$HOME`` denies ``~/.codex``
    (memories, history, sessions), so codex runs with none of its own
    cross-session state — the same leak class the old blocklist left open.

    ``apikey`` auth works out of the box (OPENAI_API_KEY injected via env).
    Callers should stage ChatGPT authentication and control-plane caches in a
    temporary writable Codex home and pass it through ``sandbox_binds`` with
    ``mount_chatgpt_auth=False``. The legacy direct-file mount remains available
    to command-construction callers.
    ``bwrap=False`` is a debug escape hatch with no filesystem sandbox.
    """
    if network_isolated and not bwrap:
        raise ValueError("network-isolated Codex requires the fairness sandbox")
    if network_isolated and tls_egress_gate_host_dir is None:
        raise ValueError("network-isolated Codex requires a TLS egress gateway")
    if not bwrap:
        return codex_command(
            run_dir,
            model=model,
            sandbox=sandbox,
            codex_executable=codex_executable,
            auth=auth,
            config_overrides=config_overrides,
            enable_features=enable_features,
            disable_features=disable_features,
            ephemeral=ephemeral,
            strict_config=strict_config,
            ignore_rules=ignore_rules,
            network_access=network_access,
            resume_session_id=resume_session_id,
            last_message_path=last_message_path,
        )
    # Invoke the resolved binary by absolute path so it runs without relying on
    # the launcher's ~/.codex lookup (which the sandbox hides).
    which = shutil.which(codex_executable)
    real = str(Path(which).resolve()) if which else codex_executable
    cmd = codex_command(
        run_dir,
        model=model,
        sandbox=sandbox,
        codex_executable=real,
        auth=auth,
        config_overrides=config_overrides,
        enable_features=enable_features,
        disable_features=disable_features,
        ephemeral=ephemeral,
        strict_config=strict_config,
        ignore_rules=ignore_rules,
        network_access=network_access,
        resume_session_id=resume_session_id,
        last_message_path=last_message_path,
    )
    toolchain = runtime_sandbox.codex_toolchain_paths(codex_executable)
    bin_dir = str(toolchain[0]) if toolchain else None
    # (B1) analysis env first on PATH so `python` has the pandas/duckdb stack.
    parts = (
        [str(ANALYSIS_ENV_BIN)] + ([bin_dir] if bin_dir else []) + ["/usr/bin", "/bin"]
    )
    # Legacy command-only path: bind the credential and policy cache read-only.
    # Runtime callers use ``temporary_codex_home`` instead so model metadata can
    # refresh without racing on the user's live state.
    resolved_binds: list[tuple[str, str, bool]] = []
    if auth == "chatgpt" and mount_chatgpt_auth:
        codex_home = Path.home() / ".codex"
        for filename in ("auth.json", "cloud-config-bundle-cache.json"):
            source = codex_home / filename
            if source.exists():
                resolved_binds.append(
                    (
                        str(source),
                        f"{runtime_sandbox.FAKE_HOME}/.codex/{filename}",
                        True,
                    )
                )
    resolved_binds.extend(sandbox_binds)
    if network_isolated:
        inner_cmd = cmd
        cmd = [
            "/usr/bin/python3",
            str(DEFAULT_MODEL_PROXY_BRIDGE),
            "--socket",
            runtime_sandbox.TLS_EGRESS_GATE_SOCKET,
            "--port",
            str(runtime_sandbox.TLS_EGRESS_GATE_PORT),
        ]
        if literature_gate_host_dir is not None:
            cmd.extend(
                [
                    "--relay",
                    (
                        f"{runtime_sandbox.LITERATURE_GATE_PORT}:"
                        f"{runtime_sandbox.LITERATURE_GATE_SOCKET}"
                    ),
                ]
            )
        if biokg_gate_host_dir is not None:
            cmd.extend(
                [
                    "--relay",
                    f"{runtime_sandbox.BIOKG_GATE_PORT}:{runtime_sandbox.BIOKG_GATE_SOCKET}",
                ]
            )
        cmd.extend(["--", *inner_cmd])
        resolved_binds.append(
            (
                str(tls_egress_gate_host_dir),
                runtime_sandbox.TLS_EGRESS_GATE_DIR,
                False,
            )
        )
        if literature_gate_host_dir is not None:
            resolved_binds.append(
                (
                    str(literature_gate_host_dir),
                    runtime_sandbox.LITERATURE_GATE_DIR,
                    False,
                )
            )
        if biokg_gate_host_dir is not None:
            resolved_binds.append(
                (
                    str(biokg_gate_host_dir),
                    runtime_sandbox.BIOKG_GATE_DIR,
                    False,
                )
            )
    bridge_paths = [DEFAULT_MODEL_PROXY_BRIDGE] if network_isolated else []
    return runtime_sandbox.bwrap_allowlist_command(
        cmd,
        chdir=str(run_dir),
        allow_ro=[
            ANALYSIS_ENV,
            *bridge_paths,
            *input_roots,
            *toolchain,
        ],
        allow_rw=[run_dir],
        path=":".join(parts),
        share_net=not network_isolated,
        extra_binds=resolved_binds,
    )


def run_codex_prompt(
    framework_prompt: FrameworkPrompt,
    *,
    model: str = DEFAULT_CODEX_MODEL,
    sandbox: str = DEFAULT_CODEX_SANDBOX,
    codex_executable: str = "codex",
    cwd: Path | None = None,
    auth: str = DEFAULT_CODEX_AUTH,
    bwrap: bool = DEFAULT_CODEX_BWRAP,
    input_roots: Iterable[Path] = DEFAULT_INPUT_ROOTS,
    source_policy: SourcePolicy | None = None,
    filtered_search_image: Path | None = None,
    apptainer_executable: str = "apptainer",
    track_cost: bool = True,
    developer_instructions: str | None = None,
    disable_features: Iterable[str] = (),
) -> FrameworkRunResult:
    """Run one rendered prompt through Codex CLI non-interactively.

    ``cwd`` is the host launch dir (repo root) used only to resolve ``.env`` for
    apikey auth; Codex's own working dir is ``run_dir`` via ``--cd``. ``bwrap``
    wraps the run in the allowlist fairness sandbox (mounts only input_roots +
    the codex binary; tmpfs $HOME hides ~/.codex).
    """
    log_path = framework_prompt.run_dir / "runner.log"
    events_path = framework_prompt.run_dir / "events.jsonl"
    policy_enabled = bool(source_policy and source_policy.enabled)
    literature_enabled = bool(
        policy_enabled and source_policy and source_policy.literature_access
    )
    if policy_enabled and not bwrap:
        raise ValueError("protected Codex runs require --codex-bwrap")
    if policy_enabled and sandbox != "workspace-write":
        raise ValueError("protected Codex runs require --codex-sandbox workspace-write")
    if literature_enabled and filtered_search_image is None:
        raise ValueError("protected Codex runs require a filtered-search SIF")

    with contextlib.ExitStack() as stack:
        staged_home = None
        if bwrap and auth == "chatgpt":
            staged_home = stack.enter_context(temporary_codex_home(auth=auth))
        gateways = stack.enter_context(
            framework_gateways(
                run_dir=framework_prompt.run_dir,
                source_policy=source_policy,
                filtered_search_image=filtered_search_image,
                apptainer_executable=apptainer_executable,
                proxy_context=contextlib.nullcontext(None),
                # Codex reports native token usage. Its ChatGPT-auth transport
                # cannot use the LiteLLM model gateway, so protected Codex sends
                # that transport through the filtered TLS egress gateway.
                require_model_gateway=False,
            )
        )
        config_overrides: tuple[str, ...] = ()
        if gateways.filtered_mcp_url is not None:
            config_overrides = filtered_codex_config(gateways.filtered_mcp_url)
        if policy_enabled:
            # `codex_env` puts the proxy and CA settings on the codex process,
            # but codex filters the shell tool's own environment, so without
            # this the agent's subprocesses see no proxy and every outbound
            # request dies as "Operation not permitted" rather than reaching
            # the audited gateway.
            shell_env_keys = (
                *BASE_SHELL_ENV_KEYS,
                "DISTRIBUTED_AGENTS_*",
                "BIOKG_*",
                *(PROTECTED_SHELL_ENV_KEYS if literature_enabled else ()),
            )
            config_overrides = (
                *config_overrides,
                'shell_environment_policy.inherit="all"',
                "shell_environment_policy.include_only="
                + json.dumps(list(shell_env_keys)),
            )
        if developer_instructions is not None:
            config_overrides = (
                *config_overrides,
                "developer_instructions="
                + json.dumps(developer_instructions, ensure_ascii=True),
            )
        disabled_features = tuple(
            dict.fromkeys(
                (
                    *(CODEX_PROTECTED_DISABLED_FEATURES if policy_enabled else ()),
                    *disable_features,
                )
            )
        )
        sandbox_binds: tuple[tuple[str, str, bool], ...] = ()
        runtime_env: dict[str, str] = {}
        if staged_home is not None:
            sandbox_binds = (
                (str(staged_home), f"{runtime_sandbox.FAKE_HOME}/.codex", False),
            )
            runtime_env["CODEX_HOME"] = f"{runtime_sandbox.FAKE_HOME}/.codex"
        cmd = codex_run_command(
            framework_prompt.run_dir,
            model=model,
            sandbox=sandbox,
            codex_executable=codex_executable,
            auth=auth,
            bwrap=bwrap,
            input_roots=input_roots,
            config_overrides=config_overrides,
            disable_features=disabled_features,
            sandbox_binds=sandbox_binds,
            mount_chatgpt_auth=staged_home is None,
            # The outer bwrap namespace is the protected network boundary: with
            # network_isolated the process gets an empty netns whose only routes
            # are the audited loopback relays. Codex's own sandbox flag is a
            # second, redundant block that denies socket() outright with EPERM,
            # so leaving it off made those relays unreachable from shell tools
            # and every live fetch failed as "Operation not permitted". The
            # DistributedAgents query backend has always passed True here for exactly
            # this reason; this path was the outlier.
            network_access=True,
            network_isolated=policy_enabled,
            literature_gate_host_dir=gateways.literature_gate_host_dir,
            tls_egress_gate_host_dir=gateways.tls_egress_gate_host_dir,
            strict_config=policy_enabled,
        )
        t0 = time.time()
        returncode = run_subprocess_with_log(
            cmd,
            log_path=log_path,
            cwd=cwd,
            env=codex_env(
                auth=auth,
                cwd=cwd,
                fairness_sandbox=bwrap,
                extra=runtime_env,
                tls_egress_proxy_url=gateways.tls_egress_proxy_url,
            ),
            stdin_path=framework_prompt.prompt_path,
            stdout_path=events_path,
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
    usage = finalize_usage(
        parse_codex_usage(events_path),
        model=model,
        cost_source="tokens",
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
