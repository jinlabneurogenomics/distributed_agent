"""Argument validation, parsing, pagination, and output bounds."""

from __future__ import annotations

import json
from collections import Counter
from typing import Any, Mapping, Sequence

from .constants import MAX_OUTPUT_BYTES, MAX_ROWS, SEARCH_TOKEN
from .errors import CorpusToolError


def _check_keys(arguments: Mapping[str, Any], allowed: set[str]) -> None:
    extras = sorted(set(arguments) - allowed)
    if extras:
        raise CorpusToolError(f"unexpected arguments: {', '.join(extras)}")


def _required_string(arguments: Mapping[str, Any], name: str) -> str:
    value = arguments.get(name)
    if not isinstance(value, str) or not value.strip():
        raise CorpusToolError(f"{name} must be a non-empty string")
    if len(value) > 256:
        raise CorpusToolError(f"{name} exceeds 256 characters")
    return value.strip()


def _optional_string(arguments: Mapping[str, Any], name: str) -> str | None:
    if name not in arguments or arguments[name] is None:
        return None
    return _required_string(arguments, name)


def _enum(
    arguments: Mapping[str, Any],
    name: str,
    values: Sequence[str],
    *,
    default: str | None = None,
) -> str:
    value = default if name not in arguments else _required_string(arguments, name)
    if value is None or value not in values:
        raise CorpusToolError(f"{name} must be one of: {', '.join(values)}")
    return value


def _string_list(
    arguments: Mapping[str, Any],
    name: str,
    *,
    required: bool = False,
    max_items: int = 50,
) -> list[str]:
    value = arguments.get(name, [])
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item.strip() or len(item) > 256 for item in value
    ):
        raise CorpusToolError(f"{name} must be an array of non-empty strings")
    if len(value) > max_items or len(set(value)) != len(value):
        raise CorpusToolError(
            f"{name} must contain at most {max_items} unique values"
        )
    if required and not value:
        raise CorpusToolError(f"{name} must contain at least one value")
    return value


def _integer(
    arguments: Mapping[str, Any],
    name: str,
    *,
    minimum: int,
    maximum: int,
    default: int,
) -> int:
    value = arguments.get(name, default)
    if (
        isinstance(value, bool)
        or not isinstance(value, int)
        or not minimum <= value <= maximum
    ):
        raise CorpusToolError(
            f"{name} must be an integer between {minimum} and {maximum}"
        )
    return value


def _number(
    arguments: Mapping[str, Any],
    name: str,
    *,
    minimum: float,
    maximum: float,
    default: float,
    exclusive: bool = False,
) -> float:
    value = arguments.get(name, default)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CorpusToolError(f"{name} must be a number")
    parsed = float(value)
    valid = (
        minimum < parsed < maximum
        if exclusive
        else minimum <= parsed <= maximum
    )
    if not valid:
        qualifier = "strictly between" if exclusive else "between"
        raise CorpusToolError(
            f"{name} must be {qualifier} {minimum:g} and {maximum:g}"
        )
    return parsed


def _limit(arguments: Mapping[str, Any], *, default: int) -> int:
    value = arguments.get("limit", default)
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= MAX_ROWS:
        raise CorpusToolError(f"limit must be an integer between 1 and {MAX_ROWS}")
    return value


def _limit_named(arguments: Mapping[str, Any], name: str, *, default: int) -> int:
    value = arguments.get(name, default)
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= MAX_ROWS:
        raise CorpusToolError(f"{name} must be an integer between 1 and {MAX_ROWS}")
    return value


def _offset(arguments: Mapping[str, Any], name: str) -> int:
    value = arguments.get(name, 0)
    if (
        isinstance(value, bool)
        or not isinstance(value, int)
        or not 0 <= value <= 1_000_000
    ):
        raise CorpusToolError(f"{name} must be an integer between 0 and 1000000")
    return value


def _boolean(arguments: Mapping[str, Any], name: str, *, default: bool) -> bool:
    value = arguments.get(name, default)
    if not isinstance(value, bool):
        raise CorpusToolError(f"{name} must be a boolean")
    return value


def _search_terms(value: str) -> list[str]:
    return [match.group(0).casefold() for match in SEARCH_TOKEN.finditer(value)]


def _page_metadata(
    offset: int, limit: int, exact_total: int, emitted: int
) -> dict[str, Any]:
    return {
        "offset": offset,
        "limit": limit,
        "exact_total": exact_total,
        "emitted": emitted,
        "has_more": offset + emitted < exact_total,
        "next_offset": offset + emitted if offset + emitted < exact_total else None,
        "truncated_by_output_bytes": False,
        "max_rows": MAX_ROWS,
        "max_output_bytes": MAX_OUTPUT_BYTES,
    }


def _parse_json_object(value: str, operation: str) -> dict[str, Any]:
    try:
        payload = json.loads(value)
    except json.JSONDecodeError as exc:
        raise CorpusToolError(f"{operation} adapter returned invalid JSON") from exc
    if not isinstance(payload, dict):
        raise CorpusToolError(f"{operation} adapter returned a non-object JSON value")
    return payload


def _parse_json_array(value: str, operation: str) -> list[dict[str, Any]]:
    try:
        payload = json.loads(value)
    except json.JSONDecodeError as exc:
        raise CorpusToolError(f"{operation} adapter returned invalid JSON") from exc
    if not isinstance(payload, list) or any(not isinstance(row, dict) for row in payload):
        raise CorpusToolError(f"{operation} adapter returned a non-object JSON array")
    return payload


def _parse_json_lines(value: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(value.splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise CorpusToolError(f"ledger adapter returned invalid JSON on line {line_number}") from exc
        if not isinstance(row, dict):
            raise CorpusToolError(f"ledger adapter returned a non-object on line {line_number}")
        records.append(row)
    return records


def _json_size(payload: Mapping[str, Any]) -> int:
    return len(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8"))


def _bound_list_fields(
    payload: dict[str, Any], list_fields: Sequence[str]
) -> dict[str, Any]:
    result = {**payload, **{field: list(payload[field]) for field in list_fields}}
    page_names = {
        "left_to_right_references": "left_to_right_page",
        "right_to_left_references": "right_to_left_page",
    }

    def page_for(field: str) -> dict[str, Any] | None:
        named = page_names.get(field, f"{field}_page")
        page = result.get(named)
        if not isinstance(page, dict):
            page = result.get("page")
        return page if isinstance(page, dict) else None

    removed: Counter[str] = Counter()
    while _json_size(result) > MAX_OUTPUT_BYTES:
        candidates = [field for field in list_fields if result[field]]
        if not candidates:
            raise CorpusToolError("bounded graph metadata exceeds the output byte ceiling")
        field = max(candidates, key=lambda value: len(result[value]))
        result[field].pop()
        removed[field] += 1
        page = page_for(field)
        if page is not None:
            page["emitted"] = len(result[field])
            page["has_more"] = True
            page["next_offset"] = page["offset"] + len(result[field])
            page["truncated_by_output_bytes"] = True
    return result


def _bound_analog_suggestions(payload: dict[str, Any]) -> dict[str, Any]:
    """Trim nested per-target candidate pages without dropping target status."""

    result = {
        **payload,
        "targets": [
            {**target, "candidates": list(target["candidates"])}
            for target in payload["targets"]
        ],
    }
    while _json_size(result) > MAX_OUTPUT_BYTES:
        candidates = [
            target for target in result["targets"] if target["candidates"]
        ]
        if not candidates:
            raise CorpusToolError(
                "bounded target-analog metadata exceeds the output byte ceiling"
            )
        target = max(
            candidates,
            key=lambda row: (
                len(row["candidates"]),
                str(row["canonical_target"]).casefold(),
            ),
        )
        target["candidates"].pop()
        page = target["page"]
        page["emitted"] = len(target["candidates"])
        page["has_more"] = True
        page["next_offset"] = page["offset"] + len(target["candidates"])
        page["truncated_by_output_bytes"] = True
    return result


def _bound_records(payload: dict[str, Any]) -> dict[str, Any]:
    records = list(payload["records"])
    removed = 0
    while records:
        candidate = {**payload, "records": records}
        candidate["truncation"] = {
            **payload["truncation"],
            "truncated": bool(payload["truncation"]["truncated"] or removed),
            "emitted": len(records),
        }
        if _json_size(candidate) <= MAX_OUTPUT_BYTES:
            return candidate
        records.pop()
        removed += 1
    candidate = {**payload, "records": []}
    candidate["truncation"] = {
        **payload["truncation"],
        "truncated": bool(payload["records"]),
        "emitted": 0,
    }
    if _json_size(candidate) > MAX_OUTPUT_BYTES:
        raise CorpusToolError("bounded ledger metadata exceeds the output byte ceiling")
    return candidate


def _bound_evidence(payload: dict[str, Any], release_id: str) -> dict[str, Any]:
    evidence = payload.get("evidence") or []
    references = payload.get("references") or []
    if not isinstance(evidence, list) or not isinstance(references, list):
        raise CorpusToolError("evidence adapter returned an invalid response shape")
    evidence_total = len(evidence)
    references_total = len(references)
    result: dict[str, Any] = {
        "schema_version": "distributed_agents-corpus-mcp-v1",
        "operation": "corpus.evidence.resolve",
        "release_id": release_id,
        "evidence": list(evidence),
        "references": list(references),
        "truncation": {
            "truncated": False,
            "evidence_total": evidence_total,
            "references_total": references_total,
            "evidence_emitted": evidence_total,
            "references_emitted": references_total,
            "max_output_bytes": MAX_OUTPUT_BYTES,
        },
    }
    while _json_size(result) > MAX_OUTPUT_BYTES:
        if not (result["references"] or result["evidence"]):
            raise CorpusToolError("bounded evidence metadata exceeds the output byte ceiling")
        result["truncation"]["truncated"] = True
        if result["references"]:
            result["references"].pop()
        elif result["evidence"]:
            result["evidence"].pop()
        result["truncation"]["evidence_emitted"] = len(result["evidence"])
        result["truncation"]["references_emitted"] = len(result["references"])
    return result
