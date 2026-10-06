# Pax1 `n_degs` forecast

## Declared target and endpoint

- Target: `Pax1`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Prediction: `0`

## Evidence used

1. The run-local holdout manifest and biology bundle both declare `Pax1` as the single target.
2. The Pax1 biology bundle reports exact in-assay focal reach of zero: in `151 TH Prkcd Grin2c Glut` non-target nuclei, Pax1 had `0` UMIs across `23,679` nuclei, `0` expressing cells, `mean_cp10k = 0.0`, `mean_log1p_cp10k = 0.0`, and `pseudobulk_cpm = 0.0`.
3. The same bundle characterizes Pax1 as a nuclear paired-box sequence-specific transcriptional activator with defined mouse loss phenotypes in embryonic axial skeleton and thymic development, not in acute postnatal thalamic neurons. Its functional stock at P37-P44 after a P16 edit is indeterminate because no Pax1 protein half-life, chromatin residence, or depletion trajectory was available in a transferable neuronal context.
4. The selected same-experiment corpus release contained no Pax1 target report, Claim, or explicit Pax1 comparator Finding, so it did not add a target-specific measured signature or a strong corpus analogue.
5. The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 training perturbations. Its distribution is sparse: 1,205/1,674 have `n_degs = 0`, the median is `0`, the 75th percentile is `1`, the 90th percentile is `2`, and the 95th percentile is `18`.
6. Developmental and paired-box transcription-factor comparators in the same focal cell count table were quiet: `Pax2`, `Pax3`, `Pax4`, `Pax6`, `Pax7`, and `Pax8` each had `0` DEGs; `Atoh1`, `Dlx3`, `Dlx6`, `Foxa2`, `Foxp2`, `Foxp3`, `Neurod1`, `Neurod2`, `Otx2`, `Sox4`, `Sox9`, `Sox10`, `Sox11`, and `Tbr1` also had `0`; `Sox2` and `Sox5` had `2`.
7. Direct inspection of `training_de_all_cell_groups.parquet` in the focal group confirmed the same count-table calls for these comparators: the queried Pax-family and developmental TF perturbations each had 17,259 measured genes, and all except `Sox2` and `Sox5` had no rows with `pvals_adj < 0.05`.
8. A typed annotation nomination against the 1,674-gene training universe found only `broad_functional_fallback` Pax1 nominees, with no exact paralog/complex, narrow-module, direct-interaction, or bidirectional-corpus comparator tier. Among the leading 25 broad nominees, 22 had `0` DEGs in the focal count table; the nonzero rows were `Smad2 = 1`, `Crebbp = 8`, and `Ctnnb1 = 383`.

## Reasoning

The endpoint is a same-population transcriptional footprint in recovered thalamic glutamatergic neurons. Pax1's own focal-population target RNA was exactly undetected in the non-target cells used for the expression-reach measurement, so a Pax1 edit has little evidence of an expressed Pax1-dependent regulatory program to perturb in this recovered population. The developmental skeletal/thymic Pax1-null biology establishes that the gene can matter in the right embryonic tissues, but it does not establish acute postnatal thalamic demand; the functional-stock card likewise leaves Pax1 stock loss by harvest unresolved rather than arguing for a delayed hidden effect.

Quantitatively, the focal training endpoint is dominated by zeroes, and the high tail is mostly ubiquitous RNA-processing, proteostasis, transport, or chromatin regulators. The closest available Pax-family and developmental TF perturbations are nearly all zero in the exact focal count table and in the raw Parquet-derived FDR rows. The broad annotation nominees are less specific than the Pax-family comparators; most are also zero, and the larger nonzero value for `Ctnnb1` is plausibly a Wnt/adhesion hub effect rather than a Pax1-scale donor.

I therefore place Pax1 at the modal zero-response point rather than borrowing a positive count from high-yield but mechanistically broad machinery perturbations.
