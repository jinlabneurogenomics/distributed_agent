#!/usr/bin/env python3
"""Materialize the compact row-level input used by the S5B KDE."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent
ROOT = next(path for path in HERE.parents if (path / "pyproject.toml").is_file())
ARCHIVE = ROOT / "manuscript" / "_archive_260924"
WORKBOOK = (
    ARCHIVE
    / "tables"
    / "legacy_preferred_union_findings_three_tiers_with_references.xlsx"
)
FOOTPRINT = ARCHIVE / "fig3" / "novelty_stats" / "target_footprint.csv"
OUTPUT = HERE / "current_flag_deg_footprints.csv"


def load_flag_style():
    path = ROOT / "src" / "figures" / "flag_style.py"
    spec = importlib.util.spec_from_file_location("s5_flag_style", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    flag_style = load_flag_style()
    findings = pd.read_excel(WORKBOOK, sheet_name="findings", engine="openpyxl")
    blank = findings["flag"].isna() | findings["flag"].astype(str).str.strip().eq("")
    rows = findings.loc[~blank, ["perturbation", "flag"]].copy()
    rows["flag_key"] = rows["flag"].map(flag_style.normalize_flag)

    footprint = pd.read_csv(FOOTPRINT).rename(columns={"target": "perturbation"})
    rows = rows.merge(
        footprint[["perturbation", "total_deg05"]],
        on="perturbation",
        how="left",
        validate="many_to_one",
    )
    if rows["total_deg05"].isna().any():
        missing = sorted(rows.loc[rows["total_deg05"].isna(), "perturbation"].unique())
        raise ValueError(f"Missing target DEG footprint for: {missing[:10]}")
    rows["total_deg05"] = rows["total_deg05"].astype(int)
    rows["log10_deg_plus_1"] = np.log10(rows["total_deg05"] + 1)
    rows[["perturbation", "flag_key", "total_deg05", "log10_deg_plus_1"]].to_csv(
        OUTPUT, index=False
    )
    if len(rows) != 5_125:
        raise ValueError(f"Expected 5,125 populated-flag rows; observed {len(rows):,}")
    print(f"wrote {len(rows):,} rows to {OUTPUT}")


if __name__ == "__main__":
    main()
