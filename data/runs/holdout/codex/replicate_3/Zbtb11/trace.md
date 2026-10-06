# Zbtb11 direct n_degs forecast

Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with Wilcoxon `pvals_adj < 0.05`.

Target identity and target biology:

- The one-row manifest names `Zbtb11`.
- In the supplied biology bundle, this packet follows GeneID 68193 / ENSMUSG00000098274: historical `Zbtb11`, current `Rpl24`, encoding ribosomal protein eL24 of the cytosolic 60S subunit. I therefore ignored current-Zbtb transcription-factor family neighbors.
- Exact non-target expression in the focal population was available and strong enough for the endpoint: `mean_raw_umi = 1.2465`, `mean_cp10k = 0.7720`, `pseudobulk_cpm = 78.12`, and `15795 / 23679 = 66.7%` non-target nuclei expressing the feature.
- The functional-stock card judged operative RPL24-bearing ribosome stock likely substantially depleted by the P37-P44 harvest. The reason was not immediate destruction of old ribosomes: editing stops new RPL24 supply, while mature pre-edit ribosomes initially persist. The 21-28 day assay interval spans several average ribosomal-protein lifetimes, with ongoing neuronal Rpl24 synthesis and mature-ribosome exchange supporting postnatal demand but leaving a long-lived residual tail.

Training count table context:

- The declared training table for this focal class has 1674 measured targets. It is zero-heavy: 1205 rows have `n_degs = 0`, median 0, 75th percentile 1, 90th percentile 2, 95th percentile 18, 99th percentile 430, and mean 14.05.
- Close translation/ribosome-biology counts were small to modest at the exact requested threshold:

| measured target | focal `n_degs` |
|---|---:|
| `Nop56` | 25 |
| `Eef2` | 9 |
| `Ddx3x` | 8 |
| `Eif4a2` | 2 |
| `Eif4g1` | 1 |
| `Eif4h` | 1 |
| `Eif5a` | 0 |
| `Las1l` | 0 |

Measured profile evidence:

- The focal Parquet rows exactly reproduced the count table for the selected analogs. `Nop56` had 25 focal DEGs, split 10 up and 15 down; the significant set included a mostly negative RNA-processing branch with `Rsrp1`, `Ddx17`, `Srsf5`, `Srsf11`, `Tcea2`, `Ddx5`, `Srsf6`, `Pabpn1`, and `Clk4`, plus a significant self row.
- `Eef2` had only 9 focal DEGs despite a direct translation-elongation role.
- `Ddx3x` had 8 focal DEGs, and cap-initiation/elongation relatives were nearly null in this cell class.
- A symmetric profile comparison of `Nop56`, `Eef2`, `Ddx3x`, `Las1l`, `Eif4a2`, `Eif4g1`, `Eif4h`, `Eif5a`, and high-response boundary signatures showed low overlap in significant programs among the close low-burden translation/ribosome cohort. Directional cohesion across those 28 pairs had mean significant-program overlap coefficient 0.0 for positive changes and 0.0167 for negative changes. This made a single shared translation-failure DEG count unsupported.

Same-experiment corpus context for measured comparators:

- `Nop56:F001` reports that `Nop56` loss was narrow across neurons and concentrated in `151 TH Prkcd Grin2c Glut`.
- `Nop56:F002` reports that its focal response was dominated by the negative SR-splicing/RNA-processing branch, not just a generic rRNA-maturation output.
- `Nop56:F005` reports absence of a canonical nucleolar-stress, p53/apoptosis, ISR, or autophagy program in surviving focal neurons, with comparison to very high-burden `Uba5` and `Ufc1`.
- `Las1l:F001` shows that another large-subunit biogenesis factor was completely FDR-null across recovered postnatal neurons.
- `Eef2:F009` and `Ddx3x:F005` show that represented cytoplasmic translation-control perturbations did not phenocopy one another or form a generic shared mRNA response.

Forecast synthesis:

`Nop56` is the most relevant measured upper anchor because it is a nucleolar 60S/ribosome-biogenesis perturbation with a real focal response, but its 25 DEGs include a branch toward SR-splicing/Tnpo3-like RNA handling that is not a direct consequence of losing mature RPL24. `Las1l`, `Eef2`, and the eIF targets pull the estimate downward because direct translation and 60S-biogenesis perturbations were often buffered or survivor-conditioned to 0-9 focal DEGs. I upweighted from those near-null values because RPL24 is part of the mature ribosome itself, is strongly detected in the focal population, and should lose most renewable operative stock during the 21-28 day interval. I excluded `Uba5`, `Ufc1`, `Tnpo3`, `Rnpc3`, and `U2af2` as scale anchors: they help interpret downstream modules but sit on UFMylation, SR-import, or broad RNA-processing branches with hundreds to thousands of DEGs, not on the direct RPL24 perturbation.

Point prediction: a modest but clearly nonzero focal signature, slightly below the `Nop56` upper analog and around the 95th percentile of the whole zero-inflated training table.

Predicted `n_degs = 18`.
