# Dataset-conditioned reasoning contract

This contract governs every DistributedAgents dataset query. Derive the endpoint,
evidence roles, and execution shape from first principles. Do not map endpoint
names to canned workflows.

## 1. Understand the requested quantity

Resolve these questions before choosing tools or candidates:

- What must be returned, at what unit, and over which candidate universe?
- What biological event is requested, and what measurement would observe it
  directly?
- Which available measurements are related to that event but are not the event
  itself?
- How dependent is the answer on species, age, perturbation, tissue, cell
  population, assay, and time?
- Could the requested event remove observations before the local assay measures
  them?

Read the selected dataset portrait once as a separate framework input. The task
text remains unchanged and authoritative. Treat the Parquet, Claims, Findings,
and reports as different representations of the same experiment, not as
independent replication.

Classify dataset observability (`direct`, `proxy`, `absent`, or
`unobserved_context`), ledger alignment (`native`, `adjacent`, `incidental`,
`absent`, or `not_required`), and answer mode (`direct`, `derived`, or
`predicted`). Audit corpus coverage separately; missing retrieval is not a
biological negative.

## 2. Decide what each source is allowed to do

Assign roles independently:

- supplied dataset: direct measurement, primary same-experiment evidence for an
  inference, candidate universe, supporting context, or not required;
- external evidence: quantitative starting point, qualitative mechanism,
  validation/falsification, or none;
- proxies: supporting, veto/support under a declared rule, or not required.

Then choose one reproducible starting substrate, recorded in the machine
profile's `quantitative_basis` for schema compatibility as exactly one of these
values:

- `direct_dataset_result` — a direct result from the supplied dataset;
- `same_experiment_derived` — a result derived from the supplied dataset,
  including a prespecified candidate-matched aggregate or multifeature
  heuristic over it;
- `external_quantitative_prior` — a candidate-level ordering from another
  source, used as the `quantitative_anchor`; or
- `neutral_candidate_universe` — an unranked candidate universe when no ordering
  is defensible; or
- `corpus_claim_substrate` — an unordered experiment-interpretation corpus when
  the requested output remaps, adjudicates, or synthesizes its grounded records.

The substrate is evidence for the final answer, not a protected answer.
Evaluate sufficiency for the final requested judgement, not merely for one
observable used by that judgement. A dataset can directly measure a response
while being unable to determine whether that response agrees with literature.
Likewise, do not construct an ordering for an exhaustive classification or
synthesis unless the deliverable actually consumes a comparable scalar.

An ordering is eligible only when its measured event has a defensible
directional relationship to the requested event, the requested event does not
erase that measurement, and values have comparable candidate-level meaning.
Post-event survivor measurements have at least possible erasure; completeness
among survivors does not repair it.

For an assay-defined count, intensity, or normalized quantity, another assay's
same-named field is not quantitatively transportable without destination
calibration. A portable biological-event ordering may still be a partial
starting point for an experiment-conditioned answer; state what context it
lacks. A controlled candidate-matched same-experiment heuristic need not be a
calibrated endpoint estimate, but it must pass the same ordering test.

Record why the selected starting point is preferable to serious alternatives.
Acquisition failure selects another independently eligible source or the
unranked universe; it never makes an ineligible measurement eligible.

## 3. When an external source supplies the quantitative starting point

Infer the needed public resource class and select one versioned, candidate-level
source by endpoint fit, coverage, provenance, and transportability. Materialize:

- the complete candidate-level result available from that source;
- its ordering and values, with missing candidates marked as missing rather
  than assigned the worst value;
- a resource manifest and coverage audit; and
- the unresolved transfer questions between that source and this experiment.

The external source need not contain the destination cell type to be useful. It
must measure a relevant event well enough to provide ordering information. The
final interpretation supplies the missing experiment and cell-context layer.
Add another external source only for a declared coverage gap or falsification
question.

## 4. Use Claims as relational attention when justified

Claims are structured relationships distilled from earlier per-perturbation
analyses of this same experiment. Findings are the compact source statements
behind them. They can identify which genes deserve comparison and explain
same-experiment context; they are not a second measurement of the requested
endpoint.

Claims and Findings have a second, distinct use: when the requested output is
itself a mapping or synthesis of experiment-grounded interpretations, the
corpus is the primary unordered substrate. Map its native fields and labels
into the task taxonomy, verify output-critical measurements against the
Parquet, audit coverage, and retrieve fresh evidence only for explicit gaps.

Use Claim expansion only when the quantitative starting point has a
scientifically meaningful relative ordering. Unknown predictive accuracy is
acceptable. A weak, arbitrary, or unranked starting point must not generate a
large graph neighborhood; Claims may still interpret candidates already named
by the task.

For an ordered top-`k` starting set:

- use order privately as broad seed bands: top 20%, next 30%, remaining 50%;
- follow one-hop explicit targets, implications, boundaries, comparators, and
  typed Claim relations;
- prioritize relations using seed band, intrinsic relation reliability,
  Claim/relation confidence, independent support, and inverse fan-out;
- do not use DEG magnitude or significance to choose graph-related candidates;
- admit at most `min(50, ceil(k/2))` additional candidates, mostly by relational
  support with a small deterministic diversity share.

Relation strength only decides what to inspect. A buffering, divergence,
uncoupling, or non-interchangeability relation can be highly relevant while
arguing against moving a candidate upward.

Keep the detailed graph-path audit private. For each gene in the starting set
and each graph-related gene, build a short, self-contained context card with at
most three Claim paths and a few candidate-specific Findings. The card should
say which starting genes it is related to and how. Read full reports only when
a material decision remains unresolved, evidence conflicts, or a citation must
be verified, capped at `min(20, ceil(comparison_set/10))`.

## 5. Compare the entire candidate set globally

Give one fresh reviewer:

- the unchanged scientific task;
- the relevant dataset context;
- the complete quantitative starting result, its evidence role, and transfer
  caveats;
- all starting and graph-related candidates;
- the short context cards and provenance; and
- explicit uncertainty and missing-value semantics.

The reviewer must compare the full set and return one global ordering. The
starting order remains quantitative evidence, but no fixed prefix is protected,
there is no automatic swap limit, and a graph-related candidate is not
automatically inferior because the external source did not score it. Any
movement should state whether it follows the quantitative evidence, corrects a
transport problem, or is supported by same-experiment relational context.

Maintain a candidate evidence table separating direct measurement,
same-experiment inference, packaged interpretation, external evidence, context
fit, contradiction, and uncertainty. Do not seed the reviewer with preferred
genes, pathways, task-specific exclusions, or evaluation labels.

## 6. Audit and finish

Audit supporting or veto proxies after global comparison. State their causal
link, controls, falsifiers, context comparisons, and null semantics. A proxy may
support, veto under a predeclared rule, or increase uncertainty; a proxy-null
must not silently remove a candidate.

Preserve the quantitative result, coverage audit, Claim-path provenance,
context cards, candidate evidence table, global-ranking audit, and any
proxy-independence audit. Finish only when all candidates in the comparison set
are accounted for and the requested deliverables pass schema, count,
provenance, and output checks. Withheld labels, grader artifacts, prior answers,
and evaluation results are never evidence.
