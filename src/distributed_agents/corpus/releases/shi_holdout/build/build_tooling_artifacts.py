#!/usr/bin/env python3
"""Build release-native relation and calibration artifacts for Shi holdout.

The Shi holdout source already contains structured Findings. This build keeps
each Finding as one atomic Claim for the structural relation layer. Relations are emitted
only when two target-scoped Findings explicitly name one another's targets as
comparators.  Such links nominate records for review; they do not assert
agreement, causal transfer, or biological priority.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


SCHEMA_VERSION = "distributed_agents-july-tooling-build-v1"
CALIBRATION_SCHEMA_VERSION = "distributed_agents-july-ledger-calibration-v1"
CLAIM_UNIT_VERSION = "july-atomic-finding-claim-v1"
RELATION_VERSION = "july-reciprocal-comparator-review-v1"
RELEASE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FINDINGS = RELEASE_ROOT / "artifacts" / "ledgers" / "findings.jsonl"
DEFAULT_RELATIONS_DIR = RELEASE_ROOT / "artifacts" / "relations"
DEFAULT_CONTRACTS_DIR = RELEASE_ROOT / "artifacts" / "contracts"

ASSIGNMENT_FIELDS = (
    "claim_id",
    "doc_id",
    "target_gene",
    "member_role",
    "canonical_summary",
    "relation_family",
    "direction_pattern",
    "targets",
    "finding_types",
    "confidence",
    "claim_unit",
    "source_hash",
)
RELATION_FIELDS = (
    "source_claim_id",
    "target_claim_id",
    "source_target",
    "target_target",
    "relation_type",
    "confidence",
    "basis",
    "reason",
    "relation_version",
)
DICTIONARY_FIELDS = (
    "artifact",
    "field",
    "value_or_pattern",
    "meaning",
    "non_meaning",
    "aliases",
    "derivation",
    "constraints",
    "related_fields",
    "example_ids",
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
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


def _write_csv(
    path: Path,
    rows: Sequence[Mapping[str, Any]],
    fields: Sequence[str],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.casefold()).strip("_")


def _claim_id(row: Mapping[str, Any]) -> str:
    source_hash = str(row.get("_source_record_sha256") or "")
    if not re.fullmatch(r"[0-9a-f]{64}", source_hash):
        raise ValueError(f"{row.get('doc_id')}: missing source-record SHA-256")
    return f"claim:atomic:{_slug(str(row['doc_id']))}_{source_hash[:12]}"


def _pipe(values: object) -> str:
    if not isinstance(values, list):
        return ""
    return "|".join(str(value) for value in values if str(value))


def build_atomic_claims(
    findings: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, str]], dict[str, str]]:
    assignments: list[dict[str, str]] = []
    by_doc_id: dict[str, str] = {}
    for row in findings:
        doc_id = str(row.get("doc_id") or "")
        target = str(row.get("target_gene") or "")
        finding_id = str(row.get("finding_id") or "")
        if not doc_id or doc_id != f"{target}:{finding_id}":
            raise ValueError(f"invalid target-scoped Finding identity: {doc_id!r}")
        claim_id = _claim_id(row)
        if doc_id in by_doc_id:
            raise ValueError(f"duplicate Finding identity: {doc_id}")
        by_doc_id[doc_id] = claim_id
        assignments.append(
            {
                "claim_id": claim_id,
                "doc_id": doc_id,
                "target_gene": target,
                "member_role": "anchor",
                "canonical_summary": str(row.get("summary") or ""),
                "relation_family": str(row.get("finding_type") or ""),
                "direction_pattern": str(row.get("direction") or ""),
                "targets": target,
                "finding_types": str(row.get("finding_type") or ""),
                "confidence": str(row.get("confidence") or ""),
                "claim_unit": CLAIM_UNIT_VERSION,
                "source_hash": str(row.get("_source_record_sha256") or ""),
            }
        )
    assignments.sort(key=lambda row: row["doc_id"].casefold())
    return assignments, by_doc_id


def build_relations(
    findings: Sequence[Mapping[str, Any]],
    claim_by_doc_id: Mapping[str, str],
) -> list[dict[str, str]]:
    by_target: dict[str, list[tuple[Mapping[str, Any], set[str]]]] = defaultdict(list)
    display: dict[str, str] = {}
    for row in findings:
        target = str(row["target_gene"])
        key = target.casefold()
        display.setdefault(key, target)
        comparator_keys = {
            str(value).casefold()
            for value in row.get("comparators") or []
            if str(value).strip() and str(value).casefold() != key
        }
        by_target[key].append((row, comparator_keys))

    unique: dict[tuple[str, str], dict[str, str]] = {}
    for source in findings:
        source_target = str(source["target_gene"])
        source_key = source_target.casefold()
        for target_key in sorted(
            {
                str(value).casefold()
                for value in source.get("comparators") or []
                if str(value).strip()
            }
        ):
            if target_key == source_key:
                continue
            for target, target_comparators in by_target.get(target_key, []):
                if source_key not in target_comparators:
                    continue
                source_doc = str(source["doc_id"])
                target_doc = str(target["doc_id"])
                source_claim = claim_by_doc_id[source_doc]
                target_claim = claim_by_doc_id[target_doc]
                key = (source_claim, target_claim)
                unique[key] = {
                    "source_claim_id": source_claim,
                    "target_claim_id": target_claim,
                    "source_target": source_target,
                    "target_target": str(target["target_gene"]),
                    "relation_type": "REVIEW_WITH",
                    "confidence": "structural_only",
                    "basis": "reciprocal_explicit_comparator",
                    "reason": (
                        f"{source_doc} and {target_doc} explicitly name one "
                        "another's perturbation targets as comparators."
                    ),
                    "relation_version": RELATION_VERSION,
                }
    return [unique[key] for key in sorted(unique)]


def _frequency(
    rows: Iterable[Mapping[str, Any]], field: str
) -> list[dict[str, Any]]:
    counts: Counter[str] = Counter()
    for row in rows:
        value = row.get(field)
        if isinstance(value, list):
            counts.update(str(item) for item in value)
        else:
            counts[str(value or "")] += 1
    return [
        {"value": value, "count": count}
        for value, count in sorted(
            counts.items(), key=lambda item: (-item[1], item[0].casefold())
        )
    ]


def _crosstab(
    rows: Iterable[Mapping[str, Any]], left: str, right: str
) -> list[dict[str, Any]]:
    counts = Counter(
        (str(row.get(left) or ""), str(row.get(right) or "")) for row in rows
    )
    return [
        {left: key[0], right: key[1], "count": count}
        for key, count in sorted(counts.items())
    ]


def _is_control(target: str) -> bool:
    folded = target.casefold()
    return folded == "non_target" or folded.startswith("safe_target_")


def _check(identifier: str, actual: object, expected: object) -> dict[str, Any]:
    if actual != expected:
        raise ValueError(f"{identifier}: {actual!r} != {expected!r}")
    return {"id": identifier, "status": "passed", "actual": actual, "expected": expected}


def _source(
    path: Path, schema_version: str, *, logical_path: str
) -> dict[str, Any]:
    return {
        "path": logical_path,
        "sha256": _sha256(path),
        "schema_version": schema_version,
    }


def build_calibration(
    *,
    findings: Sequence[Mapping[str, Any]],
    assignments: Sequence[Mapping[str, str]],
    relations: Sequence[Mapping[str, str]],
    findings_path: Path,
    assignments_path: Path,
    relations_path: Path,
) -> dict[str, Any]:
    targets = {str(row["target_gene"]) for row in findings}
    controls = {target for target in targets if _is_control(target)}
    claims = {row["claim_id"] for row in assignments}
    relation_claims = {
        value
        for row in relations
        for value in (row["source_claim_id"], row["target_claim_id"])
    }
    relation_pairs = {
        (row["source_claim_id"], row["target_claim_id"]) for row in relations
    }
    findings_with_comparators = sum(bool(row.get("comparators")) for row in findings)
    high_confidence = sum(str(row.get("confidence")) == "high" for row in findings)
    exploratory_or_low = sum(
        str(row.get("confidence")) in {"exploratory", "low"} for row in findings
    )
    checks = [
        _check("finding_doc_ids_unique", len({str(row["doc_id"]) for row in findings}), len(findings)),
        _check("assignment_doc_ids_unique", len({row["doc_id"] for row in assignments}), len(assignments)),
        _check("one_atomic_claim_per_finding", len(assignments), len(findings)),
        _check("claim_ids_unique", len(claims), len(assignments)),
        _check("relation_endpoints_resolve", relation_claims.issubset(claims), True),
        _check(
            "relations_are_reciprocal_pairs",
            all(
                (row["target_claim_id"], row["source_claim_id"])
                in relation_pairs
                for row in relations
            ),
            True,
        ),
    ]
    finding_frequency_fields = (
        "finding_type",
        "confidence",
        "direction",
        "lit_direction",
        "lit_novelty",
    )
    claim_frequency_fields = ("relation_family", "confidence", "claim_unit")
    return {
        "schema_version": CALIBRATION_SCHEMA_VERSION,
        "generation_version": SCHEMA_VERSION,
        "sources": {
            "findings": _source(
                findings_path,
                "july-finding-jsonl-v1",
                logical_path="artifacts/ledgers/findings.jsonl",
            ),
            "claim_assignments": _source(
                assignments_path,
                CLAIM_UNIT_VERSION,
                logical_path="artifacts/relations/claim_assignments.csv",
            ),
            "claim_relations": _source(
                relations_path,
                RELATION_VERSION,
                logical_path="artifacts/relations/claim_relations.csv",
            ),
        },
        "counts": {
            "findings": len(findings),
            "claims": len(claims),
            "claim_assignment_rows": len(assignments),
            "targets_with_findings": len(targets),
            "biological_targets_with_findings": len(targets - controls),
            "controls_with_findings": len(controls),
            "claim_relations": len(relations),
        },
        "field_value_frequencies": {
            "findings": {
                field: _frequency(findings, field) for field in finding_frequency_fields
            },
            "claims": {
                field: _frequency(assignments, field) for field in claim_frequency_fields
            },
            "relations": {
                "relation_type": _frequency(relations, "relation_type"),
                "confidence": _frequency(relations, "confidence"),
                "basis": _frequency(relations, "basis"),
            },
        },
        "crosstabs": {
            "finding_confidence_by_type": _crosstab(findings, "confidence", "finding_type"),
            "finding_literature_direction_by_type": _crosstab(findings, "lit_direction", "finding_type"),
        },
        "atomic_claim_projection": {
            "unit": CLAIM_UNIT_VERSION,
            "finding_rows": len(findings),
            "claim_review_units": len(claims),
            "findings_per_claim": 1.0,
            "duplicate_reduction_fraction": 0.0,
            "interpretation": (
                "Each Shi holdout Finding is exposed as one atomic Claim for relation "
                "inspection. No semantic deduplication or cross-Finding merge was run."
            ),
        },
        "relation_projection": {
            "unit": RELATION_VERSION,
            "directed_relations": len(relations),
            "undirected_reciprocal_pairs": len(relations) // 2,
            "claims_with_a_relation": len(relation_claims),
            "interpretation": (
                "REVIEW_WITH records encode reciprocal explicit comparator mentions "
                "only. They do not assert agreement, transfer, causality, or priority."
            ),
        },
        "candidate_pool_descriptors": {
            "high_confidence_findings": high_confidence,
            "exploratory_or_low_confidence_findings": exploratory_or_low,
            "findings_with_comparators": findings_with_comparators,
            "claims_with_reciprocal_comparator_relations": len(relation_claims),
            "interpretation": (
                "Inventory descriptors only; none estimates biological importance, "
                "endpoint effect, or predictive performance."
            ),
        },
        "semantic_assertions": [
            {
                "id": "atomic_claim_identity",
                "statement": "A Shi holdout atomic Claim is exactly one Finding in the structural relation layer.",
            },
            {
                "id": "relation_scope",
                "statement": "REVIEW_WITH means reciprocal explicit comparator mention and only nominates a pair for review.",
            },
            {
                "id": "confidence_scope",
                "statement": "Finding confidence is confidence in the statement as written and can be high for a measured null or limitation.",
            },
            {
                "id": "frequency_not_priority",
                "statement": "Finding, comparator, citation, and relation frequencies are not biological priority scores.",
            },
            {
                "id": "no_de_recalibration",
                "statement": "This corpus calibration does not recompute endpoint measurements or differential expression.",
            },
            {
                "id": "claim_unit_scope",
                "statement": "Atomic structural Claim counts are not directly comparable to higher-order semantic Claim counts.",
            },
        ],
        "reconciliation": {"status": "passed", "checks": checks},
    }


def _dictionary_row(
    artifact: str,
    field: str,
    meaning: str,
    non_meaning: str,
    *,
    value: str = "*",
    aliases: str = "",
    derivation: str = "source artifact",
    constraints: str = "",
    related_fields: str = "",
    example_ids: str = "",
) -> dict[str, str]:
    return {
        "artifact": artifact,
        "field": field,
        "value_or_pattern": value,
        "meaning": meaning,
        "non_meaning": non_meaning,
        "aliases": aliases,
        "derivation": derivation,
        "constraints": constraints,
        "related_fields": related_fields,
        "example_ids": example_ids,
    }


def build_dictionary(
    findings: Sequence[Mapping[str, Any]],
    assignments: Sequence[Mapping[str, str]],
    relations: Sequence[Mapping[str, str]],
) -> list[dict[str, str]]:
    rows = [
        _dictionary_row(
            "corpus_identity",
            "Finding",
            "Target-scoped structured biological statement preserved from one Shi holdout report.",
            "Not an independent experiment or a calibrated priority unit.",
            aliases="atomic finding",
            related_fields="Claim|doc_id|finding_id",
        ),
        _dictionary_row(
            "corpus_identity",
            "Claim",
            "Compatibility review unit mapped one-to-one to a Shi holdout Finding.",
            "Not the legacy model-adjudicated duplicate-reduced Claim unit.",
            aliases="atomic claim",
            derivation=CLAIM_UNIT_VERSION,
            related_fields="Finding|claim_unit",
        ),
        _dictionary_row(
            "claim_relations",
            "relation_type",
            "REVIEW_WITH nominates two atomic Claims whose targets are reciprocal explicit comparators.",
            "Does not assert agreement, convergence, causal transfer, or priority.",
            value="REVIEW_WITH",
            derivation=RELATION_VERSION,
            related_fields="basis|source_claim_id|target_claim_id",
        ),
        _dictionary_row(
            "findings_ledger",
            "lit_direction",
            "Source-authored relationship between the Finding and its cited literature claim.",
            "Not a recomputed literature review or endpoint measurement.",
            related_fields="literature_claim|lit_context|lit_novelty",
        ),
        _dictionary_row(
            "findings_ledger",
            "comparators",
            "Perturbation targets explicitly named as comparators by this Finding.",
            "A mention is not positive support and does not imply reciprocal agreement.",
            related_fields="finding_type|direction|summary",
        ),
        _dictionary_row(
            "findings_ledger",
            "confidence",
            "Confidence in the Finding statement as written, including nulls and cautions.",
            "Not a novelty, effect-size, importance, or prediction score.",
        ),
    ]
    for artifact, source_rows, fields in (
        ("findings_ledger", findings, ("finding_type", "confidence", "lit_direction", "lit_novelty")),
        ("claim_assignments", assignments, ("member_role", "relation_family", "confidence", "claim_unit")),
        ("claim_relations", relations, ("relation_type", "confidence", "basis", "relation_version")),
    ):
        for field in fields:
            for item in _frequency(source_rows, field):
                rows.append(
                    _dictionary_row(
                        artifact,
                        field,
                        f"Observed {field} value in {item['count']} {artifact} rows.",
                        "Row frequency is not an independent biological-support or priority count.",
                        value=str(item["value"]) or "<empty>",
                        derivation=f"exact frequency from {artifact}",
                    )
                )
    return sorted(
        rows,
        key=lambda row: (
            row["artifact"], row["field"], row["value_or_pattern"].casefold()
        ),
    )


def build(
    *,
    findings_path: Path,
    relations_dir: Path,
    contracts_dir: Path,
) -> dict[str, Any]:
    findings = _read_jsonl(findings_path)
    assignments, claim_by_doc = build_atomic_claims(findings)
    relations = build_relations(findings, claim_by_doc)
    assignments_path = relations_dir / "claim_assignments.csv"
    relations_path = relations_dir / "claim_relations.csv"
    _write_csv(assignments_path, assignments, ASSIGNMENT_FIELDS)
    _write_csv(relations_path, relations, RELATION_FIELDS)

    calibration = build_calibration(
        findings=findings,
        assignments=assignments,
        relations=relations,
        findings_path=findings_path,
        assignments_path=assignments_path,
        relations_path=relations_path,
    )
    calibration_path = contracts_dir / "ledger_calibration.json"
    dictionary_path = contracts_dir / "value_dictionary.csv"
    _write_json(calibration_path, calibration)
    dictionary = build_dictionary(findings, assignments, relations)
    _write_csv(dictionary_path, dictionary, DICTIONARY_FIELDS)

    build_record = {
        "schema_version": SCHEMA_VERSION,
        "build_policy": {
            "claim_unit": CLAIM_UNIT_VERSION,
            "relation_unit": RELATION_VERSION,
            "semantic_deduplication": False,
            "model_calls": False,
            "network": False,
            "evaluation_inputs": False,
        },
        "inputs": {
            "findings": {
                "path": "artifacts/ledgers/findings.jsonl",
                "records": len(findings),
                "sha256": _sha256(findings_path),
            }
        },
        "outputs": {
            "claim_assignments": {
                "path": "artifacts/relations/claim_assignments.csv",
                "records": len(assignments),
                "bytes": assignments_path.stat().st_size,
                "sha256": _sha256(assignments_path),
            },
            "claim_relations": {
                "path": "artifacts/relations/claim_relations.csv",
                "records": len(relations),
                "bytes": relations_path.stat().st_size,
                "sha256": _sha256(relations_path),
            },
            "ledger_calibration": {
                "path": "artifacts/contracts/ledger_calibration.json",
                "records": 1,
                "bytes": calibration_path.stat().st_size,
                "sha256": _sha256(calibration_path),
            },
            "value_dictionary": {
                "path": "artifacts/contracts/value_dictionary.csv",
                "records": len(dictionary),
                "bytes": dictionary_path.stat().st_size,
                "sha256": _sha256(dictionary_path),
            },
        },
        "reconciliation": calibration["reconciliation"],
    }
    build_path = relations_dir / "tooling_build.json"
    _write_json(build_path, build_record)
    return {**build_record, "build_record": "artifacts/relations/tooling_build.json"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--findings", type=Path, default=DEFAULT_FINDINGS)
    parser.add_argument("--relations-dir", type=Path, default=DEFAULT_RELATIONS_DIR)
    parser.add_argument("--contracts-dir", type=Path, default=DEFAULT_CONTRACTS_DIR)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = build(
        findings_path=args.findings.resolve(),
        relations_dir=args.relations_dir.resolve(),
        contracts_dir=args.contracts_dir.resolve(),
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
