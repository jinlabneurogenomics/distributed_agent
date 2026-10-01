Prioritize evidence by what can change the answer:

- For a named, report-rich comparison, inspect compact Findings, Claims,
  packaged Evidence, or bounded report prose first.
- For a new quantitative calculation, start from the declared dataset.
- For a predictive ranking, establish the quantitative ordering basis first,
  then inspect a bounded set of boundary cases or falsifiers.
- For broad findings or story synthesis, begin with the structured corpus index
  and aggregate before opening full reports.

For a ranking with supplied supervision, compare a small set of plausible
non-graph quantitative bases against the supplied ranks. Use out-of-fold,
leave-one-example-out, bootstrap, or other stability evidence available under
the declared capabilities. When `dataset.perturbseq_features` is available, use
its cached `summarize` output and nested `calibrate` operation instead of
writing a new Parquet aggregation or combining features by hand. This capability
is specific to predictive rankings with active ranked or partial-ranked gene
supervision. Never invoke it for scalar/count prediction, unranked target lists,
or ordinary interpretation; use narrow declared-dataset queries for genuinely
new numerical calculations. Prefer the simplest stable single feature unless a
more complex model shows a material
out-of-fold improvement. State the chosen basis and its endpoint relationship,
missingness, counterexamples, and uncertainty. Distinguish proxy stability from
endpoint adequacy: a feature can be reproducible yet systematically
underpredict supplied examples because it does not measure the requested
endpoint. Label the requested endpoint as directly observed, supported by a
validated proxy, or absent from the declared inputs before treating the emitted
canonical order as authoritative. Run `synthesis.ordering_validate` when the
requested output is a ranking.

Construct a compact causal model of the experiment before transferring an
observed outcome between biologically related perturbations: intervention ->
direct molecular consequence -> propagation through complexes, pathways, or
programs -> exposure and selection -> sampling or survivorship -> measured
endpoint. Interpret each evidence item at the stage where it occurs. For each
candidate inspected from a bounded nomination, predict whether the same
intervention is expected to move the requested endpoint in the same direction,
the opposite direction, or an indeterminate direction. An obligate complex or established
directional dependency is a same-outcome prior when both perturbations impair
the same limiting function in the relevant context and time window; broad
pathway co-membership alone is not. Downgrade transfer only for a candidate-
specific reason such as opposite causal sign, redundancy or bypass,
compensatory feedback, absent context or exposure, ineffective perturbation,
timing mismatch, or documented endpoint divergence. A downstream readout
measured only in survivors cannot by itself falsify an earlier selection
effect. Use this causal transfer analysis as bounded endpoint evidence, never
as an unqualified graph or pathway score.

An established causal dependency that satisfies that chain is endpoint-bearing
transfer evidence even when the source did not measure the identical endpoint.
Different tissue, cell type, or model is a confidence qualifier, not by itself
a causal break: if declining transfer, identify the candidate-specific link in
the chain expected to fail. Conditional or synthetic-only evidence is not a
same-outcome transfer unless the requested experiment contains the required
second condition. Generic pathway membership, semantic similarity, and an
unsupported plausible story remain insufficient.

Use same-experiment relational structure to nominate challenges to the
quantitative basis. Do not use the broad `corpus.relational_candidates`
operation or narrative `corpus.findings` access for predictive
rankings. Candidate Finding summaries are not adjudication evidence in this
route.

When the requested endpoint is absent from the declared inputs and
`corpus.predictive_graph_review` is available, invoke its bounded `nominate`
operation once after quantitative calibration. Pass the run-local task bindings
and calibration artifacts plus the requested `top-k`; do not hand-select seeds,
the candidate universe, or retrieval limits. The operation uses the directed
relation where a visible seed's Finding names the candidate, emits every
candidate in each retained multiplicity tier without splitting the boundary
tier, and marks each nominee's quantitative rank and whether it overlaps the
quantitative top-k. Distinct-visible-seed comparator multiplicity selects only
the review pool. Read the complete alphabetically serialized nomination, which
contains candidate identities, multiplicity, visible anchors, and quantitative
overlap metadata but no Finding text.

Treat the quantitative top-k plus graph-only challengers as the adjudication
union. Explicitly inspect every `graph_only_challenger` and record a short
disposition rationale even when evidence is insufficient. The anchors,
multiplicity count, tier, pool membership, and row order are not endpoint
evidence and must not order the answer. Set `evidence_read=true` only when
independently resolved candidate-specific endpoint evidence, rather than legacy
Finding summaries, entered the decision.

For an absent endpoint, the canonical quantitative order is a proxy baseline,
not a protected prefix. Review may consider graph-nominated candidates from
anywhere in the declared universe and may change membership or positions
anywhere in the requested top-k, but only candidate-specific endpoint-bearing
evidence can justify a change. Generic relation presence or multiplicity alone
is insufficient. Every changed rank still requires an exact override record
with the promoted and displaced candidates, evidence source, endpoint
relationship, and reason; run `synthesis.ordering_validate` with those records.
After freezing the answer, invoke predictive graph-review `finalize` so the run
records nominated, inspected, evidence-read, retained-quantitative, promoted,
rejected, and not-reviewed candidates.

When the endpoint is directly observed or a validated proxy is established,
keep a quantitative core and use at most the lowest
`min(5, ceil(0.1 * k))` positions as a causal review band. Use the emitted
residual anchors with `corpus.direct_evidence` for strongly underpredicted
supplied examples or genuine boundary candidates. Pass `--calibration` so the
tool derives both anchors and the canonical candidate universe; do not hand-set
retrieval limits. Read its compact, host-capped summary index first. It contains
only identity, pairing precision, and one causal summary; preassigned evidence
status, confidence, limitations, and citations are not decision inputs. Request
compact experimental qualifiers for a material `record_id` only when missing
context could change the decision. Exact comparison pairs are presented first
for attention, not as a score.

Promote a candidate into this smaller band only when out-of-fold residuals show
the quantitative proxy underpredicts a relevant supplied anchor,
candidate-specific evidence establishes an obligate or directional link to the
same limiting function, the experimental chain predicts the endpoint in the
same direction, and no candidate-specific divergence mechanism is supported.
Preserve canonical order outside the band and among non-promoted candidates;
record each exact promotion and displacement for validation. If declining a
strong transfer candidate in either endpoint regime, state the
candidate-specific causal break rather than citing context difference alone.

External retrieval is optional and bounded to an explicit definition, missing
prior, conflict, boundary decision, or falsification need. Keep source roles and
uncertainty explicit.
