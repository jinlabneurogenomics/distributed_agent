#!/usr/bin/env python3
"""Retrieve typed candidate perturbations from visible Perturb-seq anchors.

The runtime is deliberately truth-blind. It reads visible anchor genes and the
same-experiment Findings ledger, exposes several relational evidence lanes, and
uses deterministic seed dropout to measure whether each lane can recover
withheld *visible* anchors. It never accepts benchmark labels or a ground-truth
ranking.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Sequence


SCHEMA_VERSION = "distributed_agents-relational-candidates-v2"
DEFAULT_LEDGER = (
    Path(__file__).resolve().parents[3]
    / "artifacts"
    / "ledgers"
    / "findings.csv"
)
GENE_FIELDS = (
    "gene_target",
    "target_gene",
    "gene",
    "symbol",
    "perturbation",
)
GENE_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]*$")
FENCE_PATTERN = re.compile(r"```(?:tsv|csv|text)?\s*\n(.*?)```", re.I | re.S)


def _split_pipe(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [item.strip() for item in str(value or "").split("|") if item.strip()]


def _canonical_map(values: Iterable[str]) -> dict[str, str]:
    return {value.casefold(): value for value in values if value}


def _dedupe(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        clean = value.strip()
        key = clean.casefold()
        if clean and key not in seen:
            seen.add(key)
            result.append(clean)
    return result


def _is_control(gene: str) -> bool:
    folded = gene.casefold()
    return folded == "non_target" or folded.startswith("safe_target_")


def _rows_from_delimited(text: str, delimiter: str) -> list[dict[str, str]]:
    reader = csv.DictReader(text.splitlines(), delimiter=delimiter)
    if not reader.fieldnames:
        return []
    return [
        {str(key or "").strip(): str(value or "").strip() for key, value in row.items()}
        for row in reader
    ]


def _genes_from_delimited(text: str) -> list[str]:
    first = next((line for line in text.splitlines() if line.strip()), "")
    delimiter = "\t" if "\t" in first else ","
    rows = _rows_from_delimited(text, delimiter)
    if not rows:
        return []
    fields = {field.casefold(): field for field in rows[0]}
    selected = next((fields[field] for field in GENE_FIELDS if field in fields), None)
    if selected is None:
        return []
    return _dedupe(
        row[selected]
        for row in rows
        if row.get(selected) and GENE_PATTERN.fullmatch(row[selected])
    )


def read_gene_file(path: Path) -> list[str]:
    """Read genes from CSV/TSV, a one-column file, or a fenced Markdown table."""

    text = path.read_text(encoding="utf-8")
    if path.suffix.casefold() in {".md", ".markdown"}:
        for block in FENCE_PATTERN.findall(text):
            genes = _genes_from_delimited(block)
            if genes:
                return genes
        return []
    genes = _genes_from_delimited(text)
    if genes:
        return genes
    result: list[str] = []
    for line in text.splitlines():
        fields = re.split(r"[\t,]", line.strip())
        value = fields[-1].strip() if fields else ""
        if GENE_PATTERN.fullmatch(value) and value.casefold() not in GENE_FIELDS:
            result.append(value)
    return _dedupe(result)


def ledger_path(override: str | None) -> Path:
    if override:
        return Path(override).expanduser().resolve()
    env = os.environ.get("DISTRIBUTED_AGENTS_FINDINGS_LEDGER")
    if env:
        return Path(env).expanduser().resolve()
    return DEFAULT_LEDGER.resolve()


def load_ledger(path: Path) -> list[dict[str, Any]]:
    """Load the flat CSV ledger or its nested JSONL representation."""

    if not path.is_file():
        raise FileNotFoundError(
            f"Findings ledger not found at {path}; pass --findings-ledger "
            "or set DISTRIBUTED_AGENTS_FINDINGS_LEDGER."
        )
    rows: list[dict[str, Any]] = []
    if path.suffix.casefold() == ".csv":
        with path.open(newline="", encoding="utf-8") as handle:
            for raw in csv.DictReader(handle):
                target = str(raw.get("target_gene") or "").strip()
                finding_id = str(raw.get("finding_id") or "").strip()
                if not target:
                    continue
                rows.append(
                    {
                        "target_gene": target,
                        "finding_id": finding_id,
                        "doc_id": f"{target}:{finding_id}",
                        "finding_type": str(raw.get("finding_type") or "").strip(),
                        "direction": str(raw.get("direction") or "").strip(),
                        "comparators": _split_pipe(raw.get("comparators")),
                        "response_terms": _split_pipe(raw.get("genes")),
                        "evidence_ids": _split_pipe(raw.get("evidence_ids")),
                    }
                )
        return rows

    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                raw = json.loads(line)
            except json.JSONDecodeError:
                continue
            source = raw.get("source") or {}
            target = str(raw.get("gene_target") or "").strip()
            if not target:
                continue
            finding_id = str(raw.get("finding_id") or "").strip()
            rows.append(
                {
                    "target_gene": target,
                    "finding_id": finding_id,
                    "doc_id": str(raw.get("doc_id") or f"{target}:{finding_id}"),
                    "finding_type": str(source.get("finding_type") or "").strip(),
                    "direction": str(source.get("direction") or "").strip(),
                    "comparators": _split_pipe(source.get("comparators")),
                    "response_terms": _split_pipe(source.get("genes")),
                    "evidence_ids": _split_pipe(source.get("evidence_ids")),
                }
            )
    return rows


class RelationalIndex:
    """In-memory typed projection of the Findings ledger."""

    def __init__(self, rows: Sequence[dict[str, Any]]) -> None:
        self.rows = list(rows)
        targets = _dedupe(str(row["target_gene"]) for row in rows)
        self.canonical = _canonical_map(targets)
        self.rows_by_target: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self.out_rows: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(
            lambda: defaultdict(list)
        )
        self.in_rows: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(
            lambda: defaultdict(list)
        )
        self.response_terms: dict[str, set[str]] = defaultdict(set)
        self.term_display: dict[str, str] = {}
        for row in rows:
            target = self.resolve(str(row["target_gene"]))
            self.rows_by_target[target].append(row)
            for comparator_raw in row["comparators"]:
                comparator = self.resolve(comparator_raw)
                self.out_rows[target][comparator].append(row)
                self.in_rows[comparator][target].append(row)
            for raw_term in row["response_terms"]:
                term = raw_term.casefold()
                self.response_terms[target].add(term)
                self.term_display.setdefault(term, raw_term)
        self.term_df = Counter(
            term
            for target_terms in self.response_terms.values()
            for term in target_terms
        )

    def resolve(self, gene: str) -> str:
        clean = gene.strip()
        return self.canonical.get(clean.casefold(), clean)

    @property
    def biological_targets(self) -> list[str]:
        return sorted(
            (target for target in self.canonical.values() if not _is_control(target)),
            key=str.casefold,
        )

    def comparator_degree(self, target: str) -> int:
        return self.outgoing_comparator_degree(
            target
        ) + self.incoming_comparator_degree(target)

    def outgoing_comparator_degree(self, target: str) -> int:
        return len(self.out_rows.get(target, {}))

    def incoming_comparator_degree(self, target: str) -> int:
        return len(self.in_rows.get(target, {}))

    def features(
        self,
        seeds: Sequence[str],
        candidates: Iterable[str],
    ) -> dict[str, dict[str, Any]]:
        seed_list = _dedupe(self.resolve(seed) for seed in seeds)
        seed_set = set(seed_list)
        seed_term_union = set().union(
            *(self.response_terms.get(seed, set()) for seed in seed_list)
        )
        records: dict[str, dict[str, Any]] = {}

        for raw_candidate in candidates:
            candidate = self.resolve(raw_candidate)
            if candidate in seed_set or _is_control(candidate):
                continue
            outgoing_seed_rows: dict[str, list[dict[str, Any]]] = {}
            reverse_seed_rows: dict[str, list[dict[str, Any]]] = {}
            for seed in seed_list:
                outgoing = self.out_rows.get(seed, {}).get(candidate, [])
                reverse = self.out_rows.get(candidate, {}).get(seed, [])
                if outgoing:
                    outgoing_seed_rows[seed] = outgoing
                if reverse:
                    reverse_seed_rows[seed] = reverse

            outgoing_seed_set = set(outgoing_seed_rows)
            reverse_seed_set = set(reverse_seed_rows)
            reciprocal_seeds = outgoing_seed_set & reverse_seed_set
            outgoing_rows = [
                row for rows in outgoing_seed_rows.values() for row in rows
            ]
            reverse_rows = [row for rows in reverse_seed_rows.values() for row in rows]

            second_hop_paths: set[tuple[str, str, str]] = set()
            second_hop_weighted = 0.0
            second_hop_seeds: set[str] = set()
            for seed in seed_list:
                for middle in self.out_rows.get(seed, {}):
                    if middle == candidate:
                        continue
                    if candidate not in self.out_rows.get(middle, {}):
                        continue
                    path = (seed, middle, candidate)
                    if path in second_hop_paths:
                        continue
                    second_hop_paths.add(path)
                    second_hop_seeds.add(seed)
                    middle_fanout = len(self.out_rows.get(middle, {}))
                    second_hop_weighted += 1.0 / math.log2(2.0 + middle_fanout)
            incoming_degree = self.incoming_comparator_degree(candidate)
            second_hop_specificity = second_hop_weighted / (1.0 + incoming_degree)

            candidate_terms = self.response_terms.get(candidate, set())
            shared_pairs: set[tuple[str, str]] = set()
            response_seeds: set[str] = set()
            for seed in seed_list:
                for term in candidate_terms & self.response_terms.get(seed, set()):
                    shared_pairs.add((seed, term))
                    response_seeds.add(seed)
            response_weighted = sum(
                1.0 / math.log2(2.0 + self.term_df[term]) for _, term in shared_pairs
            )
            weighted_intersection = sum(
                1.0 / math.log2(2.0 + self.term_df[term])
                for term in candidate_terms & seed_term_union
            )
            weighted_union = sum(
                1.0 / math.log2(2.0 + self.term_df[term])
                for term in candidate_terms | seed_term_union
            )

            relation_types_out = Counter(
                str(row.get("finding_type") or "untyped") for row in outgoing_rows
            )
            relation_types_reverse = Counter(
                str(row.get("finding_type") or "untyped") for row in reverse_rows
            )
            directions_out = Counter(
                str(row.get("direction") or "unspecified") for row in outgoing_rows
            )
            directions_reverse = Counter(
                str(row.get("direction") or "unspecified") for row in reverse_rows
            )
            outgoing_relations = [
                {
                    "seed": seed,
                    "finding_id": str(row["doc_id"]),
                    "finding_type": str(row.get("finding_type") or "untyped"),
                    "direction": str(row.get("direction") or "unspecified"),
                    "evidence_ids": list(row["evidence_ids"]),
                }
                for seed in sorted(outgoing_seed_rows, key=str.casefold)
                for row in outgoing_seed_rows[seed]
            ]
            reverse_relations = [
                {
                    "seed": seed,
                    "finding_id": str(row["doc_id"]),
                    "finding_type": str(row.get("finding_type") or "untyped"),
                    "direction": str(row.get("direction") or "unspecified"),
                    "evidence_ids": list(row["evidence_ids"]),
                }
                for seed in sorted(reverse_seed_rows, key=str.casefold)
                for row in reverse_seed_rows[seed]
            ]
            records[candidate] = {
                "gene_target": candidate,
                "outgoing_seed_count": len(outgoing_seed_set),
                "outgoing_mentions": len(outgoing_rows),
                "reverse_seed_count": len(reverse_seed_set),
                "reverse_mentions": len(reverse_rows),
                "reciprocal_seed_count": len(reciprocal_seeds),
                "bidirectional_mentions": len(outgoing_rows) + len(reverse_rows),
                "second_hop_seed_count": len(second_hop_seeds),
                "second_hop_path_count": len(second_hop_paths),
                "second_hop_weighted": round(second_hop_weighted, 6),
                "second_hop_specificity": round(second_hop_specificity, 6),
                "second_hop_supported": int(len(second_hop_seeds) >= 2),
                "shared_response_seed_count": len(response_seeds),
                "shared_response_pair_count": len(shared_pairs),
                "shared_response_weighted": round(response_weighted, 6),
                "shared_response_weighted_jaccard": round(
                    weighted_intersection / weighted_union if weighted_union else 0.0,
                    6,
                ),
                "outgoing_comparator_degree": self.outgoing_comparator_degree(
                    candidate
                ),
                "incoming_comparator_degree": incoming_degree,
                "comparator_degree": self.comparator_degree(candidate),
                "finding_count": len(self.rows_by_target.get(candidate, [])),
                "outgoing_seeds": sorted(outgoing_seed_set, key=str.casefold),
                "reverse_seeds": sorted(reverse_seed_set, key=str.casefold),
                "reciprocal_seeds": sorted(reciprocal_seeds, key=str.casefold),
                "relation_types_outgoing": dict(sorted(relation_types_out.items())),
                "relation_types_reverse": dict(sorted(relation_types_reverse.items())),
                "directions_outgoing": dict(sorted(directions_out.items())),
                "directions_reverse": dict(sorted(directions_reverse.items())),
                "outgoing_relations": outgoing_relations,
                "reverse_relations": reverse_relations,
                "outgoing_finding_ids": sorted(
                    {str(row["doc_id"]) for row in outgoing_rows}
                ),
                "reverse_finding_ids": sorted(
                    {str(row["doc_id"]) for row in reverse_rows}
                ),
                "outgoing_evidence_ids": sorted(
                    {
                        evidence_id
                        for row in outgoing_rows
                        for evidence_id in row["evidence_ids"]
                    }
                ),
                "reverse_evidence_ids": sorted(
                    {
                        evidence_id
                        for row in reverse_rows
                        for evidence_id in row["evidence_ids"]
                    }
                ),
                "second_hop_examples": [
                    {"seed": seed, "via": middle}
                    for seed, middle, _ in sorted(second_hop_paths)[:20]
                ],
                "shared_response_terms": sorted(
                    {self.term_display.get(term, term) for _, term in shared_pairs},
                    key=str.casefold,
                )[:30],
            }
        return records


FEATURES = {
    "outgoing": "outgoing_mentions",
    "reverse": "reverse_mentions",
    "bidirectional": "bidirectional_mentions",
    "second_hop": "second_hop_supported",
    "shared_response": "shared_response_weighted",
    "comparator_degree_control": "outgoing_comparator_degree",
    "finding_count_control": "finding_count",
}


def _semantic_lanes(
    records: dict[str, dict[str, Any]],
) -> dict[str, list[str]]:
    """Return exhaustive, alphabetically ordered semantic groups.

    Ordering is deliberately non-scientific. These groups expose where context
    exists; they do not rank candidate relevance to the task endpoint.
    """

    predicates = {
        "outgoing": lambda row: bool(row["outgoing_relations"]),
        "reverse": lambda row: bool(row["reverse_relations"]),
        "reciprocal": lambda row: bool(row["reciprocal_seeds"]),
        "bidirectional": lambda row: (
            bool(row["outgoing_relations"]) and bool(row["reverse_relations"])
        ),
        "second_hop": lambda row: bool(row["second_hop_examples"]),
        "shared_response": lambda row: bool(row["shared_response_terms"]),
    }
    return {
        name: sorted(
            (
                gene
                for gene, row in records.items()
                if predicate(row)
            ),
            key=str.casefold,
        )
        for name, predicate in predicates.items()
    }


def average_precision(labels: Sequence[bool], scores: Sequence[float]) -> float:
    positives = sum(labels)
    if not labels or positives == 0:
        return 0.0
    grouped: dict[float, list[bool]] = defaultdict(list)
    for label, score in zip(labels, scores):
        grouped[float(score)].append(bool(label))
    true_positive = 0
    false_positive = 0
    previous_recall = 0.0
    result = 0.0
    for score in sorted(grouped, reverse=True):
        values = grouped[score]
        true_positive += sum(values)
        false_positive += len(values) - sum(values)
        recall = true_positive / positives
        precision = true_positive / (true_positive + false_positive)
        result += (recall - previous_recall) * precision
        previous_recall = recall
    return result


def tie_aware_auc(labels: Sequence[bool], scores: Sequence[float]) -> float:
    positive_scores = [score for label, score in zip(labels, scores) if label]
    negative_scores = [score for label, score in zip(labels, scores) if not label]
    if not positive_scores or not negative_scores:
        return 0.5
    favorable = 0.0
    for positive in positive_scores:
        for negative in negative_scores:
            favorable += float(positive > negative) + 0.5 * float(positive == negative)
    return favorable / (len(positive_scores) * len(negative_scores))


def _pool_metrics(
    records: dict[str, dict[str, Any]],
    held: set[str],
    candidate_count: int,
) -> dict[str, dict[str, float | int]]:
    baseline = len(held) / candidate_count if candidate_count else 0.0
    predicates = {
        "outgoing": lambda row: row["outgoing_seed_count"] > 0,
        "reverse": lambda row: row["reverse_seed_count"] > 0,
        "union": lambda row: (
            row["outgoing_seed_count"] > 0 or row["reverse_seed_count"] > 0
        ),
        "reciprocal": lambda row: row["reciprocal_seed_count"] > 0,
        "bidirectional_intersection": lambda row: (
            row["outgoing_seed_count"] > 0 and row["reverse_seed_count"] > 0
        ),
        "second_hop_any": lambda row: row["second_hop_path_count"] > 0,
        "second_hop_supported": lambda row: row["second_hop_supported"] > 0,
        "shared_response_any": lambda row: row["shared_response_pair_count"] > 0,
        "shared_response_10plus": lambda row: row["shared_response_pair_count"] >= 10,
    }
    result: dict[str, dict[str, float | int]] = {}
    for name, predicate in predicates.items():
        pool = {gene for gene, row in records.items() if predicate(row)}
        recovered = len(pool & held)
        precision = recovered / len(pool) if pool else 0.0
        result[name] = {
            "pool_size": len(pool),
            "recovered": recovered,
            "recall": round(recovered / len(held) if held else 0.0, 6),
            "precision": round(precision, 6),
            "enrichment_over_random": round(
                precision / baseline if baseline and pool else 0.0,
                6,
            ),
        }
    return result


def seed_dropout(
    index: RelationalIndex,
    seeds: Sequence[str],
    universe: Sequence[str],
    folds: int,
) -> dict[str, Any]:
    """Evaluate retrieval lanes by hiding rank-interleaved visible anchors."""

    visible = _dedupe(index.resolve(seed) for seed in seeds)
    universe_set = set(universe)
    available = [seed for seed in visible if seed in universe_set]
    if len(available) < 4:
        return {
            "status": "unavailable",
            "reason": "At least four visible anchors must occur in the candidate universe.",
            "visible_seed_count": len(visible),
            "eligible_visible_seed_count": len(available),
        }
    fold_count = max(2, min(folds, len(available)))
    fold_rows: list[dict[str, Any]] = []
    for fold_index in range(fold_count):
        held = set(available[fold_index::fold_count])
        if not held:
            continue
        training = [seed for seed in available if seed not in held]
        training_set = set(training)
        candidates = [gene for gene in universe if gene not in training_set]
        records = index.features(training, candidates)
        labels = [gene in held for gene in records]
        baseline = sum(labels) / len(labels) if labels else 0.0
        feature_metrics: dict[str, dict[str, float]] = {}
        for feature_name, field in FEATURES.items():
            scores = [float(row[field]) for row in records.values()]
            ap = average_precision(labels, scores)
            feature_metrics[feature_name] = {
                "average_precision": round(ap, 6),
                "ap_lift_over_random": round(ap / baseline if baseline else 0.0, 6),
                "auc": round(tie_aware_auc(labels, scores), 6),
            }
        fold_rows.append(
            {
                "fold": fold_index + 1,
                "training_seed_count": len(training),
                "held_visible_seeds": sorted(held, key=str.casefold),
                "candidate_count": len(records),
                "random_baseline": round(baseline, 8),
                "features": feature_metrics,
                "pools": _pool_metrics(records, held, len(records)),
            }
        )

    feature_summary: dict[str, dict[str, float | int]] = {}
    for feature_name in FEATURES:
        lifts = [
            float(fold["features"][feature_name]["ap_lift_over_random"])
            for fold in fold_rows
        ]
        aucs = [float(fold["features"][feature_name]["auc"]) for fold in fold_rows]
        feature_summary[feature_name] = {
            "mean_ap_lift_over_random": round(statistics.fmean(lifts), 6),
            "median_ap_lift_over_random": round(statistics.median(lifts), 6),
            "min_ap_lift_over_random": round(min(lifts), 6),
            "max_ap_lift_over_random": round(max(lifts), 6),
            "mean_auc": round(statistics.fmean(aucs), 6),
            "folds_below_random_ap": sum(lift < 1.0 for lift in lifts),
        }

    pool_summary: dict[str, dict[str, float]] = {}
    for pool_name in fold_rows[0]["pools"]:
        pool_summary[pool_name] = {
            metric: round(
                statistics.fmean(
                    float(fold["pools"][pool_name][metric]) for fold in fold_rows
                ),
                6,
            )
            for metric in (
                "pool_size",
                "recall",
                "precision",
                "enrichment_over_random",
            )
        }

    return {
        "status": "available",
        "method": (
            "Deterministic rank-interleaved folds over visible anchors. Each fold "
            "hides visible anchors, builds features from the remainder, and treats "
            "all other eligible targets as unlabeled negatives."
        ),
        "interpretation_guard": (
            "These are proxy retrieval diagnostics, not performance on withheld "
            "benchmark answers and not evidence that any candidate is a true hit."
        ),
        "fold_count": len(fold_rows),
        "visible_seed_count": len(visible),
        "eligible_visible_seed_count": len(available),
        "features": feature_summary,
        "pools": pool_summary,
        "folds": fold_rows,
    }


def _semantic_candidate_rows(
    records: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Project numeric graph diagnostics into unranked semantic context."""

    rows: list[dict[str, Any]] = []
    for gene in sorted(records, key=str.casefold):
        record = records[gene]
        semantic_lanes = [
            name
            for name, present in (
                ("outgoing", bool(record["outgoing_relations"])),
                ("reverse", bool(record["reverse_relations"])),
                ("reciprocal", bool(record["reciprocal_seeds"])),
                (
                    "bidirectional",
                    bool(record["outgoing_relations"])
                    and bool(record["reverse_relations"]),
                ),
                ("second_hop", bool(record["second_hop_examples"])),
                ("shared_response", bool(record["shared_response_terms"])),
            )
            if present
        ]
        if not semantic_lanes:
            continue
        rows.append(
            {
                "gene_target": gene,
                "semantic_lanes": semantic_lanes,
                "outgoing_relations": record["outgoing_relations"],
                "reverse_relations": record["reverse_relations"],
                "reciprocal_seeds": record["reciprocal_seeds"],
                "second_hop_examples": record["second_hop_examples"],
                "shared_response_terms": record["shared_response_terms"],
            }
        )
    return rows


def write_candidate_csv(path: Path, rows: Sequence[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    json_fields = (
        "semantic_lanes",
        "outgoing_relations",
        "reverse_relations",
        "reciprocal_seeds",
        "second_hop_examples",
        "shared_response_terms",
    )
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["gene_target", *json_fields],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "gene_target": row["gene_target"],
                    **{
                        field: json.dumps(row[field], sort_keys=True)
                        for field in json_fields
                    },
                }
            )


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--seeds-file",
        type=Path,
        help="CSV, TSV, one-column, or Markdown file containing visible anchors.",
    )
    parser.add_argument(
        "--seed",
        action="append",
        default=[],
        help="Visible anchor gene; repeatable and combined with --seeds-file.",
    )
    parser.add_argument(
        "--findings-ledger",
        "--ledger-path",
        dest="findings_ledger",
        help="Override the Findings CSV/JSONL path.",
    )
    parser.add_argument(
        "--candidate-universe",
        type=Path,
        help="Optional CSV/TSV/Markdown candidate universe; defaults to ledger targets.",
    )
    parser.add_argument("--out", type=Path, required=True, help="JSON report path.")
    parser.add_argument(
        "--candidates-out",
        type=Path,
        help="Optional unranked semantic candidate map in CSV format.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=100,
        help=(
            "Deprecated compatibility option; semantic groups are exhaustive "
            "and never graph-ranked."
        ),
    )
    parser.add_argument(
        "--folds",
        type=int,
        default=5,
        help="Rank-interleaved visible-seed dropout folds (default: 5).",
    )
    return parser.parse_args(argv)


def run(args: argparse.Namespace) -> dict[str, Any]:
    seed_values = list(args.seed)
    if args.seeds_file:
        seed_values.extend(read_gene_file(args.seeds_file))
    seed_values = _dedupe(seed_values)
    if not seed_values:
        raise ValueError(
            "No visible anchors found; pass --seed or a supported --seeds-file."
        )
    path = ledger_path(args.findings_ledger)
    rows = load_ledger(path)
    index = RelationalIndex(rows)
    seeds = _dedupe(index.resolve(seed) for seed in seed_values)
    if args.candidate_universe:
        universe_values = read_gene_file(args.candidate_universe)
        universe = _dedupe(index.resolve(gene) for gene in universe_values)
    else:
        universe = index.biological_targets
    universe = [gene for gene in universe if not _is_control(gene)]
    universe_set = set(universe)
    seed_set = set(seeds)
    records = index.features(seeds, universe)
    lanes = _semantic_lanes(records)
    candidate_map = _semantic_candidate_rows(records)
    seed_rows = {
        seed: {
            "finding_count": len(index.rows_by_target.get(seed, [])),
            "outgoing_candidate_count": len(
                {
                    candidate
                    for candidate in index.out_rows.get(seed, {})
                    if candidate in universe_set and candidate not in seed_set
                }
            ),
            "response_term_count": len(index.response_terms.get(seed, set())),
        }
        for seed in seeds
    }
    report = {
        "schema_version": SCHEMA_VERSION,
        "inputs": {
            "seeds_file": str(args.seeds_file.resolve()) if args.seeds_file else None,
            "findings_ledger": str(path),
            "candidate_universe_file": (
                str(args.candidate_universe.resolve())
                if args.candidate_universe
                else None
            ),
        },
        "guards": [
            "The tool has no argument for ground truth or benchmark labels.",
            "The graph is semantic navigation only, never a candidate score or ranking signal.",
            "Never combine graph counts, weights, degrees, paths, lane membership, or dropout diagnostics into candidate ordering.",
            "Candidate ordering must come from endpoint-specific observed data or separately justified endpoint-bearing evidence.",
            "Negative, divergent, opposite, uncoupled, and warning relations remain semantic cautions, not positive links.",
        ],
        "seeds": {
            "supplied": seed_values,
            "resolved": seeds,
            "missing_from_ledger": [
                seed for seed in seeds if seed not in index.rows_by_target
            ],
            "profiles": seed_rows,
        },
        "universe": {
            "eligible_target_count": len(universe),
            "mapped_candidate_count": len(candidate_map),
            "control_filter": "Exclude Non_target and Safe_target_*.",
            "ordering": (
                "Alphabetical for deterministic serialization; explicitly not "
                "a scientific ranking."
            ),
        },
        "lane_definitions": {
            "outgoing": "Visible anchor finding explicitly names candidate as comparator.",
            "reverse": "Candidate finding explicitly names a visible anchor as comparator.",
            "reciprocal": "The same visible anchor and candidate name one another.",
            "bidirectional": "Candidate has explicit comparator context in both orientations, not necessarily the same pair.",
            "second_hop": "Anchor-to-intermediate-to-candidate comparator paths for semantic follow-up.",
            "shared_response": "Shared response terms that may motivate a targeted comparison.",
        },
        "map_diagnostics": {
            "outgoing_candidate_count": sum(
                row["outgoing_seed_count"] > 0 for row in records.values()
            ),
            "reverse_candidate_count": sum(
                row["reverse_seed_count"] > 0 for row in records.values()
            ),
            "union_candidate_count": sum(
                row["outgoing_seed_count"] > 0 or row["reverse_seed_count"] > 0
                for row in records.values()
            ),
            "reciprocal_candidate_count": sum(
                row["reciprocal_seed_count"] > 0 for row in records.values()
            ),
            "bidirectional_intersection_candidate_count": sum(
                row["outgoing_seed_count"] > 0 and row["reverse_seed_count"] > 0
                for row in records.values()
            ),
            "second_hop_any_candidate_count": sum(
                row["second_hop_path_count"] > 0 for row in records.values()
            ),
            "second_hop_supported_candidate_count": sum(
                row["second_hop_supported"] > 0 for row in records.values()
            ),
            "shared_response_any_candidate_count": sum(
                row["shared_response_pair_count"] > 0 for row in records.values()
            ),
            "shared_response_10plus_candidate_count": sum(
                row["shared_response_pair_count"] >= 10 for row in records.values()
            ),
        },
        "lanes": lanes,
        "candidate_map": candidate_map,
        "seed_dropout": seed_dropout(index, seeds, universe, args.folds),
    }
    if args.candidates_out:
        write_candidate_csv(args.candidates_out, candidate_map)
        report["inputs"]["candidate_table"] = str(args.candidates_out.resolve())
    return report


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        report = run(args)
    except (FileNotFoundError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "out": str(args.out.resolve()),
                "seed_count": len(report["seeds"]["resolved"]),
                "candidate_count": report["universe"]["mapped_candidate_count"],
                "dropout_status": report["seed_dropout"]["status"],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
