"""Persistent chat state models."""

from dataclasses import dataclass
from pathlib import Path

from ..query import QueryResult


class ChatStateError(RuntimeError):
    """Raised when a persisted chat is incompatible or incomplete."""


@dataclass(frozen=True)
class ChatTurn:
    """One archived interactive turn."""

    answer: str
    session_id: str
    turn_number: int
    thread_id: str
    trace_dir: Path
    result: QueryResult

