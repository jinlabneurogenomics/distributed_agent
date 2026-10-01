#!/usr/bin/env python
"""Generate Q7b depletion ranking comparison plots.

The evaluation treats the ground-truth top 100 depleted genes as the relevant
set, while still annotating genes that appear in GT ranks 101-150.
"""

from __future__ import annotations

import csv
import math
import os
import re
from pathlib import Path


OUT_DIR = Path(__file__).resolve().parent
OUT_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(OUT_DIR / ".mplconfig"))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch


ROOT = OUT_DIR.parents[2]
STYLE_PATH = ROOT / "src/figures/style.mplstyle"
GT_PATH = ROOT / "debug/depletion/ground_truth/fisher/top150_depletion_151_TH_Prkcd_Grin2c_Glut_predicted_group.csv"
PREDICTIONS = {
    "BioAgents q7b_v2": ROOT / "debug/depletion/runs/20260529T191007Z/bioagents/answer.txt",
    "q7b_r4": ROOT / "debug/depletion/runs/q7b_r4/answer.txt",
}
DISPLAY_LABELS = {
    "BioAgents q7b_v2": "2000agents",
    "q7b_r4": "biomni",
}
CUTOFFS = [10, 20, 50, 75, 100]
TOP_GT = 100

COLORS = {
    "BioAgents q7b_v2": "#0072B2",
    "q7b_r4": "#D55E00",
}
BIN_COLORS = {
    "GT 1-10": "#166534",
    "GT 11-25": "#65a30d",
    "GT 26-50": "#f59e0b",
    "GT 51-100": "#ea580c",
    "GT 101-150": "#8b5cf6",
    "NA": "#d1d5db",
}
BIN_ORDER = ["GT 1-10", "GT 11-25", "GT 26-50", "GT 51-100", "GT 101-150", "NA"]


def apply_style() -> None:
    """Apply the project mplstyle. Idempotent."""
    if STYLE_PATH.exists():
        plt.style.use(str(STYLE_PATH))


def parse_prediction_file(path: Path) -> list[tuple[int, str]]:
    lines = path.read_text().splitlines()
    ranked: list[tuple[int, str]] = []
    patterns = (
        # Canonical fenced TSV deliverable used by current bioeval tasks.
        re.compile(r"^\s*(\d+)\t([A-Za-z0-9_.-]+)\s*$"),
        # Legacy prose/Markdown numbered lists.
        re.compile(r"^\s*(\d+)\.\s+([A-Za-z0-9_.-]+)\b"),
        # Markdown tables with rank and gene in the first two columns.
        re.compile(r"^\s*\|\s*(\d+)\s*\|\s*`?([A-Za-z0-9_.-]+)`?\s*\|"),
    )
    for line in lines:
        for pattern in patterns:
            match = pattern.match(line)
            if match:
                ranked.append((int(match.group(1)), match.group(2)))
                break
    if ranked:
        return sorted(ranked, key=lambda item: item[0])

    genes: list[tuple[int, str]] = []
    for line in lines:
        gene = line.strip()
        if (
            gene
            and gene.lower() not in {"gene", "gene_target", "rank"}
            and re.match(r"^[A-Za-z0-9_.-]+$", gene)
        ):
            genes.append((len(genes) + 1, gene))
    return genes


def load_ground_truth(path: Path) -> pd.DataFrame:
    gt = pd.read_csv(path)
    gt["depletion_rank"] = gt["depletion_rank"].astype(int)
    return gt.sort_values("depletion_rank").reset_index(drop=True)


def precision_at_k(pred_genes: list[str], relevant: set[str], k: int) -> float:
    return sum(gene in relevant for gene in pred_genes[:k]) / k


def recall_at_k(pred_genes: list[str], relevant: set[str], k: int) -> float:
    return sum(gene in relevant for gene in pred_genes[:k]) / len(relevant)


def average_precision(pred_genes: list[str], relevant: set[str]) -> float:
    hits = 0
    precisions = []
    for idx, gene in enumerate(pred_genes, start=1):
        if gene in relevant:
            hits += 1
            precisions.append(hits / idx)
    return sum(precisions) / len(relevant)


def ndcg_linear(pred_genes: list[str], truth_rank: dict[str, int], k: int, top_gt: int = TOP_GT) -> float:
    padded = pred_genes[:k] + [None] * max(0, k - len(pred_genes))
    gains = [
        top_gt + 1 - truth_rank[gene]
        if gene is not None and truth_rank.get(gene, top_gt + 1) <= top_gt
        else 0
        for gene in padded[:k]
    ]
    ideal = list(range(top_gt, 0, -1))[:k]

    def dcg(values: list[int]) -> float:
        return sum(value / math.log2(idx + 2) for idx, value in enumerate(values))

    return dcg(gains) / dcg(ideal)


def gt_bin(rank: int | float | None) -> str:
    if rank is None or pd.isna(rank):
        return "NA"
    rank = int(rank)
    if rank <= 10:
        return "GT 1-10"
    if rank <= 25:
        return "GT 11-25"
    if rank <= 50:
        return "GT 26-50"
    if rank <= 100:
        return "GT 51-100"
    if rank <= 150:
        return "GT 101-150"
    return "NA"


def write_markdown_tables(metrics_df: pd.DataFrame, pred_map: pd.DataFrame, gt_map: pd.DataFrame) -> None:
    rows = []
    for _, row in metrics_df.iterrows():
        if row["cutoff"] in CUTOFFS:
            rows.append(
                [
                    DISPLAY_LABELS[row["framework"]],
                    int(row["cutoff"]),
                    int(row["hits_gt_top100"]),
                    f"{row['precision']:.3f}",
                    f"{row['recall_gt_top100']:.3f}",
                    f"{int(row['prefix_hits_gt_topk'])}/{int(row['cutoff'])} = {row['prefix_overlap_gt_topk']:.3f}",
                ]
            )

    lines = [
        "# Q7b Depletion Evaluation Tables",
        "",
        "Ground-truth relevance is constrained to GT top100.",
        "",
        "| Framework | Pred cutoff | Hits in GT top100 | Precision | Recall of GT top100 | Prefix overlap with GT topK |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for framework, cutoff, hits, precision, recall, prefix in rows:
        lines.append(f"| {framework} | {cutoff} | {hits} | {precision} | {recall} | {prefix} |")

    lines += [
        "",
        "| Framework | AP | NDCG@100 |",
        "|---|---:|---:|",
    ]
    for framework in PREDICTIONS:
        sub = metrics_df[(metrics_df["framework"] == framework) & (metrics_df["cutoff"] == 100)].iloc[0]
        lines.append(f"| {DISPLAY_LABELS[framework]} | {sub['ap']:.3f} | {sub['ndcg_linear']:.3f} |")

    lines += [
        "",
        "## Top 30 Rank Mapping",
        "",
        "| Framework | Pred rank | Pred gene | GT rank | GT rank | GT gene | Pred rank |",
        "|---|---:|---|---:|---:|---|---:|",
    ]
    for framework in PREDICTIONS:
        for idx in range(30):
            pred_row = pred_map[(pred_map["framework"] == framework) & (pred_map["pred_rank"] == idx + 1)].iloc[0]
            gt_row = gt_map[(gt_map["framework"] == framework) & (gt_map["gt_rank"] == idx + 1)].iloc[0]
            lines.append(
                "| "
                + " | ".join(
                    [
                        DISPLAY_LABELS[framework],
                        str(idx + 1),
                        str(pred_row["pred_gene"]),
                        str(pred_row["gt_rank_display"]),
                        str(idx + 1),
                        str(gt_row["gt_gene"]),
                        str(gt_row["pred_rank_display"]),
                    ]
                )
                + " |"
            )
    (OUT_DIR / "summary_tables.md").write_text("\n".join(lines) + "\n")


def plot_metric_summary(metrics_df: pd.DataFrame) -> None:
    selected = []
    for framework in PREDICTIONS:
        sub = metrics_df[metrics_df["framework"] == framework].set_index("cutoff")
        selected.extend(
            [
                {"framework": framework, "metric": "P@10", "value": sub.loc[10, "precision"]},
                {"framework": framework, "metric": "P@50", "value": sub.loc[50, "precision"]},
                {"framework": framework, "metric": "P@100", "value": sub.loc[100, "precision"]},
                {"framework": framework, "metric": "R@100", "value": sub.loc[100, "recall_gt_top100"]},
                {"framework": framework, "metric": "AP", "value": sub.loc[100, "ap"]},
                {"framework": framework, "metric": "NDCG@100", "value": sub.loc[100, "ndcg_linear"]},
            ]
        )
    data = pd.DataFrame(selected)
    metrics = data["metric"].drop_duplicates().tolist()
    x = np.arange(len(metrics))
    width = 0.36

    fig, ax = plt.subplots(figsize=(10, 5))
    for offset, framework in zip([-width / 2, width / 2], PREDICTIONS):
        vals = data[data["framework"] == framework].set_index("metric").loc[metrics, "value"].to_numpy()
        bars = ax.bar(x + offset, vals, width, label=DISPLAY_LABELS[framework], color=COLORS[framework])
        ax.bar_label(bars, fmt="%.2f", fontsize=8, padding=2)
    ax.set_xticks(x, metrics)
    ax.set_ylim(0, 0.6)
    ax.set_ylabel("Score")
    ax.set_title("Q7b depletion ranking metrics, GT top100 relevance")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "01_metric_summary_top100.png", dpi=300)
    plt.close(fig)


def plot_metric_summary_no_ap(metrics_df: pd.DataFrame) -> None:
    selected = []
    for framework in PREDICTIONS:
        sub = metrics_df[metrics_df["framework"] == framework].set_index("cutoff")
        selected.extend(
            [
                {"framework": framework, "metric": "P@10", "value": sub.loc[10, "precision"]},
                {"framework": framework, "metric": "P@50", "value": sub.loc[50, "precision"]},
                {"framework": framework, "metric": "P@100", "value": sub.loc[100, "precision"]},
                {"framework": framework, "metric": "R@100", "value": sub.loc[100, "recall_gt_top100"]},
                {"framework": framework, "metric": "NDCG@100", "value": sub.loc[100, "ndcg_linear"]},
            ]
        )
    data = pd.DataFrame(selected)
    metrics = data["metric"].drop_duplicates().tolist()
    x = np.arange(len(metrics))
    width = 0.36

    fig, ax = plt.subplots(figsize=(8.5, 5))
    for offset, framework in zip([-width / 2, width / 2], PREDICTIONS):
        vals = data[data["framework"] == framework].set_index("metric").loc[metrics, "value"].to_numpy()
        bars = ax.bar(x + offset, vals, width, label=DISPLAY_LABELS[framework], color=COLORS[framework])
        ax.bar_label(bars, fmt="%.2f", fontsize=8, padding=2)
    ax.set_xticks(x, metrics)
    ax.set_ylim(0, 0.6)
    ax.set_ylabel("Score")
    ax.set_title("2000agents wins broad recovery; biomni wins top-10 precision")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "01v2_metric_summary_top100_no_ap.png", dpi=300)
    plt.close(fig)


def plot_at_k_curves(metrics_df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(13, 4), sharex=True)
    specs = [
        ("precision", "Precision@K"),
        ("recall_gt_top100", "Recall@K of GT top100"),
        ("prefix_overlap_gt_topk", "Prefix overlap@K"),
    ]
    for ax, (col, label) in zip(axes, specs):
        for framework in PREDICTIONS:
            sub = metrics_df[metrics_df["framework"] == framework]
            ax.plot(
                sub["cutoff"],
                sub[col],
                marker="o",
                linewidth=2.2,
                label=DISPLAY_LABELS[framework],
                color=COLORS[framework],
            )
        ax.set_title(label)
        ax.set_xlabel("Predicted rank cutoff")
        ax.set_xticks(CUTOFFS)
        ax.set_ylim(0, 0.55)
        ax.grid(alpha=0.25)
    axes[0].set_ylabel("Score")
    axes[-1].legend(frameon=False, loc="upper right")
    fig.suptitle("At-K behavior separates early precision from broader recall", y=1.03)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "02_at_k_curves_top100.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_cumulative_hits(pred_annot: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))
    for framework in PREDICTIONS:
        sub = pred_annot[pred_annot["framework"] == framework].sort_values("pred_rank")
        y = (sub["gt_rank"].fillna(10**9) <= TOP_GT).cumsum()
        ax.step(
            sub["pred_rank"],
            y,
            where="post",
            linewidth=2.4,
            label=DISPLAY_LABELS[framework],
            color=COLORS[framework],
        )
    ax.plot([1, 100], [1, 100], color="#9ca3af", linestyle="--", linewidth=1.2, label="Perfect retrieval")
    ax.set_xlim(1, 100)
    ax.set_ylim(0, 105)
    ax.set_xlabel("Predicted rank")
    ax.set_ylabel("Cumulative hits in GT top100")
    ax.set_title("Cumulative recovery of GT top100 depleted genes")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "03_cumulative_hits_top100.png", dpi=300)
    plt.close(fig)


def plot_rank_scatter(pred_annot: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharex=True, sharey=True)
    for ax, framework in zip(axes, PREDICTIONS):
        sub = pred_annot[(pred_annot["framework"] == framework) & pred_annot["gt_rank"].notna()]
        colors = [BIN_COLORS[gt_bin(rank)] for rank in sub["gt_rank"]]
        ax.scatter(sub["pred_rank"], sub["gt_rank"], s=44, c=colors, edgecolor="white", linewidth=0.5)
        ax.plot([1, 100], [1, 100], color="#6b7280", linestyle="--", linewidth=1)
        ax.axhline(100, color="#111827", linewidth=1, alpha=0.5)
        ax.set_title(DISPLAY_LABELS[framework])
        ax.set_xlabel("Predicted rank")
        ax.grid(alpha=0.25)
    axes[0].set_ylabel("GT depletion rank, lower is better")
    axes[0].invert_yaxis()
    legend = [Patch(facecolor=BIN_COLORS[label], label=label) for label in BIN_ORDER[:-1]]
    axes[1].legend(handles=legend, frameon=False, loc="lower right")
    fig.suptitle("Rank mapping for predicted genes found in GT top150", y=1.03)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "04_rank_scatter_gt150.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_rank_strips(pred_annot: pd.DataFrame) -> None:
    bin_to_value = {label: idx for idx, label in enumerate(BIN_ORDER)}
    matrix = []
    labels = []
    for framework in PREDICTIONS:
        sub = pred_annot[pred_annot["framework"] == framework].sort_values("pred_rank")
        matrix.append([bin_to_value[label] for label in sub["gt_bin"].tolist()])
        labels.append(DISPLAY_LABELS[framework])
    cmap = ListedColormap([BIN_COLORS[label] for label in BIN_ORDER])

    fig, ax = plt.subplots(figsize=(12, 2.6))
    ax.imshow(np.array(matrix), aspect="auto", interpolation="nearest", cmap=cmap, vmin=0, vmax=len(BIN_ORDER) - 1)
    ax.set_yticks(range(len(labels)), labels)
    ax.set_xticks([0, 9, 19, 49, 74, 99], [1, 10, 20, 50, 75, 100])
    ax.set_xlabel("Predicted rank")
    ax.set_title("Predicted-rank strips colored by GT depletion bin")
    handles = [Patch(facecolor=BIN_COLORS[label], label=label) for label in BIN_ORDER]
    ax.legend(handles=handles, ncol=6, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.35), fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "05_predicted_rank_strips_gt_bins.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_gt_top30_recovery(gt_map: pd.DataFrame) -> None:
    top30 = gt_map[gt_map["gt_rank"] <= 30].copy()
    genes = top30[top30["framework"] == next(iter(PREDICTIONS))].sort_values("gt_rank")["gt_gene"].tolist()
    y_positions = np.arange(len(genes))

    fig, ax = plt.subplots(figsize=(10, 10))
    offsets = {"BioAgents q7b_v2": -0.16, "q7b_r4": 0.16}
    for framework in PREDICTIONS:
        sub = top30[top30["framework"] == framework].set_index("gt_gene").loc[genes]
        x = [rank if not pd.isna(rank) else 106 for rank in sub["pred_rank"]]
        ax.scatter(
            x,
            y_positions + offsets[framework],
            s=48,
            label=DISPLAY_LABELS[framework],
            color=COLORS[framework],
        )
    ax.axvline(100, color="#6b7280", linestyle="--", linewidth=1)
    ax.set_yticks(y_positions, [f"{idx + 1}. {gene}" for idx, gene in enumerate(genes)])
    ax.set_xticks([1, 10, 25, 50, 75, 100, 106], ["1", "10", "25", "50", "75", "100", "NA"])
    ax.set_xlim(0, 110)
    ax.invert_yaxis()
    ax.set_xlabel("Predicted rank")
    ax.set_title("Recovery of GT top30 depleted genes")
    ax.grid(axis="x", alpha=0.25)
    handles = [
        Patch(facecolor=COLORS[framework], label=DISPLAY_LABELS[framework])
        for framework in PREDICTIONS
    ]
    ax.legend(handles=handles, frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "06_gt_top30_recovery.png", dpi=300)
    plt.close(fig)


def plot_hit_bin_composition(pred_annot: pd.DataFrame) -> None:
    counts = (
        pred_annot.groupby(["framework", "gt_bin"])
        .size()
        .unstack(fill_value=0)
        .reindex(index=list(PREDICTIONS), columns=BIN_ORDER, fill_value=0)
    )
    fig, ax = plt.subplots(figsize=(9, 5))
    bottom = np.zeros(len(counts))
    x = np.arange(len(counts))
    for label in BIN_ORDER:
        vals = counts[label].to_numpy()
        ax.bar(x, vals, bottom=bottom, color=BIN_COLORS[label], label=label)
        bottom += vals
    ax.set_xticks(x, [DISPLAY_LABELS[label] for label in counts.index])
    ax.set_ylabel("Predictions in top 100 list")
    ax.set_title("Composition of predicted lists by GT depletion bin")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "07_hit_bin_composition.png", dpi=300)
    plt.close(fig)


def plot_mapping_table(pred_map: pd.DataFrame, gt_map: pd.DataFrame) -> None:
    for framework in PREDICTIONS:
        rows = []
        for idx in range(30):
            pred_row = pred_map[(pred_map["framework"] == framework) & (pred_map["pred_rank"] == idx + 1)].iloc[0]
            gt_row = gt_map[(gt_map["framework"] == framework) & (gt_map["gt_rank"] == idx + 1)].iloc[0]
            rows.append(
                [
                    str(idx + 1),
                    pred_row["pred_gene"],
                    pred_row["gt_rank_display"],
                    str(idx + 1),
                    gt_row["gt_gene"],
                    gt_row["pred_rank_display"],
                ]
            )

        fig, ax = plt.subplots(figsize=(11, 10))
        ax.axis("off")
        table = ax.table(
            cellText=rows,
            colLabels=["Pred rank", "Pred gene", "GT rank", "GT rank", "GT gene", "Pred rank"],
            loc="center",
            cellLoc="left",
            colLoc="left",
            colWidths=[0.10, 0.22, 0.11, 0.10, 0.22, 0.11],
        )
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1, 1.35)
        for (row, col), cell in table.get_celld().items():
            if row == 0:
                cell.set_text_props(weight="bold", color="white")
                cell.set_facecolor("#111827")
            elif row % 2:
                cell.set_facecolor("#f3f4f6")
            else:
                cell.set_facecolor("white")
            cell.set_edgecolor("#d1d5db")
        ax.set_title(f"Top 30 rank mapping: {DISPLAY_LABELS[framework]}", pad=18, fontsize=13, weight="bold")
        fig.tight_layout()
        safe_name = framework.lower().replace(" ", "_").replace("/", "_")
        fig.savefig(OUT_DIR / f"08_top30_mapping_table_{safe_name}.png", dpi=300, bbox_inches="tight")
        plt.close(fig)


def main() -> None:
    apply_style()

    gt = load_ground_truth(GT_PATH)
    truth_rank = dict(zip(gt["gene_target"], gt["depletion_rank"]))
    gt_top100 = set(gt.loc[gt["depletion_rank"] <= TOP_GT, "gene_target"])

    predictions = {name: parse_prediction_file(path)[:100] for name, path in PREDICTIONS.items()}
    metrics_rows = []
    pred_rows = []
    pred_map_rows = []
    gt_map_rows = []

    for framework, ranked in predictions.items():
        pred_genes = [gene for _, gene in ranked]
        ap = average_precision(pred_genes, gt_top100)
        ndcg100 = ndcg_linear(pred_genes, truth_rank, 100)
        for cutoff in CUTOFFS:
            pred_top = set(pred_genes[:cutoff])
            gt_topk = set(gt.loc[gt["depletion_rank"] <= cutoff, "gene_target"])
            hits = sum(gene in gt_top100 for gene in pred_genes[:cutoff])
            prefix_hits = len(pred_top & gt_topk)
            metrics_rows.append(
                {
                    "framework": framework,
                    "cutoff": cutoff,
                    "hits_gt_top100": hits,
                    "precision": precision_at_k(pred_genes, gt_top100, cutoff),
                    "recall_gt_top100": recall_at_k(pred_genes, gt_top100, cutoff),
                    "prefix_hits_gt_topk": prefix_hits,
                    "prefix_overlap_gt_topk": prefix_hits / cutoff,
                    "ap": ap,
                    "ndcg_linear": ndcg_linear(pred_genes, truth_rank, cutoff),
                    "ndcg100": ndcg100,
                }
            )

        for pred_rank, gene in ranked:
            rank = truth_rank.get(gene)
            pred_rows.append(
                {
                    "framework": framework,
                    "pred_rank": pred_rank,
                    "pred_gene": gene,
                    "gt_rank": rank,
                    "gt_bin": gt_bin(rank),
                    "is_gt_top100": bool(rank is not None and rank <= TOP_GT),
                }
            )

        for idx in range(30):
            pred_rank, gene = ranked[idx]
            rank = truth_rank.get(gene)
            pred_map_rows.append(
                {
                    "framework": framework,
                    "pred_rank": pred_rank,
                    "pred_gene": gene,
                    "gt_rank": rank,
                    "gt_rank_display": str(rank) if rank is not None else "NA",
                }
            )

        pred_rank_lookup = {gene: rank for rank, gene in ranked}
        for _, row in gt.head(100).iterrows():
            rank = int(row["depletion_rank"])
            gene = row["gene_target"]
            pred_rank = pred_rank_lookup.get(gene)
            gt_map_rows.append(
                {
                    "framework": framework,
                    "gt_rank": rank,
                    "gt_gene": gene,
                    "pred_rank": pred_rank,
                    "pred_rank_display": str(pred_rank) if pred_rank is not None else "NA",
                }
            )

    metrics_df = pd.DataFrame(metrics_rows)
    pred_annot = pd.DataFrame(pred_rows)
    pred_map = pd.DataFrame(pred_map_rows)
    gt_map = pd.DataFrame(gt_map_rows)

    metrics_df.to_csv(OUT_DIR / "metrics_top100.csv", index=False)
    pred_annot.to_csv(OUT_DIR / "prediction_annotations.csv", index=False)
    pred_map.to_csv(OUT_DIR / "predicted_top30_mapping.csv", index=False)
    gt_map.to_csv(OUT_DIR / "gt_top100_recovery.csv", index=False)
    write_markdown_tables(metrics_df, pred_map, gt_map)

    plot_metric_summary(metrics_df)
    plot_metric_summary_no_ap(metrics_df)
    plot_at_k_curves(metrics_df)
    plot_cumulative_hits(pred_annot)
    plot_rank_scatter(pred_annot)
    plot_rank_strips(pred_annot)
    plot_gt_top30_recovery(gt_map)
    plot_hit_bin_composition(pred_annot)
    plot_mapping_table(pred_map, gt_map)

    manifest = {
        "ground_truth": str(GT_PATH),
        "predictions": {name: str(path) for name, path in PREDICTIONS.items()},
        "top_gt_relevance_cutoff": TOP_GT,
        "pngs": sorted(path.name for path in OUT_DIR.glob("*.png")),
        "tables": sorted(path.name for path in OUT_DIR.glob("*.csv")) + ["summary_tables.md"],
    }
    with (OUT_DIR / "manifest.json").open("w", newline="") as handle:
        import json

        json.dump(manifest, handle, indent=2)

    print(f"Wrote {len(manifest['pngs'])} PNGs and {len(manifest['tables'])} table files to {OUT_DIR}")


if __name__ == "__main__":
    main()
