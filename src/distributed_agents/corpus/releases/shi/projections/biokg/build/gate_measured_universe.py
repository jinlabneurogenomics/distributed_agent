#!/usr/bin/env python3
"""Gate BioKG `Gene` nodes to the screen's measured universe (build post-merge step).

Drops every `Gene` node whose symbol is NOT in the measured universe
(`measured_universe.txt` — the frozen `is_measured OR is_perturbation_target` set from the
annotation store's `genes.parquet`), plus all relationships incident to those nodes.
`TargetGene` nodes are never dropped. Operates in place on a merged CSV dir (default: the
release-owned BioKG base data). Stdlib-only, idempotent, dry-run by default.

The dropped tokens are overwhelmingly non-genes miscategorised into the gene lane — drugs in
`therapeutic_direction` comparators (e.g. Maraviroc, AdipoRon), control tokens (`Non_target`,
`Safe_target_*`), leaked cell-types/anatomy, and phenotype phrases — plus a few human-symbol
variants (e.g. `AGTR1`). Reclassifying the drug tokens to `Other`/drug nodes instead of
deleting them is TODO P2-6 (backlog); this step just removes them from the gene lane.

Pipeline position:  build_biokg_v2 -> merge_canonical_entities -> **gate_measured_universe** ->
packaged CSVs -> biokg-rebuild.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

from ..paths import BASE_DATA_DIR, MEASURED_UNIVERSE_FILE

DEFAULT_CSV_DIR = BASE_DATA_DIR
DEFAULT_UNIVERSE = MEASURED_UNIVERSE_FILE


def load_universe(path: Path) -> set[str]:
    genes: set[str] = set()
    with path.open() as handle:
        for line in handle:
            line = line.strip()
            if line and not line.startswith("#"):
                genes.add(line.casefold())
    return genes


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv-dir", type=Path, default=DEFAULT_CSV_DIR)
    ap.add_argument("--universe", type=Path, default=DEFAULT_UNIVERSE)
    ap.add_argument("--apply", action="store_true", help="write changes (default: dry-run)")
    args = ap.parse_args()
    csv.field_size_limit(10 ** 7)

    uni = load_universe(args.universe)
    nodes_p = args.csv_dir / "nodes.merged.csv"
    rels_p = args.csv_dir / "relationships.merged.csv"

    with nodes_p.open(newline="") as f:
        reader = csv.DictReader(f)
        node_fields = reader.fieldnames
        nodes = list(reader)
    drop_ids: set[str] = set()
    kept_nodes = []
    for n in nodes:
        labels = set(n["labels"].split(";"))
        if "Gene" in labels and "TargetGene" not in labels and n["name"].casefold() not in uni:
            drop_ids.add(n["id"])
        else:
            kept_nodes.append(n)

    with rels_p.open(newline="") as f:
        reader = csv.DictReader(f)
        rel_fields = reader.fieldnames
        rels = list(reader)
    kept_rels = [r for r in rels if r["start_id"] not in drop_ids and r["end_id"] not in drop_ids]

    print(f"universe: {len(uni)} genes")
    print(f"nodes: {len(nodes)} -> {len(kept_nodes)}  (dropped {len(drop_ids)} out-of-universe Gene nodes)")
    print(f"rels:  {len(rels)} -> {len(kept_rels)}  (dropped {len(rels) - len(kept_rels)} incident edges)")
    if not args.apply:
        print("dry-run — pass --apply to write")
        return

    with nodes_p.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=node_fields)
        writer.writeheader()
        writer.writerows(kept_nodes)
    with rels_p.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rel_fields)
        writer.writeheader()
        writer.writerows(kept_rels)
    print(f"written to {args.csv_dir}")


if __name__ == "__main__":
    main()
