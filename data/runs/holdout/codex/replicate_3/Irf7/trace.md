# Irf7 direct DEG-count prediction

## Target and endpoint

- Target in the one-row holdout manifest: `Irf7`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: count of measured genes in that focal population with Wilcoxon `pvals_adj < 0.05`.
- Declared count-table support: the focal training table contains 1,674 non-Irf7 training targets and omits the target outcome.

## Evidence used

### In-assay Irf7 reach

The canonical Irf7 biology bundle reports exact baseline focal-population reach for `Irf7` in non-target cells:

- `n_non_target_cells`: 23,679
- `n_cells_expressing`: 762
- `pct_cells_expressing`: 3.2180413024198655
- `mean_cp10k`: 0.03211120884329289
- `mean_raw_umi`: 0.04784830440474682
- `pseudobulk_cpm`: 2.998822913040856

Thus the target is measurable but very low and sparse at baseline in the assayed thalamic glutamatergic population.

### Biology prior

The same canonical bundle characterizes IRF7 as a short-lived, inducible transcription factor for type-I interferon amplification. A successful disruptive edit should deplete functional IRF7 by the P37-P44 harvest in cells that rely on new IRF7 synthesis, but the strongest mouse phenotypes and the CNS induction evidence are viral/TLR challenge contexts. The bundle explicitly notes low uninfected thalamic/CNS expression and inducibility during viral encephalitis rather than broad homeostatic expression in healthy thalamic neurons.

### Training endpoint distribution

The declared `151 TH Prkcd Grin2c Glut` training count table is highly concentrated at zero:

- 1,205 / 1,674 targets have `n_degs = 0`.
- 276 / 1,674 targets have `n_degs = 1`.
- 1,546 / 1,674 targets have `n_degs <= 5`.
- The median is 0, the 90th percentile is 2, and the 95th percentile is 18.

Large counts in this class are a small tail dominated by broadly essential regulators such as `Uba5`, `Tpr`, `Sin3a`, spliceosome factors, proteasome factors, and related core machinery genes; `Irf7` is not a close biological match to that high-yield tail under an uninfected neuronal readout.

### Same-pathway training perturbations

I treated the interferon/IRF and proximal innate-immune signaling genes in the training table as the most relevant measured comparators. Their focal counts are almost uniformly null:

| training target | focal `n_degs` |
|---|---:|
| `Irf1` | 0 |
| `Irf2` | 0 |
| `Irf3` | 0 |
| `Irf5` | 0 |
| `Irf8` | 0 |
| `Irf9` | 0 |
| `Ifih1` | 0 |
| `Ifnar1` | 0 |
| `Ifnar2` | 0 |
| `Ifngr1` | 0 |
| `Ifngr2` | 0 |
| `Nfkb1` | 0 |
| `Stat1` | 1 |
| `Stat2` | 0 |
| `Stat3` | 0 |
| `Tlr3` | 0 |
| `Tlr7` | 0 |
| `Traf3` | 0 |

I checked the corresponding rows in the declared expression Parquet for the exact focal population. Each of these perturbations had 17,259 tested features. All were BH-null except `Stat1`, where the lone adjusted-significant feature was the `Stat1` self row (`q = 0.0270288`); no comparator showed a broad induced antiviral/interferon survivor-state signature.

## Synthesis

The decisive downward evidence is the combination of sparse baseline `Irf7` reach in the focal neurons and the empirical quietness of the measured IRF/interferon signaling perturbations in the same high-yield thalamic class. The functional-stock card says CRISPR should be able to remove IRF7 capacity in edited cells by harvest, so I did not treat existing protein persistence as protective. The limiting issue is instead endpoint coupling: this assay samples unchallenged survivor-conditioned neuronal nuclei, whereas IRF7's established neural effects are induced during viral interferon states.

A tiny count from rare Irf7-expressing neurons or residual AAV/innate-immune stimulation is possible, but the closest measured training genes center at zero with only a single self-transcript `Stat1` event among the selected pathway comparators. I therefore place the integer point forecast at the null mode.

Predicted `n_degs`: 0
