"""First-stage generation of source reports for corpus construction."""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

from ..runtime.agent_shell import make_local_shell_executor
from ..skills.registry import load_local_skills_dirs, resolve_skills
from .contracts import (
    REPORT_BASE_CONTRACT_ID,
    REPORT_BASE_CONTRACT_SHA256,
    REPORT_PROMPT_ID,
    REPORT_PROMPT_SHA256,
    load_build_instructions,
    render_findings_report_prompt,
)
from .models import BUILD_REASONING_EFFORTS, BuildRequest, BuildResult
from .validation import (
    REPORT_APPENDIX_SCHEMA_ID,
    REPORT_APPENDIX_SCHEMA_SHA256,
    AppendixValidationError,
    validate_findings_report,
)


DEFAULT_BUILD_MODEL = os.environ.get("DISTRIBUTED_AGENTS_MODEL", "gpt-rosalind-260428")


class BuildError(RuntimeError):
    """Raised when a corpus-authoring build fails."""


def _usage_dict(result: Any) -> dict[str, int] | None:
    usage = getattr(getattr(result, "context_wrapper", None), "usage", None)
    if usage is None:
        return None
    values = {
        name: value
        for name in ("requests", "input_tokens", "output_tokens", "total_tokens")
        if isinstance((value := getattr(usage, name, None)), int)
    }
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


def build_findings_report(request: BuildRequest) -> BuildResult:
    """Generate and persist one canonical findings-centered source report."""

    gene_target = request.gene_target.strip()
    if not gene_target:
        raise ValueError("gene_target must not be empty")
    if request.max_turns < 1:
        raise ValueError("max_turns must be at least 1")
    if request.reasoning_effort not in BUILD_REASONING_EFFORTS:
        raise ValueError(
            f"unknown build reasoning effort {request.reasoning_effort!r}"
        )
    parquet_path = request.parquet_path.expanduser().resolve()
    if not parquet_path.is_file():
        raise FileNotFoundError(f"build input parquet does not exist: {parquet_path}")

    model = request.model or DEFAULT_BUILD_MODEL
    run_dir = request.out_dir.expanduser().resolve()
    run_dir.mkdir(parents=True, exist_ok=True)
    started = time.time()
    skills_destination, skills_index, skill_dirs = resolve_skills(
        request.skills_destination,
        request.skills_index_container_path,
        include_project=False,
    )
    local_skills = load_local_skills_dirs(skill_dirs)
    instructions = load_build_instructions().format(
        skills_destination=skills_destination,
        skills_index_container_path=skills_index,
    )

    try:
        import httpx
        from agents import (
            Agent,
            ModelSettings,
            RunConfig,
            Runner,
            ShellTool,
            WebSearchTool,
            set_default_openai_client,
        )
        from openai import AsyncOpenAI
        from openai.types.shared import Reasoning
    except ImportError as exc:
        raise BuildError(
            "the build stage requires the `distributed_agents[build]` optional dependencies"
        ) from exc

    set_default_openai_client(
        AsyncOpenAI(
            timeout=httpx.Timeout(connect=30.0, read=600.0, write=60.0, pool=60.0)
        )
    )
    shell_tool = ShellTool(
        executor=make_local_shell_executor(
            readable_roots=(parquet_path, *map(Path, skill_dirs)),
            writable_dir=run_dir,
        ),
        environment={"type": "local", "skills": local_skills},
    )
    agent = Agent(
        name="scientist",
        model=model,
        instructions=instructions,
        tools=[shell_tool, WebSearchTool()],
        model_settings=ModelSettings(
            reasoning=Reasoning(effort=request.reasoning_effort)
        ),
    )
    previous_output = os.environ.get("DISTRIBUTED_AGENTS_OUTPUT_DIR")
    previous_toollog = os.environ.get("DISTRIBUTED_AGENTS_TOOLLOG")
    os.environ["DISTRIBUTED_AGENTS_OUTPUT_DIR"] = str(run_dir)
    os.environ["DISTRIBUTED_AGENTS_TOOLLOG"] = str(run_dir / "tool_calls.jsonl")
    try:
        result = Runner.run_sync(
            agent,
            render_findings_report_prompt(
                gene_target=gene_target,
                parquet_path=str(parquet_path),
            ),
            max_turns=request.max_turns,
            run_config=RunConfig(
                workflow_name="build-findings-report",
                trace_metadata={
                    "stage": "build",
                    "model": model,
                    "gene_target": gene_target,
                    "report_prompt_id": REPORT_PROMPT_ID,
                    "report_prompt_sha256": REPORT_PROMPT_SHA256,
                    "base_contract_id": REPORT_BASE_CONTRACT_ID,
                    "base_contract_sha256": REPORT_BASE_CONTRACT_SHA256,
                    "appendix_schema_id": REPORT_APPENDIX_SCHEMA_ID,
                    "appendix_schema_sha256": REPORT_APPENDIX_SCHEMA_SHA256,
                },
            ),
        )
    except Exception as exc:
        manifest_path = run_dir / "run.json"
        manifest_path.write_text(
            json.dumps(
                {
                    "stage": "build",
                    "status": "failed",
                    "model": model,
                    "gene_target": gene_target,
                    "duration_s": round(time.time() - started, 2),
                    "report_prompt_id": REPORT_PROMPT_ID,
                    "report_prompt_sha256": REPORT_PROMPT_SHA256,
                    "base_contract_id": REPORT_BASE_CONTRACT_ID,
                    "base_contract_sha256": REPORT_BASE_CONTRACT_SHA256,
                    "appendix_schema_id": REPORT_APPENDIX_SCHEMA_ID,
                    "appendix_schema_sha256": REPORT_APPENDIX_SCHEMA_SHA256,
                    "errors": [f"{type(exc).__name__}: {exc}"],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        raise BuildError(f"findings-report build failed; see {manifest_path}") from exc
    finally:
        _flush_traces()
        if previous_output is None:
            os.environ.pop("DISTRIBUTED_AGENTS_OUTPUT_DIR", None)
        else:
            os.environ["DISTRIBUTED_AGENTS_OUTPUT_DIR"] = previous_output
        if previous_toollog is None:
            os.environ.pop("DISTRIBUTED_AGENTS_TOOLLOG", None)
        else:
            os.environ["DISTRIBUTED_AGENTS_TOOLLOG"] = previous_toollog

    report = str(result.final_output or "")
    if request.deliverable_path is not None:
        deliverable = request.deliverable_path.expanduser().resolve()
        if deliverable.is_file() and deliverable.stat().st_size > 0:
            report = deliverable.read_text(encoding="utf-8")
    report_path = run_dir / "report.md"
    report_path.write_text(report, encoding="utf-8")
    try:
        appendix = validate_findings_report(report, gene_target=gene_target)
    except Exception as exc:
        errors = (
            list(exc.errors)
            if isinstance(exc, AppendixValidationError)
            else [f"{type(exc).__name__}: {exc}"]
        )
        manifest_path = run_dir / "run.json"
        manifest_path.write_text(
            json.dumps(
                {
                    "stage": "build",
                    "status": "failed",
                    "phase": "appendix_validation",
                    "model": model,
                    "gene_target": gene_target,
                    "duration_s": round(time.time() - started, 2),
                    "report_prompt_id": REPORT_PROMPT_ID,
                    "report_prompt_sha256": REPORT_PROMPT_SHA256,
                    "base_contract_id": REPORT_BASE_CONTRACT_ID,
                    "base_contract_sha256": REPORT_BASE_CONTRACT_SHA256,
                    "appendix_schema_id": REPORT_APPENDIX_SCHEMA_ID,
                    "appendix_schema_sha256": REPORT_APPENDIX_SCHEMA_SHA256,
                    "errors": errors,
                    "artifacts": {"report": str(report_path)},
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        raise BuildError(
            f"findings-report appendix validation failed; see {manifest_path}"
        ) from exc
    appendix_path = run_dir / "structured_appendix.json"
    appendix_path.write_text(
        json.dumps(appendix, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    usage = _usage_dict(result)
    duration_s = round(time.time() - started, 2)
    artifacts = {
        "report": str(report_path),
        "structured_appendix": str(appendix_path),
        "tool_calls": str(run_dir / "tool_calls.jsonl"),
    }
    manifest = {
        "stage": "build",
        "status": "completed",
        "model": model,
        "gene_target": gene_target,
        "input": str(parquet_path),
        "duration_s": duration_s,
        "usage": usage,
        "max_turns": request.max_turns,
        "reasoning_effort": request.reasoning_effort,
        "report_prompt_id": REPORT_PROMPT_ID,
        "report_prompt_sha256": REPORT_PROMPT_SHA256,
        "base_contract_id": REPORT_BASE_CONTRACT_ID,
        "base_contract_sha256": REPORT_BASE_CONTRACT_SHA256,
        "appendix_schema_id": REPORT_APPENDIX_SCHEMA_ID,
        "appendix_schema_sha256": REPORT_APPENDIX_SCHEMA_SHA256,
        "artifacts": artifacts,
    }
    manifest_path = run_dir / "run.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    artifacts["run_manifest"] = str(manifest_path)
    return BuildResult(
        report=report,
        model=model,
        status="completed",
        run_dir=run_dir,
        duration_s=duration_s,
        usage=usage,
        artifacts=artifacts,
    )
