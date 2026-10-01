#!/usr/bin/env python3
"""Render Graphviz network diagrams for the strongest BioKG convergence queries.

Each diagram shows TargetGene -> shared Entity edges (the convergence the graph
recovers), edges colored by effect_status, entity nodes grouped/colored by kind
or biological category. Reads the merged graph; writes .dot + .png to viz/.
"""
from __future__ import annotations
import csv, subprocess
from collections import defaultdict

from ..paths import GRAPH_WORK_DIR, VISUALIZE_WORK_DIR

csv.field_size_limit(10 ** 7)
OUT = GRAPH_WORK_DIR
VIZ = VISUALIZE_WORK_DIR / "convergence"; VIZ.mkdir(parents=True, exist_ok=True)

N = {r["id"]: r for r in csv.DictReader((OUT / "nodes.merged.csv").open())}
R = list(csv.DictReader((OUT / "relationships.merged.csv").open()))
def labs(i): return set(N[i]["labels"].split(";"))
hf = defaultdict(list)
for r in R:
    if r["type"] == "HAS_FINDING": hf[r["start_id"]].append(r["end_id"])
fin_tgt = {}
for tid in hf:
    for fid in hf[tid]: fin_tgt[fid] = N[tid]["symbol"]
sym2tid = {N[i]["symbol"]: i for i in N if "TargetGene" in labs(i)}
def pick_kind(i):
    ls = labs(i)
    for lab in ("Complex", "Pathway", "Module", "Phenotype", "Gene", "Other"):
        if lab in ls: return lab
    return "Gene" if "TargetGene" in ls else "Other"  # entities that are themselves targets render as genes
fin_ent = defaultdict(list)
for r in R:
    if r["type"] in ("IMPLICATES", "AFFECTS_GENE", "COMPARES_TO"):
        fin_ent[r["start_id"]].append((N[r["end_id"]]["name"], pick_kind(r["end_id"]), r["effect_status"]))

NEG = {"absent_or_not_detected", "fdr_insignificant"}
PRIO = {"affected": 6, "implicated": 5, "buffered": 4, "nominal": 3, "mixed": 2, "compared": 1, "uncertain": 0}
STATUS_COLOR = {"affected": "#1a7f37", "implicated": "#1f6feb", "buffered": "#e09b00",
                "nominal": "#8a8a8a", "mixed": "#8a8a8a", "compared": "#8250df", "uncertain": "#c9c9c9"}
KIND_FILL = {"Complex": "#ffe8a3", "Pathway": "#c6f0c2", "Phenotype": "#f7c6d9",
             "Gene": "#eef2f7", "Module": "#e3d7f5", "Other": "#e8e8e8"}


def best_edges(targets):
    """(target, entity_name, kind) -> best effect_status across that target's findings."""
    edges = {}
    for s in targets:
        tid = sym2tid.get(s)
        if not tid: continue
        for fid in hf[tid]:
            for nm, kind, st in fin_ent.get(fid, []):
                k = (s, nm, kind)
                if k not in edges or PRIO.get(st, -1) > PRIO.get(edges[k], -1):
                    edges[k] = st
    return edges


def esc(s): return s.replace('"', '\\"')


def render(spec):
    targets = spec["targets"]
    edges = best_edges(targets)
    # keep only entities shared by >= min_share targets, non-negative status, and in allowed kinds
    by_ent = defaultdict(dict)
    for (s, nm, kind), st in edges.items():
        if st in NEG: continue
        if spec.get("kinds") and kind not in spec["kinds"]: continue
        if spec.get("entities") and nm not in spec["entities"]: continue
        by_ent[(nm, kind)][s] = st
    shared = {k: v for k, v in by_ent.items() if len(v) >= spec["min_share"]}

    lines = ['digraph G {', 'rankdir=LR; bgcolor="white"; node [fontname="Helvetica"]; edge [fontname="Helvetica"];',
             f'labelloc="t"; fontsize=18; label="{esc(spec["title"])}";']
    # target nodes
    lines.append('{ rank=same;')
    for s in targets:
        present = "" if sym2tid.get(s) and any(s in v for v in shared.values()) else "\\n(no shared hit)"
        lines.append(f'"T:{s}" [label="{s}{present}", shape=box, style="filled,bold", fillcolor="#bcd9ff", penwidth=2];')
    lines.append('}')
    # entity nodes grouped by category cluster
    cat_of = spec.get("category", lambda nm, kind: kind)
    clusters = defaultdict(list)
    for (nm, kind) in shared: clusters[cat_of(nm, kind)].append((nm, kind))
    for ci, (cat, members) in enumerate(sorted(clusters.items())):
        lines.append(f'subgraph cluster_{ci} {{ label="{esc(cat)}"; style="rounded,dashed"; color="#999999"; fontsize=12;')
        for nm, kind in sorted(members):
            lines.append(f'"E:{nm}" [label="{esc(nm)}", shape=ellipse, style=filled, fillcolor="{KIND_FILL.get(kind,"#eeeeee")}"];')
        lines.append('}')
    # edges
    for (nm, kind), tmap in shared.items():
        for s, st in tmap.items():
            lines.append(f'"T:{s}" -> "E:{nm}" [color="{STATUS_COLOR.get(st,"#cccccc")}", penwidth=1.6];')
    # legend
    lines.append('subgraph cluster_legend { label="effect_status"; fontsize=11; style=rounded; color="#cccccc";')
    prev = None
    for st in ["affected", "implicated", "buffered", "nominal", "uncertain"]:
        lines.append(f'"L:{st}" [label="{st}", shape=plaintext, fontcolor="{STATUS_COLOR[st]}"];')
        if prev: lines.append(f'"L:{prev}" -> "L:{st}" [style=invis];')
        prev = st
    lines.append('}')
    lines.append('}')
    dot = VIZ / (spec["file"] + ".dot")
    png = VIZ / (spec["file"] + ".png")
    dot.write_text("\n".join(lines))
    subprocess.run(["dot", "-Tpng", "-Gdpi=120", str(dot), "-o", str(png)], check=True)
    print(f"  {png}  ({len(shared)} shared entities, {len(targets)} targets)")


STEROL = {"Dhcr7", "Cyp51", "Msmo1", "Insig1", "Ldlr", "Sqle", "Hmgcr", "Fdps"}
MTOR = {"Mtor", "Rptor", "Rheb", "Akt1"}
LYSO = {"Lamp2", "Atp6v0b", "Dpp7"}


def tsc_cat(nm, kind):
    if nm in STEROL: return "sterol / cholesterol biosynthesis"
    if nm in MTOR: return "mTORC1 core"
    if nm in LYSO: return "lysosomal / v-ATPase"
    return "other shared genes"


def prot_cat(nm, kind):
    if nm.startswith("Psm") or nm == "proteasome": return "proteasome subunits / complex"
    if nm in {"Ddit3", "Hsph1", "Bax", "Atf4", "Trib3"}: return "integrated stress / proteotoxic response"
    return "other shared genes"


print("Rendering convergence visualizations...")
render({
    "title": "Proteasome subunit convergence: Pomp / Psmb4 / Psmc1 / Psmc5 -> shared response",
    "file": "proteasome_convergence", "targets": ["Pomp", "Psmb4", "Psmc1", "Psmc5"],
    "min_share": 3, "kinds": {"Gene", "Complex"}, "category": prot_cat,
})
render({
    "title": "Tsc1 vs Tsc2 paralog coherence -> mTORC1 + sterol biosynthesis",
    "file": "tsc1_tsc2_coherence", "targets": ["Tsc1", "Tsc2"],
    "min_share": 2, "kinds": {"Gene", "Complex", "Pathway"}, "category": tsc_cat,
})
render({
    "title": "mSWI/SNF (BAF) complex coherence: subunit perturbations -> BAF complex node",
    "file": "baf_complex_coherence",
    "targets": ["Arid1a", "Arid1b", "Bcl11a", "Smarca2", "Smarca4", "Smarcb1",
                "Smarcc1", "Smarcc2", "Smarcd1", "Smarce1"],
    "min_share": 1, "entities": {"mSWI/SNF (BAF) complex"}, "kinds": {"Complex"},
    "category": lambda nm, kind: "chromatin-remodeling complex",
})
