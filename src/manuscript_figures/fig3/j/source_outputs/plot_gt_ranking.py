#!/usr/bin/env python
"""Replot the depletion ground-truth ranking in the fig4/a log-rank style.

This is a single-panel diagnostic, so the standalone square panel is also the
plate.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedFormatter, FixedLocator, NullLocator


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
STYLE_PATH = ROOT / "src/figures/style.mplstyle"

FISHER_CSV = (
    ROOT
    / "debug/depletion/ground_truth/fisher/"
    "fisher_results_per_gene_predicted_group.csv"
)
CELL_TYPE = "151 TH Prkcd Grin2c Glut"
FISHER_BH_ALPHA = 0.05

GREY = "#6B7280"
OTHER = "#DADADA"
SIGNIFICANT = "#E69F00"


def load_ranking() -> pd.DataFrame:
    """Return all screened genes ranked by depletion odds ratio."""
    fisher = pd.read_csv(FISHER_CSV)
    ranking = fisher.loc[fisher["cell_type"].eq(CELL_TYPE)].copy()
    ranking["log2_or"] = np.log2(ranking["odds_ratio"].where(ranking["odds_ratio"] > 0))
    ranking = ranking.sort_values("log2_or", ascending=False, na_position="last").reset_index(drop=True)
    ranking["rank"] = np.arange(1, len(ranking) + 1)
    ranking["depletion_log2_or"] = ranking["log2_or"].clip(lower=0)
    ranking["significant"] = ranking["adj_p_value"].lt(FISHER_BH_ALPHA)
    return ranking


def set_plain_log_ticks(ax: plt.Axes) -> None:
    """Keep log ticks as editable plain text in the SVG export."""
    ticks = [1, 10, 100, 1000]
    ax.xaxis.set_major_locator(FixedLocator(ticks))
    ax.xaxis.set_minor_locator(NullLocator())
    ax.xaxis.set_major_formatter(FixedFormatter([str(tick) for tick in ticks]))


def plot_ranking(ranking: pd.DataFrame) -> plt.Figure:
    """Draw the compact log-rank depletion panel."""
    fig, ax = plt.subplots(figsize=(3.5, 3.5), layout="constrained")
    ax.axhline(0, color=GREY, ls="--", lw=0.6, zorder=1)

    other = ranking.loc[~ranking["significant"]]
    sig = ranking.loc[ranking["significant"]]
    ax.scatter(
        other["rank"],
        other["depletion_log2_or"],
        s=2.5,
        c=OTHER,
        lw=0,
        zorder=2,
        rasterized=True,
    )
    ax.scatter(
        sig["rank"],
        sig["depletion_log2_or"],
        s=8,
        c=SIGNIFICANT,
        lw=0,
        zorder=3,
    )

    ax.set_xscale("log")
    ax.set_xlim(1, len(ranking) * 1.05)
    set_plain_log_ticks(ax)

    ymax = ranking["depletion_log2_or"].max(skipna=True)
    ax.set_ylim(0, ymax * 1.30)
    ax.axvline(100, color=GREY, lw=0.5, ls=":", zorder=1)
    ax.text(
        100,
        ymax * 1.26,
        " rank cutoff defining top 100",
        fontsize=5.0,
        color=GREY,
        va="top",
        ha="left",
    )

    ax.set_xlabel(f"Depletion rank among screened genes (n={len(ranking)})")
    ax.set_ylabel("log₂ depletion odds ratio (minimum 0)", fontsize=6.2)
    ax.set_title("Held-out depletion ranking", fontsize=7.5)

    handles = [
        Line2D(
            [],
            [],
            marker="o",
            ls="",
            ms=3,
            mfc=SIGNIFICANT,
            mec="none",
            label=f"Fisher BH q < {FISHER_BH_ALPHA:g} (n={len(sig)})",
        ),
        Line2D(
            [],
            [],
            marker="o",
            ls="",
            ms=2.4,
            mfc=OTHER,
            mec="none",
            label=f"all other screened (n={len(other)})",
        ),
    ]
    ax.legend(
        handles=handles,
        loc="lower left",
        fontsize=5.2,
        handletextpad=0.2,
        labelspacing=0.22,
        borderpad=0.2,
    )
    return fig


def main() -> None:
    if STYLE_PATH.exists():
        plt.style.use(STYLE_PATH)

    ranking = load_ranking()
    ranking.loc[
        :,
        [
            "rank",
            "gene_target",
            "log2_or",
            "depletion_log2_or",
            "adj_p_value",
            "significant",
        ],
    ].to_csv(HERE / "gt_ranking_data.csv", index=False)

    fig = plot_ranking(ranking)
    stem = HERE / "gt_ranking_log"
    fig.savefig(stem.with_suffix(".svg"))
    fig.savefig(stem.with_suffix(".pdf"))
    fig.savefig(stem.with_suffix(".png"), dpi=300)
    plt.close(fig)

    n_significant = int(ranking["significant"].sum())
    print(f"Wrote {stem.name}.pdf/.png/.svg ({len(ranking)} genes; {n_significant} significant)")


if __name__ == "__main__":
    main()
