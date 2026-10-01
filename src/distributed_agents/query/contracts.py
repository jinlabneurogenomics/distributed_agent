"""Render the backend-neutral query instruction contract."""

from __future__ import annotations

import os
from importlib.resources import files
from pathlib import Path
from pathlib import PurePosixPath

from .adaptive import AdaptiveContext
from .models import QueryRequest


ADAPTIVE_QUERY_CONTRACT = "adaptive_query_contract.md"
ADAPTIVE_QUERY_SCIENTIFIC_POLICY = "adaptive_query_scientific_policy.md"
DIRECT_QUERY_CONTRACT = "direct_query_contract.md"
_ADAPTIVE_POLICY_OVERRIDE_ENV = "DISTRIBUTED_AGENTS_ADAPTIVE_SCIENTIFIC_POLICY_FILE"
_MAX_ADAPTIVE_POLICY_CHARS = 20_000


def _load_query_contract(prompt_id: str) -> str:
    relative = PurePosixPath(prompt_id)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"invalid query prompt identifier: {prompt_id!r}")
    resource = files(__package__).joinpath("prompts", *relative.parts)
    if not resource.is_file():
        raise FileNotFoundError(f"query prompt asset not found: {prompt_id}")
    return resource.read_text(encoding="utf-8")


def adaptive_scientific_policy() -> str:
    """Load the default policy or an explicit host-side candidate."""

    override = os.environ.get(_ADAPTIVE_POLICY_OVERRIDE_ENV, "").strip()
    if override:
        path = Path(override).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(
                f"{_ADAPTIVE_POLICY_OVERRIDE_ENV} does not name a file: {path}"
            )
        policy = path.read_text(encoding="utf-8")
    else:
        policy = _load_query_contract(ADAPTIVE_QUERY_SCIENTIFIC_POLICY)
    policy = policy.strip()
    if not policy:
        raise ValueError("adaptive scientific policy must not be empty")
    if "\x00" in policy:
        raise ValueError("adaptive scientific policy must not contain NUL bytes")
    if len(policy) > _MAX_ADAPTIVE_POLICY_CHARS:
        raise ValueError(
            "adaptive scientific policy exceeds "
            f"{_MAX_ADAPTIVE_POLICY_CHARS:,} characters"
        )
    return policy


def render_query_contract(
    request: QueryRequest,
    *,
    runtime_dir: Path,
    skills_destination: str,
    skills_index: str,
    adaptive_context: AdaptiveContext | None = None,
) -> str:
    """Render the common direct/adaptive contract for either backend."""

    pipeline_dir = runtime_dir / "pipeline"
    adaptive_skill_path = (
        adaptive_context.skill_path
        if adaptive_context is not None
        else Path(skills_destination) / "runtime" / "adaptive-query-skill"
    )
    capability_manifest_path = (
        adaptive_context.capability_manifest
        if adaptive_context is not None
        else pipeline_dir / "capabilities.json"
    )
    coverage_path = (
        adaptive_context.coverage
        if adaptive_context is not None and adaptive_context.coverage is not None
        else pipeline_dir / "coverage.json"
    )
    output_dir = request.out_dir.resolve() if request.out_dir else Path("")
    common = {
        "skills_destination": skills_destination,
        "skills_index_container_path": skills_index,
        "output_dir": str(output_dir),
        "runtime_artifacts_dir": str(pipeline_dir),
        "task_path": str(output_dir / "task.md") if request.out_dir else "",
        "dataset_context_path": str(pipeline_dir / "dataset_context.md"),
        "dataset_context_manifest_path": str(pipeline_dir / "dataset_context.json"),
        "adaptive_skill_path": str(adaptive_skill_path),
        "capability_manifest_path": str(capability_manifest_path),
        "coverage_path": str(coverage_path),
        "adaptive_scientific_policy": (
            adaptive_scientific_policy() if request.mode == "adaptive" else ""
        ),
    }
    template = {
        "direct": DIRECT_QUERY_CONTRACT,
        "adaptive": ADAPTIVE_QUERY_CONTRACT,
    }[request.mode]
    contract = _load_query_contract(template).format(**common)
    return contract + (
        "\n\n<one_shot_runtime>\n"
        "This is an artifact-complete one-shot job. Finish the requested work in "
        "this run. Do not substitute an offer to run a longer job later. If an "
        "external limit prevents completion, preserve checkpoints and report exact "
        "processed/remaining counts, failed units, and the limiting resource.\n"
        "</one_shot_runtime>\n"
    )
