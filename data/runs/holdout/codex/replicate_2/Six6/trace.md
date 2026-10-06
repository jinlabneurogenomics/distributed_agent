# Direct forecast trace

## Target and endpoint

- Target: `Six6`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Prediction target exposure: the `Six6` perturbation profile and target DEG count were held out and were not used.

## Evidence used

1. **Training count table**

   The declared `151 TH Prkcd_Grin2c_Glut` training table contains 1,674 measured training perturbations. Its count distribution is mostly zero:

   - `n_degs = 0`: 1,205 / 1,674 targets, 71.98%
   - `n_degs <= 1`: 1,481 / 1,674 targets, 88.47%
   - `n_degs <= 2`: 1,512 / 1,674 targets, 90.32%
   - median `n_degs`: 0
   - 90th percentile: 2
   - 95th percentile: 18

   This gives a strong sparse-response prior for a target without direct evidence of active thalamic transcriptional demand.

2. **Canonical `Six6` biology bundle**

   The declared biology bundle reports exact in-assay target reach in the same focal population:

   - `Six6` transcript detected in 9 of 23,679 matched non-target nuclei
   - expressing fraction: 0.0380%
   - mean raw UMI: 0.000380 per nucleus
   - total `Six6` UMIs: 9
   - pseudobulk CPM: 0.0238

   `Six6` is a homeodomain transcription factor. A P16 CRISPR edit should stop synthesis of new intact SIX6 protein in an edited, truly `Six6`-expressing cell, but it does not acutely inactivate pre-existing protein. The bundle had no transferable measurement of SIX6 protein turnover over the 21-28 day edit-to-harvest window. The strongest functional phenotypes came from developmental hypothalamic GnRH-neuron or SCN models, not from postmitotic thalamic neurons. Adult thalamic regional RNA/ISH non-detection and the direct snRNA expression measurement together make a large assayed thalamic SIX6-dependent program unlikely, while the sparse 9-cell expression tail leaves a small residual possibility.

3. **Training-available analog nomination**

   The typed mouse analog nominator resolved `Six6` but found it absent from the training universe, the selected corpus ledger, and the selected BioKG projection. Among 1,201 training-available nominees, it found no exact-complex/paralog, bidirectional-corpus-comparator, narrow-module, or direct-interaction tier; all nominees came from broad functional-fallback annotations such as eye development, sequence-specific DNA binding, and transcription-factor activity.

   I inspected the highest-priority broad nominees against the declared count table:

   | nominee | n_degs |
   |---|---:|
   | Atf6 | 0 |
   | Meis2 | 0 |
   | Pbx1 | 0 |
   | Six3 | 0 |
   | Foxe3 | 0 |
   | Meis1 | 0 |
   | Pbx3 | 0 |
   | Bmpr1b | 0 |
   | Gata4 | 0 |
   | Pax6 | 0 |
   | Otx2 | 0 |
   | En1 | 0 |
   | Sox2 | 2 |

   The declared all-cell training Parquet profile comparison in `151 TH Prkcd Grin2c Glut` gave the same result: among these 13 broad developmental/transcription-factor comparators, 12 had no BH-significant features and one had 1-9 significant features. Pairwise significant-program overlap was absent across this cohort, so the few unadjusted tail features did not form a recurrent thalamic program.

## Synthesis

The decisive facts are the near-absent focal expression of `Six6` and the lack of a strong local comparator. A severe effect in GnRH or SCN development does not transfer cleanly to a sparse postnatal thalamic population, and the unknown SIX6 protein residence time weakens rather than strengthens a P16-to-P37/P44 transcriptional-loss projection. The broad TF/developmental nominees were useful as a falsification check: if general eye/developmental homeobox-like TF biology caused a visible signature in this class, the top nominated training perturbations should have shown it, but they were almost all exact zeros.

I therefore place `Six6` at the null mode of the training distribution. The exact non-target expression tail prevents interpreting zero as a biological impossibility, but it is too small and too weakly connected to the assayed thalamic endpoint to move the integer point above zero.

Point prediction: `0`
