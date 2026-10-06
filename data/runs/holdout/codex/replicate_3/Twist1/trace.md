# Twist1 DEG-count forecast

## Endpoint and target

- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, defined as the count of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- Target: `Twist1`, from the one-row holdout manifest.
- The prediction is for the P16-to-P37/P44 sparse CRISPR loss-of-function, survivor-conditioned NeuN+ thalamic neuronal readout.

## Evidence used

- `Twist1` is a bHLH nuclear transcription factor, so a successful disruptive edit should remove an active diffusible regulator rather than leave a long-lived installed product. The functional-stock card calls substantial protein depletion by harvest likely: pre-edit Twist1 would be diluted by many hour-scale protein-turnover cycles over the 21-28 day edit-to-harvest window.
- That realization prior is limited by reach. The exact in-assay focal-population measurement was extremely low: `Twist1` had `mean_raw_umi = 0.0054056337`, `pseudobulk_cpm = 0.3387902`, and only 104 of 23,679 matched non-target nuclei expressed the transcript, i.e. 0.439% of nuclei. The source card also placed the best direct loss evidence in embryonic cranial development and found no matched postnatal thalamic-neuron Twist1 loss study.
- The declared training count table for `151 TH Prkcd Grin2c Glut` contained 1,674 perturbations. Its empirical mode and median were both 0: 1,205 targets had 0 DEGs, only 469 had any DEG, 193 had at least 2, 106 had at least 10, and 43 had at least 100.
- I used the expression Parquet in the same focal class to verify that the relevant developmental/transcription-factor comparators were measured over 17,259 genes in this population rather than absent. Close or thematically adjacent developmental TFs were mostly null in the focal count table: `Twist2 = 0`, `Atoh1 = 0`, `Tcf3 = 0`, `Tcf12 = 0`, `Runx2 = 0`, `Neurod1 = 0`, `Neurod2 = 0`, `Neurog3 = 0`, `Mef2d = 0`, with only small exceptions such as `Mef2c = 1`, `Mef2a = 4`, and `Zeb1 = 15`.
- The same-experiment corpus report for `Twist2`, the closest paralog exposed in training, described a pan-neuronal negative result: no robust downstream single-nucleus RNA response in any of the 23 measured neuronal groups. Directly recomputing `Twist2` from the training Parquet gave 0 genes with `pvals_adj < 0.05` in all 23 groups, including `151 TH Prkcd Grin2c Glut`.

## Synthesis

The edit window should be long enough to deplete functional Twist1 in cells that depend on ongoing Twist1 supply, so I did not down-weight the perturbation as a persistent-stock failure. The decisive factor was coverage and context: Twist1 RNA was nearly absent in the assayed thalamic NeuN+ population, and the prior biology points to developmental/non-neuronal roles rather than a broad postmitotic thalamic-neuron program. In the training data, the base rate in this cell class is already heavily null, and the paralog/developmental-bHLH training perturbations sit on the null or near-null part of the distribution rather than with broadly expressed chromatin or core transcription regulators.

I therefore used the modal value for this class and comparator family and predict no BH-significant measured genes.
