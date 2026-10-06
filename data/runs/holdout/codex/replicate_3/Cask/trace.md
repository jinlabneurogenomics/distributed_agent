# Cask DEG-count forecast

Endpoint: `n_degs` is the number of measured genes with BH-adjusted Wilcoxon
`pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut`.

## Declared target biology

- The held-out perturbation is `Cask`.
- In the exact non-target focal population, `Cask` is detectable rather than a
  rare feature: 14,967 of 23,679 nuclei express it, `pct_cells_expressing =
  63.2079`, `mean_cp10k = 0.7225`, and `pseudobulk_cpm = 72.7711`.
- The biology-only bundle adjudicates the CASK functional stock as
  `likely_substantially_depleted` by the P37-P44 harvest. The main support is
  that CASK is a renewable multidomain MAGUK scaffold, has target-specific
  neuronal turnover on a roughly six-day scale in culture, turns over in adult
  mouse brain, and can become immunoblot-undetectable four days after Cre
  deletion in mouse neural culture.
- The same bundle supports a postnatal neuronal consequence, but the strongest
  mouse evidence is cortical or pan-neuronal rather than an acute P16 thalamic
  perturbation. That makes the loss biologically plausible while leaving the
  recovered-nucleus transcriptional endpoint uncertain.

## Declared training measurements

The declared focal count table contains 1,674 training perturbations. The
distribution is extremely zero-inflated:

- 1,205/1,674 have `n_degs = 0`;
- 1,512/1,674 have `n_degs <= 2`;
- 1,571/1,674 have `n_degs <= 10`;
- the median is 0 and the mean is 14.05 because a small tail reaches hundreds to
  thousands of DEGs.

I used CASK's molecular role to restrict quantitative transfer to synaptic
scaffold, neurexin/neuroligin, NMDA/calcium-channel, and synaptic-vesicle
perturbations observed in the same table. Their focal counts were:

| target | n_degs |
| --- | ---: |
| `Nrxn1` | 1 |
| `Nrxn2` | 0 |
| `Nrxn3` | 0 |
| `Nlgn3` | 1 |
| `Dlg4` | 1 |
| `Dlgap4` | 2 |
| `Shank2` | 0 |
| `Shank3` | 2 |
| `Homer2` | 0 |
| `Cacna1a` | 0 |
| `Cacnb4` | 1 |
| `Grin1` | 89 |
| `Grin2b` | 2 |
| `Camk2a` | 0 |
| `Camk2b` | 1 |
| `Stxbp1` | 1 |
| `Syngap1` | 0 |
| `Bsn` | 0 |
| `Pclo` | 0 |
| `Syp` | 1 |
| `Syn1` | 1 |
| `Syn2` | 0 |
| `Unc13a` | 0 |
| `Unc13b` | 0 |
| `Unc13c` | 0 |
| `Cntnap1` | 1 |
| `Cntnap2` | 1 |

This cohort has median `n_degs = 1`; excluding the receptor-core outlier
`Grin1`, the 26 remaining counts sum to only 16.

## Focal Parquet checks

A direct scan of the declared expression parquet for these 27 training targets
in `151 TH Prkcd Grin2c Glut` showed that most one-DEG analogs were self-only.
`Dlg4`, `Nrxn1`, `Nlgn3`, `Cacnb4`, `Camk2b`, `Stxbp1`, `Syn1`, `Syp`,
`Cntnap1`, and `Cntnap2` had exactly one significant feature and in each case it
was the perturbed transcript itself. Outside `Grin1`, only `Dlgap4`, `Grin2b`,
and `Shank3` had a single significant trans gene among the queried CASK-axis
training perturbations.

Symmetric profile comparison of the same 27 targets found 13 targets with no
significant features, 13 with one to nine significant features, and only
`Grin1` with at least 50. Pairwise inspection around the closest MAGUK/neurexin
nodes found no overlap of significant features between `Dlg4` or `Dlgap4` and
the NMDA/channel peers, consistent with weak isolated self or one-gene effects
rather than a recurrent broad thalamic program.

## Synthesis

The CASK card makes complete biological non-realization unlikely: the target is
expressed in the focal population and the protein stock should turn over within
the 21-28 day assay window. I therefore did not push the estimate all the way to
a confident zero.

However, the same-experiment training set says that CASK's nearest assayed
synaptic-scaffold and adhesion partners are usually transcriptionally quiet in
this thalamic class. The few nonzero analogs are generally explained by
self-transcript detection, and the only broad exception, `Grin1`, is a direct
obligate NMDAR subunit with a much more proximal receptor-loss operation than
CASK scaffold loss. The point forecast is therefore a detectable but minimal
signature:

`predicted_n_degs = 1`
