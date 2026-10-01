#!/usr/bin/env python3
"""Bounded deterministic lookup and aggregates over reconciled Findings."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Mapping, Sequence


SCHEMA_VERSION = "distributed_agents-corpus-query-v1"
SCRIPT_DIR = Path(__file__).resolve().parent
RELEASE_ROOT = SCRIPT_DIR.parents[2]
DEFAULT_FINDINGS = RELEASE_ROOT / "artifacts" / "ledgers" / "findings.csv"
DEFAULT_CALIBRATION = SCRIPT_DIR / "out" / "ledger_calibration.json"
DEFAULT_DICTIONARY = SCRIPT_DIR / "out" / "value_dictionary.csv"
MAX_ROWS = 50
DEFAULT_LIMIT = 10
MAX_OUTPUT_BYTES = 32_000


def _finding_summaries_disabled() -> bool:
    return os.environ.get("DISTRIBUTED_AGENTS_DISABLE_FINDING_SUMMARIES", "").casefold() in {
        "1",
        "true",
        "yes",
    }


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_table(path: Path, *, delimiter: str) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle, delimiter=delimiter)]


def _bounded_limit(value: int) -> int:
    if value < 1 or value > MAX_ROWS:
        raise ValueError(f"--limit must be between 1 and {MAX_ROWS}")
    return value


def _with_bound(payload: dict[str, Any], *, exact_total: int, emitted: int) -> dict[str, Any]:
    return {
        **payload,
        "truncation": {
            "truncated": emitted < exact_total,
            "exact_total": exact_total,
            "emitted": emitted,
            "omitted": max(0, exact_total - emitted),
            "max_rows": MAX_ROWS,
            "max_output_bytes": MAX_OUTPUT_BYTES,
        },
    }


def _emit(payload: dict[str, Any], *, list_field: str | None = None) -> None:
    result = dict(payload)
    if list_field is not None:
        rows = list(result.get(list_field) or [])
        exact_total = int(result.pop("_exact_total", len(rows)))
        while rows:
            trial = _with_bound(
                {**result, list_field: rows},
                exact_total=exact_total,
                emitted=len(rows),
            )
            if len(json.dumps(trial, ensure_ascii=False).encode("utf-8")) <= MAX_OUTPUT_BYTES:
                result = trial
                break
            rows.pop()
        else:
            result = _with_bound(
                {**result, list_field: []}, exact_total=exact_total, emitted=0
            )
    rendered = json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if len(rendered.encode("utf-8")) > MAX_OUTPUT_BYTES:
        raise ValueError("bounded response metadata exceeds output byte ceiling")
    sys.stdout.write(rendered)


def _load_calibration(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != "distributed_agents-ledger-calibration-v2":
        raise ValueError("unsupported ledger calibration schema")
    return payload


def describe(args: argparse.Namespace) -> None:
    limit = _bounded_limit(args.limit)
    rows = _read_table(args.dictionary, delimiter=",")
    query = args.query.casefold()

    def rank(row: Mapping[str, str]) -> tuple[int, str, str, str]:
        field = str(row.get("field") or "")
        value = str(row.get("value_or_pattern") or "")
        exact = query in {field.casefold(), value.casefold()}
        starts = field.casefold().startswith(query) or value.casefold().startswith(query)
        return (0 if exact else 1 if starts else 2, row["artifact"], field, value)

    matches = [
        row
        for row in rows
        if query
        in " ".join(
            (
                row.get("artifact", ""),
                row.get("field", ""),
                row.get("value_or_pattern", ""),
                row.get("aliases", ""),
            )
        ).casefold()
    ]
    matches.sort(key=rank)
    _emit(
        {
            "schema_version": SCHEMA_VERSION,
            "operation": "corpus.describe",
            "query": args.query,
            "dictionary_sha256": _sha256(args.dictionary),
            "records": matches[:limit],
            "_exact_total": len(matches),
        },
        list_field="records",
    )


def calibrate(args: argparse.Namespace) -> None:
    payload = _load_calibration(args.calibration)
    topics: dict[str, Any] = {
        "summary": {
            "counts": payload["counts"],
            "claim_layer": payload["claim_layer"],
            "semantic_assertions": payload["semantic_assertions"],
            "reconciliation": payload["reconciliation"],
        },
        "counts": payload["counts"],
        "claim-layer": payload["claim_layer"],
        "semantic-assertions": payload["semantic_assertions"],
        "finding-confidence-by-type": payload["crosstabs"]["finding_confidence_by_type"],
        "sources": payload["sources"],
    }
    data = topics[args.topic]
    result = {
        "schema_version": SCHEMA_VERSION,
        "operation": "corpus.calibrate",
        "artifact_schema_version": payload["schema_version"],
        "artifact_sha256": _sha256(args.calibration),
        "topic": args.topic,
        "data": data,
    }
    if isinstance(data, list):
        limit = _bounded_limit(args.limit)
        result["data"] = data[:limit]
        result["_exact_total"] = len(data)
        _emit(result, list_field="data")
    else:
        _emit(result)


def count_values(args: argparse.Namespace) -> None:
    limit = _bounded_limit(args.limit)
    calibration = _load_calibration(args.calibration)
    if args.canonical:
        if not (
            args.artifact == "findings"
            and args.field == "literature_status"
            and args.canonical == "contradiction"
        ):
            raise ValueError(
                "--canonical contradiction is defined only for findings literature_status"
            )
        rows = _read_table(args.findings, delimiter=",")
        all_values = Counter(str(row.get("literature_status") or "") for row in rows)
        selected = Counter(
            {
                value: frequency
                for value, frequency in all_values.items()
                if value.casefold().startswith("contradict")
            }
        )
        excluded = Counter(
            {
                value: frequency
                for value, frequency in all_values.items()
                if "contradict" in value.casefold()
                and not value.casefold().startswith("contradict")
            }
        )
        _emit(
            {
                "schema_version": SCHEMA_VERSION,
                "operation": "corpus.aggregate.count",
                "artifact": args.artifact,
                "field": args.field,
                "canonical": "contradiction_asserting",
                "exact_matching_findings": sum(selected.values()),
                "values": [
                    {"value": value, "count": frequency}
                    for value, frequency in selected.most_common()
                ][:limit],
                "excluded_substring_matches": [
                    {"value": value, "count": frequency}
                    for value, frequency in excluded.most_common()
                ],
                "_exact_total": len(selected),
            },
            list_field="values",
        )
        return

    fields = calibration["field_value_frequencies"].get("findings", {})
    values = fields.get(args.field)
    if not isinstance(values, list):
        raise ValueError(
            f"no compact frequency table for {args.artifact}.{args.field}; use corpus.describe"
        )
    _emit(
        {
            "schema_version": SCHEMA_VERSION,
            "operation": "corpus.aggregate.count",
            "artifact": args.artifact,
            "field": args.field,
            "exact_matching_rows": sum(int(item["count"]) for item in values),
            "values": values[:limit],
            "_exact_total": len(values),
        },
        list_field="values",
    )


def inventory(args: argparse.Namespace) -> None:
    if _finding_summaries_disabled():
        raise ValueError(
            "narrative Finding/Claim summaries are disabled for predictive rankings; "
            "use the summary-free predictive graph nomination"
        )
    limit = _bounded_limit(args.limit)
    genes = {value.casefold() for value in args.genes}
    rows = _read_table(args.findings, delimiter=",")
    selected = [
        row
        for row in rows
        if (not genes or row["target_gene"].casefold() in genes)
        and (not args.finding_type or row["finding_type"] == args.finding_type)
    ]
    examples = [
        {
            "finding_uid": f"{row['target_gene']}:{row['finding_id']}",
            "finding_type": row["finding_type"],
            "confidence": row["confidence"],
            "summary": row["summary"],
        }
        for row in selected[:limit]
    ]
    _emit(
        {
            "schema_version": SCHEMA_VERSION,
            "operation": "corpus.inventory",
            "artifact": args.artifact,
            "filters": {"genes": args.genes, "finding_type": args.finding_type},
            "exact_total": len(selected),
            "examples": examples,
            "_exact_total": len(selected),
        },
        list_field="examples",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--calibration", type=Path, default=DEFAULT_CALIBRATION)
    parser.add_argument("--dictionary", type=Path, default=DEFAULT_DICTIONARY)
    parser.add_argument("--findings", type=Path, default=DEFAULT_FINDINGS)
    subparsers = parser.add_subparsers(dest="command", required=True)

    describe_parser = subparsers.add_parser("describe")
    describe_parser.add_argument("query")
    describe_parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    describe_parser.set_defaults(func=describe)

    calibrate_parser = subparsers.add_parser("calibrate")
    calibrate_parser.add_argument(
        "topic",
        choices=(
            "summary",
            "counts",
            "claim-layer",
            "semantic-assertions",
            "finding-confidence-by-type",
            "sources",
        ),
    )
    calibrate_parser.add_argument("--limit", type=int, default=MAX_ROWS)
    calibrate_parser.set_defaults(func=calibrate)

    count_parser = subparsers.add_parser("count")
    count_parser.add_argument("--artifact", choices=("findings",), required=True)
    count_parser.add_argument("--field", required=True)
    count_parser.add_argument("--canonical", choices=("contradiction",))
    count_parser.add_argument("--limit", type=int, default=20)
    count_parser.set_defaults(func=count_values)

    inventory_parser = subparsers.add_parser("inventory")
    inventory_parser.add_argument("--artifact", choices=("findings",), required=True)
    inventory_parser.add_argument("--gene", action="append", dest="genes", default=[])
    inventory_parser.add_argument("--finding-type")
    inventory_parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    inventory_parser.set_defaults(func=inventory)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        args.func(args)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
