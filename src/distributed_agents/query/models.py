"""Stable request, option, and result types for query backends."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


QueryBackendName = Literal["codex", "api"]
QueryRunStatus = Literal["completed", "completed_with_warnings", "failed"]
QueryMode = Literal["adaptive", "direct"]

QUERY_BACKENDS: tuple[QueryBackendName, ...] = ("codex", "api")
QUERY_MODES: tuple[QueryMode, ...] = ("adaptive", "direct")

DEFAULT_CODEX_CHATGPT_MODEL = "gpt-rosalind-5.5"
DEFAULT_CODEX_API_MODEL = "gpt-rosalind-260428"
DEFAULT_CODEX_REASONING_EFFORT = "high"
DEFAULT_API_MODEL = "gpt-rosalind-260428"
DEFAULT_API_REASONING_EFFORT = "high"
DEFAULT_MAX_CONCURRENT_SUBAGENTS = 3
DEFAULT_MAX_SUBAGENTS = 24

CODEX_AUTH_MODES = ("chatgpt", "apikey")
CODEX_SANDBOX_MODES = ("read-only", "workspace-write", "danger-full-access")
CODEX_REASONING_EFFORTS = ("minimal", "low", "medium", "high", "xhigh", "max")
API_REASONING_EFFORTS = ("minimal", "low", "medium", "high")


@dataclass(frozen=True)
class CodexQueryOptions:
    """Runtime controls for the default Codex executable backend."""

    auth: Literal["chatgpt", "apikey"] = "chatgpt"
    sandbox: Literal["read-only", "workspace-write", "danger-full-access"] = (
        "workspace-write"
    )
    executable: str = "codex"
    bwrap: bool = True
    reasoning_effort: str = DEFAULT_CODEX_REASONING_EFFORT
    timeout_seconds: float = 0.0
    max_concurrent_subagents: int = DEFAULT_MAX_CONCURRENT_SUBAGENTS
    max_subagents: int = DEFAULT_MAX_SUBAGENTS
    input_roots: tuple[Path, ...] | None = None
    config_overrides: tuple[str, ...] = ()
    session_home: Path | None = None
    resume_session_id: str | None = None


@dataclass(frozen=True)
class ApiQueryOptions:
    """Runtime controls for the direct OpenAI Agents SDK backend."""

    reasoning_effort: str = DEFAULT_API_REASONING_EFFORT
    max_turns: int = 50
    max_concurrent_subagents: int = DEFAULT_MAX_CONCURRENT_SUBAGENTS
    max_subagents: int = DEFAULT_MAX_SUBAGENTS
    input_roots: tuple[Path, ...] | None = None


@dataclass(frozen=True)
class QueryRequest:
    """Complete input to one query backend invocation."""

    query: str
    backend: QueryBackendName = "codex"
    model: str | None = None
    skills_destination: str = ""
    skills_index_container_path: str = ""
    out_dir: Path | None = None
    working_directory: Path | None = None
    codex: CodexQueryOptions = field(default_factory=CodexQueryOptions)
    api: ApiQueryOptions = field(default_factory=ApiQueryOptions)
    mode: QueryMode = "adaptive"
    corpus_release: str | None = None


@dataclass(frozen=True)
class QueryResult:
    """Normalized result returned by every query backend."""

    answer: str
    backend: QueryBackendName
    model: str
    status: QueryRunStatus
    run_dir: Path | None = None
    returncode: int | None = None
    duration_s: float | None = None
    usage: dict | None = None
    warnings: tuple[str, ...] = ()
    artifacts: dict[str, str] = field(default_factory=dict)
    thread_id: str | None = None
