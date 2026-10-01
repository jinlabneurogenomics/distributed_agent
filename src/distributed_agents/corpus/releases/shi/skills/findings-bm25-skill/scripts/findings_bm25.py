#!/usr/bin/env python3
"""Build, verify, and search the Shi Finding-native BM25 index.

The SQLite FTS5 index is deterministic and contains only the canonical summary
and why_it_matters fields as searchable text. Other Finding columns are
retained as unindexed return metadata so callers can resolve evidence and
references in a second hop.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sqlite3
from collections import defaultdict
from contextlib import closing
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import quote


INDEX_SCHEMA_VERSION = "distributed_agents-findings-bm25-sqlite-v1"
RESULT_SCHEMA_VERSION = "distributed_agents-findings-bm25-result-v1"
RELEASE_ID = "shi"
INDEXED_FIELDS = ("summary", "why_it_matters")
TOKENIZER = "unicode61 remove_diacritics 2"
RRF_K = 60
MAX_QUERIES = 8
MAX_RESULTS = 50
QUERY_TOKEN = re.compile(r"[A-Za-z0-9]+")
QUERY_STOPWORDS = frozenset(
    {
        "a",
        "about",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "been",
        "being",
        "between",
        "by",
        "can",
        "could",
        "did",
        "do",
        "does",
        "for",
        "from",
        "had",
        "has",
        "have",
        "how",
        "in",
        "is",
        "it",
        "its",
        "of",
        "on",
        "or",
        "please",
        "show",
        "shows",
        "that",
        "the",
        "these",
        "this",
        "those",
        "to",
        "was",
        "were",
        "what",
        "which",
        "who",
        "why",
        "with",
        "would",
    }
)

RELEASE_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_FINDINGS = RELEASE_ROOT / "artifacts" / "ledgers" / "findings.csv"
DEFAULT_INDEX = RELEASE_ROOT / "artifacts" / "indexes" / "findings_bm25.sqlite3"


class FindingsIndexError(RuntimeError):
    """Raised when the immutable Finding index is unavailable or inconsistent."""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_source(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise FindingsIndexError(f"canonical Findings ledger is unavailable: {path}")
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {
            "target_gene",
            "finding_id",
            "finding_type",
            "summary",
            "why_it_matters",
            "evidence_ids",
            "ref_ids",
        }
        missing = sorted(required - set(reader.fieldnames or ()))
        if missing:
            raise FindingsIndexError(
                "canonical Findings ledger is missing columns: " + ", ".join(missing)
            )
        rows = [dict(row) for row in reader]
    identities = {(row["target_gene"], row["finding_id"]) for row in rows}
    if len(identities) != len(rows):
        raise FindingsIndexError(
            "canonical Findings ledger has duplicate target-scoped IDs"
        )
    return rows


def _read_only_connection(path: Path) -> sqlite3.Connection:
    if not path.is_file():
        raise FindingsIndexError(f"Finding BM25 index is unavailable: {path}")
    connection = sqlite3.connect(f"file:{quote(str(path))}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    return connection


def build_index(
    findings_path: Path, index_path: Path, *, overwrite: bool
) -> dict[str, Any]:
    rows = _read_source(findings_path)
    source_sha256 = sha256(findings_path)
    index_path.parent.mkdir(parents=True, exist_ok=True)
    if index_path.exists() and not overwrite:
        raise FindingsIndexError(
            f"index already exists; pass --overwrite: {index_path}"
        )
    temporary = index_path.with_name(index_path.name + ".tmp")
    if temporary.exists():
        temporary.unlink()

    connection = sqlite3.connect(temporary)
    try:
        connection.executescript(
            """
            PRAGMA page_size = 4096;
            PRAGMA journal_mode = OFF;
            PRAGMA synchronous = OFF;
            PRAGMA temp_store = MEMORY;
            PRAGMA auto_vacuum = NONE;
            CREATE TABLE metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            ) WITHOUT ROWID;
            CREATE TABLE findings (
                id INTEGER PRIMARY KEY,
                doc_id TEXT NOT NULL UNIQUE,
                target_gene TEXT NOT NULL,
                finding_id TEXT NOT NULL,
                finding_type TEXT NOT NULL,
                summary TEXT NOT NULL,
                why_it_matters TEXT NOT NULL,
                evidence_ids TEXT NOT NULL,
                ref_ids TEXT NOT NULL
            );
            CREATE VIRTUAL TABLE findings_fts USING fts5(
                summary,
                why_it_matters,
                content='findings',
                content_rowid='id',
                tokenize='unicode61 remove_diacritics 2'
            );
            """
        )
        for row_id, row in enumerate(rows, 1):
            target = row["target_gene"]
            finding_id = row["finding_id"]
            connection.execute(
                """
                INSERT INTO findings (
                    id, doc_id, target_gene, finding_id, finding_type,
                    summary, why_it_matters, evidence_ids, ref_ids
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row_id,
                    f"{target}:{finding_id}",
                    target,
                    finding_id,
                    row["finding_type"],
                    row["summary"],
                    row["why_it_matters"],
                    row["evidence_ids"],
                    row["ref_ids"],
                ),
            )
        metadata = {
            "schema_version": INDEX_SCHEMA_VERSION,
            "release_id": RELEASE_ID,
            "source_sha256": source_sha256,
            "source_records": str(len(rows)),
            "indexed_fields": json.dumps(INDEXED_FIELDS, separators=(",", ":")),
            "tokenizer": TOKENIZER,
            "ranking": "sqlite_fts5_bm25_then_rrf",
            "llm_rewrite": "false",
        }
        connection.executemany(
            "INSERT INTO metadata (key, value) VALUES (?, ?)",
            sorted(metadata.items()),
        )
        connection.execute("INSERT INTO findings_fts(findings_fts) VALUES ('rebuild')")
        connection.execute("INSERT INTO findings_fts(findings_fts) VALUES ('optimize')")
        connection.commit()
        connection.execute("VACUUM")
    finally:
        connection.close()
    os.replace(temporary, index_path)
    return {
        "schema_version": INDEX_SCHEMA_VERSION,
        "operation": "build",
        "index_path": str(index_path.resolve()),
        "index_sha256": sha256(index_path),
        "index_bytes": index_path.stat().st_size,
        "source_sha256": source_sha256,
        "source_records": len(rows),
        "indexed_fields": list(INDEXED_FIELDS),
        "llm_rewrite": False,
    }


def _metadata(connection: sqlite3.Connection) -> dict[str, str]:
    try:
        return {
            str(row["key"]): str(row["value"])
            for row in connection.execute(
                "SELECT key, value FROM metadata ORDER BY key"
            )
        }
    except sqlite3.Error as exc:
        raise FindingsIndexError(f"cannot read Finding BM25 metadata: {exc}") from exc


def verify_index(
    index_path: Path,
    findings_path: Path,
    *,
    expected_source_sha256: str | None = None,
    expected_release_id: str = RELEASE_ID,
) -> dict[str, Any]:
    source_sha256 = expected_source_sha256 or sha256(findings_path)
    with closing(_read_only_connection(index_path)) as connection:
        metadata = _metadata(connection)
        expected = {
            "schema_version": INDEX_SCHEMA_VERSION,
            "release_id": expected_release_id,
            "source_sha256": source_sha256,
            "indexed_fields": json.dumps(INDEXED_FIELDS, separators=(",", ":")),
            "tokenizer": TOKENIZER,
            "llm_rewrite": "false",
        }
        mismatches = {
            key: {"expected": value, "observed": metadata.get(key)}
            for key, value in expected.items()
            if metadata.get(key) != value
        }
        records = int(connection.execute("SELECT count(*) FROM findings").fetchone()[0])
        indexed_records = int(
            connection.execute("SELECT count(*) FROM findings_fts").fetchone()[0]
        )
        quick_check = str(connection.execute("PRAGMA quick_check").fetchone()[0])
    expected_records = int(metadata.get("source_records") or -1)
    if records != expected_records or indexed_records != records:
        mismatches["records"] = {
            "expected": expected_records,
            "observed": {
                "findings": records,
                "findings_fts": indexed_records,
            },
        }
    if quick_check != "ok":
        mismatches["quick_check"] = {"expected": "ok", "observed": quick_check}
    if mismatches:
        raise FindingsIndexError(
            "Finding BM25 index verification failed: "
            + json.dumps(mismatches, sort_keys=True)
        )
    return {
        "schema_version": INDEX_SCHEMA_VERSION,
        "operation": "verify",
        "release_id": metadata["release_id"],
        "index_path": str(index_path.resolve()),
        "index_sha256": sha256(index_path),
        "source_sha256": metadata["source_sha256"],
        "source_records": records,
        "indexed_fields": list(INDEXED_FIELDS),
        "tokenizer": TOKENIZER,
        "llm_rewrite": False,
        "status": "ok",
    }


def _query_tokens(value: str) -> tuple[list[str], list[str]]:
    raw = list(dict.fromkeys(QUERY_TOKEN.findall(value.casefold())))
    tokens = [token for token in raw if token not in QUERY_STOPWORDS]
    return (tokens or raw), [token for token in raw if token in QUERY_STOPWORDS]


def _match_expression(tokens: Iterable[str]) -> str:
    return " OR ".join(f'"{token}"' for token in tokens)


def _split_ids(value: str) -> list[str]:
    return [item for item in value.split("|") if item]


def _load_cards(
    connection: sqlite3.Connection, row_ids: list[int]
) -> dict[int, dict[str, Any]]:
    if not row_ids:
        return {}
    placeholders = ",".join("?" for _ in row_ids)
    rows = connection.execute(
        f"""
        SELECT id, doc_id, target_gene, finding_id, finding_type, summary,
               why_it_matters, evidence_ids, ref_ids
        FROM findings
        WHERE id IN ({placeholders})
        """,
        row_ids,
    )
    return {
        int(row["id"]): {
            "doc_id": row["doc_id"],
            "target_gene": row["target_gene"],
            "finding_id": row["finding_id"],
            "finding_type": row["finding_type"],
            "summary": row["summary"],
            "why_it_matters": row["why_it_matters"],
            "evidence_ids": _split_ids(str(row["evidence_ids"])),
            "ref_ids": _split_ids(str(row["ref_ids"])),
        }
        for row in rows
    }


def search_index(
    index_path: Path,
    findings_path: Path,
    queries: list[str],
    *,
    level: str,
    top_k: int,
    offset: int = 0,
    finding_type: str | None = None,
    expected_source_sha256: str | None = None,
    expected_release_id: str = RELEASE_ID,
) -> dict[str, Any]:
    if not 1 <= len(queries) <= MAX_QUERIES:
        raise FindingsIndexError(f"search requires 1-{MAX_QUERIES} queries")
    if not 1 <= top_k <= MAX_RESULTS:
        raise FindingsIndexError(f"top_k must be between 1 and {MAX_RESULTS}")
    if not 0 <= offset <= 1_000_000:
        raise FindingsIndexError("offset must be between 0 and 1000000")
    if level not in {"finding", "target"}:
        raise FindingsIndexError("level must be finding or target")
    verified = verify_index(
        index_path,
        findings_path,
        expected_source_sha256=expected_source_sha256,
        expected_release_id=expected_release_id,
    )

    rrf_scores: defaultdict[int, float] = defaultdict(float)
    query_matches: defaultdict[int, list[dict[str, Any]]] = defaultdict(list)
    identities: dict[int, tuple[str, str]] = {}
    query_summaries: list[dict[str, Any]] = []
    with closing(_read_only_connection(index_path)) as connection:
        for query_index, query in enumerate(queries):
            tokens, ignored_tokens = _query_tokens(query)
            if not tokens:
                raise FindingsIndexError(
                    f"query {query_index + 1} has no searchable tokens"
                )
            parameters: list[Any] = [_match_expression(tokens)]
            predicate = ""
            if finding_type:
                predicate = " AND f.finding_type = ?"
                parameters.append(finding_type)
            hits = list(
                connection.execute(
                    f"""
                    SELECT f.id, f.doc_id, f.target_gene,
                           bm25(findings_fts, 1.0, 1.0) AS bm25_score
                    FROM findings_fts
                    JOIN findings AS f ON f.id = findings_fts.rowid
                    WHERE findings_fts MATCH ?{predicate}
                    ORDER BY bm25_score ASC, f.doc_id ASC
                    """,
                    parameters,
                )
            )
            query_summaries.append(
                {
                    "query": query,
                    "tokens": tokens,
                    "ignored_stopwords": ignored_tokens,
                    "matching_findings": len(hits),
                }
            )
            for rank, row in enumerate(hits, 1):
                row_id = int(row["id"])
                identities[row_id] = (
                    str(row["doc_id"]),
                    str(row["target_gene"]),
                )
                rrf_scores[row_id] += 1.0 / (RRF_K + rank)
                query_matches[row_id].append(
                    {
                        "query_index": query_index,
                        "rank": rank,
                        "bm25_score": round(float(row["bm25_score"]), 8),
                    }
                )

        ordered_findings = sorted(
            rrf_scores,
            key=lambda row_id: (
                -rrf_scores[row_id],
                identities[row_id][0].casefold(),
                identities[row_id][0],
            ),
        )
        if level == "finding":
            selected_ids = ordered_findings[offset : offset + top_k]
            cards = _load_cards(connection, selected_ids)
            results = [
                {
                    "rank": rank,
                    "rrf_score": round(rrf_scores[row_id], 8),
                    "query_matches": query_matches[row_id],
                    "finding": cards[row_id],
                }
                for rank, row_id in enumerate(selected_ids, offset + 1)
            ]
            exact_total = len(ordered_findings)
        else:
            by_target: defaultdict[str, list[int]] = defaultdict(list)
            target_symbols: dict[str, str] = {}
            for row_id in ordered_findings:
                target = identities[row_id][1]
                key = target.casefold()
                target_symbols.setdefault(key, target)
                by_target[key].append(row_id)
            ordered_targets = sorted(
                by_target,
                key=lambda key: (
                    -rrf_scores[by_target[key][0]],
                    key,
                    target_symbols[key],
                ),
            )
            selected_targets = ordered_targets[offset : offset + top_k]
            selected_ids = [by_target[key][0] for key in selected_targets]
            cards = _load_cards(connection, selected_ids)
            results = [
                {
                    "rank": rank,
                    "target_gene": target_symbols[key],
                    "rrf_score": round(rrf_scores[row_id], 8),
                    "matched_finding_count": len(by_target[key]),
                    "query_matches": query_matches[row_id],
                    "top_finding": cards[row_id],
                }
                for rank, key in enumerate(selected_targets, offset + 1)
                for row_id in (by_target[key][0],)
            ]
            exact_total = len(ordered_targets)

    return {
        "schema_version": RESULT_SCHEMA_VERSION,
        "operation": "corpus.findings.bm25_search",
        "release_id": verified["release_id"],
        "queries": query_summaries,
        "level": level,
        "filters": {"finding_type": finding_type},
        "retrieval_semantics": (
            "SQLite FTS5 BM25 over summary and why_it_matters only; "
            "multi-query results use reciprocal rank fusion; retrieval relevance "
            "is not biological evidence or a final candidate rank"
        ),
        "index": {
            "schema_version": verified["schema_version"],
            "source_sha256": verified["source_sha256"],
            "source_records": verified["source_records"],
            "indexed_fields": verified["indexed_fields"],
            "tokenizer": verified["tokenizer"],
            "llm_rewrite": verified["llm_rewrite"],
        },
        "results": results,
        "page": {
            "offset": offset,
            "exact_total": exact_total,
            "emitted": len(results),
            "limit": top_k,
            "truncated": offset > 0 or offset + len(results) < exact_total,
            "has_more": offset + len(results) < exact_total,
            "next_offset": (
                offset + len(results)
                if offset + len(results) < exact_total
                else None
            ),
            "truncated_by_output_bytes": False,
        },
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build", help="Build the deterministic index.")
    build.add_argument("--findings-path", type=Path, default=DEFAULT_FINDINGS)
    build.add_argument("--index-path", type=Path, default=DEFAULT_INDEX)
    build.add_argument("--overwrite", action="store_true")

    verify = subparsers.add_parser(
        "verify", help="Verify index provenance and integrity."
    )
    verify.add_argument("--findings-path", type=Path, default=DEFAULT_FINDINGS)
    verify.add_argument("--index-path", type=Path, default=DEFAULT_INDEX)
    verify.add_argument("--expected-source-sha256")
    verify.add_argument("--expected-release-id", default=RELEASE_ID)
    verify.add_argument("--pretty", action="store_true")

    search = subparsers.add_parser("search", help="Search Findings with BM25/RRF.")
    search.add_argument("--query", action="append", dest="queries", required=True)
    search.add_argument("--level", choices=("finding", "target"), default="finding")
    search.add_argument("--top-k", type=int, default=20)
    search.add_argument("--offset", type=int, default=0)
    search.add_argument("--finding-type")
    search.add_argument("--findings-path", type=Path, default=DEFAULT_FINDINGS)
    search.add_argument("--index-path", type=Path, default=DEFAULT_INDEX)
    search.add_argument("--expected-source-sha256")
    search.add_argument("--expected-release-id", default=RELEASE_ID)
    search.add_argument("--pretty", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.command == "build":
            payload = build_index(
                args.findings_path, args.index_path, overwrite=args.overwrite
            )
            pretty = True
        elif args.command == "verify":
            payload = verify_index(
                args.index_path,
                args.findings_path,
                expected_source_sha256=args.expected_source_sha256,
                expected_release_id=args.expected_release_id,
            )
            pretty = args.pretty
        else:
            payload = search_index(
                args.index_path,
                args.findings_path,
                args.queries,
                level=args.level,
                top_k=args.top_k,
                offset=args.offset,
                finding_type=args.finding_type,
                expected_source_sha256=args.expected_source_sha256,
                expected_release_id=args.expected_release_id,
            )
            pretty = args.pretty
    except (FindingsIndexError, OSError, sqlite3.Error, ValueError) as exc:
        print(f"error: {exc}", file=os.sys.stderr)
        return 2
    print(json.dumps(payload, indent=2 if pretty else None, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
