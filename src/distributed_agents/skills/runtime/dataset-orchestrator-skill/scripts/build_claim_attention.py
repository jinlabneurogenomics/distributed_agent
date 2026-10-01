#!/usr/bin/env python3
"""Find a small Claim-related neighborhood around an ordered starting result.

This helper deliberately ignores Program/Complex memberships and
SHARES_GRAPH_CONCEPT edges. Private rank bands focus the search, while a
separate, self-describing summary tells downstream readers which additional
gene perturbations are related to which genes in the starting result. It does
not expose ranks, scores, or attention weights.
"""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path

EXPLICIT_LINK_FIELDS = (
    "supporting_targets",
    "implication_targets",
    "boundary_targets",
    "comparators",
)
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
CONFIDENCE_POINTS = {"high": 3, "moderate": 2, "low": 1}
HARD_TYPED_RELATIONS = frozenset({"QUALIFIES", "CONTRASTS_WITH", "IMPLICATION_OF"})
PRIVATE_OUTPUT_FIELDS = (
    "candidate",
    "selected",
    "selection_channel",
    "attention_anchor_count",
    "admission_basis",
    "anchor",
    "private_anchor_rank",
    "private_seed_tier",
    "attention_role",
    "attention_claim_id",
    "linked_claim_id",
    "candidate_claim_ids",
    "relation_type",
    "relation_family",
    "direction_pattern",
    "support_level",
    "de_support_level",
    "confidence",
    "relation_confidence",
    "link_reliability_tier",
    "relation_fanout",
    "private_path_attention",
    "semantic_relation_class",
    "reason",
)
SUMMARY_OUTPUT_FIELDS = (
    "gene_target",
    "linked_starting_gene_count",
    "selection_reason",
    "linked_starting_genes",
    "relation_roles",
    "claim_ids",
    "linked_claim_ids",
    "gene_claim_ids",
    "relation_types",
    "relation_families",
    "direction_patterns",
    "semantic_relation_classes",
    "relation_summaries",
)


def _delimiter(path: Path) -> str:
    return "\t" if path.suffix.casefold() == ".tsv" else ","


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter=_delimiter(path)))


def _split_genes(value: str) -> list[str]:
    return [item.strip() for item in value.split("|") if item.strip()]


def _truthy(value: str) -> bool:
    return value.strip().casefold() in {"1", "true", "yes", "y"}


def _number(value: str, *, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _write_rows(
    path: Path,
    rows: list[dict[str, str]],
    *,
    fieldnames: tuple[str, ...],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def _seed_tier(rank: int, anchor_count: int) -> tuple[str, int]:
    primary_end = max(1, math.ceil(anchor_count * 0.2))
    secondary_end = max(primary_end, math.ceil(anchor_count * 0.5))
    if rank <= primary_end:
        return "primary", 3
    if rank <= secondary_end:
        return "secondary", 2
    return "coverage", 1


def _link_reliability(row: dict[str, str]) -> int:
    role = row["attention_role"]
    relation_type = row["relation_type"]
    if relation_type in HARD_TYPED_RELATIONS:
        return 3
    if role in {"claim_supporting", "claim_implication", "claim_boundary"}:
        return 3
    if relation_type == "REVIEW_WITH":
        return 2
    if (
        role == "claim_co_target"
        and row["relation_family"].casefold() in RELATIONAL_FAMILIES
    ):
        return 2
    return 1


def _semantic_relation_class(row: dict[str, str]) -> str:
    relation_type = row["relation_type"]
    if relation_type == "QUALIFIES" or row["attention_role"] == "claim_boundary":
        return "qualification"
    if relation_type == "CONTRASTS_WITH":
        return "contrast"
    if relation_type == "IMPLICATION_OF" or row["attention_role"] in {
        "claim_supporting",
        "claim_implication",
    }:
        return "implication"
    if relation_type == "REVIEW_WITH":
        return "review"
    if row["attention_role"] == "claim_comparators":
        return "comparator"
    return "co_narrative"


def _confidence_points(row: dict[str, str]) -> int:
    claim_points = CONFIDENCE_POINTS.get(row["confidence"].casefold(), 1)
    relation = row["relation_confidence"].casefold()
    if not relation:
        return claim_points
    return min(claim_points, CONFIDENCE_POINTS.get(relation, 1))


def _independent_paths(
    rows: list[dict[str, str]],
    *,
    limit: int,
) -> list[dict[str, str]]:
    selected: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    for row in sorted(
        rows,
        key=lambda item: (
            -float(item["private_path_attention"]),
            item["anchor"].casefold(),
            item["attention_claim_id"],
            item["relation_type"],
        ),
    ):
        key = (
            row["anchor"].casefold(),
            row["attention_claim_id"],
            row["relation_family"].casefold(),
        )
        if key in seen:
            continue
        seen.add(key)
        selected.append(row)
        if len(selected) == limit:
            break
    return selected


def build_attention(
    *,
    candidate_prior: Path,
    claims_path: Path,
    edges_path: Path,
    out_path: Path,
    candidate_out_path: Path | None = None,
    anchor_count: int = 100,
    max_related_candidates: int | None = None,
    precision_fraction: float = 0.8,
    max_paths_per_candidate: int = 3,
    min_comparator_anchors: int = 2,
    candidate_column: str = "gene_target",
    rank_column: str = "rank",
    score_column: str = "endpoint_prior_score",
) -> dict[str, int]:
    """Write a private path audit and a compact related-gene summary."""
    prior_rows = _read_rows(candidate_prior)
    if not prior_rows or candidate_column not in prior_rows[0]:
        raise ValueError(f"candidate prior lacks {candidate_column!r}")
    if anchor_count < 1:
        raise ValueError("anchor_count must be positive")
    if max_related_candidates is None:
        max_related_candidates = min(50, math.ceil(anchor_count / 2))
    if max_related_candidates < 1:
        raise ValueError("max_related_candidates must be positive")
    if max_related_candidates > min(50, math.ceil(anchor_count / 2)):
        raise ValueError(
            "max_related_candidates exceeds min(50, ceil(anchor_count / 2))"
        )
    if not 0 <= precision_fraction <= 1:
        raise ValueError("precision_fraction must be between 0 and 1")
    if max_paths_per_candidate < 1:
        raise ValueError("max_paths_per_candidate must be positive")
    if min_comparator_anchors < 1:
        raise ValueError("min_comparator_anchors must be positive")

    biological = [
        row
        for row in prior_rows
        if row.get(candidate_column, "").strip()
        and not _truthy(row.get("is_control", ""))
    ]
    if any(row.get(rank_column, "").strip() for row in biological):
        biological.sort(
            key=lambda row: _number(row.get(rank_column, ""), default=float("inf"))
        )
    elif any(row.get(score_column, "").strip() for row in biological):
        biological.sort(
            key=lambda row: _number(row.get(score_column, ""), default=float("-inf")),
            reverse=True,
        )
    else:
        raise ValueError(f"candidate prior needs {rank_column!r} or {score_column!r}")

    canonical_by_fold: dict[str, str] = {}
    prior_by_gene: dict[str, dict[str, str]] = {}
    for row in biological:
        gene = row[candidate_column].strip()
        folded = gene.casefold()
        if folded in canonical_by_fold:
            continue
        canonical_by_fold[folded] = gene
        prior_by_gene[gene] = row

    anchor_order = list(prior_by_gene)[:anchor_count]
    anchors = set(anchor_order)
    anchor_rank = {gene: index for index, gene in enumerate(anchor_order, start=1)}
    claims = _read_rows(claims_path)
    claims_by_id = {
        row.get("doc_id", "").strip(): row
        for row in claims
        if row.get("doc_id", "").strip()
    }
    targets_by_claim: dict[str, set[str]] = {}
    claim_ids_by_candidate: dict[str, set[str]] = defaultdict(set)
    for claim_id, row in claims_by_id.items():
        targets: set[str] = set()
        for value in _split_genes(row.get("targets", "")):
            canonical = canonical_by_fold.get(value.casefold())
            if canonical:
                targets.add(canonical)
                claim_ids_by_candidate[canonical].add(claim_id)
        targets_by_claim[claim_id] = targets

    paths: dict[tuple[str, ...], dict[str, str]] = {}

    def add_path(
        *,
        candidate: str,
        anchor: str,
        role: str,
        attention_claim_id: str,
        linked_claim_id: str = "",
        relation_type: str = "",
        relation_confidence: str = "",
        reason: str = "",
    ) -> None:
        if candidate == anchor or candidate in anchors or anchor not in anchors:
            return
        claim = claims_by_id.get(attention_claim_id, {})
        row = {
            "candidate": candidate,
            "selected": "false",
            "selection_channel": "",
            "attention_anchor_count": "",
            "admission_basis": "",
            "anchor": anchor,
            "private_anchor_rank": str(anchor_rank[anchor]),
            "private_seed_tier": _seed_tier(anchor_rank[anchor], len(anchor_order))[0],
            "attention_role": role,
            "attention_claim_id": attention_claim_id,
            "linked_claim_id": linked_claim_id,
            "candidate_claim_ids": "|".join(
                sorted(claim_ids_by_candidate.get(candidate, set()))
            ),
            "relation_type": relation_type,
            "relation_family": claim.get("relation_family", ""),
            "direction_pattern": claim.get("direction_pattern", ""),
            "support_level": claim.get("support_level", ""),
            "de_support_level": claim.get("de_support_level", ""),
            "confidence": claim.get("confidence", ""),
            "relation_confidence": relation_confidence,
            "link_reliability_tier": "",
            "relation_fanout": "",
            "private_path_attention": "",
            "semantic_relation_class": "",
            "reason": reason,
        }
        key = (
            candidate,
            anchor,
            role,
            attention_claim_id,
            linked_claim_id,
            relation_type,
        )
        paths[key] = row

    for claim_id, claim in claims_by_id.items():
        targets = targets_by_claim[claim_id]
        anchor_targets = targets & anchors
        non_anchor_targets = targets - anchors
        for anchor in anchor_targets:
            for candidate in non_anchor_targets:
                add_path(
                    candidate=candidate,
                    anchor=anchor,
                    role="claim_co_target",
                    attention_claim_id=claim_id,
                    reason="candidate and endpoint anchor are explicit Claim targets",
                )
        for field in EXPLICIT_LINK_FIELDS:
            linked = {
                canonical_by_fold[value.casefold()]
                for value in _split_genes(claim.get(field, ""))
                if value.casefold() in canonical_by_fold
            }
            for candidate in non_anchor_targets:
                for anchor in linked & anchors:
                    add_path(
                        candidate=candidate,
                        anchor=anchor,
                        role=f"claim_{field.removesuffix('_targets')}",
                        attention_claim_id=claim_id,
                        reason=f"candidate Claim explicitly names anchor in {field}",
                    )
            for anchor in anchor_targets:
                for candidate in linked - anchors:
                    add_path(
                        candidate=candidate,
                        anchor=anchor,
                        role=f"claim_{field.removesuffix('_targets')}",
                        attention_claim_id=claim_id,
                        reason=f"anchor Claim explicitly names candidate in {field}",
                    )

    for edge in _read_rows(edges_path):
        relation_type = edge.get("edge_type", "").strip()
        if not relation_type or relation_type == "SHARES_GRAPH_CONCEPT":
            continue
        source_id = edge.get("source_claim_id", "").strip()
        target_id = edge.get("target_claim_id", "").strip()
        source_targets = targets_by_claim.get(source_id, set())
        target_targets = targets_by_claim.get(target_id, set())
        for anchor in source_targets & anchors:
            for candidate in target_targets - anchors:
                add_path(
                    candidate=candidate,
                    anchor=anchor,
                    role="typed_claim_relation",
                    attention_claim_id=target_id,
                    linked_claim_id=source_id,
                    relation_type=relation_type,
                    relation_confidence=edge.get("confidence", "").strip(),
                    reason=edge.get("reason", "").strip(),
                )
        for anchor in target_targets & anchors:
            for candidate in source_targets - anchors:
                add_path(
                    candidate=candidate,
                    anchor=anchor,
                    role="typed_claim_relation",
                    attention_claim_id=source_id,
                    linked_claim_id=target_id,
                    relation_type=relation_type,
                    relation_confidence=edge.get("confidence", "").strip(),
                    reason=edge.get("reason", "").strip(),
                )

    fanout_candidates: dict[tuple[str, str, str, str], set[str]] = defaultdict(set)
    for row in paths.values():
        fanout_key = (
            row["attention_claim_id"],
            row["linked_claim_id"],
            row["attention_role"],
            row["relation_type"],
        )
        fanout_candidates[fanout_key].add(row["candidate"])
    for row in paths.values():
        fanout_key = (
            row["attention_claim_id"],
            row["linked_claim_id"],
            row["attention_role"],
            row["relation_type"],
        )
        fanout = len(fanout_candidates[fanout_key])
        seed_points = _seed_tier(int(row["private_anchor_rank"]), len(anchor_order))[1]
        link_points = _link_reliability(row)
        confidence_points = _confidence_points(row)
        row["link_reliability_tier"] = str(link_points)
        row["relation_fanout"] = str(fanout)
        row["private_path_attention"] = (
            f"{seed_points * link_points * confidence_points / math.log2(2 + fanout):.8f}"
        )
        row["semantic_relation_class"] = _semantic_relation_class(row)

    paths_by_candidate: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in paths.values():
        paths_by_candidate[row["candidate"]].append(row)
    strong_roles = {
        "typed_claim_relation",
        "claim_co_target",
        "claim_supporting",
        "claim_implication",
        "claim_boundary",
    }
    admitted: set[str] = set()
    for candidate, candidate_paths in paths_by_candidate.items():
        distinct_anchors = {row["anchor"] for row in candidate_paths}
        has_strong_path = any(
            row["attention_role"] in strong_roles for row in candidate_paths
        )
        if has_strong_path or len(distinct_anchors) >= min_comparator_anchors:
            admitted.add(candidate)
            basis = (
                "typed_or_directional_claim"
                if has_strong_path
                else "multiple_endpoint_anchors"
            )
            for row in candidate_paths:
                row["attention_anchor_count"] = str(len(distinct_anchors))
                row["admission_basis"] = basis

    independent_by_candidate = {
        candidate: _independent_paths(
            paths_by_candidate[candidate],
            limit=max_paths_per_candidate,
        )
        for candidate in admitted
    }

    def attention_priority(candidate: str) -> tuple[object, ...]:
        independent = independent_by_candidate[candidate]
        attention_score = sum(
            float(row["private_path_attention"]) for row in independent
        )
        return (
            -attention_score,
            -len({row["anchor"] for row in independent}),
            -max(int(row["link_reliability_tier"]) for row in independent),
            min(int(row["relation_fanout"]) for row in independent),
            candidate.casefold(),
        )

    admitted_before_limit = len(admitted)
    ordered_admitted = sorted(admitted, key=attention_priority)
    precision_count = min(
        len(ordered_admitted),
        math.floor(max_related_candidates * precision_fraction),
    )
    if precision_fraction > 0 and precision_count == 0:
        precision_count = 1
    precision_selected = ordered_admitted[:precision_count]
    selected_order = list(precision_selected)
    selected_set = set(selected_order)

    buckets: dict[tuple[int, str], list[str]] = defaultdict(list)
    for candidate in ordered_admitted:
        if candidate in selected_set:
            continue
        best = independent_by_candidate[candidate][0]
        seed_points = _seed_tier(int(best["private_anchor_rank"]), len(anchor_order))[1]
        family = best["relation_family"].casefold() or best["semantic_relation_class"]
        buckets[(seed_points, family)].append(candidate)
    bucket_keys = sorted(buckets, key=lambda item: (item[0], item[1]))
    while bucket_keys and len(selected_order) < max_related_candidates:
        next_keys: list[tuple[int, str]] = []
        for key in bucket_keys:
            if len(selected_order) >= max_related_candidates:
                break
            bucket = buckets[key]
            while bucket and bucket[0] in selected_set:
                bucket.pop(0)
            if bucket:
                candidate = bucket.pop(0)
                selected_order.append(candidate)
                selected_set.add(candidate)
            if bucket:
                next_keys.append(key)
        bucket_keys = next_keys
    if len(selected_order) < max_related_candidates:
        for candidate in ordered_admitted:
            if candidate not in selected_set:
                selected_order.append(candidate)
                selected_set.add(candidate)
            if len(selected_order) == max_related_candidates:
                break

    precision_set = set(precision_selected)
    for candidate in admitted:
        channel = (
            "precision"
            if candidate in precision_set
            else ("diversity" if candidate in selected_set else "")
        )
        for row in paths_by_candidate[candidate]:
            row["selected"] = str(candidate in selected_set).lower()
            row["selection_channel"] = channel

    output_rows = sorted(
        (row for candidate in admitted for row in paths_by_candidate[candidate]),
        key=lambda row: (
            row["candidate"].casefold(),
            row["anchor"].casefold(),
            row["attention_role"],
            row["attention_claim_id"],
        ),
    )
    _write_rows(out_path, output_rows, fieldnames=PRIVATE_OUTPUT_FIELDS)

    summary_rows: list[dict[str, str]] = []
    for candidate in sorted(selected_set, key=str.casefold):
        top_paths = independent_by_candidate[candidate]
        all_candidate_claim_ids = sorted(
            {
                claim_id
                for row in top_paths
                for claim_id in _split_genes(row["candidate_claim_ids"])
            }
        )
        summary_rows.append(
            {
                "gene_target": candidate,
                "linked_starting_gene_count": str(
                    len({row["anchor"] for row in paths_by_candidate[candidate]})
                ),
                "selection_reason": top_paths[0]["admission_basis"],
                "linked_starting_genes": "|".join(
                    row["anchor"] for row in top_paths
                ),
                "relation_roles": "|".join(
                    row["attention_role"] for row in top_paths
                ),
                "claim_ids": "|".join(
                    row["attention_claim_id"] for row in top_paths
                ),
                "linked_claim_ids": "|".join(
                    row["linked_claim_id"] or "-" for row in top_paths
                ),
                "gene_claim_ids": "|".join(all_candidate_claim_ids),
                "relation_types": "|".join(
                    row["relation_type"] or "-" for row in top_paths
                ),
                "relation_families": "|".join(
                    row["relation_family"] or "-" for row in top_paths
                ),
                "direction_patterns": "|".join(
                    row["direction_pattern"] or "-" for row in top_paths
                ),
                "semantic_relation_classes": "|".join(
                    row["semantic_relation_class"] for row in top_paths
                ),
                "relation_summaries": " || ".join(
                    row["reason"] for row in top_paths
                ),
            }
        )
    if candidate_out_path is not None:
        _write_rows(
            candidate_out_path,
            summary_rows,
            fieldnames=SUMMARY_OUTPUT_FIELDS,
        )
    return {
        "candidate_universe": len(prior_by_gene),
        "anchors": len(anchors),
        "raw_attention_candidates": len(paths_by_candidate),
        "raw_attention_paths": len(paths),
        "eligible_attention_candidates": admitted_before_limit,
        "attention_candidates": len(selected_set),
        "attention_paths": sum(row["selected"] == "true" for row in output_rows),
        "audit_paths": len(output_rows),
        "precision_candidates": len(precision_set),
        "diversity_candidates": len(selected_set - precision_set),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-prior", type=Path, required=True)
    parser.add_argument("--claims", type=Path, required=True)
    parser.add_argument("--edges", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument(
        "--out-candidates",
        type=Path,
        required=True,
        help="compact one-row-per-related-gene summary for the final reviewer",
    )
    parser.add_argument("--anchor-count", type=int, default=100)
    parser.add_argument(
        "--max-related-candidates",
        type=int,
        help="maximum additional Claim-related genes",
    )
    parser.add_argument("--precision-fraction", type=float, default=0.8)
    parser.add_argument("--max-paths-per-candidate", type=int, default=3)
    parser.add_argument("--min-comparator-anchors", type=int, default=2)
    parser.add_argument("--candidate-column", default="gene_target")
    parser.add_argument("--rank-column", default="rank")
    parser.add_argument("--score-column", default="endpoint_prior_score")
    args = parser.parse_args()
    summary = build_attention(
        candidate_prior=args.candidate_prior,
        claims_path=args.claims,
        edges_path=args.edges,
        out_path=args.out,
        candidate_out_path=args.out_candidates,
        anchor_count=args.anchor_count,
        max_related_candidates=args.max_related_candidates,
        precision_fraction=args.precision_fraction,
        max_paths_per_candidate=args.max_paths_per_candidate,
        min_comparator_anchors=args.min_comparator_anchors,
        candidate_column=args.candidate_column,
        rank_column=args.rank_column,
        score_column=args.score_column,
    )
    print(
        "Claim attention: "
        f"{summary['attention_candidates']} candidates across "
        f"{summary['attention_paths']} selected paths "
        f"({summary['audit_paths']} eligible paths audited) from "
        f"{summary['raw_attention_candidates']} raw candidates and "
        f"{summary['anchors']} genes in the starting result "
        f"({summary['eligible_attention_candidates']} passed relation gating)"
    )


if __name__ == "__main__":
    main()
