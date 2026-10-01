"""Resolve BioEval-owned filesystem locations."""

from __future__ import annotations

import os
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PACKAGE_ROOT.parents[1]


def runs_root() -> Path:
    """Return BioEval's writable run-artifact root."""

    return (
        Path(os.environ.get("BIOEVAL_RUN_ROOT", PACKAGE_ROOT / "runs"))
        .expanduser()
        .resolve()
    )


DEFAULT_RUNS_ROOT = runs_root()
