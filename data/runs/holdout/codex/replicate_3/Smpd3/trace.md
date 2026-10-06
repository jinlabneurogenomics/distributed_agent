# Smpd3 n_degs prediction for 151 TH Prkcd Grin2c Glut

Prediction: **1 measured gene at BH-adjusted Wilcoxon p < 0.05**.

## Evidence used

- Target and endpoint:
  - Target manifest: `Smpd3`.
  - Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, counted in the declared training table as all measured genes with `pvals_adj < 0.05`.

- Training count table:
  - `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` contains 1,674 training perturbations and excludes `Smpd3`.
  - The endpoint distribution is highly sparse: 1,205/1,674 training targets have 0 DEGs, 1,481/1,674 have at most 1 DEG, and the median is 0.
  - Nearby lipid, sphingolipid, and lysosome/peroxisome targets in the same table were near-null:
    - `Asah1=0`, `Sptlc2=1`, `Psap=1`, `Sphk1=0`, `Scarb2=1`
    - `Ppt1=1`, `Lamp2=0`, `Ctsb=1`, `Atp13a2=1`, `Gaa=1`
    - `Abhd12=1`, `Abcd3=0`, `Pex1=0`, `Pex14=1`

- Smpd3 biology bundle:
  - The declared canonical biology view reports SMPD3/nSMase2 as a Mg2+-dependent neutral sphingomyelinase that hydrolyzes sphingomyelin to ceramide and phosphocholine in dynamic Golgi/plasma-membrane sphingomyelin cycling.
  - The functional-stock adjudication calls Smpd3 stock `likely_substantially_depleted` by the P37-P44 harvest after a P16 edit, but with only partial evidence because direct P16-P44 thalamic neuronal turnover was not measured.
  - Exact non-target reach in the requested population was moderate rather than broad: `9,214 / 23,679` nuclei expressed `Smpd3`, `pct_cells_expressing = 38.9121`, `mean_raw_umi = 0.5906`, and `pseudobulk_cpm = 37.0128`.
  - The postnatal phenotypic prior is real but context-distant: available mouse neural phenotypes are hypothalamic/developmental or progressive over months, not an acute thalamic-neuron phenotype 21-28 days after editing.

- Same-experiment corpus over training perturbations:
  - `Asah1:F001` and `Asah1:F002`: Asah1 was buffered in every recovered neuronal class and did not converge with represented sphingolipid or lysosomal relatives. The Asah1 report explicitly notes that direct ceramide-metabolism relatives including `Smpd3` were absent as visible perturbation targets, so I did not use an observed Smpd3 result.
  - `Sptlc2:F002` and `Sptlc2:F003`: in `151 TH Prkcd Grin2c Glut`, Sptlc2 had significant self-transcript depletion but 0 downstream genes at FDR < 0.10, and expected ER-stress/ISR/autophagy/sphingolipid-compensation markers were absent.
  - `Ppt1:F001`: Ppt1 was pan-neuronally downstream-null despite frequent self-transcript effects.
  - `Lamp2:F002`: Lamp2 did not induce a corrected lysosome, macroautophagy, chaperone-mediated-autophagy, proteasome, UPR/ISR, or redox program in any measured neuronal group.
  - `Abhd12:F001`: Abhd12 lowered its own transcript broadly without a robust downstream neuronal transcriptomic response.

- Matched Parquet profile check:
  - I compared the exact `151 TH Prkcd Grin2c Glut` Parquet profiles for a declared cohort of `Asah1`, `Sptlc2`, `Abhd12`, `Ppt1`, `Lamp2`, `Ctsb`, `Abcd3`, `Pex1`, and `Pex14`.
  - All nine profiles were available. Four had no FDR < 0.05 genes and five had only 1-9.
  - The five most interpretable focal comparators were exactly `Asah1=0`, `Sptlc2=1`, `Abhd12=1`, `Ppt1=1`, and `Lamp2=0` at the same FDR < 0.05 endpoint.
  - Pairwise significant-program intersections among these focal profiles were zero, and the cohort's mean positive top-tail overlap was only 0.044. That argues against a shared multi-gene positive response hidden among the lipid/lysosome neighbors.

## Synthesis

Smpd3 loss should be molecularly realized within the 21-28 day editing window, so I did not treat it as a pure failed-stock/null-operation case. However, its cell reach in the assayed thalamic population is only partial, and the nearest measured lipid and lysosome perturbations are not large transcriptional responders in juvenile NeuN+ nuclei. The same-experiment reports are especially important for scale: `Sptlc2`, `Ppt1`, and `Abhd12` can lose their own target transcript yet remain downstream-null, showing that a count of 1 in this table can simply be a self row rather than a broader pathway state.

I therefore forecast no robust downstream module and place the count at the self-transcript boundary. Given detectable but moderate `Smpd3` expression in 38.9% of matched thalamic controls, the integer point is 1 rather than 0: a single self-target or isolated measured-gene call is plausible, while a multi-DEG response is not supported by the training comparators.

The Parquet rows, the training count table, and the packaged Findings/Evidence are same-experiment representations; the corpus was used only to interpret the visible training perturbations, not as independent replication.
