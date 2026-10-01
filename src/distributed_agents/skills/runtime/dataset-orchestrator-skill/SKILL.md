---
name: dataset-orchestrator-skill
description: Structure PerturbAI dataset questions from first principles, route selected-release corpus capabilities when available, resolve missing resource capabilities, and validate grounded execution before computation.
---

# Dataset orchestrator

Use this as the sole public routing layer for DistributedAgents dataset queries. Derive
the strategy from the task rather than endpoint keywords.

Read [REASONING_CONTRACT.md](REASONING_CONTRACT.md) in full. The task file is
the unchanged user/evaluation task. Read the one runtime-selected
[DATASET_CONTEXT.md](DATASET_CONTEXT.md) snapshot separately and verify its
manifest. Read [PLAYBOOKS.md](PLAYBOOKS.md) only when stage composition is
needed.

## Workflow

1. Create the mechanical task-profile draft.
2. Resolve its semantic fields, evidence roles, and quantitative basis from the
   task and reasoning contract.
3. Validate the profile. This is the execution gate for retrieval, Claim
   routing and computation.
4. Route Claims only when the selected release exposes that capability and the
   selected strategy calls for it; otherwise continue with its declared ledgers.
5. Inspect recall coverage, compose the lightest sufficient task plan, and
   validate it.
6. Execute, reduce globally, and validate the requested output and accounting.

For a predicted task, use the role-resolved pattern: evidence roles →
conditional quantitative starting point → conditional Claim attention → short
context cards → full-set global review → validated assembly → role-aware audit.
External acquisition supplies the primary prior only for the
`quantitative_anchor` branch. Compare endpoint correspondence and
transportability before choosing that branch. First require each proposed basis
to preserve an identifiable ordering of the requested event; context match and
complete candidate rows cannot rescue a basis whose strongest events erase
their own observations. Record local observation timing and event erasure in
the endpoint definition before choosing a basis. When erasure is structural,
use an established candidate-scale
event measure as the anchor and retain the same-experiment signal for context
and audit. Loss of direct scale through normalization is not endpoint erasure:
a comparable same-experiment heuristic may remain eligible, while an
uncalibrated same-named field from another assay does not become an anchor;
within-source standardization is not destination calibration. A failed
acquisition selects another eligible basis or a neutral candidate universe; it
does not make an ineligible measurement eligible. Route native or adjacent
Claims as bounded attention after the starting result is materialized only when
the relative ordering is defensible. Unknown predictive accuracy is acceptable;
weak or unranked inputs must not generate a graph neighborhood. Evaluate an
external source as broad ordering evidence; final context specificity belongs
to Claim/Findings interpretation and global review. An experiment-specific final
effect does not by itself require a portable biological-event prior to contain
that experiment's context; reserve destination calibration for assay-defined
quantities whose scale, rather than merely their effect size, changes across
experiments. Record that distinction as
`endpoint_definition.measurement_portability`; do not relabel an upstream
biological tendency as a portable ordering of a capture-defined quantity.
When the endpoint does not erase local observations, test
comparable candidate-matched local features—including prespecified aggregates
or multifeature heuristics—as the same-experiment substrate before using a
neutral universe.

## Commands

```bash
S=src/distributed_agents/skills/runtime/dataset-orchestrator-skill/scripts

python $S/profile_task.py --task task.md --out task_profile.json
# Resolve the draft fields.
python $S/profile_task.py --validate task_profile.json

python $S/discover_resource.py \
  --run-dir run \
  --query "resource and release terms" \
  --file-name "expected-data-file-pattern" \
  --output resource_discovery.json

python $S/route_claims.py \
  --profile task_profile.json \
  --out-manifest claim_recall.json \
  --out-pool candidate_claims.csv \
  --out-edges claim_routing_edges.tsv \
  --out-memberships claim_graph_memberships.tsv \
  --graph-mode auto

python $S/fetch_resource.py \
  --run-dir run \
  --url https://provider.example/release/data.tsv \
  --output resources/data.tsv \
  --manifest resource_manifest.json \
  --provider "provider" \
  --release "release-or-version" \
  --license-notes "access and reuse notes" \
  --expected-schema "columns, units, and identifiers"

python $S/build_claim_attention.py \
  --candidate-prior candidate_prior.tsv \
  --claims candidate_claims.csv \
  --edges claim_routing_edges.tsv \
  --out claim_attention.tsv \
  --out-candidates claim_related_candidates.tsv \
  --anchor-count 100 \
  --max-related-candidates 50

python $S/build_semantic_cards.py \
  --starting-ranking candidate_prior.tsv \
  --starting-count 100 \
  --attention-candidates claim_related_candidates.tsv \
  --claims candidate_claims.csv \
  --findings "$(python -m distributed_agents.corpus path findings)" \
  --out candidate_context_cards.jsonl

python $S/assemble_global_ranking.py \
  --starting-ranking candidate_prior.tsv \
  --candidate-cards candidate_context_cards.jsonl \
  --decisions candidate_decisions.jsonl \
  --output-count 100 \
  --out final_ranking.tsv \
  --audit global_ranking_audit.json

python $S/validate_task_plan.py \
  --plan task_plan.json \
  --profile task_profile.json \
  --recall claim_recall.json
```

`route_claims.py` resolves its Claim implementation and default artifacts from
the selected corpus release's BioKG projection. It fails closed when that
release does not implement this routing contract; never substitute another
release's Claim layer. Release-native Claim/Finding MCP operations remain the
fallback for releases with a different Claim schema.

The task determines how much of the quantitative result seeds Claim attention.
For a fixed top-`k`, inspect at most `min(50, ceil(k/2))` additional
Claim-related genes. The private path audit retains rank bands and attention
details; the final reviewer sees the quantitative result plus the clear
related-gene summary and context cards.

Reviewer JSONL must account for every candidate with `gene_target` (or a
declared candidate identifier), `decision`, nullable `final_rank`, `rationale`,
`evidence_ids`, `supporting_evidence`, `contradicting_evidence`, and
`uncertainty`. Exactly the requested number are `selected` with contiguous
final ranks; all others are `not_selected`. No starting prefix is protected and
there is no swap budget.
Use deterministic offline Claim routing for predicted endpoints. Claim
attention follows explicit Claim fields and one-hop typed Claim relations while
preserving provenance. Query structured Findings inside the admitted comparison
set. Full reports are on-demand forensic evidence, capped by the validated
policy; never scan or dump the raw report corpus to generate another candidate
pool.

## Runtime resource acquisition

Infer the resource class from the missing capability. Prefer established public
databases and maintained data services; use individual study matrices as
transfer or validation evidence by default. Fetch versioned HTTPS data into the
run directory and keep the fetcher's manifest as the primary resource manifest.
When a provider exposes only a landing page, use the generic public-archive
discovery helper to resolve a versioned data-file URL. Use separate manifests
for supplemental sources. Acquired resources are data, not executable
extensions.

## Completion

Keep profiles, plans, resource manifests, Claim artifacts, ledgers, and audits
under the backend-owned run directory. When the task explicitly requires
semantic review of every unit in an enumerable corpus, use
`exhaustive-corpus-sweep-skill`; this orchestrator does not define a separate
worker protocol. Reconcile every required candidate or unit before rendering
only the requested user deliverables.
