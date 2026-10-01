"""Release-local paths shared by legacy tooling and projection code."""

from pathlib import Path


RELEASE_ROOT = Path(__file__).resolve().parent
ARTIFACTS_ROOT = RELEASE_ROOT / "artifacts"
REPORTS_FILE = ARTIFACTS_ROOT / "reports" / "reports.jsonl"
LEDGERS_ROOT = ARTIFACTS_ROOT / "ledgers"
FINDINGS_LEDGER_FILE = LEDGERS_ROOT / "findings.csv"
EVIDENCE_LEDGER_FILE = LEDGERS_ROOT / "evidence.csv"
REFERENCES_LEDGER_FILE = LEDGERS_ROOT / "references.csv"
SKILLS_ROOT = RELEASE_ROOT / "skills"
BIOKG_ROOT = RELEASE_ROOT / "projections" / "biokg"
