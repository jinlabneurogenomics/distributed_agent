# Med12 DEG-count forecast for `151 TH Prkcd Grin2c Glut`

## Target and endpoint

- Target: `Med12`, the only row of the declared holdout manifest
  `[local file: Med12.csv]`.
- Endpoint: `n_degs`, the number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- I used the declared focal count table
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  and the declared full-count Parquet
  `[local file: training_de_all_cell_groups.parquet]`.
  `Med12` was absent from the training count table.

## Target biology

The declared biology bundle
`[local file: Med12.json]`
places MED12 in the dissociable Mediator CDK8 kinase module, contacting
CDK8-cyclin C and MED13, and adjudicates the edited functional stock as
`likely_substantially_depleted` by the P37-P44 harvest. That argues against a
pure technical null: the P16 edit should have enough time to reduce supply of a
dynamic nuclear Mediator component.

The same bundle gives exact in-assay focal expression in non-target nuclei:
Med12 was detectable but not broad in this class, with mean CP10K 0.13897,
mean log1p(CP10K) 0.10133, 5215 total Med12 UMIs in 23,679 non-target nuclei,
and 4548/23,679 cells expressing the transcript, or 19.21%. I treated that as
permissive but lower-reach expression, not as a direct edit-efficiency estimate.

## Training measurements used

The focal count table contained 1,674 measured training targets with a skewed
burden:

- median `n_degs`: 0
- zero-DEG targets: 1205/1674
- 75th percentile: 1
- 90th percentile: 2
- 95th percentile: 18
- targets with at least 100 DEGs: 43/1674

The directly measured Mediator/CDK8 neighborhood was small:

| target | 151 TH BH<0.05 DEGs |
| --- | ---: |
| Cdk8 | 0 |
| Med13l | 1 |
| Med13 | 11 |
| Med23 | 13 |
| Med15 | 19 |

Full-Parquet inspection confirmed that the significant `Med13`, `Med15`, and
`Med23` features were mostly shared down-regulated thalamic neuronal genes.
The exact BH<0.05 overlaps included recurrent repression of `Prkcd`, `Grm1`,
`Pcp4`, `Plekhg1`, and `Atp2a2`; `Cdk8` had 0 significant genes and `Med13l`
had only `Grm1`. Matched focal perturbed-nucleus counts for these comparators
were 192 for `Cdk8`, 200 for `Med13l`, 154 for `Med13`, 160 for `Med23`, and
158 for `Med15`, all against 23,679 matched control nuclei, so their low
counts were not just tiny-cell-count artifacts.

The same-experiment corpus is another representation of these training
measurements, not independent replication. Its Mediator Findings nevertheless
helped interpret the raw counts: `Med13:F006`, `Med15:F004`, and `Med23:F003`
describe the same selective `Med13`/`Med15`/`Med23` down-regulated 151-thalamic
module, while `Cdk8:F003` and `Med15:F005` explicitly mark `Cdk8` and `Med13l`
as non-phenocopying boundaries. A run-local profile comparison over `Cdk8`,
`Med13`, `Med13l`, `Med15`, and `Med23`
(`workbench/mediator_profile_compare.json`,
`workbench/mediator_direct_profile_cohort.json`) likewise found stronger
negative-tail cohesion than positive-tail cohesion, with six significant
negative-program overlaps across the ten selected Mediator pairs.

## Forecast

I forecast a small but nonzero Med12 response. MED12 is biologically closer to
the `Med13` scaffold side of the kinase module than to the enzymatic `Cdk8`
null, and broad Mediator subunits in the same 151 population produced a
reproducible 11-19 gene down-state. However, the measured Mediator family also
showed non-interchangeability, the closest kinase-module boundary `Cdk8` was
flat, `Med13l` contributed only one gene, and Med12's exact expression reach in
the focal population was modest. Those points kept the estimate near the
direct Mediator counts rather than near high-burden transcriptional regulators
such as `Brd4` or `Sin3a`.

Point forecast: **12** BH<0.05 DEGs.
