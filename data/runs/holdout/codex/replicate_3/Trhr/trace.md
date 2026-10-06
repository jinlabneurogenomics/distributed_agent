# Trhr n_degs prediction

## Prediction

`target_name = Trhr`

`predicted_n_degs = 0`

## Evidence used

### Declared endpoint and training scale

- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut`.
- Training table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- The held-out target `Trhr` is absent from the 1,674-row declared training count table.
- The visible class is sparse: 1,205/1,674 training perturbations have `n_degs = 0`; the median is 0; the 75th percentile is 1; the 90th percentile is 2; only 103/1,674 have `n_degs > 10`.

This makes zero the default point estimate unless target biology or training analogs give a strong reason to expect a rare, broad response.

### Biology-only Trhr bundle

The declared Trhr characterization bundle reports:

- Focal expression is extremely low in the assayed non-target nuclei: 155/23,679 cells express `Trhr`, `pct_cells_expressing = 0.6546`, `mean_raw_umi = 0.0080`, `mean_cp10k = 0.0051`, and `pseudobulk_cpm = 0.5029` in `151 TH Prkcd Grin2c Glut`.
- TRHR is a seven-transmembrane receptor for TRH coupled to phosphatidylinositol/IP3-calcium-PKC signaling.
- The receptor is a preexisting membrane GPCR: a disruptive genomic edit stops new functional supply but does not directly inactivate receptor molecules already made before editing.
- Functional stock by the P37-P44 harvest is indeterminate. The source card found rapid agonist-driven phosphorylation, internalization, dephosphorylation, recruitment, and recycling, but no target-specific endogenous neuronal degradation half-life or acute postnatal loss clock.
- Adult global Trhr1 loss has endocrine and behavioral phenotypes, but that evidence is whole-animal, constitutive, and not thalamic-neuron-restricted.
- Trhr2 is a related TRH receptor with distinct knockout phenotypes; same-context compensation after acute Trhr editing was not tested.

The exact in-assay expression is the strongest downward term. A receptor present in about 0.65% of the broad recovered thalamic class gives very little perturbation reach after aggregation across all `151 TH Prkcd Grin2c Glut` nuclei, even before accounting for sparse mosaic editing and survivor-conditioned sampling.

### Training analogs and measured profiles

I nominated training-available Trhr comparators from typed mouse annotations and the selected same-experiment corpus. The nomination found no exact-complex/paralog, bidirectional same-experiment comparator, narrow-module, or direct-interaction/dependency nominee for Trhr. All 1,009 available nominees were broad functional fallbacks.

The top broad nominees were GPCR, Gq/PLC, peptide-receptor, and calcium-signaling genes rather than Trhr-specific partners. Their visible `151 TH Prkcd Grin2c Glut` DEG counts were nearly all zero:

| training target | n_degs |
|---|---:|
| Agtr1a | 0 |
| Avpr1b | 0 |
| Cckbr | 0 |
| Ednra | 0 |
| Oxtr | 0 |
| Cx3cr1 | 0 |
| Tfrc | 0 |
| Mchr1 | 0 |
| Plcb1 | 0 |
| Adra1a | 0 |
| Grm1 | 1 |
| Htr2c | 0 |
| Gnas | 0 |
| Adcy5 | 0 |
| Oprl1 | 0 |
| Oprk1 | 0 |
| Gnao1 | 1 |
| Adcy1 | 0 |
| Htr2a | 0 |
| Adcy3 | 0 |
| Prkaca | 1 |
| Prkcg | 1 |
| Prkca | 0 |
| Grm5 | 0 |
| Creb1 | 10 |
| Itpr1 | 0 |

The raw expression Parquet was then used for a matched `151 TH Prkcd Grin2c Glut` profile comparison of the top 30 annotation nominees. It found 25/30 with no significant features, 4/30 with 1 to 9, and 1/30 with 10 to 49. Across the 435 signed profile pairs, the median positive-tail overlap coefficient was only 0.075, and there was no pair with positive significant-program overlap, so these broad GPCR/calcium genes did not form a coherent high-DE transcriptional state.

The same-experiment report-edge expansion of the top 20 broad nominees was also consistent with buffering rather than strong convergence: the exact reported relation summaries around recurrent outgoing comparators were dominated by `no_shared_*`, `nonconvergent`, `absent`, `mostly_no_downstream_FDR_signal`, and `selective_pathway_visibility` calls. The 21 recurrent expansion targets again had low visible counts: 17 were zero, Prkaca/Prkcg/Camk2b/Prkar1a were one, Crebbp was eight, and Creb1 was ten.

## Synthesis

The evidence did not identify a measured training perturbation that is close enough to Trhr to override the background zero. The best direct biology argues for weak aggregate observability: the target transcript is detected in fewer than 1% of focal thalamic nuclei, and the functional effect of stopping new receptor synthesis is timing-limited by unknown turnover of an already translated GPCR pool. The visible GPCR and calcium-signaling training genes, including receptors and downstream transducers, are overwhelmingly null or near-null in this same cell class. I therefore predict that the held-out Trhr perturbation will not cross BH FDR 0.05 for any measured gene in `151 TH Prkcd Grin2c Glut`.
