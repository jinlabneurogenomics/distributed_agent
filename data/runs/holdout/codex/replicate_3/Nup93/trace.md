# Direct n_degs forecast for Nup93 in 151 TH Prkcd Grin2c Glut

## Declared target context

- The one-row holdout manifest and canonical biology bundle identify the held-out target as `Nup93`.
- In the exact focal population, the biology bundle reports that `Nup93` is a measured feature with expression in 19,848 of 23,679 matched non-target nuclei, 83.821107% of cells, mean raw UMI 2.335783, and mean CP10K 1.479350. The target is therefore reachable in `151 TH Prkcd Grin2c Glut`; this expression evidence is not an endpoint observation.
- The functional-stock card adjudicates NUP93 as a nuclear-pore inner-ring scaffold/linker in an installed complex. A disruptive edit should stop new synthesis but should not directly remove NUP93 that was already incorporated into assembled nuclear pore complexes before the P16 edit.
- The same card concludes that functional pore-incorporated stock likely persists through the 21-28 day P16 to P37-P44 assay window. The strongest timing evidence is slow NUP93/NUP155/NUP205 scaffold exchange in postmitotic neuronal nuclei, with support from little detectable Nup93 exchange over 14 days in postmitotic mouse myotubes; the closer mature postmitotic mouse loss model is podocyte loss, where overt dysfunction occurs over months rather than weeks.
- The operation is potentially consequential if the lesion is realized: NUP93 has no resolved close mouse paralog and Xenopus depletion/add-back work supports a nonredundant role in forming transport-competent NPCs. The unresolved piece is timing in juvenile thalamic neurons: no direct postnatal mouse neuron Nup93 loss phenotype was identified in the declared source card.

## Same-population training measurements

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` contains 1,674 observed training targets and excludes `Nup93`. In this class the endpoint is sparse:

| quantity | value |
| --- | ---: |
| targets with 0 DEGs | 1205 / 1674 |
| median n_degs | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2677 |

Thus a weakly realized or delayed perturbation should remain at zero or very near zero, whereas counts of tens of DEGs already lie in the upper 5% of the training endpoint.

## Nuclear-pore and transport analogs

The count table has very few direct nuclear-pore or nuclear-transport perturbations. A targeted pass over the declared Parquet in the same `151 TH Prkcd Grin2c Glut` context gave:

| training target | role used in forecast | n_degs, BH < 0.05 | n_degs, BH < 0.10 | min BH q |
| --- | --- | ---: | ---: | ---: |
| `Tpr` | nuclear basket/nucleoporin, high-response upper bound rather than stable inner-ring stock | 1768 | 2262 | 8.44e-17 |
| `Tnpo3` | nuclear transport receptor, high-response transport comparison | 618 | 891 | 2.02e-12 |
| `Ranbp2` | large nucleoporin/cytoplasmic-filament comparison | 0 | 0 | 0.20197 |
| `Kpna3` | importin-alpha comparison | 0 | 0 | 0.16976 |
| `Xpo7` | exportin comparison | 0 | 0 | 1 |

The Parquet and count table are two views of the same training experiment, so this is not replication. The exact rows were useful for separating two facts: (i) disruption of selected transport-related genes can produce a very large thalamic transcriptional state, as in `Tpr` and `Tnpo3`; but (ii) pore or transport identity alone does not imply a nonzero response, as `Ranbp2`, `Kpna3`, and `Xpo7` had no significant genes even at BH < 0.10. The strongest large responder, `Tpr`, is a basket component rather than the long-lived NUP93 inner-ring scaffold, so I did not transfer its 1768-DEG state to Nup93.

## Synthesis

The forecast rests on two opposing signals. `Nup93` is expressed broadly enough in the assayed thalamic nuclei, encodes a nonredundant NPC scaffold, and could matter if new pore assembly or maintenance becomes limiting after editing. Against that, the operative NUP93 stock is mostly pre-installed by P16 and is specifically expected to persist in postmitotic cells across the 21-28 day window. The task-matched count distribution makes zero the dominant prior class, and the training analogs do not show that every nuclear transport perturbation escapes that sparse baseline.

I therefore used the modal low-response outcome rather than a `Tpr`-like high-footprint transfer.

Predicted `n_degs`: **0**
