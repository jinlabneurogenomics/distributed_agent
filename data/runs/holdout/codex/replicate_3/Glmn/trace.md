# Glmn n_degs forecast

## Requested target

The one-row holdout manifest names `Glmn` as the target for `151 TH Prkcd Grin2c Glut`. `Glmn` is absent from the declared 1,674-row focal count table, so its TH `n_degs` value was not available in the training counts used for the forecast.

## Direct target biology

- In the exact focal population, `Glmn` is detectably expressed: 17,055 of 23,679 non-target cells express it, or 72.03%, with mean expression 0.905 CP10k. I treated this as evidence that the target is reachable in the sampled TH neurons, not as evidence for a large response.
- The perturbation card defines GLMN as a soluble RBX1-binding regulator of cullin-RING ligases. A disruptive edit should stop new GLMN supply, but available evidence did not resolve GLMN protein half-life, RBX1 residence, or whether the relevant functional stock is depleted by the P37-P44 harvest after a P16 edit.
- Mouse loss evidence is embryonic and dominated by vascular failure; it does not establish an acute postmitotic thalamic-neuron requirement. The card found no close mouse paralog, which weakly supports possible observability, but pathway-level CRL buffering remains untested.

## Training measurements used

The focal TH training count table is highly zero-inflated:

- rows: 1,674 training perturbations
- `n_degs = 0`: 1,205
- `n_degs > 0`: 469
- median: 0
- 75th percentile: 1
- 90th percentile: 2
- arithmetic mean: 14.05, inflated by rare large responders such as `Uba5`, `Tpr`, and `Sin3a`

I therefore interpreted a forecast of 1-2 genes as a weak but detectable response, not as a full null.

The Glmn analogue search over the exact 1,674-gene training universe found no exact GLMN paralog or direct RBX1/CUL1 target in the count table. The nine direct-interaction or CRL-side nominees that were available had the following TH counts:

| target | n_degs |
| --- | ---: |
| Arih1 | 7 |
| Crbn | 0 |
| Dcaf8 | 0 |
| Ddb2 | 0 |
| Depdc5 | 13 |
| Kbtbd7 | 0 |
| Klhl20 | 0 |
| Klhl7 | 0 |
| Lztr1 | 1 |

Additional same-assay F-box, RING, and ubiquitin-conjugation comparators were also mostly silent:

| target | n_degs |
| --- | ---: |
| Fbxo11 | 1 |
| Fbxo38 | 0 |
| Fbxw7 | 1 |
| Rnf216 | 0 |
| Rnf220 | 0 |
| Ube2e2 | 0 |
| Ube3a | 0 |

Same-experiment corpus findings gave the same picture. `Fbxw7` produced only a single significant TH downstream gene and did not recover canonical FBXW7 substrate-output transcriptional programs in postnatal neurons. `Arih1` produced a restricted 151 TH response, but corpus review explicitly found that it did not simply phenocopy broad proteotoxic collapse and that represented E3-ligase-family comparators did not share its 14-feature response across measured groups.

I also compared these CRL/F-box nominees directly in the declared Parquet for `151 TH Prkcd Grin2c Glut`. The induced report topology over the 16 narrow nominees was sparse, with 13 of 120 possible explicit-Finding pairs connected and no shared-Claim pairs. Pairwise TH profiles around `Arih1` and `Fbxw7` had essentially no FDR-program overlap with the quiet Cul4/KLHL/F-box peers; for example, `Arih1` versus `Klhl20`, `Kbtbd7`, `Lztr1`, `Klhl7`, `Ddb2`, `Crbn`, `Dcaf8`, `Fbxo11`, or `Fbxo38` had zero same-direction significant intersections in the bounded inspection.

Broad proteostasis perturbations define a much higher endpoint scale in this same cell class (`Uba5` 2,677, `Psmb4` 742, `Psmc1` 430), but I treated them as upper-state context rather than direct GLMN magnitude donors. GLMN loss removes an RBX1/CRL inhibitor rather than the proteasome, UFMylation, or endolysosomal machinery itself, and the closest same-experiment E3/CRL perturbations remained sparse or null.

## Synthesis

The exact TH expression argues against a pure absence-of-target explanation, and lack of a known paralog leaves some room for a detectable response. The strongest downward evidence is that loss of available CRL/F-box/E3 relatives at the same P16-to-P37/P44 endpoint was usually 0 or 1 DEG, with only sparse `Arih1` and `Depdc5` responses among the direct nominees and no coherent CRL-wide TH signature. Unknown GLMN turnover and the developmental/vascular nature of the mouse null further prevent assigning the large proteostasis scale.

I therefore placed `Glmn` just above the zero/one direct-comparator mass and far below the broad proteostasis tail, at **2 BH-significant genes**.
