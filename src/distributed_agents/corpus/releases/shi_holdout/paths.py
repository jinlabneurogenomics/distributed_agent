"""Stable paths inside the Shi holdout corpus capsule."""

from pathlib import Path


RELEASE_ROOT = Path(__file__).resolve().parent
ARTIFACTS_ROOT = RELEASE_ROOT / "artifacts"
REPORTS_FILE = ARTIFACTS_ROOT / "reports" / "reports.jsonl"
LEDGERS_ROOT = ARTIFACTS_ROOT / "ledgers"
AUDITS_ROOT = ARTIFACTS_ROOT / "audits"
SKILLS_ROOT = RELEASE_ROOT / "skills"
TOOLING_ROOT = RELEASE_ROOT / "tooling"
BIOKG_ROOT = RELEASE_ROOT / "projections" / "biokg"
BIOKG_DATA_ROOT = BIOKG_ROOT / "data" / "base"
