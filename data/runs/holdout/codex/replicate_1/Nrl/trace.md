# Direct DEG-count forecast for Nrl

## Target and endpoint

- **Target:** `Nrl`, the single gene in the declared holdout manifest for `151 TH Prkcd Grin2c Glut`.
- **Endpoint:** number of measured genes with Wilcoxon BH-adjusted `p < 0.05` in this focal thalamic glutamatergic class.
- **Point prediction:** `0`.

## Evidence used

1. **Target reach in the exact assayed population was nearly absent.** The declared biology bundle reports `Nrl` as available in the exact focal non-target population, but only **4 of 23,679** matched control nuclei expressed it: `pct_cells_expressing = 0.0168926`, `mean_raw_umi = 0.0001689`, and `pseudobulk_cpm = 0.0106`. The focal expression estimate supersedes broader expression priors for this endpoint.

2. **The perturbation should realize if the edited neuron supplies LCN2, but the matched context is weak.** The bundle resolves this `Nrl` target to the identifier-anchored `Lcn2`/LCN2 locus and describes LCN2 as a secreted lipocalin with short-lived intracellular stock, so a disruptive P16 edit should stop new production long before P37-P44. The main neural loss evidence, however, is adult hippocampal and stress related rather than juvenile thalamus, and healthy thalamic Lcn2 signal was reported as very low. With the transcript observed in only four focal control nuclei, few edited 151-class neurons should have any cell-autonomous LCN2 program to remove.

3. **Training counts in the same cell class are dominated by exact zeros.** In `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, `Nrl` is absent as intended and the 1,674 observed training perturbations have median `n_degs = 0`; **1,205 / 1,674 = 72.0%** are zero, **1,481 / 1,674 = 88.5%** are at most one, and the 75th percentile is one DEG. A prediction of zero is therefore not an outlier default in this context.

4. **Immune/inflammatory training perturbations did not show a recurrent 151 response.** I checked a small hand-selected set of observed targets with inflammatory, cytokine-sensing, Toll-like, or glial-biased biology in the raw Parquet slice for `151 TH Prkcd Grin2c Glut`: `Axl`, `C3`, `Csf1r`, `Cx3cr1`, `Il1r1`, `Il6ra`, `Irf3`, `Nfkb1`, `Rel`, `Stat3`, `Tlr4`, `Tlr7`, and `Tnfrsf1a`. Each had 17,259 measured-gene rows and **zero** BH-significant genes in the count table/Parquet-derived endpoint; their minimum adjusted p-values were all above 0.05. These are not mechanistic replicas of LCN2 loss, but they argue against assigning a nonzero DEG burden simply because the target touches injury or immune signaling.

## Synthesis

The strongest possible reason to predict a nonzero value is that LCN2 is a real secreted, replenished protein and has postnatal neural biology in other regions. For this specific single-nucleus endpoint, that prior is swamped by exact focal reach: only four non-target 151-class nuclei carried any detected `Nrl` transcript, and non-neuronal or extracellular LCN2 sources are not directly removed by a sparse neuronal edit. Against a zero-heavy empirical training distribution and multiple zero-DEG immune/inflammatory perturbations, the most defensible integer forecast is therefore:

`predicted_n_degs = 0`
