#!/usr/bin/env python3
"""Reproduce the ATXN1/CIC target-level cosine-similarity panel."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


HERE = Path(__file__).resolve().parent
INPUT = HERE.parent / "inputs" / "perturbation_effect_vectors_by_target.csv"
STEM = HERE / "rank21_selected_target_effect_vector_similarity"
MATRIX = HERE / "rank21_selected_target_effect_vector_cosine.csv"
TARGETS = ["Atxn1", "Cic", "Atxn2", "Atxn7", "Atxn10", "Braf", "Map2k1", "Nf1"]


def main() -> None:
    effect = pd.read_csv(INPUT, index_col="gene_target")
    values = effect.to_numpy(float)
    values = values / np.linalg.norm(values, axis=1, keepdims=True)
    similarity = pd.DataFrame(
        values @ values.T,
        index=effect.index,
        columns=effect.index,
    )
    available = [target for target in TARGETS if target in similarity.index]
    selected = similarity.loc[available, available]
    selected.to_csv(MATRIX)

    plt.rcParams.update(
        {
            "font.family": "Arial",
            "font.sans-serif": ["Arial"],
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )
    sns.set_style("white")
    fig, ax = plt.subplots(figsize=(8, 7))
    sns.heatmap(
        selected,
        cmap="vlag",
        center=0,
        vmin=-1,
        vmax=1,
        square=True,
        annot=True,
        fmt=".2f",
        annot_kws={"fontsize": 8},
        linewidths=0.5,
        cbar_kws={"label": "Cosine similarity"},
        ax=ax,
    )
    ax.set(title="Target-level effect-vector similarity", xlabel="", ylabel="")
    ax.tick_params(axis="x", rotation=45)
    ax.tick_params(axis="y", rotation=0)
    fig.tight_layout()
    for extension in ("png", "pdf", "svg"):
        kwargs = {"dpi": 300} if extension == "png" else {}
        fig.savefig(f"{STEM}.{extension}", bbox_inches="tight", **kwargs)
    plt.close(fig)


if __name__ == "__main__":
    main()
