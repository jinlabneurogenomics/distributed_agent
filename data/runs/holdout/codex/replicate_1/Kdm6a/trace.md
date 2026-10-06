# Kdm6a direct forecast

## Declared target

- Target: `Kdm6a`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Declared holdout manifest: one row, `Kdm6a`

## Evidence used

### Target biology bundle

The endpoint-excluded `Kdm6a` biology bundle reports exact focal expression in matched non-target nuclei for `151 TH Prkcd Grin2c Glut`:

- `feature_available`: true
- `n_non_target_cells`: 23,679
- `n_cells_expressing`: 14,887
- `pct_cells_expressing`: 62.87
- `mean_raw_umi`: 1.1417
- `mean_cp10k`: 0.7263
- `pseudobulk_cpm`: 71.56

So the target is visibly expressed in the focal thalamic population; lack of expression is not the main reason to predict a null.

The same bundle adjudicates KDM6A as a nuclear H3K27me2/H3K27me3 demethylase and MLL3/4-associated chromatin-regulatory component. Its functional stock is predicted to be `likely_substantially_depleted` by the P37-P44 harvest after a P16 disruptive edit, because acute deletion in P0-derived hippocampal neurons produced KDM6A-dependent dendritic and spine phenotypes by DIV7-DIV19. The bundle also notes important scale-limiting uncertainty: the postnatal effect is from hippocampal culture rather than thalamus in vivo, neuronal KDM6A protein half-life is unresolved, pre-existing chromatin states may persist heterogeneously, and UTY may preserve some noncatalytic functions.

### Focal training counts

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` contains 1,674 non-held-out biological targets and no `Kdm6a` row. Its distribution is very sparse:

- median: 0
- 75th percentile: 1
- 90th percentile: 2
- 95th percentile: 18
- 469/1,674 targets have any DEG at `p_adj < 0.05`
- 103/1,674 exceed 10 DEGs

That puts any chromatin prior on top of a strong zero-inflated empirical base rate.

### Measured related perturbations

I inspected the focal parquet rows for chromatin and signaling comparators chosen from KDM6A's direct biochemical neighborhood and nearby chromatin-regulator biology. Exact focal counts at `p_adj < 0.05` were:

| training target | focal `n_degs` | matched perturbed nuclei | bearing |
| --- | ---: | ---: | --- |
| `Kdm6b` | 0 | 203 | closest active H3K27 demethylase; argues for buffering of the KDM6 catalytic axis in basal postnatal neurons |
| `Kmt2c` | 0 | 55 | enhancer MLL3 relative in the KDM6A-associated MLL3/4 axis; low power but no focal response |
| `Kmt2a` | 24 | 161 | H3K4 writer with a real but sparse focal response |
| `Crebbp` | 8 | 61 | chromatin coactivator with a small thalamic-only response |
| `Ep300` | 0 | 155 | KAT3 coactivator paralog buffered across assayed groups |
| `Gsk3b` | 6 | 108 | non-chromatin signaling comparator with prior neuronal relevance but only a tiny 151 response |
| `Setd1a` | 368 | 154 | broad H3K4 writer response; proves detectability of strong chromatin effects but is a less direct scale analogue |
| `Sin3a` | 1433 | 176 | broad repressor-complex scaffold response; a high-end chromatin boundary rather than a KDM6A analogue |
| `Phf12` | 403 | 234 | strong PHF/SIN3-associated boundary, mechanistically more RNA/proteostasis-like than KDM6A |

Packaged same-experiment Findings for the training comparators matched these measurements: `Kdm6b` was FDR-null in every recovered neuronal group and specifically flat in 151 despite other chromatin regulators responding; `Kmt2c` was almost globally buffered, with a single Prnp hit outside 151; `Kmt2a` produced a sparse glutamatergic-biased response with most hits in 151 and did not phenocopy `Kmt2c` or broad `Setd1a`; `Crebbp` had a small 151-restricted response; `Ep300` was buffered across 21 measured neuronal groups. Those reports are semantic summaries of the same experiment rather than independent replication.

## Synthesis

`Kdm6a` should not be forced to zero: it is expressed in the focal cells, it has catalytic and noncatalytic chromatin functions, and postnatal neuronal loss can manifest within the assay window. But the direct observed analogues point lower than a generic "chromatin regulator" prior. The closest measured KDM6-family perturbation, `Kdm6b`, has 0 DEGs in the same focal population despite good matched perturbed-cell recovery, and the MLL3-family comparator `Kmt2c` is also 0 in 151. Sparse positives from `Kmt2a` and `Crebbp` support a small nonzero possibility rather than the hundreds-to-thousands DEG behavior of `Setd1a`, `Sin3a`, or `Phf12`.

Taking the direct zero analogues as the strongest downward evidence and the postnatal KDM6A phenotype plus focal expression as upward evidence, I place the point just above the training distribution's 90th percentile but below the small `Crebbp`/`Gsk3b` responses.

Predicted `n_degs`: **2**
