# Direct DEG-count forecast for Zkscan3

Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, defined as the number of measured genes in the held-out perturbation with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

## Evidence used

- The declared holdout manifest contains the single target `Zkscan3`; `Zkscan3` is absent from the 1,674-row declared training count table, so no target outcome row was used.
- The training count distribution in `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` is sparse and heavy-tailed: 1,205 of 1,674 training targets have `n_degs = 0`; the median is `0`, the 75th percentile is `1`, and only 106 training targets have `n_degs >= 10`.
- The exact target biology bundle reports real focal-population reach for the target transcript: `Zkscan3` is detected in 16,790 of 23,679 non-target nuclei in `151 TH Prkcd Grin2c Glut` with mean CP10K 0.879. This makes a response biologically possible, but target expression alone is not a calibrated effect-size estimate.
- The same bundle characterizes ZKSCAN3 as a nuclear KRAB/SCAN C2H2 transcription regulator with direct mouse perturbation evidence mainly in erythroid cells and autophagy regulation evidence largely outside mouse postmitotic thalamic neurons. Zkscan3-null mice were grossly viable without a marked autophagy-response phenotype in assayed MEF/heart contexts, a Zkscan4 paralog is suggested as a possible buffer, and no target-specific endogenous ZKSCAN3 protein half-life or chromatin-residence clock was found for the 21-28 day P16-to-P37/P44 window.
- The nearest represented SCAN/C2H2 training perturbations in the focal class were silent in the declared count table and Parquet:
  - `Zkscan1`: `0` focal DEGs; focal Parquet minimum adjusted p value `1.0`.
  - `Zkscan16`: `0` focal DEGs; focal minimum adjusted p value `1.0`.
  - `Zscan26`: `0` focal DEGs; focal minimum adjusted p value `1.0`.
  - `Zfp148` and `Zfp236` gave small nonzero focal counts, `8` and `19`; broad zinc-finger outliers such as `Zbtb7a` and `Zfp423` had much larger counts but are not closer SCAN/KRAB analogues.
- Same-experiment corpus Findings for the observed training SCAN targets describe `Zkscan1` and `Zscan26` as downstream-null across recovered neuronal groups and `Zkscan16` as only a two-hit, two-cell-class surface; the synthesized Claim around `Zfp397`, `Zfp612`, `Zfp664`, `Zkscan1`, `Zkscan16`, and `Zscan26` states that represented SCAN/C2H2/KRAB-associated zinc-finger perturbations do not form an interchangeable shared neuronal transcriptomic regulon.
- The focal-class counts for genes in the ZKSCAN3 erythroid/autophagy prior were also mostly at the floor: `Gata1 = 0`, `Klf1 = 0`, `Tiam1 = 0`, `Atg5 = 0`, `Becn1 = 0`, `Atg16l1 = 0`, `Sqstm1 = 1`, and `Rb1cc1 = 4`. The corpus interpretation of `Atg5` reports only a tiny 155 MB Glut Calr/Rtn1 edge rather than a pan-neuronal autophagy/lysosomal/UPR program.

## Synthesis

`Zkscan3` is expressed broadly enough in the exact held-out population that a few direct transcriptional targets could in principle pass FDR, so I did not treat the target as unreachable. The evidence that mattered quantitatively, though, points toward the low-count mode: the closest measured SCAN-family perturbations are focal zeros and remain flat or nearly flat outside the focal class; the documented ZKSCAN3 biology is not a matched postnatal neuronal dependency; and autophagy-associated training perturbations show that this screen usually does not turn direct autophagy lesions into a thalamic nuclear RNA program.

I therefore predict the modal floor rather than borrowing from broad, mechanistically more central chromatin or proteostasis responders.

Predicted `n_degs`: **0**.
