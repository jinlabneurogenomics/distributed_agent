#!/usr/bin/env python3
"""Plot the current four-flag findings against DEG burden and target pathway.

This is the current-workbook counterpart of
``manuscript/fig2/_archive/c/build_flag_distributions.py``.  It emits the three
views from that analysis as individual panels and as one joint plate:

* conditional KDE of target DEG footprint for each literature flag;
* 100%-stacked flag composition by DEG-footprint bin;
* 100%-stacked flag composition by target pathway category.

Unit: one populated-flag row in the legacy-preferred union findings workbook.
Rows with a blank flag are counted in the summary and excluded from all three
panels.  DEG footprint and pathway category reuse the Fig. 3 target annotations
so this update remains directly comparable with the archived plot.

The two simple panels are square.  The pathway panel deliberately yields the
square default because its long categorical labels need a wider plotting area.

Run from any working directory:

    pixi run --locked python \
      manuscript/fig2/_debug/current_flag_distributions/build_current_flag_distributions.py
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/mplconfig_current_flag_distributions")
Path(os.environ["MPLCONFIGDIR"]).mkdir(parents=True, exist_ok=True)

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Patch
from scipy.stats import gaussian_kde

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]

import sys

sys.path.insert(0, str(ROOT / "src"))
from figures.flag_style import (  # noqa: E402
    FLAG_COLORS,
    FLAG_LABELS,
    FLAG_ORDER,
    normalize_flag,
)
from figures.panel_kit import audit, house_style, save, square  # noqa: E402


DEFAULT_WORKBOOK = (
    ROOT
    / "manuscript/tables/legacy_preferred_union_findings_three_tiers_with_references.xlsx"
)
FOOTPRINT_CSV = ROOT / "manuscript/fig3/novelty_stats/target_footprint.csv"
PATHWAY_CSV = ROOT / "manuscript/fig3/novelty_stats/target_pathway_category.csv"

DEG_BINS = ("0", "1–10", "11–50", "51–200", "200+")
PLOTTED_DEG_BINS = DEG_BINS[1:]
MIN_PATHWAY_N = 20
GAP = {"edgecolor": "white", "linewidth": 0.8}
INK = "#202020"
MUTED = "#66635f"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workbook", type=Path, default=DEFAULT_WORKBOOK)
    parser.add_argument("--outdir", type=Path, default=HERE)
    return parser.parse_args()


def deg_bin(value: int) -> str:
    if value == 0:
        return "0"
    if value <= 10:
        return "1–10"
    if value <= 50:
        return "11–50"
    if value <= 200:
        return "51–200"
    return "200+"


def load_data(workbook: Path) -> tuple[pd.DataFrame, dict[str, int]]:
    findings = pd.read_excel(workbook, sheet_name="findings", engine="openpyxl")
    required = {"perturbation", "flag"}
    missing = required - set(findings.columns)
    if missing:
        raise ValueError(f"findings sheet is missing columns: {sorted(missing)}")

    blank = findings["flag"].isna() | findings["flag"].astype(str).str.strip().eq("")
    rows = findings.loc[~blank].copy()
    rows["flag_key"] = rows["flag"].map(normalize_flag)

    footprint = pd.read_csv(FOOTPRINT_CSV).rename(columns={"target": "perturbation"})
    rows = rows.merge(
        footprint[["perturbation", "total_deg05"]],
        on="perturbation",
        how="left",
        validate="many_to_one",
    )
    if rows["total_deg05"].isna().any():
        targets = sorted(rows.loc[rows["total_deg05"].isna(), "perturbation"].unique())
        raise ValueError(f"missing DEG footprint for {len(targets)} targets: {targets[:10]}")
    rows["total_deg05"] = rows["total_deg05"].astype(int)
    rows["deg_bin"] = rows["total_deg05"].map(deg_bin)
    rows["log10_deg_plus_1"] = np.log10(rows["total_deg05"] + 1)

    pathway = pd.read_csv(PATHWAY_CSV).rename(columns={"gene": "perturbation"})
    rows = rows.merge(
        pathway[["perturbation", "category"]],
        on="perturbation",
        how="left",
        validate="many_to_one",
    )
    rows["category"] = rows["category"].fillna("Other")

    annotated = set(pathway["perturbation"])
    counts = {
        "workbook_rows": int(len(findings)),
        "plotted_rows": int(len(rows)),
        "blank_flag_rows": int(blank.sum()),
        "unique_targets": int(rows["perturbation"].nunique()),
        "targets_missing_pathway_annotation": int(
            len(set(rows["perturbation"]) - annotated)
        ),
    }
    return rows, counts


def composition_table(rows: pd.DataFrame, group: str, order: list[str]) -> pd.DataFrame:
    count = (
        rows.groupby([group, "flag_key"], observed=True)
        .size()
        .unstack(fill_value=0)
        .reindex(index=order, fill_value=0)
        .reindex(columns=FLAG_ORDER, fill_value=0)
    )
    out = pd.DataFrame({group: count.index, "n_findings": count.sum(axis=1).values})
    for flag in FLAG_ORDER:
        out[f"{flag}_count"] = count[flag].values
        out[f"{flag}_percent"] = np.divide(
            count[flag].values * 100,
            count.sum(axis=1).values,
            out=np.zeros(len(count), dtype=float),
            where=count.sum(axis=1).values != 0,
        ).round(1)
    return out


def legend(
    ax: plt.Axes,
    *,
    ncol: int = 2,
    location: str = "upper right",
    bbox_to_anchor: tuple[float, float] | None = None,
) -> None:
    handles = [
        Patch(facecolor=FLAG_COLORS[key], edgecolor="white", label=FLAG_LABELS[key])
        for key in FLAG_ORDER
    ]
    ax.legend(
        handles=handles,
        frameon=False,
        ncol=ncol,
        loc=location,
        bbox_to_anchor=bbox_to_anchor,
        handlelength=1.1,
        columnspacing=1.0,
    )


def draw_kde(ax: plt.Axes, rows: pd.DataFrame, *, tag: str = "") -> None:
    support_max = max(4.0, float(rows["log10_deg_plus_1"].max()))
    grid = np.linspace(0, support_max, 300)
    for flag in FLAG_ORDER:
        values = rows.loc[rows["flag_key"].eq(flag), "log10_deg_plus_1"].to_numpy()
        if len(values) < 2 or np.allclose(values, values[0]):
            continue
        # Reflection at zero prevents the density from leaking into impossible
        # negative DEG burdens.  Dividing by two is unnecessary because the
        # curve is interpreted conditionally within each flag and only x >= 0
        # is drawn, matching the archived implementation.
        reflected = np.concatenate([values, -values])
        density = 2.0 * gaussian_kde(reflected, bw_method=0.25)(grid)
        ax.fill_between(
            grid, 0, density, color=FLAG_COLORS[flag], alpha=0.06, linewidth=0
        )
        ax.plot(
            grid,
            density,
            color=FLAG_COLORS[flag],
            linewidth=1.8,
            label=f"{FLAG_LABELS[flag]} (n={len(values):,})",
        )
    # Zero is the physical support boundary.  Keep it on the axis; add a small
    # high-side pad so the finite evaluation grid does not collide with a spine.
    ax.set_xlim(0, support_max * 1.04)
    ax.set_ylim(bottom=0)
    ax.set_xlabel("Target DEG footprint, log₁₀(total DEG at FDR < 0.05 + 1)")
    ax.set_ylabel("Density within flag")
    ax.set_title(f"{tag}DEG footprint by literature flag", loc="left")
    ax.legend(frameon=False, ncol=1, loc="upper right", handlelength=1.4)
    square(ax)


def draw_deg_bins(ax: plt.Axes, rows: pd.DataFrame, *, tag: str = "") -> None:
    # The zero-DEG stratum remains in the source table but is intentionally
    # omitted from this panel so the plotted comparison is among nonzero bins.
    table = composition_table(rows, "deg_bin", list(PLOTTED_DEG_BINS))
    present = table.loc[table["n_findings"].gt(0)].reset_index(drop=True)
    x = np.arange(len(present))
    bottom = np.zeros(len(present), dtype=float)
    for flag in FLAG_ORDER:
        values = present[f"{flag}_percent"].to_numpy()
        ax.bar(x, values, bottom=bottom, color=FLAG_COLORS[flag], width=0.82, **GAP)
        for xpos, low, width in zip(x, bottom, values):
            if width >= 8:
                ax.text(
                    xpos,
                    low + width / 2,
                    f"{width:.0f}%",
                    ha="center",
                    va="center",
                    fontsize=6.2,
                    color="white" if flag == "disagree" else INK,
                )
        bottom += values

    labels = [
        f"{row.deg_bin}\n(n={int(row.n_findings):,})" for row in present.itertuples()
    ]
    ax.set_xticks(x, labels)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Findings (%)")
    ax.set_xlabel("Target DEG footprint bin (FDR < 0.05)")
    ax.set_title(f"{tag}Flag composition by DEG bin", loc="left", pad=28)
    legend(
        ax,
        ncol=2,
        location="lower left",
        bbox_to_anchor=(0.0, 1.005),
    )
    square(ax)


def pathway_order(rows: pd.DataFrame) -> list[str]:
    counts = rows.groupby("category", observed=True).size()
    keep = counts[counts.ge(MIN_PATHWAY_N)].index
    subset = rows.loc[rows["category"].isin(keep)]
    disagree = subset.groupby("category", observed=True)["flag_key"].apply(
        lambda values: 100 * values.eq("disagree").mean()
    )
    # barh draws the last row at the top, so ascending order puts the largest
    # Disagree share at the visual top.
    return disagree.sort_values(kind="stable").index.tolist()


def draw_pathway(ax: plt.Axes, rows: pd.DataFrame, *, tag: str = "") -> None:
    order = pathway_order(rows)
    table = composition_table(rows, "category", order)
    y = np.arange(len(table))
    left = np.zeros(len(table), dtype=float)
    for flag in FLAG_ORDER:
        values = table[f"{flag}_percent"].to_numpy()
        ax.barh(y, values, left=left, color=FLAG_COLORS[flag], height=0.78, **GAP)
        left += values

    labels = [
        value.replace("/", "/\n") if len(value) > 30 else value
        for value in table["category"]
    ]
    ax.set_yticks(y, labels)
    for ypos, row in enumerate(table.itertuples()):
        ax.text(
            101.5,
            ypos,
            f"n={int(row.n_findings):,}  ({row.disagree_percent:.1f}% disagree)",
            ha="left",
            va="center",
            fontsize=6.2,
            color=MUTED,
        )
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.6, len(table) - 0.4)
    ax.set_xlabel("Findings (%)")
    ax.set_title(
        f"{tag}Flag composition by target pathway category", loc="left", pad=24
    )
    ax.tick_params(axis="y", length=0)
    legend(
        ax,
        ncol=4,
        location="lower left",
        bbox_to_anchor=(0.0, 1.005),
    )
    # Intentionally not square: the long category labels are the data's aspect.


def save_and_close(fig: plt.Figure, stem: Path, *, run_audit: bool = True) -> None:
    if run_audit:
        audit(fig, reserved=FLAG_COLORS)
    save(fig, stem, dpi=300)
    plt.close(fig)


def write_tables(
    rows: pd.DataFrame, counts: dict[str, int], outdir: Path, workbook: Path
) -> None:
    flag_counts = (
        rows["flag_key"]
        .value_counts()
        .reindex(FLAG_ORDER, fill_value=0)
        .rename_axis("flag_key")
        .reset_index(name="n_findings")
    )
    flag_counts["flag"] = flag_counts["flag_key"].map(FLAG_LABELS)
    flag_counts["percent"] = (100 * flag_counts["n_findings"] / len(rows)).round(1)
    flag_counts[["flag_key", "flag", "n_findings", "percent"]].to_csv(
        outdir / "current_flag_counts.csv", index=False
    )

    deg = composition_table(rows, "deg_bin", list(DEG_BINS))
    deg.to_csv(outdir / "current_flag_composition_by_deg_bin.csv", index=False)

    category_counts = rows.groupby("category", observed=True).size().sort_values(ascending=False)
    pathway = composition_table(rows, "category", category_counts.index.tolist())
    pathway["plotted"] = pathway["n_findings"].ge(MIN_PATHWAY_N)
    pathway.to_csv(outdir / "current_flag_composition_by_pathway.csv", index=False)

    summary = {
        **counts,
        "input_workbook": (
            str(workbook.relative_to(ROOT))
            if workbook.is_relative_to(ROOT)
            else str(workbook)
        ),
        "deg_footprint_definition": "per-target total DE genes at FDR < 0.05",
        "plot_unit": "finding row with a populated flag",
        "pathway_minimum_n": MIN_PATHWAY_N,
        "flag_counts": {
            FLAG_LABELS[row.flag_key]: int(row.n_findings)
            for row in flag_counts.itertuples()
        },
        "outputs": [
            "fig_current_flag_distributions__a_deg_kde.{png,svg}",
            "fig_current_flag_distributions__b_deg_bins.{png,svg}",
            "fig_current_flag_distributions__c_pathway.{png,svg}",
            "fig_current_flag_distributions.{png,svg}",
        ],
    }
    (outdir / "current_flag_distributions_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )


def main() -> None:
    args = parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    house_style()
    rows, counts = load_data(args.workbook.resolve())
    write_tables(rows, counts, args.outdir, args.workbook.resolve())

    fig, ax = plt.subplots(figsize=(4.2, 4.2))
    draw_kde(ax, rows)
    fig.tight_layout()
    save_and_close(fig, args.outdir / "fig_current_flag_distributions__a_deg_kde")

    fig, ax = plt.subplots(figsize=(4.2, 4.2))
    draw_deg_bins(ax, rows)
    fig.tight_layout()
    save_and_close(fig, args.outdir / "fig_current_flag_distributions__b_deg_bins")

    fig, ax = plt.subplots(figsize=(6.2, 4.8))
    draw_pathway(ax, rows)
    fig.subplots_adjust(left=0.28, right=0.79, top=0.92, bottom=0.13)
    # The pathway panel's non-square aspect is an explicit categorical-axis yield.
    save_and_close(
        fig,
        args.outdir / "fig_current_flag_distributions__c_pathway",
        run_audit=False,
    )

    fig = plt.figure(figsize=(11.0, 6.2))
    grid = GridSpec(
        2,
        2,
        figure=fig,
        width_ratios=(1.0, 1.05),
        hspace=0.56,
        wspace=0.38,
        left=0.07,
        right=0.985,
        top=0.87,
        bottom=0.10,
    )
    draw_kde(fig.add_subplot(grid[0, 0]), rows, tag="A  ")
    draw_deg_bins(fig.add_subplot(grid[1, 0]), rows, tag="B  ")
    draw_pathway(fig.add_subplot(grid[:, 1]), rows, tag="C  ")
    fig.suptitle(
        f"Current literature flags by target DEG footprint and pathway "
        f"(n={len(rows):,} findings)",
        fontsize=10,
        y=0.985,
    )
    # A joint plate has a layout aspect by definition; individual A/B panels
    # above carry the square-panel audit.
    save_and_close(
        fig, args.outdir / "fig_current_flag_distributions", run_audit=False
    )

    counts_by_flag = rows["flag_key"].value_counts().reindex(FLAG_ORDER, fill_value=0)
    print(
        f"workbook_rows={counts['workbook_rows']:,}  plotted_flags={len(rows):,}  "
        f"blank_flags={counts['blank_flag_rows']:,}  targets={counts['unique_targets']:,}"
    )
    for flag in FLAG_ORDER:
        print(f"  {FLAG_LABELS[flag]:<14} {counts_by_flag[flag]:>5,}")
    print(f"wrote panels, joint plate, tables, and summary to {args.outdir}")


if __name__ == "__main__":
    main()
