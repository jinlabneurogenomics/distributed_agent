#!/usr/bin/env python3
"""Merge the two-corpus union and render distributions plus heatmaps."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
CURRENT = ROOT / "manuscript/fig2/_debug/260801/meaningful_biology_rescue/meaningful_primary_findings_conservative.csv"
STAGE1 = HERE / "stage1_union_decisions.csv"
REVIEWS = HERE / "stage2_literature_reviews.csv"
DEG_CSV = ROOT / "data/groupxtarget_deg.csv"
STYLE = ROOT / "src/figures/style.mplstyle"
FINAL = HERE / "meaningful_primary_findings_union.csv"

FLAGS = ("Agree", "Disagree", "Inferred", "No Literature")
COLORS = {"Agree": "#70bf73", "Disagree": "#ed8255", "Inferred": "#92918c", "No Literature": "#c8c7be"}
PAIR_PRIORITY = {"No Literature": 0, "Inferred": 1, "Agree": 2, "Disagree": 3}
CELL_TYPES = [
    "001 L5-6 IT Glut", "005 L4-5 IT CTX Glut", "007 L2-3 IT CTX Glut",
    "008 L2-3 IT ENT PPP RSP Glut", "009 L2-3 IT PIR AON ENT Glut",
    "022 L5 ET CTX Glut", "027 NP-CT-L6b-OB Glut", "012 MEA LA CA1 DG Glut",
    "017 CA3 CA2-FC DG Glut", "046 CTX-CGE GABA", "052 Pvalb Gaba",
    "053 Sst Gaba", "054 CNU-MGE GABA", "059 CNU-LGE LSX GABA",
    "066 CNU-HYa HY GABA", "110 CNU-HYa HY MM Glut", "145 MH-LH TH Glut",
    "151 TH Prkcd Grin2c Glut", "155 MB Glut", "191 MB P MY GABA",
    "215 MB Dopa", "217 P MY Pineal Glut", "308 CB GABA",
]
STRATA = ("Strong", "Moderate", "Low", "No local DEGs", "No placement")
STRATUM_LABELS = {
    "Strong": "Strong local signal (≥100)", "Moderate": "Moderate local signal (25–99)",
    "Low": "Low local signal (1–24)", "No local DEGs": "No local DEGs (0)",
    "No placement": "No supported cell placement",
}
SIGNAL_COLORS = {"Low": "#c6dbe7", "Moderate": "#70a5be", "Strong": "#285f7d"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(rows)


def parse_json(value: Any, fallback: Any) -> Any:
    try: return json.loads(str(value))
    except (TypeError, ValueError, json.JSONDecodeError): return fallback


def setup_plotting() -> Any:
    os.environ.setdefault("MPLCONFIGDIR", "/tmp/mplconfig_meaningful_union")
    Path(os.environ["MPLCONFIGDIR"]).mkdir(parents=True, exist_ok=True)
    import matplotlib.pyplot as plt
    if STYLE.is_file(): plt.style.use(STYLE)
    plt.rcParams.update({"svg.fonttype": "none", "pdf.fonttype": 42, "savefig.bbox": "tight"})
    return plt


def save(fig: Any, stem: str) -> None:
    for suffix in ("png", "svg", "pdf"):
        fig.savefig(HERE / f"{stem}.{suffix}", dpi=300 if suffix == "png" else None, bbox_inches="tight")


def stratum(maximum: int | None) -> str:
    if maximum is None: return "No placement"
    if maximum >= 100: return "Strong"
    if maximum >= 25: return "Moderate"
    if maximum >= 1: return "Low"
    return "No local DEGs"


def load_deg() -> tuple[dict[tuple[str, str], int], dict[str, int]]:
    pair = {}; totals: Counter[str] = Counter()
    for row in read_csv(DEG_CSV):
        gene = row["gene_target"]; cell = row["group_name"]; n = int(float(row["ndeg_padj_0.1"]))
        pair[(gene, cell)] = n; totals[gene] += n
    return pair, dict(totals)


def literature_audit_fields(lit: dict[str, str], review_key: str) -> dict[str, str]:
    """Keep the literature decision and its links attached to the final finding."""
    return {
        "literature_review_key": review_key,
        "literature_claim_scope": lit.get("claim_scope", ""),
        "documented_expectation": lit.get("documented_expectation", ""),
        "missing_or_conflicting_link": lit.get("missing_or_conflicting_link", ""),
        "literature_rationale": lit.get("rationale", ""),
        "dataset_support_summary": lit.get("dataset_support_summary", ""),
        "supporting_reference_keys_json": lit.get("supporting_reference_keys_json", "[]"),
        "supporting_references_json": lit.get("supporting_references_json", "[]"),
        "adjudication_override_id": lit.get("override_id", ""),
        "adjudication_date": lit.get("adjudication_date", ""),
    }


def merge() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    current = read_csv(CURRENT); stage1 = read_csv(STAGE1); reviews = read_csv(REVIEWS)
    review = {row["review_key"]: row for row in reviews}
    extensions: dict[str, list[dict[str, str]]] = defaultdict(list)
    new = []
    for row in stage1:
        if row["disposition"] == "extend_current_primary": extensions[row["matched_current_candidate_id"]].append(row)
        elif row["disposition"] == "new_primary": new.append(row)
    pair_deg, _ = load_deg()

    baseline = []
    union = []
    for row in current:
        cells = list(dict.fromkeys(parse_json(row["supported_cell_types_json"], [])))
        maximum = max([pair_deg.get((row["gene_target"], c), 0) for c in cells] or [None])
        base = {
            "union_id": row["candidate_id"], "gene_target": row["gene_target"],
            "finding_id": row["finding_id"], "finding_type": row["finding_type"],
            "biological_form": row["biological_form"], "summary": row["summary"],
            "flag": row["flag"], "confidence": row["confidence"],
            "biology_confidence": row["confidence"], "literature_confidence": row["confidence"],
            "supported_cell_types_json": json.dumps(cells, ensure_ascii=False),
            "maximum_local_deg": maximum if maximum is not None else "",
            "local_signal_stratum": stratum(maximum), "union_source": "current_conservative",
            "current_candidate_id": row["candidate_id"], "older_source_keys_json": "[]",
            "literature_relation": "", "extension_summaries_json": "[]",
            "literature_review_key": "", "literature_claim_scope": "",
            "documented_expectation": "",
            "missing_or_conflicting_link": "", "literature_rationale": "",
            "dataset_support_summary": "", "supporting_reference_keys_json": "[]",
            "supporting_references_json": "[]", "adjudication_override_id": "",
            "adjudication_date": "",
        }
        baseline.append(dict(base))
        ext = extensions.get(row["candidate_id"], [])
        if ext:
            ext_cells = [c for e in ext for c in parse_json(e["supported_cell_types_json"], [])]
            cells = list(dict.fromkeys(cells + ext_cells))
            maximum = max([pair_deg.get((row["gene_target"], c), 0) for c in cells] or [None])
            lit = review[f"EXT:{row['candidate_id']}"]
            base.update({
                "summary": lit.get("summary_override") or base["summary"],
                "flag": lit["flag"], "confidence": lit["confidence"],
                "supported_cell_types_json": json.dumps(cells, ensure_ascii=False),
                "maximum_local_deg": maximum if maximum is not None else "",
                "local_signal_stratum": stratum(maximum), "union_source": "current_extended_by_older",
                "older_source_keys_json": json.dumps([e["source_key"] for e in ext]),
                "literature_relation": lit["relation"],
                "extension_summaries_json": json.dumps([e["primary_summary"] for e in ext], ensure_ascii=False),
                "extension_biology_confidences_json": json.dumps([e["confidence"] for e in ext]),
                "literature_confidence": lit["confidence"],
            })
            base.update(literature_audit_fields(lit, f"EXT:{row['candidate_id']}"))
        union.append(base)
    for row in new:
        if row["gene_target"].startswith("Safe_target"):
            continue
        lit = review[f"NEW:{row['source_key']}"]
        cells = list(dict.fromkeys(parse_json(row["supported_cell_types_json"], [])))
        maximum = max([pair_deg.get((row["gene_target"], c), 0) for c in cells] or [None])
        new_row = {
            "union_id": row["source_key"], "gene_target": row["gene_target"],
            "finding_id": row["finding_id"], "finding_type": "older_recovered",
            "biological_form": row["biological_form"], "summary": row["primary_summary"],
            "flag": lit["flag"], "confidence": lit["confidence"],
            "biology_confidence": row["confidence"], "literature_confidence": lit["confidence"],
            "supported_cell_types_json": json.dumps(cells, ensure_ascii=False),
            "maximum_local_deg": maximum if maximum is not None else "",
            "local_signal_stratum": stratum(maximum), "union_source": "older_new_primary",
            "current_candidate_id": "", "older_source_keys_json": json.dumps([row["source_key"]]),
            "literature_relation": lit["relation"], "extension_summaries_json": "[]",
        }
        new_row.update(literature_audit_fields(lit, f"NEW:{row['source_key']}"))
        union.append(new_row)
    return baseline, union


def distribution(rows: list[dict[str, Any]], layer: str) -> list[dict[str, Any]]:
    counts = Counter(row["flag"] for row in rows); n = len(rows)
    return [{"layer": layer, "flag": f, "count": counts[f], "percent": 100 * counts[f] / n, "n_findings": n} for f in FLAGS]


def plot_overall(baseline: list[dict[str, Any]], union: list[dict[str, Any]]) -> list[dict[str, Any]]:
    plt = setup_plotting(); from matplotlib.patches import Patch
    rows = distribution(baseline, "Current conservative rescue") + distribution(union, "Two-corpus union")
    lookup = {(r["layer"], r["flag"]): r for r in rows}; layers = ("Current conservative rescue", "Two-corpus union")
    fig, ax = plt.subplots(figsize=(9.6, 2.8))
    for y, layer in zip((1, 0), layers):
        left = 0
        for flag in FLAGS:
            width = lookup[(layer, flag)]["percent"]
            ax.barh(y, width, left=left, height=.58, color=COLORS[flag], edgecolor="white", linewidth=.8)
            if width >= 2.4: ax.text(left + width/2, y, f"{width:.1f}%", ha="center", va="center", fontsize=8, color="white" if flag in {"Disagree", "Inferred"} else "#333")
            left += width
        ax.text(101, y, f"n={lookup[(layer, FLAGS[0])]['n_findings']:,}", va="center", fontsize=8, color="#555")
    ax.set_xlim(0, 109); ax.set_yticks((1, 0), layers); ax.set_xlabel("Percent of primary findings")
    ax.set_title("Meaningful-biology literature flags — current atlas and two-corpus union", loc="left")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.legend(handles=[Patch(fc=COLORS[f], label=f) for f in FLAGS], ncol=4, frameon=False, loc="upper center", bbox_to_anchor=(.5, -.35))
    save(fig, "union_flag_distribution"); plt.close(fig); return rows


def plot_local(baseline: list[dict[str, Any]], union: list[dict[str, Any]]) -> list[dict[str, Any]]:
    plt = setup_plotting(); from matplotlib.patches import Patch
    layers = ("Current", "Union"); source = {"Current": baseline, "Union": union}; out = []
    for s in STRATA:
        for layer in layers:
            subset = [r for r in source[layer] if r["local_signal_stratum"] == s]; counts = Counter(r["flag"] for r in subset); n = len(subset)
            for f in FLAGS: out.append({"local_signal_stratum": s, "layer": layer, "flag": f, "count": counts[f], "percent": 100*counts[f]/n if n else 0, "n_findings": n})
    shown = [s for s in STRATA if any(r["local_signal_stratum"] == s for r in union)]
    fig, ax = plt.subplots(figsize=(10.8, 1.3 + 1.05*len(shown))); lookup={(r["local_signal_stratum"],r["layer"],r["flag"]):r for r in out}
    positions=[]; labels=[]; y=0
    for s in reversed(shown):
        active_layers = [layer for layer in layers if lookup[(s, layer, FLAGS[0])]["n_findings"] > 0]
        for layer in reversed(active_layers):
            positions.append(y); labels.append(f"{STRATUM_LABELS[s]} · {layer}"); left=0
            for f in FLAGS:
                row=lookup[(s,layer,f)]; width=row["percent"]
                ax.barh(y,width,left=left,height=.58,color=COLORS[f],edgecolor="white",linewidth=.7)
                if width>=2.4: ax.text(left+width/2,y,f"{width:.1f}%",ha="center",va="center",fontsize=7.4,color="white" if f in {"Disagree","Inferred"} else "#333")
                left+=width
            ax.text(101,y,f"n={lookup[(s,layer,FLAGS[0])]['n_findings']:,}",va="center",fontsize=7.5,color="#555"); y+=1
        if s != shown[0]:
            ax.plot([-.32, 1.0], [y-.5,y-.5], transform=ax.get_yaxis_transform(), color="#aaa", lw=.7, ls=(0,(3,3)), clip_on=False)
        y+=.35
    ax.set_xlim(0,110); ax.set_yticks(positions,labels); ax.set_xlabel("Percent of primary findings")
    ax.set_title("Meaningful-biology flags by finding-level maximum local signal",loc="left")
    ax.spines[["top","right","left"]].set_visible(False)
    ax.legend(handles=[Patch(fc=COLORS[f],label=f) for f in FLAGS],ncol=4,frameon=False,loc="upper center",bbox_to_anchor=(.5,-.14))
    save(fig,"union_flag_distribution_by_local_signal"); plt.close(fig); return out


def target_order(totals: dict[str, int]) -> list[str]:
    def stable(name: str) -> int: return int(hashlib.md5(name.encode()).hexdigest(),16)
    return sorted([g for g,n in totals.items() if n>0 and not g.startswith("Safe_target")], key=lambda g:(-totals[g],stable(g)))


def plot_heatmaps(rows: list[dict[str, Any]]) -> None:
    plt=setup_plotting(); from matplotlib.colors import BoundaryNorm,ListedColormap; from matplotlib.gridspec import GridSpec; from matplotlib.patches import Patch
    pair_deg,totals=load_deg(); targets=target_order(totals); ti={g:i for i,g in enumerate(targets)}; ci={c:i for i,c in enumerate(CELL_TYPES)}
    pair_flags: dict[tuple[str,str],list[str]]=defaultdict(list)
    for row in rows:
        gene=row["gene_target"]
        for cell in parse_json(row["supported_cell_types_json"],[]):
            if gene in ti and cell in ci and pair_deg.get((gene,cell),0)>0: pair_flags[(gene,cell)].append(row["flag"])
    chosen={pair:max(flags,key=PAIR_PRIORITY.get) for pair,flags in pair_flags.items()}
    flag_code={f:i for i,f in enumerate(FLAGS)}; signal_code={"Low":0,"Moderate":1,"Strong":2}
    flag_matrix=np.full((len(CELL_TYPES),len(targets)),np.nan); signal_matrix=np.full_like(flag_matrix,np.nan)
    for (gene,cell),flag in chosen.items():
        n=pair_deg[(gene,cell)]; s="Strong" if n>=100 else "Moderate" if n>=25 else "Low"
        flag_matrix[ci[cell],ti[gene]]=flag_code[flag]; signal_matrix[ci[cell],ti[gene]]=signal_code[s]

    def draw(matrix: np.ndarray, colors: list[str], labels: list[str], stem: str, title: str, subtitle: str, xlabel: str) -> None:
        cmap=ListedColormap(colors); cmap.set_bad("white"); norm=BoundaryNorm(np.arange(-.5,len(colors)+.5,1),cmap.N)
        burden=np.log10(np.array([totals[g] for g in targets])+1)
        fig=plt.figure(figsize=(8.2,3.85)); gs=GridSpec(2,2,figure=fig,width_ratios=[1,.14],height_ratios=[.16,1],wspace=.04,hspace=.06,left=.16,right=.985,top=.82,bottom=.14)
        top=fig.add_subplot(gs[0,0]); ax=fig.add_subplot(gs[1,0],sharex=top); right=fig.add_subplot(gs[1,1],sharey=ax); mix=fig.add_subplot(gs[0,1])
        ax.imshow(matrix,aspect="auto",cmap=cmap,norm=norm,interpolation="nearest",origin="upper",extent=[0,len(targets),len(CELL_TYPES),0])
        ax.set_yticks(np.arange(len(CELL_TYPES))+.5,CELL_TYPES,fontsize=5.1); ax.tick_params(axis="y",length=0); ax.set_xlabel(xlabel,fontsize=6.2)
        top.fill_between(np.arange(len(targets))+.5,burden,step="mid",color="#9c6b4a",linewidth=0); top.set_ylim(0,burden.max()*1.05); top.set_ylabel("DEG burden\nlog10(n+1)",fontsize=5.2,rotation=0,ha="right",va="center"); top.yaxis.set_label_coords(-.02,.5); top.tick_params(axis="x",labelbottom=False,length=0); top.tick_params(axis="y",labelsize=5,length=2)
        for side in ("top","right"): top.spines[side].set_visible(False)
        for i in range(len(CELL_TYPES)):
            vals=matrix[i][~np.isnan(matrix[i])]; left=0
            for code,color in enumerate(colors):
                frac=float(np.sum(vals==code)/len(vals)) if len(vals) else 0; right.barh(i+.5,frac,left=left,height=.8,color=color,linewidth=0); left+=frac
        right.set_xlim(0,1); right.set_ylim(len(CELL_TYPES),0); right.set_xlabel("mix per class",fontsize=5.2); right.set_xticks([0,1]); right.tick_params(axis="x",labelsize=5,length=2); right.tick_params(axis="y",labelleft=False,length=0); right.spines[["top","right"]].set_visible(False)
        vals=matrix[~np.isnan(matrix)]; left=0
        for code,color in enumerate(colors):
            frac=float(np.sum(vals==code)/len(vals)) if len(vals) else 0; mix.barh(0,frac,left=left,height=.72,color=color,linewidth=0);left+=frac
        mix.set_xlim(0,1);mix.set_ylim(-.6,.6);mix.axis("off");mix.set_title("overall mix",fontsize=5.2,pad=1)
        n_pairs=int(np.sum(~np.isnan(matrix)));n_targets=int(np.sum(np.any(~np.isnan(matrix),axis=0)))
        fig.text(.16,.965,title,fontsize=8.5,fontweight="bold",ha="left",va="top");fig.text(.16,.905,f"{n_pairs:,} non-null target×class placements across {n_targets:,}/{len(targets):,} DEG-positive targets. {subtitle}",fontsize=5.35,ha="left",va="top",color="#555")
        fig.legend(handles=[Patch(fc=c,ec="#ccc",lw=.3) for c in colors],labels=labels,ncol=len(labels),frameon=False,fontsize=6,loc="lower center",bbox_to_anchor=(.5,-.01),handlelength=1,columnspacing=1)
        save(fig,stem);plt.close(fig)

    draw(signal_matrix,[SIGNAL_COLORS[s] for s in ("Low","Moderate","Strong")],["Low 1–24","Moderate 25–99","Strong ≥100"],"union_local_signal_heatmap_nonnull","Two-corpus union coverage by target × cell-type DEG signal","White denotes no supported primary finding; zero-DEG placements are not plotted.",f"Perturbation target (n={len(targets):,}; sorted by total DEG burden ↓)")
    draw(flag_matrix,[COLORS[f] for f in FLAGS],list(FLAGS),"union_flag_heatmap_nonnull","Two-corpus union literature relation across cell classes and perturbations","White denotes no supported primary finding; pair aggregation surfaces Disagree, then Agree, Inferred, and No Literature.",f"Perturbation target (n={len(targets):,}; sorted by total DEG burden ↓)")
    matrix_rows=[]
    for cell in CELL_TYPES:
        for gene in targets:
            n=pair_deg.get((gene,cell),0); flag=chosen.get((gene,cell),"")
            matrix_rows.append({"gene_target":gene,"cell_type":cell,"target_total_deg":totals[gene],"target_cell_deg":n,"covered_nonnull":int(bool(flag) and n>0),"flag":flag,"local_signal_stratum":"Strong" if n>=100 else "Moderate" if n>=25 else "Low" if n>=1 else "No local DEGs"})
    write_csv(HERE/"union_heatmap_cells.csv",matrix_rows)


def main() -> None:
    baseline,union=merge();write_csv(FINAL,union)
    overall=plot_overall(baseline,union);write_csv(HERE/"union_flag_distribution.csv",overall)
    local=plot_local(baseline,union);write_csv(HERE/"union_flag_distribution_by_local_signal.csv",local)
    plot_heatmaps(union)
    payload={"current_conservative_primary":len(baseline),"union_primary":len(union),"new_primary":sum(r["union_source"]=="older_new_primary" for r in union),"extended_current":sum(r["union_source"]=="current_extended_by_older" for r in union),"excluded_control_findings":1,"flags":dict(Counter(r["flag"] for r in union)),"local_signal":dict(Counter(r["local_signal_stratum"] for r in union))}
    (HERE/"union_summary.json").write_text(json.dumps(payload,indent=2)+"\n");print(json.dumps(payload,indent=2))


if __name__ == "__main__": main()
