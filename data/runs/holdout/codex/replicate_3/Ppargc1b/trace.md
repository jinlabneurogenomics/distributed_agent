# Ppargc1b n_degs forecast

## Target and endpoint

- **Target:** `Ppargc1b`
- **Cell group:** `151 TH Prkcd Grin2c Glut`
- **Endpoint:** number of measured genes with `pvals_adj < 0.05` in the held-out `Ppargc1b` perturbation.

## Target biology used

The declared biology bundle identifies PGC-1beta as a recruited nuclear transcriptional coactivator for ERR/NRF-linked mitochondrial oxidative programs, not as a stable product-installing enzyme. Its functional-stock card adjudicates the 21-28 day post-edit window as likely long enough for substantial loss of newly supplied coactivator: pre-edit protein may remain until normal turnover, but the operative stock is a renewing ubiquitin/proteasome-regulated pool rather than a durable installed structure.

The strongest in-assay target-presence fact is the exact focal expression measurement in non-target cells: `Ppargc1b` is observed in 13,862 of 23,679 nuclei in this class, or **58.54%**, with mean raw UMI **1.02** and mean log1p CP10K **0.407**. I therefore did not set the count to zero because the target is absent. The limiting biology is instead endpoint transfer: the best direct loss evidence is developmental/germline mouse brain data in other regions, the acute P16-to-P37 thalamic clock is not directly measured, and `Ppargc1a` could partly buffer PGC-1beta-dependent mitochondrial regulation in a context-dependent way.

## Training count context

The declared count table contains **1,674** training perturbations for `151 TH Prkcd Grin2c Glut`; `Ppargc1b` is absent. This endpoint is sparse in the training surface:

- 1,205 / 1,674 training targets have `n_degs = 0`
- median = 0
- 75th percentile = 1
- 90th percentile = 2
- 95th percentile = 18
- mean = 14.05, inflated by a long upper tail

So the local baseline for a biologically plausible but not clearly pleiotropic perturbation is zero to one significant genes, not the arithmetic mean.

## Comparator evidence from the declared table and Parquet

I nominated available comparators from typed mouse annotations and retained the candidates that actually probe the PGC-1beta mitochondrial-coactivator axis in the training universe. Their observed `151 TH Prkcd Grin2c Glut` counts were:

| comparator | relation used | n_degs |
| --- | --- | ---: |
| `Ppargc1a` | closest available PGC-1 paralog; shared mitochondrial gene-expression module | 0 |
| `Ncoa1` | broad nuclear-receptor coactivator | 0 |
| `Pparg` | PGC-1/PPAR-axis receptor, broader and not thalamus-specific | 0 |
| `Ppara` | PPAR-axis receptor, broader and not thalamus-specific | 0 |
| `Ppard` | PPAR-axis receptor, broader and not thalamus-specific | 0 |
| `Esrrg` | ERR-family comparator without the specific responsive ERR-alpha profile | 0 |
| `Ppp3ca` | upstream calcineurin/CREB-axis comparator | 4 |
| `Creb1` | upstream broad transcriptional regulator | 10 |
| `Esrra` | direct ERR regulator of the mitochondrial program | 57 |
| `Nrf1` | direct mitochondrial DNA-binding regulator | 138 |

The high rows therefore came from direct DNA-binding transcription factors, not from PGC-1-like coactivators or PPAR/ERR-family receptor perturbations in general. In the profile comparison over the declared expression Parquet, the 12-node PGC/PPAR/ERR/NRF cohort contained 8 no-DEG profiles, one 1-9 profile, one 10-49 profile, and only two profiles with at least 50 significant genes. The significant programs of the larger `Nrf1` and `Esrra` rows were also not a tight reusable module: across the full 12-node cohort, positive significant-program overlap was 0, and the negative significant-program overlap was weak and present only for pairs where both nodes had significant genes. This made the direct `Nrf1`/`Esrra` transcription-factor counts useful as an upper boundary but not as a scale-matched center for loss of one recruited coactivator.

Corpus topology among `Ppargc1a`, `Nrf1`, `Esrra`, `Ppara`, `Ppard`, and `Pparg` was dense, with 12 of 15 possible explicit report-reference pairs represented, confirming that these are a coherent same-experiment neighborhood. Because the observed profile rows inside that neighborhood split into mostly zero coactivator/receptor counts versus larger direct-regulator counts, I treated the dense topology as relevance support, not as a reason to average the response magnitudes.

## Forecast

`Ppargc1b` has enough focal expression and a dynamic protein stock, so a small mitochondrial-state response is plausible. The matched quantitative comparators nevertheless put the nearest PGC-1/coactivator/receptor neighborhood at the zero-count mode, and the nonzero direct-regulator rows are broader lesions than removing PGC-1beta. I therefore placed the point estimate at the training distribution's modal local outcome:

**predicted_n_degs = 0**
