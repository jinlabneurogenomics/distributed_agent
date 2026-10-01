#!/usr/bin/env python3
"""Build and finalize a bounded comparator-multiplicity prediction review.

The operation is truth-blind. It derives visible anchors and the candidate
universe from run-local calibration artifacts, uses graph multiplicity only to
bound review breadth, and emits only nomination metadata. It neither accepts
benchmark labels nor emits Finding text, and it never treats graph structure as
endpoint evidence.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Sequence

from relational_candidates import (
    RelationalIndex,
    _dedupe,
    _is_control,
    ledger_path,
    load_ledger,
    read_gene_file,
)


REVIEW_SCHEMA = "distributed_agents-predictive-graph-review-v2"
TELEMETRY_SCHEMA = "distributed_agents-predictive-graph-review-telemetry-v2"
MAX_OUTPUT_CHARS = 64_000


def _read_json_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object at {path}")
    return value


def _referenced_path(raw: object, *, relative_to: Path) -> Path:
    value = str(raw or "").strip()
    if not value:
        raise ValueError("calibration does not declare ranking_output")
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = relative_to / path
    path = path.resolve()
    if not path.is_file():
        raise ValueError(f"declared candidate universe is unavailable: {path}")
    return path


def _visible_seeds(bindings: dict[str, Any]) -> list[str]:
    seeds: list[str] = []
    for entity_set in bindings.get("entity_sets") or []:
        if not isinstance(entity_set, dict) or not entity_set.get(
            "active_for_coverage"
        ):
            continue
        ordering = entity_set.get("ordering") or {}
        if ordering.get("kind") not in {"ranked", "partial_ranked"}:
            continue
        for item in entity_set.get("items") or []:
            if not isinstance(item, dict):
                continue
            gene = str(item.get("canonical") or "").strip()
            if gene and not _is_control(gene):
                seeds.append(gene)
    result = _dedupe(seeds)
    if not result:
        raise ValueError(
            "task bindings contain no active ranked or partial-ranked gene anchors"
        )
    return result


def _read_quantitative_ranking(path: Path) -> list[tuple[int, str]]:
    """Read the calibrated non-seed prediction order from its canonical TSV."""

    text = path.read_text(encoding="utf-8")
    first = next((line for line in text.splitlines() if line.strip()), "")
    delimiter = "\t" if "\t" in first else ","
    reader = csv.DictReader(text.splitlines(), delimiter=delimiter)
    fields = {str(field or "").casefold(): str(field) for field in reader.fieldnames or []}
    gene_field = next(
        (fields[name] for name in ("gene_target", "target_gene", "gene") if name in fields),
        None,
    )
    rank_field = next(
        (fields[name] for name in ("prediction_rank", "rank") if name in fields),
        None,
    )
    if gene_field is None or rank_field is None:
        raise ValueError(
            "calibration ranking_output requires gene_target and prediction_rank columns"
        )
    rows: list[tuple[int, str]] = []
    seen: set[str] = set()
    for row in reader:
        gene = str(row.get(gene_field) or "").strip()
        raw_rank = str(row.get(rank_field) or "").strip()
        if not gene or not raw_rank:
            continue
        try:
            numeric_rank = float(raw_rank)
        except ValueError as exc:
            raise ValueError(f"{gene}: invalid prediction rank {raw_rank!r}") from exc
        rank = int(numeric_rank)
        if numeric_rank != rank or rank <= 0:
            raise ValueError(f"{gene}: prediction rank must be a positive integer")
        key = gene.casefold()
        if key in seen:
            raise ValueError(f"duplicate candidate in calibration ranking: {gene}")
        seen.add(key)
        rows.append((rank, gene))
    rows.sort(key=lambda item: (item[0], item[1].casefold()))
    if [rank for rank, _ in rows] != list(range(1, len(rows) + 1)):
        raise ValueError("calibration prediction ranks must be contiguous from 1")
    if not rows:
        raise ValueError("calibration ranking_output contains no predictions")
    return rows


def _candidate_record(
    gene: str,
    record: dict[str, Any],
    *,
    quantitative_rank: int,
    top_k: int,
) -> dict[str, Any]:
    multiplicity = int(record.get("outgoing_seed_count") or 0)
    in_quantitative_top_k = quantitative_rank <= top_k
    return {
        "gene_target": gene,
        "nomination_tier": (
            "first_pass_m3plus"
            if multiplicity >= 3
            else "rescue_m2"
            if multiplicity == 2
            else "single_anchor"
        ),
        "distinct_visible_seed_multiplicity": multiplicity,
        "visible_anchors": list(record.get("outgoing_seeds") or []),
        "quantitative_prediction_rank": quantitative_rank,
        "quantitative_top_k_member": in_quantitative_top_k,
        "review_role": (
            "quantitative_overlap"
            if in_quantitative_top_k
            else "graph_only_challenger"
        ),
    }


def _write_dispositions(path: Path, candidates: Sequence[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            delimiter="\t",
            fieldnames=[
                "gene_target",
                "review_role",
                "quantitative_prediction_rank",
                "inspected",
                "evidence_read",
                "rationale",
            ],
        )
        writer.writeheader()
        for candidate in candidates:
            writer.writerow(
                {
                    "gene_target": candidate["gene_target"],
                    "review_role": candidate["review_role"],
                    "quantitative_prediction_rank": candidate[
                        "quantitative_prediction_rank"
                    ],
                    "inspected": "false",
                    "evidence_read": "false",
                    "rationale": "",
                }
            )


def _serialize_with_count(report: dict[str, Any]) -> str:
    """Render pretty JSON with an exact, self-consistent character count."""

    report["output_char_count"] = 0
    while True:
        rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
        count = len(rendered)
        if report["output_char_count"] == count:
            return rendered
        report["output_char_count"] = count


def nominate(
    *,
    bindings_path: Path,
    calibration_path: Path,
    output_path: Path,
    dispositions_path: Path,
    findings_ledger: str | None,
    top_k: int,
) -> dict[str, Any]:
    if top_k <= 0:
        raise ValueError("top_k must be positive")
    bindings = _read_json_object(bindings_path)
    calibration = _read_json_object(calibration_path)
    seeds = _visible_seeds(bindings)
    ranking_path = _referenced_path(
        calibration.get("ranking_output"), relative_to=calibration_path.parent
    )
    seed_keys = {seed.casefold() for seed in seeds}
    quantitative_rows = _read_quantitative_ranking(ranking_path)
    universe = [
        gene
        for _, gene in quantitative_rows
        if not _is_control(gene) and gene.casefold() not in seed_keys
    ]
    if not universe:
        raise ValueError("calibration ranking_output contains no eligible candidates")

    source_path = ledger_path(findings_ledger)
    index = RelationalIndex(load_ledger(source_path))
    resolved_seeds = _dedupe(index.resolve(seed) for seed in seeds)
    resolved_universe = _dedupe(index.resolve(gene) for gene in universe)
    quantitative_rank_by_gene = {
        index.resolve(gene).casefold(): rank for rank, gene in quantitative_rows
    }
    records = index.features(resolved_seeds, resolved_universe)
    minimum_multiplicity = 2 if len(resolved_seeds) >= 6 else 1
    eligible = [
        (gene, row)
        for gene, row in records.items()
        if int(row.get("outgoing_seed_count") or 0) >= minimum_multiplicity
    ]
    eligible.sort(
        key=lambda item: (
            -int(item[1].get("outgoing_seed_count") or 0),
            item[0].casefold(),
        )
    )
    selected_priority = list(eligible)

    def render(selected: Sequence[tuple[str, dict[str, Any]]]) -> dict[str, Any]:
        candidates = sorted(
            (
                _candidate_record(
                    gene,
                    row,
                    quantitative_rank=quantitative_rank_by_gene[gene.casefold()],
                    top_k=top_k,
                )
                for gene, row in selected
            ),
            key=lambda row: str(row["gene_target"]).casefold(),
        )
        quantitative_overlap_count = sum(
            bool(row["quantitative_top_k_member"]) for row in candidates
        )
        return {
            "schema_version": REVIEW_SCHEMA,
            "status": "ready",
            "inputs": {
                "bindings": str(bindings_path.resolve()),
                "calibration": str(calibration_path.resolve()),
                "candidate_universe_file": str(ranking_path),
                "findings_ledger": str(source_path),
                "dispositions": str(dispositions_path.resolve()),
            },
            "bounds": {
                "max_output_chars": MAX_OUTPUT_CHARS,
                "requested_minimum_multiplicity": minimum_multiplicity,
                "effective_minimum_multiplicity": (
                    min(
                        int(row["distinct_visible_seed_multiplicity"])
                        for row in candidates
                    )
                    if candidates
                    else None
                ),
                "candidate_limit_policy": (
                    "complete directed-multiplicity tiers within the output bound"
                ),
            },
            "method": {
                "edge_direction": "visible_seed_finding_names_candidate",
                "multiplicity": "distinct_visible_seed_count",
                "tie_policy": "never_split_a_multiplicity_tier",
            },
            "guards": [
                "No benchmark labels or protected answers are accepted.",
                "Directed distinct-visible-seed comparator multiplicity selects bounded review breadth only; it is not endpoint evidence or a final ranking score.",
                "Candidates are serialized alphabetically after pool formation, so row order is not scientific supervision.",
                "The nomination contains no Finding text; selection or ordering requires a separate endpoint-bearing evidence operation.",
                "Every graph-only challenger requires an explicit completed review disposition before finalization.",
            ],
            "seeds": {
                "supplied": seeds,
                "resolved": resolved_seeds,
                "count": len(resolved_seeds),
            },
            "universe": {
                "eligible_candidate_count": len(resolved_universe),
                "multiplicity_eligible_count": len(eligible),
                "emitted_candidate_count": len(candidates),
                "omitted_by_output_bound": max(0, len(eligible) - len(candidates)),
                "boundary_multiplicity_tier_complete": True,
                "serialization_order": "alphabetical_not_scientific",
            },
            "heuristic_union": {
                "top_k": top_k,
                "quantitative_candidate_count": min(top_k, len(universe)),
                "graph_nominee_count": len(candidates),
                "quantitative_overlap_count": quantitative_overlap_count,
                "graph_only_challenger_count": (
                    len(candidates) - quantitative_overlap_count
                ),
                "union_candidate_count": (
                    min(top_k, len(universe))
                    + len(candidates)
                    - quantitative_overlap_count
                ),
                "required_review_role": "graph_only_challenger",
            },
            "candidates": candidates,
        }

    report = render(selected_priority)
    rendered = _serialize_with_count(report)
    while selected_priority and len(rendered) > MAX_OUTPUT_CHARS:
        boundary_multiplicity = min(
            int(row.get("outgoing_seed_count") or 0) for _, row in selected_priority
        )
        boundary_size = sum(
            int(row.get("outgoing_seed_count") or 0) == boundary_multiplicity
            for _, row in selected_priority
        )
        if boundary_size == len(selected_priority):
            raise ValueError(
                "the highest directed-multiplicity tier exceeds the JSON output bound"
            )
        selected_priority = [
            (gene, row)
            for gene, row in selected_priority
            if int(row.get("outgoing_seed_count") or 0) > boundary_multiplicity
        ]
        report = render(selected_priority)
        rendered = _serialize_with_count(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")
    _write_dispositions(dispositions_path, report["candidates"])
    return report


def _parse_bool(value: object, *, field: str, gene: str) -> bool:
    normalized = str(value or "").strip().casefold()
    if normalized in {"true", "1", "yes"}:
        return True
    if normalized in {"false", "0", "no"}:
        return False
    raise ValueError(f"{gene}: {field} must be true or false")


def _read_dispositions(path: Path) -> tuple[dict[str, dict[str, str]], list[str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    result: dict[str, dict[str, str]] = {}
    duplicates: list[str] = []
    for row in rows:
        gene = str(row.get("gene_target") or "").strip()
        key = gene.casefold()
        if not gene:
            continue
        if key in result:
            duplicates.append(gene)
        result[key] = {str(k): str(v or "") for k, v in row.items()}
    return result, duplicates


def finalize(
    *,
    review_path: Path,
    dispositions_path: Path,
    answer_path: Path,
    output_path: Path,
    top_k: int,
) -> dict[str, Any]:
    review = _read_json_object(review_path)
    if review.get("schema_version") != REVIEW_SCHEMA:
        raise ValueError("review has the wrong schema_version")
    candidate_rows = review.get("candidates") or []
    if not isinstance(candidate_rows, list):
        raise ValueError("review candidates must be a list")
    candidate_names = [
        str(row.get("gene_target") or "").strip()
        for row in candidate_rows
        if isinstance(row, dict) and str(row.get("gene_target") or "").strip()
    ]
    candidate_metadata = {
        str(row.get("gene_target") or "").strip().casefold(): row
        for row in candidate_rows
        if isinstance(row, dict) and str(row.get("gene_target") or "").strip()
    }
    dispositions, duplicates = _read_dispositions(dispositions_path)
    answer = read_gene_file(answer_path)[:top_k]
    ranking_path = Path(str((review.get("inputs") or {}).get("candidate_universe_file")))
    canonical = [gene for _, gene in _read_quantitative_ranking(ranking_path)[:top_k]]
    answer_set = {gene.casefold() for gene in answer}
    canonical_set = {gene.casefold() for gene in canonical}
    errors: list[str] = []
    if top_k <= 0:
        errors.append("top_k must be positive")
    if len(answer) != top_k:
        errors.append(f"answer contains {len(answer)} genes; expected {top_k}")
    review_top_k = int((review.get("heuristic_union") or {}).get("top_k") or 0)
    if review_top_k != top_k:
        errors.append(
            f"review union top_k is {review_top_k}; finalize requested {top_k}"
        )
    if duplicates:
        errors.append(f"duplicate disposition rows: {', '.join(sorted(duplicates))}")

    telemetry_rows: list[dict[str, Any]] = []
    for gene in candidate_names:
        metadata = candidate_metadata[gene.casefold()]
        review_role = str(metadata.get("review_role") or "").strip()
        quantitative_rank = metadata.get("quantitative_prediction_rank")
        row = dispositions.get(gene.casefold())
        if row is None:
            errors.append(f"{gene}: missing disposition row")
            inspected = False
            evidence_read = False
            rationale = ""
        else:
            inspected = _parse_bool(row.get("inspected"), field="inspected", gene=gene)
            evidence_read = _parse_bool(
                row.get("evidence_read"), field="evidence_read", gene=gene
            )
            rationale = str(row.get("rationale") or "").strip()
        if evidence_read and not inspected:
            errors.append(f"{gene}: evidence_read=true requires inspected=true")
        if inspected and not rationale:
            errors.append(f"{gene}: inspected candidates require a rationale")
        if review_role == "graph_only_challenger" and not inspected:
            errors.append(
                f"{gene}: graph-only challengers require inspected=true and a disposition rationale"
            )
        selected = gene.casefold() in answer_set
        in_canonical_top_k = gene.casefold() in canonical_set
        if selected and not in_canonical_top_k:
            disposition = "promoted"
            if not inspected or not evidence_read:
                errors.append(
                    f"{gene}: graph-nominated promotion requires inspected=true and evidence_read=true"
                )
        elif selected:
            disposition = "retained_quantitative"
        elif inspected:
            disposition = "rejected"
        else:
            disposition = "not_reviewed"
        telemetry_rows.append(
            {
                "gene_target": gene,
                "inspected": inspected,
                "evidence_read": evidence_read,
                "selected": selected,
                "in_canonical_top_k": in_canonical_top_k,
                "quantitative_prediction_rank": quantitative_rank,
                "review_role": review_role,
                "final_disposition": disposition,
                "rationale": rationale,
            }
        )

    expected = {gene.casefold() for gene in candidate_names}
    extras = sorted(
        (row["gene_target"] for key, row in dispositions.items() if key not in expected),
        key=str.casefold,
    )
    if extras:
        errors.append(f"dispositions contain non-nominated candidates: {', '.join(extras)}")

    categories = (
        "retained_quantitative",
        "promoted",
        "rejected",
        "not_reviewed",
    )
    result = {
        "schema_version": TELEMETRY_SCHEMA,
        "status": "passed" if not errors else "failed",
        "review": str(review_path.resolve()),
        "dispositions": str(dispositions_path.resolve()),
        "answer": str(answer_path.resolve()),
        "top_k": top_k,
        "counts": {
            "nominated": len(candidate_names),
            "quantitative_overlap": sum(
                row["review_role"] == "quantitative_overlap" for row in telemetry_rows
            ),
            "graph_only_challengers": sum(
                row["review_role"] == "graph_only_challenger"
                for row in telemetry_rows
            ),
            "completed_graph_only_reviews": sum(
                row["review_role"] == "graph_only_challenger" and row["inspected"]
                for row in telemetry_rows
            ),
            "inspected": sum(bool(row["inspected"]) for row in telemetry_rows),
            "evidence_read": sum(
                bool(row["evidence_read"]) for row in telemetry_rows
            ),
            **{
                category: sum(
                    row["final_disposition"] == category for row in telemetry_rows
                )
                for category in categories
            },
        },
        "candidates": telemetry_rows,
        "errors": errors,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    nominate_parser = commands.add_parser("nominate")
    nominate_parser.add_argument("--bindings", type=Path, required=True)
    nominate_parser.add_argument("--calibration", type=Path, required=True)
    nominate_parser.add_argument("--top-k", type=int, required=True)
    nominate_parser.add_argument("--findings-ledger")
    nominate_parser.add_argument("--out", type=Path, required=True)
    nominate_parser.add_argument("--dispositions-out", type=Path, required=True)
    finalize_parser = commands.add_parser("finalize")
    finalize_parser.add_argument("--review", type=Path, required=True)
    finalize_parser.add_argument("--dispositions", type=Path, required=True)
    finalize_parser.add_argument("--answer", type=Path, required=True)
    finalize_parser.add_argument("--top-k", type=int, required=True)
    finalize_parser.add_argument("--out", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.command == "nominate":
            result = nominate(
                bindings_path=args.bindings,
                calibration_path=args.calibration,
                output_path=args.out,
                dispositions_path=args.dispositions_out,
                findings_ledger=args.findings_ledger,
                top_k=args.top_k,
            )
        else:
            result = finalize(
                review_path=args.review,
                dispositions_path=args.dispositions,
                answer_path=args.answer,
                output_path=args.out,
                top_k=args.top_k,
            )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        result = {"status": "failed", "command": args.command, "error": str(exc)}
        output = getattr(args, "out", None)
        if output:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2))
        return 1
    if args.command == "nominate":
        receipt = {
            "status": result.get("status"),
            "out": str(args.out.resolve()),
            "dispositions": str(args.dispositions_out.resolve()),
            "seed_count": (result.get("seeds") or {}).get("count"),
            "candidate_count": len(result.get("candidates") or []),
            "output_char_count": result.get("output_char_count"),
        }
    else:
        receipt = {
            "status": result.get("status"),
            "out": str(args.out.resolve()),
            "counts": result.get("counts"),
            "errors": result.get("errors"),
        }
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if result.get("status") in {"ready", "passed"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
