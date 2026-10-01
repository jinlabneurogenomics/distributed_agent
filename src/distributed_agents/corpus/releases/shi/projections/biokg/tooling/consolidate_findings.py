#!/usr/bin/env python3
"""Deterministic finding consolidation: ranked relational ledger + BioKG -> deduplicated,
archetype-tagged story hubs, each with the minimal set of findings to read.

This is the computational half of candidate story consolidation. It does NOT
interpret: grouping, dedup, archetype classification, and read-set selection
are graph queries plus set operations. The agent consumes the output and spends
its reasoning on the irreducible semantic mile: significance, where to cut a
convergence hub, polarity, and naming.

Method (all deterministic; connected components, no community detection)
------------------------------------------------------------------------
Two role-edges carry the two story archetypes (REPORTS_GENE.role):
  * comparator  (finding_reported_comparator): peer comparison -> within-complex contrast
  * downstream  (finding_reported_gene):       shared DEG program -> convergence of effect

1. Build a comparator gene-graph (reciprocal, over the ledger's genes) -> connected components.
   A multi-gene component is a COMPARISON hub (its members name each other as peers).
2. Build a downstream finding-graph (findings sharing >= MIN_SHARED readout genes) -> components.
   A component that spans >= 2 comparator components is a CONVERGENCE hub (different upstream
   lesions, one downstream program — they never name each other).
3. Route every ledger finding finding-level:
     - has comparator peers, gene is comparator-connected            -> COMPARISON
     - comparator-silent, but its readout crosses >= 2 comp components -> CONVERGENCE  (e.g. Rab7:F003 sterol)
     - comparator-silent, readout stays within its own comp component -> COMPARISON   (e.g. Mga:F001 rides its gene)
     - otherwise                                                       -> singleton
4. Per hub emit archetype, rank (max R_band of members), members, and the MINIMAL READ-SET:
     - COMPARISON: the finding naming the most other members as comparators (the contrast).
     - CONVERGENCE: one representative finding per BRANCH, where a branch = a comparator
       sub-component inside the convergence hub (this is the deterministic proxy for the
       "distinct upstream branches" an agent would otherwise have to label by hand).

NO engagement gate: self-knockdown / "was it engaged" is an artifact in this assay (self-KD is
uncorrelated with downstream effect), so non-response is taken at face value; a single blanket
guide-efficacy caveat replaces any per-member filtering.

Run
---
    python -m distributed_agents.corpus.launch biokg.tooling.consolidate_findings \
        --ledger /path/to/relational_findings.csv \
        --out /tmp/hubs.csv
Requires a live, host-managed Neo4j. Task-time model sandboxes must not start
or rebuild the service.
"""
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

import networkx as nx

CYPHER = Path(__file__).resolve().parent / "biokg_cypher.py"
CACHE = Path(tempfile.gettempdir()) / "biokg_consolidate_cache"

Q_COMENTION = """
MATCH (a:TargetGene)-[:HAS_FINDING]->(f:Finding)
      -[:REPORTS_GENE {role:'finding_reported_comparator'}]->(g:Gene)
MATCH (b:TargetGene) WHERE b.name = g.name AND a.name <> b.name
RETURN a.name AS src, b.name AS dst, count(DISTINCT f) AS n
"""
Q_COMPARATOR = """
MATCH (tg:TargetGene)-[:HAS_FINDING]->(f:Finding)
      -[:REPORTS_GENE {role:'finding_reported_comparator'}]->(g:Gene)
RETURN tg.name AS gene, f.finding_id AS fid, collect(DISTINCT g.name) AS genes
"""
Q_DOWNSTREAM = """
MATCH (tg:TargetGene)-[:HAS_FINDING]->(f:Finding)
      -[:REPORTS_GENE {role:'finding_reported_gene'}]->(g:Gene)
RETURN tg.name AS gene, f.finding_id AS fid, collect(DISTINCT g.name) AS genes
"""
Q_FTYPE = """
MATCH (tg:TargetGene)-[:HAS_FINDING]->(f:Finding)
RETURN tg.name AS gene, f.finding_id AS fid, f.finding_type AS ftype
"""
# finding_types that state a relational claim (preferred for a comparison hub's read-set)
CONTRAST_TYPES = {"cross_perturbation_contrast", "convergent_module",
                  "pathway_uncoupling", "non_interchangeability", "homeostatic_compensation"}


def run_cypher(query: str) -> list[dict]:
    with tempfile.NamedTemporaryFile("w", suffix=".cypher", delete=False) as fh:
        fh.write(query)
        qpath = fh.name
    proc = subprocess.run([sys.executable, str(CYPHER), "--file", qpath, "--format", "json"],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        sys.exit(
            "biokg_cypher failed; the host-managed graph is unavailable. "
            f"Do not start services from a model sandbox.\n{proc.stderr}"
        )
    return json.loads(proc.stdout)


def cached(name: str, query: str, refresh: bool) -> list[dict]:
    CACHE.mkdir(parents=True, exist_ok=True)
    p = CACHE / f"{name}.json"
    if p.exists() and not refresh:
        return json.loads(p.read_text())
    rows = run_cypher(query)
    p.write_text(json.dumps(rows))
    return rows


def load_ledger(path: Path) -> list[dict]:
    rows = []
    for r in csv.DictReader(path.open()):
        r["_fid"] = f"{r['gene']}:{r['finding_id']}"
        try:
            r["_rank"] = int(r.get("R_band") or 0)
        except ValueError:
            r["_rank"] = 0
        rows.append(r)
    return rows


def consolidate(ledger, dw, comp, down, ftype, min_shared, recip_t, read_k=3):
    fids = [r["_fid"] for r in ledger]
    fid_gene = {r["_fid"]: r["gene"] for r in ledger}
    fid_rank = {r["_fid"]: r["_rank"] for r in ledger}
    genes = set(fid_gene.values())

    # 1. comparator gene-communities (reciprocal graph over ledger genes). Raw connected
    #    components leave one giant blob (the whole complex-of-complexes is weakly chained);
    #    fixed-seed Louvain subdivides it into the real complexes. This is a reproducible
    #    computation (no LLM, no judgment), just community detection rather than raw CC.
    # NB: insert nodes/edges in sorted order so the graph is byte-identical across processes
    # (Python set/dict iteration order varies with hash randomization; Louvain is order-sensitive).
    Gc = nx.Graph()
    Gc.add_nodes_from(sorted(genes))
    for (s, d) in sorted(dw):
        n = dw[(s, d)]
        if s in genes and d in genes and s < d and (d, s) in dw and min(n, dw[(d, s)]) >= recip_t:
            Gc.add_edge(s, d, weight=min(n, dw[(d, s)]))
    communities = nx.community.louvain_communities(Gc, weight="weight", seed=1)
    gene_comp = {g: i for i, c in enumerate(communities) for g in c}
    comp_size = Counter(gene_comp.values())

    # 2. downstream finding-graph (shared readout, excluding ledger targets themselves)
    dn = {f: (set(down.get(f, set())) - genes) for f in fids}
    Gd = nx.Graph()
    Gd.add_nodes_from(fids)
    for i in range(len(fids)):
        for j in range(i + 1, len(fids)):
            if len(dn[fids[i]] & dn[fids[j]]) >= min_shared:
                Gd.add_edge(fids[i], fids[j])
    down_clu = {f: c for c in nx.connected_components(Gd) for f in c}

    # 3. route each finding
    assign = {}
    for f in fids:
        g = fid_gene[f]
        is_cmp_gene = comp_size[gene_comp[g]] >= 2
        f_comps = set(comp.get(f, set())) & genes
        clu = down_clu.get(f, {f})
        clu_components = {gene_comp[fid_gene[x]] for x in clu if x in fid_gene}
        cross_component = len(clu_components) >= 2
        if is_cmp_gene and (f_comps or not cross_component):
            assign[f] = ("CMP", gene_comp[g])
        elif cross_component:
            assign[f] = ("CNV", frozenset(clu))
        elif is_cmp_gene:
            assign[f] = ("CMP", gene_comp[g])
        else:
            assign[f] = ("SGL", f)

    # 4. build hubs
    hub_members = defaultdict(list)
    for f, key in assign.items():
        hub_members[key].append(f)

    hubs = []
    for key, members in hub_members.items():
        # a lone finding is a singleton whatever route it took (convergence/comparison need >=2)
        arche = ("SINGLETON" if len(members) == 1
                 else {"CMP": "COMPARISON", "CNV": "CONVERGENCE", "SGL": "SINGLETON"}[key[0]])
        hgenes = sorted({fid_gene[f] for f in members})
        rank = max(fid_rank[f] for f in members)
        # minimal read-set
        if arche == "COMPARISON":
            # A comparison hub can hold >1 sub-conclusion (e.g. Myc-network = MAX/MGA->Stag3
            # AND Mnt->clock). Don't pick one "headline" structurally — surface the top-K
            # contrast findings (findings naming the most OTHER members, contrast-type first)
            # and let the agent read them and decide.
            scored = []
            for f in members:
                named = len({x for x in comp.get(f, set()) if x in hgenes and x != fid_gene[f]})
                scored.append((f, named, ftype.get(f, "") in CONTRAST_TYPES, fid_rank[f]))
            cand = [s for s in scored if s[1] >= 2] or scored
            cand.sort(key=lambda s: (-s[1], -int(s[2]), -s[3]))
            read_set = [s[0] for s in cand[:read_k]]
            branches = []
        elif arche == "CONVERGENCE":
            # branch = comparator sub-component within the hub
            branch_of = defaultdict(list)
            for f in members:
                branch_of[gene_comp[fid_gene[f]]].append(f)
            branches = [sorted({fid_gene[f] for f in fs}) for fs in branch_of.values()]
            read_set = [max(fs, key=lambda f: fid_rank[f]) for fs in branch_of.values()]
        else:
            read_set = members
            branches = []
        # consensus downstream readout (convergence signal), genes in >=40% of members
        dcount = Counter(x for f in members for x in dn[f])
        shared_readout = sorted(x for x, c in dcount.items() if c >= max(2, 0.4 * len(members)))
        hubs.append({
            "archetype": arche, "rank_R_band": rank, "n_genes": len(hgenes),
            "n_findings": len(members), "genes": "|".join(hgenes),
            "member_findings": "|".join(sorted(members)),
            "read_set": "|".join(sorted(read_set)),
            "n_branches": len(branches),
            "branches": " ; ".join("/".join(b) for b in branches),
            "shared_readout": "|".join(shared_readout[:20]),
        })
    # rank: by R_band desc, then size desc; keep multi-finding hubs before singletons
    hubs.sort(key=lambda h: (h["archetype"] == "SINGLETON", -h["rank_R_band"], -h["n_findings"], -h["n_genes"]))
    for i, h in enumerate(hubs, 1):
        h["hub_id"] = i
    return hubs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", type=Path, required=True,
                    help="ranked relational finding ledger CSV")
    ap.add_argument("--out", type=Path, required=True, help="output CSV of hubs")
    ap.add_argument("--min-shared", type=int, default=3, help="downstream genes shared to link (convergence)")
    ap.add_argument("--recip-threshold", type=int, default=1, help="reciprocal comparator weight")
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args()

    ledger = load_ledger(args.ledger)
    dw = {(e["src"], e["dst"]): e["n"] for e in cached("comention", Q_COMENTION, args.refresh)}
    comp = {f"{d['gene']}:{d['fid']}": set(d["genes"]) for d in cached("comparator", Q_COMPARATOR, args.refresh)}
    down = {f"{d['gene']}:{d['fid']}": set(d["genes"]) for d in cached("downstream", Q_DOWNSTREAM, args.refresh)}
    ftype = {f"{d['gene']}:{d['fid']}": (d.get("ftype") or "") for d in cached("ftype", Q_FTYPE, args.refresh)}

    hubs = consolidate(ledger, dw, comp, down, ftype, args.min_shared, args.recip_threshold)
    cols = ["hub_id", "archetype", "rank_R_band", "n_genes", "n_findings", "n_branches",
            "genes", "branches", "read_set", "shared_readout", "member_findings"]
    with args.out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(hubs)

    n = Counter(h["archetype"] for h in hubs)
    multi = [h for h in hubs if h["n_findings"] > 1]
    print(f"{len(ledger)} ledger findings -> {len(hubs)} hubs "
          f"({n.get('COMPARISON',0)} comparison, {n.get('CONVERGENCE',0)} convergence, {n.get('SINGLETON',0)} singleton)")
    print(f"wrote {args.out}")
    print("\ntop multi-finding hubs (rank / archetype / #f / read-set size):")
    for h in multi[:12]:
        rs = len(h["read_set"].split("|"))
        print(f"  #{h['hub_id']:<3} R{h['rank_R_band']} {h['archetype']:<11} {h['n_findings']:>2}f/{h['n_genes']:>2}g "
              f"read={rs:<2} {h['genes'][:52]}")


if __name__ == "__main__":
    main()
