# Direct forecast for Sry in `151 TH Prkcd Grin2c Glut`

## Point prediction

`predicted_n_degs = 0`

## Evidence used

- The one-row declared manifest names `Sry` as the only target.
- The requested focal population is exactly `151 TH Prkcd Grin2c Glut`, i.e. thalamic glutamatergic neurons rather than tyrosine-hydroxylase dopaminergic neurons.
- In the canonical `Sry` biology bundle, the exact focal non-target expression measurement is zero:
  - expression feature: available
  - group: `151 TH Prkcd Grin2c Glut`
  - `n_non_target_cells = 23679`
  - `n_cells_expressing = 0`
  - `pct_cells_expressing = 0.0`
  - `total_target_umi = 0.0`
  - `pseudobulk_cpm = 0.0`
- The same bundle supports realization only in Sry-expressing neurons: SRY is a nuclear, short-lived transcription factor, so a P16 disruptive edit should deplete active SRY by the P37-P44 harvest where the gene is being renewed. That stock argument does not create a focal effect where no Sry RNA is detected in the assayed thalamic population.
- The direct neural positive-control biology for Sry is from adult rodent substantia nigra dopaminergic neurons after Sry antisense treatment. That is outside the requested thalamic glutamatergic class, and the Sry source card explicitly leaves postnatal mouse thalamic cellular reach unresolved before exact in-assay reach supersession.
- The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table is sparse:
  - 1,674 training perturbations
  - 1,205 with `n_degs = 0`
  - median `n_degs = 0`
  - 75th percentile `n_degs = 1`
  - 90th percentile `n_degs = 2`
  - 95th percentile `n_degs = 18`
- Training Sox-family perturbations available in the same 151-class count table did not show a large local footprint:
  - `Sox9`, a source-card paralogous developmental comparator for Sry HMG-domain activity: 0 DEGs
  - `Sox4`, `Sox10`, `Sox11`, `Sox17`, `Sox18`: 0 DEGs
  - `Sox2`, `Sox5`: 2 DEGs each
- Re-reading the matching rows in `training_de_all_cell_groups.parquet` for those Sox targets in `151 TH Prkcd Grin2c Glut` reproduced the same 0-or-2 significant-gene counts at BH-adjusted Wilcoxon `p < 0.05`.
- In the same training Parquet and focal group, no training profile had a DE row with `names = 'Sry'`, consistent with Sry being absent as an expressed/measured focal feature across the visible 151-class training contrasts.

## Synthesis

The biology bundle says an edited Sry allele should matter within 21-28 days only in cells that rely on ongoing SRY production. The exact focal measurement found no Sry molecules in 23,679 non-target thalamic glutamatergic nuclei, so the assayed recovered 151-class population has no detectable substrate for Sry loss. The one well documented postnatal neuronal Sry phenotype is nigral and dopaminergic, not thalamic glutamatergic, and the related Sox transcription-factor perturbations in the same training class sit at the floor of the observed DEG distribution. I therefore assign the target to the zero component of the highly zero-inflated 151-class count distribution and predict no FDR-significant measured genes.
