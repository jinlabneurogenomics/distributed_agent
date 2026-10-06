# Gatad1 direct forecast

Target:

- `Gatad1` in `151 TH Prkcd Grin2c Glut`
- endpoint: number of measured genes in this focal class with Wilcoxon BH-adjusted `pvals_adj < 0.05`
- withheld Gatad1 DE rows and the withheld Gatad1 count were not used

Evidence that determined the point:

1. The canonical Gatad1 biology bundle reports exact focal-class expression in the matched non-target nuclei: Gatad1 is detected in 10,176 of 23,679 non-target nuclei, or 42.97%, with mean raw UMI 0.607 and mean log1p CP10k 0.260. This supports the target being present in a material fraction of the thalamic glutamatergic cells, but it is still a modest nuclear transcript and does not establish editing efficiency or functional dependence.

2. The endpoint-blind biology card places GATAD1 in an H3K4me3-linked EMSY/KDM5A/SIN3B chromatin regulatory complex. The same card keeps realization uncertain: disruptive editing stops new GATAD1 supply, but no target-specific protein half-life, chromatin residence time, or 21-28 day complex-loss timing was found. Adult regional brain expression and the absence of a close paralog give a route to effect, while global embryonic lethality and a largely negative cardiomyocyte knockout do not establish a postnatal neuronal requirement.

3. The declared focal training count table has 1,674 visible targets. It is dominated by weak or unobserved responses: 1,205 targets have `n_degs = 0`, 276 have `n_degs = 1`, the median is 0, and the mean is pulled upward to 14.05 by rare outliers such as `Uba5`, `Tpr`, and `Sin3a`.

4. Annotation-based analog nomination for Gatad1 found no training-available exact-complex, paralog, or narrow-module analogs; the 844 available nominees were all broad functional fallbacks from terms such as chromatin organization, chromatin remodeling, nuclear localization, and DNA-templated transcription. I therefore used the annotation layer only to sanity-check chromatin/regulatory comparators, not to rank or weight the forecast.

5. The hand-retained chromatin-reader/remodeler comparators in the focal count table span almost the whole low-to-high range: `Kdm5b = 0`, `Mbd2 = 0`, `Gatad2b = 1`, `Kdm5c = 18`, `Zmynd8 = 74`, `Chd4 = 100`, and `Sin3a = 1433`. A run-local profile comparison of `Gatad2b`, `Zmynd8`, `Kdm5c`, `Kdm5b`, `Mbd2`, `Chd4`, `Sin3a`, `Zbtb7a`, and `Ctcf` confirmed that these training perturbations are available in the focal class but have highly heterogeneous DEG burdens rather than one transferable scale.

Reasoning:

Gatad1 has enough focal expression to avoid treating the perturbation as an expression-reach null, and lack of a close paralog argues against a fully redundant target. Against that, the operative lesion is an accessory chromatin-complex component with unknown turnover through the P16-to-P37/P44 window, no direct postnatal neuronal phenotype, and no training target in the declared universe that exactly captures EMSY/KDM5A/SIN3B GATAD1 loss.

The most informative measured comparators are therefore the quiet/weak chromatin-associated genes rather than the extreme global regulators. `Sin3a` is a core HDAC scaffold and a 1,433-DEG outlier, while `Chd4` is a NuRD ATPase with a broader remodeling role. `Kdm5c` and `Zmynd8` show small-to-moderate responses, but the same KDM5 family includes the silent `Kdm5b`, and the GATAD-family NuRD subunit `Gatad2b` gives only one significant gene. Those measurements make a large Gatad1 signature possible but not the center of the distribution for a non-core, incompletely realized chromatin reader perturbation.

I therefore placed Gatad1 just above the screen-wide zero mode: a weak focal response with only one measured gene passing BH FDR 0.05.
