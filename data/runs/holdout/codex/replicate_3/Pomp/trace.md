# Pomp n_degs forecast for 151 TH Prkcd Grin2c Glut

## Endpoint

Target: `Pomp`.

Predicted endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with Wilcoxon BH-adjusted `pvals_adj < 0.05`.

I used the declared biology-only `Pomp` bundle, the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` training count table, and a filtered extract of the declared `training_de_all_cell_groups.parquet`. I did not use scalar-prior, calibrated-probability, relationship-review, branch-calibration, or terminal-prediction artifacts.

## Biology of the held-out perturbation

The `Pomp` bundle places POMP upstream of 20S proteasome core biogenesis: POMP is an assembly chaperone for standard and immunoproteasome 20S cores, is present in precursor particles rather than mature 20S cores, and is consumed during core maturation. It therefore has a real latency that a structural proteasome failure need not have: editing `Pomp` should stop resupply of newly assembled cores but should not instantly inactivate already mature proteasomes.

That latency is bounded, not indefinite. The same bundle adjudicates the functional stock at harvest as `likely_substantially_depleted`; the P16-to-P37/P44 window is 21-28 days, substantially longer than the 27 h and 133 h mature-core half-lives measured in human T2-derived cell pulse-chase experiments. The bundle still keeps timing uncertainty because those half-lives are not juvenile mouse thalamic-neuron measurements.

The focal thalamic population has enough `Pomp` transcript for perturbation reach to be plausible: in the exact non-target expression measurement, `Pomp` was detected in 13,943 of 23,679 matched non-target nuclei, 58.883% expressing, with mean CP10K 0.6251 and pseudobulk CPM 62.14. The bundle found no close mouse paralog for `Pomp`, so compensation by a duplicate assembly chaperone is not the obvious explanation for a null.

## Training measurements that set the scale

The declared focal count table contains 1,674 training perturbations. It is sparse overall: 1,205 have 0 DEGs in this cell class, the median is 0, the 75th percentile is 1, the 95th percentile is 18, and the 99th percentile is 430. So a three-digit prediction requires a direct reason; broad essentiality alone is not enough.

The closest direct measured anchors are the two structural 26S proteasome perturbations in the table:

| training perturbation | focal `n_degs` |
|---|---:|
| `Psmb4` | 742 |
| `Psmc1` | 430 |

The same-experiment reports support treating these as a specific proteasome-failure state rather than unrelated large stressors. `Psmb4:F007` reports that `Psmc1` was the top data-driven neighbor of `Psmb4` and that 5,107 of 5,113 shared significant sparse features across the screen agreed in sign. `Psmc1:F007` reciprocally reports `Psmb4` as the only strong positive `Psmc1` signature neighbor. In my exact `151 TH Prkcd Grin2c Glut` Parquet slice at the task threshold, `Psmb4` and `Psmc1` shared 215 significant measured genes with the same log-fold-change sign and 0 with opposite sign.

Adjacent proteostasis nodes were much weaker in the same endpoint:

| training perturbation | focal `n_degs` | interpretation |
|---|---:|---|
| `Nfe2l1` | 0 | proteasome bounce-back regulator, but basal LoF was flat |
| `Nfe2l2` | 0 | related oxidative-stress regulator, flat |
| `Vcp` | 2 | UPS/autophagy/ERAD accessory node, flat |
| `Hspa5` | 5 | BiP/ER stress was detectable but small at FDR < 0.05 |
| `Sec63` | 11 | ER chaperone cofactor, small |
| `Atg5` | 0 | core autophagy lipidation component, flat in 151 |
| `Becn1` | 0 | autophagy/endosome scaffold, flat in 151 |

These are downward guards: they show that not every proteostasis or UPR component phenocopies the 20S/19S core signatures. For POMP, though, they are weaker analogues than `Psmb4` and `Psmc1` because POMP is a dedicated, required supplier of the 20S core itself.

I treated very high nonspecific stress profiles as upper context rather than direct scale donors. `Uba5`, `Tpr`, `U2af2`, `Ufc1`, and `Prpf6` had 2,677, 1,768, 828, 572, and 454 focal DEGs, respectively, but they do not block 20S assembly. Their large burdens confirm that this class can return hundreds to thousands of DEGs, but they do not supersede the specific proteasome anchors.

## Point synthesis

`Pomp` should be much closer to the structural proteasome pair than to flat basal regulators such as `Nfe2l1`, `Vcp`, or `Atg5`: loss of POMP removes new 20S core assembly, the exact target transcript is present in the assayed thalamic population, no paralog was found, and the screen has a strong recurrent 20S/19S proteasome-loss signature in the same cell class.

I discounted below `Psmb4` and just below `Psmc1` because POMP is not part of mature proteasomes; pre-existing mature cores remain initially functional, and the 21-28 day stock-depletion inference rests on non-neuronal core half-lives. Survivor-conditioned sampling could also preferentially retain partially edited or better-buffered nuclei after a proteasome-assembly lesion.

Those bearings put the forecast far above the focal median and the `Nrf1`/UPR range, but below the direct structural pair:

`predicted_n_degs = 416`
