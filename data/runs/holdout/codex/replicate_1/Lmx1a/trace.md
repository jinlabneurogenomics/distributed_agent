# Lmx1a `n_degs` forecast

Target: `Lmx1a`

Focal population: `151 TH Prkcd Grin2c Glut`

Predicted `n_degs`: `0`

## Evidence used

- The one-row holdout manifest names `Lmx1a`, and `Lmx1a` is absent from the focal training count table, so no target endpoint was available in the declared count input.
- The biology bundle's exact in-assay reach measurement for `Lmx1a` in `151 TH Prkcd Grin2c Glut` is essentially absent: 21 total `Lmx1a` UMIs across 23,679 non-target nuclei, 19 expressing cells, `0.0802%` expressing cells, mean raw UMI `0.000887`, mean log1p CP10k `0.000449`, and pseudobulk CPM `0.0556`.
- The same bundle supports loss of functional stock in any successfully edited expressing cell: `Lmx1a` is a renewable nuclear LIM-homeodomain transcription factor, and pre-edit protein is expected to clear within the 21-28 day edit-to-harvest window. This raises confidence that an expressing cell can be functionally perturbed, but it does not overcome the focal population's near-zero target expression.
- The bundle's anatomical prior is concordant with the focal expression measurement: postnatal `Lmx1a` expression is restricted to selected hypothalamic, ventral-midbrain, and hindbrain populations, and an external adult thalamic single-cell atlas detected `Lmx1a` in only 5 of 1,972 thalamic projection neurons.
- The focal training count table contains 1,674 perturbations with a sparse, zero-heavy distribution: 1,205 targets have 0 DEGs, the median is 0, the 75th percentile is 1, the 95th percentile is 18, and only 43 targets have at least 100 DEGs.
- Biologically close postmitotic/developmental identity-factor comparators in the same focal table are flat: `Lmx1b`, `Pitx3`, `En1`, `Foxa2`, `Otx2`, `Isl1`, and `Tbr1` each have `n_degs = 0`; `Zic2`, `Lhx3`, and `Lhx4` are also 0, while `Sox5` and `Zic1` have only 2.
- Direct inspection of the focal Parquet rows confirmed that `Lmx1b`, `Pitx3`, `En1`, `Foxa2`, `Otx2`, `Isl1`, and `Tbr1` each had 17,259 measured genes and 0 genes at both FDR < 0.05 and FDR < 0.10. `Lmx1b` had 271 matched perturbed nuclei and every adjusted p-value in the focal group was 1.0.
- Low recovered-cell count alone was not enough to force a null in this same context: `Rora` had 278 focal DEGs with 139 matched perturbed nuclei, and `Tcf7l2` had 106 with 111 matched perturbed nuclei. The zero call for Lmx1a was therefore driven by expression reach and biology, not by treating all modest-n cells as silent.
- The packaged same-experiment corpus report for training target `Lmx1b` called an all-class FDR < 0.10 transcriptional null and found no robust convergence with the represented midbrain-dopaminergic network perturbations. I used this only as curated interpretation of the training surface, not as independent replication.

## Reasoning

`Lmx1a` is a plausible transcriptional regulator in the cells where it is actually expressed, and its functional stock should be depleted by harvest after an effective P16 edit. The direct focal reach measurement, however, places almost no `Lmx1a` transcript in the assayed thalamic class. A pooled, sparse postmitotic CRISPR perturbation of a TF that is absent from 99.92% of matched control nuclei has little opportunity to create a shared recovered-cell RNA state large enough to pass BH correction over 17k genes.

The most relevant training evidence points the same way. The close paralog `Lmx1b` and several represented midbrain/developmental homeobox or identity TFs were zero in this thalamic class, while true thalamic regulators such as `Rora` and `Tcf7l2` can produce large signatures even with fewer matched perturbed nuclei. That pattern makes a rare, large hidden `Lmx1a` response less likely than an ordinary null-bin target.

I therefore used the lower mode of the focal training distribution as the point forecast and predicted no BH-significant measured genes.
