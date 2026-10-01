#!/usr/bin/env python3
"""Screen and route canonical BioKG Claims for one task profile.

Every Claim receives exactly one disposition.  The frozen Claim assignments and
typed relations are mandatory; live Neo4j enrichment is optional unless
``--graph-mode required`` is requested.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from types import ModuleType
from typing import Iterable


SCHEMA_VERSION = "distributed_agents-claim-recall-v1"
CONFIDENCE_ORDER = {"low": 0, "moderate": 1, "high": 2}
SUPPORT_ORDER = {
    "narrative_only": 0,
    "null": 1,
    "nominal": 2,
    "mixed": 3,
    "fdr_supported": 4,
}
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
EDGE_FIELDS = (
    "source_claim_id",
    "target_claim_id",
    "edge_type",
    "confidence",
    "reason",
    "source_layer",
    "weight",
)
MEMBERSHIP_FIELDS = (
    "claim_id",
    "source_doc_id",
    "concept_kind",
    "concept_id",
    "concept_name",
    "ontology_kind",
    "effect_status",
    "source_layer",
)
POSITIVE_PROGRAM_EFFECTS = frozenset({"affected", "implicated", "buffered"})
BOUNDARY_FAMILIES = frozenset({"buffering", "negative_result", "therapeutic"})
STOPWORDS = frozenset(
    {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "by",
        "cell",
        "data",
        "dataset",
        "effect",
        "for",
        "from",
        "gene",
        "in",
        "is",
        "it",
        "of",
        "on",
        "or",
        "perturbation",
        "rank",
        "the",
        "to",
        "with",
    }
)


def _selected_biokg_module(suffix: str) -> ModuleType:
    """Import one BioKG module from the selected release projection.

    Release projections intentionally use the top-level ``biokg`` module name
    inside their self-contained capsule. Resolve that name only after the
    registry selects a release; never fall back to a package-level legacy copy.
    """

    module_name = f"biokg.{suffix}"
    from distributed_agents.corpus.registry import CorpusRegistryError, get_release

    try:
        release = get_release()
        projection_root = release.projection("biokg").resolve()
    except CorpusRegistryError as exc:
        raise RuntimeError(f"cannot resolve the selected release BioKG: {exc}") from exc

    loaded = sys.modules.get(module_name)
    if isinstance(loaded, ModuleType):
        loaded_file = getattr(loaded, "__file__", None)
        if loaded_file is None:  # Explicit test doubles have no filesystem owner.
            return loaded
        loaded_path = Path(loaded_file).resolve()
        if loaded_path.is_relative_to(projection_root):
            return loaded
        raise RuntimeError(
            f"{module_name} is already loaded outside selected release "
            f"{release.release_id!r}: {loaded_path}"
        )

    projections_root = projection_root.parent
    marker = str(projections_root)
    if marker not in sys.path:
        sys.path.insert(0, marker)
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            f"release {release.release_id!r} does not provide {module_name}"
        ) from exc

    module_path = Path(getattr(module, "__file__", "")).resolve()
    if not module_path.is_relative_to(projection_root):
        raise RuntimeError(
            f"resolved {module_name} outside selected release {release.release_id!r}: "
            f"{module_path}"
        )
    return module


def _selected_claim_layer() -> ModuleType:
    module = _selected_biokg_module("build.claim_layer")
    required = (
        "DEFAULT_ASSIGNMENTS",
        "DEFAULT_LEDGER",
        "DEFAULT_RELATIONS",
        "claim_cards",
        "read_ledger",
        "read_tsv",
        "validate_assignments",
        "validate_relations",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        raise RuntimeError(
            "selected release Claim layer lacks required operations: "
            + ", ".join(missing)
        )
    return module


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _tokens(values: Iterable[object]) -> set[str]:
    result: set[str] = set()
    for value in values:
        for token in re.findall(r"[A-Za-z0-9]+", str(value).casefold()):
            if len(token) >= 3 and token not in STOPWORDS:
                result.add(token)
    return result


def _is_control(card: dict[str, object]) -> bool:
    targets = [str(value).casefold() for value in card.get("targets", [])]
    return bool(targets) and all(
        target == "non_target" or target.startswith("safe_target") for target in targets
    )


def _card_terms(card: dict[str, object]) -> set[str]:
    return _tokens(
        [
            card.get("canonical_summary", ""),
            card.get("direction_pattern", ""),
            card.get("relation_family", ""),
            card.get("evidence_mode", ""),
            *card.get("targets", []),
            *card.get("readouts", []),
            *card.get("finding_types", []),
            *card.get("cell_scope", []),
        ]
    )


def _routing_scores(
    cards: list[dict[str, object]], profile: dict[str, object]
) -> dict[str, float]:
    query_tokens = _tokens(profile.get("query_terms", []))
    explicit_targets = {
        str(value).casefold() for value in profile.get("explicit_targets", [])
    }
    terms_by_claim = {str(card["claim_id"]): _card_terms(card) for card in cards}
    document_frequency = Counter(
        token
        for tokens in terms_by_claim.values()
        for token in tokens
        if token in query_tokens
    )
    n_docs = max(len(cards), 1)
    scores: dict[str, float] = {}
    for card in cards:
        claim_id = str(card["claim_id"])
        overlap = terms_by_claim[claim_id] & query_tokens
        lexical = sum(
            math.log((n_docs + 1) / (document_frequency[token] + 1)) + 1
            for token in overlap
        )
        target_match = bool(
            explicit_targets
            & {str(value).casefold() for value in card.get("targets", [])}
        )
        score = lexical + (12.0 if target_match else 0.0)
        if card.get("active_default"):
            score += 0.25
        if card.get("de_support_level") == "fdr_supported":
            score += 0.5
        elif card.get("de_support_level") == "nominal":
            score += 0.2
        scores[claim_id] = round(score, 8)
    return scores


def _offline_relations(
    path: Path,
    claim_ids: set[str],
    *,
    claim_layer: ModuleType,
) -> list[dict[str, str]]:
    relations = claim_layer.read_tsv(path)
    claim_layer.validate_relations(relations, claim_ids)
    return relations


def _relation_adjacency(
    relations: list[dict[str, str]],
) -> dict[str, list[dict[str, str]]]:
    adjacency: dict[str, list[dict[str, str]]] = defaultdict(list)
    for relation in relations:
        adjacency[relation["source_claim_id"]].append(relation)
        adjacency[relation["target_claim_id"]].append(relation)
    return adjacency


def _boundary_supported(card: dict[str, object]) -> bool:
    de_level = str(card.get("de_support_level") or "")
    support = SUPPORT_ORDER.get(str(card.get("support_level") or ""), -1)
    confidence = CONFIDENCE_ORDER.get(str(card.get("confidence") or ""), -1)
    return de_level in {"nominal", "fdr_supported"} or (
        confidence >= CONFIDENCE_ORDER["moderate"]
        and support >= SUPPORT_ORDER["nominal"]
    )


def _screen(
    cards: list[dict[str, object]],
    profile: dict[str, object],
    scores: dict[str, float],
    relations: list[dict[str, str]],
) -> tuple[set[str], dict[str, list[str]]]:
    strategy = str(profile.get("claim_strategy") or "requires_semantic_review")
    if strategy in {"none", "requires_semantic_review"}:
        raise ValueError(
            "Claim routing requires a resolved claim_strategy; validate the v4 "
            "task profile before routing"
        )
    explicit_targets = {
        str(value).casefold() for value in profile.get("explicit_targets", [])
    }
    by_id = {str(card["claim_id"]): card for card in cards}
    active = {
        claim_id for claim_id, card in by_id.items() if card.get("active_default")
    }
    adjacency = _relation_adjacency(relations)
    selected: set[str] = set()
    reasons: dict[str, list[str]] = defaultdict(list)

    for claim_id, card in by_id.items():
        if _is_control(card):
            reasons[claim_id].append(
                "control target excluded from scientific candidates"
            )
            continue
        target_match = bool(
            explicit_targets
            & {str(value).casefold() for value in card.get("targets", [])}
        )
        lexical_match = scores[claim_id] > 0.75
        family = str(card.get("relation_family") or "")
        has_active_neighbor = any(
            (
                relation["target_claim_id"]
                if relation["source_claim_id"] == claim_id
                else relation["source_claim_id"]
            )
            in active
            for relation in adjacency.get(claim_id, [])
        )

        if strategy == "all_relational":
            if card.get("active_default") and family in RELATIONAL_FAMILIES:
                selected.add(claim_id)
                reasons[claim_id].append("active relational Claim")
        elif strategy == "all_active":
            if card.get("active_default"):
                selected.add(claim_id)
                reasons[claim_id].append("active substantive Claim")
            elif target_match:
                selected.add(claim_id)
                reasons[claim_id].append(
                    "inactive boundary Claim directly matches a named target"
                )
            elif _boundary_supported(card):
                selected.add(claim_id)
                reasons[claim_id].append(
                    "inactive boundary Claim has evidence/confidence support"
                )
            elif has_active_neighbor:
                selected.add(claim_id)
                reasons[claim_id].append(
                    "inactive boundary Claim qualifies an active Claim"
                )
        elif strategy == "semantic_screen":
            if lexical_match or family in BOUNDARY_FAMILIES:
                selected.add(claim_id)
                reasons[claim_id].append(
                    "task-relevant semantic Claim, including boundary/warning evidence"
                )
        elif strategy == "all_claims":
            selected.add(claim_id)
            reasons[claim_id].append("complete Claim context requested by the profile")
        else:
            if target_match or lexical_match:
                selected.add(claim_id)
                reasons[claim_id].append("direct target or semantic task match")

    if strategy == "targeted":
        seeds = set(selected)
        for relation in relations:
            left = relation["source_claim_id"]
            right = relation["target_claim_id"]
            if (
                left in seeds
                and right not in selected
                and not _is_control(by_id[right])
            ):
                selected.add(right)
                reasons[right].append(
                    f"one-hop {relation['relation_type']} neighbor of {left}"
                )
            elif (
                right in seeds and left not in selected and not _is_control(by_id[left])
            ):
                selected.add(left)
                reasons[left].append(
                    f"one-hop {relation['relation_type']} neighbor of {right}"
                )

    for claim_id, card in by_id.items():
        if claim_id in selected or reasons[claim_id]:
            continue
        if (
            not card.get("active_default")
            and str(card.get("relation_family")) in BOUNDARY_FAMILIES
        ):
            reasons[claim_id].append(
                "standalone inactive boundary Claim did not clear task-aware screen"
            )
        else:
            reasons[claim_id].append("Claim did not match this task's evidence needs")
    return selected, reasons


def _finding_to_claim(assignments: list[dict[str, str]]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for row in assignments:
        doc_id = str(row.get("doc_id") or "").strip()
        claim_id = str(row.get("claim_id") or "").strip()
        if not doc_id or not claim_id:
            continue
        previous = mapping.setdefault(doc_id, claim_id)
        if previous != claim_id:
            raise ValueError(
                f"Finding {doc_id} maps to multiple Claims: {previous}, {claim_id}"
            )
    return mapping


def _live_memberships(
    graph_mode: str,
    finding_to_claim: dict[str, str],
) -> tuple[list[dict[str, str]], dict[str, object]]:
    if graph_mode == "offline":
        return [], {
            "mode": graph_mode,
            "status": "offline_only",
            "fallback_reason": "disabled",
            "membership_count": 0,
            "source_edge_count": 0,
            "claim_count": 0,
            "program_membership_count": 0,
            "complex_membership_count": 0,
            "program_claim_count": 0,
            "complex_claim_count": 0,
        }
    try:
        biokg_cypher = _selected_biokg_module("tooling.biokg_cypher")
        rows_from_result = biokg_cypher._rows
        run_cypher = biokg_cypher.run_cypher

        conn = {
            "http_url": os.environ.get("BIOKG_NEO4J_HTTP_URL", "http://127.0.0.1:7474"),
            "database": os.environ.get("BIOKG_NEO4J_DATABASE", "neo4j"),
            "user": os.environ.get("BIOKG_NEO4J_USER", "neo4j"),
            "password": os.environ.get("BIOKG_NEO4J_PASSWORD", "biokgpassword"),
            "timeout": 8.0,
        }
        query = """
        MATCH (f:Finding)-[r:IMPLICATES_PROGRAM]->(p:Program)
        WHERE r.effect_status IN $positive_program_effects
        RETURN f.doc_id AS doc_id, 'Program' AS concept_kind,
               coalesce(p.program_id, p.name, p.id) AS concept_id,
               coalesce(p.name, p.program_id, p.id) AS concept_name,
               coalesce(p.kind, 'program') AS ontology_kind,
               coalesce(r.effect_status, '') AS effect_status,
               'live_finding_program' AS source_layer
        UNION
        MATCH (f:Finding)-[r:IMPLICATES]->(x:Complex)
        RETURN f.doc_id AS doc_id, 'Complex' AS concept_kind,
               coalesce(x.id, x.name) AS concept_id,
               coalesce(x.name, x.id) AS concept_name,
               'complex' AS ontology_kind,
               coalesce(r.effect_status, '') AS effect_status,
               'live_finding_complex' AS source_layer
        """
        columns, data = rows_from_result(
            run_cypher(
                query,
                parameters={
                    "positive_program_effects": sorted(POSITIVE_PROGRAM_EFFECTS)
                },
                **conn,
            )
        )
        memberships: list[dict[str, str]] = []
        seen: set[tuple[str, ...]] = set()
        source_edges = 0
        for row in data:
            record = dict(zip(columns, row))
            source_doc_id = str(record.get("doc_id") or "").strip()
            claim_id = finding_to_claim.get(source_doc_id, "")
            concept_kind = str(record.get("concept_kind") or "").strip()
            concept_id = str(record.get("concept_id") or "").strip()
            if not claim_id or not concept_kind or not concept_id:
                continue
            source_edges += 1
            membership = {
                "claim_id": claim_id,
                "source_doc_id": source_doc_id,
                "concept_kind": concept_kind,
                "concept_id": concept_id,
                "concept_name": str(record.get("concept_name") or concept_id).strip(),
                "ontology_kind": str(
                    record.get("ontology_kind") or concept_kind.casefold()
                ).strip(),
                "effect_status": str(record.get("effect_status") or "").strip(),
                "source_layer": str(record.get("source_layer") or "").strip(),
            }
            key = tuple(membership[field] for field in MEMBERSHIP_FIELDS)
            if key not in seen:
                seen.add(key)
                memberships.append(membership)
        memberships.sort(
            key=lambda row: (
                row["claim_id"].casefold(),
                row["concept_kind"].casefold(),
                row["concept_id"].casefold(),
                row["source_doc_id"].casefold(),
            )
        )
        return memberships, {
            "mode": graph_mode,
            "status": "enriched" if memberships else "connected_no_memberships",
            "fallback_reason": "",
            "membership_source": "live_finding_to_frozen_claim_join",
            "membership_count": len(memberships),
            "source_edge_count": source_edges,
            "claim_count": len({row["claim_id"] for row in memberships}),
            "program_membership_count": sum(
                row["concept_kind"] == "Program" for row in memberships
            ),
            "complex_membership_count": sum(
                row["concept_kind"] == "Complex" for row in memberships
            ),
            "program_claim_count": len(
                {
                    row["claim_id"]
                    for row in memberships
                    if row["concept_kind"] == "Program"
                }
            ),
            "complex_claim_count": len(
                {
                    row["claim_id"]
                    for row in memberships
                    if row["concept_kind"] == "Complex"
                }
            ),
        }
    except (
        BaseException
    ) as exc:  # Neo4j helper reports connection failures as SystemExit
        if graph_mode == "required":
            raise RuntimeError(
                f"live graph enrichment required but unavailable: {exc}"
            ) from exc
        return [], {
            "mode": graph_mode,
            "status": "offline_fallback",
            "fallback_reason": f"{type(exc).__name__}: {exc}",
            "membership_count": 0,
            "source_edge_count": 0,
            "claim_count": 0,
            "program_membership_count": 0,
            "complex_membership_count": 0,
            "program_claim_count": 0,
            "complex_claim_count": 0,
        }


def _routing_edges(
    selected: set[str],
    relations: list[dict[str, str]],
    memberships: list[dict[str, str]],
    *,
    hubcap: int,
) -> list[dict[str, object]]:
    edges: list[dict[str, object]] = []
    for relation in relations:
        left = relation["source_claim_id"]
        right = relation["target_claim_id"]
        if left in selected and right in selected:
            edges.append(
                {
                    "source_claim_id": left,
                    "target_claim_id": right,
                    "edge_type": relation["relation_type"],
                    "confidence": relation["confidence"],
                    "reason": relation["reason"],
                    "source_layer": "frozen_claim_relation",
                    "weight": 2.0 if relation["confidence"] == "high" else 1.0,
                }
            )
    by_concept: dict[str, list[str]] = defaultdict(list)
    for membership in memberships:
        claim_id = membership["claim_id"]
        if claim_id in selected:
            concept = f"{membership['concept_kind']}:{membership['concept_id']}"
            by_concept[concept].append(claim_id)
    for concept, claims in sorted(by_concept.items()):
        claims = sorted(set(claims), key=str.casefold)
        if len(claims) < 2 or len(claims) > hubcap:
            continue
        weight = round(1.0 / math.log2(len(claims) + 1), 8)
        for index, left in enumerate(claims):
            for right in claims[index + 1 :]:
                edges.append(
                    {
                        "source_claim_id": left,
                        "target_claim_id": right,
                        "edge_type": "SHARES_GRAPH_CONCEPT",
                        "confidence": "routing_only",
                        "reason": concept,
                        "source_layer": "live_program_complex",
                        "weight": weight,
                    }
                )
    return edges


def _write_pool(
    path: Path,
    cards: list[dict[str, object]],
    selected: set[str],
    scores: dict[str, float],
    reasons: dict[str, list[str]],
) -> None:
    by_id = {str(card["claim_id"]): card for card in cards}
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=(
                "doc_id",
                "unit_kind",
                "lane_score",
                "canonical_summary",
                "targets",
                "primary_anchors",
                "supporting_targets",
                "implication_targets",
                "boundary_targets",
                "comparators",
                "readouts",
                "relation_family",
                "direction_pattern",
                "evidence_mode",
                "active_default",
                "support_level",
                "de_support_level",
                "confidence",
                "member_count",
                "member_doc_ids",
                "member_roles",
                "selection_reason",
            ),
        )
        writer.writeheader()
        for claim_id in sorted(
            selected, key=lambda value: (-scores[value], value.casefold())
        ):
            card = by_id[claim_id]
            writer.writerow(
                {
                    "doc_id": claim_id,
                    "unit_kind": "claim",
                    "lane_score": f"{scores[claim_id]:.8f}",
                    "canonical_summary": card.get("canonical_summary", ""),
                    "targets": "|".join(card.get("targets", [])),
                    "primary_anchors": "|".join(card.get("primary_anchors", [])),
                    "supporting_targets": "|".join(card.get("supporting_targets", [])),
                    "implication_targets": "|".join(
                        card.get("implication_targets", [])
                    ),
                    "boundary_targets": "|".join(card.get("boundary_targets", [])),
                    "comparators": "|".join(card.get("comparators", [])),
                    "readouts": "|".join(card.get("readouts", [])),
                    "relation_family": card.get("relation_family", ""),
                    "direction_pattern": card.get("direction_pattern", ""),
                    "evidence_mode": card.get("evidence_mode", ""),
                    "active_default": str(bool(card.get("active_default"))).lower(),
                    "support_level": card.get("support_level", ""),
                    "de_support_level": card.get("de_support_level", ""),
                    "confidence": card.get("confidence", ""),
                    "member_count": card.get("member_count", 0),
                    "member_doc_ids": "|".join(
                        str(member.get("doc_id") or "")
                        for member in card.get("members", [])
                    ),
                    "member_roles": "|".join(
                        str(member.get("member_role") or "")
                        for member in card.get("members", [])
                    ),
                    "selection_reason": " | ".join(reasons[claim_id]),
                }
            )


def _write_edges(path: Path, edges: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=EDGE_FIELDS, delimiter="\t")
        writer.writeheader()
        writer.writerows(edges)


def _write_memberships(path: Path, memberships: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=MEMBERSHIP_FIELDS,
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(memberships)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", required=True, type=Path)
    parser.add_argument("--out-manifest", required=True, type=Path)
    parser.add_argument("--out-pool", required=True, type=Path)
    parser.add_argument("--out-edges", required=True, type=Path)
    parser.add_argument(
        "--out-memberships",
        type=Path,
        help=(
            "Optional provenance-preserving live Finding-to-Claim graph "
            "membership export."
        ),
    )
    parser.add_argument(
        "--assignments",
        type=Path,
        help="Claim assignments; defaults to the selected release projection",
    )
    parser.add_argument(
        "--relations",
        type=Path,
        help="Claim relations; defaults to the selected release projection",
    )
    parser.add_argument(
        "--ledger",
        type=Path,
        help="Finding ledger; defaults to the selected release Claim contract",
    )
    parser.add_argument(
        "--graph-mode", choices=("offline", "auto", "required"), default="auto"
    )
    parser.add_argument("--graph-hubcap", type=int, default=120)
    args = parser.parse_args()

    try:
        claim_layer = _selected_claim_layer()
    except RuntimeError as exc:
        parser.error(str(exc))
    args.assignments = args.assignments or Path(claim_layer.DEFAULT_ASSIGNMENTS)
    args.relations = args.relations or Path(claim_layer.DEFAULT_RELATIONS)
    args.ledger = args.ledger or Path(claim_layer.DEFAULT_LEDGER)

    profile = json.loads(args.profile.read_text(encoding="utf-8"))
    if not profile.get("claim_recall_required", True):
        raise SystemExit("direct_measurement does not require Claim recall")
    for required_path in (args.assignments, args.relations, args.ledger):
        if not required_path.is_file():
            raise SystemExit(f"required Claim artifact is missing: {required_path}")

    assignments = claim_layer.read_tsv(args.assignments)
    ledger = claim_layer.read_ledger(args.ledger)
    coverage = claim_layer.validate_assignments(assignments, ledger)
    cards = claim_layer.claim_cards(assignments, ledger)
    claim_ids = {str(card["claim_id"]) for card in cards}
    relations = _offline_relations(
        args.relations,
        claim_ids,
        claim_layer=claim_layer,
    )
    scores = _routing_scores(cards, profile)
    selected, reasons = _screen(cards, profile, scores, relations)
    memberships, graph = _live_memberships(
        args.graph_mode,
        _finding_to_claim(assignments),
    )
    edges = _routing_edges(
        selected,
        relations,
        memberships,
        hubcap=max(args.graph_hubcap, 2),
    )

    _write_pool(args.out_pool, cards, selected, scores, reasons)
    _write_edges(args.out_edges, edges)
    if args.out_memberships:
        _write_memberships(args.out_memberships, memberships)
    dispositions = []
    for card in sorted(cards, key=lambda value: str(value["claim_id"]).casefold()):
        claim_id = str(card["claim_id"])
        if claim_id in selected:
            disposition = "selected"
        elif _is_control(card):
            disposition = "excluded_control"
        else:
            disposition = "deprioritized"
        dispositions.append(
            {
                "claim_id": claim_id,
                "disposition": disposition,
                "reason": reasons[claim_id],
                "routing_score": scores[claim_id],
                "relation_family": card.get("relation_family"),
                "targets": card.get("targets"),
                "primary_anchors": card.get("primary_anchors"),
                "supporting_targets": card.get("supporting_targets"),
                "implication_targets": card.get("implication_targets"),
                "boundary_targets": card.get("boundary_targets"),
                "comparators": card.get("comparators"),
                "readouts": card.get("readouts"),
                "direction_pattern": card.get("direction_pattern"),
                "active_default": card.get("active_default"),
                "support_level": card.get("support_level"),
                "de_support_level": card.get("de_support_level"),
                "confidence": card.get("confidence"),
            }
        )
    counts = Counter(row["disposition"] for row in dispositions)
    relation_counts = Counter(
        str(card["relation_family"])
        for card in cards
        if str(card["claim_id"]) in selected
    )
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "task_class": profile.get("task_class"),
        "claim_strategy": profile.get("claim_strategy"),
        "profile_path": str(args.profile.resolve()),
        "artifacts": {
            "assignments": str(args.assignments.resolve()),
            "assignments_sha256": _sha256(args.assignments),
            "relations": str(args.relations.resolve()),
            "relations_sha256": _sha256(args.relations),
            "ledger": str(args.ledger.resolve()),
            "ledger_sha256": _sha256(args.ledger),
            "candidate_pool": str(args.out_pool.resolve()),
            "routing_edges": str(args.out_edges.resolve()),
        },
        "facets": {
            "endpoint": (profile.get("endpoint_definition") or {}).get("name"),
            "candidate_scope": profile.get("candidate_scope"),
            "explicit_targets": profile.get("explicit_targets", []),
            "query_terms": profile.get("query_terms", []),
        },
        "coverage": {
            "findings": coverage["findings"],
            "claims": coverage["claims"],
            "selected": counts["selected"],
            "deprioritized": counts["deprioritized"],
            "excluded_control": counts["excluded_control"],
            "accounted": sum(counts.values()),
            "unresolved": 0,
            "selected_by_relation_family": dict(sorted(relation_counts.items())),
        },
        "graph": {
            **graph,
            "frozen_relation_count": len(relations),
            "selected_routing_edge_count": len(edges),
            "selected_live_edge_count": sum(
                edge["source_layer"] == "live_program_complex" for edge in edges
            ),
        },
        "dispositions": dispositions,
    }
    if args.out_memberships:
        manifest["artifacts"].update(
            {
                "graph_memberships": str(args.out_memberships.resolve()),
                "graph_memberships_sha256": _sha256(args.out_memberships),
            }
        )
    if manifest["coverage"]["accounted"] != manifest["coverage"]["claims"]:
        raise RuntimeError("Claim disposition accounting failed")
    args.out_manifest.parent.mkdir(parents=True, exist_ok=True)
    args.out_manifest.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "task_class": manifest["task_class"],
                "coverage": manifest["coverage"],
                "graph": manifest["graph"],
                "manifest": str(args.out_manifest),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
