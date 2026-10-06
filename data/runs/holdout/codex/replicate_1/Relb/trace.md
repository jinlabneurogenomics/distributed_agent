# Relb n_degs forecast for 151 TH Prkcd Grin2c Glut

## Endpoint and declared target

- Target in the one-row holdout manifest: `Relb`.
- Requested endpoint: `n_degs`, the count of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Direct training table: 1,674 measured training perturbations for the focal thalamic class; `Relb` is absent from that table.

## Target biology

- Exact focal-population reach from the declared Relb biology bundle is very low: 460 of 23,679 non-target nuclei expressed `Relb` in `151 TH Prkcd Grin2c Glut` (`pct_cells_expressing = 1.94%`, `mean_raw_umi = 0.0209`, `mean_cp10k = 0.0130`, `pseudobulk_cpm = 1.31`).
- RelB is a DNA-binding NF-kappaB transcriptional subunit that works in partner-containing complexes, especially RelB-p52. The bundle adjudicates the P16-to-P37/P44 loss-of-function window as `partially_depleted_or_leading_edge`: new RelB synthesis should stop, but pre-edit partner-bound complexes may persist because p100/p52 and p105/p50 stabilize RelB.
- The external postnatal-neural phenotype evidence is positive but mismatched: conditional Relb loss had a CNS phenotype under inflammatory/EAE conditions and in glial/CNS-lineage settings, not a demonstrated healthy thalamic glutamatergic-neuron requirement. Together with the exact sparse target expression, this made a large recovered-cell transcriptional footprint unlikely.

## Training perturbations used

- The focal count distribution is dominated by zero or one DEG: 1,205/1,674 perturbations have `n_degs = 0`, 1,481/1,674 have `n_degs <= 1`, and only 80/1,674 reach `n_degs >= 20`. The mean is 14.1 only because a small tail of generic high-burden perturbations reaches hundreds to thousands of DEGs.
- I nominated training-available `Relb` analogs from typed mouse annotations rather than a symbol-prefix rule. The strongest exact/paralog or projected-complex nominees were:
  - `Nfkb1`: `n_degs = 0`
  - `Rel`: `n_degs = 0`
  - `Chuk`: `n_degs = 0`
  - `Ddx3x`: `n_degs = 8`
  - `Yy1`: `n_degs = 720`
  - `Gtf2i`: `n_degs = 10`
  - `Kpna3`: `n_degs = 0`
- The NF-kappaB receptor/signaling neighborhood gave the same directional signal in the declared focal counts: `Map3k7 = 0`, `Traf3 = 0`, `Tlr4 = 0`, `Irf9 = 0`, `Stat1 = 1`, and `Stat3 = 0`.
- `Yy1`, `Psmc1`, and `Psmb4` were useful as high-DEG contrasts but were not weighted like the NF-kappaB-side genes. Their large burdens reflect chromatin or proteasome/proteostasis branches in this assay rather than a close RelB-subunit perturbation.

## Parquet/profile checks

- The declared Parquet confirmed the focal counts for the 20 inspected Relb-neighborhood training perturbations and had no missing profiles in `151 TH Prkcd Grin2c Glut`.
- Among those 20 candidates, the profile activity bins were 12 with no significant features, 4 with 1-9, 1 with 10-49, and 3 with at least 50.
- A six-node core NF-kappaB cohort, `Nfkb1`, `Rel`, `Chuk`, `Map3k7`, `Traf3`, and `Tlr4`, was also connected by report-derived explicit references. All six had `n_degs = 0`.
- Their pairwise signed-tail overlap was weak, and the core cohort had no shared significant-program overlap. I therefore treated their agreement as six nearby zero endpoint observations, not as a transferable nonzero transcriptional program.

## Forecast

`Relb` has a biologically plausible but partial perturbation, extremely narrow exact focal expression, and its closest measured NF-kappaB/module comparators are almost uniformly silent in this same thalamic class. I therefore predict that the Relb perturbation will fall on the modal zero-count outcome rather than in the rare high-burden tail.

Predicted `n_degs`: **0**
