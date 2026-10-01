#!/usr/bin/env python3
"""Query the BioKG v2 graph with a configurable effect_status filter.

The dataset encodes negative/null findings by design (~50% of entity edges are
`absent_or_not_detected` or `uncertain`). How you count those edges as "support"
is a precision/recall knob, so it is exposed as --status-mode:

  all           every edge counts. Highest recall, lowest precision. A pathway
                that was *tested and did NOT respond* inflates its rank (this is
                why 'Hedgehog' ranked #1 — see DEDUP_NOTES.md).
  positive      measured effects. Genes (MEASURED_GENE): {affected, nominal}.
                Concepts (IMPLICATES): {affected, implicated, buffered}. Highest
                precision; best for "what biology dominates the screen?" ranking.
  non-negative  everything except the explicit negatives
                {absent_or_not_detected, fdr_insignificant}. Keeps gene 'measured'
                (neutral) + uncertain/nominal/mixed/compared -> surfaces weak and
                *inferred/hypothesized* shared mechanisms for the scientist to
                vet. Use for discovery, not for claims. (default)

Lanes (after dropping the LLM gene lane, 2026-06-27): genes come from
MEASURED_GENE (Evidence->Gene, carries effect_status+direction) bridged to a
finding via SUPPORTED_BY; concepts from IMPLICATES (Finding->concept). REPORTS_GENE
(finding-claimed genes/comparators) carries no status and is not counted here.

Per-query recommended modes (applied unless --status-mode is given):
  dominant     -> positive      (ranking; precision matters)
  convergence  -> non-negative  (discovery; preserve hedged hits)
  support      -> all           (show the full status breakdown)
  celltypes    -> n/a           (status filter does not apply to OBSERVED_IN)
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path

from ..paths import BASE_DATA_DIR

csv.field_size_limit(10 ** 7)

# Gene (MEASURED_GENE) and concept (IMPLICATES) lanes have DIFFERENT status
# vocabularies, so "positive" is lane-specific (matches biokg-recall-skill/SKILL.md).
GENE_POSITIVE = {"affected", "nominal"}
CONCEPT_POSITIVE = {"affected", "implicated", "buffered"}
NEGATIVE = {"absent_or_not_detected", "fdr_insignificant"}
CONCEPT_RELS = ("IMPLICATES",)              # Finding -> concept, carries effect_status
GENE_RELS = ("MEASURED_GENE",)              # Evidence -> Gene, carries effect_status (bridge via SUPPORTED_BY)
CONCEPT_LABELS = {"Pathway", "Complex", "Module"}
RECOMMENDED = {"dominant": "positive", "convergence": "non-negative", "support": "all", "celltypes": "all"}


def status_ok(status: str, mode: str, lane: str) -> bool:
    if mode == "all":
        return True
    if mode == "positive":
        return status in (GENE_POSITIVE if lane == "gene" else CONCEPT_POSITIVE)
    if mode == "non-negative":
        return status not in NEGATIVE
    raise ValueError(mode)


class Graph:
    def __init__(self, csv_dir: Path):
        nodes_csv = csv_dir / "nodes.merged.csv"
        rels_csv = csv_dir / "relationships.merged.csv"
        if not nodes_csv.exists():  # fall back to the pre-merge build
            nodes_csv, rels_csv = csv_dir / "nodes.csv", csv_dir / "relationships.csv"
        self.source = nodes_csv.name
        self.N = {r["id"]: r for r in csv.DictReader(nodes_csv.open())}
        self.R = list(csv.DictReader(rels_csv.open()))
        self.hf: dict[str, list[str]] = defaultdict(list)        # target id -> finding ids
        self.fin_tgt: dict[str, str] = {}                        # finding id -> target symbol
        self.fin_ent: dict[str, list[tuple[str, str, str]]] = defaultdict(list)  # finding -> [(entity_id, status, lane)]
        self.ent_sup: dict[str, list[tuple[str, str, str]]] = defaultdict(list)  # entity_id -> [(target_symbol, status, lane)]
        self.sym2tid = {r["symbol"]: i for i, r in self.N.items() if "TargetGene" in self.labs(i)}
        for r in self.R:
            if r["type"] == "HAS_FINDING":
                self.hf[r["start_id"]].append(r["end_id"])
                self.fin_tgt[r["end_id"]] = self.N[r["start_id"]]["symbol"]
        # Evidence -> findings that cite it (SUPPORTED_BY is Finding -> Evidence).
        ev2fins: dict[str, list[str]] = defaultdict(list)
        for r in self.R:
            if r["type"] == "SUPPORTED_BY":
                ev2fins[r["end_id"]].append(r["start_id"])
        for r in self.R:
            if r["type"] in CONCEPT_RELS:                        # Finding -> concept (direct)
                self._link(r["start_id"], r["end_id"], r["effect_status"], "concept")
            elif r["type"] in GENE_RELS:                         # Evidence -> Gene (bridge to findings)
                for fid in ev2fins.get(r["start_id"], ()):
                    self._link(fid, r["end_id"], r["effect_status"], "gene")

    def _link(self, fid: str, eid: str, status: str, lane: str) -> None:
        self.fin_ent[fid].append((eid, status, lane))
        tgt = self.fin_tgt.get(fid)
        if tgt is not None:
            self.ent_sup[eid].append((tgt, status, lane))

    def labs(self, i: str) -> set[str]:
        return set(self.N[i]["labels"].split(";")) if i in self.N else set()

    def entity_support(self, mode: str) -> dict[str, set[str]]:
        """entity id -> set of distinct target symbols (edges passing the status filter)."""
        sup: dict[str, set[str]] = defaultdict(set)
        for eid, pairs in self.ent_sup.items():
            for tgt, st, lane in pairs:
                if status_ok(st, mode, lane):
                    sup[eid].add(tgt)
        return sup


def q_dominant(g: Graph, mode: str, top: int) -> None:
    sup = g.entity_support(mode)
    rows = [(len(sup[i]), (g.labs(i) & CONCEPT_LABELS).pop(), g.N[i]["name"])
            for i in g.N if (g.labs(i) & CONCEPT_LABELS)]
    print(f"Dominant pathways/complexes/modules by target support [status-mode={mode}]:")
    for c, lab, nm in sorted(rows, reverse=True)[:top]:
        print(f"  {c:>4}  [{lab}] {nm!r}")


def q_convergence(g: Graph, mode: str, targets: list[str], min_share: int, top: int) -> None:
    cnt: Counter = Counter()
    present = [t for t in targets if t in g.sym2tid]
    missing = [t for t in targets if t not in g.sym2tid]
    for s in present:
        seen = set()
        for fid in g.hf[g.sym2tid[s]]:
            for eid, st, lane in g.fin_ent.get(fid, []):
                if status_ok(st, mode, lane):
                    seen.add(g.N[eid]["name"])
        for nm in seen:
            cnt[nm] += 1
    print(f"Entities shared by >={min_share} of {len(present)} targets {present} "
          f"[status-mode={mode}]" + (f"  (missing: {missing})" if missing else ""))
    for nm, c in sorted(((nm, c) for nm, c in cnt.items() if c >= min_share), key=lambda x: -x[1])[:top]:
        print(f"  [{c}/{len(present)}]  {nm!r}")


def q_support(g: Graph, name: str) -> None:
    ids = [i for i in g.N if g.N[i]["name"].lower() == name.lower()]
    if not ids:
        print(f"No node named {name!r}")
        return
    for i in ids:
        lab = ";".join(sorted(g.labs(i) - {"BioKGNode"}))
        by_status: dict[str, set[str]] = defaultdict(set)
        pos_tgts: set[str] = set()
        for tgt, st, lane in g.ent_sup.get(i, ()):
            by_status[st].add(tgt)
            if status_ok(st, "positive", lane):
                pos_tgts.add(tgt)
        tot = len(set().union(*by_status.values())) if by_status else 0
        pos = len(pos_tgts)
        print(f"{name!r} [{lab}]  total={tot}  positive={pos}")
        for st, ts in sorted(by_status.items(), key=lambda x: -len(x[1])):
            print(f"    {len(ts):>4}  {st}")


def q_celltypes(g: Graph, top: int, depletion: bool) -> None:
    fin_dir = {i: g.N[i].get("direction", "") for i in g.N if "Finding" in g.labs(i)}
    fin_ft = {i: g.N[i].get("finding_type", "") for i in g.N if "Finding" in g.labs(i)}
    ct: dict[str, set[str]] = defaultdict(set)
    for r in g.R:
        if r["type"] == "OBSERVED_IN":
            fid = r["start_id"]
            if depletion and not ("deplet" in (fin_dir.get(fid, "") + fin_ft.get(fid, "")).lower()
                                  or fin_dir.get(fid, "") == "down"):
                continue
            ct[g.N[r["end_id"]]["name"]].add(g.fin_tgt.get(fid))
    title = "depletion-direction" if depletion else "all"
    print(f"Cell types by # distinct targets ({title} findings) [status filter N/A]:")
    for name, ts in sorted(ct.items(), key=lambda x: -len(x[1]))[:top]:
        print(f"  {len(ts):>4}  {name!r}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query", choices=["dominant", "convergence", "support", "celltypes"])
    ap.add_argument(
        "--csv-dir",
        type=Path,
        default=BASE_DATA_DIR,
        help="Dir with nodes.merged.csv/relationships.merged.csv (default: release data/base).",
    )
    ap.add_argument("--status-mode", choices=["all", "positive", "non-negative"], default=None,
                    help="Default is the per-query recommendation (see module docstring).")
    ap.add_argument("--targets", nargs="+", default=[], help="convergence: target gene symbols")
    ap.add_argument("--min-share", type=int, default=2, help="convergence: min #targets sharing an entity")
    ap.add_argument("--name", help="support: node name to break down by effect_status")
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--depletion", action="store_true", help="celltypes: restrict to depletion-direction findings")
    args = ap.parse_args()

    mode = args.status_mode or RECOMMENDED[args.query]
    g = Graph(args.csv_dir)
    print(f"# graph: {args.csv_dir}/{g.source}  nodes={len(g.N)} rels={len(g.R)}\n")
    if args.query == "dominant":
        q_dominant(g, mode, args.top)
    elif args.query == "convergence":
        if not args.targets:
            ap.error("convergence requires --targets")
        q_convergence(g, mode, args.targets, args.min_share, args.top)
    elif args.query == "support":
        if not args.name:
            ap.error("support requires --name")
        q_support(g, args.name)
    elif args.query == "celltypes":
        q_celltypes(g, args.top, args.depletion)


if __name__ == "__main__":
    main()
