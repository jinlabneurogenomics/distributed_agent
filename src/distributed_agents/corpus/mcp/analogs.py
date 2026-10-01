"""Read-only access to the release-frozen target-analog annotation index."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Iterable, Mapping
from urllib.parse import quote

from .binding import ReleaseBinding
from .errors import CorpusToolError


TARGET_ANALOG_ARTIFACT = "gene_analog_index"
SCHEMA_VERSION = "distributed_agents-gene-analog-index-v1"
TIER_RANK = {
    "exact_complex_or_paralog": 10,
    "bidirectional_corpus_comparator": 20,
    "narrow_module": 30,
    "direct_interaction_or_dependency": 40,
    "broad_functional_fallback": 50,
}


def _gene_key(value: str) -> str:
    return value.strip().casefold()


def _is_control(value: str) -> bool:
    folded = _gene_key(value)
    return folded == "non_target" or folded.startswith("safe_target_")


class GeneAnalogIndex:
    """Query typed curated relationships without loading the full store."""

    def __init__(self, release: ReleaseBinding) -> None:
        if TARGET_ANALOG_ARTIFACT not in release.artifact_names:
            raise CorpusToolError(
                "selected release does not declare target-analog grounding"
            )
        self.path = release.artifact(TARGET_ANALOG_ARTIFACT)
        self._metadata = self._read_metadata()
        if self._metadata.get("schema_version") != SCHEMA_VERSION:
            raise CorpusToolError("unsupported target-analog index schema")

    def _connect(self) -> sqlite3.Connection:
        path = Path(self.path).resolve()
        connection = sqlite3.connect(
            f"file:{quote(str(path))}?mode=ro", uri=True
        )
        connection.row_factory = sqlite3.Row
        return connection

    def _read_metadata(self) -> dict[str, str]:
        try:
            with self._connect() as connection:
                rows = connection.execute(
                    "SELECT key, value FROM metadata ORDER BY key"
                ).fetchall()
        except sqlite3.Error as exc:
            raise CorpusToolError(
                f"target-analog index is unreadable: {exc}"
            ) from exc
        return {str(row["key"]): str(row["value"]) for row in rows}

    @property
    def metadata(self) -> dict[str, Any]:
        result: dict[str, Any] = dict(self._metadata)
        for field in (
            "taxonomy_id",
            "gene_count",
            "set_count",
            "membership_count",
            "relationship_count",
        ):
            if field in result:
                result[field] = int(result[field])
        return result

    def resolve_symbols(
        self, values: Iterable[str]
    ) -> tuple[dict[str, str], list[str]]:
        requested = list(values)
        keys = sorted({_gene_key(value) for value in requested if value.strip()})
        if not keys:
            return {}, []
        resolved: dict[str, str] = {}
        try:
            with self._connect() as connection:
                for start in range(0, len(keys), 500):
                    batch = keys[start : start + 500]
                    placeholders = ",".join("?" for _ in batch)
                    rows = connection.execute(
                        f"SELECT symbol_key, symbol FROM genes "
                        f"WHERE symbol_key IN ({placeholders})",
                        batch,
                    ).fetchall()
                    resolved.update(
                        {str(row["symbol_key"]): str(row["symbol"]) for row in rows}
                    )
        except sqlite3.Error as exc:
            raise CorpusToolError(
                f"target-analog symbol resolution failed: {exc}"
            ) from exc
        unresolved = [value for value in requested if _gene_key(value) not in resolved]
        return resolved, unresolved

    def query(
        self,
        *,
        target: str,
        eligible_symbols: Iterable[str],
        include_broad_fallback: bool,
        source_limit: int,
    ) -> dict[str, dict[str, Any]]:
        target_key = _gene_key(target)
        eligible_keys = {
            _gene_key(value)
            for value in eligible_symbols
            if value.strip() and not _is_control(value)
        }
        eligible_keys.discard(target_key)
        if not eligible_keys:
            return {}

        candidates: dict[str, dict[str, Any]] = {}
        try:
            with self._connect() as connection:
                target_row = connection.execute(
                    "SELECT id, symbol FROM genes WHERE symbol_key = ?", (target_key,)
                ).fetchone()
                if target_row is None:
                    return {}
                connection.execute(
                    "CREATE TEMP TABLE eligible (gene_id INTEGER PRIMARY KEY)"
                )
                for start in range(0, len(eligible_keys), 500):
                    batch = sorted(eligible_keys)[start : start + 500]
                    placeholders = ",".join("?" for _ in batch)
                    rows = connection.execute(
                        f"SELECT id FROM genes WHERE symbol_key IN ({placeholders})",
                        batch,
                    ).fetchall()
                    connection.executemany(
                        "INSERT OR IGNORE INTO eligible VALUES (?)",
                        ((int(row["id"]),) for row in rows),
                    )

                broad_clause = (
                    ""
                    if include_broad_fallback
                    else "AND annotation_sets.tier != 'broad_functional_fallback'"
                )
                memberships = connection.execute(
                    f"""
                    SELECT candidate.symbol AS candidate,
                           annotation_sets.tier AS tier,
                           annotation_sets.tier_rank AS tier_rank,
                           annotation_sets.relationship_type AS relationship_type,
                           annotation_sets.resource AS resource,
                           annotation_sets.source_id AS source_id,
                           annotation_sets.set_name AS label,
                           annotation_sets.assignment_basis AS assignment_basis,
                           annotation_sets.member_count AS member_count,
                           annotation_sets.metadata_json AS metadata_json,
                           target_membership.source_gene AS target_source_gene,
                           candidate_membership.source_gene AS candidate_source_gene
                    FROM memberships AS target_membership
                    JOIN annotation_sets
                      ON annotation_sets.id = target_membership.set_id
                    JOIN memberships AS candidate_membership
                      ON candidate_membership.set_id = annotation_sets.id
                    JOIN eligible
                      ON eligible.gene_id = candidate_membership.gene_id
                    JOIN genes AS candidate
                      ON candidate.id = candidate_membership.gene_id
                    WHERE target_membership.gene_id = ?
                      AND candidate_membership.gene_id != ?
                      {broad_clause}
                    ORDER BY candidate.symbol_key,
                             annotation_sets.tier_rank,
                             annotation_sets.relationship_type,
                             annotation_sets.resource,
                             annotation_sets.source_id
                    """,
                    (int(target_row["id"]), int(target_row["id"])),
                )
                for row in memberships:
                    metadata = json.loads(str(row["metadata_json"]))
                    source = {
                        "kind": "curated_annotation",
                        "resource": str(row["resource"]),
                        "source_id": str(row["source_id"]),
                        "label": str(row["label"]),
                        "set_member_count": int(row["member_count"]),
                        "tier_assignment_basis": str(row["assignment_basis"]),
                        **metadata,
                    }
                    if str(row["target_source_gene"]):
                        source["target_source_gene"] = str(
                            row["target_source_gene"]
                        )
                    if str(row["candidate_source_gene"]):
                        source["candidate_source_gene"] = str(
                            row["candidate_source_gene"]
                        )
                    self._add_source(
                        candidates,
                        candidate=str(row["candidate"]),
                        tier=str(row["tier"]),
                        tier_rank=int(row["tier_rank"]),
                        relationship_type=str(row["relationship_type"]),
                        source=source,
                        source_limit=source_limit,
                    )

                relationships = connection.execute(
                    """
                    SELECT candidate.symbol AS candidate,
                           relationships.tier AS tier,
                           relationships.tier_rank AS tier_rank,
                           relationships.relationship_type AS relationship_type,
                           relationships.resource AS resource,
                           relationships.source_id AS source_id,
                           relationships.label AS label,
                           relationships.metadata_json AS metadata_json
                    FROM relationships
                    JOIN genes AS candidate
                      ON candidate.id = CASE
                          WHEN relationships.gene_a_id = ?
                          THEN relationships.gene_b_id
                          ELSE relationships.gene_a_id
                      END
                    JOIN eligible ON eligible.gene_id = candidate.id
                    WHERE relationships.gene_a_id = ?
                       OR relationships.gene_b_id = ?
                    ORDER BY candidate.symbol_key,
                             relationships.tier_rank,
                             relationships.relationship_type,
                             relationships.resource,
                             relationships.source_id
                    """,
                    (
                        int(target_row["id"]),
                        int(target_row["id"]),
                        int(target_row["id"]),
                    ),
                )
                for row in relationships:
                    source = {
                        "kind": "curated_annotation",
                        "resource": str(row["resource"]),
                        "source_id": str(row["source_id"]),
                        "label": str(row["label"]),
                        **json.loads(str(row["metadata_json"])),
                    }
                    self._add_source(
                        candidates,
                        candidate=str(row["candidate"]),
                        tier=str(row["tier"]),
                        tier_rank=int(row["tier_rank"]),
                        relationship_type=str(row["relationship_type"]),
                        source=source,
                        source_limit=source_limit,
                    )
        except (json.JSONDecodeError, sqlite3.Error) as exc:
            raise CorpusToolError(f"target-analog query failed: {exc}") from exc
        return candidates

    @staticmethod
    def _add_source(
        candidates: dict[str, dict[str, Any]],
        *,
        candidate: str,
        tier: str,
        tier_rank: int,
        relationship_type: str,
        source: Mapping[str, Any],
        source_limit: int,
    ) -> None:
        card = candidates.setdefault(
            candidate,
            {"canonical_symbol": candidate, "relationships": {}},
        )
        identity = (tier, relationship_type)
        relationship = card["relationships"].setdefault(
            identity,
            {
                "tier": tier,
                "tier_rank": tier_rank,
                "relationship_type": relationship_type,
                "source_count": 0,
                "sources": [],
            },
        )
        relationship["source_count"] += 1
        if len(relationship["sources"]) < source_limit:
            relationship["sources"].append(dict(source))


def materialize_candidate(card: Mapping[str, Any]) -> dict[str, Any]:
    relationships = sorted(
        (dict(value) for value in card["relationships"].values()),
        key=lambda row: (
            int(row["tier_rank"]),
            str(row["relationship_type"]).casefold(),
        ),
    )
    for relationship in relationships:
        relationship["sources_truncated"] = (
            int(relationship["source_count"]) > len(relationship["sources"])
        )
    tiers = sorted(
        {str(row["tier"]) for row in relationships}, key=TIER_RANK.__getitem__
    )
    return {
        "canonical_symbol": str(card["canonical_symbol"]),
        "best_tier": tiers[0],
        "relationship_tiers": tiers,
        "relationship_types": sorted(
            {str(row["relationship_type"]) for row in relationships},
            key=str.casefold,
        ),
        "relationships": relationships,
    }
