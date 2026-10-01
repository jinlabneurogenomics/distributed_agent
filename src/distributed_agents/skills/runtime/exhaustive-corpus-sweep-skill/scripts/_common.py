"""Shared validation helpers for exhaustive corpus-sweep artifacts."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


PLAN_SCHEMA = "distributed_agents-corpus-sweep-plan-v1"
AUDIT_SCHEMA = "distributed_agents-corpus-sweep-audit-v1"
SLICE_AUDIT_SCHEMA = "distributed_agents-corpus-sweep-slice-audit-v1"


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[Any]:
    rows: list[Any] = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            rows.append(json.loads(raw))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
    return rows


def write_jsonl(path: Path, rows: Iterable[Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(canonical_json(row) + "\n")
    temporary.replace(path)


def planned_ids(plan: dict[str, Any], slice_id: str) -> list[str]:
    return [
        str(unit["unit_id"])
        for unit in plan.get("units", [])
        if unit.get("slice_id") == slice_id
    ]


def validate_result_rows(
    expected_ids: list[str], rows: list[Any]
) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    seen: list[str] = []
    allowed_keys = {
        "unit_id",
        "decision",
        "records",
        "rationale",
        "evidence_ids",
        "uncertainty",
    }
    for index, row in enumerate(rows, 1):
        label = f"result row {index}"
        if not isinstance(row, dict):
            errors.append(f"{label} is not an object")
            continue
        unknown = sorted(set(row) - allowed_keys)
        missing_fields = sorted(allowed_keys - set(row))
        if missing_fields:
            errors.append(f"{label} lacks fields: {', '.join(missing_fields)}")
        if unknown:
            errors.append(f"{label} has unknown fields: {', '.join(unknown)}")
        unit_id = row.get("unit_id")
        if not isinstance(unit_id, str) or not unit_id:
            errors.append(f"{label} has an invalid unit_id")
        else:
            seen.append(unit_id)
        decision = row.get("decision")
        records = row.get("records")
        if decision not in {"emit", "reject"}:
            errors.append(f"{label} has an invalid decision")
        if not isinstance(records, list):
            errors.append(f"{label} records is not a list")
        elif not all(isinstance(record, dict) for record in records):
            errors.append(f"{label} records contains a non-object")
        elif decision == "emit" and not records:
            errors.append(f"{label} emits no records")
        elif decision == "reject" and records:
            errors.append(f"{label} rejects with nonempty records")
        if not isinstance(row.get("rationale"), str) or not row.get("rationale", "").strip():
            errors.append(f"{label} has no rationale")
        evidence_ids = row.get("evidence_ids")
        if not isinstance(evidence_ids, list) or not all(
            isinstance(value, str) for value in evidence_ids
        ):
            errors.append(f"{label} evidence_ids is not a string list")
        if row.get("uncertainty") not in {"low", "medium", "high"}:
            errors.append(f"{label} has an invalid uncertainty")

    expected = set(expected_ids)
    actual = set(seen)
    duplicates = sorted(
        value for value, count in Counter(seen).items() if count > 1
    )
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if duplicates:
        errors.append(f"duplicate unit IDs: {', '.join(duplicates)}")
    if missing:
        errors.append(f"missing unit IDs: {', '.join(missing)}")
    if extra:
        errors.append(f"extra unit IDs: {', '.join(extra)}")
    return errors, {
        "planned": len(expected_ids),
        "covered": len(actual & expected),
        "missing_ids": missing,
        "extra_ids": extra,
        "duplicate_ids": duplicates,
    }
