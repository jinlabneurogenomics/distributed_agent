#!/usr/bin/env python3
"""Query the gene-annotation store — the deterministic gene<->set membership backbone.

Filter / parameter-provider primitive over the closed gene universe (18,023 real
genes: perturbation targets + measured readout). Two tables:

  out/genes.parquet            DIMENSION: one row per gene, scalar flags
                               (is_perturbation_target, is_measured, is_control_target,
                               type_of_gene, entrez/ensembl IDs).
  out/gene_membership.parquet  FACT: (gene, resource, set_id, set_name), many-to-many.
                               Resources: GO:BP/CC/MF, reactome, kegg, MSigDB:MH,
                               MSigDB:CP:WIKIPATHWAYS, MSigDB:CP:BIOCARTA, CORUM,
                               functional_class.

Its main job is to hand a *deterministic gene list* to the graph / retrieval lanes
as a **prior group** — e.g. the CORUM proteasome subunits, or the WikiPathways WNT
set — which `biokg_cypher.py` then consumes as `--param family='[...]'`. Divergence,
specificity, and manuscript-synthesis reasoning all need this "expected-similar" set
to compare observed findings against. It also answers attribute-set questions
directly ("list all TF targets" = 398), the deterministic 4th access mode.

Runs in the `annotation` pixi env (needs pandas):

    pixi run -e annotation python debug/260704_annotation/query_gene_annotations.py MODE ...

Modes
-----
  resources                     list resources with #sets and #rows (orientation)
  search   --term WNT           discover matching set names/ids + member counts
  genes-in --set <query>        set -> member genes   (the parameter provider)
  sets-for --gene <symbol>      gene -> its set memberships

Examples
--------
    # all TF perturbation targets (= 398), as a JSON array ready for --param
    ... genes-in --set transcription_factor --targets-only --json

    # find the exact set first (names are messy), then pull its genes
    ... search   --term proteasome --resource CORUM
    ... genes-in --set-id CORUM:181 --targets-only --json

    # WNT pathway genes, union across matching WikiPathways sets
    ... genes-in --set WNT --resource MSigDB:CP:WIKIPATHWAYS --union --json

    # what canonical sets is a gene in?
    ... sets-for --gene Ctnnb1 --resource MSigDB:CP:WIKIPATHWAYS
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import pandas as pd

_HERE = Path(__file__).resolve().parent


def store_dir(override: str | None) -> Path:
    if override:
        return Path(override).expanduser()
    env = os.environ.get("DISTRIBUTED_AGENTS_GENE_STORE")
    return Path(env).expanduser() if env else _HERE / "out"


def load(store: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    dim_p, fact_p = store / "genes.parquet", store / "gene_membership.parquet"
    if not fact_p.is_file():
        raise SystemExit(f"gene-annotation store not found at {store}\n"
                         "Pass --store-dir or set DISTRIBUTED_AGENTS_GENE_STORE.")
    return pd.read_parquet(dim_p), pd.read_parquet(fact_p)


def target_measured(dim: pd.DataFrame) -> tuple[set[str], set[str]]:
    tgt = set(dim.query("is_perturbation_target & ~is_control_target")["gene"])
    measured = set(dim.query("is_measured")["gene"])
    return tgt, measured


def apply_dim_filter(genes: set[str], args, dim: pd.DataFrame) -> set[str]:
    tgt, measured = target_measured(dim)
    if args.targets_only:
        genes &= tgt
    if args.measured_only:
        genes &= measured
    return genes


def emit_genes(genes: list[str], as_json: bool) -> None:
    if as_json:
        print(json.dumps(genes))
    else:
        for g in genes:
            print(g)


# --------------------------------------------------------------------------- #
def cmd_resources(fact: pd.DataFrame, args) -> int:
    g = (fact.groupby("resource")
         .agg(sets=("set_id", "nunique"), rows=("gene", "size"), genes=("gene", "nunique"))
         .sort_values("rows", ascending=False))
    print(g.to_string())
    return 0


def cmd_search(fact: pd.DataFrame, args) -> int:
    df = fact
    if args.resource:
        df = df[df["resource"] == args.resource]
    term = args.term.casefold()
    hit = df[df["set_name"].str.casefold().str.contains(term, na=False)
             | df["set_id"].str.casefold().str.contains(term, na=False)]
    grp = (hit.groupby(["resource", "set_id", "set_name"])
           .agg(genes=("gene", "nunique")).reset_index()
           .sort_values("genes", ascending=False))
    if grp.empty:
        print(f"# no sets match {args.term!r}"
              + (f" in {args.resource}" if args.resource else ""), file=sys.stderr)
        return 1
    for _, r in grp.head(args.limit or len(grp)).iterrows():
        print(f"{r['genes']:>6}  {r['resource']:<22} {r['set_id']:<16} {r['set_name']}")
    print(f"# {len(grp)} matching sets", file=sys.stderr)
    return 0


def cmd_genes_in(dim: pd.DataFrame, fact: pd.DataFrame, args) -> int:
    df = fact
    if args.resource:
        df = df[df["resource"] == args.resource]
    if args.set_id:
        matched = df[df["set_id"] == args.set_id]
        sets = matched[["resource", "set_id", "set_name"]].drop_duplicates()
    else:
        q = args.set.casefold()
        exact = df[(df["set_name"].str.casefold() == q) | (df["set_id"].str.casefold() == q)]
        matched = exact if not exact.empty else df[
            df["set_name"].str.casefold().str.contains(q, na=False)
            | df["set_id"].str.casefold().str.contains(q, na=False)]
        sets = matched[["resource", "set_id", "set_name"]].drop_duplicates()

    if sets.empty:
        print(f"# no set matches {args.set_id or args.set!r}"
              + (f" in {args.resource}" if args.resource else "")
              + " — try `search`.", file=sys.stderr)
        return 1
    if len(sets) > 1 and not args.union:
        print(f"# {len(sets)} sets match — disambiguate with --set-id/--resource, "
              f"or pass --union to merge them:", file=sys.stderr)
        for _, r in sets.iterrows():
            n = matched[matched["set_id"] == r["set_id"]]["gene"].nunique()
            print(f"  [{n}] {r['resource']} {r['set_id']} {r['set_name']}", file=sys.stderr)
        return 2

    genes = apply_dim_filter(set(matched["gene"]), args, dim)
    emit_genes(sorted(genes), args.json)
    label = args.set_id or args.set
    scope = " ".join(x for x in ("targets" if args.targets_only else "",
                                 "measured" if args.measured_only else "") if x) or "all"
    print(f"# {len(genes)} genes ({scope}) in {len(sets)} set(s) matching {label!r}",
          file=sys.stderr)
    return 0


def cmd_sets_for(fact: pd.DataFrame, args) -> int:
    want = {g.casefold() for g in args.genes}
    df = fact[fact["gene"].str.casefold().isin(want)]
    if args.resource:
        df = df[df["resource"] == args.resource]
    if df.empty:
        print(f"# no memberships for {args.genes}"
              + (f" in {args.resource}" if args.resource else ""), file=sys.stderr)
        return 1
    df = df.sort_values(["gene", "resource", "set_id"])
    if args.json:
        for _, r in df.iterrows():
            print(json.dumps({k: r[k] for k in ("gene", "resource", "set_id", "set_name")}))
    else:
        for _, r in df.head(args.limit or len(df)).iterrows():
            print(f"{r['gene']:<12} {r['resource']:<22} {r['set_id']:<16} {r['set_name']}")
    print(f"# {len(df)} memberships across {df['gene'].nunique()} genes", file=sys.stderr)
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("mode", choices=["resources", "search", "genes-in", "sets-for"])
    p.add_argument("--store-dir", default=None, help="Override the store dir (holds *.parquet).")
    p.add_argument("--resource", default=None,
                   help="Restrict to one resource (e.g. CORUM, reactome, GO:BP, "
                        "MSigDB:CP:WIKIPATHWAYS, functional_class).")
    p.add_argument("--term", default=None, help="search: substring over set_name/set_id.")
    p.add_argument("--set", default=None, help="genes-in: set name/id (exact, else substring).")
    p.add_argument("--set-id", default=None, help="genes-in: exact set_id.")
    p.add_argument("--union", action="store_true",
                   help="genes-in: merge genes across all matching sets instead of "
                        "requiring a unique match.")
    p.add_argument("--gene", action="append", dest="genes", default=[],
                   help="sets-for: gene symbol (case-insensitive); repeatable.")
    p.add_argument("--targets-only", action="store_true",
                   help="genes-in: keep only perturbation targets (excl. controls).")
    p.add_argument("--measured-only", action="store_true",
                   help="genes-in: keep only measured-readout genes.")
    p.add_argument("--json", action="store_true", help="Machine-readable output.")
    p.add_argument("--limit", type=int, default=0, help="Cap printed rows (0 = no cap).")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    dim, fact = load(store_dir(args.store_dir))
    if args.mode == "resources":
        return cmd_resources(fact, args)
    if args.mode == "search":
        if not args.term:
            raise SystemExit("search requires --term")
        return cmd_search(fact, args)
    if args.mode == "genes-in":
        if not (args.set or args.set_id):
            raise SystemExit("genes-in requires --set or --set-id")
        return cmd_genes_in(dim, fact, args)
    if args.mode == "sets-for":
        if not args.genes:
            raise SystemExit("sets-for requires --gene")
        return cmd_sets_for(fact, args)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
