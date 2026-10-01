#!/usr/bin/env python3
"""Run bounded calibration and atomic-Claim queries over Shi holdout."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence


SCHEMA_VERSION = "distributed_agents-corpus-query-v1"
CALIBRATION_SCHEMA_VERSION = "distributed_agents-july-ledger-calibration-v1"
SCRIPT_DIR = Path(__file__).resolve().parent
RELEASE_ROOT = SCRIPT_DIR.parents[2]
DEFAULT_FINDINGS = RELEASE_ROOT / "artifacts" / "ledgers" / "findings.jsonl"
DEFAULT_CLAIMS = RELEASE_ROOT / "artifacts" / "relations" / "claim_assignments.csv"
DEFAULT_RELATIONS = RELEASE_ROOT / "artifacts" / "relations" / "claim_relations.csv"
DEFAULT_CALIBRATION = RELEASE_ROOT / "artifacts" / "contracts" / "ledger_calibration.json"
DEFAULT_DICTIONARY = RELEASE_ROOT / "artifacts" / "contracts" / "value_dictionary.csv"
MAX_ROWS = 50
DEFAULT_LIMIT = 10
MAX_OUTPUT_BYTES = 32_000


def _summaries_disabled() -> bool:
    return os.environ.get("DISTRIBUTED_AGENTS_DISABLE_FINDING_SUMMARIES", "").casefold() in {
        "1",
        "true",
        "yes",
    }


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _read_findings(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_number}: expected JSON object")
            rows.append(row)
    return rows


def _bounded_limit(value: int) -> int:
    if value < 1 or value > MAX_ROWS:
        raise ValueError(f"--limit must be between 1 and {MAX_ROWS}")
    return value


def _with_bound(
    payload: dict[str, Any], *, exact_total: int, emitted: int
) -> dict[str, Any]:
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
        while True:
            trial = _with_bound(
                {**result, list_field: rows},
                exact_total=exact_total,
                emitted=len(rows),
            )
            if len(json.dumps(trial, ensure_ascii=False).encode("utf-8")) <= MAX_OUTPUT_BYTES:
                result = trial
                break
            if not rows:
                raise ValueError("bounded response metadata exceeds output byte ceiling")
            rows.pop()
    rendered = json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if len(rendered.encode("utf-8")) > MAX_OUTPUT_BYTES:
        raise ValueError("bounded response exceeds output byte ceiling")
    sys.stdout.write(rendered)


def _load_calibration(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != CALIBRATION_SCHEMA_VERSION:
        raise ValueError("unsupported Shi holdout ledger calibration schema")
    return payload


def _contains(row: Mapping[str, str], query: str) -> bool:
    return query in " ".join(str(value) for value in row.values()).casefold()


def describe(args: argparse.Namespace) -> None:
    limit = _bounded_limit(args.limit)
    rows = _read_csv(args.dictionary)
    query = args.query.casefold()

    def rank(row: Mapping[str, str]) -> tuple[int, str, str, str]:
        field = str(row.get("field") or "")
        value = str(row.get("value_or_pattern") or "")
        exact = query in {field.casefold(), value.casefold()}
        starts = field.casefold().startswith(query) or value.casefold().startswith(query)
        return (0 if exact else 1 if starts else 2, row.get("artifact", ""), field, value)

    matches = sorted((row for row in rows if _contains(row, query)), key=rank)
    _emit(
        {
            "schema_version": SCHEMA_VERSION,
            "operation": "corpus.describe",
            "release_contract": CALIBRATION_SCHEMA_VERSION,
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
            "atomic_claim_projection": payload["atomic_claim_projection"],
            "relation_projection": payload["relation_projection"],
            "candidate_pool_descriptors": payload["candidate_pool_descriptors"],
            "semantic_assertions": payload["semantic_assertions"],
        },
        "counts": payload["counts"],
        "claims": payload["atomic_claim_projection"],
        "relations": payload["relation_projection"],
        "candidate-pools": payload["candidate_pool_descriptors"],
        "field-frequencies": payload["field_value_frequencies"],
        "finding-confidence-by-type": payload["crosstabs"]["finding_confidence_by_type"],
        "literature-direction-by-type": payload["crosstabs"]["finding_literature_direction_by_type"],
        "semantic-assertions": payload["semantic_assertions"],
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
            and args.field == "lit_direction"
            and args.canonical == "contradiction"
        ):
            raise ValueError(
                "Shi holdout --canonical contradiction is defined only for findings.lit_direction"
            )
        rows = _read_findings(args.findings)
        exact = sum(str(row.get("lit_direction") or "").casefold() == "disagree" for row in rows)
        _emit(
            {
                "schema_version": SCHEMA_VERSION,
                "operation": "corpus.aggregate.count",
                "artifact": "findings",
                "field": "lit_direction",
                "canonical": "contradiction_asserting",
                "exact_matching_findings": exact,
                "values": [{"value": "disagree", "count": exact}],
                "_exact_total": 1,
            },
            list_field="values",
        )
        return

    frequency_artifact = "relations" if args.artifact == "relations" else args.artifact
    values = (
        calibration["field_value_frequencies"]
        .get(frequency_artifact, {})
        .get(args.field)
    )
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


def story_count(args: argparse.Namespace) -> None:
    if _summaries_disabled():
        raise ValueError(
            "narrative Finding/Claim summaries are disabled for predictive rankings; "
            "use the summary-free predictive graph nomination"
        )
    requested = {gene.casefold() for gene in args.genes}
    claims = _read_csv(args.claims)
    selected = []
    for claim in claims:
        targets = {
            value.casefold() for value in str(claim.get("targets") or "").split("|") if value
        }
        if not requested.issubset(targets):
            continue
        if args.finding_type and args.finding_type != claim.get("relation_family"):
            continue
        selected.append(
            {
                "claim_id": claim["claim_id"],
                "member_doc_ids": [claim["doc_id"]],
                "member_count": 1,
                "relation_family": claim["relation_family"],
                "finding_types": [claim["finding_types"]],
                "canonical_summary": claim["canonical_summary"],
                "claim_unit": claim["claim_unit"],
            }
        )
    limit = _bounded_limit(args.limit)
    _emit(
        {
            "schema_version": SCHEMA_VERSION,
            "operation": "corpus.story_count",
            "claim_semantics": "one atomic Shi holdout Finding per Claim; no duplicate reduction",
            "genes": args.genes,
            "finding_type": args.finding_type,
            "distinct_claims": len(selected),
            "claims": selected[:limit],
            "_exact_total": len(selected),
        },
        list_field="claims",
    )


def inventory(args: argparse.Namespace) -> None:
    if _summaries_disabled() and args.artifact in {"findings", "claims"}:
        raise ValueError(
            "narrative Finding/Claim summaries are disabled for predictive rankings; "
            "use the summary-free predictive graph nomination"
        )
    limit = _bounded_limit(args.limit)
    genes = {value.casefold() for value in args.genes}
    if args.artifact == "findings":
        rows = _read_findings(args.findings)
        selected = [
            row
            for row in rows
            if (not genes or str(row.get("target_gene") or "").casefold() in genes)
            and (not args.finding_type or row.get("finding_type") == args.finding_type)
        ]
        examples = [
            {
                "finding_uid": row["doc_id"],
                "finding_type": row["finding_type"],
                "confidence": row["confidence"],
                "summary": row["summary"],
            }
            for row in selected[:limit]
        ]
    elif args.artifact == "claims":
        rows = _read_csv(args.claims)
        selected = [
            row
            for row in rows
            if (not genes or row["target_gene"].casefold() in genes)
            and (not args.finding_type or row["relation_family"] == args.finding_type)
        ]
        examples = [
            {
                "claim_id": row["claim_id"],
                "member_count": 1,
                "confidence": row["confidence"],
                "claim_unit": row["claim_unit"],
                "canonical_summary": row["canonical_summary"],
            }
            for row in selected[:limit]
        ]
    else:
        rows = _read_csv(args.relations)
        selected = [
            row
            for row in rows
            if not genes
            or row["source_target"].casefold() in genes
            or row["target_target"].casefold() in genes
        ]
        examples = [
            {
                key: row[key]
                for key in (
                    "source_claim_id",
                    "target_claim_id",
                    "source_target",
                    "target_target",
                    "relation_type",
                    "basis",
                )
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
    parser.add_argument("--claims", type=Path, default=DEFAULT_CLAIMS)
    parser.add_argument("--relations", type=Path, default=DEFAULT_RELATIONS)
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
            "claims",
            "relations",
            "candidate-pools",
            "field-frequencies",
            "finding-confidence-by-type",
            "literature-direction-by-type",
            "semantic-assertions",
            "sources",
        ),
    )
    calibrate_parser.add_argument("--limit", type=int, default=MAX_ROWS)
    calibrate_parser.set_defaults(func=calibrate)

    count_parser = subparsers.add_parser("count")
    count_parser.add_argument(
        "--artifact", choices=("findings", "claims", "relations"), required=True
    )
    count_parser.add_argument("--field", required=True)
    count_parser.add_argument("--canonical", choices=("contradiction",))
    count_parser.add_argument("--limit", type=int, default=20)
    count_parser.set_defaults(func=count_values)

    story_parser = subparsers.add_parser("story-count")
    story_parser.add_argument("--gene", action="append", dest="genes", required=True)
    story_parser.add_argument("--finding-type")
    story_parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    story_parser.set_defaults(func=story_count)

    inventory_parser = subparsers.add_parser("inventory")
    inventory_parser.add_argument(
        "--artifact", choices=("findings", "claims", "relations"), required=True
    )
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
