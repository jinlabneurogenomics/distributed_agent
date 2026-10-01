#!/usr/bin/env python3
"""Plot Task-1 predictive performance against depletion and cell recovery."""

from __future__ import annotations

import os
import sys
from collections.abc import Callable
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/bioagents-mpl")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "src"))

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from scipy.stats import pearsonr, spearmanr  # noqa: E402

from figures.panel_kit import house_style, plate, square  # noqa: E402


INPUT_CSV = (
    HERE
    / "holdout_depletion_rank_cells_v1_20260919"
    / "holdout_depletion_rank_recovered_cells.csv"
)
OUTPUT_DIR = HERE / "prediction_error_vs_depletion_v1_20260919"
OUTPUT_STEM = "fig_prediction_error_vs_depletion"

SYSTEMS = {
    "Codex": ("codex_predicted_n_degs", "#0072B2"),
    "BioAgents": ("bioagents_predicted_n_degs", "#D55E00"),
}
DEPLETION_ORDER = [
    "reference",
    "0.1–0.2",
    "0.2–0.3",
    "0.3–0.5",
    "0.5–0.9",
    ">0.9",
]
DEPLETION_LABELS = [
    "≤.1",
    ".1–.2",
    ".2–.3",
    ".3–.5",
    ".5–.9",
    ">.9",
]
def deterministic_jitter(n: int, *, group_index: int, system_index: int) -> np.ndarray:
    """Stable horizontal jitter without implying an additional statistic."""
    if n <= 1:
        return np.zeros(n)
    base = np.linspace(-0.07, 0.07, n)
    shift = (group_index * 17 + system_index * 11) % n
    return np.roll(base, shift)


def load_data() -> pd.DataFrame:
    frame = pd.read_csv(INPUT_CSV)
    if len(frame) != 272:
        raise ValueError(f"Expected 272 holdouts, found {len(frame)}")
    for system, (prediction_column, _) in SYSTEMS.items():
        signed = np.log1p(frame[prediction_column]) - np.log1p(frame["actual_n_degs"])
        frame[f"{system}_absolute_log1p_error"] = signed.abs()
        frame[f"{system}_squared_log1p_error"] = signed.pow(2)
        frame[f"{system}_effect_correct"] = (
            frame[prediction_column].gt(0).eq(frame["actual_n_degs"].gt(0)).astype(float)
        )
    frame["framework_mean_absolute_log1p_error"] = frame[
        [f"{system}_absolute_log1p_error" for system in SYSTEMS]
    ].mean(axis=1)
    frame["depletion_stratum"] = pd.cut(
        frame["log2_depletion_odds_ratio"],
        bins=[-np.inf, 0.1, 0.2, 0.3, 0.5, 0.9, np.inf],
        labels=DEPLETION_ORDER,
        include_lowest=True,
    ).astype(str)
    frame["cell_bin"] = pd.cut(
        frame["recovered_perturbed_cells"],
        bins=[-np.inf, 74, 99, 124, 149, 174, 199, 224, 249, 274, 299, np.inf],
        labels=[
            "<75",
            "75–99",
            "100–124",
            "125–149",
            "150–174",
            "175–199",
            "200–224",
            "225–249",
            "250–274",
            "275–299",
            "≥300",
        ],
        include_lowest=True,
    ).astype(str)
    return frame


def draw_grouped_metric(
    ax: plt.Axes,
    frame: pd.DataFrame,
    *,
    group_column: str,
    group_order: list[str],
    group_labels: list[str],
    outcome_suffix: str,
    ylabel: str,
    title: str,
    ylim: tuple[float, float],
    legend: bool,
) -> None:
    x = np.arange(len(group_order), dtype=float)
    offsets = {"Codex": -0.09, "BioAgents": 0.09}
    for system_index, (system, (_, color)) in enumerate(SYSTEMS.items()):
        means: list[float] = []
        raw_x: list[float] = []
        raw_y: list[float] = []
        for group_index, group in enumerate(group_order):
            values = frame.loc[
                frame[group_column].eq(group), f"{system}_{outcome_suffix}"
            ].to_numpy(dtype=float)
            mean = float(values.mean())
            jitter = deterministic_jitter(
                len(values), group_index=group_index, system_index=system_index
            )
            means.append(mean)
            raw_x.extend(group_index + offsets[system] + jitter)
            raw_y.extend(values)
        ax.scatter(
            raw_x,
            raw_y,
            s=9,
            color=color,
            alpha=0.28,
            edgecolor="none",
            rasterized=True,
            zorder=1,
        )
        xpos = x + offsets[system]
        means_array = np.asarray(means)
        ax.plot(xpos, means_array, color=color, linewidth=1.25, zorder=2)
        ax.scatter(
            xpos,
            means_array,
            s=26,
            facecolor="white",
            edgecolor=color,
            linewidth=1.0,
            clip_on=False,
            zorder=3,
        )

    counts = frame[group_column].value_counts()
    count_fontsize = 4.8 if len(group_order) > 8 else 5.7
    for xpos, group in zip(x, group_order):
        ax.text(
            xpos,
            0.985,
            f"n={int(counts[group])}",
            transform=ax.get_xaxis_transform(),
            ha="center",
            va="top",
            fontsize=count_fontsize,
            color="#6B7280",
        )
    ax.set_xticks(x, group_labels)
    if len(group_order) > 4:
        ax.tick_params(axis="x", labelrotation=35)
        for label in ax.get_xticklabels():
            label.set_ha("right")
    ax.set_xlim(-0.55, len(group_order) - 0.45)
    ax.set_ylim(*ylim)
    ax.set_ylabel(ylabel)
    ax.set_title(title, loc="left")
    ax.grid(axis="y")
    if legend:
        handles = [
            Line2D(
                [],
                [],
                marker="o",
                linestyle="-",
                markerfacecolor="white",
                markeredgecolor=color,
                color=color,
                label=system,
            )
            for system, (_, color) in SYSTEMS.items()
        ]
        ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.0, 0.91))
    square(ax)


def draw_depletion_mse(ax: plt.Axes, frame: pd.DataFrame) -> None:
    draw_grouped_metric(
        ax,
        frame,
        group_column="depletion_stratum",
        group_order=DEPLETION_ORDER,
        group_labels=DEPLETION_LABELS,
        outcome_suffix="absolute_log1p_error",
        ylabel="Absolute log1p count error",
        title="a  Error concentrates in the depletion tail",
        ylim=(-0.08, 7.6),
        legend=True,
    )
    ax.set_xlabel("log₂ Fisher odds-ratio stratum\n← enrichment | depletion →")


def draw_depletion_accuracy(ax: plt.Axes, frame: pd.DataFrame) -> None:
    draw_grouped_metric(
        ax,
        frame,
        group_column="depletion_stratum",
        group_order=DEPLETION_ORDER,
        group_labels=DEPLETION_LABELS,
        outcome_suffix="effect_correct",
        ylabel="Correct zero/nonzero call",
        title="b  Effect-call accuracy is less monotonic",
        ylim=(-0.03, 1.03),
        legend=False,
    )
    ax.set_xlabel("log₂ Fisher odds-ratio stratum\n← enrichment | depletion →")
    ax.set_yticks(
        [0, 0.2, 0.4, 0.6, 0.8, 1.0],
        ["0%", "20%", "40%", "60%", "80%", "100%"],
    )


def draw_cell_mse(ax: plt.Axes, frame: pd.DataFrame) -> None:
    order = [
        "≥300",
        "275–299",
        "250–274",
        "225–249",
        "200–224",
        "175–199",
        "150–174",
        "125–149",
        "100–124",
        "75–99",
        "<75",
    ]
    draw_grouped_metric(
        ax,
        frame,
        group_column="cell_bin",
        group_order=order,
        group_labels=order,
        outcome_suffix="absolute_log1p_error",
        ylabel="Absolute log1p count error",
        title="c  Error rises as recovered cell number falls",
        ylim=(-0.08, 7.6),
        legend=False,
    )
    ax.set_xlabel("Recovered perturbed-cell bin\nhigh recovery ← | → low recovery")
    pearson = pearsonr(
        frame["recovered_perturbed_cells"],
        frame["framework_mean_absolute_log1p_error"],
    )
    spearman = spearmanr(
        frame["recovered_perturbed_cells"],
        frame["framework_mean_absolute_log1p_error"],
    )
    ax.text(
        0.025,
        0.90,
        (
            "Framework-mean error\n"
            f"Pearson r = {pearson.statistic:.2f} (p = {pearson.pvalue:.3f})\n"
            f"Spearman rho = {spearman.statistic:.2f} (p = {spearman.pvalue:.3f})"
        ),
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=5.7,
        color="#374151",
    )


def main() -> None:
    house_style()
    frame = load_data()
    panels: dict[str, Callable[[plt.Axes], None]] = {
        "a": lambda ax: draw_depletion_mse(ax, frame),
        "b": lambda ax: draw_depletion_accuracy(ax, frame),
        "c": lambda ax: draw_cell_mse(ax, frame),
    }
    plate(
        panels,
        OUTPUT_DIR,
        OUTPUT_STEM,
        layout=(1, 3),
        panel_size=(3.4, 3.4),
        joint_size=(11.7, 3.4),
        concepts={
            "Codex": "#0072B2",
            "BioAgents": "#D55E00",
        },
    )


if __name__ == "__main__":
    main()
