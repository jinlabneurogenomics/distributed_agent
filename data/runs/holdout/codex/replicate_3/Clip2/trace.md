# Trace

## Target and endpoint

- Target: `Clip2`, from the declared one-row `Clip2.csv` holdout manifest and the matching `Clip2.json` biology bundle.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Declared measurement sources used:
  - `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  - `[local file: training_de_all_cell_groups.parquet]`
  - `[local file: Clip2.json]`

## Clip2 prior from the declared biology bundle

The biology-only `Clip2` bundle reports broad in-assay focal expression, with
`Clip2` detected in 18,303 of 23,679 non-target 151-class nuclei
(`77.2963%` expressing; mean raw UMI `1.73597`; mean log1p CP10k `0.64207`).
The functional-stock card concluded `likely_substantially_depleted` by the
P37-P44 harvest because the edit starts at P16 and CLIP2 is a dynamic
microtubule/plus-end and dendritic-lamellar-body-associated protein pool, but
that conclusion was only partially evidenced because no CLIP2-specific
postnatal thalamic protein-turnover curve was available.

The same bundle put the observable transcriptional effect lower than the
functional reach. The best mouse neural loss evidence is germline/developmental
rather than acute P16 thalamic loss, phenotype latency after postnatal loss is
unreported, and the `Clip1`/CLIP-170 plus dynactin redistribution after CLIP2
loss is direct buffering evidence. This made a durable, broad 151-class nuclear
RNA response possible but not the default expectation.

## Training endpoint distribution

The declared 151-class count table is highly sparse: among 1,674 visible
training perturbations, 1,205 had `n_degs = 0`, the median was `0`, the 75th
percentile was `1`, the 90th percentile was `2`, and the 95th percentile was
`18`. Thus an uncalibrated biology prior over a cytoskeletal target should stay
near zero unless there is specific evidence for a recurrent high-response
state.

## CLIP2-related visible perturbations

I nominated training-available analogs for `Clip2` with the deterministic
gene-analog nominator using the 151-class count table as the explicit universe;
the result was written to `workbench/clip2_analogs.jsonl`. The nominator found
no exact paralog, complex mate, direct dependency, narrow-module analog, or
bidirectional corpus comparator for `Clip2` in the training set. Its leading
1328 candidates were all `broad_functional_fallback` annotations, headed by
microtubule plus-end and cytoplasmic-microtubule communities.

The exact curated CLIP2-overlapping GO groups were also low in the declared
counts:

- `microtubule plus-end binding` / `GO:0051010`: visible members `Dst = 0`,
  `Mapre2 = 1`; `Apc` and `Stim1` were not in the training count table.
- `cytoplasmic microtubule organization` / `GO:0031122`: `Camsap1 = 0`,
  `Dctn1 = 75`, `Dst = 0`, `Ift88 = 0`; `Chp1` and `Dync1h1` were absent.
- `microtubule plus-end` / `GO:0035371`: `Dctn1 = 75`, `Dst = 0`,
  `Mapre2 = 1`, `Tuba1a = 7`.
- `dendritic microtubule` / `GO:1901588`: `Drd4 = 0`, `Zfp804a = 0`.

`Dctn1` was the only high-count member of the close cytoskeletal nominations.
Its selected-corpus report instead identified a DCTN1-specific SREBF2-like
sterol/cholesterol feedback state (`Dctn1:F001`, `F006`, `F007`) and separated
that response from generic cytoskeletal or trafficking-neighborhood loss.
The exact plus-end neighbor reports pointed the other way: `Dst:F001-F003`
reported no robust downstream response and a flat cytolinker/plakin
neighborhood, while `Mapre2:F001-F003` reported a 151-class self-transcript
decrease with no non-self FDR response and no convergence with Dctn1,
Tuba1a, kinesin, MAP, or tubulin perturbations. These report, Claim, and
Finding records are same-experiment interpretations of the Parquet, not
independent replication.

## Matched profile check

I compared the top 45 deterministic analog nominees in the exact
`151 TH Prkcd Grin2c Glut` Parquet context with `pvals_adj < 0.05` as the
significance definition. The comparison, `workbench/microtubule_profile_compare.json`,
had no missing profiles. Its activity bins were:

- `24` of 45 candidates with no significant features.
- `20` of 45 with 1-9 significant features.
- `1` of 45 with at least 50 significant features.

Directly scanning the same 45 targets in the Parquet gave 776,655 measured
target-gene rows and 102 significant rows. `Dctn1` contributed 75 of them
with 49 up and 26 down; `Tuba1a` contributed 7, mostly a tubulin-paralog
compensation signature; `Tuba4a` contributed 2; every other significant member
was a singleton. `Dst`, `Camsap1`, `Ift88`, `Kif3b`, `Fmn2`, `Macf1`, `Kif1b`,
`Kif2a`, `Map6`, and `Nin` had zero significant 151-class rows.

The cohort diagnostic (`workbench/microtubule_profile_cohort.json`) found no
coherent significant FDR program: among all 990 candidate pairs, the significant
program-overlap coefficient was 0 whenever such an overlap was defined. The
profile similarities among the many null and self-only nodes were therefore
not evidence of a recurrent CLIP2-scale cytoskeletal response.

## Forecast

The high-count `Dctn1` and modest `Tuba1a` states are boundary cases rather
than scale donors for `Clip2`: they produce sterol or tubulin-isotype modules
not seen across the exact CLIP2 plus-end neighbors. The strongest endpoint-
matched evidence is the near-zero GO neighborhood, especially `Dst = 0`,
`Camsap1 = 0`, `Ift88 = 0`, and `Mapre2 = 1` with a self-only 151-class hit.

I therefore forecast a singleton FDR hit in 151 rather than a downstream module.
This point allows for the common self/singleton outcome among expressed,
functionally engaged microtubule-associated perturbations, while keeping the
expected non-self response at zero because acute postnatal `Clip2` loss has
developmental-context and CLIP1-compensation caveats.

Predicted `n_degs`: `1`.
