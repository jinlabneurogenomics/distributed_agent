# Direct outcome-blind forecast for Tmem63a

Target and endpoint: `Tmem63a` in `151 TH Prkcd Grin2c Glut`; predict the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.

## Declared target biology used

The declared target bundle makes `Tmem63a` a plausible neural perturbation but a weak match to this exact endpoint.

- The exact focal-population reach is low but nonzero: 2,257 of 23,679 non-target nuclei in `151 TH Prkcd Grin2c Glut` express `Tmem63a` (`9.53%`, mean raw UMI `0.109`, pseudobulk `6.85` CPM).
- TMEM63A is a mechanically activated cation channel in plasma and organellar membranes.
- The best mouse CNS phenotypes are developmental oligodendrocyte/myelination phenotypes; postnatal brain protein is reported as concentrated in oligodendrocytes and almost absent from NeuN-positive neurons. That argues for strong dilution or lack of coupling in the recovered thalamic neuronal nuclei requested here.
- The functional-stock card is indeterminate for a P16 edit harvested at P37-P44: editing stops new channel supply, but existing membrane channel can initially persist, and no basal neural TMEM63A half-life was found.
- `Tmem63b` and `Tmem63c` are the declared paralogs; no matched brain-cell compensation test was available.

## Training measurements used

I used the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` and the declared training Parquet only for non-target training perturbations. `Tmem63a` is absent from the count table.

The count table is highly zero-inflated in this focal class:

- 1,674 training perturbations
- 1,205 with `n_degs = 0`
- 276 with `n_degs = 1`
- median `0`, 75th percentile `1`, 90th percentile `2`

The closest family perturbations were directly represented and quiet:

| target | 151-class `n_degs` | interpretation |
| --- | ---: | --- |
| `Tmem63b` | 1 | the single FDR<0.05 Parquet row in this class was `Tmem63b` itself (`logFC = -0.701`, `p_adj = 4.16e-17`); no downstream gene passed the threshold |
| `Tmem63c` | 0 | no FDR<0.05 rows in this class |

The same-experiment corpus reports for these two represented paralogs also treated them as buffered or null-like neuronal perturbations: `Tmem63c` had no downstream FDR<0.10 genes across all matched neuronal groups, and `Tmem63b` had only two singleton downstream genes across 22 recovered groups. The explicit cross-paralog finding concluded that `Tmem63b` and `Tmem63c` did not form an interchangeable TMEM63-family nuclear-RNA response in the postnatal neuronal assay; importantly, those reports did not include `Tmem63a` itself.

I also checked an observed-profile neighborhood for `Tmem63b` and `Tmem63c` against all 1,674 eligible training perturbations in the same cell group using signed Wilcoxon scores. It did not reveal a coherent non-null TMEM63-centered module: `Tmem63b` had only 1 significant feature and top whole-profile Pearson/cosine neighbors near `0.06`; `Tmem63c` had 0 significant features and top whole-profile neighbors near `0.14`.

Several broad channel perturbations in the same count table were likewise at `0` or `1` FDR<0.05 genes in this class (`Cacna1a`, `Cacna1d`, `Cacna1e`, `Kcnb1`, `Kcnb2`, `Kcnma1`, `Scn1a`, `Scn2a`, `Tmem63b`, `Tmem63c`), so the measured family/channel neighborhood did not supply a positive magnitude anchor.

## Synthesis

There is credible long-horizon CNS biology for `Tmem63a`, but the source of that biology is oligodendrocyte myelination rather than the assayed NeuN-positive thalamic neurons. Within the requested focal population, `Tmem63a` is sparsely expressed, the P16-to-P37/P44 knockout may leave some pre-existing channel stock, and the closest observed paralog perturbations are transcriptionally silent downstream of self-knockdown. Given the zero-inflated class-wide training distribution, I put the point forecast at the modal quiet state rather than at the one-gene shoulder.

Predicted `n_degs`: **0**
