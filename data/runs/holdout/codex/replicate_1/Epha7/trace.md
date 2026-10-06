# Epha7 n_degs prediction

## Target and endpoint

- Target: `Epha7`, the single target declared by the one-row holdout manifest.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: total measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in this cell class. The training count table's endpoint includes the perturbed transcript itself when it passes FDR; it is not restricted to downstream genes.
- Outcome-blind inputs used:
  - `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
  - `training_de_all_cell_groups.parquet`
  - the declared Epha7 canonical biology bundle exposed through `characterization_bundle(view="biology")`
  - same-experiment corpus Findings and Claims for measured Eph-family comparators, not for the held-out Epha7 outcome

## Empirical count scale in the matched cell class

The focal training table contains 1,674 measured training perturbations and does not contain `Epha7`. Its count distribution is dominated by exact zeros:

| summary | value |
|---|---:|
| mean `n_degs` | 14.05 |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| max | 2,677 |

Count bins:

| bin | targets |
|---|---:|
| `0` | 1,205 |
| `1-5` | 341 |
| `6-20` | 50 |
| `21-100` | 36 |
| `>100` | 42 |

The large arithmetic mean is therefore driven by a small tail of broad machinery and stress-like perturbations rather than by the typical target in `151 TH Prkcd Grin2c Glut`.

## Matched Eph-family and proximal-pathway evidence

The represented EphA/EphB receptor perturbations in the focal count table were:

| target | focal `n_degs` |
|---|---:|
| `Epha10` | 0 |
| `Epha2` | 0 |
| `Epha3` | 0 |
| `Epha4` | 1 |
| `Epha5` | 0 |
| `Ephb1` | 0 |
| `Ephb2` | 0 |
| `Ephb4` | 0 |

Direct parquet aggregation in `151 TH Prkcd Grin2c Glut` separated total FDR hits from downstream hits for these Eph receptors plus proximal Eph/Rho/Pak/MAPK/PI3K comparators:

- All 21 selected Eph/proximal nodes had **0 downstream genes** at `pvals_adj < 0.05` and also 0 downstream genes at `pvals_adj < 0.10` in the focal cell class.
- `Epha4`, `Cdc42`, and `Pak1` each had a total focal count of 1, consistent with a self-only or singleton count rather than a propagated downstream program.
- Across all 23 profiled cell classes, the selected Eph/proximal set produced only four downstream BH < 0.05 singleton events: `Epha4` in `053 Sst Gaba`, `Epha5` in `012 MEA LA CA1 DG Glut`, `Ephb1` in `308 CB GABA`, and `Rac1` in `053 Sst Gaba`.

I also profiled the exact focal Eph-receptor cohort `Epha2,Epha3,Epha4,Epha5,Epha10,Ephb1,Ephb2,Ephb4` against the raw signed Wilcoxon vectors. In the matched `151 TH Prkcd Grin2c Glut` comparison:

- 7 of 8 receptors had `no_significant_features`.
- 1 of 8 had `1_to_9_significant_features`.
- Across 28 receptor pairs, the positive-tail overlap coefficient averaged 0.0305 and the negative-tail overlap coefficient averaged 0.0245.
- No pair had any significant-program overlap to quantify.

That profile comparison supports the same conclusion as the count table: represented Eph receptors do not form a coherent high-yield focal thalamic RNA state.

## Packaged same-experiment comparator interpretation

The Epha4 report is the closest measured family analogue because Epha4 overlaps Epha7 in developing thalamic domains. Its packaged Findings state that:

- five groups showed significant `Epha4` mRNA depletion but no downstream genes, including the thalamic `151 TH Prkcd Grin2c Glut` and `155 MB Glut` groups;
- represented Eph receptors and Rho/Pak actin nodes did not phenocopy `Epha4`;
- single represented Eph receptor perturbations were flat, singleton-only, or receptor-specific rather than instances of a common Eph-family nuclear transcriptomic program.

These Findings are same-experiment interpretations of the training profiles, so I used them as semantic grounding rather than as independent validation.

## Epha7 biology prior

The Epha7 biology bundle says the target is actually reachable in the focal assayed population:

- exact non-target expression in `151 TH Prkcd Grin2c Glut`: `83.466%` expressing nuclei, mean raw UMI `3.206`, mean CP10k `1.967`;
- operative biology: full-length kinase-positive and kinase-negative membrane EphA7 pools;
- functional-stock conclusion: successful P16 editing should stop new receptor production while pre-edit stock persists, and Eph-family surface-receptor turnover makes substantial depletion by the P37-P44 harvest likely;
- observability: germline `Epha7` loss has postnatal cortical dendritic/synaptic phenotypes, but those phenotypes are developmental and not a matched acute thalamic snRNA phenotype;
- redundancy: `Epha4` overlaps `Epha7` in developing thalamus, but a matched compensation test after juvenile Epha7 loss is not available.

This makes Epha7 a plausible functional perturbation in this class, but it does not place it in the high-count tail: the direct receptor analogues point toward post-translational wiring or synaptic effects with little persistent nuclear RNA output.

## Point synthesis

The downstream DEG expectation is essentially zero: every represented Eph receptor and the assayed proximal Eph/Rho/Pak/MAPK/PI3K nodes had zero downstream BH < 0.05 genes in `151 TH Prkcd Grin2c Glut`, and their rare atlas-wide events were isolated singletons in other cell classes.

The requested `n_degs`, however, counts the self transcript. Epha7 is highly expressed in the focal non-target nuclei, its receptor stock should be substantially renewable over the 21-28 day experiment, and the closest thalamic family analogue `Epha4` landed at exactly one total focal DEG with no downstream genes. I therefore predict a self-dominated one-gene signature rather than a pure null or a multi-gene response.

Predicted `n_degs`: **1**
