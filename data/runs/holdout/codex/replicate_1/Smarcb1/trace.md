# Smarcb1 DEG-count forecast

## Target and endpoint

- Target: `Smarcb1`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with Wilcoxon `pvals_adj < 0.05` in that focal population.
- Declared target-outcome status: the `Smarcb1` focal DE signature and DEG count were not used or reconstructed.

## Biological target evidence

The declared `Smarcb1` biology bundle supplies the relevant target-state prior. In the exact focal non-target population, `Smarcb1` is detected in 15,357 of 23,679 nuclei, 64.85%, with mean raw UMI 1.151 and mean CP10K 0.718. This makes target presence in the assayed thalamic neurons plausible rather than a major dilution concern, while still leaving ordinary mosaic-editing and survivor-conditioning uncertainty.

The same bundle identifies SMARCB1/BAF47 as a renewable core member of mammalian mSWI/SNF chromatin-remodeling complexes. It adjudicates the P16 to P37-P44 window as likely long enough to substantially deplete new SMARCB1-containing functional stock, with partial evidence because no SMARCB1-specific half-life in juvenile postmitotic thalamic neurons was found. The card also found no close same-position mammalian paralog, which makes a complete null less likely than for duplicated family positions such as `Smarcc1`/`Smarcc2` or `Smarca2`/`Smarca4`.

The downward caveats are material: the direct mouse neural loss evidence is developmental and cerebellar rather than P16 postmitotic thalamus, residual SMARCB1-deficient complexes can persist, and recovered single nuclei would miss any pre-harvest depletion. I therefore treated the bundle as support for a real BAF-axis response, not for a maximum-size response.

## Training measurements

The declared focal count table contains 1,674 labeled training perturbations. Its count distribution is sparse: 1,205/1,674 targets have 0 DEGs, the median is 0, the 90th percentile is 2, the 95th percentile is 18, the 98th percentile is 150, and the maximum is 2,677. A nonzero chromatin-remodeler forecast is therefore already in the upper tail.

I used deterministic Reactome/GO/CORUM mSWI/SNF membership to choose observed BAF-related training perturbations and then read their focal measurements from the count table and Parquet. The closest observed set gave:

| training target | focal n_degs |
|---|---:|
| `Smarcc2` | 185 |
| `Arid2` | 56 |
| `Arid1a` | 22 |
| `Smarce1` | 11 |
| `Actg1` | 1 |
| `Arid1b` | 1 |
| `Smarca2` | 1 |
| `Smarcd1` | 1 |
| `Bcl11a` | 0 |
| `Bcl11b` | 0 |
| `Bicra` | 0 |
| `Smarca4` | 0 |
| `Smarcc1` | 0 |

Direct focal Parquet inspection recapitulated those counts with matched perturbed nuclei ranging from 146 to 316 in this cohort. The active BAF members were mixed rather than one-sided: `Smarcc2` had 71 up and 114 down significant genes; `Arid2`, 30 up and 26 down; `Arid1a`, 7 up and 15 down; `Smarce1`, 0 up and 11 down. Same-experiment corpus Claim `claim:845db620c0afdfc1b86a` summarizes the corresponding observed result as a subunit-selective BAF/mSWI/SNF module in `151 TH Prkcd Grin2c Glut`: `Smarcc2`, `Smarce1`, and `Arid1a` converge most clearly, `Arid2` participates partially, and several represented relatives are weak, flat, or divergent rather than interchangeable phenocopies.

## Synthesis

`Smarcb1` is more compelling than most null BAF-family training targets because it is a broadly detected, non-paralogous core subunit whose functional stock should decline over the 21 to 28 day interval. I therefore forecast above the all-training median and above the single-self-hit `Smarca2`/`Arid1b`/`Smarcd1` group.

I did not use `Smarcc2 = 185` as the direct point because the represented BAF module is explicitly subunit selective: `Smarcc1`, `Smarca4`, `Smarca2`, `Bicra`, `Bcl11a`, and `Bcl11b` are null in the same table, and `Arid2` and `Arid1a` have smaller, partially distinct signatures. The best biological placement for `Smarcb1` is a realized, core cBAF/PBAF lesion with no same-position paralog, but with no matched mature-thalamic phenotype and possible residual complex buffering. I placed it near the upper end of the active BAF middle, below the `Smarcc2` outlier and close to but slightly below `Arid2`.

Predicted `n_degs`: 48.
