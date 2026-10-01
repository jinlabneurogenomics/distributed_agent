#!/usr/bin/env python3
"""Skill entry point for the release-owned offline BioKG query client."""

from __future__ import annotations

import sys
from pathlib import Path


PROJECTIONS_ROOT = Path(__file__).resolve().parents[3] / "projections"
if str(PROJECTIONS_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECTIONS_ROOT))

from biokg.tooling.query_biokg import main  # noqa: E402


if __name__ == "__main__":
    main()
