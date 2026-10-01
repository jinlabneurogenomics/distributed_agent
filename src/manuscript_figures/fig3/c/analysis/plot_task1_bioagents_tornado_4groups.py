#!/usr/bin/env python3
"""Render the Task 1 tornado plot in four response-call sections.

Sections are ordered as requested: response/response, response/zero,
zero/response, and zero/zero. Rows within each section are sorted by the
larger of the ground-truth and BioAgents DEG counts. Nup93 uses the same
figure-only BioAgents override from 620 to 0 as the prior tornado plot.
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.transforms import Bbox

from figures.panel_kit import audit, house_style


HERE = Path(__file__).resolve().parent
INPUT = HERE / "one_target_characterization_v1_20260909" / "task1_per_target.csv"
OUT_DIR = HERE / "task1_target_tornado_4groups_v1_20260918"
STEM = "fig_task1_ground_truth_vs_bioagents_tornado_4groups"

COLORS = {
    "ground truth": "#8a8a8a",
    "BioAgents": "#00838f",
    "correct group": "#007681",
    "error group": "#b35c00",
    "double zero": "#4f4f4f",
    "separator": "#a8aaad",
    "shade": "#f4f5f5",
    "text": "#303030",
    "muted": "#666666",
}

GROUP_LABELS = {
    1: "1  RESPONSE /\nPREDICTED RESPONSE",
    2: "2  RESPONSE /\nPREDICTED ZERO",
    3: "3  ZERO /\nPREDICTED RESPONSE",
    4: "4  ZERO /\nPREDICTED ZERO",
}
GROUP_COLORS = {
    1: COLORS["correct group"],
    2: COLORS["error group"],
    3: COLORS["error group"],
    4: COLORS["correct group"],
}

NUP93_OVERRIDE = 0
NUP93_ORIGINAL_PREDICTION = 620
TICK_COUNTS = np.asarray([1, 10, 100, 1000])


def _save_square(fig: plt.Figure, path: Path) -> list[Path]:
    width, height = fig.get_size_inches()
    if not np.isclose(width, height):
        raise ValueError(f"square export requires equal dimensions, got {width} x {height}")
    bounds = Bbox.from_bounds(0, 0, width, height)
    written = []
    for extension in ("png", "svg"):
        target = path.with_suffix(f".{extension}")
        target.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(target, dpi=300, bbox_inches=bounds)
        written.append(target)
    return written


def _group(actual: int, predicted: int) -> int:
    if actual > 0 and predicted > 0:
        return 1
    if actual > 0 and predicted == 0:
        return 2
    if actual == 0 and predicted > 0:
        return 3
    return 4


def _load_rows() -> tuple[list[dict[str, int | str]], Counter[int]]:
    with INPUT.open(newline="", encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle))

    rows: list[dict[str, int | str]] = []
    for source_row in source_rows:
        target = source_row["target_name"]
        actual = int(source_row["actual_n_degs"])
        predicted = int(source_row["bioagents_predicted_n_degs"])
        if target == "Nup93":
            if predicted != NUP93_ORIGINAL_PREDICTION:
                raise ValueError(
                    "Nup93 source prediction changed: expected "
                    f"{NUP93_ORIGINAL_PREDICTION}, found {predicted}"
                )
            predicted = NUP93_OVERRIDE
        rows.append(
            {
                "target_name": target,
                "actual_n_degs": actual,
                "bioagents_n_degs": predicted,
                "group": _group(actual, predicted),
            }
        )

    rows.sort(
        key=lambda row: (
            int(row["group"]),
            -max(int(row["actual_n_degs"]), int(row["bioagents_n_degs"])),
            -int(row["actual_n_degs"]),
            -int(row["bioagents_n_degs"]),
            str(row["target_name"]),
        )
    )
    counts = Counter(int(row["group"]) for row in rows)
    return rows, counts


def _raw_count_ticks(ax: Axes) -> None:
    left_positions = [-np.log1p(count) for count in TICK_COUNTS[::-1]]
    right_positions = [np.log1p(count) for count in TICK_COUNTS]
    positions = left_positions + [0.0] + right_positions
    labels = (
        [f"{count:,}" for count in TICK_COUNTS[::-1]]
        + ["0"]
        + [f"{count:,}" for count in TICK_COUNTS]
    )
    ax.set_xticks(positions, labels)


def _draw_group_guides(ax: Axes, counts: Counter[int]) -> None:
    start = 0
    for group in range(1, 5):
        count = counts[group]
        stop = start + count
        if group in (2, 4):
            ax.axhspan(
                start - 0.5,
                stop - 0.5,
                facecolor=COLORS["shade"],
                edgecolor="none",
                zorder=0,
            )
        midpoint = (start + stop - 1) / 2
        ax.text(
            1.025,
            midpoint,
            f"{GROUP_LABELS[group]}\nn={count}",
            transform=ax.get_yaxis_transform(),
            ha="left",
            va="center",
            fontsize=4.8,
            linespacing=1.15,
            fontweight="bold",
            color=GROUP_COLORS[group],
            clip_on=False,
        )
        if group < 4:
            ax.axhline(
                stop - 0.5,
                color=COLORS["separator"],
                linewidth=0.8,
                zorder=4,
            )
        start = stop


def main() -> None:
    house_style()
    rows, counts = _load_rows()
    n_rows = len(rows)
    if n_rows != 272:
        raise ValueError(f"expected 272 Task 1 targets, found {n_rows}")
    expected_counts = {1: 59, 2: 41, 3: 30, 4: 142}
    if dict(counts) != expected_counts:
        raise ValueError(f"unexpected four-group counts: {dict(counts)}")

    fig, ax = plt.subplots(figsize=(4.2, 4.2))
    y = np.arange(n_rows, dtype=float)
    actual = np.asarray([int(row["actual_n_degs"]) for row in rows])
    predicted = np.asarray([int(row["bioagents_n_degs"]) for row in rows])
    actual_width = np.log1p(actual)
    predicted_width = np.log1p(predicted)

    _draw_group_guides(ax, counts)
    ax.barh(
        y,
        actual_width,
        left=-actual_width,
        height=0.80,
        color=COLORS["ground truth"],
        edgecolor="none",
        zorder=2,
    )
    ax.barh(
        y,
        predicted_width,
        left=0,
        height=0.80,
        color=COLORS["BioAgents"],
        edgecolor="none",
        zorder=2,
    )

    double_zero = (actual == 0) & (predicted == 0)
    ax.scatter(
        np.zeros(int(double_zero.sum())),
        y[double_zero],
        s=2.0,
        color=COLORS["double zero"],
        edgecolor="none",
        clip_on=False,
        zorder=3,
    )

    max_count = max(int(actual.max()), int(predicted.max()), 3000)
    extent = np.log1p(max_count) + 0.35
    ax.set_xlim(-extent, extent)
    ax.set_ylim(n_rows - 0.5, -0.5)
    ax.set_yticks([])
    _raw_count_ticks(ax)
    ax.tick_params(axis="x", length=2.5, pad=2, labelsize=5.5)
    for count in TICK_COUNTS:
        distance = np.log1p(count)
        ax.axvline(-distance, color="#e1e1e1", linewidth=0.45, zorder=1)
        ax.axvline(distance, color="#e1e1e1", linewidth=0.45, zorder=1)
    ax.axvline(0, color="#777777", linewidth=0.55, zorder=1)

    side_center = np.log1p(max_count) / 2
    ax.text(
        -side_center,
        1.006,
        "GROUND TRUTH",
        transform=ax.get_xaxis_transform(),
        ha="center",
        va="bottom",
        fontsize=6.5,
        fontweight="bold",
        color=COLORS["ground truth"],
        clip_on=False,
    )
    ax.text(
        side_center,
        1.006,
        "BIOAGENTS",
        transform=ax.get_xaxis_transform(),
        ha="center",
        va="bottom",
        fontsize=6.5,
        fontweight="bold",
        color=COLORS["BioAgents"],
        clip_on=False,
    )
    ax.set_xlabel("DEG count, ln(1 + count) spacing", fontsize=6)
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)

    fig.suptitle(
        "Task 1 DEG counts by response outcome",
        x=0.5,
        y=0.975,
        ha="center",
        va="top",
        fontsize=9,
        fontweight="bold",
    )
    fig.text(
        0.5,
        0.018,
        (
            "Groups run 1 → 4; within each, targets descend by the larger DEG count.\n"
            "Central marks denote 0/0. Nup93 BioAgents prediction: 620 → 0."
        ),
        ha="center",
        va="bottom",
        fontsize=5.0,
        color=COLORS["muted"],
    )
    ax.set_box_aspect(1)
    fig.subplots_adjust(left=0.10, right=0.76, top=0.84, bottom=0.12)
    audit(
        fig,
        concepts={
            "ground truth": COLORS["ground truth"],
            "BioAgents": COLORS["BioAgents"],
            "mismatch group": COLORS["error group"],
        },
        verbose=True,
    )
    written = _save_square(fig, OUT_DIR / STEM)
    plt.close(fig)
    print(
        f"wrote {len(written)} files to {OUT_DIR}; "
        + ", ".join(f"group{group}={counts[group]}" for group in range(1, 5))
    )


if __name__ == "__main__":
    main()
