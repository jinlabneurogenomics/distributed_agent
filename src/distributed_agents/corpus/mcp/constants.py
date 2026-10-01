"""Shared corpus MCP protocol and service constants."""

import re


SERVER_NAME = "distributed_agents_corpus"
SERVER_VERSION = "0.7.0"
PROTOCOL_VERSION = "2025-06-18"
MAX_ROWS = 50
MAX_OUTPUT_BYTES = 32_000
TOOL_TIMEOUT_SECONDS = 45

CALIBRATION_CAPABILITY = "corpus.calibration"
FINDINGS_CAPABILITY = "corpus.findings"
EVIDENCE_CAPABILITY = "corpus.report_evidence"
GRAPH_CAPABILITY = "corpus.graph"
TARGET_ANALOG_CAPABILITY = "corpus.target_analogs"

CLAIM_GRAPH_ARTIFACTS = frozenset(
    {"claims", "claim_contributions", "finding_claim_dispositions", "findings"}
)
CLAIM_ROLES = ("ANCHORS", "SUPPORTS", "QUALIFIES", "CONTRASTS")
FINDINGS_BM25_ARTIFACT = "findings_bm25"
FINDINGS_BM25_ROLE = "lexical_retrieval"

SHI_HOLDOUT_TOPICS = (
    "summary",
    "counts",
    "claims",
    "relations",
    "candidate-pools",
    "finding-confidence-by-type",
    "literature-direction-by-type",
    "semantic-assertions",
    "sources",
)
LEGACY_TOPICS = (
    "summary",
    "counts",
    "de-support",
    "compression",
    "routing",
    "sparsity",
    "semantic-assertions",
    "finding-confidence-by-type",
    "claim-confidence-by-support",
    "claim-confidence-by-de-support",
    "sources",
)
LEGACY_FINDINGS_TOPICS = (
    "summary",
    "counts",
    "claim-layer",
    "semantic-assertions",
    "finding-confidence-by-type",
    "sources",
)
SHI_TOPICS = (
    "summary",
    "counts",
    "claim-layer",
    "claims",
    "relations",
    "semantic-assertions",
    "finding-confidence-by-type",
    "sources",
)
QUERY_LEDGER_NAMES = (
    "findings",
    "null_findings",
    "pathways",
    "cell_types",
)
SAFE_FIELD = re.compile(r"^[A-Za-z][A-Za-z0-9_]{0,63}$")
SEARCH_TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*")
