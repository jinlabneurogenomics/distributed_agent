---
name: relational-candidate-skill
description: Retrieve release-native comparator maps and bounded review candidates from the Shi holdout corpus. Use for semantic navigation around visible perturbation anchors or for summary-free challenger review after quantitative calibration; never use relation counts or topology as an endpoint score.
---

# Shi Holdout Relational Candidates

Use this skill to inspect relationships explicitly encoded by the Shi holdout
Findings. The substrate is the structured `comparators` and `genes` fields in
the Finding ledger; it is distinct from the higher-order Claim graph.

For an unranked semantic map:

```bash
python scripts/relational_candidates.py \
  --seed Tsc1 --seed Tsc2 --out evidence/semantic-map.json
```

For an absent-endpoint prediction task, first create the quantitative ranking,
then nominate the complete eligible comparator-multiplicity tiers:

```bash
python scripts/predictive_graph_review.py nominate \
  --bindings pipeline/task_bindings.json \
  --calibration workbench/calibration.json \
  --top-k 50 \
  --out workbench/predictive_graph_review.json \
  --dispositions-out workbench/predictive_graph_review_dispositions.tsv
```

The predictive output contains identities and visible anchors, never Finding
prose. Multiplicity controls review breadth only. Every graph-only challenger
requires independent endpoint-bearing evidence and a completed disposition;
final ordering cannot be derived from comparator degree, lane membership,
shared-gene counts, or other topology.

Use `direct_evidence.py` for a bounded summary-first view of explicitly named
comparators. All Shi holdout comparator evidence is Finding-scoped: references and
caveats belong to the whole Finding and are not automatically paired to one
candidate.
