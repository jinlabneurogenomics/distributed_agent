# Trace

## Target and endpoint

- Target manifest: `Srsf1`.
- Endpoint: `n_degs`, the number of `151 TH Prkcd Grin2c Glut` measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- The declared training endpoint table has 1,674 observed perturbations; its median was 0, 90th percentile was 2, 95th percentile was 18, and 99th percentile was 436.48. I therefore treated hundreds of DE genes as a genuinely high response in this focal class.

## Target-side biology

The declared `Srsf1` biology bundle and characterization card were the target-side prior.

- Exact focal reach was high: `Srsf1` RNA was detected in 21,599 of 23,679 non-target focal nuclei, or 91.2158452637358%, with mean log1p CP10K 1.0019309179820632 and pseudobulk CPM 202.99093174743368.
- SRSF1 was characterized as an SR-family RNA-binding factor for constitutive and alternative pre-mRNA splicing with post-splicing export/translation roles.
- The functional-stock adjudication concluded `functional_stock_by_harvest = likely_substantially_depleted`: P16 editing stops new intact SRSF1 supply, its active nuclear and shuttling/cytoplasmic pools require renewal, and an Srsf1 neural knockdown changes an RNA-processing output within four days in a developmental neural model. The same card kept the caveat that a postmitotic thalamic neuronal protein half-life was not found.
- The same-experiment corpus had no Srsf1 Findings or Claims, so no held-out Srsf1 outcome-bearing report text was available or used.

This combination made a nonzero transcriptional response likely enough that I did not use the training-set median of zero as the center.

## Observed analogs

Because the closest exact paralog/interactor entries from the biology card, `Srsf2` and `Elavl1`, were absent from the training endpoint table, I used the offline mouse gene-analog nomination over the declared training universe. Its leading specific nominees were spliceosome or spliceosome-adjacent RNA-processing genes: `U2af2`, `Snrpb`, `Prpf6`, `Hnrnpu`, `Hnrnpa2b1`, `Syncrip`, `Snrnp70`, `Cdc40`, `Ddx39b`, and `Rnpc3`.

I then compared those nominees and nearby RNA-processing controls in the declared Parquet restricted to `group_name = "151 TH Prkcd Grin2c Glut"`. The measured focal counts split into three roles:

- High primary anchors: `U2af2` 828, `Prpf6` 454, `Hnrnpu` 733, `Rnpc3` 868.
- Same RNA-processing module but lower scale: `Snrnp70` 213, `Cdc40` 624, `Tardbp` 210, `Hnrnpc` 122, `Thoc1` 303.
- Spliceosome/RBP boundaries: `Snrpb` 0, `Ddx39b` 0, `Son` 0, `Syncrip` 0, `Hnrnpa2b1` 11, `Hspa8` 9, `Ctnnbl1` 1, `Hnrnph2` 4.

The profile comparison supported using the high anchors as a coherent broad RNA-processing state but not as a deterministic complex-membership rule. In the 17-gene comparison, nine nodes had at least 50 focal significant genes and four had none. Same-experiment Finding context for `Prpf6` and `Rnpc3` also described a selective shared spliceosome/RNA-processing neuronal module in which `U2af2`, `Prpf6`, `Snrnp70`, `Rnpc3`, `Cdc40`, and `Hnrnpu` converge, while `Snrpb`, `Ctnnbl1`, `Snrpn`, `Rp9`, and non-RNA-processing transport targets define measured boundaries.

## Numerical synthesis

The four strongest direct/RNA-processing anchors center near 700 DEGs on a log scale; adding the moderate same-module comparators gives a log-scale center near 398. I placed `Srsf1` just under `Prpf6` rather than near `U2af2`/`Rnpc3` because SRSF1 is an SR regulator with paralog overlap and unresolved postmitotic compensation, not a uniquely limiting U2AF or core minor-spliceosome component. I did not pull the point down to the all-nominee median of 122 because `Srsf1` has high focal expression and a renewable functional pool likely depleted by harvest, unlike many flat annotated boundaries.

Final point estimate: `400`.
