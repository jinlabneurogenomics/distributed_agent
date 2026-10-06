# Six6 DEG-count forecast

## Target and endpoint

- Target: `Six6`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes in the focal population with BH-adjusted Wilcoxon `p < 0.05`

## Evidence used

### Declared Six6 biology bundle

The canonical biology-only bundle reported exact focal-population reach for `Six6` in matched non-target cells:

- `9 / 23679` non-target nuclei expressed `Six6`
- `pct_cells_expressing = 0.03800836183960471`
- `total_target_umi = 9`
- `pseudobulk_cpm = 0.023821188188321008`
- `mean_raw_umi = 0.0003800836183960471`

The same bundle classified SIX6 as a homeodomain transcription factor but found no target-specific turnover clock, no transferable timing for a P16 thalamic edit, and only developmental neural phenotypes in hypothalamic GnRH neurons / SCN rather than an acute postnatal thalamic requirement. Its stock conclusion was therefore `functional_stock_by_harvest = indeterminate`.

Interpretation: in a cell that actually uses SIX6, a disruptive edit should stop new intact TF production; however, the exact in-assay 151-class RNA reach says that such cells are extremely rare within the assayed recovered population. Any Six6-dependent minority state would be heavily diluted in a class-level Wilcoxon contrast.

### 151-class training count table

The declared count table contained 1,674 training perturbations for the same endpoint and focal population.

- `1205 / 1674` training targets had `n_degs = 0`.
- Median `n_degs = 0`; 75th percentile `= 1`; 90th percentile `= 2`; 95th percentile `= 18`.
- The mean was `14.05`, driven by a long tail of broad responders such as `Uba5`, `Tpr`, and `Sin3a`, not by a typical perturbation.

Biology-matched developmental/homeobox comparators available in the same count table were mostly null:

| comparator | 151 TH Prkcd Grin2c Glut `n_degs` |
| --- | ---: |
| `Six3` | 0 |
| `Rax` | 0 |
| `Alx1` | 0 |
| `Alx3` | 0 |
| `Alx4` | 0 |
| `Arx` | 0 |
| `Atoh1` | 0 |
| `Pax6` | 0 |
| `Vsx1` | 0 |
| `Vsx2` | 0 |
| `Tshz2` | 0 |
| `Tshz3` | 0 |
| `Zfhx2` | 0 |
| `Zbtb20` | 0 |
| `Zic2` | 0 |
| `Zic3` | 0 |
| `Zic4` | 0 |
| `Zic1` | 2 |
| `Prox1` | 50 |
| `Zfp423` | 150 |

The closest declared paralog, `Six3`, had no FDR<0.05 hits in 151. Same-experiment Finding summaries for `Six3`, `Rax`, and the `Zic` genes likewise placed these acute postnatal developmental TF perturbations in sparse or null response regimes; the positive `Prox1` and `Zfp423` 151 responses were useful as boundaries because they showed that the focal class can respond to selected developmental regulators, but their packaged summaries tied the signals to Prox1 or Zfp423 programs rather than to a recurrent SIX/homeobox module.

### Expression-Parquet profile check

I compared the 20 comparator signatures above in `training_de_all_cell_groups.parquet`, restricted to `151 TH Prkcd Grin2c Glut`, with `logfoldchanges` as the signed value and `pvals_adj < 0.05` as significance.

The profile artifact classified:

- 17 of the 20 selected perturbations as `no_significant_features`;
- `Zic1` as the only `1_to_9_significant_features` member;
- `Prox1` and `Zfp423` as the only `at_least_50_significant_features` members.

The selected cohort also lacked a coherent shared 151 profile: across 190 comparator pairs, the median positive top-tail overlap was `0.02`, median negative top-tail overlap was `0.04`, and the significant-program overlap median was `0` in both directions. This makes the nonzero `Prox1`/`Zfp423` cases poor quantitative templates for a Six-family target.

## Prediction

The decisive evidence is the exact `Six6` reach: 9 total UMI and 0.038% expressing non-target cells in an aggregate class of 23,679 nuclei is far below the level expected to yield a class-wide BH-significant Wilcoxon signature after sparse P16 editing. The target biology points to a transcription factor whose strongest known functions are developmental and hypothalamic/retinal, with unresolved adult thalamic stock and no timed protein-clearance evidence; it does not offset the near-absence of focal expression.

Given the 72% zero mass in the matched training count table and the 17/20 null outcomes among the closest developmental/homeobox comparators, I put `Six6` in the null component rather than in the rare responder tail.

`predicted_n_degs = 0`
