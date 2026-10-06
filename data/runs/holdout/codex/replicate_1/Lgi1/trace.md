# Lgi1 forecast trace

## Target and endpoint

- Target: `Lgi1`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05` in the declared held-out perturbation.
- Prediction: `1`

## Evidence used

The declared biology bundle for `Lgi1` reports exact in-assay reach in this focal population: `Lgi1` was detected in 10,872 of 23,679 non-target nuclei, 45.914% of the population, with mean log1p(CP10k) 0.3218. The functional-stock card treats LGI1 as a secreted ADAM22/ADAM23 trans-synaptic organizer whose new supply should stop after successful editing, and whose synaptic pool should substantially decline over the 21-28 days from P16 edit to P37-P44 harvest. It also flags restricted thalamic expression, uncertain target-specific extracellular residence, and possible supply from unedited neighbors as unresolved dampers.

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table is very sparse: among 1,674 held-in perturbations, 1,205 had zero DEGs, the median was zero, 75% were at one or below, and only 43 reached 100 or more DEGs. High-count outliers were broad cell-intrinsic regulators such as `Uba5`, `Tpr`, `Sin3a`, and spliceosome/proteasome/chromatin factors, not close secreted-synapse analogs for LGI1.

The closest training perturbations in the LGI1 synaptic axis were flat or self-only in the same `151` count table and Parquet rows:

| training target | `151` n_degs | interpretation from the `151` Parquet |
|---|---:|---|
| `Adam22` | 1 | only `Adam22` itself was significant |
| `Kcna1` | 0 | no significant feature |
| `Kcna2` | 0 | no significant feature |
| `Kcnab2` | 1 | only `Kcnab2` itself was significant |
| `Cacng2` | 0 | no significant feature |
| `Gria1` | 0 | no significant feature |
| `Gria2` | 0 | no significant feature |
| `Gria3` | 0 | no significant feature |
| `Dlg4` | 1 | only `Dlg4` itself was significant |
| `Nrxn1` | 1 | only `Nrxn1` itself was significant |
| `Shank3` | 2 | `Shank3` plus one downstream hit |

The same-experiment corpus supported this interpretation without acting as an independent replicate: its packaged Findings describe `Adam22`, `Cacng2`, `Dlg4`, `Gria1/2/3`, `Kcna1`, `Nrxn1`, and `Shank3` as buffered or essentially flat in the recovered neuronal transcriptome, and specifically place `Adam22`, `Cacng2`, `Dlg4`, AMPAR genes, and Kv1 genes in a weakly responsive synaptic-complex class rather than in an NMDAR-like program.

I used the expression Parquet to compare a hand-selected 13-target synaptic cohort in exactly `151 TH Prkcd Grin2c Glut`: `Adam22`, `Dlg4`, `Cacng2`, `Kcna1`, `Kcna2`, `Kcnab2`, `Gria1`, `Gria2`, `Gria3`, `Nrxn1`, `Shank3`, `Grin1`, and `Cacna1g`. Six of thirteen had no significant feature in this group, five had 1-9, one had 10-49, and only `Grin1` exceeded 50. Pairwise significant-program overlap across the cohort was essentially absent, so these analogs did not expose a shared downstream module that should be added to the LGI1 forecast.

## Synthesis

`Lgi1` is not a pure no-expression null: almost half of the non-target thalamic nuclei expressed the gene, and the functional-stock card makes loss of newly secreted LGI1 biologically plausible by harvest. The closest measured receptor/channel/scaffold perturbations, however, show that this synaptic-organizer axis is usually transcriptionally buffered in the sparse postnatal mosaic assay. Mosaic extracellular rescue and regionally restricted ligand expression further reduce the chance of a broad cell-autonomous survivor RNA state.

The best point is therefore a self-or-singleton-scale response. I chose `1` rather than `0` because focal `Lgi1` reach is substantial enough that a self-transcript Wilcoxon hit is plausible in the high-yield `151` population, while the close analogs argue against more than an isolated downstream change.
