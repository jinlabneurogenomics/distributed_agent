# Zfp329 direct n_degs forecast

## Target and declared inputs

- Target: `Zfp329`, the only row in the declared holdout manifest.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, counted as measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Biology bundle used: `[local file: Zfp329.json]`, SHA256 `0d1476207e47dc51bdfcf51c72638a69bd19d6728ddd869e8715498ea5db28c5`.
- Focal training counts used: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`, SHA256 `48fb8105306c5444815f5fa82affeb83ca439ccb20751783172fe545881098f3`.
- Training profile comparison used: `evidence/zinc_finger_profile_comparison.json`, SHA256 `2306afacd2cd3be036302d5882ce298c3010e25406d2760638063f17907ddffe`; cohort diagnostic `evidence/zinc_finger_profile_cohort.json`, SHA256 `90af8a9a4391b5f0754784506ba93d800f317c70eaba3441e08b49911f991c18`.

## Evidence that determined the point

The biology-only bundle makes `Zfp329` assay-reachable but not a high-confidence thalamic maintenance regulator. It is a nuclear C2H2 zinc-finger protein predicted to bind RNA-polymerase-II regulatory DNA. In the exact focal non-target population, the `Zfp329` feature was present in 16,911 of 23,679 nuclei, with 71.418% of cells expressing it, mean log1p CP10K 0.5454, and pseudobulk CPM 86.844. Its functional stock was adjudicated as likely substantially depleted by P37-P44 because a P16 edit stops new protein supply and the closest thalamic turnover evidence supports protein renewal over days. The uncertainty is biological rather than assay presence: its germline phenotype is visual-system developmental, no P16-to-P44 thalamic loss time course was found, and no tested same-context compensator or postnatal thalamic target program was established.

The focal endpoint is strongly zero-inflated. Among 1,674 training perturbations in the 151 count table, 1,205 had `n_degs = 0`; the median was 0, the 75th percentile was 1, the 90th percentile was 2, and the 95th percentile was 18. Officially annotated transcription factors in the training table behaved similarly: 284 of 344 had zero focal DEGs, the median was 0, the 90th percentile was 2, and the 95th percentile was 15. The large training values came from a few named hubs such as `Zbtb7a`, `Yy1`, `Cic`, `Thap11`, `Rora`, and `Ctcf`, not from transcription-factor status in general.

I then compared the measured focal signatures of a 47-gene zinc-finger / POZ / SCAN-adjacent training cohort selected from the count table. Of these closest symbol-and-annotation analogs, 35 were null, five had only 1-9 DEGs, four had 10-49, and three had at least 50. The nonzero values were `[1, 1, 1, 5, 8, 15, 15, 19, 22, 74, 150, 841]`, so the central mass was still at zero with a small number of exceptional high responders. Within the 29 measured `Zfp*` perturbations, 24 were zero; the only nonzero examples were `Zfp612 = 1`, `Zfp692 = 1`, `Zfp148 = 8`, `Zfp236 = 19`, and the known developmental regulator `Zfp423 = 150`.

The profile cohort did not show a shared large zinc-finger program that would justify borrowing the high tail. Across 1,081 pairwise comparisons among the 47 selected zinc-finger-associated perturbations, the median positive top-tail overlap coefficient was 0.04 and the median negative top-tail coefficient was 0.06. Significant-program overlap was absent for most pairs: the median significant-program overlap coefficient was 0.0 in both directions. Packaged same-experiment Findings on visible comparators were consistent with this split: orphan or KRAB/SCAN-like factors such as `Zfp1`, `Zfp160`, `Zfp292`, `Zkscan1`, `Zkscan16`, and `Zscan26` were interpreted as context-local nulls in postmitotic neurons, whereas `Zfp148`, `Zfp236`, `Zeb1`, and `Zbtb7a` had specific narrow or exceptional modules not implied by Zfp329's sparse prior.

## Synthesis

`Zfp329` should be editable and visible in the assayed thalamic cells, so I did not force an absolute zero prior. But its card does not connect it to a known P16-P44 thalamic neuronal state, the closest measured anonymous zinc-finger factors were overwhelmingly null or single-gene responders, and the strong zinc-finger outliers had specific biology or observed programs that `Zfp329` lacks. I therefore put the forecast on the 0/1 floor rather than the heavy tail and used a one-gene point to allow either a self-transcript hit or one isolated downstream target.

Predicted `n_degs`: **1**
