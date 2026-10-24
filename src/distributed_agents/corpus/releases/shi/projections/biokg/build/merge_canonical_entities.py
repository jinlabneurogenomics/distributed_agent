#!/usr/bin/env python3
"""Posthoc canonical-entity merge for an already-built BioKG v2 graph.

This is a graph-level repair, not a pipeline rerun. It collapses synonymous
non-seed nodes (Pathway, Phenotype, Complex, Module) that the per-finding LLM
extraction emitted as separate surface forms, using:

  1. formatting normalization (case, punctuation, hyphens, Greek letters, and
     trailing decorator words like "pathway"/"signaling"/"response"), and
  2. a small curated acronym<->expansion / synonym map for the specific
     fragmented families detected during graph assessment (OXPHOS, UPR, ISR,
     UPS, and the "buffered transcriptional response" phenotype family).

Merging is confined to a single primary label. The representative node is the
variant with the most distinct target-gene support (ties broken by shortest
name). Relationships are redirected to the representative and de-duplicated.
Inputs are read from --in-dir and written to --out-dir (default: in place with
*.merged.csv plus merge_report.json), leaving the original CSVs intact.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

from ..paths import GRAPH_WORK_DIR

csv.field_size_limit(10 ** 7)

MERGE_LABELS = ("Pathway", "Phenotype", "Complex", "Module")

# TODO P2-4: the generic merge is label-blind and includes `Other`.
# The five concept labels are schema-identical (all four property-keysets appear
# under all five), and the label is the LLM extractor's per-finding `kind` choice,
# so the same concept lands under different labels and `(label, key)` can never
# reunite it -- all 347 duplicate-name groups spanned >1 label. `Other` was never
# in MERGE_LABELS at all, so its 3,737 nodes had never been deduped.
# MERGE_LABELS still scopes the SPOTTED_CLUSTERS pass, whose regexes were tuned
# against Pathway/Complex/Module only.
CONCEPT_LABELS = MERGE_LABELS + ("Other",)

GREEK = {
    "α": "alpha", "β": "beta", "γ": "gamma", "δ": "delta", "ε": "epsilon",
    "κ": "kappa", "λ": "lambda", "μ": "mu", "σ": "sigma", "ω": "omega",
}
# Decorator words that carry no biological distinction for grouping purposes.
DECORATORS = {
    "the", "a", "an", "pathway", "pathways", "signaling", "signalling",
    "signal", "response", "responses", "transcriptional", "transcriptomic",
    "program", "programme", "programs",
}

# Curated equivalence keyed on the *post-base_key* form (decorators already
# stripped). High precision: exact base-key match, not substring, so distinct
# concepts like "mitochondrial unfolded protein" (UPRmt) stay separate.
CURATED = {
    # OXPHOS
    "oxphos": "oxidative phosphorylation",
    "oxidative phosphorylation": "oxidative phosphorylation",
    # Unfolded protein response (ER UPR only; UPRmt kept separate by its prefix)
    "upr": "unfolded protein response",
    "unfolded protein": "unfolded protein response",
    "er stress unfolded protein": "unfolded protein response",
    # Integrated stress response
    "isr": "integrated stress response",
    "integrated stress": "integrated stress response",
    # Ubiquitin-proteasome system
    "ups": "ubiquitin proteasome system",
    "ubiquitin proteasome system": "ubiquitin proteasome system",
    "ubiquitin proteasome": "ubiquitin proteasome system",
    # Transcriptional-buffering synonyms that lack the literal "buffer" token
    # (the buffer* family is otherwise collapsed by the rule in canon_key).
    "transcriptionally silent": "buffered transcriptional response",
    "transcriptomic null": "buffered transcriptional response",
    "transcriptional null": "buffered transcriptional response",
}


def base_key(name: str) -> str:
    s = name.lower().strip()
    for g, r in GREEK.items():
        s = s.replace(g, r)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[\-/_]", " ", s)
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    tokens = [t for t in s.split() if t not in DECORATORS]
    return " ".join(tokens)


def canon_key(name: str) -> str:
    bk = base_key(name)
    if not bk:
        return ""  # name was entirely decorators/punctuation -> not mergeable
    # The buffering phenotype is a single dominant concept in this dataset;
    # collapse every "buffer*" variant (degree/scope adjectives are not
    # distinct phenotypes for convergence queries).
    if re.search(r"buffer", bk):
        return "buffered transcriptional response"
    return CURATED.get(bk, bk)


def token_key(name: str) -> str:
    """`canon_key` with tokens sorted, so word order stops mattering.

    Digits stay their own tokens, so "Interleukin 1" and "Interleukin 17" remain
    distinct -- the failure mode a letters-only bag-of-words hits. Subsumes
    `canon_key`: equal canon_keys always give equal token_keys.
    """
    ck = canon_key(name)
    return " ".join(sorted(ck.split())) if ck else ""


# --- Spotted-cluster cross-label dedup ---
# A targeted, manually-verified collapse of the specific synonym/acronym/label-
# split clusters found during graph assessment. This is NOT a general semantic
# dedup engine: full semantic deduplication is deferred to LLM agents run over
# the graph. Each cluster is (canonical_name, canonical_label, include_regex,
# exclude_regex); members are matched among Pathway/Complex/Module nodes, merged
# across labels into one representative carrying the canonical name+label.
# Patterns were dry-run and tightened to avoid sweeping in distinct concepts
# (e.g. non-canonical NF-kB, receptor-specific NF-kB pathways, mTORC2, PBAF/ncBAF,
# the proteasome bounce-back program, named remodeling axes).
SPOTTED_CLUSTERS = [
    ("proteasome", "Complex", r"proteasome",
     r"program|signature|bounce|compensat|perturbat|pattern|maturation|loss|-up$|"
     r"immuno|thymo|assembly|chaperone|inhibitor|activator|subunit|ubiquitin|stress"),
    ("mTORC1", "Complex", r"^(mtor|mtorc1|mtor complex 1|mechanistic target of rapamycin)$", r""),
    ("mSWI/SNF (BAF) complex", "Complex", r"\bbaf\b|swi.?snf|mswi",
     r"non-|sensitive|module|thalamic|atpase|ptpn3|response|program|related|axis|brwd|smarca"),
    ("spliceosome", "Complex", r"^spliceosom(e|al)?(\s*(complex|pathway|machinery))?$", r""),
    ("NF-kB", "Pathway", r"nf.?kappa|nf.?kb|nuclear factor kappa",
     r"non.?canonical|noncanonical|/|tlr|tnf|nod|mapk|jnk|src|pi3k|rank|myd88|irf|"
     r"flagellin|cytokine|gq|ikk|related|activator|immediate"),
    ("nucleocytoplasmic transport", "Pathway",
     r"^(nuclear transport|nucleocytoplasmic( protein)? transport|nls-dependent nucleocytoplasmic import.*)$",
     r"mrna|export"),
    ("JAK/STAT signaling pathway", "Pathway",
     r"^(cytokine[ /])?(jak[ /-]?stat|janus kinase[ /]signal transducer and activator of transcription)"
     r"( signaling)?( pathway| signaling)?$", r"clcf|crlf|gh-|gpr45|ifnar|socs|il6"),
    ("ER proteostasis", "Pathway", r"^(er|endoplasmic reticulum) proteostasis$", r"mito"),
]


# --- Post-hoc prune phase ---
# Non-seed labels that should never carry a cell-type or (for buffering) be a Pathway.
NONSEED_LABELS = ("Gene", "Complex", "Module", "Pathway", "Phenotype", "Other")
# Trailing decorator tokens appended to leaked cell-type labels, e.g.
# "CNU-HYa HY GABA cell group".
CELLTYPE_SUFFIX_TOKENS = {"cell", "type", "group", "class", "cells", "variant", "context"}


def celltype_token_sets(seed_cell_names) -> set[frozenset]:
    """Token sets of seed cell types with the leading numeric id removed."""
    out = set()
    for name in seed_cell_names:
        toks = name.lower().split()
        if toks and toks[0].isdigit():
            toks = toks[1:]
        if toks:
            out.add(frozenset(toks))
    return out


def is_leaked_celltype(name: str, seed_sets: set[frozenset]) -> bool:
    """True if a (prefix-stripped) name matches a seed cell type's token set."""
    toks = name.lower().split()
    if toks and toks[0].isdigit():
        toks = toks[1:]
    toks = [t for t in toks if t not in CELLTYPE_SUFFIX_TOKENS]
    ts = frozenset(toks)
    return len(ts) >= 2 and ts in seed_sets


def read_rows(path: Path) -> list[dict]:
    with path.open() as fh:
        return list(csv.DictReader(fh))


def write_rows(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--in-dir", type=Path, default=GRAPH_WORK_DIR)
    ap.add_argument("--out-dir", type=Path, default=None, help="Default: --in-dir.")
    args = ap.parse_args()
    out_dir = args.out_dir or args.in_dir

    node_rows = read_rows(args.in_dir / "nodes.csv")
    rel_rows = read_rows(args.in_dir / "relationships.csv")
    node_fields = list(node_rows[0].keys())
    if "aliases" not in node_fields:
        node_fields.append("aliases")   # merged-away spellings (TODO P2-4)
    rel_fields = list(rel_rows[0].keys())
    nodes = {r["id"]: r for r in node_rows}

    def primary_label(r: dict) -> str:
        labs = r["labels"].split(";")
        for lab in MERGE_LABELS:
            if lab in labs:
                return lab
        return ""

    def concept_label(r: dict) -> str:
        labs = r["labels"].split(";")
        for lab in CONCEPT_LABELS:
            if lab in labs:
                return lab
        return ""

    # Target-support per node: distinct target genes whose findings link to it.
    has_finding = defaultdict(list)  # target_id -> [finding_id]
    for r in rel_rows:
        if r["type"] == "HAS_FINDING":
            has_finding[r["start_id"]].append(r["end_id"])
    fin_to_targets = defaultdict(set)  # finding_id -> {target symbol}
    for tid, fids in has_finding.items():
        sym = nodes[tid].get("symbol") or tid
        for fid in fids:
            fin_to_targets[fid].add(sym)
    node_targets = defaultdict(set)  # entity_id -> {target symbol}
    for r in rel_rows:
        if r["type"] in ("IMPLICATES", "AFFECTS_GENE", "COMPARES_TO"):
            node_targets[r["end_id"]] |= fin_to_targets.get(r["start_id"], set())

    # Prune phase: drop buffering Pathway nodes and leaked cell-type nodes.
    seed_sets = celltype_token_sets(
        r["name"] for r in nodes.values() if "CellType" in r["labels"].split(";")
    )
    dropped: dict[str, str] = {}  # node id -> reason
    for nid, r in nodes.items():
        labset = set(r["labels"].split(";"))
        if not (labset & set(NONSEED_LABELS)):
            continue
        if "Pathway" in labset and re.search(r"buffer", r["name"].lower()):
            dropped[nid] = "buffering_pathway"
        elif is_leaked_celltype(r["name"], seed_sets):
            dropped[nid] = "leaked_celltype"
    drop_counts = Counter(dropped.values())

    # Group mergeable concept nodes by canonical key ALONE (TODO P2-4). The label
    # is deliberately not part of identity; the representative's label wins.
    groups: dict[str, list[str]] = defaultdict(list)
    for nid, r in nodes.items():
        if nid in dropped:
            continue
        if not concept_label(r):
            continue
        key = token_key(r["name"])
        if not key:
            continue  # all-decorator / unmergeable name
        groups[key].append(nid)

    remap: dict[str, str] = {}  # merged node id -> representative id
    merge_report = []
    for key, ids in groups.items():
        if len(ids) < 2:
            continue
        rep = max(ids, key=lambda i: (len(node_targets[i]), -len(nodes[i]["name"])))
        members = sorted((i for i in ids if i != rep), key=lambda i: nodes[i]["name"])
        aliases = sorted({nodes[i]["name"] for i in members})
        merged_labels = sorted({concept_label(nodes[i]) for i in ids})
        # `Other` is the extractor's catch-all, so a group that contains any
        # specifically-typed member must not inherit it: the standard concept
        # query filters on Pathway|Complex|Module|Phenotype, and demoting e.g.
        # MAPK to `Other` would drop it from that query entirely.
        if concept_label(nodes[rep]) == "Other":
            specific = Counter(
                lab for lab in (concept_label(nodes[i]) for i in ids) if lab != "Other"
            )
            if specific:
                best = min(specific, key=lambda l: (-specific[l], MERGE_LABELS.index(l)))
                nodes[rep]["labels"] = "BioKGNode;" + best
        # Keep every merged-away spelling on the representative so downstream
        # name-keyed passes (apply_llm_normalization.py) still resolve them.
        nodes[rep]["aliases"] = "|".join(aliases)
        for i in members:
            remap[i] = rep
        merge_report.append({
            "label": concept_label(nodes[rep]),
            "merged_labels": merged_labels,
            "cross_label": len(merged_labels) > 1,
            "canonical_key": key,
            "representative": nodes[rep]["name"],
            "rep_target_support": len(node_targets[rep]),
            "merged_count": len(members),
            "merged_names": aliases,
        })

    # Spotted-cluster cross-label collapse, on the survivors of the generic merge.
    # Consolidate target support across the generic remap so survivor reps carry
    # the targets of everything already merged into them.
    survivors = [nid for nid in nodes if nid not in remap and nid not in dropped]
    consolidated: dict[str, set] = defaultdict(set)
    for nid in nodes:
        if nid in dropped:
            continue
        consolidated[remap.get(nid, nid)] |= node_targets[nid]
    remap2: dict[str, str] = {}  # surviving member id -> representative id
    cluster_report = []
    for canon, lab, inc, exc in SPOTTED_CLUSTERS:
        rxi = re.compile(inc, re.I)
        rxe = re.compile(exc, re.I) if exc else None
        members = [
            nid for nid in survivors
            if primary_label(nodes[nid]) and nid not in remap2
            and rxi.search(nodes[nid]["name"])
            and not (rxe and rxe.search(nodes[nid]["name"]))
        ]
        if len(members) < 2:
            continue
        rep = max(members, key=lambda i: (len(consolidated[i]), -len(nodes[i]["name"])))
        names = sorted({nodes[i]["name"] for i in members})
        union = set().union(*(consolidated[i] for i in members))
        # Make the representative carry the canonical name + label.
        nodes[rep]["name"] = canon
        nodes[rep]["labels"] = "BioKGNode;" + lab
        nodes[rep]["kind"] = lab
        for i in members:
            if i != rep:
                remap2[i] = rep
        cluster_report.append({
            "canonical": canon, "label": lab,
            "merged_count": len(members) - 1,
            "union_target_support": len(union),
            "merged_names": names,
        })

    def resolve(x: str) -> str:
        x = remap.get(x, x)
        return remap2.get(x, x)

    # Apply prune + both remaps: drop merged/pruned nodes, redirect + dedup edges.
    gone = set(remap) | set(remap2) | set(dropped)
    kept_nodes = [r for nid, r in nodes.items() if nid not in gone]
    seen_rel = set()
    new_rels = []
    for r in rel_rows:
        if r["start_id"] in dropped or r["end_id"] in dropped:
            continue  # edge touches a pruned node
        r = dict(r)
        r["start_id"] = resolve(r["start_id"])
        r["end_id"] = resolve(r["end_id"])
        if r["start_id"] == r["end_id"]:
            continue  # self-loop created by merge
        sig = (r["start_id"], r["end_id"], r["type"], r.get("role", ""), r.get("effect_status", ""))
        if sig in seen_rel:
            continue
        seen_rel.add(sig)
        new_rels.append(r)

    write_rows(out_dir / "nodes.merged.csv", node_fields, kept_nodes)
    write_rows(out_dir / "relationships.merged.csv", rel_fields, new_rels)

    merge_report.sort(key=lambda m: -m["merged_count"])
    cluster_report.sort(key=lambda m: -m["union_target_support"])
    summary = {
        "nodes_before": len(node_rows),
        "nodes_after": len(kept_nodes),
        "nodes_pruned": len(dropped),
        "pruned_by_reason": dict(drop_counts),
        "nodes_merged_generic": len(remap),
        "nodes_merged_spotted_clusters": len(remap2),
        "rels_before": len(rel_rows),
        "rels_after": len(new_rels),
        "merge_groups": len(merge_report),
        "spotted_clusters": len(cluster_report),
        "by_label": dict(Counter(m["label"] for m in merge_report)),
    }
    (out_dir / "merge_report.json").write_text(
        json.dumps(
            {"summary": summary, "spotted_cluster_merges": cluster_report, "merges": merge_report},
            indent=2,
        )
    )
    print(json.dumps(summary, indent=2))
    print("\nSpotted-cluster cross-label dedup:")
    for m in cluster_report:
        print(f"  [{m['label']}] {m['canonical']!r}  <- {m['merged_count']} variants  (union={m['union_target_support']} tgts)")


if __name__ == "__main__":
    main()
