# Ndufs3 direct `n_degs` forecast

## Endpoint

`n_degs` is the count of measured genes in `151 TH Prkcd Grin2c Glut` with
BH-adjusted Wilcoxon `pvals_adj < 0.05`.

Declared endpoint sources:

- Training count table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Training expression table:
  `[local file: training_de_all_cell_groups.parquet]`
- Biology-only target bundle:
  `[local file: Ndufs3.json]`

The training count table contains 1,674 perturbations and no `Ndufs3` row.

## Target biology

The holdout target is `Ndufs3`. The canonical biology bundle puts it in the
mammalian respiratory complex-I Q module with `Ndufs2`, `Ndufs7`, and `Ndufs8`.
The exact non-target expression measurement for the focal thalamic class shows
that `Ndufs3` is measurable and broadly expressed:

- `feature_available = true`
- `pct_cells_expressing = 92.9093`
- `mean_raw_umi = 3.3812`
- `mean_cp10k = 2.1344`

That supports the possibility of observing the `Ndufs3` transcript itself if it
is depleted, but it does not by itself establish functional loss or downstream
transcriptional response.

The functional-stock card argues against a large short-window complex-I state:
P16 editing should stop new NDUFS3 supply, but installed complex I is the
operative entity. The closest postnatal-neuron clock retained near-control
NDUFS3 at one month and began progressive decline around two months, so the
P37-P44 harvest is most consistent with partial or leading-edge stock loss.

## Training comparators

The global target-class training endpoint is zero-heavy: 1,205/1,674
perturbations have 0 DEGs, the median is 0, the 75th percentile is 1, the 90th
percentile is 2, and the heavy tail is driven by unrelated targets such as
`Uba5`, `Tpr`, `Sin3a`, and RNA-processing/proteostasis regulators.

The closest local respiratory-complex rows do not show a broad shared
mitochondrial stress footprint in `151 TH Prkcd Grin2c Glut`:

| Comparator | `n_degs` |
| --- | ---: |
| `Ndufs2` | 1 |
| `Ndufs7` | 0 |
| `Ndufs8` | 1 |
| `Ndufs4` | 0 |
| `Ndufv1` | 0 |
| `Ndufv2` | 1 |

Across every `Nduf*` training perturbation in the table, all 23 matched rows
have either 0 or 1 DEG; 12 are 0 and 11 are 1. The expression parquet shows that
10 of the 11 significant `Nduf*` rows are the knocked-down transcript itself.
For the same core Q-module neighbors, the only significant rows were:

| Perturbation | Significant measured gene | log fold-change | `pvals_adj` |
| --- | --- | ---: | ---: |
| `Ndufs2` | `Ndufs2` | -0.7281 | 8.261e-12 |
| `Ndufs8` | `Ndufs8` | -0.6497 | 3.058e-08 |

`Ndufs7` had no FDR-significant row despite a negative self-transcript effect
(`logfoldchanges = -0.3435`, `pvals_adj = 1.0`). `Ndufs4` likewise had no
FDR-significant row (`logfoldchanges = -0.6227`, `pvals_adj = 0.5024` for its
self transcript).

## Synthesis

I used `Ndufs2`, `Ndufs7`, and `Ndufs8` as the highest-weight measured
comparators because they share the NDUFS3-containing Q module. They bound the
expected response to 0-1 genes in the focal class, and the wider `Nduf*` cohort
supports the same low-count interpretation with no member exceeding one DEG.

The target bundle makes a nonzero self-transcript hit plausible because
`Ndufs3` is well observed in this thalamic class, while the delayed stock-loss
biology and absence of a downstream complex-I program in the training
comparators argue against moving into the high-response tail. The point
forecast is therefore a one-gene footprint, most likely the target transcript
alone rather than a multi-gene response.

Predicted `n_degs`: **1**
