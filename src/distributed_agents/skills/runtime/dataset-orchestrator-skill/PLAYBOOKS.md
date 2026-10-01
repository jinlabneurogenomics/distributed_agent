# Composable execution patterns

These are optional stage shapes, not task classifiers. First resolve and
validate `distributed_agents-task-profile-v4`; then use, adapt, combine, or ignore these
patterns.

## v4 plan contract

`distributed_agents-task-plan-v4` carries the resolved profile into execution:

- endpoint, layered schema relation, coverage, candidate universe, and output
  contract;
- dataset-context manifest and task overrides;
- skill roles, resource strategy, transfer caveats, and residual questions;
- independent dataset, external, and indirect evidence roles plus the selected
  quantitative basis;
- candidate decision criteria, mechanism and multi-hop models, proxy model, and
  evidence roles;
- evidence-ledger and reduction policy;
- ordered stages with owners, inputs, outputs, completion tests, recovery, and
  termination.

`playbook` is optional provenance and never controls dispatch.

## Bounded measurement

Use the authoritative input directly when it observes the endpoint. Preserve the
requested unit and aggregation.

## Targeted synthesis

Route the requested targets and relevant semantic context. Read their packaged
grounding, validate output-critical measurements, and synthesize the bounded
relationship.

## Atlas discovery

Route the complete selected Claim scope, review coherent clusters, preserve
distinct grounded anchors, and compare the complete evidence-backed candidate
set only at final reduction.

## Contextual-prior ranking

Use this branch only when external evidence is the declared
`quantitative_anchor`:

1. `endpoint_capability`
2. `claim_attention` only for a defensible ordered basis
3. optional evidence or `mechanism_expansion`
4. `score_blind_interpretation`
5. `global_reduction`
6. `role_aware_audit` when a proxy is required
7. `assembly`

`endpoint_capability` produces the versioned resource manifest, full-universe
candidate result and coverage audit. `claim_attention` uses
`build_claim_attention.py` to write a private weighted path audit and a compact
summary of additional related genes. `score_blind_interpretation` is the
machine stage name for building short Claim/Finding context cards; the cards
retain each starting gene's ordinal position but not private graph weights.
`global_reduction` sees the quantitative result, evidence role, transfer
caveats, and every context card, then ranks the whole comparison set.
`assemble_global_ranking.py` validates complete accounting and contiguous final
ranks without protecting a prefix or imposing a swap budget.

## Same-experiment prediction

When the supplied dataset is the `primary_same_experiment_inferential_substrate`,
use:

1. `quantitative_basis`
2. `claim_attention` only for a defensible ordered basis
3. optional evidence or `mechanism_expansion`
4. `score_blind_interpretation`
5. `global_reduction`
6. `role_aware_audit` when a separate proxy is required
7. `assembly`

External evidence may provide qualitative mechanism or validation without
generating the basis.

## Exhaustive classification

Enumerate the complete unit space mechanically. Join ledger evidence through
stable identifiers, apply the requested taxonomy per unit, and validate exact
accounting and referential integrity. When the experiment corpus contains the
needed observations, interpretations, literature status, references, and
caveats, map those native primitives into the requested taxonomy rather than
recomputing the semantic layer from scratch. Validate exact measurements
against the dataset and retrieve fresh evidence only for explicit coverage
gaps or conflicts.

## Composed analysis

Compose only the measurement, semantic, external-prior, transfer, causal,
ranking, or classification stages required by the validated profile. Stop when
the exact deliverable and its accounting are complete.
