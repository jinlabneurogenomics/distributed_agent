# Direct forecast for Sec31a in `151 TH Prkcd Grin2c Glut`

## Declared target and endpoint

- Target: `Sec31a`.
- Endpoint: focal-population `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut`.
- The declared training Parquet contained no `gene_target == Sec31a` rows in the focal population or in any other assayed group, so the held-out Sec31a signature was not used.

## Evidence used

1. **Sec31a biology bundle**

   The canonical target bundle identifies SEC31A as a SEC13-SEC31 COPII outer-coat component recruited during ER-exit-site vesicle formation. Successful loss should eventually reduce anterograde ER export capacity, and the focal expression readthrough is strong enough for the transcript to be observable: `Sec31a` is expressed in 19,488 of 23,679 non-target focal nuclei, 82.3%, with mean log1p CP10K 0.724 and pseudobulk 126.9 CPM.

   This supports a possible perturbation effect, but not a large guaranteed acute transcriptome. The stock card adjudicates SEC31A as a dynamic complex component whose new intact supply stops after editing while existing SEC31A persists; no usable endogenous SEC31A degradation half-life was found for mouse thalamic neurons, so functional loss by the P37-P44 harvest remains indeterminate. The Sec31b paralog is only a related-gene/residual uncertainty item rather than a demonstrated focal compensation mechanism.

2. **Focal training count table**

   The `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table has 1,674 observed training perturbations. Its empirical burden is very sparse:

   - `n_degs = 0`: 1,205 / 1,674
   - `n_degs <= 1`: 1,481 / 1,674
   - `n_degs <= 5`: 1,546 / 1,674
   - median: 0
   - mean: 14.05, dominated by a small high-count tail

   This makes a zero-or-singleton forecast the local prior unless there is a strong measured analogue for a broader state.

3. **Observed secretory-pathway comparators in the same table and focal Parquet rows**

   The closest COPII targets present in the training table were both quiet:

   | target | focal `n_degs` | self logFC | self BH-adjusted p |
   | --- | ---: | ---: | ---: |
   | `Sec23a` | 0 | -0.351 | 0.873 |
   | `Sar1b` | 0 | -0.615 | 0.108 |

   Other present ER/export or vesicle-trafficking comparators were also mostly at zero or self-only levels: `Atf6 = 0`, `Copa = 0`, `Lman2l = 0`, `Rab18 = 0`, `Rab27a = 0`, `Stx5a = 0`, `Tango2 = 0`, `Copg1 = 1`, `Stx16 = 1`, `Stxbp1 = 1`. The larger but still modest ER-stress/translocation examples were `Hspa5 = 5` and `Sec63 = 11`.

4. **Self-transcript behavior in the focal training set**

   In the focal Parquet rows for all 1,674 training targets, 319 targets had a significant self transcript. None of the 1,205 zero-count targets had significant self, while 237 of the 276 one-count targets were self-only singletons. Thus the most likely way for `Sec31a` to clear the zero baseline is its own high-coverage transcript rather than a broad downstream COPII/UPR survivor-state program.

## Synthesis

SEC31A is focal-cell expressed and biologically central to COPII outer-coat function, so I do not treat it as an inert target. The direct focal training evidence, however, keeps the expected measured response very small: the only measured inner-coat or SAR1 perturbations available, `Sec23a` and `Sar1b`, had zero BH-significant genes, and the nearby vesicle-trafficking cohort lacked a recurrent multi-gene focal response. The stock adjudication also leaves uncertainty about how fully pre-existing SEC31A protein is depleted in the 21-28 day CRISPR window.

Balancing those two directions, I forecast a singleton signature. The integer point is **1 DEG**, representing a likely self-transcript call or at most a single visible ER-export/stress gene, with the main downside being a completely quiet recovered profile and only weak support for a larger `Sec63`/`Hspa5`-like response.
