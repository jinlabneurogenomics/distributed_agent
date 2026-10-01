#!/usr/bin/env python3
"""Build compact, self-describing context cards for global candidate review.

Each card states whether the gene came from the quantitative starting result or
from a Claim relation, which starting genes it is related to, and what the
same-experiment Claims and Findings say. Starting rank is retained as declared
quantitative evidence; private graph-attention weights and DEG support fields
are not copied into the cards.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


SCHEMA_VERSION = "distributed_agents-candidate-context-card-v2"
RELATIONAL_FAMILIES = frozenset(
    {
        "convergence",
        "divergence",
        "non_interchangeability",
        "epistasis",
        "ectopic",
        "uncoupling",
        "compensation",
    }
)
CONFIDENCE_ORDER = {"high": 0, "moderate": 1, "low": 2}
FINDING_TYPE_ORDER = {
    "cross_perturbation_contrast": 0,
    "pathway_uncoupling": 1,
    "negative_result": 2,
    "buffered_response": 3,
    "therapeutic_direction_warning": 4,
}


def _delimiter(path: Path) -> str:
    return "\t" if path.suffix.casefold() == ".tsv" else ","


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter=_delimiter(path)))


def _split(value: str) -> list[str]:
    return [item.strip() for item in str(value or "").split("|") if item.strip()]


def _candidate_column(rows: list[dict[str, str]], path: Path) -> str:
    if not rows:
        raise ValueError(f"candidate table is empty: {path}")
    for field in ("gene_target", "candidate", "gene"):
        if field in rows[0]:
            return field
    raise ValueError(f"candidate table lacks gene_target/candidate/gene: {path}")


def _claim_priority(row: dict[str, str]) -> tuple[object, ...]:
    family = row.get("relation_family", "").casefold()
    return (
        0 if family in RELATIONAL_FAMILIES else 1,
        0 if row.get("active_default", "").casefold() == "true" else 1,
        CONFIDENCE_ORDER.get(row.get("confidence", "").casefold(), 3),
        row.get("doc_id", "").casefold(),
    )


def _finding_priority(row: dict[str, str]) -> tuple[object, ...]:
    return (
        FINDING_TYPE_ORDER.get(row.get("finding_type", "").casefold(), 5),
        CONFIDENCE_ORDER.get(row.get("confidence", "").casefold(), 3),
        row.get("finding_id", "").casefold(),
    )


def _aligned(row: dict[str, str], fields: tuple[str, ...]) -> list[dict[str, str]]:
    values = {field: _split(row.get(field, "")) for field in fields}
    width = max((len(items) for items in values.values()), default=0)
    aligned: list[dict[str, str]] = []
    for index in range(width):
        aligned.append(
            {
                field: (
                    values[field][index]
                    if index < len(values[field]) and values[field][index] != "-"
                    else ""
                )
                for field in fields
            }
        )
    return aligned


def build_cards(
    *,
    starting_ranking: Path,
    starting_count: int,
    attention_candidates: Path | None,
    claims_path: Path,
    findings_path: Path,
    out_path: Path,
    max_claim_paths: int = 3,
    max_findings: int = 4,
) -> dict[str, int]:
    if starting_count < 1:
        raise ValueError("starting_count must be positive")
    if max_claim_paths < 1 or max_findings < 1:
        raise ValueError("card limits must be positive")

    starting_rows = _read_rows(starting_ranking)
    starting_column = _candidate_column(starting_rows, starting_ranking)
    if any(row.get("rank", "").strip() for row in starting_rows):
        starting_rows.sort(
            key=lambda row: float(row.get("rank", "") or float("inf"))
        )
    starting: list[str] = []
    starting_rank: dict[str, int] = {}
    seen: set[str] = set()
    for row in starting_rows:
        candidate = row.get(starting_column, "").strip()
        if candidate and candidate.casefold() not in seen:
            starting.append(candidate)
            seen.add(candidate.casefold())
            starting_rank[candidate.casefold()] = int(
                float(row.get("rank", "") or len(starting))
            )
        if len(starting) == starting_count:
            break
    if len(starting) < starting_count:
        raise ValueError(
            f"starting ranking has {len(starting)} unique candidates, "
            f"expected {starting_count}"
        )

    attention_rows = (
        _read_rows(attention_candidates) if attention_candidates is not None else []
    )
    attention_by_candidate = {
        (row.get("gene_target") or row.get("candidate") or "").strip(): row
        for row in attention_rows
        if (row.get("gene_target") or row.get("candidate") or "").strip()
    }
    starting_fold = {candidate.casefold() for candidate in starting}
    related_candidates = sorted(
        (
            candidate
            for candidate in attention_by_candidate
            if candidate.casefold() not in starting_fold
        ),
        key=str.casefold,
    )

    claims = _read_rows(claims_path)
    claims_by_id = {
        row.get("doc_id", "").strip(): row
        for row in claims
        if row.get("doc_id", "").strip()
    }
    claims_by_target: dict[str, list[dict[str, str]]] = {}
    for row in claims:
        for target in _split(row.get("targets", "")):
            claims_by_target.setdefault(target.casefold(), []).append(row)

    findings = _read_rows(findings_path)
    findings_by_doc: dict[str, dict[str, str]] = {}
    findings_by_target: dict[str, list[dict[str, str]]] = {}
    for row in findings:
        target = row.get("target_gene", "").strip()
        finding_id = row.get("finding_id", "").strip()
        if target and finding_id:
            findings_by_doc[f"{target}:{finding_id}".casefold()] = row
            findings_by_target.setdefault(target.casefold(), []).append(row)

    cards: list[dict[str, object]] = []
    for candidate in sorted([*starting, *related_candidates], key=str.casefold):
        attention = attention_by_candidate.get(candidate)
        path_rows: list[dict[str, str]] = []
        if attention is not None:
            # Accept the original field names for old diagnostic artifacts, but
            # emit only the clearer v2 names below.
            path_rows = _aligned(
                attention,
                (
                    (
                        "linked_starting_genes"
                        if "linked_starting_genes" in attention
                        else "sponsoring_anchors"
                    ),
                    (
                        "relation_roles"
                        if "relation_roles" in attention
                        else "attention_roles"
                    ),
                    "claim_ids" if "claim_ids" in attention else "attention_claim_ids",
                    "linked_claim_ids",
                    "relation_types",
                    "relation_families",
                    "direction_patterns",
                    "semantic_relation_classes",
                ),
            )[:max_claim_paths]
            for path in path_rows:
                path["linked_starting_genes"] = path.pop(
                    "linked_starting_genes",
                    path.pop("sponsoring_anchors", ""),
                )
                path["relation_roles"] = path.pop(
                    "relation_roles",
                    path.pop("attention_roles", ""),
                )
                path["claim_ids"] = path.pop(
                    "claim_ids",
                    path.pop("attention_claim_ids", ""),
                )
        else:
            for claim in sorted(
                claims_by_target.get(candidate.casefold(), []),
                key=_claim_priority,
            )[:max_claim_paths]:
                path_rows.append(
                    {
                        "linked_starting_genes": candidate,
                        "relation_roles": "gene_claim",
                        "claim_ids": claim.get("doc_id", ""),
                        "linked_claim_ids": "",
                        "relation_types": "",
                        "relation_families": claim.get("relation_family", ""),
                        "direction_patterns": claim.get("direction_pattern", ""),
                        "semantic_relation_classes": "self_claim",
                    }
                )

        claim_cards: list[dict[str, str]] = []
        member_doc_ids: list[str] = []
        for path in path_rows:
            claim_id = path.get("claim_ids", "")
            claim = claims_by_id.get(claim_id, {})
            claim_cards.append(
                {
                    "linked_starting_gene": path.get("linked_starting_genes", ""),
                    "relation_role": path.get("relation_roles", ""),
                    "claim_id": claim_id,
                    "linked_claim_id": path.get("linked_claim_ids", ""),
                    "relation_type": path.get("relation_types", ""),
                    "relation_family": path.get("relation_families", ""),
                    "direction_pattern": path.get("direction_patterns", ""),
                    "semantic_relation_class": path.get(
                        "semantic_relation_classes", ""
                    ),
                    "canonical_summary": claim.get("canonical_summary", ""),
                }
            )
            member_doc_ids.extend(_split(claim.get("member_doc_ids", "")))

        candidate_findings: list[dict[str, str]] = []
        used_finding_ids: set[str] = set()
        for doc_id in member_doc_ids:
            row = findings_by_doc.get(doc_id.casefold())
            if row is None or row.get("target_gene", "").casefold() != (
                candidate.casefold()
            ):
                continue
            finding_id = row.get("finding_id", "")
            if finding_id not in used_finding_ids:
                candidate_findings.append(row)
                used_finding_ids.add(finding_id)
        for row in sorted(
            findings_by_target.get(candidate.casefold(), []),
            key=_finding_priority,
        ):
            finding_id = row.get("finding_id", "")
            if finding_id not in used_finding_ids:
                candidate_findings.append(row)
                used_finding_ids.add(finding_id)
            if len(candidate_findings) >= max_findings:
                break
        candidate_findings = sorted(candidate_findings, key=_finding_priority)[
            :max_findings
        ]

        cards.append(
            {
                "schema_version": SCHEMA_VERSION,
                "gene_target": candidate,
                "comparison_origin": (
                    "quantitative_starting_result"
                    if candidate.casefold() in starting_fold
                    else "claim_related_candidate"
                ),
                "quantitative_starting_evidence": {
                    "included": candidate.casefold() in starting_fold,
                    "starting_rank": starting_rank.get(candidate.casefold()),
                },
                "same_experiment_relations": claim_cards,
                "same_experiment_findings": [
                    {
                        "finding_id": row.get("finding_id", ""),
                        "finding_type": row.get("finding_type", ""),
                        "direction": row.get("direction", ""),
                        "confidence": row.get("confidence", ""),
                        "summary": row.get("summary", ""),
                        "why_it_matters": row.get("why_it_matters", ""),
                        "main_caveats": row.get("main_caveats", ""),
                    }
                    for row in candidate_findings
                ],
            }
        )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as handle:
        for card in cards:
            handle.write(json.dumps(card, sort_keys=True) + "\n")
    return {
        "starting_candidates": len(starting),
        "related_candidates": len(related_candidates),
        "cards": len(cards),
        "claims": sum(len(card["same_experiment_relations"]) for card in cards),
        "findings": sum(len(card["same_experiment_findings"]) for card in cards),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--starting-ranking", type=Path, required=True)
    parser.add_argument("--starting-count", type=int, required=True)
    parser.add_argument("--attention-candidates", type=Path)
    parser.add_argument("--claims", type=Path, required=True)
    parser.add_argument("--findings", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-claim-paths", type=int, default=3)
    parser.add_argument("--max-findings", type=int, default=4)
    args = parser.parse_args()
    summary = build_cards(
        starting_ranking=args.starting_ranking,
        starting_count=args.starting_count,
        attention_candidates=args.attention_candidates,
        claims_path=args.claims,
        findings_path=args.findings,
        out_path=args.out,
        max_claim_paths=args.max_claim_paths,
        max_findings=args.max_findings,
    )
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
