# Pax1 direct DEG-count forecast

## Declared target

- Target manifest: `Pax1`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Forecasted endpoint: `n_degs`

I used the declared biology-only `Pax1.json` bundle, the declared 151 TH training count table, and a direct Parquet check of the selected training comparators. I did not use a Pax1 target outcome, Pax1 same-experiment report text, a calibrated response probability, labeled-neighbor outcomes, endpoint-selection metadata, or any branch/terminal prediction review artifact.

## Target-side biology

The exact in-assay reach measurement is the dominant target-side datum. In non-target `151 TH Prkcd Grin2c Glut` nuclei, `Pax1` had:

- `n_non_target_cells = 23679`
- `n_cells_expressing = 0`
- `pct_cells_expressing = 0.0`
- `total_target_umi = 0.0`
- `mean_raw_umi = 0.0`
- `mean_cp10k = 0.0`
- `pseudobulk_cpm = 0.0`

Thus Pax1 RNA was not observed at all in the recovered control nuclei from the exact population being scored. That does not mathematically rule out pre-existing Pax1 protein or rare edited cells, but it makes a 21-28 day postnatal knockout unlikely to remove an actively renewed transcription factor program in the assayed survivors.

The biological card is consistent with a weak short-window forecast:

- Pax1 is a nuclear paired-box sequence-specific transcriptional activator.
- The defined Pax1-null mouse phenotype is embryonic and non-neural, centered on axial skeleton and thymic development.
- Regional adult mouse thalamus has only trace-to-very-low Pax1 RNA in the external expression summaries captured by the bundle.
- Pax9 can partly compensate Pax1 loss in embryonic sclerotome, but that redundancy is not demonstrated in postmitotic thalamic neurons.
- Pax1 protein turnover, chromatin residence, and depletion kinetics over the P16 to P37-P44 window are unknown; the functional-stock adjudication is therefore indeterminate rather than confidently depleted.

Given zero RNA reach in the exact focal controls, the unknown stock kinetics mainly add uncertainty around an already inactive-looking target rather than supplying a reason to expect a large survivor transcriptional state.

## Training measurements

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 measured training perturbations. It is heavily zero-inflated in this focal cell class:

- `n_degs = 0`: 1,205 / 1,674
- median: 0
- 75th percentile: 1
- 90th percentile: 2
- 95th percentile: 18
- maximum: 2,677

Typed analog nomination against the exact training universe found no Pax1 candidate in the exact-complex/paralog, bidirectional-corpus-comparator, narrow-module, or direct-interaction/dependency tiers. All 798 nominated measured genes were broad functional fallbacks, so they were treated as developmental/transcription-factor context rather than close endpoint analogs.

The strongest fallback candidates were mostly null in the endpoint itself:

- Top 10 broad fallback candidates: 9 zeros, median 0, maximum 1.
- Top 20 broad fallback candidates: 17 zeros, median 0; the main large exception was the generic Wnt/developmental node `Ctnnb1`, with 383 DEGs.
- The nominated measured Pax-family genes were also all null: `Pax2 = 0`, `Pax3 = 0`, `Pax4 = 0`, `Pax6 = 0`, `Pax7 = 0`, and `Pax8 = 0`.

A direct filtered read from `training_de_all_cell_groups.parquet` for the measured Pax genes plus the leading fallback cohort confirmed that the same selected rows were quiet in `151 TH Prkcd Grin2c Glut`: among those targets, only `Smad2` with 1 row and `Ctnnb1` with 383 rows had any `pvals_adj < 0.05` entries.

## Point forecast

I put most weight on the exact absence of Pax1 RNA in 23,679 focal non-target nuclei, then used the training distribution and measured developmental TF/Pax comparators as local scale checks. The plausible upward errors are rare Pax1-positive cells below the expression-reach limit, long-lived pre-edit Pax1 stock, or an indirect stress/off-target state, but none is supported strongly enough to move the point forecast out of the modal zero bin.

Forecast: `Pax1` has `0` FDR-significant genes in `151 TH Prkcd Grin2c Glut`.
