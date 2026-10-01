"""Line-oriented terminal interface for persistent chat."""

from __future__ import annotations

import json
import sys
from collections.abc import Callable
from typing import TextIO

from ..query import CodexQueryError
from .models import ChatStateError
from .session import SandboxedChat


_HELP = """Commands:
  /help                 Show this help.
  /new                  Start and activate a fresh, uncontaminated session.
  /sessions             List persisted sessions.
  /use SESSION          Resume a persisted session.
  /cold QUESTION        Run one question in a fresh session without switching.
  /trace                Show the active thread, mounts, and latest trace path.
  /paste                Enter a multiline question; finish with a line containing only '.'.
  /quit                 Exit. The active session remains resumable.
"""


def run_terminal_repl(
    chat: SandboxedChat,
    *,
    initial_message: str | None = None,
    input_fn: Callable[[str], str] = input,
    output: TextIO = sys.stdout,
) -> int:
    """Run the line-oriented terminal interface."""

    print(
        f"DistributedAgents chat ({chat.active_session_id}); sandbox canary passed. "
        "Type /help for commands.",
        file=output,
    )

    def submit(message: str, *, cold: bool = False) -> None:
        try:
            turn = chat.cold_ask(message) if cold else chat.ask(message)
        except (CodexQueryError, ChatStateError, ValueError) as exc:
            print(f"error: {exc}", file=output)
            return
        label = "cold" if cold else "DistributedAgents"
        print(f"\n{label} [{turn.session_id} turn {turn.turn_number}]:", file=output)
        print(turn.answer.rstrip(), file=output)
        print(f"trace: {turn.trace_dir}\n", file=output)

    if initial_message:
        submit(initial_message)
    while True:
        try:
            line = input_fn(f"distributed_agents[{chat.active_session_id}]> ")
        except (EOFError, KeyboardInterrupt):
            print("\nSession saved.", file=output)
            return 0
        message = line.strip()
        if not message:
            continue
        command, _, argument = message.partition(" ")
        if command in {"/quit", "/exit"}:
            print("Session saved.", file=output)
            return 0
        if command == "/help":
            print(_HELP, file=output)
            continue
        if command == "/new":
            session_id = chat.new_session()
            print(f"Started {session_id}.", file=output)
            continue
        if command == "/sessions":
            for row in chat.list_sessions():
                marker = "*" if row.get("session_id") == chat.active_session_id else " "
                turns = int(row.get("next_turn", 1)) - 1
                print(
                    f"{marker} {row.get('session_id')} "
                    f"kind={row.get('kind')} turns={turns}",
                    file=output,
                )
            continue
        if command == "/use":
            if not argument.strip():
                print("error: /use requires a session id", file=output)
                continue
            try:
                chat.use_session(argument.strip())
            except ChatStateError as exc:
                print(f"error: {exc}", file=output)
            else:
                print(f"Resumed {chat.active_session_id}.", file=output)
            continue
        if command == "/trace":
            print(json.dumps(chat.trace_summary(), indent=2), file=output)
            continue
        if command == "/cold":
            if not argument.strip():
                print("error: /cold requires a question", file=output)
                continue
            submit(argument.strip(), cold=True)
            continue
        if command == "/paste":
            print(
                "Enter the question; finish with a line containing only '.'.",
                file=output,
            )
            lines: list[str] = []
            while True:
                try:
                    pasted = input_fn("")
                except (EOFError, KeyboardInterrupt):
                    pasted = "."
                if pasted == ".":
                    break
                lines.append(pasted)
            submit("\n".join(lines))
            continue
        if command.startswith("/"):
            print(f"error: unknown command {command}; use /help", file=output)
            continue
        submit(message)

