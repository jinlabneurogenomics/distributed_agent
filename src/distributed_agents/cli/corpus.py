"""Corpus registry subcommand."""

from __future__ import annotations

import argparse
import sys

from ..corpus.cli import add_subcommands, run_from_namespace
from ..corpus.registry import CorpusRegistryError


def add_parser(subcommands: argparse._SubParsersAction) -> None:
    parser = subcommands.add_parser(
        "corpus",
        help="Discover, inspect, and validate installed corpus releases.",
    )
    add_subcommands(parser)
    parser.set_defaults(func=run)


def run(args: argparse.Namespace, _parser: argparse.ArgumentParser) -> int:
    try:
        return run_from_namespace(args)
    except CorpusRegistryError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
