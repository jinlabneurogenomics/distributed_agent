# Sry forecast for `151 TH Prkcd Grin2c Glut`

## Evidence used

- **Declared target:** the one-row manifest is `Sry`.
- **Target focal reach:** the canonical `Sry` biology bundle reports exact non-target expression in `151 TH Prkcd Grin2c Glut` as `0 / 23679` expressing nuclei, `total_target_umi = 0`, `pseudobulk_cpm = 0`, `mean_cp10k = 0`, and `mean_log1p_cp10k = 0`. The bundle marks this exact in-assay expression as superseding qualitative target-presence estimates for the focal population.
- **Functional stock:** where Sry is expressed, the same bundle adjudicates the active molecule as a short-lived nuclear transcription factor whose existing protein stock should be substantially depleted by the P37-P44 harvest after P16 disruptive editing. This argues against persistence as the reason for a null, but only in cells with ongoing Sry expression.
- **Context mismatch of positive prior biology:** adult rat substantia-nigra antisense data support a postnatal neural Sry loss phenotype within ten days, but that evidence is dopaminergic substantia nigra rather than mouse thalamic NeuN-positive nuclei. The bundle did not find a postnatal thalamic single-cell or histologic map establishing broad Sry expression.
- **Training endpoint scale:** the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` contains 1,674 training targets; `Sry` is absent. The distribution is highly zero-inflated: 1,205/1,674 are exactly `0`, the median is `0`, the 75th percentile is `1`, and only 42/1,674 exceed 100 DEGs.
- **Nearest related training perturbations:** the source bundle only nominated Sox-family HMG-domain genes as explicit molecular relatives. In the same declared count table, the Sox perturbations present in training were:

| target_name | n_degs |
|---|---:|
| Sox2 | 2 |
| Sox4 | 0 |
| Sox5 | 2 |
| Sox9 | 0 |
| Sox10 | 0 |
| Sox11 | 0 |

The focal expression Parquet agrees with those counts: in `151 TH Prkcd Grin2c Glut`, `Sox2` had two BH-significant measured genes, `Sox5` had two, and `Sox4`, `Sox9`, `Sox10`, and `Sox11` had none.

## Reasoning

The endpoint is the focal-population number of measured genes with BH-adjusted Wilcoxon `p < 0.05`, so I treated the count table and Parquet as direct training measurements for the requested response scale. Those two internal surfaces are the same Perturb-seq experiment, so the Parquet check was used only to confirm the row-level focal counts for selected training comparators, not as independent replication.

The central biological determinant is expression reach. Sry has convincing acute loss-of-function realizability for any neuron that actively makes SRY protein, because stopping new synthesis of a short-lived transcription factor should deplete the active pool within the 21-28 day editing window. But the exact focal baseline has no detected Sry RNA in 23,679 matched non-target thalamic nuclei. That does not prove absence of every molecule in vivo, yet it makes a recovered, aggregate thalamic transcriptional footprint unlikely: any real Sry-positive compartment would have to be very rare or very weakly captured.

The generic transcription-factor prior also stays small in this class. Four of six training Sox/HMG comparators were exactly silent and the other two produced only two DEGs each. Given the focal count distribution's point mass at zero and the lack of detected Sry expression in the assayed population, the modal value is the best integer forecast. I therefore predict **0 DEGs**.
