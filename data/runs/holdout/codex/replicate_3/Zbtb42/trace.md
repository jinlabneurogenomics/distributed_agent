# Direct DEG-count forecast for Zbtb42 in `151 TH Prkcd Grin2c Glut`

## Point prediction

I predict **0 BH-adjusted Wilcoxon DEGs** for `Zbtb42` in `151 TH Prkcd Grin2c Glut`.

## Evidence used

- The target and target biology bundle identify the held-out perturbation as `Zbtb42`; no `Zbtb42` outcome was present in the declared 151-class training count table.
- The exact in-assay reach for the focal population was extremely low: in matched non-target `151 TH Prkcd Grin2c Glut` nuclei, `Zbtb42` had 33 total UMIs across 23,679 nuclei, 31 expressing nuclei, `0.1309%` expressing nuclei, `0.000694` mean log1p CP10K, and `0.0873` pseudobulk CPM.
- The biology card supports only a weak-to-moderate realization prior. ZBTB42 is a putative soluble nuclear BTB/POZ-C2H2 transcriptional regulator, so stopping new synthesis can matter, but the card had no ZBTB42-specific protein half-life or acute edit-to-functional-loss clock. Functional stock by the P37-P44 harvest window after a P16 edit was adjudicated as indeterminate.
- The same card supplied nervous-system prior evidence only at a mismatched scale: a constitutive homozygous mouse phenotype with decreased prepulse inhibition and low adult thalamic bulk RNA detection, with no evidence that juvenile thalamic `Prkcd`/`Grin2c` glutamatergic neurons specifically require `Zbtb42` within 21-28 days.
- The declared 151-class training count table contained 1,674 measured training perturbations. Its DEG burden was strongly zero-inflated: 1,205 perturbations had `n_degs = 0`, 276 had `n_degs = 1`, the median was 0, the 75th percentile was 1, and the 90th percentile was 2.
- I used ZBTB/zinc-finger transcriptional regulators in the training table as the closest simple biological calibration set. The ZBTB-family training counts were `Zbtb7a=841`, `Zbtb18=5`, `Zbtb38=1`, and `Zbtb10=Zbtb16=Zbtb20=Zbtb21=0`; excluding the broad `Zbtb7a` outlier, those ZBTB paralog-class perturbations averaged 1 DEG and had median 0. A wider zinc-finger/KLF set was also dominated by 0-count genes, with only a few moderate outliers such as `Zfp423=150`, `Klf9=19`, `Zfp236=19`, and `Zfp148=8`.
- I compared observed 151-class profiles for `Zbtb7a`, `Zbtb18`, `Zbtb38`, `Zbtb10`, `Zbtb16`, `Zbtb20`, `Zbtb21`, `Klf9`, `Zfp423`, `Zfp148`, and `Zfp236` against the declared eligible training universe. In this focused profile comparison, four of the eleven selected nodes had no significant features, three had 1-9, two had 10-49, and only `Zbtb7a` and `Zfp423` had at least 50. The zero/low-count ZBTB nodes still had nontrivial whole-profile correlations with larger responders, so I treated the high `Zbtb7a` count as a boundary case rather than as transferable evidence for every BTB-zinc-finger gene.

## Synthesis

`Zbtb42` has the right broad molecular type to be a transcriptional regulator, but the focal-population expression evidence is much weaker than the functional annotation: only about one in 760 non-target thalamic nuclei expressed any detectable target transcript. In a sparse, survivor-conditioned CRISPR/snRNA-seq screen where 72% of 151-class training perturbations have zero DEGs and 88% have at most one, a weakly reached target with unresolved acute functional-stock depletion should stay on the zero side unless there is a strong matched reason to expect a recurrent response state.

The closest measured ZBTB-family perturbations did not provide that reason. Most were exactly 0 or nearly 0, while `Zbtb7a` was a singular broad responder whose 841-DEG footprint was not representative of the family. I therefore rounded the forecast to the empirical mode and chose:

```tsv
target_name	predicted_n_degs
Zbtb42	0
```
