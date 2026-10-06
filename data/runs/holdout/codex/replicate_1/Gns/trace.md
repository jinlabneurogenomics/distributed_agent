# Gns in 151 TH Prkcd Grin2c Glut

## Prediction

`predicted_n_degs = 1`.

## Evidence used

- The declared holdout manifest contains one target, `Gns`; the training count table contains 1,674 other perturbations for `151 TH Prkcd Grin2c Glut`, and the declared DE parquet omits the `Gns` perturbation profile. I did not query a `gene_target = 'Gns'` endpoint row.
- The in-assay target-expression bundle reports that `Gns` is present in the focal non-target cells: 18,103/23,679 nuclei express it, `pct_cells_expressing = 76.45%`, `mean_cp10k = 1.064`, and `pseudobulk_cpm = 108.44`. The same bundle marks the operative stock as soluble lysosomal GNS activity and concludes that it is likely substantially depleted by P37-P44 because the closest mouse-brain clock gives recombinant GNS activity a ~1.1 day half-life. That supports target reach by harvest, but the card also notes that congenital neuropathology was first assessed later, at 12 weeks, so it does not prove a 3-4 week neuronal RNA program.
- The 151 TH training endpoint is very sparse: 1,205/1,674 targets have zero DEGs, 276 have exactly one, the median is 0, and the 75th percentile is 1 at BH-adjusted Wilcoxon `p < 0.05`.
- The represented lysosomal/endolysosomal panel available in the 151 TH training table is almost entirely flat or singleton-level. In the exact parquet rows for `Atp13a2`, `Atp6v0a1`, `Clcn4`, `Ctsb`, `Gaa`, `Grn`, `Ppt1`, `Psap`, and `Scarb2`, each had exactly one FDR<0.05 feature and that feature was the target transcript itself. `Lamp2`, `Manba`, `Atp6v1a`, `Atp6v1b2`, and `Atp6v1e1` had zero FDR<0.05 features in the same focal population.
- The same-experiment corpus interprets several of those parquet observations as real buffered responses rather than an unmeasured hidden lysosomal module. `Gaa` had no non-`Gaa` FDR<0.10 genes in all 23 recovered neuronal groups; `Ppt1` had 0 non-`Ppt1` FDR<0.10 genes in all 23 groups; `Atp13a2` had no corrected downstream response in any recovered group despite directional self-depletion; and `Grn` lacked its chronic lysosomal/autophagy/immune sentinel program in the acute NeuN+ assay. Shared claims over `Ppt1`, `Manba`, `Psap`, `Gnptab/Gnptg`, `Sort1`, and `Tmem106b` state that represented lysosomal hydrolase and M6P-pathway perturbations were largely buffered and did not converge on a broad storage-stress, autophagy, TFEB/MiT, or ISR/UPR RNA module.
- I compared 14 represented lysosomal/endosomal profiles in the focal cell group. The profile cohort covered all 91 pairs; no pair shared a significant positive feature, and among the 36 pairs with significant negative features the significant-program overlap coefficient was 0. This supported treating lysosomal membership as a low-burden prior, not as evidence for a recurrent multi-gene signature.
- Across all training targets with a measurable self row in `151 TH Prkcd Grin2c Glut`, 237/276 single-DEG perturbations were self-transcript-only positives, whereas every zero-DEG perturbation lacked a significant self row. Thus the local distinction between `0` and `1` is often whether the edited target mRNA itself clears FDR, not whether a downstream program appears.

## Synthesis

The biology bundle makes `Gns` a credible realized lesion: it is expressed in the assayed thalamic nuclei, its soluble lysosomal enzyme stock should turn over within the 21-28 day window, and related extracellular sulfatases are not true replacements for the lysosomal exo-hydrolase step. However, the closest measured perturbations in this acute sparse neuronal screen argue strongly against a broad downstream storage-stress RNA response. Soluble hydrolases and lysosomal cargo or trafficking targets repeatedly produced either no 151 TH DEGs or one self-transcript hit, and packaged same-experiment reports found no shared autophagy/lysosomal/TFEB/ISR program for them.

Given `Gns`'s strong baseline detection in the exact focal population, I forecast that the target transcript itself is the most likely single FDR<0.05 row. I therefore set the integer prediction to `1`, with the expected downstream count approximately zero.
