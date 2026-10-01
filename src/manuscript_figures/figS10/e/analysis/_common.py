"""Shared config, data loaders, metrics and palette for fig4/c (depletion panel).

Source experiment: q7 depletion eval, cell group `151 TH Prkcd Grin2c Glut`
(debug/depletion). Ground truth = Fisher depletion ranking (observed vs
AAV-pool-expected perturbed cells → log2 depletion odds ratio). Predictions =
two frameworks that returned up to 100 ranked candidate depleters.

All figure scripts import from here so the data provenance, palette and metric
definitions live in exactly one place.
"""
from __future__ import annotations

import math
import re
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# ---------------------------------------------------------------- paths
HERE = Path(__file__).resolve().parent       # .../manuscript/fig4/c
ROOT = HERE.parents[2]                        # repo root: .../bioagents
PANELS = HERE / "panels"
PANELS.mkdir(exist_ok=True)

STYLE_PATH = ROOT / "src/figures/style.mplstyle"

GT_DIR = ROOT / "debug/depletion/ground_truth"
GT_CSV = GT_DIR / "fisher/top150_depletion_151_TH_Prkcd_Grin2c_Glut_predicted_group.csv"
DEG_COUNTS = GT_DIR / "top100_deg_counts.csv"
MSIGDB_SIG = GT_DIR / "q2_msigdb_enrichment_sig.csv"
FISHER_PERGENE = GT_DIR / "fisher/fisher_results_per_gene_predicted_group.csv"
OBS_AAV = GT_DIR / "fisher/guide_observed_cell_fraction_vs_aav_fraction_predicted_group.csv"

CELLTYPE = "151 TH Prkcd Grin2c Glut"
CELLTYPE_SHORT = "TH Prkcd Grin2c Glut (151)"
TOP_GT = 100                                 # relevant set = GT top 100

# Prediction files. Labels are provisional (carried from the debug manifest) and
# are trivial to reassign here once the final method names for the paper are set.
PREDICTIONS: dict[str, Path] = {
    "A": ROOT / "results/bioeval/q7b_v2/20260529T191007Z/bioagents/answer.txt",
    "B": ROOT / "results/q7b_r4/answer.txt",
}
PRED_LABELS = {"A": "2000agents", "B": "biomni"}

# ---------------------------------------------------------------- palette
# Okabe-Ito driven, matched to src/figures/style.mplstyle. GT panels use a
# "truth" palette (grays + teal + amber); prediction panels use the two method
# hues (blue / vermillion). Kept disjoint so a composite figure never reuses a
# colour for two different meanings.
INK = "#222222"
GRID = "#CCCCCC"

# Ground-truth / DEG
C_ALL = "#DADADA"          # all screened genes (background)
C_GT = "#4D4D4D"           # GT depletion curve / points
C_HASDEG = "#009E73"       # target has >=1 DEG in this cell type
C_NULL = "#BDBDBD"         # null hit (0 DEGs)
C_HEATMAP = "#E69F00"      # passes original heatmap filter (high-confidence set)

# Pathway collections
COLLECTION_COLORS = {
    "GO_BP": "#009E73",
    "Hallmark": "#CC79A7",
    "C2_CP": "#56B4E9",
    "Reactome": "#56B4E9",
}

# Prediction methods
METHOD_COLORS = {"A": "#0072B2", "B": "#D55E00"}

# GT depletion-rank bins (for prediction-vs-GT mapping panels)
BIN_COLORS = {
    "GT 1-10": "#166534",
    "GT 11-25": "#65A30D",
    "GT 26-50": "#F59E0B",
    "GT 51-100": "#EA580C",
    "GT 101-150": "#8B5CF6",
    "NA": "#E5E7EB",
}
BIN_ORDER = ["GT 1-10", "GT 11-25", "GT 26-50", "GT 51-100", "GT 101-150", "NA"]


def apply_style() -> None:
    if STYLE_PATH.exists():
        plt.style.use(str(STYLE_PATH))


def save(fig, name: str) -> None:
    """Save every panel as editable-text SVG + vector PDF + PNG (raster ref).

    SVG uses `svg.fonttype: none` (from the mplstyle) so text stays live/editable
    in Illustrator/Inkscape. PNG is kept because the options contact-sheets are
    assembled from the rasters.
    """
    fig.savefig(PANELS / f"{name}.svg")
    fig.savefig(PANELS / f"{name}.pdf")
    fig.savefig(PANELS / f"{name}.png", dpi=300)
    plt.close(fig)
    print(f"  wrote panels/{name}.svg + .pdf + .png")


# ---------------------------------------------------------------- loaders
def load_gt() -> pd.DataFrame:
    """Full GT top-150 depletion ranking with per-target DEG counts merged in."""
    gt = pd.read_csv(GT_CSV).sort_values("depletion_rank").reset_index(drop=True)
    gt["depletion_rank"] = gt["depletion_rank"].astype(int)
    deg = pd.read_csv(DEG_COUNTS)[["gene_target", "n_deg", "has_deg"]]
    gt = gt.merge(deg, on="gene_target", how="left")
    # top150 CSV already carries n_deg/has_deg for the full 150; prefer those and
    # only fall back to the merged top-100 deg-counts for any gaps.
    if "n_deg_x" in gt.columns:
        gt["n_deg"] = gt["n_deg_x"].fillna(gt["n_deg_y"])
        gt["has_deg"] = gt["has_deg_x"].fillna(gt["has_deg_y"])
        gt = gt.drop(columns=[c for c in gt.columns if c.endswith(("_x", "_y"))])
    return gt


def load_fisher_celltype() -> pd.DataFrame:
    """Per-gene Fisher result for the target cell group only (1948 genes)."""
    df = pd.read_csv(FISHER_PERGENE)
    df = df[df["cell_type"] == CELLTYPE].copy()
    df = df.rename(columns={
        "observed_pert_in_T (b)": "observed",
        "expected_pert_in_T (a)": "expected",
    })
    df["log2_or"] = df["odds_ratio"].apply(lambda x: math.log2(x) if x > 0 else float("nan"))
    return df.reset_index(drop=True)


def load_pathways() -> pd.DataFrame:
    df = pd.read_csv(MSIGDB_SIG)
    df["neglog10q"] = -df["qvalue"].apply(math.log10)
    # short human label from the MSigDB ID
    df["label"] = (
        df["ID"].str.replace(r"^(GOBP|HALLMARK|REACTOME|WP|KEGG_[A-Z]+)_", "", regex=True)
        .str.replace("_", " ").str.title()
    )
    return df.sort_values("neglog10q", ascending=True).reset_index(drop=True)


def load_obs_aav() -> pd.DataFrame:
    df = pd.read_csv(OBS_AAV)
    return df[df["predicted_group"] == CELLTYPE].copy().reset_index(drop=True)


# ---------------------------------------------------------------- predictions
def parse_prediction_file(path: Path) -> list[str]:
    """Return the ordered gene list from an answer.txt (numbered or bare list)."""
    lines = path.read_text().splitlines()
    numbered: list[tuple[int, str]] = []
    for line in lines:
        m = re.match(r"^\s*(\d+)[.)]\s+([A-Za-z0-9_.-]+)\b", line)
        if m:
            numbered.append((int(m.group(1)), m.group(2)))
    if numbered:
        return [g for _, g in sorted(numbered, key=lambda t: t[0])]
    genes = []
    for line in lines:
        g = line.strip()
        if g and re.match(r"^[A-Za-z0-9_.-]+$", g):
            genes.append(g)
    return genes


def load_predictions(k: int = 100) -> dict[str, list[str]]:
    return {name: parse_prediction_file(p)[:k] for name, p in PREDICTIONS.items()}


# ---------------------------------------------------------------- metrics
def gt_bin(rank) -> str:
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


def precision_at_k(pred: list[str], relevant: set[str], k: int) -> float:
    return sum(g in relevant for g in pred[:k]) / k


def recall_at_k(pred: list[str], relevant: set[str], k: int) -> float:
    return sum(g in relevant for g in pred[:k]) / len(relevant)


def average_precision(pred: list[str], relevant: set[str]) -> float:
    hits, precs = 0, []
    for i, g in enumerate(pred, 1):
        if g in relevant:
            hits += 1
            precs.append(hits / i)
    return sum(precs) / len(relevant) if relevant else 0.0


def ndcg_linear(pred: list[str], truth_rank: dict[str, int], k: int, top_gt: int = TOP_GT) -> float:
    padded = pred[:k] + [None] * max(0, k - len(pred))
    gains = [
        top_gt + 1 - truth_rank[g] if g is not None and truth_rank.get(g, top_gt + 1) <= top_gt else 0
        for g in padded[:k]
    ]
    ideal = list(range(top_gt, 0, -1))[:k]

    def dcg(vals):
        return sum(v / math.log2(i + 2) for i, v in enumerate(vals))

    return dcg(gains) / dcg(ideal) if ideal else 0.0
