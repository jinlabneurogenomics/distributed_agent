# Ddr2 direct DEG-count forecast

## Target and endpoint

- Target manifest: `Ddr2`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Forecasted endpoint: number of measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05`.

## Evidence used

1. **Declared Ddr2 biology bundle**
   - Source: `biology_bundles/Ddr2.json`
   - The exact in-assay non-target expression reach for Ddr2 in `151 TH Prkcd Grin2c Glut` is extremely low:
     - `n_non_target_cells = 23679`
     - `n_cells_expressing = 129`
     - `pct_cells_expressing = 0.5447865197010009`
     - `mean_raw_umi = 0.006799273617973732`
     - `mean_cp10k = 0.003755938610471446`
     - `pseudobulk_cpm = 0.4261345887021869`
   - The functional-stock adjudication calls the pre-edit DDR2 receptor stock `likely_substantially_depleted` by the P37-P44 harvest after a P16 edit, based on the receptor being a renewed collagen-activated receptor tyrosine kinase and on mature DDR2 turnover within roughly a day in heterologous cells.
   - The same bundle does **not** establish a postnatal thalamic-neuron requirement: the closest mouse phenotypes are constitutive and non-neural/systemic, the same-context receptor demand is untested, and Ddr1 compensation is unresolved rather than demonstrated.

2. **Training focal-class DEG counts**
   - Source: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
   - Ddr2 is held out; the table contains 1,674 observed training perturbations for this same cell class.
   - The distribution is zero-inflated:
     - 1,205 / 1,674 training targets have `n_degs = 0`.
     - 469 / 1,674 have at least one significant gene.
     - median = 0, 75th percentile = 1, 90th percentile = 2, mean = 14.05.
     - the mean is pulled upward by a small tail of broad signatures such as `Uba5 = 2677`, `Tpr = 1768`, and `Sin3a = 1433`.

3. **Surface-receptor and cell-matrix signaling comparators from the same training table**
   - Source: the same count table, interpreted with the focal-class rows of `training_de_all_cell_groups.parquet`.
   - A manually selected receptor/co-receptor comparator set in the declared training targets was very quiet in this thalamic class: `Alk`, `Axl`, `Epha2`, `Epha3`, `Epha4`, `Epha5`, `Ephb1`, `Ephb2`, `Ephb4`, `Erbb3`, `Erbb4`, `Fgfr1`, `Fgfr2`, `Fgfr3`, `Flt3`, `Flt4`, `Igf1r`, `Insr`, `Itga2`, `Itga4`, `Itga6`, `Itga7`, `Itga8`, `Itga9`, `Itgb1`, `Kdr`, `Kit`, `Mertk`, `Met`, `Musk`, `Ntrk1`, `Ntrk2`, `Ntrk3`, `Pdgfrb`, `Ret`, `Ror1`, `Ror2`, and `Vldlr`.
   - In the count table, 36 / 38 of those receptor or adhesion perturbations had `n_degs = 0`. The only positive counts were `Ntrk2 = 3` and `Epha4 = 1`, for four significant rows in 655,842 measured-gene contrasts across the group.
   - The Parquet rows for this same set confirmed that each comparator contributed the expected 17,259 measured genes in `151 TH Prkcd Grin2c Glut`, so these were assayed profiles rather than absent targets.

## Synthesis

Loss of Ddr2 should remove newly synthesized DDR2 receptor within the experimental window, so persistent pre-edit protein is not the main reason to call the perturbation quiet. The stronger determinant is focal-population observability: Ddr2 transcript is detected in only about 0.5% of non-target nuclei in the target class, and the available biology does not show a broad juvenile thalamic-neuron dependence on collagen-DDR2 signaling. The training distribution also makes zero the modal result, and biologically nearby membrane-receptor or matrix-signaling losses in the same focal-class table almost all produced zero or only one to three significant genes.

Given those pieces together, the best integer forecast is that Ddr2 loss produces no BH-significant transcriptional signature in recovered `151 TH Prkcd Grin2c Glut` nuclei.

