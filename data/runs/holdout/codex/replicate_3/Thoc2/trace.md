# Direct forecast for `151 TH Prkcd Grin2c Glut`

## Target and endpoint

- Target: `Thoc2`
- Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `p < 0.05`.
- The training count table contained 1,674 visible focal-class targets and did not contain `Thoc2`. The focal-class target count distribution was highly sparse: median 0, 75th percentile 1, 95th percentile 18, mean 14.05, and 43 of 1,674 training targets had at least 100 DEGs.

## Target biology used

- The prediction-safe `Thoc2` biology bundle identifies THOC2 as a core THO/TREX mRNA-processing and export subunit. The relevant functional stock is a dynamic nuclear complex component, not a stable pre-installed neuronal structure.
- The same bundle reports measured THOC2 protein half-lives of 43.023 h and 45.015 h in nondividing primary mouse cortical neurons. Over a P16-to-P37/P44 Perturb-seq interval, this is roughly 11-16 half-lives, so the pre-edit protein pool should be mostly cleared by harvest in successfully edited cells.
- `Thoc2` is expressed in the exact non-target focal population: 20,186 of 23,679 non-target nuclei expressed it, or 85.25%, with mean raw UMI 2.225 and pseudobulk CPM 139.43. This supports target reach in the thalamic glutamatergic context but was not used as an editing-efficiency proxy.
- A Thoc2-like locus exists, but the bundle had no evidence that it buffers THOC2 loss in thalamic neurons.

## Training perturbations that set the scale

`Thoc1` was the closest measured donor because it is the represented core THO/TREX-complex perturbation.

| training target | focal n_degs | focal DE direction | focal perturbed nuclei | role in forecast |
| --- | ---: | --- | ---: | --- |
| `Thoc1` | 303 | 233 up / 70 down | 121 | primary direct THO-complex scale |
| `Ddx39b` | 0 | 0 up / 0 down | 48 | related TREX/export counterexample |
| `Snrnp70` | 213 | 127 up / 86 down | 135 | RNA-biogenesis lower-scale neighbor |
| `Prpf6` | 454 | 243 up / 211 down | 72 | spliceosome/export-adjacent upper context |
| `Cdc40` | 624 | 446 up / 178 down | 159 | spliceosome/export-adjacent upper context |
| `Hnrnpu` | 733 | 483 up / 250 down | 163 | RNA-processing upper context |
| `U2af2` | 828 | 446 up / 382 down | 222 | spliceosome/export-adjacent upper context |
| `Rnpc3` | 868 | 390 up / 478 down | 149 | spliceosome/export-adjacent upper context |
| `Tpr` | 1768 | 1315 up / 453 down | 114 | nuclear-pore upper context |

The same-experiment corpus reports that acute `Thoc1` loss had a THO/TREX-compatible RNA-biogenesis program and that `Ddx39b`, `Tpr`, `U2af2`, `Snrnp70`, `Cdc40`, and `Prpf6` were same-direction comparators of that program in other responsive groups. In the focal 151 class, a training-parquet profile scan gave `Thoc1` nearest whole-score neighbors of `Tpr`, `Snrnp70`, `Rnpc3`, `Prpf6`, `Cdc40`, `U2af2`, `Psmb4`, `Psmc1`, and then `Ddx39b`, confirming that the THOC1 response sits inside a broad RNA-biogenesis/proteostasis neighborhood rather than among random small signatures.

## Forecast

The primary scale is the `Thoc1` focal count of 303 DEGs. `Thoc2` is another core THO-complex subunit, is expressed in most focal nuclei, and should have time to lose functional protein by harvest; these facts argue against the baseline sparse prior or the focal `Ddx39b` null being the best point estimate. I still kept the forecast below the broad spliceosome, nuclear-pore, and proteasome stress counts because those perturbations can create wider downstream states than loss of a single THO core component, and because severe THOC2 loss could be partly survivor-conditioned before snRNA-seq recovery.

Predicted `n_degs`: 300.
