# Opn1mw DEG-count forecast

## Requested endpoint

- Target: `Opn1mw`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Forecast: `0`

## Evidence used

### Declared target and biology bundle

- The one-row holdout manifest names `Opn1mw`.
- The prediction-safe `Opn1mw` biology bundle is outcome-blind and reports exact in-assay focal expression in `151 TH Prkcd Grin2c Glut`: `mean_raw_umi = 0.0427382913`, `mean_cp10k = 0.0270206681`, `pseudobulk_cpm = 2.67856027`, and `885 / 23679 = 3.7375%` of matched non-target nuclei with any `Opn1mw` UMI.
- The functional stock card supports `Opn1mw` as an installed, continuously renewed retinal cone outer-segment photopigment whose stock would likely be depleted across 21-28 days in an edited cone.
- That same source card explicitly places the known operation in retinal cones and says the thalamic relevance is unsupported: the cone photopigment evidence does not demonstrate an `Opn1mw` function in thalamic NeuN-positive nuclei.

### Packaged same-experiment corpus

- `distributed_agents_corpus.target_context(target="Opn1mw")` in release `perturbai-july-260713-sourceguard-1773-v1` returned no Findings, no Claims, and no explicit same-experiment references for `Opn1mw`.
- I treated this only as absence of a released packaged interpretation, not as an independent negative measurement.

### Declared training count table

- The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 training targets and excludes `Opn1mw`.
- Its matched-cell count distribution is extremely zero-heavy: median `n_degs = 0`, 1,205 / 1,674 targets have `n_degs = 0`, 1,481 / 1,674 have `n_degs <= 1`, and the 75th percentile is `1`.
- Retina/phototransduction-biased visible comparators were all null in this same endpoint:
  - `Opn1sw`: `0`
  - `Rho`: `0`
  - `Crx`: `0`
  - `Otx2`: `0`

### Declared expression Parquet checks

I filtered `training_de_all_cell_groups.parquet` to `group_name == "151 TH Prkcd Grin2c Glut"` for `Opn1sw`, `Rho`, `Crx`, and `Otx2`.

- Each comparator had 17,259 measured-gene rows in this focal class.
- None had any measured gene with `pvals_adj < 0.05`.
- The strongest adjusted p-values were still nonsignificant:
  - `Opn1sw`: minimum adjusted p-value `1.0`
  - `Crx`: minimum adjusted p-value `1.0`
  - `Otx2`: minimum adjusted p-value `0.8849070507`
  - `Rho`: minimum adjusted p-value `0.6607190772`

## Reasoning

`Opn1mw` has strong biology in the retina but almost no biology that should couple an acute sparse P16 edit to a survivor-conditioned transcriptional response in thalamic glutamatergic neurons. Its known effector is an abundant cone outer-segment photopigment; the assayed focal population is not a cone population, and the exact focal expression measurement is a trace-level signal spread across only 3.7% of non-target nuclei. That leaves little reason to expect many cells in `151 TH Prkcd Grin2c Glut` to carry functional Opn1mw protein whose removal could perturb a regulatory or homeostatic program.

The quantitative training surface reinforces the downward call. The focal count table is dominated by zeros even in this high-yield class, and the closest visible retinal sensory comparators, especially the cone paralog `Opn1sw` and the rod opsin `Rho`, were exactly zero-DEG perturbations in the same count table and had no near-threshold FDR signal in the Parquet rows. Those are not labeled neighbors for `Opn1mw`; they are simply endpoint-matched training examples showing that photoreceptor-restricted visual genes can be transcriptionally inert in this thalamic class.

Given trace focal reach, context-mismatched retinal biology, no packaged same-experiment `Opn1mw` signal, and null matched phototransduction comparators, the best integer point estimate is:

```text
n_degs = 0
```
