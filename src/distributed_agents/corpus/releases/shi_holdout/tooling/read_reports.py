#!/usr/bin/env python3
"""Read bounded target reports from the Shi holdout release."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from _common import REPORTS, iter_jsonl


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("genes", nargs="*")
    parser.add_argument("--reports-path", default=None)
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--grep", default=None)
    parser.add_argument("--max-chars", type=int, default=0)
    parser.add_argument("--max-reports", type=int, default=20)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    path = Path(args.reports_path).expanduser() if args.reports_path else REPORTS
    if args.list:
        targets = sorted(
            (str(row["gene_target"]) for row in iter_jsonl(path)), key=str.casefold
        )
        print(f"# {len(targets)} gene_targets in {path}")
        print("\n".join(targets))
        return 0
    if not args.genes:
        raise SystemExit("provide one or more gene symbols, or use --list")
    wanted = list(dict.fromkeys(gene.casefold() for gene in args.genes))
    if args.max_reports < 1 or len(wanted) > args.max_reports:
        raise SystemExit(
            f"requested {len(wanted)} reports; --max-reports is {args.max_reports}"
        )
    labels = {gene.casefold(): gene for gene in args.genes}
    found = {
        str(row["gene_target"]).casefold(): str(row["report"])
        for row in iter_jsonl(path)
        if str(row["gene_target"]).casefold() in labels
    }
    pattern = re.compile(args.grep, re.IGNORECASE) if args.grep else None
    for key in wanted:
        label = labels[key]
        report = found.get(key)
        if report is None:
            print(f"## {label}\n(no report found)\n")
            continue
        if pattern:
            hits = [
                re.sub(r"\s+", " ", sentence.strip())
                for sentence in re.split(r"(?<=[.!?])\s+", report)
                if pattern.search(sentence)
            ]
            print(f"## {label} [{len(hits)} matching sentences]")
            print("\n".join(f"- {hit}" for hit in hits) or "(no matches)")
            print()
        else:
            body = report if args.max_chars <= 0 else report[: args.max_chars]
            print(f"## {label}\n{body}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
