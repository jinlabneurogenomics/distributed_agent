# P2rx2 direct DEG-count forecast

## Evidence used

- Target and endpoint: the one-row holdout manifest names `P2rx2`, and the requested endpoint is `n_degs` in `151 TH Prkcd Grin2c Glut`, i.e. the count of measured genes with Wilcoxon BH-adjusted `p < 0.05`.
- In the exact 151-class non-target expression measurement, `P2rx2` was detected in 167 of 23,679 nuclei, or 0.705%, with 196 total target UMIs, mean raw UMI 0.0083 per nucleus, and pseudobulk CPM 0.519. This is the strongest quantitative point because it says a P2rx2-dependent state should be diluted across an aggregate in which contemporaneous target RNA was observed in well under 1% of recovered nuclei.
- The biology bundle argues that a successful edit should eventually matter in expressing neurons: P2X2 is an ATP-gated cation-channel subunit, existing surface channels are not instantly removed by a disruptive edit, but adult postmitotic-neuron AAV-Cre evidence supports substantial P2X2 protein decline by roughly the 21- to 28-day harvest window. That raises the probability of target realization in P2rx2-positive cells but does not overcome the very narrow exact thalamic reach.
- The declared 151-class training count table has 1,674 non-held-out targets and is highly zero-inflated: 1,205 targets have `n_degs = 0`, 276 have exactly one, and only 193 have two or more.
- The training perturbations closest to a purinergic membrane-receptor/channel mechanism were almost all quiet. `P2ry12` and `P2ry14` both had zero DEGs. In a broader receptor/channel set of 92 `P2ry*`, adrenergic, cannabinoid, dopamine, GABA, glutamate, serotonin, opioid, nicotinic, calcium-channel, sodium-channel, and potassium-channel subunit targets, 69/92 had zero DEGs and the median was zero.
- Direct inspection of the training expression Parquet in the same 151 class confirmed the quietness of specific membrane excitability comparators rather than a table-only artifact: `P2ry12`, `P2ry14`, `Adra1a`, `Adra2a`, `Cacna1a`, `Cacna1d`, `Cacna1e`, `Gria1`, `Gria2`, `Grin2d`, `Htr2a`, and `Kcna1` had zero BH-significant genes; `Scn1a`, `Scn2a`, and `Scn8a` had one each.

## Synthesis

P2rx2 looks functionally editable by P37-P44, but the focal population barely expresses it in the assayed non-target nuclei. A loss-of-function effect restricted to fewer than 1% of nuclei would be averaged across all recovered thalamic glutamatergic nuclei, and the closest training class -- low-burden neuronal receptor and ion-channel perturbations, including the only available purinergic receptors -- overwhelmingly produced no aggregate FDR-significant expression response. I therefore treat a null measured survivor-state signature as the most likely integer outcome and predict:

`n_degs = 0`
