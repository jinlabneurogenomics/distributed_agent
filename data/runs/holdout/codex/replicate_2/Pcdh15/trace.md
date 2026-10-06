# Pcdh15 DEG-count forecast

## Declared endpoint

- Target: `Pcdh15`
- Cell population: `151 TH Prkcd Grin2c Glut`
- Endpoint: count of measured genes with BH-adjusted Wilcoxon `p < 0.05`

## Evidence used

The declared biology bundle places the perturbation in a thalamic neuronal population where the target transcript is present but not pan-cellular: `Pcdh15` is detected in 10,132 of 23,679 matched non-target nuclei in `151 TH Prkcd Grin2c Glut`, or 42.789%, with pseudobulk CPM 48.61 and mean log1p CP10K 0.301. That makes the target reachable in a material minority of assayed nuclei, not an expression-absent case.

The same bundle does not support a strong short-window functional forecast. PCDH15 is an installed membrane cadherin best established as the lower tip-link component with CDH23 in sensory hair cells. A P16 disruptive edit should stop production of affected new protein, but it does not directly sever existing membrane or complex-associated PCDH15. The thalamic operative pool, renewal demand, and clearance time are unknown; the functional-stock adjudication therefore called functional stock by P37-P44 indeterminate. Adult constitutive mouse loss shows neural and behavioral phenotypes, but that evidence is systemic and developmental and does not establish a post-P16 thalamic transcriptional response.

The matched 151 training count table is highly zero-heavy: 1,205 of 1,674 training perturbations have `n_degs = 0`; only 106 reach 10, 43 reach 100, and 3 reach 1000. The high tail is dominated by RNA processing, spliceosome, proteostasis, and transcriptional regulators (`Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, `Zbtb7a`, `U2af2`, `Psmb4`, `Hnrnpu`, `Yy1`, `Elp1`), not by cell-surface adhesion genes.

The direct partner `Cdh23` was absent from the declared 151 training table, so the closest measured rows were lower-specificity adhesion, protocadherin, and guidance targets:

| training perturbation | 151 `n_degs` | significant rows across all training cell groups | interpretation |
|---|---:|---:|---|
| `Pcdh19` | 0 | 0 | available protocadherin row, transcriptionally silent |
| `Adgrv1` | 0 | 0 | Usher-related membrane adhesion row, silent |
| `Dscam` | 0 | 0 | cell-adhesion/guidance row, only a subthreshold self hit in 151 |
| `Dcc` | 0 | 0 | axon-guidance receptor row, silent |
| `Ptprd` | 0 | 0 | neural adhesion/phosphatase row, silent |
| `Unc5d` | 0 | 0 | guidance receptor row, silent |
| `Cntnap1` | 1 | 5 | one 151 hit, the target transcript |
| `Cntnap2` | 1 | 6 | one 151 hit, the target transcript |
| `Ncam1` | 1 | 10 | one 151 hit, the target transcript |
| `Unc5c` | 1 | 1 | one 151 hit, the target transcript |

## Synthesis

`Pcdh15` has enough baseline expression that a single self-transcript DEG or a small downstream program is plausible. I did not add a self-hit by default, however: in this perturbation design visible self-knockdown is not a reliable editing or effect readout, and the closest zero-count adhesion rows included negative but nonsignificant self contrasts such as `Pcdh19` and `Dscam`. The observed same-class adhesion and guidance perturbations therefore put the best endpoint scale at 0 to 1 significant genes rather than at the table mean.

The biology prior pushes the point to the lower end of that interval. PCDH15 loss may be meaningful in adult neurons, but the experiment asks for an acute postmitotic P16-to-P37/P44 CRISPR response among recovered thalamic nuclei. The declared evidence leaves existing protein persistence, thalamic complex identity, and latency unresolved, and it supplies no operation-matched training perturbation with a recurrent positive thalamic RNA program. I therefore predict no BH-significant genes in the held-out 151 contrast.

Predicted `n_degs`: 0
