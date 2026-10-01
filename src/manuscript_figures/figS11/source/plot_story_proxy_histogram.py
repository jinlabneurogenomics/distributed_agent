#!/usr/bin/env python3
"""Plot final-story representatives against the 3,397-finding score distribution.

The static plate stacks the panels so their score axes align exactly. This yields
on the square-panel default because horizontal alignment is the point of the
figure: panel A gives the corpus distribution and panel B resolves all 144 story
positions without jittering their scores. A standalone interactive HTML provides
the story identity and narratives on hover.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedLocator, FixedFormatter


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
ANALYSIS = HERE / "analysis_table.csv"
STORIES = HERE / "story_best_central_gene_top_relational_finding.tsv"
STYLE = REPO / "src/figures/style.mplstyle"

OUT_BASE = HERE / "fig1_story_proxy_score_hist"

COL = {
    "hist": "#B8BEC7",
    "hist_edge": "#FFFFFF",
    "proxy": "#0072B2",
    "anchor": "#D55E00",
    "median": "#4A4A4A",
    "grid": "#DDDDDD",
}


def load_data():
    with ANALYSIS.open(newline="") as fh:
        findings = list(csv.DictReader(fh))
    with STORIES.open(newline="") as fh:
        stories = list(csv.DictReader(fh, delimiter="\t"))
    scores = np.asarray([float(r["evidence"]) for r in findings])
    for row in stories:
        row["score"] = float(row["relational_proxy_score"])
        row["final_rank"] = int(row["story_rank"])
        row["relational_rank"] = int(row["relational_proxy_rank"])
        row["is_exact"] = row["proxy_is_exact_central_anchor"] == "True"
    stories.sort(key=lambda r: r["final_rank"])
    return scores, stories


def configure_score_axis(ax, show_label=True):
    xmax = 3.62
    ax.set_xlim(-0.03, xmax)
    ax.set_xticks(np.arange(0, 3.6, 0.5))
    if show_label:
        ax.set_xlabel("relational score")


def draw_histogram(ax, scores, stories, title=True):
    bins = np.linspace(0, scores.max(), 51)
    counts, edges = np.histogram(scores, bins=bins)
    baseline = 0.7
    ax.bar(
        edges[:-1],
        np.clip(counts - baseline, 0, None),
        width=np.diff(edges),
        align="edge",
        bottom=baseline,
        color=COL["hist"],
        edgecolor=COL["hist_edge"],
        linewidth=0.35,
        zorder=1,
    )
    ax.set_yscale("log")
    ax.set_ylim(baseline, counts.max() * 1.55)
    ax.yaxis.set_major_locator(FixedLocator([1, 10, 100, 1000]))
    ax.yaxis.set_major_formatter(FixedFormatter(["1", "10", "100", "1,000"]))
    median = float(np.median(scores))
    ax.axvline(median, color=COL["median"], lw=1.2, ls="--", zorder=3)

    proxy_x = [r["score"] for r in stories if not r["is_exact"]]
    anchor_x = [r["score"] for r in stories if r["is_exact"]]
    ax.scatter(
        proxy_x,
        np.full(len(proxy_x), 0.82),
        marker="|",
        s=55,
        linewidths=0.8,
        color=COL["proxy"],
        alpha=0.60,
        clip_on=False,
        zorder=4,
    )
    ax.scatter(
        anchor_x,
        np.full(len(anchor_x), 1.18),
        marker="^",
        s=14,
        linewidths=0,
        color=COL["anchor"],
        alpha=0.85,
        clip_on=False,
        zorder=5,
    )
    ax.text(
        median + 0.035,
        counts.max() * 1.28,
        f"corpus median {median:.3f}",
        color=COL["median"],
        fontsize=8,
        ha="left",
        va="top",
    )
    ax.set_ylabel("findings (log scale)")
    if title:
        ax.set_title("3,397 relational findings with 144 story representatives")
    configure_score_axis(ax, show_label=False)
    ax.grid(axis="x", visible=False)


def draw_story_map(ax, scores, stories, title=True):
    median = float(np.median(scores))
    ax.axvline(median, color=COL["median"], lw=1.2, ls="--", zorder=1)
    for is_exact, marker, color, label in [
        (False, "o", COL["proxy"], "same-gene proxy"),
        (True, "^", COL["anchor"], "proxy is exact story anchor"),
    ]:
        group = [r for r in stories if r["is_exact"] == is_exact]
        ax.scatter(
            [r["score"] for r in group],
            [r["final_rank"] for r in group],
            marker=marker,
            s=18 if not is_exact else 24,
            color=color,
            edgecolors="none",
            alpha=0.82,
            clip_on=False,
            label=f"{label} (n={len(group)})",
            zorder=3,
        )
    ax.set_ylim(147, -3)
    ax.set_yticks([1, 25, 50, 75, 100, 125, 144])
    ax.set_ylabel("final story rank")
    configure_score_axis(ax, show_label=True)
    if title:
        ax.set_title("One highest-ranked same-gene representative per story")
    ax.legend(
        loc="lower right",
        frameon=False,
        fontsize=8,
        handletextpad=0.4,
        borderaxespad=0.2,
    )


def save(fig, stem):
    fig.savefig(stem.with_suffix(".png"), dpi=180, bbox_inches="tight")
    fig.savefig(stem.with_suffix(".svg"), dpi=600, bbox_inches="tight", transparent=True)
    plt.close(fig)


def render_static(scores, stories):
    with plt.style.context(STYLE):
        fig, ax = plt.subplots(figsize=(5.2, 5.2))
        draw_histogram(ax, scores, stories)
        ax.set_xlabel("relational score")
        fig.tight_layout()
        save(fig, Path(str(OUT_BASE) + "__a"))

        fig, ax = plt.subplots(figsize=(5.2, 5.2))
        draw_story_map(ax, scores, stories)
        fig.tight_layout()
        save(fig, Path(str(OUT_BASE) + "__b"))

        # The shared horizontal scale is the comparison, so the joint plate is
        # stacked rather than forcing two square panels side by side.
        fig = plt.figure(figsize=(7.2, 7.8))
        grid = fig.add_gridspec(2, 1, height_ratios=[0.92, 1.18], hspace=0.10)
        ax_hist = fig.add_subplot(grid[0])
        ax_map = fig.add_subplot(grid[1], sharex=ax_hist)
        draw_histogram(ax_hist, scores, stories, title=False)
        draw_story_map(ax_map, scores, stories, title=False)
        ax_hist.tick_params(axis="x", labelbottom=False)
        fig.suptitle(
            "Where final-story representatives fall in the relational score distribution",
            y=0.992,
        )
        fig.subplots_adjust(left=0.12, right=0.98, top=0.955, bottom=0.09)
        save(fig, OUT_BASE)


def render_html(scores, stories):
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    bins = np.linspace(0, scores.max(), 51)
    counts, edges = np.histogram(scores, bins=bins)
    centers = (edges[:-1] + edges[1:]) / 2
    widths = np.diff(edges)
    median = float(np.median(scores))

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        row_heights=[0.44, 0.56],
        vertical_spacing=0.07,
        subplot_titles=(
            "3,397-finding distribution",
            "One highest-ranked same-gene representative per story",
        ),
    )
    fig.add_trace(
        go.Bar(
            x=centers,
            y=counts,
            width=widths,
            marker={"color": COL["hist"], "line": {"color": "white", "width": 0.4}},
            name="relational findings",
            hovertemplate="score bin %{x:.2f}<br>findings %{y}<extra></extra>",
        ),
        row=1,
        col=1,
    )
    for is_exact, symbol, color, label in [
        (False, "circle", COL["proxy"], "same-gene proxy"),
        (True, "triangle-up", COL["anchor"], "exact story anchor"),
    ]:
        group = [r for r in stories if r["is_exact"] == is_exact]
        custom = [
            [
                r["story_id"],
                r["story_title"],
                r["all_central_genes"],
                r["selected_central_gene"],
                r["relational_proxy_doc_id"],
                r["relational_rank"],
                r["proxy_summary"],
            ]
            for r in group
        ]
        fig.add_trace(
            go.Scatter(
                x=[r["score"] for r in group],
                y=[r["final_rank"] for r in group],
                mode="markers",
                marker={"symbol": symbol, "size": 8, "color": color, "opacity": 0.82},
                name=f"{label} (n={len(group)})",
                customdata=custom,
                hovertemplate=(
                    "<b>%{customdata[0]}</b> · final rank %{y}<br>"
                    "%{customdata[1]}<br>central genes: %{customdata[2]}<br>"
                    "selected: %{customdata[3]} → %{customdata[4]}<br>"
                    "relational score %{x:.4f} · rank %{customdata[5]}/3,397<br>"
                    "%{customdata[6]}<extra></extra>"
                ),
            ),
            row=2,
            col=1,
        )
    fig.add_vline(x=median, line_dash="dash", line_color=COL["median"], row="all", col=1)
    fig.update_yaxes(type="log", title_text="findings (log scale)", row=1, col=1)
    fig.update_yaxes(title_text="final story rank", autorange="reversed", row=2, col=1)
    fig.update_xaxes(range=[-0.03, 3.62], title_text="relational score", row=2, col=1)
    fig.update_layout(
        title="Where final-story representatives fall in the relational score distribution",
        template="simple_white",
        width=900,
        height=820,
        bargap=0,
        legend={"orientation": "h", "y": -0.10, "x": 0},
        margin={"l": 75, "r": 25, "t": 90, "b": 110},
    )
    fig.write_html(
        OUT_BASE.with_suffix(".html"),
        include_plotlyjs=True,
        full_html=True,
        config={"displaylogo": False, "responsive": True},
    )


def main():
    scores, stories = load_data()
    assert len(scores) == 3397
    assert len(stories) == 144
    render_static(scores, stories)
    render_html(scores, stories)
    exact = sum(r["is_exact"] for r in stories)
    vals = np.asarray([r["score"] for r in stories])
    print(f"wrote {OUT_BASE}.png/.svg/.html and individual panels")
    print(
        "story representatives:",
        len(stories),
        "exact anchors:",
        exact,
        "median score:",
        f"{np.median(vals):.4f}",
        "below corpus median:",
        int((vals < np.median(scores)).sum()),
    )


if __name__ == "__main__":
    main()
