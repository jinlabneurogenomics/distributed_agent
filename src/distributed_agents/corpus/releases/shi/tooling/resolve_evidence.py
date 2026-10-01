#!/usr/bin/env python3
"""Resolve the Evidence and Reference ledgers behind PerturbAI findings.

Findings (see `query_findings.py`) carry gene-scoped `evidence_ids` (E0xx) and
`ref_ids` (R0xx). This script resolves those IDs to the structured rows the
original per-perturbation analysis recorded in each report's Structured Appendix:

  - EVIDENCE   -> the actual DE support (cell type, genes, statistics, description)
  - REFERENCES -> the citations behind a claim (source, source_type, citation, URL)

Use it so citations and supporting data are pulled FROM THE CORPUS (verifiable,
with a URL) rather than recalled from model memory. If you need a reference the
corpus does not carry, verify it via `research-router-skill` before asserting an
identifier — never emit a confabulated PMID/DOI.

Artifacts packaged with this release (artifacts/ledgers/, copied from the report appendix,
same finding/evidence/ref ID space as the narrative-findings ledger):
  evidence.csv           (target_gene, evidence_id, evidence_slug, cell_type,
                          genes, n_genes, statistics, description, ...)
  references.csv         (target_gene, ref_id, ref_slug, source, source_type,
                          citation, url, description)
  findings.csv           flat CSV mirror of the findings; carries pipe-delimited
                          evidence_ids / ref_ids per finding_id (for --finding)

IDs are GENE-SCOPED (E001 for one gene != E001 for another), so `--gene` is required.
Stdlib-only; no pixi env needed.

Examples
--------
  # everything behind a gene
  python resolve_evidence.py --gene Arx
  # just the verifiable references (citation + source_type + URL)
  python resolve_evidence.py --gene Arx --refs-only
  # resolve exactly what a finding cites (reads findings_ledger.csv)
  python resolve_evidence.py --gene Arx --finding F002
  # specific IDs
  python resolve_evidence.py --gene Arx --ref-id R004 --evidence-id E002
  # machine-readable
  python resolve_evidence.py --gene Arx --finding F002 --json
"""
import argparse
import csv
import json
import sys
from pathlib import Path

_OUT = Path(__file__).resolve().parents[1] / "artifacts" / "ledgers"


def _load(name: str) -> list[dict]:
    path = _OUT / name
    if not path.exists():
        sys.exit(f"missing release artifact: {path}")
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gene", action="append", required=True,
                    help="target gene (repeatable). Evidence/ref IDs are gene-scoped.")
    ap.add_argument("--finding", help="finding_id (e.g. F002): resolve exactly the evidence/refs it cites.")
    ap.add_argument("--evidence-id", action="append", default=[], help="filter to specific evidence id(s).")
    ap.add_argument("--ref-id", action="append", default=[], help="filter to specific reference id(s).")
    ap.add_argument("--evidence-only", action="store_true")
    ap.add_argument("--refs-only", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    genes = set(args.gene)
    ev = [r for r in _load("evidence.csv") if r["target_gene"] in genes]
    rf = [r for r in _load("references.csv") if r["target_gene"] in genes]

    ev_ids = set(args.evidence_id)
    rf_ids = set(args.ref_id)
    if args.finding:
        found = False
        for r in _load("findings.csv"):
            if r["target_gene"] in genes and r["finding_id"] == args.finding:
                found = True
                ev_ids |= set(filter(None, (r.get("evidence_ids") or "").split("|")))
                rf_ids |= set(filter(None, (r.get("ref_ids") or "").split("|")))
        if not found:
            sys.exit(f"finding {args.finding} not found for gene(s) {sorted(genes)}")
    if ev_ids:
        ev = [r for r in ev if r["evidence_id"] in ev_ids]
    if rf_ids:
        rf = [r for r in rf if r["ref_id"] in rf_ids]

    if args.refs_only:
        ev = []
    if args.evidence_only:
        rf = []

    if args.json:
        print(json.dumps({"evidence": ev, "references": rf}, indent=2))
        return 0

    if ev:
        print(f"# EVIDENCE ({len(ev)})")
        for r in ev:
            print(f"[{r['target_gene']}:{r['evidence_id']}] {r['evidence_slug']}  "
                  f"cell_type={r['cell_type'] or '-'}  genes={r['genes']}")
            if r.get("statistics"):
                print(f"    stats: {r['statistics']}")
            if r.get("description"):
                print(f"    {r['description']}")
    if rf:
        print(f"\n# REFERENCES ({len(rf)})")
        for r in rf:
            print(f"[{r['target_gene']}:{r['ref_id']}] ({r['source_type']}) {r['source']}")
            if r.get("citation"):
                print(f"    {r['citation']}")
            if r.get("url"):
                print(f"    url: {r['url']}")
            if r.get("description"):
                print(f"    {r['description']}")
    if not ev and not rf:
        print("(no evidence/reference rows matched)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
