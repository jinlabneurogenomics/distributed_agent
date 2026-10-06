# Kcnab1 n_degs prediction

## Target and endpoint

- Target: `Kcnab1`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- Declared count table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Declared profile table: `[local file: training_de_all_cell_groups.parquet]`.
- Biology bundle: `[local file: Kcnab1.json]`, sha256 `2718be44331d00f4d6858edd19df3d7170b5d3fb4c54866032a22a3e4fc59382`.

## Evidence used

### Kcnab1 reach and biology

The target bundle reports exact in-assay expression in the focal non-target population: 18,265 of 23,679 nuclei expressed `Kcnab1` in `151 TH Prkcd Grin2c Glut` cells, with `pct_cells_expressing = 77.13585877782`, `mean_raw_umi = 2.0391486126947926`, and `pseudobulk_cpm = 127.8006746303422`.

The same bundle places Kcnab1 as a cytoplasmic Kvbeta1 auxiliary component of native Kv1 potassium-channel complexes rather than a transcriptional regulator. Its source card links Kvbeta1 to Kv1 alpha subunits `Kcna1`, `Kcna2`, `Kcna4`, and `Kcna6`; the functional-stock card judges the P16-to-P37/P44 stock state as indeterminate, because a disruptive edit stops new Kvbeta1 production but pre-existing channel complexes should persist until subunit or complex turnover, and no target-specific half-life or dated mature-neuron loss clock was available.

### Training distribution in the requested class

The requested class is sparse in the 1,674-row training count table:

- `n_degs = 0`: 1,205 targets
- `n_degs = 1`: 276 targets
- `n_degs > 1`: 193 targets
- median `n_degs`: 0
- 90th percentile: 2
- 95th percentile: 18

Among target-self rows present in the focal-class Parquet, 319 of 1,642 training targets had significant self RNA at BH `p < 0.05`; 237 of the 276 one-DEG training targets were explained by a significant self row.

### Kv1 and ion-channel analogs

The closest training-observed molecular analogs from the Kv1 complex were quiet in the focal class:

| analog | focal `n_degs` | focal significant row |
| --- | ---: | --- |
| `Kcna1` | 0 | none |
| `Kcna2` | 0 | none |
| `Kcnab2` | 1 | `Kcnab2` self RNA only |

The broader channel or channel-complex checks were also self-only or zero in this class:

| analog | focal `n_degs` | focal significant row |
| --- | ---: | --- |
| `Adam22` | 1 | `Adam22` self RNA only |
| `Dlg4` | 1 | `Dlg4` self RNA only |
| `Kcnb1` | 0 | none |
| `Kcnq2` | 1 | `Kcnq2` self RNA only |

The packaged same-experiment corpus, used here as interpretation of the same training experiment rather than independent replication, made the same boundary explicit. `Kcnab2:F001` reports that `Kcnab2` had no downstream genes at FDR < 0.10 in any of the 22 recovered neuronal classes despite significant self-RNA depletion in five groups. `Kcnab2:F004` reports that Kv1 alpha-subunit perturbations `Kcna1` and `Kcna2` were transcriptionally flat like `Kcnab2`, while broader potassium-channelopathy genes such as `Kcnb1` and `Kcnq2` yielded only sparse, non-overlapping downstream hits.

## Synthesis

`Kcnab1` has strong expression reach in the assayed thalamic population, so the edit is not excluded by target absence. But its closest observed Kv1-complex relatives in the training data produced no focal downstream program: `Kcna1 = 0`, `Kcna2 = 0`, and `Kcnab2 = 1` with the one DEG being self depletion. That made a many-gene transcriptional state unlikely.

The remaining distinction is zero versus a single self-transcript call. Because the endpoint includes self RNA, because high focal expression gives the assay the opportunity to detect target-RNA depletion, and because the strongest beta-subunit comparator `Kcnab2` had exactly a self-only focal hit, I assigned `Kcnab1` to the same self-only near-null pattern rather than to a downstream-response class.

Predicted `n_degs`: 1
