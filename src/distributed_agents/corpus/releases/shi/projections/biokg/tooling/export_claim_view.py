#!/usr/bin/env python3
"""Export canonical BioKG Claim cards for retrieval or synthesis."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from ..build.claim_layer import (
    DEFAULT_ASSIGNMENTS,
    DEFAULT_LEDGER,
    RELATIONAL_FAMILIES,
    claim_cards,
    read_ledger,
    read_tsv,
    validate_assignments,
)


def filter_cards(cards: list[dict], scope: str) -> list[dict]:
    if scope == "all":
        return cards
    if scope == "default":
        return [card for card in cards if card["active_default"]]
    return [
        card
        for card in cards
        if card["active_default"] and card["relation_family"] in RELATIONAL_FAMILIES
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assignments", type=Path, default=DEFAULT_ASSIGNMENTS)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--scope", choices=["relational", "default", "all"], default="relational")
    parser.add_argument("--out", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ledger = read_ledger(args.ledger)
    assignments = read_tsv(args.assignments)
    validate_assignments(assignments, ledger)
    cards = filter_cards(claim_cards(assignments, ledger), args.scope)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.out.suffix == ".jsonl":
        with args.out.open("w", encoding="utf-8") as handle:
            for card in cards:
                handle.write(json.dumps(card, ensure_ascii=False, sort_keys=True) + "\n")
    elif args.out.suffix == ".csv":
        fields = [
            "claim_id",
            "canonical_summary",
            "relation_family",
            "direction_pattern",
            "evidence_mode",
            "support_level",
            "de_support_level",
            "de_direction",
            "de_support_count",
            "active_default",
            "targets",
            "readouts",
            "finding_types",
            "member_count",
            "confidence",
        ]
        with args.out.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            for card in cards:
                row = dict(card)
                for field in ("targets", "readouts", "finding_types"):
                    row[field] = "|".join(row[field])
                writer.writerow({field: row.get(field, "") for field in fields})
    else:
        args.out.write_text(json.dumps(cards, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {
                "scope": args.scope,
                "claims": len(cards),
                "findings": sum(card["member_count"] for card in cards),
                "out": str(args.out),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
