"""Launch a module from a selected release projection.

Used by Pixi tasks so `DISTRIBUTED_AGENTS_CORPUS_RELEASE` selects both immutable data and
the matching implementation instead of baking one release's Python path into
the task definition.
"""

from __future__ import annotations

import argparse
import runpy
import sys

from .registry import CorpusRegistryError, get_release


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m distributed_agents.corpus.launch")
    parser.add_argument("module", help="Projection module, for example biokg.host")
    arguments = list(sys.argv[1:] if argv is None else argv)
    if not arguments or arguments[0] in {"-h", "--help"}:
        parser.print_help()
        return 0
    # Parse only the projection module. Every later argument, including
    # ``--help``, belongs to the selected release's module.
    args = parser.parse_args(arguments[:1])
    remainder = arguments[1:]
    projection, _, suffix = args.module.partition(".")
    if projection != "biokg":
        parser.error("only the selected release's biokg projection is supported")
    try:
        projection_root = get_release().projection(projection)
    except CorpusRegistryError as exc:
        parser.error(str(exc))
    projections_root = projection_root.parent
    sys.path.insert(0, str(projections_root))
    replacements = {
        "@BIOKG_ROOT@": str(projection_root),
        "@BIOKG_BASE@": str(projection_root / "data" / "base"),
    }
    resolved_args = [replacements.get(value, value) for value in remainder]
    sys.argv = [args.module, *resolved_args]
    runpy.run_module(
        projection if not suffix else f"{projection}.{suffix}",
        run_name="__main__",
        alter_sys=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
