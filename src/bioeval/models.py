"""Shared comparison-run data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .runtime.policy import SourcePolicy


@dataclass(frozen=True)
class FrameworkPrompt:
    """Rendered prompt and run directory for one framework."""

    framework: str
    run_dir: Path
    prompt_path: Path
    expected_outputs: tuple[Path, ...]


@dataclass(frozen=True)
class PromptRun:
    """Resolved layout for one prompt-file run."""

    prompt_file: Path
    question_id: str
    run_id: str
    eval_root: Path
    old_output_dir: Path | None
    frameworks: tuple[FrameworkPrompt, ...]
    created_at: str
    # Declared input files (declarative task specs only): substituted into the
    # prompt AND used as the sandbox read-only mount allowlist. Empty for
    # legacy prompt-file runs.
    declared_inputs: tuple[Path, ...] = ()
    # Optional task-level source denial. The secret deny strings are retained
    # only in harness memory and are never serialized into the agent-visible
    # run directory.
    source_policy: SourcePolicy | None = None


@dataclass
class FrameworkRunResult:
    """Execution result for one framework."""

    framework: str
    run_dir: Path
    prompt_path: Path
    expected_outputs: tuple[Path, ...]
    model: str | None = None
    returncode: int | None = None
    command: list[str] | None = None
    log_path: Path | None = None
    output_status: dict[str, bool] = field(default_factory=dict)
    duration_s: float | None = None
    usage: dict | None = None
    source_policy_audit: dict | None = None
