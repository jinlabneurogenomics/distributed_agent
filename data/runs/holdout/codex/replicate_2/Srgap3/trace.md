# Srgap3 direct forecast

## Target and endpoint

- Target: `Srgap3`, the only row in `[local file: Srgap3.csv]`.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, defined as the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Direct endpoint source for training targets: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Direct profile source for training targets: `[local file: training_de_all_cell_groups.parquet]`.
- Srgap3 target characterization: `[local file: Srgap3.json]`, `sha256=82f3d32c91423c135bfd18b1fb0654de26990dd8319aabd8b43725bb06fdae15`.

The target profile and target count were not used. The selected same-experiment corpus release returned no target-local Findings or Claims for `Srgap3` (`target_found=false`), so the target side came from the declared biology bundle rather than from a packaged report of the held-out perturbation.

## Biology used

The packet symbol `Srgap3` denotes Entrez 14270 / ENSMUSG00000026425, now official mouse `Srgap2` with historical alias `srGAP3`, not the distinct current mouse `Srgap3` locus. The biology bundle characterizes this as a cytosolic, F-BAR/RhoGAP/SH3 membrane-remodeling protein enriched at postsynaptic sites. A disruptive P16 edit should stop new SRGAP2 supply while leaving any already existing protein and spine structure to decay or remodel.

The functional-stock card adjudicates the harvest state as `likely_substantially_depleted`: rescued postmitotic mouse cortical-neuron knockdown altered spine morphology within 9-10 days, shorter than the 21-28 day edit-to-harvest interval. That supported treating Srgap3 as biologically engaged by harvest, while keeping the main endpoint projection uncertain because the direct evidence is cortical/spine morphology rather than thalamic nuclear RNA.

The exact focal-population expression measurement showed Srgap3 RNA was measurable but not broad in the 151 class: mean CP10K `0.270845`, mean log1p CP10K `0.184694`, and `7,313 / 23,679` non-target nuclei expressing it (`30.884%`). This is enough that a functional edit is plausible, but it leaves substantial dilution in an aggregated thalamic class and does not guarantee a detectable self-transcript hit.

## Training measurements used

The declared 151-class training count table is zero-heavy:

- `1,674` training targets.
- `1,205` had `n_degs = 0`.
- Median `n_degs = 0`.
- 75th percentile `= 1`; 90th percentile `= 2`; 95th percentile `= 18`.

I therefore did not use the all-target mean of `14.054` as a central prior; it is inflated by a very small number of broad-response targets, while most observed postnatal neuronal perturbations are quiet at BH<0.05 even in this high-yield thalamic group.

For the biologically closest represented training perturbations, I used Rac/Cdc42/Kalirin/Tiam, GEF/GAP, WRC, PAK/LIMK/cofilin, EphB, PSD, and cytoskeletal comparators. Their exact 151-class count-table outcomes were:

`Rac1 0`, `Cdc42 1`, `Kalrn 0`, `Tiam1 0`, `Ephb1 0`, `Ephb2 0`, `Dock3 0`, `Fgd4 0`, `Arhgap18 0`, `Arhgap32 0`, `Arhgef9 1`, `Cyfip1 0`, `Cyfip2 1`, `Pak1 1`, `Pak2 0`, `Pak3 0`, `Limk1 0`, `Cfl2 0`, `Baiap2 0`, `Dlg4 1`, `Syngap1 0`, `Actg1 1`, `Specc1l 0`.

That cohort had `17 / 23` zeros and `6 / 23` one-DEG calls, with no member above one DEG. A direct Parquet query over the same 23 targets showed all six significant rows were self-transcript rows:

`Actg1->Actg1`, `Arhgef9->Arhgef9`, `Cdc42->Cdc42`, `Cyfip2->Cyfip2`, `Dlg4->Dlg4`, and `Pak1->Pak1`.

Thus, within the selected actin/spine-signaling analogs, no perturbation produced even one downstream BH<0.05 RNA feature in `151 TH Prkcd Grin2c Glut`.

The run-local matched Parquet comparison in `workbench/srgap3_actin_profile_compare.json` used these 23 nodes at `group_name = 151 TH Prkcd Grin2c Glut`, `value_column = logfoldchanges`, and `significance_column = pvals_adj < 0.05`. It reproduced the same activity scale: 17 nodes had no significant features and 6 had only 1-9. The bounded inspection in `workbench/srgap3_actin_profile_inspect.json` confirmed exact zero downstream-significant features for the focal anchors `Rac1`, `Kalrn`, `Tiam1`, and `Arhgap32`, and one self-only feature for `Cdc42`.

The same-experiment corpus Claim `claim:1aeabad1e41e30f971bc` independently summarized the actin/Rac/Cdc42 neighborhood within the same experiment: represented Rac/Cdc42-linked actin-cytoskeleton signaling perturbations were transcriptionally buffered and did not form a recurrent shared nuclear mRNA module. I used that as semantic interpretation of the same Parquet-era observations, not as an independent replicate.

## Synthesis

The forecast separates biological realization from RNA visibility. Srgap3/Srgap2 loss should be functionally realized by harvest and may affect spine morphology, but the training perturbations that most closely occupy the same local postsynaptic Rho-family/cytoskeletal biology almost never create downstream BH<0.05 features in this assay. Their rare one-count outcomes are entirely explained by detectable self-transcript rows, not by a shared downstream actin/spine state.

The exact Srgap3 expression reach argues against forcing a self-only `1`: only about 31% of focal non-target nuclei express detectable Srgap3, the baseline level is low, and the PerturbAI portrait cautions that CRISPR loss often is not visible as nuclear target-transcript reduction. I therefore put the mode at the observed analog null rather than at a self-only singleton.

Point prediction: `0`.
