# Pnpt1 `n_degs` forecast for `151 TH Prkcd Grin2c Glut`

## Point prediction

`predicted_n_degs = 4`

## Evidence used

- The held-out target is `Pnpt1`; the endpoint is the count of measured genes with BH-adjusted Wilcoxon `p < 0.05` in `151 TH Prkcd Grin2c Glut`.
- The exact target-expression card reports that `Pnpt1` is measurable in the focal non-target population: 18,215 of 23,679 nuclei expressing, 76.92% expressing, mean CP10K 1.0717, mean raw UMI 1.6960. The card states that exact expression supports focal reach but is not an editing-efficiency measurement.
- The target biology card places PNPase in a renewable mitochondrial RNA-processing/import role: a homotrimeric mitochondrial RNA exoribonuclease needed for RNA handling and respiratory-chain maintenance, with no close substitute identified. Because P16 editing stops new supply while pre-existing trimers initially persist, the stock adjudication was `likely_substantially_depleted`, with residual uncertainty from unknown PNPase protein half-life in postmitotic thalamic neurons and possible survivor attenuation.
- The declared `151 TH Prkcd Grin2c Glut` training count table is very sparse: 1,674 training perturbations; median 0; 75th percentile 1; 90th percentile 2; 95th percentile 18; 106 targets reached at least 10 DEGs; 59 reached at least 50. A forecast of 4 is therefore above the main null mass but far below the high-response tail.
- Mitochondrial respiratory-chain, TCA, matrix-protease, mitochondrial-translation, and redox perturbations in the same training table mostly had zero or one DEG in this exact cell class:

| Training target | `n_degs` |
| --- | ---: |
| `Opa1` | 37 |
| `Sucla2` | 1 |
| `Sod2` | 1 |
| `Park7` | 1 |
| `Lonp1` | 0 |
| `Lrpprc` | 0 |
| `Suclg1` | 0 |
| `Ndufs4` | 0 |
| `Ndufs7` | 0 |
| `Rars2` | 0 |
| `Fars2` | 0 |
| `Lars2` | 0 |
| `Gfm2` | 0 |
| `Clpp` | 0 |
| `Afg3l2` | 0 |
| `Yme1l1` | 0 |
| `Mff` | 0 |

- Same-experiment Findings for those training genes sharpened the table: `Opa1` was the clear positive mitochondrial-stress comparator, with ATF4/ISR-like amino-acid stress in `151 TH Prkcd Grin2c Glut`, while `Lrpprc`, `Sucla2`, `Ndufs4`, `Ndufs7`, `Rars2`, `Sod2`, `Park7`, and `Clpp` were buffered or nearly flat across their represented neuronal surfaces. This argues against transferring a generic "mitochondrial essential gene" prior directly to dozens or hundreds of focal DEGs.
- Because PNPT1 loss can plausibly expose mitochondrial dsRNA upstream of innate-RNA sensing, I also checked basal neuronal IFN/RNA-sensing perturbations in the training count table. They were again flat in this focal class: `Adar = 0`, `Ifih1 = 0`, `Ifnar1 = 0`, `Ifnar2 = 0`, `Stat1 = 1`, `Stat2 = 0`, `Irf3 = 0`, `Tlr3 = 0`, and `Tlr7 = 0`. Packaged Findings explicitly reported absent MDA5/type-I-IFN output after `Adar` and `Ifih1` perturbation in recovered neurons, so a large interferon-only projection for `Pnpt1` was not favored.
- A focal profile comparison over 17 selected mitochondrial/stress training targets in `151 TH Prkcd Grin2c Glut` found 13/17 with no significant features, 3/17 with 1-9, and only `Opa1` in the 10-49 band. Across 136 selected pairs, the mean positive and negative top-tail overlap coefficients were only 0.0248 and 0.0255, and there was no positive significant-program overlap. Even `Opa1` versus `Lonp1`, the nearest pair in this cohort by whole-profile Pearson, had `r = 0.148` and no shared significant features in the focal class.

## Synthesis

`Pnpt1` was placed above a strict zero because it is expressed in most focal nuclei, its function is continuously renewed, and it could combine mitochondrial RNA-processing failure with an mt-dsRNA stress route that is not exactly represented by the training mitochondrial comparators. I placed it far below `Opa1 = 37` because the focal measured cohort shows strong postmitotic buffering for many mitochondrial and IFN/RNA-sensing perturbations, and the available training analogs did not form a shared high-count mitochondrial module. The resulting point is a sparse nonzero response, 4 DEGs, with the main downward risk being residual PNPase protein stock or recovered-cell buffering and the main upward risk being a PNPT1-specific RNA-stress program.
