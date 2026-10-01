#!/usr/bin/env python3
"""Filter, count, and inspect one canonical Shi holdout JSONL ledger."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter

from _common import ID_FIELDS, LEDGER_NAMES, iter_jsonl, ledger_path, values


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", choices=LEDGER_NAMES)
    parser.add_argument("--ledger-path", default=None)
    parser.add_argument("--gene", action="append", default=[])
    parser.add_argument("--id", action="append", default=[])
    parser.add_argument("--finding-type", action="append", default=[])
    parser.add_argument("--grep", default=None)
    parser.add_argument("--count", metavar="FIELD")
    parser.add_argument("--fields", help="comma-separated fields; default is every field")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    path = ledger_path(args.ledger, args.ledger_path)
    genes = {gene.casefold() for gene in args.gene}
    ids = set(args.id)
    finding_types = set(args.finding_type)
    pattern = re.compile(args.grep, re.IGNORECASE) if args.grep else None
    id_field = ID_FIELDS[args.ledger]

    def selected():
        for row in iter_jsonl(path):
            if genes and str(row.get("target_gene", "")).casefold() not in genes:
                continue
            if ids and str(row.get(id_field, "")) not in ids:
                continue
            if finding_types and str(row.get("finding_type", "")) not in finding_types:
                continue
            if pattern and not pattern.search(json.dumps(row, ensure_ascii=False, sort_keys=True)):
                continue
            yield row

    if args.count:
        counter: Counter[str] = Counter()
        for row in selected():
            for value in values(row.get(args.count)) or [""]:
                counter[value] += 1
        print(f"# {len(counter)} distinct {args.count} values")
        for value, count in counter.most_common():
            print(f"{count}\t{value}")
        return 0

    fields = [item.strip() for item in args.fields.split(",")] if args.fields else []
    count = 0
    for row in selected():
        if args.limit and count >= args.limit:
            break
        count += 1
        output = {field: row.get(field) for field in fields} if fields else row
        if args.json:
            print(json.dumps(output, ensure_ascii=False, sort_keys=True))
        else:
            print(f"## {row.get('target_gene')} {row.get(id_field)}")
            for key, value in output.items():
                if key not in {"target_gene", id_field}:
                    print(f"- {key}: {json.dumps(value, ensure_ascii=False) if isinstance(value, (list, dict)) else value}")
            print()
    if not args.json:
        print(f"# {count} records printed from {path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
