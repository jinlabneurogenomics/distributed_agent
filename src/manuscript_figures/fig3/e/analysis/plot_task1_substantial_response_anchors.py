#!/usr/bin/env python3
"""Plot substantial Task-1 response predictions and their trace-selected anchors.

The primary set is defined before plotting: both observed and BioAgents counts
must be at least 50 DEGs and must differ by no more than threefold.  Tsc1 is
included below a divider as a near-miss because its trace used an unusually
clean same-complex anchor (Tsc2), making the remaining magnitude error
scientifically informative.

Panel a is square by house convention.  Panel b is a trace-card column and is
allowed to be text-shaped rather than data-shaped.  Both panels and the joint
plate are emitted from the same functions for Illustrator assembly.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch, Rectangle

from figures.panel_kit import breathe, house_style, plate, square


HERE = Path(__file__).resolve().parent
PER_TARGET_CSV = (
    HERE / "one_target_characterization_v1_20260909" / "task1_per_target.csv"
)
TRAINING_COUNTS_CSV = (
    HERE
    / "holdout_task"
    / "Inputs"
    / "151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv"
)
OUT_DIR = HERE / "task1_substantial_response_anchors_v1_20260919"
STEM = "fig_task1_substantial_response_anchors"

RUN_ROOT = (
    HERE.parents[1]
    / "runs"
    / "holdout-prediction"
    / "july-260713-adaptive-seed-260901"
)
REMAINING_RUN = "remaining262-post-ec7234d-20260902"
CURRENT_RUN = "current-tools10-20260902"

ACTUAL_COLOR = "#222222"
BIOAGENTS_COLOR = "#00838F"
STRING_COLOR = "#6F4C9B"
ALTERNATIVE_COLOR = "#D57A1F"
NEAR_MISS_COLOR = "#8A8A8A"
CARD_BORDER_COLOR = "#D7DADD"
CARD_TEXT_COLOR = "#252525"
CARD_MUTED_COLOR = "#666666"

PLOT_TITLE_SIZE = 13.5
PLOT_AXIS_SIZE = 11.5
PLOT_TICK_SIZE = 10.5
PLOT_ROW_SIZE = 12.0
PLOT_ANNOTATION_SIZE = 7.5
PLOT_LEGEND_SIZE = 9.0
CARD_TARGET_SIZE = 10.2
CARD_META_SIZE = 7.8
CARD_BODY_SIZE = 7.6

SUBSTANTIAL_MIN = 50
MAX_FOLD_ERROR = 3.0
PRIMARY_ORDER = ("Psmc5", "Fus", "Srrm2", "Apc", "Ddx23")
NEAR_MISS_TARGET = "Tsc1"


def _trace_path(run: str, batch: str) -> Path:
    return (
        RUN_ROOT
        / run
        / "results"
        / "holdout-deg-count"
        / "bioagents"
        / run
        / "bs001"
        / batch
        / "r01"
        / "trace.md"
    )


# Comparator membership was audited against each frozen BioAgents trace.
# ``string`` contains high-confidence functional STRING neighbors that the trace
# used quantitatively. ``alternative`` contains trace-selected comparators that
# do not meet that STRING definition.  Low/null counterexamples remain in the
# quoted cards rather than being plotted as magnitude anchors.
CASES = (
    {
        "target": "Psmc5",
        "string": ("Psmc1", "Psmb4"),
        "alternative": (),
        "placements": {
            "Psmc1": (-0.15, -5, -9),
            "Psmb4": (0.15, 6, -9),
        },
        "trace": _trace_path(REMAINING_RUN, "b0261"),
        "quote": (
            "I set Psmc5 below Psmb4 and slightly above Psmc1: below Psmb4 "
            "because the closer same-subcomplex anchor is the 430-DEG Psmc1 "
            "perturbation, [...] and because the two measured structural "
            "perturbations span a broad 430-742 range even in the same cell "
            "group. The final point prediction is therefore 520 DEGs."
        ),
    },
    {
        "target": "Fus",
        "string": ("Tardbp", "Snrnp70"),
        "alternative": ("Matr3", "Hnrnpc"),
        "placements": {
            "Hnrnpc": (0.30, -5, 7),
            "Matr3": (-0.30, -5, -9),
            "Tardbp": (0.12, 7, 7),
            "Snrnp70": (-0.12, 7, -9),
        },
        "trace": _trace_path(REMAINING_RUN, "b0182"),
        "quote": (
            "I therefore predict a nonzero intermediate focal-cell response "
            "for Fus, closest to the Tardbp 210 / Matr3 149 / Hnrnpc 122 tier "
            "and below the core spliceosome and Hnrnpu tier: [...]"
        ),
    },
    {
        "target": "Srrm2",
        "string": ("Prpf6", "Cdc40"),
        "alternative": ("Thoc1", "Hnrnpc", "Matr3", "Tardbp", "Snrnp70"),
        "placements": {
            "Hnrnpc": (-0.30, -4, -8),
            "Matr3": (0.10, -6, 8),
            "Tardbp": (-0.10, 7, -9),
            "Snrnp70": (0.30, -5, 8),
            "Thoc1": (0.05, 7, -9),
            "Prpf6": (-0.25, -5, -9),
            "Cdc40": (0.22, 7, -8),
        },
        "trace": _trace_path(REMAINING_RUN, "b0041"),
        "quote": (
            "Approximate count: I place Srrm2 below Thoc1/Prpf6 and well "
            "below U2af2/Rnpc3, but slightly above the weaker associated "
            "RNA-binding anchors Hnrnpc, Matr3, Tardbp, and Snrnp70. The point "
            "estimate is therefore 260 DEGs."
        ),
    },
    {
        "target": "Apc",
        "string": ("Ctnnb1",),
        "alternative": ("Tcf7l2",),
        "placements": {
            "Ctnnb1": (0.05, -5, 8),
            "Tcf7l2": (-0.05, -6, 8),
        },
        "trace": _trace_path(CURRENT_RUN, "b0008"),
        "quote": (
            "Apc: predicted 120 FDR<0.05 genes. The prediction is driven "
            "mainly by within-dataset Ctnnb1 at 383 and Tcf7l2 at 106 in the "
            "same focal cell group. [...] The small Gsk3b, Lrp6, and "
            "Frizzled counts pull the estimate down because not every Wnt "
            "component is limiting under sparse postnatal neuronal CRISPR."
        ),
    },
    {
        "target": "Ddx23",
        "string": ("Prpf6",),
        "alternative": ("Snrnp70", "Cdc40", "U2af2", "Thoc1"),
        "placements": {
            "Snrnp70": (-0.24, -5, -9),
            "Thoc1": (0.18, -5, 8),
            "Prpf6": (-0.02, -5, 9),
            "Cdc40": (-0.28, 7, -9),
            "U2af2": (0.28, -5, 8),
        },
        "trace": _trace_path(REMAINING_RUN, "b0091"),
        "quote": (
            "I therefore predicted a broad, clearly nonzero response, "
            "slightly below the observed Prpf6 count but above Snrnp70 and "
            "Thoc1. The point estimate is 380 DEGs. It is driven primarily "
            "by within-dataset Prpf6/Snrnp70/Cdc40/U2af2 evidence and "
            "externally by DDX23's assignment to the PRP28 U5/tri-snRNP "
            "activation step."
        ),
    },
    {
        "target": "Tsc1",
        "string": ("Tsc2",),
        "alternative": ("Depdc5",),
        "placements": {
            "Tsc2": (0.03, -5, 8),
            "Depdc5": (-0.03, -6, 8),
        },
        "trace": _trace_path(REMAINING_RUN, "b0060"),
        "quote": (
            "I therefore transferred most of the Tsc2 count to Tsc1, with a "
            "small downward adjustment for two uncertainties: TSC2 carries "
            "the catalytic GAP activity whereas TSC1 is the stabilizing "
            "partner, and the held-out Tsc1 guides could have had fewer "
            "recovered edited nuclei or a weaker effective perturbation than "
            "the measured Tsc2 guides."
        ),
    },
)


def load_data() -> tuple[pd.DataFrame, dict[str, int]]:
    performance = pd.read_csv(PER_TARGET_CSV).set_index("target_name")
    training = pd.read_csv(TRAINING_COUNTS_CSV).set_index("target_name")["n_degs"]
    counts = {str(name): int(value) for name, value in training.items()}

    positive = performance[
        performance["actual_n_degs"].gt(0)
        & performance["bioagents_predicted_n_degs"].gt(0)
    ].copy()
    positive["fold_error"] = positive[
        ["actual_n_degs", "bioagents_predicted_n_degs"]
    ].max(axis=1) / positive[
        ["actual_n_degs", "bioagents_predicted_n_degs"]
    ].min(axis=1)
    selected = positive[
        positive["actual_n_degs"].ge(SUBSTANTIAL_MIN)
        & positive["bioagents_predicted_n_degs"].ge(SUBSTANTIAL_MIN)
        & positive["fold_error"].le(MAX_FOLD_ERROR)
    ]
    if set(selected.index) != set(PRIMARY_ORDER):
        raise ValueError(
            "Substantial-response rule no longer yields the frozen five cases: "
            f"{sorted(selected.index)}"
        )

    for case in CASES:
        if not case["trace"].is_file():
            raise FileNotFoundError(case["trace"])
        for gene in (*case["string"], *case["alternative"]):
            if gene not in counts:
                raise KeyError(f"Missing training count for comparator {gene}")
    return performance, counts


def _annotate_comparators(
    ax: plt.Axes,
    names: tuple[str, ...],
    counts: dict[str, int],
    y: float,
    color: str,
    marker: str,
    placements: dict[str, tuple[float, int, int]],
) -> None:
    if not names:
        return
    for index, name in enumerate(names):
        dy, horizontal, vertical = placements.get(
            name,
            (0.0, -5 if index % 2 == 0 else 5, 6 if index % 2 == 0 else -9),
        )
        value = counts[name]
        x = np.log1p(value)
        ax.scatter(
            [x],
            [y + dy],
            s=72,
            marker=marker,
            facecolor="white",
            edgecolor=color,
            linewidth=1.25,
            clip_on=False,
            zorder=4,
        )
        if value == 0:
            horizontal = 7
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


def _anchor_panel(ax: plt.Axes) -> None:
    performance, counts = load_data()
    n = len(CASES)

    for row_index, case in enumerate(CASES):
        target = case["target"]
        actual = int(performance.loc[target, "actual_n_degs"])
        predicted = int(performance.loc[target, "bioagents_predicted_n_degs"])
        y = float(n - 1 - row_index)
        actual_x = np.log1p(actual)
        predicted_x = np.log1p(predicted)

        line_color = NEAR_MISS_COLOR if target == NEAR_MISS_TARGET else BIOAGENTS_COLOR
        ax.plot(
            [actual_x, predicted_x],
            [y, y],
            color=line_color,
            alpha=0.48,
            linewidth=2.0,
            zorder=1,
        )
        _annotate_comparators(
            ax,
            case["alternative"],
            counts,
            y,
            ALTERNATIVE_COLOR,
            "^",
            case["placements"],
        )
        _annotate_comparators(
            ax,
            case["string"],
            counts,
            y,
            STRING_COLOR,
            "s",
            case["placements"],
        )
        ax.scatter(
            [actual_x],
            [y],
            s=90,
            marker="D",
            facecolor=ACTUAL_COLOR,
            edgecolor="white",
            linewidth=0.7,
            clip_on=False,
            zorder=6,
        )
        ax.scatter(
            [predicted_x],
            [y],
            s=58,
            marker="o",
            facecolor=BIOAGENTS_COLOR,
            edgecolor="white",
            linewidth=0.8,
            clip_on=False,
            zorder=7,
        )

    ticks = np.array((0, 1, 5, 10, 50, 100, 500, 1_000), dtype=float)
    ax.set_xticks(np.log1p(ticks), [f"{int(value):,}" for value in ticks])
    ax.set_xlim(0, np.log1p(1_150))
    ax.set_yticks(
        np.arange(n - 1, -1, -1),
        [case["target"] for case in CASES],
    )
    ax.set_xlabel("DEG count (log-scaled position)", fontsize=PLOT_AXIS_SIZE)
    ax.grid(axis="x", color="#E0E0E0", linewidth=0.65, zorder=0)
    ax.axhline(0.5, color="#999999", linewidth=0.9)
    ax.text(
        np.log1p(1_110),
        0.34,
        "near miss",
        ha="right",
        va="top",
        fontsize=8.2,
        color=NEAR_MISS_COLOR,
    )
    handles = [
        plt.Line2D(
            [], [], marker="D", linestyle="", color=ACTUAL_COLOR, label="Observed"
        ),
        plt.Line2D(
            [], [], marker="o", linestyle="", color=BIOAGENTS_COLOR, label="BioAgents"
        ),
        plt.Line2D(
            [],
            [],
            marker="s",
            linestyle="",
            markerfacecolor="white",
            color=STRING_COLOR,
            label="Trace-used STRING neighbor",
        ),
        plt.Line2D(
            [],
            [],
            marker="^",
            linestyle="",
            markerfacecolor="white",
            color=ALTERNATIVE_COLOR,
            label="Trace-selected alternative",
        ),
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
    ax.tick_params(axis="y", labelsize=PLOT_ROW_SIZE, pad=8)
    ax.set_title(
        "a  Substantial responses and their anchors",
        loc="left",
        fontsize=PLOT_TITLE_SIZE,
        pad=11,
    )
    breathe(ax, "x", "low")
    breathe(ax, "x", "high")
    square(ax)


def _draw_card(
    ax: plt.Axes,
    case: dict[str, object],
    performance: pd.DataFrame,
    index: int,
) -> None:
    target = str(case["target"])
    actual = int(performance.loc[target, "actual_n_degs"])
    predicted = int(performance.loc[target, "bioagents_predicted_n_degs"])
    n = len(CASES)
    gap = 0.012
    height = (0.94 - gap * (n - 1)) / n
    y0 = 0.02 + (n - 1 - index) * (height + gap)
    x0 = 0.015
    width = 0.97

    ax.add_patch(
        FancyBboxPatch(
            (x0, y0),
            width,
            height,
            boxstyle="round,pad=0.006,rounding_size=0.015",
            transform=ax.transAxes,
            facecolor="white",
            edgecolor=CARD_BORDER_COLOR,
            linewidth=0.9,
            clip_on=False,
        )
    )
    stripe = NEAR_MISS_COLOR if target == NEAR_MISS_TARGET else ALTERNATIVE_COLOR
    ax.add_patch(
        Rectangle(
            (x0, y0 + height - 0.009),
            width,
            0.009,
            transform=ax.transAxes,
            facecolor=stripe,
            edgecolor="none",
            clip_on=False,
        )
    )
    ax.text(
        x0 + 0.022,
        y0 + height - 0.025,
        target,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=CARD_TARGET_SIZE,
        fontweight="bold",
        color=CARD_TEXT_COLOR,
    )
    ax.text(
        x0 + width - 0.022,
        y0 + height - 0.027,
        f"observed {actual:,}  |  predicted {predicted:,}",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=CARD_META_SIZE,
        color=CARD_MUTED_COLOR,
    )
    wrapped = textwrap.fill(str(case["quote"]), width=71)
    ax.text(
        x0 + 0.022,
        y0 + height - 0.066,
        f"“{wrapped}”",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=CARD_BODY_SIZE,
        fontstyle="italic",
        linespacing=1.06,
        color=CARD_TEXT_COLOR,
    )


def _card_panel(ax: plt.Axes) -> None:
    performance, _ = load_data()
    ax.set_axis_off()
    for index, case in enumerate(CASES):
        _draw_card(ax, case, performance, index)
    ax.set_title(
        "b  BioAgents trace excerpts",
        loc="left",
        fontsize=PLOT_TITLE_SIZE,
        pad=11,
    )
    ax.text(
        0.985,
        0.985,
        "Verbatim excerpts; [...] marks an omission",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=7.3,
        color=CARD_MUTED_COLOR,
    )
    # Text cards need a slightly taller-than-wide field; a forced square would
    # either shrink the quoted traces or waste horizontal plate space.
    ax.set_box_aspect(1.06)


def write_tables(performance: pd.DataFrame, counts: dict[str, int]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    featured_rows = []
    anchor_rows = []
    trace_rows = []
    for case in CASES:
        target = str(case["target"])
        actual = int(performance.loc[target, "actual_n_degs"])
        predicted = int(performance.loc[target, "bioagents_predicted_n_degs"])
        featured_rows.append(
            {
                "target_name": target,
                "set": "near_miss" if target == NEAR_MISS_TARGET else "substantial_response",
                "actual_n_degs": actual,
                "bioagents_predicted_n_degs": predicted,
                "fold_error": max(actual, predicted) / min(actual, predicted),
            }
        )
        for source, names in (
            ("trace_used_string", case["string"]),
            ("trace_selected_alternative", case["alternative"]),
        ):
            for name in names:
                anchor_rows.append(
                    {
                        "target_name": target,
                        "anchor_name": name,
                        "anchor_n_degs": counts[name],
                        "anchor_source": source,
                    }
                )
        trace_rows.append(
            {
                "target_name": target,
                "trace_path": str(case["trace"]),
                "quoted_excerpt": str(case["quote"]),
            }
        )
    pd.DataFrame(featured_rows).to_csv(OUT_DIR / "featured_cases.csv", index=False)
    pd.DataFrame(anchor_rows).to_csv(OUT_DIR / "trace_anchors.csv", index=False)
    pd.DataFrame(trace_rows).to_csv(OUT_DIR / "trace_excerpts.csv", index=False)


def main() -> None:
    house_style()
    performance, counts = load_data()
    write_tables(performance, counts)
    concepts = {
        "observed response": ACTUAL_COLOR,
        "BioAgents prediction": BIOAGENTS_COLOR,
        "trace-used STRING neighbor": STRING_COLOR,
        "trace-selected alternative": ALTERNATIVE_COLOR,
        "near-miss separator": NEAR_MISS_COLOR,
    }
    written = plate(
        {"a": _anchor_panel, "b": _card_panel},
        OUT_DIR,
        STEM,
        panel_size=(9.2, 8.7),
        joint_size=(18.4, 9.4),
        gridspec_kw={"width_ratios": (1.0, 1.13), "wspace": 0.20},
        concepts=concepts,
        tight_kw={"pad": 0.8},
    )
    print(f"wrote {len(written)} figure files to {OUT_DIR}")


if __name__ == "__main__":
    main()
