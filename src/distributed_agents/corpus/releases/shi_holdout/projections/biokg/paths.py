"""Stable filesystem locations for the Shi holdout BioKG projection."""

from __future__ import annotations

import os
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parent
RELEASE_ROOT = PACKAGE_ROOT.parents[1]
DATA_ROOT = PACKAGE_ROOT / "data"
REPORTS_FILE = RELEASE_ROOT / "artifacts" / "reports" / "reports.jsonl"
FINDINGS_LEDGER_FILE = RELEASE_ROOT / "artifacts" / "ledgers" / "findings.jsonl"
EVIDENCE_LEDGER_FILE = RELEASE_ROOT / "artifacts" / "ledgers" / "evidence.jsonl"
REFERENCES_LEDGER_FILE = RELEASE_ROOT / "artifacts" / "ledgers" / "references.jsonl"
BASE_DATA_DIR = DATA_ROOT / "base"
NODES_FILE = BASE_DATA_DIR / "nodes.jsonl"
NODE_BUILD_FILE = BASE_DATA_DIR / "node_build.json"
RELATIONSHIPS_FILE = BASE_DATA_DIR / "relationships.jsonl"
RELATIONSHIP_BUILD_FILE = BASE_DATA_DIR / "relationship_build.json"


def _work_root() -> Path:
    configured = os.environ.get("BIOKG_WORK_ROOT")
    if configured:
        return Path(configured).expanduser().resolve()
    return PACKAGE_ROOT / "_work"


WORK_ROOT = _work_root()
