# Gpr68 DEG-count forecast

## Declared endpoint

- Target: `Gpr68`
- Population: `151 TH Prkcd Grin2c Glut`
- Endpoint: measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05` in the thalamic perturbation contrast
- Declared training scalar: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, 1,674 observed training perturbations
- Declared profile table: `training_de_all_cell_groups.parquet`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"` for matched profile checks

## Biology-only Gpr68 evidence

The target card reports exact focal expression rather than a qualitative reach guess: `Gpr68` was detected in 9,377 of 23,679 non-target nuclei in this population, or 39.6005%, with mean log1p CP10K of 0.244247. This makes the perturbation at least expressible in a sizeable subpopulation, but the card also notes that expression reach does not establish editing efficiency or dependence of a basal transcriptional state on GPR68.

GPR68 is an extracellular proton-sensing GPCR. Its clearest mouse-neural phenotypes are adult hippocampal physiology/behavior phenotypes in germline loss and neuroprotection under acidosis or ischemia. Those support real neural observability outside the exact assay but do not establish a tonic requirement in healthy postnatal thalamic glutamatergic neurons. The functional-stock adjudication favors partial depletion by the 21-28 day harvest window: a disruptive edit should stop new receptor synthesis, but existing surface receptor can persist until normal turnover, and no GPR68-specific neuronal half-life was found.

That combination pushed the forecast upward from an inexpressed/null receptor, but only weakly: `Gpr68` should be partially realized in many assayed neurons, yet it is a conditional membrane receptor rather than a chromatin, proteostasis, RNA-processing, or core survival factor.

## Matched training measurements

The full scalar table in the requested cell class is extremely floor-heavy:

- 1,205 / 1,674 training perturbations have `n_degs = 0`.
- 1,481 / 1,674 have `n_degs <= 1`.
- Only 106 / 1,674 have `n_degs >= 10`, and only 43 / 1,674 have `n_degs >= 100`.
- The largest signatures come from broadly disruptive factors such as `Uba5` 2677, `Tpr` 1768, `Sin3a` 1433, `Rnpc3` 868, `U2af2` 828, and `Psmb4` 742, not from receptor-level signaling.

I then checked a hand-curated GPCR/heptahelical-receptor training cohort containing 80 targets in the same scalar table. Seventy were exactly 0 DEGs; the remaining ten were exactly 1 DEG. No GPCR-like comparator in that cohort exceeded 1 DEG in `151 TH Prkcd Grin2c Glut`.

Immediate GPCR-cascade perturbations in the training table were also near the floor. `Gnas`, `Prkca`, `Plcb1`, `Adcy1`, `Adcy3`, `Adcy5`, `Mapk1`, `Camk2a`, `Camk2g`, `Rgs6`, `Gnb5`, `Pde10a`, `Pde1c`, `Pde4b`, `Pde4d`, and `Itpr1` all had 0 DEGs; `Gnao1` had 1; and the broader calcium-effector node `Ppp3ca` had 4.

As a parquet cross-check, I ran a matched profile comparison over 13 receptor/proximal-signaling perturbations (`Cnr1`, `Gabbr1`, `Gabbr2`, `Grm1`, `Grm7`, `Gnas`, `Gnao1`, `Prkca`, `Plcb1`, `Ppp3ca`, `Adcy1`, `Adcy5`, `Mapk1`) in `151 TH Prkcd Grin2c Glut`. The profile-derived significant-feature counts were all 0 to 4: six nodes had no significant features and seven had 1 to 4. This confirmed directly on the DE parquet that this receptor/signaling neighborhood produces tiny matched signatures, not a hidden high-burden module.

## Synthesis

The exact GPR68 reach and partial-stock call make a zero outcome uncertain, so I did not treat the perturbation as absent or technically impossible. The best outcome-matched comparators, however, put surface GPCRs and proximal GPCR signaling at the empirical floor in this thalamic class. Because the located GPR68 loss biology is largely conditional on pH stress or transferred from hippocampus, there is no strong reason to move it away from that floor for a healthy 21-28 day thalamic snRNA-seq assay.

I therefore predict a floor response:

`predicted_n_degs = 0`
