# Apc DEG-count forecast

## Target and endpoint

- Target: `Apc`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with Wilcoxon BH-adjusted `p < 0.05`
- Prediction: `64`

## Evidence used

The target biology bundle supports real perturbation reach in the assayed cells. `Apc` is measured in `22,354 / 23,679` non-target nuclei in `151 TH Prkcd Grin2c Glut` (`94.4043%`; mean raw UMI `3.7946`; mean log1p CP10k `1.1210`), so a sparse or absent response would not be explained by lack of baseline target RNA in this population.

The same bundle adjudicates full-length APC stock as `likely_substantially_depleted` by P37-P44 after a P16 disruptive edit. The supporting card evidence is only partial, because pre-existing protein is not instantly removed and stable N-terminal fragments can persist, but the direct postmitotic-neuron conditional model plus dynamic APC pools point toward appreciable loss of full-length APC function during the 21-28 day assay window.

Functionally, the relevant operation is not simple Wnt effector loss. APC restrains canonical Wnt/beta-catenin signaling and also scaffolds microtubule, adhesion, centrosomal, and synaptic pools. Therefore Apc loss should be able to reach the thalamic beta-catenin/TCF state, but its sign is expected to be Wnt activation or derepression, opposite to `Ctnnb1` or `Tcf7l2` loss for the canonical feedback arm.

The declared 151-count training table is highly sparse: among 1,674 training targets, the median is 0 DEGs, the 75th percentile is 1, the 95th percentile is 18, and only a small tail exceeds 100. The measured Wnt/catenin entries in the table split sharply:

| training target | n_degs in 151 |
| --- | ---: |
| `Ctnnb1` | 383 |
| `Tcf7l2` | 106 |
| `Csnk2b` | 25 |
| `Gsk3b` | 6 |
| `Lrp6` | 4 |
| `Lrp5`, `Fzd2`, `Fzd4`, `Fzd6`, `Fzd9`, `Kremen1`, `Prickle1`, `Macf1`, `Ctnna2`, `Ctnna3` | 0 |

The same-experiment corpus Findings refine those counts without adding independent replication. `Ctnnb1:F002` and `Ctnnb1:F007` report that beta-catenin loss recovers a canonical Wnt-feedback and thalamic excitability/adhesion state and that only `Lrp6` and `Tcf7l2` converge with `Ctnnb1` among represented Wnt/catenin relatives. `Tcf7l2:F004` reports same-direction `Ctnnb1`/`Tcf7l2` convergence in 151. `Gsk3b:F005` reports that isolated `Gsk3b` loss did not induce canonical Wnt/beta-catenin transcription despite strong `Ctnnb1`/`Tcf7l2` detectability. `Lrp6:F003` reports a weak but same-direction Axin2-containing overlap between `Lrp6` and `Ctnnb1`.

I checked the declared parquet directly at the requested FDR threshold. In `151 TH Prkcd Grin2c Glut`, `Ctnnb1` has 383 DEGs, 100 up and 283 down; `Tcf7l2` has 106, 39 up and 67 down; `Gsk3b` has 6; and `Lrp6` has 4. `Ctnnb1` and `Tcf7l2` share 44 significant genes, 40 with the same sign. `Ctnnb1` and `Lrp6` share 4, all same sign. `Ctnnb1` and `Gsk3b` share only 1. Canonical readouts such as `Axin2`, `Lef1`, `Notum`, `Wnt9b`, and `Vangl1` are down after `Ctnnb1` loss but are not FDR-significant after `Gsk3b` loss at this threshold.

## Synthesis

`Apc` should not be collapsed onto the quiet receptor-level rows. Unlike single Frizzled receptors or `Lrp5`, it is an intracellular destruction-complex scaffold with broad measured expression in the exact focal population and literature support for postmitotic-neuron APC depletion affecting beta-catenin/Wnt and synaptic biology on a within-weeks scale. That pushed the forecast well above the zero-to-singleton Wnt relatives and above `Gsk3b`, whose weak response is plausibly buffered by `Gsk3a` and by its many beta-catenin-independent substrates.

I also kept `Apc` below the `Tcf7l2`/`Ctnnb1` effector-loss counts. Loss of beta-catenin or TCF7L2 directly removes the transcriptional arm that maintains the 151 thalamic terminal state, producing 106-383 DEGs. Removing APC should derepress beta-catenin rather than remove it, and APC2 compensation, stable edit-produced fragments, pool-specific scaffold functions, and survivor-conditioned recovery all make the nuclear RNA footprint likely smaller and less perfectly aligned than direct effector loss.

Those two constraints place `Apc` in a moderate Wnt-response regime: clearly nonzero and above the low one-digit upstream controls, but below the 106-DEG `Tcf7l2` effector anchor. I used a point of **64 DEGs**, roughly two-thirds of the `Tcf7l2` count and far below the broader `Ctnnb1` response, to represent a central but sign-opposite APC lesion with partial compensation and fragment caveats.
