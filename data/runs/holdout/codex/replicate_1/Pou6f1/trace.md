# Pou6f1 direct n_degs forecast

Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

Prediction: **0 DEGs**.

## Evidence used

- The declared holdout manifest contains the single target `Pou6f1`; `Pou6f1` is absent from the 1,674-row `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` training count table.
- The exact target-expression bundle reports measurable but partial reach in the focal non-target population: `mean_cp10k = 0.413999`, `mean_log1p_cp10k = 0.274887`, `10239 / 23679` nuclei expressing `Pou6f1`, or `43.24%`.
- The functional-stock card calls `Pou6f1` a nuclear sequence-specific POU transcription factor whose intact protein supply should plausibly be depleted by P37-P44 after a P16 disruptive edit, because editing stops new intact DNA-binding protein; it also flags target-specific turnover and thalamic dependence as unresolved.
- The `151 TH Prkcd Grin2c Glut` count table is heavily zero-inflated: 1205/1674 training targets have 0 DEGs, the median is 0, the 90th percentile is 2, and only 25 training targets exceed 100 DEGs.
- Closest class/family observations in the exact class are null. In the `151` count table, all represented POU targets had `n_degs = 0`: `Pou1f1`, `Pou2f1`, `Pou2f2`, `Pou3f3`, `Pou3f4`, `Pou4f3`, `Pou5f1`, and the closest class-VI paralog `Pou6f2`.
- I re-queried the expression parquet for those represented POU targets in `151 TH Prkcd Grin2c Glut`; each had 17,259 measured-gene rows and none had even `pvals_adj < 0.10`.
- The same-experiment corpus had no `Pou6f1` Finding or Claim in this prediction-safe release. It did have a `Pou6f2:F003` pathway-uncoupling Finding, supported by `Pou6f2:E027`, stating that represented POU targets did not phenocopy `Pou6f2` or reveal a generic acute POU-family response in P16 brain neurons. The Finding's main caveat is directly relevant: `Pou6f1` itself was absent as the strictest class-VI paralog perturbation.

## Reasoning

`Pou6f1` is not a clear technical null: the target RNA is detected in a large subset of the focal thalamic nuclei, and the edit should cut off production of an intact soluble nuclear transcription factor over the 21-28 day window. That makes a nonzero downstream signature biologically possible.

The task-matched empirical scale, however, puts the prior mass at zero. Most training perturbations in this cell class have no FDR-significant genes, and the exact POU-family comparators are even more informative than the marginal distribution: `Pou6f2`, the closest represented paralog, and all other represented POU factors are FDR-flat in the focal class, with no `pvals_adj < 0.10` genes in the parquet. Same-experiment report text also treats the represented POU factors as sparse and nonconvergent rather than as members of a shared acute neuronal response module.

I therefore did not use high-burden transcriptional regulators such as `Zbtb7a` or `Zfp423` as quantitative analogs: they demonstrate that transcription factors can generate large `151` signatures, but the matched POU observations point the other way. The final point forecast is the modal and nearest-family value, **0**.
