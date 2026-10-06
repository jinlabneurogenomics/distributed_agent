# Grip1 n_degs forecast

## Target and endpoint

- Target manifest: `Grip1`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Prediction: `0`

## Biology that set the prior

The declared biology bundle maps Grip1 to Ncoa2/GRIP1, a ligand-dependent p160 nuclear-receptor transcriptional coactivator. In the exact focal population, Grip1 was detected in 10,194 of 23,679 non-target nuclei, or 43.0508%, with mean CP10K 0.4044 and pseudobulk CPM 40.0884. That makes the target present in the assayed class but only at moderate cellular reach.

The functional-stock card argues that a P16 disruptive edit should eventually reduce the soluble, dynamic Ncoa2/GRIP1 coactivator pool by the P37-P44 harvest because the operative molecule is a reversible recruited coactivator rather than a durable installed structure. I treated that as evidence that loss could be realized by the 21-28 day readout.

The same bundle left the endpoint coupling weak: the direct loss phenotypes are systemic/reproductive rather than postnatal thalamic neuronal, no target-specific neuronal depletion curve was found, nuclear-receptor/coactivator output is ligand and promoter dependent, and the p160 paralogs Ncoa1 and Ncoa3 provide plausible but untested buffering in this context.

## Training measurements used

The declared count table contains 1,674 held-out-free training targets for `151 TH Prkcd Grin2c Glut`.

Global count distribution:

- median: 0
- mean: 14.05
- nonzero targets: 469 / 1,674
- 75th percentile: 1
- 90th percentile: 2
- 95th percentile: 18

Closest p160/nuclear-receptor-axis training counts at the exact endpoint:

| target | n_degs |
| --- | ---: |
| Ncoa1 | 0 |
| Ncoa3 | 0 |
| Ep300 | 0 |
| Crebbp | 8 |
| Ppargc1a | 0 |
| Rxra | 0 |
| Rxrb | 0 |
| Rxrg | 0 |
| Ppara | 0 |
| Ppard | 0 |
| Pparg | 0 |
| Esr1 | 0 |
| Esr2 | 0 |
| Nr3c1 | 0 |
| Nr3c2 | 0 |
| Ar | 0 |
| Pgr | 0 |
| Thra | 3 |
| Thrb | 0 |
| Vdr | 0 |

This 20-gene operation-proximal set has median 0, mean 0.55, and 18 / 20 members at zero FDR<0.05 genes. The broader nuclear-receptor list was also zero-centered, but it included assay-positive receptor-family controls, especially Rora 278, Nr1d1 116, and Esrra 57, showing that a nuclear-receptor transcription-factor perturbation could be detected in this thalamic class when it drove a strong basal program.

I then checked the matched Parquet rows for the most material comparators. Ncoa1, Ncoa3, and Ep300 each had 17,259 measured genes in this cell class and zero FDR<0.05 features; their matched perturbed-cell counts were 189, 147, and 155 against the same 23,679 controls, so their zero calls were not obviously caused by vanishing recovered-cell support. Their largest residual adjusted p-values were also far from threshold: the top Ncoa1 row had `pvals_adj = 0.83`, and the top Ncoa3 and Ep300 rows had `pvals_adj = 1`.

The profile comparison across the same 20-gene p160/receptor cohort preserved the same activity split: 18 nodes had `no_significant_features`, while Crebbp had 8 and Thra had 3. I did not treat high whole-profile logFC correlations among flat nodes as magnitude evidence because the endpoint is the FDR count and those pairs had no significant-feature overlap.

## Same-experiment corpus context

The packaged Ncoa1 and Ncoa3 findings supported interpreting those two paralogs as buffered, low-amplitude comparators rather than as an assay failure:

- Ncoa1 had no FDR<0.05 genes in `151 TH Prkcd Grin2c Glut`; the corpus also reports only one FDR<0.10 downstream event in any recovered cell group and no meaningful module among unbiased signature neighbors.
- Ncoa3 likewise had no FDR<0.05 genes in the focal class, only a singleton FDR<0.10 event elsewhere, and no strong transcriptome-wide neighbor.
- The reciprocal Ncoa1/Ncoa3 comparison rejected simple p160 interchangeability while noting that Ncoa2/Grip1 itself was unmeasured.
- Steroid-receptor and RXR/PPAR comparators were mostly flat, whereas Rora, Nr1d1, Crebbp, and Mediator components showed that the thalamic cell class had dynamic range for some transcription-regulator losses.

## Synthesis

Upward evidence was real but limited: Grip1 is present in 43% of the focal non-target nuclei and its protein stock should not persist indefinitely after editing. The strongest downward evidence was the matched training behavior of its nearest assayed biological neighbors: Ncoa1, Ncoa3, Ep300, PGC-1alpha/RXR/PPAR/steroid-receptor comparators were almost uniformly FDR-flat in the same cell class. Broader transcriptional regulators could give large signatures in this assay, but those were less operation-close than the ligand-dependent coactivator axis and tended to be dedicated TFs, Mediator/SWI-SNF/coregulator nodes, or chromatin regulators rather than a buffered p160 coactivator.

I therefore treated zero as the modal and best integer point. A tiny response of one to several genes remained plausible because Grip1 itself was not measured in training and is not guaranteed to phenocopy either Ncoa1 or Ncoa3, but the closest endpoint-matched evidence placed it below the FDR-count threshold more often than in the Crebbp/Med15/Rora-like response regimes.
