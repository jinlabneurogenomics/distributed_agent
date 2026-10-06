# Direct DEG-count prediction trace

Target: `Cdh2`

Cell group: `151 TH Prkcd Grin2c Glut`

## Declared biology used

- The held-out manifest contains one target, `Cdh2`.
- The canonical `Cdh2` biology bundle exposed no target outcome and no labeled-neighbor outcomes.
- In the exact focal population, `Cdh2` is readily measured: 23,116 of 23,679 non-target nuclei expressed it, `pct_cells_expressing = 97.62236580936695`, `mean_raw_umi = 7.0440896997339415`, and `mean_log1p_cp10k = 1.5560314762815577`. I therefore did not down-weight the perturbation for lack of focal expression.
- The functional-stock adjudication called N-cadherin an installed membrane/synaptic adhesion complex whose replacement supply stops after a disruptive edit, with the operative stock `likely_substantially_depleted` by the P37-P44 harvest. That argues that a P16 edit could be functional within the 21-28 day window.
- The same bundle also made two response-limiting points material to the forecast: known postnatal phenotypes came from hippocampal/forebrain neurons rather than thalamus, and Cdh4/Cdh6 substitution was seen only in vitro with no matched thalamic compensation test.

## Training measurements used

- `Cdh2` is absent from the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, so no target DEG count was available.
- The 1,674-target focal count table is very sparse:
  - 1,205/1,674 targets have `n_degs = 0`.
  - median = 0, 75th percentile = 1, 90th percentile = 2.
  - 106/1,674 targets have at least 10 DEGs, and 43/1,674 have at least 100.
- I selected training perturbations by biology, emphasizing measured adhesion or synaptic-surface genes and the catenin/turnover genes named in the `Cdh2` bundle. Recomputing exact focal counts from the training Parquet gave:

| target | measured focal rows | pvals_adj < 0.05 |
| --- | ---: | ---: |
| Adam10 | 17259 | 0 |
| Cadm2 | 17259 | 1 |
| Celsr2 | 17259 | 1 |
| Chl1 | 17259 | 1 |
| Ctnna2 | 17259 | 0 |
| Ctnnd2 | 17259 | 1 |
| Ctnnb1 | 17259 | 383 |
| Dscam | 17259 | 0 |
| Itgb1 | 17259 | 0 |
| Ncam1 | 17259 | 1 |
| Pcdh19 | 17259 | 0 |

- A matched profile comparison over the same Parquet cohort likewise separated the large `Ctnnb1` response from the cell-surface comparators: among these 11 nodes, five had no significant features, five had 1-9 significant features, and only `Ctnnb1` had at least 50.

## Synthesis

The high in-assay reach and the functional-stock call make `Cdh2` more credible than an unexpressed or persistent-stock membrane target, so a strict null felt too low. Its closest measured membrane-adhesion comparators in the same thalamic class, however, were almost all 0- or 1-DEG perturbations. I discounted `Ctnnb1 = 383` as an upper-bound outlier because beta-catenin can affect Wnt/transcriptional programs in addition to cadherin junctions, whereas N-cadherin loss is primarily an installed synaptic adhesion perturbation with selective mature-synapse phenotypes.

I therefore forecast a very small but nonzero recovered-nucleus transcriptional footprint:

`predicted_n_degs = 1`
