# Direct forecast trace

## Target and endpoint

- Target perturbation: `Mc4r`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: measured genes in that population with Wilcoxon BH-adjusted `p < 0.05`
- Point forecast: `0`

## Evidence used

The run-local holdout manifest names `Mc4r`, and the one-row biology bundle is outcome-blind: it exposes exact focal-population Mc4r reach plus biological stock/observability evidence, not the held-out DE count or held-out expression signature.

Exact in-assay reach was the strongest target-specific bearing. In non-target nuclei from `151 TH Prkcd Grin2c Glut`, `Mc4r` was detected in 80 of 23,679 nuclei, or 0.338%, with only 97 total Mc4r UMIs, mean raw expression 0.0041 UMI/cell, and pseudobulk 0.257 CPM. That argues that successfully editing `Mc4r` can only directly alter a very rare slice of the aggregate assayed class.

The canonical biology card supports functional realization but not a large endpoint magnitude. MC4R is a dynamic cell-surface melanocortin GPCR; stopping synthesis should substantially deplete functional receptor over the 21-28 day window, and adult focal neural deletion can have an in-window behavioral effect. The same card marks the matched evidence as partial: endogenous MC4R half-life in thalamic postmitotic neurons was not measured, the focal adult evidence was cortical rather than thalamic, and thalamic expression is low and nucleus-selective.

The focal training count table contained 1,674 non-held-out perturbations. Its empirical distribution was sparse and long-tailed: median `n_degs = 0`, 75th percentile `= 1`, 90th percentile `= 2`, and 469/1,674 perturbations were nonzero. The large arithmetic mean of 14.05 was driven by a small tail of broad RNA-processing, proteostasis, and chromatin perturbations, not by sparse receptor perturbations.

I therefore used a same-operation training cohort rather than the table-wide mean. In the declared Parquet restricted to `151 TH Prkcd Grin2c Glut`, these measured GPCR / receptor / cAMP perturbations had the following BH `< 0.05` DEG counts:

| cohort | targets in training table | focal `n_degs` |
| --- | --- | --- |
| melanocortin-family receptors | `Mc1r`, `Mc2r` | `0`, `0` |
| cAMP-associated GPCR or effector comparators | `Crhr1`, `Drd2`, `Drd4`, `Drd5`, `Mchr1`, `Npy1r`, `Npy2r`, `Npy5r`, `Oprd1`, `Oprk1`, `Oprl1`, `Oprm1`, `Sstr5`, `Adcy1`, `Adcy3`, `Adcy5` | all `0` |
| serotonin receptors | `Htr1a`, `Htr1b`, `Htr1f`, `Htr2a`, `Htr2b`, `Htr2c`, `Htr4`, `Htr6`, `Htr7` | all `0` |
| metabotropic glutamate GPCRs | `Grm1`, `Grm5`, `Grm6`, `Grm7`, `Grm8` | `1`, `0`, `0`, `1`, `0` |

The same-experiment Findings corpus was consistent with those counts rather than independent of them: packaged reports for `Adcy3`, `Crhr1`, `Drd2`, `Grm1`, `Grm7`, and several `Htr*` receptors summarize these basal GPCR/cAMP perturbations as flat, buffered, or uncoupled from the expected acute second-messenger / immediate-early transcriptional programs.

## Synthesis

`Mc4r` has a real, receptor-level loss-of-function prior over the assay window, so I did not treat it as an inactive edit. The point estimate nevertheless should sit at the floor: the exact target transcript is present in far below 1% of assayed non-target thalamic nuclei, the perturbation is a modulatory GPCR rather than a ubiquitous core process, and close training analogs in the same cell class almost always had zero corrected genes. The only nonzero receptor-side comparators above were one-gene, self-transcript-only mGluR calls, which are enough to leave uncertainty above zero but not enough to move the integer point away from the modal and median value.
