#!/usr/bin/env python3
"""Plot STRING support for the six largest Task-1 response -> zero misses.

This is a compact, target-level companion to the aggregate STRING
physical/functional/literature bucket plots.  Panel a establishes miss
severity (observed DEG count versus the BioAgents zero call).  Panel b shows
whether each target has no qualifying STRING training partner (A), only
response-mismatched partners (B), or at least one response-matched partner
(C).  The B/C distinction is evaluator-side and post-hoc: it characterizes
the miss but does not prove that network coverage caused the model error.

The long categorical rows are still kept in square plotting boxes: at six
targets they remain readable and tile cleanly.  Both individual panels and the
joint plate are emitted from the same draw functions, per repo convention.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Callable

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/bioagents-mpl")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "src"))

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch, Rectangle  # noqa: E402
from figures.panel_kit import house_style, plate, square  # noqa: E402


INPUT_CSV = (
    HERE
    / "task1_string_partner_buckets_v1_20260919"
    / "per_target_buckets.csv"
)
OUTPUT_DIR = HERE / "task1_top6_zero_miss_string_support_v1_20260919"
OUTPUT_STEM = "fig_task1_top6_zero_miss_string_support"
SUMMARY_CSV = OUTPUT_DIR / "top6_zero_miss_string_buckets.csv"

NETWORK_ORDER = ("functional", "physical", "literature")
NETWORK_LABELS = {
    "functional": "Functional",
    "physical": "Physical",
    "literature": "Literature",
}
BUCKET_ORDER = ("A", "B", "C")
BUCKET_COLORS = {
    "A": "#D9DEE5",
    "B": "#D9822B",
    "C": "#138A8A",
}
BUCKET_LABELS = {
    "A": "A  no partner",
    "B": "B  no matched partner",
    "C": "C  matched partner",
}
OBSERVED_COLOR = "#334155"
PREDICTED_COLOR = "#D94841"
LINK_COLOR = "#C7CDD6"


def load_top_misses() -> tuple[pd.DataFrame, pd.DataFrame]:
    frame = pd.read_csv(INPUT_CSV)
    frame = frame[
        frame["response_definition"].eq("same_seven_level_bin")
        & frame["network"].isin(NETWORK_ORDER)
    ].copy()

    repeated = frame[frame["network"].eq("functional")].copy()
    misses = repeated[
        repeated["actual_n_degs"].gt(0)
        & repeated["bioagents_predicted_n_degs"].eq(0)
    ].nlargest(6, "actual_n_degs")
    target_order = misses["p"].tolist()

    selected = frame[frame["p"].isin(target_order)].copy()
    selected["target_order"] = pd.Categorical(
        selected["p"], categories=target_order, ordered=True
    )
    selected["network_order"] = pd.Categorical(
        selected["network"], categories=NETWORK_ORDER, ordered=True
    )
    selected = selected.sort_values(["target_order", "network_order"])

    expected_rows = len(target_order) * len(NETWORK_ORDER)
    if len(target_order) != 6 or len(selected) != expected_rows:
        raise ValueError(
            f"Expected 6 targets x 3 networks, found {len(target_order)} targets "
            f"and {len(selected)} rows"
        )
    if not selected["bioagents_predicted_n_degs"].eq(0).all():
        raise ValueError("Selected targets must all be BioAgents zero calls")
    if selected.duplicated(["p", "network"]).any():
        raise ValueError("Expected one row per target and network")

    target_summary = (
        selected.groupby("p", observed=True, sort=False)
        .agg(
            actual_n_degs=("actual_n_degs", "first"),
            bioagents_predicted_n_degs=("bioagents_predicted_n_degs", "first"),
        )
        .reindex(target_order)
        .reset_index()
    )
    return selected, target_summary


def format_count(value: float | int) -> str:
    return f"{int(value):,}"


def draw_severity(ax: plt.Axes, targets: pd.DataFrame) -> None:
    y = np.arange(len(targets))
    actual = targets["actual_n_degs"].to_numpy(dtype=float)
    observed_x = np.log1p(actual)
    predicted_x = np.log1p(
        targets["bioagents_predicted_n_degs"].to_numpy(dtype=float)
    )

    ax.hlines(y, predicted_x, observed_x, color=LINK_COLOR, linewidth=3.2, zorder=1)
    ax.scatter(
        observed_x,
        y,
        s=31,
        color=OBSERVED_COLOR,
        edgecolor="white",
        linewidth=0.5,
        zorder=3,
    )
    ax.scatter(
        predicted_x,
        y,
        s=27,
        color=PREDICTED_COLOR,
        edgecolor="white",
        linewidth=0.5,
        zorder=3,
    )
    for xpos, ypos, value in zip(observed_x, y, actual):
        ax.annotate(
            format_count(value),
            (xpos, ypos),
            xytext=(4, 0),
            textcoords="offset points",
            va="center",
            fontsize=6.5,
            color=OBSERVED_COLOR,
        )

    ticks = np.log1p(np.array([0, 1, 10, 100, 1000], dtype=float))
    ax.set_xticks(ticks, ["0", "1", "10", "100", "1,000"])
    # Open a small transformed-space margin so the predicted-zero dots do not
    # disappear into the y spine; no negative count is labeled or implied.
    ax.set_xlim(-0.28, max(observed_x) + 0.70)
    ax.set_yticks(y, targets["p"])
    ax.set_ylim(len(targets) - 0.5, -0.5)
    ax.set_xlabel("DEG count (log1p scale)")
    ax.set_title("a  Miss severity", loc="left")
    ax.grid(axis="x")
    ax.legend(
        handles=[
            Line2D(
                [],
                [],
                marker="o",
                linestyle="none",
                markersize=5,
                color=OBSERVED_COLOR,
                label="Observed",
            ),
            Line2D(
                [],
                [],
                marker="o",
                linestyle="none",
                markersize=5,
                color=PREDICTED_COLOR,
                label="BioAgents",
            ),
        ],
        loc="lower right",
        frameon=False,
        fontsize=6.5,
        ncol=2,
        columnspacing=0.8,
        handletextpad=0.3,
    )
    square(ax)


def draw_string_matrix(
    ax: plt.Axes, selected: pd.DataFrame, targets: pd.DataFrame
) -> None:
    target_order = targets["p"].tolist()
    lookup = selected.set_index(["p", "network"])

    for row, target in enumerate(target_order):
        for col, network in enumerate(NETWORK_ORDER):
            record = lookup.loc[(target, network)]
            bucket = record["bucket"]
            ax.add_patch(
                Rectangle(
                    (col - 0.5, row - 0.5),
                    1,
                    1,
                    facecolor=BUCKET_COLORS[bucket],
                    edgecolor="white",
                    linewidth=1.5,
                )
            )
            if bucket == "A":
                text = "A\nnone"
                text_color = "#44505F"
            else:
                partner = str(record["best_partner"])
                partner_count = format_count(record["best_partner_n_degs"])
                text = f"{bucket}\n{partner} · {partner_count}"
                text_color = "white"
            ax.text(
                col,
                row,
                text,
                ha="center",
                va="center",
                fontsize=6.1,
                color=text_color,
                linespacing=1.12,
            )

    ax.set_xticks(np.arange(len(NETWORK_ORDER)), [NETWORK_LABELS[n] for n in NETWORK_ORDER])
    ax.tick_params(axis="x", top=True, labeltop=True, bottom=False, labelbottom=False)
    ax.set_yticks(np.arange(len(target_order)), target_order)
    ax.set_xlim(-0.5, len(NETWORK_ORDER) - 0.5)
    ax.set_ylim(len(target_order) - 0.5, -0.5)
    ax.set_xticks(np.arange(-0.5, len(NETWORK_ORDER), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(target_order), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=1.5)
    ax.tick_params(which="minor", bottom=False, left=False)
    ax.set_title("b  STRING support", loc="left", pad=22)
    ax.legend(
        handles=[
            Patch(facecolor=BUCKET_COLORS[bucket], edgecolor="none", label=BUCKET_LABELS[bucket])
            for bucket in BUCKET_ORDER
        ],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.10),
        frameon=False,
        fontsize=5.8,
        ncol=1,
        handlelength=0.9,
        handletextpad=0.4,
        labelspacing=0.25,
    )
    square(ax)


def write_results(selected: pd.DataFrame, targets: pd.DataFrame) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    selected.to_csv(SUMMARY_CSV, index=False)
    counts = selected["bucket"].value_counts().reindex(BUCKET_ORDER, fill_value=0)
    target_lines = "\n".join(
        f"- {row.p}: {format_count(row.actual_n_degs)} observed, 0 predicted"
        for row in targets.itertuples(index=False)
    )
    (OUTPUT_DIR / "RESULTS.md").write_text(
        "# Top-six Task-1 response-to-zero misses: STRING support\n\n"
        "The six largest observed responses assigned a BioAgents count of zero are:\n\n"
        f"{target_lines}\n\n"
        "Across the 18 target-by-network comparisons, the primary STRING analysis "
        f"assigns **{counts['A']} to A** (no qualifying training partner), "
        f"**{counts['B']} to B** (qualifying partners exist, but none occupy the "
        f"target's observed seven-level DEG-count range), and **{counts['C']} to C** "
        "(at least one response-matched partner).\n\n"
        "This is the target-level version of the aggregate physical, functional, "
        "and literature result: response-matched partners are associated with lower "
        "count error, whereas proximity without response similarity is not sufficient. "
        "Because response similarity uses held-out truth, this is a post-hoc "
        "characterization and not causal proof of why the model emitted zero.\n",
        encoding="utf-8",
    )


def main() -> None:
    selected, targets = load_top_misses()
    write_results(selected, targets)
    house_style()
    panels: dict[str, Callable[[plt.Axes], None]] = {
        "a": lambda ax: draw_severity(ax, targets),
        "b": lambda ax: draw_string_matrix(ax, selected, targets),
    }
    written = plate(
        panels,
        OUTPUT_DIR,
        OUTPUT_STEM,
        panel_size=(3.35, 3.35),
        joint_size=(7.0, 3.35),
        concepts={
            "observed count": OBSERVED_COLOR,
            "BioAgents prediction": PREDICTED_COLOR,
            "no qualifying partner": BUCKET_COLORS["A"],
            "no response-matched partner": BUCKET_COLORS["B"],
            "response-matched partner": BUCKET_COLORS["C"],
        },
        tight_kw={"pad": 0.6},
    )
    print(f"  wrote {SUMMARY_CSV.name}")
    print("  bucket counts:", selected["bucket"].value_counts().to_dict())
    print("  targets:", ", ".join(targets["p"]))
    if len(written) != 6:
        raise RuntimeError(f"Expected six panel/plate files, wrote {len(written)}")


if __name__ == "__main__":
    main()
