#!/usr/bin/env python
"""Vertical three-arm composition of reviewer-normalized finding scopes.

The source ``finding_type`` column is intentionally not plotted: unshuffled
reports use the legacy narrative vocabulary, whereas the two shuffle arms use
the V4 ``claim_kind`` vocabulary.  ``claim_scope`` is assigned by the same
blinded grader across all three arms and is therefore the comparable axis.

This is a companion to ``plot_three_arm_panel.py`` and deliberately keeps its
tall, narrow geometry rather than forcing a square plotting box.  The exception
is useful here because the panel is intended for the same Figure 2 column slot.
The 0--100% axis also deliberately meets the bars at zero because contact with
the baseline is meaningful for stacked shares.

Reads ``final_classified_findings.csv`` and writes:

* ``final_finding_scope_distribution.csv``;
* ``fig_three_arm_finding_scope_vertical_primary.{png,svg,pdf}``; and
* ``fig_three_arm_finding_scope_vertical_sensitivity.{png,svg,pdf}``.

Run from anywhere:

    python manuscript/fig2/d/plot_three_arm_finding_scope.py
"""

from __future__ import annotations

import csv
import os
import sys
from collections import Counter
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
STYLE = ROOT / "src/figures/style.mplstyle"
CLASSIFIED_FINDINGS = HERE / "final_classified_findings.csv"
SUMMARY_CSV = HERE / "final_finding_scope_distribution.csv"

ARMS = (
    "Unshuffled",
    "Within-screen shuffled",
    "Out-of-screen shuffled",
)
ARM_DISPLAY = {
    "Unshuffled": "Unshuffled",
    "Within-screen shuffled": "Within-screen",
    "Out-of-screen shuffled": "Out-of-screen",
}

SCOPES = (
    "program_response",
    "comparator_relationship",
    "expected_program_test",
    "cell_group_relationship",
    "mixed",
)
SCOPE_LABELS = {
    "program_response": "Pathway or state change",
    "comparator_relationship": "Perturbation convergence/divergence",
    "expected_program_test": "Prior-prediction outcome",
    "cell_group_relationship": "Cell-group-dependent response",
    "mixed": "Other",
}
LEGEND_LABELS = {
    "program_response": "Pathway or state\nchange",
    "comparator_relationship": "Perturbation convergence/\ndivergence",
    "expected_program_test": "Prior-prediction\noutcome",
    "cell_group_relationship": "Cell-group-dependent\nresponse",
    "mixed": "Other",
}

# Finding-scope concepts deliberately avoid the repository-reserved literature-
# flag colors.  These are five distinct colors from established qualitative,
# color-vision-conscious palettes; keep this mapping centralized for reruns.
COLORS = {
    "program_response": "#0072B2",
    "comparator_relationship": "#56B4E9",
    "expected_program_test": "#CC79A7",
    "cell_group_relationship": "#F0E442",
    "mixed": "#332288",
}
LABEL_INK = {
    "program_response": "#ffffff",
    "comparator_relationship": "#1f2b33",
    "expected_program_test": "#ffffff",
    "cell_group_relationship": "#29270f",
    "mixed": "#ffffff",
}

SURFACE = "#ffffff"
INK = "#000000"
INK_MUTED = "#555555"

# Match the established vertical literature-flag panel.
FIG_W = 2.65
FIG_H = 2.65
BAR_WIDTH = 0.56
BAR_STEP = 1.40
INSIDE_MIN = 7.5
OUTSIDE_MIN_GAP = 7.5
OUTSIDE_LOW = 3.0
OUTSIDE_HIGH = 94.0

FS_VALUE = 5.8
FS_SMALL_VALUE = 6.0
FS_ARM = 7.0
FS_N = 6.0
FS_LEGEND = 6.2

LAYERS = {
    "primary": "valid_for_primary",
    "sensitivity": "valid_for_sensitivity",
}
SUBTITLES = {
    "primary": "Biological inferences",
    "sensitivity": "Biological inferences + evidence-only",
}


def parse_bool(value: str) -> bool:
    return value.strip().casefold() == "true"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def summarize(
    rows: list[dict[str, str]],
) -> list[dict[str, str | int | float]]:
    observed_scopes = {row["claim_scope"] for row in rows if row["claim_scope"]}
    unexpected = observed_scopes - set(SCOPES)
    if unexpected:
        raise ValueError(f"unexpected claim_scope values: {sorted(unexpected)}")

    summary: list[dict[str, str | int | float]] = []
    for layer, gate in LAYERS.items():
        for arm in ARMS:
            selected = [
                row for row in rows if row["arm"] == arm and parse_bool(row[gate])
            ]
            counts = Counter(row["claim_scope"] for row in selected)
            n_findings = len(selected)
            if not n_findings:
                raise ValueError(f"{layer}: no retained findings for {arm}")
            if sum(counts.values()) != n_findings:
                raise ValueError(f"{layer}: blank claim_scope among retained {arm} rows")
            for scope in SCOPES:
                count = counts[scope]
                summary.append(
                    {
                        "analysis_layer": layer,
                        "arm": arm,
                        "scope": scope,
                        "scope_label": SCOPE_LABELS[scope],
                        "count": count,
                        "percent": 100.0 * count / n_findings,
                        "n_findings": n_findings,
                    }
                )
    return summary


def write_summary(rows: list[dict[str, str | int | float]], path: Path) -> None:
    fieldnames = [
        "analysis_layer",
        "arm",
        "scope",
        "scope_label",
        "count",
        "percent",
        "n_findings",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({**row, "percent": f"{float(row['percent']):.3f}"})


def setup_matplotlib() -> Any:
    os.environ.setdefault("MPLCONFIGDIR", "/tmp/mplconfig_fig2_finding_scope")
    Path(os.environ["MPLCONFIGDIR"]).mkdir(parents=True, exist_ok=True)
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    if STYLE.is_file():
        plt.style.use(STYLE)
    plt.rcParams.update({"svg.fonttype": "none", "pdf.fonttype": 42})
    return plt


def spread_outside_labels(centres: list[float]) -> list[float]:
    """Spread thin-slice labels while keeping them below the per-bar n label."""
    if not centres:
        return []
    placed = sorted(centres)
    for idx in range(1, len(placed)):
        placed[idx] = max(placed[idx], placed[idx - 1] + OUTSIDE_MIN_GAP)
    if placed[-1] > OUTSIDE_HIGH:
        shift = placed[-1] - OUTSIDE_HIGH
        placed = [value - shift for value in placed]
    if placed[0] < OUTSIDE_LOW:
        shift = OUTSIDE_LOW - placed[0]
        placed = [value + shift for value in placed]
    return placed


def plot_layer(
    summary: list[dict[str, str | int | float]], layer: str
) -> Path:
    plt = setup_matplotlib()
    from matplotlib.patches import Patch

    lookup = {
        (str(row["arm"]), str(row["scope"])): row
        for row in summary
        if row["analysis_layer"] == layer
    }
    missing = [(arm, scope) for arm in ARMS for scope in SCOPES if (arm, scope) not in lookup]
    if missing:
        raise ValueError(f"{layer}: missing arm/scope rows {missing}")

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    x_positions = [index * BAR_STEP for index in range(len(ARMS))]
    half = BAR_WIDTH / 2

    for x, arm in zip(x_positions, ARMS):
        bottom = 0.0
        outside: list[tuple[float, float]] = []
        for scope in SCOPES:
            height = float(lookup[(arm, scope)]["percent"])
            ax.bar(
                x,
                height,
                bottom=bottom,
                width=BAR_WIDTH,
                color=COLORS[scope],
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
                    color=LABEL_INK[scope],
                    zorder=4,
                )
            elif height >= 0.05:
                outside.append((centre, height))
            bottom += height

        label_positions = spread_outside_labels([centre for centre, _ in outside])
        for (centre, height), label_y in zip(sorted(outside), label_positions):
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

        n_findings = int(lookup[(arm, SCOPES[0])]["n_findings"])
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
        [ARM_DISPLAY[arm] for arm in ARMS],
        rotation=45,
        ha="right",
        rotation_mode="anchor",
        fontsize=FS_ARM,
        color=INK,
    )
    ax.set_xlim(-0.55, x_positions[-1] + 0.95)
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_ylabel("Percent of findings", fontsize=FS_ARM)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(axis="x", length=0)
    ax.tick_params(axis="y", labelsize=FS_ARM)

    handles = [
        Patch(facecolor=COLORS[scope], label=LEGEND_LABELS[scope])
        for scope in SCOPES
    ]
    ax.legend(
        handles=handles,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.40),
        ncol=2,
        frameon=False,
        fontsize=FS_LEGEND,
        handlelength=1.1,
        handleheight=0.9,
        handletextpad=0.5,
        labelspacing=0.35,
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

    # Run the house audit. Its expected non-square warning is documented in this
    # module's docstring: matching the adjacent vertical panel is the more
    # legible geometry here. The high-spine warning is also expected and does
    # not identify a data clash: audit sees the leader-line endpoint anchored to
    # each tiny top slice as a mark. Expanding the y range would misstate the
    # bounded 0--100% share scale, so that rule yields as well.
    sys.path.insert(0, str(ROOT / "src"))
    from figures.panel_kit import audit

    audit(fig, concepts={SCOPE_LABELS[scope]: COLORS[scope] for scope in SCOPES})

    stem = HERE / f"fig_three_arm_finding_scope_vertical_{layer}"
    fig.savefig(stem.with_suffix(".png"), dpi=600, bbox_inches="tight")
    fig.savefig(stem.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)
    return stem


def main() -> None:
    rows = read_rows(CLASSIFIED_FINDINGS)
    summary = summarize(rows)
    write_summary(summary, SUMMARY_CSV)
    print(f"wrote {SUMMARY_CSV.name}")

    for layer in LAYERS:
        stem = plot_layer(summary, layer)
        print(f"{layer}: {stem.name}.{{png,svg,pdf}}")
        lookup = {
            (str(row["arm"]), str(row["scope"])): row
            for row in summary
            if row["analysis_layer"] == layer
        }
        for arm in ARMS:
            parts = " ".join(
                f"{SCOPE_LABELS[scope]} {float(lookup[(arm, scope)]['percent']):.1f}%"
                for scope in SCOPES
            )
            n_findings = int(lookup[(arm, SCOPES[0])]["n_findings"])
            print(f"  {arm:<24} n={n_findings:>5,}  {parts}")


if __name__ == "__main__":
    main()
