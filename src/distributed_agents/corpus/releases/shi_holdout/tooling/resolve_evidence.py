#!/usr/bin/env python3
"""Resolve gene-scoped Shi holdout finding links to evidence and references."""

from __future__ import annotations

import argparse
import json
import sys

from _common import iter_jsonl, ledger_path, values


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gene", required=True)
    parser.add_argument("--finding")
    parser.add_argument("--evidence-id", action="append", default=[])
    parser.add_argument("--ref-id", action="append", default=[])
    parser.add_argument("--evidence-only", action="store_true")
    parser.add_argument("--refs-only", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    target = args.gene.casefold()
    evidence_ids = set(args.evidence_id)
    ref_ids = set(args.ref_id)
    if args.finding:
        matches = [
            row
            for name in ("findings", "null_findings")
            for row in iter_jsonl(ledger_path(name))
            if str(row.get("target_gene", "")).casefold() == target
            and row.get("finding_id") == args.finding
        ]
        if len(matches) != 1:
            raise SystemExit(f"expected one {args.gene}:{args.finding} finding; found {len(matches)}")
        evidence_ids.update(values(matches[0].get("evidence_ids")))
        ref_ids.update(values(matches[0].get("ref_ids")))

    evidence = [
        row for row in iter_jsonl(ledger_path("evidence"))
        if str(row.get("target_gene", "")).casefold() == target
        and (not evidence_ids or row.get("evidence_id") in evidence_ids)
    ]
    references = [
        row for row in iter_jsonl(ledger_path("references"))
        if str(row.get("target_gene", "")).casefold() == target
        and (not ref_ids or row.get("ref_id") in ref_ids)
    ]
    if args.refs_only:
        evidence = []
    if args.evidence_only:
        references = []
    result = {"evidence": evidence, "references": references}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        for heading, rows in (("EVIDENCE", evidence), ("REFERENCES", references)):
            if rows:
                print(f"# {heading} ({len(rows)})")
                for row in rows:
                    local_id = row.get("evidence_id") or row.get("ref_id")
                    detail = row.get("description") or row.get("citation") or ""
                    print(f"[{row['target_gene']}:{local_id}] {detail}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
