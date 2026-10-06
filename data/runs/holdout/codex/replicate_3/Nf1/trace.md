# Direct DEG-count forecast for `Nf1`

## Target and endpoint

- Manifest target: `Nf1`.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, defined as measured genes with Wilcoxon `pvals_adj < 0.05`.
- Target-outcome guard: I used the declared `Nf1` biology bundle and the training count table / training Parquet. I did not query an `Nf1` DE profile or infer the held-out target count from the Parquet.

## Biology prior from the declared `Nf1` bundle

- The exact focal-population expression measurement reports `Nf1` expression in 20,079 / 23,679 non-target nuclei, `pct_cells_expressing = 84.7967`, `mean_cp10k = 1.4027`, and available target expression in `151 TH Prkcd Grin2c Glut`.
- The functional-stock adjudication calls neurofibromin a dynamic Ras-GAP homodimer whose pre-edit stock is likely substantially depleted by the P37-P44 harvest after a P16 edit. The support is partial because the turnover datum is from 293T cells and the closest postnatal timing anchor is mature oligodendrocytes, not juvenile thalamic neurons.
- The observability card supports a real postnatal neural requirement outside the assayed class, but same-context compensation and the 21-28 day neuronal latency remain unresolved.

Interpretation: the perturbation should be engaged in many focal nuclei, so a strict zero prior is too pessimistic, but the biology bundle does not by itself imply a wide DEG burden in this survivor-conditioned neuronal RNA endpoint.

## Training measurements used

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` contains 1,674 training targets. Its DEG burden is highly sparse: 1,205 / 1,674 targets have 0 DEGs, 337 have 1-4, 63 have 5-24, 10 have 25-49, 16 have 50-99, 28 have 100-499, 12 have 500-999, and 3 exceed 1,000. The median is 0 and the mean is 14.05, dominated by a small upper tail.

I manually inspected Ras/MAPK-proximal and adjacent growth-signaling perturbations available in the training table, then recomputed their focal-class FDR counts directly from `training_de_all_cell_groups.parquet` using:

```text
gene_target  n_degs
Cic          576
Tsc2         86
Braf         4
Map2k1       4
Mtor         2
Shoc2        1
Akt3         0
Hras         0
Kras         0
Map2k2       0
Mapk1        0
Pik3r1       0
Ptpn11       0
Rac1         0
Raf1         0
Rasa2        0
Sos1         0
Spred1       0
Spred2       0
```

All selected rows had 17,259 measured genes in the focal class, and the recomputed `SUM(pvals_adj < 0.05)` matched the declared count table. I did not use self-target log-fold change as an editing-efficiency weight.

## Profile comparison

I compared the 19 selected training perturbations in the exact focal class with `profile_compare` / `profile_cohort`, using `logfoldchanges` as the signed value and `pvals_adj < 0.05` as the significant-program threshold.

The count split in this biology-picked cohort was 13 no-response targets, four 1-9 DEG targets, and two targets with at least 50 DEGs. The broad Pearson/cosine values were not decisive because most genes are unchanged and all whole-profile correlations were dominated by a shared negative background component. The FDR-supported overlaps were more informative:

- `Braf` and `Map2k1` both produced only four DEGs and shared three significant downregulated genes, consistent with a reproducible but tiny MAPK-loss footprint.
- `Spred1`, `Spred2`, `Rasa2`, `Sos1`, `Ptpn11`, `Raf1`, `Mapk1`, `Hras`, and `Kras` were all FDR-quiet in the same endpoint.
- `Tsc2` was larger at 86 DEGs and `Cic` was much larger at 576 DEGs; the `Cic`/`Tsc2` pair shared only 8 positive and 7 negative significant genes and had 3 direction conflicts, so I treated them as downstream or parallel response-state boundaries rather than equal-scale `Nf1` analogues.

## Forecast

`Nf1` loss is likely functional by harvest and reaches a broad fraction of the assayed thalamic neurons, which argues for a small nonzero point rather than blindly following the many quiet Ras-pathway training rows. However, the closest available measured Ras/MAPK perturbations are overwhelmingly quiet, and the two broad-response references are either a direct transcriptional repressor loss (`Cic`) or TSC/mTOR-axis loss (`Tsc2`) whose measured programs are much wider than the direct MAPK footprints.

I therefore placed `Nf1` at the reproducible low Ras/MAPK scale, matching the `Braf` / `Map2k1` 4-DEG footprint and far below the `Tsc2` or `Cic` state-boundary counts.
