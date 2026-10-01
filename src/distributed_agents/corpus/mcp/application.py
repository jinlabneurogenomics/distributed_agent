#!/usr/bin/env python3
"""JSON-RPC/STDIO application for the corpus MCP service."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

from .binding import ReleaseBinding
from .constants import (
    CALIBRATION_CAPABILITY,
    EVIDENCE_CAPABILITY,
    FINDINGS_CAPABILITY,
    PROTOCOL_VERSION,
    SERVER_NAME,
    SERVER_VERSION,
    TARGET_ANALOG_CAPABILITY,
)
from .errors import CorpusToolError
from .policy import CapabilityPolicy
from .service import CorpusService


class McpApplication:
    def __init__(self, service: CorpusService) -> None:
        self.service = service

    def instructions(self) -> str:
        release_id = self.service.release.release_id
        parts = [
            f"Use these read-only tools to answer questions about DistributedAgents corpus release {release_id}. ",
        ]
        if self.service.policy.allows(CALIBRATION_CAPABILITY):
            parts.append("Calibrate unfamiliar fields before interpreting them. ")
        if self.service.allowed_ledgers():
            parts.append(
                "For a known target, type, or local ID, use query_ledger. "
            )
        if self.service.policy.allows(EVIDENCE_CAPABILITY):
            parts.append(
                "Resolve returned evidence and reference IDs with resolve_evidence. "
            )
        parts.append("Local IDs are target-gene scoped. ")
        if self.service.supports_compatibility_claims and self.service.policy.allows(
            FINDINGS_CAPABILITY
        ):
            parts.append(
                "Use query_claims for the Shi Claim layer and the two target tools for structured relationships. related_targets supports direct one-anchor evidence paths and multi-source random walk with restart; its reachability score is not biological rank. Keep shared-Claim membership, typed Claim relations, and directional Finding comparator references in separate lanes. "
            )
        if self.service.supports_target_analogs and self.service.policy.allows(
            TARGET_ANALOG_CAPABILITY
        ):
            parts.append(
                "Use suggest_target_analogs when a requested mouse perturbation is absent from the corpus or an explicit eligible universe needs curated typed comparators. Its categorical evidence tiers are nominations, not outcome predictions or a biological similarity score. "
            )
        if self.service.supports_findings_bm25 and self.service.policy.allows(
            FINDINGS_CAPABILITY
        ):
            parts.append(
                "For a concept-first question, start with one target-level search_findings call using two or three focused lexical formulations, then resolve only representative hits. BM25 rank is retrieval relevance, not biological rank."
            )
        elif self.service.supports_claim_graph and self.service.policy.allows(
            FINDINGS_CAPABILITY
        ):
            parts.append(
                "Keep shared-Claim paths separate from one-sided explicit Finding references, and do not treat graph topology as biological rank."
            )
        return "".join(parts)

    def dispatch(self, request: Mapping[str, Any]) -> dict[str, Any] | None:
        request_id = request.get("id")
        method = request.get("method")
        if not isinstance(method, str) or not method:
            return self._error(request_id, -32600, "invalid request")
        if method.startswith("notifications/"):
            return None
        try:
            if method == "initialize":
                params = request.get("params") or {}
                if not isinstance(params, Mapping):
                    raise CorpusToolError("initialize params must be an object")
                requested = str(params.get("protocolVersion") or PROTOCOL_VERSION)
                result = {
                    "protocolVersion": requested,
                    "capabilities": {"tools": {"listChanged": False}},
                    "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
                    "instructions": self.instructions(),
                }
            elif method == "ping":
                result = {}
            elif method == "tools/list":
                result = {"tools": self.service.tools()}
            elif method == "tools/call":
                params = request.get("params") or {}
                if not isinstance(params, Mapping):
                    raise CorpusToolError("tools/call params must be an object")
                name = params.get("name")
                arguments = params.get("arguments") or {}
                if not isinstance(name, str) or not isinstance(arguments, Mapping):
                    raise CorpusToolError("tools/call requires a tool name and object arguments")
                payload = self.service.call(name, arguments)
                rendered = json.dumps(payload, ensure_ascii=False, sort_keys=True)
                result = {
                    "content": [{"type": "text", "text": rendered}],
                    "isError": False,
                }
            elif method in {"resources/list", "prompts/list"}:
                result = {"resources" if method == "resources/list" else "prompts": []}
            else:
                return self._error(request_id, -32601, f"method not found: {method}")
            return {"jsonrpc": "2.0", "id": request_id, "result": result}
        except CorpusToolError as exc:
            if method == "tools/call":
                result = {
                    "content": [{"type": "text", "text": str(exc)}],
                    "isError": True,
                }
                return {"jsonrpc": "2.0", "id": request_id, "result": result}
            return self._error(request_id, -32602, str(exc))
        except (TypeError, ValueError, json.JSONDecodeError) as exc:
            return self._error(request_id, -32602, str(exc))

    @staticmethod
    def _error(request_id: Any, code: int, message: str) -> dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": code, "message": message},
        }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release-manifest", type=Path, required=True)
    parser.add_argument("--capabilities", type=Path, required=True)
    return parser


def run_stdio(application: McpApplication) -> int:
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            request = json.loads(line)
            if not isinstance(request, Mapping):
                raise ValueError("request must be an object")
            response = application.dispatch(request)
        except (json.JSONDecodeError, ValueError) as exc:
            response = McpApplication._error(None, -32700, str(exc))
        if response is not None:
            sys.stdout.write(json.dumps(response, ensure_ascii=False, separators=(",", ":")) + "\n")
            sys.stdout.flush()
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    release = ReleaseBinding.load(args.release_manifest)
    policy = CapabilityPolicy.load(args.capabilities)
    return run_stdio(McpApplication(CorpusService(release, policy)))


if __name__ == "__main__":
    raise SystemExit(main())
