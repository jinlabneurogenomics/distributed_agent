# Pdss2 n_degs forecast for 151 TH Prkcd Grin2c Glut

## Inputs used

- Held-out target: `Pdss2`, from the one-row manifest `Pdss2.csv`.
- Biology-only target bundle: `biology_bundles/Pdss2.json`; this exposed Pdss2 biology and exact focal-population expression but not the held-out Pdss2 DEG count or Pdss2 DE signature.
- Training endpoint table: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, with 1,674 non-held-out targets and `n_degs = count(pvals_adj < 0.05)` in `151 TH Prkcd Grin2c Glut`.
- Declared training DE parquet: `training_de_all_cell_groups.parquet`, inspected through `workbench/mito_profile_compare.json` and `workbench/mito_profile_inspect.json` for a caller-selected mitochondrial/CoQ cohort in the matched cell class.
- Same-experiment corpus summaries for non-held-out training perturbations, especially `Coq5`; these are interpreted as packaged summaries of the same Perturb-seq experiment, not external replication.

## Evidence

`Pdss2` is a mechanistically plausible perturbation in this assay. The supplied biology bundle identifies Pdss2 as the Pdss1 partner that supplies the polyisoprenoid side chain for coenzyme Q biosynthesis, and the functional-stock adjudication calls the operative Pdss1/Pdss2-plus-CoQ pool likely substantially depleted by the P37-P44 harvest, while preserving uncertainty from pre-existing synthase and lipid CoQ pools. The exact in-assay reach was nontrivial in the focal population: Pdss2 RNA was available, with mean raw UMI 0.7908 and 12,352/23,679 non-target cells expressing Pdss2, or 52.16%.

The direct matched training evidence is much more buffered than that prior alone would suggest. In the focal count table, the only explicit CoQ-biosynthetic training target, `Coq5`, had `n_degs = 0`. Other nearby mitochondrial perturbations were also at the floor or near it: `Clpp = 0`, `Fars2 = 0`, `Lrpprc = 0`, `Hmgcr = 0`, `Ndufs4 = 0`, `Ndufv1 = 0`, `Uqcrfs1 = 0`, `Uqcrc2 = 1`, `Sdha = 1`, and `Cox4i1 = 0`. Across a 43-target hand-selected CoQ/ETC/mitochondrial slice from the declared table, the median was 0 and only 18/43 had any significant genes.

The high-count mitochondrial-adjacent entries were broader regulatory or stress-axis perturbations rather than proximal CoQ/ETC losses: `Nrf1 = 138`, `Dhdds = 116`, and `Esrra = 57` in this cell class. The selected-profile comparison over 14 mitochondrial/cofactor targets found 9/14 with no significant features, 2/14 with 1-9, and 3/14 with at least 50; the three active nodes were those broad `Dhdds`/`Esrra`/`Nrf1` cases. `Coq5`, `Clpp`, `Fars2`, and `Lrpprc` each had zero significant genes across the 17,259 focal features in the profile artifact.

The same-experiment `Coq5` Findings make the Coq5 zero particularly informative rather than merely a single focal accident. The packaged report records a high-confidence buffered response for Coq5, with 22 measured neuronal groups all having zero downstream genes at FDR < 0.10; it also records absence of the expected mitochondrial ISR/UPR program even though the assay detected those marker genes after other perturbations, and no meaningful convergence between Coq5 and represented UQCRC/CYC1/NDUF/LONP1/CLPP comparators. The important caveat is that CoQ abundance and respiration were not assayed, so this is evidence for lack of a nuclear RNA response in recovered nuclei, not proof of intact CoQ metabolism.

## Forecast

Pdss2 should have real functional reach in thalamic neurons, but the endpoint is a short-window, survivor-conditioned nuclear RNA DEG count. The closest measured CoQ perturbation and most direct ETC/mitochondrial training comparators were silent or one-gene responses in exactly this class, while the larger mitochondrial-adjacent signatures came from broader ER-stress or transcriptional regulators that are not good scale donors for a Pdss2 side-chain synthase loss. I therefore treat a small but detectable Pdss2 response as possible and a broad `Dhdds`/`Nrf1`-scale response as unlikely; the strongest point forecast is the direct CoQ/ETC floor.

Predicted `n_degs`: 0.
