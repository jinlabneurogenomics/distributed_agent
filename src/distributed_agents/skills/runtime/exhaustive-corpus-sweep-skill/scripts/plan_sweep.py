#!/usr/bin/env python3
"""Create deterministic, content-hashed partitions for an exhaustive sweep."""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path
from typing import Any

from _common import PLAN_SCHEMA, canonical_json, sha256_path, write_json, write_jsonl


def _rows(path: Path) -> list[dict[str, Any]]:
    if path.suffix.casefold() == ".csv":
        with path.open(newline="", encoding="utf-8-sig") as handle:
            return [dict(row) for row in csv.DictReader(handle)]
    from _common import read_jsonl

    rows = read_jsonl(path)
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError("every JSONL unit must be an object")
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--id-field", required=True)
    parser.add_argument("--slice-count", required=True, type=int)
    parser.add_argument("--task", required=True, type=Path)
    parser.add_argument("--release-manifest", type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    args = parser.parse_args()

    source = args.input.resolve()
    if not source.is_file():
        parser.error(f"input does not exist: {source}")
    rows = _rows(source)
    if not rows:
        parser.error("input universe is empty")
    if args.slice_count < 1 or args.slice_count > len(rows):
        parser.error("slice count must be between 1 and the number of units")
    out_dir = args.out_dir.resolve()
    plan_path = out_dir / "sweep_plan.json"
    if out_dir.is_dir() and any(out_dir.iterdir()):
        parser.error(f"refusing to use nonempty sweep directory: {out_dir}")

    seen: set[str] = set()
    partitions: dict[str, list[dict[str, Any]]] = {
        f"slice-{index:04d}": [] for index in range(args.slice_count)
    }
    prepared: list[tuple[str, str, dict[str, Any]]] = []
    for row_number, row in enumerate(rows, 1):
        raw_id = row.get(args.id_field)
        if raw_id is None or str(raw_id) == "":
            parser.error(f"row {row_number} lacks nonempty {args.id_field!r}")
        unit_id = str(raw_id)
        if unit_id in seen:
            parser.error(f"duplicate unit ID: {unit_id}")
        seen.add(unit_id)
        content_sha256 = hashlib.sha256(
            canonical_json(row).encode("utf-8")
        ).hexdigest()
        prepared.append((content_sha256, unit_id, row))

    units: list[dict[str, str]] = []
    for index, (content_sha256, unit_id, row) in enumerate(sorted(prepared)):
        slice_id = f"slice-{index % args.slice_count:04d}"
        partitions[slice_id].append(row)
        units.append(
            {
                "unit_id": unit_id,
                "slice_id": slice_id,
                "content_sha256": content_sha256,
            }
        )

    slice_entries: list[dict[str, Any]] = []
    for slice_id, slice_rows in partitions.items():
        path = out_dir / "slices" / f"{slice_id}.jsonl"
        write_jsonl(path, slice_rows)
        slice_entries.append(
            {
                "slice_id": slice_id,
                "path": str(path),
                "unit_count": len(slice_rows),
                "sha256": sha256_path(path),
            }
        )

    def optional_digest(path: Path | None) -> dict[str, str] | None:
        if path is None:
            return None
        resolved = path.resolve()
        if not resolved.is_file():
            parser.error(f"referenced file does not exist: {resolved}")
        return {"path": str(resolved), "sha256": sha256_path(resolved)}

    plan = {
        "schema_version": PLAN_SCHEMA,
        "input": {"path": str(source), "sha256": sha256_path(source)},
        "id_field": args.id_field,
        "unit_count": len(rows),
        "slice_count": args.slice_count,
        "partition_method": "sha256-canonical-unit-balanced-round-robin",
        "task": optional_digest(args.task),
        "release_manifest": optional_digest(args.release_manifest),
        "slices": slice_entries,
        "units": sorted(units, key=lambda row: row["unit_id"]),
    }
    write_json(plan_path, plan)
    print(plan_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
