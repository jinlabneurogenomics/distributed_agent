#!/usr/bin/env python3
"""Reconcile all exhaustive-sweep slices and emit a fail-closed audit."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _common import (
    AUDIT_SCHEMA,
    PLAN_SCHEMA,
    planned_ids,
    read_json,
    read_jsonl,
    sha256_path,
    validate_result_rows,
    write_json,
    write_jsonl,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    args = parser.parse_args()

    out_dir = args.out_dir.resolve()
    audit_path = out_dir / "sweep_audit.json"
    errors: list[str] = []
    missing_ids: list[str] = []
    extra_ids: list[str] = []
    duplicate_ids: list[str] = []
    covered_ids: set[str] = set()
    emitted_units = 0
    rejected_units = 0
    merged: list[dict[str, Any]] = []
    slice_audits: list[dict[str, Any]] = []

    try:
        plan = read_json(args.plan)
    except (OSError, ValueError) as exc:
        plan = {}
        errors.append(f"invalid plan: {exc}")
    if not isinstance(plan, dict) or plan.get("schema_version") != PLAN_SCHEMA:
        errors.append("plan has the wrong schema")
        plan = {}

    slices = plan.get("slices", [])
    if not isinstance(slices, list):
        errors.append("plan slices is not a list")
        slices = []
    for entry in slices:
        if not isinstance(entry, dict) or not isinstance(entry.get("slice_id"), str):
            errors.append("plan contains an invalid slice entry")
            continue
        slice_id = entry["slice_id"]
        slice_path = Path(str(entry.get("path", "")))
        result_path = out_dir / "workers" / slice_id / "slice_results.jsonl"
        expected = planned_ids(plan, slice_id)
        rows: list[Any] = []
        local_errors: list[str] = []
        if not slice_path.is_file():
            local_errors.append(f"planned slice file is missing: {slice_path}")
        elif sha256_path(slice_path) != entry.get("sha256"):
            local_errors.append(f"planned slice hash changed: {slice_path}")
        if not result_path.is_file():
            local_errors.append(f"missing results for {slice_id}")
        else:
            try:
                rows = read_jsonl(result_path)
            except (OSError, ValueError) as exc:
                local_errors.append(str(exc))
        row_errors, counts = validate_result_rows(expected, rows)
        local_errors.extend(row_errors)
        missing_ids.extend(counts["missing_ids"])
        extra_ids.extend(counts["extra_ids"])
        duplicate_ids.extend(counts["duplicate_ids"])
        if local_errors:
            errors.extend(f"{slice_id}: {error}" for error in local_errors)
        else:
            for row in rows:
                unit_id = row["unit_id"]
                if unit_id in covered_ids:
                    duplicate_ids.append(unit_id)
                    errors.append(f"unit {unit_id} appears in multiple slices")
                    continue
                covered_ids.add(unit_id)
                if row["decision"] == "emit":
                    emitted_units += 1
                    merged.extend(
                        {
                            "unit_id": unit_id,
                            "slice_id": slice_id,
                            "record": record,
                            "rationale": row["rationale"],
                            "evidence_ids": row["evidence_ids"],
                            "uncertainty": row["uncertainty"],
                        }
                        for record in row["records"]
                    )
                else:
                    rejected_units += 1
        slice_audits.append(
            {
                "slice_id": slice_id,
                "status": "failed" if local_errors else "passed",
                "results_path": str(result_path),
                "results_sha256": sha256_path(result_path) if result_path.is_file() else None,
                "counts": counts,
                "errors": local_errors,
            }
        )

    all_planned = {
        str(row["unit_id"])
        for row in plan.get("units", [])
        if isinstance(row, dict) and row.get("unit_id") is not None
    }
    global_missing = sorted(all_planned - covered_ids)
    global_extra = sorted(covered_ids - all_planned)
    missing_ids = sorted(set(missing_ids) | set(global_missing))
    extra_ids = sorted(set(extra_ids) | set(global_extra))
    duplicate_ids = sorted(set(duplicate_ids))
    if missing_ids and not any("missing unit IDs" in error for error in errors):
        errors.append("sweep has missing unit IDs")
    if extra_ids and not any("extra unit IDs" in error for error in errors):
        errors.append("sweep has extra unit IDs")
    if duplicate_ids and not any("duplicate" in error for error in errors):
        errors.append("sweep has duplicate unit IDs")

    merged_path = out_dir / "merged_candidates.jsonl"
    write_jsonl(merged_path, merged if not errors else [])
    audit = {
        "schema_version": AUDIT_SCHEMA,
        "status": "failed" if errors else "passed",
        "plan_path": str(args.plan.resolve()),
        "plan_sha256": sha256_path(args.plan) if args.plan.is_file() else None,
        "merged_path": str(merged_path),
        "merged_sha256": sha256_path(merged_path),
        "counts": {
            "planned": len(all_planned),
            "covered": len(covered_ids & all_planned),
            "emitted_units": emitted_units,
            "rejected_units": rejected_units,
            "emitted_records": len(merged) if not errors else 0,
        },
        "missing_ids": missing_ids,
        "extra_ids": extra_ids,
        "duplicate_ids": duplicate_ids,
        "slices": slice_audits,
        "errors": errors,
    }
    write_json(audit_path, audit)
    print(audit_path)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
