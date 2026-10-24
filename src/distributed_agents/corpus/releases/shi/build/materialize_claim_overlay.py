#!/usr/bin/env python3
"""Overlay Sourceguard Findings onto the legacy Claim topology.

The overlay keeps unaffected Claim rows byte-for-byte where their Finding
content is unchanged.  For each Sourceguard Finding nominated by the semantic
reconciliation, it selects the strongest legacy Finding/Claim match and keeps
the legacy Claim identifier.  Missing Claims and Sourceguard Findings without
a legacy semantic match are omitted from the projection.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, Mapping


RELEASE_ROOT = Path(__file__).resolve().parents[1]
LEGACY_ROOT = RELEASE_ROOT.parent / "legacy_reports_v1"
CURRENT_FINDINGS = RELEASE_ROOT / "artifacts" / "ledgers" / "findings.csv"
RECONCILIATION = RELEASE_ROOT / "artifacts" / "audits" / "claim_reconciliation.jsonl"
LEGACY_CLAIMS = (
    LEGACY_ROOT / "projections" / "biokg" / "data" / "claims" / "claim_assignments.tsv"
)
LEGACY_RELATIONS = (
    LEGACY_ROOT / "projections" / "biokg" / "data" / "claims" / "claim_relations.tsv"
)
OUT_DIR = RELEASE_ROOT / "projections" / "biokg" / "data" / "claims"

ASSIGNMENT_FIELDS = (
    "claim_id",
    "doc_id",
    "member_role",
    "canonical_summary",
    "relation_family",
    "direction_pattern",
    "evidence_mode",
    "support_level",
    "de_support_level",
    "de_direction",
    "de_support_count",
    "cell_scope",
    "active_default",
    "targets",
    "readouts",
    "finding_types",
    "member_count",
    "confidence",
    "adjudication_version",
    "source_hash",
)
RELATION_FIELDS = (
    "source_claim_id",
    "target_claim_id",
    "relation_type",
    "confidence",
    "reason",
    "adjudication_version",
)

MATCH_ORDER = {
    "matched": 4,
    "partially_matched": 3,
    "superseded": 2,
    "missing_nonessential": 1,
    "missing_essential": 0,
}
CONTRIBUTION_ORDER = {"essential": 3, "supporting": 2, "nonessential": 1}
CONFIDENCE_ORDER = {"high": 3, "moderate": 2, "low": 1}
ROLE_ORDER = {"anchor": 5, "corroborating": 4, "boundary": 3, "implication": 2, "warning": 1}
DISPOSITION_ORDER = {"preserved": 2, "revised": 1, "missing": 0}


def read_delimited(path: Path, delimiter: str) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle, delimiter=delimiter)]


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def split_pipe(value: object) -> list[str]:
    return list(dict.fromkeys(part.strip() for part in str(value or "").split("|") if part.strip()))


def pipe_join(values: Iterable[object]) -> str:
    return "|".join(dict.fromkeys(str(value).strip() for value in values if str(value).strip()))


def normalize_text(value: object) -> str:
    return " ".join(str(value or "").split())


def finding_content_hash(row: Mapping[str, object]) -> str:
    fields = (
        "doc_id",
        "finding_type",
        "direction",
        "confidence",
        "literature_status",
        "summary",
        "why_it_matters",
        "genes",
        "comparators",
        "cell_types",
        "evidence_ids",
        "main_caveats",
    )
    payload = json.dumps(
        {field: normalize_text(row.get(field)) for field in fields},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def write_tsv(path: Path, rows: Iterable[Mapping[str, object]], fields: tuple[str, ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def ordered_subset(existing: object, allowed: set[str]) -> list[str]:
    allowed_casefold: dict[str, str] = {}
    for value in sorted(allowed, key=lambda item: (item.casefold(), item)):
        allowed_casefold.setdefault(value.casefold(), value)
    return [
        allowed_casefold[value.casefold()]
        for value in split_pipe(existing)
        if value.casefold() in allowed_casefold
    ]


def candidate_key(candidate: Mapping[str, object]) -> tuple:
    """Sort strongest semantic match first, then break ties deterministically."""

    return (
        -int(candidate["direct_member_match"]),
        -MATCH_ORDER.get(str(candidate["match_status"]), 0),
        -CONTRIBUTION_ORDER.get(str(candidate["contribution"]), 0),
        int(candidate["replacement_rank"]),
        -ROLE_ORDER.get(str(candidate["replacement_role"]), 0),
        -DISPOSITION_ORDER.get(str(candidate["disposition"]), 0),
        -CONFIDENCE_ORDER.get(str(candidate["confidence"]), 0),
        str(candidate["claim_id"]),
        str(candidate["legacy_doc_id"]),
    )


def main() -> None:
    current_rows = read_delimited(CURRENT_FINDINGS, ",")
    for row in current_rows:
        row["doc_id"] = f"{row['target_gene']}:{row['finding_id']}"
    current_by_doc = {row["doc_id"]: row for row in current_rows}

    legacy_rows = read_delimited(LEGACY_CLAIMS, "\t")
    legacy_by_claim: dict[str, list[dict[str, str]]] = defaultdict(list)
    legacy_by_doc: dict[str, dict[str, str]] = {}
    for row in legacy_rows:
        legacy_by_claim[row["claim_id"]].append(row)
        legacy_by_doc[row["doc_id"]] = row

    reconciliations = read_jsonl(RECONCILIATION)
    reconciliation_by_claim = {row["legacy_claim_id"]: row for row in reconciliations}
    affected_claim_ids = set(reconciliation_by_claim)

    unaffected_rows = [row.copy() for row in legacy_rows if row["claim_id"] not in affected_claim_ids]
    unaffected_docs = {row["doc_id"] for row in unaffected_rows}
    for row in unaffected_rows:
        current = current_by_doc.get(row["doc_id"])
        if current is None:
            raise ValueError(f"unaffected Claim member is absent from Sourceguard: {row['doc_id']}")
        expected_hash = finding_content_hash(current)
        if row["source_hash"] != expected_hash:
            raise ValueError(f"unaffected Claim member changed content: {row['doc_id']}")

    candidates_by_doc: dict[str, list[dict[str, object]]] = defaultdict(list)
    for claim_id, reconciliation in reconciliation_by_claim.items():
        if reconciliation["disposition"] == "missing":
            continue
        replacement_roles = {
            row["doc_id"]: row["role"] for row in reconciliation["replacement_findings"]
        }
        claim_member_docs: set[str] = set()
        for member in reconciliation["legacy_members"]:
            for rank, doc_id in enumerate(member["replacement_finding_ids"]):
                if doc_id not in replacement_roles:
                    continue
                claim_member_docs.add(doc_id)
                candidates_by_doc[doc_id].append(
                    {
                        "claim_id": claim_id,
                        "legacy_doc_id": member["legacy_doc_id"],
                        "match_status": member["match_status"],
                        "contribution": member["contribution"],
                        "replacement_rank": rank,
                        "replacement_role": replacement_roles.get(doc_id, "corroborating"),
                        "direct_member_match": 1,
                        "disposition": reconciliation["disposition"],
                        "confidence": reconciliation["confidence"],
                    }
                )
        for replacement in reconciliation["replacement_findings"]:
            doc_id = replacement["doc_id"]
            if doc_id in claim_member_docs:
                continue
            candidates_by_doc[doc_id].append(
                {
                    "claim_id": claim_id,
                    "legacy_doc_id": "",
                    "match_status": "",
                    "contribution": "",
                    "replacement_rank": 999,
                    "replacement_role": replacement["role"],
                    "direct_member_match": 0,
                    "disposition": reconciliation["disposition"],
                    "confidence": reconciliation["confidence"],
                }
            )

    unknown = sorted(set(candidates_by_doc) - set(current_by_doc))
    if unknown:
        raise ValueError(f"reconciliation references unknown Sourceguard Findings: {unknown[:8]}")

    selected_by_claim: dict[str, list[tuple[str, dict[str, object]]]] = defaultdict(list)
    shared_candidate_docs = 0
    for doc_id, candidates in sorted(candidates_by_doc.items()):
        by_claim: dict[str, list[dict[str, object]]] = defaultdict(list)
        for candidate in candidates:
            by_claim[str(candidate["claim_id"])].append(candidate)
        if len(by_claim) > 1:
            shared_candidate_docs += 1
        for claim_id, claim_candidates in by_claim.items():
            selected_by_claim[claim_id].append(
                (doc_id, sorted(claim_candidates, key=candidate_key)[0])
            )

    affected_rows: list[dict[str, str]] = []
    surviving_affected_claims: set[str] = set()
    for claim_id, selected in sorted(selected_by_claim.items()):
        reconciliation = reconciliation_by_claim[claim_id]
        legacy_members = legacy_by_claim[claim_id]
        first = legacy_members[0]
        selected.sort(key=lambda item: item[0].casefold())
        findings = [current_by_doc[doc_id] for doc_id, _ in selected]
        targets = set(row["target_gene"] for row in findings)
        finding_types = set(row["finding_type"] for row in findings)
        allowed_readouts = {
            gene for row in findings for gene in split_pipe(row.get("genes"))
        }
        allowed_cells = {
            cell for row in findings for cell in split_pipe(row.get("cell_types"))
        }
        claim_values = {
            "canonical_summary": (
                reconciliation["proposed_canonical_summary"]
                if reconciliation["disposition"] == "revised"
                else first["canonical_summary"]
            ),
            "relation_family": first["relation_family"],
            "direction_pattern": first["direction_pattern"],
            "evidence_mode": first["evidence_mode"],
            "support_level": first["support_level"],
            "de_support_level": first["de_support_level"],
            "de_direction": first["de_direction"],
            "de_support_count": first["de_support_count"],
            "cell_scope": pipe_join(ordered_subset(first["cell_scope"], allowed_cells)),
            "active_default": first["active_default"],
            "targets": pipe_join(ordered_subset(first["targets"], targets) + sorted(targets - set(split_pipe(first["targets"])), key=str.casefold)),
            "readouts": pipe_join(ordered_subset(first["readouts"], allowed_readouts)),
            "finding_types": pipe_join(ordered_subset(first["finding_types"], finding_types) + sorted(finding_types - set(split_pipe(first["finding_types"])), key=str.casefold)),
            "member_count": str(len(selected)),
            "confidence": first["confidence"],
            "adjudication_version": first["adjudication_version"],
        }
        for doc_id, candidate in selected:
            legacy_doc_id = str(candidate["legacy_doc_id"])
            member_role = (
                legacy_by_doc[legacy_doc_id]["member_role"]
                if legacy_doc_id
                else str(candidate["replacement_role"])
            )
            affected_rows.append(
                {
                    "claim_id": claim_id,
                    "doc_id": doc_id,
                    "member_role": member_role,
                    **claim_values,
                    "source_hash": finding_content_hash(current_by_doc[doc_id]),
                }
            )
        surviving_affected_claims.add(claim_id)

    expected_survivors = {
        claim_id
        for claim_id, row in reconciliation_by_claim.items()
        if row["disposition"] != "missing"
    }
    missing_survivors = sorted(expected_survivors - surviving_affected_claims)
    if missing_survivors:
        raise ValueError(f"surviving Claims lost all replacement Findings: {missing_survivors[:8]}")

    assignments = sorted(
        unaffected_rows + affected_rows,
        key=lambda row: (row["claim_id"], row["doc_id"].casefold()),
    )
    assignment_docs = [row["doc_id"] for row in assignments]
    duplicate_memberships = [
        (row["claim_id"], row["doc_id"]) for row in assignments
    ]
    duplicate_pairs = sorted(
        pair for pair, count in Counter(duplicate_memberships).items() if count > 1
    )
    if duplicate_pairs:
        raise ValueError(f"duplicate Finding membership within a Claim: {duplicate_pairs[:8]}")

    surviving_claim_ids = {row["claim_id"] for row in assignments}
    relations = [
        row
        for row in read_delimited(LEGACY_RELATIONS, "\t")
        if row["source_claim_id"] in surviving_claim_ids
        and row["target_claim_id"] in surviving_claim_ids
    ]

    write_tsv(OUT_DIR / "claim_assignments.tsv", assignments, ASSIGNMENT_FIELDS)
    write_tsv(OUT_DIR / "claim_relations.tsv", relations, RELATION_FIELDS)

    claimed_docs = set(assignment_docs)
    multi_claim_findings = sum(
        count > 1 for count in Counter(assignment_docs).values()
    )
    unclaimed = sorted(set(current_by_doc) - claimed_docs, key=str.casefold)
    summary = {
        "findings": len(current_rows),
        "claimed_findings": len(claimed_docs),
        "claim_memberships": len(assignments),
        "unclaimed_findings": len(unclaimed),
        "claims": len(surviving_claim_ids),
        "unaffected_claims": len(surviving_claim_ids - surviving_affected_claims),
        "preserved_claims": sum(row["disposition"] == "preserved" for row in reconciliations),
        "revised_claims": sum(row["disposition"] == "revised" for row in reconciliations),
        "retired_missing_claims": sum(row["disposition"] == "missing" for row in reconciliations),
        "replacement_memberships": len(affected_rows),
        "shared_replacement_findings": shared_candidate_docs,
        "multi_claim_findings": multi_claim_findings,
        "claim_relations": len(relations),
    }
    (OUT_DIR / "claim_assignments.summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
