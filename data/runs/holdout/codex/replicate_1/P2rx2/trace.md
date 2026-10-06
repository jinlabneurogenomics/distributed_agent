# Direct n_degs forecast for P2rx2 in 151 TH Prkcd Grin2c Glut

## Prediction

`P2rx2`: **0** BH-adjusted Wilcoxon DEGs at `pvals_adj < 0.05`.

## Evidence used

- **Declared biology bundle:** `P2rx2` encodes an extracellular-ATP-gated P2X cation-channel subunit. The perturbation is expected to stop new functional P2X2 production, and adult postmitotic-neuron evidence supports substantial receptor-stock decline over a 21+ day window, so the edit itself is biologically meaningful when it lands in P2X2-dependent cells.
- **Exact focal-population reach:** in non-target `151 TH Prkcd Grin2c Glut` nuclei, `P2rx2` is extremely rare: 196 total UMIs across 23,679 nuclei, 167 expressing nuclei, `0.705%` cells expressing, mean raw UMI `0.00828`, and pseudobulk CPM `0.519`.
- **P2rx2 same-experiment corpus context:** the packaged July-260713 corpus release has no `P2rx2` Claims, no `P2rx2` Findings, and no explicit Finding-reference comparators, so there was no release-declared P2rx2 response story to transfer from.
- **Training count scale:** the declared `151 TH Prkcd Grin2c Glut` count table contains 1,674 observed training perturbations; 1,205 have `n_degs = 0`, the median is `0`, 1,481 have `n_degs <= 1`, and 1,546 have `n_degs <= 5`. Large DEG burdens are rare and mostly broad nuclear/proteostasis regulators.
- **Closest training perturbations:** the only purinergic-receptor perturbations present in the count table, `P2ry12` and `P2ry14`, both have `0` DEGs. Direct Parquet aggregation in the matched focal class also returned `0` significant rows for `P2ry12` and `P2ry14`, with minimum adjusted p-values of `1.0`.
- **Receptor/channel reference scale:** among 91 training targets in a receptor/channel slice matching prefixes such as `Grin`, `Gria`, `Grik`, `Gabr`, `Kcn`, `Scn`, `Cacn`, `Chr`, `Drd`, `Htr`, and `P2ry`, 67 had `0` DEGs. A few broadly used channels had nonzero outputs, led by `Grin1` with 89 and `Cacna1g` with 12, but those are poor scale donors for a transcript detected in under 1% of the focal non-target cells.

## Reasoning

The functional-stock card keeps `P2rx2` from being treated as an editing null: successfully edited P2X2-expressing neurons should lose new receptor supply by the P37-P44 harvest. The bottleneck for this endpoint is instead population reach. The requested count is aggregated over the thalamic glutamatergic class; only 0.705% of the matched non-target nuclei have any observed `P2rx2` RNA, and the total target UMI burden is tiny. That makes even a real electrophysiological effect likely to be diluted below class-level Wilcoxon/FDR detection unless `P2rx2` marks a rare substate with a very large, coherent transcriptomic shift.

The declared training outcomes put such receptor-like perturbations on the quiet end of the scale in this population. The two available purinergic GPCRs are exactly zero, most receptor/channel perturbations are zero, and the nonzero ion-channel cases involve much broader glutamatergic machinery than a rare P2X2 ATP receptor. I therefore expect the held-out `P2rx2` contrast to land at the mode of the training distribution rather than in the small positive tail.
