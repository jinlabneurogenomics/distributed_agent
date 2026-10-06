# Thbd n_degs forecast

## Target and endpoint

- Target: `Thbd`.
- Population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: count of measured genes in the held-out `Thbd` perturbation with Wilcoxon BH-adjusted `pvals_adj < 0.05`.
- The focal count table contains 1,674 training perturbations and does not contain `Thbd`.

## Target biology used

- The canonical target bundle was served in `biology` view with `target_outcome_exposed=false` and `labeled_neighbors_exposed=false`.
- Exact focal reach was almost absent: `Thbd` had 54 total UMIs among 23,679 matched non-target nuclei in `151 TH Prkcd Grin2c Glut`, mean raw UMI 0.00228, pseudobulk CPM 0.1429, and only 50/23,679 non-target nuclei expressing it, or 0.211%.
- The Thbd source card assigns the canonical operation to endothelial cell-surface thrombomodulin in the thrombin-protein C pathway. Mouse loss phenotypes were severe postnatal vascular/systemic coagulopathy, but explicitly outside the NeuN-positive thalamic neuronal population.
- The baseline-expression fact placed THBD in brain vasculature rather than broad thalamic neurons, and the observability card found no matched postnatal neuronal loss context.
- Existing thrombomodulin stock would not be directly destroyed by a disruptive edit and the card found no matched basal half-life for juvenile mouse brain endothelium or neurons. In this assay the limiting issue is stronger than stock persistence: the target is essentially not present in the assayed recovered neurons.

## Training measurements used

- The focal training count table was strongly zero-inflated: 1,205/1,674 targets were exactly 0, the median was 0, the 75th percentile was 1, and the 90th percentile was 2. The few high values were from broad nuclear/proteostasis regulators, not vascular surface receptors.
- Training perturbations with vascular or endothelial receptor biology available in the table were quiet in the same focal class:

| target | `n_degs` in count table | `pvals_adj < 0.05` rows recomputed from focal Parquet |
| --- | ---: | ---: |
| `Eng` | 0 | 0 |
| `Itgb1` | 0 | 0 |
| `Kdr` | 0 | 0 |
| `Lrp1` | 0 | 0 |
| `Robo4` | 0 | 0 |
| `Tek` | 0 | 0 |

- Same-experiment corpus findings were consistent with those focal counts: `Eng`, `Robo4`, and `Tek` were summarized as transcriptomically silent or pan-null across recovered NeuN-positive neuronal groups, and `Kdr` was summarized as almost completely flat without a canonical VEGF/endothelial program.

## Synthesis

The direct-systemic Thbd loss phenotype is real, but it is endothelial and coagulation-centered, while this readout samples recovered NeuN-positive thalamic nuclei. Exact in-assay expression in the focal class is only 0.211% of matched non-target nuclei with 54 target UMIs total, so most edited neurons should lack a Thbd transcript and a thrombomodulin-dependent cell-intrinsic process to perturb. The focal training distribution already puts most perturbations at zero, and the nearest available vascular/endothelial training genes also sit at zero in the declared count table and in the underlying focal Parquet rows. I therefore forecast no BH-significant downstream genes for held-out `Thbd` in `151 TH Prkcd Grin2c Glut`.

Predicted `n_degs`: `0`.
