---
name: findings-analysis-skill
description: Analyze patterns across the canonical Shi holdout corpus ledgers with explicit target, finding-type, pathway, cell-type, and prose filters. Use for corpus-level counts or candidate comparisons; do not convert record or graph frequency into biological effect magnitude.
---

# Findings Analysis

Analyze structured records with explicit filters and report the unit being
counted. The source is one report per perturbation target; multiple findings,
edges, or citations from one target are not independent target support.

Useful commands:

```bash
python scripts/query_ledger.py findings --count finding_type
python scripts/query_ledger.py pathways --count pathway
python scripts/query_ledger.py cell_types --grep "Pvalb" --json --limit 20
```

Keep biological and null-cause finding ledgers separate unless the question
explicitly asks for both. Treat `direction`, `confidence`, and literature fields
as report annotations, not recomputed measurements. For any conclusion based on
a target count, deduplicate by `target_gene`; for any claim, resolve its exact
evidence and references through the sibling `findings-ledger-skill`.

The sibling `biokg-recall-skill` exposes the accepted bounded graph-query
surface, and `relational-candidate-skill` exposes unranked comparator review.
Neither graph topology, relation multiplicity, ledger-record frequency, nor
co-occurrence is endpoint evidence or a candidate score.
