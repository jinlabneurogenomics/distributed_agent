#!/usr/bin/env python3
"""Validate and assemble a full-union candidate ranking.

The reviewer may reorder every candidate in the comparison set.  The starting
quantitative result is retained only for provenance and movement auditing; this
helper does not protect a prefix or impose a swap budget.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


SCHEMA_VERSION = "distributed_agents-global-ranking-audit-v1"
DECISIONS = frozenset({"selected", "not_selected"})


def _delimiter(path: Path) -> str:
    return "\t" if path.suffix.casefold() == ".tsv" else ","


def _read_table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter=_delimiter(path)))


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"line {line_number} is not a JSON object")
            rows.append(value)
    return rows


def _candidate(value: dict[str, object], *, source: str) -> str:
    for field in ("gene_target", "candidate_id", "candidate"):
        candidate = str(value.get(field) or "").strip()
        if candidate:
            return candidate
    raise ValueError(f"{source} row lacks gene_target/candidate_id/candidate")


def _starting_ranks(
    path: Path | None,
    *,
    candidate_column: str,
    rank_column: str,
) -> dict[str, int]:
    if path is None:
        return {}
    rows = _read_table(path)
    ranks: dict[str, int] = {}
    for row in rows:
        candidate = row.get(candidate_column, "").strip()
        rank_text = row.get(rank_column, "").strip()
        if not candidate or not rank_text:
            continue
        rank = int(float(rank_text))
        if rank < 1:
            raise ValueError(f"starting rank for {candidate} must be positive")
        folded = candidate.casefold()
        if folded in ranks:
            raise ValueError(f"duplicate starting candidate {candidate}")
        ranks[folded] = rank
    return ranks


def assemble_ranking(
    *,
    candidate_cards: Path,
    decisions_path: Path,
    out_path: Path,
    audit_path: Path,
    output_count: int,
    starting_ranking: Path | None = None,
    candidate_column: str = "gene_target",
    rank_column: str = "rank",
    output_candidate_column: str = "gene_target",
) -> dict[str, int]:
    if output_count < 1:
        raise ValueError("output_count must be positive")

    cards = _read_jsonl(candidate_cards)
    comparison: dict[str, str] = {}
    origins: dict[str, str] = {}
    for row in cards:
        candidate = _candidate(row, source="candidate-card")
        folded = candidate.casefold()
        if folded in comparison:
            raise ValueError(f"duplicate candidate card for {candidate}")
        comparison[folded] = candidate
        origins[folded] = str(
            row.get("comparison_origin")
            or row.get("comparison_role")
            or "unspecified"
        ).strip()
    if len(comparison) < output_count:
        raise ValueError(
            f"comparison set has {len(comparison)} candidates, fewer than "
            f"requested output_count={output_count}"
        )

    decisions = _read_jsonl(decisions_path)
    by_candidate: dict[str, dict[str, object]] = {}
    selected: list[tuple[int, str, dict[str, object]]] = []
    for row in decisions:
        candidate = _candidate(row, source="reviewer-decision")
        folded = candidate.casefold()
        if folded not in comparison:
            raise ValueError(f"reviewer returned unknown candidate {candidate}")
        if folded in by_candidate:
            raise ValueError(f"duplicate reviewer decision for {candidate}")
        decision = str(row.get("decision") or "").strip()
        if decision not in DECISIONS:
            raise ValueError(
                f"decision for {candidate} must be selected or not_selected"
            )
        if not str(row.get("rationale") or "").strip():
            raise ValueError(f"decision for {candidate} requires a rationale")
        for field in (
            "evidence_ids",
            "supporting_evidence",
            "contradicting_evidence",
            "uncertainty",
        ):
            if not isinstance(row.get(field), list):
                raise ValueError(f"decision for {candidate} requires list {field}")
        final_rank = row.get("final_rank")
        if decision == "selected":
            if not isinstance(final_rank, int) or isinstance(final_rank, bool):
                raise ValueError(
                    f"selected candidate {candidate} requires integer final_rank"
                )
            selected.append((final_rank, comparison[folded], row))
        elif final_rank not in (None, ""):
            raise ValueError(
                f"not-selected candidate {candidate} must have null final_rank"
            )
        by_candidate[folded] = row

    missing = sorted(set(comparison) - set(by_candidate))
    if missing:
        raise ValueError(
            "reviewer did not account for every comparison candidate: "
            + ", ".join(comparison[item] for item in missing)
        )
    if len(selected) != output_count:
        raise ValueError(
            f"reviewer selected {len(selected)} candidates; expected {output_count}"
        )
    selected.sort(key=lambda item: item[0])
    observed_ranks = [rank for rank, _, _ in selected]
    expected_ranks = list(range(1, output_count + 1))
    if observed_ranks != expected_ranks:
        raise ValueError(
            "selected final_rank values must be unique and contiguous from 1 "
            f"through {output_count}"
        )

    start_ranks = _starting_ranks(
        starting_ranking,
        candidate_column=candidate_column,
        rank_column=rank_column,
    )
    movements: list[dict[str, object]] = []
    for final_rank, candidate, row in selected:
        folded = candidate.casefold()
        start_rank = start_ranks.get(folded)
        movements.append(
            {
                "candidate": candidate,
                "comparison_origin": origins[folded],
                "starting_rank": start_rank,
                "final_rank": final_rank,
                "rank_change": (
                    start_rank - final_rank if start_rank is not None else None
                ),
                "rationale": str(row["rationale"]),
            }
        )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["rank", output_candidate_column],
            delimiter="\t" if out_path.suffix.casefold() == ".tsv" else ",",
        )
        writer.writeheader()
        for final_rank, candidate, _ in selected:
            writer.writerow({"rank": final_rank, output_candidate_column: candidate})

    starting_folded = set(start_ranks)
    selected_folded = {candidate.casefold() for _, candidate, _ in selected}
    audit = {
        "schema_version": SCHEMA_VERSION,
        "status": "valid",
        "comparison_candidate_count": len(comparison),
        "selected_candidate_count": len(selected),
        "starting_result_candidate_count": len(start_ranks),
        "selected_from_starting_result": len(selected_folded & starting_folded),
        "selected_outside_starting_result": len(selected_folded - starting_folded),
        "protected_prefix_length": 0,
        "swap_limit": None,
        "movements": movements,
    }
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    audit_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
    return {
        "comparison_candidates": len(comparison),
        "selected_candidates": len(selected),
        "selected_outside_starting_result": len(selected_folded - starting_folded),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-cards", type=Path, required=True)
    parser.add_argument("--decisions", type=Path, required=True)
    parser.add_argument("--starting-ranking", type=Path)
    parser.add_argument("--output-count", type=int, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--candidate-column", default="gene_target")
    parser.add_argument("--rank-column", default="rank")
    parser.add_argument("--output-candidate-column", default="gene_target")
    args = parser.parse_args()
    summary = assemble_ranking(
        candidate_cards=args.candidate_cards,
        decisions_path=args.decisions,
        starting_ranking=args.starting_ranking,
        out_path=args.out,
        audit_path=args.audit,
        output_count=args.output_count,
        candidate_column=args.candidate_column,
        rank_column=args.rank_column,
        output_candidate_column=args.output_candidate_column,
    )
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
