#!/usr/bin/env python3
"""Run bounded read-only Cypher against the Shi holdout BioKG Neo4j graph.

This stdlib-only client talks to the host-provided Neo4j HTTP endpoint.  The
query agent writes task-specific Cypher, but every caller query must end with a
numeric ``LIMIT <= 50`` and write/admin clauses are always refused. The Shi holdout
graph projects explicit Finding comparators through canonical Gene nodes and
frozen bottom-up Claims through typed Finding contributions.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.request
from typing import Any

DEFAULT_HTTP_URL = os.environ.get("BIOKG_NEO4J_HTTP_URL", "http://127.0.0.1:7474")
DEFAULT_DATABASE = os.environ.get("BIOKG_NEO4J_DATABASE", "neo4j")
DEFAULT_USER = os.environ.get("BIOKG_NEO4J_USER", "neo4j")
DEFAULT_PASSWORD = os.environ.get("BIOKG_NEO4J_PASSWORD", "biokgpassword")
MAX_RESPONSE_BYTES = 1_000_000

WRITE_CLAUSE = re.compile(
    r"(?i)(?<![A-Za-z_])(CREATE|MERGE|DELETE|SET|REMOVE|DROP|ALTER|RENAME|"
    r"GRANT|DENY|REVOKE|LOAD\s+CSV|CALL|START\s+DATABASE|STOP\s+DATABASE|"
    r"TERMINATE\s+TRANSACTIONS)(?![A-Za-z_])"
)
LIMIT_CLAUSE = re.compile(r"(?i)(?<![A-Za-z_])LIMIT\s+(\d+)(?![A-Za-z_])")
FINAL_LIMIT_CLAUSE = re.compile(r"(?i)(?<![A-Za-z_])LIMIT\s+(\d+)\s*;?\s*$")
NON_CODE = re.compile(
    r"""(?sx)/\*.*?\*/|//[^\r\n]*|'(?:''|\\.|[^'\\])*'|"""
    r'''"(?:""|\\.|[^"\\])*"'''
)


def _cypher_structure(statement: str) -> str:
    """Mask literals and comments before safety inspection."""

    return NON_CODE.sub(lambda match: " " * len(match.group(0)), statement)


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
) -> dict[str, Any]:
    """POST one statement to /db/<database>/tx/commit and return the parsed payload."""
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
            raw = response.read(MAX_RESPONSE_BYTES + 1)
            if len(raw) > MAX_RESPONSE_BYTES:
                raise SystemExit(
                    f"Neo4j response exceeds the {MAX_RESPONSE_BYTES}-byte bound"
                )
            return json.loads(raw.decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(
            f"Neo4j HTTP {exc.code} from {endpoint}: {detail}\n"
            "The host-provided BioKG service failed after preflight; treat "
            "corpus.graph as unavailable and use a bounded ledger path."
        ) from exc
    except urllib.error.URLError as exc:
        raise SystemExit(
            f"Cannot reach Neo4j at {endpoint}: {exc}\n"
            "Do not start services from the model sandbox; treat corpus.graph "
            "as unavailable and use a bounded ledger path."
        ) from exc


def _rows(payload: dict[str, Any]) -> tuple[list[str], list[list[Any]]]:
    errors = payload.get("errors") or []
    if errors:
        msgs = "; ".join(f"{e.get('code')}: {e.get('message')}" for e in errors)
        raise SystemExit(f"Cypher error: {msgs}")
    results = payload.get("results") or []
    if not results:
        return [], []
    result = results[0]
    columns = result.get("columns", [])
    data = [item.get("row", []) for item in result.get("data", [])]
    return columns, data


def _print_table(columns: list[str], data: list[list[Any]]) -> None:
    if not columns:
        print("(no columns returned)")
        return
    rows = [[_fmt(cell) for cell in row] for row in data]
    widths = [len(c) for c in columns]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))
    widths = [min(w, 60) for w in widths]
    header = "  ".join(c.ljust(widths[i]) for i, c in enumerate(columns))
    print(header)
    print("  ".join("-" * widths[i] for i in range(len(columns))))
    for row in rows:
        print("  ".join(cell[: widths[i]].ljust(widths[i]) for i, cell in enumerate(row)))
    print(f"\n({len(data)} rows)")


def _fmt(cell: Any) -> str:
    if cell is None:
        return ""
    if isinstance(cell, (dict, list)):
        return json.dumps(cell, ensure_ascii=False)
    return str(cell)


SCHEMA_QUERIES = {
    "node_label_counts": "MATCH (n) UNWIND labels(n) AS label "
    "RETURN label, count(*) AS n ORDER BY n DESC",
    "rel_type_counts": "MATCH ()-[r]->() RETURN type(r) AS type, count(*) AS n ORDER BY n DESC",
    "source_artifact_counts": "MATCH (n:BioKGNode) "
    "RETURN n.source_artifact AS source_artifact, count(*) AS n ORDER BY n DESC",
}


def show_schema(conn: dict[str, Any]) -> None:
    print(f"# BioKG Neo4j @ {conn['http_url']} db={conn['database']}\n")
    for title, query in SCHEMA_QUERIES.items():
        cols, data = _rows(run_cypher(query, **conn))
        print(f"## {title}")
        _print_table(cols, data)
        print()
    print("## key node properties (sampled)")
    for label in ["TargetGene", "Gene", "Finding", "Evidence", "Reference", "Claim"]:
        cols, data = _rows(
            run_cypher(f"MATCH (n:{label}) RETURN keys(n) AS keys LIMIT 1", **conn)
        )
        keys = data[0][0] if data else []
        print(f"  {label:14} {keys}")
    print(
        "\nThis release has no extracted concept, Program, or CellType nodes. "
        "REPORTS_GENE records explicit comparators, not effect support; "
        "EXPRESSES_CLAIM records frozen Claim contributions and their roles."
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-q", "--query", help="Inline Cypher statement.")
    parser.add_argument("--file", help="Read a Cypher statement from a file ('-' for stdin).")
    parser.add_argument("--schema", action="store_true", help="Print labels, rel types, counts, props.")
    parser.add_argument(
        "--param",
        action="append",
        default=[],
        metavar="NAME=JSON",
        help="Cypher parameter as NAME=<json>; repeatable. Example: targets='[\"Pomp\"]'.",
    )
    parser.add_argument("--format", choices=["table", "json"], default="table")
    parser.add_argument("--http-url", default=DEFAULT_HTTP_URL)
    parser.add_argument("--database", default=DEFAULT_DATABASE)
    parser.add_argument("--user", default=DEFAULT_USER)
    parser.add_argument("--password", default=DEFAULT_PASSWORD)
    parser.add_argument("--timeout", type=float, default=120.0)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    conn = {
        "http_url": args.http_url,
        "database": args.database,
        "user": args.user,
        "password": args.password,
        "timeout": args.timeout,
    }

    if args.schema:
        show_schema(conn)
        return 0

    if args.file:
        statement = sys.stdin.read() if args.file == "-" else open(args.file).read()
    elif args.query:
        statement = args.query
    elif not sys.stdin.isatty():
        statement = sys.stdin.read()
    else:
        raise SystemExit("provide a query via -q/--query, --file, stdin, or use --schema")

    statement = statement.strip()
    if not statement:
        raise SystemExit("empty Cypher statement")
    structure = _cypher_structure(statement)
    if WRITE_CLAUSE.search(structure):
        raise SystemExit(
            "refusing a write, administrative, LOAD CSV, or CALL clause in read-only mode"
        )
    if re.search(r"(?i)(?<![A-Za-z_])UNION(?![A-Za-z_])", structure):
        raise SystemExit("caller Cypher may not use UNION")
    limits = [int(match.group(1)) for match in LIMIT_CLAUSE.finditer(structure)]
    final_limit = FINAL_LIMIT_CLAUSE.search(structure)
    if not limits or final_limit is None:
        raise SystemExit("caller Cypher must end with a numeric LIMIT <= 50")
    if any(limit < 1 or limit > 50 for limit in limits):
        raise SystemExit("every caller Cypher LIMIT must be between 1 and 50")

    parameters: dict[str, Any] = {}
    for spec in args.param:
        if "=" not in spec:
            raise SystemExit(f"bad --param {spec!r}; use NAME=<json>")
        name, raw = spec.split("=", 1)
        try:
            parameters[name.strip()] = json.loads(raw)
        except json.JSONDecodeError:
            parameters[name.strip()] = raw  # treat as bare string
    payload = run_cypher(statement, parameters=parameters, **conn)
    cols, data = _rows(payload)
    if args.format == "json":
        print(json.dumps([dict(zip(cols, row)) for row in data], indent=2, ensure_ascii=False))
    else:
        _print_table(cols, data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
