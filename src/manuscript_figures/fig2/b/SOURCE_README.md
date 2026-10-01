# Meaningful-biology two-corpus union

This directory contains the completed union sweep of the 260713 unshuffled
reports and the older unshuffled report corpus for every non-control target
with at least one DEG at FDR < 0.1. The conservative 1,071-finding rescue atlas
is the immutable current anchor.

For the complete stepwise lineage and materialized per-finding provenance, use
the stable [meaningful-biology pipeline](../../meaningful_biology_pipeline/README.md).
This dated directory remains the immutable execution record for the union step.

## Design

The workflow has two stages.

1. `run_union.py` reviews every older finding in a whole-gene dossier containing
   all older findings, all current findings, current primary anchors, and the
   target's local DEG profile. Each older row is assigned exactly one of:
   duplicate current primary, material extension, new primary, duplicate of a
   new primary, evidence only, or reject. This stage does not retrieve or
   regrade literature.
2. `review_union_literature.py` reopens the complete References JSONL ledgers
   only for new and materially extended claims. It assigns the strict
   target-to-effect relation used to derive Agree, Disagree, Inferred, or No
   Literature. Exact cell context and unmeasured non-RNA modalities are not
   literature gates.

Runs used `gpt-5.6-sol` with eight workers. Stage 1 used medium reasoning and
completed 180 packets in 3,908 seconds; Stage 2 used calibrated low reasoning
and completed 84 packets in 569 seconds. All 6,375 older findings and all 524
deduplicated citation-review units have valid exact coverage.

## Results

- Current conservative primary atlas: 1,071 findings.
- New older-derived primary findings: 448 non-control findings.
- Current findings materially extended by older evidence: 75 unique findings
  (76 source rows); extensions do not increase the finding count.
- Final union: 1,519 findings.
- One `Safe_target_65` tested-absence row was excluded from the final atlas.

Final literature flags, ordered along the literature axis (Agree, Disagree and
Inferred all rest on retrieved literature; No Literature does not):

- Agree: 420 (27.6%).
- Disagree: 101 (6.6%).
- Inferred: 636 (41.9%).
- No Literature: 362 (23.8%).
- Has literature (Agree + Disagree + Inferred): 1,157 (76.2%).

These counts include the explicit human adjudication of Sin3a F004 recorded in
`manual_literature_overrides.json`. That override narrows the flag scope to the
measured E2F-linked centriole/centrosome/cilium transcriptional program and
keeps it Inferred because the literature does not establish Multicilin-independent
activation of the selective E2F4/5 centriole arm after SIN3A loss. The override
stores the exact missing edge and full supporting references.
`review_union_literature.py finalize` reapplies it, so regenerating the review
table does not erase the adjudication.

New finding forms are 153 tested absences, 119 cross-perturbation
relationships, 63 coherent programs, 57 disease/allele refinements, 34
recurrent signed edges, 19 expected readouts, and 3 power-accounted cell-type
boundaries.

## Cell placement and heatmaps

The heatmap uses a stricter placement rule than the biological review. A
rescued claim colors a target×cell block only when that cell was explicitly
listed on the source finding. Cells inferred by the model from the surrounding
DEG profile are retained in `model_supported_cell_types_json` for audit but
removed from `supported_cell_types_json`. Zero-DEG placements are not plotted.

This raises non-null pair coverage from 1,340/4,174 (32.1%) in the current
anchor to 1,738/4,174 (41.6%) in the union, and target coverage from 358/1,092
to 509/1,092 non-control DEG-positive targets.

The requested updated signal heatmap is
`union_local_signal_heatmap_nonnull.{png,svg,pdf}`. A companion flag heatmap is
`union_flag_heatmap_nonnull.{png,svg,pdf}`.

## Maximal-coverage heatmaps over the whole ledger

`build_full_coverage_heatmaps.py` plots every adjudicated finding in both
corpora, not just the 1,519 primary claims: 10,898 rows (1,519 load-bearing,
679 cross-corpus duplicates, 4,684 evidence-only, 4,016 low-grade). Each
target×cell block takes the strongest tier that places a finding there, so the
figure is a quality gradient rather than a binary mask. Coverage rises from
1,738/4,174 blocks (41.6%) and 509 targets in the primary atlas to
**3,629/4,174 blocks (86.9%) across 1,090/1,092 targets**. Evidence-only rows do
nearly all of that work: they alone lift block coverage past 81% and target
coverage past 98%. Cross-corpus duplicates add only 38 blocks, because a
duplicate almost always lands where its primary already sits.

Placement rules differ by corpus and are not interchangeable. Older-corpus rows
use the same explicit-source rule as the union atlas. Current-corpus
non-primary rows have no audited placement, so they use the finding's own
reported `cell_types_json`, which is looser. Model-inferred older placements
remain excluded; adding them would gain only ~35 blocks.

Confidence is a per-claim model enum present on **all** rows in both corpora
(6,375/6,375 older, 4,727/4,727 current) and is independent of the
admissibility or disposition label — a `reject` row still carries a confidence.
It is uncalibrated: no pass defines high/moderate/low, and the meaning drifts
between passes. The current-corpus classification pass is 76% high
(3,029/3,623) and rates 1,692/1,921 `uninterpretable_or_underpowered` rows
high, which reads as confidence in the *verdict*; the union stage-1 and rescue
passes read as confidence in the *claim*. Consequently:

- `full_coverage_confidence_heatmap` colors the strongest row per block and
  saturates to High (2,467/3,629), partly encoding which pass adjudicated the
  block. Blocks whose only support is low-grade are drawn neutral rather than
  given a ramp step, since their confidence is verdict confidence.
- `full_coverage_confidence_heatmap_primary` restricts to the 1,738
  load-bearing blocks and is the interpretable version: 1,111 High, 618
  Moderate, 9 Low.

## Principal outputs

- `meaningful_primary_findings_union.csv`: final deduplicated primary atlas.
- `stage1_union_decisions.csv`: all 6,375 older-finding dispositions, including
  raw and explicit-source-filtered cell placements.
- `stage2_literature_reviews.csv`: citation-level relation and supporting-source
  audit for all new/extended units.
- `manual_literature_overrides.json`: reproducible human adjudications, scoped
  claim rewrites, and complete added reference records.
- `union_flag_distribution.{png,svg,pdf,csv}`: current versus union overall.
- `union_flag_distribution_by_local_signal.{png,svg,pdf,csv}`: current versus
  union by strong, moderate, low, zero, and unplaced local signal.
- `union_flag_distribution_by_local_signal_union_only.{png,svg,pdf,csv}`: the same
  strata with the Current layer dropped — union bars only, one per stratum, with
  the has/no-literature rule. Literature coverage is flat across strong (77.3%,
  n=466) and low (77.3%, n=634) signal but dips at moderate (64.3%, n=241).
- `union_local_signal_heatmap_nonnull.{png,svg,pdf}`: rescued finding coverage
  colored by local DEG stratum.
- `union_flag_heatmap_nonnull.{png,svg,pdf}`: the same placements colored by
  literature flag.
- `union_heatmap_cells.csv`: complete target×cell heatmap audit matrix.
- `union_flag_taxonomy.{png,svg,pdf,csv}`: aggregate flag distribution with the
  has/no-literature bracket (form of `manuscript/fig2/b/flag_taxonomy.svg`).
- `load_bearing_findings.csv` / `.md`: readable views of the 1,519 load-bearing
  primary claims, written by `list_load_bearing.py`. Both drop the reference
  blobs and order targets by DEG burden to match the heatmap column order; the
  markdown groups by target for reading, the CSV is flat for filtering.
- `results/bioeval/lit-agree-4flag/phenotype_findings_by_perturbation.csv` /
  `.md`: reader-facing views of
  5,142 findings, grouped alphabetically by perturbation and then by
  `phenotype_confidence`: all 1,519 canonical union findings are `high`, while
  `moderate` and `low` contain only July 13 corpus findings. Older-corpus
  moderate and low rows are excluded. The CSV columns are `perturbation`,
  `flag`, `phenotype_confidence`, `finding_summary`, `finding_consequence`,
  `literature_rationale`, `finding_type`, `cell_types`, and `source_id`.
  Finding types and consequences come from the original source finding; high
  summaries/flags come from the union, while moderate/low flags use the July 31
  four-flag regrade. `literature_rationale` is populated for the 1,519 high
  union rows and blank for moderate/low rows. The 17 rows without an assessable
  relation retain a blank `flag`. These files and
  `phenotype_findings_summary.json` are written by
  `organize_phenotype_findings.py`.
- `results/bioeval/lit-agree-4flag/phenotype_findings_by_perturbation_deg_ordered.csv`:
  the same rows and columns, with perturbations ordered by descending total DEG
  count (summed across cell types), alphabetical target name for ties, and
  high-to-low phenotype confidence within each perturbation.
- `full_coverage_tier_heatmap.{png,svg,pdf}`: whole-ledger target×class coverage
  colored by evidence tier.
- `full_coverage_confidence_heatmap.{png,svg,pdf}`: the same blocks colored by
  the strongest row's self-reported confidence.
- `full_coverage_confidence_heatmap_primary.{png,svg,pdf}`: confidence
  restricted to load-bearing primary blocks.
- `fig2_high_moderate_confidence_heatmap.{png,svg,pdf}`: cell-class ×
  perturbation coverage for the reader-facing high and moderate
  `phenotype_confidence` findings only, colored by the canonical literature
  flags. Each block takes the most decisive flag (Disagree, Agree, Inferred, No
  Literature, then Unassessed). Low findings and zero-DEG placements are
  excluded. Noncanonical aggregate cell labels are retained in the audit
  summary but are not expanded into inferred cell placements. Both exported
  forms use a square matrix, with uncovered blocks left white; the `__matrix`
  files are the standalone heatmap, while the unsuffixed files add DEG-burden
  and flag-mix marginals.
- `fig2_high_moderate_confidence_heatmap_cells.csv` and `_summary.json`:
  block-level audit matrix and aggregate counts for that heatmap.
- `fig2_high_moderate_confidence_heatmap_presentation.{png,svg,pdf}`: a
  projection-first variant that widens each exact heatmap mark by two adjacent
  targets on either side within the positive-DEG universe. Exact blocks retain
  their adjudicated flag, overlap uses the standard flag priority, and the
  right/top marginal statistics remain exact. The widening is display-only and
  must not be read as quantitative block coverage.
- `fig2_high_moderate_confidence_heatmap_three_densities.{png,svg,pdf}` and
  `fig2_high_moderate_confidence_heatmap_three_densities_presentation.{png,svg,pdf}`:
  new joint-plate variants whose top marginal overlays peak-normalized,
  Gaussian-smoothed densities across DEG-sorted perturbation rank for total DEG
  burden, load-bearing finding count, and evidence-only finding count.
  The smoothing bandwidth is 18 targets. The standard form retains exact
  heatmap cells; the presentation form uses the documented display-only ±2
  target widening.
- `fig2_literature_flag_tier_density_heatmap.{png,svg,pdf}` and its `__matrix`
  panel: the literature-flag heatmap plus peak-normalized, Gaussian-smoothed
  densities for DEG burden and all three reader-facing finding tiers:
  load-bearing, evidence-only, and non-admissible. All three tiers contribute
  literature flags to the heatmap, using the same block-level priority rule.
  The companion `_target_counts.csv` records the unsmoothed per-target inputs
  and `_summary.json` records the tier mapping, counts, bandwidth, and coverage.
- `fig2_literature_flag_tier_density_heatmap_all_mentions.{png,svg,pdf}` and its
  `__matrix` panel: the same all-tier flag and density display without requiring
  a positive local DEG for the matrix. Every explicit placement in one of the
  23 canonical cell classes is shown; unresolved aggregate labels remain
  excluded rather than being expanded by inference.
- `fig2_literature_flag_load_bearing_all_mentions.{png,svg,pdf}` and
  `fig2_literature_flag_load_bearing_evidence_only_all_mentions.{png,svg,pdf}`:
  no-local-DEG comparison plates restricted to load-bearing findings alone or
  load-bearing + evidence-only findings, respectively. Each has a standalone
  `__matrix` panel and summary JSON.
- `full_coverage_cells.csv`: per-block audit with best tier, confidence, corpus,
  adjudicating pass, and per-tier finding counts.
- `full_coverage_finding_tiers.csv`: finding-level tier × disposition × corpus ×
  confidence counts for all 10,898 plotted rows.
- `full_coverage_tier_by_cell_class.csv`: tier composition per cell class.
- `full_coverage_summary.json`: coverage and tier/confidence totals.
- `union_flag_by_pathway.{png,svg,pdf,csv}`: flag composition per target pathway
  family (form of `manuscript/fig2/c/figC_flag_dist_C_pathway`). Pathway families
  are reused verbatim from `manuscript/fig3/novelty_stats/target_pathway_category.csv`;
  the 7 findings whose target is absent from that table fall to `Other`. Every one
  of the 9 families clears the n≥20 floor. Literature coverage runs from Nuclear
  transport (90.5% has-literature, n=21) down to Chromatin/transcription/epigenetic
  (66.1%, n=218) and RNA splicing & processing (67.1%, n=161).

## Reproduction

```bash
python run_union.py prepare
python run_union.py run --workers 8 --model gpt-5.6-sol --reasoning-effort medium
python run_union.py finalize
python review_union_literature.py prepare
python review_union_literature.py run --workers 8 --model gpt-5.6-sol --reasoning-effort low
python review_union_literature.py finalize
MPLCONFIGDIR=/tmp/mplconfig_meaningful_union python finalize_union.py
MPLCONFIGDIR=/tmp/mplconfig_meaningful_union python build_flag_pathway_figs.py
MPLCONFIGDIR=/tmp/mplconfig_meaningful_union python build_full_coverage_heatmaps.py
python organize_phenotype_findings.py
MPLCONFIGDIR=/tmp/mplconfig_meaningful_union python build_high_moderate_confidence_heatmap.py
MPLCONFIGDIR=/tmp/mplconfig_meaningful_union python build_literature_flag_tier_density_heatmap.py
MPLCONFIGDIR=/tmp/mplconfig_meaningful_union python build_literature_flag_tier_density_heatmap_all_mentions.py
MPLCONFIGDIR=/tmp/mplconfig_meaningful_union python build_literature_flag_subset_all_mentions_heatmaps.py
```
