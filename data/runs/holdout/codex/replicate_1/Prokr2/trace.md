# Prokr2 n_degs forecast

## Prediction

`target_name`: `Prokr2`

`predicted_n_degs`: `0`

## Evidence used

- The one-row holdout manifest declares `Prokr2` as the sole target.
- The requested cell population is exactly `151 TH Prkcd Grin2c Glut`, an aggregated thalamic glutamatergic neuronal class.
- The endpoint is the count of measured genes with Wilcoxon BH-adjusted `p < 0.05` in that class.
- The prediction-safe `Prokr2` biology bundle reports `target_outcome_exposed=false` and gives exact non-target expression in the focal class: 188 of 23,679 nuclei express `Prokr2`, `pct_cells_expressing=0.7939524473161873`, `mean_raw_umi=0.009206469867815363`, `pseudobulk_cpm=0.5770021138948866`, and `mean_cp10k=0.006018538137168563`.
- The same bundle adjudicates Prokr2 as a ligand-responsive seven-transmembrane prokineticin GPCR whose new functional supply should stop after a disruptive edit. Substantial receptor-stock depletion by the P37-P44 harvest is favored because the receptor is a renewed trafficking pool, but the bundle also notes partial evidence: no matched postmitotic thalamic Prokr2 clearance time is known.
- The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 training perturbations. Its distribution is heavily zero-inflated: 1,205 targets have 0 DEGs, 1,481 have at most 1 DEG, the median is 0, the 90th percentile is 2, and only 103 targets have more than 10 DEGs.
- I checked the declared differential-expression Parquet for a focused GPCR/neuropeptide-receptor comparator set in the same focal class. Sixteen of the 20 queried receptor targets had 0 significant genes (`Avpr1a`, `Avpr1b`, `Cckar`, `Cckbr`, `Drd2`, `Grm5`, `Htr1a`, `Htr2c`, `Npy1r`, `Npy2r`, `Npy5r`, `Oprk1`, `Oprm1`, `Oxtr`, `Sstr5`, `Tacr3`); the remaining four were exactly 1 (`Gabbr1`, `Gabbr2`, `Grm1`, `Grm7`). This was measured directly from the Parquet with `group_name = '151 TH Prkcd Grin2c Glut'` and `pvals_adj < 0.05`.

## Reasoning

Functional perturbation of `Prokr2` is biologically plausible over the screen window: editing at P16 should block new GPCR production, and a trafficked membrane receptor is not expected to remain fully functional for 21-28 days without resupply. That supports a real molecular perturbation rather than a pure functional-stock null.

The limiting evidence is endpoint reach in the actual assayed aggregate. `Prokr2` is detected in less than 1% of non-target nuclei in `151 TH Prkcd Grin2c Glut`; even a response in the small expressing subpopulation would be diluted across the broad thalamic class tested by the Wilcoxon contrast. The qualitative adult-thalamus expression evidence is therefore superseded downward by the exact in-assay expression measurement.

Training measurements make a large footprint unlikely. Most perturbations in this high-yield class are still zero, and the closest measured operation class, loss of neuromodulatory or metabotropic receptors, is essentially silent: the focused Parquet check found a 0-1 DEG range for the selected receptor comparators rather than a moderate tail. `Prokr2` lacks evidence for a broad cell-intrinsic transcriptional program comparable to chromatin, proteostasis, or RNA-processing perturbations that dominate the high-count tail.

Balancing likely stock depletion against extremely sparse focal expression and near-zero receptor analogs, I place `Prokr2` at the floor of the observed receptor-like training range. The point forecast is therefore 0 DEGs, with one DEG as the nearest plausible alternative if a single low-level self or downstream transcript crossed FDR.
