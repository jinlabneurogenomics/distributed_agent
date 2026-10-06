# Tmem63a n_degs forecast

## Requested endpoint

- **Target:** `Tmem63a`
- **Cell class:** `151 TH Prkcd Grin2c Glut`
- **Endpoint:** integer count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- **Prediction:** 0

## Declared target biology

The declared biology bundle for `Tmem63a` identifies TMEM63A as a mechanically activated / osmolarity-sensitive cation channel in plasma and lysosomal or organellar membranes. Disruptive editing should stop production of new channel, but pre-existing membrane pools are not directly disabled by the edit, and the bundle found no basal half-life or post-edit clearance time in mouse neurons or oligodendrocytes that would prove depletion over the P16 to P37-P44 assay window.

The strongest positive mouse CNS phenotype is outside the assayed cells: Tmem63a loss has a postnatal oligodendrocyte/myelination phenotype. The same card explicitly noted that postnatal brain TMEM63A is concentrated in differentiated oligodendrocytes rather than NeuN-positive neurons, so that biology supports neural observability in general but is a weak match to survivor-conditioned thalamic NeuN-positive nuclei.

The exact expression reach in the focal class also points toward a small neuronal transcriptomic footprint:

- `Tmem63a` non-target expression in `151 TH Prkcd Grin2c Glut`: 2,257 / 23,679 nuclei expressing, 9.5317%.
- Pseudobulk abundance: 6.8526 CPM.
- Mean raw UMI: 0.1093.
- Mean log1p CP10K: 0.0491.

That reach supersedes any qualitative expression guess. It confirms that the target transcript is detectable, but only sparsely in this thalamic neuronal aggregate.

## Training measurements used

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table has 1,674 visible training targets and excludes `Tmem63a`. Its distribution is zero-heavy:

- median `n_degs`: 0
- 75th percentile: 1
- 90th percentile: 2
- 1,205 / 1,674 targets, 71.98%, have 0 DEGs
- 1,481 / 1,674 targets, 88.47%, have 0 or 1 DEG

The long upper tail is made by broadly disruptive RNA-processing, proteostasis, and chromatin targets, not by the target's TMEM63-family channel biology.

The explicit paralogs named in the biology bundle were the most direct measured comparators:

| training target | count-table `n_degs` | exact significant rows in the declared parquet |
| --- | ---: | --- |
| `Tmem63b` | 1 | only `Tmem63b` itself: logFC -0.7010, `pvals_adj = 4.1586e-17` |
| `Tmem63c` | 0 | none; its self row had logFC -0.3167 and `pvals_adj = 0.9747` |

The profile comparison over the same `151 TH Prkcd Grin2c Glut` parquet rows confirmed that both paralog profiles were available over 17,259 measured features; `Tmem63b` had exactly one FDR-significant negative feature and `Tmem63c` had no significant features. Thus the nearest same-family evidence is not a hidden broad downstream program: after removing the self-transcript row from `Tmem63b`, both paralogs are downstream-null in the focal cell class.

Other visible ion-channel comparators in the count table were also mostly quiet in this endpoint: `Trpm3`, `Trpm7`, `Pkd1`, `Kcnn2`, `Kcnn3`, `Cacna1a`, `Cacna1d`, `Cacna1e`, and `Cacna2d2` all had 0 DEGs, while `Cacna2d1` had 1 and thalamus-relevant `Cacna1g` had 12. This does not override the closer `Tmem63b`/`Tmem63c` evidence, but it supports the idea that deleting a membrane channel is usually not enough by itself to create a large recovered-nucleus DEG burden here.

## Synthesis

The forecast is dominated by three observations:

1. `Tmem63a` biology is glial/myelination-heavy, whereas the endpoint is NeuN-positive thalamic neuronal RNA.
2. The exact focal-population expression reach is low, so a sparse self-transcript test is uncertain and any cell-autonomous neuronal state should be diluted across the aggregated thalamic class.
3. The two closest measurable family members showed 0 downstream FDR-significant genes; the only paralog hit was `Tmem63b` self-knockdown.

Those bearings put the expected value below one significant gene. A self `Tmem63a` row could in principle pass if editing produces an unusually strong nuclear transcript drop, but the dataset-wide self-knockdown guard prevents treating that as guaranteed, and the weaker `Tmem63c` self row shows that a TMEM63-family guide set can remain nonsignificant after BH correction. I therefore round the direct biology-plus-training forecast to:

`predicted_n_degs = 0`

No target `Tmem63a` perturbation contrast or held-out outcome was queried or used.
