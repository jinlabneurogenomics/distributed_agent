# Direct n_degs forecast for Eef1a2

## Target and endpoint

- Target manifest: `Eef1a2`.
- Requested endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, the count of measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05`.
- Same-experiment Parquet rows and corpus reports are different representations of one Perturb-seq experiment, not independent validation.
- I used the declared Eef1a2 biology bundle and training measurements only. I did not query the Eef1a2 held-out differential-expression rows, report, or DEG count.

## Eef1a2 biology bearing

The declared canonical Eef1a2 bundle supports a real lesion in the assayed window:

- Exact focal-population reach is high: Eef1a2 was detected in 23,620 of 23,679 non-target nuclei in `151 TH Prkcd Grin2c Glut` with `mean_raw_umi = 13.98` and `mean_log1p_cp10k = 2.19`.
- EEF1A2 is the mature neuronal eEF1A isoform and delivers aminoacyl-tRNA during cytoplasmic translation elongation.
- The bundle adjudicates pre-edit stock as likely substantially depleted by the P37-P44 harvest because a P16 edit stops new EEF1A2 supply, the 21-28 day interval spans several heterologous 95-hour half-lives, and mouse neurons normally switch from EEF1A1 to EEF1A2 near this postnatal period.
- Wasted Eef1a2-null mice develop a severe postnatal neurological syndrome, but the most direct mouse phenotype is motor-neuron heavy and germline; this raises the prior above a generic quiet perturbation without proving a broad thalamic survivor-state mRNA response.

## Training-count bearing

The focal training count table has 1,674 perturbations. It is zero-inflated in this cell class:

- 1,205 / 1,674 have `n_degs = 0`.
- Median = 0.
- 75th percentile = 1.
- 90th percentile = 2.
- 95th percentile = 18.
- 106 / 1,674 exceed 9 DEGs.

The closest represented cytosolic translation perturbations were low to low-moderate in the same focal class:

| training perturbation | focal n_degs |
| --- | ---: |
| Aimp1 | 0 |
| Eif5a | 0 |
| Eif4g1 | 1 |
| Eif4h | 1 |
| Eif4a2 | 2 |
| Eef2 | 9 |

Direct focal Parquet inspection of these perturbations showed that `Eef2`, the other core elongation-factor target in this small set, had nine BH<0.05 genes in `151 TH Prkcd Grin2c Glut`: `Ranbp2`, `Ufd1`, `Mul1`, `Prkcsh`, `Khdc4`, `Fbxo9`, `Atl1`, `Chd8`, and `Tnfrsf12a`. `Eif4a2` had `Eif4a2` and `Cadm4`; `Eif4g1` had only `Eif4g1`; `Eif4h` had only `Hexim1`; `Aimp1`, `Eif5a`, `Eif2ak4`, `Fars2`, `Gfm2`, and `Lars2` had no BH<0.05 rows in the focal class.

The same-experiment Findings ledger agrees with this narrow translation-factor bearing: `Aimp1` and the eIF perturbations did not activate broad ISR/UPR/proteostasis programs, and `Eef2` was explicitly interpreted as broad in selected other neuronal classes but only focal or absent elsewhere.

## Synthesis

I set the forecast slightly above the direct `Eef2` focal footprint but below the 95th percentile of the full focal training table.

The upward adjustment from the 0-2 eIF/Aimp1 group comes from Eef1a2's strong focal expression, mature-neuronal isoform role, weak expected Eef1a1 buffering after the switch, and stock depletion by harvest. The ceiling comes from two experiment-local constraints: core translation-factor perturbations mostly failed to create a broad focal transcriptional stress program in recovered nuclei, and a severe translation lesion can be attenuated in single-nucleus DE by mosaic editing, long-lived pre-edit protein, and survivor conditioning.

Point forecast: `12` BH<0.05 genes.
