# Dcx n_degs forecast for 151 TH Prkcd Grin2c Glut

## Target and declared endpoint

The one-row manifest target is `Dcx`. I interpreted the requested endpoint as the 151-class count of measured genes with Wilcoxon `pvals_adj < 0.05` in the declared training table and `training_de_all_cell_groups.parquet`.

All endpoint-scale numerical comparisons below use training perturbations only. `Dcx` was absent from the 1,674-row 151-class count table and was not queried as a perturbation in the training expression parquet.

## Biology of the held-out target

The declared `Dcx.json` bundle supports a weak mature-thalamus effect prior rather than a large response prior.

- In the exact focal population, `Dcx` is detectable but low: 11,066 of 23,679 non-target 151-class nuclei expressed it, `mean_raw_umi = 0.841`, `mean_cp10k = 0.544`, and `pseudobulk_cpm = 52.72`.
- The functional-stock card judged DCX stock as `likely_substantially_depleted` within the P16 to P37-P44 window if an edited cell needs DCX, because DCX is a soluble, renewable microtubule-associated protein and a neuronal DCX-Halo pulse-chase measured hour-scale turnover.
- The same source card makes the consequence uncertain in this assay context: Dcx is primarily an immature-neuron and developmental migration/lamination gene by late postnatal or adult stages; adult dentate-gyrus acute loss did not change selected newborn-neuron survival, maturation, or fate; and Dcx/Dclk redundancy was shown in developing hippocampus rather than P16-P44 thalamus.

My read is therefore: target engagement should remove DCX in the minority of cells with material DCX, but the aggregated recovered 151 profile is likely to look like a weak postnatal structural or migration-gene perturbation, not like the high-burden essential-gene tail.

## Training count scale

The 151-class count table is highly zero-inflated:

- `n = 1674` training targets
- 1205 / 1674 had `n_degs = 0`
- 1481 / 1674 had `n_degs <= 1`
- 1512 / 1674 had `n_degs <= 2`
- median `n_degs = 0`
- 95th percentile `n_degs = 18`
- the large tail was off-axis for Dcx, led by broad spliceosome/proteasome/ubiquitin and transcriptional machinery perturbations such as `Uba5 = 2677`, `Tpr = 1768`, `Sin3a = 1433`, and `Psmb4 = 742`.

## Training analogs that drove the forecast

I used the typed gene-analog nomination step with `Dcx` and the explicit training universe. No Dcx paralog or exact-complex mate was training-available. The useful nominees fell into two interpretable sets.

**Reelin / LIS1 and developmental migration comparators**

The strongest narrow nominees were `Lrp8` and `Reln`; the explicit corpus topology also recovered a reciprocal Reelin-core component with `Dab1`, `Fyn`, and `Vldlr`.

Their exact 151-class counts were:

| target | n_degs |
| --- | ---: |
| Lrp8 | 0 |
| Reln | 0 |
| Dab1 | 0 |
| Fyn | 0 |
| Vldlr | 0 |

The same-experiment Findings were consistent with those counts: `Dab1:F001` reported no downstream FDR<0.10 response in any of 20 recovered groups; `Vldlr:F001` reported no FDR-supported downstream transcriptome in any recovered juvenile neuronal class; `Reln:F001` reported only one downstream DEG across 22 recovered classes; and `Lrp8:F001` placed its only robust downstream response outside the 151 class.

These are not DCX molecular phenocopies, but they are close in the same developmental migration and lamination biology that dominates the Dcx prior. Their flat juvenile postmitotic RNA surfaces pulled the forecast downward.

**Microtubule and microtubule-associated comparators**

The MAP/tubulin side was similarly small in the 151 class:

| target | n_degs |
| --- | ---: |
| Map1b | 1 |
| Mapt | 1 |
| Kif5a | 1 |
| Stmn2 | 1 |
| Tubb5 | 1 |
| Tuba1a | 7 |

The corpus again argued against a hidden broad cytoskeletal state: `Map1b:F001` described Map1b as transcript-self-only in 151 and 155, `Mapt:F001` reported no FDR-resolved downstream response in any of 22 groups, and `Tuba1a:F001`/`Tuba1a:F003` described a restricted tubulin-compensation program rather than a broad stress or synaptic-collapse program.

I treated `Tuba1a = 7` as an upper local reference rather than a point donor because TUBA1A is an abundant core alpha-tubulin, while DCX is a lowly expressed accessory MAP whose known loss biology is developmental and immature-neuron-biased.

## Numeric synthesis

The nearest specific training evidence was centered at zero:

- all five Reelin-core/LIS1 comparators above were `0` in 151;
- four of five non-Tuba1a MAP/microtubule comparators were `1`;
- among the 16 training-available narrow nominees from the typed nomination artifact, 14 were `0` and the maximum was `1`;
- broad active outliers such as `Ctnnb1`, `Grin1`, `Tsc2`, and `Dctn1` were high because of Wnt, NMDA-receptor, mTOR, or dynactin/stress programs and were not operation-scale analogs for low postnatal DCX loss.

I assigned the integer point to the mode of the specific developmental/Reelin cohort rather than to the broader count-table mean. A self-transcript-only hit would make `Dcx` a one-DEG perturbation, but the exact focal-population Dcx abundance is low and the closest postmitotic developmental analogs did not show robust 151-class downstream signal. The final forecast is:

`Dcx = 0`
