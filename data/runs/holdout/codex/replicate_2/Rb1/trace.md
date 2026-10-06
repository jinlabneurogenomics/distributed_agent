# Rb1 direct forecast trace

## Declared target and reachable biology

- Target: `Rb1`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Requested endpoint: measured genes in this focal population with BH-adjusted Wilcoxon `p < 0.05`

The declared biology-only `Rb1` bundle reports exact focal-population reach in the same assayed population: `Rb1` is detected in 17,384 of 23,679 non-target nuclei, 73.42%, with mean raw UMI 1.47 and pseudobulk CPM 91.85. That makes the target RNA visibly present in most recovered thalamic glutamatergic nuclei, while still leaving dilution from nonexpressing cells and from sparse mosaic editing.

The functional-stock card argues that a disruptive edit should deplete operative pRB within the 21-28 day P16-to-P37/P44 window. The object is a dynamic E2F-associated nuclear corepressor, not an installed structural state; cultured-cell pRB turnover is on an hourly scale, and acute adult forebrain deletion reduced cortical pRB by one week. The same adult postmitotic-neuron model also induced ectopic cell-cycle/DNA-damage markers and neuronal loss by four weeks, so realized `Rb1` loss can be biologically consequential in postmitotic mouse neurons on a matched timescale.

The main downward caveat is endpoint capture. The focal assay is survivor-conditioned snRNA-seq, the direct in vivo timing evidence is adult cortex rather than P16 thalamus, and an Rb-triggered cell-cycle/death response can be partially removed from the recovered-nucleus pool before harvest.

## Same-experiment and training evidence

The July same-experiment corpus has no `Rb1` target report in this release (`target_found=false`), so I treated corpus records only as context for measured training perturbations.

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 non-`Rb1` training perturbations. It is very zero-heavy in the requested endpoint: 1,205 targets have `n_degs=0`, the median is 0, p75 is 1, p90 is 2, p95 is 18, and only 15 targets reach at least 500 DEGs. Thus a handful of DEGs is already above most training perturbations, while hundreds of DEGs belongs to a small nuclear/chromatin stress tail.

Mechanism-near E2F/DP/cell-cycle training counts in the same focal class were small:

- `E2f1`: 0
- `E2f5`: 0
- `Tfdp1`: 2
- `Tfdp2`: 0
- `Myc`: 0
- `Mycn`: 0
- `Trp53`: 0
- `Cdkn2a`: 0

The packaged Findings for `E2f1` and `Tfdp1` are consistent with those exact BH<0.05 counts but use the report layer's FDR<0.10 threshold: represented E2F/DP perturbations did not uncover a coordinated G1/S, replication, mitotic, or apoptotic program in basal postnatal NeuN-positive neurons, and the `Tfdp1` response was only a tiny noncanonical thalamic signature. Those Findings explicitly note that `Rb1`, `Rbl1`, and `Rbl2` were not represented, so the quiet E2F/DP arm is a boundary, not a direct Rb-family donor.

Broader transcription/chromatin perturbations in the same class can be large:

- `Sin3a`: 1433
- `Yy1`: 720
- `Thap11`: 478
- `Setd1a`: 368
- `Brd4`: 311
- `Ctcf`: 270
- `Chd4`: 100
- `Chd8`: 61
- `Arid1a`: 22

I compared a 20-node cohort spanning these active chromatin targets and the quiet E2F/DP/Myc/p53 targets against the declared focal Parquet with `pvals_adj < 0.05` as the significance column. The comparison found all selected profiles available and split them into 11 `>=50` DEG profiles, one 10-49 profile, one 1-9 profile, and seven no-significant-feature profiles. A follow-up cohort diagnostic showed weak positive-tail sharing across the full cohort and only modest negative-tail recurrence, so the active chromatin perturbations are not a single interchangeable donor state for pRB loss.

## Forecast synthesis

I weighted the evidence as follows.

The upward evidence is that `Rb1` is actually expressed in most focal nuclei, the edited pRB stock should turn over before harvest, and postmitotic-neuron `Rb1` loss is not merely developmental: acute adult-neuron deletion produces molecular cell-cycle stress within the screen's time horizon.

The downward evidence is that the measured same-axis E2F/DP and p53/MYC/cell-cycle perturbations in this dataset are nearly silent in the requested cell class, and the high-burden chromatin perturbations perturb broad neuronal-maintenance states rather than cleanly modeling loss of an Rb-E2F gate. Survivor conditioning also makes a lethal Rb response look smaller in recovered nuclei.

Those bearings put `Rb1` above the 0-2 DEG E2F/DP boundary but well below the p95 and far below the broad Sin3a/Yy1/Thap11 tail. I therefore forecast a small nonzero footprint.

Point prediction: `n_degs = 6`.
