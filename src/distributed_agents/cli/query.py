"""One-shot query subcommand."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from ..corpus.registry import CorpusRegistryError
from ..query import (
    API_REASONING_EFFORTS,
    CODEX_AUTH_MODES,
    CODEX_REASONING_EFFORTS,
    CODEX_SANDBOX_MODES,
    QUERY_BACKENDS,
    QUERY_MODES,
    ApiQueryError,
    ApiQueryOptions,
    CodexQueryError,
    CodexQueryOptions,
    run_query_pipeline,
)


def add_parser(subcommands: argparse._SubParsersAction) -> None:
    parser = subcommands.add_parser(
        "query",
        help="Run an adaptive research query (Codex backend by default).",
    )
    parser.add_argument("query", nargs="?")
    parser.add_argument("--task-file")
    parser.add_argument("--mode", choices=QUERY_MODES, default="adaptive")
    parser.add_argument("--corpus-release")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument(
        "--backend",
        choices=QUERY_BACKENDS,
        default="codex",
        help="Execution backend: Codex executable (default) or direct API.",
    )
    parser.add_argument("--model")
    parser.add_argument("--skills-destination", default="")
    parser.add_argument("--skills-index-container-path", default="")
    parser.add_argument("--codex-auth", choices=CODEX_AUTH_MODES, default="chatgpt")
    parser.add_argument(
        "--codex-sandbox",
        choices=CODEX_SANDBOX_MODES,
        default="workspace-write",
    )
    parser.add_argument("--codex-executable", default="codex")
    parser.add_argument(
        "--codex-bwrap",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    parser.add_argument("--codex-input-root", action="append", type=Path)
    parser.add_argument("--codex-config-override", action="append", default=[])
    parser.add_argument(
        "--codex-reasoning-effort",
        choices=CODEX_REASONING_EFFORTS,
        default="high",
    )
    parser.add_argument("--codex-timeout-seconds", type=float, default=0.0)
    parser.add_argument(
        "--codex-max-concurrent-subagents",
        type=int,
        default=3,
        help="Maximum concurrent adaptive sweep readers (default 3).",
    )
    parser.add_argument(
        "--codex-max-subagents",
        type=int,
        default=24,
        help=(
            "Maximum reader starts, including retries, in one adaptive query "
            "(default 24)."
        ),
    )
    parser.add_argument("--api-input-root", action="append", type=Path)
    parser.add_argument(
        "--api-reasoning-effort",
        choices=API_REASONING_EFFORTS,
        default="high",
    )
    parser.add_argument("--api-max-turns", type=int, default=50)
    parser.add_argument(
        "--api-max-concurrent-subagents",
        type=int,
        default=3,
        help="Maximum concurrent adaptive API sweep readers (default 3).",
    )
    parser.add_argument(
        "--api-max-subagents",
        type=int,
        default=24,
        help="Maximum reader-agent calls in one adaptive API query (default 24).",
    )
    parser.set_defaults(func=run)


def _query_text(args: argparse.Namespace, parser: argparse.ArgumentParser) -> str:
    if args.task_file and args.query:
        parser.error("provide either a query string or --task-file, not both")
    if args.task_file:
        return Path(args.task_file).read_text()
    if args.query:
        return args.query
    parser.error("provide a query string or --task-file")


def run(args: argparse.Namespace, parser: argparse.ArgumentParser) -> int:
    query = _query_text(args, parser)
    if args.codex_timeout_seconds < 0:
        parser.error("--codex-timeout-seconds must be >= 0")
    if args.api_max_turns < 1:
        parser.error("--api-max-turns must be >= 1")
    for name in (
        "codex_max_concurrent_subagents",
        "codex_max_subagents",
        "api_max_concurrent_subagents",
        "api_max_subagents",
    ):
        if getattr(args, name) < 1:
            parser.error(f"--{name.replace('_', '-')} must be >= 1")
    if args.codex_max_subagents < args.codex_max_concurrent_subagents:
        parser.error(
            "--codex-max-subagents must be >= --codex-max-concurrent-subagents"
        )
    if args.api_max_subagents < args.api_max_concurrent_subagents:
        parser.error(
            "--api-max-subagents must be >= --api-max-concurrent-subagents"
        )
    out_dir = Path(args.out_dir).resolve()
    launch_cwd = Path.cwd()
    out_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("DISTRIBUTED_AGENTS_TOOLLOG", str(out_dir / "tool_calls.jsonl"))
    os.environ.setdefault("DISTRIBUTED_AGENTS_OUTPUT_DIR", str(out_dir))
    os.chdir(out_dir)
    try:
        answer = run_query_pipeline(
            query,
            skills_destination=args.skills_destination,
            skills_index_container_path=args.skills_index_container_path,
            model=args.model,
            backend=args.backend,
            out_dir=out_dir,
            working_directory=launch_cwd,
            codex_options=CodexQueryOptions(
                auth=args.codex_auth,
                sandbox=args.codex_sandbox,
                executable=args.codex_executable,
                bwrap=args.codex_bwrap,
                reasoning_effort=args.codex_reasoning_effort,
                timeout_seconds=args.codex_timeout_seconds,
                max_concurrent_subagents=args.codex_max_concurrent_subagents,
                max_subagents=args.codex_max_subagents,
                input_roots=(
                    tuple(args.codex_input_root) if args.codex_input_root else None
                ),
                config_overrides=tuple(args.codex_config_override),
            ),
            api_options=ApiQueryOptions(
                reasoning_effort=args.api_reasoning_effort,
                max_turns=args.api_max_turns,
                max_concurrent_subagents=args.api_max_concurrent_subagents,
                max_subagents=args.api_max_subagents,
                input_roots=tuple(args.api_input_root) if args.api_input_root else None,
            ),
            mode=args.mode,
            corpus_release=args.corpus_release,
        )
    except (ApiQueryError, CodexQueryError, CorpusRegistryError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    finally:
        os.chdir(launch_cwd)
    (out_dir / "query.md").write_text(answer)
    print(f"wrote {out_dir / 'query.md'}")
    return 0
