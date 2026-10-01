#!/usr/bin/env python3
"""Render a reduced Task 1 characterization heatmap.

This is a separate variant of ``plot_comparison_tables.py``. It leaves the
existing Task 1 heatmap untouched while removing Pearson, Spearman, the four
confusion-matrix columns, the redundant ``always_zero`` baseline, and the
overlapping accuracy, F1, and MCC summaries. Balanced accuracy, precision, and
recall retain the prevalence-aware summary and its interpretable trade-off. The
single-agent comparator is also omitted so the agent section contains BioAgents
alone.

The table deliberately yields the square-panel convention because its metric
columns and long row labels require a natural rectangular aspect.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from figures.panel_kit import audit, house_style, save

import plot_comparison_tables as source


HERE = Path(__file__).resolve().parent
OUT_DIR = HERE / "task1_characterization_heatmap_v2_20260918"
STEM = "fig_task1_characterization_heatmap_reduced"

METRIC_KEYS = {
    "balanced_accuracy",
    "precision",
    "recall",
    "mse_log1p_all",
    "mse_log1p_true_effect",
}
METRICS = tuple(
    metric for metric in source.TASK1_METRICS if metric.key in METRIC_KEYS
)

PREDICTION_BASELINES = {
    "constant_log_mse",
    "constant_arithmetic_mean",
    "all_cell_types_constant_log_mse",
    "all_cell_types_constant_arithmetic_mean",
    "physical_neighbor_mean_count",
}


def main() -> None:
    house_style()
    rows = [
        row
        for row in source._read_selected(source.TASK1_CSV)
        if (
            row["system"] == "baseline"
            and row["method"] in PREDICTION_BASELINES
        )
        or row["system"] == "bioagents"
    ]
    if len(rows) != 6:
        raise ValueError(f"expected 6 reduced Task 1 rows, found {len(rows)}")
    if len(METRICS) != 5:
        raise ValueError(f"expected 5 reduced Task 1 metrics, found {len(METRICS)}")

    fig, ax = plt.subplots(figsize=(10.8, 6.0))
    source._draw_table(
        ax,
        rows,
        METRICS,
        source.TASK1_LABELS,
        title="Task 1 — DEG-count baselines and BioAgents",
        box_aspect=1.15,
    )
    row_labels = [
        "BioAgents" if row["system"] == "bioagents" else tick.get_text()
        for tick, row in zip(ax.get_yticklabels(), rows, strict=True)
    ]
    ax.set_yticks(ax.get_yticks(), row_labels)
    for tick, row in zip(ax.get_yticklabels(), rows, strict=True):
        tick.set_color(source.ROW_COLORS[source._row_concept(row)])
        if row["system"] != "baseline":
            tick.set_fontweight("bold")
    fig.text(
        0.5,
        0.018,
        "Darker cells are better within each column; arrows give the preferred "
        "direction. MSE uses ln(1 + count).",
        ha="center",
        va="bottom",
        fontsize=7,
        color="#444444",
    )
    audit(fig, verbose=True)
    fig.subplots_adjust(left=0.30, right=0.995, top=0.74, bottom=0.11)
    written = save(fig, OUT_DIR / STEM)
    plt.close(fig)
    print(f"wrote {len(written)} files to {OUT_DIR}")


if __name__ == "__main__":
    main()
