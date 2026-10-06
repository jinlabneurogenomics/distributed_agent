# Sp4 n_degs forecast

## Target and endpoint

- Target: `Sp4`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Point forecast: `10`

## Evidence used

1. The declared one-row manifest names `Sp4` as the held-out target. The declared target bundle is a biology-only `Sp4` bundle and reports `target_outcome_exposed=false`; it provided the focal-population reach and functional-stock interpretation but no held-out differential-expression signature.

2. Exact focal expression supports perturbability but not saturation. In matched non-target nuclei from `151 TH Prkcd Grin2c Glut`, `Sp4` was detected in 12,209 of 23,679 nuclei, or 51.56%, with mean CP10K 0.510. That makes a recovered transcriptional response plausible in roughly half of the focal population, while still leaving a large non-expressing fraction to dilute an aggregate snRNA-seq contrast.

3. The biological prior is non-null. SP4 is a nuclear GC/GT-box-binding transcription factor; the bundle adjudicates it as a free, continuously renewed protein whose functional stock should be substantially depleted within the 21-28 day P16-to-P37/P44 edit window. Germline null and lifelong neural hypomorph mouse evidence support neural relevance despite Sp-family paralogs, but that evidence is developmental or hippocampal rather than an inducible postnatal thalamic loss test.

4. The visible `151 TH Prkcd Grin2c Glut` training count table is sparse overall: among 1,674 training perturbations, 1,205 have zero DEGs, the median and Q75 are 0 and 1, Q90 is 2, Q95 is 18, and only 106 targets reach at least 10 DEGs. The mean is 14.05 because of a long high-response tail led by broad essential and chromatin/RNA-processing regulators.

5. Visible transcription-factor comparators in the same cell group were mostly weak:

   | comparator | `n_degs` |
   | --- | ---: |
   | `Klf9` | 19 |
   | `Creb1` | 10 |
   | `Zfp148` | 8 |
   | `Mef2a` | 4 |
   | `Klf7` | 1 |
   | `Mef2c` | 1 |
   | `Sox2` | 2 |
   | `Sox5` | 2 |
   | `Klf1`, `Klf11`, `Klf12`, `Klf13`, `Jund`, `Sp7`, `Satb2`, `Sox4`, `Tcf4` | 0 each |

   Across a broader hand-curated set of 76 visible C2H2 zinc-finger, KLF, CREB, MEF2, POU, SOX, TCF, Zic, and immediate-early transcription-factor perturbations, 60 were zero and the mean was 5.37 DEGs; the mean is inflated by a few outliers such as `Zfp423` and `Zmynd8`.

6. The same-experiment Klf9 corpus report is useful as a semantic boundary, not as an independent replicate. `Klf9` had a restricted 151-dominated basal response and represented KLF paralogs did not phenocopy one another, arguing against transferring a generic KLF-family magnitude to `Sp4`. In the raw training Parquet, `Klf9` had 19 DEGs in `151` and only one significant gene outside it, `Creb1` had 10 in `151` and four one-to-three-gene responses elsewhere, `Mef2a` had 4 in `151`, and `Mef2c` had 1 in `151`.

## Synthesis

`Sp4` should not be forecast as a null: the target is actually expressed in the assayed thalamic population, encodes a short-lived DNA-binding regulator, and has mouse neural loss-of-function evidence that makes residual functional stock unlikely to hide a successful P16 edit. The exact reach of 51.56% and possible compensation by related GC-box factors argue against a large broad-regulator footprint, and the visible related TFs show that postnatal thalamic transcription-factor knockouts often remain very small even in the highest-yield cell group.

I therefore placed `Sp4` near the high end of the sparse TF band, aligned with `Creb1` and below the more clearly observed `Klf9` restricted response. The selected integer is `10`.
