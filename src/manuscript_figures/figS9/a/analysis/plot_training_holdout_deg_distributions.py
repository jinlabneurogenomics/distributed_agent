#!/usr/bin/env python3
"""Compare training and holdout DEG-count distributions as within-set shares."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import PercentFormatter

from figures.panel_kit import audit, house_style, save, square


HERE = Path(__file__).resolve().parent
INPUT_DIR = HERE / "holdout_task/Inputs"
TRAINING_CSV = INPUT_DIR / "151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv"
HOLDOUT_CSV = INPUT_DIR / "151_TH_Prkcd_Grin2c_Glut_deg_counts_holdouts.csv"
OUT_DIR = HERE / "task1_target_figures_v1_20260908"
STEM = "fig_training_holdout_deg_distributions"

COLORS = {
    "Training": "#7D8994",
    "Holdout": "#3676A8",
}
COUNT_RANGES = (
    ("0", 0, 0),
    ("1", 1, 1),
    ("2–9", 2, 9),
    ("10–49", 10, 49),
    ("50–249", 50, 249),
    ("250–999", 250, 999),
    ("≥1,000", 1000, np.inf),
)


def _bin_counts(values: np.ndarray) -> np.ndarray:
    return np.asarray(
        [
            np.sum((values >= lower) & (values <= upper))
            for _, lower, upper in COUNT_RANGES
        ],
        dtype=int,
    )


def main() -> None:
    training = pd.read_csv(TRAINING_CSV)["n_degs"].to_numpy(dtype=int)
    holdout = pd.read_csv(HOLDOUT_CSV)["n_degs"].to_numpy(dtype=int)
    counts = {
        "Training": _bin_counts(training),
        "Holdout": _bin_counts(holdout),
    }
    sizes = {"Training": len(training), "Holdout": len(holdout)}

    house_style()
    fig, ax = plt.subplots(figsize=(7.2, 5.5))
    x = np.arange(len(COUNT_RANGES), dtype=float)
    width = 0.37

    for label, offset in (("Training", -width / 2), ("Holdout", width / 2)):
        proportions = counts[label] / sizes[label]
        bars = ax.bar(
            x + offset,
            proportions,
            width=width,
            color=COLORS[label],
            edgecolor="white",
            linewidth=0.6,
            label=f"{label}  (n = {sizes[label]:,})",
        )
        ax.bar_label(
            bars,
            labels=[f"{value:.0%}" if value >= 0.01 else f"{value:.1%}" for value in proportions],
            padding=3,
            fontsize=7,
        )

    ax.set_xticks(x, [label for label, _, _ in COUNT_RANGES])
    ax.set_xlim(-0.62, len(COUNT_RANGES) - 0.38)
    ax.set_ylim(0, 0.80)
    ax.set_yticks(np.arange(0, 0.81, 0.10))
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0))
    ax.set_xlabel("True DEG count range")
    ax.set_ylabel("Perturbations within partition")
    ax.set_title("DEG-count distributions by perturbation partition", loc="left")
    ax.legend(loc="upper right", frameon=False)
    square(ax)
    fig.tight_layout(pad=1.1)

    audit(fig, concepts=COLORS, verbose=True)
    written = save(fig, OUT_DIR / STEM)
    plt.close(fig)
    print(f"training counts: {counts['Training'].tolist()}")
    print(f"holdout counts: {counts['Holdout'].tolist()}")
    print(f"wrote {len(written)} files to {OUT_DIR}")


if __name__ == "__main__":
    main()
