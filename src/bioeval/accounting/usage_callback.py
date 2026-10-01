"""Append per-request LiteLLM usage and cost to JSONL.

This module runs *inside the litellm-proxy environment* (see the ``litellm``
pixi feature), not the eval environment. It therefore imports only the stdlib
and ``litellm`` — never ``bioeval``. BioEval's generated single-model proxy
config loads ``usage_callback.usage_logger``; the launcher puts this
file's directory on ``PYTHONPATH`` and sets ``BIOEVAL_USAGE_LOG`` to the
destination.

One JSON object is written per completed (or failed) LLM request. bioeval
attributes rows to a framework run by wall-clock window (``ts_start`` falling
between the subprocess start and end), so no per-request tagging is needed.
"""

from __future__ import annotations

import json
import os
import threading

from litellm.integrations.custom_logger import CustomLogger

_WRITE_LOCK = threading.Lock()


def _epoch(value) -> float | None:
    """Coerce a litellm callback timestamp (datetime or float) to epoch seconds."""
    if value is None:
        return None
    ts = getattr(value, "timestamp", None)
    if callable(ts):
        return ts()
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _first(*values):
    for value in values:
        if value is not None:
            return value
    return None


class UsageLogger(CustomLogger):
    """Append usage rows for every proxied request to ``$BIOEVAL_USAGE_LOG``."""

    def _row(self, kwargs, response_obj, start_time, end_time, *, ok: bool) -> dict:
        slo = kwargs.get("standard_logging_object") or {}

        usage = {}
        if isinstance(response_obj, dict):
            usage = response_obj.get("usage") or {}
        else:
            usage = getattr(response_obj, "usage", None) or {}
        usage_get = (
            usage.get
            if isinstance(usage, dict)
            else (lambda k: getattr(usage, k, None))
        )

        prompt_tokens = _first(
            slo.get("prompt_tokens"),
            usage_get("prompt_tokens"),
            usage_get("input_tokens"),
        )
        completion_tokens = _first(
            slo.get("completion_tokens"),
            usage_get("completion_tokens"),
            usage_get("output_tokens"),
        )
        total_tokens = _first(slo.get("total_tokens"), usage_get("total_tokens"))
        prompt_details = usage_get("prompt_tokens_details") or {}
        details_get = (
            prompt_details.get
            if isinstance(prompt_details, dict)
            else lambda k: getattr(prompt_details, k, None)
        )
        cache_read_tokens = _first(
            usage_get("cache_read_input_tokens"),
            usage_get("cached_input_tokens"),
            details_get("cached_tokens"),
        )
        cache_creation_tokens = usage_get("cache_creation_input_tokens")
        response_cost = _first(slo.get("response_cost"), kwargs.get("response_cost"))

        return {
            "ts_start": _epoch(start_time),
            "ts_end": _epoch(end_time),
            "ok": ok,
            "model": _first(slo.get("model"), kwargs.get("model")),
            "call_type": _first(slo.get("call_type"), kwargs.get("call_type")),
            "request_id": _first(slo.get("request_id"), slo.get("id")),
            # Stable per-logical-call id. The Responses API fires the success
            # callback twice with the same id; aggregation dedups on this.
            "litellm_call_id": _first(
                kwargs.get("litellm_call_id"), slo.get("litellm_call_id")
            ),
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "cache_read_input_tokens": cache_read_tokens,
            "cache_creation_input_tokens": cache_creation_tokens,
            "response_cost": response_cost,
            # Surfaces unregistered pricing during verification: tokens but no $.
            "cost_unconfigured": bool((total_tokens or 0) > 0 and not response_cost),
        }

    def _write(self, row: dict) -> None:
        path = os.environ.get("BIOEVAL_USAGE_LOG")
        if not path:
            return
        line = json.dumps(row) + "\n"
        with _WRITE_LOCK:
            with open(path, "a") as fh:
                fh.write(line)
                fh.flush()

    # litellm invokes the async variants on the proxy; sync ones cover direct use.
    def log_success_event(self, kwargs, response_obj, start_time, end_time):
        self._write(self._row(kwargs, response_obj, start_time, end_time, ok=True))

    async def async_log_success_event(self, kwargs, response_obj, start_time, end_time):
        self._write(self._row(kwargs, response_obj, start_time, end_time, ok=True))

    def log_failure_event(self, kwargs, response_obj, start_time, end_time):
        self._write(self._row(kwargs, response_obj, start_time, end_time, ok=False))

    async def async_log_failure_event(self, kwargs, response_obj, start_time, end_time):
        self._write(self._row(kwargs, response_obj, start_time, end_time, ok=False))


# Instance referenced by each generated single-model proxy config.
usage_logger = UsageLogger()
