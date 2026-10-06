# Slc17a5 direct `n_degs` forecast

Endpoint: number of genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut`.

## Evidence used

- The declared holdout target is `Slc17a5`. `Slc17a5` is absent from both the one-row training count table and `training_de_all_cell_groups.parquet`, so the target count and target signature were not available from the training measurements.
- The exact focal-population expression bundle shows detectable but diluted target reach: `Slc17a5` is expressed in 11,054/23,679 non-target nuclei, or 46.68%, with mean raw UMI 0.697, mean log1p CP10K 0.292, and pseudobulk CPM 43.7.
- The endpoint-matched training distribution is very zero-heavy: among 1,674 measured training perturbations in `151 TH Prkcd Grin2c Glut`, 1,205 had `n_degs = 0`, 276 had `n_degs = 1`, and 1,481 had `n_degs <= 1`; the median was 0, the 90th percentile was 2, and only the extreme tail gave a mean as high as 14.05.
- The biology bundle places Slc17a5/sialin function in lysosomal sialic-acid export plus a vesicular acidic amino-acid pool. It supports likely substantial depletion of renewable transporter stock over the 21-28 day post-edit window, but the phenotype evidence is germline/developmental and strongly glial/myelination-related rather than an acute postmitotic thalamic-neuron loss measurement.
- I compared same-class training perturbations around lysosomal pH, lysosomal hydrolase/support factors, autophagy, and endosomal trafficking. The closest single lysosomal/vesicular or lysosomal-proton perturbations were quiet or self-only: `Atp13a2 = 1`, `Atp6v0a1 = 1`, `Ctsb = 1`, `Gaa = 1`, `Psap = 1`, `Slc9a7 = 1`, `Lamp2 = 0`, `Atp13a3 = 0`, `Atp6v1a = 0`, `Atp6v1b2 = 0`, `Atp6v1e1 = 0`, `Atg5 = 0`, `Atg16l1 = 0`, and `Ap3b1 = 0`. In the significant-row slice, the singleton calls for `Atp13a2`, `Atp6v0a1`, `Ctsb`, `Gaa`, `Psap`, and `Slc9a7` were just their own perturbed transcripts.
- I treated high-burden trafficking regulators as boundaries, not direct averages. `Rab7` had 501 significant genes and induced a broad endolysosomal/cholesterol response; `Vps35` and `Vps54` had 17 and 31 genes. Those perturbations affect late-endosomal identity, retromer, or vesicle traffic much more broadly than a substrate-specific Slc17a5 transporter.

## Synthesis

Slc17a5 is sufficiently expressed that a CRISPR-induced self-transcript decrease could be detected, and its membrane stock should probably turn over within the experiment. The observed training perturbations closest to that biology, however, do not usually produce a broader survivor-state transcriptional program in this thalamic class; they sit at 0 or at self-only 1. I therefore forecast no robust downstream response and choose the self-only analogue count.

Predicted `n_degs`: **1**
