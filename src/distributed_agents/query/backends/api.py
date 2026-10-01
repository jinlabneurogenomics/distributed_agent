"""Direct OpenAI Agents SDK query backend."""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

from ...corpus.registry import DEFAULT_RELEASE_ENV, get_release
from ...runtime.agent_shell import make_local_shell_executor
from ...skills.registry import (
    load_local_skills_dirs,
    resolve_skills,
    write_active_skills_index,
)
from ..adaptive import prepare_adaptive_context
from ..audit import audit_adaptive_artifacts
from ..context import (
    canonical_dataset_context_path,
    sha256_path,
    snapshot_dataset_context,
)
from ..contracts import render_query_contract
from ..errors import ApiQueryError
from ..models import API_REASONING_EFFORTS, QueryRequest, QueryResult


def _resolved_input_roots(request: QueryRequest) -> tuple[Path, ...]:
    roots: list[Path] = []
    for value in request.api.input_roots or ():
        path = value.expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(f"declared query input does not exist: {path}")
        if path not in roots:
            roots.append(path)
    return tuple(roots)


def _usage_dict(result: Any) -> dict[str, int] | None:
    usage = getattr(getattr(result, "context_wrapper", None), "usage", None)
    if usage is None:
        return None
    values: dict[str, int] = {}
    for name in ("requests", "input_tokens", "output_tokens", "total_tokens"):
        value = getattr(usage, name, None)
        if isinstance(value, int):
            values[name] = value
    return values or None


def _flush_traces() -> None:
    if os.environ.get("DISTRIBUTED_AGENTS_TRACE_FLUSH", "1").strip().lower() in {
        "0",
        "false",
        "no",
        "off",
    }:
        return
    try:
        from agents import flush_traces

        flush_traces()
    except Exception:
        pass


def _sweep_skill_path(local_skills: list[dict[str, str]]) -> Path | None:
    for skill in local_skills:
        if skill.get("name") == "exhaustive-corpus-sweep-skill":
            path = Path(skill["path"]).expanduser().resolve()
            if (path / "SKILL.md").is_file():
                return path
    return None


def _sweep_doctrine_provenance(skill_path: Path | None) -> dict[str, str]:
    if skill_path is None:
        return {}
    files = (
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
    return {
        relative.replace("/", "_").replace(".", "_") + "_sha256": (
            sha256_path(skill_path / relative)
            if (skill_path / relative).is_file()
            else ""
        )
        for relative in files
    }


def run_api_query(request: QueryRequest, *, model: str) -> QueryResult:
    """Run one query directly through the OpenAI Agents SDK."""

    if request.out_dir is None:
        raise ValueError("the API query backend requires out_dir for durable artifacts")
    options = request.api
    if options.reasoning_effort not in API_REASONING_EFFORTS:
        raise ValueError(
            f"unknown API reasoning effort {options.reasoning_effort!r}; "
            f"choose from {API_REASONING_EFFORTS}"
        )
    if options.max_turns < 1:
        raise ValueError("API max_turns must be at least 1")
    if options.max_concurrent_subagents < 1:
        raise ValueError("API max_concurrent_subagents must be at least 1")
    if options.max_subagents < options.max_concurrent_subagents:
        raise ValueError(
            "API max_subagents must be at least max_concurrent_subagents"
        )
    multi_agent = request.mode == "adaptive"

    started = time.time()
    run_dir = request.out_dir.expanduser().resolve()
    run_dir.mkdir(parents=True, exist_ok=True)
    runtime_dir = run_dir / "api_runtime"
    pipeline_dir = runtime_dir / "pipeline"
    pipeline_dir.mkdir(parents=True, exist_ok=True)
    task_path = run_dir / "task.md"
    task_path.write_text(request.query, encoding="utf-8")

    release = get_release(request.corpus_release)
    custom_skills = bool(request.skills_destination)
    skills_destination, skills_index, skill_dirs = resolve_skills(
        request.skills_destination,
        request.skills_index_container_path,
        include_project=True,
        corpus_release=release,
    )
    local_skills = load_local_skills_dirs(skill_dirs, query_role=True)
    if request.mode == "adaptive":
        workflow_skills = {"adaptive-query-skill", "dataset-orchestrator-skill"}
        local_skills = [
            skill
            for skill in local_skills
            if Path(skill["path"]).name not in workflow_skills
        ]
    if not custom_skills:
        skills_index = str(
            write_active_skills_index(
                runtime_dir / "SKILLS_INDEX.md",
                skills=local_skills,
            )
        )

    dataset_context_path = pipeline_dir / "dataset_context.md"
    snapshot_dataset_context(
        canonical_dataset_context_path(Path(skills_destination)),
        dataset_context_path,
        pipeline_dir / "dataset_context.json",
    )
    input_roots = _resolved_input_roots(request)
    runtime_env = {
        DEFAULT_RELEASE_ENV: release.release_id,
        "DISTRIBUTED_AGENTS_OUTPUT_DIR": str(run_dir),
        "DISTRIBUTED_AGENTS_PIPELINE_DIR": str(pipeline_dir),
        "DISTRIBUTED_AGENTS_TOOLLOG": str(run_dir / "tool_calls.jsonl"),
        "DISTRIBUTED_AGENTS_MAX_CONCURRENT_SUBAGENTS": str(
            options.max_concurrent_subagents if multi_agent else 0
        ),
        "DISTRIBUTED_AGENTS_MAX_SUBAGENTS": str(
            options.max_subagents if multi_agent else 0
        ),
    }
    for key in (
        "DISTRIBUTED_AGENTS_FINDINGS_LEDGER",
        "DISTRIBUTED_AGENTS_GENE_STORE",
        "BIOKG_REPORTS_PATH",
        "BIOKG_NEO4J_HTTP_URL",
        "BIOKG_NEO4J_DATABASE",
        "BIOKG_NEO4J_URI",
        "BIOKG_NEO4J_USER",
        "BIOKG_NEO4J_PASSWORD",
    ):
        if value := os.environ.get(key):
            runtime_env[key] = value
    adaptive_context = prepare_adaptive_context(
        mode=request.mode,
        release=release,
        task_path=task_path,
        dataset_context_path=dataset_context_path,
        pipeline_dir=pipeline_dir,
        skills_destination=skills_destination,
        runtime_env=runtime_env,
        input_roots=input_roots,
        declared_inputs=options.input_roots,
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
    (contracts_dir / "root.md").write_text(contract, encoding="utf-8")

    try:
        import httpx
        from agents import (
            Agent,
            ModelSettings,
            RunConfig,
            Runner,
            ShellTool,
            ToolExecutionConfig,
            WebSearchTool,
            set_default_openai_client,
        )
        from openai import AsyncOpenAI
        from openai.types.shared import Reasoning
    except ImportError as exc:
        raise ApiQueryError(
            "the API backend requires the `distributed_agents[api]` optional dependencies"
        ) from exc

    set_default_openai_client(
        AsyncOpenAI(
            timeout=httpx.Timeout(connect=30.0, read=600.0, write=60.0, pool=60.0)
        )
    )
    shell_tool = ShellTool(
        executor=make_local_shell_executor(
            readable_roots=(
                *input_roots,
                *map(Path, skill_dirs),
                *release.runtime_roots(),
            ),
            writable_dir=run_dir,
        ),
        environment={"type": "local", "skills": local_skills},
    )
    tools = [shell_tool, WebSearchTool()]
    reader_calls = {"started": 0, "completed": 0, "failed": 0, "refused": 0}
    sweep_skill = _sweep_skill_path(local_skills) if multi_agent else None
    if sweep_skill is not None:
        reader_contract = (sweep_skill / "references" / "reader.md").read_text(
            encoding="utf-8"
        )
        reader_agent = Agent(
            name="corpus_sweep_reader",
            model=model,
            instructions=(
                "You are a child reader invoked only for one planned exhaustive "
                "corpus slice. The parent input supplies exact task, slice, skill, "
                "and output paths. Follow it only within this protocol.\n\n"
                + reader_contract
            ),
            tools=[shell_tool, WebSearchTool()],
            model_settings=ModelSettings(
                reasoning=Reasoning(effort=options.reasoning_effort)
            ),
        )

        async def extract_reader_output(run_result: Any) -> str:
            reader_calls["completed"] += 1
            return str(run_result.final_output or "")

        def handle_reader_failure(_context: Any, error: Exception) -> str:
            reader_calls["failed"] += 1
            return (
                "Corpus reader failed. The coordinator may retry this slice once. "
                f"Error: {error}"
            )

        reader_tool = reader_agent.as_tool(
            tool_name="corpus_sweep_reader",
            tool_description=(
                "Process exactly one deterministic slice created by "
                "exhaustive-corpus-sweep-skill. The input must include the exact "
                "task path, slice path, reader-protocol path, and slice-specific "
                "output directory. Never use for search, sampling, or global "
                "synthesis."
            ),
            custom_output_extractor=extract_reader_output,
            failure_error_function=handle_reader_failure,
            max_turns=options.max_turns,
        )
        invoke_reader = reader_tool.on_invoke_tool

        async def invoke_bounded_reader(context: Any, tool_input: str) -> Any:
            if reader_calls["started"] >= options.max_subagents:
                reader_calls["refused"] += 1
                return (
                    "Reader call refused: DISTRIBUTED_AGENTS_MAX_SUBAGENTS was exhausted. "
                    "Do not claim the sweep is complete."
                )
            reader_calls["started"] += 1
            return await invoke_reader(context, tool_input)

        reader_tool.on_invoke_tool = invoke_bounded_reader
        tools.append(reader_tool)

    agent = Agent(
        name="query",
        model=model,
        instructions=contract,
        tools=tools,
        model_settings=ModelSettings(
            reasoning=Reasoning(effort=options.reasoning_effort),
            parallel_tool_calls=multi_agent,
        ),
    )
    previous_env = {key: os.environ.get(key) for key in runtime_env}
    os.environ.update(runtime_env)
    try:
        result = Runner.run_sync(
            agent,
            request.query,
            max_turns=options.max_turns,
            run_config=RunConfig(
                workflow_name="query-api",
                tool_execution=ToolExecutionConfig(
                    max_function_tool_concurrency=(
                        options.max_concurrent_subagents if multi_agent else 1
                    )
                ),
                trace_metadata={
                    "backend": "api",
                    "mode": request.mode,
                    "model": model,
                    "corpus_release": release.release_id,
                },
            ),
        )
    except Exception as exc:
        manifest_path = run_dir / "run.json"
        manifest_path.write_text(
            json.dumps(
                {
                    "backend": "api",
                    "mode": request.mode,
                    "status": "failed",
                    "model": model,
                    "duration_s": round(time.time() - started, 2),
                    "errors": [f"{type(exc).__name__}: {exc}"],
                    "subagents": {
                        "enabled": multi_agent and sweep_skill is not None,
                        **reader_calls,
                        "max_concurrent": (
                            options.max_concurrent_subagents if multi_agent else 0
                        ),
                        "max_total": options.max_subagents if multi_agent else 0,
                    },
                    "corpus_release": release.as_dict(),
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        raise ApiQueryError(f"API query failed; see {manifest_path}") from exc
    finally:
        _flush_traces()
        for key, value in previous_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    answer = str(result.final_output or "")
    answer_path = run_dir / "query.md"
    answer_path.write_text(answer, encoding="utf-8")
    audit = audit_adaptive_artifacts(
        mode=request.mode,
        pipeline_dir=pipeline_dir,
        capability_manifest=adaptive_context.capability_manifest,
    )
    warnings = tuple(
        str(value)
        for value in audit.get("warnings", [])
        if str(value).strip()
    )
    failure_reasons = [
        str(value)
        for value in audit.get("blocking_errors", [])
        if str(value).strip()
    ]
    if reader_calls["refused"]:
        failure_reasons.append(
            f"{reader_calls['refused']} corpus reader call(s) exceeded the "
            "configured subagent budget"
        )
    status = (
        "failed"
        if failure_reasons
        else "completed_with_warnings" if warnings else "completed"
    )
    usage = _usage_dict(result)
    artifacts = {
        "answer": str(answer_path),
        "task": str(task_path),
        "contract": str(contracts_dir / "root.md"),
        "capability_manifest": str(adaptive_context.capability_manifest),
    }
    if adaptive_context.coverage is not None:
        artifacts["coverage"] = str(adaptive_context.coverage)
    audit_artifacts = audit.get("artifacts")
    if isinstance(audit_artifacts, dict):
        artifacts.update(
            {
                str(name): str(path)
                for name, path in audit_artifacts.items()
                if str(path).strip()
            }
        )
    manifest = {
        "backend": "api",
        "mode": request.mode,
        "status": status,
        "model": model,
        "duration_s": round(time.time() - started, 2),
        "usage": usage,
        "warnings": list(warnings),
        "errors": list(dict.fromkeys(failure_reasons)),
        "max_turns": options.max_turns,
        "subagents": {
            "enabled": multi_agent and sweep_skill is not None,
            **reader_calls,
            "max_concurrent": (
                options.max_concurrent_subagents if multi_agent else 0
            ),
            "max_total": options.max_subagents if multi_agent else 0,
        },
        "reasoning_effort": options.reasoning_effort,
        "input_roots": [str(path) for path in input_roots],
        "corpus_release": release.as_dict(),
        "doctrine": _sweep_doctrine_provenance(sweep_skill),
        "adaptive_artifact_audit": audit,
        "artifacts": artifacts,
    }
    manifest_path = run_dir / "run.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    if failure_reasons:
        detail = "; ".join(dict.fromkeys(failure_reasons))
        raise ApiQueryError(f"API query failed: {detail}; see {manifest_path}")
    return QueryResult(
        answer=answer,
        backend="api",
        model=model,
        status=status,
        run_dir=run_dir,
        duration_s=manifest["duration_s"],
        usage=usage,
        warnings=warnings,
        artifacts=artifacts,
    )
