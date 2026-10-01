"""Canonical filesystem locations for the Shi BioKG projection.

This module is deliberately side-effect free: importing it resolves names but
does not create directories, download assets, or modify build/runtime state.
"""

from __future__ import annotations

import os
from pathlib import Path


PROJECTION_ROOT = Path(__file__).resolve().parent
RELEASE_ROOT = PROJECTION_ROOT.parents[1]
DATA_ROOT = PROJECTION_ROOT / "data"
DOCS_ROOT = PROJECTION_ROOT / "docs"
HOST_ROOT = PROJECTION_ROOT / "host"
HOST_PLUGIN_DIR = HOST_ROOT / "plugins"
HOST_OFFLINE_CONFIG = HOST_ROOT / "neo4j_offline.conf"
REPORTS_FILE = RELEASE_ROOT / "artifacts" / "reports" / "reports.jsonl"
FINDINGS_LEDGER_FILE = RELEASE_ROOT / "artifacts" / "ledgers" / "findings.csv"
EVIDENCE_LEDGER_FILE = RELEASE_ROOT / "artifacts" / "ledgers" / "evidence.csv"
REFERENCES_LEDGER_FILE = RELEASE_ROOT / "artifacts" / "ledgers" / "references.csv"


def _work_root() -> Path:
    configured = os.environ.get("BIOKG_WORK_ROOT")
    if configured:
        return Path(configured).expanduser().resolve()
    return PROJECTION_ROOT / "_work"


WORK_ROOT = _work_root()

BASE_DATA_DIR = DATA_ROOT / "base"
CLAIM_DATA_DIR = DATA_ROOT / "claims"
GRAPH_DATA_DIR = DATA_ROOT / "graph"
NORMALIZATION_DATA_DIR = DATA_ROOT / "normalization"
NORMALIZATION_FILE = NORMALIZATION_DATA_DIR / "normalization.tsv"
MEASURED_UNIVERSE_FILE = NORMALIZATION_DATA_DIR / "measured_universe.txt"
NEO4J_DUMP_FILE = GRAPH_DATA_DIR / "neo4j.dump"
NEO4J_DUMP_MANIFEST_FILE = GRAPH_DATA_DIR / "manifest.json"

BUILD_WORK_DIR = WORK_ROOT / "build"
GRAPH_WORK_DIR = BUILD_WORK_DIR / "graph"
CLAIM_WORK_DIR = BUILD_WORK_DIR / "claims"
NORMALIZATION_WORK_DIR = BUILD_WORK_DIR / "normalization"
VISUALIZE_WORK_DIR = WORK_ROOT / "visualize"

NEO4J_WORK_DIR = WORK_ROOT / "neo4j"
NEO4J_DATA_DIR = NEO4J_WORK_DIR / "data"
NEO4J_IMAGE_DIR = NEO4J_WORK_DIR / "image"
NEO4J_IMAGE_FILE = NEO4J_IMAGE_DIR / "neo4j_5_community.sif"
NEO4J_LOG_DIR = NEO4J_WORK_DIR / "logs"
