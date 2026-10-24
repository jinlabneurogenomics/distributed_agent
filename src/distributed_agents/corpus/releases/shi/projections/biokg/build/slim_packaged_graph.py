#!/usr/bin/env python3
"""Remove exact schema mirrors from the packaged BioKG base CSVs."""

from __future__ import annotations

import argparse
import csv
import json
import os
from collections.abc import Callable
from pathlib import Path

from ..paths import BASE_DATA_DIR


NODE_FIELDS_TO_DROP = frozenset(
    {"assertion_id", "concept_type", "source_kind", "source_target", "statement"}
)
RELATIONSHIP_FIELDS_TO_DROP = frozenset(
    {"assertion_id", "finding_id", "source_doc"}
)
RELATIONSHIP_TYPES_WITH_CONFIDENCE = frozenset({"IMPLICATES"})
RELATIONSHIP_TYPES_WITH_ROLE = frozenset({"IMPLICATES", "REPORTS_GENE"})


def _node_row(row: dict[str, str]) -> dict[str, str] | None:
    labels = set(row.get("labels", "").split(";"))
    if row.get("kind") == "Caveat" or "Caveat" in labels:
        return None
    if row.get("kind") == "Gene":
        row["target_gene"] = ""
    return row


def _relationship_row(row: dict[str, str]) -> dict[str, str] | None:
    relationship_type = row.get("type", "")
    if relationship_type == "HAS_CAVEAT":
        return None
    if relationship_type not in RELATIONSHIP_TYPES_WITH_CONFIDENCE:
        row["confidence"] = ""
    if relationship_type not in RELATIONSHIP_TYPES_WITH_ROLE:
        row["role"] = ""
    return row


def _rewrite_csv(
    path: Path,
    *,
    fields_to_drop: frozenset[str],
    transform: Callable[[dict[str, str]], dict[str, str] | None],
    apply: bool,
) -> dict[str, object]:
    temp_path = path.with_name(f".{path.name}.slim.tmp")
    before = 0
    after = 0
    changed_cells = 0
    try:
        with path.open(newline="", encoding="utf-8") as source:
            reader = csv.DictReader(source)
            if reader.fieldnames is None:
                raise ValueError(f"CSV has no header: {path}")
            removed_fields = [
                field for field in reader.fieldnames if field in fields_to_drop
            ]
            output_fields = [
                field for field in reader.fieldnames if field not in fields_to_drop
            ]
            destination = (
                temp_path.open("w", newline="", encoding="utf-8") if apply else None
            )
            try:
                writer = (
                    csv.DictWriter(destination, fieldnames=output_fields)
                    if destination is not None
                    else None
                )
                if writer is not None:
                    writer.writeheader()

                for row in reader:
                    before += 1
                    original = row.copy()
                    row = transform(row)
                    if row is None:
                        continue
                    after += 1
                    changed_cells += sum(
                        1
                        for field in output_fields
                        if original.get(field, "") != row.get(field, "")
                    )
                    if writer is not None:
                        writer.writerow(
                            {field: row.get(field, "") for field in output_fields}
                        )
            finally:
                if destination is not None:
                    destination.close()
        changed = bool(removed_fields or before != after or changed_cells)
        if apply:
            if changed:
                os.replace(temp_path, path)
            else:
                temp_path.unlink()
        return {
            "path": str(path),
            "rows_before": before,
            "rows_after": after,
            "rows_removed": before - after,
            "fields_removed": removed_fields,
            "changed": changed,
        }
    finally:
        if temp_path.exists():
            temp_path.unlink()


def slim_graph(csv_dir: Path, *, apply: bool) -> dict[str, object]:
    nodes = _rewrite_csv(
        csv_dir / "nodes.merged.csv",
        fields_to_drop=NODE_FIELDS_TO_DROP,
        transform=_node_row,
        apply=apply,
    )
    relationships = _rewrite_csv(
        csv_dir / "relationships.merged.csv",
        fields_to_drop=RELATIONSHIP_FIELDS_TO_DROP,
        transform=_relationship_row,
        apply=apply,
    )
    return {
        "schema_version": "distributed_agents-biokg-schema-cleanup-v1",
        "applied": apply,
        "nodes": nodes,
        "relationships": relationships,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv-dir", type=Path, default=BASE_DATA_DIR)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Atomically replace the packaged CSVs; otherwise report only.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(json.dumps(slim_graph(args.csv_dir, apply=args.apply), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
