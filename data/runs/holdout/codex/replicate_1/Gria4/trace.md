# Direct forecast trace

## Target

- Target: `Gria4`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Predicted endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in that focal population.

## Biology-only target evidence

- The declared target manifest and canonical biology bundle both identify the held-out target as `Gria4`.
- `Gria4` is strongly present in the exact in-assay non-target focal population: 23,472 of 23,679 nuclei expressed it, 99.13% expressing; mean raw UMI was 8.60 and mean log1p CP10K was 1.786.
- The functional-stock card supports a reachable perturbation by harvest rather than a pure persistence null: GluA4 is a pore-forming AMPA-receptor subunit, a disruptive edit stops new functional GluA4 synthesis, and the selected turnover evidence measured GluR4 protein half-life at 23 +/- 8 hours in cultured neurons, far shorter than the P16 to P37-P44 interval.
- The same biology card leaves the RNA-response magnitude uncertain: the closest thalamic loss phenotypes are germline/electrophysiological and concentrated in reticular-thalamic circuitry, whereas this endpoint is acute, mosaic, survivor-conditioned nuclear RNA in a thalamic glutamatergic class.

## Training evidence used for scale

The 1,674-row focal count table excludes `Gria4`; its median `n_degs` is 0, the 75th percentile is 1, and 1,205 of 1,674 training perturbations are at 0.

Focal-class `n_degs` for the closest AMPA receptor paralogs and AMPAR-associated genes were:

| target | n_degs |
| --- | ---: |
| Gria1 | 0 |
| Gria2 | 0 |
| Gria3 | 0 |
| Cacng2 | 0 |
| Cacng3 | 0 |
| Nsf | 0 |
| Dlg4 | 1 |
| Abhd12 | 1 |
| Adam22 | 1 |
| Cnr1 | 1 |

Other glutamate-receptor subunits in the same count table were likewise mostly quiet:

| target | n_degs |
| --- | ---: |
| Grik1 | 0 |
| Grik3 | 0 |
| Grik4 | 0 |
| Grik5 | 1 |
| Grin2a | 1 |
| Grin2b | 2 |
| Grin2d | 0 |
| Grin3a | 0 |
| Grin1 | 89 |

A focused scan of `training_de_all_cell_groups.parquet` in `151 TH Prkcd Grin2c Glut` matched those focal counts. For several one-hit/few-hit receptor perturbations the top significant feature was the perturbed receptor transcript itself, e.g. `Grin2a`, `Grin2b`, `Grik5`, `Gabrb2`, and `Gabrd`, rather than a broad downstream program.

The same-experiment corpus was used only as an interpretation of those training measurements. Its `Gria1` report links `Gria1`, `Gria2`, and `Gria3` to a high-confidence AMPAR-core/trafficking claim: represented AMPAR-core and AMPAR-trafficking/scaffold perturbations were transcriptionally buffered in basal juvenile neurons rather than forming an interchangeable AMPAR-loss nuclear-RNA program. The same report contrasts that AMPAR flatness with visible NMDAR subunit responses, especially `Grin1`; therefore `Grin1 = 89` is an internal detectability boundary, not the best scale donor for `Gria4`.

## Synthesis

High focal `Gria4` expression and short GluA4 turnover argue that the perturbation could be functionally realized by harvest, so I did not treat the target as unexpressed or inaccessible. The focal quantitative neighbors most directly tied to GluA AMPA-receptor loss, however, are all zero or singleton responses, and the thalamic functional prior for `Gria4` is not a matched acute transcriptional phenotype in the assayed glutamatergic class. I therefore put the point forecast at the AMPAR-family mode rather than at the broader ionotropic-receptor outlier.

Predicted `n_degs`: 0
