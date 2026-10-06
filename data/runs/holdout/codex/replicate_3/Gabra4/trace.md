# Gabra4 forecast for `151 TH Prkcd Grin2c Glut`

## Point estimate

`predicted_n_degs = 2`

This is a direct forecast for the one held-out target `Gabra4`. The target row is absent from the declared focal count table and no Gabra4 endpoint, calibrated response probability, or labeled-neighbor outcome was used.

## Evidence used

- **Declared target and endpoint.** `codex_runtime/pipeline/task_bindings_receipt.json` binds the one-row holdout manifest to `Gabra4` and the endpoint to the training table `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]` for `151 TH Prkcd Grin2c Glut`. The requested count is measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in that class.

- **Gabra4 biology bundle.** The canonical biology view of `[local file: Gabra4.json]`, sha256 `a0cb28ff8acd9b4ca31195a7ce980caf6ca5b00b35d0f90bcd76321d786d5549`, reports that alpha-4 is an extrasynaptic GABA(A) receptor subunit mediating tonic inhibition in thalamic relay neurons. `Gabra4` has exact focal-population expression in non-target thalamic nuclei: 23,570 / 23,679 cells expressing, 99.54% expressing, mean CP10K 8.51, and mean raw UMI 13.74. The functional-stock adjudication concludes that P16 CRISPR should stop new alpha-4 supply and that surface alpha-4/delta receptor stock is likely substantially depleted by the P37-P44 harvest, while alpha-4-specific thalamic turnover after postnatal edit remains unmeasured.

- **Whole training-count scale.** The declared focal count table contains 1,674 non-held-out training targets and excludes `Gabra4`. It is highly sparse: 1,205 targets have 0 DEGs, 1,481 have at most 1 DEG, 1,512 have at most 2 DEGs, and 1,542 have at most 4 DEGs. The median is 0 and the nonzero median is 1.

- **Closest GABA(A)-receptor family counts.** The GABA(A) receptor subunits present in the same count table sit at the floor:

  ```text
  Gabra1  1
  Gabra2  0
  Gabra3  0
  Gabra5  0
  Gabrb1  0
  Gabrb2  4
  Gabrb3  0
  Gabrd   2
  Gabrg2  1
  Gabrg3  0
  Gabrr2  0
  ```

  `Gabra6`, another alpha paralog named in the Gabra4 card as a related subunit, was absent from this training table.

- **Exact focal Parquet rows for the selected analogs.** I filtered `[local file: training_de_all_cell_groups.parquet]` to `group_name == "151 TH Prkcd Grin2c Glut"`, the GABA(A) family targets above, and `pvals_adj < 0.05`. The active family members were dominated by their self-transcript rows: `Gabra1` had only `Gabra1`; `Gabrg2` had only `Gabrg2`; `Gabrd` had `Gabrd` plus `Cttnbp2`; and `Gabrb2` had `Gabrb2`, `Nr4a1`, `Vgf`, and `Nalf1`. The other seven family members had no significant genes in this class.

- **Measured profile recurrence.** A profile comparison over those 11 GABA(A) subunits in the same Parquet slice wrote `profile/gaba_receptor_compare.json` and `profile/gaba_receptor_cohort.json`. The comparison found 7/11 nodes with no significant features and 4/11 with only 1-9 significant features. The cohort diagnostic did not show a shared significant program: significant-program overlap was 0 in the positive and negative directions for the GABA(A) pairs where significant features existed. This is a profile-topology diagnostic of the same training Parquet, not independent replication.

- **Excitability boundary checks.** Nearby ion-channel and glutamate-receptor perturbations in the same focal count table were also mostly small, with `Grin2a = 1`, `Grin2b = 2`, `Grin2d = 0`, `Grin3a = 0`, and the thalamic calcium-channel target `Cacna1g = 12`. `Grin1` was the clear larger excitatory-receptor exception at 89 DEGs, so I treated strong NMDA core loss as an upper-scale warning rather than as the Gabra4 point.

## Synthesis

The count table alone would put an arbitrary held-out perturbation at zero. Gabra4 is not arbitrary, because its transcript is broadly and strongly detected in the exact thalamic population and its receptor stock should be functionally reachable by the 21-28 day endpoint. That made a pure null less plausible than for absent or context-mismatched receptor genes.

The best quantitative comparators, however, argue for only a tiny count. Loss of the delta partner `Gabrd` produced 2 DEGs, the gamma partner `Gabrg2` produced 1, the closest assayed alpha subunit `Gabra1` produced 1, and even the largest local GABA(A) beta-subunit response was 4. Their exact significant rows are mostly self-transcript detection rather than a recurrent downstream thalamic state. Gabra4 therefore looked much closer to `Gabrd`/`Gabrg2`/`Gabra1` than to broad transcriptional regulators or to the `Grin1` exception.

I therefore placed the forecast just above the self-only floor: one expected self-transcript DEG plus roughly one additional downstream/adaptive thalamic gene, giving a point estimate of **2**.
