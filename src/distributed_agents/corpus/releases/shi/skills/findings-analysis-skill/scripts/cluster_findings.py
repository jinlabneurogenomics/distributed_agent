#!/usr/bin/env python3
"""Deterministic two-archetype Claim clusterer for optional graph routing.

Clusters a task-selected pool of Claims or Findings into candidate story units
using the two archetypes on cleanly separated edge types:

  CONVERGENCE  edges: findings sharing >= --min-shared downstream `genes` (IDF-weighted,
                      hub-capped at --hubcap) -> convergence-of-effect (sterol/SREBP2, ISR/ATF4).
  COMPARATOR   edges: findings whose targets name each other (reciprocal) or share
                      >= --comp-min-shared named comparators (IDF-weighted) -> peer-comparison /
                      non-interchangeability (cohesin, MAX/MGA, NMDAR, Mediator).

Keeping the two roles on separate edge types is load-bearing: mixing them bridges hubs into
blobs. Louvain at --resolution (the granularity dial; tighten as the pool
grows). Communities > --maxsize are recursively re-split at escalating resolution so a genuine
multi-program blob breaks into driver sub-stories while a coherent large program stays whole.
Polarity (convergence vs "did-not-phenocopy"), where-to-cut, and naming stay with the reader/LLM.

Input : --pool-in, a task-selected pool with a `doc_id` column and optional
        routing score; .csv or .json.
        Claim IDs resolve through the frozen BioKG Claim artifact; Finding IDs remain
        supported when that artifact is absent or explicitly bypassed.
Output: <out-dir>/clusters.json  (reader-ready: per cluster archetype_hint, members, read_set,
        shared_core, comparators, prose_index), clusters.md (human-readable), and one compact
        description-only cluster_prose/<cluster_id>.md file per cluster for semantic adjudication.

Usage:
  python cluster_findings.py --pool-in candidate_claims.csv --out-dir ./clust --resolution 2.4
  python cluster_findings.py --pool-in pool.csv --out-dir ./clust --sweep   # size dists per res
"""
import argparse, csv, importlib.util, json, math, sys
from collections import Counter, defaultdict
from pathlib import Path

import networkx as nx

HERE = Path(__file__).resolve().parent
RELEASE_ROOT = HERE.parents[2]
PROJECTIONS_ROOT = RELEASE_ROOT / "projections"
if str(PROJECTIONS_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECTIONS_ROOT))

from biokg.build.claim_layer import (  # noqa: E402
    DEFAULT_ASSIGNMENTS,
    DEFAULT_LEDGER,
    claim_cards,
    read_ledger as read_claim_ledger,
    read_tsv as read_claim_tsv,
    validate_assignments,
)

# The relational SET is a metadata filter (E2E doctrine): these four finding_type classes
# capture ~99% of the consolidated relational gold. The fine rel_type (convergence / divergence /
# non-interchangeability / paralog-contrast / epistasis) is a READING sub-label of these, not a
# separate filter. This is a RECALL filter (do not miss a buried divergence), NOT a score rank.
DEFAULT_RELATIONAL_CLASSES = {
    "convergent_module", "cross_perturbation_contrast", "pathway_uncoupling", "homeostatic_compensation",
}


def _loader():
    spec = importlib.util.spec_from_file_location("sf", HERE / "score_findings.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def read_pool(path: str):
    """Return [(doc_id, lane_score)] from a --pool-in .csv (doc_id[,lane_score]) or .json list.
    If no usable score column, rank by row order (first row = highest)."""
    p = Path(path)
    rows = []
    if p.suffix == ".json":
        for r in json.loads(p.read_text()):
            rows.append((r["doc_id"], float(r.get("lane_score") or 0.0)))
    else:
        rdr = list(csv.DictReader(p.read_text().splitlines()))
        for r in rdr:
            d = r.get("doc_id") or r.get("doc") or ""
            if not d:
                continue
            sc = r.get("lane_score") or r.get("score") or ""
            rows.append((d, float(sc) if sc else 0.0))
    if rows and all(s == 0.0 for _, s in rows):
        n = len(rows)
        rows = [(d, float(n - i)) for i, (d, _) in enumerate(rows)]
    return rows


def _target_names(value):
    if isinstance(value, str):
        return frozenset([value]) if value else frozenset()
    return frozenset(value or [])


def add_routing_edges(G, path, valid_nodes):
    """Add typed Claim/router edges without treating them as hard merges."""
    if not path:
        return 0
    edge_path = Path(path)
    if not edge_path.is_file():
        raise FileNotFoundError(edge_path)
    added = 0
    for row in csv.DictReader(edge_path.read_text().splitlines(), delimiter="\t"):
        left = row.get("source_claim_id") or ""
        right = row.get("target_claim_id") or ""
        if left not in valid_nodes or right not in valid_nodes or left == right:
            continue
        edge_type = row.get("edge_type") or "ROUTING"
        try:
            weight = float(row.get("weight") or 1.0)
        except ValueError:
            weight = 1.0
        kind = "comp" if edge_type == "CONTRASTS_WITH" else "route"
        if G.has_edge(left, right):
            G[left][right]["weight"] += weight
            kinds = set(G[left][right].get("routing_kinds") or [])
            kinds.add(edge_type)
            G[left][right]["routing_kinds"] = sorted(kinds)
        else:
            G.add_edge(
                left,
                right,
                weight=weight,
                kind=kind,
                routing_kinds=[edge_type],
            )
        added += 1
    return added


def build_graph(DOCS, REC, TARGET, *, min_shared, hubcap, comp_min_shared, comp_w=1.0, conv_w=1.0):
    G = nx.Graph()
    G.add_nodes_from(DOCS)
    # ---- convergence edges (shared downstream readout genes) ----
    down = {
        d: frozenset(
            g
            for g in REC[d]["genes"]
            if g.casefold() not in {target.casefold() for target in _target_names(TARGET[d])}
        )
        for d in DOCS
    }
    df = Counter(g for d in DOCS for g in sorted(down[d], key=str.casefold))
    N = max(len(DOCS), 1)
    idf = {g: math.log(N / c) for g, c in df.items()}
    downcap = {d: frozenset(g for g in down[d] if df[g] <= hubcap) for d in DOCS}
    for i in range(len(DOCS)):
        a = DOCS[i]; Ai = downcap[a]
        if not Ai:
            continue
        for j in range(i + 1, len(DOCS)):
            b = DOCS[j]; shared = Ai & downcap[b]
            if len(shared) >= min_shared:
                w = conv_w * sum(idf[g] for g in sorted(shared, key=str.casefold))
                if G.has_edge(a, b):
                    G[a][b]["weight"] += w
                else:
                    G.add_edge(a, b, weight=w, kind="conv")
    # ---- comparator edges (targets naming each other / shared comparators) ----
    comp = {d: frozenset(REC[d]["comparators"]) for d in DOCS}
    cdf = Counter(c for d in DOCS for c in sorted(comp[d], key=str.casefold))
    cidf = {c: math.log(N / n) for c, n in cdf.items()}
    for i in range(len(DOCS)):
        a = DOCS[i]; Ta = _target_names(TARGET[a]); Ca = comp[a]
        for j in range(i + 1, len(DOCS)):
            b = DOCS[j]; Tb = _target_names(TARGET[b]); Cb = comp[b]
            w = 0.0
            w += sum(
                cidf.get(target, 0.0) for target in sorted(Tb & Ca, key=str.casefold)
            )
            w += sum(
                cidf.get(target, 0.0) for target in sorted(Ta & Cb, key=str.casefold)
            )
            sh = sorted((c for c in Ca & Cb if cdf[c] <= hubcap), key=str.casefold)
            if len(sh) >= comp_min_shared:
                w += 0.5 * sum(cidf[c] for c in sh)
            if w > 0:
                w *= comp_w
                if G.has_edge(a, b):
                    G[a][b]["weight"] += w
                else:
                    G.add_edge(a, b, weight=w, kind="comp")
    return G


def louvain(G, resolution, seed=1):
    # NetworkX's seeded Louvain can still vary across Python processes when
    # string-node set iteration follows a randomized hash order. Canonicalize
    # to stable integer IDs and edge insertion order before community detection.
    nodes = sorted(G.nodes, key=str.casefold)
    to_int = {node: index for index, node in enumerate(nodes)}
    canonical = nx.Graph()
    canonical.add_nodes_from(range(len(nodes)))
    edges = sorted(
        G.edges(data=True),
        key=lambda edge: tuple(sorted((to_int[edge[0]], to_int[edge[1]]))),
    )
    for left, right, data in edges:
        canonical.add_edge(to_int[left], to_int[right], **data)
    communities = nx.community.louvain_communities(
        canonical, weight="weight", resolution=resolution, seed=seed
    )
    return [{nodes[index] for index in community} for community in communities]


def split_big(G, comm, maxsize, base_res, seed=1):
    out = []
    for c in comm:
        if len(c) <= maxsize:
            out.append(c); continue
        sub = G.subgraph(c); res = base_res; pieces = [c]
        for _ in range(6):
            res *= 1.6
            p = louvain(sub, res, seed)
            if len(p) > 1:
                pieces = p; break
        out.extend(split_big(G, pieces, maxsize, res, seed) if len(pieces) > 1 else [c])
    return out


def archetype_hint(G, members):
    """convergence vs divergence(comparator) by dominant intra-cluster edge kind."""
    conv = comp = 0.0
    for i, a in enumerate(members):
        for b in members[i + 1:]:
            if G.has_edge(a, b):
                ed = G[a][b]
                if ed.get("kind") == "conv":
                    conv += ed["weight"]
                elif ed.get("kind") == "comp":
                    comp += ed["weight"]
    if conv == comp == 0:
        return "mixed_routing"
    return "convergence" if conv >= comp else "divergence"


# ---------------------------------------------------------------------------
# BATCH mode (routing for the batched-worker synthesis pipeline).
#
# Story boundaries and ranking are irreducibly semantic, so we do not
# ask the graph to define stories here. Instead we ROUTE: partition the WHOLE pool into a
# small number of THEME-COHERENT batches, each sized for one worker to consolidate in-context
# (a single agent handled ~648 findings -> 25 stories). A whole convergence theme (e.g. sterol)
# must land WHOLLY in one batch so no cross-worker fragmentation is possible; blobbing at THIS
# level is fine (the worker makes the mechanism cut). Every finding is routed to some batch —
# the isolated long-tail is pooled into a residual batch so 2-member divergences / singletons
# still get read, not just the hubs.
# ---------------------------------------------------------------------------
def _inter_weights(G, comms):
    """Sum of edge weights BETWEEN each pair of communities (by list index)."""
    idx = {n: i for i, c in enumerate(comms) for n in c}
    W = defaultdict(float)
    for a, b, d in G.edges(data=True):
        ia, ib = idx[a], idx[b]
        if ia != ib:
            W[(min(ia, ib), max(ia, ib))] += d["weight"]
    return W


def merge_to_n(G, comms, n_target):
    """Reduce to ~n_target communities by repeatedly folding the SMALLEST community into its
    most-connected neighbor. Merging only GROWS communities (never splits), so a theme stays
    whole; eliminating the smallest each round avoids the rich-get-richer snowball that a
    greedy max-weight merge produces. Isolated (no inter-community edge) communities are left
    for residual pooling."""
    comms = [set(c) for c in comms]
    while len(comms) > n_target:
        W = _inter_weights(G, comms)
        if not W:
            break
        merged = False
        for i in sorted(range(len(comms)), key=lambda k: len(comms[k])):  # smallest first
            best_j, best_w = None, 0.0
            for (a, b), w in W.items():
                if a == i or b == i:
                    j = b if a == i else a
                    if w > best_w:
                        best_j, best_w = j, w
            if best_j is not None:
                lo, hi = sorted((i, best_j))
                comms[lo] |= comms[hi]
                del comms[hi]
                merged = True
                break
        if not merged:  # every remaining community is isolated
            break
    return comms


def build_batches(G, DOCS, SCORE, *, coarse_resolution, n_batches, batch_cap):
    """Coarse-cluster -> merge to ~n_batches theme-coherent groups -> pool the isolated
    long-tail into a residual batch -> cap-split anything larger than one worker can hold."""
    comm = louvain(G, coarse_resolution)
    comm = merge_to_n(G, comm, n_batches)
    # pool fully-isolated (degree-0) singletons into ONE residual long-tail batch
    connected, residual = [], set()
    for c in comm:
        if len(c) == 1 and G.degree(next(iter(c))) == 0:
            residual |= c
        else:
            connected.append(set(c))
    # a batch bigger than one worker's capacity is re-split (sub-themes stay together)
    connected = split_big(G, connected, batch_cap, coarse_resolution)
    if residual:
        # the residual can itself exceed the cap; chunk it deterministically by score order
        res_sorted = sorted(residual, key=lambda d: (-SCORE[d], d.casefold()))
        for k in range(0, len(res_sorted), batch_cap):
            connected.append(set(res_sorted[k:k + batch_cap]))
    return sorted(
        connected,
        key=lambda c: (-max(SCORE[d] for d in c), min(d.casefold() for d in c)),
    )


def describe_unit(G, mem, REC, TARGET, SCORE, readset_size):
    """Shared per-unit descriptor (shared_core downstream genes, top comparators, members,
    read_set) used by both cluster and batch emit."""
    down = defaultdict(int)
    for d in mem:
        for g in REC[d]["genes"]:
            if g.casefold() not in {target.casefold() for target in _target_names(TARGET[d])}:
                down[g] += 1
    shared_core = [g for g, n in sorted(down.items(), key=lambda x: (-x[1], x[0])) if n >= 2][:14]
    comps = Counter(cc for d in mem for cc in REC[d]["comparators"])
    routing = Counter()
    for index, left in enumerate(mem):
        for right in mem[index + 1:]:
            if G.has_edge(left, right):
                routing.update(G[left][right].get("routing_kinds") or [])
    return {
        "n": len(mem),
        "archetype_hint": archetype_hint(G, mem) if len(mem) > 1 else "singleton",
        "targets": sorted({target for d in mem for target in _target_names(TARGET[d])}),
        "read_set": [d for d in mem[:readset_size]],
        "shared_core": shared_core,
        "top_comparators": [c for c, _ in comps.most_common(10)],
        "routing_relations": [kind for kind, _ in routing.most_common(10)],
        "members": [{"gene_target": REC[d]["gene_target"], "finding_id": REC[d]["finding_id"],
                     "doc_id": d, "finding_type": REC[d].get("finding_type") or "",
                     "unit_kind": REC[d].get("unit_kind") or "finding",
                     "direction": REC[d].get("direction") or "",
                     "literature_status": REC[d].get("literature_status") or "",
                     "source_finding_count": int(REC[d].get("member_count") or 1),
                     "lane_score": SCORE[d]} for d in mem],
    }


def load_claim_records(assignments_path, ledger_path=DEFAULT_LEDGER):
    ledger = read_claim_ledger(Path(ledger_path))
    assignments = read_claim_tsv(Path(assignments_path))
    validate_assignments(assignments, ledger)
    records = {}
    for card in claim_cards(assignments, ledger):
        records[card["claim_id"]] = {
            "doc_id": card["claim_id"],
            "unit_kind": "claim",
            "gene_target": card["targets"][0] if card["targets"] else "",
            "targets": card["targets"],
            "primary_anchors": card["primary_anchors"],
            "supporting_targets": card["supporting_targets"],
            "implication_targets": card["implication_targets"],
            "boundary_targets": card["boundary_targets"],
            "target_roles": card["target_roles"],
            "finding_id": "",
            "finding_type": card["relation_family"],
            "direction": card["direction_pattern"],
            "confidence": card["confidence"],
            "literature_status": "",
            "summary": card["canonical_summary"],
            "why_it_matters": "",
            "genes": card["readouts"] or card["genes"],
            "comparators": card["comparators"],
            "cell_types": card["cell_scope"],
            "member_count": card["member_count"],
            "member_doc_ids": [member["doc_id"] for member in card["members"]],
            "de_support_level": card["de_support_level"],
            "de_direction": card["de_direction"],
            "de_support_count": card["de_support_count"],
        }
    return records


def write_prose_index(path, unit_id, unit, REC, *, target_label):
    """Write compact finding descriptions without expanding to reports or raw DE rows."""
    claim_mode = all(
        REC[member["doc_id"]].get("unit_kind") == "claim" for member in unit["members"]
    )
    unit_label = "claims" if claim_mode else "findings"
    lines = [
        f"# {unit_id} — {unit['n']} {unit_label}; {target_label}: "
        f"{', '.join(unit['targets'][:40])}\n"
    ]
    for member in unit["members"]:
        finding = REC[member["doc_id"]]
        summary = " ".join((finding.get("summary") or "").split())
        comparators = ",".join(finding.get("comparators", [])[:8])
        if finding.get("unit_kind") == "claim":
            readouts = ",".join(finding.get("genes", [])[:12])
            cells = ",".join(finding.get("cell_types", [])[:4])
            anchors = ",".join(finding.get("primary_anchors", []))
            supporting = ",".join(finding.get("supporting_targets", []))
            implications = ",".join(finding.get("implication_targets", []))
            boundaries = ",".join(finding.get("boundary_targets", []))
            de = finding.get("de_support_level") or "not_applicable"
            if finding.get("de_direction"):
                de += f"/{finding['de_direction']}"
            lines.append(
                f"- {member['doc_id']} [{member['finding_type']}] "
                f"anchors={anchors} supporting={supporting} "
                f"implications={implications} boundaries={boundaries} "
                f"readouts={readouts} cells={cells} de={de} comps={comparators}\n"
                f"    summary: {summary}"
            )
            continue
        why = " ".join((finding.get("why_it_matters") or "").split())
        lines.append(
            f"- {member['doc_id']} [{member['finding_type']}] "
            f"dir={member['direction']} lit={member['literature_status']} "
            f"comps={comparators}\n"
            f"    summary: {summary}\n    why: {why}"
        )
    path.write_text("\n".join(lines) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pool-in", default=None, help="ranked pool: .csv (doc_id[,lane_score]) or .json list")
    ap.add_argument("--relational-prefilter", action="store_true",
                    help="build the pool DIRECTLY from the ledger's relational finding_type classes "
                         "(recall filter, NO score rank) instead of --pool-in")
    ap.add_argument("--relational-class", action="append", dest="relational_classes", default=[],
                    help="override the relational finding_type classes (repeatable)")
    ap.add_argument("--ledger-path", default=None, help="findings ledger (default: skill resolver)")
    ap.add_argument("--claim-assignments", default=str(DEFAULT_ASSIGNMENTS),
                    help="frozen Claim assignments used when --pool-in contains Claim IDs")
    ap.add_argument("--claim-ledger", default=str(DEFAULT_LEDGER),
                    help="flat findings ledger used to construct Claim reader cards")
    ap.add_argument("--routing-edges", default=None,
                    help="optional task-aware Claim routing-edge TSV from route_claims.py")
    ap.add_argument("--out-dir", default=".")
    ap.add_argument("--resolution", type=float, default=2.4, help="Louvain granularity dial (tighten as pool grows)")
    ap.add_argument("--maxsize", type=int, default=20, help="re-split communities larger than this")
    ap.add_argument("--hubcap", type=int, default=120, help="drop a gene/comparator appearing in > this many findings")
    ap.add_argument("--min-shared", type=int, default=3, help="min shared downstream genes for a convergence edge")
    ap.add_argument("--comp-min-shared", type=int, default=2, help="min shared comparators for a comparator edge")
    ap.add_argument("--readset-size", type=int, default=4, help="top-N members (by score) as each cluster's read_set")
    ap.add_argument("--sweep", action="store_true", help="print community-size distributions across resolutions and exit")
    ap.add_argument("--emit", choices=["clusters", "batches"], default="clusters",
                    help="clusters = fine story-units (per-cluster readers); "
                         "batches = few theme-coherent worker batches (batched-worker synthesis)")
    ap.add_argument("--n-batches", type=int, default=6, help="[--emit batches] target number of worker batches")
    ap.add_argument("--batch-cap", type=int, default=300, help="[--emit batches] max findings per batch (worker capacity)")
    ap.add_argument("--coarse-resolution", type=float, default=1.0,
                    help="[--emit batches] LOW Louvain resolution for coarse theme communities before merge")
    a = ap.parse_args()

    sf = _loader()
    findings = sf.load_findings(sf.ledger_path(a.ledger_path))
    by_id = {f["doc_id"]: f for f in findings}

    DOCS, SCORE, REC, TARGET = [], {}, {}, {}
    if a.relational_prefilter or a.relational_classes:
        classes = set(a.relational_classes) or DEFAULT_RELATIONAL_CLASSES
        for f in findings:
            if (f.get("finding_type") or "") in classes:
                d = f["doc_id"]; DOCS.append(d); SCORE[d] = 0.0; REC[d] = f; TARGET[d] = f["gene_target"]
        print(f"relational-class prefilter: {len(DOCS)} findings in {sorted(classes)} (recall filter, no score)")
    else:
        if not a.pool_in:
            ap.error("provide --pool-in or --relational-prefilter")
        pool = read_pool(a.pool_in)
        if any(d.startswith("claim:") for d, _ in pool):
            claim_path = Path(a.claim_assignments)
            if not claim_path.exists():
                ap.error(f"Claim pool requires frozen assignments at {claim_path}")
            by_id.update(load_claim_records(claim_path, a.claim_ledger))
        missing = 0
        for d, sc in pool:
            f = by_id.get(d)
            if f is None:
                missing += 1
                continue
            DOCS.append(d); SCORE[d] = sc; REC[d] = f; TARGET[d] = f.get("targets") or f["gene_target"]
        pool_label = "claims" if any(d.startswith("claim:") for d in DOCS) else "findings"
        print(f"pool: {len(DOCS)} {pool_label} clustered ({missing} IDs not found, skipped)")

    unit_label = "claims" if DOCS and all(d.startswith("claim:") for d in DOCS) else "findings"

    G = build_graph(DOCS, REC, TARGET, min_shared=a.min_shared, hubcap=a.hubcap,
                    comp_min_shared=a.comp_min_shared)
    nrouting = add_routing_edges(G, a.routing_edges, set(DOCS))
    nconv = sum(1 for _, _, d in G.edges(data=True) if d.get("kind") == "conv")
    ncomp = sum(1 for _, _, d in G.edges(data=True) if d.get("kind") == "comp")
    print(f"graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges "
          f"({nconv} conv, {ncomp} comp, {nrouting} routed records), "
          f"{sum(1 for d in DOCS if G.degree(d) == 0)} isolated")

    if a.sweep:
        for res in (1.0, 1.5, 2.0, 2.4, 3.0, 4.0):
            cm = split_big(G, louvain(G, res), a.maxsize, res)
            multi = sum(1 for c in cm if len(c) >= 2)
            print(f"  res={res:<4} communities={len(cm):>3} multi={multi:>3} "
                  f"singletons={sum(1 for c in cm if len(c) == 1):>3} "
                  f"biggest={max((len(c) for c in cm), default=0):>3}")
        return

    out = Path(a.out_dir); out.mkdir(parents=True, exist_ok=True)

    if a.emit == "batches":
        comm = build_batches(G, DOCS, SCORE, coarse_resolution=a.coarse_resolution,
                             n_batches=a.n_batches, batch_cap=a.batch_cap)
        batches, lines = [], [f"# Relational worker batches (theme-coherent routing, "
                              f"coarse_res={a.coarse_resolution}, n_batches~={a.n_batches}, "
                              f"cap={a.batch_cap}) — {len(comm)} batches from {len(DOCS)} "
                              f"{unit_label}\n"]
        prose_dir = out / "batch_prose"; prose_dir.mkdir(exist_ok=True)
        for i, c in enumerate(comm, 1):
            mem = sorted(c, key=lambda d: (-SCORE[d], d.casefold()))
            u = describe_unit(G, mem, REC, TARGET, SCORE, a.readset_size)
            bid = f"B{i:02d}"
            prose_path = str((prose_dir / f"{bid}.md").resolve())
            batches.append({"batch_id": bid, "n": u["n"], "archetype_hint": u["archetype_hint"],
                            "theme_targets": u["targets"], "shared_core": u["shared_core"],
                            "top_comparators": u["top_comparators"],
                            "routing_relations": u["routing_relations"],
                            "read_set": u["read_set"], "prose_index": prose_path,
                            "unit_ids": [m["doc_id"] for m in u["members"]],
                            "finding_ids": [m["doc_id"] for m in u["members"]],
                            "members": u["members"]})
            lines.append(f"## {bid}  [{u['archetype_hint']}]  n={u['n']}  prose={prose_path}")
            if u["shared_core"]:
                lines.append(f"   shared-core: {', '.join(u['shared_core'][:12])}")
            if u["top_comparators"]:
                lines.append(f"   comparators: {', '.join(u['top_comparators'])}")
            lines.append(f"   targets ({len(u['targets'])}): {'|'.join(u['targets'][:40])}"
                         + (" ..." if len(u["targets"]) > 40 else ""))
            lines.append("")
            # Per-slice prose index is the consolidator worker's compact reading substrate.
            write_prose_index(
                prose_dir / f"{bid}.md", bid, u, REC, target_label="theme targets"
            )
        (out / "batches.json").write_text(json.dumps(batches, indent=1))
        (out / "batches.md").write_text("\n".join(lines))
        sizes = sorted((b["n"] for b in batches), reverse=True)
        print(f"emit: {len(batches)} batches, sizes={sizes} (sum={sum(sizes)}) -> "
              f"{out}/batches.json + batches.md")
        return

    comm = split_big(G, louvain(G, a.resolution), a.maxsize, a.resolution)
    comm = sorted(
        comm,
        key=lambda c: (-max(SCORE[d] for d in c), min(d.casefold() for d in c)),
    )

    clusters, lines = [], [f"# Relational clusters (two-archetype graph grouping, res={a.resolution}, "
                           f"maxsize={a.maxsize}) — {len(comm)} clusters from {len(DOCS)} "
                           f"{unit_label}\n"]
    prose_dir = out / "cluster_prose"
    prose_dir.mkdir(exist_ok=True)
    for i, c in enumerate(comm, 1):
        mem = sorted(c, key=lambda d: (-SCORE[d], d.casefold()))
        u = describe_unit(G, mem, REC, TARGET, SCORE, a.readset_size)
        cid = f"C{i:03d}"
        prose_path = str((prose_dir / f"{cid}.md").resolve())
        clusters.append({"cluster_id": cid, "prose_index": prose_path, **u})
        lines.append(f"## {cid}  [{u['archetype_hint']}]  n={len(mem)}  prose={prose_path}  "
                     f"targets={'|'.join(u['targets'][:12])}")
        if u["shared_core"]:
            lines.append(f"   shared-core: {', '.join(u['shared_core'][:12])}")
        if u["top_comparators"]:
            lines.append(f"   comparators: {', '.join(u['top_comparators'])}")
        lines.append(f"   read_set: {'|'.join(u['read_set'])}")
        for m in u["members"][:14]:
            lines.append(f"   - {m['gene_target']}:{m['finding_id']} [{m['finding_type']}] dir={m['direction']}")
        if len(mem) > 14:
            lines.append(f"   ... (+{len(mem) - 14} more)")
        lines.append("")
        write_prose_index(
            prose_dir / f"{cid}.md", cid, u, REC, target_label="targets"
        )

    (out / "clusters.json").write_text(json.dumps(clusters, indent=1))
    (out / "clusters.md").write_text("\n".join(lines))
    multi = sum(1 for c in clusters if c["n"] >= 2)
    print(f"emit: {len(clusters)} clusters ({multi} multi, {len(clusters) - multi} singleton); "
          f"biggest={max((c['n'] for c in clusters), default=0)} -> "
          f"{out}/clusters.json + clusters.md + cluster_prose/")


if __name__ == "__main__":
    main()
