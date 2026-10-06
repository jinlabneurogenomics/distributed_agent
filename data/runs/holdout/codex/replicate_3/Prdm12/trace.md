## Prediction

`Prdm12` in `151 TH Prkcd Grin2c Glut`: **0 DEGs** at BH-adjusted Wilcoxon `p < 0.05`.

## Evidence used

- Declared target: the one-row manifest names `Prdm12`.
- Target biology-only bundle: PRDM12 is a dynamic nuclear transcriptional regulator, and successful editing should plausibly deplete new functional PRDM12 by the P37-P44 harvest window. The supporting adult loss evidence is in peripheral nociceptors and hypothalamic POMC neurons rather than in this exact thalamic glutamatergic class, so it supports possible postnatal neuronal activity but leaves exact thalamic endpoint coupling uncertain.
- Exact focal-population reach from the declared bundle superseded the qualitative expression prior: in matched non-target `151 TH Prkcd Grin2c Glut` nuclei, `Prdm12` was detected in 30 of 23,679 nuclei, with `pct_cells_expressing = 0.1266945`, `total_target_umi = 34`, `mean_raw_umi = 0.0014359`, and `mean_cp10k = 0.0008068`.
- The 151-class training count table is heavily zero-inflated: 1,205 of 1,674 training targets have `n_degs = 0`; the median is 0, the 75th percentile is 1, and the 90th percentile is 2.
- The same training count table gives the represented PRDM-family comparators in this focal class as `Prdm10 = 52`, `Prdm16 = 0`, `Prdm2 = 0`, and `Prdm5 = 0`.
- A matched 151-class profile comparison over the declared Parquet reproduced those endpoint counts directly from `pvals_adj < 0.05`: `Prdm10` had 52 significant features, split 41 negative and 11 positive, while `Prdm2`, `Prdm5`, and `Prdm16` each had 0.
- Same-experiment corpus context for `Prdm10:F009` reports that represented PRDM-family perturbations did not phenocopy one another: `Prdm10` produced a recurrent neuronal module, whereas `Prdm16` and `Prdm5` were flat and `Prdm2` had only a non-overlapping Pvalb signal. I treated that as interpretation of the same experiment, not independent replication.

## Reasoning

Prdm12 has a plausible within-window molecular loss prior because it is a renewable nuclear regulator rather than a fixed developmental structure. That keeps it from being an automatic null. However, the requested endpoint is a BH-significant aggregate differential-expression count in all recovered `151 TH Prkcd Grin2c Glut` nuclei. The exact in-assay reach is the decisive downward bearing: only 0.127% of non-target nuclei contained any detectable `Prdm12` RNA, for 34 total UMIs across the full matched control population. Even a strong change in the true Prdm12-positive minority would be diluted across the aggregated thalamic class and unlikely to move many genes past BH correction.

Training measurements are consistent with that conservative placement. Zero is the modal and median outcome in this focal count table, and closely represented PRDM-family observations do not justify borrowing the `Prdm10` response scale: `Prdm10` is the lone active represented PRDM perturbation, the other represented PRDMs are silent in the focal 151 endpoint, and the corpus explicitly calls the PRDM-family response non-interchangeable. Broad chromatin regulators can yield large 151 footprints, but Prdm12's exact reach is unlike a broad regulator in this assayed population.

The most likely focal aggregate result is therefore below the first detectable gene threshold, so I rounded the forecast to `0`.
