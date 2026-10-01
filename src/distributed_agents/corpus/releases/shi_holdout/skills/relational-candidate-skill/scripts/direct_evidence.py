#!/usr/bin/env python3
"""Retrieve bounded Shi holdout Finding-scoped comparator evidence around anchors."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path
from typing import Any, Iterable, Sequence

from relational_candidates import read_gene_file


SCHEMA_VERSION = "distributed_agents-direct-evidence-slice-v4"
DEFAULT_LEDGER = (
    Path(__file__).resolve().parents[3]
    / "artifacts"
    / "ledgers"
    / "findings.jsonl"
)
MAX_ANCHORS = 10
MAX_RECORDS_PER_ANCHOR = 3
MAX_DECISION_RECORDS = 16
MAX_OUTPUT_CHARS = 12_000
MAX_DETAIL_RECORDS = 3


def _unique(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        clean = str(value).strip()
        key = clean.casefold()
        if clean and key not in seen:
            seen.add(key)
            result.append(clean)
    return result


def _clip(value: object, limit: int) -> str | None:
    text = " ".join(str(value or "").split())
    if not text:
        return None
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def _ledger_path(override: str | None) -> Path:
    selected = override or os.environ.get("DISTRIBUTED_AGENTS_FINDINGS_LEDGER")
    return Path(selected).expanduser().resolve() if selected else DEFAULT_LEDGER.resolve()


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


def _referenced_path(raw: object, *, relative_to: Path) -> Path:
    if not isinstance(raw, str) or not raw.strip():
        raise ValueError("calibration JSON has no ranking_output")
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = (relative_to / path).resolve()
    if not path.is_file():
        raise ValueError(f"calibration ranking_output does not exist: {path}")
    return path


def _ranking_genes(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        return []
    delimiter = "\t" if "\t" in lines[0] else ","
    reader = csv.DictReader(lines, delimiter=delimiter)
    fields = {str(field).casefold(): str(field) for field in reader.fieldnames or []}
    gene_field = next(
        (fields[name] for name in ("gene_target", "target_gene", "gene", "symbol") if name in fields),
        None,
    )
    rank_field = next(
        (fields[name] for name in ("prediction_rank", "rank", "overall_rank") if name in fields),
        None,
    )
    if gene_field is None:
        raise ValueError(f"{path}: ranking has no gene column")
    rows: list[tuple[float, int, str]] = []
    for index, row in enumerate(reader, 1):
        gene = str(row.get(gene_field) or "").strip()
        if not gene:
            continue
        raw_rank = str(row.get(rank_field) or "").strip() if rank_field else ""
        rank = float(raw_rank) if raw_rank else float("inf")
        rows.append((rank, index, gene))
    return _unique(gene for _, _, gene in sorted(rows))


def _calibration_context(path: Path) -> tuple[list[str], list[str]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("calibration must be a JSON object")
    nested = payload.get("nested_evaluation")
    counterexamples = nested.get("counterexamples") if isinstance(nested, dict) else None
    if not isinstance(counterexamples, list):
        raise ValueError("calibration JSON has no nested_evaluation.counterexamples")
    anchors = _unique(
        str(row.get("gene_target") or "")
        for row in counterexamples
        if isinstance(row, dict)
    )
    ranking = _referenced_path(payload.get("ranking_output"), relative_to=path.parent)
    return anchors, _ranking_genes(ranking)


def _record_id(anchor: str, candidate: str, doc_id: str) -> str:
    return f"direct::{anchor}::{candidate}::{doc_id}::finding-scoped"


def _parse_record_id(record_id: str) -> tuple[str, str, str]:
    parts = record_id.split("::")
    if len(parts) != 5 or parts[0] != "direct" or parts[4] != "finding-scoped":
        raise ValueError(f"invalid direct evidence record_id: {record_id}")
    if not all(parts[1:4]):
        raise ValueError(f"invalid direct evidence record_id: {record_id}")
    return parts[1], parts[2], parts[3]


def _with_output_count(payload: dict[str, Any]) -> tuple[dict[str, Any], str]:
    result = {**payload, "output_char_count": 0}
    while True:
        rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
        count = len(rendered)
        if result["output_char_count"] == count:
            return result, rendered
        result["output_char_count"] = count


def _fit_records(base: dict[str, Any], records: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for record in records[:MAX_DECISION_RECORDS]:
        _, rendered = _with_output_count({**base, "records": [*selected, record]})
        if len(rendered) > MAX_OUTPUT_CHARS:
            break
        selected.append(record)
    return selected


def _index(
    rows: Sequence[dict[str, Any]],
    *,
    anchors: Sequence[str],
    candidates: Sequence[str],
    candidate_source: str,
    ledger: Path,
) -> dict[str, Any]:
    canonical = {
        str(row.get("target_gene") or "").casefold(): str(row.get("target_gene") or "")
        for row in rows
        if row.get("target_gene")
    }
    selected_anchors = _unique(canonical.get(value.casefold(), value) for value in anchors)[:MAX_ANCHORS]
    if not selected_anchors:
        raise ValueError("at least one anchor is required for an index query")
    candidate_keys = {value.casefold() for value in candidates}
    by_anchor: dict[str, list[dict[str, Any]]] = {anchor.casefold(): [] for anchor in selected_anchors}
    for row in rows:
        anchor = str(row.get("target_gene") or "")
        key = anchor.casefold()
        if key not in by_anchor:
            continue
        comparator_rows = []
        for raw_candidate in row.get("comparators") or []:
            candidate = canonical.get(str(raw_candidate).casefold(), str(raw_candidate))
            if candidate.casefold() == key:
                continue
            if candidate_keys and candidate.casefold() not in candidate_keys:
                continue
            comparator_rows.append(
                {
                    "candidate": candidate,
                    "record_id": _record_id(anchor, candidate, str(row["doc_id"])),
                }
            )
        if not comparator_rows:
            continue
        by_anchor[key].append(
            {
                "anchor": anchor,
                "pairing": "finding_scoped_comparator",
                "finding_doc_id": row["doc_id"],
                "summary": _clip(row.get("summary"), 560),
                "candidate_records": sorted(comparator_rows, key=lambda item: item["candidate"].casefold()),
            }
        )
    ordered: list[dict[str, Any]] = []
    for anchor in selected_anchors:
        ordered.extend(
            sorted(
                by_anchor[anchor.casefold()],
                key=lambda row: str(row["finding_doc_id"]).casefold(),
            )[:MAX_RECORDS_PER_ANCHOR]
        )
    base = {
        "schema_version": SCHEMA_VERSION,
        "status": "passed",
        "view": "index",
        "source_semantics": (
            "Shi holdout comparators are Finding-scoped; no candidate-specific comparison IDs "
            "are present in this release."
        ),
        "retrieval_controls": {
            "policy": "release_fixed",
            "max_anchors": MAX_ANCHORS,
            "max_records_per_anchor": MAX_RECORDS_PER_ANCHOR,
            "max_decision_records": MAX_DECISION_RECORDS,
            "max_output_chars": MAX_OUTPUT_CHARS,
            "candidate_source": candidate_source,
            "candidate_universe_count": len(_unique(candidates)),
        },
        "decision_guard": (
            "Summary-first, unranked evidence. Comparator mention orders attention "
            "only and never supplies an endpoint score or final candidate rank."
        ),
        "inputs": {"findings_ledger": str(ledger), "anchors": selected_anchors},
    }
    records = _fit_records(base, ordered)
    return {
        **base,
        "retrieved_record_count": len(ordered),
        "record_count": len(records),
        "records": records,
    }


def _detail(
    rows: Sequence[dict[str, Any]], record_ids: Sequence[str], *, ledger: Path
) -> dict[str, Any]:
    selected = _unique(record_ids)
    if len(selected) > MAX_DETAIL_RECORDS:
        raise ValueError(f"at most {MAX_DETAIL_RECORDS} detail record IDs may be requested")
    by_doc = {str(row.get("doc_id") or ""): row for row in rows}
    records = []
    missing = []
    for record_id in selected:
        anchor, candidate, doc_id = _parse_record_id(record_id)
        row = by_doc.get(doc_id)
        comparators = {
            str(value).casefold() for value in (row or {}).get("comparators") or []
        }
        if (
            row is None
            or str(row.get("target_gene") or "").casefold() != anchor.casefold()
            or candidate.casefold() not in comparators
        ):
            missing.append(record_id)
            continue
        records.append(
            {
                "record_id": record_id,
                "anchor": anchor,
                "candidate": candidate,
                "pairing": "finding_scoped_comparator",
                "association_scope": (
                    "The candidate is explicitly named in this Finding; caveats and "
                    "reference IDs remain Finding-scoped rather than candidate-paired."
                ),
                "summary": _clip(row.get("summary"), 560),
                "boundary_conditions": _clip(row.get("main_caveats"), 480),
                "reference_ids": _unique(str(value) for value in row.get("ref_ids") or []),
            }
        )
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "passed",
        "view": "detail",
        "source_semantics": "Finding-scoped Shi holdout comparator evidence",
        "retrieval_controls": {
            "policy": "release_fixed",
            "max_detail_records": MAX_DETAIL_RECORDS,
            "max_output_chars": MAX_OUTPUT_CHARS,
        },
        "association_guard": (
            "Reference IDs and caveats qualify the complete Finding and are not "
            "automatically specific to the named comparator."
        ),
        "inputs": {"findings_ledger": str(ledger)},
        "requested_record_ids": selected,
        "missing_record_ids": missing,
        "retrieved_record_count": len(records),
        "record_count": len(records),
        "records": records,
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--calibration", type=Path)
    parser.add_argument("--anchor", action="append", default=[])
    parser.add_argument("--anchors-file", type=Path)
    parser.add_argument("--detail-record", action="append", default=[])
    parser.add_argument("--findings-ledger")
    parser.add_argument("--out", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        ledger = _ledger_path(args.findings_ledger)
        rows = _read_findings(ledger)
        if args.detail_record:
            result = _detail(rows, args.detail_record, ledger=ledger)
        else:
            anchors = list(args.anchor)
            candidates: list[str] = []
            candidate_source = "unbounded_release_comparators"
            if args.anchors_file:
                anchors.extend(read_gene_file(args.anchors_file))
            if args.calibration:
                calibrated_anchors, candidates = _calibration_context(args.calibration.resolve())
                anchors = [*calibrated_anchors, *anchors]
                candidate_source = "calibration_ranking_output"
            result = _index(
                rows,
                anchors=anchors,
                candidates=candidates,
                candidate_source=candidate_source,
                ledger=ledger,
            )
        counted, rendered = _with_output_count(result)
        if len(rendered) > MAX_OUTPUT_CHARS:
            raise ValueError("direct evidence result exceeds the fixed output bound")
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered, encoding="utf-8")
        print(
            json.dumps(
                {
                    "status": counted["status"],
                    "view": counted["view"],
                    "out": str(args.out.resolve()),
                    "record_count": counted["record_count"],
                    "output_char_count": counted["output_char_count"],
                },
                sort_keys=True,
            )
        )
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        failure = {"status": "failed", "error": str(exc)}
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(failure, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(failure), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
