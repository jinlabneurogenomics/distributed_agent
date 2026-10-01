#!/usr/bin/env python3
"""
Fig 2g — expanded Category-1 set (27 targets) organized by mechanistic family, on the
cell-class × DEG matrix. Built after the 5-agent literature sweep over the 107 candidates.

  (A) full cell-class × DEG matrix (23 × 1,919, DEG-sorted, brown log) with all 27 Category-1
      targets marked as columns + finding-cell dots — regime context.
  (B) focused 23 × 27 zoom grouped by family (family header bar + separators); per-(target,cell)
      nDEG coloured, finding cells boxed with their nDEG — the low-signal regime, at scale.

Source: cache/category1_expanded.csv (8 locked + 19 sweep-confirmed; lit-checked, PMIDs inside),
DEG matrix cache/deg_coverage_matrix.csv.

    python3 manuscript/fig2/g/build_category1_families.py
"""
from __future__ import annotations
import os, pathlib
os.environ.setdefault("MPLCONFIGDIR", "/tmp/mplconfig_fig2g")
pathlib.Path(os.environ["MPLCONFIGDIR"]).mkdir(parents=True, exist_ok=True)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap, LogNorm
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[2]
STYLE = REPO / "src" / "figures" / "style.mplstyle"
CACHE = HERE / "cache"
# Colour floor is a pale tan (not white) so nDEG=1 (bottom of the LogNorm) is visibly
# distinct from a truly-empty nDEG=0 cell, which is masked to white below. Without this the
# lowest measured value and "no DEG" are both white and can't be told apart.
DEG_CMAP = LinearSegmentedColormap.from_list("DEGbrown", ["#ecddcb", "#7a4a28"])
# empty (masked) cells → opaque white, not transparent. Same as figG_deg_coverage: a
# transparent bad-colour makes matplotlib anti-alias the alpha at every cell edge, which
# Illustrator then renders as a mesh of seam lines over the heatmap.
DEG_CMAP.set_bad("white")
HL = "#2c7fb8"
CANON_ORDER = ["001 L5-6 IT Glut","005 L4-5 IT CTX Glut","007 L2-3 IT CTX Glut",
 "008 L2-3 IT ENT PPP RSP Glut","009 L2-3 IT PIR AON ENT Glut","022 L5 ET CTX Glut",
 "027 NP-CT-L6b-OB Glut","012 MEA LA CA1 DG Glut","017 CA3 CA2-FC DG Glut","046 CTX-CGE GABA",
 "052 Pvalb Gaba","053 Sst Gaba","054 CNU-MGE GABA","059 CNU-LGE LSX GABA","066 CNU-HYa HY GABA",
 "110 CNU-HYa HY MM Glut","145 MH-LH TH Glut","151 TH Prkcd Grin2c Glut","155 MB Glut",
 "191 MB P MY GABA","215 MB Dopa","217 P MY Pineal Glut","308 CB GABA"]
ROW = {c: i for i, c in enumerate(CANON_ORDER)}
# family display order (multi-member families first)
FAM_ORDER = ["ether-lipid→sterol","chromatin derepression","neurotrophin RAS-ERK→Vgf",
             "sterol/SREBP","tubulin autoregulation","activity-dependent IEG",
             "UPR/ER-chaperone","integrated stress response","TF target/complex",
             "chaperone/HSF1","cytoskeletal/axon","mito biogenesis","IFN/MHC-I"]
FAM_SHORT = {"ether-lipid→sterol":"ether-lipid\n→ sterol","chromatin derepression":"chromatin\nderepression",
             "neurotrophin RAS-ERK→Vgf":"RAS-ERK\n→ Vgf","sterol/SREBP":"sterol/\nSREBP",
             "tubulin autoregulation":"tubulin\nautoreg.","activity-dependent IEG":"activity\nIEG",
             "UPR/ER-chaperone":"UPR","integrated stress response":"ISR\n(ATF4)",
             "TF target/complex":"TF\ntarget","chaperone/HSF1":"HSF1","cytoskeletal/axon":"axon",
             "mito biogenesis":"mito-\nbiogen.","IFN/MHC-I":"IFN/\nMHC-I"}


def main():
    ex = pd.read_csv(CACHE / "category1_expanded.csv")
    ex["cells"] = ex.cell_types.fillna("").apply(lambda s: [c for c in s.split("|") if c])
    dm = pd.read_csv(CACHE / "deg_coverage_matrix.csv")
    dm = dm[dm["cell_class"].isin(CANON_ORDER)].set_index("cell_class").reindex(CANON_ORDER)
    D = dm.to_numpy(dtype=float); cols = list(dm.columns); cidx = {g: j for j, g in enumerate(cols)}
    ncols = D.shape[1]; burden_curve = D.sum(axis=0)
    # shared log scale = same as figG_deg_coverage (LogNorm over the full DEG matrix max),
    # used by both panels so colours are comparable rather than stretched to each subset.
    dnorm = LogNorm(vmin=1, vmax=float(D.max()))

    # column order: family (FAM_ORDER) then burden asc
    ex["famrank"] = ex.family.apply(lambda f: FAM_ORDER.index(f) if f in FAM_ORDER else 99)
    ex = ex.sort_values(["famrank", "deg_burden"]).reset_index(drop=True)
    order = list(ex.target)
    fam_of = dict(zip(ex.target, ex.family))

    if STYLE.exists(): plt.style.use(str(STYLE))
    plt.rcParams.update({"savefig.bbox": "tight", "savefig.pad_inches": 0.04})

    fig = plt.figure(figsize=(9.6, 6.6))
    gs = GridSpec(3, 1, figure=fig, height_ratios=[0.11, 0.78, 1.25], hspace=0.62,
                  left=0.14, right=0.90, top=0.91, bottom=0.20)
    ax_top = fig.add_subplot(gs[0]); axA = fig.add_subplot(gs[1], sharex=ax_top)
    axB = fig.add_subplot(gs[2])

    # ---- Panel A ----
    axA.imshow(np.where(D >= 1, D, np.nan), aspect="auto", cmap=DEG_CMAP,
               norm=dnorm, interpolation="nearest",
               origin="upper", extent=[0, ncols, len(CANON_ORDER), 0])
    axA.set_facecolor("white"); axA.set_xlim(0, ncols)
    axA.set_yticks(np.arange(len(CANON_ORDER)) + 0.5)
    axA.set_yticklabels(CANON_ORDER, fontsize=4.4); axA.tick_params(axis="y", length=0)
    axA.tick_params(axis="x", labelsize=6)
    axA.set_xlabel(f"perturbation target (n={ncols:,}, sorted by total DEG burden ↓)", fontsize=6)
    for s in ("top", "right"): axA.spines[s].set_color("#cccccc")
    for tgt in order:
        j = cidx.get(tgt)
        if j is None: continue
        axA.axvline(j + 0.5, color=HL, lw=0.4, alpha=0.5, zorder=3)
        ax_top.axvline(j + 0.5, color=HL, lw=0.4, alpha=0.6)
        for c in ex[ex.target == tgt].cells.iloc[0]:
            if c in ROW: axA.plot(j + 0.5, ROW[c] + 0.5, "o", ms=1.8, mfc=HL, mec="white", mew=0.25, zorder=5)
    ax_top.fill_between(np.arange(ncols) + 0.5, np.log10(burden_curve + 1), step="mid", color="#9c6b4a", lw=0)
    ax_top.set_ylim(0, np.log10(burden_curve.max() + 1) * 1.05); ax_top.set_yticks([])
    ax_top.set_ylabel("DEG\nburden", fontsize=5, rotation=0, ha="right", va="center")
    ax_top.yaxis.set_label_coords(-0.015, 0.5)
    plt.setp(ax_top.get_xticklabels(), visible=False); ax_top.tick_params(length=0)
    for s in ("top", "right", "left"): ax_top.spines[s].set_visible(False)
    axA.set_title("A  All 27 Category-1 targets on the full cell-class × DEG matrix (blue = target column, dot = finding cell class)",
                  fontsize=6.6, loc="left", pad=4)

    # ---- Panel B: focused 23 x 27, grouped by family ----
    M = np.column_stack([D[:, cidx[t]] if t in cidx else np.zeros(len(CANON_ORDER)) for t in order])
    imB = axB.imshow(np.where(M >= 1, M, np.nan), aspect="auto", cmap=DEG_CMAP,
                     norm=dnorm, interpolation="nearest",
                     origin="upper", extent=[0, len(order), len(CANON_ORDER), 0])
    axB.set_facecolor("white")
    axB.set_yticks(np.arange(len(CANON_ORDER)) + 0.5)
    axB.set_yticklabels(CANON_ORDER, fontsize=4.6); axB.tick_params(axis="y", length=0)
    axB.set_xticks(np.arange(len(order)) + 0.5)
    axB.set_xticklabels([f"{t} ({int(ex[ex.target==t].deg_burden.iloc[0])})" for t in order],
                        fontsize=4.9, rotation=90)
    axB.tick_params(axis="x", length=0)
    for jj, tgt in enumerate(order):
        for c in ex[ex.target == tgt].cells.iloc[0]:
            if c not in ROW: continue
            i = ROW[c]
            axB.add_patch(Rectangle((jj + 0.08, i + 0.08), 0.84, 0.84, fill=False, edgecolor=HL, lw=0.7, zorder=6))
            v = int(M[i, jj])
            axB.text(jj + 0.5, i + 0.5, str(v), ha="center", va="center", fontsize=3.6,
                     color=HL if dnorm(v) < 0.6 else "white", zorder=7, fontweight="bold")
    # family separators + header labels (stagger to avoid collisions among 1-column families)
    b = 0; k = 0
    for fam in FAM_ORDER:
        n = int((ex.family == fam).sum())
        if n == 0: continue
        if b > 0: axB.axvline(b, color="#444444", lw=0.7, zorder=8)
        ytext = -1.1 if (n > 1 or k % 2 == 0) else -3.0
        axB.annotate(FAM_SHORT.get(fam, fam), xy=(b + n / 2, 0), xytext=(b + n / 2, ytext),
                     fontsize=4.6, color="#333333", ha="center", va="bottom", annotation_clip=False)
        b += n; k += 1
    for s in ("top", "right"): axB.spines[s].set_color("#cccccc")
    axB.set_title("B  grouped by mechanistic family — box = finding cell class, number = nDEG@padj<0.1 in that cell",
                  fontsize=6.6, loc="left", pad=20)

    cb = fig.colorbar(imB, ax=axB, fraction=0.02, pad=0.01)
    cb.set_label("nDEG\n(padj<0.1)", fontsize=5); cb.ax.tick_params(labelsize=4.5, length=2)
    cbticks = [t for t in (1, 10, 100, 1000) if t <= float(D.max())]
    cb.set_ticks(cbticks); cb.set_ticklabels([str(t) for t in cbticks]); cb.outline.set_linewidth(0.4)

    fig.suptitle(f"Positive concordance at low DEG — {len(ex)} literature-confirmed targets "
                 f"across {ex.family.nunique()} mechanistic families",
                 fontsize=8.4, fontweight="bold", x=0.14, ha="left", y=0.975)

    for ext in ("svg", "pdf"): fig.savefig(HERE / f"figG_category1_families.{ext}")
    fig.savefig(HERE / "figG_category1_families.png", dpi=300)
    plt.close(fig)
    print(f"wrote figG_category1_families.{{svg,pdf,png}}  ({len(ex)} targets, {ex.family.nunique()} families)")


if __name__ == "__main__":
    main()
