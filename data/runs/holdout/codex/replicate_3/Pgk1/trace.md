# Trace

## Target and endpoint

- Target: `Pgk1`.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the count of measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05` in this cell class.
- The held-out target is absent from the declared training count table and from the expression parquet; the Pgk1 biology bundle is endpoint-blind for the target outcome.

## Pgk1 biology used

The Pgk1 bundle supports biological reach and functional realization, but not an expected large transcriptional endpoint:

- PGK1 is a soluble cytosolic glycolytic ATP-generating enzyme.
- Editing at P16 stops new functional PGK1 synthesis while pre-existing enzyme decays.
- Mouse PGK1 peptide half-lives of about 67-125 hours in non-neural cells make substantial depletion plausible by the P37-P44 harvest, while leaving some uncertainty because the turnover measurements were not from postmitotic thalamic neurons.
- Pgk2 is the close phosphoglycerate-kinase paralog but is testis-associated rather than an established brain substitute.
- Pgk1 itself is well detected in the exact focal population: 18,351 of 23,679 non-target cells expressed the transcript, 77.499% of cells, with mean raw UMI 1.916 and pseudobulk CPM 120.067.

This made an edited-cell molecular effect plausible and made a self-transcript row assayable, but it did not identify a Pgk1-loss response program in thalamic neurons.

## Training measurements used

I used the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` count table and the declared `training_de_all_cell_groups.parquet`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"`.

The closest represented glycolysis and pyruvate-dehydrogenase donors were all quiet:

| training perturbation | n_degs |
| --- | ---: |
| Hk1 | 1 |
| Gpi1 | 1 |
| Pfkm | 1 |
| Tpi1 | 1 |
| Eno1 | 0 |
| Dlat | 1 |
| Dld | 0 |
| Pdha1 | 1 |

Those eight perturbations had mean `n_degs = 0.75` and median `n_degs = 1`.

I then widened the check to central carbon and energy-metabolism genes present in the training table:

| training perturbation | n_degs |
| --- | ---: |
| Aco2 | 0 |
| Cox4i1 | 0 |
| Dlat | 1 |
| Dld | 0 |
| Eno1 | 0 |
| Gpi1 | 1 |
| Hk1 | 1 |
| Idh3a | 1 |
| Mpc1 | 0 |
| Ndufv1 | 0 |
| Ogdh | 0 |
| Pdha1 | 1 |
| Pfkm | 1 |
| Slc2a1 | 0 |
| Sucla2 | 1 |
| Suclg1 | 0 |
| Tpi1 | 1 |

This 17-gene cohort had mean `n_degs = 0.471`, median `n_degs = 0`, and no perturbation above one DEG.

## Parquet and profile checks

Directly filtering the expression parquet for those 17 donors and `pvals_adj < 0.05` found exactly eight significant rows, all self rows:

| perturbation | significant measured gene | pvals_adj | logfoldchanges |
| --- | --- | ---: | ---: |
| Dlat | Dlat | 2.81e-07 | -0.673 |
| Gpi1 | Gpi1 | 2.14e-07 | -0.673 |
| Hk1 | Hk1 | 9.86e-05 | -0.768 |
| Idh3a | Idh3a | 9.27e-11 | -0.817 |
| Pdha1 | Pdha1 | 1.31e-06 | -1.039 |
| Pfkm | Pfkm | 6.42e-14 | -0.857 |
| Sucla2 | Sucla2 | 5.12e-05 | -0.659 |
| Tpi1 | Tpi1 | 6.23e-12 | -1.010 |

The `dataset.candidate_profile_review` comparison for the 17-node cohort wrote `workbench/central_carbon_profile_compare.json`, and the cohort diagnostic wrote `workbench/central_carbon_profile_cohort.json`. Across all 136 available pairs, the mean positive top-tail overlap coefficient was 0.0244 and the mean negative top-tail overlap coefficient was 0.0277. There was no positive significant-program overlap to compute, and the 28 pairs with negative significant-program overlap all had coefficient 0.0. Thus the low counts were not hiding a single common subthreshold expression module that should be projected to Pgk1.

## Prediction synthesis

The closest training perturbations favor a count at the floor: single-enzyme perturbations in glycolysis, pyruvate entry, the TCA cycle, and respiratory metabolism produced zero or one FDR-significant gene in this exact thalamic class, and the one-DEG cases were self-transcript decreases rather than downstream programs. Pgk1 differs by being highly expressed and likely functionally depleted within the harvest window, so I put it on the one-self-row side of that 0/1 boundary rather than at a complete null. I did not use a Pgk1 expression signature, a Pgk1 DEG count, labeled-neighbor outcomes, scalar-prior calibration, or any calibrated probability artifact.

Predicted `n_degs`: `1`.
