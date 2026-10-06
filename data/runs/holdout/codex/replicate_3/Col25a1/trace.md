# Col25a1 forecast for `151 TH Prkcd Grin2c Glut`

Endpoint: `n_degs`, the number of measured genes in the focal thalamic glutamatergic class with BH-adjusted Wilcoxon `p < 0.05`.

## Declared target biology

The canonical biology bundle identifies `Col25a1` as a type-II membrane collagen with a furin-shed extracellular ectodomain. The P16 edit should block new COL25A1 synthesis, and P25 thalamic neuronal expression supports target reach during the assay window, but the operative stock is split across a renewable membrane pool and a potentially persistent extracellular collagen pool. The functional-stock adjudication therefore calls the P37-P44 state `partially_depleted_or_leading_edge`, not a confidently cleared loss.

Exact focal-population baseline reach is permissive but not overwhelming: in non-target `151 TH Prkcd Grin2c Glut` nuclei, `Col25a1` was detected in 12,027 of 23,679 cells, `pct_cells_expressing = 50.7918`, `mean_cp10k = 0.8378`, and `pseudobulk_cpm = 84.417`. This supports the possibility of measuring a self-transcript decrease, while the bundle notes that baseline RNA expression does not prove editing efficiency or functional dependence.

The prior loss phenotype is embryonic motor-axon failure and motoneuron loss. That supports real neural biology for the gene, but it is not a matched postnatal thalamic loss state and does not argue for a large acute survivor-conditioned RNA response in P37-P44 thalamic neurons.

## Training measurements used

The declared focal count table has 1,674 non-held-out targets. Its distribution is strongly concentrated near zero:

| count range | number of targets |
|---|---:|
| 0 | 1205 |
| 1 | 276 |
| 2-4 | 61 |
| 5-9 | 26 |
| 10-24 | 37 |
| 25-99 | 26 |
| 100-499 | 28 |
| >=500 | 15 |

Thus 1,481 / 1,674 training perturbations have either 0 or 1 DEG in the same focal class.

No MACIT paralog of `Col25a1` was present in the focal training endpoint table, so I checked indirect extracellular, adhesion/guidance, amyloid/APP-processing, and convertase comparators instead. Counts from the declared table and focal rows in the Parquet were:

| comparator | focal `n_degs` | Parquet interpretation |
|---|---:|---|
| `Adam10` | 0 | no significant genes |
| `App` | 1 | only `App` itself was significant |
| `Dcc` | 0 | no significant genes |
| `Itga2`, `Itga2b`, `Itga4`, `Itga6`, `Itga7`, `Itga8`, `Itga9`, `Itgb1` | 0 | no significant genes |
| `Pcsk2` | 1 | only `Pcsk2` itself was significant |
| `Pcsk5` | 0 | no significant genes |
| `Psen1` | 0 | no significant genes |
| `Reln` | 0 | no significant genes |
| `Slc1a2` | 1 | only `Slc1a2` itself was significant |
| `Vldlr` | 0 | no significant genes |

These are imperfect analogs, but they cover the local biology available in the training table. They support a very small response forecast: mostly zero downstream calls, with occasional one-gene profiles driven by the perturbed transcript crossing FDR.

## Synthesis

I predict `Col25a1` will sit in the zero-or-one part of the distribution, not in the heavy tail. The upward evidence is exact in-assay expression in about half of focal non-target nuclei plus continued postnatal supply of a membrane precursor. The downward evidence is stronger for downstream burden: postnatal thalamic functional demand is unproven, part of the operative extracellular stock may persist through harvest, and the closest observed training perturbations in ECM/adhesion/guidance or APP-related biology were transcriptionally quiet in this class.

Because `n_degs` includes the target transcript, the permissive baseline expression makes a single significant `Col25a1` self-transcript call more plausible than a completely silent endpoint, even though self-knockdown is not interpretable as functional knockout strength. I therefore choose the smallest nonzero endpoint:

`predicted_n_degs = 1`
