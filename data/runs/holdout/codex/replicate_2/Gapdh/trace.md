# Gapdh direct DEG-count forecast

## Target and endpoint

- Target: `Gapdh`, from the one-row holdout manifest.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes in that population with Wilcoxon BH-adjusted `pvals_adj < 0.05`.
- The target perturbation profile and target count were not used; the declared training evidence was `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` plus `training_de_all_cell_groups.parquet`.

## Biology prior

- The declared `Gapdh` biology bundle supports a plausible realized perturbation: Gapdh is a soluble, continuously renewed glycolytic dehydrogenase; P16 editing would block newly synthesized competent enzyme; the 21-28 day harvest window spans multiple typical mouse-brain protein lifetimes; and the close `Gapdhs` isozyme is germ-cell restricted rather than a thalamic-neuron substitute.
- The same bundle keeps the assay projection uncertain. Available loss evidence is systemic/developmental rather than acute postnatal neuronal, exact thalamic cellular reach is unresolved, metabolic reserve is unresolved, and survivor-conditioned nuclear recovery could leave the recovered transcriptional profile quiet.
- Exact focal expression for the `Gapdh` feature is unavailable because the target gene is `excluded_as_unused_gene`. Therefore a pure self-target transcript call, which is a common one-gene outcome for metabolic analogs, cannot contribute one DEG for Gapdh.

## Training measurements used

- The thalamic training count table contains 1,674 perturbations. Its burden is highly sparse and skewed: 1,205/1,674 targets have `n_degs = 0`, the median is 0, the 75th percentile is 1, the 90th percentile is 2, and the mean is inflated to 14.05 by a small long tail.
- Curated annotation sets around Gapdh selected `Hk1`, `Pfkm`, `Tpi1`, and `Eno1` as the main available glycolysis comparators; `Gpi1`, `Dlat`, and `Pdha1` were used as adjacent glucose/pyruvate-metabolism checks; `Dld` was a quiet pyruvate-dehydrogenase-adjacent boundary.
- In the declared focal count table:

| comparator | `n_degs` |
|---|---:|
| `Eno1` | 0 |
| `Dld` | 0 |
| `Dlat` | 1 |
| `Gpi1` | 1 |
| `Hk1` | 1 |
| `Pdha1` | 1 |
| `Pfkm` | 1 |
| `Tpi1` | 1 |

- The full Parquet showed that every one-count core/adjacent comparator above was self-only in `151 TH Prkcd Grin2c Glut`: `Dlat -> Dlat`, `Gpi1 -> Gpi1`, `Hk1 -> Hk1`, `Pdha1 -> Pdha1`, `Pfkm -> Pfkm`, and `Tpi1 -> Tpi1`.
- A symmetric profile comparison of `Hk1`, `Pfkm`, `Tpi1`, `Eno1`, `Gpi1`, `Dlat`, `Pdha1`, and `Dld` found all profiles available, two nodes with no significant features, and six nodes with only 1-9 significant features. Inspecting the main glycolysis nodes against `Dlat`, `Dld`, and `Eno1` found no pairwise significant-feature intersections; their profiles are weak singleton/self perturbations rather than one coherent downstream state.
- Broader energy-metabolism checks did not overturn the glycolysis evidence. `Uqcrb`, `Uqcrfs1`, `Uqcrh`, and `Cox4i1` were zero; `Uqcrc2`, `Uqcrq`, and `Ndufs8` were one-count perturbations, with `Uqcrc2` and `Ndufs8` self-only. The large `Gfpt1` signal was down-weighted because it is a hexosamine/ER-stress perturbation rather than direct Gapdh-like glycolytic flux.

## Synthesis

Gapdh is central enough that functional depletion by harvest is plausible, but the target-cell endpoint is survivor-conditioned nuclear RNA rather than enzyme activity or survival. The exact task-matched analogs argue that perturbing glycolytic enzymes in this thalamic class usually produces either no significant downstream transcript or only the targeted transcript as a DEG. Because `Gapdh` itself is not a measured feature, that recurrent one-gene self signature would round down to zero measured DEGs for the held-out target.

`predicted_n_degs = 0`
