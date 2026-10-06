# Direct DEG-count forecast for Gli3

## Target and endpoint

- Target: `Gli3`.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Held-out status: `Gli3` is absent from the declared 151-class training count table.

## Evidence used

1. **Canonical biology bundle**: `[local file: Gli3.json]`

   The focal non-target expression reach is extremely small: 83 of 23,679 non-target nuclei express `Gli3`, with `pct_cells_expressing = 0.3505215591874657`, `mean_raw_umi = 0.005405633683854893`, `mean_cp10k = 0.003210283177171745`, and `pseudobulk_cpm = 0.3387902320116766`.

   The same bundle judged the functional stock likely to be substantially depleted by the P37-P44 harvest because a P16 edit should block new intact GLI3 supply and the full-length/repressor protein pools are dynamically processed and degraded. That evidence is partial: the turnover facts come from non-neuronal cultured cells, and the clearest mouse neural loss-of-function phenotype comes from embryonic cortical progenitor deletion rather than acute loss in postmitotic thalamic neurons.

2. **Training count table**: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`

   The 151-class training table contains 1,674 perturbations and is strongly zero-inflated:

   | band | count |
   | --- | ---: |
   | `n_degs = 0` | 1205 |
   | `n_degs = 1` | 276 |
   | `n_degs = 2-9` | 87 |
   | `n_degs = 10-99` | 63 |
   | `n_degs >= 100` | 43 |

   Median `n_degs` is 0 and the 90th percentile is 2, so a nonzero call needs target-specific reason rather than a background expectation.

3. **Hedgehog/GLI training comparators from the count table**

   The training-available perturbations closest to the canonical GLI3 operation were quiet in this same cell class:

   | training perturbation | relation to GLI3 biology | `n_degs` |
   | --- | --- | ---: |
   | `Gli1` | GLI-family transcription factor | 0 |
   | `Gli2` | GLI-family transcription factor | 0 |
   | `Ptch1` | Hedgehog receptor/upstream pathway component | 0 |
   | `Ptch2` | Hedgehog receptor/upstream pathway component | 0 |
   | `Smo` | Hedgehog signal transducer | 0 |
   | `Gpr161` | ciliary Hedgehog-pathway regulator | 0 |
   | `Ift88` | ciliary trafficking component that can affect Hedgehog signaling | 0 |
   | `Prkaca` | broader kinase that can regulate GLI processing among other substrates | 1 |
   | `Gsk3b` | broader kinase that can regulate GLI processing among other substrates | 6 |

4. **Training Parquet profile comparison**

   I symmetrically compared `Gli1`, `Gli2`, `Ptch1`, `Ptch2`, `Smo`, `Gpr161`, `Ift88`, `Prkaca`, and `Gsk3b` in the declared Parquet restricted to `group_name = "151 TH Prkcd Grin2c Glut"`. The profile comparison is a derived read of `[local file: training_de_all_cell_groups.parquet]`, not an independent experiment.

   The five direct Hedgehog/GLI nodes inspected from that comparison each had 17,259 profiled measured genes and zero FDR-significant positive or negative genes. Across all direct-node pairs to the selected cohort, there were no significant same-direction intersections and no significant direction conflicts because `Gli1`, `Gli2`, `Ptch1`, `Ptch2`, and `Smo` had no significant features at `pvals_adj < 0.05`.

## Reasoning

Successful `Gli3` editing should exhaust much of the existing GLI3 protein over 21-28 days, but the endpoint is a recovered-nucleus, class-level transcriptional contrast. The exact focal expression reach says very few assayed 151-class control nuclei contain detectable `Gli3` RNA. That makes a widespread downstream signature in this aggregate thalamic class unlikely unless either `Gli3` is active below detection in many nuclei or rare edited cells impose a large enough state change to dominate the matched contrast.

The training data argue against that rescue. Direct GLI-family and Hedgehog-pathway perturbations that are present in the same 151-class count table all produced `n_degs = 0`; broader kinases affecting GLI processing were only 1 and 6. Their Parquet profiles also did not reveal a hidden recurrent significant program beneath the count-table zeros.

I therefore place `Gli3` with the zero direct-pathway comparators rather than with the small nonzero kinase controls or the rare high-yield transcriptional regulators. The main uncertainty is that the bundle supports possible functional depletion of GLI3 protein despite low RNA detection, but the developmental evidence is context-mismatched and does not justify a large postnatal thalamic survivor-state response.

Predicted `n_degs`: **0**
