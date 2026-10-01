"""In-memory indexes over bottom-up Claim and Finding ledgers."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Mapping

from .binding import ReleaseBinding
from .constants import CLAIM_GRAPH_ARTIFACTS, CLAIM_ROLES
from .errors import CorpusToolError


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        with path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                row = json.loads(line)
                if not isinstance(row, dict):
                    raise CorpusToolError(
                        f"{path.name}:{line_number}: expected a JSON object"
                    )
                rows.append(row)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise CorpusToolError(f"cannot read declared artifact {path.name}: {exc}") from exc
    return rows


def _gene_key(value: str) -> str:
    return value.strip().casefold()


def _stable_hash_key(namespace: str, value: str) -> tuple[str, str]:
    digest = hashlib.sha256(f"{namespace}\0{value}".encode()).hexdigest()
    return digest, value


class ClaimGraphIndex:
    """Lazy in-memory index over the frozen bottom-up Claim and Finding ledgers."""

    def __init__(self, release: ReleaseBinding) -> None:
        missing = sorted(CLAIM_GRAPH_ARTIFACTS - release.artifact_names)
        if missing:
            raise CorpusToolError(
                "selected release has no bottom-up Claim graph artifacts: "
                + ", ".join(missing)
            )

        findings = _read_jsonl(release.artifact("findings"))
        claims = _read_jsonl(release.artifact("claims"))
        contributions = _read_jsonl(release.artifact("claim_contributions"))
        dispositions = _read_jsonl(release.artifact("finding_claim_dispositions"))

        self.findings_by_doc = {
            str(row["doc_id"]): row for row in findings
        }
        self.findings_by_doc_key = {
            str(row["doc_id"]).casefold(): row for row in findings
        }
        self.claims_by_id = {
            str(row["claim_id"]): row for row in claims
        }
        self.dispositions_by_doc = {
            str(row["finding_doc_id"]): row for row in dispositions
        }
        if len(self.findings_by_doc) != len(findings):
            raise CorpusToolError("bottom-up Claim index found duplicate Finding doc IDs")
        if len(self.claims_by_id) != len(claims):
            raise CorpusToolError("bottom-up Claim index found duplicate Claim IDs")

        self.target_symbols: dict[str, str] = {}
        self.findings_by_target: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
        for finding in findings:
            target = str(finding["target_gene"])
            key = _gene_key(target)
            self.target_symbols.setdefault(key, target)
            self.findings_by_target[key].append(finding)
        for rows in self.findings_by_target.values():
            rows.sort(key=lambda row: str(row["doc_id"]))

        self.contributions_by_claim: defaultdict[str, list[dict[str, Any]]] = (
            defaultdict(list)
        )
        self.contributions_by_finding: defaultdict[str, list[dict[str, Any]]] = (
            defaultdict(list)
        )
        self.claim_ids_by_target: defaultdict[str, set[str]] = defaultdict(set)
        for contribution in contributions:
            claim_id = str(contribution["claim_id"])
            finding_doc_id = str(contribution["finding_doc_id"])
            if claim_id not in self.claims_by_id:
                raise CorpusToolError(f"unresolved Claim contribution: {claim_id}")
            if finding_doc_id not in self.findings_by_doc:
                raise CorpusToolError(
                    f"unresolved Finding contribution: {finding_doc_id}"
                )
            role = str(contribution["role"])
            if role not in CLAIM_ROLES:
                raise CorpusToolError(f"unsupported Claim contribution role: {role}")
            self.contributions_by_claim[claim_id].append(contribution)
            self.contributions_by_finding[finding_doc_id].append(contribution)
            target_key = _gene_key(str(contribution["target_gene"]))
            self.claim_ids_by_target[target_key].add(claim_id)
        for rows in self.contributions_by_claim.values():
            rows.sort(key=lambda row: str(row["contribution_id"]))
        for rows in self.contributions_by_finding.values():
            rows.sort(key=lambda row: str(row["contribution_id"]))

        self.explicit_outbound: defaultdict[
            str, defaultdict[str, list[dict[str, Any]]]
        ] = defaultdict(lambda: defaultdict(list))
        for finding in findings:
            source_key = _gene_key(str(finding["target_gene"]))
            comparators = finding.get("comparators") or []
            if not isinstance(comparators, list):
                raise CorpusToolError(
                    f"Finding {finding['doc_id']} has a non-list comparators field"
                )
            seen: set[str] = set()
            for comparator in comparators:
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
                rows.sort(key=lambda row: str(row["doc_id"]))

        disposition_counts = Counter(
            str(row.get("disposition") or "") for row in dispositions
        )
        self.counts = {
            "claims": len(claims),
            "claim_contributions": len(contributions),
            "findings": len(findings),
            "findings_with_claim_contributions": len(self.contributions_by_finding),
            "findings_without_claim_contributions": (
                len(findings) - len(self.contributions_by_finding)
            ),
            "finding_dispositions": dict(sorted(disposition_counts.items())),
        }

    def canonical_target(self, value: str) -> tuple[str, str]:
        key = _gene_key(value)
        return key, self.target_symbols.get(key, value.strip())

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
                "direction",
                "confidence",
                "main_caveats",
                "comparators",
                "evidence_ids",
                "ref_ids",
            )
        }

    @staticmethod
    def claim_card(claim: Mapping[str, Any]) -> dict[str, Any]:
        return {
            key: claim.get(key)
            for key in (
                "claim_id",
                "statement",
                "scope",
                "higher_order_basis",
                "confidence",
                "target_genes",
                "contribution_count",
            )
        }

    @staticmethod
    def contribution_card(contribution: Mapping[str, Any]) -> dict[str, Any]:
        return {
            key: contribution.get(key)
            for key in (
                "contribution_id",
                "claim_id",
                "finding_doc_id",
                "target_gene",
                "finding_id",
                "role",
                "rationale",
            )
        }

