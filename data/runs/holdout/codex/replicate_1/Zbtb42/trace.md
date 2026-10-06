# Zbtb42 direct n_degs prediction

## Target and endpoint

- Target manifest: `Zbtb42`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with Wilcoxon `pvals_adj < 0.05`
- Prediction: `0`

## Evidence used

### Declared Zbtb42 biology bundle

- The exact in-assay non-target expression reach for `Zbtb42` in `151 TH Prkcd Grin2c Glut` is extremely small: 33 target UMIs across 23,679 non-target nuclei, 31 expressing nuclei, `0.13091769078086068%` expressing, `mean_raw_umi = 0.0013936399341188395`, `mean_cp10k = 0.0009379209085359432`, and `pseudobulk_cpm = 0.08734435669051036`.
- The public biology prior is compatible with a nuclear BTB/POZ and C2H2 zinc-finger transcriptional regulator, and constitutive homozygous mutant mice have a nervous-system behavioral phenotype, but the evidence does not localize a juvenile postmitotic thalamic requirement.
- Whole-brain protein and adult thalamus bulk RNA support only low neural expression, not broad expression in the assayed thalamic neuronal class.
- Functional stock by the P37-P44 harvest is indeterminate: the edit should stop new ZBTB42 protein supply, but no target-specific protein half-life, chromatin residence, or clearance measurement pins down residual ZBTB42 activity 21-28 days after P16 editing.
- The same-experiment corpus had no `Zbtb42` Findings, Claims, or explicit references, so it did not provide a target outcome or a packaged same-experiment comparator for the held-out target.

### Training counts in the focal class

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table has 1,674 measured training targets. Its focal-class count distribution is dominated by zeros:

- median `n_degs = 0`
- 1,205 / 1,674 targets have `n_degs = 0`
- 1,481 / 1,674 targets have `n_degs <= 1`
- 1,546 / 1,674 targets have `n_degs <= 5`
- the mean is inflated to 14.05 by a very small number of broad responders; the 99th percentile is 430 and the maximum is 2,677

Measured ZBTB-family perturbations in the same focal count table were:

| target | n_degs |
|---|---:|
| Zbtb10 | 0 |
| Zbtb16 | 0 |
| Zbtb18 | 5 |
| Zbtb20 | 0 |
| Zbtb21 | 0 |
| Zbtb38 | 1 |
| Zbtb7a | 841 |

The declared expression parquet confirms that in the focal class the sparse nonzero family members were truly small FDR<0.05 signatures: `Zbtb18` had five significant genes and `Zbtb38` had one. Across all measured neuronal classes at the same FDR threshold, the same seven training ZBTB perturbations had only three nonzero members: `Zbtb18` with 9 significant rows across 5 groups, `Zbtb38` with 2 significant rows across 2 groups, and `Zbtb7a` with 2,007 significant rows across 22 groups.

Packaged same-experiment interpretations agree with those exact counts: `Zbtb10`, `Zbtb16`, `Zbtb20`, and `Zbtb21` were transcriptionally flat; `Zbtb18` and `Zbtb38` were weak/sparse; and `Zbtb7a` was the broad exception rather than a generic BTB-zinc-finger representative.

## Synthesis

The strongest quantitative prior is zero: nearly three quarters of all training perturbations and most measured ZBTB-family transcription-factor perturbations had no focal-class DEGs. `Zbtb7a` shows that the screen can detect a broad BTB-zinc-finger response when one exists, but the rest of the family argues that BTB/POZ zinc-finger identity alone is not enough to transfer the `Zbtb7a` scale.

For `Zbtb42` specifically, the exact focal-population expression reach is far weaker than would be expected for a broadly active 151-class regulator: only 31 of 23,679 non-target nuclei had any detected target UMI. Some functional protein may be missed by nuclear RNA sampling, and the constitutive mouse phenotype keeps a rare or developmental neural effect plausible, but the endpoint aggregates across the whole recovered thalamic class at an acute P16-to-P37/P44 interval. With target stock unresolved and no evidence for a broad juvenile thalamic program, the most likely BH<0.05 count is the modal value.

Therefore my point prediction is `n_degs = 0`.
