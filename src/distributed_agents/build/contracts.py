"""Canonical contracts owned by the corpus-authoring build stage."""

from __future__ import annotations

import hashlib
from importlib.resources import files
from pathlib import PurePosixPath


REPORT_BASE_CONTRACT_ID = "base_scientist_contract.md"
REPORT_BASE_CONTRACT_SHA256 = (
    "2e30229438f3f05f4a48d94da4ed514516e379da790ae752175cfab9665dbcd3"
)
REPORT_PROMPT_ID = "findings_report.md"
REPORT_PROMPT_SHA256 = (
    "095b534b9bdb9a8fb3e05d8218bfb3b07fe186ccd50a8fd450183a0042fc075c"
)


def _load_verified_contract(prompt_id: str, expected_sha256: str) -> str:
    relative = PurePosixPath(prompt_id)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"invalid build prompt identifier: {prompt_id!r}")
    resource = files(__package__).joinpath("prompts", *relative.parts)
    if not resource.is_file():
        raise FileNotFoundError(f"build prompt asset not found: {prompt_id}")
    content = resource.read_text(encoding="utf-8")
    actual = hashlib.sha256(content.encode()).hexdigest()
    if actual != expected_sha256:
        raise RuntimeError(
            f"canonical build prompt {prompt_id!r} has SHA-256 {actual}; "
            f"expected {expected_sha256}"
        )
    return content


def load_build_instructions() -> str:
    """Return the hash-verified report-generation instructions."""

    return _load_verified_contract(
        REPORT_BASE_CONTRACT_ID,
        REPORT_BASE_CONTRACT_SHA256,
    )


def render_findings_report_prompt(*, gene_target: str, parquet_path: str) -> str:
    """Render the sole supported source-report build task."""

    return _load_verified_contract(REPORT_PROMPT_ID, REPORT_PROMPT_SHA256).format(
        gene_target=gene_target,
        parquet_path=parquet_path,
    )
