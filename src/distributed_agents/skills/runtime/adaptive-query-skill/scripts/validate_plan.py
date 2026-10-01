#!/usr/bin/env python3
"""Validate only the safe structural waist of an adaptive evidence plan."""

from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
from typing import Any


EXPECTED_SCHEMA = "distributed_agents-adaptive-plan-v1"


def _mapping(value: object) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _safe_relative(value: object) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts


def validate_plan(plan: object, capabilities: object) -> list[str]:
    errors: list[str] = []
    root = _mapping(plan)
    manifest = _mapping(capabilities)
    if root.get("schema_version") != EXPECTED_SCHEMA:
        errors.append(f"schema_version must be {EXPECTED_SCHEMA!r}")
    declared = {
        str(row.get("id"))
        for row in manifest.get("capabilities", [])
        if isinstance(row, dict) and row.get("id")
    }
    steps = root.get("steps")
    if not isinstance(steps, list) or not steps:
        return [*errors, "steps must be a non-empty list"]

    ids: list[str] = []
    dependencies: dict[str, list[str]] = {}
    for index, raw in enumerate(steps):
        step = _mapping(raw)
        prefix = f"steps[{index}]"
        step_id = step.get("id")
        if not isinstance(step_id, str) or not step_id.strip():
            errors.append(f"{prefix}.id must be non-empty text")
            continue
        if step_id in ids:
            errors.append(f"{prefix}.id duplicates {step_id!r}")
        ids.append(step_id)
        capability = step.get("capability")
        if capability not in declared:
            errors.append(f"{prefix}.capability is not declared: {capability!r}")
        for field in ("question", "evidence_role", "stop_when"):
            if not isinstance(step.get(field), str) or not str(step[field]).strip():
                errors.append(f"{prefix}.{field} must be non-empty text")
        depends_on = step.get("depends_on")
        if not isinstance(depends_on, list) or not all(
            isinstance(value, str) and value for value in depends_on
        ):
            errors.append(f"{prefix}.depends_on must be a list of step IDs")
            depends_on = []
        dependencies[step_id] = list(depends_on)
        outputs = step.get("outputs")
        if not isinstance(outputs, list) or not outputs:
            errors.append(f"{prefix}.outputs must be a non-empty list")
        elif not all(_safe_relative(value) for value in outputs):
            errors.append(f"{prefix}.outputs must be safe relative paths")

    known = set(ids)
    for step_id, values in dependencies.items():
        missing = [value for value in values if value not in known]
        if missing:
            errors.append(f"{step_id!r} depends on unknown steps: {missing}")
        if step_id in values:
            errors.append(f"{step_id!r} depends on itself")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(step_id: str) -> None:
        if step_id in visited:
            return
        if step_id in visiting:
            errors.append(f"dependency cycle includes {step_id!r}")
            return
        visiting.add(step_id)
        for dependency in dependencies.get(step_id, []):
            if dependency in known:
                visit(dependency)
        visiting.remove(step_id)
        visited.add(step_id)

    for step_id in ids:
        visit(step_id)
    return list(dict.fromkeys(errors))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True)
    parser.add_argument("--capabilities", required=True)
    parser.add_argument("--out")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    plan = json.loads(Path(args.plan).read_text())
    capabilities = json.loads(Path(args.capabilities).read_text())
    errors = validate_plan(plan, capabilities)
    result = {
        "schema_version": "distributed_agents-adaptive-plan-validation-v1",
        "status": "failed" if errors else "passed",
        "errors": errors,
    }
    text = json.dumps(result, indent=2) + "\n"
    if args.out:
        Path(args.out).write_text(text)
    print(text, end="")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
