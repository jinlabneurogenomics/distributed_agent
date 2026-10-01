"""Serialize per-framework results and comparison summaries."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from ..models import FrameworkRunResult


def framework_result_to_dict(result: FrameworkRunResult) -> dict:
    """Return a JSON-serialisable representation of one framework result."""
    return {
        "schema_version": 2,
        "framework": result.framework,
        "model": result.model,
        "run_dir": str(result.run_dir),
        "prompt_path": str(result.prompt_path),
        "expected_outputs": [str(path) for path in result.expected_outputs],
        "returncode": result.returncode,
        "command": result.command,
        "log_path": str(result.log_path) if result.log_path else None,
        "output_status": result.output_status,
        "duration_s": result.duration_s,
        "usage": result.usage,
        "source_policy_audit": result.source_policy_audit,
    }


def write_framework_result(result: FrameworkRunResult) -> Path:
    """Write the canonical per-framework result artifact."""
    path = result.run_dir / "runner_result.json"
    path.write_text(json.dumps(framework_result_to_dict(result), indent=2) + "\n")
    return path


def write_summary(eval_root: Path, results: Iterable[FrameworkRunResult]) -> Path:
    """Write run summary metadata."""
    path = eval_root / "run_summary.json"
    path.write_text(
        json.dumps([framework_result_to_dict(result) for result in results], indent=2)
        + "\n"
    )
    return path
