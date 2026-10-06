# Direct forecast trace

Target: `Mapk8`

Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, defined as the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.

## Target biology used

- The canonical biology bundle reports exact focal expression for `Mapk8`: 18,740 of 23,679 non-target nuclei in `151 TH Prkcd Grin2c Glut` express the feature, with mean CP10K 1.1758 and mean raw UMI 1.8746. Target reach therefore supports the edit being observable in this assayed population.
- MAPK8/JNK1 is a soluble serine/threonine kinase in stimulus-coupled JNK signaling. A P16 disruptive edit should stop intact MAPK8 resupply, and over the P37-P44 harvest interval the canonical functional-stock card calls MAPK8 `likely_substantially_depleted`, but with partial evidence because no MAPK8-specific half-life in mature thalamic neurons was found.
- The same bundle also weakens a large deterministic effect: JNK substrate use is stimulus-, compartment-, and state-dependent; the clearest mouse neural phenotype is adult hippocampus rather than juvenile thalamus; and JNK-family paralogs can buffer some operations.

## Training measurements used

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` contains 1,674 training perturbations. Its endpoint distribution is zero-inflated and highly skewed:

- median `n_degs`: 0
- mean `n_degs`: 14.05
- zeros: 1,205 / 1,674
- 75th percentile: 1
- 90th percentile: 2
- 95th percentile: 18
- 99th percentile: 430

I therefore did not use the global mean as the point estimate; it is dominated by a small tail of generic regulators.

Typed analog nomination against the training universe prioritized MAPK/JNK candidates rather than symbol-prefix matches. The strongest training-available candidates were `Mapk9`, `Map3k7`, `Mapk1`, `Map2k1`, and `Map2k2`; they came from exact-complex/paralog, JNK/MAPK activity, AP-1/MAPK activation, and related narrow MAPK modules. Their exact training counts in the held-out cell class were:

| training perturbation | relationship to Mapk8 used for interpretation | n_degs |
| --- | --- | ---: |
| `Mapk9` | JNK paralog / JNK-module member | 0 |
| `Map3k7` | upstream stress-JNK kinase in shared modules | 0 |
| `Mapk1` | MAPK/AP-1 module member | 0 |
| `Map2k1` | MAPK module member | 4 |
| `Map2k2` | MAPK module member | 0 |
| `Map2k6` | stress-MAPK module member | 0 |
| `Prkca` | broader MAPK-signaling module member | 0 |
| `Chuk` | NF-kB/TLR stress branch comparator | 0 |
| `Nfkb1` | NF-kB/TLR stress branch comparator | 0 |
| `Raf1` | RAF/ERK branch comparator | 0 |

I verified the top comparator counts directly in the declared expression Parquet for `151 TH Prkcd Grin2c Glut`: each queried comparator had 17,259 measured genes; the nine zero-count candidates above had no genes with `pvals_adj < 0.05`, while `Map2k1` had four.

## Corpus/profile checks

The report-derived explicit-Finding topology over the 10 MAPK/JNK/NF-kB source candidates formed one connected component with 17 explicit comparator pairs. Expanding outbound report neighbors with at least two source candidates yielded 17 additional eligible training nodes; these were RAS/RAF/ERK boundaries, TLR/NF-kB boundaries, or explicitly nonconvergent/null profile neighbors rather than closer JNK1 donors.

A symmetric measured-profile comparison of the 27 source-plus-expansion nodes in `151 TH Prkcd Grin2c Glut` found 22/27 with no significant genes and only 5/27 in the 1-to-9 DEG band. The nonzero expansion nodes were still tiny: `Mef2c`, `Fbxo11`, and `Lztr1` had 1 DEG and `Braf` had 4; the RAS/RAF/ERK report paths were treated as boundary evidence because they encode loss-of-function/gain-of-function divergence or expected-program absence rather than a positive JNK1 analogue.

## Synthesis

`Mapk8` is expressed and the perturbation should be functionally realized by harvest, so the prediction should not be a technical missingness call. However, the endpoint asks for an FDR-significant recovered-nucleus transcriptional burden in one thalamic glutamatergic class. The closest measured JNK/MAPK perturbations are silent in that class, the broader stress/TLR and ERK boundaries are also silent or 1-4 genes, and the high tail of the training table is composed of regulators unlike a stimulus-coupled JNK kinase. I therefore placed `Mapk8` at the zero/near-zero mode and used the exact JNK paralog and upstream-module zeros to break the tie to a point of 0.

Predicted `n_degs`: 0
