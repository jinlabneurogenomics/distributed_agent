#!/usr/bin/env python3
"""Discover versioned data files in a public archive without downloading them."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from fetch_resource import resolve_run_path


FIGSHARE_API = "https://api.figshare.com/v2"


def _request_json(
    url: str,
    *,
    payload: dict[str, object] | None = None,
    timeout: float,
) -> object:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST" if data is not None else "GET",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        if response.geturl().split(":", 1)[0].casefold() != "https":
            raise ValueError("archive request redirected away from HTTPS")
        content_type = str(response.headers.get_content_type() or "").casefold()
        if content_type not in {"application/json", "text/json"}:
            raise ValueError(
                f"archive returned {content_type or 'an unknown content type'}, not JSON"
            )
        return json.load(response)


def _file_record(row: object) -> dict[str, object] | None:
    if not isinstance(row, dict):
        return None
    return {
        "id": row.get("id"),
        "name": str(row.get("name") or ""),
        "size_bytes": row.get("size"),
        "mimetype": str(row.get("mimetype") or ""),
        "download_url": str(row.get("download_url") or ""),
        "supplied_md5": str(row.get("supplied_md5") or ""),
        "computed_md5": str(row.get("computed_md5") or ""),
    }


def discover_figshare(
    *,
    query: str,
    limit: int = 10,
    file_name: str | None = None,
    timeout: float = 30.0,
) -> dict[str, object]:
    """Return detailed Figshare article and file metadata for a text query."""

    query = query.strip()
    if not query:
        raise ValueError("query must be non-empty")
    if not 1 <= limit <= 100:
        raise ValueError("limit must be between 1 and 100")
    pattern = re.compile(file_name, re.IGNORECASE) if file_name else None
    rows = _request_json(
        f"{FIGSHARE_API}/articles/search",
        payload={"search_for": query, "limit": limit},
        timeout=timeout,
    )
    if not isinstance(rows, list):
        raise ValueError("archive search response must be a list")

    articles: list[dict[str, object]] = []
    for summary in rows[:limit]:
        if not isinstance(summary, dict) or not isinstance(summary.get("id"), int):
            continue
        article_id = int(summary["id"])
        detail = _request_json(
            f"{FIGSHARE_API}/articles/{article_id}",
            timeout=timeout,
        )
        if not isinstance(detail, dict):
            continue
        files = [
            record
            for row in detail.get("files", [])
            if (record := _file_record(row)) is not None
            and (pattern is None or pattern.search(str(record["name"])))
        ]
        if pattern is not None and not files:
            continue
        articles.append(
            {
                "id": article_id,
                "title": str(detail.get("title") or summary.get("title") or ""),
                "doi": str(detail.get("doi") or summary.get("doi") or ""),
                "url_public_api": str(
                    detail.get("url_public_api")
                    or f"{FIGSHARE_API}/articles/{article_id}"
                ),
                "url_public_html": str(detail.get("url_public_html") or ""),
                "published_date": str(detail.get("published_date") or ""),
                "modified_date": str(detail.get("modified_date") or ""),
                "license": detail.get("license"),
                "files": files,
            }
        )
    return {
        "schema_version": "distributed_agents-resource-discovery-v1",
        "catalog": "Figshare",
        "catalog_api": FIGSHARE_API,
        "query": query,
        "file_name_pattern": file_name or "",
        "searched_at": datetime.now(timezone.utc).isoformat(),
        "articles": articles,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--query", required=True)
    parser.add_argument("--output", default="resource_discovery.json")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument(
        "--file-name",
        help="optional case-insensitive regular expression for archived filenames",
    )
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args()
    try:
        result = discover_figshare(
            query=args.query,
            limit=args.limit,
            file_name=args.file_name,
            timeout=args.timeout,
        )
    except (TimeoutError, OSError) as exc:
        # A slow archive is a retry, not a stack trace. One basis stage read a
        # `urlopen` traceback as an unrecoverable acquisition failure and
        # downgraded to a neutral universe instead of trying again.
        print(
            f"archive did not answer within {args.timeout:g}s ({exc}); "
            "retry, with a smaller --limit or a longer --timeout, before "
            "treating this as an acquisition failure",
            file=sys.stderr,
        )
        return 2
    output = resolve_run_path(args.run_dir, args.output, label="output")
    if output.suffix.casefold() != ".json":
        raise ValueError("discovery output must be JSON")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
