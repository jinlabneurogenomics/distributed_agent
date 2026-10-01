"""DistributedAgents public API with dependency-light package initialization."""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Any

__version__ = "0.0.0"

if TYPE_CHECKING:
    from .build import BuildRequest, BuildResult, build_findings_report
    from .query import (
        ApiQueryOptions,
        CodexQueryOptions,
        QueryRequest,
        QueryResult,
        run_query_job,
        run_query_pipeline,
    )

__all__ = [
    "__version__",
    "ApiQueryOptions",
    "BuildRequest",
    "BuildResult",
    "CodexQueryOptions",
    "QueryRequest",
    "QueryResult",
    "build_findings_report",
    "run_query_job",
    "run_query_pipeline",
]

_LAZY_EXPORTS = {
    "ApiQueryOptions": (".query", "ApiQueryOptions"),
    "BuildRequest": (".build", "BuildRequest"),
    "BuildResult": (".build", "BuildResult"),
    "CodexQueryOptions": (".query", "CodexQueryOptions"),
    "QueryRequest": (".query", "QueryRequest"),
    "QueryResult": (".query", "QueryResult"),
    "build_findings_report": (".build", "build_findings_report"),
    "run_query_job": (".query", "run_query_job"),
    "run_query_pipeline": (".query", "run_query_pipeline"),
}


def __getattr__(name: str) -> Any:
    """Load public runtime surfaces only when callers request them."""

    target = _LAZY_EXPORTS.get(name)
    if target is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_name, attribute = target
    value = getattr(import_module(module_name, __name__), attribute)
    globals()[name] = value
    return value
