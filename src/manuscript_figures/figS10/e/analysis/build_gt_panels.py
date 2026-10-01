#!/usr/bin/env python
"""fig4/c ground-truth candidate panels (start-wide set).

Renders many views of the GT depletion screen for cell group
`151 TH Prkcd Grin2c Glut` so main-vs-supp can be chosen visually:

  gt_ranking_waterfall      full depletion ranking (log2 OR vs rank)
  gt_ranking_top30          top-30 depleters, lollipop, colored by DEG status
  gt_recovery_vs_aav        recovered cells vs AAV-pool expectation (the screen)
  gt_deg_hist               DEG-count distribution across top-100 (log1p)
  gt_deg_binary             null vs DEG-positive split
  gt_deg_vs_depletion       depletion strength vs transcriptional response (orthogonality)
  gt_null_by_rankbin        null rate is flat across the ranking
  gt_pathways_bar           enriched programs (MSigDB, screen-correct background)
  gt_pathways_dot           same, dot-plot view

Run:  <repo>/.pixi/envs/default/bin/python manuscript/fig4/c/build_gt_panels.py
"""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LinearSegmentedColormap, LogNorm
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from scipy.stats import gaussian_kde, spearmanr

import _common as C


def gt_ranking_waterfall(gt, fisher):
    """Full ranking of every screened gene by log2 depletion odds ratio."""
    f = fisher.sort_values("log2_or", ascending=False).reset_index(drop=True)
    f["rank"] = np.arange(1, len(f) + 1)
    top150 = set(gt["gene_target"])
    top100 = set(gt.loc[gt["depletion_rank"] <= 100, "gene_target"])
    heat = set(gt.loc[gt["passes_heatmap_filter"] == True, "gene_target"])  # noqa: E712

    fig, ax = plt.subplots(figsize=(4.6, 2.9), layout="constrained")
    ax.axhline(0, color="#9CA3AF", ls="--", lw=0.6, zorder=1)
    ax.axvspan(1, 100, color=C.C_HASDEG, alpha=0.07, lw=0, zorder=0)

    other = f[~f["gene_target"].isin(top150)]
    ax.scatter(other["rank"], other["log2_or"], s=3, c=C.C_ALL, lw=0, zorder=2)
    ins = f[f["gene_target"].isin(top150) & ~f["gene_target"].isin(heat)]
    ax.scatter(ins["rank"], ins["log2_or"], s=7, c=C.C_GT, lw=0, zorder=3)
    hp = f[f["gene_target"].isin(heat)]
    ax.scatter(hp["rank"], hp["log2_or"], s=16, c=C.C_HEATMAP,
               edgecolor="white", lw=0.3, zorder=4)

    ax.set_xscale("log")
    ax.set_xlim(1, len(f))
    ax.set_xlabel("Depletion rank among screened genes")
    ax.set_ylabel("log₂ depletion odds ratio")
    ax.set_title(f"Depletion ranking · {C.CELLTYPE_SHORT}", fontsize=7.5)
    ax.axvline(100, color="#6B7280", lw=0.5, ls=":")
    ax.text(100, ax.get_ylim()[1], " top 100", va="top", ha="left",
            fontsize=6, color="#6B7280")
    handles = [
        Line2D([], [], marker="o", ls="", ms=3.5, mfc=C.C_ALL, mec="none", label=f"all screened (n={len(f)})"),
        Line2D([], [], marker="o", ls="", ms=4, mfc=C.C_GT, mec="none", label="GT top 150"),
        Line2D([], [], marker="o", ls="", ms=4.5, mfc=C.C_HEATMAP, mec="white", label=f"heatmap-filter set (n={len(heat)})"),
    ]
    ax.legend(handles=handles, loc="upper right", fontsize=5.6, handletextpad=0.3)
    C.save(fig, "gt_ranking_waterfall")


def gt_ranking_top30(gt):
    """Top-30 depleters as a lollipop, DEG-positive genes shaded by DEG *count*."""
    top = gt[gt["depletion_rank"] <= 30].sort_values("depletion_rank").reset_index(drop=True)
    y = np.arange(len(top))[::-1]
    n_deg = top["n_deg"].to_numpy(float)
    has = n_deg >= 1

    # sequential "has DEG" scale: mid→dark green (skip the near-white low end so a
    # 1-DEG gene still reads as green, not grey). null = flat grey.
    greens = LinearSegmentedColormap.from_list("degs", ["#A7E0C8", "#00794F"])
    norm = LogNorm(vmin=1, vmax=n_deg.max())

    fig, ax = plt.subplots(figsize=(3.7, 4.6), layout="constrained")
    ax.hlines(y, 0, top["log2_odds_ratio"], color="#D9D9D9", lw=1.0, zorder=1)
    ax.scatter(top["log2_odds_ratio"][~has], y[~has], s=30, c=C.C_NULL,
               edgecolor="white", lw=0.4, zorder=3)
    ax.scatter(top["log2_odds_ratio"][has], y[has], s=34, c=n_deg[has],
               cmap=greens, norm=norm, edgecolor="white", lw=0.4, zorder=4)

    ax.set_yticks(y, [f"{r}. {g}" for r, g in zip(top["depletion_rank"], top["gene_target"])],
                  fontsize=5.8)
    ax.set_xlabel("log₂ depletion odds ratio")
    ax.set_title("Top-30 depleters", fontsize=7.5)
    ax.set_xlim(0, top["log2_odds_ratio"].max() * 1.08)

    cb = fig.colorbar(ScalarMappable(norm=norm, cmap=greens), ax=ax,
                      fraction=0.05, pad=0.03, ticks=[1, 10, 100, 1000])
    cb.ax.set_yticklabels(["1", "10", "100", "1000"])
    cb.set_label(f"# DEGs in {C.CELLTYPE_SHORT}", fontsize=6)
    cb.ax.tick_params(labelsize=5.5)
    ax.legend(handles=[Patch(fc=C.C_NULL, label="null (0 DEG)")],
              loc="lower right", fontsize=6, handletextpad=0.3)
    C.save(fig, "gt_ranking_top30")


def gt_recovery_vs_aav(fisher, gt):
    """The screen itself: recovered perturbed cells vs AAV-pool expectation."""
    f = fisher.copy()
    top100 = set(gt.loc[gt["depletion_rank"] <= 100, "gene_target"])
    is_top = f["gene_target"].isin(top100)

    fig, ax = plt.subplots(figsize=(3.5, 3.0), layout="constrained")
    lim = [f[["observed", "expected"]].to_numpy().min() * 0.7,
           f[["observed", "expected"]].to_numpy().max() * 1.3]
    ax.plot(lim, lim, color="#9CA3AF", ls="--", lw=0.7, zorder=1)
    ax.scatter(f["expected"][~is_top], f["observed"][~is_top], s=5,
               c=C.C_ALL, lw=0, zorder=2, label="other genes")
    sc = ax.scatter(f["expected"][is_top], f["observed"][is_top], s=16,
                    c=f["log2_or"][is_top], cmap="magma_r", vmin=0,
                    edgecolor="white", lw=0.2, zorder=3, label="GT top 100")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(lim)
    ax.set_ylim(lim)
    ax.set_xlabel("Expected perturbed cells (AAV pool)")
    ax.set_ylabel("Observed perturbed cells (recovered)")
    ax.set_title(f"Cell recovery vs AAV pool · {C.CELLTYPE_SHORT}", fontsize=7)
    ax.text(0.04, 0.96, "depleted\n(below diagonal)", transform=ax.transAxes,
            va="top", ha="left", fontsize=5.6, color="#6B7280")
    cb = fig.colorbar(sc, ax=ax, fraction=0.045, pad=0.02)
    cb.set_label("log₂ odds ratio", fontsize=6)
    cb.ax.tick_params(labelsize=5.5)
    C.save(fig, "gt_recovery_vs_aav")


def gt_deg_hist(gt):
    """DEG-count distribution across the top-100 depleters (log1p axis)."""
    top = gt[gt["depletion_rank"] <= 100]
    vals = np.log1p(top["n_deg"].to_numpy(float))
    fig, ax = plt.subplots(figsize=(3.4, 2.7), layout="constrained")
    bins = np.linspace(0, vals.max(), 26)
    ax.hist(vals, bins=bins, density=True, color="#BFD9EC", edgecolor="white", lw=0.4)
    kde = gaussian_kde(vals, bw_method=0.28)
    xs = np.linspace(0, vals.max(), 400)
    ax.plot(xs, kde(xs), color="#08519C", lw=1.4)
    ax.plot(vals, np.full_like(vals, -0.03), "|", color="#08519C", alpha=0.5, ms=6)
    med = np.log1p(top["n_deg"].median())
    ax.axvline(med, color=C.C_HEATMAP, ls="--", lw=1.0)
    ticks = [0, 1, 10, 100, 1000, int(top["n_deg"].max())]
    ax.set_xticks([np.log1p(t) for t in ticks], ticks)
    ax.set_xlabel(f"# DEGs in {C.CELLTYPE_SHORT}  (log1p)")
    ax.set_ylabel("Density")
    ax.set_title("DEG burden of top-100 depleters", fontsize=7.5)
    ax.text(0.97, 0.9, f"median = {int(top['n_deg'].median())} DEG",
            transform=ax.transAxes, ha="right", fontsize=6, color=C.C_HEATMAP)
    C.save(fig, "gt_deg_hist")


def gt_deg_binary(gt):
    """Half the real depleters are transcriptionally silent in survivors."""
    top = gt[gt["depletion_rank"] <= 100]
    n_null = int((~top["has_deg"].astype(bool)).sum())
    n_hit = int(top["has_deg"].astype(bool).sum())
    fig, ax = plt.subplots(figsize=(2.8, 2.7), layout="constrained")
    bars = ax.bar(["null hit\n(0 DEG)", "has DEG\n(≥1)"], [n_null, n_hit],
                  color=[C.C_NULL, C.C_HASDEG], edgecolor="white", width=0.62)
    for b, h in zip(bars, [n_null, n_hit]):
        ax.text(b.get_x() + b.get_width() / 2, h + 0.6, f"{h}\n({h}%)",
                ha="center", va="bottom", fontsize=6.5, weight="bold")
    ax.set_ylabel("# of top-100 depleters")
    ax.set_ylim(0, max(n_null, n_hit) * 1.22)
    ax.set_title("Depletion without a\ntranscriptional signature", fontsize=7.5)
    C.save(fig, "gt_deg_binary")


def gt_deg_vs_depletion(gt):
    """Depletion strength is orthogonal to transcriptional response."""
    top = gt[gt["depletion_rank"] <= 100].copy()
    y = np.log1p(top["n_deg"].to_numpy(float))
    x = top["log2_odds_ratio"].to_numpy(float)
    rho, p = spearmanr(top["depletion_rank"], top["n_deg"])
    colors = [C.C_HASDEG if h else C.C_NULL for h in top["has_deg"].astype(bool)]

    fig, ax = plt.subplots(figsize=(3.4, 2.7), layout="constrained")
    ax.scatter(x, y, s=18, c=colors, edgecolor="white", lw=0.3)
    ticks = [0, 1, 10, 100, 1000]
    ax.set_yticks([np.log1p(t) for t in ticks], ticks)
    ax.set_xlabel("log₂ depletion odds ratio")
    ax.set_ylabel(f"# DEGs in {C.CELLTYPE_SHORT}  (log1p)")
    ax.set_title("Fitness phenotype ≠ expression change", fontsize=7.5)
    ax.text(0.96, 0.96, f"Spearman ρ = {rho:.2f}\n(rank vs #DEG, p = {p:.2f})",
            transform=ax.transAxes, va="top", ha="right", fontsize=6, color="#374151")
    handles = [Patch(fc=C.C_HASDEG, label="has DEG(s)"), Patch(fc=C.C_NULL, label="null")]
    ax.legend(handles=handles, loc="upper left", fontsize=5.8, handletextpad=0.3)
    C.save(fig, "gt_deg_vs_depletion")


def gt_null_by_rankbin(gt):
    """Null-hit rate is flat across the depletion ranking (not a top-tail artifact)."""
    top = gt[gt["depletion_rank"] <= 100].copy()
    top["band"] = np.where(top["depletion_rank"] <= 50, "rank 1–50", "rank 51–100")
    grp = top.groupby("band")["has_deg"].agg(["sum", "count"])
    bands = ["rank 1–50", "rank 51–100"]
    has = grp.loc[bands, "sum"].to_numpy()
    null = (grp.loc[bands, "count"] - grp.loc[bands, "sum"]).to_numpy()

    fig, ax = plt.subplots(figsize=(2.8, 2.7), layout="constrained")
    x = np.arange(len(bands))
    ax.bar(x, has, color=C.C_HASDEG, width=0.6, label="has DEG(s)")
    ax.bar(x, null, bottom=has, color=C.C_NULL, width=0.6, label="null")
    for i in range(len(bands)):
        rate = null[i] / (null[i] + has[i])
        ax.text(i, has[i] + null[i] / 2, f"{rate:.0%}\nnull", ha="center",
                va="center", fontsize=6.5, color="#374151", weight="bold")
    ax.set_xticks(x, bands)
    ax.set_ylabel("# depleters")
    ax.set_ylim(0, 64)
    ax.set_title("Null rate is flat across ranks", fontsize=7.5)
    ax.legend(loc="upper right", fontsize=5.8, ncol=2, columnspacing=0.8)
    C.save(fig, "gt_null_by_rankbin")


def gt_pathways_bar(paths):
    fig, ax = plt.subplots(figsize=(4.3, 2.7), layout="constrained")
    colors = [C.COLLECTION_COLORS.get(c, "#888888") for c in paths["collection"]]
    y = np.arange(len(paths))
    ax.barh(y, paths["neglog10q"], color=colors, edgecolor="white", lw=0.4)
    ax.set_yticks(y, paths["label"], fontsize=6)
    ax.axvline(-np.log10(0.05), color="#6B7280", ls="--", lw=0.6)
    ax.text(-np.log10(0.05), len(paths) - 0.4, " q=0.05", fontsize=5.5, color="#6B7280")
    for yi, ratio in enumerate(paths["GeneRatio"]):
        ax.text(paths["neglog10q"].iloc[yi] + 0.03, yi, f"{ratio}", va="center", fontsize=5.3, color="#374151")
    ax.set_xlim(0, paths["neglog10q"].max() * 1.32)
    ax.set_xlabel("−log₁₀ q")
    ax.set_title("Enriched programs in top-100 depleters\n(MSigDB, screen-correct background)", fontsize=7)
    seen = paths["collection"].unique()
    handles = [Patch(fc=C.COLLECTION_COLORS.get(c, "#888888"), label=c) for c in seen]
    ax.legend(handles=handles, loc="center right", bbox_to_anchor=(1.0, 0.42), fontsize=5.8)
    C.save(fig, "gt_pathways_bar")


def gt_pathways_dot(paths):
    fig, ax = plt.subplots(figsize=(4.3, 2.7), layout="constrained")
    y = np.arange(len(paths))
    sizes = paths["Count"].to_numpy() * 16
    sc = ax.scatter(paths["FoldEnrichment"], y, s=sizes, c=paths["neglog10q"],
                    cmap="viridis", edgecolor="white", lw=0.4, zorder=3)
    ax.set_yticks(y, paths["label"], fontsize=6)
    ax.set_xlabel("Fold enrichment")
    ax.set_title("Enriched programs in top-100 depleters", fontsize=7.5)
    ax.grid(axis="x", color=C.GRID, lw=0.3, alpha=0.6)
    cb = fig.colorbar(sc, ax=ax, fraction=0.045, pad=0.02)
    cb.set_label("−log₁₀ q", fontsize=6)
    cb.ax.tick_params(labelsize=5.5)
    # size legend
    for cnt in [4, 6, 9]:
        ax.scatter([], [], s=cnt * 16, c="#888888", label=f"{cnt} genes")
    ax.legend(loc="lower right", fontsize=5.6, labelspacing=0.9, borderpad=0.6)
    C.save(fig, "gt_pathways_dot")


def main():
    C.apply_style()

    gt = C.load_gt()
    fisher = C.load_fisher_celltype()
    paths = C.load_pathways()

    print("ground-truth panels:")
    gt_ranking_waterfall(gt, fisher)
    gt_ranking_top30(gt)
    gt_recovery_vs_aav(fisher, gt)
    gt_deg_hist(gt)
    gt_deg_binary(gt)
    gt_deg_vs_depletion(gt)
    gt_null_by_rankbin(gt)
    gt_pathways_bar(paths)
    gt_pathways_dot(paths)


if __name__ == "__main__":
    main()
