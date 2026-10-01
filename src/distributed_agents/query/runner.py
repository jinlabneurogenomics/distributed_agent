"""Backend selection and normalized query execution."""

from __future__ import annotations

from pathlib import Path

from .backends.api import run_api_query
from .backends.codex import run_codex_query
from .models import (
    DEFAULT_API_MODEL,
    DEFAULT_CODEX_API_MODEL,
    DEFAULT_CODEX_CHATGPT_MODEL,
    QUERY_BACKENDS,
    QUERY_MODES,
    ApiQueryOptions,
    CodexQueryOptions,
    QueryBackendName,
    QueryMode,
    QueryRequest,
    QueryResult,
)


def resolve_query_model(request: QueryRequest) -> str:
    """Resolve the selected backend's default without changing explicit models."""

    if request.model:
        return request.model
    if request.backend == "api":
        return DEFAULT_API_MODEL
    if request.codex.auth == "apikey":
        return DEFAULT_CODEX_API_MODEL
    return DEFAULT_CODEX_CHATGPT_MODEL


def run_query_job(request: QueryRequest) -> QueryResult:
    """Dispatch a query to the selected backend."""

    if request.backend not in QUERY_BACKENDS:
        raise ValueError(
            f"unknown query backend {request.backend!r}; choose from {QUERY_BACKENDS}"
        )
    if request.mode not in QUERY_MODES:
        raise ValueError(
            f"unknown query mode {request.mode!r}; choose from {QUERY_MODES}"
        )
    model = resolve_query_model(request)
    if request.backend == "api":
        return run_api_query(request, model=model)
    return run_codex_query(request, model=model)


def run_query_pipeline(
    query: str,
    *,
    skills_destination: str = "",
    skills_index_container_path: str = "",
    model: str | None = None,
    backend: QueryBackendName = "codex",
    out_dir: Path | None = None,
    working_directory: Path | None = None,
    codex_options: CodexQueryOptions | None = None,
    api_options: ApiQueryOptions | None = None,
    mode: QueryMode = "adaptive",
    corpus_release: str | None = None,
) -> str:
    """Run the query harness and return only its answer."""

    return run_query_job(
        QueryRequest(
            query=query,
            backend=backend,
            model=model,
            skills_destination=skills_destination,
            skills_index_container_path=skills_index_container_path,
            out_dir=out_dir,
            working_directory=working_directory,
            codex=codex_options or CodexQueryOptions(),
            api=api_options or ApiQueryOptions(),
            mode=mode,
            corpus_release=corpus_release,
        )
    ).answer
