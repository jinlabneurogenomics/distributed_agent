---
name: findings-ledger-skill
description: Retrieve exact reports, findings, null-cause findings, evidence, references, pathways, and cell-type summaries from the Shi holdout corpus. Use for target-scoped corpus lookup and citation or evidence resolution; do not use it as an endpoint measurement or evaluation answer source.
---

# Findings Ledger

Use the canonical ledgers before opening full prose. IDs are target-scoped:
`Cplx1:F003` and another target's `F003` are different records. Preserve the
source distinction between biological findings (`F...`) and null-cause findings
(`N...`).

Run the packaged commands from this skill directory:

```bash
python scripts/query_ledger.py findings --gene Cplx1 --json
python scripts/query_ledger.py null_findings --gene Cplx1 --json
python scripts/resolve_evidence.py --gene Cplx1 --finding F003 --json
python scripts/read_reports.py Cplx1 --grep "vesicle|synaptic" --max-reports 1
python scripts/query_corpus.py calibrate summary
python scripts/query_corpus.py count --artifact claims --field relation_family
python scripts/query_corpus.py inventory --artifact relations --gene Cplx1 --limit 20
```

The six ledgers are `findings`, `null_findings`, `evidence`, `references`,
`pathways`, and `cell_types`. `query_ledger.py --count FIELD` gives transparent
field counts; `--grep` searches the complete structured record.

Open full reports only when the structured record is insufficient. Cite the
target-scoped finding/evidence/reference IDs and retain caveats. `Atp6v1b2` has
a source-truncated appendix: its recovered evidence and two complete references
are valid, but absent downstream sections must not be inferred.

For compatibility queries, one Shi holdout atomic `Claim` is exactly one `Finding`;
no semantic deduplication or cross-Finding merge was performed. A
`REVIEW_WITH` relation means only that the two Findings' targets are reciprocal
explicit comparators. Treat it as a prompt for review, never as agreement,
endpoint evidence, causal transfer, or priority.
