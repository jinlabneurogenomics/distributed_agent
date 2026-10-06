# Zfhx3 direct n_degs forecast

Target: `Zfhx3`

Cell class: `151 TH Prkcd Grin2c Glut`

Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.

## Evidence used

- The held-out biology bundle reports exact focal expression of `Zfhx3` in the requested class: 16,679 of 23,679 non-target nuclei expressed it, or 70.44%, with mean CP10K 0.881 and mean log1p(CP10K) 0.540. The feature was available in this population, so the perturbation has target-expressing thalamic cells in reach.
- The same bundle adjudicates ZFHX3 as a renewed nuclear AT-motif/homeodomain transcription factor whose functional stock is likely substantially depleted within the P16-to-P37/P44 perturbation window. The strongest direct timing evidence is adult mouse SCN, not thalamus, so I treated it as evidence that the edit can realize in postmitotic neurons, not as an exact magnitude donor.
- The `151 TH Prkcd Grin2c Glut` training count table is very sparse: among 1,674 visible targets, 1,205 have `n_degs = 0`, the median is 0, the 75th percentile is 1, and only 106 targets have `n_degs >= 10`.
- The same-family visible comparator `Zfhx2` has `n_degs = 0` in this cell class. Its same-experiment corpus context describes only a weak singleton FDR<0.10 response in another glutamatergic class and no broad ZFHX-family transcriptional state, so it acts as a downward boundary on transferring the adult SCN Zfhx3 biology into sampled central neurons.
- A deterministic typed analog nomination for Zfhx3 returned mostly broad transcription-factor or circadian annotations rather than exact-complex/paralog donors. The one direct-interaction nominee, `Runx3`, has `n_degs = 0`; the top broad SMAD/SOX/TBX nominees were also quiet in this class: `Smad3 = 0`, `Smad4 = 0`, `Smad2 = 1`, `Sox4 = 0`, `Tbx3 = 0`, `Ppard = 0`, `Mkx = 0`, `Smarca4 = 0`, and `Pparg = 0`.
- Some loose circadian or generic TF comparators were high-count outliers, for example `Nr1d1 = 116`, `Nrf1 = 138`, `Tcf7l2 = 106`, and `Zfp423 = 150`, but they were not close operation analogues. A matched profile comparison over 17 Zfhx3-adjacent nominees found that 11/17 had no significant genes, only 4/17 had at least 50 significant genes, and the positive-program overlap across the cohort was weak: mean positive top-tail overlap 0.0758, with significant-program overlap on only 10 of 136 pairs.

## Synthesis

Zfhx3 has enough in-population expression and short-enough protein turnover that a downstream thalamic signature is biologically reachable. I therefore did not assign a hard zero. The exact cell-class count distribution, the quiet Zfhx2 and Runx3 comparators, and the mostly quiet high-priority TF nominees all argue that any measured response is likely to sit near the mode of the training table rather than in the 100-DEG circadian/chromatin outlier range.

I put the forecast just above the all-training median, at the 75th percentile of the training table:

`predicted_n_degs = 1`
