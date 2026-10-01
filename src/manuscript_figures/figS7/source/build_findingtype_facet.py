#!/usr/bin/env python3
"""
Fig 2g — exploratory: what does faceting findings by finding_type against DEG burden show?

Two subplots (one figure, prototype for the bottom-right "statistics for findings" block):

  (left)  Enrichment — for each of the 12 finding_types, log2( share among zero-DEG-target
          findings / share among DEG-positive-target findings ). Bars right (brown) = the
          type is over-represented on null targets; left (blue) = over-represented where
          there is DEG signal. Answers "which finding types characterize null targets".

  (right) Composition gradient — findings binned by their target's total DEG burden
          (0, 1-10, 11-100, 101-1000, >1000), stacked by a coarse 3-family grouping
          (null / prior-driven / measurement-grounded). Shows the compositional shift as
          DEG signal vanishes.

The 3-family grouping is a coarse interpretation (see FAMILY below), labelled as such.

Source: debug/260627_biokg_evidence/findings_ledger.csv (finding_type per finding)
        data/groupxtarget_deg.csv (target DEG burden -> zero-DEG vs DEG-positive, and bins)

    python3 manuscript/fig2/g/build_findingtype_facet.py
"""
from __future__ import annotations

import collections
import csv
import os
import pathlib

os.environ.setdefault("MPLCONFIGDIR", "/tmp/mplconfig_fig2g")
pathlib.Path(os.environ["MPLCONFIGDIR"]).mkdir(parents=True, exist_ok=True)

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.gridspec import GridSpec

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[2]
STYLE = REPO / "src" / "figures" / "style.mplstyle"
LEDGER = REPO / "debug" / "260627_biokg_evidence" / "findings_ledger.csv"
DEG_CSV = REPO / "data" / "groupxtarget_deg.csv"

NULL_C, PRIOR_C, MEAS_C = "#c0392b", "#9c6b4a", "#4a6f9c"  # null / prior-driven / measurement
# coarse 3-family grouping of the 12 finding_types (interpretation, not a data field)
FAMILY = {
    "negative_result": "null",
    "cross_perturbation_contrast": "prior-driven",
    "pathway_uncoupling": "prior-driven",
    "therapeutic_direction_warning": "prior-driven",
    "disease_mechanism_refinement": "prior-driven",
    "literature_direction_mismatch": "prior-driven",
    "biomarker_candidate": "measurement-grounded",
    "convergent_module": "measurement-grounded",
    "cell_type_selectivity": "measurement-grounded",
    "homeostatic_compensation": "measurement-grounded",
    "buffered_response": "measurement-grounded",
    "other": "measurement-grounded",
}
FAM_ORDER = ["measurement-grounded", "prior-driven", "null"]
FAM_COLOR = {"null": NULL_C, "prior-driven": PRIOR_C, "measurement-grounded": MEAS_C}
BINS = [(0, 0, "0"), (1, 10, "1–10"), (11, 100, "11–100"),
        (101, 1000, "101–1k"), (1001, 10**9, ">1k")]


# two population framings: (focus upper bound inclusive, focus label, complement label, prefix)
POPS = [
    (10, "low-DEG targets (≤10)", "higher-DEG targets (>10)", "lowdeg"),   # MAIN
    (0, "zero-DEG targets (0)", "DEG-positive targets (≥1)", "zerodeg"),   # SUPPLEMENT
]


def render_facet(rows, burden, focus_hi, focus_name, comp_name, out_prefix):
    b = lambda g: int(burden.get(g, 0))
    is_focus = lambda g: b(g) <= focus_hi

    # ---- enrichment: type share, focus population vs its complement ----
    z = collections.Counter(); d = collections.Counter()
    for r in rows:
        (z if is_focus(r["target_gene"]) else d)[r["finding_type"]] += 1
    nz, nd = sum(z.values()), sum(d.values())
    types = sorted(set(z) | set(d), key=lambda t: (z[t] / nz) / max(d[t] / nd, 1e-9))
    enrich = [np.log2((z[t] / nz) / max(d[t] / nd, 1e-9)) for t in types]

    # ---- composition across DEG bins (same full continuum in both variants) ----
    binfam = {lab: collections.Counter() for *_, lab in BINS}
    binN = collections.Counter()
    for r in rows:
        v = b(r["target_gene"])
        lab = next(lab for lo, hi, lab in BINS if lo <= v <= hi)
        binfam[lab][FAMILY.get(r["finding_type"], "measurement-grounded")] += 1
        binN[lab] += 1

    fig = plt.figure(figsize=(7.2, 3.1))
    gs = GridSpec(1, 2, figure=fig, width_ratios=[1.25, 1.0], wspace=0.42,
                  left=0.24, right=0.97, top=0.82, bottom=0.16)
    axE = fig.add_subplot(gs[0, 0])
    axC = fig.add_subplot(gs[0, 1])

    # --- enrichment diverging bars ---
    y = np.arange(len(types))
    colors = [PRIOR_C if e > 0 else MEAS_C for e in enrich]
    axE.barh(y, enrich, color=colors, height=0.72, linewidth=0)
    axE.axvline(0, color="#555555", lw=0.6)
    axE.set_yticks(y)
    axE.set_yticklabels([t.replace("_", " ") for t in types], fontsize=5.6)
    axE.set_xlabel(f"log2( share on {focus_name} / share on {comp_name} )", fontsize=6.0)
    axE.set_title(f"Which finding types characterize {focus_name}", fontsize=7, loc="left")
    axE.tick_params(axis="x", labelsize=5.5)
    axE.text(0.98, 0.04, f"→ enriched on {focus_name}", transform=axE.transAxes,
             fontsize=5, color=PRIOR_C, ha="right", va="bottom")
    axE.text(0.02, 0.96, f"enriched on {comp_name} ←", transform=axE.transAxes,
             fontsize=5, color=MEAS_C, ha="left", va="top")

    # --- composition stacked across DEG bins ---
    labs = [lab for *_, lab in BINS]
    x = np.arange(len(labs))
    # shade the DEG bins that belong to the focus population
    focus_labs = [lab for lo, hi, lab in BINS if lo <= focus_hi]
    if focus_labs:
        axC.axvspan(-0.5, len(focus_labs) - 0.5, color="#f0e9e2", zorder=0)
        axC.text(len(focus_labs) / 2 - 0.5, 101.5, focus_name, fontsize=5,
                 color=PRIOR_C, ha="center", va="bottom")
    bottom = np.zeros(len(labs))
    for fam in FAM_ORDER:
        vals = np.array([binfam[lab][fam] / max(binN[lab], 1) * 100 for lab in labs])
        axC.bar(x, vals, bottom=bottom, width=0.8, color=FAM_COLOR[fam], label=fam,
                linewidth=0.4, edgecolor="white")
        bottom += vals
    axC.set_xticks(x)
    axC.set_xticklabels([f"{lab}\n(n={binN[lab]:,})" for lab in labs], fontsize=5.4)
    axC.set_ylim(0, 100)
    axC.set_ylabel("% of findings", fontsize=6.5)
    axC.set_xlabel("target DEG burden (nDEG@padj<0.1)", fontsize=6.2)
    axC.set_title("Finding-type mix vs DEG burden", fontsize=7, loc="left")
    axC.tick_params(axis="y", labelsize=5.5)
    axC.legend(fontsize=5.2, loc="lower center", bbox_to_anchor=(0.5, 1.06),
               ncol=3, frameon=False, handlelength=1.0, columnspacing=1.0)

    fig.text(0.24, 0.965, f"Findings by type across the DEG-signal axis — focus: {focus_name}",
             fontsize=8.5, fontweight="bold", ha="left", va="top")

    for ext in ("svg", "pdf"):
        fig.savefig(HERE / f"figG_findingtype_facet_{out_prefix}.{ext}")
    fig.savefig(HERE / f"figG_findingtype_facet_{out_prefix}.png", dpi=300)
    plt.close(fig)

    print(f"\n=== facet: focus={focus_name} ({out_prefix}) ===")
    print("finding_type enrichment (focus vs complement), log2:")
    for t, e in sorted(zip(types, enrich), key=lambda p: -p[1]):
        print(f"  {e:+.2f}  {t}")
    print("composition by DEG bin (% null / prior / measurement):")
    for lab in labs:
        tot = max(binN[lab], 1)
        print(f"  {lab:>7} n={binN[lab]:>5}  "
              f"null={100*binfam[lab]['null']/tot:4.1f}  "
              f"prior={100*binfam[lab]['prior-driven']/tot:4.1f}  "
              f"meas={100*binfam[lab]['measurement-grounded']/tot:4.1f}")
    print(f"wrote figG_findingtype_facet_{out_prefix}.{{svg,pdf,png}}")


def main():
    # drop Safe_target_* non-targeting controls (not real perturbations; see build_panel_g.py)
    rows = [r for r in csv.DictReader(open(LEDGER))
            if not r["target_gene"].startswith("Safe_target")]
    burden = pd.read_csv(DEG_CSV).groupby("gene_target")["ndeg_padj_0.1"].sum()
    if STYLE.exists():
        plt.style.use(str(STYLE))
    plt.rcParams.update({"savefig.bbox": "tight", "savefig.pad_inches": 0.04})
    for focus_hi, focus_name, comp_name, prefix in POPS:
        render_facet(rows, burden, focus_hi, focus_name, comp_name, prefix)


if __name__ == "__main__":
    main()
