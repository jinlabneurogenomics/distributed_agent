# Direct `n_degs` forecast for `Uqcrc1`

## Target and endpoint

- **Target:** `Uqcrc1`
- **Cell class:** `151 TH Prkcd Grin2c Glut`
- **Endpoint:** count of measured genes with Wilcoxon BH-adjusted `p < 0.05`
- **Point forecast:** `1`

## Evidence used

1. **Declared prediction-safe biology bundle**

   Source: `[local file: Uqcrc1.json]`, canonical biology view, SHA-256 `e737617ad4a1da05ed690979dfec693fb1d6dfac0f76bb1d3b5aaa456486e864`.

   `Uqcrc1` is observable in the focal non-target cells: `23,218 / 23,679` nuclei express it, `pct_cells_expressing = 98.053`, `mean_raw_umi = 6.289`, `mean_cp10k = 3.843`, and `mean_log1p_cp10k = 1.492` in `151 TH Prkcd Grin2c Glut`.

   The same bundle classifies UQCRC1 as an already-installed complex-III core subunit. A P16 disruptive edit should stop new UQCRC1 synthesis but leave pre-edit assembled complex III and supercomplex-associated material initially functional. The adjudicated functional-stock conclusion was `partially_depleted_or_leading_edge` by the P37-P44 harvest: some decline over 21-28 days is plausible, but considerable residual function is expected because a target-specific neuronal UQCRC1 clearance clock is not known and adult brain ETC proteins can be long-lived.

2. **Focal training count table**

   Source: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.

   The table contains `1,674` non-held-out perturbations and excludes `Uqcrc1`. Its distribution is highly zero-inflated in this cell class: `1,205 / 1,674` perturbations have `0` DEGs, the median is `0`, the 75th percentile is `1`, the 90th percentile is `2`, and the mean is `14.05` only because of a small extreme right tail headed by perturbations such as `Uba5 = 2677`, `Tpr = 1768`, and `Sin3a = 1433`.

3. **Observed respiratory-chain comparators in the focal Parquet slice**

   Source: `[local file: training_de_all_cell_groups.parquet]`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"`.

   The closest available complex-III perturbations were essentially transcriptionally silent in the requested cell class:

   | target | focal `n_degs` | significant focal rows |
   | --- | ---: | --- |
   | `Cyc1` | 1 | `Cyc1` self-transcript only |
   | `Uqcrb` | 0 | none |
   | `Uqcrc2` | 1 | `Uqcrc2` self-transcript only |
   | `Uqcrfs1` | 0 | none |
   | `Uqcrh` | 0 | none |
   | `Uqcrq` | 1 | one non-self singleton, `Gpr180` |

   A broader manually selected respiratory-chain / mitochondrial-import panel in the same focal Parquet slice, comprising the five `Uqcr*` genes above plus `Cyc1`, `Cox11`, five expressed COX subunits, 23 complex-I subunits or assembly factors, `Sdha`, `Timmdc1`, and `Tomm40`, had the same scale: every one of the 38 profiled targets had either `0` or `1` significant focal genes.

   The `n_pert_matched` values for the six complex-III comparators in this class were not vanishingly small: `Uqcrb = 127`, `Uqcrc2 = 142`, `Uqcrfs1 = 233`, `Uqcrh = 152`, `Uqcrq = 345`, and `Cyc1 = 221`, each against `23,679` matched control nuclei.

4. **Same-experiment corpus interpretation of observed complex-III comparators**

   Source: selected July corpus release `perturbai-july-260713-sourceguard-1773-v1`, `query_ledger(findings/null_findings)` for the observed training genes only.

   The packaged Uqcrc2 report records a high-confidence negative finding (`Uqcrc2:F001`) that `Uqcrc2` produced no robust downstream single-gene DE in measured neuronal groups, and a buffered-response finding (`Uqcrc2:F003`) that `Uqcrb`, `Uqcrfs1`, `Uqcrh`, `Uqcrq`, `Cyc1`, and `Ttc19` similarly had only `0-1` downstream genes in Uqcrc2-matched groups. These ledgers are the same experiment as the Parquet, so I used them as interpretation of the measured complex-III null pattern, not as independent replication.

## Reasoning

`Uqcrc1` has excellent transcript reach in the focal population, so a complete non-observability prior would be too low. The protein-level perturbation, however, targets an already assembled complex-III component. The biology bundle specifically argues for a leading-edge depletion state at 21-28 days rather than an acute collapse of mitochondrial activity, and the closest measured structural complex-III subunits show almost no downstream nuclear response in the same assay.

The strongest local quantitative prior is therefore the complex-III neighborhood, not the heavy-tailed all-target mean. In that neighborhood, `Uqcrc2` and `Cyc1` each score exactly one DEG through self-transcript depletion alone, while three `Uqcr*` subunits are strict zeros. Because `Uqcrc1` is highly expressed in almost every focal non-target nucleus, I shifted the point estimate from `0` toward a single detectable transcript-level event, but I did not project a multi-gene stress program.

Final synthesis: **one** BH-significant measured gene is the most likely integer-scale outcome for `Uqcrc1` in `151 TH Prkcd Grin2c Glut`.
