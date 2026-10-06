# Ank3 prediction for `151 TH Prkcd Grin2c Glut`

## Point prediction

`predicted_n_degs = 1`

## Evidence used

- **Declared target and endpoint.** The one-row holdout manifest names `Ank3`; the endpoint is the number of focal `151 TH Prkcd Grin2c Glut` measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05`.
- **Focal expression reach.** The canonical biology bundle reports exact non-target expression for `Ank3` in the focal class: mean raw UMI 11.317, mean CP10K 7.128, and 23,624 / 23,679 non-target nuclei expressing `Ank3` (99.77%). This makes the locus available in the assayed thalamic population, while the bundle explicitly notes that expression reach does not prove editing efficiency or functional dependence.
- **Functional-stock prior.** The same bundle adjudicates Ank3 as an installed AIS/nodal membrane-domain scaffold. A P16 CRISPR loss stops new ankyrin-G supply but does not directly remove pre-existing scaffold; the 16.6-day mouse cortex protein lifetime and nodal persistence data imply substantial but incomplete depletion during the 21-28 day edit-to-harvest window. The bundle conclusion is therefore `partially_depleted_or_leading_edge`, not near-complete acute loss.
- **Training-set scale.** In the 1,674-row held-in focal count table, 1,205 targets were 0, the median was 0, the 75th percentile was 1, the 90th percentile was 2, and the 95th percentile was 18. Broad DEG footprints were rare and concentrated in general nuclear/proteostasis targets rather than in local membrane-scaffold genes.
- **Biologically nearest held-in perturbations.** The nearest assay-matched structural and excitability comparators were essentially silent in the focal class:

| target | focal `n_degs` |
| --- | ---: |
| `Ank1` | 0 |
| `Ank2` | 0 |
| `Add1` | 0 |
| `Add2` | 0 |
| `Add3` | 0 |
| `Sptb` | 0 |
| `Cacna1a` | 0 |
| `Kcnq1` | 0 |
| `Scn3a` | 0 |
| `Kcnq2` | 1 |
| `Kcnq3` | 1 |
| `Scn1a` | 1 |
| `Scn2a` | 1 |
| `Scn8a` | 1 |
| `Sptan1` | 1 |
| `Cntnap1` | 1 |
| `Cntnap2` | 1 |
| `Nrcam` | 2 |
| `Scn1b` | 2 |

For the exact Parquet rows checked in `151 TH Prkcd Grin2c Glut`, `Ank1`, `Ank2`, `Sptb`, `Cacna1a`, `Kcnq1`, and `Scn3a` had no FDR<0.05 genes; the singleton calls for `Kcnq2`, `Kcnq3`, `Scn1a`, `Scn2a`, `Scn8a`, `Sptan1`, `Cntnap1`, and `Cntnap2` were the perturbed transcript itself; and only `Nrcam` and `Scn1b` contributed one downstream feature each. Thus the immediate ankyrin / spectrin / AIS / nodal-channel neighborhood averaged less than one focal DEG and almost no downstream DE.
- **Packaged same-experiment interpretation.** The held-in `Ank2:F004` Finding independently summarized the same pattern: sodium-channel and KCNQ perturbations often showed target engagement but little downstream RNA output, paralleling an `Ank2` null and arguing that AIS or excitability biology is weakly coupled to broad postmitotic snRNA-seq rewiring in this experiment.

## Synthesis

The upward evidence is that `Ank3` is expressed in nearly all focal non-target nuclei and has established postnatal neuronal AIS / nodal maintenance biology. The downward evidence is stronger for this scalar endpoint: loss has to work through slow turnover of an already installed scaffold, thalamic AIS/nodal phenotypes need not become nuclear RNA changes by P37-P44, partial Ank1 buffering is possible at nodes, and the directly comparable held-in ankyrin, spectrin, adhesion, sodium-channel, and KCNQ perturbations occupy the 0-2 DEG floor with their few significant calls mostly being self-transcripts.

I therefore expect `Ank3` to be nonzero only if the self-transcript or one isolated downstream feature crosses BH FDR, and I set the point estimate to **1 DEG**.
