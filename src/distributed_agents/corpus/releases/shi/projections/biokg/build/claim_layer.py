#!/usr/bin/env python3
"""Shared types and validation for the corpus-wide BioKG Claim layer.

The source ``Finding`` remains the immutable evidence unit.  A ``Claim`` is a
coarser, canonical story kernel that groups one or more findings which reach the
same biological conclusion through different report lenses.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

from ..paths import CLAIM_DATA_DIR, FINDINGS_LEDGER_FILE

DEFAULT_LEDGER = FINDINGS_LEDGER_FILE
DEFAULT_ASSIGNMENTS = CLAIM_DATA_DIR / "claim_assignments.tsv"
DEFAULT_RELATIONS = CLAIM_DATA_DIR / "claim_relations.tsv"

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
CLAIM_RELATION_FAMILIES = (
    "convergence",
    "divergence",
    "non_interchangeability",
    "epistasis",
    "ectopic",
    "uncoupling",
    "compensation",
    "cell_selectivity",
    "buffering",
    "negative_result",
    "therapeutic",
    "disease_refinement",
    "biomarker",
    "other",
)
EVIDENCE_MODES = (
    "deg",
    "signature_correlation",
    "module_or_pathway",
    "buffered_or_null",
    "literature_context",
    "mixed",
)
CLAIM_ROLES = frozenset({"anchor", "corroborating", "boundary", "implication", "warning"})
TARGET_ROLE_ORDER = {
    "anchor": 0,
    "corroborating": 1,
    "implication": 2,
    "boundary": 3,
    "warning": 4,
}
CONFIDENCE_ORDER = {"low": 0, "moderate": 1, "high": 2}
SUPPORT_ORDER = {
    "narrative_only": 0,
    "null": 1,
    "nominal": 2,
    "mixed": 3,
    "fdr_supported": 4,
}
DE_SUPPORT_LEVELS = frozenset(
    {"not_applicable", "unverified", "null", "nominal", "fdr_supported"}
)

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


def split_pipe(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        parts = [str(item).strip() for item in value]
    else:
        parts = [part.strip() for part in str(value).split("|")]
    return list(dict.fromkeys(part for part in parts if part))


def pipe_join(values: Iterable[object]) -> str:
    return "|".join(dict.fromkeys(str(value).strip() for value in values if str(value).strip()))


def normalize_text(value: object) -> str:
    return " ".join(str(value or "").split())


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: Iterable[Mapping[str, object]], fields: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for source in rows:
            writer.writerow({field: source.get(field, "") for field in fields})


def read_ledger(path: Path = DEFAULT_LEDGER) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        row["doc_id"] = f"{row['target_gene']}:{row['finding_id']}"
    return rows


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


def stable_claim_id(member_doc_ids: Iterable[str]) -> str:
    members = sorted(set(member_doc_ids), key=str.casefold)
    if not members:
        raise ValueError("a Claim requires at least one Finding")
    digest = hashlib.sha1("\n".join(members).encode("utf-8")).hexdigest()[:12]
    anchor = "".join(ch.lower() if ch.isalnum() else "_" for ch in members[0]).strip("_")
    return f"claim:{anchor[:48]}_{digest}"


def is_true(value: object) -> bool:
    return str(value).strip().casefold() in {"1", "true", "yes", "y"}


@dataclass(frozen=True)
class ClaimRecord:
    claim_id: str
    members: tuple[dict[str, str], ...]
    canonical_summary: str
    relation_family: str
    direction_pattern: str
    evidence_mode: str
    support_level: str
    de_support_level: str
    de_direction: str
    de_support_count: int
    cell_scope: tuple[str, ...]
    active_default: bool
    targets: tuple[str, ...]
    readouts: tuple[str, ...]
    finding_types: tuple[str, ...]
    confidence: str
    adjudication_version: str
    source_hash: str


def group_assignments(rows: Sequence[dict[str, str]]) -> list[ClaimRecord]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["claim_id"]].append(row)
    claims: list[ClaimRecord] = []
    for claim_id, members in sorted(grouped.items()):
        first = members[0]
        claims.append(
            ClaimRecord(
                claim_id=claim_id,
                members=tuple(sorted(members, key=lambda row: row["doc_id"].casefold())),
                canonical_summary=first["canonical_summary"],
                relation_family=first["relation_family"],
                direction_pattern=first["direction_pattern"],
                evidence_mode=first["evidence_mode"],
                support_level=first["support_level"],
                de_support_level=first["de_support_level"],
                de_direction=first["de_direction"],
                de_support_count=int(first["de_support_count"] or 0),
                cell_scope=tuple(split_pipe(first["cell_scope"])),
                active_default=is_true(first["active_default"]),
                targets=tuple(split_pipe(first["targets"])),
                readouts=tuple(split_pipe(first["readouts"])),
                finding_types=tuple(split_pipe(first["finding_types"])),
                confidence=first["confidence"],
                adjudication_version=first["adjudication_version"],
                source_hash=first["source_hash"],
            )
        )
    return claims


def claim_cards(
    assignment_rows: Sequence[dict[str, str]],
    ledger_rows: Sequence[dict[str, str]],
) -> list[dict[str, object]]:
    """Return reader-ready Claim records with their supporting Findings."""
    ledger_by_doc = {row["doc_id"]: row for row in ledger_rows}
    cards = []
    for claim in group_assignments(list(assignment_rows)):
        members = []
        genes: list[str] = []
        comparators: list[str] = []
        target_role_sets: dict[str, set[str]] = defaultdict(set)
        target_names: dict[str, str] = {}
        for assignment in claim.members:
            finding = ledger_by_doc[assignment["doc_id"]]
            target = finding["target_gene"]
            target_names.setdefault(target.casefold(), target)
            target_role_sets[target.casefold()].add(assignment["member_role"])
            for gene in split_pipe(finding.get("genes")):
                if gene.casefold() not in {target.casefold() for target in claim.targets}:
                    genes.append(gene)
            comparators.extend(split_pipe(finding.get("comparators")))
            members.append(
                {
                    "doc_id": assignment["doc_id"],
                    "member_role": assignment["member_role"],
                    "gene_target": finding["target_gene"],
                    "finding_id": finding["finding_id"],
                    "finding_type": finding["finding_type"],
                    "direction": finding["direction"],
                    "confidence": finding["confidence"],
                    "literature_status": finding["literature_status"],
                    "summary": finding["summary"],
                    "why_it_matters": finding["why_it_matters"],
                    "genes": split_pipe(finding.get("genes")),
                    "comparators": split_pipe(finding.get("comparators")),
                    "cell_types": split_pipe(finding.get("cell_types")),
                    "evidence_ids": split_pipe(finding.get("evidence_ids")),
                    "main_caveats": finding.get("main_caveats", ""),
                }
            )
        target_roles = {
            target_names[key]: sorted(roles, key=lambda role: TARGET_ROLE_ORDER[role])
            for key, roles in sorted(target_role_sets.items())
        }
        primary_anchors = [
            target for target, roles in target_roles.items() if "anchor" in roles
        ]
        if not primary_anchors:
            primary_anchors = [
                target
                for target, roles in target_roles.items()
                if not set(roles) & {"boundary", "warning", "implication"}
            ]
        supporting_targets = [
            target
            for target, roles in target_roles.items()
            if "corroborating" in roles and target not in primary_anchors
        ]
        implication_targets = [
            target
            for target, roles in target_roles.items()
            if "implication" in roles and target not in primary_anchors
        ]
        boundary_targets = [
            target
            for target, roles in target_roles.items()
            if set(roles) & {"boundary", "warning"} and target not in primary_anchors
        ]
        cards.append(
            {
                "claim_id": claim.claim_id,
                "canonical_summary": claim.canonical_summary,
                "relation_family": claim.relation_family,
                "direction_pattern": claim.direction_pattern,
                "evidence_mode": claim.evidence_mode,
                "support_level": claim.support_level,
                "de_support_level": claim.de_support_level,
                "de_direction": claim.de_direction,
                "de_support_count": claim.de_support_count,
                "cell_scope": list(claim.cell_scope),
                "active_default": claim.active_default,
                "targets": list(claim.targets),
                "readouts": list(claim.readouts),
                "finding_types": list(claim.finding_types),
                "confidence": claim.confidence,
                "member_count": len(claim.members),
                "genes": list(dict.fromkeys(genes)),
                "comparators": list(dict.fromkeys(comparators)),
                "target_roles": target_roles,
                "primary_anchors": primary_anchors,
                "co_anchors": primary_anchors if len(primary_anchors) > 1 else [],
                "supporting_targets": supporting_targets,
                "implication_targets": implication_targets,
                "boundary_targets": boundary_targets,
                "members": members,
            }
        )
    return cards


def validate_assignments(
    rows: Sequence[dict[str, str]],
    ledger_rows: Sequence[dict[str, str]],
    *,
    require_compression: bool = True,
    require_complete: bool = False,
    require_unique_membership: bool = False,
    require_stable_ids: bool = False,
) -> dict[str, object]:
    """Validate the Sourceguard compatibility overlay.

    The overlay deliberately preserves legacy Claim IDs, permits a Finding to
    support more than one retained Claim, and leaves novel Findings outside the
    Claim projection.  Callers can re-enable the original partition checks with
    the keyword flags when validating a newly induced Claim layer.
    """

    expected = {row["doc_id"]: row for row in ledger_rows}
    counts = Counter(row.get("doc_id", "") for row in rows)
    missing = sorted(set(expected) - set(counts))
    unknown = sorted(set(counts) - set(expected))
    duplicate = sorted(doc_id for doc_id, count in counts.items() if count != 1)
    if unknown or (require_complete and missing) or (require_unique_membership and duplicate):
        raise ValueError(
            "invalid Claim coverage: "
            f"missing={missing[:8]} unknown={unknown[:8]} duplicate={duplicate[:8]}"
        )

    required = set(ASSIGNMENT_FIELDS)
    for row in rows:
        absent = sorted(field for field in required if field not in row)
        if absent:
            raise ValueError(f"assignment for {row.get('doc_id')} lacks fields {absent}")
        if row["member_role"] not in CLAIM_ROLES:
            raise ValueError(f"invalid member_role for {row['doc_id']}: {row['member_role']!r}")
        if row["confidence"] not in CONFIDENCE_ORDER:
            raise ValueError(f"invalid confidence for {row['doc_id']}: {row['confidence']!r}")
        if row["relation_family"] not in CLAIM_RELATION_FAMILIES:
            raise ValueError(
                f"invalid relation_family for {row['doc_id']}: {row['relation_family']!r}"
            )
        if row["evidence_mode"] not in EVIDENCE_MODES:
            raise ValueError(
                f"invalid evidence_mode for {row['doc_id']}: {row['evidence_mode']!r}"
            )
        if row["support_level"] not in SUPPORT_ORDER:
            raise ValueError(
                f"invalid support_level for {row['doc_id']}: {row['support_level']!r}"
            )
        if row["de_support_level"] not in DE_SUPPORT_LEVELS:
            raise ValueError(
                f"invalid de_support_level for {row['doc_id']}: {row['de_support_level']!r}"
            )
        if str(row["active_default"]).casefold() not in {"true", "false"}:
            raise ValueError(
                f"invalid active_default for {row['doc_id']}: {row['active_default']!r}"
            )
        if not row["canonical_summary"].strip():
            raise ValueError(f"empty canonical_summary for {row['doc_id']}")
        expected_hash = finding_content_hash(expected[row["doc_id"]])
        if row["source_hash"] != expected_hash:
            raise ValueError(f"stale Claim assignment for {row['doc_id']}")

    claims = group_assignments(list(rows))
    if require_compression and len(claims) >= len(ledger_rows):
        raise ValueError(
            f"Claim layer did not compress Findings: {len(claims)} claims for {len(ledger_rows)} findings"
        )
    for claim in claims:
        expected_count = len(claim.members)
        expected_claim_id = stable_claim_id(member["doc_id"] for member in claim.members)
        if require_stable_ids and claim.claim_id != expected_claim_id:
            raise ValueError(
                f"unstable claim_id for {claim.claim_id}: expected {expected_claim_id}"
            )
        values = {int(member["member_count"]) for member in claim.members}
        if values != {expected_count}:
            raise ValueError(f"member_count mismatch for {claim.claim_id}: {values} != {expected_count}")
        invariant_fields = (
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
            "confidence",
            "adjudication_version",
        )
        for field in invariant_fields:
            values = {member[field] for member in claim.members}
            if len(values) != 1:
                raise ValueError(f"Claim-level field {field} differs within {claim.claim_id}")
        member_findings = [expected[member["doc_id"]] for member in claim.members]
        expected_targets = {row["target_gene"].casefold() for row in member_findings}
        if {value.casefold() for value in claim.targets} != expected_targets:
            raise ValueError(f"target set mismatch for {claim.claim_id}")
        expected_types = {row["finding_type"] for row in member_findings}
        if set(claim.finding_types) != expected_types:
            raise ValueError(f"finding_type set mismatch for {claim.claim_id}")
        allowed_readouts = {
            gene.casefold() for row in member_findings for gene in split_pipe(row.get("genes"))
        }
        if any(readout.casefold() not in allowed_readouts for readout in claim.readouts):
            raise ValueError(f"readout outside member evidence for {claim.claim_id}")
        allowed_cells = {
            cell for row in member_findings for cell in split_pipe(row.get("cell_types"))
        }
        if any(cell not in allowed_cells for cell in claim.cell_scope):
            raise ValueError(f"cell scope outside member evidence for {claim.claim_id}")

    return {
        "findings": len(ledger_rows),
        "claimed_findings": len(counts),
        "unclaimed_findings": len(missing),
        "claim_memberships": len(rows),
        "multi_claim_findings": sum(count > 1 for count in counts.values()),
        "claims": len(claims),
        "compressed_findings": len(counts) - len(claims),
        "multi_finding_claims": sum(len(claim.members) > 1 for claim in claims),
        "finding_types": dict(sorted(Counter(row["finding_type"] for row in ledger_rows).items())),
        "relation_families": dict(sorted(Counter(claim.relation_family for claim in claims).items())),
        "active_default": sum(claim.active_default for claim in claims),
    }


def annotate_de_support(
    assignment_rows: list[dict[str, object]], parquet_path: Path
) -> dict[str, object]:
    """Cross-check Claim target/readout pairs against the raw DE parquet."""
    if not parquet_path.exists():
        raise FileNotFoundError(parquet_path)
    by_claim: dict[str, dict[str, object]] = {}
    assignments_by_claim: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in assignment_rows:
        claim_id = str(row["claim_id"])
        by_claim.setdefault(claim_id, row)
        assignments_by_claim[claim_id].append(row)
    requests = []
    for claim_id, row in by_claim.items():
        # Treat the raw table as an independent cross-check, not as something
        # implied by the semantic evidence_mode label. Mixed-evidence Claims
        # can still have a concrete target/readout DEG result, and retaining it
        # is useful downstream so long as it stays in the separate ``de_*``
        # fields.
        cells = split_pipe(row["cell_scope"]) or [""]
        for target in split_pipe(row["targets"]):
            for readout in split_pipe(row["readouts"]):
                for cell in cells:
                    requests.append((claim_id, target, readout, cell))
    requests = sorted(set(requests))

    import duckdb

    con = duckdb.connect(database=":memory:")
    try:
        con.execute(
            "CREATE TEMP TABLE claim_requests "
            "(claim_id VARCHAR, target_gene VARCHAR, readout VARCHAR, cell_type VARCHAR)"
        )
        if requests:
            con.executemany("INSERT INTO claim_requests VALUES (?, ?, ?, ?)", requests)
        rows = con.execute(
            """SELECT q.claim_id,
                      CAST(p.logfoldchanges AS DOUBLE) AS logfc,
                      CAST(p.pvals_adj AS DOUBLE) AS fdr
               FROM claim_requests q
               JOIN read_parquet(?) p
                 ON lower(p.gene_target) = lower(q.target_gene)
                AND lower(p.names) = lower(q.readout)
                AND (q.cell_type = '' OR p.group_name = q.cell_type)""",
            [str(parquet_path)],
        ).fetchall()
    finally:
        con.close()

    support: dict[str, list[tuple[float, float]]] = defaultdict(list)
    for claim_id, logfc, fdr in rows:
        if logfc is not None and fdr is not None:
            support[str(claim_id)].append((float(logfc), float(fdr)))
    for claim_id, source in by_claim.items():
        if not split_pipe(source["targets"]) or not split_pipe(source["readouts"]):
            level, direction, count = "not_applicable", "", 0
        else:
            observed = support.get(claim_id, [])
            fdr_hits = [(logfc, fdr) for logfc, fdr in observed if fdr < 0.05]
            nominal = [(logfc, fdr) for logfc, fdr in observed if fdr < 0.1]
            selected = fdr_hits or nominal
            if fdr_hits:
                level = "fdr_supported"
            elif nominal:
                level = "nominal"
            elif observed:
                level = "null"
            else:
                level = "unverified"
            directions = {"up" if logfc > 0 else "down" for logfc, _ in selected if logfc != 0}
            direction = next(iter(directions)) if len(directions) == 1 else ("mixed" if directions else "")
            count = len(selected)
        for row in assignments_by_claim[claim_id]:
            row["de_support_level"] = level
            row["de_direction"] = direction
            row["de_support_count"] = count
    return {
        "de_requests": len(requests),
        "de_claims": len({claim_id for claim_id, *_ in requests}),
        "de_verified": sum(
            row.get("de_support_level") in {"fdr_supported", "nominal", "null"}
            for row in by_claim.values()
        ),
    }


def validate_relations(rows: Sequence[dict[str, str]], claim_ids: set[str]) -> None:
    allowed = {"QUALIFIES", "CONTRASTS_WITH", "IMPLICATION_OF", "REVIEW_WITH"}
    seen: set[tuple[str, str, str]] = set()
    for row in rows:
        source = row.get("source_claim_id", "")
        target = row.get("target_claim_id", "")
        relation_type = row.get("relation_type", "")
        if source not in claim_ids or target not in claim_ids:
            raise ValueError(f"Claim relation references an unknown Claim: {source} -> {target}")
        if source == target:
            raise ValueError(f"self Claim relation is not allowed: {source}")
        if relation_type not in allowed:
            raise ValueError(f"invalid Claim relation type: {relation_type!r}")
        key = (source, target, relation_type)
        if key in seen:
            raise ValueError(f"duplicate Claim relation: {key}")
        seen.add(key)
