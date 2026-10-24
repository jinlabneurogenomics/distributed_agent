#!/usr/bin/env python3
"""Build bottom-up Claims over the Shi holdout biological Findings ledger.

The pipeline deliberately does not partition Findings into Claims. It builds
overlapping corpus-global neighborhoods, asks a model to propose higher-order
biological propositions, consolidates overlapping proposals, and records
many-to-many Finding contributions. The deterministic freeze stage validates
accepted outputs without changing the immutable source Findings or making
model calls.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import math
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping, Sequence


SCHEMA_VERSION = "july-bottom-up-claims-v1"
INDUCTION_VERSION = "july-bottom-up-claims-batched-v1"
CONSOLIDATION_VERSION = "july-bottom-up-claim-consolidation-v2"
BUILD_DIR = Path(__file__).resolve().parent
CONSOLIDATION_PROMPT_ID = "prompts/claim_consolidation_v2.md"
CONSOLIDATION_PROMPT_SHA256 = (
    "e11945da18cf2b93b0458c908191e689df4ba80c3132ffed1326b50f95eb335b"
)
CONSOLIDATION_OUTPUT_SCHEMA_ID = (
    "schemas/claim_consolidation_output_v2.schema.json"
)
CONSOLIDATION_OUTPUT_SCHEMA_SHA256 = (
    "cbf2ebccbf27509e20b6852c83aa463cadcca7ae75277445efb792f66816fa39"
)
FROZEN_NEIGHBORHOOD_VERSION = "july-bottom-up-claim-neighborhood-v1"
FROZEN_PROPOSAL_VERSION = "july-bottom-up-claim-proposal-v1"
FROZEN_PROPOSAL_DISPOSITION_VERSION = (
    "july-bottom-up-claim-proposal-disposition-v1"
)
FROZEN_CLAIM_VERSION = "july-bottom-up-claim-v1"
FROZEN_CONTRIBUTION_VERSION = "july-bottom-up-claim-contribution-v1"
FROZEN_FINDING_DISPOSITION_VERSION = (
    "july-bottom-up-finding-claim-disposition-v1"
)
FROZEN_BUILD_VERSION = "july-bottom-up-claim-build-v1"
DEFAULT_MAX_NEIGHBORHOODS_PER_CALL = 8
DEFAULT_MAX_PROMPT_CHARACTERS = 120_000
DEFAULT_MAX_NEIGHBORHOOD_SIMILARITY = 0.08
DEFAULT_MAX_COMPONENTS_PER_CALL = 8
DEFAULT_MAX_CONSOLIDATION_PROMPT_CHARACTERS = 120_000
DEFAULT_MAX_SINGLE_COMPONENT_PROMPT_CHARACTERS = 240_000
CONTRIBUTION_ROLES = frozenset(
    {"ANCHORS", "SUPPORTS", "QUALIFIES", "CONTRASTS"}
)
DISPOSITIONS = frozenset({"contributed", "no_higher_order_claim"})
WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]{2,}")
SPACE_RE = re.compile(r"\s+")
STOPWORDS = frozenset(
    """
    about after against all also among and are because been before being between
    both but can cannot compared comparison could data did does down during each
    effect effects either especially evidence finding findings first for from
    gene genes generated had has have having into its loss may measured more most
    not only other our out over perturbation perturbations response result same
    should signature than that the their them these they this those through to
    under up upon was were whereas which while with within would
    """.split()
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stable_id(prefix: str, values: Sequence[str]) -> str:
    digest = hashlib.sha256("\0".join(sorted(values)).encode()).hexdigest()[:20]
    return f"{prefix}:{digest}"


def text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def load_verified_method_asset(asset_id: str, expected_sha256: str) -> str:
    path = BUILD_DIR / asset_id
    if not path.is_file():
        raise FileNotFoundError(f"Claim method asset not found: {asset_id}")
    content = path.read_text(encoding="utf-8")
    actual = text_sha256(content)
    if actual != expected_sha256:
        raise ValueError(
            f"Claim method asset {asset_id!r} has SHA-256 {actual}; "
            f"expected {expected_sha256}"
        )
    return content


def iter_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_number}: expected a JSON object")
            yield value


def write_jsonl(path: Path, rows: Iterable[Mapping[str, Any]]) -> tuple[int, str]:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(canonical_json(dict(row)) + "\n")
            count += 1
    return count, sha256(path)


def write_json(path: Path, value: Mapping[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return sha256(path)


def release_relative_path(path: Path, release_root: Path) -> str:
    """Return a release-relative path when possible, otherwise an absolute path."""

    resolved = path.resolve()
    try:
        return resolved.relative_to(release_root.resolve()).as_posix()
    except ValueError:
        return str(resolved)


def normalized_text(value: Any) -> str:
    return SPACE_RE.sub(" ", str(value or "").casefold()).strip()


def load_findings(path: Path) -> list[dict[str, Any]]:
    rows = sorted(iter_jsonl(path), key=lambda row: str(row["doc_id"]))
    ids = [str(row.get("doc_id") or "") for row in rows]
    duplicates = sorted(doc_id for doc_id, count in Counter(ids).items() if count > 1)
    if not rows or not all(ids):
        raise ValueError("findings ledger must contain non-empty doc_id values")
    if duplicates:
        raise ValueError(f"duplicate finding doc_id values: {duplicates[:10]}")
    if any(row.get("null_cause") is not None for row in rows):
        raise ValueError("Claim induction accepts biological findings.jsonl only")
    return rows


def narrative(row: Mapping[str, Any]) -> str:
    return " ".join(
        normalized_text(row.get(field))
        for field in ("summary", "why_it_matters", "main_caveats", "direction")
    )


def text_features(row: Mapping[str, Any]) -> set[str]:
    """Return retrieval-only features; no feature becomes a durable Concept."""

    words = [
        token.casefold()
        for token in WORD_RE.findall(narrative(row))
        if token.casefold() not in STOPWORDS and not token.isdigit()
    ]
    features = {f"word:{word}" for word in words}
    features.update(
        f"bigram:{left}_{right}"
        for left, right in zip(words, words[1:])
        if left != right
    )
    features.add(f"type:{normalized_text(row.get('finding_type'))}")
    for gene in row.get("genes") or []:
        features.add(f"gene:{normalized_text(gene)}")
    for cell_type in row.get("cell_types") or []:
        features.add(f"cell:{normalized_text(cell_type)}")
    return {feature for feature in features if not feature.endswith(":")}


def explicit_name(text: str, name: str) -> bool:
    return bool(
        re.search(
            rf"(?<![a-z0-9]){re.escape(normalized_text(name))}(?![a-z0-9])",
            text,
        )
    )


def canonical_pair(left: str, right: str) -> tuple[str, str]:
    if left == right:
        raise ValueError(f"self-pair is invalid: {left}")
    return (left, right) if left < right else (right, left)


def pair_id(left: str, right: str) -> str:
    return stable_id("pair", canonical_pair(left, right))


def build_similarity(
    findings: Sequence[Mapping[str, Any]],
    *,
    maximum_feature_frequency: int,
) -> tuple[
    dict[str, set[str]],
    dict[str, float],
    dict[tuple[str, str], float],
    dict[tuple[str, str], tuple[str, ...]],
]:
    features_by_id = {
        str(row["doc_id"]): text_features(row)
        for row in sorted(findings, key=lambda value: str(value["doc_id"]))
    }
    postings: dict[str, list[str]] = defaultdict(list)
    for doc_id, features in features_by_id.items():
        for feature in features:
            postings[feature].append(doc_id)
    retained = {
        feature: sorted(doc_ids)
        for feature, doc_ids in postings.items()
        if 1 < len(doc_ids) <= maximum_feature_frequency
    }
    document_count = len(findings)
    weights = {
        feature: math.log((document_count + 1) / (len(doc_ids) + 1)) + 1.0
        for feature, doc_ids in retained.items()
    }
    norms = {
        doc_id: math.sqrt(
            sum(weights[feature] ** 2 for feature in features if feature in weights)
        )
        for doc_id, features in features_by_id.items()
    }
    dots: dict[tuple[str, str], float] = defaultdict(float)
    shared: dict[tuple[str, str], list[str]] = defaultdict(list)
    for feature in sorted(retained):
        weight_squared = weights[feature] ** 2
        doc_ids = retained[feature]
        for offset, left in enumerate(doc_ids):
            for right in doc_ids[offset + 1 :]:
                pair = (left, right)
                dots[pair] += weight_squared
                shared[pair].append(feature)
    scores: dict[tuple[str, str], float] = {}
    for pair, dot in dots.items():
        denominator = norms[pair[0]] * norms[pair[1]]
        scores[pair] = dot / denominator if denominator else 0.0
    return (
        features_by_id,
        weights,
        scores,
        {pair: tuple(sorted(values)) for pair, values in shared.items()},
    )


def _pair_signals(
    left: Mapping[str, Any],
    right: Mapping[str, Any],
    shared: Sequence[str],
) -> dict[str, Any]:
    left_target = normalized_text(left.get("target_gene"))
    right_target = normalized_text(right.get("target_gene"))
    left_comparators = {normalized_text(value) for value in left.get("comparators") or []}
    right_comparators = {normalized_text(value) for value in right.get("comparators") or []}
    return {
        "same_target": left_target == right_target,
        "left_explicitly_names_right": explicit_name(narrative(left), right_target),
        "right_explicitly_names_left": explicit_name(narrative(right), left_target),
        "left_lists_right_comparator": right_target in left_comparators,
        "right_lists_left_comparator": left_target in right_comparators,
        "shared_genes": sorted(
            feature.removeprefix("gene:")
            for feature in shared
            if feature.startswith("gene:")
        ),
        "shared_cell_types": sorted(
            feature.removeprefix("cell:")
            for feature in shared
            if feature.startswith("cell:")
        ),
    }


def generate_candidate_pairs(
    findings: Sequence[Mapping[str, Any]],
    *,
    neighbors_per_finding: int = 3,
    semantic_minimum_score: float = 0.32,
    one_sided_minimum_score: float = 0.16,
    maximum_feature_frequency: int = 96,
) -> list[dict[str, Any]]:
    """Return global semantic and explicit-one-sided seed pairs.

    Reciprocity never admits or rejects a pair. It is recorded after selection
    only so downstream audits can measure—not enforce—reciprocal reporting.
    """

    ordered = sorted(findings, key=lambda row: str(row["doc_id"]))
    row_by_id = {str(row["doc_id"]): row for row in ordered}
    by_target: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in ordered:
        by_target[normalized_text(row["target_gene"])].append(row)
    _, _, scores, shared = build_similarity(
        ordered, maximum_feature_frequency=maximum_feature_frequency
    )
    lanes: dict[tuple[str, str], set[str]] = defaultdict(set)

    neighbors: dict[str, list[tuple[float, str, tuple[str, str]]]] = defaultdict(list)
    for pair, score in scores.items():
        if score < semantic_minimum_score:
            continue
        neighbors[pair[0]].append((score, pair[1], pair))
        neighbors[pair[1]].append((score, pair[0], pair))
    for doc_id in sorted(row_by_id):
        ranked = sorted(neighbors.get(doc_id, ()), key=lambda item: (-item[0], item[1]))
        for _, _, pair in ranked[:neighbors_per_finding]:
            lanes[pair].add("global_semantic_neighbor")

    for source in ordered:
        source_id = str(source["doc_id"])
        source_text = narrative(source)
        source_target = normalized_text(source["target_gene"])
        comparator_targets = sorted(
            {
                normalized_text(value)
                for value in source.get("comparators") or []
                if normalized_text(value) != source_target
                and explicit_name(source_text, str(value))
            }
        )
        for target in comparator_targets:
            ranked: list[tuple[float, str, tuple[str, str]]] = []
            for other in by_target.get(target, ()):
                other_id = str(other["doc_id"])
                pair = canonical_pair(source_id, other_id)
                score = scores.get(pair, 0.0)
                pair_shared = shared.get(pair, ())
                concrete_overlap = any(
                    feature.startswith(("gene:", "cell:")) for feature in pair_shared
                )
                if score >= one_sided_minimum_score and concrete_overlap:
                    ranked.append((score, other_id, pair))
            if ranked:
                best = sorted(ranked, key=lambda item: (-item[0], item[1]))[0]
                lanes[best[2]].add("explicit_one_sided_mention")

    output: list[dict[str, Any]] = []
    for left_id, right_id in sorted(lanes):
        pair = (left_id, right_id)
        output.append(
            {
                "schema_version": SCHEMA_VERSION,
                "pair_id": pair_id(left_id, right_id),
                "left_doc_id": left_id,
                "right_doc_id": right_id,
                "retrieval_score": round(scores.get(pair, 0.0), 8),
                "retrieval_lanes": sorted(lanes[pair]),
                "signals": _pair_signals(
                    row_by_id[left_id], row_by_id[right_id], shared.get(pair, ())
                ),
            }
        )
    return output


def build_neighborhoods(
    pairs: Sequence[Mapping[str, Any]],
    *,
    maximum_findings: int = 6,
) -> list[dict[str, Any]]:
    """Expand each seed pair into a stable, overlapping local neighborhood."""

    if maximum_findings < 2:
        raise ValueError("maximum_findings must be at least two")
    adjacency: dict[str, list[tuple[float, str, str]]] = defaultdict(list)
    for row in pairs:
        left = str(row["left_doc_id"])
        right = str(row["right_doc_id"])
        score = float(row["retrieval_score"])
        identifier = str(row["pair_id"])
        adjacency[left].append((score, right, identifier))
        adjacency[right].append((score, left, identifier))

    grouped: dict[tuple[str, ...], dict[str, Any]] = {}
    for seed in sorted(pairs, key=lambda row: str(row["pair_id"])):
        left = str(seed["left_doc_id"])
        right = str(seed["right_doc_id"])
        members = {left, right}
        expansion = sorted(
            [*adjacency[left], *adjacency[right]],
            key=lambda item: (-item[0], item[1], item[2]),
        )
        for _, doc_id, _ in expansion:
            if len(members) >= maximum_findings:
                break
            members.add(doc_id)
        key = tuple(sorted(members))
        record = grouped.setdefault(
            key,
            {
                "schema_version": SCHEMA_VERSION,
                "neighborhood_id": stable_id("neighborhood", key),
                "finding_doc_ids": list(key),
                "seed_pair_ids": [],
                "retrieval_lanes": set(),
                "contains_one_sided_seed": False,
            },
        )
        record["seed_pair_ids"].append(str(seed["pair_id"]))
        record["retrieval_lanes"].update(seed["retrieval_lanes"])
        signals = seed["signals"]
        explicit_left = bool(signals["left_explicitly_names_right"])
        explicit_right = bool(signals["right_explicitly_names_left"])
        if explicit_left != explicit_right:
            record["contains_one_sided_seed"] = True

    output = []
    for record in grouped.values():
        output.append(
            {
                **record,
                "seed_pair_ids": sorted(set(record["seed_pair_ids"])),
                "retrieval_lanes": sorted(record["retrieval_lanes"]),
            }
        )
    return sorted(output, key=lambda row: str(row["neighborhood_id"]))


def finding_card(row: Mapping[str, Any]) -> dict[str, Any]:
    return {
        field: row.get(field)
        for field in (
            "doc_id",
            "target_gene",
            "finding_id",
            "finding_type",
            "summary",
            "why_it_matters",
            "direction",
            "confidence",
            "genes",
            "cell_types",
            "comparators",
            "main_caveats",
        )
    }


def prompt_finding_order(
    neighborhood_id: str, finding_doc_ids: Sequence[str]
) -> list[str]:
    """Return a stable hash order with no systematic target-alphabet position."""

    return sorted(
        finding_doc_ids,
        key=lambda doc_id: hashlib.sha256(
            f"{neighborhood_id}\0{doc_id}".encode()
        ).hexdigest(),
    )


def induction_prompt(
    neighborhood: Mapping[str, Any],
    findings_by_id: Mapping[str, Mapping[str, Any]],
) -> str:
    payload = {
        "neighborhood_id": neighborhood["neighborhood_id"],
        "findings": [
            finding_card(findings_by_id[doc_id])
            for doc_id in prompt_finding_order(
                str(neighborhood["neighborhood_id"]),
                neighborhood["finding_doc_ids"],
            )
        ],
    }
    return f"""Induce higher-order biological Claims bottom-up from this Finding neighborhood.

Each Finding is an immutable, perturbation-centered source interpretation. A
Claim is a new central biological proposition jointly established or bounded by
multiple Findings. Do NOT create one Claim per Finding and do NOT merely
paraphrase a Finding. Emit no Claim when the supplied Findings do not support a
coherent higher-order proposition.

A promoted Claim must:
- be one atomic, falsifiable biological proposition that can independently be
  true or false;
- have contributions from at least two distinct Findings;
- have at least one ANCHORS contribution;
- remain faithful to the supplied context, direction, and caveats;
- allow one-sided reporting: reciprocal comparator mention is never required.

Contribution roles:
- ANCHORS: directly states a central observation needed for the proposition.
- SUPPORTS: independently agrees with or strengthens the proposition.
- QUALIFIES: narrows its context, certainty, scope, or interpretation.
- CONTRASTS: supplies an opposing or non-phenocopy boundary that helps define it.

A Finding may contribute to more than one Claim. A broad coverage Finding can
anchor a broad Claim while narrow Findings support or qualify it. Do not invent
Programs, Concepts, mechanisms, measurements, or ontology labels not present in
the Findings.

Return the required JSON. local_claim_id values are C1, C2, ... . Give every
supplied Finding exactly one disposition: contributed if it occurs in any
Claim, otherwise no_higher_order_claim.

NEIGHBORHOOD:
{json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)}
"""


def neighborhood_batch_features(
    neighborhood: Mapping[str, Any],
    findings_by_id: Mapping[str, Mapping[str, Any]],
) -> frozenset[str]:
    """Return retrieval-like features used only to keep transport tasks apart."""

    features: set[str] = set()
    for doc_id in neighborhood["finding_doc_ids"]:
        finding = findings_by_id[str(doc_id)]
        features.add(f"target:{normalized_text(finding.get('target_gene'))}")
        features.update(
            feature
            for feature in text_features(finding)
            if feature.startswith(("gene:", "word:", "bigram:"))
        )
    return frozenset(features)


def feature_jaccard(left: frozenset[str], right: frozenset[str]) -> float:
    union = left | right
    return len(left & right) / len(union) if union else 0.0


def batch_neighborhood_order(
    batch_id: str,
    neighborhoods: Sequence[Mapping[str, Any]],
) -> list[Mapping[str, Any]]:
    """Use a stable non-alphabetical order inside a transport batch."""

    return sorted(
        neighborhoods,
        key=lambda row: hashlib.sha256(
            f"{batch_id}\0{row['neighborhood_id']}".encode()
        ).hexdigest(),
    )


def induction_batch_id(neighborhoods: Sequence[Mapping[str, Any]]) -> str:
    return stable_id(
        "induction-batch",
        [str(row["neighborhood_id"]) for row in neighborhoods],
    )


def batch_induction_prompt(
    neighborhoods: Sequence[Mapping[str, Any]],
    findings_by_id: Mapping[str, Mapping[str, Any]],
) -> str:
    batch_id = induction_batch_id(neighborhoods)
    payload = {
        "batch_id": batch_id,
        "neighborhoods": [
            {
                "neighborhood_id": neighborhood["neighborhood_id"],
                "findings": [
                    finding_card(findings_by_id[doc_id])
                    for doc_id in prompt_finding_order(
                        str(neighborhood["neighborhood_id"]),
                        neighborhood["finding_doc_ids"],
                    )
                ],
            }
            for neighborhood in batch_neighborhood_order(batch_id, neighborhoods)
        ],
    }
    return f"""Induce higher-order biological Claims independently for each supplied Finding neighborhood.

This call is only a transport batch. Neighborhoods were intentionally chosen to
be dissimilar and non-overlapping. Do not compare, combine, harmonize, rank, or
create contributions across neighborhood boundaries. Return exactly one result
for each neighborhood, even when that result contains no Claims.

Within each neighborhood, each Finding is an immutable,
perturbation-centered source interpretation. A Claim is a new central
biological proposition jointly established or bounded by multiple Findings.
Do NOT create one Claim per Finding and do NOT merely paraphrase a Finding.
Emit no Claim when that neighborhood does not support a coherent higher-order
proposition.

Each promoted Claim must:
- be one atomic, falsifiable biological proposition that can independently be
  true or false;
- have contributions from at least two distinct Findings in its neighborhood;
- have at least one ANCHORS contribution;
- remain faithful to the supplied context, direction, and caveats;
- allow one-sided reporting: reciprocal comparator mention is never required.

Contribution roles:
- ANCHORS: directly states a central observation needed for the proposition.
- SUPPORTS: independently agrees with or strengthens the proposition.
- QUALIFIES: narrows its context, certainty, scope, or interpretation.
- CONTRASTS: supplies an opposing or non-phenocopy boundary that helps define it.

A Finding may contribute to more than one Claim within its neighborhood. A
broad coverage Finding can anchor a broad Claim while narrow Findings support
or qualify it. Do not invent Programs, Concepts, mechanisms, measurements, or
ontology labels not present in that neighborhood.

For each neighborhood, local_claim_id values are C1, C2, ... . Give every
Finding exactly one disposition: contributed if it occurs in any Claim,
otherwise no_higher_order_claim.

BATCH:
{canonical_json(payload)}
"""


def batch_pair_similarity(
    neighborhoods: Sequence[Mapping[str, Any]],
    features_by_neighborhood: Mapping[str, frozenset[str]],
) -> float:
    maximum = 0.0
    for offset, left in enumerate(neighborhoods):
        left_id = str(left["neighborhood_id"])
        for right in neighborhoods[offset + 1 :]:
            right_id = str(right["neighborhood_id"])
            maximum = max(
                maximum,
                feature_jaccard(
                    features_by_neighborhood[left_id],
                    features_by_neighborhood[right_id],
                ),
            )
    return maximum


def pack_induction_batches(
    neighborhoods: Sequence[Mapping[str, Any]],
    findings_by_id: Mapping[str, Mapping[str, Any]],
    *,
    maximum_neighborhoods_per_call: int = DEFAULT_MAX_NEIGHBORHOODS_PER_CALL,
    maximum_prompt_characters: int = DEFAULT_MAX_PROMPT_CHARACTERS,
    maximum_neighborhood_similarity: float = DEFAULT_MAX_NEIGHBORHOOD_SIMILARITY,
) -> list[dict[str, Any]]:
    """Pack independent neighborhoods without turning batches into semantic units."""

    if maximum_neighborhoods_per_call < 1:
        raise ValueError("maximum_neighborhoods_per_call must be positive")
    if maximum_prompt_characters < 1:
        raise ValueError("maximum_prompt_characters must be positive")
    if not 0.0 <= maximum_neighborhood_similarity <= 1.0:
        raise ValueError("maximum_neighborhood_similarity must be between zero and one")

    ordered = sorted(
        neighborhoods,
        key=lambda row: text_sha256(str(row["neighborhood_id"])),
    )
    features = {
        str(row["neighborhood_id"]): neighborhood_batch_features(row, findings_by_id)
        for row in ordered
    }
    doc_ids = {
        str(row["neighborhood_id"]): set(map(str, row["finding_doc_ids"]))
        for row in ordered
    }
    targets = {
        str(row["neighborhood_id"]): {
            normalized_text(findings_by_id[str(doc_id)].get("target_gene"))
            for doc_id in row["finding_doc_ids"]
        }
        for row in ordered
    }
    groups: list[list[Mapping[str, Any]]] = []
    for neighborhood in ordered:
        neighborhood_id = str(neighborhood["neighborhood_id"])
        candidates: list[tuple[float, int]] = []
        for index, group in enumerate(groups):
            if len(group) >= maximum_neighborhoods_per_call:
                continue
            group_ids = [str(row["neighborhood_id"]) for row in group]
            if any(
                doc_ids[neighborhood_id] & doc_ids[group_id]
                for group_id in group_ids
            ):
                continue
            if any(
                targets[neighborhood_id] & targets[group_id]
                for group_id in group_ids
            ):
                continue
            similarity = max(
                (
                    feature_jaccard(features[neighborhood_id], features[group_id])
                    for group_id in group_ids
                ),
                default=0.0,
            )
            if similarity > maximum_neighborhood_similarity:
                continue
            tentative = [*group, neighborhood]
            if (
                len(batch_induction_prompt(tentative, findings_by_id))
                > maximum_prompt_characters
            ):
                continue
            candidates.append((similarity, index))
        if candidates:
            _, index = min(candidates, key=lambda item: (item[0], item[1]))
            groups[index].append(neighborhood)
            continue
        if (
            len(batch_induction_prompt([neighborhood], findings_by_id))
            > maximum_prompt_characters
        ):
            raise ValueError(
                f"{neighborhood_id}: one neighborhood exceeds "
                "maximum_prompt_characters"
            )
        groups.append([neighborhood])

    batches = []
    for group in groups:
        batch_id = induction_batch_id(group)
        prompt_characters = len(batch_induction_prompt(group, findings_by_id))
        batches.append(
            {
                "schema_version": INDUCTION_VERSION,
                "batch_id": batch_id,
                "neighborhoods": batch_neighborhood_order(batch_id, group),
                "maximum_pair_similarity": round(
                    batch_pair_similarity(group, features), 8
                ),
                "prompt_characters": prompt_characters,
                "estimated_prompt_tokens": math.ceil(prompt_characters / 4),
            }
        )
    return sorted(batches, key=lambda row: str(row["batch_id"]))


def induction_output_schema() -> dict[str, Any]:
    contribution = {
        "type": "object",
        "additionalProperties": False,
        "required": ["finding_doc_id", "role", "rationale"],
        "properties": {
            "finding_doc_id": {"type": "string"},
            "role": {"type": "string", "enum": sorted(CONTRIBUTION_ROLES)},
            "rationale": {"type": "string", "minLength": 1},
        },
    }
    claim = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "local_claim_id",
            "statement",
            "scope",
            "higher_order_basis",
            "confidence",
            "contributions",
        ],
        "properties": {
            "local_claim_id": {"type": "string"},
            "statement": {"type": "string", "minLength": 1},
            "scope": {"type": "string", "minLength": 1},
            "higher_order_basis": {"type": "string", "minLength": 1},
            "confidence": {
                "type": "string",
                "enum": ["high", "moderate", "low"],
            },
            "contributions": {
                "type": "array",
                "minItems": 2,
                "items": contribution,
            },
        },
    }
    disposition = {
        "type": "object",
        "additionalProperties": False,
        "required": ["finding_doc_id", "disposition", "rationale"],
        "properties": {
            "finding_doc_id": {"type": "string"},
            "disposition": {"type": "string", "enum": sorted(DISPOSITIONS)},
            "rationale": {"type": "string", "minLength": 1},
        },
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": ["neighborhood_id", "claims", "finding_dispositions"],
        "properties": {
            "neighborhood_id": {"type": "string"},
            "claims": {"type": "array", "items": claim},
            "finding_dispositions": {"type": "array", "items": disposition},
        },
    }


def batch_induction_output_schema() -> dict[str, Any]:
    neighborhood_result = dict(induction_output_schema())
    neighborhood_result.pop("$schema", None)
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": ["batch_id", "neighborhood_results"],
        "properties": {
            "batch_id": {"type": "string"},
            "neighborhood_results": {
                "type": "array",
                "items": neighborhood_result,
            },
        },
    }


def validate_induction_result(
    neighborhood: Mapping[str, Any],
    result: Mapping[str, Any],
    findings_by_id: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    if result.get("neighborhood_id") != neighborhood["neighborhood_id"]:
        raise ValueError("neighborhood_id mismatch")
    allowed = set(neighborhood["finding_doc_ids"])
    claims = result.get("claims") or []
    local_ids = [str(row.get("local_claim_id") or "") for row in claims]
    if not all(local_ids) or len(local_ids) != len(set(local_ids)):
        raise ValueError("local Claim IDs must be non-empty and unique")
    contributed: set[str] = set()
    source_summaries = {
        normalized_text(findings_by_id[doc_id].get("summary")) for doc_id in allowed
    }
    for claim in claims:
        contributions = claim.get("contributions") or []
        doc_ids = [str(row.get("finding_doc_id") or "") for row in contributions]
        if len(set(doc_ids)) < 2 or len(doc_ids) != len(set(doc_ids)):
            raise ValueError(
                f"{claim.get('local_claim_id')}: needs at least two unique contributions"
            )
        if not set(doc_ids).issubset(allowed):
            raise ValueError(f"{claim.get('local_claim_id')}: invented Finding")
        roles = {str(row.get("role") or "") for row in contributions}
        if not roles.issubset(CONTRIBUTION_ROLES) or "ANCHORS" not in roles:
            raise ValueError(
                f"{claim.get('local_claim_id')}: invalid roles or missing ANCHORS"
            )
        if normalized_text(claim.get("statement")) in source_summaries:
            raise ValueError(
                f"{claim.get('local_claim_id')}: Claim merely copies a Finding summary"
            )
        contributed.update(doc_ids)

    dispositions = result.get("finding_dispositions") or []
    disposition_ids = [str(row.get("finding_doc_id") or "") for row in dispositions]
    if len(disposition_ids) != len(set(disposition_ids)) or set(disposition_ids) != allowed:
        raise ValueError("finding dispositions must cover the neighborhood exactly once")
    for row in dispositions:
        doc_id = str(row["finding_doc_id"])
        expected = "contributed" if doc_id in contributed else "no_higher_order_claim"
        if row.get("disposition") != expected:
            raise ValueError(f"{doc_id}: disposition must be {expected}")
    return {"schema_version": SCHEMA_VERSION, **dict(result)}



def validate_batch_result(
    batch: Mapping[str, Any],
    result: Mapping[str, Any],
    findings_by_id: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    if result.get("batch_id") != batch["batch_id"]:
        raise ValueError("batch_id mismatch")
    expected = {
        str(row["neighborhood_id"]): row for row in batch["neighborhoods"]
    }
    result_rows = result.get("neighborhood_results") or []
    result_ids = [str(row.get("neighborhood_id") or "") for row in result_rows]
    if (
        not all(result_ids)
        or len(result_ids) != len(set(result_ids))
        or set(result_ids) != set(expected)
    ):
        raise ValueError("batch must return every neighborhood exactly once")
    validated = [
        validate_induction_result(expected[neighborhood_id], row, findings_by_id)
        for neighborhood_id, row in (
            (str(row["neighborhood_id"]), row) for row in result_rows
        )
    ]
    return {
        "schema_version": INDUCTION_VERSION,
        "batch_id": batch["batch_id"],
        "neighborhood_results": validated,
    }


def batch_cache_metadata(
    batch: Mapping[str, Any],
    *,
    prompt: str,
    findings_sha256: str,
    neighborhoods_sha256: str,
    response_schema_sha256: str,
    model: str,
    reasoning_effort: str,
) -> dict[str, Any]:
    batch_source = [
        {
            "neighborhood_id": row["neighborhood_id"],
            "finding_doc_ids": row["finding_doc_ids"],
        }
        for row in batch["neighborhoods"]
    ]
    return {
        "induction_version": INDUCTION_VERSION,
        "batch_id": batch["batch_id"],
        "batch_source_sha256": text_sha256(canonical_json(batch_source)),
        "findings_sha256": findings_sha256,
        "neighborhoods_sha256": neighborhoods_sha256,
        "prompt_sha256": text_sha256(prompt),
        "response_schema_sha256": response_schema_sha256,
        "model": model,
        "reasoning_effort": reasoning_effort,
    }


def materialize_neighborhood_results(
    validated_batch: Mapping[str, Any],
    results_dir: Path,
) -> None:
    for result in validated_batch["neighborhood_results"]:
        stem = str(result["neighborhood_id"]).removeprefix("neighborhood:")
        write_json(results_dir / f"{stem}.json", result)


def run_induction_batch(
    batch: Mapping[str, Any],
    *,
    findings_by_id: Mapping[str, Mapping[str, Any]],
    findings_sha256: str,
    neighborhoods_sha256: str,
    results_dir: Path,
    batch_results_dir: Path,
    schema_path: Path,
    model: str,
    reasoning_effort: str,
    codex: str,
    timeout_seconds: int,
    overwrite: bool,
    repository: Path,
) -> tuple[str, str]:
    batch_id = str(batch["batch_id"])
    stem = batch_id.removeprefix("induction-batch:")
    output = batch_results_dir / f"{stem}.json"
    metadata_path = batch_results_dir / f"{stem}.meta.json"
    log = batch_results_dir / f"{stem}.log"
    prompt = batch_induction_prompt(batch["neighborhoods"], findings_by_id)
    expected_metadata = batch_cache_metadata(
        batch,
        prompt=prompt,
        findings_sha256=findings_sha256,
        neighborhoods_sha256=neighborhoods_sha256,
        response_schema_sha256=sha256(schema_path),
        model=model,
        reasoning_effort=reasoning_effort,
    )
    if output.is_file() and metadata_path.is_file() and not overwrite:
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            parsed = json.loads(output.read_text(encoding="utf-8"))
            if metadata != expected_metadata:
                raise ValueError("cache fingerprint mismatch")
            validated = validate_batch_result(batch, parsed, findings_by_id)
            materialize_neighborhood_results(validated, results_dir)
            return batch_id, "cached"
        except (OSError, ValueError, json.JSONDecodeError):
            pass

    command = [
        codex,
        "exec",
        "--ephemeral",
        "--ignore-user-config",
        "--skip-git-repo-check",
        "--sandbox",
        "read-only",
        "--model",
        model,
        "--config",
        f'model_reasoning_effort="{reasoning_effort}"',
        "--output-schema",
        str(schema_path),
        "--output-last-message",
        str(output),
        "-",
    ]
    try:
        completed = subprocess.run(
            command,
            input=prompt,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=repository,
            env=os.environ.copy(),
            check=False,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        log.write_text(str(exc.stdout or ""), encoding="utf-8")
        raise RuntimeError(
            f"{batch_id}: Codex timeout after {timeout_seconds}s"
        ) from exc
    log.write_text(completed.stdout or "", encoding="utf-8")
    if completed.returncode != 0:
        raise RuntimeError(f"{batch_id}: Codex exit {completed.returncode}")
    try:
        parsed = json.loads(output.read_text(encoding="utf-8"))
        validated = validate_batch_result(batch, parsed, findings_by_id)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"{batch_id}: invalid result: {exc}") from exc
    materialize_neighborhood_results(validated, results_dir)
    write_json(metadata_path, expected_metadata)
    return batch_id, "induced"


def prepare_command(args: argparse.Namespace) -> int:
    findings = load_findings(args.findings)
    pairs = generate_candidate_pairs(
        findings,
        neighbors_per_finding=args.neighbors_per_finding,
        semantic_minimum_score=args.semantic_minimum_score,
        one_sided_minimum_score=args.one_sided_minimum_score,
        maximum_feature_frequency=args.maximum_feature_frequency,
    )
    neighborhoods = build_neighborhoods(
        pairs, maximum_findings=args.maximum_findings
    )
    pair_count, pair_hash = write_jsonl(args.pairs, pairs)
    neighborhood_count, neighborhood_hash = write_jsonl(
        args.neighborhoods, neighborhoods
    )
    build = {
        "schema_version": SCHEMA_VERSION,
        "stage": "neighborhood_preparation",
        "source": {
            "artifact": "findings",
            "sha256": sha256(args.findings),
            "records": len(findings),
        },
        "outputs": {
            "pairs": {"records": pair_count, "sha256": pair_hash},
            "neighborhoods": {
                "records": neighborhood_count,
                "sha256": neighborhood_hash,
            },
        },
        "parameters": {
            "neighbors_per_finding": args.neighbors_per_finding,
            "semantic_minimum_score": args.semantic_minimum_score,
            "one_sided_minimum_score": args.one_sided_minimum_score,
            "maximum_feature_frequency": args.maximum_feature_frequency,
            "maximum_findings": args.maximum_findings,
        },
        "build_policy": {
            "scope": "corpus_global_overlapping_neighborhoods",
            "target_partition": False,
            "alphabetical_packets": False,
            "prompt_finding_order": "sha256_neighborhood_and_doc_id",
            "reciprocity_required": False,
            "explicit_one_sided_lane": True,
            "network": False,
            "model_calls": False,
        },
    }
    write_json(args.build_record, build)
    print(canonical_json(build["outputs"]))
    return 0


def selected_neighborhoods(
    neighborhoods: Sequence[Mapping[str, Any]], args: argparse.Namespace
) -> list[Mapping[str, Any]]:
    selected = list(neighborhoods)
    if args.neighborhood_id:
        wanted = set(args.neighborhood_id)
        selected = [row for row in selected if row["neighborhood_id"] in wanted]
        missing = wanted - {str(row["neighborhood_id"]) for row in selected}
        if missing:
            raise ValueError(f"unknown neighborhood IDs: {sorted(missing)}")
    if args.contains:
        wanted_docs = set(args.contains)
        selected = [
            row
            for row in selected
            if wanted_docs.intersection(row["finding_doc_ids"])
        ]
    if args.limit:
        selected = selected[: args.limit]
    if not selected:
        raise ValueError("no neighborhoods selected")
    return selected



def batch_plan_record(batch: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": INDUCTION_VERSION,
        "batch_id": batch["batch_id"],
        "neighborhood_ids": [
            row["neighborhood_id"] for row in batch["neighborhoods"]
        ],
        "neighborhood_count": len(batch["neighborhoods"]),
        "maximum_pair_similarity": batch["maximum_pair_similarity"],
        "prompt_characters": batch["prompt_characters"],
        "estimated_prompt_tokens": batch["estimated_prompt_tokens"],
    }


def run_batched_command(args: argparse.Namespace) -> int:
    findings = load_findings(args.findings)
    findings_by_id = {str(row["doc_id"]): row for row in findings}
    neighborhoods = list(iter_jsonl(args.neighborhoods))
    selected = selected_neighborhoods(neighborhoods, args)
    batches = pack_induction_batches(
        selected,
        findings_by_id,
        maximum_neighborhoods_per_call=args.maximum_neighborhoods_per_call,
        maximum_prompt_characters=args.maximum_prompt_characters,
        maximum_neighborhood_similarity=args.maximum_neighborhood_similarity,
    )
    args.work_dir.mkdir(parents=True, exist_ok=True)
    plan_count, plan_digest = write_jsonl(
        args.batch_plan, [batch_plan_record(batch) for batch in batches]
    )
    prompt_characters = [int(batch["prompt_characters"]) for batch in batches]
    plan_summary = {
        "schema_version": INDUCTION_VERSION,
        "selected_neighborhoods": len(selected),
        "model_calls": len(batches),
        "batch_plan": {
            "path": str(args.batch_plan),
            "records": plan_count,
            "sha256": plan_digest,
        },
        "batch_sizes": dict(
            sorted(
                Counter(len(batch["neighborhoods"]) for batch in batches).items()
            )
        ),
        "prompt_characters": {
            "minimum": min(prompt_characters),
            "maximum": max(prompt_characters),
            "mean": round(sum(prompt_characters) / len(prompt_characters), 2),
        },
        "maximum_estimated_prompt_tokens": max(
            int(batch["estimated_prompt_tokens"]) for batch in batches
        ),
    }
    if args.plan_only:
        print(canonical_json(plan_summary))
        return 0

    results_dir = args.work_dir / "results"
    results_dir.mkdir(exist_ok=True)
    batch_results_dir = args.work_dir / "batch-results"
    batch_results_dir.mkdir(exist_ok=True)
    schema_path = args.work_dir / "batch-induction-output.schema.json"
    write_json(schema_path, batch_induction_output_schema())
    repository = Path(__file__).resolve().parents[6]
    findings_digest = sha256(args.findings)
    neighborhoods_digest = sha256(args.neighborhoods)
    lock_path = args.work_dir / ".run.lock"
    with lock_path.open("w", encoding="utf-8") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise ValueError(f"another Claim induction is using {args.work_dir}") from exc
        lock.write(f"pid={os.getpid()}\n")
        lock.flush()
        failures: list[str] = []
        completed_count = 0
        with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
            futures = {
                pool.submit(
                    run_induction_batch,
                    batch,
                    findings_by_id=findings_by_id,
                    findings_sha256=findings_digest,
                    neighborhoods_sha256=neighborhoods_digest,
                    results_dir=results_dir,
                    batch_results_dir=batch_results_dir,
                    schema_path=schema_path,
                    model=args.model,
                    reasoning_effort=args.reasoning_effort,
                    codex=args.codex,
                    timeout_seconds=args.timeout_seconds,
                    overwrite=args.overwrite,
                    repository=repository,
                ): batch
                for batch in batches
            }
            for future in as_completed(futures):
                completed_count += 1
                batch = futures[future]
                try:
                    identifier, disposition = future.result()
                    print(
                        f"[{completed_count}/{len(batches)}] "
                        f"{identifier} {disposition}",
                        file=sys.stderr,
                    )
                except Exception as exc:  # noqa: BLE001 - collect independent failures
                    failures.append(f"{batch['batch_id']}: {exc}")
                    print(
                        f"[{completed_count}/{len(batches)}] {failures[-1]}",
                        file=sys.stderr,
                    )
        if failures:
            raise RuntimeError(
                f"{len(failures)} induction batches failed; "
                f"first failures: {failures[:5]}"
            )

    combined = []
    by_id = {str(row["neighborhood_id"]): row for row in neighborhoods}
    for neighborhood in selected:
        stem = str(neighborhood["neighborhood_id"]).removeprefix("neighborhood:")
        parsed = json.loads(
            (results_dir / f"{stem}.json").read_text(encoding="utf-8")
        )
        combined.append(
            validate_induction_result(
                by_id[str(neighborhood["neighborhood_id"])],
                parsed,
                findings_by_id,
            )
        )
    count, digest = write_jsonl(args.results, combined)
    print(
        canonical_json(
            {
                **plan_summary,
                "results": str(args.results),
                "records": count,
                "sha256": digest,
            }
        )
    )
    return 0


def flatten_induction_proposals(
    results: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Return stable proposal records from neighborhood-local model outputs."""

    proposals: list[dict[str, Any]] = []
    seen: set[str] = set()
    for result in sorted(results, key=lambda row: str(row["neighborhood_id"])):
        neighborhood_id = str(result["neighborhood_id"])
        for claim in result.get("claims") or []:
            local_claim_id = str(claim["local_claim_id"])
            identifier = stable_id(
                "proposal", [neighborhood_id, local_claim_id]
            )
            if identifier in seen:
                raise ValueError(f"duplicate proposal ID: {identifier}")
            seen.add(identifier)
            contributions = sorted(
                (dict(row) for row in claim["contributions"]),
                key=lambda row: str(row["finding_doc_id"]),
            )
            proposals.append(
                {
                    "schema_version": CONSOLIDATION_VERSION,
                    "proposal_id": identifier,
                    "source_neighborhood_id": neighborhood_id,
                    "source_local_claim_id": local_claim_id,
                    "statement": claim["statement"],
                    "scope": claim["scope"],
                    "higher_order_basis": claim["higher_order_basis"],
                    "confidence": claim["confidence"],
                    "contributions": contributions,
                }
            )
    return sorted(proposals, key=lambda row: str(row["proposal_id"]))


def build_proposal_components(
    proposals: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Connect proposals through shared Finding contributions."""

    ordered = sorted(proposals, key=lambda row: str(row["proposal_id"]))
    parent = list(range(len(ordered)))

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left: int, right: int) -> None:
        left_root = find(left)
        right_root = find(right)
        if left_root != right_root:
            parent[right_root] = left_root

    finding_owner: dict[str, int] = {}
    for index, proposal in enumerate(ordered):
        for contribution in proposal["contributions"]:
            doc_id = str(contribution["finding_doc_id"])
            if doc_id in finding_owner:
                union(index, finding_owner[doc_id])
            else:
                finding_owner[doc_id] = index

    grouped: dict[int, list[Mapping[str, Any]]] = defaultdict(list)
    for index, proposal in enumerate(ordered):
        grouped[find(index)].append(proposal)

    components: list[dict[str, Any]] = []
    for rows in grouped.values():
        proposal_ids = sorted(str(row["proposal_id"]) for row in rows)
        finding_doc_ids = sorted(
            {
                str(contribution["finding_doc_id"])
                for row in rows
                for contribution in row["contributions"]
            }
        )
        components.append(
            {
                "schema_version": CONSOLIDATION_VERSION,
                "component_id": stable_id("proposal-component", proposal_ids),
                "proposal_ids": proposal_ids,
                "finding_doc_ids": finding_doc_ids,
            }
        )
    return sorted(components, key=lambda row: str(row["component_id"]))


def consolidation_component_payload(
    component: Mapping[str, Any],
    proposals_by_id: Mapping[str, Mapping[str, Any]],
    findings_by_id: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    component_id = str(component["component_id"])
    proposal_ids = sorted(
        component["proposal_ids"],
        key=lambda proposal_id: text_sha256(f"{component_id}\0{proposal_id}"),
    )
    finding_doc_ids = sorted(
        component["finding_doc_ids"],
        key=lambda doc_id: text_sha256(f"{component_id}\0{doc_id}"),
    )
    return {
        "component_id": component_id,
        "proposals": [proposals_by_id[str(value)] for value in proposal_ids],
        "findings": [
            finding_card(findings_by_id[str(value)]) for value in finding_doc_ids
        ],
    }


def consolidation_batch_id(
    components: Sequence[Mapping[str, Any]],
) -> str:
    return stable_id(
        "consolidation-batch",
        [str(row["component_id"]) for row in components],
    )


def consolidation_batch_order(
    batch_id: str,
    components: Sequence[Mapping[str, Any]],
) -> list[Mapping[str, Any]]:
    return sorted(
        components,
        key=lambda row: text_sha256(
            f"{batch_id}\0{row['component_id']}"
        ),
    )


def consolidation_prompt(
    components: Sequence[Mapping[str, Any]],
    proposals_by_id: Mapping[str, Mapping[str, Any]],
    findings_by_id: Mapping[str, Mapping[str, Any]],
) -> str:
    batch_id = consolidation_batch_id(components)
    payload = {
        "batch_id": batch_id,
        "components": [
            consolidation_component_payload(
                component, proposals_by_id, findings_by_id
            )
            for component in consolidation_batch_order(batch_id, components)
        ],
    }
    template = load_verified_method_asset(
        CONSOLIDATION_PROMPT_ID, CONSOLIDATION_PROMPT_SHA256
    )
    placeholder = "{json(payload)}"
    if template.count(placeholder) != 1:
        raise ValueError(
            f"Claim consolidation prompt must contain one {placeholder!r} placeholder"
        )
    return template.replace(placeholder, canonical_json(payload))


def pack_consolidation_batches(
    components: Sequence[Mapping[str, Any]],
    proposals_by_id: Mapping[str, Mapping[str, Any]],
    findings_by_id: Mapping[str, Mapping[str, Any]],
    *,
    maximum_components_per_call: int = DEFAULT_MAX_COMPONENTS_PER_CALL,
    maximum_prompt_characters: int = (
        DEFAULT_MAX_CONSOLIDATION_PROMPT_CHARACTERS
    ),
    maximum_single_component_prompt_characters: int = (
        DEFAULT_MAX_SINGLE_COMPONENT_PROMPT_CHARACTERS
    ),
) -> list[dict[str, Any]]:
    """Best-fit-pack disjoint proposal components into transport calls."""

    if maximum_components_per_call < 1:
        raise ValueError("maximum_components_per_call must be positive")
    if maximum_prompt_characters < 1:
        raise ValueError("maximum_prompt_characters must be positive")
    if (
        maximum_single_component_prompt_characters
        < maximum_prompt_characters
    ):
        raise ValueError(
            "maximum_single_component_prompt_characters must be at least "
            "maximum_prompt_characters"
        )

    single_sizes = {
        str(component["component_id"]): len(
            consolidation_prompt(
                [component], proposals_by_id, findings_by_id
            )
        )
        for component in components
    }
    ordered = sorted(
        components,
        key=lambda row: (
            -single_sizes[str(row["component_id"])],
            text_sha256(str(row["component_id"])),
        ),
    )
    groups: list[list[Mapping[str, Any]]] = []
    group_sizes: list[int] = []
    for component in ordered:
        component_id = str(component["component_id"])
        single_size = single_sizes[component_id]
        if single_size > maximum_single_component_prompt_characters:
            raise ValueError(
                f"{component_id}: prompt has {single_size} characters, above "
                "maximum_single_component_prompt_characters"
            )
        if single_size > maximum_prompt_characters:
            groups.append([component])
            group_sizes.append(single_size)
            continue

        candidates: list[tuple[int, int]] = []
        for index, group in enumerate(groups):
            if group_sizes[index] > maximum_prompt_characters:
                continue
            if len(group) >= maximum_components_per_call:
                continue
            prompt_characters = len(
                consolidation_prompt(
                    [*group, component], proposals_by_id, findings_by_id
                )
            )
            if prompt_characters <= maximum_prompt_characters:
                candidates.append((prompt_characters, index))
        if candidates:
            prompt_characters, index = max(
                candidates, key=lambda item: (item[0], -item[1])
            )
            groups[index].append(component)
            group_sizes[index] = prompt_characters
        else:
            groups.append([component])
            group_sizes.append(single_size)

    batches = []
    for group in groups:
        batch_id = consolidation_batch_id(group)
        prompt_characters = len(
            consolidation_prompt(group, proposals_by_id, findings_by_id)
        )
        batches.append(
            {
                "schema_version": CONSOLIDATION_VERSION,
                "batch_id": batch_id,
                "components": consolidation_batch_order(batch_id, group),
                "prompt_characters": prompt_characters,
                "estimated_prompt_tokens": math.ceil(prompt_characters / 4),
                "oversized_single_component": (
                    len(group) == 1
                    and prompt_characters > maximum_prompt_characters
                ),
            }
        )
    return sorted(batches, key=lambda row: str(row["batch_id"]))


def consolidation_output_schema() -> dict[str, Any]:
    content = load_verified_method_asset(
        CONSOLIDATION_OUTPUT_SCHEMA_ID,
        CONSOLIDATION_OUTPUT_SCHEMA_SHA256,
    )
    schema = json.loads(content)
    schema_roles = set(
        schema["$defs"]["contribution"]["properties"]["role"]["enum"]
    )
    if schema_roles != CONTRIBUTION_ROLES:
        raise ValueError("Claim consolidation schema roles do not match runtime roles")
    return schema


def validate_consolidation_component(
    component: Mapping[str, Any],
    result: Mapping[str, Any],
    proposals_by_id: Mapping[str, Mapping[str, Any]],
    findings_by_id: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    component_id = str(component["component_id"])
    if result.get("component_id") != component_id:
        raise ValueError("component_id mismatch")
    allowed_proposals = set(map(str, component["proposal_ids"]))
    allowed_findings = set(map(str, component["finding_doc_ids"]))

    claims = result.get("claims") or []
    local_ids = [str(row.get("local_claim_id") or "") for row in claims]
    if not all(local_ids) or len(local_ids) != len(set(local_ids)):
        raise ValueError(
            f"{component_id}: local Claim IDs must be non-empty and unique"
        )
    statement_signatures = [
        (normalized_text(row.get("statement")), normalized_text(row.get("scope")))
        for row in claims
    ]
    if len(statement_signatures) != len(set(statement_signatures)):
        raise ValueError(f"{component_id}: duplicate canonical Claims")

    proposal_claims: dict[str, list[str]] = defaultdict(list)
    claim_source_counts: dict[str, int] = {}
    source_summaries = {
        normalized_text(findings_by_id[doc_id].get("summary"))
        for doc_id in allowed_findings
    }
    for claim in claims:
        local_claim_id = str(claim["local_claim_id"])
        source_proposal_ids = list(map(str, claim["source_proposal_ids"]))
        if (
            not source_proposal_ids
            or len(source_proposal_ids) != len(set(source_proposal_ids))
            or not set(source_proposal_ids).issubset(allowed_proposals)
        ):
            raise ValueError(
                f"{component_id}/{local_claim_id}: invalid source proposals"
            )
        claim_source_counts[local_claim_id] = len(source_proposal_ids)
        for proposal_id in source_proposal_ids:
            proposal_claims[proposal_id].append(local_claim_id)

        contributions = claim.get("contributions") or []
        finding_doc_ids = [
            str(row.get("finding_doc_id") or "") for row in contributions
        ]
        if (
            len(finding_doc_ids) < 2
            or len(finding_doc_ids) != len(set(finding_doc_ids))
            or not set(finding_doc_ids).issubset(allowed_findings)
        ):
            raise ValueError(
                f"{component_id}/{local_claim_id}: invalid Finding contributions"
            )
        targets = {
            normalized_text(findings_by_id[doc_id].get("target_gene"))
            for doc_id in finding_doc_ids
        }
        if len(targets) < 2:
            raise ValueError(
                f"{component_id}/{local_claim_id}: requires two target genes"
            )
        roles = {str(row.get("role") or "") for row in contributions}
        if not roles.issubset(CONTRIBUTION_ROLES) or "ANCHORS" not in roles:
            raise ValueError(
                f"{component_id}/{local_claim_id}: invalid roles or missing ANCHORS"
            )
        if normalized_text(claim.get("statement")) in source_summaries:
            raise ValueError(
                f"{component_id}/{local_claim_id}: copies a Finding summary"
            )

    rejections = result.get("rejected_proposals") or []
    rejected_ids = [str(row.get("proposal_id") or "") for row in rejections]
    if len(rejected_ids) != len(set(rejected_ids)):
        raise ValueError(f"{component_id}: duplicate proposal rejections")
    rejected = set(rejected_ids)
    used = set(proposal_claims)
    if (
        not rejected.issubset(allowed_proposals)
        or used & rejected
        or used | rejected != allowed_proposals
    ):
        raise ValueError(
            f"{component_id}: proposals must be used or rejected exactly once"
        )

    dispositions = []
    for proposal_id in sorted(allowed_proposals):
        mapped = sorted(set(proposal_claims.get(proposal_id, ())))
        if proposal_id in rejected:
            disposition = "rejected"
            rationale = next(
                str(row["rationale"])
                for row in rejections
                if str(row["proposal_id"]) == proposal_id
            )
        elif len(mapped) > 1:
            disposition = "split"
            rationale = (
                "The source proposal contributed to multiple atomic canonical Claims."
            )
        elif claim_source_counts[mapped[0]] > 1:
            disposition = "merged"
            rationale = (
                "The source proposal was consolidated with overlapping proposals."
            )
        else:
            disposition = "retained"
            rationale = (
                "The source proposal remained a distinct cross-target Claim."
            )
        dispositions.append(
            {
                "proposal_id": proposal_id,
                "disposition": disposition,
                "resulting_local_claim_ids": mapped,
                "rationale": rationale,
            }
        )
    return {
        "schema_version": CONSOLIDATION_VERSION,
        "component_id": component_id,
        "claims": [dict(row) for row in claims],
        "rejected_proposals": [dict(row) for row in rejections],
        "proposal_dispositions": dispositions,
    }


def validate_consolidation_batch(
    batch: Mapping[str, Any],
    result: Mapping[str, Any],
    proposals_by_id: Mapping[str, Mapping[str, Any]],
    findings_by_id: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    if result.get("batch_id") != batch["batch_id"]:
        raise ValueError("consolidation batch_id mismatch")
    expected = {
        str(row["component_id"]): row for row in batch["components"]
    }
    result_rows = result.get("component_results") or []
    result_ids = [str(row.get("component_id") or "") for row in result_rows]
    if (
        not all(result_ids)
        or len(result_ids) != len(set(result_ids))
        or set(result_ids) != set(expected)
    ):
        raise ValueError(
            "consolidation batch must return every component exactly once"
        )
    validated = [
        validate_consolidation_component(
            expected[component_id],
            row,
            proposals_by_id,
            findings_by_id,
        )
        for component_id, row in (
            (str(row["component_id"]), row) for row in result_rows
        )
    ]
    return {
        "schema_version": CONSOLIDATION_VERSION,
        "batch_id": batch["batch_id"],
        "component_results": validated,
    }


def consolidation_cache_metadata(
    batch: Mapping[str, Any],
    *,
    prompt: str,
    findings_sha256: str,
    induction_results_sha256: str,
    proposals_sha256: str,
    components_sha256: str,
    response_schema_sha256: str,
    model: str,
    reasoning_effort: str,
) -> dict[str, Any]:
    batch_source = [
        {
            "component_id": component["component_id"],
            "proposal_ids": component["proposal_ids"],
            "finding_doc_ids": component["finding_doc_ids"],
        }
        for component in batch["components"]
    ]
    return {
        "consolidation_version": CONSOLIDATION_VERSION,
        "prompt_id": CONSOLIDATION_PROMPT_ID,
        "prompt_template_sha256": CONSOLIDATION_PROMPT_SHA256,
        "output_schema_id": CONSOLIDATION_OUTPUT_SCHEMA_ID,
        "output_schema_source_sha256": CONSOLIDATION_OUTPUT_SCHEMA_SHA256,
        "batch_id": batch["batch_id"],
        "batch_source_sha256": text_sha256(canonical_json(batch_source)),
        "findings_sha256": findings_sha256,
        "induction_results_sha256": induction_results_sha256,
        "proposals_sha256": proposals_sha256,
        "components_sha256": components_sha256,
        "prompt_sha256": text_sha256(prompt),
        "response_schema_sha256": response_schema_sha256,
        "model": model,
        "reasoning_effort": reasoning_effort,
    }


def consolidation_component_cache_metadata(
    component: Mapping[str, Any],
    *,
    findings_sha256: str,
    induction_results_sha256: str,
    proposals_sha256: str,
    response_schema_sha256: str,
    model: str,
    reasoning_effort: str,
) -> dict[str, Any]:
    component_source = {
        "component_id": component["component_id"],
        "proposal_ids": component["proposal_ids"],
        "finding_doc_ids": component["finding_doc_ids"],
    }
    return {
        "consolidation_version": CONSOLIDATION_VERSION,
        "prompt_id": CONSOLIDATION_PROMPT_ID,
        "prompt_template_sha256": CONSOLIDATION_PROMPT_SHA256,
        "output_schema_id": CONSOLIDATION_OUTPUT_SCHEMA_ID,
        "output_schema_source_sha256": CONSOLIDATION_OUTPUT_SCHEMA_SHA256,
        "component_id": component["component_id"],
        "component_source_sha256": text_sha256(canonical_json(component_source)),
        "findings_sha256": findings_sha256,
        "induction_results_sha256": induction_results_sha256,
        "proposals_sha256": proposals_sha256,
        "response_schema_sha256": response_schema_sha256,
        "model": model,
        "reasoning_effort": reasoning_effort,
    }


def materialize_component_results(
    validated_batch: Mapping[str, Any],
    results_dir: Path,
    metadata_by_component_id: Mapping[str, Mapping[str, Any]],
) -> None:
    for result in validated_batch["component_results"]:
        component_id = str(result["component_id"])
        stem = component_id.removeprefix("proposal-component:")
        write_json(results_dir / f"{stem}.json", result)
        write_json(
            results_dir / f"{stem}.meta.json",
            metadata_by_component_id[component_id],
        )


def run_consolidation_batch(
    batch: Mapping[str, Any],
    *,
    proposals_by_id: Mapping[str, Mapping[str, Any]],
    findings_by_id: Mapping[str, Mapping[str, Any]],
    findings_sha256: str,
    induction_results_sha256: str,
    proposals_sha256: str,
    components_sha256: str,
    results_dir: Path,
    batch_results_dir: Path,
    schema_path: Path,
    model: str,
    reasoning_effort: str,
    codex: str,
    timeout_seconds: int,
    overwrite: bool,
    repository: Path,
) -> tuple[str, str]:
    batch_id = str(batch["batch_id"])
    stem = batch_id.removeprefix("consolidation-batch:")
    output = batch_results_dir / f"{stem}.json"
    metadata_path = batch_results_dir / f"{stem}.meta.json"
    log = batch_results_dir / f"{stem}.log"
    prompt = consolidation_prompt(
        batch["components"], proposals_by_id, findings_by_id
    )
    expected_metadata = consolidation_cache_metadata(
        batch,
        prompt=prompt,
        findings_sha256=findings_sha256,
        induction_results_sha256=induction_results_sha256,
        proposals_sha256=proposals_sha256,
        components_sha256=components_sha256,
        response_schema_sha256=sha256(schema_path),
        model=model,
        reasoning_effort=reasoning_effort,
    )
    component_metadata = {
        str(component["component_id"]): consolidation_component_cache_metadata(
            component,
            findings_sha256=findings_sha256,
            induction_results_sha256=induction_results_sha256,
            proposals_sha256=proposals_sha256,
            response_schema_sha256=sha256(schema_path),
            model=model,
            reasoning_effort=reasoning_effort,
        )
        for component in batch["components"]
    }
    if output.is_file() and metadata_path.is_file() and not overwrite:
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            parsed = json.loads(output.read_text(encoding="utf-8"))
            if metadata != expected_metadata:
                raise ValueError("cache fingerprint mismatch")
            validated = validate_consolidation_batch(
                batch, parsed, proposals_by_id, findings_by_id
            )
            materialize_component_results(
                validated, results_dir, component_metadata
            )
            return batch_id, "cached"
        except (OSError, ValueError, json.JSONDecodeError):
            pass

    expected_components = {
        str(component["component_id"]): component
        for component in batch["components"]
    }
    if output.is_file() and not overwrite:
        try:
            partial = json.loads(output.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            partial = {}
        if partial.get("batch_id") == batch_id:
            seen_partial: set[str] = set()
            for row in partial.get("component_results") or []:
                component_id = str(row.get("component_id") or "")
                if (
                    component_id not in expected_components
                    or component_id in seen_partial
                ):
                    continue
                seen_partial.add(component_id)
                try:
                    validated_component = validate_consolidation_component(
                        expected_components[component_id],
                        row,
                        proposals_by_id,
                        findings_by_id,
                    )
                except ValueError:
                    continue
                materialize_component_results(
                    {"component_results": [validated_component]},
                    results_dir,
                    component_metadata,
                )

    if not overwrite:
        cached_components = []
        for component in batch["components"]:
            component_id = str(component["component_id"])
            stem = component_id.removeprefix("proposal-component:")
            component_output = results_dir / f"{stem}.json"
            component_meta = results_dir / f"{stem}.meta.json"
            try:
                metadata = json.loads(component_meta.read_text(encoding="utf-8"))
                parsed_component = json.loads(
                    component_output.read_text(encoding="utf-8")
                )
                if metadata != component_metadata[component_id]:
                    raise ValueError("component cache fingerprint mismatch")
                cached_components.append(
                    validate_consolidation_component(
                        component,
                        parsed_component,
                        proposals_by_id,
                        findings_by_id,
                    )
                )
            except (OSError, ValueError, json.JSONDecodeError):
                break
        else:
            validated = {
                "schema_version": CONSOLIDATION_VERSION,
                "batch_id": batch_id,
                "component_results": cached_components,
            }
            write_json(output, validated)
            write_json(metadata_path, expected_metadata)
            return batch_id, "component-cached"

    command = [
        codex,
        "exec",
        "--ephemeral",
        "--ignore-user-config",
        "--skip-git-repo-check",
        "--sandbox",
        "read-only",
        "--model",
        model,
        "--config",
        f'model_reasoning_effort="{reasoning_effort}"',
        "--output-schema",
        str(schema_path),
        "--output-last-message",
        str(output),
        "-",
    ]
    try:
        completed = subprocess.run(
            command,
            input=prompt,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=repository,
            env=os.environ.copy(),
            check=False,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        log.write_text(str(exc.stdout or ""), encoding="utf-8")
        raise RuntimeError(
            f"{batch_id}: Codex timeout after {timeout_seconds}s"
        ) from exc
    log.write_text(completed.stdout or "", encoding="utf-8")
    if completed.returncode != 0:
        raise RuntimeError(f"{batch_id}: Codex exit {completed.returncode}")
    try:
        parsed = json.loads(output.read_text(encoding="utf-8"))
        validated = validate_consolidation_batch(
            batch, parsed, proposals_by_id, findings_by_id
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"{batch_id}: invalid result: {exc}") from exc
    materialize_component_results(validated, results_dir, component_metadata)
    write_json(metadata_path, expected_metadata)
    return batch_id, "consolidated"


def consolidation_plan_record(batch: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": CONSOLIDATION_VERSION,
        "batch_id": batch["batch_id"],
        "component_ids": [
            row["component_id"] for row in batch["components"]
        ],
        "component_count": len(batch["components"]),
        "proposal_count": sum(
            len(row["proposal_ids"]) for row in batch["components"]
        ),
        "finding_count": sum(
            len(row["finding_doc_ids"]) for row in batch["components"]
        ),
        "prompt_characters": batch["prompt_characters"],
        "estimated_prompt_tokens": batch["estimated_prompt_tokens"],
        "oversized_single_component": batch["oversized_single_component"],
    }


def freeze_consolidation_rows(
    component_results: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Assign stable provisional Claim IDs and translate proposal mappings."""

    claims: list[dict[str, Any]] = []
    dispositions: list[dict[str, Any]] = []
    seen_claim_ids: set[str] = set()
    for result in sorted(
        component_results, key=lambda row: str(row["component_id"])
    ):
        component_id = str(result["component_id"])
        local_to_global: dict[str, str] = {}
        for claim in result["claims"]:
            contributions = sorted(
                (dict(row) for row in claim["contributions"]),
                key=lambda row: str(row["finding_doc_id"]),
            )
            identifier = stable_id(
                "claim",
                [
                    normalized_text(claim["statement"]),
                    normalized_text(claim["scope"]),
                    *[
                        str(row["finding_doc_id"])
                        for row in contributions
                    ],
                ],
            )
            if identifier in seen_claim_ids:
                raise ValueError(
                    f"duplicate consolidated Claim ID: {identifier}"
                )
            seen_claim_ids.add(identifier)
            local_claim_id = str(claim["local_claim_id"])
            local_to_global[local_claim_id] = identifier
            claims.append(
                {
                    "schema_version": CONSOLIDATION_VERSION,
                    "claim_id": identifier,
                    "source_component_id": component_id,
                    "source_proposal_ids": sorted(
                        map(str, claim["source_proposal_ids"])
                    ),
                    "statement": claim["statement"],
                    "scope": claim["scope"],
                    "higher_order_basis": claim["higher_order_basis"],
                    "confidence": claim["confidence"],
                    "contributions": contributions,
                }
            )
        for disposition in result["proposal_dispositions"]:
            dispositions.append(
                {
                    "schema_version": CONSOLIDATION_VERSION,
                    "proposal_id": disposition["proposal_id"],
                    "source_component_id": component_id,
                    "disposition": disposition["disposition"],
                    "resulting_claim_ids": [
                        local_to_global[local_claim_id]
                        for local_claim_id in disposition[
                            "resulting_local_claim_ids"
                        ]
                    ],
                    "rationale": disposition["rationale"],
                }
            )
    return (
        sorted(claims, key=lambda row: str(row["claim_id"])),
        sorted(dispositions, key=lambda row: str(row["proposal_id"])),
    )


def apply_coverage_attachments(
    batch_results_dir: Path,
    attachments: Sequence[str],
    components: Sequence[Mapping[str, Any]],
    proposals_by_id: Mapping[str, Mapping[str, Any]],
    findings_by_id: Mapping[str, Mapping[str, Any]],
) -> int:
    """Apply explicit proposal-to-Claim repair decisions to raw batch outputs."""

    requested: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for attachment in attachments:
        fields = attachment.split(",")
        if len(fields) != 3 or not all(fields):
            raise ValueError(
                "--attach-proposal must be COMPONENT_ID,PROPOSAL_ID,LOCAL_CLAIM_ID"
            )
        component_id, proposal_id, local_claim_id = fields
        requested[component_id].append((proposal_id, local_claim_id))

    components_by_id = {
        str(component["component_id"]): component for component in components
    }
    unknown_components = sorted(set(requested) - set(components_by_id))
    if unknown_components:
        raise ValueError(
            f"coverage attachments reference unknown components: "
            f"{unknown_components[:10]}"
        )

    applied = 0
    pending = set(requested)
    for output in sorted(batch_results_dir.glob("*.json")):
        try:
            parsed = json.loads(output.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        changed = False
        for result in parsed.get("component_results") or []:
            component_id = str(result.get("component_id") or "")
            if component_id not in requested:
                continue
            claims_by_id = {
                str(claim.get("local_claim_id") or ""): claim
                for claim in result.get("claims") or []
            }
            used = {
                str(proposal_id)
                for claim in result.get("claims") or []
                for proposal_id in claim.get("source_proposal_ids") or []
            }
            rejected = {
                str(row.get("proposal_id") or "")
                for row in result.get("rejected_proposals") or []
            }
            for proposal_id, local_claim_id in requested[component_id]:
                if proposal_id not in proposals_by_id:
                    raise ValueError(f"unknown proposal attachment: {proposal_id}")
                if proposal_id in used or proposal_id in rejected:
                    raise ValueError(
                        f"proposal attachment is not uncovered: {proposal_id}"
                    )
                if local_claim_id not in claims_by_id:
                    raise ValueError(
                        f"unknown local Claim attachment: "
                        f"{component_id}/{local_claim_id}"
                    )
                source_ids = claims_by_id[local_claim_id]["source_proposal_ids"]
                source_ids.append(proposal_id)
                source_ids.sort()
                used.add(proposal_id)
                applied += 1
                changed = True
            validate_consolidation_component(
                components_by_id[component_id],
                result,
                proposals_by_id,
                findings_by_id,
            )
            pending.remove(component_id)
        if changed:
            write_json(output, parsed)
    if pending:
        raise ValueError(
            f"coverage attachment components not found in raw outputs: "
            f"{sorted(pending)}"
        )
    return applied


def consolidate_command(args: argparse.Namespace) -> int:
    findings = load_findings(args.findings)
    findings_by_id = {str(row["doc_id"]): row for row in findings}
    induction_results = list(iter_jsonl(args.induction_results))
    proposals = flatten_induction_proposals(induction_results)
    proposals_by_id = {
        str(row["proposal_id"]): row for row in proposals
    }
    components = build_proposal_components(proposals)
    unknown_findings = sorted(
        {
            str(doc_id)
            for component in components
            for doc_id in component["finding_doc_ids"]
            if str(doc_id) not in findings_by_id
        }
    )
    if unknown_findings:
        raise ValueError(
            f"proposal components reference unknown Findings: "
            f"{unknown_findings[:10]}"
        )
    if args.component_id:
        requested_components = set(map(str, args.component_id))
        available_components = {
            str(component["component_id"]) for component in components
        }
        unknown_components = sorted(requested_components - available_components)
        if unknown_components:
            raise ValueError(
                f"unknown proposal components: {unknown_components[:10]}"
            )
        components = [
            component
            for component in components
            if str(component["component_id"]) in requested_components
        ]
    if args.repair_only and not args.component_id:
        raise ValueError("--repair-only requires at least one --component-id")
    if args.attach_proposal and not args.repair_only:
        raise ValueError("--attach-proposal requires --repair-only")

    run_work_dir = args.work_dir
    proposals_output = args.proposals
    components_output = args.components
    batch_plan_output = args.batch_plan
    component_results_output = args.component_results
    claims_output = args.claims
    proposal_dispositions_output = args.proposal_dispositions
    if args.repair_only:
        repair_key = text_sha256(
            canonical_json(sorted(map(str, args.component_id)))
        )[:20]
        run_work_dir = args.work_dir / "repairs" / repair_key
        proposals_output = run_work_dir / "proposals.jsonl"
        components_output = run_work_dir / "components.jsonl"
        batch_plan_output = run_work_dir / "batch_plan.jsonl"
        component_results_output = run_work_dir / "component_results.jsonl"
        claims_output = run_work_dir / "claims.jsonl"
        proposal_dispositions_output = (
            run_work_dir / "proposal_dispositions.jsonl"
        )

    run_work_dir.mkdir(parents=True, exist_ok=True)
    proposal_count, proposals_digest = write_jsonl(proposals_output, proposals)
    component_count, components_digest = write_jsonl(
        components_output, components
    )
    batches = pack_consolidation_batches(
        components,
        proposals_by_id,
        findings_by_id,
        maximum_components_per_call=args.maximum_components_per_call,
        maximum_prompt_characters=args.maximum_prompt_characters,
        maximum_single_component_prompt_characters=(
            args.maximum_single_component_prompt_characters
        ),
    )
    plan_count, plan_digest = write_jsonl(
        batch_plan_output,
        [consolidation_plan_record(batch) for batch in batches],
    )
    prompt_characters = [int(batch["prompt_characters"]) for batch in batches]
    plan_summary = {
        "schema_version": CONSOLIDATION_VERSION,
        "method_assets": {
            "prompt": {
                "id": CONSOLIDATION_PROMPT_ID,
                "sha256": CONSOLIDATION_PROMPT_SHA256,
            },
            "output_schema": {
                "id": CONSOLIDATION_OUTPUT_SCHEMA_ID,
                "sha256": CONSOLIDATION_OUTPUT_SCHEMA_SHA256,
            },
        },
        "source_proposals": proposal_count,
        "proposal_components": component_count,
        "component_sizes": dict(
            sorted(
                Counter(
                    len(component["proposal_ids"])
                    for component in components
                ).items()
            )
        ),
        "model_calls": len(batches),
        "batch_sizes": dict(
            sorted(
                Counter(len(batch["components"]) for batch in batches).items()
            )
        ),
        "oversized_single_component_calls": sum(
            bool(batch["oversized_single_component"]) for batch in batches
        ),
        "prompt_characters": {
            "minimum": min(prompt_characters),
            "maximum": max(prompt_characters),
            "mean": round(
                sum(prompt_characters) / len(prompt_characters), 2
            ),
        },
        "maximum_estimated_prompt_tokens": max(
            int(batch["estimated_prompt_tokens"]) for batch in batches
        ),
        "batch_plan": {
            "path": str(batch_plan_output),
            "records": plan_count,
            "sha256": plan_digest,
        },
    }
    if args.plan_only:
        print(canonical_json(plan_summary))
        return 0

    results_dir = args.work_dir / "component-results"
    results_dir.mkdir(parents=True, exist_ok=True)
    batch_results_dir = run_work_dir / "batch-results"
    batch_results_dir.mkdir(parents=True, exist_ok=True)
    schema_path = run_work_dir / "consolidation-output.schema.json"
    write_json(schema_path, consolidation_output_schema())
    if args.attach_proposal:
        attached = apply_coverage_attachments(
            batch_results_dir,
            args.attach_proposal,
            components,
            proposals_by_id,
            findings_by_id,
        )
        print(
            f"applied {attached} explicit proposal coverage attachments",
            file=sys.stderr,
        )
    repository = Path(__file__).resolve().parents[6]
    findings_digest = sha256(args.findings)
    induction_results_digest = sha256(args.induction_results)
    lock_path = run_work_dir / ".run.lock"
    with lock_path.open("w", encoding="utf-8") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise ValueError(
                f"another Claim consolidation is using {run_work_dir}"
            ) from exc
        lock.write(f"pid={os.getpid()}\n")
        lock.flush()
        failures: list[str] = []
        completed_count = 0
        with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
            futures = {
                pool.submit(
                    run_consolidation_batch,
                    batch,
                    proposals_by_id=proposals_by_id,
                    findings_by_id=findings_by_id,
                    findings_sha256=findings_digest,
                    induction_results_sha256=induction_results_digest,
                    proposals_sha256=proposals_digest,
                    components_sha256=components_digest,
                    results_dir=results_dir,
                    batch_results_dir=batch_results_dir,
                    schema_path=schema_path,
                    model=args.model,
                    reasoning_effort=args.reasoning_effort,
                    codex=args.codex,
                    timeout_seconds=args.timeout_seconds,
                    overwrite=args.overwrite,
                    repository=repository,
                ): batch
                for batch in batches
            }
            for future in as_completed(futures):
                completed_count += 1
                batch = futures[future]
                try:
                    identifier, disposition = future.result()
                    print(
                        f"[{completed_count}/{len(batches)}] "
                        f"{identifier} {disposition}",
                        file=sys.stderr,
                    )
                except Exception as exc:  # noqa: BLE001
                    failures.append(f"{batch['batch_id']}: {exc}")
                    print(
                        f"[{completed_count}/{len(batches)}] {failures[-1]}",
                        file=sys.stderr,
                    )
        if failures:
            raise RuntimeError(
                f"{len(failures)} consolidation batches failed; "
                f"first failures: {failures[:5]}"
            )

    components_by_id = {
        str(row["component_id"]): row for row in components
    }
    component_results = []
    for component in components:
        component_id = str(component["component_id"])
        stem = component_id.removeprefix("proposal-component:")
        parsed = json.loads(
            (results_dir / f"{stem}.json").read_text(encoding="utf-8")
        )
        component_results.append(
            validate_consolidation_component(
                components_by_id[component_id],
                parsed,
                proposals_by_id,
                findings_by_id,
            )
        )
    component_result_count, component_result_digest = write_jsonl(
        component_results_output, component_results
    )
    claims, dispositions = freeze_consolidation_rows(component_results)
    claim_count, claims_digest = write_jsonl(claims_output, claims)
    disposition_count, disposition_digest = write_jsonl(
        proposal_dispositions_output, dispositions
    )
    role_counts = Counter(
        str(contribution["role"])
        for claim in claims
        for contribution in claim["contributions"]
    )
    disposition_counts = Counter(
        str(row["disposition"]) for row in dispositions
    )
    summary = {
        **plan_summary,
        "component_results": {
            "path": str(component_results_output),
            "records": component_result_count,
            "sha256": component_result_digest,
        },
        "claims": {
            "path": str(claims_output),
            "records": claim_count,
            "sha256": claims_digest,
        },
        "proposal_dispositions": {
            "path": str(proposal_dispositions_output),
            "records": disposition_count,
            "sha256": disposition_digest,
            "counts": dict(sorted(disposition_counts.items())),
        },
        "contribution_roles": dict(sorted(role_counts.items())),
        "contribution_edges": sum(role_counts.values()),
        "contributing_findings": len(
            {
                str(contribution["finding_doc_id"])
                for claim in claims
                for contribution in claim["contributions"]
            }
        ),
    }
    print(canonical_json(summary))
    return 0


def require_freeze_text(
    row: Mapping[str, Any],
    field: str,
    *,
    location: str,
) -> str:
    value = row.get(field)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{location}: {field} must be a non-empty string")
    return value


def normalized_frozen_contributions(
    rows: Sequence[Mapping[str, Any]],
    findings_by_id: Mapping[str, Mapping[str, Any]],
    *,
    location: str,
    allowed_findings: set[str] | None = None,
    require_cross_target: bool = True,
) -> list[dict[str, str]]:
    contributions = []
    seen: set[str] = set()
    for index, row in enumerate(rows):
        item_location = f"{location}/contributions/{index}"
        finding_doc_id = require_freeze_text(
            row, "finding_doc_id", location=item_location
        )
        role = require_freeze_text(row, "role", location=item_location)
        rationale = require_freeze_text(
            row, "rationale", location=item_location
        )
        if finding_doc_id not in findings_by_id:
            raise ValueError(
                f"{item_location}: unknown Finding {finding_doc_id!r}"
            )
        if allowed_findings is not None and finding_doc_id not in allowed_findings:
            raise ValueError(
                f"{item_location}: Finding is outside the source neighborhood"
            )
        if finding_doc_id in seen:
            raise ValueError(
                f"{location}: duplicate Finding contribution {finding_doc_id!r}"
            )
        if role not in CONTRIBUTION_ROLES:
            raise ValueError(f"{item_location}: invalid contribution role {role!r}")
        seen.add(finding_doc_id)
        contributions.append(
            {
                "finding_doc_id": finding_doc_id,
                "rationale": rationale,
                "role": role,
            }
        )
    targets = {
        str(findings_by_id[row["finding_doc_id"]]["target_gene"])
        for row in contributions
    }
    roles = {row["role"] for row in contributions}
    if len(contributions) < 2 or (require_cross_target and len(targets) < 2):
        raise ValueError(
            f"{location}: Claim content requires two Findings from two targets"
        )
    if "ANCHORS" not in roles:
        raise ValueError(f"{location}: Claim content requires an ANCHORS role")
    return sorted(contributions, key=lambda row: row["finding_doc_id"])


def frozen_file_record(
    path: Path,
    release_root: Path,
    records: int,
) -> dict[str, Any]:
    return {
        "bytes": path.stat().st_size,
        "path": release_relative_path(path, release_root),
        "records": records,
        "sha256": sha256(path),
    }


def require_consolidation_version(
    rows: Sequence[Mapping[str, Any]], *, label: str
) -> None:
    versions = {str(row.get("schema_version") or "") for row in rows}
    if versions != {CONSOLIDATION_VERSION}:
        raise ValueError(
            f"{label} must use {CONSOLIDATION_VERSION}; found {sorted(versions)}"
        )


def freeze_command(args: argparse.Namespace) -> int:
    """Validate and freeze the accepted Claim construction and final ledgers."""

    release_root = Path(__file__).resolve().parents[1]
    findings = load_findings(args.findings)
    findings_by_id = {str(row["doc_id"]): row for row in findings}
    raw_neighborhoods = list(iter_jsonl(args.neighborhoods))
    raw_proposals = list(iter_jsonl(args.proposals))
    raw_claims = list(iter_jsonl(args.claims))
    raw_proposal_dispositions = list(iter_jsonl(args.proposal_dispositions))
    require_consolidation_version(raw_proposals, label="raw proposals")
    require_consolidation_version(raw_claims, label="raw Claims")
    require_consolidation_version(
        raw_proposal_dispositions, label="raw proposal dispositions"
    )

    frozen_neighborhoods = []
    neighborhood_ids: set[str] = set()
    neighborhood_counts: Counter[str] = Counter()
    for row in sorted(
        raw_neighborhoods, key=lambda item: str(item.get("neighborhood_id") or "")
    ):
        identifier = require_freeze_text(
            row, "neighborhood_id", location="neighborhood"
        )
        if identifier in neighborhood_ids:
            raise ValueError(f"duplicate neighborhood ID: {identifier}")
        neighborhood_ids.add(identifier)
        finding_doc_ids = sorted(map(str, row.get("finding_doc_ids") or []))
        if (
            len(finding_doc_ids) < 2
            or len(finding_doc_ids) != len(set(finding_doc_ids))
        ):
            raise ValueError(f"{identifier}: invalid Finding membership")
        unknown = sorted(set(finding_doc_ids) - set(findings_by_id))
        if unknown:
            raise ValueError(f"{identifier}: unknown Findings: {unknown[:10]}")
        neighborhood_counts.update(finding_doc_ids)
        frozen_neighborhoods.append(
            {
                "schema_version": FROZEN_NEIGHBORHOOD_VERSION,
                "construction_scope": "corpus",
                "neighborhood_id": identifier,
                "finding_doc_ids": finding_doc_ids,
                "seed_pair_ids": sorted(map(str, row.get("seed_pair_ids") or [])),
                "retrieval_lanes": sorted(map(str, row.get("retrieval_lanes") or [])),
                "contains_one_sided_seed": bool(
                    row.get("contains_one_sided_seed")
                ),
            }
        )

    frozen_proposals = []
    proposals_by_id: dict[str, dict[str, Any]] = {}
    for row in sorted(
        raw_proposals, key=lambda item: str(item.get("proposal_id") or "")
    ):
        identifier = require_freeze_text(row, "proposal_id", location="proposal")
        if identifier in proposals_by_id:
            raise ValueError(f"duplicate proposal ID: {identifier}")
        source_neighborhood_id = require_freeze_text(
            row, "source_neighborhood_id", location=identifier
        )
        if source_neighborhood_id not in neighborhood_ids:
            raise ValueError(
                f"{identifier}: unknown neighborhood {source_neighborhood_id!r}"
            )
        neighborhood = next(
            item
            for item in frozen_neighborhoods
            if item["neighborhood_id"] == source_neighborhood_id
        )
        contributions = normalized_frozen_contributions(
            row.get("contributions") or [],
            findings_by_id,
            location=identifier,
            allowed_findings=set(neighborhood["finding_doc_ids"]),
            require_cross_target=False,
        )
        proposal = {
            "schema_version": FROZEN_PROPOSAL_VERSION,
            "construction_scope": "corpus",
            "proposal_id": identifier,
            "source_neighborhood_id": source_neighborhood_id,
            "source_local_claim_id": require_freeze_text(
                row, "source_local_claim_id", location=identifier
            ),
            "statement": require_freeze_text(
                row, "statement", location=identifier
            ),
            "scope": require_freeze_text(row, "scope", location=identifier),
            "higher_order_basis": require_freeze_text(
                row, "higher_order_basis", location=identifier
            ),
            "confidence": require_freeze_text(
                row, "confidence", location=identifier
            ),
            "contributions": contributions,
        }
        if proposal["confidence"] not in {"high", "moderate", "low"}:
            raise ValueError(f"{identifier}: invalid confidence")
        proposals_by_id[identifier] = proposal
        frozen_proposals.append(proposal)

    proposal_component_by_id = {
        proposal_id: str(component["component_id"])
        for component in build_proposal_components(frozen_proposals)
        for proposal_id in component["proposal_ids"]
    }

    frozen_claims = []
    frozen_contributions = []
    claims_by_id: dict[str, dict[str, Any]] = {}
    statement_signatures: set[str] = set()
    proposal_to_claims: dict[str, set[str]] = defaultdict(set)
    finding_to_claims: dict[str, set[str]] = defaultdict(set)
    finding_to_roles: dict[str, set[str]] = defaultdict(set)
    for row in sorted(raw_claims, key=lambda item: str(item.get("claim_id") or "")):
        claim_id = require_freeze_text(row, "claim_id", location="Claim")
        if claim_id in claims_by_id:
            raise ValueError(f"duplicate Claim ID: {claim_id}")
        statement = require_freeze_text(row, "statement", location=claim_id)
        signature = normalized_text(statement)
        if signature in statement_signatures:
            raise ValueError(f"{claim_id}: duplicate normalized Claim statement")
        statement_signatures.add(signature)
        source_proposal_ids = sorted(map(str, row.get("source_proposal_ids") or []))
        if (
            not source_proposal_ids
            or len(source_proposal_ids) != len(set(source_proposal_ids))
            or not set(source_proposal_ids).issubset(proposals_by_id)
        ):
            raise ValueError(f"{claim_id}: invalid source proposals")
        contributions = normalized_frozen_contributions(
            row.get("contributions") or [],
            findings_by_id,
            location=claim_id,
        )
        target_genes = sorted(
            {
                str(findings_by_id[item["finding_doc_id"]]["target_gene"])
                for item in contributions
            }
        )
        source_component_id = require_freeze_text(
            row, "source_component_id", location=claim_id
        )
        source_components = {
            proposal_component_by_id[proposal_id]
            for proposal_id in source_proposal_ids
        }
        if source_components != {source_component_id}:
            raise ValueError(
                f"{claim_id}: source proposals do not match source component"
            )
        claim = {
            "schema_version": FROZEN_CLAIM_VERSION,
            "claim_scope": "corpus",
            "construction_scope": "corpus",
            "claim_id": claim_id,
            "statement": statement,
            "scope": require_freeze_text(row, "scope", location=claim_id),
            "higher_order_basis": require_freeze_text(
                row, "higher_order_basis", location=claim_id
            ),
            "confidence": require_freeze_text(
                row, "confidence", location=claim_id
            ),
            "source_component_id": source_component_id,
            "source_proposal_ids": source_proposal_ids,
            "target_genes": target_genes,
            "contribution_count": len(contributions),
        }
        if claim["confidence"] not in {"high", "moderate", "low"}:
            raise ValueError(f"{claim_id}: invalid confidence")
        claims_by_id[claim_id] = claim
        frozen_claims.append(claim)
        for proposal_id in source_proposal_ids:
            proposal_to_claims[proposal_id].add(claim_id)
        for item in contributions:
            finding_doc_id = item["finding_doc_id"]
            finding = findings_by_id[finding_doc_id]
            finding_to_claims[finding_doc_id].add(claim_id)
            finding_to_roles[finding_doc_id].add(item["role"])
            frozen_contributions.append(
                {
                    "schema_version": FROZEN_CONTRIBUTION_VERSION,
                    "contribution_id": stable_id(
                        "claim-contribution", [claim_id, finding_doc_id]
                    ),
                    "claim_id": claim_id,
                    "claim_scope": "corpus",
                    "finding_doc_id": finding_doc_id,
                    "target_gene": str(finding["target_gene"]),
                    "finding_id": str(finding["finding_id"]),
                    "role": item["role"],
                    "rationale": item["rationale"],
                }
            )

    frozen_contributions.sort(key=lambda row: row["contribution_id"])
    contribution_ids = [row["contribution_id"] for row in frozen_contributions]
    if len(contribution_ids) != len(set(contribution_ids)):
        raise ValueError("duplicate frozen Claim contribution IDs")

    frozen_proposal_dispositions = []
    disposition_ids: set[str] = set()
    for row in sorted(
        raw_proposal_dispositions,
        key=lambda item: str(item.get("proposal_id") or ""),
    ):
        proposal_id = require_freeze_text(
            row, "proposal_id", location="proposal disposition"
        )
        if proposal_id not in proposals_by_id or proposal_id in disposition_ids:
            raise ValueError(
                f"invalid or duplicate proposal disposition: {proposal_id}"
            )
        disposition_ids.add(proposal_id)
        source_component_id = require_freeze_text(
            row, "source_component_id", location=proposal_id
        )
        if source_component_id != proposal_component_by_id[proposal_id]:
            raise ValueError(f"{proposal_id}: source component mismatch")
        resulting_claim_ids = sorted(
            map(str, row.get("resulting_claim_ids") or [])
        )
        if (
            len(resulting_claim_ids) != len(set(resulting_claim_ids))
            or not set(resulting_claim_ids).issubset(claims_by_id)
            or set(resulting_claim_ids) != proposal_to_claims.get(proposal_id, set())
        ):
            raise ValueError(
                f"{proposal_id}: disposition does not match final Claims"
            )
        disposition = require_freeze_text(
            row, "disposition", location=proposal_id
        )
        if disposition not in {"merged", "retained", "split", "rejected"}:
            raise ValueError(f"{proposal_id}: invalid disposition {disposition!r}")
        if (disposition == "rejected") != (not resulting_claim_ids):
            raise ValueError(f"{proposal_id}: rejected/resulting Claim mismatch")
        frozen_proposal_dispositions.append(
            {
                "schema_version": FROZEN_PROPOSAL_DISPOSITION_VERSION,
                "construction_scope": "corpus",
                "claim_scope": "corpus",
                "proposal_id": proposal_id,
                "source_component_id": source_component_id,
                "disposition": disposition,
                "resulting_claim_ids": resulting_claim_ids,
                "rationale": require_freeze_text(
                    row, "rationale", location=proposal_id
                ),
            }
        )
    if disposition_ids != set(proposals_by_id):
        missing = sorted(set(proposals_by_id) - disposition_ids)
        raise ValueError(f"proposal dispositions are incomplete: {missing[:10]}")

    frozen_finding_dispositions = []
    for finding in findings:
        finding_doc_id = str(finding["doc_id"])
        claim_ids = sorted(finding_to_claims.get(finding_doc_id, set()))
        if claim_ids:
            disposition = "contributed"
        elif neighborhood_counts[finding_doc_id]:
            disposition = "considered_no_contribution"
        else:
            disposition = "not_in_candidate_neighborhood"
        frozen_finding_dispositions.append(
            {
                "schema_version": FROZEN_FINDING_DISPOSITION_VERSION,
                "finding_doc_id": finding_doc_id,
                "target_gene": str(finding["target_gene"]),
                "finding_id": str(finding["finding_id"]),
                "disposition": disposition,
                "claim_ids": claim_ids,
                "contribution_roles": sorted(
                    finding_to_roles.get(finding_doc_id, set())
                ),
                "neighborhood_count": neighborhood_counts[finding_doc_id],
            }
        )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "neighborhoods": (
            args.output_dir / "neighborhoods.jsonl",
            frozen_neighborhoods,
        ),
        "proposals": (args.output_dir / "proposals.jsonl", frozen_proposals),
        "proposal_dispositions": (
            args.output_dir / "proposal_dispositions.jsonl",
            frozen_proposal_dispositions,
        ),
        "claims": (args.output_dir / "claims.jsonl", frozen_claims),
        "contributions": (
            args.output_dir / "contributions.jsonl",
            frozen_contributions,
        ),
        "finding_dispositions": (
            args.output_dir / "finding_dispositions.jsonl",
            frozen_finding_dispositions,
        ),
    }
    output_records = {}
    for name, (path, rows) in outputs.items():
        count, _ = write_jsonl(path, rows)
        output_records[name] = frozen_file_record(path, release_root, count)

    role_counts = Counter(row["role"] for row in frozen_contributions)
    proposal_disposition_counts = Counter(
        row["disposition"] for row in frozen_proposal_dispositions
    )
    finding_disposition_counts = Counter(
        row["disposition"] for row in frozen_finding_dispositions
    )
    build_record = {
        "schema_version": FROZEN_BUILD_VERSION,
        "versions": {
            "neighborhoods": SCHEMA_VERSION,
            "induction": INDUCTION_VERSION,
            "consolidation": CONSOLIDATION_VERSION,
        },
        "source": frozen_file_record(args.findings, release_root, len(findings)),
        "inputs": {
            "neighborhoods": frozen_file_record(
                args.neighborhoods, release_root, len(raw_neighborhoods)
            ),
            "proposals": frozen_file_record(
                args.proposals, release_root, len(raw_proposals)
            ),
            "claims": frozen_file_record(args.claims, release_root, len(raw_claims)),
            "proposal_dispositions": frozen_file_record(
                args.proposal_dispositions,
                release_root,
                len(raw_proposal_dispositions),
            ),
        },
        "outputs": output_records,
        "counts": {
            "findings": len(findings),
            "candidate_findings": len(neighborhood_counts),
            "neighborhoods": len(frozen_neighborhoods),
            "proposals": len(frozen_proposals),
            "claims": len(frozen_claims),
            "contributions": len(frozen_contributions),
            "contributing_findings": len(finding_to_claims),
            "contributing_targets": len(
                {
                    row["target_gene"]
                    for row in frozen_contributions
                }
            ),
            "claim_confidences": dict(
                sorted(Counter(row["confidence"] for row in frozen_claims).items())
            ),
            "contribution_roles": dict(sorted(role_counts.items())),
            "proposal_dispositions": dict(
                sorted(proposal_disposition_counts.items())
            ),
            "finding_dispositions": dict(
                sorted(finding_disposition_counts.items())
            ),
        },
        "model_provenance": {
            "induction": {
                "model": args.induction_model,
                "reasoning_effort": args.induction_reasoning_effort,
                "inference_calls": args.induction_inference_calls,
            },
            "consolidation": {
                "model": args.consolidation_model,
                "reasoning_effort": args.consolidation_reasoning_effort,
                "inference_calls": args.consolidation_inference_calls,
            },
            "total_inference_calls": (
                args.induction_inference_calls + args.consolidation_inference_calls
            ),
        },
        "method_assets": {
            "consolidation_prompt": {
                "id": CONSOLIDATION_PROMPT_ID,
                "sha256": CONSOLIDATION_PROMPT_SHA256,
            },
            "consolidation_output_schema": {
                "id": CONSOLIDATION_OUTPUT_SCHEMA_ID,
                "sha256": CONSOLIDATION_OUTPUT_SCHEMA_SHA256,
            },
        },
        "build_policy": {
            "biological_findings_only": True,
            "null_findings": False,
            "program_extraction": False,
            "concept_extraction": False,
            "claim_centric_attachment": False,
            "disconnected_semantic_merge": False,
            "freeze_model_calls": False,
            "projection_model_calls": False,
        },
    }
    write_json(args.build_record, build_record)
    print(canonical_json(build_record))
    return 0


def evaluate_results(
    neighborhoods: Sequence[Mapping[str, Any]],
    results: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    neighborhood_by_id = {
        str(row["neighborhood_id"]): row for row in neighborhoods
    }
    role_counts: Counter[str] = Counter()
    disposition_counts: Counter[str] = Counter()
    statements: list[str] = []
    cross_target_claims = 0
    proposal_count = 0
    contribution_edges = 0
    for result in results:
        neighborhood = neighborhood_by_id[str(result["neighborhood_id"])]
        target_by_doc = {
            doc_id: doc_id.split(":", 1)[0]
            for doc_id in neighborhood["finding_doc_ids"]
        }
        for claim in result.get("claims") or []:
            proposal_count += 1
            statements.append(normalized_text(claim["statement"]))
            contribution_edges += len(claim["contributions"])
            roles = [str(item["role"]) for item in claim["contributions"]]
            role_counts.update(roles)
            targets = {
                target_by_doc[str(item["finding_doc_id"])]
                for item in claim["contributions"]
            }
            if len(targets) > 1:
                cross_target_claims += 1
        disposition_counts.update(
            str(item["disposition"])
            for item in result.get("finding_dispositions") or []
        )
    duplicate_statement_count = sum(
        count - 1 for count in Counter(statements).values() if count > 1
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "evaluated_neighborhoods": len(results),
        "claim_proposals": proposal_count,
        "cross_target_claim_proposals": cross_target_claims,
        "contribution_edges": contribution_edges,
        "contribution_roles": dict(sorted(role_counts.items())),
        "finding_dispositions": dict(sorted(disposition_counts.items())),
        "exact_duplicate_statements": duplicate_statement_count,
        "warning": (
            "Pilot proposals overlap and are not frozen Claims; semantic global "
            "consolidation and corpus-wide attachment remain required."
        ),
    }


def evaluate_command(args: argparse.Namespace) -> int:
    neighborhoods = list(iter_jsonl(args.neighborhoods))
    results = list(iter_jsonl(args.results))
    report = evaluate_results(neighborhoods, results)
    if args.output:
        write_json(args.output, report)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def parser() -> argparse.ArgumentParser:
    release_root = Path(__file__).resolve().parents[1]
    findings = release_root / "artifacts" / "ledgers" / "findings.jsonl"
    work = release_root / "_work" / "claims"
    consolidation_work = work / "consolidation"
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command", required=True)

    prepare = commands.add_parser("prepare", help="build global overlapping neighborhoods")
    prepare.add_argument("--findings", type=Path, default=findings)
    prepare.add_argument("--pairs", type=Path, default=work / "candidate_pairs.jsonl")
    prepare.add_argument("--neighborhoods", type=Path, default=work / "neighborhoods.jsonl")
    prepare.add_argument("--build-record", type=Path, default=work / "neighborhood_build.json")
    prepare.add_argument("--neighbors-per-finding", type=int, default=3)
    prepare.add_argument("--semantic-minimum-score", type=float, default=0.32)
    prepare.add_argument("--one-sided-minimum-score", type=float, default=0.16)
    prepare.add_argument("--maximum-feature-frequency", type=int, default=96)
    prepare.add_argument("--maximum-findings", type=int, default=6)
    prepare.set_defaults(function=prepare_command)

    run = commands.add_parser("run", help="induce Claim proposals in selected neighborhoods")
    run.add_argument("--findings", type=Path, default=findings)
    run.add_argument("--neighborhoods", type=Path, default=work / "neighborhoods.jsonl")
    run.add_argument("--work-dir", type=Path, default=work)
    run.add_argument("--batch-plan", type=Path, default=work / "batch_plan.jsonl")
    run.add_argument("--results", type=Path, default=work / "pilot_results.jsonl")
    run.add_argument("--model", default="gpt-5.5")
    run.add_argument("--reasoning-effort", default="low")
    run.add_argument("--workers", type=int, default=4)
    run.add_argument("--timeout-seconds", type=int, default=900)
    run.add_argument(
        "--maximum-neighborhoods-per-call",
        type=int,
        default=DEFAULT_MAX_NEIGHBORHOODS_PER_CALL,
    )
    run.add_argument(
        "--maximum-prompt-characters",
        type=int,
        default=DEFAULT_MAX_PROMPT_CHARACTERS,
    )
    run.add_argument(
        "--maximum-neighborhood-similarity",
        type=float,
        default=DEFAULT_MAX_NEIGHBORHOOD_SIMILARITY,
    )
    run.add_argument("--limit", type=int, default=0)
    run.add_argument("--neighborhood-id", action="append", default=[])
    run.add_argument("--contains", action="append", default=[])
    run.add_argument("--codex", default="codex")
    run.add_argument("--plan-only", action="store_true")
    run.add_argument("--overwrite", action="store_true")
    run.set_defaults(function=run_batched_command)

    consolidate = commands.add_parser(
        "consolidate",
        help="consolidate overlapping proposals into provisional Claims",
    )
    consolidate.add_argument("--findings", type=Path, default=findings)
    consolidate.add_argument(
        "--induction-results",
        type=Path,
        default=work / "pilot_results.jsonl",
    )
    consolidate.add_argument("--work-dir", type=Path, default=consolidation_work)
    consolidate.add_argument(
        "--proposals",
        type=Path,
        default=consolidation_work / "proposals.jsonl",
    )
    consolidate.add_argument(
        "--components",
        type=Path,
        default=consolidation_work / "components.jsonl",
    )
    consolidate.add_argument(
        "--batch-plan",
        type=Path,
        default=consolidation_work / "batch_plan.jsonl",
    )
    consolidate.add_argument(
        "--component-results",
        type=Path,
        default=consolidation_work / "component_results.jsonl",
    )
    consolidate.add_argument(
        "--claims",
        type=Path,
        default=consolidation_work / "claims.jsonl",
    )
    consolidate.add_argument(
        "--proposal-dispositions",
        type=Path,
        default=consolidation_work / "proposal_dispositions.jsonl",
    )
    consolidate.add_argument("--model", default="gpt-rosalind-5.5")
    consolidate.add_argument("--reasoning-effort", default="high")
    consolidate.add_argument("--workers", type=int, default=8)
    consolidate.add_argument("--timeout-seconds", type=int, default=900)
    consolidate.add_argument(
        "--maximum-components-per-call",
        type=int,
        default=DEFAULT_MAX_COMPONENTS_PER_CALL,
    )
    consolidate.add_argument(
        "--maximum-prompt-characters",
        type=int,
        default=DEFAULT_MAX_CONSOLIDATION_PROMPT_CHARACTERS,
    )
    consolidate.add_argument(
        "--maximum-single-component-prompt-characters",
        type=int,
        default=DEFAULT_MAX_SINGLE_COMPONENT_PROMPT_CHARACTERS,
    )
    consolidate.add_argument("--codex", default="codex")
    consolidate.add_argument("--component-id", action="append", default=[])
    consolidate.add_argument("--repair-only", action="store_true")
    consolidate.add_argument("--attach-proposal", action="append", default=[])
    consolidate.add_argument("--plan-only", action="store_true")
    consolidate.add_argument("--overwrite", action="store_true")
    consolidate.set_defaults(function=consolidate_command)

    freeze = commands.add_parser(
        "freeze",
        help="validate and freeze accepted Claim artifacts without model calls",
    )
    freeze.add_argument("--findings", type=Path, default=findings)
    freeze.add_argument(
        "--neighborhoods",
        type=Path,
        default=work / "neighborhoods.jsonl",
    )
    freeze.add_argument(
        "--proposals",
        type=Path,
        default=consolidation_work / "proposals.jsonl",
    )
    freeze.add_argument(
        "--claims",
        type=Path,
        default=consolidation_work / "claims.jsonl",
    )
    freeze.add_argument(
        "--proposal-dispositions",
        type=Path,
        default=consolidation_work / "proposal_dispositions.jsonl",
    )
    freeze_output = release_root / "artifacts" / "claims"
    freeze.add_argument("--output-dir", type=Path, default=freeze_output)
    freeze.add_argument(
        "--build-record",
        type=Path,
        default=freeze_output / "build.json",
    )
    freeze.add_argument("--induction-model", default="gpt-5.5")
    freeze.add_argument("--induction-reasoning-effort", default="low")
    freeze.add_argument("--induction-inference-calls", type=int, default=176)
    freeze.add_argument("--consolidation-model", default="gpt-rosalind-5.5")
    freeze.add_argument("--consolidation-reasoning-effort", default="high")
    freeze.add_argument(
        "--consolidation-inference-calls",
        type=int,
        default=81,
    )
    freeze.set_defaults(function=freeze_command)

    evaluate = commands.add_parser("evaluate", help="summarize a pilot proposal set")
    evaluate.add_argument("--neighborhoods", type=Path, default=work / "neighborhoods.jsonl")
    evaluate.add_argument("--results", type=Path, default=work / "pilot_results.jsonl")
    evaluate.add_argument("--output", type=Path, default=None)
    evaluate.set_defaults(function=evaluate_command)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        return int(args.function(args))
    except (KeyError, OSError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
