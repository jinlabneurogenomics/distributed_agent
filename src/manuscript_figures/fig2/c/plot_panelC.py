#!/usr/bin/env python3
"""Recreate Figure 2C with the full June source-access audit.

The visual structure is the selected design B from ../plot_panelC_options.py.
Only the corpus-dependent quantities change: 2,046 June reports replace the
2,045-report July corpus, and the old 300-trace search proxy is replaced by the
audited per-report counts of distinct sources accessed and cited.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
STYLE = REPO / "src" / "figures" / "style.mplstyle"
RUNTIME_INPUT = (
    REPO / "debug" / "260730_prompt_v4_live_eval" / "analysis" / "per_report.csv"
)
FRAMEWORK_INPUT = HERE.parent / "framework_human_scale_summary.json"
SOURCE_SUMMARY_INPUT = HERE / "source_access_summary.json"
SOURCE_PER_REPORT_INPUT = HERE / "source_access_per_report.csv"

PANEL_W, PANEL_H = 2.1, 2.3
HUMAN_MIN_PER_PERTURBATION = 15.0
HUMAN_MIN_PER_SOURCE = 10.0
HUMAN_HOURLY_USD = 25.0

COLORS = {
    "surface": "#ffffff",
    "ink": "#0b0b0b",
    "ink2": "#52514e",
    "muted": "#898781",
    "grid": "#e6e5de",
    "axis": "#b9b8ae",
    "agent": "#256abf",
    "human": "#eb6834",
    "cited": "#b5407f",
}

HOUR_TICKS = [
    (1, "1 h"),
    (24, "1 day"),
    (168, "1 wk"),
    (730, "1 mo"),
    (8766, "1 yr"),
]
FS_TITLE, FS_BAND, FS_ROW, FS_VAL, FS_TICK, FS_NOTE = 6.6, 5.6, 5.0, 5.4, 5.0, 4.4


def load_style() -> None:
    if STYLE.exists():
        plt.style.use(STYLE)
    mpl.rcParams.update(
        {
            "figure.facecolor": COLORS["surface"],
            "axes.facecolor": COLORS["surface"],
            "savefig.facecolor": COLORS["surface"],
            "axes.edgecolor": COLORS["axis"],
            "axes.labelcolor": COLORS["ink"],
            "xtick.color": COLORS["axis"],
            "ytick.color": COLORS["axis"],
            "xtick.labelcolor": COLORS["ink2"],
            "ytick.labelcolor": COLORS["ink2"],
            "xtick.major.size": 2.0,
            "ytick.major.size": 0.0,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "text.parse_math": False,
        }
    )


def duration(hours: float) -> str:
    if hours < 1:
        return f"{hours * 60:.0f} min"
    if hours < 36:
        return f"{hours:.0f} h"
    if hours < 168 * 6:
        return f"{hours / 168:.1f} wk"
    if hours < 8766:
        return f"{hours / 730:.1f} mo"
    return f"{hours / 8766:.1f} yr"


def money(usd: float) -> str:
    return f"${usd / 1000:.1f}k" if usd < 10_000 else f"${usd / 1000:.0f}k"


def load_numbers() -> dict:
    source_summary = json.loads(SOURCE_SUMMARY_INPUT.read_text())
    framework = json.loads(FRAMEWORK_INPUT.read_text())
    per_report = pd.read_csv(SOURCE_PER_REPORT_INPUT)
    runtimes_min = pd.read_csv(RUNTIME_INPUT)["latency_seconds"] / 60.0

    n = len(per_report)
    accessed = per_report["accessed_sources"].astype(float)
    cited = per_report["cited_sources"].astype(float)
    citation_entries = per_report["citation_entries"].astype(float)

    expected = {
        "n": 2046,
        "accessed": int(source_summary["accessed_report_source_pairs"]),
        "cited": int(source_summary["cited_report_source_pairs"]),
        "citation_entries": int(source_summary["citation_entries_raw"]),
    }
    observed = {
        "n": n,
        "accessed": int(accessed.sum()),
        "cited": int(cited.sum()),
        "citation_entries": int(citation_entries.sum()),
    }
    if observed != expected:
        raise RuntimeError(f"panel inputs drifted: {observed=} {expected=}")

    agent_unit_min = float(runtimes_min.median())
    agent_unit_cost = float(
        framework["agent_scale1_proxy"]["estimated_list_cost_usd_mean"]
    )
    cited_unit_min = HUMAN_MIN_PER_PERTURBATION + HUMAN_MIN_PER_SOURCE * cited.mean()
    accessed_unit_min = (
        HUMAN_MIN_PER_PERTURBATION + HUMAN_MIN_PER_SOURCE * accessed.mean()
    )

    data = {
        "n": n,
        "accessed_raw": accessed.to_numpy(),
        "cited_raw": cited.to_numpy(),
        "accessed_total": int(accessed.sum()),
        "cited_total": int(cited.sum()),
        "citation_entries_total": int(citation_entries.sum()),
        "accessed_mean": float(accessed.mean()),
        "accessed_median": float(accessed.median()),
        "cited_mean": float(cited.mean()),
        "cited_median": float(cited.median()),
        "agent_unit_min": agent_unit_min,
        "agent_min_iqr": [
            float(runtimes_min.quantile(0.25)),
            float(runtimes_min.quantile(0.75)),
        ],
        "agent_min_range": [float(runtimes_min.min()), float(runtimes_min.max())],
        "agent_runtime_n": len(runtimes_min),
        "agent_unit_cost": agent_unit_cost,
        "agent_parallel_hours": agent_unit_min / 60.0,
        "agent_serial_hours": n * agent_unit_min / 60.0,
        "agent_total_cost": n * agent_unit_cost,
        "analyst_base_hours": n * HUMAN_MIN_PER_PERTURBATION / 60.0,
        "analyst_cited_hours": n * cited_unit_min / 60.0,
        "analyst_accessed_hours": n * accessed_unit_min / 60.0,
    }
    data["analyst_base_cost"] = data["analyst_base_hours"] * HUMAN_HOURLY_USD
    data["analyst_cited_cost"] = data["analyst_cited_hours"] * HUMAN_HOURLY_USD
    data["analyst_accessed_cost"] = (
        data["analyst_accessed_hours"] * HUMAN_HOURLY_USD
    )
    return data


def bare_density_axis(ax: plt.Axes) -> None:
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_linewidth(0.4)
    ax.spines["bottom"].set_color(COLORS["axis"])
    ax.tick_params(axis="x", length=1.8, width=0.4, pad=1.5, labelsize=FS_TICK)
    ax.tick_params(axis="y", length=0)


def source_density(ax: plt.Axes, data: dict) -> None:
    grid = np.linspace(0, 60, 400)
    series = [
        (data["cited_raw"], "sources cited", COLORS["cited"]),
        (data["accessed_raw"], "sources accessed", COLORS["agent"]),
    ]
    peaks = []
    for raw, label, color in series:
        density = gaussian_kde(raw)(grid)
        density /= density.max()
        keep = density > 0.004
        x, y = grid[keep], density[keep]
        ax.fill_between(x, 0, y, color=color, alpha=0.16, lw=0, zorder=3)
        ax.plot(x, y, color=color, lw=0.9, zorder=4)
        mean = float(np.mean(raw))
        ax.plot(
            [mean, mean],
            [0, np.interp(mean, grid, density)],
            color=color,
            lw=0.7,
            zorder=5,
        )
        peaks.append((grid[density.argmax()], mean, label, color))

    for index, (peak, mean, label, color) in enumerate(peaks):
        ax.annotate(
            f"{mean:.1f}",
            xy=(peak, 1.04),
            fontsize=FS_VAL,
            fontweight="bold",
            color=color,
            ha="center",
            va="bottom",
        )
        ax.annotate(
            label,
            xy=(1 if index == 0 else 59, 1.42),
            fontsize=FS_NOTE,
            color=color,
            ha="left" if index == 0 else "right",
            va="bottom",
        )

    ax.set_xlim(0, 60)
    ax.set_ylim(0, 1.95)
    ax.set_yticks([])
    ax.set_xticks([0, 10, 20, 30, 40, 50, 60])
    ax.set_xticklabels(["0", "10", "20", "30", "40", "50", "60"])
    ax.set_xlabel(
        f"distinct sources per report, n={data['n']:,}",
        fontsize=FS_NOTE,
        color=COLORS["ink2"],
        labelpad=1,
    )
    bare_density_axis(ax)


def draw_sources_panel(data: dict) -> plt.Figure:
    """Square standalone form of the source-density band.

    The combined panel needs a wide horizontal strip above the cost/time plane.
    Alone, the same comparison reads more clearly as a vertical distribution:
    count runs down the shared axis and density extends right, leaving room for
    direct labels and corpus totals without shrinking the type.
    """
    fig = plt.figure(figsize=(3.0, 3.0))
    ax = fig.add_axes([0.27, 0.20, 0.68, 0.56])

    fig.text(
        0.055,
        0.91,
        "c",
        fontsize=15,
        fontweight="bold",
        color=COLORS["ink"],
        ha="left",
        va="top",
    )
    fig.text(
        0.60,
        0.93,
        "Agent source-use\ndistribution",
        fontsize=12,
        color=COLORS["ink"],
        ha="center",
        va="top",
        linespacing=1.08,
    )

    grid = np.linspace(0, 60, 400)
    series = [
        (data["cited_raw"], "sources cited", COLORS["cited"]),
        (data["accessed_raw"], "sources accessed", COLORS["agent"]),
    ]
    for raw, label, color in series:
        density = gaussian_kde(raw)(grid)
        density /= density.max()
        width = density * 0.29
        keep = density > 0.004
        y, x = grid[keep], width[keep]
        ax.fill_betweenx(y, 0, x, color=color, alpha=0.16, lw=0, zorder=2)
        ax.plot(x, y, color=color, lw=1.25, zorder=3)
        mean = float(np.mean(raw))
        mean_width = float(np.interp(mean, grid, width))
        ax.plot([0, mean_width], [mean, mean], color=color, lw=1.0, zorder=4)
        ax.text(
            0.33,
            mean,
            f"{mean:.1f} {label.removeprefix('sources ')}\n(mean per report)",
            fontsize=8.4,
            color=color,
            ha="left",
            va="center",
            linespacing=1.15,
        )

    ax.set_xlim(0, 1.06)
    ax.set_ylim(60, 0)
    ax.set_xticks([])
    ax.set_yticks([0, 10, 20, 30, 40, 50, 60])
    ax.set_ylabel("distinct sources per report", fontsize=8.5, color=COLORS["ink2"])
    for side in ("top", "right", "bottom"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_linewidth(0.55)
    ax.spines["left"].set_color(COLORS["axis"])
    ax.tick_params(
        axis="y",
        length=2.4,
        width=0.5,
        pad=2,
        labelsize=7.5,
        colors=COLORS["ink2"],
    )

    fig.text(
        0.39,
        0.145,
        f"across {data['n']:,} reports:",
        fontsize=8.2,
        color=COLORS["muted"],
        ha="left",
        va="center",
    )
    fig.text(
        0.39,
        0.098,
        f"{data['cited_total']:,} sources cited",
        fontsize=8.6,
        color=COLORS["cited"],
        ha="left",
        va="center",
    )
    fig.text(
        0.39,
        0.052,
        f"{data['accessed_total']:,} sources accessed",
        fontsize=8.6,
        color=COLORS["agent"],
        ha="left",
        va="center",
    )
    return fig


def draw_panel(data: dict) -> plt.Figure:
    fig = plt.figure(figsize=(PANEL_W, PANEL_H))
    fw, fh = fig.get_size_inches()
    box = lambda x, y, w, h: fig.add_axes([x / fw, y / fh, w / fw, h / fh])  # noqa: E731

    fig.text(
        0,
        (PANEL_H - 0.04) / fh,
        "One agent per target",
        fontsize=FS_TITLE,
        fontweight="bold",
        color=COLORS["ink"],
        ha="left",
        va="top",
    )
    fig.text(
        0,
        (PANEL_H - 0.17) / fh,
        f"all {data['n']:,} at once costs what running them one at a time costs",
        fontsize=FS_NOTE,
        color=COLORS["ink2"],
        ha="left",
        va="top",
    )

    fig.text(
        0,
        (PANEL_H - 0.36) / fh,
        "sources",
        fontsize=FS_BAND,
        fontweight="bold",
        color=COLORS["ink"],
        ha="left",
        va="center",
    )
    fig.text(
        1,
        (PANEL_H - 0.36) / fh,
        (
            f"{data['accessed_total'] / 1000:.1f}k accessed, "
            f"{data['citation_entries_total'] / 1000:.1f}k citation entries"
        ),
        fontsize=FS_NOTE,
        color=COLORS["muted"],
        ha="right",
        va="center",
    )
    source_density(box(0.10, 1.52, 1.90, 0.34), data)

    fig.text(
        0,
        1.30 / fh,
        f"all {data['n']:,}",
        fontsize=FS_BAND,
        fontweight="bold",
        color=COLORS["ink"],
        ha="left",
        va="center",
    )
    ax = box(0.40, 0.42, 1.44, 0.82)

    analyst_hours = [
        data["analyst_base_hours"],
        data["analyst_cited_hours"],
        data["analyst_accessed_hours"],
    ]
    analyst_cost_thousands = [
        data["analyst_base_cost"] / 1000,
        data["analyst_cited_cost"] / 1000,
        data["analyst_accessed_cost"] / 1000,
    ]
    ax.plot(
        analyst_cost_thousands,
        analyst_hours,
        color=COLORS["human"],
        lw=0.8,
        alpha=0.5,
        zorder=2,
    )
    ax.scatter(
        analyst_cost_thousands,
        analyst_hours,
        s=15,
        color=COLORS["human"],
        lw=0.5,
        edgecolor=COLORS["surface"],
        zorder=4,
    )
    analyst_labels = [
        "15 min each",
        f"+ {data['cited_mean']:.1f} cited sources",
        f"+ {data['accessed_mean']:.1f} accessed sources",
    ]
    for index, (cost, hours, label) in enumerate(
        zip(analyst_cost_thousands, analyst_hours, analyst_labels)
    ):
        ax.annotate(
            label,
            xy=(cost, hours),
            xytext=((-3.0 if index == 2 else 3.0), -4.5),
            textcoords="offset points",
            fontsize=FS_NOTE,
            color=COLORS["human"],
            ha="right" if index == 2 else "left",
            va="top",
        )
    ax.annotate(
        "one analyst",
        xy=(analyst_cost_thousands[-1], analyst_hours[-1]),
        xytext=(-1, 5),
        textcoords="offset points",
        fontsize=FS_ROW,
        fontweight="bold",
        color=COLORS["human"],
        ha="right",
        va="bottom",
    )

    agent_cost_thousands = data["agent_total_cost"] / 1000
    ax.annotate(
        "",
        xy=(agent_cost_thousands, data["agent_parallel_hours"] * 1.22),
        xytext=(agent_cost_thousands, data["agent_serial_hours"]),
        arrowprops={
            "arrowstyle": "-|>",
            "color": COLORS["agent"],
            "lw": 1.3,
            "mutation_scale": 5.5,
            "shrinkA": 0,
            "shrinkB": 0,
        },
    )
    ax.scatter(
        [agent_cost_thousands] * 2,
        [data["agent_serial_hours"], data["agent_parallel_hours"]],
        s=15,
        color=COLORS["agent"],
        lw=0.5,
        edgecolor=COLORS["surface"],
        zorder=5,
    )
    ax.annotate(
        f"one at a time,\n{duration(data['agent_serial_hours'])}",
        xy=(agent_cost_thousands, data["agent_serial_hours"]),
        xytext=(2, 3),
        textcoords="offset points",
        fontsize=FS_NOTE,
        color=COLORS["agent"],
        ha="left",
        va="bottom",
        linespacing=1.3,
    )
    ax.annotate(
        f"{data['n']:,} agents at once, {duration(data['agent_parallel_hours'])}",
        xy=(agent_cost_thousands, data["agent_parallel_hours"]),
        xytext=(4, 0),
        textcoords="offset points",
        fontsize=FS_ROW,
        fontweight="bold",
        color=COLORS["agent"],
        ha="left",
        va="center",
    )
    ax.annotate(
        f"÷ {data['n']:,}",
        xy=(
            agent_cost_thousands,
            np.sqrt(data["agent_serial_hours"] * data["agent_parallel_hours"]),
        ),
        xytext=(4, 0),
        textcoords="offset points",
        fontsize=FS_NOTE,
        color=COLORS["agent"],
        ha="left",
        va="center",
    )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(2.6, 240)
    ax.set_ylim(0.20, 4.5e4)
    ax.set_xticks([3, 10, 30, 100, 200])
    ax.set_xticklabels(["$3k", "$10k", "$30k", "$100k", "$200k"])
    ax.xaxis.set_minor_locator(mpl.ticker.NullLocator())
    ax.set_yticks([tick for tick, _ in HOUR_TICKS])
    ax.set_yticklabels([label for _, label in HOUR_TICKS])
    ax.yaxis.set_minor_locator(mpl.ticker.NullLocator())
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_linewidth(0.4)
        ax.spines[side].set_color(COLORS["axis"])
    ax.tick_params(length=1.8, width=0.4, pad=1.5, labelsize=FS_TICK)
    ax.grid(color=COLORS["grid"], lw=0.35, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlabel(
        f"cost, all {data['n']:,}",
        fontsize=FS_NOTE + 0.4,
        color=COLORS["ink2"],
        labelpad=1,
    )
    ax.set_ylabel(
        f"wall clock, all {data['n']:,}",
        fontsize=FS_NOTE + 0.4,
        color=COLORS["ink2"],
        labelpad=1,
    )

    fig.text(
        0,
        0.11 / fh,
        (
            f"agent: {data['agent_unit_min']:.0f} min/target measured over "
            f"{data['agent_runtime_n']} single-target runs; "
            f"${data['agent_unit_cost']:.2f}/target estimated"
        ),
        fontsize=FS_NOTE - 0.2,
        color=COLORS["muted"],
        ha="left",
        va="bottom",
    )
    fig.text(
        0,
        0.03 / fh,
        "analyst: 15 min/perturbation + 10 min per distinct source read, $25/h",
        fontsize=FS_NOTE - 0.2,
        color=COLORS["muted"],
        ha="left",
        va="bottom",
    )
    return fig


def draw_cost_time_panel(data: dict) -> plt.Figure:
    """Wide standalone cost-by-time panel matching the original crop.

    The x limit ends just beyond the largest analyst estimate ($176k) rather
    than carrying the legacy scale to $1.1m. This gives the $100k-to-$176k
    interval enough physical width and avoids an unsupported $300k tick.
    """
    # Match the supplied original crop exactly: 974 × 534 px at 200 dpi.
    fig = plt.figure(figsize=(4.87, 2.67))
    ax = fig.add_axes([0.19, 0.20, 0.61, 0.77])

    analyst_hours = [
        data["analyst_base_hours"],
        data["analyst_cited_hours"],
        data["analyst_accessed_hours"],
    ]
    analyst_cost_thousands = [
        data["analyst_base_cost"] / 1000,
        data["analyst_cited_cost"] / 1000,
        data["analyst_accessed_cost"] / 1000,
    ]
    ax.plot(
        analyst_cost_thousands,
        analyst_hours,
        color=COLORS["human"],
        lw=1.45,
        alpha=0.55,
        zorder=2,
    )
    ax.scatter(
        analyst_cost_thousands,
        analyst_hours,
        s=48,
        color=COLORS["human"],
        lw=0.8,
        edgecolor=COLORS["surface"],
        clip_on=False,
        zorder=4,
    )

    fig.text(
        0.27,
        0.84,
        "human analyst",
        fontsize=10.5,
        fontweight="bold",
        color=COLORS["human"],
        ha="left",
        va="top",
    )
    ax.annotate(
        "analysis only",
        xy=(analyst_cost_thousands[0], analyst_hours[0]),
        xytext=(-2, -10),
        textcoords="offset points",
        fontsize=8.7,
        color=COLORS["human"],
        ha="center",
        va="top",
    )
    ax.annotate(
        f"+ {data['cited_mean']:.1f} cited/report",
        xy=(analyst_cost_thousands[1], analyst_hours[1]),
        xytext=(5, -7),
        textcoords="offset points",
        fontsize=8.7,
        color=COLORS["human"],
        ha="left",
        va="top",
        linespacing=1.25,
    )
    ax.annotate(
        f"+ {data['accessed_mean']:.1f} retrieved\n/ report",
        xy=(analyst_cost_thousands[2], analyst_hours[2]),
        xytext=(5, 0),
        textcoords="offset points",
        fontsize=8.7,
        color=COLORS["human"],
        ha="left",
        va="center",
        linespacing=1.25,
    )

    agent_cost_thousands = data["agent_total_cost"] / 1000
    ax.scatter(
        [agent_cost_thousands],
        [data["agent_parallel_hours"]],
        s=48,
        color=COLORS["agent"],
        lw=0.8,
        edgecolor=COLORS["surface"],
        clip_on=False,
        zorder=5,
    )
    ax.annotate(
        f"{data['n']:,} agents parallel, {duration(data['agent_parallel_hours'])}",
        xy=(agent_cost_thousands, data["agent_parallel_hours"]),
        xytext=(6, 0),
        textcoords="offset points",
        fontsize=10.2,
        fontweight="bold",
        color=COLORS["agent"],
        ha="left",
        va="center",
    )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(2.6, 240)
    ax.set_ylim(0.20, 4.5e4)
    ax.set_xticks([3, 10, 30, 100, 200])
    ax.set_xticklabels(["$3k", "$10k", "$30k", "$100k", "$200k"])
    ax.get_xticklabels()[-2].set_ha("right")
    ax.get_xticklabels()[-1].set_ha("left")
    ax.xaxis.set_minor_locator(mpl.ticker.NullLocator())
    ax.set_yticks([tick for tick, _ in HOUR_TICKS])
    ax.set_yticklabels([label for _, label in HOUR_TICKS])
    ax.yaxis.set_minor_locator(mpl.ticker.NullLocator())
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_linewidth(0.55)
        ax.spines[side].set_color(COLORS["axis"])
    ax.tick_params(length=2.5, width=0.55, pad=2.5, labelsize=9.0)
    ax.grid(color=COLORS["grid"], lw=0.55, linestyle="--", zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlabel(
        f"cost, all {data['n']:,}",
        fontsize=10.0,
        color=COLORS["ink2"],
        labelpad=2,
    )
    ax.set_ylabel("Time", fontsize=10.5, color=COLORS["ink2"], labelpad=5)
    return fig


def serializable_summary(data: dict) -> dict:
    return {
        key: value
        for key, value in data.items()
        if key not in {"accessed_raw", "cited_raw"}
    }


def main() -> None:
    load_style()
    data = load_numbers()
    fig = draw_panel(data)
    fig.savefig(HERE / "fig_panelC.png", dpi=400)
    fig.savefig(HERE / "fig_panelC.svg")
    plt.close(fig)

    sources_fig = draw_sources_panel(data)
    # Override the house style's tight bounding box here: the standalone panel
    # is deliberately a square deliverable, not merely a square plotting axes.
    with mpl.rc_context({"savefig.bbox": None, "savefig.pad_inches": 0}):
        sources_fig.savefig(HERE / "fig_panelC_sources.png", dpi=400)
        sources_fig.savefig(HERE / "fig_panelC_sources.svg")
    plt.close(sources_fig)

    cost_time_fig = draw_cost_time_panel(data)
    with mpl.rc_context({"savefig.bbox": None, "savefig.pad_inches": 0}):
        cost_time_fig.savefig(HERE / "fig_panelC_cost_time.png", dpi=200)
        cost_time_fig.savefig(HERE / "fig_panelC_cost_time.svg")
    plt.close(cost_time_fig)

    summary = serializable_summary(data)
    summary["counting_note"] = (
        "Accessed and cited distributions use distinct report-source pairs. "
        "The displayed 16.6k citation total is the 16,555 raw reference entries."
    )
    summary["source_inputs"] = {
        "source_access_summary": str(SOURCE_SUMMARY_INPUT.relative_to(REPO)),
        "source_access_per_report": str(SOURCE_PER_REPORT_INPUT.relative_to(REPO)),
        "runtime": str(RUNTIME_INPUT.relative_to(REPO)),
        "agent_cost_proxy": str(FRAMEWORK_INPUT.relative_to(REPO)),
    }
    (HERE / "fig_panelC_analysis.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )

    print(f"reports: {data['n']:,}")
    print(
        f"sources: {data['accessed_total']:,} accessed; "
        f"{data['cited_total']:,} distinct cited; "
        f"{data['citation_entries_total']:,} citation entries"
    )
    print(
        f"per report: {data['accessed_mean']:.2f} accessed "
        f"(median {data['accessed_median']:.0f}); "
        f"{data['cited_mean']:.2f} cited (median {data['cited_median']:.0f})"
    )
    print(
        f"agent: {duration(data['agent_serial_hours'])} serial, "
        f"{duration(data['agent_parallel_hours'])} parallel, "
        f"{money(data['agent_total_cost'])}"
    )
    print(
        f"analyst: {duration(data['analyst_cited_hours'])} / "
        f"{money(data['analyst_cited_cost'])} for cited sources; "
        f"{duration(data['analyst_accessed_hours'])} / "
        f"{money(data['analyst_accessed_cost'])} for accessed sources"
    )
    print(
        "wrote fig_panelC.{png,svg}, fig_panelC_sources.{png,svg}, "
        "fig_panelC_cost_time.{png,svg}, "
        "and fig_panelC_analysis.json"
    )


if __name__ == "__main__":
    main()
