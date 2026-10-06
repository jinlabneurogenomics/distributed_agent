# Hdac4 direct held-out DEG-count forecast

Endpoint: `n_degs` for `Hdac4` in `151 TH Prkcd Grin2c Glut`, counting measured genes with BH-adjusted Wilcoxon `p < 0.05`.

## Target biology used

- The manifest target is `Hdac4`.
- The canonical biology bundle resolves this packet by supplied identifiers to mouse Entrez 15184 / ENSMUSG00000008855, official `Hdac5`; official mouse `Hdac4` was treated as a distinct locus and was not used as target biology.
- Exact in-assay focal expression reach was high: the target feature was present in 18,962 of 23,679 non-target nuclei in `151 TH Prkcd Grin2c Glut` cells, 80.079% expressing, mean log1p-CP10K 0.691. This made a transcriptomic effect assay-visible in principle.
- HDAC5 is a signal-responsive class-IIa corepressor component whose associated deacetylase function depends on SMRT/N-CoR-HDAC3 assemblies and whose neuronal nuclear occupancy is activity-regulated.
- The biology packet did not establish an endogenous HDAC5 protein or complex half-life in postmitotic thalamic neurons over the 21 to 28 day P16-to-harvest interval. Editing should stop new HDAC5 production but need not immediately remove existing corepressor stock.
- Single Hdac5 loss is buffered in the available mouse-neural literature, while combined HDAC4/HDAC5 loss exposes forebrain phenotypes, supporting compensation as a live reason that a single class-IIa HDAC lesion could be weak in basal juvenile thalamic neurons.

## Training measurements used

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 training targets. Its distribution is extremely zero-heavy:

- 1,205 / 1,674 targets have 0 DEGs.
- Median = 0.
- 75th percentile = 1.
- 90th percentile = 2.
- 95th percentile = 18.
- Mean = 14.05, inflated by a small heavy tail; the maximum is 2,677.

I ran the typed gene-analog nomination skill using that count table as the training universe. It found `Hdac4` absent from the training universe and surfaced a small exact/direct tier inside a much broader chromatin-transcription fallback pool. The strongest HDAC or MEF2-axis training perturbations in the exact 151-class endpoint were all low:

| comparator | typed role from nomination or biology | 151-class n_degs |
|---|---:|---:|
| `Hdac5` | class-IIa HDAC/physical interaction comparator | 0 |
| `Hdac8` | HDAC-family fallback | 0 |
| `Mef2a` | HDAC-regulated MEF2 axis | 4 |
| `Mef2c` | MEF2 complex or interaction comparator | 1 |
| `Mef2d` | MEF2-family comparator | 0 |
| `Camk2a` | HDAC5 localization/activity pathway | 0 |
| `Camk2b` | HDAC5 localization/activity pathway | 1 |
| `Camk2g` | HDAC5 localization/activity pathway | 0 |
| `Ep300` | activity-dependent chromatin cofactor contrast | 0 |
| `Crebbp` | KAT3 chromatin cofactor contrast | 8 |
| `Ctbp1` | transcriptional corepressor contrast | 5 |

Among the 13 nomination hits with exact-complex, paralog, physical-interaction, or direct-dependency provenance, 8 had 0 DEGs and 11 had at most 4 DEGs. The two high outliers, `Yy1` and `Sin3a`, had 720 and 1,433 DEGs, but these are broad essential chromatin regulators rather than class-IIa HDAC/MEF2-like single-loss comparators.

I also compared 22 HDAC, MEF2, CaMK, 14-3-3, and chromatin/corepressor training perturbations directly in the declared Parquet for `151 TH Prkcd Grin2c Glut`. The exact Parquet activity table gave 0 significant features for `Hdac5` and `Ep300`, 4 for `Mef2a`, 1 for `Mef2c`, 8 for `Crebbp`, 5 for `Ctbp1`, 720 for `Yy1`, and 1,433 for `Sin3a`, confirming that the local close mechanistic comparators are sparse while the large responses come from broader regulators.

## Packaged same-experiment interpretations used

The same-experiment corpus was used only to interpret training perturbations, not as independent validation.

- The `Hdac5` report described only a single-gene FDR<0.10 response in `012 MEA LA CA1 DG Glut`, with no 151-class response, no canonical activity/MEF2 program, and no meaningful convergent profile neighbor.
- `Mef2a` had a tiny, 151-restricted response, while `Mef2c` had its main signal in cortical IT neurons and only a tiny 151-class response; `Mef2d` was transcriptionally buffered. The corpus explicitly separated `Mef2c` from `Mef2a`, `Mef2d`, and `Hdac5` rather than treating the family/corepressor axis as one shared state.
- `Ep300` was flat across measured neuronal groups, and `Crebbp` made only a small 151-class response. This made a generic chromatin cofactor expectation a poor reason to borrow high counts from broad regulators.

## Forecast synthesis

The target transcript is detectable in the focal population, so I did not treat `Hdac4` as unreachable. The stronger bearings, however, were downward:

- the most local represented HDAC comparator, `Hdac5`, was exactly 0 in the requested group;
- MEF2/CaMK pathway perturbations were 0 to 4 in the same endpoint rather than large;
- same-experiment reports argue against a linear HDAC5 loss -> MEF2 activation -> broad activity-gene module in unstimulated P16-to-P37/P44 neurons;
- single class-IIa HDAC loss has both functional-stock uncertainty and paralog buffering.

I therefore chose the modal and median small-effect value for the exact endpoint rather than the broad chromatin-regulator tail.

Predicted `n_degs`: **0**
