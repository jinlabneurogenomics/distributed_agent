# Hspd1 direct forecast

## Endpoint and target

- Target from the declared one-row holdout manifest: `Hspd1`.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: all measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in that matched perturbation contrast. I treated the count as self-transcript-inclusive because the supplied training count table counts every measured feature, not only downstream genes.

## Evidence used

- The canonical Hspd1 biology bundle reports measurable focal-population reach: in non-target `151 TH Prkcd Grin2c Glut` nuclei, Hspd1 is detected in 13,638 of 23,679 cells, with 57.595% expressing, mean raw UMI 0.954, mean log1p CP10K 0.385, and pseudobulk CPM 59.77. This makes a self-feature hit plausible if nuclear target RNA is depleted, but the dataset portrait cautions that self-logFC is not a reliable editing-strength proxy.
- The same bundle characterizes HSPD1 as the mitochondrial Hsp60 component of a dynamic Hsp60-Hsp10 chaperonin for imported or stress-unfolded mitochondrial proteins. Editing should stop new HSPD1 supply while leaving pre-edit protein intact; adult mouse brain HSPD1 half-lives of roughly 25-30 days put the P16-to-P37/P44 harvest at about one protein half-life, so the expected state is partial depletion or leading-edge functional loss rather than cleared stock.
- The `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table has 1,674 observed training perturbations. Its count distribution is extremely zero-inflated: 1,205/1,674 rows have `n_degs = 0`, the median is 0, the 75th percentile is 1, the 90th percentile is 2, and the mean is inflated to 14.05 by a small tail of broad stress/splicing/proteasome responses.
- I used the training count table to focus on observed mitochondrial proteostasis, respiratory-chain, import, and chaperone perturbations closest to Hspd1 biology. Their `151` counts were mostly null or singleton:
  - `0`: `Aco2`, `Afg3l2`, `Clpp`, `Clpx`, `Lonp1`, `Ndufs4`, `Timmdc1`, `Uqcrfs1`, `Yme1l1`
  - `1`: `Atp13a2`, `Hsp90ab1`, `Sdha`, `Tomm40`, `Uqcrc2`
  - `2`: `Vcp`
  - `5`: `Hspa5`
  - `9`: `Hspa8`
  - `37`: `Opa1`
- Querying the declared Parquet for those same 18 targets in `151 TH Prkcd Grin2c Glut` confirmed 17,259 measured features per perturbation and the same FDR<0.05 activity. In several one-count mitochondrial or chaperone rows, the lone significant feature was the target itself: `Atp13a2`, `Hsp90ab1`, `Sdha`, `Tomm40`, and `Uqcrc2` were all self-transcript hits. That is the closest quantitative pattern for a measurable but downstream-buffered target.
- The same-experiment corpus supported treating a broad mitochondrial-stress response as unlikely rather than merely unobserved in one hand-picked table: `Clpx` and `Yme1l1` were transcriptionally flat across recovered postmitotic neurons; `Afg3l2`, `Clpp`, and `Lonp1` had only sparse focal responses outside this thalamic class; `Hsp90ab1` had no downstream FDR<0.10 genes; `Hspa8` and `Hspa5` produced small class-restricted chaperone/ER stress signatures; and the stronger `Opa1` program activated an ISR-like state without inducing a canonical `Hspd1`/`Hspe1`/`Clpp` mitochondrial UPR.

## Synthesis

Hspd1 is expressed in the focal thalamic neurons and encodes a continuously used mitochondrial folding machine, so I did not collapse the forecast to a complete biological null. The harvest window, however, is only around one adult-brain HSPD1 half-life, successful editing would leave a substantial pre-edit protein pool, and the readout is conditioned on nuclei that survived and were recovered. In the task-matched training data, loss of mitochondrial proteases, respiratory-chain components, mitochondrial import genes, and major chaperones was overwhelmingly 0-1 DEG in this cell class, with `Opa1` as the clear ISR outlier rather than the center of the Hspd1 analogue set.

I therefore expect no resolved broad downstream state, but one feature is plausible from the self transcript in a detectable target. Point prediction: **1 DEG**.
