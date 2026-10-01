"""GT expansion for q7 depletion eval, cell group '151 TH Prkcd Grin2c Glut'.

Q1: Of the top-100 depletion hits, what is the DEG distribution in this cell group?
    How many are null hits (0 DEGs) vs have DEGs? Visualize as KDE and binary.

DEG definition (project convention, lib/biomni_q2.py): pvals_adj < 0.1, no LFC threshold.
"""
import json
from pathlib import Path
import duckdb
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
PARQUET = "/gpfs/home/asun/jin_lab/bioagents/data/wilcoxon_de_results_group_name_final_data_no_multi_guide_cells.parquet"
GT_CSV = HERE / "fisher/top150_depletion_151_TH_Prkcd_Grin2c_Glut_predicted_group.csv"
CELLTYPE = "151 TH Prkcd Grin2c Glut"
PADJ = 0.1

# ---- top 100 depletion hits ----
gt = pd.read_csv(GT_CSV).sort_values("depletion_rank")
top100 = gt[gt.depletion_rank <= 100].copy()
genes = top100.gene_target.tolist()
print(f"top100 genes: {len(genes)} (unique {len(set(genes))})")

# ---- DEG counts per target in this cell type ----
con = duckdb.connect()
genes_sql = ",".join(f"'{g}'" for g in genes)
df = con.execute(
    f"""SELECT gene_target, names, pvals_adj, logfoldchanges
        FROM read_parquet('{PARQUET}')
        WHERE group_name = '{CELLTYPE}' AND gene_target IN ({genes_sql})"""
).df()
print(f"rows pulled: {len(df)}; targets present: {df.gene_target.nunique()}")

# DEG = pvals_adj < PADJ (NaN padj -> not significant)
df["is_deg"] = df.pvals_adj < PADJ
counts = df.groupby("gene_target").agg(
    n_tested=("names", "size"),
    n_deg=("is_deg", "sum"),
).reset_index()

# merge back to top100 (targets with NO rows in this cell type -> n_tested=0, n_deg=0)
res = top100[["depletion_rank", "gene_target", "log2_odds_ratio",
              "passes_heatmap_filter", "adj_p_value_bh"]].merge(
    counts, on="gene_target", how="left")
res["n_tested"] = res["n_tested"].fillna(0).astype(int)
res["n_deg"] = res["n_deg"].fillna(0).astype(int)
res["has_deg"] = res["n_deg"] > 0
res["absent_in_celltype"] = res["n_tested"] == 0
res = res.sort_values("depletion_rank")
res.to_csv(HERE / "top100_deg_counts.csv", index=False)

n_null = int((~res.has_deg).sum())
n_hit = int(res.has_deg.sum())
n_absent = int(res.absent_in_celltype.sum())
summary = {
    "cell_type": CELLTYPE,
    "deg_definition": f"pvals_adj < {PADJ}",
    "n_top100": len(res),
    "n_with_deg": n_hit,
    "n_null_hits": n_null,
    "of_which_absent_in_celltype": n_absent,
    "n_null_but_tested": n_null - n_absent,
    "n_deg_mean": float(res.n_deg.mean()),
    "n_deg_median": float(res.n_deg.median()),
    "n_deg_max": int(res.n_deg.max()),
}
print(json.dumps(summary, indent=2))
(HERE / "top100_deg_summary.json").write_text(json.dumps(summary, indent=2))

# ---------------- Figure: KDE + binary ----------------
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# (A) KDE / distribution of DEG counts (log1p axis: distribution is zero-inflated
#     with a long right tail, so raw-count KDE is uninformative)
ax = axes[0]
from scipy.stats import gaussian_kde
vals = np.log1p(res.n_deg.values.astype(float))
maxv = vals.max()
bins = np.linspace(0, maxv, 30)
ax.hist(vals, bins=bins, density=True, color="#9ecae1", alpha=0.6,
        edgecolor="white", label="histogram")
kde = gaussian_kde(vals, bw_method=0.25)
xs = np.linspace(0, maxv, 400)
ax.plot(xs, kde(xs), color="#08519c", lw=2.2, label="KDE")
ax.plot(vals, np.full_like(vals, -0.02, dtype=float), "|", color="#08519c",
        alpha=0.5, ms=12)
med = np.log1p(res.n_deg.median())
ax.axvline(med, color="#e6550d", ls="--", lw=1.5,
           label=f"median = {int(res.n_deg.median())} DEGs")
# label ticks in original DEG counts
ticks = [0, 1, 10, 100, 1000, 2262]
ax.set_xticks([np.log1p(t) for t in ticks])
ax.set_xticklabels(ticks)
ax.set_xlabel(f"# DEGs (pvals_adj < {PADJ}) in {CELLTYPE}  [log1p axis]")
ax.set_ylabel("density")
ax.set_title("A. DEG-count distribution of top-100 depletion hits")
ax.legend(frameon=False)
ax.spines[["top", "right"]].set_visible(False)

# (B) Binary: null vs has-DEG
ax = axes[1]
cats = ["Null hit\n(0 DEGs)", "Has DEGs\n(≥1)"]
heights = [n_null, n_hit]
colors = ["#bdbdbd", "#3182bd"]
bars = ax.bar(cats, heights, color=colors, edgecolor="black", width=0.6)
for b, h in zip(bars, heights):
    ax.text(b.get_x() + b.get_width() / 2, h + 0.8, f"{h}\n({100*h/len(res):.0f}%)",
            ha="center", va="bottom", fontsize=11, fontweight="bold")
# annotate absent-in-celltype portion of null bar
if n_absent:
    ax.bar(cats[0], n_absent, color="#737373", edgecolor="black", width=0.6,
           hatch="///", label=f"absent in cell type (n={n_absent})")
    ax.legend(frameon=False, loc="upper left")
ax.set_ylabel("# of top-100 depletion hits")
ax.set_ylim(0, max(heights) * 1.18)
ax.set_title("B. Null vs DEG-positive (binary)")
ax.spines[["top", "right"]].set_visible(False)

fig.suptitle(f"Top-100 depletion hits: DEG status in '{CELLTYPE}'",
             fontsize=14, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(HERE / "q1_deg_distribution_top100.png", dpi=150)
print("wrote q1_deg_distribution_top100.png")
