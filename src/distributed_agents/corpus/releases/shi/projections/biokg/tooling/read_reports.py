#!/usr/bin/env python3
"""Read the dataset's own per-perturbation reports by gene symbol.

The BioKG graph is a lossy, derived index over these reports: the typed edges and
findings were compressed from this prose, which carries the integrated, hedged
biological judgment per perturbation (e.g. "essential subunit, weak/buffered
footprint, do not read as safe"). For a material ranking — and for any
out-of-schema endpoint (depletion, survival, accessibility, ...) — that judgment
lives HERE, not in the typed edges. Use the graph (`biokg_cypher.py`) to narrow
to candidate genes, then read their full reports with this script and rank from
the prose.

Stdlib-only. The corpus is one JSON object per line with keys `gene_target` and
`final_report`.

Examples
--------
Read full reports for a candidate set:

    python read_reports.py Atp6v1e1 Thoc2 Hspa5

Pull only the depletion/survival-relevant sentences (regex over the prose):

    python read_reports.py Taf1 Gbf1 --grep "deplet|surviv|essential|lethal|buffered|do not read as"

List how many / which targets exist:

    python read_reports.py --list | head
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

from ..paths import REPORTS_FILE

_DEFAULT_REPORTS = REPORTS_FILE


def reports_path(override: str | None) -> Path:
    if override:
        return Path(override).expanduser()
    env = os.environ.get("BIOKG_REPORTS_PATH")
    if env:
        return Path(env).expanduser()
    return _DEFAULT_REPORTS


def iter_reports(path: Path):
    if not path.is_file():
        raise SystemExit(
            f"reports corpus not found at {path}\n"
            "Pass --reports-path or set BIOKG_REPORTS_PATH."
        )
    with path.open() as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            yield str(rec.get("gene_target", "")), str(rec.get("final_report", ""))


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("genes", nargs="*", help="Gene symbols (case-insensitive); repeatable.")
    p.add_argument("--reports-path", default=None, help="Override the reports JSONL path.")
    p.add_argument("--list", action="store_true", help="List available gene_targets and exit.")
    p.add_argument(
        "--grep",
        default=None,
        help="Print only report sentences matching this case-insensitive regex.",
    )
    p.add_argument(
        "--max-chars",
        type=int,
        default=0,
        help="Truncate each report to N chars (0 = full report, the default).",
    )
    return p.parse_args(argv)


def sentences(text: str) -> list[str]:
    return re.split(r"(?<=[.!?])\s+", text)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    path = reports_path(args.reports_path)

    if args.list:
        targets = sorted({g for g, _ in iter_reports(path) if g})
        print(f"# {len(targets)} gene_targets in {path}")
        for g in targets:
            print(g)
        return 0

    if not args.genes:
        raise SystemExit("provide one or more gene symbols, or use --list")

    wanted = {g.casefold(): g for g in args.genes}
    found: dict[str, str] = {}
    for gene, report in iter_reports(path):
        key = gene.casefold()
        if key in wanted:
            found[key] = report

    pattern = re.compile(args.grep, re.I) if args.grep else None
    for key, original in wanted.items():
        report = found.get(key)
        if report is None:
            print(f"## {original}\n(no report found for {original!r})\n")
            continue
        if pattern is not None:
            hits = [re.sub(r"\s+", " ", s.strip()) for s in sentences(report) if pattern.search(s)]
            body = "\n".join("  • " + s for s in hits) or "  (no matching sentences)"
            print(f"## {original}  [{len(hits)} sentences matching /{args.grep}/]\n{body}\n")
        else:
            body = report if args.max_chars <= 0 else report[: args.max_chars]
            print(f"## {original}\n{body}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
