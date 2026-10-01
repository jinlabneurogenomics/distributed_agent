"""Codex execution for the open-ended DistributedAgents query harness."""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from ...runtime import sandbox
from ...runtime.events import codex_thread_id, parse_codex_events
from ...runtime.codex import (
    codex_env,
    codex_run_command,
    parse_codex_usage,
    run_subprocess_with_log,
    stage_chatgpt_codex_state,
)

from ..adaptive import (
    prepare_adaptive_context,
)
from ..audit import audit_adaptive_artifacts
from ...skills.registry import (
    load_local_skills_dirs,
    resolve_skills,
    write_active_skills_index,
)
from ...corpus.registry import (
    DEFAULT_RELEASE_ENV,
    CorpusRelease,
    get_release,
)
from ..context import (
    canonical_dataset_context_path,
    sha256_path,
    snapshot_dataset_context,
)
from ..access import (
    CORPUS_MCP_PYTHON,
    CORPUS_MCP_SERVER_PATH,
    _codex_passthrough_env,
    _codex_runtime_access_plan,
    _preflight_release_runtime,
)
from ..contracts import render_query_contract
from ..errors import CodexQueryError
from ..models import (
    CODEX_AUTH_MODES,
    CODEX_REASONING_EFFORTS,
    CODEX_SANDBOX_MODES,
    CodexQueryOptions,
    QueryRequest,
    QueryResult,
    QueryRunStatus,
)

_BIOKG_PREFLIGHT_HTTP_URL_ENV = "DISTRIBUTED_AGENTS_BIOKG_PREFLIGHT_HTTP_URL"
@contextlib.contextmanager
def _codex_query_home(options: CodexQueryOptions):
    """Yield either a one-shot temporary home or an explicit persistent home."""

    if options.session_home is None:
        with tempfile.TemporaryDirectory(prefix="distributed_agents-codex-home-") as raw:
            yield Path(raw)
        return
    home = options.session_home.expanduser().resolve()
    home.mkdir(parents=True, exist_ok=True)
    yield home


def run_codex_query(request: QueryRequest, *, model: str) -> QueryResult:
    options = request.codex
    multi_agent = request.mode == "adaptive"
    if request.out_dir is None:
        raise ValueError(
            "the Codex query backend requires out_dir for durable artifacts"
        )
    if options.auth not in CODEX_AUTH_MODES:
        raise ValueError(f"unknown Codex auth mode {options.auth!r}")
    if options.sandbox not in CODEX_SANDBOX_MODES:
        raise ValueError(f"unknown Codex sandbox {options.sandbox!r}")
    if options.reasoning_effort not in CODEX_REASONING_EFFORTS:
        raise ValueError(f"unknown Codex reasoning effort {options.reasoning_effort!r}")
    if options.max_concurrent_subagents < 1:
        raise ValueError("Codex max_concurrent_subagents must be at least 1")
    if options.max_subagents < options.max_concurrent_subagents:
        raise ValueError(
            "Codex max_subagents must be at least max_concurrent_subagents"
        )
    _validate_codex_config_overrides(options.config_overrides)
    if options.sandbox == "read-only":
        raise ValueError("Codex dataset orchestration requires a writable sandbox")
    if options.resume_session_id and options.session_home is None:
        raise ValueError("resuming a Codex query requires a persistent session_home")
    if (
        options.auth == "chatgpt"
        and not (Path.home() / ".codex" / "auth.json").is_file()
    ):
        raise CodexQueryError("ChatGPT Codex auth not found; run `codex login` first")

    run_dir = request.out_dir.expanduser().resolve()
    run_dir.mkdir(parents=True, exist_ok=True)
    working_directory = (
        request.working_directory.expanduser().resolve()
        if request.working_directory is not None
        else Path.cwd().resolve()
    )
    if options.session_home is not None:
        session_home = options.session_home.expanduser().resolve()
        if (
            session_home == run_dir
            or session_home.is_relative_to(run_dir)
            or run_dir.is_relative_to(session_home)
        ):
            raise ValueError(
                "persistent session_home and the agent-visible run directory "
                "must not overlap"
            )
    codex_version = _codex_preflight(
        options.executable,
        require_multi_agent=multi_agent,
    )
    corpus_release = get_release(request.corpus_release)

    custom_skills_destination = bool(request.skills_destination)
    skills_destination, skills_index, skill_dirs = resolve_skills(
        request.skills_destination,
        request.skills_index_container_path,
        include_project=True,
        corpus_release=corpus_release,
    )
    runtime_dir = run_dir / "codex_runtime"
    pipeline_dir = runtime_dir / "pipeline"
    dataset_context_path = pipeline_dir / "dataset_context.md"
    dataset_context_manifest_path = pipeline_dir / "dataset_context.json"
    snapshot_dataset_context(
        canonical_dataset_context_path(Path(skills_destination)),
        dataset_context_path,
        dataset_context_manifest_path,
    )
    local_skills = load_local_skills_dirs(skill_dirs, query_role=True)
    if request.mode == "adaptive":
        workflow_skills = {"adaptive-query-skill", "dataset-orchestrator-skill"}
        local_skills = [
            skill
            for skill in local_skills
            if Path(skill["path"]).name not in workflow_skills
        ]
    if not custom_skills_destination:
        skills_index = str(
            write_active_skills_index(
                runtime_dir / "SKILLS_INDEX.md",
                skills=local_skills,
            )
        )
    # Preserve the caller's task verbatim.  The selected dataset portrait is a
    # separate, hashed framework input so evaluation wording remains identical
    # across frameworks.
    task_input = request.query
    task_path = run_dir / "task.md"
    task_path.write_text(task_input)
    runtime_env = _codex_passthrough_env(run_dir)
    runtime_env[DEFAULT_RELEASE_ENV] = corpus_release.release_id
    runtime_env["DISTRIBUTED_AGENTS_PIPELINE_DIR"] = str(pipeline_dir)
    runtime_env["DISTRIBUTED_AGENTS_MAX_CONCURRENT_SUBAGENTS"] = str(
        options.max_concurrent_subagents if multi_agent else 0
    )
    runtime_env["DISTRIBUTED_AGENTS_MAX_SUBAGENTS"] = str(
        options.max_subagents if multi_agent else 0
    )
    access_plan = _codex_runtime_access_plan(
        skill_dirs,
        runtime_env,
        task_input_roots=options.input_roots,
        include_packaged_skills=not bool(request.skills_destination),
        corpus_release=corpus_release,
    )
    input_roots = access_plan.effective_roots
    capability_preflight = _preflight_release_runtime(
        access_plan,
        pipeline_dir=pipeline_dir,
        runtime_env=runtime_env,
        bwrap=options.bwrap,
    )
    adaptive_context = prepare_adaptive_context(
        mode=request.mode,
        release=corpus_release,
        task_path=task_path,
        dataset_context_path=dataset_context_path,
        pipeline_dir=pipeline_dir,
        skills_destination=skills_destination,
        runtime_env=runtime_env,
        input_roots=input_roots,
        declared_inputs=options.input_roots,
        capability_preflight=capability_preflight,
        biokg_preflight_http_url=(
            os.environ.get(_BIOKG_PREFLIGHT_HTTP_URL_ENV) or None
        ),
    )
    contract = render_query_contract(
        request,
        runtime_dir=runtime_dir,
        skills_destination=skills_destination,
        skills_index=skills_index,
        adaptive_context=adaptive_context,
    )
    contracts_dir = runtime_dir / "contracts"
    contracts_dir.mkdir(parents=True, exist_ok=True)
    rendered_contracts = {"root": contract}
    (contracts_dir / "root.md").write_text(contract)

    main_config = _main_codex_config(
        contract,
        local_skills=local_skills,
        reasoning_effort=options.reasoning_effort,
        multi_agent=multi_agent,
        max_threads=(options.max_concurrent_subagents + 1 if multi_agent else 1),
        corpus_release=corpus_release,
        capability_manifest=adaptive_context.capability_manifest,
    )
    config_path = runtime_dir / "config.toml"
    config_path.write_text(main_config)

    events_path = run_dir / "events.jsonl"
    log_path = run_dir / "runner.log"
    last_message_path = run_dir / "last_message.txt"
    started = time.time()
    with _codex_query_home(options) as codex_home:
        shutil.copy2(config_path, codex_home / "config.toml")
        if options.auth == "chatgpt":
            try:
                stage_chatgpt_codex_state(codex_home)
            except FileNotFoundError as exc:
                raise CodexQueryError(
                    "ChatGPT Codex auth not found; run `codex login` first"
                ) from exc

        sandbox_binds: tuple[tuple[str, str, bool], ...] = ()
        if options.bwrap:
            # Codex refreshes signed policy/model caches during startup. Mount
            # only the isolated home read-write so those refreshes and optional
            # chat sessions work while the user's real ~/.codex stays outside.
            sandbox_binds = ((str(codex_home), f"{sandbox.FAKE_HOME}/.codex", False),)
            runtime_env["CODEX_HOME"] = f"{sandbox.FAKE_HOME}/.codex"
        else:
            runtime_env["CODEX_HOME"] = str(codex_home)

        cmd = codex_run_command(
            run_dir,
            model=model,
            sandbox=options.sandbox,
            codex_executable=options.executable,
            auth=options.auth,
            bwrap=options.bwrap,
            input_roots=input_roots,
            ephemeral=options.session_home is None,
            strict_config=True,
            ignore_rules=True,
            sandbox_binds=sandbox_binds,
            config_overrides=options.config_overrides,
            network_access=True,
            resume_session_id=options.resume_session_id,
        )
        env = codex_env(
            auth=options.auth,
            cwd=working_directory,
            fairness_sandbox=options.bwrap,
            extra=runtime_env,
        )
        returncode = run_subprocess_with_log(
            cmd,
            log_path=log_path,
            cwd=working_directory,
            env=env,
            stdin_path=task_path,
            stdout_path=events_path,
            timeout_seconds=options.timeout_seconds or None,
        )
    duration_s = round(time.time() - started, 2)

    event_summary = parse_codex_events(events_path)
    thread_id = codex_thread_id(events_path) or options.resume_session_id
    warnings = list(event_summary.warnings)
    adaptive_artifact_audit = audit_adaptive_artifacts(
        mode=request.mode,
        pipeline_dir=pipeline_dir,
        capability_manifest=(
            adaptive_context.capability_manifest if adaptive_context else None
        ),
    )
    warnings.extend(
        str(value)
        for value in adaptive_artifact_audit.get("warnings", [])
        if str(value).strip()
    )
    if not multi_agent and event_summary.subagents_started:
        warnings.append(
            "direct query unexpectedly delegated to "
            f"{event_summary.subagents_started} subagent(s)"
        )
    answer = last_message_path.read_text() if last_message_path.is_file() else ""
    status: QueryRunStatus = "completed"
    failure_reasons: list[str] = list(event_summary.errors)
    failure_reasons.extend(
        str(value)
        for value in adaptive_artifact_audit.get("blocking_errors", [])
        if str(value).strip()
    )
    if not multi_agent and event_summary.subagents_started:
        failure_reasons.append("direct query used a subagent while delegation was disabled")
    if multi_agent and event_summary.subagents_started > options.max_subagents:
        failure_reasons.append(
            "adaptive query exceeded its logical subagent budget: "
            f"{event_summary.subagents_started} > {options.max_subagents}"
        )
    if returncode:
        failure_reasons.append(
            "Codex timed out"
            if returncode == 124
            else f"Codex exited with status {returncode}"
        )
    if event_summary.failed_turns:
        failure_reasons.append(f"{event_summary.failed_turns} Codex turn(s) failed")
    if not event_summary.completed_turns:
        failure_reasons.append("Codex emitted no turn.completed event")
    if not answer.strip():
        failure_reasons.append("Codex produced no final message")
    if failure_reasons:
        status = "failed"
    elif warnings:
        status = "completed_with_warnings"

    if answer:
        (run_dir / "query.md").write_text(answer)
    usage = parse_codex_usage(events_path)
    artifact_paths = {
        "answer": str(run_dir / "query.md"),
        "task": str(task_path),
        "events": str(events_path),
        "last_message": str(last_message_path),
        "runner_log": str(log_path),
        "runtime_config": str(config_path),
        "capability_preflight": str(pipeline_dir / "capability_preflight.json"),
    }
    for name in ("task_profile", "claim_recall", "task_plan", "final_ranking"):
        path = pipeline_dir / f"{name}.json"
        if path.is_file():
            artifact_paths[name] = str(path)
    for name, path in {
        "dataset_context": pipeline_dir / "dataset_context.md",
        "dataset_context_manifest": pipeline_dir / "dataset_context.json",
        "claim_graph_memberships": pipeline_dir / "claim_graph_memberships.tsv",
        "final_ranking_validation": pipeline_dir / "final_ranking_validation.json",
        "ranking_catalog": pipeline_dir / "ranking_handoff" / "ranking_catalog.json",
        "story_catalog": pipeline_dir / "ranking_handoff" / "story_catalog.md",
        "hub_catalog": pipeline_dir / "ranking_handoff" / "hub_catalog.md",
        "evidence_index": pipeline_dir / "ranking_handoff" / "evidence_index.json",
        "ranking_context": pipeline_dir / "ranking_handoff" / "ranking_context.md",
        "report": run_dir / "report.md",
    }.items():
        if path.is_file():
            artifact_paths[name] = str(path)
    adaptive_artifacts = adaptive_artifact_audit.get("artifacts")
    if isinstance(adaptive_artifacts, dict):
        artifact_paths.update(
            {
                str(name): str(path)
                for name, path in adaptive_artifacts.items()
                if str(path).strip()
            }
        )

    ranking_telemetry: dict[str, object] = {}
    final_ranking_path = pipeline_dir / "final_ranking.json"
    if final_ranking_path.is_file():
        try:
            final_ranking = json.loads(final_ranking_path.read_text())
        except (OSError, json.JSONDecodeError):
            final_ranking = {}
        if isinstance(final_ranking, dict):
            ranked = final_ranking.get("ranked")
            opened = final_ranking.get("opened_evidence")
            ranking_telemetry = {
                "schema_version": final_ranking.get("schema_version"),
                "status": final_ranking.get("status"),
                "input_story_count": final_ranking.get("input_story_count"),
                "ranked": len(ranked) if isinstance(ranked, list) else None,
                "ranked_hubs": (
                    sum(
                        isinstance(row, dict) and row.get("candidate_type") != "story"
                        for row in ranked
                    )
                    if isinstance(ranked, list)
                    else None
                ),
                "opened_evidence": (len(opened) if isinstance(opened, list) else None),
            }

    manifest = {
        "backend": "codex",
        "mode": request.mode,
        "status": status,
        "model": model,
        "auth": options.auth,
        "codex_version": codex_version,
        "returncode": returncode,
        "duration_s": duration_s,
        "usage": usage,
        "warnings": warnings,
        "errors": list(dict.fromkeys(failure_reasons)),
        "subagents": {
            "started": event_summary.subagents_started,
            "completed": event_summary.subagents_completed,
            "failed": event_summary.subagents_failed,
            "enabled": multi_agent,
            "max_threads": (
                options.max_concurrent_subagents + 1 if multi_agent else 1
            ),
            "max_concurrent": (
                options.max_concurrent_subagents if multi_agent else 0
            ),
            "max_total": options.max_subagents if multi_agent else 0,
        },
        "ranking": ranking_telemetry,
        "adaptive_artifact_audit": adaptive_artifact_audit,
        "adaptive_context": (
            {
                "skill_path": str(adaptive_context.skill_path),
                "capability_manifest": str(adaptive_context.capability_manifest),
                "coverage": (
                    str(adaptive_context.coverage)
                    if adaptive_context.coverage is not None
                    else None
                ),
                "preparation": adaptive_context.preparation,
            }
            if adaptive_context
            else None
        ),
        "sandbox": {
            "mode": options.sandbox,
            "bwrap": options.bwrap,
            "owner": "distributed_agents" if options.bwrap else "external",
        },
        "corpus_release": corpus_release.as_dict(),
        "runtime_access": access_plan.as_dict(),
        "session": {
            "persistent": options.session_home is not None,
            "thread_id": thread_id,
            "resumed": options.resume_session_id is not None,
        },
        "input_roots": [str(path) for path in input_roots],
        "working_directory": str(working_directory),
        "environment_keys": sorted(runtime_env),
        "contracts": {
            f"{name.replace('-', '_')}_sha256": _sha256(value)
            for name, value in rendered_contracts.items()
        },
        "doctrine": _doctrine_provenance(Path(skills_destination)),
        "source_revision": _source_revision(),
        "artifacts": artifact_paths,
        "command": cmd,
    }
    manifest_path = run_dir / "run.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    if status == "failed":
        detail = "; ".join(dict.fromkeys(failure_reasons))
        raise CodexQueryError(f"Codex query failed: {detail}; see {manifest_path}")
    return QueryResult(
        answer=answer,
        backend="codex",
        model=model,
        status=status,
        run_dir=run_dir,
        returncode=returncode,
        duration_s=duration_s,
        usage=usage,
        warnings=tuple(warnings),
        artifacts={key: str(value) for key, value in manifest["artifacts"].items()},
        thread_id=thread_id,
    )


def _main_codex_config(
    developer_instructions: str,
    *,
    local_skills: list[dict[str, str]],
    reasoning_effort: str,
    multi_agent: bool,
    max_threads: int,
    corpus_release: CorpusRelease | None = None,
    capability_manifest: Path | None = None,
) -> str:
    shell_env_keys = [
        "PATH",
        "HOME",
        "TMPDIR",
        "LANG",
        "LC_ALL",
        "DISTRIBUTED_AGENTS_*",
        "BIOKG_*",
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
    ]
    lines = [
        f"model_reasoning_effort = {_toml(reasoning_effort)}",
        f"developer_instructions = {_toml(developer_instructions)}",
        "project_doc_max_bytes = 0",
        'approval_policy = "never"',
        "",
        "[features]",
        f"multi_agent = {'true' if multi_agent else 'false'}",
        "goals = false",
        "memories = false",
        "plugins = false",
        "apps = false",
    ]
    if multi_agent:
        lines.extend(
            [
                "",
                "[agents]",
                f"max_threads = {max_threads}",
                "max_depth = 1",
            ]
        )
    lines.extend(
        [
            "",
            "[tools]",
            "web_search = true",
            "",
            "[shell_environment_policy]",
            'inherit = "all"',
            "include_only = [" + ", ".join(_toml(key) for key in shell_env_keys) + "]",
        ]
    )
    for skill in local_skills:
        lines.extend(
            [
                "",
                "[[skills.config]]",
                f"path = {_toml(skill['path'])}",
                "enabled = true",
            ]
        )
    if corpus_release is not None and capability_manifest is not None:
        lines.extend(
            [
                "",
                "[mcp_servers.distributed_agents_corpus]",
                f"command = {_toml(str(CORPUS_MCP_PYTHON))}",
                "args = ["
                + ", ".join(
                    _toml(value)
                    for value in (
                        str(CORPUS_MCP_SERVER_PATH),
                        "--release-manifest",
                        str(corpus_release.manifest_path),
                        "--capabilities",
                        str(capability_manifest),
                    )
                )
                + "]",
                "required = true",
                'default_tools_approval_mode = "approve"',
                "startup_timeout_sec = 30",
                "tool_timeout_sec = 60",
            ]
        )
    return "\n".join(lines) + "\n"


_RUNTIME_OWNED_CODEX_KEYS = {
    "agents.max_depth",
    "agents.max_threads",
    "features.multi_agent",
}


def _validate_codex_config_overrides(overrides: tuple[str, ...]) -> None:
    """Keep delegation policy and recorded limits owned by DistributedAgents."""

    for override in overrides:
        key = override.partition("=")[0].strip()
        if key in _RUNTIME_OWNED_CODEX_KEYS:
            raise ValueError(
                f"Codex config override {key!r} is runtime-owned; use the "
                "dedicated DistributedAgents subagent options"
            )


def _codex_preflight(executable: str, *, require_multi_agent: bool = False) -> str:
    resolved = shutil.which(executable)
    if resolved is None:
        raise CodexQueryError(f"Codex executable not found: {executable!r}")
    version_proc = subprocess.run(
        [resolved, "--version"],
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    version = (version_proc.stdout or version_proc.stderr).strip()
    if version_proc.returncode:
        raise CodexQueryError(f"failed to inspect Codex version: {version}")
    if require_multi_agent:
        features_proc = subprocess.run(
            [
                resolved,
                "features",
                "list",
                "--config",
                "features.multi_agent=true",
            ],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        feature_text = f"{features_proc.stdout}\n{features_proc.stderr}"
        enabled = bool(
            re.search(r"(?m)^multi_agent\s+\S+\s+true\s*$", feature_text)
        )
        if features_proc.returncode or not enabled:
            raise CodexQueryError(
                "this Codex installation does not expose native multi_agent "
                "support required by adaptive corpus sweeps"
            )
    return version


def _toml(value: str) -> str:
    return json.dumps(value, ensure_ascii=True)


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# The rendered contracts above are hashed, and the portrait carries its own
# manifest. Runtime skill doctrine and its gating scripts are also read live,
# so hash them to preserve the exact behavior visible to a run.
_DOCTRINE_FILES = (
    "REASONING_CONTRACT.md",
    "SKILL.md",
    "PLAYBOOKS.md",
    "scripts/profile_task.py",
    "scripts/validate_task_plan.py",
    "scripts/route_claims.py",
    "scripts/build_claim_attention.py",
)

_SWEEP_DOCTRINE_FILES = (
    "SKILL.md",
    "references/coordinator.md",
    "references/reader.md",
    "references/reduction.md",
    "scripts/_common.py",
    "scripts/plan_sweep.py",
    "scripts/validate_slice.py",
    "scripts/reconcile_sweep.py",
    "schemas/sweep_plan.schema.json",
    "schemas/slice_result.schema.json",
    "schemas/sweep_audit.schema.json",
)


def _doctrine_provenance(skills_destination: Path) -> dict[str, str]:
    """Hash the orchestrator and exhaustive-sweep doctrine visible to a run."""

    skill_root = canonical_dataset_context_path(skills_destination).parent
    provenance: dict[str, str] = {}
    for relative in _DOCTRINE_FILES:
        path = skill_root / relative
        key = relative.replace("scripts/", "").replace(".", "_").replace("-", "_")
        provenance[f"{key}_sha256"] = sha256_path(path) if path.is_file() else ""
    sweep_root = skill_root.parent / "exhaustive-corpus-sweep-skill"
    for relative in _SWEEP_DOCTRINE_FILES:
        path = sweep_root / relative
        key = relative.replace("/", "_").replace(".", "_").replace("-", "_")
        provenance[f"corpus_sweep_{key}_sha256"] = (
            sha256_path(path) if path.is_file() else ""
        )
    return provenance


def _source_revision() -> dict[str, object]:
    """Record the checked-out commit and whether tracked files were modified."""

    repo = Path(__file__).resolve().parents[2]

    def git(*args: str) -> str | None:
        try:
            done = subprocess.run(
                ("git", "-C", str(repo), *args),
                capture_output=True,
                text=True,
                check=False,
                timeout=15,
            )
        except (OSError, subprocess.SubprocessError):
            return None
        return done.stdout.strip() if done.returncode == 0 else None

    commit = git("rev-parse", "HEAD")
    porcelain = git("status", "--porcelain", "--untracked-files=no")
    return {
        "commit": commit or "",
        "dirty": bool(porcelain) if porcelain is not None else None,
        "dirty_tracked_files": len(porcelain.splitlines()) if porcelain else 0,
    }
