# Kmt2d forecast for `151 TH Prkcd Grin2c Glut`

## Target

The one-row holdout manifest names `Kmt2d`. The requested endpoint is the number of measured genes in `151 TH Prkcd Grin2c Glut` with Wilcoxon BH-adjusted `pvals_adj < 0.05`.

## Biology used

The declared Kmt2d biology bundle says that KMT2D is an enhancer-associated H3K4 mono-/dimethyltransferase COMPASS scaffold, with Kmt2c providing partial but incomplete paralog buffering. In the focal non-target nuclei, `Kmt2d` was directly detected in 20,842 of 23,679 cells, 88.0189%, with mean raw UMI 2.532 and pseudobulk 158.71 CPM, so target RNA reach should not be the limiting uncertainty in this class.

The same bundle adjudicates the functional stock as `likely_substantially_depleted` by the P37-P44 harvest: a P16 disruptive edit stops new KMT2D synthesis; an adult mouse hippocampal RNAi experiment had lower Kmt2d RNA and a supplied H3K4 mark by four weeks; neuronal H3.3 carrier turnover continues over a similar interval. The evidence is partial because the direct neural timing anchor is hippocampal RNAi rather than P16 thalamic editing, and persistent pre-edit chromatin plus Kmt2c redundancy can dampen the short-window effect.

## Training measurements used

The focal count table contains 1,674 training targets and excludes `Kmt2d`. It is highly zero-inflated: 1,205 targets had 0 significant genes, the median was 0, the 75th percentile was 1, the 95th percentile was 18, and the maximum was 2,677.

Typed analog nomination against that same training universe put the H3K4/COMPASS-adjacent genes first. Their measured 151-class counts were:

| training target | relationship used | n_degs |
|---|---:|---:|
| Kmt2c | close paralog / projected KMT2D complex / H3K4 methyltransferase | 0 |
| Kmt2a | projected KMT2D complex / H3K4 methyltransferase | 24 |
| Setd1a | projected KMT2D complex / H3K4 methyltransferase | 368 |
| Ash1l | H3K4 methyltransferase annotation | 1 |
| Pitx2 | projected PITX2-MLL4-ASH2L-RBBP5-PTIP complex | 0 |
| Ogt | projected MLL2 complex | 4 |

The declared Parquet confirmed that those rows came from the same matched focal contrast. The five most specific nominees spanned 0, 24, 368, 1, and 0 significant genes. Adding nearby chromatin regulators preserved the same qualitative picture: some broad chromatin perturbations were large, for example `Brd4` at 311 and `Sin3a` at 1,433, but many specific enhancer/H3K4 or coactivator comparators were null or weak, including `Kmt2c` 0, `Pitx2` 0, `Ep300` 0, `Ash1l` 1, `Ogt` 4, and `Crebbp` 8.

Profile comparison on the focal Parquet did not reveal a shared high-count H3K4 program to transfer. `Setd1a`, the only high H3K4-count analog, had 368 DEGs but a predominantly negative program and little significant-gene overlap with the lower-count comparators, so I treated it as an upper boundary rather than the central forecast. `Kmt2c` is biologically the closest available paralog and was transcriptionally silent in this endpoint, but it had only 55 matched perturbed nuclei, leaving a null boundary rather than a decisive Kmt2d null prediction.

## Synthesis

Kmt2d has stronger focal expression and a stronger short-window functional-stock prior than a generic silent target, so I lifted the forecast above the 0-4 range suggested by `Kmt2c`, `Pitx2`, `Ash1l`, and `Ogt`. The closest non-null methyltransferase measurement, `Kmt2a` at 24 DEGs, and the low double-digit chromatin measurements around `Crebbp`, `Nsd1`, `Setdb1`, and `Arid1a` looked more plausible than the `Setd1a`/`Brd4` high tail because KMT2D loss is partly buffered by Kmt2c and by pre-existing enhancer marks over this 21-28 day window.

I therefore forecast a low but nonzero focal response: **18 DEGs**.
