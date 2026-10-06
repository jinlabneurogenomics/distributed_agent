# Ednrb direct n_degs forecast

## Target and endpoint

- Target manifest: `Ednrb`.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Prediction: `0`.

## Evidence used

1. **Declared Ednrb biology-only bundle**

   The canonical Ednrb bundle reports that EDNRB is a renewable endothelin GPCR and that receptor stock in successfully edited, ligand-responsive cells is plausibly depleted by the P37-P44 harvest after a P16 edit. That supports functional realization of an edit rather than a long-lived inert target.

   The same bundle also gives the exact focal assay reach in `151 TH Prkcd Grin2c Glut`: only 453 of 23,679 non-target nuclei expressed Ednrb, i.e. 1.913%, with mean log1p CP10k 0.0100 and pseudobulk CPM 1.355. The bundle explicitly supersedes bulk thalamus expression with this exact in-assay value. I treated this as strong evidence that any EDNRB-dependent cell-autonomous response would be highly diluted in the aggregated thalamic class.

2. **151 TH Prkcd Grin2c Glut training count table**

   The focal count table contains 1,674 training perturbations. It is zero-heavy: 1,205 training perturbations have `n_degs = 0`, 1,481 have `n_degs <= 1`, and 1,546 have `n_degs <= 5`; the median is 0 and the 75th percentile is 1.

   The closest available pathway analog, `Ednra`, has `n_degs = 0` in this same focal table. Other represented endothelin-downstream genes named in the Ednra same-experiment report were mostly flat in this class as well: `Mapk1 = 0`, `Plcb1 = 0`, `Prkca = 0`, `Calm2 = 0`, `Dlx6 = 0`, `Calm3 = 1`, and `Calm1 = 14`. The broader receptor-like set was also quiet: 51 of 61 GPCR or receptor-like training perturbations identified from the focal table had `n_degs = 0`; the remaining 10 had exactly one DEG.

3. **Declared expression Parquet**

   Direct Parquet aggregation in the focal group confirmed the count-table boundary around the closest analogs: `Ednra`, `Mapk1`, `Plcb1`, `Prkca`, `Calm2`, and `Dlx6` each had 17,259 measured genes and zero genes with `pvals_adj < 0.05`; `Ednra` in particular had minimum adjusted p-value 1.0 in this focal group.

   A profile-neighbor projection of `Ednra` against all 1,674 eligible training nodes in the same focal Parquet produced a broad, low-specificity neighborhood rather than a robust recurrent module. I used that only as a sanity check that the Ednra zero count was not hiding a strong near-threshold 151-class signature.

4. **Same-experiment corpus for the training analog**

   The Ednra report in the selected same-experiment corpus summarizes P16 Ednra loss as buffered across assayed postmitotic neuronal groups: 19 of 20 measured groups had zero downstream FDR<0.10 genes and the remaining group had only one. It further reports no convergence with represented endothelin-pathway targets. This is not independent replication of the Parquet, but it is useful biological interpretation of the Ednra training measurement.

## Reasoning

Ednrb has credible target-side biology in a responsive cell, so the forecast should not be a structural assay-failure null. The limiting factor is instead focal reach: Ednrb RNA is detected in only about 2% of non-target nuclei in the aggregated `151 TH Prkcd Grin2c Glut` class. A sparse GPCR-dependent effect in such a small subpopulation is unlikely to create a detectable whole-class Wilcoxon signature after BH correction.

The available matched training evidence supports that downward placement. The same receptor family's available analog, `Ednra`, is exactly zero in this class; represented endothelin-proximal genes and a broad set of neuronal GPCR-like perturbations are almost all 0-1 DEG outcomes; and the global focal training distribution puts zero as the modal and median result. The high-count tail in this class is dominated by core chromatin, RNA-processing, proteostasis, and essential trafficking perturbations with broad expression and broad postmitotic transcriptional consequences, not by low-reach neuromodulatory receptors.

Balancing plausible EDNRB stock loss against very low in-assay reach and near-null endothelin/GPCR training behavior, the most likely integer count is the focal null:

`predicted_n_degs = 0`.
