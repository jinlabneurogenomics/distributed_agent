"""Enforce BioEval's withheld-source policy inside mitmproxy."""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
import time
from pathlib import Path

from mitmproxy import http

from bioeval.runtime.policy import SourcePolicy
from bioeval.runtime.tls import (
    request_filter_text,
    response_filter_text,
    url_sha256,
)


_POLICY_PATH = Path(os.environ["BIOEVAL_TLS_POLICY"])
_AUDIT_PATH = (
    Path(os.environ["BIOEVAL_TLS_AUDIT"])
    if os.environ.get("BIOEVAL_TLS_AUDIT")
    else None
)
_LEASE_DIR = (
    Path(os.environ["BIOEVAL_TLS_LEASE_DIR"])
    if os.environ.get("BIOEVAL_TLS_LEASE_DIR")
    else None
)
_AUDIT_DIR = (
    Path(os.environ["BIOEVAL_TLS_AUDIT_DIR"])
    if os.environ.get("BIOEVAL_TLS_AUDIT_DIR")
    else None
)
_RAW_POLICY = json.loads(_POLICY_PATH.read_text())
_POLICY = SourcePolicy(
    mode="filtered-literature",
    deny_patterns=tuple(_RAW_POLICY["deny_patterns"]),
    max_results=int(_RAW_POLICY.get("max_results", 20)),
)


def _lease_audit_path(flow: http.HTTPFlow) -> Path | None:
    if _LEASE_DIR is None or _AUDIT_DIR is None:
        return _AUDIT_PATH
    credentials = flow.metadata.get("proxyauth")
    if (
        not isinstance(credentials, tuple)
        or len(credentials) != 2
        or not all(isinstance(value, str) for value in credentials)
    ):
        return None
    token, password = credentials
    if re.fullmatch(r"[a-f0-9]{48}", token) is None:
        return None
    lease_path = _LEASE_DIR / f"{token}.json"
    try:
        lease = json.loads(lease_path.read_text())
    except (OSError, json.JSONDecodeError):
        return None
    expected = str(lease.get("password_sha256") or "")
    observed = hashlib.sha256(password.encode()).hexdigest()
    if not expected or not hmac.compare_digest(expected, observed):
        return None
    flow.metadata["bioeval_source_policy_lease"] = token
    return _AUDIT_DIR / f"{token}.jsonl"


def _flow_audit_path(flow: http.HTTPFlow) -> Path | None:
    token = flow.metadata.get("bioeval_source_policy_lease")
    if isinstance(token, str) and _AUDIT_DIR is not None:
        return _AUDIT_DIR / f"{token}.jsonl"
    return _lease_audit_path(flow)


def _audit(
    flow: http.HTTPFlow,
    *,
    decision: str,
    phase: str,
    pattern_hashes: list[str] | None = None,
) -> None:
    audit_path = _flow_audit_path(flow)
    if audit_path is None:
        return
    record = {
        "timestamp": time.time(),
        "decision": decision,
        "phase": phase,
        "method": flow.request.method,
        "url_sha256": url_sha256(flow.request.pretty_url),
        "pattern_hashes": pattern_hashes or [],
    }
    with audit_path.open("a") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")


def _blocked_response() -> http.Response:
    return http.Response.make(
        403,
        b"blocked by bioeval source policy\n",
        {"Content-Type": "text/plain; charset=utf-8"},
    )


def request(flow: http.HTTPFlow) -> None:
    if _flow_audit_path(flow) is None:
        flow.metadata["bioeval_source_policy_blocked"] = True
        flow.response = _blocked_response()
        return
    inspected = request_filter_text(
        url=flow.request.pretty_url,
        method=flow.request.method,
        headers=flow.request.headers.items(multi=True),
        body=flow.request.get_content(strict=False),
    )
    matches = _POLICY.matches(inspected)
    if matches:
        _audit(
            flow,
            decision="deny_request",
            phase="request",
            pattern_hashes=matches,
        )
        flow.metadata["bioeval_source_policy_blocked"] = True
        flow.response = _blocked_response()


def response(flow: http.HTTPFlow) -> None:
    if flow.response is None:
        return
    if flow.metadata.get("bioeval_source_policy_blocked"):
        return
    inspected = response_filter_text(
        headers=flow.response.headers.items(multi=True),
        body=flow.response.get_content(strict=False),
    )
    matches = _POLICY.matches(inspected)
    if matches:
        _audit(
            flow,
            decision="deny_response",
            phase="response",
            pattern_hashes=matches,
        )
        flow.metadata["bioeval_source_policy_blocked"] = True
        flow.response = _blocked_response()
        return
    _audit(flow, decision="allow", phase="response")


def error(flow: http.HTTPFlow) -> None:
    _audit(flow, decision="upstream_error", phase="error")
