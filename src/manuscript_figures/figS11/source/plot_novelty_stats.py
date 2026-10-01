#!/usr/bin/env python3
"""Novelty EDA over the ranked-fusion full corpus — score = the `evidence` column.

Inputs
  ranked_fusion_fullcorpus.csv : rank, doc_id, gene_target, finding_id, finding_type,
                                 evidence (SCORE), winning_facet {conv/bm_div/ectopy},
                                 gold_significance, in_gold, marquee  (10,898 rows).
                                 `evidence` is zero-inflated: ~78% pile near the 0.0005
                                 floor, high tail to ~4.04 (hence log-y histogram).
  findings_ledger.csv          : joined by (gene_target==target_gene, finding_id) for cell_types
  target_footprint.csv         : per-target total DEGs (FDR<0.05) from the full
                                 wilcoxon parquet (DuckDB aggregation)

Outputs (in this dir)
  analysis_table.csv         : merged per-finding table used for all plots
  fig1_score_hist.png        : evidence distribution (x=score, y=# findings, log-y)
  fig2_score_by_celltype.png : evidence across mentioned cell types
  fig3_score_by_footprint.png: evidence across target DEG footprint
  fig4_score_by_facet.png    : evidence by winning facet (conv/bm_div/ectopy)
  fig5_score_by_findingtype.png: evidence by finding type
  fig6_score_vs_goldsig.png   : evidence vs gold significance
"""
import csv
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SCORED = Path("/gpfs/home/asun/jin_lab/bioagents/debug/260715_consolidated/build/"
              "e2e_relational/ranked_fusion_fullcorpus.csv")
LEDGER = REPO / "src/bioagents/skills/bioagents/findings-ledger-skill/scripts/out/findings_ledger.csv"
FOOTPRINT = HERE / "target_footprint.csv"
# Reuse the precomputed ORA over ground-truth DEGs from Fig1 (per target x cell type x
# library x pathway; GO_BP / Reactome / Hallmark). See manuscript/fig1/g/gt/ora_gt.py.
ORA_GT = REPO / "manuscript/fig1/g/gt/ora_gt.parquet"
# Direct gene->pathway membership (which sets each TARGET gene belongs to).
GENE_MEMBERSHIP = REPO / ("src/bioagents/skills/bioagents/gene-annotation-skill/"
                          "scripts/out/gene_membership.parquet")

# Okabe-Ito colorblind-safe palette
OI = {
    "blue": "#0072B2", "orange": "#E69F00", "green": "#009E73",
    "vermillion": "#D55E00", "purple": "#CC79A7", "sky": "#56B4E9",
    "yellow": "#F0E442", "grey": "#999999",
}
FACET_COLOR = {"conv": OI["blue"], "bm_div": OI["orange"], "ectopy": OI["green"]}
FACET_LABEL = {"conv": "conv", "bm_div": "bm_div", "ectopy": "ectopy"}
GOLD_COLOR = {"1": OI["vermillion"], "0": OI["grey"]}
SCORE_LABEL = "score"
MEAN_NOTE = "box = median/IQR · whiskers = min–max · ◆ = mean"

# Canonical cell groups. cell_types in the ledger are '|'-joined and also contain
# free-text extraction artifacts (e.g. "22 measured X cell classes"); keep only these 23.
CELL_WHITELIST = {
    "001 L5-6 IT Glut", "005 L4-5 IT CTX Glut", "007 L2-3 IT CTX Glut",
    "008 L2-3 IT ENT PPP RSP Glut", "009 L2-3 IT PIR AON ENT Glut",
    "012 MEA LA CA1 DG Glut", "017 CA3 CA2-FC DG Glut", "022 L5 ET CTX Glut",
    "027 NP-CT-L6b-OB Glut", "046 CTX-CGE GABA", "052 Pvalb Gaba", "053 Sst Gaba",
    "054 CNU-MGE GABA", "059 CNU-LGE LSX GABA", "066 CNU-HYa HY GABA",
    "110 CNU-HYa HY MM Glut", "145 MH-LH TH Glut", "151 TH Prkcd Grin2c Glut",
    "155 MB Glut", "191 MB P MY GABA", "215 MB Dopa", "217 P MY Pineal Glut",
    "308 CB GABA",
}

# Overridable by CLI (see main). OUTDIR = where figures are written; CORPUS_LABEL = title suffix.
OUTDIR = HERE
CORPUS_LABEL = "full corpus"

plt.rcParams.update({
    "figure.dpi": 130, "savefig.dpi": 200, "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.25, "grid.linewidth": 0.6,
    "axes.axisbelow": True,
    "svg.fonttype": "none",  # keep text as editable text in the SVG
})

SAVE_FMTS = ["png", "svg"]  # every figure is written in each format


def _save(fig, path):
    path = Path(path)
    for fmt in SAVE_FMTS:
        fig.savefig(path.with_suffix("." + fmt))
    plt.close(fig)
    print("wrote", path.with_suffix(""), "[" + ", ".join(SAVE_FMTS) + "]")


def load():
    fp = {r["target"]: int(r["total_deg05"]) for r in csv.DictReader(FOOTPRINT.open())}
    cell = {}
    for r in csv.DictReader(LEDGER.open()):
        cell[(r["target_gene"], r["finding_id"])] = r["cell_types"]
    rows = []
    for r in csv.DictReader(SCORED.open()):
        g = r["gene_target"]
        key = (g, r["finding_id"])
        try:
            gsig = float(r["gold_significance"])
        except (ValueError, KeyError):
            gsig = np.nan
        rows.append({
            "gene": g, "finding_id": r["finding_id"],
            "finding_type": r["finding_type"],
            "score": float(r["evidence"]),
            "facet": r["winning_facet"],
            "in_gold": r["in_gold"],
            "gold_sig": gsig,
            "footprint": fp.get(g, np.nan),
            "cell_types": [c.strip() for c in cell.get(key, "").split("|")
                           if c.strip() in CELL_WHITELIST],
        })
    return rows


def save_table(rows):
    out = OUTDIR / "analysis_table.csv"
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["gene", "finding_id", "finding_type", "evidence", "winning_facet",
                    "in_gold", "gold_sig", "footprint", "n_cell_types", "cell_types"])
        for r in rows:
            w.writerow([r["gene"], r["finding_id"], r["finding_type"],
                        f"{r['score']:.4f}", r["facet"], r["in_gold"],
                        "" if np.isnan(r["gold_sig"]) else f"{r['gold_sig']:.3f}",
                        "" if np.isnan(r["footprint"]) else int(r["footprint"]),
                        len(r["cell_types"]), "|".join(r["cell_types"])])
    print("wrote", out)


def _median_line(ax, vals, label=True):
    m = np.median(vals)
    ax.axvline(m, color=OI["vermillion"], lw=1.6, ls="--")
    if label:
        ax.text(m, ax.get_ylim()[1] * 0.96, f" median {m:.3f}",
                color=OI["vermillion"], va="top", fontsize=9)


def fig_hist(rows):
    scores = np.array([r["score"] for r in rows])
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    bins = np.linspace(0, scores.max(), 51)
    # Draw bars from a POSITIVE baseline (b0), not 0: a bar bottom at 0 on a log
    # axis maps to -inf and the SVG backend emits a rectangle running off the plot
    # (Agg clips it, most SVG viewers don't). height = count - b0 keeps the bar TOP
    # at `count`, so the log-scale heights are still exact.
    counts, edges = np.histogram(scores, bins=bins)
    b0 = 0.7
    ax.bar(edges[:-1], np.clip(counts - b0, 0, None), width=np.diff(edges),
           align="edge", bottom=b0, color=OI["blue"], alpha=0.85,
           edgecolor="white", linewidth=0.3)
    ax.set_yscale("log")
    ax.set_ylim(b0, counts.max() * 1.4)
    n_floor = int((scores < 0.01).sum())
    ax.axvline(np.median(scores), color=OI["vermillion"], lw=1.6, ls="--")
    ax.text(0.98, 0.96, f"median {np.median(scores):.3f}\n{n_floor:,} of {len(scores):,} "
            f"findings at floor (<0.01)", transform=ax.transAxes, va="top", ha="right",
            fontsize=9, color=OI["vermillion"])
    ax.set_xlabel(SCORE_LABEL)
    ax.set_ylabel("# findings  (log scale)")
    ax.set_title(f"Score distribution (n={len(scores):,} findings, {CORPUS_LABEL})")
    fig.tight_layout()
    p = OUTDIR / "fig1_score_hist.png"
    _save(fig, p)


KDE_NOTE = "filled = score KDE (per-row peak-normalized)"


def _ridgeline(labels, groups, color, title, out, xmax=None, overlap=0.92,
               bw=0.15, figsize=None):
    """Stacked per-group KDEs (ridgeline), ordered like the boxplots (lowest mean
    at bottom). Score is bounded at 0 and zero-inflated, so each KDE is boundary-
    corrected by reflection at 0 and peak-normalized per row. overlap<1 keeps each
    curve inside its own lane (no spill into neighbors)."""
    from scipy.stats import gaussian_kde
    n = len(groups)
    xmax = xmax if xmax is not None else max(float(np.max(g)) for g in groups)
    xs = np.linspace(0.0, xmax, 400)
    fig, ax = plt.subplots(figsize=figsize or (10.2, 0.5 * n + 2.2))
    for i, vals in enumerate(groups):
        vals = np.asarray(vals, float)
        try:
            dens = 2.0 * gaussian_kde(np.concatenate([vals, -vals]), bw_method=bw)(xs)
        except Exception:
            dens = np.zeros_like(xs)
        peak = dens.max()
        if peak > 0:
            dens = dens / peak * overlap
        ax.fill_between(xs, i, i + dens, color=color, alpha=0.72,
                        edgecolor="black", linewidth=0.6, zorder=2 * (n - i))
    # labels centered on each KDE band (not on its baseline)
    ax.set_yticks([i + overlap / 2 for i in range(n)])
    ax.set_yticklabels(labels, fontsize=8.5)
    ax.set_xlim(0, xmax); ax.set_ylim(-0.5, n - 1 + overlap + 0.2)
    ax.set_xlabel(SCORE_LABEL)
    ax.set_title(title, fontsize=12)
    ax.grid(axis="y", visible=False)
    fig.tight_layout()
    _save(fig, out)


def _ridgeline_scoped(labels, groups, color, title, out, lo, hi,
                      overlap=0.92, bw=0.06, figsize=None):
    """Ridgeline zoomed to the score window [lo, hi]. The KDE is fit on the full
    data (reflected at 0) but displayed on [lo, hi] and GLOBALLY scaled, so a
    group's bump height reflects how much mass it has in the window (flat = none).
    Per-row normalization would be degenerate here (the window is a near-ceiling
    spike), so global scaling carries the signal."""
    from scipy.stats import gaussian_kde
    n = len(groups)
    xs = np.linspace(lo, hi, 300)
    dens = []
    for vals in groups:
        vals = np.asarray(vals, float)
        try:
            dens.append(2.0 * gaussian_kde(np.concatenate([vals, -vals]),
                                           bw_method=bw)(xs))
        except Exception:
            dens.append(np.zeros_like(xs))
    gmax = max((d.max() for d in dens), default=0.0) or 1.0
    fig, ax = plt.subplots(figsize=figsize or (8.6, 0.5 * n + 2.2))
    for i, d in enumerate(dens):
        ax.fill_between(xs, i, i + d / gmax * overlap, color=color, alpha=0.72,
                        edgecolor="black", linewidth=0.6, zorder=2 * (n - i))
    # labels centered on each KDE band (not on its baseline)
    ax.set_yticks([i + overlap / 2 for i in range(n)])
    ax.set_yticklabels(labels, fontsize=8.5)
    ax.set_xlim(lo, hi); ax.set_ylim(-0.5, n - 1 + overlap + 0.2)
    ax.set_xlabel(SCORE_LABEL)
    ax.set_title(title, fontsize=11)
    ax.grid(axis="y", visible=False)
    fig.tight_layout()
    _save(fig, out)


def _barplot_share(labels, groups, color, title, out, lo, figsize=None):
    """Horizontal bars: share (%) of each group's findings with score >= lo, raw
    count annotated. Same (mean) row order as the KDE/boxplot panels."""
    n = len(groups)
    fracs = [100.0 * np.mean(np.asarray(g) >= lo) for g in groups]
    counts = [int(np.sum(np.asarray(g) >= lo)) for g in groups]
    fig, ax = plt.subplots(figsize=figsize or (8.2, 0.5 * n + 2.0))
    ax.barh(range(n), fracs, color=color, alpha=0.85, edgecolor="black",
            linewidth=0.6, height=0.7)
    for i, (fr, c) in enumerate(zip(fracs, counts)):
        ax.text(fr + max(fracs) * 0.01, i, f"{c}", va="center", fontsize=8.5)
    ax.set_yticks(range(n)); ax.set_yticklabels(labels, fontsize=8.5)
    ax.set_xlim(0, max(fracs) * 1.12 if max(fracs) > 0 else 1)
    ax.set_xlabel(f"% of findings with score ≥ {lo:g}   (n annotated)")
    ax.set_title(title, fontsize=11)
    ax.grid(axis="y", visible=False)
    fig.tight_layout()
    _save(fig, out)


def _boxplot(ax, groups, labels, colors, vert=False):
    # whis=(0,100): whiskers span the full data range (group min→max), no fliers.
    bp = ax.boxplot(groups, vert=vert, patch_artist=True, widths=0.62,
                    whis=(0, 100), showfliers=False,
                    medianprops=dict(color="black", lw=1.4))
    for patch, c in zip(bp["boxes"], colors):
        patch.set_facecolor(c); patch.set_alpha(0.75); patch.set_edgecolor("black")
        patch.set_linewidth(0.7)
    return bp


def fig_by_celltype(rows, top_n=25):
    from collections import defaultdict
    by_ct = defaultdict(list)
    n_empty = 0
    for r in rows:
        if not r["cell_types"]:
            n_empty += 1
        for c in r["cell_types"]:
            by_ct[c].append(r["score"])
    top = sorted(by_ct, key=lambda c: len(by_ct[c]), reverse=True)[:top_n]
    # order displayed by mean score (median ~ floor under zero-inflation)
    top = sorted(top, key=lambda c: np.mean(by_ct[c]))
    groups = [by_ct[c] for c in top]
    labels = [f"{c}  (n={len(by_ct[c])})" for c in top]
    fig, ax = plt.subplots(figsize=(9.4, 8.8))
    _boxplot(ax, groups, labels, [OI["sky"]] * len(top), vert=False)
    ax.plot([np.mean(g) for g in groups], range(1, len(top) + 1), "D",
            color=OI["vermillion"], ms=6, zorder=5)
    ax.set_yticks(range(1, len(top) + 1)); ax.set_yticklabels(labels, fontsize=8.5)
    ax.set_xlabel(SCORE_LABEL)
    ax.set_title(f"Score by cell type — {len(top)} canonical cell groups (ordered by mean)\n"
                 f"{MEAN_NOTE}", fontsize=12)
    ax.text(0.99, 0.01, f"{n_empty} of {len(rows)} findings mention none of the "
            f"{len(CELL_WHITELIST)}", transform=ax.transAxes, ha="right", va="bottom",
            fontsize=8.5, color=OI["grey"])
    fig.tight_layout()
    p = OUTDIR / "fig2_score_by_celltype.png"
    _save(fig, p)

    # KDE ridgeline version (same ordering)
    _ridgeline(labels, groups, OI["sky"],
               f"Score KDE by cell type — {len(top)} canonical cell groups "
               f"(ordered by mean)\n{KDE_NOTE}",
               OUTDIR / "fig2_score_by_celltype_kde.png", figsize=(9.6, 9.2))
    hi = max(max(g) for g in groups)
    _ridgeline_scoped(labels, groups, OI["sky"],
                      f"Score KDE by cell type, tail only  (score ∈ [3.0, {hi:.2f}])\n"
                      f"filled = KDE, globally scaled → bump ∝ ceiling mass",
                      OUTDIR / "fig2_score_by_celltype_kde_ge3.png", 3.0, hi,
                      figsize=(8.4, 9.2))


def fig_by_footprint(rows):
    edges = [-0.5, 0.5, 10, 50, 200, 1000, np.inf]
    labels = ["0", "1–10", "11–50", "51–200", "201–1000", ">1000"]
    groups = [[] for _ in labels]
    for r in rows:
        fpv = r["footprint"]
        if np.isnan(fpv):
            continue
        for i in range(len(labels)):
            if edges[i] < fpv <= edges[i + 1]:
                groups[i].append(r["score"]); break
    counts = [len(g) for g in groups]
    fig, ax = plt.subplots(figsize=(7.8, 4.6))
    _boxplot(ax, groups, labels, [OI["orange"]] * len(labels), vert=True)
    ax.set_xticks(range(1, len(labels) + 1))
    ax.set_xticklabels([f"{l}\n(n={c})" for l, c in zip(labels, counts)], fontsize=9)
    # diamond = group mean (no connecting line), matching the cell-type panel
    means = [np.mean(g) if g else np.nan for g in groups]
    ax.plot(range(1, len(labels) + 1), means, "D", color=OI["vermillion"], ms=7,
            zorder=5)
    ax.set_xlabel("target DEG footprint  (total genes FDR<0.05 across cell types)")
    ax.set_ylabel(SCORE_LABEL)
    ax.set_title(f"Score vs target transcriptional footprint\n{MEAN_NOTE}", fontsize=11)
    fig.tight_layout()
    p = OUTDIR / "fig3_score_by_footprint.png"
    _save(fig, p)


def fig_by_facet(rows):
    keys = ["conv", "ectopy", "bm_div"]
    groups = [[r["score"] for r in rows if r["facet"] == k] for k in keys]
    fig, ax = plt.subplots(figsize=(7.4, 4.8))
    _boxplot(ax, groups, keys, [FACET_COLOR[k] for k in keys], vert=True)
    means = [np.mean(g) for g in groups]
    ax.plot(range(1, len(keys) + 1), means, "D", color=OI["vermillion"], ms=8,
            zorder=5)
    ax.set_xticks(range(1, len(keys) + 1))
    ax.set_xticklabels([f"{FACET_LABEL[k]}\nn={len(g)}  ·  μ={np.mean(g):.2f}  ·  "
                        f"m={np.median(g):.3f}" for k, g in zip(keys, groups)],
                       fontsize=9)
    ax.set_ylabel(SCORE_LABEL)
    ax.set_title(f"Score by winning facet\n{MEAN_NOTE}", fontsize=11)
    fig.tight_layout()
    p = OUTDIR / "fig4_score_by_facet.png"
    _save(fig, p)


def fig_by_findingtype(rows):
    from collections import defaultdict
    by_ft = defaultdict(list)
    for r in rows:
        by_ft[r["finding_type"]].append(r["score"])
    order = sorted(by_ft, key=lambda t: np.mean(by_ft[t]))
    groups = [by_ft[t] for t in order]
    labels = [f"{t}  (n={len(by_ft[t])})" for t in order]
    fig, ax = plt.subplots(figsize=(8.8, 0.55 * len(order) + 1.9))
    _boxplot(ax, groups, labels, [OI["purple"]] * len(order), vert=False)
    ax.plot([np.mean(g) for g in groups], range(1, len(order) + 1), "D",
            color=OI["vermillion"], ms=6, zorder=5)
    ax.set_yticks(range(1, len(order) + 1)); ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel(SCORE_LABEL)
    ax.set_title(f"Score by finding type  (ordered by mean)\n{MEAN_NOTE}", fontsize=11)
    fig.tight_layout()
    p = OUTDIR / "fig5_score_by_findingtype.png"
    _save(fig, p)


def fig_vs_goldsig(rows):
    xy = [(r["gold_sig"], r["score"], r["facet"])
          for r in rows if not np.isnan(r["gold_sig"])]
    x = np.array([a for a, _, _ in xy]); y = np.array([b for _, b, _ in xy])
    fig, ax = plt.subplots(figsize=(7.6, 5.0))
    for k in ["bm_div", "ectopy", "conv"]:
        m = [i for i, (_, _, kk) in enumerate(xy) if kk == k]
        ax.scatter(x[m], y[m], s=16, color=FACET_COLOR[k], alpha=0.6,
                   edgecolor="none", label=f"{k} (n={len(m)})")
    r_pear = np.corrcoef(x, y)[0, 1]
    ax.set_xlabel("gold significance")
    ax.set_ylabel(SCORE_LABEL)
    ax.set_title(f"Score vs gold significance  (gold subset, n={len(x)}, r={r_pear:.2f})")
    # legend outside the axes (right) so it can't overlap points or title
    ax.legend(frameon=False, fontsize=9, title="winning facet",
              loc="upper left", bbox_to_anchor=(1.01, 1.0))
    fig.tight_layout()
    p = OUTDIR / "fig6_score_vs_goldsig.png"
    _save(fig, p)


def _clean_pathway(name):
    for pre in ("REACTOME_", "HALLMARK_", "GOBP_"):
        if name.startswith(pre):
            name = name[len(pre):]
    return name.replace("_", " ").title()


def _ora_top(rel_targets, lib, top_n=10, padj=0.05):
    """Top pathways in `lib`, ranked by # distinct relational targets significantly
    enriched (padj<threshold) in >=1 cell type."""
    df = pd.read_parquet(ORA_GT, columns=["gene_target", "lib", "pathway", "padj"])
    df = df[(df["lib"] == lib) & (df["padj"] < padj) &
            (df["gene_target"].isin(rel_targets))]
    df["name"] = df["pathway"].str.split("::").str[-1].map(_clean_pathway)
    counts = df.groupby("name")["gene_target"].nunique().sort_values(ascending=False)
    n_targets = df["gene_target"].nunique()
    return counts.head(top_n), n_targets


def fig_pathways(rows):
    def _short(n, w=46):
        return n if len(n) <= w else n[:w - 1] + "…"

    rel_targets = {r["gene"] for r in rows}
    counts, n_tgt = _ora_top(rel_targets, "Reactome", top_n=10)
    names = [_short(n) for n in counts.index[::-1]]; vals = counts.values[::-1]
    fig, ax = plt.subplots(figsize=(11.0, 5.4))
    ax.barh(range(len(names)), vals, color=OI["green"], alpha=0.85,
            edgecolor="black", linewidth=0.6)
    ax.set_yticks(range(len(names))); ax.set_yticklabels(names, fontsize=9.5)
    for i, v in enumerate(vals):
        ax.text(v + 0.6, i, str(int(v)), va="center", fontsize=9)
    ax.set_xlim(0, vals.max() * 1.12)
    ax.set_xlabel("# targets with pathway enriched  (ORA padj<0.05)")
    ax.set_title(f"Top 10 Reactome pathways — {CORPUS_LABEL}\n"
                 f"ORA of ground-truth DEGs (Fig1 ora_gt); {n_tgt} of "
                 f"{len(rel_targets)} targets have ≥1 significant term", fontsize=12)
    fig.tight_layout()
    p = OUTDIR / "fig7_top_pathways.png"
    _save(fig, p)

    # companion: three libraries side by side
    libs = ["Reactome", "Hallmark", "GO_BP"]
    colors = [OI["green"], OI["orange"], OI["blue"]]
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.6))
    for ax, lib, col in zip(axes, libs, colors):
        c, nt = _ora_top(rel_targets, lib, top_n=10)
        nm = c.index[::-1]; vv = c.values[::-1]
        ax.barh(range(len(nm)), vv, color=col, alpha=0.85,
                edgecolor="black", linewidth=0.6)
        ax.set_yticks(range(len(nm)))
        ax.set_yticklabels([n if len(n) <= 42 else n[:40] + "…" for n in nm],
                           fontsize=8)
        ax.set_title(f"{lib}  ({nt} targets)", fontsize=11)
        ax.set_xlabel("# targets enriched")
        ax.margins(x=0.14)
    fig.suptitle(f"Top 10 pathways per library across the {CORPUS_LABEL} "
                 "(ORA padj<0.05 of ground-truth DEGs)", fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    p = OUTDIR / "fig7b_top_pathways_bylib.png"
    _save(fig, p)

    # write the ranked table for all three libs
    out = OUTDIR / "top_pathways.csv"
    recs = []
    for lib in libs:
        c, _ = _ora_top(rel_targets, lib, top_n=25)
        for rank, (nm, n) in enumerate(c.items(), 1):
            recs.append({"lib": lib, "rank": rank, "pathway": nm, "n_targets": int(n)})
    pd.DataFrame(recs).to_csv(out, index=False)
    print("wrote", out)


def fig_by_target_pathway(rows):
    """Score distribution of findings grouped by their TARGET's functional pathway
    category (curated marker sets — see pathway_categories.py). Answers: do targets
    in a given pathway carry systematically higher/lower scores?"""
    import sys
    sys.path.insert(0, str(HERE))
    from pathway_categories import classify
    from collections import defaultdict
    scores, tgts = defaultdict(list), defaultdict(set)
    for r in rows:
        c = classify(r["gene"])
        scores[c].append(r["score"]); tgts[c].add(r["gene"])
    cats = sorted([c for c in scores if scores[c]], key=lambda c: np.mean(scores[c]))
    groups = [scores[c] for c in cats]
    labels = [f"{c}  ({len(tgts[c])} targets)" for c in cats]
    fig, ax = plt.subplots(figsize=(10.2, 0.62 * len(cats) + 2.0))
    _boxplot(ax, groups, labels, [OI["green"]] * len(cats), vert=False)
    ax.plot([np.mean(g) for g in groups], range(1, len(cats) + 1), "D",
            color=OI["vermillion"], ms=6, zorder=5)
    ax.set_yticks(range(1, len(cats) + 1)); ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel(SCORE_LABEL)
    mean_all = np.mean([r["score"] for r in rows])
    ax.axvline(mean_all, color=OI["grey"], ls=":", lw=1.4, zorder=1)
    ax.text(mean_all, 0.015, f" overall mean {mean_all:.2f}", color=OI["grey"],
            fontsize=8.5, ha="left", va="bottom", transform=ax.get_xaxis_transform())
    ax.set_title("Score by target pathway category  (ordered by mean)\n"
                 f"{MEAN_NOTE}", fontsize=12)
    fig.tight_layout()
    p = OUTDIR / "fig8_score_by_target_pathway.png"
    _save(fig, p)

    hi = max(max(g) for g in groups)
    _ridgeline_scoped(labels, groups, OI["green"],
                      f"Target pathway score KDE, tail only  (score ∈ [3.0, {hi:.2f}])\n"
                      f"filled = KDE, globally scaled → bump ∝ ceiling mass",
                      OUTDIR / "fig8_score_by_target_pathway_kde_ge3.png", 3.0, hi,
                      figsize=(8.6, 0.62 * len(cats) + 2.0))


def _short_db(name, w=52):
    name = str(name).strip()
    name = name[0:1].upper() + name[1:]  # capitalize (GO terms are lowercase)
    return name if len(name) <= w else name[:w - 1] + "…"


def fig_db_pathways(rows, top_n=15, min_targets=10, min_findings=25):
    """Data-driven analog of fig8: instead of curated categories, rank standard
    database pathways (Hallmark / Reactome / GO:BP) by the mean score of findings
    whose TARGET is a member of the set. Membership is many-to-many, so this is a
    ranking, not a partition. One panel per library."""
    from collections import defaultdict
    mem = pd.read_parquet(GENE_MEMBERSHIP, columns=["gene", "resource", "set_name"])
    scores = defaultdict(list)
    for r in rows:
        scores[r["gene"]].append(r["score"])
    keys = set(scores)
    overall = float(np.mean([s for v in scores.values() for s in v]))

    libs = [("MSigDB:MH", "Hallmark", "hallmark", OI["orange"]),
            ("reactome", "Reactome", "reactome", OI["green"]),
            ("GO:BP", "GO:BP", "gobp", OI["blue"])]
    allrecs = []
    for res, name, slug, col in libs:
        sub = mem[mem["resource"] == res]
        recs = []
        for setname, grp in sub.groupby("set_name"):
            genes = set(grp["gene"]) & keys
            if len(genes) < min_targets:
                continue
            vals = [s for g in genes for s in scores[g]]
            if len(vals) < min_findings:
                continue
            recs.append((float(np.mean(vals)), len(genes), vals, str(setname).strip()))
        recs.sort(key=lambda x: x[0], reverse=True)
        for mean, nt, vals, nm in recs:
            allrecs.append({"library": name, "pathway": nm, "n_targets": nt,
                            "n_findings": len(vals), "mean_score": round(mean, 4)})
        top = recs[:top_n][::-1]  # ascending → best at top of horizontal axis
        groups = [t[2] for t in top]
        labels = [f"{_short_db(t[3])}  ({t[1]} targets)" for t in top]
        fig, ax = plt.subplots(figsize=(10.6, 0.5 * len(top) + 2.0))
        _boxplot(ax, groups, labels, [col] * len(top), vert=False)
        ax.plot([np.mean(g) for g in groups], range(1, len(top) + 1), "D",
                color=OI["vermillion"], ms=6, zorder=5)
        ax.set_yticks(range(1, len(top) + 1)); ax.set_yticklabels(labels, fontsize=8.5)
        ax.axvline(overall, color=OI["grey"], ls=":", lw=1.4, zorder=1)
        ax.text(overall, 0.015, f" overall mean {overall:.2f}", color=OI["grey"],
                fontsize=8.5, ha="left", va="bottom",
                transform=ax.get_xaxis_transform())
        ax.set_xlabel(SCORE_LABEL)
        ax.set_title(f"Top {len(top)} {name} pathways by mean target score — "
                     f"{CORPUS_LABEL}\n{MEAN_NOTE}", fontsize=11)
        ax.text(0.0, -0.11, f"sets with ≥{min_targets} member targets & ≥{min_findings} "
                f"findings", transform=ax.transAxes,
                fontsize=8, color=OI["grey"], ha="left", va="top")
        fig.tight_layout()
        p = OUTDIR / f"fig9_{slug}_target_pathway.png"
        _save(fig, p)

        # KDE ridgeline version (same top-N, same ordering)
        _ridgeline(labels, groups, col,
                   f"Top {len(top)} {name} pathways: score KDE — {CORPUS_LABEL}\n"
                   f"{KDE_NOTE}",
                   OUTDIR / f"fig9_{slug}_target_pathway_kde.png",
                   figsize=(10.6, 0.55 * len(top) + 2.2))
        hi = max(max(g) for g in groups)
        _ridgeline_scoped(labels, groups, col,
                          f"Top {len(top)} {name} pathways — score KDE, tail ∈ "
                          f"[3.0, {hi:.2f}]\n"
                          f"filled = KDE, globally scaled → bump ∝ ceiling mass",
                          OUTDIR / f"fig9_{slug}_target_pathway_kde_ge3.png",
                          3.0, hi, figsize=(9.4, 0.55 * len(top) + 2.2))
    out = OUTDIR / "target_pathway_db_ranked.csv"
    pd.DataFrame(allrecs).to_csv(out, index=False)
    print("wrote", out)


_DEG_XLABEL = "target DEG footprint  (total genes FDR<0.05 across cell types)"


def _target_score_deg(rows):
    """Per target: DEG footprint (x) and mean score of its findings (y)."""
    from collections import defaultdict
    sc, fp = defaultdict(list), {}
    for r in rows:
        sc[r["gene"]].append(r["score"]); fp[r["gene"]] = r["footprint"]
    genes = [g for g in sc if not np.isnan(fp.get(g, np.nan))]
    x = np.array([fp[g] for g in genes], float)
    y = np.array([np.mean(sc[g]) for g in genes])
    return genes, x, y


def _lowess_curve(x, y, frac=0.3):
    """LOWESS of y on log10(DEG+1); returns (deg, smoothed) sorted for plotting.
    it=0 (local mean, matching the plotted mean-score) so it traces the real hump
    (rise then fall) instead of a median-like monotonic drift; robust iterations
    would suppress the hump. Warning suppressed: harmless divide from tied DEG values."""
    import warnings
    from statsmodels.nonparametric.smoothers_lowess import lowess
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sm = lowess(y, np.log10(x + 1.0), frac=frac, it=0, return_sorted=True)
    sm = sm[~np.isnan(sm[:, 1])]
    return 10 ** sm[:, 0] - 1.0, sm[:, 1]


def _lowess_ci(x, y, frac=0.3, B=250, grid=90):
    """LOWESS fit + 95% bootstrap CI band, evaluated on a log-DEG grid. The band is
    honest about a weak/noisy, non-monotonic relationship: tight where DEG is dense
    (~1-1000), very wide at the extremes (unstable DEG=0 mean; sparse high-DEG tail)."""
    import warnings
    from statsmodels.nonparametric.smoothers_lowess import lowess
    lx = np.log10(x + 1.0)
    glx = np.linspace(0, lx.max(), grid)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fit = lowess(y, lx, frac=frac, it=0, return_sorted=True)
        fitg = np.interp(glx, fit[:, 0], fit[:, 1])
        boot = np.empty((B, grid))
        for b in range(B):
            i = np.random.randint(0, len(y), len(y))
            s = lowess(y[i], lx[i], frac=frac, it=0, return_sorted=True)
            boot[b] = np.interp(glx, s[:, 0], s[:, 1])
    lo = np.nanpercentile(boot, 2.5, axis=0)
    hi = np.nanpercentile(boot, 97.5, axis=0)
    return 10 ** glx - 1.0, fitg, lo, hi


def fig_score_vs_deg(rows):
    """One dot per target: x = DEG footprint (symlog so the 0-footprint column and
    the long tail both show), y = mean score of that target's findings, + a LOWESS
    smoother that traces the (non-monotonic) trend faithfully."""
    genes, x, y = _target_score_deg(rows)
    fig, ax = plt.subplots(figsize=(8.6, 5.8))
    ax.scatter(x, y, s=13, color=OI["blue"], alpha=0.4, edgecolor="none", zorder=2)
    ax.set_xscale("symlog", linthresh=1)
    dg, fit, lo, hi = _lowess_ci(x, y)
    ax.fill_between(dg, lo, hi, color=OI["vermillion"], alpha=0.2, lw=0, zorder=2.5)
    ax.plot(dg, fit, color=OI["vermillion"], lw=2.4, zorder=3)
    ax.set_xlabel(_DEG_XLABEL)
    ax.set_ylabel(f"mean {SCORE_LABEL} per target")
    ax.set_title(f"Score vs DEG footprint — {CORPUS_LABEL}\n"
                 f"one dot = one target ({len(genes):,} targets) · "
                 f"red = LOWESS ± 95% bootstrap CI", fontsize=11)
    ax.margins(y=0.03)
    fig.tight_layout()
    _save(fig, OUTDIR / "fig10_score_vs_deg.png")


def fig_score_vs_deg_density(rows):
    """Density (hexbin) version — resolves the heavily overplotted low-DEG columns
    (esp. DEG=0). x = log10(DEG+1) with DEG-value ticks; log-count color; LOWESS overlay."""
    genes, x, y = _target_score_deg(rows)
    lx = np.log10(x + 1.0)
    fig, ax = plt.subplots(figsize=(9.0, 5.8))
    hb = ax.hexbin(lx, y, gridsize=32, bins="log", cmap="Blues", mincnt=1)
    fig.colorbar(hb, ax=ax, label="targets per bin (log scale)", pad=0.02)
    dx, dy = _lowess_curve(x, y)
    ax.plot(np.log10(dx + 1.0), dy, color=OI["vermillion"], lw=2.4, zorder=3)
    ticks = [0, 1, 10, 100, 1000, 10000]
    ax.set_xticks([np.log10(t + 1.0) for t in ticks])
    ax.set_xticklabels([f"{t:,}" for t in ticks])
    ax.set_xlim(-0.05, lx.max() + 0.05)
    ax.set_xlabel(_DEG_XLABEL)
    ax.set_ylabel(f"mean {SCORE_LABEL} per target")
    ax.set_title(f"Score vs DEG footprint (density) — {CORPUS_LABEL}\n"
                 f"{len(genes):,} targets · hexbin, log count · red = LOWESS",
                 fontsize=10.5)
    fig.tight_layout()
    _save(fig, OUTDIR / "fig10b_score_vs_deg_density.png")


def fig_score_by_deg_violin(rows):
    """Binned-violin view of the same relationship: per-target score distribution
    within each DEG-footprint bin. Violin = reflected-at-0 KDE (so it can't leak
    below 0); inner box = median/IQR; the median line traces the hump across bins."""
    from scipy.stats import gaussian_kde
    genes, x, y = _target_score_deg(rows)
    edges = [-0.5, 0.5, 10, 50, 200, 1000, np.inf]
    labels = ["0", "1–10", "11–50", "51–200", "201–1000", ">1000"]
    groups = [[] for _ in labels]
    for xi, yi in zip(x, y):
        for i in range(len(labels)):
            if edges[i] < xi <= edges[i + 1]:
                groups[i].append(yi); break
    keep = [(l, np.asarray(g)) for l, g in zip(labels, groups) if len(g) >= 5]
    ymax = float(max(y))
    ys = np.linspace(0, ymax, 220)
    fig, ax = plt.subplots(figsize=(8.8, 5.4))
    for i, (l, g) in enumerate(keep, start=1):
        try:
            dens = 2.0 * gaussian_kde(np.concatenate([g, -g]))(ys)
        except Exception:
            continue
        dens = dens / dens.max() * 0.42
        ax.fill_betweenx(ys, i - dens, i + dens, color=OI["orange"], alpha=0.6,
                         edgecolor="black", lw=0.7, zorder=2)
    ax.boxplot([g for _, g in keep], positions=range(1, len(keep) + 1), widths=0.10,
               showfliers=False, patch_artist=True,
               medianprops=dict(color="black", lw=1.5),
               boxprops=dict(facecolor="white", edgecolor="black", lw=0.8),
               whiskerprops=dict(color="black", lw=0.8),
               capprops=dict(color="black", lw=0.8), zorder=3)
    ax.plot(range(1, len(keep) + 1), [np.median(g) for _, g in keep], "-",
            color=OI["vermillion"], lw=1.6, alpha=0.8, zorder=4)
    ax.set_xticks(range(1, len(keep) + 1))
    ax.set_xticklabels([f"{l}\n(n={len(g)})" for l, g in keep], fontsize=9)
    ax.set_ylim(-0.05, ymax * 1.03)
    ax.set_xlabel(_DEG_XLABEL)
    ax.set_ylabel(f"mean {SCORE_LABEL} per target")
    ax.set_title(f"Score by DEG-footprint bin — {CORPUS_LABEL}\n"
                 f"violin = per-target KDE (reflected at 0) · box = median/IQR · "
                 f"red = median trend", fontsize=10.5)
    fig.tight_layout()
    _save(fig, OUTDIR / "fig10c_score_by_deg_violin.png")


def main():
    import argparse
    global SCORED, OUTDIR, CORPUS_LABEL
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--scored", type=Path, default=SCORED,
                    help="ranked-fusion CSV (evidence score). Default: full corpus.")
    ap.add_argument("--outdir", type=Path, default=OUTDIR,
                    help="output directory for figures/tables. Default: script dir.")
    ap.add_argument("--label", default=CORPUS_LABEL,
                    help="corpus label used in plot titles.")
    args = ap.parse_args()
    SCORED, CORPUS_LABEL = args.scored, args.label
    OUTDIR = args.outdir
    OUTDIR.mkdir(parents=True, exist_ok=True)
    print(f"input : {SCORED}\noutdir: {OUTDIR}\nlabel : {CORPUS_LABEL}")

    rows = load()
    print(f"loaded {len(rows)} scored findings")
    save_table(rows)
    fig_hist(rows)
    fig_by_celltype(rows)
    fig_by_footprint(rows)
    fig_by_facet(rows)
    fig_by_findingtype(rows)
    fig_vs_goldsig(rows)
    fig_pathways(rows)
    fig_by_target_pathway(rows)
    fig_db_pathways(rows)
    fig_score_vs_deg(rows)
    fig_score_vs_deg_density(rows)
    fig_score_by_deg_violin(rows)


if __name__ == "__main__":
    main()
