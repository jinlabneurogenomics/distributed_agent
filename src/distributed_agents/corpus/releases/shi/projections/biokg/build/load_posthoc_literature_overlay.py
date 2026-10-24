#!/usr/bin/env python3
"""Apply, inspect, or remove a reversible literature overlay in BioKG.

The overlay is deliberately narrow: it adds ``LiteratureComparison`` and
``Reference`` nodes around one existing ``Finding`` and connects existing
``Gene`` nodes with the graph's existing relationship types.  Base nodes and
relationships are never modified.  Every added node and edge carries one
``overlay_id`` so the treatment can be removed exactly after an ablation.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "biokg-posthoc-literature-overlay-v1"
SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]*$")
REQUIRED_RELATION_TYPES = {
    "CITES",
    "HAS_LITERATURE_COMPARISON",
    "REPORTS_GENE",
}


def _required_text(value: object, field: str) -> str:
    clean = str(value or "").strip()
    if not clean:
        raise ValueError(f"{field} must be non-empty")
    return clean


def _safe_id(value: object, field: str) -> str:
    clean = _required_text(value, field)
    if not SAFE_ID.fullmatch(clean):
        raise ValueError(f"{field} contains unsupported characters: {clean!r}")
    return clean


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.casefold()).strip("_")


def load_overlay(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("overlay must be a JSON object")
    if raw.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(
            f"schema_version must be {SCHEMA_VERSION!r}, got "
            f"{raw.get('schema_version')!r}"
        )
    overlay_id = _safe_id(raw.get("overlay_id"), "overlay_id")
    finding_doc_id = _safe_id(raw.get("finding_doc_id"), "finding_doc_id")
    finding_id = _safe_id(raw.get("finding_id"), "finding_id")
    target_gene = _safe_id(raw.get("target_gene"), "target_gene")
    if finding_doc_id != f"{target_gene}:{finding_id}":
        raise ValueError("finding_doc_id must equal '<target_gene>:<finding_id>'")
    comparisons = raw.get("comparisons")
    if not isinstance(comparisons, list) or not comparisons:
        raise ValueError("comparisons must be a non-empty list")

    seen_genes: set[str] = set()
    seen_comparisons: set[str] = set()
    seen_refs: set[str] = set()
    rows: list[dict[str, str]] = []
    overlay_slug = _slug(overlay_id)
    for index, item in enumerate(comparisons, 1):
        if not isinstance(item, dict):
            raise ValueError(f"comparisons[{index}] must be an object")
        candidate_gene = _safe_id(
            item.get("candidate_gene"), f"comparisons[{index}].candidate_gene"
        )
        comparison_id = _safe_id(
            item.get("comparison_id"), f"comparisons[{index}].comparison_id"
        )
        reference = item.get("reference")
        if not isinstance(reference, dict):
            raise ValueError(f"comparisons[{index}].reference must be an object")
        ref_id = _safe_id(reference.get("ref_id"), f"comparisons[{index}].ref_id")
        for value, seen, field in (
            (candidate_gene.casefold(), seen_genes, "candidate_gene"),
            (comparison_id.casefold(), seen_comparisons, "comparison_id"),
            (ref_id.casefold(), seen_refs, "ref_id"),
        ):
            if value in seen:
                raise ValueError(f"duplicate {field}: {value}")
            seen.add(value)
        url = _required_text(reference.get("url"), f"comparisons[{index}].url")
        if not url.startswith(("https://", "http://")):
            raise ValueError(f"comparisons[{index}].url must be HTTP(S)")
        confidence = _required_text(
            item.get("confidence"), f"comparisons[{index}].confidence"
        )
        rows.append(
            {
                "candidate_gene": candidate_gene,
                "comparison_id": comparison_id,
                "comparison_node_id": (
                    f"literature_comparison:{overlay_slug}_{_slug(comparison_id)}"
                ),
                "comparison_name": f"{target_gene}:{comparison_id}",
                "literature_status": _required_text(
                    item.get("literature_status"),
                    f"comparisons[{index}].literature_status",
                ),
                "summary": _required_text(
                    item.get("summary"), f"comparisons[{index}].summary"
                ),
                "description": _required_text(
                    item.get("description"), f"comparisons[{index}].description"
                ),
                "context_limit": _required_text(
                    item.get("context_limit"), f"comparisons[{index}].context_limit"
                ),
                "confidence": confidence,
                "ref_id": ref_id,
                "reference_node_id": f"reference:{overlay_slug}_{_slug(ref_id)}",
                "reference_name": f"{target_gene}:{ref_id}",
                "citation": _required_text(
                    reference.get("citation"), f"comparisons[{index}].citation"
                ),
                "url": url,
                "source": _required_text(
                    reference.get("source"), f"comparisons[{index}].source"
                ),
                "source_type": _required_text(
                    reference.get("source_type"),
                    f"comparisons[{index}].source_type",
                ),
                "reference_description": _required_text(
                    reference.get("description"),
                    f"comparisons[{index}].reference.description",
                ),
            }
        )
    return {
        "schema_version": SCHEMA_VERSION,
        "overlay_id": overlay_id,
        "description": _required_text(raw.get("description"), "description"),
        "finding_doc_id": finding_doc_id,
        "finding_id": finding_id,
        "target_gene": target_gene,
        "rows": rows,
    }


def _auth_header(user: str, password: str) -> str:
    token = base64.b64encode(f"{user}:{password}".encode()).decode()
    return "Basic " + token


def run_cypher(
    statement: str,
    *,
    http_url: str,
    database: str,
    user: str,
    password: str,
    parameters: dict[str, Any] | None = None,
    timeout: float = 120.0,
) -> tuple[list[str], list[list[Any]]]:
    endpoint = f"{http_url.rstrip('/')}/db/{database}/tx/commit"
    body = json.dumps(
        {"statements": [{"statement": statement, "parameters": parameters or {}}]}
    ).encode()
    request = urllib.request.Request(
        endpoint,
        data=body,
        method="POST",
        headers={
            "Authorization": _auth_header(user, password),
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Neo4j HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Cannot reach Neo4j at {endpoint}: {exc}") from exc
    errors = payload.get("errors") or []
    if errors:
        detail = "; ".join(
            f"{item.get('code')}: {item.get('message')}" for item in errors
        )
        raise RuntimeError(f"Cypher error: {detail}")
    results = payload.get("results") or []
    if not results:
        return [], []
    return (
        results[0].get("columns") or [],
        [item.get("row") or [] for item in results[0].get("data") or []],
    )


def _connection(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "http_url": args.http_url,
        "database": args.database,
        "user": args.user,
        "password": args.password,
        "timeout": args.timeout,
    }


def validate_live(overlay: dict[str, Any], conn: dict[str, Any]) -> None:
    _, rows = run_cypher(
        """MATCH (f:Finding {doc_id: $finding_doc_id})
        WITH count(f) AS finding_count
        UNWIND $candidate_genes AS candidate
        OPTIONAL MATCH (g:Gene)
        WHERE toLower(g.symbol) = toLower(candidate)
        RETURN finding_count, candidate, count(g) AS gene_count
        ORDER BY candidate""",
        parameters={
            "finding_doc_id": overlay["finding_doc_id"],
            "candidate_genes": [row["candidate_gene"] for row in overlay["rows"]],
        },
        **conn,
    )
    if not rows or any(int(row[0]) != 1 for row in rows):
        raise RuntimeError(
            f"base graph must contain exactly one Finding {overlay['finding_doc_id']}"
        )
    unresolved = [str(row[1]) for row in rows if int(row[2]) != 1]
    if unresolved:
        raise RuntimeError(
            "base graph must resolve exactly one Gene for: " + ", ".join(unresolved)
        )
    _, type_rows = run_cypher(
        "CALL db.relationshipTypes() YIELD relationshipType "
        "RETURN collect(relationshipType)",
        **conn,
    )
    live_types = set(type_rows[0][0] if type_rows else [])
    missing = sorted(REQUIRED_RELATION_TYPES - live_types)
    if missing:
        raise RuntimeError("base graph lacks required relationship types: " + ", ".join(missing))


def status(overlay: dict[str, Any], conn: dict[str, Any]) -> dict[str, Any]:
    _, node_rows = run_cypher(
        "MATCH (n:BioKGNode) WHERE n.overlay_id = $overlay_id "
        "RETURN count(n), collect(n.id)",
        parameters={"overlay_id": overlay["overlay_id"]},
        **conn,
    )
    _, rel_rows = run_cypher(
        "MATCH ()-[r]->() WHERE r.overlay_id = $overlay_id "
        "RETURN count(r), collect(type(r))",
        parameters={"overlay_id": overlay["overlay_id"]},
        **conn,
    )
    node_count, node_ids = node_rows[0] if node_rows else (0, [])
    relation_count, relation_types = rel_rows[0] if rel_rows else (0, [])
    expected_nodes = 2 * len(overlay["rows"])
    expected_relationships = 3 * len(overlay["rows"])
    return {
        "overlay_id": overlay["overlay_id"],
        "state": (
            "applied"
            if node_count == expected_nodes and relation_count == expected_relationships
            else "absent"
            if node_count == 0 and relation_count == 0
            else "partial"
        ),
        "node_count": node_count,
        "expected_node_count": expected_nodes,
        "node_ids": sorted(node_ids),
        "relationship_count": relation_count,
        "expected_relationship_count": expected_relationships,
        "relationship_types": sorted(relation_types),
    }


def apply_overlay(overlay: dict[str, Any], conn: dict[str, Any]) -> dict[str, Any]:
    validate_live(overlay, conn)
    query = """UNWIND $rows AS row
    MATCH (f:Finding {doc_id: $finding_doc_id})
    MATCH (g:Gene) WHERE toLower(g.symbol) = toLower(row.candidate_gene)
    MERGE (lc:BioKGNode:LiteratureComparison {id: row.comparison_node_id})
    SET lc.name = row.comparison_name,
        lc.target_gene = $target_gene,
        lc.candidate_gene = row.candidate_gene,
        lc.finding_id = $finding_id,
        lc.comparison_id = row.comparison_id,
        lc.literature_status = row.literature_status,
        lc.summary = row.summary,
        lc.description = row.description,
        lc.context_limit = row.context_limit,
        lc.confidence = row.confidence,
        lc.overlay_id = $overlay_id
    MERGE (ref:BioKGNode:Reference {id: row.reference_node_id})
    SET ref.name = row.reference_name,
        ref.target_gene = $target_gene,
        ref.candidate_gene = row.candidate_gene,
        ref.comparison_id = row.comparison_id,
        ref.ref_id = row.ref_id,
        ref.citation = row.citation,
        ref.url = row.url,
        ref.source = row.source,
        ref.source_type = row.source_type,
        ref.description = row.reference_description,
        ref.overlay_id = $overlay_id
    MERGE (f)-[literature:HAS_LITERATURE_COMPARISON {
        overlay_id: $overlay_id, comparison_id: row.comparison_id
    }]->(lc)
    MERGE (f)-[citation:CITES {
        overlay_id: $overlay_id,
        comparison_id: row.comparison_id,
        ref_id: row.ref_id
    }]->(ref)
    MERGE (f)-[reported:REPORTS_GENE {
        overlay_id: $overlay_id,
        role: 'finding_reported_comparator',
        comparison_id: row.comparison_id
    }]->(g)
    RETURN count(DISTINCT lc), count(DISTINCT ref), count(DISTINCT reported)"""
    run_cypher(
        query,
        parameters={
            "overlay_id": overlay["overlay_id"],
            "finding_doc_id": overlay["finding_doc_id"],
            "finding_id": overlay["finding_id"],
            "target_gene": overlay["target_gene"],
            "rows": overlay["rows"],
        },
        **conn,
    )
    return status(overlay, conn)


def remove_overlay(overlay: dict[str, Any], conn: dict[str, Any]) -> dict[str, Any]:
    run_cypher(
        "MATCH ()-[r]->() WHERE r.overlay_id = $overlay_id DELETE r",
        parameters={"overlay_id": overlay["overlay_id"]},
        **conn,
    )
    run_cypher(
        "MATCH (n:BioKGNode) WHERE n.overlay_id = $overlay_id DETACH DELETE n",
        parameters={"overlay_id": overlay["overlay_id"]},
        **conn,
    )
    return status(overlay, conn)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--overlay", type=Path, required=True)
    parser.add_argument("--action", choices=("status", "apply", "remove"), default="status")
    parser.add_argument("--allow-write", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--http-url",
        default=os.environ.get("BIOKG_NEO4J_HTTP_URL", "http://127.0.0.1:7474"),
    )
    parser.add_argument(
        "--database", default=os.environ.get("BIOKG_NEO4J_DATABASE", "neo4j")
    )
    parser.add_argument("--user", default=os.environ.get("BIOKG_NEO4J_USER", "neo4j"))
    parser.add_argument(
        "--password",
        default=os.environ.get("BIOKG_NEO4J_PASSWORD", "biokgpassword"),
    )
    parser.add_argument("--timeout", type=float, default=120.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    overlay = load_overlay(args.overlay.resolve())
    if args.dry_run:
        print(
            json.dumps(
                {
                    "status": "validated",
                    "overlay_id": overlay["overlay_id"],
                    "finding_doc_id": overlay["finding_doc_id"],
                    "candidate_genes": [
                        row["candidate_gene"] for row in overlay["rows"]
                    ],
                    "node_count": 2 * len(overlay["rows"]),
                    "relationship_count": 3 * len(overlay["rows"]),
                    "relationship_types": sorted(REQUIRED_RELATION_TYPES),
                },
                indent=2,
            )
        )
        return 0
    if args.action in {"apply", "remove"} and not args.allow_write:
        raise SystemExit("apply/remove require --allow-write")
    conn = _connection(args)
    if args.action == "apply":
        result = apply_overlay(overlay, conn)
    elif args.action == "remove":
        result = remove_overlay(overlay, conn)
    else:
        result = status(overlay, conn)
    print(json.dumps(result, indent=2))
    expected_state = "applied" if args.action == "apply" else "absent" if args.action == "remove" else None
    return 0 if expected_state is None or result["state"] == expected_state else 1


if __name__ == "__main__":
    raise SystemExit(main())
