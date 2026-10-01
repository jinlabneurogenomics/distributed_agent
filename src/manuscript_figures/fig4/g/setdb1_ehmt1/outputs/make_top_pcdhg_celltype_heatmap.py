#!/usr/bin/env python3
"""Plot the most differential Pcdhg genes and cell types for Setdb1 vs Ehmt1."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib.patches import Rectangle


HERE = Path(__file__).resolve().parent
INPUT = HERE / "setdb1_ehmt1_focal_gene_logFC_matrix.csv"
STEM = HERE / "setdb1_ehmt1_top10_pcdhg_hush_top3_celltypes_heatmap"
PERTURBATIONS = ["Setdb1", "Ehmt1"]
N_GENES = 10
N_CELL_TYPES = 3
CAP = 1.8
HUSH_GROUPS = {
    "TASOR-related": ["Tasor", "Pphln1"],
    "ATF7IP-related": ["Atf7ip", "Morc2a"],
}


def main() -> None:
    plt.rcParams.update(
        {
            "font.family": "Arial",
            "font.sans-serif": ["Arial"],
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )

    source = pd.read_csv(INPUT, index_col=0).astype(float).clip(-CAP, CAP)
    pcdhg_genes = [gene for gene in source.index if gene.startswith("Pcdhg")]
    cell_types = [
        column.split(" | ", 1)[1]
        for column in source.columns
        if column.startswith("Setdb1 |")
    ]

    paired_differences = pd.DataFrame(
        {
            cell_type: (
                source.loc[pcdhg_genes, f"Setdb1 | {cell_type}"]
                - source.loc[pcdhg_genes, f"Ehmt1 | {cell_type}"]
            ).abs()
            for cell_type in cell_types
        }
    )
    gene_scores = paired_differences.mean(axis=1).sort_values(ascending=False)
    top_genes = gene_scores.head(N_GENES).index.tolist()
    hush_genes = [gene for genes in HUSH_GROUPS.values() for gene in genes]
    plot_genes = top_genes + hush_genes
    cell_type_scores = (
        paired_differences.loc[top_genes].mean(axis=0).sort_values(ascending=False)
    )
    top_cell_types = cell_type_scores.head(N_CELL_TYPES).index.tolist()

    columns = [
        (cell_type, perturbation)
        for cell_type in top_cell_types
        for perturbation in PERTURBATIONS
    ]
    plot_data = pd.DataFrame(
        {
            f"{cell_type} | {perturbation}": source.loc[
                plot_genes, f"{perturbation} | {cell_type}"
            ]
            for cell_type, perturbation in columns
        },
        index=plot_genes,
    )

    long_values = plot_data.reset_index(names="gene").melt(
        id_vars="gene", var_name="cell_type_perturbation", value_name="logFC"
    )
    long_values[["cell_type", "perturbation"]] = long_values[
        "cell_type_perturbation"
    ].str.split(r" \| ", n=1, expand=True)
    long_values["gene_mean_abs_setdb1_ehmt1_difference"] = long_values["gene"].map(
        gene_scores
    )
    long_values["gene_group"] = long_values["gene"].map(
        {
            **{gene: "Top 10 Pcdhg" for gene in top_genes},
            **{
                gene: group
                for group, genes in HUSH_GROUPS.items()
                for gene in genes
            },
        }
    )
    long_values["cell_type_mean_abs_difference_top10_genes"] = long_values[
        "cell_type"
    ].map(cell_type_scores)
    long_values.drop(columns="cell_type_perturbation").to_csv(
        f"{STEM}_values.csv", index=False
    )

    colors = ["#486f9e", "#e8edf3", "#ffffff", "#f1dfdf", "#b86f70"]
    cmap = LinearSegmentedColormap.from_list("muted_diverging", colors)
    norm = TwoSlopeNorm(vmin=-CAP, vcenter=0.0, vmax=CAP)

    fig, ax = plt.subplots(figsize=(9.2, 9.5))
    for row in range(plot_data.shape[0]):
        for col in range(plot_data.shape[1]):
            value = plot_data.iat[row, col]
            ax.add_patch(
                Rectangle(
                    (col - 0.5, row - 0.5), 1, 1,
                    facecolor=cmap(norm(value)), edgecolor="white", linewidth=2.2,
                )
            )
            ax.text(
                col, row, f"{value:+.2f}", ha="center", va="center",
                fontsize=9.5, color="white" if abs(value) >= 0.9 else "#20252b",
            )

    ax.set_xlim(-0.5, plot_data.shape[1] - 0.5)
    ax.set_ylim(plot_data.shape[0] - 0.5, -0.5)
    ax.set_yticks(np.arange(len(plot_genes)), labels=plot_genes)
    ax.set_xticks(np.arange(len(columns)), labels=[p for _, p in columns])
    ax.xaxis.tick_top()
    ax.tick_params(axis="both", length=0, labelsize=10.5)
    ax.tick_params(axis="x", pad=5)

    for group, cell_type in enumerate(top_cell_types):
        center = group * 2 + 0.5
        ax.text(
            center, -1.35, cell_type, ha="center", va="bottom",
            fontsize=11, color="#4d5660", clip_on=False,
        )
        if group:
            ax.axvline(group * 2 - 0.5, color="white", linewidth=7)

    # Separate the Pcdhg block and the two HUSH-related blocks.
    for boundary in (N_GENES - 0.5, N_GENES + 2 - 0.5):
        ax.axhline(boundary, color="white", linewidth=7)

    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title(
        "Top 10 protocadherin-gamma genes and HUSH-related genes\n"
        "in the 3 most differential cell types",
        fontsize=13, color="#4d5660", pad=62,
    )
    fig.subplots_adjust(left=0.18, right=0.99, bottom=0.04, top=0.76)

    for extension in ("svg", "pdf", "png"):
        kwargs = {"dpi": 300} if extension == "png" else {}
        fig.savefig(f"{STEM}.{extension}", bbox_inches="tight", facecolor="white", **kwargs)
    plt.close(fig)


if __name__ == "__main__":
    main()
