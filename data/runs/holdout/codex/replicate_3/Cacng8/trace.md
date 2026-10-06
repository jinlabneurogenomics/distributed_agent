# Direct Cacng8 forecast trace

## Target and endpoint

- Target manifest entry: `Cacng8`.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the focal cell class.

## Evidence used

### Biology-only Cacng8 bundle

Source: `[local file: Cacng8.json]`, schema `expected-transcript-impact-agent-bundle-v1`, SHA-256 `f78d24edeacb00170f5298d531cf5aeca3ed5eb01373026057a01cafb3c726a0`.

- Exact in-assay focal expression was present but not saturated: `Cacng8` was detected in 10,129 of 23,679 non-target nuclei, `42.776%`, with `mean_raw_umi = 0.858`, `mean_cp10k = 0.526`, and `mean_log1p_cp10k = 0.314`.
- The functional-stock adjudication marked gamma-8 as a dynamic AMPAR-complex component and concluded that edited cells are `likely_substantially_depleted` by the P37-P44 harvest after P16 editing.
- The same card also kept the key limit: target-specific gamma-8 clearance in thalamic neurons is unmeasured, and the strongest knockout phenotypes are hippocampal or behavioral germline phenotypes rather than acute thalamic transcriptional phenotypes.

Interpretation: Cacng8 is biologically plausible and expressed in the focal class, so I did not treat it as an unexpressed null. Its mechanism is an AMPA-receptor trafficking/localization auxiliary subunit, not a transcription factor, chromatin factor, proteasome factor, or splicing factor of the kind that dominates large atlas DEG burdens.

### Declared focal training count table

Source: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.

Summary over the 1,674 declared training perturbations:

- Median `n_degs`: `0`.
- 75th percentile: `1`.
- 90th percentile: `2`.
- 95th percentile: `18`.
- Zero-DEG perturbations: `1205 / 1674`.
- Perturbations with `n_degs >= 100`: `43 / 1674`.

The high-count tail was led by global regulators, including `Uba5` at 2677, `Tpr` at 1768, `Sin3a` at 1433, `Rnpc3` at 868, `Zbtb7a` at 841, `U2af2` at 828, `Psmb4` at 742, `Hnrnpu` at 733, and `Yy1` at 720.

### AMPAR/TARP and synaptic-channel training analogs

Source: the same focal count table, with exact significant rows checked against `[local file: training_de_all_cell_groups.parquet]` restricted to `group_name = '151 TH Prkcd Grin2c Glut'`.

Closest AMPAR/TARP perturbations were completely quiet:

| target | focal `n_degs` |
| --- | ---: |
| `Cacng2` | 0 |
| `Cacng3` | 0 |
| `Gria1` | 0 |
| `Gria2` | 0 |
| `Gria3` | 0 |

Nearby glutamate-receptor and postsynaptic perturbations were also in the zero-to-self-only range, with one clear NMDAR-core exception:

| target | focal `n_degs` |
| --- | ---: |
| `Grik1` | 0 |
| `Grik3` | 0 |
| `Grik4` | 0 |
| `Grid2` | 0 |
| `Grin2d` | 0 |
| `Grid1` | 1 |
| `Grik5` | 1 |
| `Grin2a` | 1 |
| `Cplx1` | 1 |
| `Dlg4` | 1 |
| `Grin2b` | 2 |
| `Shank3` | 2 |
| `Grin1` | 89 |

For the exact AMPAR/TARP set, the Parquet profile comparison `profile_amparto_synaptic_151.json` and inspection `inspect_amparto_synaptic_151.json` confirmed that `Cacng2`, `Cacng3`, `Gria1`, `Gria2`, and `Gria3` each had 17,259 measured features and zero BH-significant features. In the 18-node receptor/synaptic cohort I checked, 10 perturbations had no significant feature, 7 had 1-9 significant features, and only the obligatory NMDAR subunit `Grin1` reached at least 50.

## Synthesis

The point estimate is driven by the analog measurements rather than by a generic expressed/not-expressed rule. `Cacng8` expression in 42.8% of focal non-target nuclei and the likely depletion of a dynamic gamma-8 AMPAR auxiliary pool make the edit credible by harvest, but the same mechanism points to a postsynaptic receptor-trafficking perturbation. In this thalamic class, the closest observed perturbations in AMPAR pore subunits and classical TARPs were not broad transcriptional responders; they were exact zeros. Broader ionotropic-glutamate and postsynaptic scaffold perturbations mostly produced only a self-target DEG or zero.

The main upward uncertainty is that gamma-8 could be more specifically required in this thalamic subtype than Cacng2/Cacng3/Gria1/Gria2/Gria3 were, and a visible self-transcript knockdown alone could make the answer 1. I still assigned the mode of the closest empirical neighborhood, `0`, because the declared endpoint is a BH-significant transcriptional footprint among recovered nuclei, not an electrophysiology or AMPAR-trafficking endpoint, and the direct cognates had no significant downstream or self feature in the focal Parquet rows.

## Prediction

`predicted_n_degs = 0`
