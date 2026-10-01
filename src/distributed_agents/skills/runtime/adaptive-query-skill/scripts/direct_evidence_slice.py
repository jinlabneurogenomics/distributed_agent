#!/usr/bin/env python3
"""Retrieve a summary-first, unranked evidence index around named anchors.

This is a two-stage retrieval tool, not a candidate generator or scorer. The
index exposes only identity, pairing precision, and one causal summary for exact
literature comparisons and explicitly tagged peer comparators. Compact
boundary conditions and reference IDs are fetched separately for at most
three explicit records. Full citations remain outside routine model context. In
predictive use, calibration supplies both residual anchors and the canonical
candidate universe; the CLI exposes no retrieval-budget controls.
"""

from __future__ import annotations

import argparse
import base64
import csv
import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Callable, Sequence


SCHEMA_VERSION = "distributed_agents-direct-evidence-slice-v4"
DEFAULT_HTTP_URL = os.environ.get("BIOKG_NEO4J_HTTP_URL", "http://127.0.0.1:7474")
DEFAULT_DATABASE = os.environ.get("BIOKG_NEO4J_DATABASE", "neo4j")
DEFAULT_USER = os.environ.get("BIOKG_NEO4J_USER", "neo4j")
DEFAULT_PASSWORD = os.environ.get("BIOKG_NEO4J_PASSWORD", "biokgpassword")
DEFAULT_MAX_ANCHORS = 10
DEFAULT_MAX_RECORDS_PER_ANCHOR = 3
DEFAULT_MAX_DECISION_RECORDS = 16
DEFAULT_MAX_OUTPUT_CHARS = 12_000
MAX_DETAIL_RECORDS = 3


DIRECT_EVIDENCE_INDEX_QUERY = """
UNWIND $anchors AS anchor_row
CALL {
  WITH anchor_row
  MATCH (target:TargetGene)-[:HAS_FINDING]->(finding:Finding)
        -[reported:REPORTS_GENE]->(candidate:Gene)
  WHERE toLower(target.symbol) = anchor_row.key
    AND toLower(candidate.symbol) <> anchor_row.key
    AND (size($candidate_keys) = 0 OR toLower(candidate.symbol) IN $candidate_keys)
    AND (
      reported.role = 'finding_reported_comparator'
      OR reported.comparison_id IS NOT NULL
    )
  OPTIONAL MATCH (finding)-[literature:HAS_LITERATURE_COMPARISON]
        ->(comparison:LiteratureComparison)
  WHERE reported.comparison_id IS NOT NULL
    AND coalesce(literature.comparison_id, comparison.comparison_id)
        = reported.comparison_id
  RETURN DISTINCT
         anchor_row.priority AS anchor_priority,
         anchor_row.symbol AS anchor_gene,
         candidate.symbol AS candidate_gene,
         finding.doc_id AS finding_doc_id,
         reported.comparison_id AS comparison_id,
         CASE WHEN reported.comparison_id IS NULL
              THEN 'finding_scoped'
              ELSE 'exact_comparison_id' END AS pairing_precision,
         coalesce(comparison.summary, comparison.statement, finding.summary)
           AS evidence_summary
  ORDER BY CASE WHEN reported.comparison_id IS NULL THEN 1 ELSE 0 END,
           candidate_gene, finding_doc_id
  LIMIT $max_records_per_anchor
}
RETURN *
ORDER BY anchor_priority,
         CASE pairing_precision WHEN 'exact_comparison_id' THEN 0 ELSE 1 END,
         candidate_gene, finding_doc_id
"""


DIRECT_EVIDENCE_DETAIL_QUERY = """
UNWIND $record_rows AS wanted
MATCH (target:TargetGene)-[:HAS_FINDING]->(finding:Finding)
      -[reported:REPORTS_GENE]->(candidate:Gene)
WHERE toLower(target.symbol) = wanted.anchor_key
  AND toLower(candidate.symbol) = wanted.candidate_key
  AND finding.doc_id = wanted.finding_doc_id
  AND (
    (wanted.comparison_id = ''
      AND reported.comparison_id IS NULL
      AND reported.role = 'finding_reported_comparator')
    OR reported.comparison_id = wanted.comparison_id
  )
OPTIONAL MATCH (finding)-[literature:HAS_LITERATURE_COMPARISON]
      ->(comparison:LiteratureComparison)
WHERE wanted.comparison_id <> ''
  AND coalesce(literature.comparison_id, comparison.comparison_id)
      = wanted.comparison_id
OPTIONAL MATCH (finding)-[citation:CITES]->(reference:Reference)
WHERE (
    wanted.comparison_id = ''
    AND coalesce(citation.comparison_id, reference.comparison_id) IS NULL
  ) OR (
    wanted.comparison_id <> ''
    AND coalesce(citation.comparison_id, reference.comparison_id)
        = wanted.comparison_id
  )
WITH wanted, target, finding, reported, candidate, comparison,
     collect(DISTINCT coalesce(reference.ref_id, citation.ref_id, reference.id))[0..4]
       AS reference_ids
RETURN DISTINCT
       wanted.record_id AS record_id,
       target.symbol AS anchor_gene,
       candidate.symbol AS candidate_gene,
       finding.doc_id AS finding_doc_id,
       reported.comparison_id AS comparison_id,
       CASE WHEN reported.comparison_id IS NULL
            THEN 'finding_scoped'
            ELSE 'exact_comparison_id' END AS pairing_precision,
       coalesce(comparison.summary, comparison.statement, finding.summary)
         AS evidence_summary,
       CASE WHEN reported.comparison_id IS NULL
            THEN finding.main_caveats
            ELSE comparison.context_limit END AS boundary_conditions,
       reference_ids
ORDER BY wanted.record_id
"""


def _auth_header(user: str, password: str) -> str:
    token = base64.b64encode(f"{user}:{password}".encode()).decode()
    return "Basic " + token


def run_query(
    statement: str,
    *,
    parameters: dict[str, Any],
    http_url: str,
    database: str,
    user: str,
    password: str,
    timeout: float,
) -> list[dict[str, Any]]:
    endpoint = f"{http_url.rstrip('/')}/db/{database}/tx/commit"
    body = json.dumps(
        {"statements": [{"statement": statement, "parameters": parameters}]}
    ).encode()
    request = urllib.request.Request(
        endpoint,
        data=body,
        method="POST",
        headers={
            "Authorization": _auth_header(user, password),
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Neo4j HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Cannot reach Neo4j at {endpoint}: {exc}") from exc
    errors = payload.get("errors") or []
    if errors:
        detail = "; ".join(
            f"{item.get('code')}: {item.get('message')}" for item in errors
        )
        raise RuntimeError(f"Cypher error: {detail}")
    results = payload.get("results") or []
    if not results:
        return []
    columns = results[0].get("columns") or []
    return [
        dict(zip(columns, item.get("row") or []))
        for item in results[0].get("data") or []
    ]


def _unique(values: Sequence[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        clean = str(value).strip()
        key = clean.casefold()
        if clean and key not in seen:
            seen.add(key)
            result.append(clean)
    return result


def _tabular_names(path: Path, preferred: Sequence[str]) -> list[str]:
    text = path.read_text(encoding="utf-8")
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        return []
    delimiter = "\t" if "\t" in lines[0] else ","
    reader = csv.DictReader(lines, delimiter=delimiter)
    if reader.fieldnames:
        by_key = {name.casefold(): name for name in reader.fieldnames}
        column = next((by_key[name.casefold()] for name in preferred if name.casefold() in by_key), None)
        if column is not None:
            return _unique([str(row.get(column) or "") for row in reader])
    return _unique(lines)


def _calibration_context(path: Path) -> tuple[list[str], Path]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    nested = payload.get("nested_evaluation") if isinstance(payload, dict) else None
    rows = nested.get("counterexamples") if isinstance(nested, dict) else None
    if not isinstance(rows, list):
        raise ValueError("calibration JSON has no nested_evaluation.counterexamples")
    anchors = _unique(
        [str(row.get("gene_target") or "") for row in rows if isinstance(row, dict)]
    )
    ranking_output = payload.get("ranking_output") if isinstance(payload, dict) else None
    if not isinstance(ranking_output, str) or not ranking_output.strip():
        raise ValueError("calibration JSON has no ranking_output")
    ranking_path = Path(ranking_output).expanduser()
    if not ranking_path.is_absolute():
        ranking_path = (path.parent / ranking_path).resolve()
    if not ranking_path.is_file():
        raise ValueError(f"calibration ranking_output does not exist: {ranking_path}")
    return anchors, ranking_path


def _calibration_anchors(path: Path) -> list[str]:
    """Compatibility helper for callers that need only the residual anchors."""

    return _calibration_context(path)[0]


def _clip(value: object, limit: int) -> str | None:
    text = " ".join(str(value or "").split())
    if not text:
        return None
    if len(text) <= limit:
        return text
    return text[: max(1, limit - 1)].rstrip() + "…"


def _record_id(row: dict[str, Any]) -> str:
    anchor = str(row.get("anchor_gene") or "unknown")
    candidate = str(row.get("candidate_gene") or "unknown")
    finding = str(row.get("finding_doc_id") or row.get("finding_id") or "unknown")
    pairing = str(row.get("comparison_id") or "finding-scoped")
    return f"direct::{anchor}::{candidate}::{finding}::{pairing}"


def _anchors_from_record_ids(record_ids: Sequence[str]) -> list[str]:
    return _unique([row["anchor_gene"] for row in _detail_requests(record_ids)])


def _detail_requests(record_ids: Sequence[str]) -> list[dict[str, str]]:
    requests = []
    for record_id in _unique(record_ids):
        parts = record_id.split("::")
        if len(parts) != 5 or parts[0] != "direct" or not all(parts[1:]):
            raise ValueError(f"invalid direct evidence record_id: {record_id}")
        anchor, candidate, finding_doc_id, pairing = parts[1:]
        requests.append(
            {
                "record_id": record_id,
                "anchor_gene": anchor,
                "anchor_key": anchor.casefold(),
                "candidate_gene": candidate,
                "candidate_key": candidate.casefold(),
                "finding_doc_id": finding_doc_id,
                "comparison_id": "" if pairing == "finding-scoped" else pairing,
            }
        )
    return requests


def _specificity_key(row: dict[str, Any]) -> tuple[int, int, str, str]:
    """Order model-facing evidence by retrieval specificity, never biology."""

    precision = str(row.get("pairing_precision") or "finding_scoped")
    exact_priority = 0 if precision == "exact_comparison_id" else 1
    anchor_priority = int(row.get("anchor_priority") or 10**9)
    return (
        exact_priority,
        anchor_priority,
        str(row.get("candidate_gene") or "").casefold(),
        str(row.get("finding_doc_id") or "").casefold(),
    )


def _presentation_order(rows: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    """Put exact pairs first, then interleave scoped records across anchors."""

    exact = sorted(
        [row for row in rows if row.get("pairing_precision") == "exact_comparison_id"],
        key=_specificity_key,
    )
    scoped = sorted(
        [row for row in rows if row.get("pairing_precision") != "exact_comparison_id"],
        key=_specificity_key,
    )
    by_anchor: dict[int, list[dict[str, Any]]] = {}
    for row in scoped:
        priority = int(row.get("anchor_priority") or 10**9)
        by_anchor.setdefault(priority, []).append(row)
    interleaved: list[dict[str, Any]] = []
    while any(by_anchor.values()):
        for priority in sorted(by_anchor):
            if by_anchor[priority]:
                interleaved.append(by_anchor[priority].pop(0))
    return [*exact, *interleaved]


def _index_record(row: dict[str, Any]) -> dict[str, Any]:
    pairing = (
        "exact"
        if row.get("pairing_precision") == "exact_comparison_id"
        else "finding_scoped_comparator"
    )
    record = {
        "record_id": _record_id(row),
        "anchor": row.get("anchor_gene"),
        "candidate": row.get("candidate_gene"),
        "pairing": pairing,
        "summary": _clip(row.get("evidence_summary"), 560),
    }
    return {
        key: value
        for key, value in record.items()
        if value not in (None, "", [])
    }


def _group_index_records(rows: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    """Deduplicate Finding-level prose while preserving candidate detail IDs."""

    groups: list[dict[str, Any]] = []
    scoped_by_finding: dict[tuple[str, str], dict[str, Any]] = {}
    for row in rows:
        record = _index_record(row)
        if record.get("pairing") == "exact":
            groups.append(record)
            continue
        key = (
            str(row.get("anchor_gene") or "").casefold(),
            str(row.get("finding_doc_id") or "").casefold(),
        )
        group = scoped_by_finding.get(key)
        if group is None:
            group = {
                key: value
                for key, value in record.items()
                if key not in {"candidate", "record_id"}
            }
            group["candidate_records"] = []
            scoped_by_finding[key] = group
            groups.append(group)
        candidate_record = {
            "candidate": record.get("candidate"),
            "record_id": record.get("record_id"),
        }
        if candidate_record not in group["candidate_records"]:
            group["candidate_records"].append(candidate_record)
    return groups


def _detail_record(row: dict[str, Any]) -> dict[str, Any]:
    exact = row.get("pairing_precision") == "exact_comparison_id"
    record = {
        "record_id": row.get("record_id") or _record_id(row),
        "anchor": row.get("anchor_gene"),
        "candidate": row.get("candidate_gene"),
        "pairing": "exact" if exact else "finding_scoped_comparator",
        "association_scope": (
            "The candidate, boundary conditions, and reference IDs share comparison_id."
            if exact
            else "The candidate is an explicitly tagged peer comparator in this Finding; finding-level reference IDs are not candidate-paired."
        ),
        "summary": _clip(row.get("evidence_summary"), 560),
        "boundary_conditions": _clip(row.get("boundary_conditions"), 480),
        "reference_ids": _unique(row.get("reference_ids") or []),
    }
    return {key: value for key, value in record.items() if value not in (None, "", [])}


def _fit_records_to_budget(
    *,
    base: dict[str, Any],
    records: Sequence[dict[str, Any]],
    max_records: int,
    max_output_chars: int,
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for record in records[:max_records]:
        trial = {**base, "records": [*selected, record]}
        if len(json.dumps(trial, ensure_ascii=False, indent=2)) > max_output_chars:
            break
        selected.append(record)
    return selected


def _with_output_char_count(payload: dict[str, Any]) -> dict[str, Any]:
    result = {**payload, "output_char_count": 0}
    for _ in range(4):
        count = len(json.dumps(result, ensure_ascii=False, indent=2)) + 1
        if result["output_char_count"] == count:
            break
        result["output_char_count"] = count
    return result


def retrieve_direct_evidence(
    *,
    anchors: Sequence[str],
    candidates: Sequence[str],
    max_anchors: int,
    max_records_per_anchor: int,
    max_decision_records: int = DEFAULT_MAX_DECISION_RECORDS,
    max_output_chars: int = DEFAULT_MAX_OUTPUT_CHARS,
    detail_record_ids: Sequence[str] = (),
    retrieval_policy: str = "library_parameters",
    candidate_source: str = "caller_supplied",
    connection: dict[str, Any],
    query_runner: Callable[..., list[dict[str, Any]]] = run_query,
) -> dict[str, Any]:
    if max_anchors < 1 or max_anchors > 25:
        raise ValueError("max_anchors must be between 1 and 25")
    if max_records_per_anchor < 1 or max_records_per_anchor > 25:
        raise ValueError("max_records_per_anchor must be between 1 and 25")
    if max_decision_records < 1 or max_decision_records > DEFAULT_MAX_DECISION_RECORDS:
        raise ValueError(
            f"max_decision_records must be between 1 and {DEFAULT_MAX_DECISION_RECORDS}"
        )
    if max_output_chars < 4_000 or max_output_chars > DEFAULT_MAX_OUTPUT_CHARS:
        raise ValueError(
            f"max_output_chars must be between 4,000 and {DEFAULT_MAX_OUTPUT_CHARS}"
        )
    selected_detail_ids = _unique(detail_record_ids)
    if len(selected_detail_ids) > MAX_DETAIL_RECORDS:
        raise ValueError(f"at most {MAX_DETAIL_RECORDS} detail record IDs may be requested")
    if selected_detail_ids:
        detail_requests = _detail_requests(selected_detail_ids)
        raw_rows = query_runner(
            DIRECT_EVIDENCE_DETAIL_QUERY,
            parameters={"record_rows": detail_requests},
            **connection,
        )
        by_id = {
            str(row.get("record_id")): _detail_record(dict(row))
            for row in raw_rows
            if row.get("record_id")
        }
        selected_details = [
            by_id[record_id]
            for record_id in selected_detail_ids
            if record_id in by_id
        ]
        result = {
            "schema_version": SCHEMA_VERSION,
            "status": "passed",
            "view": "detail",
            "retrieval_controls": {
                "policy": retrieval_policy,
                "max_detail_records": MAX_DETAIL_RECORDS,
            },
            "association_guard": (
                "Only exact records pair candidate-specific qualifiers and reference "
                "IDs. Finding-scoped records provide peer-comparator context only."
            ),
            "requested_record_ids": selected_detail_ids,
            "missing_record_ids": [
                record_id
                for record_id in selected_detail_ids
                if record_id not in by_id
            ],
            "retrieved_record_count": len(raw_rows),
            "record_count": len(selected_details),
            "records": selected_details,
        }
        result = _with_output_char_count(result)
        if result["output_char_count"] > max_output_chars:
            raise ValueError(
                "requested detail records exceed max_output_chars; request one record at a time"
            )
        return result

    selected_anchors = _unique(anchors)[:max_anchors]
    if not selected_anchors:
        raise ValueError("at least one anchor is required for an index query")
    selected_candidates = _unique(candidates)
    if len(selected_candidates) > 10000:
        raise ValueError("candidate universe exceeds 10,000 entities")
    anchor_rows = [
        {"priority": index, "symbol": symbol, "key": symbol.casefold()}
        for index, symbol in enumerate(selected_anchors, 1)
    ]
    raw_rows = query_runner(
        DIRECT_EVIDENCE_INDEX_QUERY,
        parameters={
            "anchors": anchor_rows,
            "candidate_keys": [value.casefold() for value in selected_candidates],
            "max_records_per_anchor": max_records_per_anchor,
        },
        **connection,
    )
    ordered_rows = _presentation_order([dict(row) for row in raw_rows])
    compact_records = _group_index_records(ordered_rows)
    base = {
        "schema_version": SCHEMA_VERSION,
        "status": "passed",
        "view": "index",
        "retrieval_controls": {
            "policy": retrieval_policy,
            "max_anchors": max_anchors,
            "max_records_per_anchor": max_records_per_anchor,
            "max_decision_records": max_decision_records,
            "max_output_chars": max_output_chars,
            "candidate_source": candidate_source,
            "candidate_universe_count": len(selected_candidates),
        },
        "decision_guard": (
            "Summary-first, unranked evidence: exactness orders retrieval, not "
            "biological merit. Load qualifiers only when a missing contextual fact "
            "could change a material decision; resolve full provenance separately."
        ),
        "anchors": selected_anchors,
        "retrieved_record_count": len(raw_rows),
    }
    selected_records = _fit_records_to_budget(
        base=base,
        records=compact_records,
        max_records=max_decision_records,
        max_output_chars=max_output_chars,
    )
    while True:
        result = _with_output_char_count(
            {
                **base,
                "record_count": len(selected_records),
                "omitted_record_count": len(compact_records) - len(selected_records),
                "exact_record_count": sum(
                    record.get("pairing") == "exact"
                    for record in selected_records
                ),
                "records": selected_records,
            }
        )
        if result["output_char_count"] <= max_output_chars or not selected_records:
            return result
        selected_records.pop()


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--anchor", action="append", default=[])
    parser.add_argument("--anchors-file", type=Path)
    parser.add_argument("--calibration", type=Path)
    parser.add_argument(
        "--detail-record",
        action="append",
        default=[],
        help=(
            "emit compact boundary conditions and reference IDs for this "
            "record_id (repeat at most three times)"
        ),
    )
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--http-url", default=DEFAULT_HTTP_URL)
    parser.add_argument("--database", default=DEFAULT_DATABASE)
    parser.add_argument("--user", default=DEFAULT_USER)
    parser.add_argument("--password", default=DEFAULT_PASSWORD)
    parser.add_argument("--timeout", type=float, default=120.0)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        anchors = list(args.anchor)
        anchors.extend(_anchors_from_record_ids(args.detail_record))
        if args.anchors_file:
            anchors.extend(_tabular_names(args.anchors_file, ("gene_target", "anchor_gene")))
        candidates: list[str] = []
        candidate_source = "none"
        if args.calibration:
            calibration_anchors, ranking_path = _calibration_context(args.calibration)
            anchors.extend(calibration_anchors)
            candidates = _tabular_names(
                ranking_path, ("gene_target", "candidate_gene")
            )
            candidate_source = "calibration_ranking_output"
        result = retrieve_direct_evidence(
            anchors=anchors,
            candidates=candidates,
            max_anchors=DEFAULT_MAX_ANCHORS,
            max_records_per_anchor=DEFAULT_MAX_RECORDS_PER_ANCHOR,
            max_decision_records=DEFAULT_MAX_DECISION_RECORDS,
            max_output_chars=DEFAULT_MAX_OUTPUT_CHARS,
            detail_record_ids=args.detail_record,
            retrieval_policy="host_frozen_cli",
            candidate_source=candidate_source,
            connection={
                "http_url": args.http_url,
                "database": args.database,
                "user": args.user,
                "password": args.password,
                "timeout": args.timeout,
            },
        )
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        error = {"schema_version": SCHEMA_VERSION, "status": "failed", "error": str(exc)}
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(error, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(error, indent=2))
        return 1
    print(
        json.dumps(
            {
                "schema_version": result["schema_version"],
                "status": result["status"],
                "view": result["view"],
                "output": str(args.out),
                "retrieved_record_count": result["retrieved_record_count"],
                "record_count": result["record_count"],
                "exact_record_count": result.get("exact_record_count"),
                "omitted_record_count": result.get("omitted_record_count"),
                "output_char_count": result["output_char_count"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
