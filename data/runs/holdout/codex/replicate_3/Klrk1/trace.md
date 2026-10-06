# Klrk1 `n_degs` forecast

Target: `Klrk1` in `151 TH Prkcd Grin2c Glut`.

Prediction: `0`

## Evidence used

- The declared manifest and biology bundle both identify the one held-out perturbation as `Klrk1`.
- The endpoint is the count of measured genes in the focal class with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- In the canonical biology bundle, exact non-target focal-population expression for `Klrk1` is essentially absent: 6 expressing nuclei among 23,679 non-target `151 TH Prkcd Grin2c Glut` nuclei, `pct_cells_expressing = 0.02533890789306981`, `mean_raw_umi = 0.0002533890789306981`, and `pseudobulk_cpm = 0.015880792125547338`.
- The same bundle adjudicates the operative lesion as loss of a dynamic NKG2D receptor-adaptor complex. This makes long persistence of pre-edit stock unlikely after a successful edit, but that fact only matters in cells with a functional receptor demand.
- The source-card phenotypes for `Klrk1` are immune-cell, tumor-surveillance, infection, or immune-mediated neuroinflammatory phenotypes. The bundle did not find a healthy thalamic neuron-autonomous requirement, and the exact focal expression supersedes qualitative expression uncertainty.
- The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table has 1,674 training perturbations; 1,205 have `n_degs = 0`. Its median is 0, 75th percentile is 1, and 90th percentile is 2, so a zero response is the empirical mode for this focal class.
- The count table contained no exact Klr-family or NKG2D-adaptor perturbation to transfer directly: `Klrc1`, `Klrc2`, `Klrc3`, `Klrd1`, `Klri1`, `Klri2`, `Hcst`, and `Tyrobp` were absent.
- Immune surface-receptor or lymphocyte-signaling perturbations that were present in the count table were quiet in this same endpoint: `Cd14`, `Cd247`, `Cd3d`, `Cd3e`, `Cd3g`, `Cd4`, `Cd40`, `Cd46`, `Cd79a`, `Cd79b`, and `Cd80` each had `n_degs = 0`.
- A direct Parquet check of those comparator perturbations in `151 TH Prkcd Grin2c Glut` found 17,259 measured rows per target and 0 rows with `pvals_adj < 0.05` for every one of the listed CD/TCR/BCR-surface targets.

## Synthesis

`Klrk1` should edit a renewable receptor rather than an irreversibly pre-installed product, so the loss-of-function is not blocked by the 21-28 day post-edit interval. The limiting factor is instead context reach: NKG2D is an immune activating receptor, the declared focal neuronal expression is only 6 UMIs across 23,679 matched non-target nuclei, and the curated phenotypes do not establish an acute healthy thalamic neuron-autonomous state. On the quantitative side, the training distribution in this class is mostly zero, and the observed immune receptor/signaling analogs in the same count table and Parquet rows are all exactly zero. With no exact measured adaptor analogue, I shrink to the focal-class mode and predict no BH-significant downstream genes.
