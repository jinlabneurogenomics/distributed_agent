# Col4a1 forecast trace

## Target and endpoint

- Target manifest: one row, `Col4a1`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the count of measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05` in the focal population.
- Same-experiment corpus check: the selected release had no packaged `Col4a1` Findings, Claims, or explicit report references, so the forecast used the declared biology bundle plus focal training measurements.

## Col4a1 biology used

- The canonical biology bundle identifies COL4A1 as a secreted alpha1 chain of the alpha1-alpha1-alpha2 type IV collagen heterotrimer installed in basement membrane.
- The exact focal-expression reach shows `Col4a1` RNA was measurable in non-target `151 TH Prkcd Grin2c Glut` nuclei: 17,735 / 23,679 nuclei expressing, 74.8976% expressing, mean log1p CP10k 0.7614, mean raw UMI 2.4276.
- Expression reach supports the possibility that guide editing can hit the locus, but it does not establish a cell-autonomous nuclear function. The bundle's strongest source-pattern evidence places Col4a1 mainly in vascular/perivascular brain cells rather than neurons.
- The functional-stock card judged the operative material to be a pre-installed extracellular collagen IV network. A P16 edit can stop new synthesis in edited cells, but it does not acutely dismantle already deposited collagen; by the P37-P44 harvest, depletion is expected to be partial and cell-source mismatched rather than a synchronous pan-neuronal loss.

## Training measurements used

The declared focal count table contains 1,674 training perturbations:

- median `n_degs`: 0
- mean `n_degs`: 14.05, inflated by a few high-burden intracellular perturbations
- zero-DEG perturbations: 1,205 / 1,674
- perturbations with `n_degs <= 1`: 1,481 / 1,674

I used the count table to inspect extracellular-matrix, adhesion, endothelial, and pericyte-adjacent training targets that were actually observed in the focal class:

| training target | focal `n_degs` |
| --- | ---: |
| `Col11a1` | 0 |
| `Col2a1` | 0 |
| `Fbn1` | 0 |
| `Timp3` | 1 |
| `Itga2` | 0 |
| `Itga2b` | 0 |
| `Itga4` | 0 |
| `Itga6` | 0 |
| `Itga7` | 0 |
| `Itga8` | 0 |
| `Itga9` | 0 |
| `Itgb1` | 0 |
| `Itgb2` | 0 |
| `Pdgfrb` | 0 |
| `Abcc9` | 0 |
| `Slc2a1` | 0 |
| `Kdr` | 0 |
| `Tek` | 0 |

The matched Parquet profile comparison for these 18 targets in `151 TH Prkcd Grin2c Glut` confirmed the count-table pattern: all 18 had focal profiles available; 17 had no FDR-significant genes and one had only a 1-to-9 significant-feature response. A bounded inspection verified 17,259 measured features per selected focal profile and exact `significant_feature_count` values of 0 for `Col11a1`, `Col2a1`, `Fbn1`, and `Itgb1`, with `Timp3` at 1.

## Synthesis

The exact RNA reach prevents treating `Col4a1` as unexpressed, but the endpoint still requires a recovered-neuron transcriptional response. COL4A1's molecular role is extracellular and structural, much of the relevant stock predates the P16 perturbation, and the strongest prior localizes the normal supply to vascular/perivascular cells rather than the NeuN-positive thalamic neurons read out here. In the declared training set, focal perturbation of analogous extracellular-matrix, adhesion, and vascular genes almost always yielded zero DEGs and never yielded a broad response. Against a zero median for the whole focal training table, those points make the near-zero forecast more credible than borrowing scale from the rare high-burden proteostasis, RNA-processing, or chromatin perturbations.

Point prediction: `Col4a1` -> `0` DEGs.
