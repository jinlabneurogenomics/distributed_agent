# Thbd direct n_degs forecast

## Declared target and endpoint

- Target: `Thbd`, from the one-row holdout manifest `Thbd.csv` and the canonical biology bundle `Thbd.json`.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, defined as measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- Target-outcome handling: the `characterization_bundle(target="Thbd", view="biology")` response was used; its serving metadata reported `target_outcome_exposed=false` and `labeled_neighbors_exposed=false`.

## Evidence used

### Target biology and focal reach

The biology bundle places THBD's canonical operation in vascular endothelium: thrombomodulin is a cell-surface thrombin cofactor for protein-C activation, not an established postmitotic thalamic neuronal regulator. Mouse loss evidence is severe, but it is endothelial/systemic coagulopathy rather than loss in NeuN-positive neurons, and the curated observability card found no postnatal cell-intrinsic neuronal role.

The exact in-assay non-target expression for this same class is essentially absent:

| quantity | value |
| --- | ---: |
| `n_non_target_cells` | 23679 |
| `n_cells_expressing` | 50 |
| `pct_cells_expressing` | 0.2111575658 |
| `total_target_umi` | 54 |
| `mean_raw_umi` | 0.0022805017 |
| `mean_log1p_cp10k` | 0.0010651005 |
| `pseudobulk_cpm` | 0.1429271291 |

The stock card leaves loss of pre-existing surface/recycling thrombomodulin indeterminate over the 21-28 day edit-to-harvest interval. That uncertainty matters only for cells with an operative THBD pool; the expression measurement says that, in the assayed thalamic neuronal nuclei, the target-bearing population is tiny.

### Training distribution in the declared count table

From `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`:

- Rows: 1674 biological training perturbations.
- Zero-count perturbations: 1205 / 1674 = 71.98%.
- Perturbations with `n_degs <= 1`: 1481 / 1674 = 88.47%.
- 75th percentile: 1 DEG.
- 90th percentile: 2 DEGs.
- 95th percentile: 18 DEGs.
- Maximum: 2677 DEGs.

So the focal class has a long positive tail, but the modal and median response is exactly zero.

### Biologically nearby measured training perturbations

I used represented vascular, endothelial, and coagulation-associated training targets as weak biological comparators, because they share Thbd's non-neuronal vascular/coagulation context better than the high-yield neuronal chromatin, splicing, proteasome, and essential-process perturbations do.

| training target | `151 TH Prkcd Grin2c Glut` `n_degs` |
| --- | ---: |
| `Ager` | 0 |
| `Eng` | 0 |
| `F2` | 0 |
| `Kdr` | 0 |
| `Sele` | 0 |
| `Tek` | 0 |

The declared Parquet profile comparison for exactly these six targets in the 151 class reported `response_activity_status_counts = {"no_significant_features": 6}`. Across all 15 pairwise comparisons, there was no positive or negative significant-program overlap, confirming that these are not silent only by the scalar count table; their measured 151 expression profiles have no FDR<0.05 program to transfer.

Packaged same-experiment report Findings agree with this interpretation as semantic summaries, not as independent evidence: `Ager`, `F2`, `Sele`, and `Tek` were transcriptomically null across all measured NeuN-positive classes at FDR<0.10; `Eng` was null in all 22 recovered neuronal classes; and `Kdr` had only one isolated FDR<0.10 downstream event outside the requested class with no canonical VEGF/endothelial program.

## Synthesis

The strongest direct facts all pull downward:

- Thbd expression in the requested class is nearly undetectable, with only 50/23679 non-target nuclei and 54 total UMIs.
- The documented THBD loss biology is endothelial and systemic, while this assay reads recovered NeuN-positive thalamic neuronal nuclei.
- The six represented non-neuronal vascular/coagulation training comparators all have zero BH<0.05 DEGs in the exact focal class and no significant measured 151 programs in the Parquet profiles.
- The 151 training endpoint itself is sparse: almost 72% of biological training perturbations are zero and almost 89% have at most one DEG.

The main upward facts are weak for this endpoint. THBD has a severe postnatal vascular requirement in mice and no close paralog was identified, but those do not establish a neuronal target-bearing compartment after P16 neuronal CRISPR. Functional-stock timing is unresolved, yet stock persistence cannot generate a bulk neuronal survivor signature when the baseline target is nearly absent.

I therefore predict the modal/null count:

`predicted_n_degs = 0`
