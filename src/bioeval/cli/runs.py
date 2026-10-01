"""Register and execute the `bioeval runs` command."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ..artifacts.history import discover_runs, filter_runs, format_runs
from ..runtime.paths import DEFAULT_RUNS_ROOT
from .parsing import positive_int


def _runs(args: argparse.Namespace) -> int:
    records = [
        record
        for root in (args.root or [DEFAULT_RUNS_ROOT])
        for record in discover_runs(root)
    ]
    records = filter_runs(records, task=args.task, status=args.status)[: args.limit]
    if args.json:
        print(json.dumps([record.to_dict() for record in records], indent=2))
    else:
        print(format_runs(records))
    return 0


def register(subcommands: argparse._SubParsersAction) -> None:
    parser = subcommands.add_parser("runs", help="List BioEval runs.")
    parser.add_argument("--root", action="append", type=Path)
    parser.add_argument("--task")
    parser.add_argument("--status")
    parser.add_argument("--limit", type=positive_int, default=20)
    parser.add_argument("--json", action="store_true")
    parser.set_defaults(func=_runs)
