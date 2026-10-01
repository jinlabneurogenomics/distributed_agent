#!/usr/bin/env python
"""Figure-ready vertical replot of the three-arm literature-flag composition.

The pipeline figure (`final_flag_distribution_*.png`, written by
`finalize_distribution.py`) is a wide horizontal stacked bar. Rotating that
whole panel 90 degrees to fit the Figure 2 middle column left every label
sideways and unreadable. This script re-draws the same numbers as native
*vertical* stacked bars sized for the column slot: horizontal value labels,
arm names at 45 degrees, n above each bar, and a two-column legend.

Reads `final_overall_distribution.csv` (already written by the pipeline) and
writes `fig_three_arm_flags_vertical_<layer>.{png,svg,pdf}` next to it. It
never touches the pipeline's own outputs.

Run from anywhere:

    python manuscript/fig2/_debug/260731/final_three_arm_distribution/plot_three_arm_panel.py
"""

from __future__ import annotations

import csv
import os
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
STYLE = ROOT / "src/figures/style.mplstyle"
OVERALL_DISTRIBUTION = HERE / "final_overall_distribution.csv"

FLAGS = ("agree", "disagree", "inferred", "no_literature")
FLAG_LABELS = {
    "agree": "Agree",
    "disagree": "Disagree",
    "inferred": "Inferred",
    "no_literature": "No literature",
}
# Short 45-degree tick labels: the panel header already says these are shuffle
# arms, and full names cost ~0.85 in of diagonal height in a 2 in wide column.
# Swap in the full CSV names here if the panel is ever given more room.
ARM_DISPLAY = {
    "Unshuffled": "Unshuffled",
    "Within-screen shuffled": "Within-screen",
    "Out-of-screen shuffled": "Out-of-screen",
}
# Shared Figure 2 flag palette -- keep in sync with the other fig2 panels.
COLORS = {
    "agree": "#6fc46f",
    "disagree": "#ec835a",
    "inferred": "#898781",
    "no_literature": "#c3c2b7",
}
# Ink for a value label sitting on top of each fill (text tokens, not series color).
LABEL_INK = {
    "agree": "#1f3b1f",
    "disagree": "#ffffff",
    "inferred": "#ffffff",
    "no_literature": "#3d3c36",
}
SURFACE = "#ffffff"
INK = "#000000"
INK_MUTED = "#555555"

# Panel geometry: middle column of Figure 2 is ~2.0 in wide at 183 mm figure width.
FIG_W = 2.15
FIG_H = 2.65
BAR_WIDTH = 0.62
# Segments at least this tall (percent) can hold a horizontal label inside.
INSIDE_MIN = 9.0
# Outside labels for thinner segments: minimum vertical separation, in percent
# units, so a 2.3% slice sitting on top of a 6.1% slice still reads.
OUTSIDE_MIN_GAP = 7.5

FS_VALUE = 6.5
FS_SMALL_VALUE = 6.0
FS_ARM = 7.0
FS_N = 6.0
FS_LEGEND = 6.5

LAYERS = ("primary", "sensitivity")
SUBTITLES = {
    "primary": "Load-bearing findings",
    "sensitivity": "Load-bearing + evidence-only",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def setup_matplotlib() -> Any:
    os.environ.setdefault("MPLCONFIGDIR", "/tmp/mplconfig_final_three_arm_distribution")
    Path(os.environ["MPLCONFIGDIR"]).mkdir(parents=True, exist_ok=True)
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    if STYLE.is_file():
        plt.style.use(STYLE)
    plt.rcParams.update({"svg.fonttype": "none", "pdf.fonttype": 42})
    return plt


def arms_in_order(rows: list[dict[str, str]], layer: str) -> list[str]:
    seen: list[str] = []
    for row in rows:
        if row["analysis_layer"] == layer and row["arm"] not in seen:
            seen.append(row["arm"])
    return seen


def plot_layer(rows: list[dict[str, str]], layer: str) -> Path:
    plt = setup_matplotlib()
    from matplotlib.patches import Patch

    arms = arms_in_order(rows, layer)
    lookup = {
        (row["arm"], row["flag"]): row for row in rows if row["analysis_layer"] == layer
    }
    missing = [(arm, flag) for arm in arms for flag in FLAGS if (arm, flag) not in lookup]
    if missing:
        raise ValueError(f"{layer}: missing arm/flag rows {missing}")

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    x_positions = list(range(len(arms)))
    half = BAR_WIDTH / 2

    for x, arm in zip(x_positions, arms):
        bottom = 0.0
        outside: list[tuple[float, float]] = []  # (segment centre, percent)
        for flag in FLAGS:
            height = float(lookup[(arm, flag)]["percent"])
            ax.bar(
                x,
                height,
                bottom=bottom,
                width=BAR_WIDTH,
                color=COLORS[flag],
                edgecolor=SURFACE,
                linewidth=0.9,
                zorder=2,
            )
            centre = bottom + height / 2
            if height >= INSIDE_MIN:
                ax.text(
                    x,
                    centre,
                    f"{height:.1f}%",
                    ha="center",
                    va="center",
                    fontsize=FS_VALUE,
                    color=LABEL_INK[flag],
                    zorder=4,
                )
            elif height >= 0.05:
                outside.append((centre, height))
            bottom += height

        # Thin segments get a leader into the gutter; push the labels apart from
        # the bottom up so stacked thin slices never overprint each other.
        placed: list[float] = []
        for centre, height in sorted(outside):
            label_y = centre
            if placed and label_y - placed[-1] < OUTSIDE_MIN_GAP:
                label_y = placed[-1] + OUTSIDE_MIN_GAP
            placed.append(label_y)
            ax.plot(
                [x + half, x + half + 0.11, x + half + 0.16],
                [centre, label_y, label_y],
                color=INK_MUTED,
                linewidth=0.4,
                solid_capstyle="butt",
                clip_on=False,
                zorder=4,
            )
            ax.text(
                x + half + 0.19,
                label_y,
                f"{height:.1f}%",
                ha="left",
                va="center",
                fontsize=FS_SMALL_VALUE,
                color=INK_MUTED,
                clip_on=False,
                zorder=4,
            )

        n_findings = int(lookup[(arm, FLAGS[0])]["n_findings"])
        ax.text(
            x,
            101.5,
            f"n={n_findings:,}",
            ha="center",
            va="bottom",
            fontsize=FS_N,
            color=INK_MUTED,
            clip_on=False,
        )

    ax.set_xticks(x_positions)
    ax.set_xticklabels(
        [ARM_DISPLAY.get(arm, arm) for arm in arms],
        rotation=45,
        ha="right",
        rotation_mode="anchor",
        fontsize=FS_ARM,
        color=INK,
    )
    # Right headroom keeps the last bar's gutter labels inside the axes box.
    ax.set_xlim(-0.55, len(arms) - 1 + 0.95)
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_ylabel("Percent of findings", fontsize=FS_ARM)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(axis="x", length=0)
    ax.tick_params(axis="y", labelsize=FS_ARM)

    handles = [Patch(facecolor=COLORS[flag], label=FLAG_LABELS[flag]) for flag in FLAGS]
    ax.legend(
        handles=handles,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.38),
        ncol=2,
        frameon=False,
        fontsize=FS_LEGEND,
        handlelength=1.1,
        handleheight=0.9,
        columnspacing=1.0,
        handletextpad=0.5,
        labelspacing=0.45,
    )
    ax.text(
        0.0,
        1.15,
        SUBTITLES[layer],
        transform=ax.transAxes,
        fontsize=FS_N,
        color=INK_MUTED,
    )

    fig.subplots_adjust(left=0.20, right=0.97, bottom=0.34, top=0.90)
    stem = HERE / f"fig_three_arm_flags_vertical_{layer}"
    fig.savefig(stem.with_suffix(".png"), dpi=600, bbox_inches="tight")
    fig.savefig(stem.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)
    return stem


def main() -> None:
    rows = read_rows(OVERALL_DISTRIBUTION)
    for layer in LAYERS:
        stem = plot_layer(rows, layer)
        arms = arms_in_order(rows, layer)
        lookup = {
            (row["arm"], row["flag"]): row
            for row in rows
            if row["analysis_layer"] == layer
        }
        print(f"{layer}: {stem.name}.{{png,svg,pdf}}")
        for arm in arms:
            parts = " ".join(
                f"{FLAG_LABELS[flag]} {float(lookup[(arm, flag)]['percent']):.1f}%"
                for flag in FLAGS
            )
            n_findings = int(lookup[(arm, FLAGS[0])]["n_findings"])
            print(f"  {arm:<24} n={n_findings:>5,}  {parts}")


if __name__ == "__main__":
    main()
