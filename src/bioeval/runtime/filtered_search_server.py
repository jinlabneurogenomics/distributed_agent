"""Dependency-free filtered PubMed MCP server for the BioEval SIF.

The server intentionally exposes a narrow literature surface instead of an
arbitrary URL fetcher. It implements the JSON response subset of MCP's
Streamable HTTP transport using only the Python standard library so the SIF can
be small and reproducible.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Iterable


SERVER_NAME = "bioeval-filtered-literature"
SERVER_VERSION = "1.0.0"
DEFAULT_PROTOCOL_VERSION = "2025-06-18"
EUTILS_ROOT = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
USER_AGENT = f"{SERVER_NAME}/{SERVER_VERSION}"


def _plain(value: str) -> str:
    """Normalize punctuation/spacing for resilient identifier matching."""
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


@dataclass(frozen=True)
class DenyPolicy:
    deny_patterns: tuple[str, ...]
    max_results: int = 20

    @classmethod
    def from_path(cls, path: Path) -> "DenyPolicy":
        data = json.loads(path.read_text())
        patterns = tuple(
            str(value).strip()
            for value in data.get("deny_patterns", ())
            if str(value).strip()
        )
        if not patterns:
            raise ValueError("policy must contain at least one deny pattern")
        max_results = int(data.get("max_results", 20))
        if not 1 <= max_results <= 100:
            raise ValueError("max_results must be between 1 and 100")
        return cls(deny_patterns=patterns, max_results=max_results)

    def matches(self, *values: str) -> bool:
        joined = "\n".join(value for value in values if value).casefold()
        normalized = _plain(joined)
        for pattern in self.deny_patterns:
            folded = pattern.casefold()
            if folded in joined:
                return True
            compact = _plain(pattern)
            if len(compact) >= 8 and compact in normalized:
                return True
        return False


def _text(node: ET.Element | None) -> str:
    if node is None:
        return ""
    return html.unescape("".join(node.itertext())).strip()


def _article_year(article: ET.Element) -> str:
    paths = (
        ".//ArticleDate/Year",
        ".//JournalIssue/PubDate/Year",
        ".//JournalIssue/PubDate/MedlineDate",
    )
    for path in paths:
        value = _text(article.find(path))
        if value:
            match = re.search(r"\b(?:19|20)\d{2}\b", value)
            return match.group(0) if match else value
    return ""


def _article_ids(article: ET.Element) -> dict[str, str]:
    ids: dict[str, str] = {}
    for node in article.findall(".//PubmedData/ArticleIdList/ArticleId"):
        kind = (node.attrib.get("IdType") or "").casefold()
        value = _text(node)
        if kind and value:
            ids[kind] = value
    return ids


def _parse_pubmed_xml(payload: bytes) -> list[dict[str, Any]]:
    root = ET.fromstring(payload)
    records: list[dict[str, Any]] = []
    for article in root.findall(".//PubmedArticle"):
        pmid = _text(article.find(".//MedlineCitation/PMID"))
        title = _text(article.find(".//Article/ArticleTitle"))
        abstract_parts = []
        for node in article.findall(".//Article/Abstract/AbstractText"):
            value = _text(node)
            if not value:
                continue
            label = node.attrib.get("Label")
            abstract_parts.append(f"{label}: {value}" if label else value)
        authors = []
        for node in article.findall(".//Article/AuthorList/Author"):
            collective = _text(node.find("CollectiveName"))
            if collective:
                authors.append(collective)
                continue
            last = _text(node.find("LastName"))
            initials = _text(node.find("Initials"))
            name = " ".join(part for part in (last, initials) if part)
            if name:
                authors.append(name)
        ids = _article_ids(article)
        records.append(
            {
                "pmid": pmid,
                "title": title,
                "abstract": "\n".join(abstract_parts),
                "authors": authors,
                "journal": _text(article.find(".//Article/Journal/Title")),
                "year": _article_year(article),
                "doi": ids.get("doi", ""),
                "pmc": ids.get("pmc", ""),
                "publication_types": [
                    _text(node)
                    for node in article.findall(
                        ".//Article/PublicationTypeList/PublicationType"
                    )
                    if _text(node)
                ],
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else "",
            }
        )
    return records


class PubMedClient:
    def __init__(
        self,
        *,
        timeout_s: float = 20.0,
        min_interval_s: float | None = None,
        max_retries: int = 5,
        api_key: str | None = None,
    ) -> None:
        self.timeout_s = timeout_s
        self.api_key = api_key.strip() if api_key else None
        # NCBI permits at most three requests/second without an API key and
        # ten requests/second with one. Leave a small margin below each limit.
        # A server-wide lock is required because Codex can launch MCP calls
        # concurrently and each search makes an ESearch followed by EFetch.
        self.min_interval_s = (
            min_interval_s
            if min_interval_s is not None
            else (0.11 if self.api_key else 0.4)
        )
        self.max_retries = max_retries
        self._rate_lock = threading.Lock()
        self._next_request_at = 0.0

    def _throttle(self) -> None:
        with self._rate_lock:
            now = time.monotonic()
            delay = self._next_request_at - now
            if delay > 0:
                time.sleep(delay)
                now = time.monotonic()
            self._next_request_at = now + self.min_interval_s

    def _get(self, endpoint: str, params: dict[str, str]) -> bytes:
        request_params = {**params, "tool": SERVER_NAME, "email": "bioeval@localhost"}
        if self.api_key:
            request_params["api_key"] = self.api_key
        query = urllib.parse.urlencode(request_params)
        request = urllib.request.Request(
            f"{EUTILS_ROOT}/{endpoint}?{query}",
            headers={"User-Agent": USER_AGENT, "Accept": "application/json,text/xml"},
        )
        retry_statuses = {429, 500, 502, 503, 504}
        for attempt in range(self.max_retries + 1):
            self._throttle()
            try:
                with urllib.request.urlopen(
                    request, timeout=self.timeout_s
                ) as response:
                    return response.read()
            except urllib.error.HTTPError as exc:
                if exc.code not in retry_statuses or attempt >= self.max_retries:
                    raise
                retry_after = exc.headers.get("Retry-After")
                try:
                    server_delay = float(retry_after) if retry_after else 0.0
                except ValueError:
                    server_delay = 0.0
                time.sleep(max(server_delay, min(2**attempt, 8)))
        raise RuntimeError("unreachable PubMed retry state")

    def search(
        self, query: str, *, max_results: int
    ) -> tuple[int, list[dict[str, Any]]]:
        raw = self._get(
            "esearch.fcgi",
            {
                "db": "pubmed",
                "term": query,
                "retmode": "json",
                "retmax": str(max_results),
                "sort": "relevance",
            },
        )
        search = json.loads(raw)
        result = search.get("esearchresult") or {}
        ids = [str(value) for value in result.get("idlist", ())]
        total = int(result.get("count", 0) or 0)
        if not ids:
            return total, []
        records = self.fetch_many(ids)
        order = {pmid: index for index, pmid in enumerate(ids)}
        records.sort(key=lambda item: order.get(item.get("pmid", ""), len(order)))
        return total, records

    def fetch_many(self, pmids: Iterable[str]) -> list[dict[str, Any]]:
        ids = [value for value in pmids if re.fullmatch(r"\d+", value)]
        if not ids:
            return []
        raw = self._get(
            "efetch.fcgi",
            {"db": "pubmed", "id": ",".join(ids), "retmode": "xml"},
        )
        return _parse_pubmed_xml(raw)


class AuditLog:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._lock = threading.Lock()
        path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, payload: dict[str, Any]) -> None:
        record = {"timestamp": time.time(), **payload}
        line = json.dumps(record, sort_keys=True) + "\n"
        with self._lock:
            with self.path.open("a") as handle:
                handle.write(line)


class FilteredLiteratureService:
    def __init__(
        self,
        policy: DenyPolicy,
        audit: AuditLog,
        *,
        client: PubMedClient | None = None,
    ) -> None:
        self.policy = policy
        self.audit = audit
        self.client = client or PubMedClient()

    @staticmethod
    def tools() -> list[dict[str, Any]]:
        return [
            {
                "name": "search_pubmed",
                "description": (
                    "Search PubMed for independent biomedical literature. "
                    "Protected evaluation sources and mirrors are removed."
                ),
                "annotations": {
                    "readOnlyHint": True,
                    "destructiveHint": False,
                    "idempotentHint": True,
                    "openWorldHint": True,
                },
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "PubMed query using normal Entrez syntax.",
                        },
                        "max_results": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 20,
                            "default": 10,
                        },
                    },
                    "required": ["query"],
                    "additionalProperties": False,
                },
            },
            {
                "name": "fetch_pubmed",
                "description": (
                    "Fetch title, abstract, citation metadata, DOI, and PMC id "
                    "for one numeric PMID, subject to the source-denial policy."
                ),
                "annotations": {
                    "readOnlyHint": True,
                    "destructiveHint": False,
                    "idempotentHint": True,
                    "openWorldHint": True,
                },
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "pmid": {
                            "type": "string",
                            "pattern": "^[0-9]+$",
                        }
                    },
                    "required": ["pmid"],
                    "additionalProperties": False,
                },
            },
        ]

    def _allowed_records(
        self, records: Iterable[dict[str, Any]]
    ) -> tuple[list[dict[str, Any]], int]:
        allowed = []
        excluded = 0
        for record in records:
            serialized = json.dumps(record, ensure_ascii=False, sort_keys=True)
            if self.policy.matches(serialized):
                excluded += 1
            else:
                allowed.append(record)
        return allowed, excluded

    def call_tool(self, name: str, arguments: dict[str, Any]) -> tuple[str, bool]:
        try:
            if name == "search_pubmed":
                return self._search(arguments)
            if name == "fetch_pubmed":
                return self._fetch(arguments)
            return json.dumps({"error": f"unknown tool: {name}"}), True
        except (OSError, ValueError, urllib.error.URLError, ET.ParseError) as exc:
            self.audit.write(
                {
                    "tool": name,
                    "decision": "upstream_error",
                    "error_type": type(exc).__name__,
                }
            )
            return json.dumps(
                {
                    "error": "The filtered literature service could not complete "
                    "the upstream request.",
                    "error_type": type(exc).__name__,
                }
            ), True

    def _search(self, arguments: dict[str, Any]) -> tuple[str, bool]:
        query = str(arguments.get("query", "")).strip()
        if not query:
            return json.dumps({"error": "query must be non-empty"}), True
        query_hash = hashlib.sha256(query.encode()).hexdigest()
        if self.policy.matches(query):
            self.audit.write(
                {
                    "tool": "search_pubmed",
                    "decision": "deny_query",
                    "query_sha256": query_hash,
                }
            )
            return json.dumps(
                {
                    "error": "Query blocked by the evaluation source-denial policy.",
                    "policy": "Do not identify, retrieve, or reconstruct the "
                    "withheld source-dataset manuscript or companion resources.",
                }
            ), True
        requested = int(arguments.get("max_results", 10))
        max_results = max(1, min(requested, self.policy.max_results, 20))
        total, records = self.client.search(query, max_results=max_results)
        allowed, excluded = self._allowed_records(records)
        self.audit.write(
            {
                "tool": "search_pubmed",
                "decision": "allow",
                "query": query,
                "query_sha256": query_hash,
                "upstream_total": total,
                "returned_pmids": [record["pmid"] for record in allowed],
                "excluded_count": excluded,
            }
        )
        return json.dumps(
            {
                "source": "NCBI PubMed E-utilities",
                "query": query,
                "upstream_total": total,
                "returned": len(allowed),
                "excluded_by_policy": excluded,
                "results": allowed,
            },
            ensure_ascii=True,
        ), False

    def _fetch(self, arguments: dict[str, Any]) -> tuple[str, bool]:
        pmid = str(arguments.get("pmid", "")).strip()
        if not re.fullmatch(r"\d+", pmid):
            return json.dumps({"error": "pmid must contain digits only"}), True
        records = self.client.fetch_many([pmid])
        allowed, excluded = self._allowed_records(records)
        decision = "deny_result" if excluded else "allow"
        self.audit.write(
            {
                "tool": "fetch_pubmed",
                "decision": decision,
                "requested_pmid": pmid,
                "returned_pmids": [record["pmid"] for record in allowed],
                "excluded_count": excluded,
            }
        )
        if excluded:
            return json.dumps(
                {"error": "Requested record is blocked by the source-denial policy."}
            ), True
        if not allowed:
            return json.dumps({"error": "PMID not found"}), True
        return json.dumps(
            {"source": "NCBI PubMed E-utilities", "result": allowed[0]},
            ensure_ascii=True,
        ), False


class McpApplication:
    def __init__(self, service: FilteredLiteratureService) -> None:
        self.service = service

    @staticmethod
    def _result(request_id: Any, result: Any) -> dict[str, Any]:
        return {"jsonrpc": "2.0", "id": request_id, "result": result}

    @staticmethod
    def _error(request_id: Any, code: int, message: str) -> dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": code, "message": message},
        }

    def dispatch(self, payload: dict[str, Any]) -> dict[str, Any] | None:
        request_id = payload.get("id")
        method = payload.get("method")
        params = payload.get("params") or {}
        if method == "initialize":
            requested = str(params.get("protocolVersion") or DEFAULT_PROTOCOL_VERSION)
            return self._result(
                request_id,
                {
                    "protocolVersion": requested,
                    "capabilities": {"tools": {"listChanged": False}},
                    "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
                },
            )
        if method in {
            "notifications/initialized",
            "notifications/cancelled",
            "notifications/progress",
        }:
            return None
        if method == "ping":
            return self._result(request_id, {})
        if method == "tools/list":
            return self._result(request_id, {"tools": self.service.tools()})
        if method == "tools/call":
            name = str(params.get("name") or "")
            arguments = params.get("arguments") or {}
            if not isinstance(arguments, dict):
                return self._error(request_id, -32602, "arguments must be an object")
            text, is_error = self.service.call_tool(name, arguments)
            return self._result(
                request_id,
                {
                    "content": [{"type": "text", "text": text}],
                    "isError": is_error,
                },
            )
        if method in {"resources/list", "prompts/list"}:
            key = "resources" if method.startswith("resources") else "prompts"
            return self._result(request_id, {key: []})
        return self._error(request_id, -32601, f"method not found: {method}")


class McpRequestHandler(BaseHTTPRequestHandler):
    server_version = SERVER_NAME

    @property
    def app(self) -> McpApplication:
        return self.server.app  # type: ignore[attr-defined]

    def log_message(self, _format: str, *_args: Any) -> None:
        return

    def _send_json(
        self,
        status: HTTPStatus,
        payload: dict[str, Any] | list[Any] | None,
        *,
        session_id: str | None = None,
    ) -> None:
        body = b"" if payload is None else json.dumps(payload).encode()
        self.send_response(status)
        if body:
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
        if session_id:
            self.send_header("Mcp-Session-Id", session_id)
        self.end_headers()
        if body:
            self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._send_json(
                HTTPStatus.OK,
                {"status": "ok", "name": SERVER_NAME, "version": SERVER_VERSION},
            )
            return
        self._send_json(
            HTTPStatus.METHOD_NOT_ALLOWED,
            {"error": "This stateless MCP server accepts POST requests only."},
        )

    def do_DELETE(self) -> None:  # noqa: N802
        if self.path == "/mcp":
            self._send_json(HTTPStatus.OK, {"status": "closed"})
            return
        self._send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/mcp":
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length))
        except (ValueError, json.JSONDecodeError):
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                McpApplication._error(None, -32700, "invalid JSON"),
            )
            return
        if not isinstance(payload, dict):
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                McpApplication._error(None, -32600, "request must be an object"),
            )
            return
        response = self.app.dispatch(payload)
        if response is None:
            self._send_json(HTTPStatus.ACCEPTED, None)
            return
        session_id = None
        if payload.get("method") == "initialize":
            session_id = uuid.uuid4().hex
        self._send_json(HTTPStatus.OK, response, session_id=session_id)


def make_server(
    host: str,
    port: int,
    service: FilteredLiteratureService,
) -> ThreadingHTTPServer:
    server = ThreadingHTTPServer((host, port), McpRequestHandler)
    server.app = McpApplication(service)  # type: ignore[attr-defined]
    return server


def _self_test() -> int:
    policy = DenyPolicy(("10.1234/example", "Withheld Source Paper"))
    assert policy.matches("https://example.org/10.1234/example")
    assert policy.matches("withheld-source-paper")
    assert not policy.matches("independent neuronal study")
    xml = b"""
    <PubmedArticleSet><PubmedArticle><MedlineCitation>
      <PMID>123</PMID><Article><ArticleTitle>Independent study</ArticleTitle>
      <Abstract><AbstractText>Evidence.</AbstractText></Abstract>
      <Journal><Title>Journal</Title><JournalIssue><PubDate><Year>2024</Year>
      </PubDate></JournalIssue></Journal></Article></MedlineCitation>
      <PubmedData><ArticleIdList><ArticleId IdType="doi">10.1/x</ArticleId>
      </ArticleIdList></PubmedData></PubmedArticle></PubmedArticleSet>
    """
    parsed = _parse_pubmed_xml(xml)
    assert parsed[0]["pmid"] == "123"
    assert parsed[0]["title"] == "Independent study"
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--policy", type=Path)
    parser.add_argument("--audit-log", type=Path)
    parser.add_argument("--ncbi-api-key-file", type=Path)
    parser.add_argument("--self-test", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.self_test:
        return _self_test()
    if args.policy is None or args.audit_log is None:
        raise SystemExit("--policy and --audit-log are required")
    api_key = None
    if args.ncbi_api_key_file is not None:
        api_key = args.ncbi_api_key_file.read_text(encoding="utf-8").strip()
        if not api_key:
            raise SystemExit("--ncbi-api-key-file is empty")
    policy = DenyPolicy.from_path(args.policy)
    service = FilteredLiteratureService(
        policy,
        AuditLog(args.audit_log),
        client=PubMedClient(api_key=api_key),
    )
    server = make_server(args.host, args.port, service)
    print(
        json.dumps(
            {
                "status": "ready",
                "host": args.host,
                "port": server.server_port,
                "server": SERVER_NAME,
                "version": SERVER_VERSION,
            }
        ),
        flush=True,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
