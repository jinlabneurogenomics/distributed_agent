---
name: adaptive-query-skill
description: Execute compact adaptive Perturb-seq analyses from truthful run-local capabilities; use cached quantitative feature calibration only for predictive rankings with explicit ranked or partial-ranked supervision.
---

# Adaptive Perturb-seq query

The task and dataset portrait are authoritative. Read the run-local capability
manifest and use only entries marked `available`. Capability kinds distinguish
executable tools, readable resources, and unavailable operations. Do not
reconstruct a missing framework operation from a conceptual capability.

When a corpus capability declares `mcp_server` and `mcp_tools`, call those
native tools directly. The selected release and its policy manifest are bound
by the host, so do not reconstruct a release path or invoke a release wrapper
for the same operation. A non-null `entrypoint` remains the interface for
capabilities that have not moved behind the native corpus server.

When available, prefer `target_context`, `get_claim`, `get_finding`, and
`compare_targets` over hand-written Cypher for ordinary biological navigation.
Treat shared-Claim paths and explicit Finding-reference paths as different
evidence lanes; a one-sided reference remains usable and does not require a
reciprocal mention. Use `read_cypher` only when the structured tools cannot
express the bounded read-only question.

Ordinary adaptive runs use one continuous tool loop. They do not require a plan
DAG, candidate lanes, evidence cards, execution bookkeeping, or delegation.

## Evidence order

- Named, report-rich comparison: compact Findings, Claims, Evidence, or bounded
  report prose first.
- New numerical calculation: declared dataset first.
- Predictive ranking: quantitative basis first, then a bounded falsifier or
  boundary review.
- Broad findings synthesis: structured corpus index and aggregation first.

The Parquet, reports, Findings, Claims, Evidence, References, and Literature
Comparisons are representations of the same experiment. Agreement among them is
not independent replication.

## Perturb-seq feature workbench

This is an ordinal ranking workbench, not a generic feature generator or scalar
regression utility. Use it only when `dataset.perturbseq_features` is marked
`available`. That state means all three conditions hold: the task asks for a
predicted ranked output, `task_bindings.json` contains an active ranked or
partial-ranked gene set, and a declared Parquet input is present.

Never invoke this workbench for a scalar/count prediction, an unranked target
list, or ordinary biological interpretation, even when a Parquet input exists.
For a new scalar calculation, query only the necessary declared dataset columns
and rows; do not create a whole-Parquet feature cache or attempt ordinal
calibration.

For an eligible ranking, use `scripts/perturbseq_feature_workbench.py` and the
capability manifest's `accepted_arguments`, compact `example`, and
`output_bound`; a separate `--help` invocation is unnecessary. The sequence is:

1. `summarize`: scan the declared Parquet once and cache a target-level or
   target-by-cell-type feature table. It supplies signed, absolute,
   distributional, FDR, missingness, and trans-effect summaries for the
   measurement families present in the declared schema. Continuous score and
   p-value columns are optional; a binary FDR<0.10 column supplies only the
   corresponding threshold features. Use explicit column-role arguments for a
   schema whose names differ from the canonical Perturb-seq names.
2. `calibrate`: compare single features and bounded two-feature ensembles using
   nested rank-stratified cross-validation. Pairwise-correlated ensembles are
   excluded, the final choice follows a one-standard-error simplicity rule,
   and bootstrap top-k stability is reported. The command writes a JSON report,
   a canonical ranking table, and `residual_anchors.tsv`: at most ten supplied
   examples with the largest out-of-fold underprediction gap. These are
   diagnostic review anchors, not newly scored candidates.
3. `validate-ordering`: confirm that the requested ranking either preserves the
   canonical order or supplies an exact override record for every displacement,
   with candidate-specific endpoint evidence and the displaced candidate.

The workbench rejects graph-derived columns. Its out-of-fold metrics measure
alignment with supplied ordinal examples; they do not make normalized
differential expression a direct measurement of an absent endpoint.
Distinguish proxy stability from endpoint adequacy: a stable feature can still
systematically underpredict supplied examples when it does not measure the
requested endpoint.

Do not rescan the full Parquet after `summarize`. Reuse the feature-table path
and cache key in its manifest.

## Causal experimental interpretation

Before transferring an outcome between related perturbations, trace the
experiment from intervention through direct molecular effect, propagation
through complexes or programs, exposure and selection, sampling or
survivorship, and the measured endpoint. For each candidate returned by bounded
review, state whether the endpoint direction should be the same, opposite, or
indeterminate. Obligate complexes and established directional dependencies are
same-outcome priors only when both perturbations impair the same limiting
function in the relevant context and time window; broad pathway co-membership
is not sufficient. Require a candidate-specific reason to infer divergence,
such as opposite sign, redundancy, bypass or feedback, missing context,
ineffective perturbation, timing mismatch, or documented endpoint divergence.
A downstream readout measured only in survivors cannot by itself falsify an
earlier selection effect. This is bounded endpoint reasoning, not permission to
score candidates by graph or pathway proximity.

An established causal dependency can be endpoint-bearing transfer evidence
without an identical endpoint measurement when the perturbations impair the
same limiting function and the full experimental chain predicts the same
direction. A different tissue, cell type, or model is a confidence qualifier,
not by itself a causal break; declining transfer requires naming the
candidate-specific link expected to fail. Conditional or synthetic-only
evidence does not transfer unless the requested experiment contains the second
condition. Generic pathway membership and unsupported mechanistic plausibility
remain insufficient.

## Semantic review

For a predictive ranking, do not use the broad
`corpus.relational_candidates` operation. First label the requested endpoint as
directly observed, supported by a validated proxy, or absent from the declared
inputs.

When the endpoint is absent and `corpus.predictive_graph_review` is available,
run its `nominate` command once after calibration. Pass `task_bindings.json` and
the workbench calibration JSON plus the requested `top-k`. The host-frozen
operation derives the visible anchors and candidate universe, uses the directed
relation where a visible seed's Finding names a candidate, and emits complete
multiplicity tiers within its character bound without splitting the boundary
tier. It serializes candidates alphabetically and emits only identity,
multiplicity, visible anchors, quantitative prediction rank, top-k overlap, and
review role. It emits no Finding text. Read the complete nomination.
Multiplicity, anchors, and pool membership determine retrieval breadth only;
they are not endpoint evidence or final ranking features.

Update the emitted disposition TSV truthfully: `inspected=true` means the
candidate was considered. Treat the quantitative top-k plus every
`graph_only_challenger` as the adjudication union. Inspect every graph-only
challenger and give it a short rationale, including an explicit insufficient-
evidence disposition when appropriate. Do not use `corpus.findings` or legacy
Finding summaries for predictive adjudication. Set `evidence_read=true` only
when independently resolved, candidate-specific endpoint evidence entered the
decision. After freezing the final answer, run `finalize`. It compares the
nominated pool, canonical top-k, and final answer and records nominated,
inspected, evidence-read, retained-quantitative, promoted, rejected, and
not-reviewed candidates. A graph-nominated promotion fails validation unless
it was inspected and its evidence was read.

For an absent endpoint, the canonical quantitative order is an explicit proxy
baseline, not a protected prefix. A reviewed candidate can change membership
or position anywhere in the requested top-k only when candidate-specific
endpoint-bearing evidence supports the same experimental causal chain. Graph
multiplicity, generic pathway membership, and relation presence alone never
justify promotion. Record every changed rank and paired displacement in the
override file and pass it to `validate-ordering`.

When the endpoint is directly observed or has a validated proxy, preserve a
quantitative core and reserve at most the lowest
`min(5, ceil(0.1 * k))` positions for causal review. Use
`residual_anchors.tsv` with `corpus.direct_evidence` for that smaller review,
passing `--calibration` so anchors and the candidate universe remain
host-derived. The tool admits at most 10 anchors, three records per anchor, 16
records, and 12,000 characters. Its index contains identity, pairing precision,
and one causal summary for exact comparisons or explicitly tagged peers. Exact
pairs are presented first for attention, not as a score. Load compact detail for
at most three material record IDs only when missing context can change a
decision; resolve full provenance separately only when the output needs a
citation.

Promote a candidate into this smaller band only when calibration residuals show
proxy underprediction on a relevant supplied anchor, candidate-specific
evidence establishes an obligate or directional link to the same limiting
function, the experimental chain predicts the endpoint in the same direction,
and no candidate-specific divergence mechanism is supported. Preserve
canonical order outside the band and among non-promoted candidates, and record
each exact promotion and displacement for `validate-ordering`. If declining a
strong transfer candidate in either endpoint regime, name the causal break
instead of citing context difference alone.

External retrieval is optional and bounded to an explicit definition, missing
prior, conflict, boundary decision, or falsification need.

Produce exactly the requested files and mechanically validate schemas, row
counts, uniqueness, referential integrity, and ordering before finishing.
