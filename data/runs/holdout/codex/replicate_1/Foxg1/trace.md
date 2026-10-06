# Foxg1 DEG-count forecast

## Target and endpoint

- Target: `Foxg1`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with Wilcoxon `pvals_adj < 0.05`

## Evidence used

### Declared Foxg1 biology bundle

Source: `[local file: Foxg1.json]`

- Exact focal reach in non-target `151 TH Prkcd Grin2c Glut` nuclei was low: `2151/23679` nuclei expressed `Foxg1` (`9.083998%`), with mean raw UMI `0.135943`, mean CP10K `0.078442`, and pseudobulk CPM `8.520045`.
- The functional-stock card still judged successful editing biologically realizable by harvest: FOXG1 is a soluble forkhead DNA-binding transcriptional regulator, new protein supply should stop after a disruptive edit, there is no close annotated mouse paralog, and postnatal or postmitotic neuronal Foxg1 loss has consequences within the 21-28 day experimental window in other neural contexts.
- The same bundle made the context mismatch explicit: published mouse evidence reports strong telencephalic expression but not thalamic expression, so the exact in-assay `9.08%` reach is likely the best quantitative guide for this aggregate thalamic population rather than a reason to expect a broad Foxg1-dependent state.

### Declared 151 TH training DEG counts

Source: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`

- The table contains `1674` held-in perturbations and no `Foxg1` row.
- The empirical 151 TH count distribution is very sparse: `1205/1674` targets have `0` DEGs; the median is `0`; the 75th percentile is `1`; the 90th percentile is `2`.
- Large responses exist but are a separate tail: the maximum is `2677`, the 99th percentile is about `436`, and high-count regulators in this cell class include `Yy1` (`720`), `Cic` (`576`), `Ctcf` (`270`), `Rora` (`278`), and `Zfp423` (`150`). Thus transcription-factor identity alone is insufficient; the focal context has to be permissive.

### Declared expression Parquet checks for selected training perturbations

Source: `[local file: training_de_all_cell_groups.parquet]`

I used present developmental or transcriptional regulators as scale comparators, not as outcome labels for `Foxg1`:

| target | 151 TH DEGs at q<0.05 | smallest 151 TH q-value |
|---|---:|---:|
| `Foxa2` | 0 | 1.000000 |
| `Foxp2` | 0 | 1.000000 |
| `Pax6` | 0 | 1.000000 |
| `Satb2` | 0 | 1.000000 |
| `Sox2` | 2 | 0.000003 |
| `Tbr1` | 0 | 0.943932 |
| `Tcf4` | 0 | 1.000000 |

Each of these comparisons had the full 151 TH feature set present in the Parquet (`17259` measured-gene rows). In contrast, the same query recovered broad 151 TH signatures for the high-tail controls above, for example `Cic=576`, `Ctcf=270`, `Rora=278`, and `Yy1=720`, confirming that the zero and near-zero developmental-TF cases were quiet profiles rather than an inability of the Parquet slice to expose large signatures.

## Synthesis

A successful Foxg1 edit should deplete FOXG1 protein on the assay timescale, but this only matters in cells that use FOXG1. In the declared focal thalamic class, exact baseline reach is only about `9%` of non-target nuclei and the biology card independently flags thalamus as a mismatched Foxg1 context. The held-in 151 TH endpoint has a zero median, and the closest available developmental transcription-factor perturbations in the declared training Parquet were predominantly zero with adjusted q-values far from significance.

Those pieces put `Foxg1` with the low-reach, thalamus-mismatched developmental regulators rather than the high-count 151 TH global-regulator tail. I therefore predict no FDR-significant recovered-cell transcriptional response.

Predicted `n_degs`: `0`
