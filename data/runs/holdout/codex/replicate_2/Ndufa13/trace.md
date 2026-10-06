# Direct forecast trace

Target: `Ndufa13`

Predicted endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, defined as the count of measured genes with BH-adjusted Wilcoxon `p < 0.05`.

## Declared inputs used

- Holdout manifest: `Ndufa13.csv` contains one target, `Ndufa13`.
- Focal training count table: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`; `Ndufa13` is absent.
- Declared training DE Parquet: `training_de_all_cell_groups.parquet`, filtered only to training targets in the focal `151 TH Prkcd Grin2c Glut` class.
- Canonical biology bundle: `biology_bundles/Ndufa13.json`.
- Packaged same-experiment corpus summaries for measured training comparators `Ndufs2`, `Ndufs4`, `Ndufv1`, and `Opa1`; these are interpreted reports over the same Perturb-seq experiment, not independent replication.

## Evidence that determined the point

1. The target is present in the assayed focal population.

   The exact target-expression bundle reports `Ndufa13` expression in 22,743 of 23,679 non-target `151 TH Prkcd Grin2c Glut` nuclei, or 96.05%, with mean raw UMI 4.51 and mean log1p CP10K 1.25. This makes a self-transcript call technically plausible if the guides produce an mRNA-visible allele, but it does not quantify editing or functional knockout strength.

2. The expected lesion is a slowly realized complex-I assembly lesion.

   The biology card places NDUFA13 in mitochondrial respiratory complex I and judges the relevant functional stock at the P37-P44 harvest as `partially_depleted_or_leading_edge`: a P16 disruptive edit should stop new NDUFA13 supply, but already assembled complex I should persist initially, and the closest in-vivo neuronal mitochondrial-protein turnover proxy is near the 21-28 day harvest interval. This supports possible biological effect but argues against assuming a fully penetrant acute OXPHOS-collapse state.

3. The focal count table is globally sparse and the close complex-I training class is even more tightly near-null.

   In the declared focal training table, 1,205 of 1,674 training perturbations have `n_degs = 0`; the median is 0, the 75th percentile is 1, and only 106 targets have at least 10 DE genes. For the directly relevant nuclear complex-I/assembly set in the count table
   `Ndufa10,Ndufa11,Ndufa12,Ndufa6,Ndufa8,Ndufa9,Ndufaf2,Ndufaf4,Ndufaf5,Ndufb10,Ndufb11,Ndufb8,Ndufb9,Ndufc2,Ndufs2,Ndufs4,Ndufs7,Ndufs8,Ndufv1,Ndufv2,Timmdc1`,
   the 21 focal counts have sum 10, mean 0.48, median 0, 11 zeros, 10 ones, and maximum 1. A broader 35-target nuclear ETC panel had the same shape: sum 15, median 0, maximum 1.

4. The DE Parquet shows that those one-count complex-I observations are not small shared stress modules.

   The exact BH-significant rows for the OXPHOS analogs in `151 TH Prkcd Grin2c Glut` show that the one-gene calls for `Ndufa10`, `Ndufa6`, `Ndufb10`, `Ndufb11`, `Ndufb8`, `Ndufb9`, `Ndufc2`, `Ndufs2`, and `Ndufs8` are their own target transcripts; `Ndufv2` contributes a single `Cdc40` row while its self transcript is not significant. A symmetric profile comparison of 26 mitochondrial/OXPHOS training targets in the same Parquet produced 12 targets with no significant features, 13 with 1-9 significant features, and only `Opa1` in the 10-49 bin. The cohort diagnostic did not reveal a recurrent significant program shared across the NDUF complex-I analogs.

5. The same-experiment corpus supports the raw-profile interpretation.

   The report layer for `Ndufs2`, `Ndufs4`, and `Ndufv1` assigns represented nuclear complex-I subunits and assembly factors to a buffered, flat-or-sparse transcriptional class that lacks a shared acute OXPHOS/ATF4 stress module in this P16-to-P37/P44 neuronal CRISPR/snRNA-seq assay. `Opa1` anchors a real mitochondrial ATF4/ISR-like response in the same dataset, so the OXPHOS nulls are not just global readout blindness, but `Opa1` is an inner-membrane dynamics perturbation and a positive stress benchmark rather than a same-complex numerical analog.

## Synthesis

The dominant quantitative anchor is the directly matched complex-I family in the focal count table: every close nuclear complex-I or NDUFAF comparator is either 0 or 1 DEG, and most nonzero calls are only the measured self transcript. NDUFA13 is an accessory NDUF subunit with a partially depleted installed complex-I stock by harvest, so a broad downstream stress footprint is unlikely in recovered thalamic nuclei. Its high in-assay expression makes a single self-transcript call more plausible than a strict zero.

I therefore predict a near-null response with exactly one BH-significant measured gene.
