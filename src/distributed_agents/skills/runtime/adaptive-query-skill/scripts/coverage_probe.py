#!/usr/bin/env python3
"""Build a compact, deterministic evidence-coverage portrait for one task."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from distributed_agents.corpus.registry import get_release


PACKAGE_DIR = Path(__file__).resolve().parents[4]
ACTIVE_RELEASE = get_release()
DEFAULT_FINDINGS = ACTIVE_RELEASE.artifact("findings")
DEFAULT_BIOKG = ACTIVE_RELEASE.projection("biokg")
DEFAULT_ASSIGNMENTS = DEFAULT_BIOKG / "data" / "claims" / "claim_assignments.tsv"
DEFAULT_RELATIONS = DEFAULT_BIOKG / "data" / "claims" / "claim_relations.tsv"
TOKEN_RE = re.compile(r"(?<![A-Za-z0-9_])([A-Za-z][A-Za-z0-9_.-]{1,})(?![A-Za-z0-9_])")
CELL_TYPE_RE = re.compile(
    r"\b\d{3}\s+[A-Za-z0-9][A-Za-z0-9+\- ]{2,80}?(?:Glut|GABA|Dopa)\b",
    re.IGNORECASE,
)
PARQUET_RE = re.compile(r"(?P<path>(?:/|\.{1,2}/)?[^\s`'\"]+\.parquet)", re.I)


def _existing(value: str | None, fallback: Path | None = None) -> Path | None:
    if value:
        candidate = Path(value).expanduser().resolve()
    elif fallback is not None:
        candidate = fallback.expanduser().resolve()
    else:
        return None
    return candidate if candidate.is_file() else None


def _split(value: object) -> list[str]:
    return [part for part in str(value or "").split("|") if part]


def _delimited(value: object) -> str:
    if isinstance(value, list):
        return "|".join(str(item) for item in value if str(item))
    return str(value or "")


def _table_delimiter(path: Path) -> str:
    """Detect the declared tabular delimiter from the header."""

    with path.open(encoding="utf-8") as handle:
        header = handle.readline()
    return "\t" if "\t" in header else ","


def _finding_records(path: Path) -> Iterable[dict[str, Any]]:
    if path.suffix.casefold() == ".jsonl":
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    row = json.loads(line)
                    if isinstance(row, dict):
                        yield row
        return
    with path.open(newline="", encoding="utf-8") as handle:
        yield from csv.DictReader(handle)


def _read_findings(path: Path | None) -> tuple[set[str], list[dict[str, str]]]:
    if path is None:
        return set(), []
    targets: set[str] = set()
    rows: list[dict[str, str]] = []
    for row in _finding_records(path):
        target = str(row.get("target_gene") or row.get("gene_target") or "").strip()
        if not target:
            continue
        targets.add(target)
        rows.append(
            {
                "gene_target": target,
                "finding_id": str(row.get("finding_id") or ""),
                "finding_type": str(row.get("finding_type") or ""),
                "summary": str(row.get("summary") or ""),
                "why_it_matters": str(row.get("why_it_matters") or ""),
                "cell_types": _delimited(row.get("cell_types")),
                "comparators": _delimited(row.get("comparators")),
                "evidence_ids": _delimited(row.get("evidence_ids")),
                "ref_ids": _delimited(row.get("ref_ids")),
            }
        )
    return targets, rows


def _read_assignments(
    path: Path | None,
) -> tuple[dict[str, dict[str, Any]], set[str]]:
    if path is None:
        return {}, set()
    claims: dict[str, dict[str, Any]] = {}
    targets: set[str] = set()
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter=_table_delimiter(path)):
            claim_id = str(row.get("claim_id") or "")
            claim_targets = _split(row.get("targets"))
            targets.update(claim_targets)
            if not claim_id:
                continue
            claim = claims.setdefault(
                claim_id,
                {
                    "claim_id": claim_id,
                    "targets": set(),
                    "summary": str(row.get("canonical_summary") or ""),
                    "relation_family": str(row.get("relation_family") or ""),
                    "confidence": str(row.get("confidence") or ""),
                    "doc_ids": [],
                },
            )
            claim["targets"].update(claim_targets)
            doc_id = str(row.get("doc_id") or "")
            if doc_id:
                claim["doc_ids"].append(doc_id)
    return claims, targets


def _task_targets(task: str, known_targets: Iterable[str]) -> list[str]:
    lookup = {target.casefold(): target for target in known_targets}
    seen: set[str] = set()
    result: list[str] = []
    for match in TOKEN_RE.finditer(task):
        target = lookup.get(match.group(1).rstrip(".-").casefold())
        if target and target not in seen:
            seen.add(target)
            result.append(target)
    return result


def _binding_targets(path: Path | None, known_targets: Iterable[str]) -> list[str]:
    if path is None or not path.is_file():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    lookup = {target.casefold(): target for target in known_targets}
    result: list[str] = []
    for entity_set in payload.get("entity_sets", []):
        if not isinstance(entity_set, dict) or not entity_set.get(
            "active_for_coverage"
        ):
            continue
        for item in entity_set.get("items", []):
            if not isinstance(item, dict):
                continue
            canonical = lookup.get(str(item.get("canonical") or "").casefold())
            if canonical and canonical not in result:
                result.append(canonical)
    return result


def _bounded_findings(
    rows: list[dict[str, str]],
    targets: list[str],
    *,
    limit: int,
) -> tuple[list[dict[str, Any]], dict[str, int], dict[str, int]]:
    wanted = set(targets)
    matched = [row for row in rows if row["gene_target"] in wanted]
    per_target: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in matched:
        per_target[row["gene_target"]].append(row)
    snippets: list[dict[str, Any]] = []
    if wanted:
        per_gene = max(1, limit // len(wanted))
        for target in targets:
            for row in per_target.get(target, [])[:per_gene]:
                snippets.append(
                    {
                        **row,
                        "comparators": _split(row["comparators"]),
                        "cell_types": _split(row["cell_types"]),
                        "evidence_ids": _split(row["evidence_ids"]),
                        "ref_ids": _split(row["ref_ids"]),
                    }
                )
                if len(snippets) >= limit:
                    break
            if len(snippets) >= limit:
                break
    return (
        snippets,
        dict(Counter(row["gene_target"] for row in matched)),
        dict(Counter(row["finding_type"] for row in matched)),
    )


def _bounded_claims(
    claims: dict[str, dict[str, Any]],
    task_targets: list[str],
    *,
    limit: int,
) -> tuple[list[dict[str, Any]], set[str]]:
    wanted = set(task_targets)
    selected: list[dict[str, Any]] = []
    selected_ids: set[str] = set()
    for claim_id, claim in claims.items():
        overlap = sorted(wanted.intersection(claim["targets"]))
        if not overlap:
            continue
        selected.append(
            {
                "claim_id": claim_id,
                "matched_targets": overlap,
                "targets": sorted(claim["targets"]),
                "summary": claim["summary"],
                "relation_family": claim["relation_family"],
                "confidence": claim["confidence"],
                "doc_ids": claim["doc_ids"][:8],
            }
        )
        selected_ids.add(claim_id)
        if len(selected) >= limit:
            break
    return selected, selected_ids


def _bounded_relations(
    path: Path | None,
    selected_claim_ids: set[str],
    task_targets: list[str],
    *,
    limit: int,
) -> tuple[list[dict[str, str]], int]:
    if path is None:
        return [], 0
    selected: list[dict[str, str]] = []
    matched_count = 0
    target_terms = tuple(target.casefold() for target in task_targets)
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter=_table_delimiter(path)):
            source = str(row.get("source_claim_id") or "")
            target = str(row.get("target_claim_id") or "")
            reason = str(row.get("reason") or "")
            by_claim = source in selected_claim_ids or target in selected_claim_ids
            by_text = bool(
                target_terms and any(term in reason.casefold() for term in target_terms)
            )
            if not (by_claim or by_text):
                continue
            matched_count += 1
            if len(selected) < limit:
                selected.append(
                    {
                        "source_claim_id": source,
                        "target_claim_id": target,
                        "relation_type": str(row.get("relation_type") or ""),
                        "confidence": str(row.get("confidence") or ""),
                        "reason": reason,
                    }
                )
    return selected, matched_count


def _report_targets(path: Path | None, targets: list[str]) -> list[str]:
    if path is None or not targets:
        return []
    wanted = {target.casefold(): target for target in targets}
    matched: set[str] = set()
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            raw = str(record.get("gene_target") or "")
            canonical = wanted.get(raw.casefold())
            if canonical:
                matched.add(canonical)
            if len(matched) == len(wanted):
                break
    return [target for target in targets if target in matched]


def build_coverage(args: argparse.Namespace) -> dict[str, Any]:
    task_path = Path(args.task).expanduser().resolve()
    task = task_path.read_text(encoding="utf-8")
    findings_path = _existing(
        args.findings_ledger or os.environ.get("DISTRIBUTED_AGENTS_FINDINGS_LEDGER"),
        DEFAULT_FINDINGS,
    )
    assignments_path = _existing(args.claim_assignments, DEFAULT_ASSIGNMENTS)
    relations_path = _existing(args.claim_relations, DEFAULT_RELATIONS)
    reports_path = _existing(
        args.reports or os.environ.get("BIOKG_REPORTS_PATH"),
        None,
    )

    finding_targets, finding_rows = _read_findings(findings_path)
    claims, claim_targets = _read_assignments(assignments_path)
    known_targets = finding_targets.union(claim_targets)
    targets = _task_targets(task, known_targets)
    binding_path = _existing(args.bindings)
    targets = list(
        dict.fromkeys([*targets, *_binding_targets(binding_path, known_targets)])
    )
    finding_snippets, finding_counts, finding_types = _bounded_findings(
        finding_rows,
        targets,
        limit=args.max_snippets,
    )
    claim_snippets, claim_ids = _bounded_claims(
        claims,
        targets,
        limit=args.max_snippets,
    )
    relation_snippets, relation_count = _bounded_relations(
        relations_path,
        claim_ids,
        targets,
        limit=args.max_snippets,
    )
    report_targets = _report_targets(reports_path, targets)
    parquet_paths = list(
        dict.fromkeys(match.group("path") for match in PARQUET_RE.finditer(task))
    )

    return {
        "schema_version": "distributed_agents-evidence-coverage-v1",
        "task": {
            "sha256": hashlib.sha256(task.encode()).hexdigest(),
            "characters": len(task),
        },
        "entities": {
            "gene_targets": targets,
            "gene_target_count": len(targets),
            "cell_types": list(dict.fromkeys(CELL_TYPE_RE.findall(task))),
            "declared_parquet_paths": [
                {
                    "path": value,
                    "host_readable": Path(value).expanduser().is_file(),
                }
                for value in parquet_paths
            ],
        },
        "sources": {
            "findings": {
                "available": findings_path is not None,
                "path": str(findings_path) if findings_path else None,
                "matched_targets": finding_counts,
                "finding_types": finding_types,
                "snippets": finding_snippets,
            },
            "claims": {
                "available": assignments_path is not None,
                "path": str(assignments_path) if assignments_path else None,
                "matched_claim_count": len(claim_snippets),
                "claims": claim_snippets,
            },
            "claim_relations": {
                "available": relations_path is not None,
                "path": str(relations_path) if relations_path else None,
                "matched_relation_count": relation_count,
                "relations": relation_snippets,
            },
            "reports": {
                "available": reports_path is not None,
                "path": str(reports_path) if reports_path else None,
                "matched_targets": report_targets,
            },
        },
        "interpretation_guard": (
            "Coverage is an index result over same-experiment representations. "
            "It is not biological support, independent replication, or a route label."
        ),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--findings-ledger")
    parser.add_argument("--claim-assignments")
    parser.add_argument("--claim-relations")
    parser.add_argument("--reports")
    parser.add_argument("--bindings")
    parser.add_argument("--max-snippets", type=int, default=24)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    payload = build_coverage(args)
    out = Path(args.out).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(
        json.dumps(
            {
                "out": str(out),
                "gene_target_count": payload["entities"]["gene_target_count"],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
