#!/usr/bin/env python3
"""Load the BioKG MVP CSVs into a running Neo4j instance."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

from neo4j import GraphDatabase

from ..paths import GRAPH_WORK_DIR


DEFAULT_CYPHER = GRAPH_WORK_DIR / "neo4j_load.cypher"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cypher", type=Path, default=DEFAULT_CYPHER)
    source = parser.add_mutually_exclusive_group()
    source.add_argument(
        "--csv-dir",
        type=Path,
        default=None,
        help="Load nodes.csv and relationships.csv directly through Bolt instead of executing LOAD CSV Cypher.",
    )
    source.add_argument(
        "--work-csv-dir",
        action="store_const",
        const=GRAPH_WORK_DIR,
        dest="csv_dir",
        help="Load the mutable graph candidate from the projection build workspace.",
    )
    parser.add_argument("--uri", default="bolt://127.0.0.1:7687")
    parser.add_argument("--user", default="neo4j")
    parser.add_argument("--password", default="biokgpassword")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete existing BioKGNode nodes before loading the generated CSVs.",
    )
    return parser.parse_args()


def split_cypher(text: str) -> list[str]:
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("//"):
            continue
        lines.append(line)
    uncommented = "\n".join(lines)
    return [stmt.strip() for stmt in uncommented.split(";") if stmt.strip()]


def safe_token(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", value):
        raise ValueError(f"Unsafe Neo4j token: {value!r}")
    return value


# TODO P2-7: properties that duplicate the node label or are constant, and that no
# query/analysis/skill code reads. `kind` == the node label on 92,281/92,296 nodes; its
# only query-time reader is `p.kind` on Program, which is created by
# build_program_layer.py and is not in these CSVs, so dropping it here is safe.
DEAD_PROPS = frozenset({"kind", "concept_type", "source_kind", "program_id_llm"})

# `source` is real on Reference (UniProtKB / STRING / Reactome / ChEMBL / Open Targets)
# but the constant "scispacy" on all 11,129 concepts, so it is dropped by label.
CONCEPT_LABELS = frozenset({"Pathway", "Complex", "Module", "Phenotype", "Other"})


def nonempty_props(row: dict[str, str], *, skip: set[str]) -> dict[str, str]:
    return {key: value for key, value in row.items() if key not in skip and value not in {"", None}}


def batched(rows: list[dict], size: int = 500) -> list[list[dict]]:
    return [rows[idx : idx + size] for idx in range(0, len(rows), size)]


def load_from_csv_dir(driver, csv_dir: Path, *, reset: bool) -> tuple[int, int]:
    # Prefer the post-hoc-filtered (merged) graph when present.
    nodes_path = csv_dir / "nodes.merged.csv"
    relationships_path = csv_dir / "relationships.merged.csv"
    if not nodes_path.exists():
        nodes_path = csv_dir / "nodes.csv"
        relationships_path = csv_dir / "relationships.csv"
    with nodes_path.open(newline="", encoding="utf-8") as handle:
        node_rows = list(csv.DictReader(handle))
    with relationships_path.open(newline="", encoding="utf-8") as handle:
        relationship_rows = list(csv.DictReader(handle))

    with driver.session(database="neo4j") as session:
        if reset:
            # Batched delete: a single-transaction DETACH DELETE of the whole graph
            # exceeds dbms.memory.transaction.total.max on the full BioKG.
            session.run(
                "MATCH (n:BioKGNode) CALL { WITH n DETACH DELETE n } IN TRANSACTIONS OF 5000 ROWS"
            ).consume()
        session.run(
            "CREATE CONSTRAINT biokg_node_id IF NOT EXISTS "
            "FOR (n:BioKGNode) REQUIRE n.id IS UNIQUE"
        ).consume()

        nodes_by_labels: dict[tuple[str, ...], list[dict]] = {}
        for row in node_rows:
            labels = tuple(safe_token(label) for label in row.get("labels", "").split(";") if label)
            if "BioKGNode" not in labels:
                labels = ("BioKGNode",) + labels
            skip = {"labels"} | set(DEAD_PROPS)
            if CONCEPT_LABELS.intersection(labels):
                skip.add("source")
            props = nonempty_props(row, skip=skip)
            nodes_by_labels.setdefault(labels, []).append(props)

        for labels, rows in nodes_by_labels.items():
            label_clause = "".join(f":{label}" for label in labels)
            query = f"UNWIND $rows AS row CREATE (n{label_clause}) SET n = row"
            for batch in batched(rows):
                session.run(query, rows=batch).consume()

        rels_by_type: dict[str, list[dict]] = {}
        for row in relationship_rows:
            rel_type = safe_token(row["type"])
            rels_by_type.setdefault(rel_type, []).append(
                {
                    "start_id": row["start_id"],
                    "end_id": row["end_id"],
                    "props": nonempty_props(row, skip={"start_id", "end_id", "type"}),
                }
            )

        for rel_type, rows in rels_by_type.items():
            query = (
                "UNWIND $rows AS row "
                "MATCH (a:BioKGNode {id: row.start_id}) "
                "MATCH (b:BioKGNode {id: row.end_id}) "
                f"CREATE (a)-[r:{rel_type}]->(b) "
                "SET r = row.props"
            )
            for batch in batched(rows):
                session.run(query, rows=batch).consume()

        node_count = session.run("MATCH (n:BioKGNode) RETURN count(n) AS n").single()["n"]
        rel_count = session.run("MATCH (:BioKGNode)-[r]->(:BioKGNode) RETURN count(r) AS n").single()["n"]
    return node_count, rel_count


def main() -> None:
    args = parse_args()
    driver = GraphDatabase.driver(args.uri, auth=(args.user, args.password))
    with driver:
        driver.verify_connectivity()
        if args.csv_dir is not None:
            node_count, rel_count = load_from_csv_dir(driver, args.csv_dir, reset=args.reset)
        else:
            statements = split_cypher(args.cypher.read_text(encoding="utf-8"))
            with driver.session(database="neo4j") as session:
                if args.reset:
                    session.run("MATCH (n:BioKGNode) DETACH DELETE n").consume()
                for statement in statements:
                    session.run(statement).consume()
                node_count = session.run("MATCH (n:BioKGNode) RETURN count(n) AS n").single()["n"]
                rel_count = session.run(
                    "MATCH (:BioKGNode)-[r]->(:BioKGNode) RETURN count(r) AS n"
                ).single()["n"]
    print(f"loaded BioKG graph: {node_count} nodes, {rel_count} relationships")


if __name__ == "__main__":
    main()
