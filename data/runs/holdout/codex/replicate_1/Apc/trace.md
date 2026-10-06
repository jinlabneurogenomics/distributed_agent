# Apc DEG-count forecast for `151 TH Prkcd Grin2c Glut`

## Inputs used

- Target: `Apc`, from the one-row holdout manifest.
- Endpoint: `n_degs`, the number of measured genes in `151 TH Prkcd Grin2c Glut` with Wilcoxon BH-adjusted `p < 0.05`.
- Direct target profile/outcome: absent from the declared count table and parquet; I did not query or reconstruct it.
- Biology bundle: canonical endpoint-blind `Apc` bundle, including exact in-assay target expression reach.
- Training measurements: declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` and matched rows from `training_de_all_cell_groups.parquet`.
- Same-experiment corpus: used only for training genes in the WNT/catenin neighborhood, to interpret the measured `Ctnnb1`, `Tcf7l2`, `Lrp6`, and `Gsk3b` responses.

## Quantitative anchors

The 151-class training distribution is highly zero-inflated:

- 1,674 training perturbations.
- 1,205 have `n_degs = 0`.
- Median = 0.
- 90th percentile = 2.
- 95th percentile = 18.
- 99th percentile = 430.

So an `Apc` forecast should stay at zero unless the biology plausibly reaches this neuronal endpoint within the 21-28 day assay window.

The measured WNT/catenin neighborhood available in the count table is sparse but informative:

| training target | `n_degs`, BH `p < 0.05` | interpretation for `Apc` |
| --- | ---: | --- |
| `Ctnnb1` | 383 | strong central beta-catenin/adhesion effector response in the exact focal class |
| `Tcf7l2` | 106 | a narrower but still broad WNT/TCF thalamic response |
| `Lrp6` | 4 | receptor-level LRP6 loss reaches only a tiny Axin2-containing state |
| `Gsk3b` | 6 | core destruction-complex-adjacent loss is weak and does not reproduce the Ctnnb1/Tcf7l2 canonical output |

Other represented receptor/catenin relatives named in the `Ctnnb1`/`Lrp6` training reports were essentially null in this exact endpoint: `Lrp5`, `Fzd2`, `Fzd4`, `Fzd6`, `Fzd9`, `Lgr4`, `Gpc6`, `Ctnna2`, `Ctnna3`, `Ror1`, `Ror2`, `Ryk`, `Macf1`, `Prickle1`, `Zic2`, and `Kremen1` had `0` focal-class DEGs, `Ctnnd2` and `Peg3` had `1`, and `Gsk3b`/`Lrp6` were single-digit.

The focal-class profile comparison over those 22 measured WNT/catenin-adjacent nodes recapitulated the same split:

- `Ctnnb1`: 383 significant features, 100 positive and 283 negative.
- `Tcf7l2`: 106 significant features, 39 positive and 67 negative.
- `Lrp6`: 4 significant features, 1 positive and 3 negative.
- `Gsk3b`: 6 significant features, 1 positive and 5 negative.
- Sixteen of the 22 profiled WNT/catenin-adjacent nodes had no significant features.

At `p_adj < 0.05`, `Ctnnb1` and `Tcf7l2` shared 40 same-direction significant features with 4 direction conflicts, while `Ctnnb1` and `Lrp6` shared all 4 of the tiny `Lrp6` significant set in the same direction. This agrees with the packaged training interpretation: the 151-class beta-catenin/TCF state is detectable and centered on `Ctnnb1`/`Tcf7l2`, but it is branch-specific rather than a response produced by any WNT-labeled perturbation.

## Apc biology bearing on the scalar point

`Apc` is well within expression reach in the exact focal class: 22,354 of 23,679 matched non-target nuclei expressed the transcript, or 94.4%, with mean raw UMI 3.79 and pseudobulk CPM 237.8. The functional-stock card judges full-length APC likely substantially depleted by P37-P44 because a disruptive edit should stop full-length resupply, APC participates in dynamic beta-catenin-regulatory and cytoskeletal/synaptic scaffold pools, and a direct early-postnatal postmitotic-neuron conditional model showed molecular and synaptic consequences on an approximately month-long horizon.

Those points make a silent `Apc` outcome less likely than the training-set median. `Apc` is not merely a WNT receptor paralog: it is a central destruction-complex scaffold whose loss should derepress beta-catenin and can also affect adhesion, microtubules, and synaptic complexes.

The reasons not to transfer the full `Ctnnb1` or `Tcf7l2` count are also strong:

- The training perturbations measure loss of beta-catenin/TCF output; `Apc` loss should push the pathway in the opposite, beta-catenin-stabilizing direction.
- The focal training data show that basal thalamic WNT output is narrow for several upstream/core perturbations, including `Lrp6 = 4` and `Gsk3b = 6`.
- APC2 paralogy, stable N-terminal APC fragments, and pool-specific APC turnover weaken exact projection from full `Apc` knockout literature to sparse P16 CRISPR in recovered thalamic nuclei.
- The exact one-month neuronal conditional evidence is forebrain-biased rather than a direct 151 TH Prkcd Grin2c Glut measurement.

I therefore placed `Apc` above the tiny `Lrp6`/`Gsk3b` receptor-core observations but well below the direct loss-of-output `Tcf7l2` and `Ctnnb1` responses. The point estimate is a moderate WNT/adhesion/cytoskeletal response in the upper few percent of the training distribution:

```tsv
target_name	predicted_n_degs
Apc	64
```
