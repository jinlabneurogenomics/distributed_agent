"""Indexes over the Shi Claim layer."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from typing import Any, Mapping

from .binding import ReleaseBinding
from .errors import CorpusToolError


COMPATIBILITY_CLAIM_ARTIFACTS = frozenset(
    {"findings", "claim_assignments", "claim_relations"}
)
FINDING_LIST_FIELDS = frozenset(
    {"genes", "comparators", "cell_types", "evidence_ids", "ref_ids"}
)
CLAIM_LIST_FIELDS = frozenset({"targets", "readouts", "finding_types"})
CLAIM_METADATA_FIELDS = (
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
)


def _read_table(path: Path, *, delimiter: str) -> list[dict[str, str]]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle, delimiter=delimiter)
            if reader.fieldnames is None:
                raise CorpusToolError(f"declared artifact has no header: {path.name}")
            return [dict(row) for row in reader]
    except (OSError, UnicodeError, csv.Error) as exc:
        raise CorpusToolError(f"cannot read declared artifact {path.name}: {exc}") from exc


def _split_pipe(value: str | None) -> list[str]:
    return [item for item in str(value or "").split("|") if item]


def _as_int(value: str | None, *, field: str) -> int:
    try:
        return int(str(value or "0"))
    except ValueError as exc:
        raise CorpusToolError(f"invalid integer in compatibility Claim {field}") from exc


def _as_bool(value: str | None, *, field: str) -> bool:
    folded = str(value or "").casefold()
    if folded in {"true", "1", "yes"}:
        return True
    if folded in {"false", "0", "no"}:
        return False
    raise CorpusToolError(f"invalid boolean in compatibility Claim {field}")


def _gene_key(value: str) -> str:
    return value.strip().casefold()


class CompatibilityClaimIndex:
    """Lazy in-memory view of Shi Findings, Claims, and Claim relations."""

    def __init__(self, release: ReleaseBinding) -> None:
        missing = sorted(COMPATIBILITY_CLAIM_ARTIFACTS - release.artifact_names)
        if missing:
            raise CorpusToolError(
                "selected release has no compatible Claim layer: "
                + ", ".join(missing)
            )

        findings = self._load_findings(release.artifact("findings"))
        assignments = _read_table(
            release.artifact("claim_assignments"), delimiter="\t"
        )
        relations = _read_table(release.artifact("claim_relations"), delimiter="\t")

        self.findings_by_doc = {str(row["doc_id"]): row for row in findings}
        self.findings_by_doc_key = {
            str(row["doc_id"]).casefold(): row for row in findings
        }
        if len(self.findings_by_doc) != len(findings):
            raise CorpusToolError(
                "compatibility Claim index found duplicate Finding doc IDs"
            )

        self.target_symbols: dict[str, str] = {}
        self.findings_by_target: defaultdict[str, list[dict[str, Any]]] = (
            defaultdict(list)
        )
        for finding in findings:
            target = str(finding["target_gene"])
            target_key = _gene_key(target)
            self.target_symbols.setdefault(target_key, target)
            self.findings_by_target[target_key].append(finding)
        for rows in self.findings_by_target.values():
            rows.sort(key=lambda row: str(row["doc_id"]).casefold())

        self.claims_by_id: dict[str, dict[str, Any]] = {}
        self.claims_by_id_key: dict[str, dict[str, Any]] = {}
        self.memberships_by_claim: defaultdict[str, list[dict[str, Any]]] = (
            defaultdict(list)
        )
        self.memberships_by_finding: defaultdict[str, list[dict[str, Any]]] = (
            defaultdict(list)
        )
        self.claim_ids_by_target: defaultdict[str, set[str]] = defaultdict(set)

        for row in assignments:
            claim_id = str(row.get("claim_id") or "").strip()
            doc_id = str(row.get("doc_id") or "").strip()
            role = str(row.get("member_role") or "").strip()
            if not claim_id or not doc_id or not role:
                raise CorpusToolError(
                    "compatibility Claim membership is missing claim_id, doc_id, or member_role"
                )
            finding = self.findings_by_doc.get(doc_id)
            if finding is None:
                raise CorpusToolError(
                    f"compatibility Claim membership references unknown Finding: {doc_id}"
                )
            claim = self._claim_from_assignment(row)
            existing = self.claims_by_id.get(claim_id)
            if existing is None:
                self.claims_by_id[claim_id] = claim
                self.claims_by_id_key[claim_id.casefold()] = claim
            else:
                for field in CLAIM_METADATA_FIELDS:
                    if existing[field] != claim[field]:
                        raise CorpusToolError(
                            f"inconsistent compatibility Claim metadata: {claim_id}.{field}"
                        )

            target = str(finding["target_gene"])
            target_key = _gene_key(target)
            membership = {
                "claim_id": claim_id,
                "finding_doc_id": doc_id,
                "target_gene": target,
                "finding_id": finding["finding_id"],
                "member_role": role,
                "source_hash": str(row.get("source_hash") or ""),
            }
            self.memberships_by_claim[claim_id].append(membership)
            self.memberships_by_finding[doc_id].append(membership)
            self.claim_ids_by_target[target_key].add(claim_id)

        for claim_id, claim in self.claims_by_id.items():
            memberships = self.memberships_by_claim[claim_id]
            memberships.sort(
                key=lambda row: (
                    str(row["target_gene"]).casefold(),
                    str(row["finding_doc_id"]).casefold(),
                )
            )
            target_genes = sorted(
                {str(row["target_gene"]) for row in memberships}, key=str.casefold
            )
            claim["target_genes"] = target_genes
            claim["membership_count"] = len(memberships)
            if claim["member_count"] != len(memberships):
                raise CorpusToolError(
                    f"compatibility Claim member count mismatch: {claim_id}"
                )
        for memberships in self.memberships_by_finding.values():
            memberships.sort(key=lambda row: str(row["claim_id"]))

        self.relations: list[dict[str, Any]] = []
        self.relations_by_claim: defaultdict[str, list[dict[str, Any]]] = (
            defaultdict(list)
        )
        seen_relations: set[tuple[str, str, str]] = set()
        for row in relations:
            source_id = str(row.get("source_claim_id") or "").strip()
            target_id = str(row.get("target_claim_id") or "").strip()
            relation_type = str(row.get("relation_type") or "").strip()
            if source_id not in self.claims_by_id or target_id not in self.claims_by_id:
                raise CorpusToolError(
                    "compatibility Claim relation references an unknown Claim"
                )
            identity = (source_id, target_id, relation_type)
            if identity in seen_relations:
                raise CorpusToolError(
                    "compatibility Claim index found a duplicate typed relation"
                )
            seen_relations.add(identity)
            relation = {
                "source_claim_id": source_id,
                "target_claim_id": target_id,
                "relation_type": relation_type,
                "confidence": str(row.get("confidence") or ""),
                "reason": str(row.get("reason") or ""),
                "adjudication_version": str(row.get("adjudication_version") or ""),
            }
            self.relations.append(relation)
            self.relations_by_claim[source_id].append(relation)
            self.relations_by_claim[target_id].append(relation)
        self.relations.sort(key=self._relation_sort_key)
        for rows in self.relations_by_claim.values():
            rows.sort(key=self._relation_sort_key)

        self.claim_relation_outbound: defaultdict[
            str, defaultdict[str, list[dict[str, Any]]]
        ] = defaultdict(lambda: defaultdict(list))
        for relation in self.relations:
            source_targets = self.claim_target_keys(relation["source_claim_id"])
            target_targets = self.claim_target_keys(relation["target_claim_id"])
            for source_key in source_targets:
                for target_key in target_targets:
                    if source_key != target_key:
                        self.claim_relation_outbound[source_key][target_key].append(
                            relation
                        )

        self.explicit_outbound: defaultdict[
            str, defaultdict[str, list[dict[str, Any]]]
        ] = defaultdict(lambda: defaultdict(list))
        for finding in findings:
            source_key = _gene_key(str(finding["target_gene"]))
            seen: set[str] = set()
            for comparator in finding["comparators"]:
                comparator_key = _gene_key(str(comparator))
                if (
                    not comparator_key
                    or comparator_key == source_key
                    or comparator_key in seen
                    or comparator_key not in self.target_symbols
                ):
                    continue
                seen.add(comparator_key)
                self.explicit_outbound[source_key][comparator_key].append(finding)
        for targets in self.explicit_outbound.values():
            for rows in targets.values():
                rows.sort(key=lambda row: str(row["doc_id"]).casefold())

        self.counts = {
            "findings": len(findings),
            "claims": len(self.claims_by_id),
            "claim_memberships": len(assignments),
            "claimed_findings": len(self.memberships_by_finding),
            "unclaimed_findings": len(findings) - len(self.memberships_by_finding),
            "claim_relations": len(self.relations),
        }

    @staticmethod
    def _load_findings(path: Path) -> list[dict[str, Any]]:
        rows = _read_table(path, delimiter=",")
        findings: list[dict[str, Any]] = []
        for row in rows:
            target = str(row.get("target_gene") or "").strip()
            finding_id = str(row.get("finding_id") or "").strip()
            if not target or not finding_id:
                raise CorpusToolError(
                    "Claim-member Finding is missing target_gene or finding_id"
                )
            finding: dict[str, Any] = dict(row)
            finding["doc_id"] = f"{target}:{finding_id}"
            for field in FINDING_LIST_FIELDS:
                finding[field] = _split_pipe(row.get(field))
            for field in ("n_genes", "n_cell_types"):
                if field in finding and str(finding[field]).strip():
                    finding[field] = _as_int(str(finding[field]), field=field)
            findings.append(finding)
        return findings

    @staticmethod
    def _claim_from_assignment(row: Mapping[str, str]) -> dict[str, Any]:
        claim: dict[str, Any] = {
            "claim_id": str(row.get("claim_id") or ""),
            "canonical_summary": str(row.get("canonical_summary") or ""),
            "relation_family": str(row.get("relation_family") or ""),
            "direction_pattern": str(row.get("direction_pattern") or ""),
            "evidence_mode": str(row.get("evidence_mode") or ""),
            "support_level": str(row.get("support_level") or ""),
            "de_support_level": str(row.get("de_support_level") or ""),
            "de_direction": str(row.get("de_direction") or ""),
            "de_support_count": _as_int(
                row.get("de_support_count"), field="de_support_count"
            ),
            "cell_scope": str(row.get("cell_scope") or ""),
            "active_default": _as_bool(
                row.get("active_default"), field="active_default"
            ),
            "member_count": _as_int(row.get("member_count"), field="member_count"),
            "confidence": str(row.get("confidence") or ""),
            "adjudication_version": str(row.get("adjudication_version") or ""),
        }
        for field in CLAIM_LIST_FIELDS:
            claim[field] = _split_pipe(row.get(field))
        return claim

    @staticmethod
    def _relation_sort_key(row: Mapping[str, Any]) -> tuple[str, str, str]:
        return (
            str(row["source_claim_id"]),
            str(row["target_claim_id"]),
            str(row["relation_type"]),
        )

    def canonical_target(self, value: str) -> tuple[str, str]:
        key = _gene_key(value)
        return key, self.target_symbols.get(key, value.strip())

    def claim_target_keys(self, claim_id: str) -> set[str]:
        return {
            _gene_key(str(value))
            for value in self.claims_by_id[claim_id].get("target_genes") or []
        }

    @staticmethod
    def finding_card(finding: Mapping[str, Any]) -> dict[str, Any]:
        return {
            key: finding.get(key)
            for key in (
                "doc_id",
                "target_gene",
                "finding_id",
                "finding_type",
                "summary",
                "why_it_matters",
                "direction",
                "confidence",
                "main_caveats",
                "comparators",
                "evidence_ids",
                "ref_ids",
            )
        }

    @staticmethod
    def finding_path_id_card(finding: Mapping[str, Any]) -> dict[str, Any]:
        return {
            "finding_doc_id": finding.get("doc_id"),
            "finding_type": finding.get("finding_type"),
        }

    @staticmethod
    def claim_card(claim: Mapping[str, Any]) -> dict[str, Any]:
        return {
            key: claim.get(key)
            for key in (
                "claim_id",
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
                "target_genes",
                "membership_count",
                "confidence",
                "adjudication_version",
            )
        }

    @staticmethod
    def membership_card(membership: Mapping[str, Any]) -> dict[str, Any]:
        return {
            key: membership.get(key)
            for key in (
                "finding_doc_id",
                "target_gene",
                "finding_id",
                "member_role",
                "source_hash",
            )
        }

    @staticmethod
    def relation_card(relation: Mapping[str, Any]) -> dict[str, Any]:
        return {
            key: relation.get(key)
            for key in (
                "source_claim_id",
                "target_claim_id",
                "relation_type",
                "confidence",
                "reason",
                "adjudication_version",
            )
        }
