# Cox6b1 forecast for `151 TH Prkcd Grin2c Glut`

## Prediction

`Cox6b1` -> `0` DEGs at BH-adjusted Wilcoxon `p < 0.05`.

## Evidence used

- Target identity came from the one-row manifest `Cox6b1.csv` and the matched biology-only bundle `Cox6b1.json`; the declared training endpoint was `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- The Cox6b1 bundle places the perturbation on an installed nuclear-encoded complex-IV subunit. The relevant stock prior is that a P16 disruptive edit should halt new Cox6b1 supply while pre-edit complex IV persists until respiratory-complex turnover, with COX6B1 in a shorter-lived primary-neuron mitochondrial class but partly stabilized in supercomplexes. The exact focal-population reach is real but modest: in non-target `151 TH Prkcd Grin2c Glut` nuclei, Cox6b1 had mean raw UMI 0.591 and was detected in 9,769 of 23,679 nuclei, 41.26%.
- Same-experiment corpus Finding/Claim evidence for observed training genes described a high-confidence buffered complex-IV class: `claim:e55eeb96f3be73714a12` reports that represented Complex IV structural subunits and assembly-associated genes were broadly flat or singleton at the neuronal nuclear-RNA level rather than forming a recurrent cytochrome-c-oxidase-loss or mitochondrial-stress program. Its directly relevant training contributors included `Cox4i1:F003`, `Cox5a:F002`, `Cox6a1:F003`, `Cox7b:F003`, with `Coa8`, `Cox11`, `Cox8a`, and `Ndufa4` in the same shared-claim component.
- Endpoint-matched training counts in `151 TH Prkcd Grin2c Glut` for that eight-target Complex IV/Ndufa4 cohort were:

  | target | n_degs |
  | --- | ---: |
  | Coa8 | 0 |
  | Cox11 | 0 |
  | Cox4i1 | 0 |
  | Cox5a | 1 |
  | Cox6a1 | 0 |
  | Cox7b | 0 |
  | Cox8a | 0 |
  | Ndufa4 | 1 |

  The two nonzero entries were single self-transcript calls in the Parquet, `Cox5a` and `Ndufa4`, not multi-gene downstream states in 151.
- The broader respiratory-chain and mitochondrial-proteostasis slice available in the same count table was also almost point-null after excluding the distinct Opa1 mitochondrial-architecture stressor: 44 queried Cox/Nduf/Uqcr/Sdha/COA/Lrpprc/TIMM/TOMM/mitochondrial-protease targets all had `n_degs <= 1`, with 28 at zero and a mean of 0.36.

## Reasoning

The Cox6b1 biology argues against dismissing the perturbation as irrelevant: it is broadly expressed enough to be targeted in this class, Cox6b2 is not a plausible broad thalamic substitute, and respiratory-complex turnover over 21-28 days should erode some installed COX6B1. The uncertainty is that the loss is acute, mosaic, survivor-conditioned, and read out only as nuclear RNA in postmitotic neurons; even realized biochemical impairment need not become a broad FDR-level transcriptional response.

The strongest endpoint-matched analogs are therefore not general high-impact essential genes, but the nuclear respiratory-chain subunits already measured under the same P16-to-P37/P44 design. They overwhelmingly produced either no corrected 151 DE genes or only their own depleted transcript. Cox5a is especially informative because its own mRNA was strongly visible yet did not create downstream DE in 151.

I therefore put Cox6b1 in the same buffered structural complex-IV/OXPHOS regime. A count of one is plausible if the Cox6b1 transcript itself happened to cross FDR, but target-transcript loss is not predictable from the biology bundle and is not evidence for stronger downstream action. The modal and median outcome for the matched structural-complex-IV cohort is zero, so the integer point forecast is:

```tsv
target_name	predicted_n_degs
Cox6b1	0
```
