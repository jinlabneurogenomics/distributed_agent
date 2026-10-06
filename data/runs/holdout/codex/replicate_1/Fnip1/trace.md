# Fnip1 n_degs forecast

## Target and endpoint

- Target: `Fnip1`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the held-out target profile.
- Declared target outcome status: the Fnip1 expression signature and its `n_degs` endpoint are absent from the declared inputs and were not queried or reconstructed.

## Declared evidence used

### Fnip1 biology-only bundle

Source: declared `Fnip1.json` characterization bundle, schema `expected-transcript-impact-agent-bundle-v1`, sha256 `7d09e9cd854b9f97c779f611227617784192834ac3ba7c85109cbeb5e2f60c13`.

- Exact focal-population expression reach is real but not extreme: Fnip1 was detected in `17,909 / 23,679` non-target nuclei in `151 TH Prkcd Grin2c Glut`, `75.6324%` of cells, mean raw UMI `1.6156`, mean cp10k `1.0198`.
- FNIP1 is a dynamic FLCN/AMPK-associated and Hsp90-cochaperone protein component. Editing at P16 is expected to stop new functional FNIP1 synthesis, but does not directly destroy pre-existing protein complexes.
- Functional stock at the P37-P44 harvest is indeterminate. The bundle found a proteasomal degradation route but no target-specific quantitative half-life, FLCN-FNIP complex residence time, or post-edit clearance curve in postmitotic neurons.
- Fnip2 can overlap with Fnip1 in some non-neural tissues, but the card had no thalamic-neuron compensation test.
- The closest direct loss phenotype was systemic/non-neural B-cell developmental evidence; no postnatal neural Fnip1 loss experiment established a matched transcriptional phenotype or latency.

### Same-experiment Fnip1 corpus

The selected corpus release had no packaged Findings, Claims, or explicit comparator references for `Fnip1`. I therefore did not have a same-experiment Fnip1 semantic report to transfer from; the corpus evidence used below is for selected measured training perturbations and is not independent replication of the count table.

## Training counts and selected measured perturbations

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` contained 1,674 training perturbations. Its empirical distribution is sparse:

- 1,205 targets had `n_degs = 0`
- 276 had `n_degs = 1`
- 469 had any nonzero count
- median `0`, 75th percentile `1`, 90th percentile `2`, 95th percentile `18`, mean `14.05`

Training targets on the broad FLCN/FNIP1 biological axes were mostly weak in the requested cell class:

| axis | target | n_degs at BH p < 0.05 |
| --- | --- | ---: |
| mTORC1 negative regulators | Tsc2 | 86 |
| mTORC1 negative regulators | Depdc5 | 13 |
| mTOR complex / AMPK / LKB1 branch | Mtor | 2 |
| mTOR complex / AMPK / LKB1 branch | Vcp | 2 |
| mTOR complex / AMPK / LKB1 branch | Rptor | 0 |
| mTOR complex / AMPK / LKB1 branch | Prkaa2 | 0 |
| mTOR complex / AMPK / LKB1 branch | Prkag2 | 0 |
| mTOR complex / AMPK / LKB1 branch | Strada | 0 |
| Hsp90/chaperone branch | Hsp90ab1 | 1 |
| Hsp90/chaperone branch | Hsf1 | 6 |
| Hsp90/chaperone branch | Hspa5 | 5 |
| Hsp90/chaperone branch | Hspa8 | 9 |

The corpus interpretation of those measured nodes was decisive for not treating the 86-gene Tsc2 response as a direct proxy for Fnip1:

- `Tsc2` and `Depdc5` were the two clear negative-regulator perturbations capable of derepressing an mTORC1 sterol/endolysosomal state in this thalamic class.
- `Mtor`, `Rptor`, `Prkaa2`, `Prkag2`, `Strada`, and several upstream PI3K/AKT relatives were buffered, nearly flat, or explicitly non-phenocopying despite pathway proximity.
- `Hsp90ab1` itself had no downstream program; its count-table value of 1 in this class was the self transcript, and the Hsp90 corpus Findings place single Hsp90/DnaJ/chaperone perturbations near the buffered basal-neuron regime rather than the large core-proteasome stress state.

## Matched profile analysis

I compared the exact selected 12-node cohort against the declared training Parquet in `151 TH Prkcd Grin2c Glut`, using signed Wilcoxon `scores` over measured genes and `pvals_adj < 0.05` as the significance flag. The resulting profile artifacts are:

- `evidence/fnip1_axis_profile_compare.json`
- `evidence/fnip1_axis_profile_cohort.json`

The pairwise structure supported a low, non-pooled forecast:

- `Depdc5` and `Tsc2` were the only close mTOR-negative-regulator pair in the chosen set: whole-profile Pearson `0.2877`, cosine `0.2899`, with 5 shared positive and 3 shared negative significant genes.
- `Mtor` opposed the `Tsc2`/`Depdc5` state rather than matching it: `Tsc2` vs `Mtor` cosine `-0.2042`, `Depdc5` vs `Mtor` cosine `-0.1541`.
- The selected cohort as a whole had very weak recurrence: median positive-tail overlap `0.025`, median negative-tail overlap `0.04`.
- Hsp90/chaperone nodes and AMPK/mTOR-complex nodes were mostly near zero against the Depdc5/Tsc2 sterol state; for example `Depdc5` vs `Hsp90ab1` cosine was `-0.0066`, and `Tsc2` vs `Hsp90ab1` cosine was `0.0004`.

## Synthesis

Fnip1 is genuinely expressed in the assayed thalamic nuclei, so a completely invisible perturbation is not forced by lack of target reach. The biological operation, however, is not a strong match to the two high-end training mTOR derepression phenotypes:

- FNIP1/FLCN was not directly represented in the training count table; represented single AMPK, positive mTORC1, and LKB1-axis perturbations were flat or nearly flat.
- The count-inflating Depdc5/Tsc2 module came from loss of strong negative mTORC1 brakes. Fnip1 is better treated as a buffered nutrient-sensing/cochaperone adaptor with unresolved sign, unresolved stock depletion by 21-28 days, and possible Fnip2 buffering.
- Single Hsp90/chaperone perturbations provide additional downward evidence: acute loss in the basal postmitotic-neuron setting often produced no broad heat-shock, UPR, or proteostasis transcriptome.

Those points place Fnip1 far below Tsc2 and Depdc5 and close to the dense 0-1 part of the training distribution. I used the exact Fnip1 expression reach to move off a hard zero, but only to a one-gene point because neither the same-experiment mTOR-axis neighbors nor the Hsp90-axis neighbors support a multi-gene Fnip1 state in this assay.

Predicted `n_degs`: `1`
