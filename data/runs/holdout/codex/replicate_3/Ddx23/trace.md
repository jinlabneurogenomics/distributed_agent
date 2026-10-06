# Ddx23 DEG-count forecast

## Endpoint and target

Target: `Ddx23`

Endpoint: `n_degs`, the number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

Declared endpoint inputs used:

- Biology bundle: `[local file: Ddx23.json]`
- Training count table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Training DE parquet: `[local file: training_de_all_cell_groups.parquet]`

I did not read a Ddx23 outcome profile; `Ddx23` is absent from the declared 1,674-row 151-class training count table.

## Ddx23 biology prior

The canonical Ddx23 biology bundle places the target in reach in the assayed population: in matched non-target `151 TH Prkcd Grin2c Glut` nuclei, `Ddx23` was detected in 18,481 of 23,679 nuclei, or 78.05%, with mean raw UMI 1.708, mean CP10K 1.097, and pseudobulk CPM 107.08.

The same bundle characterizes DDX23 as a dynamic U5/U4-U6-U5 tri-snRNP and spliceosomal B-complex ATP-dependent RNA helicase, with an additional annotation in R-loop suppression. A coding-disruptive edit should stop new intact DDX23 production rather than immediately eliminating pre-existing molecules, but the declared functional-stock adjudication judged harvest-time stock as `likely_substantially_depleted`: mouse mpkCCD half-lives of 39.06 to 61.43 hours put P37-P44 harvest roughly 8 to 17 half-lives after a P16 edit. The bundle also found no close DDX23/PRP28-family backup in mouse, while flagging that this is bounded-search evidence, not proof of no compensation.

The phenotype prior is biologically strong but endpoint-indirect. Homozygous mouse null loss is reported as complete-penetrance preweaning lethality, and human de novo missense variants support neural relevance, but neither result measures post-P16 thalamic neuronal CRISPR loss or a 21-28 day single-nucleus transcriptional response. I treated these as evidence that Ddx23 loss is material, not as a quantitative DEG count.

## Training measurements

The focal training table is very sparse overall:

- 1,674 training perturbations in the count table
- 1,205 with `n_degs = 0`
- median `n_degs = 0`
- mean `n_degs = 14.05`
- 95th percentile `n_degs = 18`
- 99th percentile `n_degs = 430`
- maximum `n_degs = 2,677`

The relevant exception is the upper tail of splicing and nuclear RNA-processing factors in the same cell class. Exact focal-class counts for the measured comparators I used were:

| target | n_degs |
| --- | ---: |
| Rnpc3 | 868 |
| U2af2 | 828 |
| Hnrnpu | 733 |
| Cdc40 | 624 |
| Prpf6 | 454 |
| Snrnp70 | 213 |
| Tardbp | 210 |
| Matr3 | 149 |
| Hnrnpc | 122 |
| Ddx3x | 8 |
| Snrpb | 0 |
| Syncrip | 0 |

The closest measured component-level analogs were `Prpf6`, a U5/tri-snRNP factor, plus spliceosome factors `Cdc40`, `U2af2`, `Rnpc3`, and `Snrnp70`. These are all far above the screen background in this thalamic class: among the 1,674 training perturbations, `Rnpc3` ranked 4th, `U2af2` 6th, `Cdc40` 11th, `Prpf6` 17th, and `Snrnp70` 28th by `n_degs`. The low `Ddx3x`, `Snrpb`, and `Syncrip` values served as boundaries against treating every helicase or RNP gene as high response.

I queried the training Parquet for these same nodes in `151 TH Prkcd Grin2c Glut` and verified that each count is over 17,259 measured rows in the exact requested cell class. The matched recovered-cell counts for the principal spliceosome comparators were not unusually high, so the observed hundreds of DEGs are not explainable only as the result of exceptional cell numbers:

| target | n_degs | n_pert_matched | n_ctrl_matched |
| --- | ---: | ---: | ---: |
| Rnpc3 | 868 | 149 | 23679 |
| U2af2 | 828 | 222 | 23679 |
| Cdc40 | 624 | 159 | 23679 |
| Prpf6 | 454 | 72 | 23679 |
| Snrnp70 | 213 | 135 | 23679 |

I also compared the 151-class signatures of a declared 12-gene RNA-processing cohort with `dataset.candidate_profile_review` in `evidence/splicing_rbp_profile_compare.json` and summarized it in `evidence/splicing_rbp_profile_cohort.json`. All 66 selected pairs were available. Whole-profile correlations among the core spliceosomal comparators were positive, for example `Rnpc3` versus `Prpf6` Pearson 0.595, `U2af2` versus `Prpf6` Pearson 0.564, and `Cdc40` versus `Prpf6` Pearson 0.615. Across the full 12-gene cohort, negative-tail overlap was stronger than positive-tail overlap, with mean top-tail overlap coefficient 0.139 for downregulated features versus 0.082 for upregulated features. This supported a recurrent loss-of-RNA-processing survivor state, while showing that no single measured profile should be copied directly to Ddx23.

## Point estimate

I placed Ddx23 in the high-response spliceosome range because the target is expressed in most assayed thalamic nuclei, the functional stock should substantially turn over within the 21-28 day window, and DDX23 acts in the same U5/tri-snRNP/B-complex axis as the high 151-class splicing perturbations rather than as a broad, redundant DEAD-box paralog. The principal analogs span 213 to 868 DEGs, with `Prpf6` at 454 as the nearest tri-snRNP comparator and `Cdc40`/`U2af2`/`Rnpc3` showing that core spliceosome loss can cross 600-800 DEGs in this focal class.

I discounted below the responsive-spliceosome mean because Ddx23-specific P16 thalamic latency is unmeasured, germline lethality could partly manifest as unrecovered edited neurons rather than survivor DE, and the profile cohort was a shared RNA-processing stress neighborhood rather than a target-specific analogue. Balancing those terms put the forecast slightly above `Prpf6` and below the `Cdc40`/`U2af2`/`Rnpc3` tier.

Predicted `n_degs`: **520**
