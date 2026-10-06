# Trip12 direct `n_degs` forecast

## Endpoint and visible measurements

- **Target and population:** `Trip12` in `151 TH Prkcd Grin2c Glut`.
- **Endpoint:** number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- **Training outcome table:** the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` contained 1,674 visible perturbations; `Trip12` was not in this table.
- **Training distribution in this class:** 1,205 / 1,674 visible perturbations had `n_degs = 0`; the median was 0, the 75th percentile was 1, the 90th percentile was 2, and the 95th percentile was 18. The mean was inflated to 14.1 by a few global-machinery outliers such as `Uba5` at 2,677 and `Psmb4` at 742.

## Trip12 biology bundle

- The exact focal-population reach for `Trip12` was high: `Trip12` was detected in 23,379 / 23,679 non-target nuclei, with 98.733% cells expressing, mean raw UMI 6.249, and pseudobulk CPM 391.65.
- The functional-stock adjudication concluded that functional TRIP12 protein is likely substantially depleted by harvest. The 21-28 day P16-to-P37/P44 interval spans many measured neuronal TRIP12 protein half-lives, so successfully edited neurons should have little pre-edit ligase left.
- The operative biology is a substrate-selective HECT E3 ubiquitin ligase in ubiquitin-fusion degradation, with biochemical evidence that TRIP12 ubiquitinates GCase and mouse-neural evidence that partial knockdown can change GCase and disease-model phenotypes over a much longer six-month substantia-nigra challenge.
- The same bundle also argues for caution: no healthy acute postnatal mouse thalamic neuron loss experiment was found, TRIP12 loss can be buffered for some ubiquitin-fusion substrates by HUWE1 or other E3 activity, and direct GCase/protein stabilization need not create a large nuclear RNA response by 3-4 weeks.

## Training perturbations used

I used the declared Parquet only in the focal class to inspect exact signed burdens for visible proteostasis and E3-adjacent comparators:

| comparator | role in this forecast | focal `n_degs` |
| --- | --- | ---: |
| `Huwe1` | HECT E3 and documented parallel UFD ligase; broad direct-operation upper analogue | 158 |
| `Marchf6` | substrate-selective membrane E3 with a small sterol-program response | 14 |
| `Usp48` | deubiquitinase with a small focal response | 10 |
| `Stub1` | E3/chaperone-ligase boundary case; self-only response | 1 |
| `Ube3a`, `Ubr1`, `Herc1`, `Herc2` | E3 boundary cases that were measured and quiet | 0 |
| `Vps35`, `Vps54` | proteostasis/trafficking perturbations with small responses | 17, 31 |
| `Rab7`, `Psmb4`, `Psmc1`, `Ufc1`, `Uba5` | vesicle core, proteasome, or UFMylation-core disruptions used only as non-Trip12 upper-scale references | 501, 742, 430, 572, 2,677 |

The Parquet signs reinforced the scale distinction: `Huwe1` had a real bidirectional focal signature, 90 up and 68 down; `Marchf6` and `Usp48` were small and mostly up, at 13/1 and 9/1; the quiet E3s had no significant genes or only the targeted transcript.

## Synthesis

`Trip12` is unlikely to behave like the median visible perturbation because it is expressed in nearly all focal nuclei and its catalytic protein stock should turn over well inside the experimental window. I therefore did not assign a strict zero or self-only count. At the same time, its known operation is a substrate-selective ubiquitination route, not a proteasome-core, Rab7, or UFMylation-core lesion, and the direct postnatal neural evidence comes from a disease-challenged dopaminergic system rather than this healthy thalamic glutamatergic class.

The most informative scale was therefore below `Huwe1` and far below global proteostasis machinery, but slightly above the near-null E3 boundary set because `Trip12` has high exact reach and strong turnover. I placed it at the high end of the small E3/proteostasis group, near the 95th percentile of all visible training perturbations.

**Predicted `n_degs`: 18**
