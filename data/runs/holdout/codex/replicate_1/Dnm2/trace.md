# Dnm2 forecast for `151 TH Prkcd Grin2c Glut`

## Target biology

The held-out target is `Dnm2`. The declared biology bundle reports direct focal-population reach for the target transcript: in non-target cells from `151 TH Prkcd Grin2c Glut`, `Dnm2` was detected in 16,437 of 23,679 nuclei, or 69.4%, with mean raw UMI 1.33 and mean CP10k 0.846. Thus the target was broadly enough expressed for a single-cell CRISPR perturbation to reach the assayed thalamic glutamatergic population.

The functional-stock card calls DNM2 a dynamically renewed endocytic GTPase whose pre-edit protein should be substantially depleted over the P16 to P37-P44 interval: conditional postnatal hippocampal neurons lost 92.5% of DNM2 by DIV18, inside the 21-28 day experimental window. This argues against a long-lived protein-stock explanation for a total null.

The same bundle also gives a strong attenuation prior. DNM1 and DNM3 can buffer much of the tested neuronal dynamin requirement, and effective postnatal Dnm2 single loss left the assayed hippocampal synaptic-transmission measures intact. That evidence is not a matched thalamic snRNA phenotype, but it makes a large Dnm2-only transcriptional footprint less plausible than a quiet or very small one.

## Training measurements used

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 training targets. Its endpoint distribution is zero-heavy and long-tailed:

- median `n_degs`: 0
- mean `n_degs`: 14.05
- targets with `n_degs > 0`: 469 / 1,674
- 75th percentile: 1
- 90th percentile: 2
- 95th percentile: 18
- maximum: 2,677

I used the training count table to evaluate the closest available single-gene comparators from the Dnm2 mechanism. `Dnm1`, the direct classical-dynamin paralog present in the table, had `n_degs = 1`. Other measured training perturbations in the endocytic or synaptic-vesicle neighborhood were similarly small:

| training target | n_degs |
| --- | ---: |
| Dnm1 | 1 |
| Cltc | 3 |
| Bin1 | 1 |
| Synj1 | 1 |
| Syp | 1 |
| Syn1 | 1 |
| Syn2 | 0 |
| Stx1b | 0 |

These eight biologically chosen comparators have median 1, mean 1, and maximum 3 DEGs.

## Expression-profile check

To avoid relying only on names, I projected the observed `Dnm1` differential-expression profile from `training_de_all_cell_groups.parquet` in the exact focal context `group_name = "151 TH Prkcd Grin2c Glut"`, using all 1,674 count-table genes as the eligible training universe. The Dnm1 profile itself had one BH-significant feature, matching the count table.

The Dnm1 neighborhood over the expression Parquet was also quiet. Its 112-node nearest-neighbor union had median `n_degs = 0`, mean 2.277, 87 zero-count nodes, 104 nodes at `n_degs <= 1`, and 109 nodes at `n_degs <= 5`. The leading whole-profile Pearson/cosine neighbors were mostly zero-DEG examples:

| Dnm1 profile neighbor | n_degs |
| --- | ---: |
| Orc6 | 0 |
| Htr2a | 0 |
| Tcf12 | 0 |
| Tuba4a | 2 |
| Sh3kbp1 | 0 |
| Igsf8 | 1 |
| Smarcad1 | 0 |
| Ankfy1 | 0 |
| Flnb | 0 |
| Tgfbr3 | 0 |

## Forecast

`Dnm2` is not an inexpressed or unrealized lesion: the target transcript reaches a large fraction of focal nuclei, and DNM2 protein should clear before harvest. The decisive adjustment is functional buffering. A Dnm2-only edit is expected to remove one renewed endocytic GTPase while leaving overlapping DNM1/DNM3 capacity; in the matched training readout, the direct `Dnm1` comparator and nearby endocytic targets sit at 0-3 DEGs, and the exact Dnm1 expression-neighborhood is dominated by 0-1 DEG perturbations. I therefore expect a detectable but tiny survivor-state transcriptional response rather than a broad high-yield signature.

Predicted `n_degs`: **1**
