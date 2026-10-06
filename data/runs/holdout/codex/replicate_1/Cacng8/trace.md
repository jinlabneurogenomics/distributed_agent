# Cacng8 direct DEG-count forecast

Target and endpoint:
- Manifest target: `Cacng8`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Final point prediction: `0`

Evidence used:

1. Declared target biology bundle

   The target bundle for `Cacng8` reports focal-population expression in the assayed non-target thalamic nuclei: mean CP10K `0.5256`, mean raw UMI `0.8583`, and `10,129 / 23,679` non-target nuclei expressing `Cacng8` (`42.78%`). This makes the gene reachable in `151 TH Prkcd Grin2c Glut`, but not broadly expressed in nearly every nucleus.

   The same bundle adjudicates gamma-8 as a dynamic AMPA-receptor auxiliary membrane component. A P16 disruptive edit is expected to stop new Cacng8 supply while existing AMPAR-associated gamma-8 persists until protein/complex turnover; by the P37-P44 harvest, the functional stock is judged likely substantially depleted, with uncertainty because no Cacng8-specific thalamic clearance clock is known. The literature support is mostly hippocampal or bulk thalamic rather than a direct thalamic P16-to-P37 perturbation time course.

2. 151-class training count table

   The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` contains 1,674 measured training perturbations. The count distribution is sparse: `1,205 / 1,674` are exactly zero; the median is `0`; the 75th percentile is `1`; the 90th percentile is `2`; only `43` training targets reach at least 100 DEGs.

   The high end of the table is dominated by global RNA-processing, proteostasis, and transcriptional regulators such as `Uba5=2677`, `Tpr=1768`, `Sin3a=1433`, `Rnpc3=868`, and `Zbtb7a=841`. I did not treat those as quantitative analogs for an AMPAR auxiliary subunit.

   Counts for the closest hand-selected synaptic receptor/PSD analogs were near zero in the same table:

   | target | n_degs |
   | --- | ---: |
   | `Cacng2` | 0 |
   | `Cacng3` | 0 |
   | `Gria1` | 0 |
   | `Gria2` | 0 |
   | `Gria3` | 0 |
   | `Dlg4` | 1 |
   | `Syngap1` | 0 |
   | `Shank2` | 0 |
   | `Shank3` | 2 |
   | `Grin2a` | 1 |
   | `Grin2b` | 2 |
   | `Grin1` | 89 |

3. Direct rows from the training DE Parquet

   I read the declared `training_de_all_cell_groups.parquet` for `151 TH Prkcd Grin2c Glut` and the same analog set. The AMPAR/TARP rows were not merely just below threshold: `Cacng2` and `Cacng3` each had minimum adjusted p-value `1.0`, and `Gria2` also had minimum adjusted p-value `1.0`; `Gria1` had no BH-significant gene and minimum adjusted p-value `0.2457`; `Gria3` had minimum adjusted p-value `0.9707`. `Dlg4` had exactly one significant row, its own transcript, at adjusted p-value `1.15e-08`. In contrast, the NMDAR core subunit `Grin1` had `89` DEGs with a minimum adjusted p-value of `3.31e-53`, showing that receptor perturbations can be visible in this exact cell class but that the AMPAR/TARP/PSD branch is mostly buffered in the nuclear RNA readout.

4. Same-experiment corpus interpretation

   The selected corpus release has no target-scoped Finding, Claim, or explicit reference for `Cacng8`, so it did not expose a Cacng8 endpoint. Its Cacng2 and Cacng3 reports interpret gamma-2/gamma-3 TARP loss as producing no robust downstream transcriptional response across recovered neuronal groups, and the Dlg4 and Gria1 reports similarly frame PSD-95/GluA1 loss as synaptic and post-transcriptional biology with little persistent nuclear snRNA response. These reports are same-experiment summaries of the atlas, not independent replication.

Reasoning:

`Cacng8` is expressed enough in the focal thalamic class, and gamma-8 protein stock should often decline within the 21-28 day edit-to-harvest window, so I did not demote the perturbation as unreachable. The endpoint, however, is a stringent BH-controlled nuclear RNA count in sparsely edited recovered nuclei. The directly matched training measurements say that acute perturbation of AMPAR auxiliary subunits, AMPAR pore subunits, and PSD scaffolds usually lands at zero to a couple of significant rows in `151 TH Prkcd Grin2c Glut`, with the closest TARP paralogs `Cacng2` and `Cacng3` exactly zero and statistically flat in the Parquet rows. The visible receptor counterexample is `Grin1`, a core NMDAR subunit with much less AMPAR/TARP-like redundancy; I treated it as proof of assay visibility for some glutamate-receptor genes rather than as the best quantitative analog.

The remaining uncertainty is mostly self-transcript behavior and thalamic gamma-8 dependence: the `n_degs` count would include a significant `Cacng8` self row if CRISPR editing produced a strong enough nuclear mRNA drop, and the bundle does not establish Cacng8-specific turnover or requirement in this class. Because measured self-knockdown is not a reliable effect-size proxy in this screen and the closest measured AMPAR/TARP components were flat, I put the point prediction on the modal same-branch outcome: no measured genes below BH 0.05.
