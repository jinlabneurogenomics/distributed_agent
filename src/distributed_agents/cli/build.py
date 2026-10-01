"""Corpus-authoring build subcommand."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ..build import (
    BUILD_REASONING_EFFORTS,
    BuildError,
    BuildRequest,
    DEFAULT_BUILD_MODEL,
    build_findings_report,
)


def add_parser(subcommands: argparse._SubParsersAction) -> None:
    parser = subcommands.add_parser(
        "build",
        help="Build one findings-centered source report for corpus construction.",
    )
    parser.add_argument("gene_target", help="Gene symbol, for example BDNF.")
    parser.add_argument(
        "--parquet-path",
        required=True,
        help="Path to the Perturb-seq parquet rendered into the canonical prompt.",
    )
    parser.add_argument(
        "--max-turns",
        type=int,
        default=50,
        help="Maximum Agents SDK turns before MaxTurnsExceeded (default 50).",
    )
    parser.add_argument(
        "--reasoning-effort",
        choices=BUILD_REASONING_EFFORTS,
        default="high",
    )
    parser.add_argument(
        "--out-dir",
        default="results/distributed_agents/build",
        help="Output root; build artifacts land in <out-dir>/<gene>/.",
    )
    parser.add_argument("--deliverable-path", default="")
    parser.add_argument("--model", default=DEFAULT_BUILD_MODEL)
    parser.add_argument("--skills-destination", default="")
    parser.add_argument("--skills-index-container-path", default="")
    parser.set_defaults(func=run)


def run(args: argparse.Namespace, _parser: argparse.ArgumentParser) -> int:
    out = Path(args.out_dir) / args.gene_target
    try:
        build_findings_report(
            BuildRequest(
                gene_target=args.gene_target,
                parquet_path=Path(args.parquet_path),
                out_dir=out,
                model=args.model,
                max_turns=args.max_turns,
                reasoning_effort=args.reasoning_effort,
                skills_destination=args.skills_destination,
                skills_index_container_path=args.skills_index_container_path,
                deliverable_path=(
                    Path(args.deliverable_path) if args.deliverable_path else None
                ),
            )
        )
    except (BuildError, FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {out}")
    return 0
