#!/usr/bin/env python3
"""Plot the 3x3 Spearman correlation matrix for the displayed agent runs."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import spearmanr

from plot_original_plus_two_toolbox import load_data


HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
OUTPUT = HERE / "distributed_agents_3x_spearman_heatmap"
LABELS = ["rep1", "rep2", "rep3"]


def main() -> None:
    plt.style.use(REPO_ROOT / "src/figures/style.mplstyle")
    _, predictions = load_data()
    matrix = np.asarray(spearmanr(predictions, axis=0).statistic, dtype=float)
    if matrix.shape != (3, 3):
        raise ValueError(f"Expected a 3x3 correlation matrix, found {matrix.shape}")

    fig, ax = plt.subplots(figsize=(9.5, 8.5))
    image = ax.imshow(matrix, cmap="RdBu_r", vmin=-1, vmax=1, interpolation="nearest")

    ax.set_xticks(range(3), LABELS, fontsize=26)
    ax.set_yticks(range(3), LABELS, fontsize=26)
    ax.set_xlabel("Distributed Agents", fontsize=30, labelpad=16)
    ax.set_ylabel("Distributed Agents", fontsize=30, labelpad=16)
    ax.set_title("Spearman correlation across runs", fontsize=32, pad=24)

    for row in range(3):
        for column in range(3):
            ax.text(
                column,
                row,
                f"{matrix[row, column]:.2f}",
                ha="center",
                va="center",
                fontsize=30,
                fontweight="bold",
                color="white" if matrix[row, column] >= 0.55 else "black",
            )

    ax.set_xticks(np.arange(-0.5, 3, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, 3, 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=4, linestyle="-")
    ax.tick_params(which="minor", bottom=False, left=False)
    ax.tick_params(axis="both", length=0, pad=12)
    for spine in ax.spines.values():
        spine.set_visible(False)

    colorbar = fig.colorbar(image, ax=ax, fraction=0.048, pad=0.06)
    colorbar.set_label("Spearman ρ", fontsize=27, labelpad=14)
    colorbar.ax.tick_params(labelsize=22)
    fig.tight_layout()

    fig.savefig(OUTPUT.with_suffix(".png"), dpi=300, bbox_inches="tight")
    fig.savefig(OUTPUT.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)

    print(np.array2string(matrix, precision=6))
    print(f"png={OUTPUT.with_suffix('.png')}")
    print(f"svg={OUTPUT.with_suffix('.svg')}")


if __name__ == "__main__":
    main()
