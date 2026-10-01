---
name: relational-candidate-skill
description: Retrieve an unranked typed semantic map from a supplied partial ranking, positive set, exemplar list, or other visible Perturb-seq anchors. Use when a task asks for missing candidates, analogs, comparators, convergence partners, or completion of a partly revealed result and the same-experiment Findings ledger can connect anchors to other assayed targets.
---

# Relational candidate retrieval

Use this skill to turn visible anchors into an auditable, unranked semantic map.
The runtime preserves distinct relation lanes and estimates map coverage by
hiding only visible anchors. It does not read hidden task answers or assert that
a retrieved candidate matches the endpoint.

## Non-negotiable boundary

The graph is semantic guidance only. Never use graph topology, edge counts,
relation counts, degree, path counts, reciprocal status, shared-term counts,
dropout metrics, or any combination of them to score, rank, promote, or demote
candidates. The separately declared `corpus.predictive_graph_review`
operation may use directed distinct-visible-seed comparator multiplicity only
to select complete multiplicity tiers within its output bound. It emits
candidate identities, multiplicity, visible anchors, and quantitative-overlap
metadata alphabetically, never Finding text, and requires explicit review of
every graph-only challenger plus independently resolved endpoint-bearing
evidence for any final promotion or ordering change.

Use typed relation text to decide which reports, signatures, or endpoint-bearing
evidence to inspect and which alternatives or contradictions must be considered.
If the requested answer is ordered, its ordering must come from
endpoint-specific observed data or separately justified endpoint-bearing
evidence. If that evidence is unavailable, state the limitation rather than
manufacturing an ordering from the graph.

## Run

```bash
python scripts/relational_candidates.py \
  --seeds-file task.md \
  --out evidence/relational_candidates.json \
  --candidates-out evidence/relational_candidates.csv
```

The seed file may be CSV, TSV, a one-gene-per-line file, or Markdown containing
a fenced table with `gene_target`, `target_gene`, `gene`, `symbol`, or
`perturbation`. Use `--candidate-universe` when a declared dataset target list
is available; otherwise the runtime uses biological target genes in the ledger.
It excludes visible seeds, `Non_target`, and `Safe_target_*` from candidates.

## Interpret

Read `lanes` as alphabetically serialized semantic groups and inspect
`candidate_map` for typed evidence:

- `outgoing`: an anchor Finding names the candidate.
- `reverse`: a candidate Finding names an anchor.
- `reciprocal`: both directions exist for the same pair.
- `bidirectional`: context exists in both orientations, possibly through
  different anchors.
- `second_hop`: comparator paths through an intermediate that suggest bounded
  follow-up reads.
- `shared_response`: overlapping response terms that suggest a targeted
  signature comparison.

Do not collapse, count, weight, or order these groups. Convergence or coherent
phenocopy language can guide an endpoint-relevant follow-up. `negative_result`,
divergence, opposition, pathway uncoupling, and generic stress are semantic
warnings or falsifiers, never positive edges by default.

`map_diagnostics` also reports the broader `bidirectional_intersection`: a
candidate connected in both directions, possibly through different anchors.
Do not confuse that set with same-pair reciprocal support.

## Use the dropout audit

`seed_dropout` uses deterministic rank-interleaved folds. It hides a subset of
the supplied anchors, retrieves from the remainder, and reports aggregate map
coverage and enrichment. These are tool-level diagnostics. They may justify
whether a relation lane is worth inspecting, but they must never be copied into
candidate-level features or used to order candidates.

This audit measures internal relational signal only. It is not held-out task
accuracy, does not validate the endpoint, and must not be described as recall
of the unknown answers.

## Finish

Use the candidate map to nominate bounded report reads, signature comparisons,
or endpoint-relevant questions. Cite the Finding IDs behind material semantic
guidance. Final selection and ordering require non-graph, endpoint-bearing
support.
