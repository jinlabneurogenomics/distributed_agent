"""Shared stdlib helpers for release-local command-line tools."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Iterator


RELEASE_ROOT = Path(__file__).resolve().parents[1]
REPORTS = Path(
    os.environ.get("BIOKG_REPORTS_PATH")
    or RELEASE_ROOT / "artifacts" / "reports" / "reports.jsonl"
)
LEDGERS = RELEASE_ROOT / "artifacts" / "ledgers"
LEDGER_NAMES = (
    "findings", "null_findings", "evidence", "references", "pathways", "cell_types"
)
ID_FIELDS = {
    "findings": "finding_id",
    "null_findings": "finding_id",
    "evidence": "evidence_id",
    "references": "ref_id",
    "pathways": "pathway_id",
    "cell_types": "cell_type_id",
}


def iter_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    if not path.is_file():
        raise SystemExit(f"missing release artifact: {path}")
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_number}: invalid JSON: {exc}") from exc
            if not isinstance(row, dict):
                raise SystemExit(f"{path}:{line_number}: expected JSON object")
            yield row


def ledger_path(name: str, override: str | None = None) -> Path:
    if name not in LEDGER_NAMES:
        raise SystemExit(f"unknown ledger {name!r}")
    selected = override
    if selected is None and name == "findings":
        selected = os.environ.get("DISTRIBUTED_AGENTS_FINDINGS_LEDGER")
    return (
        Path(selected).expanduser()
        if selected
        else LEDGERS / f"{name}.jsonl"
    )


def values(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]
