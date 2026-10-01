#!/usr/bin/env python3
"""Load the accepted Shi holdout JSONL graph into an existing Neo4j service."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping, Sequence

try:
    from ..paths import NODES_FILE, RELATIONSHIPS_FILE
except ImportError:  # Direct-script compatibility for release-local validation.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from paths import NODES_FILE, RELATIONSHIPS_FILE


BATCH_SIZE = 500
NODE_TYPES = ("TargetGene", "Gene", "Finding", "Evidence", "Reference", "Claim")
NODE_LABELS = {
    "TargetGene": ("Gene", "TargetGene"),
    "Gene": ("Gene",),
    "Finding": ("Finding",),
    "Evidence": ("Evidence",),
    "Reference": ("Reference",),
    "Claim": ("Claim",),
}
RELATION_TYPES = (
    "HAS_FINDING",
    "HAS_TARGET",
    "REPORTS_GENE",
    "SUPPORTED_BY",
    "CITES",
    "EXPRESSES_CLAIM",
)


def _iter_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_number}: expected JSON object")
            yield row


def _safe_properties(values: Mapping[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in values.items():
        if value is None:
            continue
        if isinstance(value, (str, int, float, bool)):
            result[str(key)] = value
        elif isinstance(value, list) and all(
            isinstance(item, (str, int, float, bool)) for item in value
        ):
            result[str(key)] = value
        else:
            raise ValueError(
                f"Neo4j-incompatible property {key!r}: {type(value).__name__}"
            )
    return result


def _batches(
    rows: Iterable[dict[str, Any]], size: int = BATCH_SIZE
) -> Iterator[list[dict[str, Any]]]:
    batch: list[dict[str, Any]] = []
    for row in rows:
        batch.append(row)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch


def inspect_graph(nodes_path: Path, relationships_path: Path) -> dict[str, Any]:
    node_counts: Counter[str] = Counter()
    node_ids: set[str] = set()
    for row in _iter_jsonl(nodes_path):
        node_type = str(row.get("type") or "")
        node_id = str(row.get("id") or "")
        if node_type not in NODE_TYPES or not node_id:
            raise ValueError(f"invalid node row: {node_id!r} {node_type!r}")
        if node_id in node_ids:
            raise ValueError(f"duplicate node ID: {node_id}")
        node_ids.add(node_id)
        _safe_properties(row.get("properties") or {})
        node_counts[node_type] += 1

    relation_counts: Counter[str] = Counter()
    dangling = 0
    for row in _iter_jsonl(relationships_path):
        relation_type = str(row.get("type") or "")
        if relation_type not in RELATION_TYPES:
            raise ValueError(f"invalid relationship type: {relation_type!r}")
        if row.get("start_id") not in node_ids or row.get("end_id") not in node_ids:
            dangling += 1
        _safe_properties(row.get("properties") or {})
        relation_counts[relation_type] += 1
    if dangling:
        raise ValueError(f"graph contains {dangling} dangling relationship endpoints")
    return {
        "nodes": len(node_ids),
        "relationships": sum(relation_counts.values()),
        "node_counts": dict(sorted(node_counts.items())),
        "relationship_counts": dict(sorted(relation_counts.items())),
        "dangling_endpoints": dangling,
    }


def load_graph(
    driver: Any,
    *,
    nodes_path: Path,
    relationships_path: Path,
    reset: bool,
) -> dict[str, Any]:
    expected = inspect_graph(nodes_path, relationships_path)
    with driver.session(database="neo4j") as session:
        if reset:
            session.run(
                "MATCH (n:BioKGNode) CALL { WITH n DETACH DELETE n } "
                "IN TRANSACTIONS OF 5000 ROWS"
            ).consume()
        session.run(
            "CREATE CONSTRAINT biokg_node_id IF NOT EXISTS "
            "FOR (n:BioKGNode) REQUIRE n.id IS UNIQUE"
        ).consume()

        for node_type in NODE_TYPES:
            rows = (
                {
                    "id": str(row["id"]),
                    "source_artifact": str(row["source_artifact"]),
                    **_safe_properties(row["properties"]),
                }
                for row in _iter_jsonl(nodes_path)
                if row["type"] == node_type
            )
            labels = ":".join(NODE_LABELS[node_type])
            query = (
                f"UNWIND $rows AS row CREATE (n:BioKGNode:{labels}) SET n = row"
            )
            for batch in _batches(rows):
                session.run(query, rows=batch).consume()

        for relation_type in RELATION_TYPES:
            rows = (
                {
                    "start_id": str(row["start_id"]),
                    "end_id": str(row["end_id"]),
                    "properties": _safe_properties(row["properties"]),
                }
                for row in _iter_jsonl(relationships_path)
                if row["type"] == relation_type
            )
            query = (
                "UNWIND $rows AS row "
                "MATCH (a:BioKGNode {id: row.start_id}) "
                "MATCH (b:BioKGNode {id: row.end_id}) "
                f"CREATE (a)-[r:{relation_type}]->(b) SET r = row.properties"
            )
            for batch in _batches(rows):
                session.run(query, rows=batch).consume()

        actual_nodes = session.run(
            "MATCH (n:BioKGNode) RETURN count(n) AS n"
        ).single()["n"]
        actual_relationships = session.run(
            "MATCH (:BioKGNode)-[r]->(:BioKGNode) RETURN count(r) AS n"
        ).single()["n"]
    if (actual_nodes, actual_relationships) != (
        expected["nodes"],
        expected["relationships"],
    ):
        raise RuntimeError(
            "Shi holdout graph load parity failure: "
            f"nodes={actual_nodes}/{expected['nodes']} "
            f"relationships={actual_relationships}/{expected['relationships']}"
        )
    return {
        **expected,
        "loaded_nodes": actual_nodes,
        "loaded_relationships": actual_relationships,
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--nodes", type=Path, default=NODES_FILE)
    parser.add_argument("--relationships", type=Path, default=RELATIONSHIPS_FILE)
    parser.add_argument("--uri", default="bolt://127.0.0.1:7687")
    parser.add_argument("--user", default="neo4j")
    parser.add_argument("--password", default="biokgpassword")
    parser.add_argument("--reset", action="store_true")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and count the JSONL graph without contacting Neo4j.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.dry_run:
        result = inspect_graph(args.nodes.resolve(), args.relationships.resolve())
    else:
        from neo4j import GraphDatabase

        driver = GraphDatabase.driver(args.uri, auth=(args.user, args.password))
        with driver:
            driver.verify_connectivity()
            result = load_graph(
                driver,
                nodes_path=args.nodes.resolve(),
                relationships_path=args.relationships.resolve(),
                reset=args.reset,
            )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
