"""Request and result models for corpus-authoring builds."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from .contracts import (
    REPORT_BASE_CONTRACT_ID,
    REPORT_BASE_CONTRACT_SHA256,
    REPORT_PROMPT_ID,
    REPORT_PROMPT_SHA256,
)
from .validation import (
    REPORT_APPENDIX_SCHEMA_ID,
    REPORT_APPENDIX_SCHEMA_SHA256,
)


BuildStatus = Literal["completed", "failed"]
BuildReasoningEffort = Literal["minimal", "low", "medium", "high"]
BUILD_REASONING_EFFORTS: tuple[BuildReasoningEffort, ...] = (
    "minimal",
    "low",
    "medium",
    "high",
)


@dataclass(frozen=True)
class BuildRequest:
    """Inputs for one findings-report build."""

    gene_target: str
    parquet_path: Path
    out_dir: Path
    model: str | None = None
    max_turns: int = 50
    reasoning_effort: BuildReasoningEffort = "high"
    skills_destination: str = ""
    skills_index_container_path: str = ""
    deliverable_path: Path | None = None


@dataclass(frozen=True)
class BuildResult:
    """Normalized output and provenance for one build."""

    report: str
    model: str
    status: BuildStatus
    run_dir: Path
    duration_s: float
    usage: dict[str, int] | None = None
    artifacts: dict[str, str] = field(default_factory=dict)
    report_prompt_id: str = REPORT_PROMPT_ID
    report_prompt_sha256: str = REPORT_PROMPT_SHA256
    base_contract_id: str = REPORT_BASE_CONTRACT_ID
    base_contract_sha256: str = REPORT_BASE_CONTRACT_SHA256
    appendix_schema_id: str = REPORT_APPENDIX_SCHEMA_ID
    appendix_schema_sha256: str = REPORT_APPENDIX_SCHEMA_SHA256
