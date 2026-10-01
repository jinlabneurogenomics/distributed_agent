"""Public failures raised after a query backend persists diagnostics."""


class QueryBackendError(RuntimeError):
    """Base class for durable query-backend failures."""


class CodexQueryError(QueryBackendError):
    """The Codex executable backend failed."""


class ApiQueryError(QueryBackendError):
    """The direct OpenAI API backend failed."""
