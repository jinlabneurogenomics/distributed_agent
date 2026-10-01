"""Assemble the BioEval command-line interface."""

from __future__ import annotations

import argparse

from . import run, runs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="bioeval",
        description=(
            "Run reproducible DistributedAgents, Codex, Claude Code, and Biomni comparisons."
        ),
    )
    subcommands = parser.add_subparsers(dest="command", required=True)
    run.register(subcommands)
    runs.register(subcommands)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
