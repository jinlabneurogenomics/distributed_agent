# Nav3 direct `n_degs` forecast

## Target and endpoint

- Target: `Nav3`, from the declared one-row manifest.
- Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with Wilcoxon
  BH-adjusted `pvals_adj < 0.05`.
- Target outcome handling: used the canonical `Nav3` biology bundle in the
  biology-only view; it exposed in-assay expression reach and source-card
  biology, and did not expose the held-out `Nav3` signature, `n_degs`, labeled
  neighbor outcomes, or calibrated response probabilities.

## Biology used

- `Nav3` is expressed in this focal assayed population: 22,647 of 23,679
  non-target cells expressed it, with mean raw UMI 4.394 and pseudobulk CPM
  275.37.
- The source card points to NAV3 as a neuron navigator family protein that
  binds and stabilizes dynamic microtubules.
- The closest loss evidence is developmental human/zebrafish evidence rather
  than a postnatal mouse thalamic loss test.
- Functional realization during the P16 to P37-P44 experiment is indeterminate:
  the edit should stop new full-length protein supply, but the bundle found no
  target-specific protein half-life, microtubule-residence, or postnatal
  perturbation-to-capacity clock.
- The explicit paralogs `Nav1` and `Nav2` were absent from the declared training
  count table, so I did not use their same-experiment outcomes as comparators.

## Training measurements used

The declared count table for this cell class has 1,674 training perturbations.
It is very sparse:

- 1,205 / 1,674 have `n_degs = 0`;
- 276 / 1,674 have `n_degs = 1`;
- the median is 0, the 75th percentile is 1, the 90th percentile is 2, and the
  95th percentile is 18.

I used present training perturbations in nearby cytoskeletal, microtubule,
kinesin, small-GTPase/neurite, and axon-guidance biology as the empirical
scale:

```tsv
target	n_degs
Map1b	1
Map6	0
Tuba1a	7
Tuba4a	2
Tubb4b	1
Tubb5	1
Dctn1	75
Kif1a	1
Kif1b	0
Kif21a	1
Kif5a	1
Kif5c	1
Cdc42	1
Dock3	0
Kalrn	0
Pak1	1
Pak2	0
Pak3	0
Rac1	0
Dcc	0
Robo1	1
Robo2	0
Sema4d	0
Sema5a	1
Sema6a	0
Slit2	0
```

Across a broader hand-selected cytoskeletal/axon-growth cohort of 35 declared
training genes, the median same-class count was 1. Excluding `Dctn1`, whose
75-DEG dynactin phenotype is much more motor/transport-complex-like than the
large NAV3 microtubule-stabilizing scaffold, the mean count was 0.765 and the
maximum was 7.

The expression Parquet cross-check on the exact
`151 TH Prkcd Grin2c Glut` rows reproduced these counts as the number of rows
with `pvals_adj < 0.05`. For the one-DEG cytoskeletal/axon-growth comparators
above, the only significant gene was their own target transcript. In the full
training set, 237 of the 276 one-DEG perturbations were likewise self-only.

## Synthesis

`Nav3` has enough focal-population expression that a detectable self-transcript
effect is plausible, but its available biology does not point to an essential
RNA-processing, proteostasis, or chromatin-like perturbation that would justify
a large 151-class signature. The developmental and zebrafish loss evidence
raises the prior above a pure null, while the lack of a matched postnatal
timing anchor, indeterminate protein/cytoskeletal stock by 21-28 days, and
near-zero counts for matched axon-growth and cytoskeletal training perturbations
keep the forecast at the self-only floor.

Point prediction: `1`.
