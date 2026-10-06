# Direct Gata2 n_degs forecast

## Declared target and endpoint

- Target: `Gata2`, the single row in the declared holdout manifest `Gata2.csv`.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, counted as measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Visible training endpoint table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Visible profile table: `[local file: training_de_all_cell_groups.parquet]`.
- Biology bundle: `[local file: Gata2.json]`, sha256 `434f266d79954d3588d1af57db1d3818e00fb68d420f4196f5e716a96550384e`.

I did not query a same-experiment `Gata2` report or any held-out `Gata2` response rows. Same-experiment Findings were used only for visible training perturbations and are not independent replication of the Parquet.

## Evidence Used

1. **Exact in-assay target reach is extremely small.** In non-targeting nuclei from `151 TH Prkcd Grin2c Glut`, the canonical biology bundle reports `Gata2` expression in 35 of 23,679 cells, `0.147810296%`, with only 38 total target UMIs, mean raw UMI `0.0016047975`, mean CP10K `0.0010014068`, and pseudobulk CPM `0.1005783501`. This supersedes qualitative regional-expression evidence for this focal cell class. GATA2 is a free nuclear transcription factor whose functional pool should substantially decline over 21-28 days if a cell is edited, but the exact focal population contains very few Gata2-expressing nuclei to perturb.

2. **The focal training count distribution is null-dominated.** Among the 1,674 visible training perturbations in the `151 TH Prkcd Grin2c Glut` count table, 1,205 have `n_degs = 0`; the median is 0, the 90th percentile is 2, the 95th percentile is 18, and the right tail is driven by a small set of broad essential or pleiotropic targets.

3. **Visible GATA-family and GATA-associated analogs are focal nulls.** The closest visible family members and represented comparators have exact focal counts:

| target | visible focal `n_degs` |
|---|---:|
| `Gata1` | 0 |
| `Gata3` | 0 |
| `Gata4` | 0 |
| `Gata6` | 0 |
| `Zfpm2` | 0 |
| `Lmx1b` | 0 |
| `Klf1` | 0 |
| `Gfi1b` | 0 |
| `Isl1` | 0 |
| `Slc32a1` | 0 |

Direct Parquet inspection in `151 TH Prkcd Grin2c Glut` confirmed that each of those ten training perturbations had 17,259 measured genes and zero genes at `pvals_adj < 0.05`.

4. **The GATA-family same-experiment corpus reinforces a lineage and timing boundary.** In the selected July 260713 corpus, `Gata1` is summarized as a complete neuronal DE null across all 23 measured cell groups, while `Gata3` is summarized as almost completely buffered across the P16-to-P37/P44 neuronal panel, with directly measurable GATA-family and GATA-associated neural comparators failing to phenocopy `Gata3`. That corpus view is a curated interpretation of the same experiment, not another measurement, but it supports the biological reading that obvious GATA paralogs and partners are not carrying a shared postmitotic thalamic response.

5. **Profile comparison did not reveal a hidden local module among the visible analogs.** A symmetric score-vector comparison of `Gata1`, `Gata3`, `Gata4`, `Gata6`, `Zfpm2`, `Lmx1b`, `Klf1`, `Gfi1b`, `Isl1`, and `Slc32a1` in the focal cell class classified all 10 nodes as `no_significant_features`. Whole-profile Pearson/cosine values among the inspected GATA and peer perturbations were near zero, so these weak rank vectors do not provide positive evidence for a recurrent response that would overcome the exact low Gata2 reach.

## Forecast

The high-confidence downward bearing is the exact target reach: only 0.15% of non-targeting focal nuclei contain detectable `Gata2` RNA, so even a successful loss of a renewable GATA2 protein pool is expected to affect at most a tiny fraction of the aggregated thalamic glutamatergic class. The developmental midbrain fate-switch evidence shows that Gata2 can be potent in the right embryonic lineage, but the biology bundle explicitly leaves postnatal thalamic maintenance unresolved. The visible closest GATA-family/partner perturbations are all endpoint nulls in this same focal class, which makes a broad mature-thalamic response unlikely.

Residual uncertainty is that a rare `Gata2`-positive thalamic subtype could be diluted in the class aggregate, or selection could hide an edited-cell response. Neither possibility argues for many BH-significant genes in the observed broad focal contrast. I therefore choose the modal exact count rather than a small positive tail value:

`predicted_n_degs = 0`
