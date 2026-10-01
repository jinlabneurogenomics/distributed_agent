"""Interactive chat subcommand."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ..chat import ChatStateError, SandboxedChat, run_terminal_repl
from ..query import CODEX_AUTH_MODES, CODEX_REASONING_EFFORTS, CodexQueryOptions


def add_parser(subcommands: argparse._SubParsersAction) -> None:
    parser = subcommands.add_parser(
        "chat",
        help="Open a persistent adaptive DistributedAgents chat in an allowlist sandbox.",
    )
    parser.add_argument("initial_message", nargs="?")
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--mode", choices=("adaptive", "direct"), default="adaptive")
    parser.add_argument("--model")
    parser.add_argument("--corpus-release")
    parser.add_argument("--skills-destination", default="")
    parser.add_argument("--skills-index-container-path", default="")
    parser.add_argument("--codex-auth", choices=CODEX_AUTH_MODES, default="chatgpt")
    parser.add_argument("--codex-executable", default="codex")
    parser.add_argument("--codex-input-root", action="append", type=Path, default=[])
    parser.add_argument("--codex-config-override", action="append", default=[])
    parser.add_argument(
        "--codex-reasoning-effort",
        choices=CODEX_REASONING_EFFORTS,
        default="high",
    )
    parser.add_argument("--codex-timeout-seconds", type=float, default=0.0)
    parser.add_argument("--codex-max-concurrent-subagents", type=int, default=3)
    parser.add_argument("--codex-max-subagents", type=int, default=24)
    parser.set_defaults(func=run)


def run(args: argparse.Namespace, parser: argparse.ArgumentParser) -> int:
    if args.codex_timeout_seconds < 0:
        parser.error("--codex-timeout-seconds must be >= 0")
    if args.codex_max_concurrent_subagents < 1:
        parser.error("--codex-max-concurrent-subagents must be >= 1")
    if args.codex_max_subagents < args.codex_max_concurrent_subagents:
        parser.error(
            "--codex-max-subagents must be >= --codex-max-concurrent-subagents"
        )
    try:
        chat = SandboxedChat(
            args.out_dir,
            working_directory=Path.cwd(),
            model=args.model,
            mode=args.mode,
            corpus_release=args.corpus_release,
            skills_destination=args.skills_destination,
            skills_index_container_path=args.skills_index_container_path,
            codex_options=CodexQueryOptions(
                auth=args.codex_auth,
                sandbox="workspace-write",
                executable=args.codex_executable,
                bwrap=True,
                reasoning_effort=args.codex_reasoning_effort,
                timeout_seconds=args.codex_timeout_seconds,
                max_concurrent_subagents=args.codex_max_concurrent_subagents,
                max_subagents=args.codex_max_subagents,
                input_roots=tuple(args.codex_input_root),
                config_overrides=tuple(args.codex_config_override),
            ),
        )
    except (ChatStateError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return run_terminal_repl(chat, initial_message=args.initial_message)
