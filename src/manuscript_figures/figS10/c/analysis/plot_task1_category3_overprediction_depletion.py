#!/usr/bin/env python3
"""Characterize Task-1 category-3 overpredictions and cell-depletion ranks.

The strict category-3 set is observed zero / BioAgents predicted response after
the established Nup93 figure-only override.  The figure shows the six largest
category-3 calls.  Pomp is added as an explicitly marked near-null reference
because it has 4 observed versus 600 predicted DEGs and was requested alongside
Thoc2 and Pafah1b1; it is not silently relabeled as category 3.

Panel a shows observed and predicted DEG counts.  Panel b shows general
qualifying functional/physical/literature STRING training neighbors without
using response matching to select the displayed partner.  Responding neighbors
are listed first, so (for example) Thoc2 shows both Thoc1 (303 DEGs) and Ddx39b
(0 DEGs).  Panel c shows the orthogonal cell-depletion rank in the same focal
population; rank 1 is strongest depletion by Fisher odds ratio.  Cell depletion
is differential recovery, not target-transcript knockdown.

All panels use square plotting boxes and are exported both separately and as a
joint plate.  The STRING grid is drawn with vector rectangles so the SVG stays
fully editable.
"""

from __future__ import annotations

import math
import os
import sys
from pathlib import Path
from typing import Callable

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/bioagents-mpl")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "src"))

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch, Rectangle  # noqa: E402
from figures.panel_kit import house_style, plate, square  # noqa: E402


TASK1_CSV = (
    HERE / "one_target_characterization_v1_20260909" / "task1_per_target.csv"
)
STRING_BUCKET_CSV = (
    HERE
    / "task1_string_partner_buckets_v1_20260919"
    / "per_target_buckets.csv"
)
FUNCTIONAL_EDGES_CSV = (
    HERE
    / "task1_string_partner_buckets_v1_20260919"
    / "functional_string_edges.csv"
)
PHYSICAL_EDGES_CSV = HERE / "task2_physical_transfer_pairs.csv"
TRAINING_COUNTS_CSV = (
    HERE
    / "holdout_task"
    / "Inputs"
    / "151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv"
)
DEPLETION_CSV = (
    ROOT
    / "debug"
    / "depletion"
    / "ground_truth"
    / "fisher"
    / "fisher_results_per_gene_predicted_group.csv"
)
DEPLETION_TOP150_CSV = (
    ROOT
    / "debug"
    / "depletion"
    / "ground_truth"
    / "fisher"
    / "top150_depletion_151_TH_Prkcd_Grin2c_Glut_predicted_group.csv"
)
OUTPUT_DIR = HERE / "task1_category3_general_string_depletion_v2_20260919"
OUTPUT_STEM = "fig_task1_category3_general_string_depletion"

CELL_TYPE = "151 TH Prkcd Grin2c Glut"
POMP_REFERENCE = "Pomp"
NUP93_OVERRIDE = 0
NUP93_ORIGINAL_PREDICTION = 620
NETWORK_ORDER = ("functional", "physical", "literature")
NETWORK_LABELS = {
    "functional": "Functional",
    "physical": "Physical",
    "literature": "Literature",
}
NON_TEXT_EVIDENCE_COLUMNS = (
    "nscore",
    "fscore",
    "pscore",
    "ascore",
    "escore",
    "dscore",
)
STRING_STATUS_ORDER = ("none", "zero_only", "responding")
STRING_STATUS_COLORS = {
    "none": "#D9DEE5",
    "zero_only": "#C8DEDA",
    "responding": "#D9822B",
}
STRING_STATUS_LABELS = {
    "none": "No qualifying neighbor",
    "zero_only": "Only zero-response neighbor(s)",
    "responding": "At least one responding neighbor",
}
OBSERVED_COLOR = "#59636F"
PREDICTED_COLOR = "#D94841"
LINK_COLOR = "#C7CDD6"
DEPLETION_COLOR = "#6B5A8E"
TOP100_BAND = "#EEEAF4"
POMP_SEPARATOR = "#9CA3AF"


def format_count(value: float | int) -> str:
    return f"{int(value):,}"


def load_general_string_neighbors(targets: list[str]) -> pd.DataFrame:
    training = pd.read_csv(TRAINING_COUNTS_CSV).rename(
        columns={"target_name": "q", "n_degs": "partner_n_degs"}
    )
    functional = pd.read_csv(FUNCTIONAL_EDGES_CSV)
    physical = pd.read_csv(PHYSICAL_EDGES_CSV)

    functional_primary = functional[
        functional["string_score"].ge(0.90)
        & functional[list(NON_TEXT_EVIDENCE_COLUMNS)].max(axis=1).ge(0.40)
    ].copy()
    functional_primary["network"] = "functional"
    functional_primary["network_score"] = functional_primary["string_score"]

    physical_primary = physical[physical["string_score"].ge(0.90)].copy()
    physical_primary["network"] = "physical"
    physical_primary["network_score"] = physical_primary["string_score"]

    literature_primary = functional[functional["tscore"].ge(0.90)].copy()
    literature_primary["network"] = "literature"
    literature_primary["network_score"] = literature_primary["tscore"]

    columns = ["p", "q", "network", "network_score"]
    neighbors = pd.concat(
        [
            functional_primary[columns],
            physical_primary[columns],
            literature_primary[columns],
        ],
        ignore_index=True,
    )
    neighbors = neighbors[neighbors["p"].isin(targets)].merge(
        training, on="q", how="left", validate="many_to_one"
    )
    if neighbors["partner_n_degs"].isna().any():
        raise ValueError("A qualifying STRING neighbor is absent from training counts")
    neighbors["partner_n_degs"] = neighbors["partner_n_degs"].astype(int)
    neighbors["partner_responds"] = neighbors["partner_n_degs"].gt(0)
    neighbors = neighbors.sort_values(
        ["p", "network", "partner_responds", "network_score", "q"],
        ascending=[True, True, False, False, True],
        kind="stable",
    ).reset_index(drop=True)

    # The earlier A/B/C table still provides an independent count of qualifying
    # neighbors.  Validate against it while deliberately ignoring its
    # response-matched partner selection.
    bucket_summary = pd.read_csv(STRING_BUCKET_CSV)
    bucket_summary = bucket_summary[
        bucket_summary["response_definition"].eq("same_seven_level_bin")
        & bucket_summary["p"].isin(targets)
        & bucket_summary["network"].isin(NETWORK_ORDER)
    ]
    observed_counts = neighbors.groupby(["p", "network"]).size().to_dict()
    for row in bucket_summary.itertuples(index=False):
        observed = int(observed_counts.get((row.p, row.network), 0))
        if observed != int(row.qualifying_partner_n):
            raise ValueError(
                f"General STRING neighbor count mismatch for {row.p}/{row.network}: "
                f"{observed} versus {row.qualifying_partner_n}"
            )
    return neighbors


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    task1 = pd.read_csv(TASK1_CSV)
    nup93 = task1[task1["target_name"].eq("Nup93")]
    if len(nup93) != 1 or int(nup93.iloc[0]["bioagents_predicted_n_degs"]) != NUP93_ORIGINAL_PREDICTION:
        raise ValueError("Nup93 source prediction no longer matches the figure override")
    task1.loc[task1["target_name"].eq("Nup93"), "bioagents_predicted_n_degs"] = NUP93_OVERRIDE

    category3 = task1[
        task1["actual_n_degs"].eq(0)
        & task1["bioagents_predicted_n_degs"].gt(0)
    ].copy()
    category3 = category3.sort_values(
        ["bioagents_predicted_n_degs", "target_name"],
        ascending=[False, True],
    ).reset_index(drop=True)
    if len(category3) != 30:
        raise ValueError(f"Expected 30 strict category-3 targets, found {len(category3)}")
    top6 = category3.head(6).copy()

    pomp = task1[task1["target_name"].eq(POMP_REFERENCE)].copy()
    if len(pomp) != 1 or int(pomp.iloc[0]["actual_n_degs"]) != 4:
        raise ValueError("Expected Pomp to be the 4-observed near-null reference")
    featured = pd.concat([pomp, top6], ignore_index=True)
    featured["role"] = ["near-null reference"] + ["strict category 3"] * len(top6)
    featured["display_name"] = featured["target_name"]
    featured.loc[
        featured["target_name"].eq(POMP_REFERENCE), "display_name"
    ] = "Pomp (obs. 4)"

    string = load_general_string_neighbors(featured["target_name"].tolist())

    depletion = pd.read_csv(DEPLETION_CSV)
    depletion = depletion[depletion["cell_type"].eq(CELL_TYPE)].copy()
    depletion = depletion.sort_values("odds_ratio", ascending=False).reset_index(drop=True)
    depletion["depletion_rank"] = np.arange(1, len(depletion) + 1)
    depletion["log2_depletion_odds_ratio"] = depletion["odds_ratio"].map(
        lambda value: math.log2(value) if value > 0 else np.nan
    )
    if len(depletion) != 1948:
        raise ValueError(f"Expected 1,948 depletion-ranked targets, found {len(depletion)}")

    # Confirm that the reconstructed full ranking agrees with the frozen top-150
    # truth file wherever the featured genes are represented there.
    frozen = pd.read_csv(DEPLETION_TOP150_CSV)[
        ["gene_target", "depletion_rank", "odds_ratio"]
    ]
    check = frozen.merge(
        depletion[["gene_target", "odds_ratio"]],
        on="gene_target",
        suffixes=("_frozen", "_full"),
        validate="one_to_one",
    )
    if len(check) != 150 or not np.allclose(
        check["odds_ratio_frozen"], check["odds_ratio_full"], rtol=0, atol=1e-12
    ):
        raise ValueError("Reconstructed depletion values do not match the frozen top 150")
    # Four top-150 genes form two exact-OR ties.  Use the frozen order within
    # those ties so reported benchmark ranks are reproduced exactly.
    frozen_rank = frozen.set_index("gene_target")["depletion_rank"]
    depletion["depletion_rank"] = depletion["gene_target"].map(frozen_rank).fillna(
        depletion["depletion_rank"]
    ).astype(int)
    if depletion["depletion_rank"].duplicated().any():
        raise ValueError("Frozen tie resolution produced duplicate depletion ranks")

    depletion_fields = [
        "gene_target",
        "depletion_rank",
        "odds_ratio",
        "log2_depletion_odds_ratio",
        "p_value",
        "adj_p_value",
        "observed_pert_in_T (b)",
        "expected_pert_in_T (a)",
    ]
    featured = featured.merge(
        depletion[depletion_fields],
        left_on="target_name",
        right_on="gene_target",
        how="left",
        validate="one_to_one",
    )
    category3_depletion = category3.merge(
        depletion[depletion_fields],
        left_on="target_name",
        right_on="gene_target",
        how="left",
        validate="one_to_one",
    )
    if featured["depletion_rank"].isna().any() or category3_depletion["depletion_rank"].isna().any():
        raise ValueError("Every featured/category-3 target should have a depletion rank")
    return featured, string, category3_depletion, depletion


def style_rows(ax: plt.Axes, featured: pd.DataFrame) -> None:
    y = np.arange(len(featured))
    ax.set_yticks(y, featured["display_name"])
    ax.set_ylim(len(featured) - 0.5, -0.5)
    ax.axhline(0.5, color=POMP_SEPARATOR, linewidth=0.8, linestyle="--", zorder=5)


def draw_overprediction(ax: plt.Axes, featured: pd.DataFrame) -> None:
    y = np.arange(len(featured))
    actual = featured["actual_n_degs"].to_numpy(dtype=float)
    predicted = featured["bioagents_predicted_n_degs"].to_numpy(dtype=float)
    actual_x = np.log1p(actual)
    predicted_x = np.log1p(predicted)

    ax.hlines(y, actual_x, predicted_x, color=LINK_COLOR, linewidth=3.2, zorder=1)
    ax.scatter(
        actual_x,
        y,
        s=29,
        color=OBSERVED_COLOR,
        edgecolor="white",
        linewidth=0.5,
        zorder=3,
    )
    ax.scatter(
        predicted_x,
        y,
        s=31,
        color=PREDICTED_COLOR,
        edgecolor="white",
        linewidth=0.5,
        zorder=4,
    )
    for xpos, ypos, value in zip(predicted_x, y, predicted):
        ax.annotate(
            format_count(value),
            (xpos, ypos),
            xytext=(4, 0),
            textcoords="offset points",
            va="center",
            fontsize=6.3,
            color=PREDICTED_COLOR,
        )

    ticks = np.log1p(np.array([0, 1, 10, 100, 1000], dtype=float))
    ax.set_xticks(ticks, ["0", "1", "10", "100", "1,000"])
    ax.set_xlim(-0.28, max(predicted_x) + 0.75)
    style_rows(ax, featured)
    ax.set_xlabel("DEG count (log1p scale)")
    ax.set_title("a  Overprediction severity", loc="left")
    ax.grid(axis="x")
    ax.legend(
        handles=[
            Line2D(
                [], [], marker="o", linestyle="none", markersize=5,
                color=OBSERVED_COLOR, label="Observed",
            ),
            Line2D(
                [], [], marker="o", linestyle="none", markersize=5,
                color=PREDICTED_COLOR, label="BioAgents",
            ),
        ],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.18),
        frameon=False,
        fontsize=6.3,
        ncol=2,
        columnspacing=0.8,
        handletextpad=0.3,
    )
    square(ax)


def draw_string_matrix(
    ax: plt.Axes, featured: pd.DataFrame, string: pd.DataFrame
) -> None:
    targets = featured["target_name"].tolist()
    for row, target in enumerate(targets):
        for col, network in enumerate(NETWORK_ORDER):
            neighbors = string[
                string["p"].eq(target) & string["network"].eq(network)
            ]
            if neighbors.empty:
                status = "none"
            elif neighbors["partner_responds"].any():
                status = "responding"
            else:
                status = "zero_only"
            ax.add_patch(
                Rectangle(
                    (col - 0.5, row - 0.5),
                    1,
                    1,
                    facecolor=STRING_STATUS_COLORS[status],
                    edgecolor="white",
                    linewidth=1.5,
                )
            )
            if status == "none":
                text = "none"
                text_color = "#44505F"
            else:
                shown = neighbors.head(2)
                lines = [
                    f"{record.q} · {format_count(record.partner_n_degs)}"
                    for record in shown.itertuples(index=False)
                ]
                remaining = len(neighbors) - len(shown)
                if remaining:
                    lines.append(f"+{remaining} more")
                text = "\n".join(lines)
                text_color = "white" if status == "responding" else "#35514D"
            ax.text(
                col,
                row,
                text,
                ha="center",
                va="center",
                fontsize=5.4,
                color=text_color,
                linespacing=1.10,
            )

    ax.set_xticks(np.arange(len(NETWORK_ORDER)), [NETWORK_LABELS[n] for n in NETWORK_ORDER])
    ax.tick_params(axis="x", top=True, labeltop=True, bottom=False, labelbottom=False)
    style_rows(ax, featured)
    ax.set_xlim(-0.5, len(NETWORK_ORDER) - 0.5)
    ax.set_title("b  General STRING neighbors", loc="left", pad=22)
    ax.legend(
        handles=[
            Patch(
                facecolor=STRING_STATUS_COLORS[status],
                edgecolor="none",
                label=STRING_STATUS_LABELS[status],
            )
            for status in STRING_STATUS_ORDER
        ],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.10),
        frameon=False,
        fontsize=5.7,
        ncol=1,
        handlelength=0.9,
        handletextpad=0.4,
        labelspacing=0.25,
    )
    square(ax)


def draw_depletion_rank(ax: plt.Axes, featured: pd.DataFrame, universe_size: int) -> None:
    y = np.arange(len(featured))
    ranks = featured["depletion_rank"].to_numpy(dtype=float)
    ax.axvspan(1, 100, facecolor=TOP100_BAND, edgecolor="none", zorder=0)
    ax.axvline(100, color="#9B8CB5", linewidth=0.9, linestyle="--", zorder=1)
    ax.hlines(y, 1, ranks, color=LINK_COLOR, linewidth=2.4, zorder=1)
    ax.scatter(
        ranks,
        y,
        s=36,
        color=DEPLETION_COLOR,
        edgecolor="white",
        linewidth=0.55,
        zorder=3,
    )
    for rank, ypos in zip(ranks, y):
        ax.annotate(
            f"#{int(rank):,}",
            (rank, ypos),
            xytext=(4, 0),
            textcoords="offset points",
            va="center",
            fontsize=6.2,
            color=DEPLETION_COLOR,
        )

    ax.set_xscale("log")
    ax.set_xlim(1, universe_size * 1.28)
    ticks = [1, 10, 100, universe_size]
    ax.set_xticks(ticks, ["1", "10", "100", f"{universe_size:,}"])
    style_rows(ax, featured)
    ax.set_xlabel("Cell-depletion rank (1 = strongest)")
    ax.set_title("c  Cell-depletion rank", loc="left")
    ax.grid(axis="x")
    ax.text(
        0.48,
        0.98,
        "top 100",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=6.0,
        color=DEPLETION_COLOR,
    )
    square(ax)


def write_outputs(
    featured: pd.DataFrame,
    string: pd.DataFrame,
    category3_depletion: pd.DataFrame,
) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    featured.to_csv(OUTPUT_DIR / "featured_overpredictions.csv", index=False)
    string.to_csv(OUTPUT_DIR / "featured_string_neighbors.csv", index=False)
    category3_depletion.to_csv(OUTPUT_DIR / "category3_depletion_ranks.csv", index=False)

    strict_names = set(
        featured.loc[featured["role"].eq("strict category 3"), "target_name"]
    )
    status_counts = {status: 0 for status in STRING_STATUS_ORDER}
    for target in strict_names:
        for network in NETWORK_ORDER:
            neighbors = string[
                string["p"].eq(target) & string["network"].eq(network)
            ]
            if neighbors.empty:
                status_counts["none"] += 1
            elif neighbors["partner_responds"].any():
                status_counts["responding"] += 1
            else:
                status_counts["zero_only"] += 1
    rank_lines = "\n".join(
        f"- {row.target_name}: observed {int(row.actual_n_degs)}, predicted "
        f"{int(row.bioagents_predicted_n_degs)}, depletion rank "
        f"{int(row.depletion_rank):,}/1,948"
        for row in featured.itertuples(index=False)
    )
    top100_all = int(category3_depletion["depletion_rank"].le(100).sum())
    (OUTPUT_DIR / "RESULTS.md").write_text(
        "# Task-1 category-3 overpredictions and cell-depletion rank\n\n"
        "The figure contains the six largest strict category-3 calls (observed zero, "
        "BioAgents predicted response) plus Pomp as a marked near-null reference. "
        "Pomp is not category 3: it has 4 observed and 600 predicted DEGs.\n\n"
        f"{rank_lines}\n\n"
        "## General STRING-neighbor pattern\n\n"
        "The display does not use response matching to select a neighbor. It shows "
        "up to two qualifying training neighbors per network, with responding "
        "neighbors ordered first and the remaining-neighbor count retained. Across "
        "the 18 strict-category-3 target-by-network comparisons, "
        f"{status_counts['responding']} contain at least one responding neighbor, "
        f"{status_counts['zero_only']} contain only zero-response neighbors, and "
        f"{status_counts['none']} have no qualifying neighbor. For Thoc2, all three "
        "network definitions show Thoc1 (303 DEGs) and Ddx39b (0 DEGs).\n\n"
        "## Depletion pattern\n\n"
        "Taf1, Pafah1b1, and Thoc2 occupy depletion ranks 3, 5, and 8, respectively. "
        "Pomp is rank 25. Med12, Hnrnpa1, and Smc3 are ranks 218, 1,057, and 1,620. "
        f"Across all 30 strict category-3 targets, {top100_all} are in the top 100 "
        "cell-depletion ranks.\n\n"
        "This supports an endpoint-mismatch interpretation for a subset: a target can "
        "be strongly depleted from the recovered population yet have zero downstream "
        "DEGs among surviving cells. It does not show that depletion caused the model "
        "prediction, and the weak depletion ranks of several other overpredictions show "
        "that depletion is not a universal explanation.\n",
        encoding="utf-8",
    )


def main() -> None:
    featured, string, category3_depletion, depletion = load_data()
    write_outputs(featured, string, category3_depletion)
    house_style()
    panels: dict[str, Callable[[plt.Axes], None]] = {
        "a": lambda ax: draw_overprediction(ax, featured),
        "b": lambda ax: draw_string_matrix(ax, featured, string),
        "c": lambda ax: draw_depletion_rank(ax, featured, len(depletion)),
    }
    written = plate(
        panels,
        OUTPUT_DIR,
        OUTPUT_STEM,
        panel_size=(3.35, 3.35),
        joint_size=(10.5, 3.35),
        concepts={
            "observed count": OBSERVED_COLOR,
            "BioAgents prediction": PREDICTED_COLOR,
            "no qualifying STRING neighbor": STRING_STATUS_COLORS["none"],
            "only zero-response STRING neighbors": STRING_STATUS_COLORS["zero_only"],
            "responding STRING neighbor": STRING_STATUS_COLORS["responding"],
            "cell-depletion rank": DEPLETION_COLOR,
        },
        tight_kw={"pad": 0.6},
    )
    print("  strict category-3 top six:", ", ".join(featured.iloc[1:]["target_name"]))
    print(
        "  featured depletion ranks:",
        ", ".join(
            f"{row.target_name}=#{int(row.depletion_rank)}"
            for row in featured.itertuples(index=False)
        ),
    )
    print("  wrote", len(written), "panel/plate files")


if __name__ == "__main__":
    main()
