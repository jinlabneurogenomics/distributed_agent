#!/usr/bin/env python3
"""Compatibility entrypoint for the packaged corpus MCP service."""

from __future__ import annotations

import sys
from pathlib import Path

if __package__:
    from .mcp.application import main
else:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from distributed_agents.corpus.mcp.application import main


if __name__ == "__main__":
    raise SystemExit(main())
