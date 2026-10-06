# Sim1 direct n_degs forecast

Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, defined as the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

## Declared target and assay reach

- The one-row manifest target is `Sim1`.
- I used the canonical `Sim1` biology-only bundle with checksum `0387014d72fb21fcfe3792493512c3703feaebb20756c0812e8dc5b68c3bebfb`. It exposes biological priors and exact focal-population expression reach, not the held-out target signature or the held-out `n_degs`.
- In the focal non-target thalamic population, `Sim1` is essentially absent: `mean_cp10k = 0.000646330638249604`, `pseudobulk_cpm = 0.058229571127006906`, `n_cells_expressing = 16` of `23,679`, and `total_target_umi = 22`.

## Biology interpreted for this endpoint

The perturbation should clear functional SIM1 in a cell that actually depends on it: SIM1 is a dynamic nuclear bHLH-PAS transcription-factor component, adult neuronal `Sim1` deletion changes hypothalamic transcription and physiology within one to two weeks, and the 21-28 day CRISPR window should be long enough for functional depletion.

The limiting fact is anatomical and quantitative reach. The supportive loss-of-function evidence is hypothalamic/PVN, while the requested population is thalamic `151 TH Prkcd Grin2c Glut`. Adult mouse `Sim1` expression is reported as concentrated in hypothalamic neuroendocrine nuclei and amygdala, not broadly in thalamus, and the bundle's exact in-assay thalamic measurement finds only 0.0676% of non-target nuclei expressing `Sim1`. That makes a population-level Wilcoxon response in this aggregated thalamic class unlikely even if rare `Sim1`-positive cells were fully edited.

## Training measurements used

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` has 1,674 training perturbations and is strongly concentrated at zero:

| training count bin | targets |
| --- | ---: |
| `0` | 1,205 |
| `1` | 276 |
| `2-5` | 65 |
| `6-20` | 50 |
| `21-100` | 36 |
| `101-500` | 27 |
| `>=501` | 15 |

The median is `0`, the 75th percentile is `1`, the 90th percentile is `2`, and 88.5% of training targets have at most one DEG in this class.

I also nominated training-available analogs from deterministic annotations over the declared training universe. `Arnt` is the only close exact-complex nominee for `Sim1`: it is in the native mouse CORUM `Arnt-Sim1 complex` and has a pinned STRING physical interaction to SIM1. Its observed count in this focal class is `0`. Broader bHLH-PAS / ARNT-axis comparators are also flat in the count table: `Ahr = 0`, `Hif1a = 0`, `Npas3 = 0`, `Bmal2 = 0`, with `Clock = 3`. The main higher bHLH-PAS value, `Bmal1 = 103`, represents a detectable CLOCK/BMAL1 circadian-output branch rather than a basal SIM1/ARNT-like state.

The selected same-experiment corpus report for `Arnt` is concordant with these counts: it records `Arnt` as pan-neuronally FDR-null, reports no recovered canonical AHR or HIF target programs after `Arnt` perturbation, and explicitly separates the flat ARNT/AHR/HIF/NPAS3/AHRR-related branch from the detectable CLOCK/BMAL1 circadian branch.

## Forecast

The strongest target-specific upward bearing is that `Sim1` encodes a transcription factor whose function can be lost within the assay window. I discounted that for the focal endpoint because expression and prior biology put SIM1 outside almost all assayed thalamic nuclei, and the only exact-complex training comparator has no DEGs under the same basal neuronal conditions.

Given the zero-heavy training distribution, the near-absent focal expression of `Sim1`, and the flat `Arnt`/AHR/HIF analog measurements, the point prediction is the floor:

`predicted_n_degs = 0`
