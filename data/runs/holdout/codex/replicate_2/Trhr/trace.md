# Trhr DEG-count forecast for `151 TH Prkcd Grin2c Glut`

## Declared target and endpoint

- Target from the one-row holdout manifest: `Trhr`.
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05` in `151 TH Prkcd Grin2c Glut`.
- Evidence used:
  - canonical biology-only `Trhr` bundle at `biology_bundles/Trhr.json`;
  - declared exact-cell-group training counts at `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`;
  - declared training DE parquet at `training_de_all_cell_groups.parquet`, filtered to the same cell group and selected training perturbations.

## Biology of `Trhr`

The canonical bundle identifies `Trhr` as a seven-transmembrane TRH receptor coupled to phosphatidylinositol/IP3-calcium-PKC signaling. Loss can matter in neural tissue: germline mouse `Trhr1` loss has endocrine and behavioral phenotypes, and `Trhr2` is a related TRH-responsive receptor with distinct in-vivo effects.

Those positive priors are weakly matched to this assay. The operation is loss of new receptor supply after a P16 CRISPR edit; it does not directly inactivate receptor already present before editing. The bundle found rapid TRHR trafficking/recycling but no endogenous postmitotic neuronal degradation half-life, so functional receptor depletion by the P37-P44 harvest is indeterminate.

The exact in-assay reach is very small. In non-target nuclei for `151 TH Prkcd Grin2c Glut`, `Trhr` was detected in 155 of 23,679 nuclei, with mean CP10K `0.005085875`, mean raw UMI `0.008023987`, and pseudobulk CPM `0.502891751`. The exact focal expression therefore supersedes qualitative thalamic reporter evidence and makes any receptor-dependent transcriptional state highly diluted in this aggregated thalamic class.

## Task-matched training scale

The declared count table for this exact endpoint contains 1,674 training perturbations:

- 1,205 / 1,674 have `n_degs = 0` in `151 TH Prkcd Grin2c Glut`.
- Median `n_degs` is `0`.
- 75th percentile is `1`; 90th percentile is `2`.
- 88.47% of training targets are at `0` or `1` DEG.
- The upper tail exists, but the largest burdens are from broad cellular regulators and machinery perturbations such as `Uba5`, `Tpr`, `Sin3a`, spliceosome, proteasome, and RNA-processing genes rather than restricted neuromodulatory receptors.

I used the parquet to inspect a biologically close surface-receptor subset in the same cell group: `Npy1r`, `Npy2r`, `Npy5r`, `Oprd1`, `Oprk1`, `Oprl1`, `Oprm1`, `Sstr5`, `Tacr3`, `Cckar`, `Cckbr`, `Galr1`, `Htr1a`, `Htr1b`, `Htr1f`, `Htr2a`, `Htr2b`, `Htr2c`, `Htr4`, `Htr6`, `Htr7`, `Chrm2`, `Chrm3`, `Adra1a`, `Adra2a`, `Adra2b`, `Adrb2`, and `Adrb3`. Each had 17,259 measured-gene rows in `151 TH Prkcd Grin2c Glut`; all 28 had zero BH-significant genes. The smallest adjusted p-value among them was still above threshold (`Htr2b`, `0.0629584`), and nearly all minima were far from significance.

## Point synthesis

`Trhr` has real ligand-receptor biology, so a nonzero survivor-state signature is not impossible if the receptor pool turns over and if the edited nuclei fall in a receptor-positive subpopulation. The stronger task-matched bearings all point lower:

- only `0.6546%` of assayed non-target nuclei in this focal class detect `Trhr`;
- pre-edit GPCR persistence through the 21-28 day edit-to-harvest window is unresolved;
- the strongest mouse phenotypes are germline and whole-animal, not acute P16 thalamic-neuron loss;
- the exact endpoint has a dominant zero mass;
- task-matched neuromodulatory receptor perturbations in the training parquet are almost uniformly quiet.

I therefore place `Trhr` at the zero endpoint mode and predict no measured genes passing BH-adjusted Wilcoxon `p < 0.05`.
