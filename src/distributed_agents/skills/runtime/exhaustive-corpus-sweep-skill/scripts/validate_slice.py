#!/usr/bin/env python3
"""Validate exact per-unit accounting for one exhaustive-sweep slice."""

from __future__ import annotations

import argparse
from pathlib import Path

from _common import (
    PLAN_SCHEMA,
    SLICE_AUDIT_SCHEMA,
    planned_ids,
    read_json,
    read_jsonl,
    sha256_path,
    validate_result_rows,
    write_json,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--slice-id", required=True)
    parser.add_argument("--results", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    errors: list[str] = []
    try:
        plan = read_json(args.plan)
    except (OSError, ValueError) as exc:
        errors.append(f"invalid plan: {exc}")
        plan = {}
    if not isinstance(plan, dict) or plan.get("schema_version") != PLAN_SCHEMA:
        errors.append("plan has the wrong schema")
        plan = {}
    slice_entry = next(
        (
            row
            for row in plan.get("slices", [])
            if isinstance(row, dict) and row.get("slice_id") == args.slice_id
        ),
        None,
    )
    if slice_entry is None:
        errors.append(f"unknown slice ID: {args.slice_id}")
    else:
        slice_path = Path(str(slice_entry.get("path", "")))
        if not slice_path.is_file():
            errors.append(f"planned slice file is missing: {slice_path}")
        elif sha256_path(slice_path) != slice_entry.get("sha256"):
            errors.append(f"planned slice hash changed: {slice_path}")
    expected = planned_ids(plan, args.slice_id)
    rows = []
    if not args.results.is_file():
        errors.append(f"results file is missing: {args.results}")
    else:
        try:
            rows = read_jsonl(args.results)
        except (OSError, ValueError) as exc:
            errors.append(str(exc))
    row_errors, counts = validate_result_rows(expected, rows)
    errors.extend(row_errors)
    audit = {
        "schema_version": SLICE_AUDIT_SCHEMA,
        "status": "failed" if errors else "passed",
        "slice_id": args.slice_id,
        "plan_path": str(args.plan.resolve()),
        "results_path": str(args.results.resolve()),
        "results_sha256": sha256_path(args.results) if args.results.is_file() else None,
        "counts": counts,
        "errors": errors,
    }
    write_json(args.out, audit)
    print(args.out)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
