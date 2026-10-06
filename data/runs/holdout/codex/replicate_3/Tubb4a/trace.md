## Prediction

Target: `Tubb4a` in `151 TH Prkcd Grin2c Glut`

Predicted `n_degs`: **1**

## Evidence

### Declared target biology

- The one-row holdout manifest names `Tubb4a`, matching the declared biology bundle `biology_bundles/Tubb4a.json` with bundle SHA-256 `2c56cc8e70e72077c2f23f12c3ebd1b6769718f566bd0cbd0dd1429414ced93f`.
- In the exact focal population, `Tubb4a` is a robustly observed transcript: 22,311 of 23,679 non-target nuclei express it, with mean raw UMI 5.06, mean CP10k 2.98, and pseudobulk CPM 317.27. The feature is therefore measurable in the assay, but this reach measurement is not the held-out perturbation result.
- The biology card calls TUBB4A a beta-tubulin structural subunit of alpha/beta heterodimers in mixed-isotype microtubules. A P16 disruptive edit should stop new TUBB4A supply, while pre-existing protein and polymerized microtubules are not directly disabled.
- The functional-stock adjudication concluded `functional_stock_by_harvest = likely_persists`: total brain tubulin turns over over days to weeks, so some renewal should occur in the P16 to P37-P44 interval, but Tubb4a-null mouse neural tissue maintains total beta-tubulin by cell-type-specific induction of other beta-tubulins and lacks a detected baseline neural phenotype through one year. That makes broad acute transcriptional injury less likely than a buffered or self-limited response, with uncertainty because the compensation evidence is germline and not a direct acute thalamic-neuron test.

### Declared training count table

The declared focal training count table was
`Inputs/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
It contains 1,674 non-held-out training targets. Its burden distribution is highly sparse:

- 1,205 / 1,674 targets have `n_degs = 0`.
- 276 have `n_degs = 1`.
- 31 have `n_degs = 2`.
- 1,512 / 1,674 have at most two DE genes.
- The median is 0 and the 75th percentile is 1.

Measured cytoskeletal/tubulin-neighborhood training perturbations in the same focal count table were:

| target | n_degs |
|---|---:|
| Tubb4b | 1 |
| Tubb5 | 1 |
| Tuba4a | 2 |
| Tuba1a | 7 |
| Dctn1 | 75 |
| Map1b | 1 |
| Map6 | 0 |
| Mapre2 | 1 |
| Mapt | 1 |
| Stmn2 | 1 |
| Kif1a | 1 |
| Kif1b | 0 |
| Kif2a | 0 |
| Kif3b | 0 |
| Kif5a | 1 |
| Kif5c | 1 |
| Kif11 | 0 |
| Kif21a | 1 |
| Kifbp | 2 |
| Dync2h1 | 0 |

This table places the directly measured beta-tubulin perturbations at one significant gene, not at a broad stress or cytoskeletal-remodeling burden.

### Matched expression profiles

The declared training Parquet was queried only for training targets in the focal `151 TH Prkcd Grin2c Glut` group. A symmetric 20-node microtubule cohort profile comparison over `scores` and `pvals_adj < 0.05` wrote:

- `workbench/microtubule_profile_compare.json`
- `workbench/microtubule_profile_cohort.json`
- `workbench/key_tubulin_profile_inspect.json`

The focal Parquet profiles confirm what the count table implies:

- `Tubb4b` has exactly one significant feature in this class, the negative self row `Tubb4b`.
- `Tubb5` has exactly one significant feature in this class, the negative self row `Tubb5`.
- `Tuba4a` has two significant features: negative self `Tuba4a` and positive `Mast1`.
- `Tuba1a` has seven significant features: negative self `Tuba1a` and six positive alpha/beta-tubulin transcripts, including `Tubb4a`, `Tubb4b`, and `Tubb5`.
- `Dctn1` is the broad outlier with 75 significant features and a sterol/lipid signature headed by `Insig1`, `Msmo1`, `Hmgcs1`, `Cyp51`, and `Hmgcr`.

The 20-node cohort was not a coherent shared profile module. Across all 190 supplied cytoskeletal pairs, the median same-tail overlap coefficient was 0.025 to 0.030, and significant-feature overlaps were zero in every same-sign intersection. That argues against transferring the Dctn1 program or the Tuba1a tubulin-feedback program wholesale to every tubulin-family perturbation.

### Same-experiment corpus

The selected same-experiment corpus had no `Tubb4a` target report, so it did not expose a held-out Tubb4a expression profile. It did contain bottom-up interpretations for the measured analogs:

- `Tubb4b:F001-F003` describe Tubb4b as transcriptomically buffered in the recovered neurons and explicitly note that Tubb4b loss did not induce the alpha/beta-tubulin replacement program visible after `Tuba1a`.
- `Tubb5:F002-F004` describe Tubb5 self-mRNA decrease as uncoupled from a stable nuclear RNA program and contrast flat Tubb5/Tubb4b beta-tubulin responses with the Tuba1a paralog feedback module.
- `Tuba4a:F001-F005` describe an almost-null alpha-tubulin response, with only the focal `Mast1` singleton outside self and no broad Dctn1-like or Tuba1a-like cascade.
- `Tuba1a:F001-F004` establish the main counterexample: the assay can see a restricted tubulin-isotype compensation program in Pvalb and 151 thalamic neurons, but that response is not a generic result of perturbing every measured tubulin transcript.

## Synthesis

`Tubb4a` is highly expressed in the target class, so a self transcript decrease is plausible enough to include one DEG. The biology bundle, however, points away from a large non-self response: TUBB4A is one member of a replaceable beta-tubulin pool, existing microtubules persist, and germline null neural tissue preserves total beta-tubulin by other isotypes.

Among declared training perturbations, the closest beta-tubulin analogs were `Tubb4b` and `Tubb5`, both with exactly one significant focal feature, their self row. `Tuba4a` is slightly more responsive but still only self plus one focal marker. `Tuba1a` is the mechanistic exception rather than the rule, and the profile comparison shows no shared cytoskeletal signature that would justify carrying its seven-DEG count to `Tubb4a`.

I therefore predict that the held-out Tubb4a contrast crosses the BH-adjusted threshold for the target transcript itself and little else:

`predicted_n_degs = 1`
