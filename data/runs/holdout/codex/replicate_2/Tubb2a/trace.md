# Direct DEG-count forecast for Tubb2a

## Target and endpoint

- Target: `Tubb2a`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Prediction: `1`

## Evidence used

### Outcome-blind target biology

I used the declared `Tubb2a` biology bundle only in its biology view. It reports that `Tubb2a` is strongly observed in the exact focal population: 22,847 of 23,679 non-target nuclei express it, 96.486% of nuclei, with mean CP10K 3.600 and mean raw UMI 5.93. This makes lack of target expression an unlikely explanation for a null result.

The same bundle adjudicates the functional stock as likely substantially depleted by P37-P44 because a disruptive edit stops new TUBB2A supply and most fast or approximately 15-day slow tubulin pools should turn over over the 21-28 day experimental interval. The operation is still buffered: TUBB2A is one beta-tubulin isotype in alpha/beta dimers and in microtubule lattice, existing lattice is not directly disabled at editing, and `Tubb2b` is an extremely close paralog with no thalamic compensation test. Germline mouse `Tubb2a` deletion was compatible with postnatal survival and caused only subtle developmental cortical phenotypes, so the prior points to a realized but probably buffered perturbation rather than a broad acute transcriptional collapse.

### Training DEG counts

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table has 1,674 training targets and does not include `Tubb2a`. Its distribution is highly concentrated at zero or very small values in this class:

- 1,205 / 1,674 targets have `n_degs = 0`.
- The median is 0.
- The 75th percentile is 1.
- The 90th percentile is 2.
- Only 43 / 1,674 targets have at least 100 DEGs.

The measured training tubulin subunits are all near-null:

| target | n_degs |
| --- | ---: |
| `Tubb4b` | 1 |
| `Tubb5` | 1 |
| `Tuba4a` | 2 |
| `Tuba1a` | 7 |

Nearby microtubule or microtubule-transport perturbations in the same table were also small except for `Dctn1`: `Map1b = 1`, `Mapt = 1`, `Stmn2 = 1`, `Kif1a = 1`, `Kif5a = 1`, while `Dctn1 = 75`.

### Training expression-profile checks

I projected the ten-node tubulin/MAP/transport cohort from `training_de_all_cell_groups.parquet` in the same `151 TH Prkcd Grin2c Glut` context using signed Wilcoxon scores and `pvals_adj < 0.05`. The four tubulin subunit perturbations had 17,259 measured genes each and only 1, 1, 2, or 7 significant features, matching the count table.

The exact significant profile rows showed:

- `Tubb4b`: only `Tubb4b` down, 1 DEG.
- `Tubb5`: only `Tubb5` down, 1 DEG.
- `Tuba4a`: `Tuba4a` down plus `Mast1` up, 2 DEGs.
- `Tuba1a`: `Tuba1a` down plus six up-regulated tubulin-family genes, 7 DEGs.

`Tuba1a` is therefore the high member of this small family because it triggers a clear compensatory tubulin-transcript program, including `Tubb2a` itself. The beta-tubulin perturbations represented in training, `Tubb4b` and `Tubb5`, did not show that program at FDR 0.05 and each counted only the self transcript.

## Synthesis

`Tubb2a` has high focal expression and enough post-edit time for depletion of renewable TUBB2A protein, so I did not set the forecast to a pure biological null. The closest measured beta-tubulin perturbations, however, produced self-transcript-only signatures, and the external mouse evidence says that single `Tubb2a` loss is compatible with survival and plausibly buffered by nearly identical `Tubb2b` and other beta-isotypes. I therefore treated `Tubb2a` as most likely to resemble `Tubb4b`/`Tubb5` rather than the broader-stress tail of the training distribution or the `Tuba1a` alpha-tubulin compensation case.

The resulting point estimate is one FDR-significant measured gene: probably the direct `Tubb2a` transcript itself, with little expectation of additional downstream genes crossing BH 0.05 in this focal population.
