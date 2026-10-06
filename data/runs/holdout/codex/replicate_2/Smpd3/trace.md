# Direct forecast for Smpd3 in 151 TH Prkcd Grin2c Glut

Target: `Smpd3`

Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `p < 0.05`.

## Evidence used

- The canonical Smpd3 biology bundle places the perturbation on neutral sphingomyelinase / ceramide production. SMPD3 is a membrane enzyme with ongoing Golgi/plasma-membrane sphingomyelin-to-ceramide flux, and the functional-stock card calls the enzyme pool likely substantially depleted by the 21-28 day harvest window. That argues that an edited, Smpd3-expressing cell can lose the intended molecular activity.
- The same bundle also makes the context match partial rather than exact. Its positive loss evidence is germline hypothalamic postnatal growth-axis dysfunction and much later adult neuronal proteostasis pathology, while matched acute P16-to-P37/P44 thalamic-neuron timing is unresolved. The exact in-assay focal expression is present but diluted: Smpd3 is detected in 9,214 of 23,679 matched non-target 151-class nuclei, 38.91%, with mean raw UMI 0.591.
- The declared 151-class training count table is strongly zero-inflated: 1,205 / 1,674 training targets have `n_degs = 0`; 1,481 / 1,674 have `n_degs <= 1`; the median is 0 and the 90th percentile is 2.
- The represented acute lipid, sphingolipid, and lysosome-adjacent training perturbations in the same class were nearly all silent:

  | target | 151-class n_degs |
  | --- | ---: |
  | Asah1 | 0 |
  | Cert1 | 0 |
  | Sphk1 | 0 |
  | Sptlc2 | 1 |
  | Lamp2 | 0 |
  | Ppt1 | 1 |
  | Abca1 | 0 |
  | Abca7 | 0 |
  | Pld3 | 1 |

- Direct parquet inspection of those nine targets in the focal class showed that the three one-hit calls were only self-transcript depletion: `Pld3`, `Ppt1`, and `Sptlc2`. None had a non-self downstream gene at `pvals_adj < 0.05` in the requested class.
- Same-experiment corpus summaries, interpreted as the semantic layer of the same experiment rather than replication, also describe acute Asah1, Cert1, Sphk1, Ppt1, Abca7, Pld3, Lamp2, and Sptlc2 as buffered or pathway-uncoupled at the nuclear transcriptome level.
- A profile comparison restricted to `151 TH Prkcd Grin2c Glut` for the nine lipid/lysosomal candidates found 6 / 9 with no significant features and 3 / 9 in the 1-to-9 significant-feature bucket. Across all 36 pairwise signed-score comparisons, the positive and negative top-tail overlaps were tiny, with medians of 0.025 in both directions, and the only significant-program overlap entries were zero. This supports using these perturbations as a measured quiet boundary, not as a coherent transferable response module.
- Self-transcript significance remains the main route from a downstream-null forecast to `n_degs = 1`. In the full 151-class training table only 319 / 1,674 perturbations had a significant self target at this threshold, and Smpd3 self-knockdown is not inferable from expression alone because the atlas portrait notes that measured target-mRNA loss is not a quantitative guide to functional editing.

## Synthesis

Smpd3 is reachable: its transcript is present in a substantial minority of the focal nuclei, and the enzyme stock should turn over within the experimental window. The expected effect, though, is an acute loss of a lipid catalyst in a subset of thalamic glutamatergic neurons, not loss of a core transcription, splicing, proteasome, or ribosome factor. The closest measured lipid and lysosomal loss-of-function perturbations in this same class landed at zero downstream DE genes, with one-count outcomes explained by self-target depletion rather than a recurrent cell-state program. The thalamic Smpd3 expression level leaves a plausible chance of a single self hit, but not enough to move the integer point above the zero mode.

Prediction: `0`
