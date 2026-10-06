# Plxnc1 direct DEG-count forecast

## Declared target and endpoint

- Target: `Plxnc1`, from the one-row holdout manifest.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, counted as measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Declared measurement sources used:
  - `biology_bundles/Plxnc1.json` for outcome-blind Plxnc1 biology and exact focal-population expression reach.
  - `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` for training target counts.
  - `training_de_all_cell_groups.parquet` for exact training signatures in the requested cell class.

## Biology prior for Plxnc1

The canonical Plxnc1 bundle supports functional realization by harvest but not a broad thalamic response. Plexin-C1 is a single-pass Sema7A receptor in a renewable cell-surface signaling pool; disruptive editing should stop new receptor supply and the bundle adjudicates the operative stock as `likely_substantially_depleted` over the P16 to P37-P44 window. The same bundle also keeps the key limits explicit: no Plxnc1-specific thalamic depletion series was found, postnatal loss phenotypes are olfactory/cerebellar rather than thalamic, and Integrin-beta1 can participate in Sema7A signaling without a matched thalamic compensation test.

The exact in-assay non-target expression reach makes the target transcript observable in the focal class: Plxnc1 is detected in 13,830 of 23,679 non-target nuclei, with 58.406% expressing cells, mean raw UMI 1.231, mean log1p(CP10k) 0.466, and pseudobulk CPM 77.16. I treated this as support that a self-transcript DEG is feasible, not as evidence of editing strength or downstream magnitude.

## Training measurements used

Across the full declared training count table for this cell class, the response distribution is sparse:

- 1,205 / 1,674 training perturbations had `n_degs = 0`.
- The 50th, 75th, and 90th percentiles were 0, 1, and 2 DEGs.

I used a receptor and axon-guidance cohort as the nearest endpoint-matched quantitative context:

`Cadm2`, `Cntnap1`, `Cntnap2`, `Dcc`, `Epha4`, `Ephb2`, `Itgb1`, `L1cam`, `Ncam1`, `Neo1`, `Nrcam`, `Nrp1`, `Nrp2`, `Plxna1`, `Plxna2`, `Plxna4`, `Plxnd1`, `Robo1`, `Robo2`, `Sema4d`, `Sema5a`, `Sema6a`, `Unc5c`, `Unc5d`.

Their declared training counts in `151 TH Prkcd Grin2c Glut` were tightly concentrated at zero or one:

- 13 / 24 had `n_degs = 0`.
- 10 / 24 had `n_degs = 1`.
- 1 / 24 had `n_degs = 2`.
- Sum across the cohort was 12 DEGs.

Exact Parquet rows showed that this was mostly visible target-transcript knockdown rather than downstream transcriptional reprogramming. The 12 significant rows in the 24-node cohort were:

| target | significant genes |
| --- | --- |
| `Cadm2` | `Cadm2` |
| `Cntnap1` | `Cntnap1` |
| `Cntnap2` | `Cntnap2` |
| `Epha4` | `Epha4` |
| `L1cam` | `L1cam` |
| `Ncam1` | `Ncam1` |
| `Nrcam` | `Nrcam`, `Letm2` |
| `Plxna2` | `Plxna2` |
| `Robo1` | `Robo1` |
| `Sema5a` | `Sema5a` |
| `Unc5c` | `Unc5c` |

Thus only one non-self significant gene, `Letm2` after `Nrcam` perturbation, appeared in this close receptor/guidance cohort. In the same-family plexin rows, `Plxna1`, `Plxna4`, and `Plxnd1` were zero and `Plxna2` had a single self-target DEG.

A profile comparison of all 24 selected perturbations against their `151 TH Prkcd Grin2c Glut` Parquet signatures found profiles for every selected node. The cohort did not carry a coherent significant downstream program: positive top-tail overlap averaged 0.0767, negative top-tail overlap averaged 0.1435, and significant-program overlap was zero in the available pairwise views. This made me treat the cohort as a sparse count prior rather than as evidence for a transferable multi-gene state.

## Synthesis

Plxnc1 is biologically reachable in this assay window and detectably expressed in the focal thalamic class, so a visible self-transcript perturbation is plausible. However, the best same-assay receptor, semaphorin/plexin, and guidance comparators almost never generated downstream DE in `151 TH Prkcd Grin2c Glut`; their one-gene signatures were usually only the perturbed transcript itself, and there was no recurrent significant guidance-receptor state in the Parquet profiles.

Those two bearings put the forecast just above the all-training and receptor-family zero mode but far below any multi-gene footprint. I therefore predict one significant gene.
