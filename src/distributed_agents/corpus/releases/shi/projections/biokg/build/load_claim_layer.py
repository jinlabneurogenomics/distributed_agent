#!/usr/bin/env python3
"""Materialize the frozen corpus-wide Claim layer into live Neo4j.

This is additive and reversible. Existing Finding nodes and relationships are
never changed; rerunning replaces only ``Claim`` nodes and their incident edges.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

from .claim_layer import (
    DEFAULT_ASSIGNMENTS,
    DEFAULT_LEDGER,
    DEFAULT_RELATIONS,
    group_assignments,
    read_ledger,
    read_tsv,
    validate_assignments,
    validate_relations,
)


def batched(rows: list[dict], size: int = 500) -> list[list[dict]]:
    return [rows[offset : offset + size] for offset in range(0, len(rows), size)]


def claim_payloads(assignments: list[dict[str, str]]) -> tuple[list[dict], list[dict]]:
    nodes = []
    memberships = []
    for claim in group_assignments(assignments):
        claim_hash = hashlib.sha256(
            "\n".join(sorted(member["source_hash"] for member in claim.members)).encode("utf-8")
        ).hexdigest()
        nodes.append(
            {
                "id": claim.claim_id,
                "claim_id": claim.claim_id,
                "summary": claim.canonical_summary,
                "relation_family": claim.relation_family,
                "direction_pattern": claim.direction_pattern,
                "evidence_mode": claim.evidence_mode,
                "support_level": claim.support_level,
                "de_support_level": claim.de_support_level,
                "de_direction": claim.de_direction,
                "de_support_count": claim.de_support_count,
                "cell_scope": "|".join(claim.cell_scope),
                "active_default": claim.active_default,
                "targets": "|".join(claim.targets),
                "readouts": "|".join(claim.readouts),
                "finding_types": "|".join(claim.finding_types),
                "member_count": len(claim.members),
                "confidence": claim.confidence,
                "source_hash": claim_hash,
            }
        )
        for member in claim.members:
            memberships.append(
                {
                    "doc_id": member["doc_id"],
                    "claim_id": claim.claim_id,
                    "role": member["member_role"],
                }
            )
    return nodes, memberships


# These fields validate the frozen tabular artifact but are aliases or
# denormalized copies once the Claim topology is materialized.
REDUNDANT_GRAPH_CLAIM_FIELDS = frozenset(
    {
        "claim_id",  # identical to BioKGNode.id
        "adjudication_version",  # artifact/build metadata
        "finding_types",  # derivable through EXPRESSES_CLAIM
        "member_count",  # count(EXPRESSES_CLAIM)
    }
)


def graph_claim_payloads(nodes: list[dict]) -> list[dict]:
    """Return only properties intrinsic to a materialized Claim node."""
    return [
        {
            key: value
            for key, value in node.items()
            if key not in REDUNDANT_GRAPH_CLAIM_FIELDS
        }
        for node in nodes
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assignments", type=Path, default=DEFAULT_ASSIGNMENTS)
    parser.add_argument("--relations", type=Path, default=DEFAULT_RELATIONS)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--uri", default=os.environ.get("BIOKG_NEO4J_BOLT", "bolt://127.0.0.1:7687"))
    parser.add_argument("--user", default="neo4j")
    parser.add_argument(
        "--password", default=os.environ.get("BIOKG_NEO4J_PASSWORD", "biokgpassword")
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--if-present",
        action="store_true",
        help="Exit successfully when the frozen artifact has not been generated yet.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.assignments.exists():
        if args.if_present:
            print(f"Claim layer skipped: {args.assignments} is absent")
            return
        raise SystemExit(f"missing frozen Claim assignments: {args.assignments}")
    ledger = read_ledger(args.ledger)
    assignments = read_tsv(args.assignments)
    relations = read_tsv(args.relations) if args.relations.exists() else []
    metrics = validate_assignments(assignments, ledger)
    claim_ids = {row["claim_id"] for row in assignments}
    validate_relations(relations, claim_ids)
    nodes, memberships = claim_payloads(assignments)
    graph_nodes = graph_claim_payloads(nodes)
    target_rows = [
        {"claim_id": node["claim_id"], "symbol": symbol}
        for node in nodes
        for symbol in node["targets"].split("|")
        if symbol
    ]
    readout_rows = [
        {"claim_id": node["claim_id"], "symbol": symbol}
        for node in nodes
        for symbol in node["readouts"].split("|")
        if symbol
    ]
    cell_rows = [
        {"claim_id": node["claim_id"], "cell": cell}
        for node in nodes
        for cell in node["cell_scope"].split("|")
        if cell
    ]
    if args.dry_run:
        print(json.dumps({**metrics, "claim_relations": len(relations)}, indent=2, sort_keys=True))
        return

    from neo4j import GraphDatabase

    driver = GraphDatabase.driver(args.uri, auth=(args.user, args.password))
    with driver, driver.session(database="neo4j") as session:
        session.run(
            "CREATE INDEX biokg_finding_doc_id IF NOT EXISTS "
            "FOR (f:Finding) ON (f.doc_id)"
        ).consume()
        session.run("CALL db.awaitIndexes(300)").consume()
        # Fail before replacing a previously valid Claim layer if the base graph
        # is absent or does not match the frozen artifact.
        required_doc_ids = sorted({row["doc_id"] for row in memberships})
        live_findings = session.run(
            "MATCH (f:Finding) WHERE f.doc_id IN $doc_ids RETURN count(DISTINCT f) AS n",
            doc_ids=required_doc_ids,
        ).single()["n"]
        if live_findings != len(required_doc_ids):
            raise RuntimeError(
                f"base graph has {live_findings}/{len(required_doc_ids)} required Finding nodes"
            )
        target_symbols = {
            str(record["symbol"] or "").casefold()
            for record in session.run(
                "MATCH (t:TargetGene) RETURN coalesce(t.symbol, t.name) AS symbol"
            )
        }
        live_targets = sum(row["symbol"].casefold() in target_symbols for row in target_rows)
        if live_targets != len(target_rows):
            raise RuntimeError(
                f"base graph resolves {live_targets}/{len(target_rows)} Claim targets"
            )
        cell_names: set[str] = set()
        for record in session.run(
            "MATCH (cell:CellType) RETURN cell.name AS name, cell.cell_type AS cell_type"
        ):
            if record["name"]:
                cell_names.add(str(record["name"]))
            cell_names.update(
                value for value in str(record["cell_type"] or "").split("|") if value
            )
        live_cells = sum(row["cell"] in cell_names for row in cell_rows)
        if live_cells != len(cell_rows):
            raise RuntimeError(
                f"base graph resolves {live_cells}/{len(cell_rows)} Claim cell scopes"
            )
        # Readout coverage is REPORTED, not asserted: the measured-universe gate
        # (TODO P2-5) legitimately drops readouts, so exact coverage is not expected.
        # This replaces the implicit coverage signal that the removed HAS_READOUT
        # edges used to carry (CLAIM_LAYER.md open item 5).
        gene_symbols = {
            str(record["symbol"] or "").casefold()
            for record in session.run(
                "MATCH (g:Gene) RETURN coalesce(g.symbol, g.name) AS symbol"
            )
        }
        live_readouts = sum(row["symbol"].casefold() in gene_symbols for row in readout_rows)

        session.run("DROP INDEX biokg_claim_id IF EXISTS").consume()
        session.run("MATCH (c:Claim) DETACH DELETE c").consume()
        for batch in batched(graph_nodes):
            session.run(
                """UNWIND $rows AS row
                CREATE (c:BioKGNode:Claim {id: row.id})
                SET c = row""",
                rows=batch,
            ).consume()
        for batch in batched(memberships):
            session.run(
                """UNWIND $rows AS row
                MATCH (f:Finding {doc_id: row.doc_id})
                MATCH (c:Claim {id: row.claim_id})
                CREATE (f)-[:EXPRESSES_CLAIM {role: row.role}]->(c)""",
                rows=batch,
            ).consume()
        # TODO P2-8: ABOUT_TARGET / HAS_READOUT / OBSERVED_IN are deliberately NOT
        # created. All three are reconstructible from
        # (Claim)<-[:EXPRESSES_CLAIM]-(Finding)-[...]->(entity) -- measured on the
        # 2026-08-24 live graph: 0 / 1 / 0 edges respectively were not derivable --
        # and their properties are verbatim copies of Claim-level fields
        # (HAS_READOUT.de_support_level equalled the parent Claim's on 36,229/36,229).
        # They added 59,336 edges (15% of the graph) that double-count, unevenly, in
        # any path- or shared-neighbour score. The preflight checks above still assert
        # that every claim target and cell scope resolves in the base graph.
        for relation_type in sorted({row["relation_type"] for row in relations}):
            relation_rows = [row for row in relations if row["relation_type"] == relation_type]
            for batch in batched(relation_rows):
                session.run(
                    f"""UNWIND $rows AS row
                    MATCH (a:Claim {{id: row.source_claim_id}})
                    MATCH (b:Claim {{id: row.target_claim_id}})
                    CREATE (a)-[r:{relation_type}]->(b)
                    SET r.confidence = row.confidence,
                        r.reason = row.reason""",
                    rows=batch,
                ).consume()
        graph_metrics = session.run(
            """MATCH (c:Claim)
            OPTIONAL MATCH (:Finding)-[m:EXPRESSES_CLAIM]->(c)
            RETURN count(DISTINCT c) AS claims,
                   count(DISTINCT m) AS memberships"""
        ).single()
        if graph_metrics["claims"] != len(nodes) or graph_metrics["memberships"] != len(
            memberships
        ):
            raise RuntimeError(
                "Claim load integrity failure: "
                f"claims={graph_metrics['claims']}/{len(nodes)} "
                f"memberships={graph_metrics['memberships']}/{len(memberships)}"
            )
    print(
        json.dumps(
            {
                **metrics,
                "claim_relations": len(relations),
                "loaded_claims": graph_metrics["claims"],
                "loaded_memberships": graph_metrics["memberships"],
                "resolved_cell_scopes": len(cell_rows),
                "resolved_readouts": live_readouts,
                "requested_readouts": len(readout_rows),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
