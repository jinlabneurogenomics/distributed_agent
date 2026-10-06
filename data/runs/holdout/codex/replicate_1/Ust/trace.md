# Ust n_degs forecast

## Target and endpoint

- Target: `Ust`.
- Endpoint: `151 TH Prkcd Grin2c Glut` `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- I used the declared one-row holdout manifest, the declared `Ust` biology bundle, the focal-population training count table, the declared expression Parquet, and same-experiment corpus summaries for training genes. I did not use a `Ust` perturbation signature, a `Ust` outcome count, labeled-neighbor outcomes, or calibrated response probabilities.

## Quantitative evidence

- The focal count table has 1,674 training perturbations. It is strongly zero-inflated in this class: 1,205/1,674 are `0`, the median is `0`, the 75th percentile is `1`, and the 90th percentile is `2`; the mean is inflated to `14.05` by a small high-response tail.
- The exact in-assay reach for `Ust` was real but sparse: 3,922/23,679 non-target cells expressed `Ust`, with 16.56% expressing cells, mean raw UMI 0.223, and pseudobulk 14.0 CPM. This supports possible target engagement in the focal population but not a large ubiquitous cell-autonomous program.
- The closest focal-class glycosaminoglycan/proteoglycan training perturbations I found in the count table were all zero:
  - `B3gat3`: `0`
  - `Ext1`: `0`
  - `Ext2`: `0`
  - `Glce`: `0`
  - `Gpc6`: `0`
  - `Hs6st2`: `0`
  - `Xylt1`: `0`
- Direct Parquet scans for those seven perturbations within `151 TH Prkcd Grin2c Glut` found no rows with `pvals_adj < 0.05`. Matched perturbed nuclei ranged from 155 to 255 against 23,679 matched controls. `Ext2` had the only near-threshold adjusted value, its self-target row at `p_adj = 0.0559`; the other pathway perturbations had minimum adjusted values from 0.1619 to 1.0.
- A symmetric profile comparison of the same seven training perturbations recorded `no_significant_features` for all seven. The cohort diagnostic had zero significant-program overlaps in both positive and negative directions, so the zero counts were not hiding an FDR-supported shared 151-class module.
- Same-experiment corpus Findings for the training comparators matched the table-level picture: `Ext1` and `Glce` were interpreted as flat across neuronal groups, `B3gat3` as extremely restricted to one non-151 GABA class, and `Ext2` as only a sparse response outside the focal class. Those Findings are semantic summaries of the same experiment, not independent replication.

## Biology-to-count synthesis

`Ust` is a Golgi uronyl 2-O-sulfotransferase for chondroitin/dermatan sulfate chains. A P16 edit should block new Ust-dependent 2-O-sulfated carrier production, and the biology bundle judges the renewable functional stock likely substantially depleted by the P37-P44 harvest, but not as an immediately lost protein or transcription factor: pre-edit sulfated glycosaminoglycans are covalently modified and can persist until their extracellular carriers turn over.

That mechanism made a massive acute nuclear RNA response less likely than for direct RNA-processing, proteasome, mitochondrial, or stress-pathway perturbations in the high-yield 151 class. The most informative measured comparators were the postnatal neuronal GAG/HS biosynthesis genes above; every one was zero in the same endpoint, and their row-level signatures lacked significant downstream genes despite hundreds of recovered perturbed nuclei. The counterweight is that `Ust` has no identified close same-reaction paralog and is expressed in the focal class, so I would not treat the effect as biologically impossible. But the local training evidence for this extracellular sulfation axis points to a silent or sub-FDR postnatal neuronal transcriptome.

Point prediction: `0`.
