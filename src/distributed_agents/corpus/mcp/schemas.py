"""JSON Schema builders for corpus MCP tools."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from .constants import MAX_ROWS


def _schema(
    properties: Mapping[str, Any], required: Sequence[str] = ()
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "type": "object",
        "properties": dict(properties),
        "additionalProperties": False,
    }
    if required:
        result["required"] = list(required)
    return result


def _string_schema(
    description: str,
    *,
    enum: Sequence[str] | None = None,
    default: str | None = None,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "type": "string",
        "minLength": 1,
        "maxLength": 256,
        "description": description,
    }
    if enum is not None:
        result["enum"] = list(enum)
    if default is not None:
        result["default"] = default
    return result


def _string_array_schema(
    description: str, *, max_items: int = 50
) -> dict[str, Any]:
    return {
        "type": "array",
        "items": {"type": "string", "minLength": 1, "maxLength": 256},
        "maxItems": max_items,
        "uniqueItems": True,
        "description": description,
    }


def _limit_schema(default: int) -> dict[str, Any]:
    return {
        "type": "integer",
        "minimum": 1,
        "maximum": MAX_ROWS,
        "default": default,
        "description": "Maximum rows returned; truncation is explicit.",
    }


def _offset_schema() -> dict[str, Any]:
    return {
        "type": "integer",
        "minimum": 0,
        "maximum": 1_000_000,
        "default": 0,
        "description": "Zero-based offset into the deterministic result set.",
    }


def _number_schema(
    description: str,
    *,
    minimum: float,
    maximum: float,
    default: float,
    exclusive: bool = False,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "type": "number",
        "default": default,
        "description": description,
    }
    result["exclusiveMinimum" if exclusive else "minimum"] = minimum
    result["exclusiveMaximum" if exclusive else "maximum"] = maximum
    return result


def _boolean_schema(description: str, default: bool) -> dict[str, Any]:
    return {"type": "boolean", "default": default, "description": description}


def _tool(name: str, title: str, description: str, input_schema: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "name": name,
        "title": title,
        "description": description,
        "inputSchema": dict(input_schema),
        "annotations": {
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    }
