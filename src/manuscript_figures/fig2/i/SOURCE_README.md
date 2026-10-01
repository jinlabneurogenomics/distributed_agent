# Final three-arm literature-flag distribution

This directory applies the completed two-layer gold-set rubric to the same 150
underlying response genes in three report arms:

- unshuffled reports generated on 260713;
- within-screen target-label shuffles generated on 260730;
- out-of-screen target-label shuffles generated on 260730.

The grader is blind to arm, generation, prior flags, and the response gene
underlying a shuffled displayed target. Each call contains three complete gene
reports using a Latin shift; a gene report is never split.

Run from the repository root:

```bash
python manuscript/fig2/_debug/260731/final_three_arm_distribution/finalize_distribution.py prepare
python manuscript/fig2/_debug/260731/final_three_arm_distribution/finalize_distribution.py run-calibration
python manuscript/fig2/_debug/260731/final_three_arm_distribution/finalize_distribution.py calibrate
python manuscript/fig2/_debug/260731/final_three_arm_distribution/finalize_distribution.py run-full
python manuscript/fig2/_debug/260731/final_three_arm_distribution/finalize_distribution.py summarize
```

## Responses API runner

`responses_api_runner.py` is a resumable Responses API alternative to the
isolated `codex exec` production runner. It loads `OPENAI_API_KEY` from the
repository `.env` and writes to `responses_api_runs/<run-name>/`; it never
overwrites the completed three-arm outputs.

Run one no-web, low-reasoning calibration packet:

```bash
python manuscript/fig2/_debug/260731/final_three_arm_distribution/responses_api_runner.py \
  --run-name smoke_full_noweb_low \
  --reasoning-effort low \
  --packet-id P009
```

Run every packet overlapping the finalized gold set with bounded concurrency:

```bash
python manuscript/fig2/_debug/260731/final_three_arm_distribution/responses_api_runner.py \
  --run-name gold_full_noweb_low \
  --reasoning-effort low \
  --workers 16 \
  --background \
  --calibration-only
```

Web search is disabled by default. Add `--web-search` only for an explicit
retrieval-enabled ablation or escalation pass. The runner fails immediately on
exhausted billing quota and retries only temporary throttling or connection
errors.

After a calibration run completes, compare it with the finalized gold rows:

```bash
python manuscript/fig2/_debug/260731/final_three_arm_distribution/evaluate_responses_api_run.py \
  gold_full_noweb_low
```

The primary analysis retains only `load_bearing` findings. The declared
sensitivity analysis adds `evidence_only`. Both exclude `over_eager` and
`uninterpretable_or_underpowered` findings. The four plotted flags are derived
mechanically from the literature relationship: Agree, Disagree, Inferred, and
No Literature.

Every final distribution is exported overall and by the underlying response
gene's local target × cell-type DEG count (FDR < 0.1): strong ≥100, moderate
25–99, low 1–24, and zero.

The unshuffled/shuffle report-generation mismatch is an explicit limitation;
the grading prompt and model are matched across arms.

## Completed result

The final run classified 2,610 source findings from 450 whole reports. The
primary analysis retained 1,649 load-bearing findings:

| Arm | n | Agree | Disagree | Inferred | No Literature |
|---|---:|---:|---:|---:|---:|
| Unshuffled | 488 | 29.3% | 2.3% | 38.5% | 29.9% |
| Within-screen shuffled | 600 | 13.2% | 7.7% | 35.7% | 43.5% |
| Out-of-screen shuffled | 561 | 6.1% | 2.5% | 30.5% | 61.0% |

The sensitivity analysis retained 1,958 findings with an evaluable literature
relationship after adding evidence-only rows. Two evidence-only bookkeeping
rows had `source_relation=not_evaluable` and therefore do not enter a four-flag
distribution.

Production grading agreed with 80.4% of the 148 finalized gold flags represented
in this matched corpus and with 85.1% of gold primary-retention decisions. The
four remaining gold rows concern genes outside the matched 150-gene set.

Primary and sensitivity figures are available as native-vector PDF/SVG and PNG:

- `final_flag_distribution_primary.*`
- `final_flag_distribution_by_celltype_signal_primary.*`
- `final_flag_distribution_sensitivity.*`
- `final_flag_distribution_by_celltype_signal_sensitivity.*`

## Figure 2 panel version

`final_flag_distribution_*` is a wide *horizontal* stacked bar. Rotating that
whole panel 90 degrees to fit the Figure 2 middle column left every label
sideways, so the column slot uses a dedicated vertical replot instead:

```bash
python manuscript/fig2/_debug/260731/final_three_arm_distribution/plot_three_arm_panel.py
```

`plot_three_arm_panel.py` reads the finished `final_overall_distribution.csv`
and writes `fig_three_arm_flags_vertical_{primary,sensitivity}.{png,svg,pdf}`.
It re-runs in a second, needs no model calls, and never overwrites the pipeline
figures. Native vertical bars, horizontal value labels, arm names at 45 degrees,
leader labels for slices under 9% (they cannot hold text inside), `n` above each
bar, and a two-column legend. Sized 2.15 x 2.65 in for a ~2 in column at 183 mm
figure width; `ARM_DISPLAY` at the top of the script holds the shortened tick
labels and `FIG_W`/`FIG_H` the panel geometry.

Known accessibility caveat in the shared Figure 2 flag palette: Agree `#6fc46f`
and Disagree `#ec835a` are adjacent in the stack but separate by only ΔE 3.1
under deuteranopia (OKLab x100), i.e. one merged blob for red-green colourblind
readers. Deepening Disagree to Okabe-Ito vermillion `#d55e00` raises the worst
adjacent CVD pair to ΔE 12.4 and is nearly invisible to normal vision, but the
same four hexes are hard-coded in 16 fig2 scripts, so it must be changed
figure-wide or not at all.

The preferred signal-stratified primary figure is
`final_flag_distribution_by_finding_max_signal_primary.*`. It counts each
load-bearing finding once and assigns its stratum from the maximum DEG count
among its listed cell types. Sixteen unshuffled findings lacking any cell-type
assignment are reported separately and excluded from that stratified figure.
The older `by_celltype_signal` figures remain coverage-weighted placement
diagnostics rather than finding-level estimates.

## Worked flag examples

`flag_examples/` holds one card per (arm × flag) cell across all three arms — twelve
fact-checked examples in the `fig2/g/deepdive` idiom (dataset side, verified citation, the rubric
relation that produced the flag, and a volcano of the surface the finding was actually written
against). Several are deliberately controlled rather than representative: the *same* Ctcf clustered
protocadherin collapse appears under three labels in three arms — `Ctcf` (Agree), `Mef2c`
(No Literature) and `Abhd10` (No Literature) — with every label a real, published gene, so what
changes is bridge specificity rather than label obscurity. The `Dync1h1` Inferred / `Chp1`
No-Literature pair is the same observed sterol program with and without a mechanistic bridge.
`flag_examples/FACTCHECK.md` records every check, including two findings whose quoted totals do not
reproduce and the corpus-wide observation that most Disagree rows are expected-program *absences*
rather than signed contradictions.

The per-finding classifications, per-placement local-signal data, and aggregated
tables are in `final_classified_findings.csv`,
`final_celltype_signal_placements.csv`, `final_overall_distribution.csv`, and
`final_local_signal_distribution.csv`.

## Gene-shuffle and finding workbook

`build_three_arm_gene_table.py` writes
`manuscript/tables/three_arm_gene_shuffle_findings_flags.xlsx`. The workbook
contains the 150-row original/within-screen/out-of-screen label map, the full
150 gene x 23 cell-type measured DEG-count matrix at padj < 0.1, the exact
1,649 primary findings and flags plotted in
`fig_three_arm_flags_vertical_primary.pdf`, and normalized supporting
references. Within-screen replacements are a permutation of the same 150
measured genes. Out-of-screen replacements are external labels and are marked
unmeasured rather than assigned zero DEGs.

The gene-level across-cell-type DEG totals are sums of target-by-cell-type DEG
calls, not unique-transcript counts; a transcript significant in multiple cell
types can contribute more than once.

## Biological-inference composition

`plot_three_arm_finding_scope.py` provides the companion vertical stacked bars
for finding composition. It uses the blinded grader's normalized `claim_scope`,
not the heterogeneous source `finding_type` column: unshuffled reports use the
legacy narrative vocabulary, whereas the two shuffle arms use V4 `claim_kind`.
The script writes `final_finding_scope_distribution.csv` plus
`fig_three_arm_finding_scope_vertical_{primary,sensitivity}.{png,svg,pdf}`.
The primary plot contains load-bearing findings; the sensitivity plot adds
evidence-only findings. Reader-facing labels are Pathway or state change,
Perturbation convergence/divergence, Prior-prediction outcome,
Cell-group-dependent response, and Other; the underlying `claim_scope` values
remain unchanged.

Finding-level maximum-signal assignments and positive target×cell-type coverage
audits are in `final_finding_max_signal_assignments_primary.csv`,
`final_flag_distribution_by_finding_max_signal_primary.csv`,
`final_positive_pair_flag_coverage_primary.csv`, and
`final_positive_pair_coverage_summary_primary.csv`.

For the unshuffled arm, `final_unshuffled_positive_pair_coverage_vs_deg_primary.*`
plots positive target×cell-type pair counts and coverage rates across DEG bins,
including whether a pair receives one or multiple distinct literature flags.
The corresponding exact table is
`final_unshuffled_positive_pair_coverage_by_deg_primary.csv`.
