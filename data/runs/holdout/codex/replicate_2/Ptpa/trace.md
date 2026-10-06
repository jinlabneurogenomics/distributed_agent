# Direct forecast for `Ptpa`

## Declared target and endpoint

- Target manifest: one held-out target, `Ptpa`.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, defined as the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Same-experiment surfaces used: the declared training count table, the declared `training_de_all_cell_groups.parquet`, and packaged July-corpus Findings for training perturbations. These are not independent replications of one another.
- The `Ptpa` target signature and target count were not present in the declared training count table or Parquet, and I did not use a `Ptpa` report: `corpus.target_context(Ptpa)` returned `target_found=false`.

## Target biology

The canonical biology bundle resolves the packet symbol `Ptpa` to mouse `Ptpra` / RPTPalpha rather than PP2A phosphatase activator. In the focal non-target population, `Ptpa` is well within reach of the assay: 20,151 of 23,679 non-target `151 TH Prkcd Grin2c Glut` nuclei expressed it, for 85.10% expressing, with mean log1p CP10K 0.7885.

The molecular prior is directionally real but weak on scalar magnitude. PTPRA is a transmembrane receptor-type tyrosine phosphatase that physiologically activates Src-family kinases including Fyn; germline null mice have hippocampal and myelination phenotypes. A P16 disruptive edit should stop production of new PTPRA protein, but it does not directly inactivate pre-existing membrane receptor, and the card found no quantitative basal PTPRA clearance measurement in postmitotic neurons. Thus strong focal RNA expression argues that edited cells can be hit, while functional stock by the P37-P44 harvest remains indeterminate rather than certainly exhausted.

## Matched training evidence

The full focal-class training table has 1,674 perturbations: 1,205 had `n_degs = 0`, 469 had at least one DEG, 106 had at least ten, and 43 had at least 100. The prior is therefore highly zero-inflated before biology is applied.

Directly relevant tyrosine-phosphatase and Src-axis perturbations in the same table were quiet:

| training target | `151 TH Prkcd Grin2c Glut` `n_degs` |
|---|---:|
| `Fyn` | 0 |
| `Ptpn1` | 0 |
| `Ptpn11` | 0 |
| `Ptprc` | 0 |
| `Ptprd` | 0 |
| `Ptprf` | 0 |
| `Ptprm` | 1 |
| `Ptprn` | 1 |
| `Ptprn2` | 1 |
| `Ptpro` | 0 |
| `Ptprt` | 0 |

This comparator set has a median of 0 and a log1p-scale center of about 0.21 DEGs. It is also biologically closer than high-response examples in the same class such as `Grin1`, because `Ptpa` is a receptor phosphatase upstream of Src/Fyn signaling rather than an obligatory ion-channel subunit.

Packaged corpus records for the measured comparators support treating their zeroes as informative endpoint boundaries for this assay. `Fyn` was FDR-flat across recovered neuronal classes, and its report explicitly found that loss of Fyn did not phenocopy NMDA-receptor subunit loss or form a Reelin/Dab1/Fyn transcriptional module after P16 perturbation. `Ptpn11` was also FDR-flat and uncoupled from the small thalamic Braf/Map2k1/Ntrk2 MAPK-output branch. `Ptprf` was pan-measured and FDR-flat, and the LAR-family receptor-phosphatase comparators `Ptprd`, `Ptprm`, and `Ptprt` likewise failed to form a coherent FDR-level transcriptional module.

## Fresh profile checks

I computed a run-local profile comparison from the declared Parquet restricted to `group_name = "151 TH Prkcd Grin2c Glut"`, using `scores` as the signed profile and `pvals_adj < 0.05` as the endpoint activity threshold. All 13 supplied training profiles were available: `Fyn`, `Ptpn1`, `Ptpn11`, `Ptprc`, `Ptprd`, `Ptprf`, `Ptprm`, `Ptprn`, `Ptprn2`, `Ptpro`, `Ptprt`, with `Grin1` and `Ntrk2` as active-response guardrails.

The main source-like profiles were exactly FDR-flat in the focal class:

| profile node | BH<0.05 features |
|---|---:|
| `Fyn` | 0 |
| `Ptpn11` | 0 |
| `Ptprf` | 0 |
| `Ptprd` | 0 |
| `Ptprc` | 0 |

Their pairwise all-gene profile similarities to active guardrails were near background. For example, `Fyn` versus `Grin1` had Pearson 0.0286 with zero shared significant features, and `Ptpn11` versus `Ntrk2` had Pearson 0.0357 with zero shared significant features. In a full eligible-neighbor scan over all 1,674 training targets, the nearest whole-profile neighbors of these five anchors also had low correlations: the top Pearson values were 0.089 for `Fyn`, 0.079 for `Ptpn11`, 0.087 for `Ptprf`, 0.169 for `Ptprd`, and 0.068 for `Ptprc`.

## Synthesis

The strongest upward evidence is that `Ptpa` is expressed in most focal nuclei and PTPRA has bona fide mouse neural Src/Fyn biology. That supports possible engagement but not a large BH-supported survivor nuclear-RNA response.

The stronger scalar evidence is downward:

- the closest direct measured effector, `Fyn`, is zero in this focal class and FDR-flat across the corpus reports;
- another broad protein tyrosine phosphatase, `Ptpn11`, is zero and did not couple into the detectable thalamic MAPK branch;
- represented receptor-type phosphatases were zero or singleton-only in the same `n_degs` table;
- their focal-class signed profiles lacked any coherent active neighbor that would suggest a hidden `Ptpa`-like FDR program; and
- the `Ptpa` biology bundle leaves residual active receptor stock after a P16 edit unresolved, so it does not justify a stronger short-window nuclear response than the directly measured Src/Fyn/PTP comparators.

I therefore place `Ptpa` in the zero/singleton regime and round the log-scale center of the source-like training comparators to the nearest integer:

`predicted_n_degs = 0`
