# Hdac4 n_degs direct forecast

## Endpoint and allowed measurements

- Target: `Hdac4` from the one-row holdout manifest.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, counted as measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- I used the declared thalamic training count table, the matching all-cell training Parquet for observed comparator profiles, and the prediction-safe `Hdac4` biology bundle. I did not use a held-out `Hdac4` DE signature or target DEG count.

## Biology bearing

The canonical bundle resolves the `Hdac4` packet by supplied IDs to the official mouse `Hdac5` target rather than to official mouse `Hdac4`. The target transcript is well reached in the assayed focal population: the exact non-target measurement reports 18,962 / 23,679 nuclei expressing the `Hdac4` feature, 80.08% expressing, mean log1p(CP10k) 0.691, and mean CP10k 1.208 in `151 TH Prkcd Grin2c Glut`.

That expression makes technical absence of target RNA unlikely, but the functional prior is damped. The operative product is an activity-regulated class IIa HDAC corepressor component in SMRT/N-CoR-HDAC3 assemblies; a P16 disruptive edit stops new supply but does not instantly remove pre-existing protein. The bundle found no endogenous HDAC5 protein half-life or multi-week thalamic-neuron complex-residence anchor, and forebrain genetics supports HDAC4/HDAC5 functional buffering. Altogether, the card supports possible activity-dependent transcriptional impact but not a confidently realized large 21-28 day thalamic survivor-RNA state.

## Training count scale

The declared `151 TH Prkcd Grin2c Glut` training table contains 1,674 observed targets. Its distribution is sharply zero-inflated:

- 1,205 / 1,674 targets have `n_degs = 0`.
- 1,546 / 1,674 have `n_degs <= 5`.
- median = 0, 75th percentile = 1, 90th percentile = 2, 95th percentile = 18.
- Only 43 / 1,674 reach `n_degs >= 100`.

Mechanistically close, observed rows sit at the floor. `Hdac5`, `Hdac8`, `Ep300`, `Kat6a`, `Kat6b`, and `Mef2d` all have 0 DEGs in the count table; `Mef2c` and `Smarca2` have 1, `Mef2a` has 4, `Crebbp` has 8, `Creb1` has 10, and `Smarce1` has 11. This is the neighborhood I treated as scale-informative for a class IIa HDAC/corepressor perturbation. I did not transfer the much larger counts of less similar broad chromatin or core gene-expression regulators, such as `Sin3a` at 1,433, `Brd4` at 311, or `Smarcc2` at 185, because those are different complexes and their strong burdens mainly bound what this high-yield population can detect.

The Parquet check of `Hdac5` itself was also quiet in the focal group: 0 significant genes among 17,259 measured genes, 333 raw `p < 0.05` genes, and the smallest adjusted p-value was 0.273 on the target feature. The bounded profile-neighborhood artifact for `Hdac5`, `Hdac8`, `Ep300`, and `Mef2d` likewise kept all four anchors in the no-significant-feature state and did not expose a recurrent high-burden HDAC-like module that would justify moving away from the zero class.

## Synthesis

High expression argues against treating `Hdac4` as an unexpressed target, but the closest assay-matched perturbations and the HDAC5/HDAC4 buffering prior both point to a silent or near-silent recovered-cell transcriptome. Because the target biology does not supply an acute thalamic loss result, I left some chance on a small nonzero count, but the modal and best-supported integer is the same floor value as the observed `Hdac5`/`Hdac8`/`Ep300`/`Kat6a`/`Kat6b`/`Mef2d` comparators.

Predicted `n_degs`: 0
