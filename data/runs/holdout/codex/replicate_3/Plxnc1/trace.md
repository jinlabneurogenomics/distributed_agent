# Plxnc1 n_degs forecast

Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05` for `Plxnc1` in `151 TH Prkcd Grin2c Glut`.

## Evidence used

- The one-row holdout manifest declares `Plxnc1`; `Plxnc1` is absent from the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table.
- The Plxnc1 biology bundle reports exact in-assay focal reach rather than an outcome: in matched non-target nuclei from `151 TH Prkcd Grin2c Glut`, `Plxnc1` was a measured feature, was detected in 13,830 of 23,679 nuclei, had `pct_cells_expressing = 58.406`, `mean_raw_umi = 1.231`, `mean_log1p_cp10k = 0.466`, and `pseudobulk_cpm = 77.162`.
- The same bundle adjudicates Plexin-C1 as a renewable single-pass Sema7A receptor whose operative stock is likely substantially depleted by the P37-P44 harvest after a P16 disruptive edit. That supports target engagement in principle, but with only partial evidence completeness: the direct postnatal phenotypes are olfactory bulb and cerebellar rather than thalamic, thalamic expression evidence outside this assay is discordant, Plexin-C1-specific protein lifetime in postmitotic neurons was not found, and Integrin-beta1/Sema7A pathway sharing has no matched thalamic compensation test.
- The training count table is strongly concentrated at the floor even in this high-yield thalamic class: 1,205/1,674 training targets have `n_degs = 0`, 1,481/1,674 have `n_degs <= 1`, the median is 0, and the upper tail is dominated by core RNA/protein-homeostasis regulators rather than cell-surface guidance receptors.
- I treated the source-card related genes and the same signaling class as the closest endpoint comparators. In the declared count table, the direct pathway partner `Itgb1` had 0 DEGs and the same-family neuronal turnover proxy `Plxnd1` had 0. Plexin/semaphorin/coreceptor comparators were similarly quiet: `Plxna1 = 0`, `Plxna2 = 1`, `Plxna4 = 0`, `Sema4d = 0`, `Sema6a = 0`, `Nrp1 = 0`, and `Nrp2 = 0`.
- The focused Parquet query for nearby guidance/synapse receptors showed that the one-DEG cases in this group were isolated self-transcript hits, not downstream thalamic programs: `Plxna2`, `Epha4`, `Robo1`, `Cadm2`, `Cntnap1`, `Cntnap2`, `Ncam1`, `Nlgn3`, `Nrxn1`, `Sema5a`, and `Unc5c` each had only the perturbed transcript itself passing `pvals_adj < 0.05`.
- The profile comparison over 12 matched guidance/receptor perturbations in the declared Parquet found no missing profiles and classified 9/12 as `no_significant_features`; the remaining 3 were in the `1_to_9_significant_features` bucket. A cohort projection showed weak positive-tail sharing and no significant-program overlap, so there was no coherent nonzero survivor-state module to transfer to Plxnc1.

## Reasoning

Plxnc1 should be biologically reachable in the assayed population: the target transcript is detectable in many focal non-target nuclei, and a membrane-receptor stock should turn over during the 21-28 day experimental window. I therefore did not treat Plxnc1 as absent, unedited, or nonfunctional.

The requested endpoint, however, is not a synaptic-pruning phenotype; it is a BH-significant nuclear RNA footprint among recovered thalamic glutamatergic nuclei. The closest measured perturbations to Plexin-C1 biology sit at the empirical floor in this exact endpoint. In particular, `Itgb1` and `Plxnd1` both had zero significant genes, most semaphorin/plexin/coreceptor genes also had zero, and the nonzero adhesion/guidance examples usually contributed just the edited transcript itself. That pattern supports a prediction of a null or nearly null measured footprint, with no evidence for a broad downstream response.

I set the integer point forecast to the floor of this analogue distribution:

`predicted_n_degs = 0`
