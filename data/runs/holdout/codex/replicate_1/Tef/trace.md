# Direct DEG-count forecast for Tef

## Target and allowed target prior

- Target: `Tef`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of focal-population measured genes with BH-adjusted Wilcoxon `p < 0.05`

The one-row declared manifest names only `Tef`. The declared biology bundle reports that `Tef` is expressed in the focal non-target cells: 20,305 of 23,679 nuclei express it, or 85.75%, with mean raw UMI 2.41 and pseudobulk CPM 151.29. That makes target reach favorable, but the bundle also adjudicates the effect as a single PAR-bZIP transcription-factor loss in a family where `Dbp` and `Hlf` strongly buffer loss of another family member in mouse brain. The functional stock is likely substantially depleted by P37-P44 after P16 editing, but the postnatal neural phenotype evidence comes from combined `Tef`/`Dbp`/`Hlf` germline family loss rather than acute `Tef`-only loss.

## Training measurements

The declared count table contains 1,674 training perturbations for `151 TH Prkcd Grin2c Glut`; `Tef` is absent. Counts are very sparse:

- 1,205 / 1,674 training perturbations have `n_degs = 0`.
- Median `n_degs` is 0; the 75th percentile is 1, the 90th percentile is 2, and the 95th percentile is 18.
- The extreme tail is a small minority: 42 / 1,674 exceed 100 and only 3 exceed 1,000.

I treated the close PAR-bZIP paralogs as unavailable because `Dbp` and `Hlf` are absent from the focal training count table. The useful visible comparators were clock-loop and bZIP-adjacent single-transcription-factor perturbations. Exact counts from the declared training Parquet in the matched focal group were:

| training target | focal `n_degs` | interpretation |
|---|---:|---|
| `Bmal1` | 103 | upstream positive-limb clock factor; broader than `Clock` |
| `Clock` | 3 | compact output: `Dbp`, `Nr1d2`, `Tef` down |
| `Cry1` | 1 | singleton `Per2` response |
| `Cry2` | 3 | compact `Nr1d1`, `Dbp`, self response |
| `Nr1d1` | 116 | REV-ERB loss with a thalamic synaptic/metabolic state |
| `Nr1d2` | 1 | near-flat accessory-loop perturbation |
| `Rora` | 278 | broad RORalpha-selective thalamic program |
| `Bmal2`, `Rorb`, `Rorc` | 0 each | represented clock/ROR relatives that were flat |
| `Maf`, `Mafa`, `Mafb` | 0 each | other bZIP-family TF losses that were flat |
| `Mafg` | 1 | other bZIP-family TF loss with a singleton response |

The packaged same-experiment Findings, which are an interpretation of the same training measurement rather than independent replication, made the larger count donors less transferable. `Rora` was described as an acute thalamic RORalpha-selective program not reproduced by `Rorb`/`Rorc`. `Nr1d1` was described as a thalamic REV-ERB response coupled to synaptic, metabolic, lipid/cholesterol, and extracellular-remodeling genes. Those outliers are accessory-loop or identity-state responses, not single PAR-bZIP output-factor analogues. In contrast, `Clock` and `Cry2` demonstrated that this cell class can show a small canonical clock-output module involving `Dbp`/`Tef`/`Nr1d` genes, but the module was only three genes at this stricter `p_adj < 0.05` cutoff.

## Synthesis

`Tef` has enough expression and likely enough protein turnover for an edit to be realized by harvest, so I did not collapse it to a guaranteed null. The stronger evidence is downward: TEF is downstream of the high-count `Bmal1`/`Nr1d1`/`Rora` control points, and the biology bundle gives direct mouse-brain evidence that PAR-bZIP family redundancy buffers single-family-member loss. In the training data, even upstream `Clock` and `Cry2` losses had only three focal DE genes, while many represented related TFs had zero or one.

I therefore placed `Tef` just above the bulk-null median and slightly below the compact `Clock`/`Cry2` responses.

Predicted `n_degs`: 2
