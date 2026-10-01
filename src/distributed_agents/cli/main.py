"""Top-level command parser and subcommand dispatch."""

from __future__ import annotations

import argparse

from .. import __version__
from . import build, chat, corpus, query


def build_parser() -> argparse.ArgumentParser:
    """Build the public DistributedAgents command parser."""

    parser = argparse.ArgumentParser(
        prog="distributed_agents",
        description="Evidence-grounded perturbation biology agents.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)
    build.add_parser(subcommands)
    query.add_parser(subcommands)
    chat.add_parser(subcommands)
    corpus.add_parser(subcommands)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args, parser)


if __name__ == "__main__":
    raise SystemExit(main())
