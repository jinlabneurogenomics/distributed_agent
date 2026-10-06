# Hmgb1 direct DEG-count forecast

## Target and endpoint

- Target: `Hmgb1`, from the one-row manifest.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the number of measured genes in this class with BH-adjusted Wilcoxon `p < 0.05`.

## Evidence used

1. Declared Hmgb1 biology bundle, served by `distributed_agents_runtime.characterization_bundle(target="Hmgb1", view="biology")`.
   - Exact focal-population expression in matched non-target nuclei:
     - `group_name`: `151 TH Prkcd Grin2c Glut`
     - `n_non_target_cells`: 23679
     - `n_cells_expressing`: 13307
     - `pct_cells_expressing`: 56.1975
     - `mean_raw_umi`: 0.9907
     - `mean_cp10k`: 0.6315
   - HMGB1 is a dynamic non-histone chromatin/DNA chaperone with nuclear, cytoplasmic, and extracellular pools.
   - Acute CRISPR loss stops new Hmgb1 supply but should not instantly remove pre-existing HMGB1 protein. The bundle's functional-stock conclusion is `partially_depleted_or_leading_edge`: mouse brain can reach near-complete HMGB1 protein loss by 6-7 weeks after inducible deletion, whereas this Perturb-seq assay harvested 21-28 days after a P16 edit.
   - Postnatal neural loss phenotypes exist in less-matched settings, but neither the adult global deletion nor the newborn astroglial deletion is a matched juvenile thalamic neuronal perturbation.
   - Hmgb2 is a close paralog with developmental overlap, but the bundle found no direct compensation test in juvenile thalamic neurons.

2. Declared training count table `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
   - 1674 visible perturbations.
   - 1205/1674 had `n_degs = 0`.
   - 1481/1674 had `n_degs <= 1`.
   - 1512/1674 had `n_degs <= 2`.
   - Median = 0, 75th percentile = 1, 90th percentile = 2, 95th percentile = 18, mean = 14.054.
   - The high mean is dominated by a small tail: examples include `Uba5` 2677, `Tpr` 1768, `Sin3a` 1433, `Rnpc3` 868, `Zbtb7a` 841, `Psmb4` 742, `Yy1` 720.

3. Declared expression Parquet `training_de_all_cell_groups.parquet`, filtered to `151 TH Prkcd Grin2c Glut` and visible chromatin/transcriptional comparators.
   - No close visible HMGB-family perturbation was present in the count table; the only `Hmg*` training row was `Hmgcr`, which is not a chromatin paralog.
   - Low architectural or broad transcriptional comparators in this cell class were near-null:
     - histone/HMG-like structural rows: `H2ac8` 0, `H3f3a` 0, `H4c11` 0, `Set` 0
     - remodeler or cofactor rows with small footprints: `Smarca4` 0, `Smarca2` 1, `Mef2c` 1, `Mef2a` 4, `Brd1` 4, `Crebbp` 8
   - More immediate and less redundant chromatin regulators gave much larger counts:
     - `Kdm5c` 18, `Setdb1` 22, `Chd2` 34, `Chd8` 61, `Chd4` 100, `Ctcf` 270, `Brd4` 311, `Setd1a` 368, `Yy1` 720, `Hnrnpu` 733
   - The Parquet slice exactly reproduced the count-table FDR calls for this cohort; each visible comparator had 17259 measured-gene rows in the 151 class.

## Synthesis

Hmgb1 is reachable in the focal population and is not a biologically inert target, so a categorical zero is slightly too pessimistic. The assay window, however, is expected to catch only the leading edge of HMGB1 protein depletion, and the closest measured training context lacks an Hmgb2/Hmgb3 direct analog. The visible chromatin regulators with large `n_degs` mostly disrupt immediate chromatin-remodeling, transcriptional, or nuclear-RNA machinery, while stable architectural and broad-factor perturbations cluster at 0-8 DEGs.

I therefore placed Hmgb1 just above the modal null regime and below the CHD/BRD/SETD/CTCF tail. The point forecast is `1`.
