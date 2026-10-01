#!/usr/bin/env python3
"""Query the PerturbAI narrative-findings ledger (one row per finding).

This is the corrected flat, atomic-Finding ledger. Each row is one Finding with
structured metadata fields and self-contained narrative columns. Filter by
structured fields (e.g. `finding_type`, `gene_target`, `cell_types`), grep the
prose, then read the full per-perturbation report for the survivors with
`read_reports.py`.

Stdlib-only. The ledger is CSV with flat columns including `target_gene`,
`finding_id`, `finding_type`, `summary`, `why_it_matters`, pipe-delimited
`cell_types`, `genes`, `comparators`, `evidence_ids`, and `ref_ids`.

Examples
--------
List the finding_type vocabulary with counts:

    python query_findings.py --count finding_type

All therapeutic-direction warnings whose prose mentions essentiality/safety:

    python query_findings.py --finding-type therapeutic_direction_warning \
        --grep "essential|do not read|not be read|deplet|surviv|safe|benign"

Findings for a candidate cell type (substring match on cell_types or prose):

    python query_findings.py --cell-type "151 TH Prkcd Grin2c Glut" --limit 20

Findings for specific targets, showing chosen fields:

    python query_findings.py --gene Atp6v1e1 --gene Taf1 \
        --fields gene_target,finding_id,finding_type,source_summary

Count distinct target genes carrying a finding type (the honest "support"):

    python query_findings.py --finding-type negative_result --count gene_target | head
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

_DEFAULT_LEDGER = (
    Path(__file__).resolve().parents[3]
    / "artifacts"
    / "ledgers"
    / "findings.csv"
)

_DEFAULT_LIMIT = 20
_MAX_LIMIT = 50
_MAX_COUNT_VALUES = 200
_SCALAR_SOURCE_FIELDS = (
    "finding_type", "confidence", "direction", "literature_status",
    "main_caveats", "source_summary", "source_why_it_matters",
)
_LIST_SOURCE_FIELDS = ("cell_types", "comparators", "genes", "evidence_ids", "ref_ids")


def ledger_path(override: str | None) -> Path:
    if override:
        return Path(override).expanduser()
    env = os.environ.get("DISTRIBUTED_AGENTS_FINDINGS_LEDGER")
    if env:
        return Path(env).expanduser()
    return _DEFAULT_LEDGER


def iter_rows(path: Path):
    if not path.is_file():
        raise SystemExit(
            f"findings ledger not found at {path}\n"
            "Pass --ledger-path or set DISTRIBUTED_AGENTS_FINDINGS_LEDGER."
        )
    if path.suffix.casefold() == ".csv":
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                target = str(row.get("target_gene") or "")
                finding = str(row.get("finding_id") or "")

                def split(key: str) -> list[str]:
                    return [
                        item for item in str(row.get(key) or "").split("|") if item
                    ]

                yield {
                    "doc_id": f"{target}:{finding}",
                    "finding_id": finding,
                    "gene_target": target,
                    "hipporag_text": " ".join(
                        filter(
                            None,
                            (
                                str(row.get("summary") or ""),
                                str(row.get("why_it_matters") or ""),
                            ),
                        )
                    ),
                    "source": {
                        "finding_type": row.get("finding_type"),
                        "confidence": row.get("confidence"),
                        "direction": row.get("direction"),
                        "literature_status": row.get("literature_status"),
                        "main_caveats": row.get("main_caveats"),
                        "source_summary": row.get("summary"),
                        "source_why_it_matters": row.get("why_it_matters"),
                        "cell_types": split("cell_types"),
                        "comparators": split("comparators"),
                        "genes": split("genes"),
                        "evidence_ids": split("evidence_ids"),
                        "ref_ids": split("ref_ids"),
                    },
                }
        return
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def flat(rec: dict) -> dict:
    """Flatten {top-level + source.*} into one dict for filtering/printing."""
    out = {
        "doc_id": rec.get("doc_id", ""),
        "finding_id": rec.get("finding_id", ""),
        "gene_target": rec.get("gene_target", ""),
        "hipporag_text": rec.get("hipporag_text", ""),
    }
    src = rec.get("source", {}) or {}
    for k in _SCALAR_SOURCE_FIELDS:
        out[k] = src.get(k)
    for k in _LIST_SOURCE_FIELDS:
        out[k] = src.get(k) or []
    return out


def as_text(value) -> str:
    if isinstance(value, list):
        return " | ".join(str(v) for v in value)
    return "" if value is None else str(value)


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--ledger-path", default=None, help="Override the ledger CSV/JSONL path.")
    p.add_argument("--gene", action="append", dest="genes", default=[],
                   help="Restrict to gene_target (case-insensitive, exact); repeatable.")
    p.add_argument("--finding-type", action="append", dest="finding_types", default=[],
                   help="Restrict to a finding_type value; repeatable.")
    p.add_argument("--cell-type", default=None,
                   help="Substring match against cell_types AND the narrative prose.")
    p.add_argument("--grep", default=None,
                   help="Case-insensitive regex over hipporag_text + source_summary + "
                        "source_why_it_matters + main_caveats.")
    p.add_argument("--fields", default=None,
                   help="Comma-separated fields to print (default: a compact set). "
                        "Use 'all' for every field.")
    p.add_argument("--count", default=None, metavar="FIELD",
                   help="Instead of rows, print value counts for FIELD "
                        "(e.g. finding_type, gene_target). List-valued fields are exploded.")
    p.add_argument("--limit", type=int, default=_DEFAULT_LIMIT,
                   help=f"Max rows to print (1-{_MAX_LIMIT}; default: {_DEFAULT_LIMIT}).")
    p.add_argument("--value-limit", type=int, default=50,
                   help=f"Max distinct values for --count (1-{_MAX_COUNT_VALUES}; default: 50).")
    p.add_argument("--json", action="store_true", help="Emit matching rows as JSONL.")
    return p.parse_args(argv)


def matches(row: dict, args: argparse.Namespace, grep: re.Pattern | None) -> bool:
    if args.genes and row["gene_target"].casefold() not in {g.casefold() for g in args.genes}:
        return False
    if args.finding_types and row.get("finding_type") not in set(args.finding_types):
        return False
    if args.cell_type:
        ct = args.cell_type.casefold()
        hay = (as_text(row.get("cell_types")) + " " + row.get("hipporag_text", "")).casefold()
        if ct not in hay:
            return False
    if grep is not None:
        blob = " ".join(as_text(row.get(k)) for k in
                        ("hipporag_text", "source_summary", "source_why_it_matters", "main_caveats"))
        if not grep.search(blob):
            return False
    return True


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if os.environ.get("DISTRIBUTED_AGENTS_DISABLE_FINDING_SUMMARIES", "").casefold() in {
        "1",
        "true",
        "yes",
    }:
        raise SystemExit(
            "narrative Finding summaries are disabled for predictive rankings; "
            "use the summary-free predictive graph nomination"
        )
    path = ledger_path(args.ledger_path)
    grep = re.compile(args.grep, re.I) if args.grep else None
    if not 1 <= args.limit <= _MAX_LIMIT:
        raise SystemExit(f"--limit must be between 1 and {_MAX_LIMIT}")
    if not 1 <= args.value_limit <= _MAX_COUNT_VALUES:
        raise SystemExit(f"--value-limit must be between 1 and {_MAX_COUNT_VALUES}")

    rows = (flat(r) for r in iter_rows(path))
    selected = [r for r in rows if matches(r, args, grep)]

    if args.count:
        counter: Counter = Counter()
        field = args.count
        for r in selected:
            v = r.get(field)
            if isinstance(v, list):
                for item in v:
                    counter[str(item)] += 1
            else:
                counter[as_text(v)] += 1
        total = sum(counter.values())
        print(f"# {len(counter)} distinct {field} values across {total} matching findings")
        emitted = counter.most_common(args.value_limit)
        for value, n in emitted:
            print(f"{n}\t{value}")
        print(
            json.dumps(
                {"truncated": len(emitted) < len(counter), "exact_distinct_total": len(counter),
                 "emitted": len(emitted), "omitted": len(counter) - len(emitted)}
            ),
            file=sys.stderr,
        )
        return 0

    default_fields = ["gene_target", "finding_id", "finding_type", "cell_types",
                      "direction", "confidence", "source_summary"]
    if args.fields == "all":
        fields = (["doc_id", "finding_id", "gene_target", "hipporag_text"]
                  + list(_SCALAR_SOURCE_FIELDS) + list(_LIST_SOURCE_FIELDS))
    elif args.fields:
        fields = [f.strip() for f in args.fields.split(",") if f.strip()]
    else:
        fields = default_fields

    for r in selected[: args.limit]:
        if args.json:
            print(json.dumps({k: r.get(k) for k in fields}, ensure_ascii=False))
            continue
        print(f"## {r['gene_target']} {r['finding_id']}")
        for f in fields:
            if f in ("gene_target", "finding_id"):
                continue
            print(f"- {f}: {as_text(r.get(f))}")
        print()
    print(
        json.dumps(
            {"truncated": len(selected) > args.limit, "exact_total": len(selected),
             "emitted": min(len(selected), args.limit), "omitted": max(0, len(selected) - args.limit),
             "ledger": str(path)},
        ),
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
