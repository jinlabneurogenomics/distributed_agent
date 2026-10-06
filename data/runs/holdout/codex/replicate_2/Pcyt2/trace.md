# Pcyt2 n_degs forecast for 151 TH Prkcd Grin2c Glut

## Declared target and biological prior

- Target: `Pcyt2`, from the one-row holdout manifest.
- Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Target biology source: `[local file: Pcyt2.json]`, schema `expected-transcript-impact-agent-bundle-v1`, SHA-256 `c71304add8116bc994e8caeb40a76f41187722f2f212e681b085717db74f5df7`.

The prediction-safe Pcyt2 bundle made the perturbation biologically plausible in this class but not an expected large, immediate transcriptional lesion. `Pcyt2` was well detected in the exact non-target focal population, with 20,185 of 23,679 nuclei expressing the gene, 85.24% detection, mean raw UMI 2.44, mean log1p CP10k 0.816, and pseudobulk CPM 152.7. Functionally, Pcyt2 is the CTP:phosphoethanolamine cytidylyltransferase for de novo phosphatidylethanolamine synthesis. Its post-P16 edit stops new Pcyt2 synthesis, while residual enzyme, pre-existing PE, slower lipid pools, and mitochondrial Pisd-dependent PE synthesis buffer the loss. The adjudicated stock state was therefore `partially_depleted_or_leading_edge`, not full persistence and not uniform depletion by the P37-P44 harvest.

## Training evidence used

Training counts came from the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, and matched differential-expression rows came from `training_de_all_cell_groups.parquet`. I used the training-only thalamic counts and did not use a `Pcyt2` DE profile or held-out count.

The focal training table is strongly zero-inflated:

| summary | value |
| --- | ---: |
| training perturbations | 1,674 |
| `n_degs = 0` | 1,205 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| mean | 14.05 |

The closest exact training perturbation named by the Pcyt2 biology bundle was `Selenoi`, the downstream ethanolamine phosphotransferase in the CDP-ethanolamine route. In the focal class `Selenoi` had 5 DEGs at BH < 0.05:

| gene | logfoldchange | BH p |
| --- | ---: | ---: |
| `Insig1` | 0.758 | 0.000376 |
| `Msmo1` | 0.713 | 0.002095 |
| `Selenoi` | -0.652 | 0.002759 |
| `Fdft1` | 0.820 | 0.002890 |
| `Nos1ap` | -0.435 | 0.039004 |

The same Parquet slice showed that `Selenoi` had zero BH < 0.05 DEGs in every other recovered cell group, including `155 MB Glut`, so the 5-count response was compact and 151-specific rather than a large pan-neuronal stress state.

Packaged same-experiment corpus Findings in release `perturbai-july-260713-sourceguard-1773-v1` supported that interpretation. `Selenoi:F001` described the response as a compact sterol-feedback signature in `151 TH Prkcd Grin2c Glut`; `Selenoi:F004` reported that literature-obvious ether-lipid and sterol-enzyme comparators such as `Agps`, `Far1`, `Hmgcr`, and `Srebf1` did not strictly phenocopy `Selenoi`; and `Selenoi:F005` reported that even the detectable `Selenoi` thalamic response lacked a broad UPR, ISR, autophagy-lysosome, redox, or `Tardbp` tail.

Consistent with those Findings, related lipid or membrane-homeostasis training perturbations stayed small in the focal count table unless they belonged to broader trafficking/proteostasis states:

| perturbation | focal `n_degs` |
| --- | ---: |
| `Selenoi` | 5 |
| `Agps` | 1 |
| `Far1` | 2 |
| `Hmgcr` | 0 |
| `Srebf1` | 0 |
| `Abhd12` | 1 |
| `Pi4kb` | 1 |
| `Synj1` | 1 |
| `Plcb1` | 0 |
| `Prkca` | 0 |
| `Prkcg` | 1 |
| `Pitpna` | 21 |
| `Marchf6` | 14 |
| `Mib1` | 27 |
| `Dctn1` | 75 |
| `Rab7` | 501 |

## Point synthesis

The baseline for an arbitrary focal-class perturbation is 0 to 1 DEGs, and the large tail is dominated by perturbations of splicing, proteostasis, trafficking, transcriptional regulation, or core neuronal physiology. Pcyt2 is not in that large-response class. Its exact thalamic expression and continuous PE renewal argue against a pure zero, but the stock card argues against assuming full loss at 21-28 days, and the closest in-training Kennedy-pathway anchor, `Selenoi`, reached only a four-downstream-gene sterol module plus its self transcript.

I therefore forecast a very small but nonzero thalamic signature: a `Selenoi`-like lipid/sterol-feedback response with one marginal downstream call lost to the weaker and partially buffered upstream Pcyt2 lesion. Point prediction: 4 DEGs.
