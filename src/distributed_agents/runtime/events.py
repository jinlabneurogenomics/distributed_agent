"""Normalization of Codex JSONL lifecycle and usage events."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CodexEventSummary:
    completed_turns: int = 0
    failed_turns: int = 0
    subagents_started: int = 0
    subagents_completed: int = 0
    subagents_failed: int = 0
    warnings: tuple[str, ...] = ()
    errors: tuple[str, ...] = ()


def _nested_strings(value: object):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield str(key)
            yield from _nested_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _nested_strings(item)


def parse_codex_events(events_path: Path) -> CodexEventSummary:
    """Summarize completion, diagnostics, and native delegation from JSONL events."""
    completed = failed = spawn_calls_started = 0
    spawned_agents: set[str] = set()
    completed_agents: set[str] = set()
    failed_agents: set[str] = set()
    warnings: list[str] = []
    errors: list[str] = []
    try:
        lines = events_path.read_text().splitlines()
    except OSError:
        lines = []
    for line in lines:
        try:
            event = json.loads(line)
        except (json.JSONDecodeError, TypeError):
            continue
        if not isinstance(event, dict):
            continue
        event_type = str(event.get("type", ""))
        item = event.get("item") if isinstance(event.get("item"), dict) else {}
        item_type = str(item.get("type", ""))
        error = event.get("error") if isinstance(event.get("error"), dict) else {}
        message = str(
            item.get("message") or event.get("message") or error.get("message") or ""
        ).strip()
        if event_type == "turn.completed":
            completed += 1
        elif event_type == "turn.failed":
            failed += 1
            errors.append(message or event_type)
        elif event_type == "error":
            # Codex emits transient reconnect events as top-level errors even
            # when a later fallback succeeds. Preserve them as diagnostics;
            # only turn.failed is terminal.
            warnings.append(message or "Codex emitted a runtime warning")
        if event_type == "item.completed" and item_type == "error":
            warnings.append(message or "Codex emitted an item-level error")

        values = set(_nested_strings(event))
        is_spawn = bool(values.intersection({"spawn_agent", "spawn_agents_on_csv"}))
        if is_spawn and event_type in {"item.started", "tool.started"}:
            spawn_calls_started += 1
        receiver_ids = item.get("receiver_thread_ids")
        if is_spawn and isinstance(receiver_ids, list):
            spawned_agents.update(str(value) for value in receiver_ids if value)
        agent_states = item.get("agents_states")
        if isinstance(agent_states, dict):
            for thread_id, state in agent_states.items():
                if not isinstance(state, dict):
                    continue
                status = str(state.get("status", "")).lower()
                if status == "completed":
                    completed_agents.add(str(thread_id))
                elif status in {"failed", "errored", "interrupted", "cancelled"}:
                    failed_agents.add(str(thread_id))
    return CodexEventSummary(
        completed_turns=completed,
        failed_turns=failed,
        subagents_started=len(spawned_agents) or spawn_calls_started,
        subagents_completed=len(completed_agents),
        subagents_failed=len(failed_agents),
        warnings=tuple(dict.fromkeys(warnings)),
        errors=tuple(dict.fromkeys(errors)),
    )


def codex_thread_id(events_path: Path) -> str | None:
    """Return the persisted Codex thread id recorded in a JSONL event stream."""

    try:
        lines = events_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None
    for line in lines:
        try:
            event = json.loads(line)
        except (json.JSONDecodeError, TypeError):
            continue
        if not isinstance(event, dict) or event.get("type") != "thread.started":
            continue
        thread_id = event.get("thread_id")
        if isinstance(thread_id, str) and thread_id.strip():
            return thread_id.strip()
    return None
