#!/usr/bin/env python3
"""Rank findings by the biological "so what" — the SEMANTIC scoring mode.

The sibling `score_findings.py` ranks on structured metadata (finding_type /
literature_status / convergence). That is fast and covers all rows, but for "which findings
are biologically INTERESTING / NOVEL" it is ~random: on a held-out expert rung grading it
scores AP ~0.12, because the discriminator — what the readout genes let the cell DO — is not
in those fields. This script instead applies a general RANKING CRITERION (rung_criterion.md)
to EACH finding with an LLM, grading the finding's readout genes by functional consequence
(capability/identity change, ectopy) over topology/fame. On the same held-out grading it
scores AP ~0.68 vs 0.12. It is the leakage-safe pipeline: the criterion encodes the general
reasoning, NOT a hardcoded list of the answer genes; the model supplies gene-function
knowledge.

Cost: ONE LLM call per finding (all ~11,343 = a real run, minutes + API cost). Filter with
--gene / --finding-type / --grep / --limit while iterating; grade the whole ledger for the
deployed ranking. Needs `openai` + OPENAI_API_KEY (unlike the stdlib score_findings.py); uses
the Responses API (chat.completions 401s on the gpt-rosalind fine-tune).

Usage:
    python grade_findings.py --out-dir ./rung_ranking --top 30
    python grade_findings.py --finding-type convergent_module --out-dir /tmp/r --workers 12
"""
from __future__ import annotations
import argparse, csv, json, os, re, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_DEFAULT_LEDGER = (
    _HERE.parents[2] / "artifacts" / "ledgers" / "findings.csv"
)
_DEFAULT_CRITERION = _HERE / "rung_criterion.md"
MODEL = os.environ.get("RUNG_GRADER_MODEL", os.environ.get("DISTRIBUTED_AGENTS_MODEL", "gpt-rosalind-260428"))


def ledger_path(override):
    if override:
        return Path(override).expanduser()
    env = os.environ.get("DISTRIBUTED_AGENTS_FINDINGS_LEDGER")
    return Path(env).expanduser() if env else _DEFAULT_LEDGER


def iter_findings(path):
    if not path.is_file():
        raise SystemExit(f"findings ledger not found at {path}\nPass --ledger-path or set DISTRIBUTED_AGENTS_FINDINGS_LEDGER.")
    if path.suffix.casefold() == ".csv":
        with path.open(newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                target = str(row.get("target_gene") or "")
                finding = str(row.get("finding_id") or "")
                split = lambda key: [
                    item for item in str(row.get(key) or "").split("|") if item
                ]
                yield {
                    "doc_id": f"{target}:{finding}",
                    "finding_id": finding,
                    "gene_target": target,
                    "hipporag_text": " ".join(
                        filter(
                            None,
                            (
                                str(row.get("summary") or ""),
                                str(row.get("why_it_matters") or ""),
                            ),
                        )
                    ),
                    "source": {
                        "finding_type": row.get("finding_type"),
                        "confidence": row.get("confidence"),
                        "direction": row.get("direction"),
                        "literature_status": row.get("literature_status"),
                        "main_caveats": row.get("main_caveats"),
                        "source_summary": row.get("summary"),
                        "source_why_it_matters": row.get("why_it_matters"),
                        "cell_types": split("cell_types"),
                        "comparators": split("comparators"),
                        "genes": split("genes"),
                        "evidence_ids": split("evidence_ids"),
                        "ref_ids": split("ref_ids"),
                    },
                }
        return
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue


def finding_view(r):
    """What the grader sees: readout genes + framework prose. Deliberately EXCLUDES
    finding_type / literature_status (the metadata we are moving beyond) and any label."""
    s = r.get("source", {}) or {}
    def lst(x):
        return ", ".join(x) if x else "(none)"
    return (
        f"Perturbed gene (target): {r.get('gene_target','')}\n"
        f"Downstream readout genes that moved: {lst(s.get('genes'))}\n"
        f"Comparators: {lst(s.get('comparators'))}\n"
        f"Cell types: {lst(s.get('cell_types')) or 'global/unspecified'}\n"
        f"Direction: {s.get('direction') or '(unspecified)'}\n"
        f"Summary: {s.get('source_summary') or ''}\n"
        f"Why it matters (reported): {s.get('source_why_it_matters') or ''}\n"
        f"Narrative: {r.get('hipporag_text','')}\n"
    )


def grade_one(client, criterion, r):
    msg = criterion + "\n\n---\nFINDING TO GRADE:\n" + finding_view(r)
    try:
        txt = client.responses.create(model=MODEL, input=msg).output_text
        m = re.search(r"\{.*\}", txt, re.S)
        return json.loads(m.group(0)) if m else {"error": "no json", "raw": txt[:120]}
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)[:200]}


def keep(r, genes, ftypes, grep):
    s = r.get("source", {}) or {}
    if genes and r.get("gene_target", "").casefold() not in genes:
        return False
    if ftypes and (s.get("finding_type") or "") not in ftypes:
        return False
    if grep is not None:
        blob = " ".join(str(x) for x in (r.get("hipporag_text", ""), s.get("source_summary", ""),
                                         s.get("source_why_it_matters", ""), s.get("genes")))
        if not grep.search(blob):
            return False
    return True


FIELDS = ["rank", "interest", "rung", "capability", "gene_target", "finding_id", "doc_id",
          "carrying_genes", "why", "readout_genes", "cell_types"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ledger-path", default=None)
    ap.add_argument("--criterion", default=str(_DEFAULT_CRITERION))
    ap.add_argument("--out-dir", default="./rung_ranking")
    ap.add_argument("--gene", action="append", dest="genes", default=[])
    ap.add_argument("--finding-type", action="append", dest="finding_types", default=[])
    ap.add_argument("--grep", default=None)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--top", type=int, default=30)
    a = ap.parse_args()

    from openai import OpenAI
    client = OpenAI()
    criterion = Path(a.criterion).read_text()

    genes = {g.casefold() for g in a.genes}
    ftypes = set(a.finding_types)
    grep = re.compile(a.grep, re.I) if a.grep else None
    findings = [r for r in iter_findings(ledger_path(a.ledger_path)) if keep(r, genes, ftypes, grep)]
    if a.limit:
        findings = findings[: a.limit]
    if not findings:
        raise SystemExit("no findings matched the filters.")

    print(f"grading {len(findings)} findings (model={MODEL}, workers={a.workers}) …", file=sys.stderr)
    graded = [None] * len(findings)
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(grade_one, client, criterion, r): i for i, r in enumerate(findings)}
        done = 0
        for fut in futs:
            i = futs[fut]
            graded[i] = fut.result()
            done += 1
            if done % 200 == 0:
                print(f"  {done}/{len(findings)}", file=sys.stderr)

    rows = []
    errs = 0
    for r, obj in zip(findings, graded):
        s = r.get("source", {}) or {}
        if "error" in obj:
            errs += 1
        try:
            interest = float(obj.get("interest"))
        except (TypeError, ValueError):
            interest = -1.0
        rows.append({
            "interest": interest, "rung": obj.get("rung", ""), "capability": obj.get("capability", ""),
            "gene_target": r.get("gene_target", ""), "finding_id": r.get("finding_id", ""),
            "doc_id": r.get("doc_id", ""),
            "carrying_genes": "|".join(obj.get("carrying_genes", []) or []),
            "why": obj.get("why", obj.get("error", "")),
            "readout_genes": "|".join(s.get("genes") or []),
            "cell_types": "|".join(s.get("cell_types") or []),
        })

    def key(x):  # rank by interest, then rung
        try:
            rung = float(x["rung"])
        except (TypeError, ValueError):
            rung = -1
        return (x["interest"], rung)
    rows.sort(key=key, reverse=True)
    for i, x in enumerate(rows, 1):
        x["rank"] = i

    out = Path(a.out_dir).expanduser()
    out.mkdir(parents=True, exist_ok=True)
    with (out / "ranked_by_rung.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)

    print(f"graded={len(rows)}  errors={errs}")
    print(f"ranked -> {out / 'ranked_by_rung.csv'}")
    if a.top:
        print(f"\nTop {min(a.top, len(rows))} by interest:")
        for x in rows[: a.top]:
            print(f"  {x['rank']:>4} int={x['interest']:.2f} rung={x['rung']}  {x['gene_target']:10} {x['finding_id']}  "
                  f"{(x['capability'] or '')[:44]:44}  [{x['carrying_genes'][:40]}]")


if __name__ == "__main__":
    main()
