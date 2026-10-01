#!/usr/bin/env python3
"""Render complete baseline versus one-target-run metric tables.

Each cell reports the original comparison-table value. Background darkness is
normalized separately within each metric column, with the direction reversed
for lower-is-better metrics. It is therefore a within-column reading aid, not
a common scale across metrics.
"""

from __future__ import annotations

import csv
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

from figures.panel_kit import audit, house_style, save


HERE = Path(__file__).resolve().parent
TASK1_CSV = HERE / "task1_deg_count_comparison.csv"
TASK2_CSV = HERE / "task2_deg_identity_comparison.csv"
OUT_DIR = HERE / "comparison_table_figures_v1_20260908"

ROW_COLORS = {
    "baseline": "#5e5e5e",
    "single agent": "#6a3d9a",
    "BioAgents": "#00838f",
    "reference ceiling": "#b35c00",
}
QUALITY_CMAP = mcolors.LinearSegmentedColormap.from_list(
    "table_quality",
    ("#ffffff", "#e5f5e0", "#a1d99b", "#238b45"),
)


@dataclass(frozen=True)
class Metric:
    key: str
    label: str
    group: str
    direction: str | None
    formatter: Callable[[float], str]


def _decimal(value: float) -> str:
    return f"{value:.3f}"


def _integer(value: float) -> str:
    return f"{value:,.0f}"


def _percent(value: float) -> str:
    return f"{100 * value:.1f}%"


TASK1_METRICS = (
    Metric("n_targets", "Perturbation\ncount", "N", None, _integer),
    Metric("accuracy", "Accuracy ↑", "Effect classification", "high", _decimal),
    Metric(
        "balanced_accuracy",
        "Balanced\naccuracy ↑",
        "Effect classification",
        "high",
        _decimal,
    ),
    Metric("precision", "Precision ↑", "Effect classification", "high", _decimal),
    Metric("recall", "Recall ↑", "Effect classification", "high", _decimal),
    Metric("f1", "F1 ↑", "Effect classification", "high", _decimal),
    Metric(
        "matthews_correlation",
        "MCC ↑",
        "Effect classification",
        "high",
        _decimal,
    ),
    Metric("pearson_log1p", "Pearson ↑", "Count agreement", "high", _decimal),
    Metric("spearman_log1p", "Spearman ↑", "Count agreement", "high", _decimal),
    Metric("mse_log1p_all", "MSE, all ↓", "Count agreement", "low", _decimal),
    Metric(
        "mse_log1p_true_effect",
        "MSE, true\neffects ↓",
        "Count agreement",
        "low",
        _decimal,
    ),
    Metric("true_negative", "TN ↑", "Confusion matrix", "high", _integer),
    Metric("false_positive", "FP ↓", "Confusion matrix", "low", _integer),
    Metric("false_negative", "FN ↓", "Confusion matrix", "low", _integer),
    Metric("true_positive", "TP ↑", "Confusion matrix", "high", _integer),
)

TASK2_METRICS = (
    Metric("n_targets", "Perturbation\ncount", "N", None, _integer),
    Metric(
        "recall_at_25",
        "Overall\nR@25 ↑",
        "Recall@25",
        "high",
        _percent,
    ),
    Metric(
        "up_recall_at_25",
        "Up ↑",
        "Recall@25",
        "high",
        _percent,
    ),
    Metric(
        "down_recall_at_25",
        "Down ↑",
        "Recall@25",
        "high",
        _percent,
    ),
    Metric(
        "recall_at_500",
        "Overall\nR@500 ↑",
        "Recall@500",
        "high",
        _percent,
    ),
    Metric(
        "up_recall_at_500",
        "Up ↑",
        "Recall@500",
        "high",
        _percent,
    ),
    Metric(
        "down_recall_at_500",
        "Down ↑",
        "Recall@500",
        "high",
        _percent,
    ),
    Metric(
        "pooled_median_actual_rank",
        "Pooled median\ntrue rank ↓",
        "Rank distribution",
        "low",
        _integer,
    ),
    Metric(
        "below_rank_10000_fraction",
        "% below true\nrank 10,000 ↓",
        "Rank distribution",
        "low",
        _percent,
    ),
)

TASK1_LABELS = {
    "always_zero": "Always zero",
    "constant_log_mse": "Thalamic log mean (1)",
    "constant_arithmetic_mean": "Thalamic raw mean (14)",
    "all_cell_types_constant_log_mse": "All-cell log mean (0)",
    "all_cell_types_constant_arithmetic_mean": "All-cell raw mean (2)",
    "physical_neighbor_mean_count": "Physical-neighbor mean (fallback 14)",
    "functional_neighbor_mean_count": (
        "High-confidence functional-neighbor\nmean (fallback 14)"
    ),
    "literature_neighbor_mean_count": (
        "High-confidence text-mining-neighbor\nmean (fallback 14)"
    ),
}

TASK2_LABELS = {
    "oracle_transfer": "Oracle transfer",
    "pseudoreplicate_ceiling": "Cross-animal pseudo-replicate ceiling",
    "uniform_random": "Uniform random",
    "random_strong_profile": "Random strong profile",
    "mean_raw_score_strong": "Raw-score mean, strong",
    "mean_raw_score_global": "Raw-score mean, global",
    "physical_neighbor_mean_raw_score": "Physical-neighbor raw-score mean",
    "functional_neighbor_mean_raw_score": (
        "High-confidence functional-neighbor\nraw-score mean"
    ),
    "literature_neighbor_mean_raw_score": (
        "High-confidence text-mining-neighbor\nraw-score mean"
    ),
    "mean_standardized_score": "Standardized-score mean, strong",
    "top25_frequency": "Top-25 frequency",
    "borda_mean_rank": "Mean rank across training perturbations (Borda)",
    "mean_shift_global_perturbation_balanced": (
        "Additive residual, global (perturbation-balanced)"
    ),
    "mean_shift_global_cell_weighted": (
        "Additive residual, global (cell-weighted)"
    ),
    "mean_shift_strong_perturbation_balanced": (
        "Additive residual, strong (perturbation-balanced)"
    ),
    "mean_shift_strong_cell_weighted": (
        "Additive residual, strong (cell-weighted)"
    ),
    "mean_shift_physical_neighbor_balanced": (
        "Additive residual, physical neighbors"
    ),
    "systema_hvg_global_cell_weighted": (
        "Systema-style global mean (5k HVGs + perturbations)"
    ),
    "pooled_wilcoxon_cell_weighted": (
        "Pooled-cell Wilcoxon (cell-weighted)"
    ),
    "pooled_wilcoxon_perturbation_balanced": (
        "Pooled-cell Wilcoxon (perturbation-balanced)"
    ),
}

REFERENCE_CEILING_METHODS = {
    "oracle_transfer",
    "pseudoreplicate_ceiling",
}


def _read_selected(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return [
        row
        for row in rows
        if row["system"] == "baseline" or row["batch_size"] == "1"
    ]


def _row_label(row: Mapping[str, str], labels: Mapping[str, str]) -> str:
    if row["system"] == "baseline":
        return labels[row["method"]]
    if row["system"] == "for_alex_single_agent":
        return "Single agent, 1 perturbation"
    return "BioAgents, 1 perturbation"


def _row_concept(row: Mapping[str, str]) -> str:
    if row["method"] in REFERENCE_CEILING_METHODS:
        return "reference ceiling"
    if row["system"] == "baseline":
        return "baseline"
    if row["system"] == "for_alex_single_agent":
        return "single agent"
    return "BioAgents"


def _row_section(row: Mapping[str, str]) -> str:
    if row["method"] in REFERENCE_CEILING_METHODS:
        return "reference ceiling"
    if row["system"] == "baseline":
        return "baseline"
    return "agent"


def _values(
    rows: Sequence[Mapping[str, str]], metrics: Sequence[Metric]
) -> np.ndarray:
    values = np.full((len(rows), len(metrics)), np.nan)
    for row_index, row in enumerate(rows):
        for column_index, metric in enumerate(metrics):
            raw = row[metric.key]
            if raw:
                values[row_index, column_index] = float(raw)
    return values


def _quality(values: np.ndarray, metrics: Sequence[Metric]) -> np.ndarray:
    quality = np.full_like(values, np.nan)
    for column_index, metric in enumerate(metrics):
        column = values[:, column_index]
        finite = np.isfinite(column)
        if metric.direction is None or not finite.any():
            continue
        low = np.min(column[finite])
        high = np.max(column[finite])
        if high == low:
            quality[finite, column_index] = 0.25
            continue
        scaled = (column[finite] - low) / (high - low)
        quality[finite, column_index] = (
            scaled if metric.direction == "high" else 1 - scaled
        )
    return quality


def _group_spans(metrics: Sequence[Metric]) -> list[tuple[str, int, int]]:
    spans: list[tuple[str, int, int]] = []
    start = 0
    for index in range(1, len(metrics) + 1):
        if index == len(metrics) or metrics[index].group != metrics[start].group:
            spans.append((metrics[start].group, start, index - 1))
            start = index
    return spans


def _draw_table(
    ax: Axes,
    rows: Sequence[Mapping[str, str]],
    metrics: Sequence[Metric],
    labels: Mapping[str, str],
    *,
    title: str,
    box_aspect: float,
) -> None:
    values = _values(rows, metrics)
    quality = _quality(values, metrics)
    masked = np.ma.masked_invalid(quality)
    cmap = QUALITY_CMAP.copy()
    cmap.set_bad("white")
    ax.imshow(masked, cmap=cmap, vmin=0, vmax=1, aspect="auto", zorder=0)

    row_labels = [_row_label(row, labels) for row in rows]
    ax.set_yticks(np.arange(len(rows)), row_labels)
    ax.set_xticks(np.arange(len(metrics)), [metric.label for metric in metrics])
    ax.tick_params(
        axis="x",
        top=True,
        bottom=False,
        labeltop=True,
        labelbottom=False,
        length=0,
        pad=8,
    )
    ax.tick_params(axis="y", length=0, pad=8)
    for tick, row in zip(ax.get_yticklabels(), rows, strict=True):
        tick.set_color(ROW_COLORS[_row_concept(row)])
        if row["system"] != "baseline":
            tick.set_fontweight("bold")

    for row_index in range(len(rows)):
        for column_index, metric in enumerate(metrics):
            value = values[row_index, column_index]
            label = "—" if not np.isfinite(value) else metric.formatter(value)
            cell_quality = quality[row_index, column_index]
            dark = np.isfinite(cell_quality) and cell_quality > 0.72
            best = np.isfinite(cell_quality) and np.isclose(cell_quality, 1.0)
            ax.text(
                column_index,
                row_index,
                label,
                ha="center",
                va="center",
                color="white" if dark else "#222222",
                fontweight="bold" if best else "normal",
                fontsize=6.6,
                zorder=2,
            )

    ax.set_xticks(np.arange(-0.5, len(metrics), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(rows), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=1.0)
    ax.tick_params(which="minor", bottom=False, left=False)

    for group, start, end in _group_spans(metrics):
        center = (start + end) / 2
        if group != "N":
            ax.text(
                center,
                1.10,
                group,
                transform=ax.get_xaxis_transform(),
                ha="center",
                va="bottom",
                fontweight="bold",
                fontsize=8,
                color="#333333",
                clip_on=False,
            )
        if end < len(metrics) - 1:
            ax.axvline(end + 0.5, color="#777777", linewidth=0.8, zorder=3)

    for row_index in range(len(rows) - 1):
        if _row_section(rows[row_index]) != _row_section(rows[row_index + 1]):
            ax.axhline(row_index + 0.5, color="#555555", linewidth=1.2, zorder=3)
    ax.set_xlim(-0.5, len(metrics) - 0.5)
    ax.set_ylim(len(rows) - 0.5, -0.5)
    ax.set_title(title, loc="left", pad=96)
    # Tables use their natural rectangular aspect so all cells remain legible.
    ax.set_box_aspect(box_aspect)
    for spine in ax.spines.values():
        spine.set_visible(False)


def _render_task1() -> list[Path]:
    rows = _read_selected(TASK1_CSV)
    if len(rows) != 10:
        raise ValueError(f"expected 10 Task 1 rows, found {len(rows)}")
    fig, ax = plt.subplots(figsize=(19.5, 7.5))
    _draw_table(
        ax,
        rows,
        TASK1_METRICS,
        TASK1_LABELS,
        title="Task 1 — DEG-count baselines and one-perturbation agent runs",
        box_aspect=0.60,
    )
    fig.text(
        0.5,
        0.015,
        "Darker cells are better within each column; arrows give the preferred direction. "
        "MSE and correlations use ln(1 + count). — indicates an undefined correlation.",
        ha="center",
        va="bottom",
        fontsize=7,
        color="#444444",
    )
    audit(fig, verbose=True)
    fig.subplots_adjust(left=0.16, right=0.995, top=0.76, bottom=0.10)
    written = save(fig, OUT_DIR / "fig_task1_metric_table")
    plt.close(fig)
    return written


def _render_task2() -> list[Path]:
    excluded_methods = {
        "mean_shift_global_perturbation_balanced",
        "mean_shift_global_cell_weighted",
        "mean_shift_strong_perturbation_balanced",
        "mean_shift_strong_cell_weighted",
        "mean_shift_physical_neighbor_balanced",
        "systema_hvg_global_cell_weighted",
    }
    selected_rows = [
        row
        for row in _read_selected(TASK2_CSV)
        if row["method"] not in excluded_methods
    ]
    rows = (
        [
            row
            for row in selected_rows
            if row["system"] == "baseline"
            and row["method"] not in REFERENCE_CEILING_METHODS
        ]
        + [row for row in selected_rows if row["system"] != "baseline"]
        + [
            row
            for row in selected_rows
            if row["method"] in REFERENCE_CEILING_METHODS
        ]
    )
    if len(rows) != 16:
        raise ValueError(f"expected 16 Task 2 rows, found {len(rows)}")
    fig, ax = plt.subplots(figsize=(16.0, 11.2))
    _draw_table(
        ax,
        rows,
        TASK2_METRICS,
        TASK2_LABELS,
        title=(
            "Task 2 — DEG-identity baselines, one-perturbation agent runs, "
            "and reference ceilings"
        ),
        box_aspect=1.18,
    )
    fig.text(
        0.5,
        0.018,
        "Darker cells are better within each column. Overall recall pools the 25 up and "
        "25 down genes; Recall@500 is the fraction of submitted genes with true rank ≤500. "
        "Rank-distribution metrics also pool both arms.\n"
        "Neighbor baselines use the global raw-score mean when no qualifying "
        "training neighbor exists. "
        "The bottom two rows are reference ceilings, not prediction-time baselines: "
        "pseudo-replicates are disjoint 37-animal halves scored against each other, and "
        "oracle transfer uses a post-hoc, truth-optimized training donor.",
        ha="center",
        va="bottom",
        fontsize=7,
        color="#444444",
    )
    audit(fig, verbose=True)
    fig.subplots_adjust(left=0.28, right=0.99, top=0.80, bottom=0.08)
    written = save(fig, OUT_DIR / "fig_task2_metric_table")
    plt.close(fig)
    return written


def main() -> None:
    house_style()
    written = _render_task1() + _render_task2()
    print(f"wrote {len(written)} files to {OUT_DIR}")


if __name__ == "__main__":
    main()
