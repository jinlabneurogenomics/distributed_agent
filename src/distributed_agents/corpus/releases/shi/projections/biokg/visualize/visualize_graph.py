#!/usr/bin/env python3
"""Render the BioKG graph as graphify's interactive vis.js ``graph.html``.

Two steps, because they need different pixi environments:

1. ``export`` — stdlib-only (urllib + base64), same access pattern as
   ``biokg_cypher.py``. Pulls an edge list out of the live Neo4j over HTTP and
   writes a small node-link JSON. Runs anywhere.
2. ``render`` — needs ``networkx`` and ``graphify``, so run it under
   ``pixi run -e graphify``. Detects communities and hands the graph to
   ``graphify.export.to_html``, the same function that produced the graphify
   ``graph.html`` for the findings corpus.

Examples
--------
    # whole-graph meta view (label x rel-type), always tiny
    python -m distributed_agents.corpus.launch biokg.visualize.visualize_graph export \
      --scope schema --out /tmp/biokg-schema.json
    pixi run -e graphify python -m distributed_agents.corpus.launch biokg.visualize.visualize_graph render \
        --graph /tmp/biokg-schema.json --out /tmp/biokg-schema.html

    # the Claim backbone (3.4k nodes / 4.3k edges, fits the 5k viz cap)
    python -m distributed_agents.corpus.launch biokg.visualize.visualize_graph export \
      --scope claims --out /tmp/biokg-claims.json

    # anything else: write your own Cypher returning the standard columns
    python -m distributed_agents.corpus.launch biokg.visualize.visualize_graph export \
      --out /tmp/x.json --cypher "
        MATCH (a:TargetGene)-[:HAS_FINDING]->(:Finding)-[r:IMPLICATES]->(b:Complex)
        RETURN a.id AS src, a.symbol AS src_label, 'TargetGene' AS src_kind,
               b.id AS tgt, b.name AS tgt_label, b.kind AS tgt_kind,
               type(r) AS rel, count(*) AS weight"

A custom ``--cypher`` must return: ``src, src_label, src_kind, tgt, tgt_label,
tgt_kind, rel`` (``weight`` optional).
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.request
from pathlib import Path

DEFAULT_HTTP_URL = os.environ.get("BIOKG_NEO4J_HTTP_URL", "http://127.0.0.1:7474")
DEFAULT_DATABASE = os.environ.get("BIOKG_NEO4J_DATABASE", "neo4j")
DEFAULT_USER = os.environ.get("BIOKG_NEO4J_USER", "neo4j")
DEFAULT_PASSWORD = os.environ.get("BIOKG_NEO4J_PASSWORD", "biokgpassword")

COLUMNS = ("src", "src_label", "src_kind", "tgt", "tgt_label", "tgt_kind", "rel")

STYLE = Path(__file__).with_name("style.mplstyle")

# Recolour = rerun (.agent/CONVENTIONS.md). Everything visual is set here.
PALETTE = [
    "#4E79A7", "#F28E2B", "#59A14F", "#E15759", "#B07AA1", "#76B7B2",
    "#EDC948", "#FF9DA7", "#9C755F", "#8CD17D", "#86BCB6", "#D4A6C8",
]
COL = {
    "edge": "#9aa5b1",
    "other": "#d0d5da",      # groups past the legend cut, and "unassigned"
    "node_edge": "#ffffff",
    "label": "#1a1a1a",
}

SCOPES = {
    # Whole graph, aggregated to the label x rel-type meta-graph. This is the
    # only view that is honestly "everything": 92k nodes cannot be laid out.
    "schema": """
        MATCH (a)-[r]->(b)
        WITH [l IN labels(a) WHERE l <> 'BioKGNode'][0] AS src_kind,
             [l IN labels(b) WHERE l <> 'BioKGNode'][0] AS tgt_kind,
             type(r) AS rel, count(*) AS weight
        RETURN src_kind AS src, src_kind AS src_label, src_kind,
               tgt_kind AS tgt, tgt_kind AS tgt_label, tgt_kind,
               rel, weight
    """,
    # Claim-to-Claim adjudicated relations: the semantic backbone.
    "claims": """
        MATCH (a:Claim)-[r]->(b:Claim)
        RETURN a.id AS src,
               coalesce(a.summary, a.name, a.claim_id) AS src_label,
               coalesce(a.relation_family, 'claim') AS src_kind,
               b.id AS tgt,
               coalesce(b.summary, b.name, b.claim_id) AS tgt_label,
               coalesce(b.relation_family, 'claim') AS tgt_kind,
               type(r) AS rel, 1 AS weight
    """,
    # Target -> implicated concept convergence, positive-effect edges only.
    "concepts": """
        MATCH (t:TargetGene)-[:HAS_FINDING]->(:Finding)-[r:IMPLICATES]->(e)
        WHERE any(l IN labels(e) WHERE l IN ['Pathway','Complex','Module','Phenotype'])
          AND r.effect_status IN ['affected','implicated','buffered']
        RETURN t.id AS src, t.symbol AS src_label, 'TargetGene' AS src_kind,
               e.id AS tgt, e.name AS tgt_label,
               coalesce(e.kind, labels(e)[0]) AS tgt_kind,
               'IMPLICATES' AS rel, count(*) AS weight
    """,
    # TargetGene--TargetGene one-mode projection through shared concepts.
    # The support bounds are the analysis, not a cosmetic filter: without an
    # upper bound two hub concepts ("buffered transcriptional response",
    # "mouse brain") generate 99% of the edges and the layout is a hairball.
    "projection": """
        MATCH (c)<-[:IMPLICATES]-(:Finding)<-[:HAS_FINDING]-(t:TargetGene)
        WHERE any(l IN labels(c) WHERE l IN ['Pathway','Complex','Module','Phenotype','Other'])
        WITH c, collect(DISTINCT t) AS ts
        WHERE size(ts) >= {min_support} AND size(ts) <= {max_support}
        UNWIND ts AS t1
        UNWIND ts AS t2
        WITH t1, t2 WHERE id(t1) < id(t2)
        RETURN t1.id AS src, t1.symbol AS src_label, 'TargetGene' AS src_kind,
               t2.id AS tgt, t2.symbol AS tgt_label, 'TargetGene' AS tgt_kind,
               'SHARES_CONCEPT' AS rel, count(*) AS weight
    """,
    # The program layer: genes and findings routed onto the 15 programs.
    "programs": """
        MATCH (a)-[r:MEMBER_OF|CANONICAL_PROGRAM|IMPLICATES_PROGRAM]->(p:Program)
        RETURN coalesce(a.id, a.name) AS src, coalesce(a.symbol, a.name, a.id) AS src_label,
               [l IN labels(a) WHERE l <> 'BioKGNode'][0] AS src_kind,
               coalesce(p.id, p.program_id, p.name) AS tgt,
               p.name AS tgt_label, 'Program' AS tgt_kind,
               type(r) AS rel, 1 AS weight
    """,
}


# For scopes whose nodes are all one label, colour needs an external attribute.
ANNOTATE = {
    "projection": """
        MATCH (t:TargetGene)-[:HAS_FINDING]->(:Finding)-[:IMPLICATES_PROGRAM]->(p:Program)
        RETURN t.id AS id, p.name AS kind, count(*) AS n
    """,
}


def run_cypher(statement: str, args: argparse.Namespace) -> list[dict]:
    payload = json.dumps({"statements": [{"statement": statement}]}).encode()
    token = base64.b64encode(f"{args.user}:{args.password}".encode()).decode()
    req = urllib.request.Request(
        f"{args.http_url.rstrip('/')}/db/{args.database}/tx/commit",
        data=payload,
        headers={"Content-Type": "application/json", "Authorization": f"Basic {token}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=args.timeout) as resp:
            body = json.load(resp)
    except OSError as exc:
        sys.exit(
            f"Cannot reach Neo4j at {args.http_url}: {exc}\n"
            "Is BioKG up? `pixi run biokg-neo4j-apptainer-up`"
        )
    if body.get("errors"):
        sys.exit(f"Cypher error: {json.dumps(body['errors'], indent=2)}")
    result = body["results"][0]
    cols = result["columns"]
    return [dict(zip(cols, row["row"])) for row in result["data"]]


def cmd_export(args: argparse.Namespace) -> None:
    statement = args.cypher or (
        SCOPES[args.scope]
        .replace("{min_support}", str(args.min_support))
        .replace("{max_support}", str(args.max_support))
    )
    rows = run_cypher(statement, args)
    missing = [c for c in COLUMNS if rows and c not in rows[0]]
    if missing:
        sys.exit(f"query must return columns {COLUMNS}; missing {missing}")

    nodes: dict[str, dict] = {}
    edges = []
    for row in rows:
        for side in ("src", "tgt"):
            nid = row[side]
            if nid is None:
                continue
            nodes.setdefault(
                nid,
                {
                    "id": nid,
                    "label": str(row[f"{side}_label"] or nid),
                    "kind": str(row[f"{side}_kind"] or "Other"),
                },
            )
        if row["src"] is None or row["tgt"] is None:
            continue
        edges.append(
            {
                "source": row["src"],
                "target": row["tgt"],
                "relation": row["rel"],
                "weight": int(row.get("weight") or 1),
            }
        )

    if not args.cypher and args.scope in ANNOTATE:
        best: dict[str, tuple[int, str]] = {}
        for row in run_cypher(ANNOTATE[args.scope], args):
            cur = best.get(row["id"])
            if cur is None or row["n"] > cur[0]:
                best[row["id"]] = (row["n"], row["kind"])
        for nid, node in nodes.items():
            node["kind"] = best[nid][1] if nid in best else "unassigned"

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(
            {"scope": args.scope if not args.cypher else "custom",
             "nodes": list(nodes.values()), "edges": edges},
            indent=1,
        ),
        encoding="utf-8",
    )
    print(f"{out}: {len(nodes)} nodes / {len(edges)} edges")


def cmd_render(args: argparse.Namespace) -> None:
    try:
        import networkx as nx
        from graphify.export import to_html
    except ImportError as exc:
        sys.exit(f"{exc}\nRun this step under `pixi run -e graphify`.")

    data = json.loads(Path(args.graph).read_text(encoding="utf-8"))
    G = nx.Graph()
    for n in data["nodes"]:
        G.add_node(n["id"], label=n["label"][:120], file_type=n["kind"])
    for e in data["edges"]:
        G.add_edge(
            e["source"], e["target"],
            relation=e["relation"], confidence="EXTRACTED",
            _src=e["source"], _tgt=e["target"], weight=e.get("weight", 1),
        )
    if G.number_of_nodes() == 0:
        sys.exit("graph is empty")

    from collections import Counter, defaultdict

    if args.color_by == "kind":
        buckets = defaultdict(list)
        for n in G:
            buckets[G.nodes[n].get("file_type") or "?"].append(n)
        ordered = sorted(buckets.items(), key=lambda kv: -len(kv[1]))
        communities = {i: sorted(v) for i, (_, v) in enumerate(ordered)}
        labels = {i: f"{k} ({len(v)})" for i, (k, v) in enumerate(ordered)}
    else:
        parts = nx.community.louvain_communities(G, seed=0, weight="weight")
        communities = {i: sorted(members) for i, members in enumerate(parts)}
        labels = {}
        for cid, members in communities.items():
            kinds = Counter(G.nodes[m].get("file_type", "?") for m in members)
            hub = max(members, key=lambda m: G.degree(m))
            labels[cid] = f"{kinds.most_common(1)[0][0]}: {G.nodes[hub]['label'][:40]}"

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    to_html(G, communities, str(out), community_labels=labels, node_limit=args.node_limit)
    if out.exists():
        print(f"{out}: {G.number_of_nodes()} nodes / {G.number_of_edges()} edges / "
              f"{len(communities)} communities")


def _groups(G, mode: str, seed: int):
    """(node -> group name) plus an ordered group list, largest first."""
    import networkx as nx
    from collections import Counter

    if mode == "community":
        parts = nx.community.louvain_communities(G, seed=seed, weight="weight")
        member = {n: f"C{i}" for i, part in enumerate(parts) for n in part}
    else:
        member = {n: G.nodes[n].get("file_type") or "?" for n in G}
    order = [g for g, _ in Counter(member.values()).most_common()]
    return member, order


def _community_layout(G, member, seed: int, iterations: int, boost: float):
    """Force layout that actually separates groups.

    Plain spring_layout interleaves communities spatially, which is what makes a
    projection read as a hairball. Two cheap fixes, both standard: seed each node
    at its community's position in a layout of the community meta-graph, and
    up-weight intra-community edges so the refinement pass keeps them together.
    """
    import networkx as nx
    from collections import Counter

    meta = nx.Graph()
    meta.add_nodes_from(set(member.values()))
    inter = Counter()
    for u, v, d in G.edges(data=True):
        a, b = member[u], member[v]
        if a != b:
            inter[(min(a, b), max(a, b))] += d.get("weight", 1)
    for (a, b), w in inter.items():
        meta.add_edge(a, b, weight=w)
    centers = nx.spring_layout(meta, seed=seed, weight="weight", iterations=200)

    rng = __import__("random").Random(seed)
    init = {
        n: (centers[member[n]][0] + rng.gauss(0, 0.02),
            centers[member[n]][1] + rng.gauss(0, 0.02))
        for n in G
    }
    H = G.copy()
    for u, v, d in H.edges(data=True):
        d["_w"] = d.get("weight", 1) * (boost if member[u] == member[v] else 1.0)
    return nx.spring_layout(H, pos=init, seed=seed, weight="_w", iterations=iterations)


def cmd_figure(args: argparse.Namespace) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import networkx as nx
    from matplotlib.collections import LineCollection
    from matplotlib.lines import Line2D

    from .svg_circles import circleify

    plt.style.use(str(STYLE))

    data = json.loads(Path(args.graph).read_text(encoding="utf-8"))
    G = nx.Graph()
    for n in data["nodes"]:
        G.add_node(n["id"], label=n["label"], file_type=n["kind"])
    for e in data["edges"]:
        G.add_edge(e["source"], e["target"], weight=e.get("weight", 1))

    if args.k_core:
        G = nx.k_core(G, k=args.k_core)
    if args.giant and G.number_of_nodes():
        G = G.subgraph(max(nx.connected_components(G), key=len)).copy()
    if not G.number_of_nodes():
        sys.exit("nothing left to draw after filtering")

    member, order = _groups(G, args.color_by, args.seed)
    shown = [g for g in order if g != "unassigned"][: args.max_legend]
    color = {g: PALETTE[i % len(PALETTE)] for i, g in enumerate(shown)}

    if args.layout == "community":
        pos = _community_layout(G, member, args.seed, args.iterations, args.group_boost)
    else:
        pos = nx.spring_layout(G, seed=args.seed, weight="weight", iterations=args.iterations)
    deg = dict(G.degree())
    max_deg = max(deg.values()) or 1

    fig, ax = plt.subplots(figsize=(args.width, args.width))

    # Edges are the dense layer -> rasterize (CONVENTIONS: dense clouds).
    weights = [G.edges[e].get("weight", 1) for e in G.edges]
    max_w = max(weights, default=1)
    ax.add_collection(LineCollection(
        [(pos[u], pos[v]) for u, v in G.edges],
        colors=COL["edge"],
        linewidths=[0.25 + 1.0 * (w / max_w) for w in weights],
        alpha=args.edge_alpha, zorder=1, rasterized=True,
    ))

    # Nodes stay vector. Size is BINNED, not continuous: matplotlib only shares
    # one <defs> circle per scatter call when every marker in it is the same
    # size, and only then does circleify() get <use> elements to rewrite. A
    # continuous s=[...] emits one 4-anchor <path> per node instead (1214 paths
    # in Illustrator). Binning also gives the reader a legible size legend.
    bins = args.size_bins
    edges_q = [max_deg * (i + 1) / bins for i in range(bins)]
    def size_bin(n):
        for i, hi in enumerate(edges_q):
            if deg[n] <= hi:
                return i
        return bins - 1
    sizes = [args.node_size * (0.4 + 1.6 * i / max(bins - 1, 1)) for i in range(bins)]

    for g in shown + [None]:
        members = [n for n in G if (member[n] == g if g else member[n] not in shown)]
        for b in range(bins):
            nodes = [n for n in members if size_bin(n) == b]
            if not nodes:
                continue
            ax.scatter(
                [pos[n][0] for n in nodes], [pos[n][1] for n in nodes],
                s=sizes[b], c=color.get(g, COL["other"]), linewidths=0.3,
                edgecolors=COL["node_edge"], clip_on=False, zorder=2,
            )

    if args.label == "hubs":
        picks = sorted(G, key=lambda n: -deg[n])[: args.label_top]
    elif args.label == "group-hubs":
        picks = [max((n for n in G if member[n] == g), key=lambda n: deg[n]) for g in shown]
    else:
        picks = []
    for n in picks:
        ax.annotate(
            G.nodes[n]["label"][:28], pos[n],
            xytext=(0, 7), textcoords="offset points",
            fontsize=6, color=COL["label"], ha="center", va="bottom", zorder=4,
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.75),
        )

    if shown:
        ax.legend(
            handles=[Line2D([], [], marker="o", ls="", markersize=4,
                            markerfacecolor=color[g], markeredgecolor="none", label=g)
                     for g in shown],
            loc="upper left", bbox_to_anchor=(1.01, 1.0), frameon=False,
            fontsize=6, handletextpad=0.4, labelspacing=0.5,
            title=("community" if args.color_by == "community" else "group"),
            title_fontsize=6.5,
        )
    ax.set_axis_off()
    ax.margins(0.02)
    fig.patch.set_visible(False)
    fig.tight_layout()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out.with_suffix(".png"), dpi=args.dpi, transparent=True, bbox_inches="tight")
    fig.savefig(out.with_suffix(".svg"), dpi=600, transparent=True, bbox_inches="tight")
    plt.close(fig)
    n_circles = circleify(out.with_suffix(".svg"))
    print(f"{out.with_suffix('.png')} + .svg: {G.number_of_nodes()} nodes / "
          f"{G.number_of_edges()} edges / {len(order)} {args.color_by} groups "
          f"({len(shown)} in legend), {n_circles} marks -> <circle>")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    e = sub.add_parser("export", help="dump an edge list from Neo4j (stdlib only)")
    e.add_argument("--scope", choices=sorted(SCOPES), default="schema")
    e.add_argument("--cypher", help="custom query returning the standard columns")
    e.add_argument("--out", required=True)
    e.add_argument("--http-url", default=DEFAULT_HTTP_URL)
    e.add_argument("--database", default=DEFAULT_DATABASE)
    e.add_argument("--user", default=DEFAULT_USER)
    e.add_argument("--password", default=DEFAULT_PASSWORD)
    e.add_argument("--min-support", type=int, default=2,
                   help="projection scope: drop concepts touching fewer targets")
    e.add_argument("--max-support", type=int, default=20,
                   help="projection scope: drop hub concepts (2 of them make 99%% of edges)")
    e.add_argument("--timeout", type=float, default=300.0)
    e.set_defaults(func=cmd_export)

    r = sub.add_parser("render", help="write graphify's vis.js graph.html (needs -e graphify)")
    r.add_argument("--graph", required=True, help="JSON written by `export`")
    r.add_argument("--out", required=True)
    r.add_argument("--color-by", choices=("community", "kind"), default="community",
                   help="community = louvain; kind = the node's label/program")
    r.add_argument("--node-limit", type=int, default=5000,
                   help="above this, graphify aggregates to a community meta-graph")
    r.set_defaults(func=cmd_render)

    f = sub.add_parser("figure", help="static PNG+SVG for figures (default pixi env)")
    f.add_argument("--graph", required=True, help="JSON written by `export`")
    f.add_argument("--out", required=True, help="path stem; .png and .svg are written")
    f.add_argument("--color-by", choices=("community", "kind"), default="community")
    f.add_argument("--k-core", type=int, default=0, help="strip nodes below this degree, iteratively")
    f.add_argument("--giant", action="store_true", help="keep only the largest component")
    f.add_argument("--max-legend", type=int, default=12, help="groups to colour; the rest go grey")
    f.add_argument("--layout", choices=("community", "spring"), default="community",
                   help="community = group-seeded force layout (readable); spring = plain")
    f.add_argument("--group-boost", type=float, default=6.0,
                   help="how hard intra-group edges pull, in the community layout")
    f.add_argument("--label", choices=("group-hubs", "hubs", "none"), default="group-hubs")
    f.add_argument("--label-top", type=int, default=25, help="--label hubs: how many")
    f.add_argument("--node-size", type=float, default=26.0)
    f.add_argument("--size-bins", type=int, default=4,
                   help="degree -> marker-size bins; keeps SVG marks as shared <circle> defs")
    f.add_argument("--edge-alpha", type=float, default=0.35)
    f.add_argument("--iterations", type=int, default=100)
    f.add_argument("--width", type=float, default=6.5)
    f.add_argument("--dpi", type=int, default=150)
    f.add_argument("--seed", type=int, default=0)
    f.set_defaults(func=cmd_figure)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
