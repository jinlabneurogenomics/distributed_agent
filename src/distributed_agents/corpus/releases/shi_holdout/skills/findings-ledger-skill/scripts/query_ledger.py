#!/usr/bin/env python3
from pathlib import Path
import runpy
import sys

tooling = Path(__file__).resolve().parents[3] / "tooling"
sys.path.insert(0, str(tooling))
runpy.run_path(str(tooling / "query_ledger.py"), run_name="__main__")
