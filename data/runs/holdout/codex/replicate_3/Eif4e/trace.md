## Forecast

`Eif4e` in `151 TH Prkcd Grin2c Glut`: **1 DEG**.

## Evidence used

The target bundle is endpoint-blind and reports that Eif4e is a cap-binding eIF4F component whose functional protein stock should be substantially depleted by the P37-P44 harvest after P16 editing. The in-assay reach is strong rather than limiting: in matched non-target nuclei from `151 TH Prkcd Grin2c Glut`, Eif4e was detected in 20,346 / 23,679 cells, or 85.9%, with mean CP10k 1.48. The bundle did not supply a context-matched postnatal thalamic phenotype clock, did note possible buffering by Eif4e2/Eif4e1b, and did not use target endpoint values.

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` is extremely zero-heavy: 1,205 / 1,674 training targets are zero, the median is zero, the 75th percentile is one, and only 43 targets have at least 100 DEGs. That prior made a large count unlikely unless the target matched one of the few broad stress or mTORC1-disinhibition programs.

I therefore used the expressed biology to choose eIF4F, mTOR, and translation-control comparators that were present in the training table, then checked their exact BH<0.05 Parquet rows in the same thalamic class:

| training target | n_degs | interpretation in the selected cohort |
| --- | ---: | --- |
| Eif4g1 | 1 | one call, the self transcript |
| Eif4a2 | 2 | self transcript plus Cadm4 |
| Eif4h | 1 | one downstream marker, Hexim1 |
| Mtor | 2 | small mixed downstream response |
| Rptor | 0 | flat |
| Eif2ak4 | 0 | flat |
| Eif5a | 0 | flat |
| Fmr1 | 0 | flat |
| Cyfip1 | 0 | flat |
| Ddx3x | 8 | modest, DEAD-box-specific response |
| Tsc2 | 86 | broad but opposite/upstream mTORC1 disinhibition branch |

The same-experiment corpus was used only as the semantic layer over those measured training perturbations, not as independent replication. It reported that Eif4g1, the closest represented eIF4F scaffold, produced no downstream FDR-level neuronal nuclear-RNA response; that Eif4a2 and Eif4h were each sparse and non-phenocopying despite physical cap-initiation relationships; and that Eif4g1/Eif4a2/Eif4h/Mtor/Rptor were flat or weak while Tsc2 produced a separable broad program.

A run-local profile comparison over these 11 training perturbations in `151 TH Prkcd Grin2c Glut` found five null nodes, five nodes with 1-9 significant features, and only Tsc2 with at least 50. Significant-feature overlap inside the chosen cohort was essentially absent, supporting the corpus interpretation that these translation-control perturbations do not share a transferable broad RNA program.

## Synthesis

Eif4e has enough expression in the focal cells and likely enough protein turnover over 21-28 days that a zero forecast would understate reachable target engagement. However, its closest assayed cap-initiation neighbors were buffered at the single-gene scale rather than entering a stress, ribosomal, or mTORC1-like secondary RNA state. The best point is therefore one BH<0.05 measured gene: a self-transcript or isolated marker call, with no evidence for a multi-gene downstream program.
