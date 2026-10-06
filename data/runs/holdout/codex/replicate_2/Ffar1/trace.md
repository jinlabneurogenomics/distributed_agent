# Direct Ffar1 `n_degs` forecast

Target and endpoint:

- Held-out target from `Ffar1.csv`: `Ffar1`.
- Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Prediction below used the declared biology-only `Ffar1.json`, the focal training count table, and direct aggregate queries of `training_de_all_cell_groups.parquet`. I did not use a relationship-review, branch-calibration, terminal-prediction, scalar-prior, calibrated-probability artifact, a target signature, or the held-out target count.

## Evidence used

### Biology bundle

The canonical `Ffar1` bundle identifies FFAR1/GPR40 as a plasma-membrane seven-transmembrane fatty-acid GPCR coupled mainly to Gq/calcium signaling. Its functional-stock adjudication calls the edited receptor stock likely substantially depleted by P37-P44 because P16 editing should stop new FFAR1 production and the 21-28 day post-edit interval is long relative to broad brain-protein turnover, even though existing receptor can traffic and recycle.

That says the perturbation can be realized in cells that depend on FFAR1; it does not put FFAR1 in the focal thalamic cells. The same bundle's exact focal measurement supersedes qualitative regional priors for this readout:

| quantity | value |
|---|---:|
| focal non-target nuclei | 23,679 |
| `Ffar1`-expressing focal nuclei | 0 |
| `pct_cells_expressing` | 0.0 |
| `total_target_umi` | 0.0 |
| `mean_raw_umi` | 0.0 |
| `pseudobulk_cpm` | 0.0 |

The positive neural prior is also spatially mismatched: the direct postnatal functional evidence in the bundle is adult hypothalamic/POMC-neuron knockdown, not thalamic `151 TH Prkcd Grin2c Glut`, and the Ffar4 note establishes only a ligand-overlapping family member without a matched thalamic compensation test.

### Training counts and Parquet checks

The focal count table has 1,674 training perturbations. Its response distribution is highly zero-inflated:

| statistic | value |
|---|---:|
| zero-DEG perturbations | 1,205 / 1,674 |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| mean | 14.05 |
| max | 2,677 |

Because `Ffar1` is a metabotropic GPCR with absent focal expression, I used the training receptor cohort rather than the essential-gene tail. The cohort was the 56 focal training targets with symbols matching metabotropic GPCR families present in the table: `Adgr*`, adrenergic receptors, `Ccr2`, `Cnr1`, `Cxcr4`, `Drd*`, `Gpr*` excluding `Gprasp2`, `Grm*`, non-`Htr3` `Htr*`, `Lpar6`, `Mc*r`, `Npy*r`, `Opr*`, `P2ry*`, `S1pr2`, `Sstr5`, and `Tacr3`.

Directly recomputing significant rows for those 56 genes from `training_de_all_cell_groups.parquet` in `151 TH Prkcd Grin2c Glut` gave:

| receptor cohort statistic | value |
|---|---:|
| targets | 56 |
| `n_degs = 0` | 49 |
| `n_degs = 1` | 7 |
| `n_degs > 1` | 0 |
| mean `n_degs` | 0.125 |
| median `n_degs` | 0 |
| total significant downstream, excluding self-target rows | 1 |

The seven significant receptor cases were all singletons. Six were only the receptor's own transcript (`Adgrl1`, `Adgrl2`, `Adgrl3`, `Gpr158`, `Grm1`, `Grm7`), and the only non-self event was `Cnr1 -> Srcap`.

## Synthesis

Two directions of evidence point to a zero count. First, exact non-target expression places `Ffar1` below the observed focal detection limit across 23,679 matched thalamic nuclei, so a postnatal CRISPR lesion should have little cell-autonomous receptor biology to remove in this assayed class. Second, when the same endpoint is measured for focal training metabotropic GPCR perturbations, the distribution is already centered at zero and any apparent response is usually just the receptor self-transcript if that receptor is detectably expressed.

The main counterweight is that FFAR1 loss is not intrinsically inert: the card supports GPCR operation, multi-week receptor-stock decline, and postnatal hypothalamic neuronal phenotypes. I downweighted that evidence because it is not thalamic, the exact focal assay saw no `Ffar1` RNA, and no matched thalamic FFAR1/Ffar4 compensation or latent developmental effect was available. Indirect or rare early effects could in principle create a singleton, but at BH FDR 0.05 the receptor training cohort makes that less likely than no significant measured gene.

Point forecast: `Ffar1 n_degs = 0`.
