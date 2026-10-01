#!/usr/bin/env python3
"""Prepare the June source-access inputs used by the updated Figure 2C.

This is intentionally a thin aggregation over the canonical report-source
ledger.  It keeps the plotting script independent of the large event-level
trace export while preserving the three quantities needed for auditability:
distinct sources accessed, distinct sources cited, and raw citation entries.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
LEDGER = REPO / "data" / "derived" / "june_source_access_ledger.csv"
AUDIT_SUMMARY = REPO / "data" / "derived" / "june_source_access_summary.json"


def main() -> None:
    ledger = pd.read_csv(LEDGER)
    per_report = (
        ledger.groupby("report_gene", sort=True)
        .agg(
            accessed_sources=("accessed", "sum"),
            cited_sources=("cited", "sum"),
            citation_entries=("citation_entry_count", "sum"),
        )
        .reset_index()
    )
    for column in ("accessed_sources", "cited_sources", "citation_entries"):
        per_report[column] = per_report[column].astype(int)

    audit = json.loads(AUDIT_SUMMARY.read_text())
    expected = {
        "reports": 2046,
        "accessed_sources": int(audit["accessed_report_source_pairs"]),
        "cited_sources": int(audit["cited_report_source_pairs"]),
        "citation_entries": int(audit["citation_entries_raw"]),
    }
    observed = {
        "reports": len(per_report),
        "accessed_sources": int(per_report["accessed_sources"].sum()),
        "cited_sources": int(per_report["cited_sources"].sum()),
        "citation_entries": int(per_report["citation_entries"].sum()),
    }
    if observed != expected:
        raise RuntimeError(f"source-access aggregation drifted: {observed=} {expected=}")

    per_report.to_csv(HERE / "source_access_per_report.csv", index=False)
    (HERE / "source_access_summary.json").write_text(
        json.dumps(audit, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(observed, indent=2))


if __name__ == "__main__":
    main()
