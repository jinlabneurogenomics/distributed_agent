#!/usr/bin/env python3
"""Visualize Task 1 STRING support and selected analogue reasoning.

Panel a is the population-level result for actual responders. Panel b is a
trace-audited analogue landscape: three clean cases and one qualified
higher-response case where BioAgents used broader mechanistic calibration,
followed by two controls that prevent the pattern from being overinterpreted.

The case panel is square even though its x-axis is long: six rows remain
legible, and equal panel dimensions let the population and mechanism views tile
as a compact manuscript plate.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch, Rectangle

from figures.panel_kit import breathe, house_style, plate, square


HERE = Path(__file__).resolve().parent
BUCKET_DIR = HERE / "task1_string_partner_buckets_v1_20260919"
SUMMARY_CSV = BUCKET_DIR / "stratified_bucket_summary.csv"
PER_TARGET_CSV = HERE / "one_target_characterization_v1_20260909" / "task1_per_target.csv"
TRAINING_COUNTS_CSV = (
    HERE
    / "holdout_task"
    / "Inputs"
    / "151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv"
)
OUT_DIR = HERE / "task1_analogue_flexibility_v1_20260919"
STEM = "fig_task1_analogue_flexibility"

NETWORK_COLORS = {
    "functional": "#3676A8",
    "physical": "#4F8A4C",
    "literature": "#B04A7A",
}
NETWORK_LABELS = {
    "functional": "Functional",
    "physical": "Physical",
    "literature": "Text-mining",
}
ACTUAL_COLOR = "#222222"
BIOAGENTS_COLOR = "#00838F"
STRING_COLOR = "#6F4C9B"
ALTERNATIVE_COLOR = "#D57A1F"
CARD_BORDER_COLOR = "#D7DADD"
CARD_TEXT_COLOR = "#252525"
CARD_MUTED_COLOR = "#666666"

# Plot typography is independent of the denser prose-card typography because
# panel b is commonly reduced as a unit during manuscript assembly.
PLOT_TITLE_SIZE = 12.0
PLOT_AXIS_SIZE = 10.5
PLOT_TICK_SIZE = 9.5
PLOT_ROW_SIZE = 10.5
PLOT_ANNOTATION_SIZE = 7.0
PLOT_LEGEND_SIZE = 8.2
TRACE_HEADER_SIZE = 7.6
TRACE_BODY_SIZE = 7.0

BUCKETS = ("A", "B", "C")
BUCKET_LABELS = (
    "No\npartner",
    "Partner,\ndifferent range",
    "Partner,\nsame range",
)

# Comparator membership was audited directly against the corresponding frozen
# BioAgents trace. Psmc5 and Tbce are deliberate controls: Psmc5 had matched
# same-complex STRING support, while Tbce copied the Tbcd count exactly.
CASES = (
    {
        "target": "Srrm2",
        "label": "Srrm2",
        "direct": ("Prpf6", "Cdc40"),
        "alternative": ("Son", "Hnrnpc", "Matr3", "Tardbp", "Snrnp70"),
    },
    {
        "target": "Myt1l",
        "label": "Myt1l",
        "direct": (),
        "alternative": ("Tbr1", "Mecp2", "Arid1a", "Chd2", "Chd4", "Sin3a"),
    },
    {
        "target": "Eef1a2",
        "label": "Eef1a2",
        "direct": ("Hsf1",),
        "alternative": ("Eef2",),
    },
    {
        "target": "Kmt2e",
        "label": "Kmt2e",
        "direct": (),
        "alternative": ("Kmt2c", "Ogt", "Crebbp", "Setd5", "Kmt2a", "Setd1a"),
    },
    {
        "target": "Psmc5",
        "label": "Psmc5",
        "direct": ("Psmc1", "Psmb4"),
        "alternative": (),
    },
    {
        "target": "Tbce",
        "label": "Tbce",
        "direct": ("Tbcd",),
        "alternative": (),
    },
)

TRACE_CARDS = {
    "Srrm2": {
        "quote": (
            "“I place Srrm2 below Thoc1/Prpf6 and well below\n"
            "U2af2/Rnpc3, but slightly above the weaker\n"
            "associated RNA-binding anchors Hnrnpc, Matr3,\n"
            "Tardbp, and Snrnp70. The point estimate is\n"
            "therefore 260 DEGs.”"
        ),
    },
    "Myt1l": {
        "quote": (
            "“The closest observed response-breadth anchors are\n"
            "therefore the modest chromatin and methyl-DNA factors,\n"
            "especially Mecp2 at 16 DEGs, Arid1a at 22, and Chd2\n"
            "at 34, with the many zero-count neuronal TFs pulling\n"
            "the estimate down and Sin3a/Chd4 treated as\n"
            "mechanistically too broad. […] Final point prediction:\n"
            "12 DEGs.”"
        ),
    },
    "Eef1a2": {
        "quote": (
            "“I did not scale the prediction to hundreds of DEGs,\n"
            "however, for three reasons. First, the same causal class\n"
            "was muted in the exact focal endpoint: Eef2 gave only\n"
            "9 focal DEGs, even though EEF2 was much broader in\n"
            "upper-layer cortical neurons in the same experiment.\n"
            "[…] Prediction: Eef1a2 = 12 DEGs at BH FDR 0.05 in\n"
            "151 TH Prkcd Grin2c Glut.”"
        ),
    },
    "Kmt2e": {
        "quote": (
            "“The better numerical bracket is therefore the\n"
            "low-positive chromatin/NDD region represented by Ogt\n"
            "at 4, Crebbp at 8, and Setd5 at 9, with Kmt2a at 24\n"
            "as an upper edge and Kmt2c at 0 as a null counterexample.\n"
            "[…] Final point prediction: 6 DEGs.”"
        ),
    },
}


def _bucket_panel(ax: plt.Axes) -> None:
    data = pd.read_csv(SUMMARY_CSV)
    data = data[
        data["stratum"].eq("actual_nonzero")
        & data["outcome"].eq("bioagents_absolute_log1p_error")
    ]
    offsets = {"functional": -0.18, "physical": 0.0, "literature": 0.18}
    for network in NETWORK_COLORS:
        selected = data[data["network"].eq(network)].set_index("bucket").loc[list(BUCKETS)]
        x = np.arange(len(BUCKETS), dtype=float) + offsets[network]
        mean = selected["mean"].to_numpy(dtype=float)
        low = selected["mean_ci_low"].to_numpy(dtype=float)
        high = selected["mean_ci_high"].to_numpy(dtype=float)
        ax.errorbar(
            x,
            mean,
            yerr=np.vstack((mean - low, high - mean)),
            color=NETWORK_COLORS[network],
            marker="o",
            markersize=5.5,
            markerfacecolor="white",
            markeredgewidth=1.5,
            linewidth=1.5,
            capsize=3,
            label=NETWORK_LABELS[network],
            zorder=3,
        )
    ax.set_xticks(np.arange(len(BUCKETS)), BUCKET_LABELS)
    ax.set_ylabel("Absolute log1p count error ↓")
    ax.set_ylim(0, 3.65)
    ax.grid(axis="y", color="#dddddd", linewidth=0.6, zorder=0)
    ax.legend(frameon=False, loc="upper right", fontsize=7)
    ax.set_title("a  Matched neighbors have lower error", loc="left")
    square(ax)


def _annotate_comparators(
    ax: plt.Axes,
    names: tuple[str, ...],
    counts: dict[str, int],
    y: float,
    color: str,
    marker: str,
) -> None:
    if not names:
        return
    jitter = np.linspace(-0.13, 0.13, len(names)) if len(names) > 1 else np.array([0.0])
    for index, (name, dy) in enumerate(zip(names, jitter, strict=True)):
        x = np.log1p(counts[name])
        ax.scatter(
            [x],
            [y + dy],
            s=60,
            marker=marker,
            facecolor="white",
            edgecolor=color,
            linewidth=1.1,
            clip_on=False,
            zorder=4,
        )
        vertical = 5 if index % 2 == 0 else -8
        # Zero-count comparators sit next to the low x spine. Keep their labels
        # inside the plotting field rather than placing text across the y-axis.
        if counts[name] == 0:
            horizontal = 7
        elif len(names) == 1 and marker == "^":
            horizontal = 7
        else:
            horizontal = -5 if index % 2 == 0 else 5
        ax.annotate(
            name,
            (x, y + dy),
            xytext=(horizontal, vertical),
            textcoords="offset points",
            ha="right" if horizontal < 0 else "left",
            va="bottom" if vertical > 0 else "top",
            fontsize=PLOT_ANNOTATION_SIZE,
            color=color,
            clip_on=False,
        )


def _draw_trace_card(ax: plt.Axes, target: str, card_index: int) -> None:
    """Draw one enlarged trace excerpt in a plot-height-aligned card column."""
    card = TRACE_CARDS[target]
    transform = ax.transAxes
    x = 1.055
    width = 0.70
    height = 0.235
    gap = 0.012
    y0 = 1.0 - height - card_index * (height + gap)

    ax.add_patch(
        FancyBboxPatch(
            (x, y0),
            width,
            height,
            boxstyle="round,pad=0.008,rounding_size=0.015",
            transform=transform,
            facecolor="white",
            edgecolor=CARD_BORDER_COLOR,
            linewidth=0.8,
            clip_on=False,
            zorder=8,
        )
    )
    ax.add_patch(
        Rectangle(
            (x, y0 + height - 0.008),
            width,
            0.008,
            transform=transform,
            facecolor=ALTERNATIVE_COLOR,
            edgecolor="none",
            clip_on=False,
            zorder=9,
        )
    )
    pad_x = 0.026
    ax.text(
        x + pad_x,
        y0 + height - 0.025,
        "BIOAGENTS TRACE",
        transform=transform,
        ha="left",
        va="top",
        fontsize=TRACE_HEADER_SIZE,
        fontweight="bold",
        color=ALTERNATIVE_COLOR,
        clip_on=False,
        zorder=10,
    )
    ax.text(
        x + pad_x,
        y0 + height - 0.071,
        card["quote"],
        transform=transform,
        ha="left",
        va="top",
        fontsize=TRACE_BODY_SIZE,
        fontstyle="italic",
        linespacing=1.08,
        color=CARD_TEXT_COLOR,
        clip_on=False,
        zorder=10,
    )


def _analogue_panel(ax: plt.Axes) -> None:
    performance = pd.read_csv(PER_TARGET_CSV).set_index("target_name")
    training = pd.read_csv(TRAINING_COUNTS_CSV).set_index("target_name")["n_degs"]
    counts = {str(name): int(value) for name, value in training.items()}

    for row_index, case in enumerate(CASES):
        target = case["target"]
        actual = int(performance.loc[target, "actual_n_degs"])
        predicted = int(performance.loc[target, "bioagents_predicted_n_degs"])
        y = float(len(CASES) - 1 - row_index)
        actual_x = np.log1p(actual)
        predicted_x = np.log1p(predicted)
        ax.plot(
            [actual_x, predicted_x],
            [y, y],
            color=BIOAGENTS_COLOR,
            alpha=0.45,
            linewidth=1.8,
            zorder=1,
        )
        _annotate_comparators(
            ax, case["alternative"], counts, y, ALTERNATIVE_COLOR, "^"
        )
        _annotate_comparators(ax, case["direct"], counts, y, STRING_COLOR, "s")
        ax.scatter(
            [actual_x],
            [y],
            s=78,
            marker="D",
            facecolor=ACTUAL_COLOR,
            edgecolor="white",
            linewidth=0.6,
            clip_on=False,
            zorder=6,
        )
        ax.scatter(
            [predicted_x],
            [y],
            s=44,
            marker="o",
            facecolor=BIOAGENTS_COLOR,
            edgecolor="white",
            linewidth=0.7,
            clip_on=False,
            zorder=7,
        )

    for card_index, target in enumerate(TRACE_CARDS):
        _draw_trace_card(ax, target, card_index)

    ticks = np.array((0, 1, 5, 10, 50, 100, 500, 1500), dtype=float)
    ax.set_xticks(np.log1p(ticks), [f"{int(value):,}" for value in ticks])
    ax.set_xlim(0, np.log1p(1_650))
    ax.set_yticks(
        np.arange(len(CASES) - 1, -1, -1),
        [str(case["label"]) for case in CASES],
    )
    ax.set_xlabel("DEG count (log-scaled position)", fontsize=PLOT_AXIS_SIZE)
    ax.axhline(1.5, color="#999999", linewidth=0.8)
    ax.grid(axis="x", color="#e0e0e0", linewidth=0.6, zorder=0)
    handles = [
        plt.Line2D([], [], marker="D", linestyle="", color=ACTUAL_COLOR, label="Observed"),
        plt.Line2D([], [], marker="o", linestyle="", color=BIOAGENTS_COLOR, label="BioAgents"),
        plt.Line2D([], [], marker="s", linestyle="", markerfacecolor="white", color=STRING_COLOR, label="Qualifying STRING"),
        plt.Line2D([], [], marker="^", linestyle="", markerfacecolor="white", color=ALTERNATIVE_COLOR, label="Trace-selected alternative"),
    ]
    ax.legend(
        handles=handles,
        frameon=False,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.16),
        ncol=2,
        fontsize=PLOT_LEGEND_SIZE,
    )
    ax.tick_params(axis="x", labelsize=PLOT_TICK_SIZE)
    ax.tick_params(axis="y", labelsize=PLOT_ROW_SIZE, pad=7)
    ax.set_title(
        "b  Selected exceptions and controls",
        loc="left",
        fontsize=PLOT_TITLE_SIZE,
        pad=10,
    )
    ax.text(
        1.055,
        1.02,
        "TRACE EXCERPTS",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=6.2,
        fontweight="bold",
        color=CARD_MUTED_COLOR,
        clip_on=False,
    )
    breathe(ax, "x", "low")
    breathe(ax, "x", "high")
    square(ax)


def main() -> None:
    house_style()
    concepts = {
        "functional network": NETWORK_COLORS["functional"],
        "physical network": NETWORK_COLORS["physical"],
        "text-mining network": NETWORK_COLORS["literature"],
        "observed response": ACTUAL_COLOR,
        "BioAgents prediction": BIOAGENTS_COLOR,
        "qualifying STRING neighbor": STRING_COLOR,
        "trace-selected alternative": ALTERNATIVE_COLOR,
    }
    written = plate(
        {"a": _bucket_panel, "b": _analogue_panel},
        OUT_DIR,
        STEM,
        panel_size=(11.5, 6.1),
        joint_size=(13.5, 6.4),
        concepts=concepts,
        tight_kw={"pad": 0.7},
    )
    print(f"wrote {len(written)} files to {OUT_DIR}")


if __name__ == "__main__":
    main()
