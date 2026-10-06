# Direct forecast trace

## Target and endpoint

- Target: `Cntn1`, from the declared one-row holdout manifest `Cntn1.csv`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the count of measured genes in the focal population with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Declared measurement sources used: the biology-only bundle `biology_bundles/Cntn1.json`; the 151-class training count table `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`; and the training Parquet `training_de_all_cell_groups.parquet`. The Parquet rows and packaged corpus Findings are different same-experiment representations, not independent replication.

## Cntn1 biology prior

The canonical Cntn1 bundle makes three endpoint-relevant points without exposing the held-out Cntn1 signature or outcome.

- Cntn1 is highly reachable in the requested focal population: 23,335 of 23,679 non-target 151-class nuclei express Cntn1, with 98.55% expressing, mean raw UMI 7.36, mean log1p(CP10K) 1.619, and pseudobulk CPM 461.4.
- Contactin-1 functions as a GPI-linked surface protein in installed paranodal Contactin-1/Caspr1/NF155 complexes and in a neuronal surface/perineuronal-net anchoring pool, so a P16 genome edit stops new supply but does not acutely remove all pre-existing protein.
- The functional-stock adjudication calls the P37-P44 lesion `partially_depleted_or_leading_edge`: ongoing postnatal myelin and PNN maturation give some demand for new Contactin-1, but direct target-protein clearance is not known and an installed paranodal-complex proxy can retain material past the 21-28 day assay window.

This prior supports a real but muted postmitotic perturbation in thalamic neurons, not a broad stress, survival, or cell-fate program.

## Training measurements

The declared 151-class count table is sparse: among 1,674 visible training perturbations, 1,205 have `n_degs = 0`; the median is 0; the 75th percentile is 1; only 193 exceed 1 DEG.

I nominated Cntn1 analogs from the whole training universe with the curated mouse annotation store rather than a symbol-prefix rule. The only specific non-fallback, training-available candidates were:

| comparator | typed relation to Cntn1 | observed `n_degs` in 151 TH |
| --- | --- | ---: |
| Nrcam | native mouse CORUM Cntn1-Nrcam-Ptprb complex | 2 |
| Cntnap1 | STRING physical; Caspr1/paranodal partner family | 1 |
| Cntnap2 | STRING physical; CASPR paralog/juxtaparanodal family | 1 |
| Prnp | STRING physical; broad GPI-linked surface neighbor | 1 |

The matched raw Parquet rows showed that this tiny burden was mostly self-transcript:

- `Cntnap1`: one significant row, `Cntnap1` down.
- `Cntnap2`: one significant row, `Cntnap2` down.
- `Prnp`: one significant row, `Prnp` down.
- `Nrcam`: two significant rows, `Nrcam` down and `Letm2` up.

Nearby L1/NCAM and synaptic-adhesion comparators in the same count table were similarly flat or self-only in the 151 class: `Dscam` 0, `Tenm4` 0, `Itgb1` 0, `Ncam1` 1, `L1cam` 1, `Chl1` 1, `Nrxn1` 1, `Nrxn2` 0, `Nrxn3` 0, `Adam22` 1, and `Scn1b` 2. In the top 100 Cntn1 annotation nominees, the median 151-class count was still 0 and the 90th percentile was 2; the large-count outliers were broad signaling or chromatin nodes such as `Ctnnb1`, not close Cntn1 operation analogs.

The profile review of 20 Cntn1-relevant adhesion/surface perturbations in the exact 151-class context also did not reveal a hidden shared module. Five supplied profiles had no significant feature and the remaining 15 were in the 1-9 significant-feature bin. Across the 190 pairwise comparisons, the median top-tail overlap coefficient was 0.025 in both the positive and negative directions, and significant-program overlap was zero. Focal comparisons of `Nrcam`, `Cntnap1`, `Cntnap2`, and `Prnp` against ten leading adhesion peers had no significant-feature intersections and near-zero whole-profile correlations; absolute Pearson correlations stayed below 0.043.

Packaged same-experiment Findings for the measured analogs agree with the raw rows. `Cntnap1` was reported as pan-surface transcriptionally buffered despite canonical paranodal biology; `Cntnap2` did not converge with `Cntnap1` or Kv1-complex genes; and `Nrcam` plus represented L1-family, ankyrin, neuropilin, and node/paranode comparators did not phenocopy one another in nuclear RNA.

## Synthesis

The strongest scale information is the matched count behavior of the Cntn1-specific comparators: `Nrcam`, `Cntnap1`, `Cntnap2`, and `Prnp` have counts 2, 1, 1, and 1, and three of those four are just the self-target row. The Cntn1 biology bundle pushes away from a complete functional null because Cntn1 is very broadly expressed in the focal class and postnatal renewal is still plausible, but it also pushes against a multi-gene downstream response because the operative Contactin-1 pools are local, installed surface structures whose loss is expected to be only partial over 21-28 days.

I therefore forecast a singleton significant row in 151 TH: most likely the target transcript itself, with no confident extra downstream program.

Point prediction: `1`.
