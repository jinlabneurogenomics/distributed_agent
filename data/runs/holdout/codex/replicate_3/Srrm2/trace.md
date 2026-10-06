# Trace

## Target and endpoint

- Target: `Srrm2`.
- Requested endpoint: number of measured genes with Wilcoxon BH-adjusted `p < 0.05` in `151 TH Prkcd Grin2c Glut`.
- The endpoint is an exact Perturb-seq whole-gene abundance count in recovered P37-P44 NeuN+ thalamic nuclei after a P16 sparse CRISPR loss-of-function perturbation.

## Evidence used

- The declared `Srrm2` biology bundle places SRRM2 in spliceosomes and nuclear speckles. It describes SRRM2 as a dynamic spliceosome-associated RNA-processing factor and nuclear-speckle organizing scaffold, with cultured-cell depletion/truncation evidence for altered cassette-exon inclusion and speckle organization.
- The same bundle adjudicates functional stock at harvest as `likely_substantially_depleted`: P16 editing stops new intact SRRM2 supply, the operative spliceosomal/speckle pool is dynamically renewed, and cultured-cell depletion acts on an approximately one-day timescale, although postmitotic mouse thalamic protein turnover is not directly measured.
- Focal baseline expression is not limiting: the exact in-assay expression record for this cell class has `pct_cells_expressing = 99.9239832763208`, `n_cells_expressing = 23661 / 23679`, and `mean_raw_umi = 12.474217661218802`.
- Srrm2 haploinsufficiency has postnatal mouse brain molecular/physiological consequences in the biology bundle. That supports observability in a postnatal neural context, but it is lifelong germline heterozygosity rather than biallelic sparse P16 editing in thalamic neurons.

## Training measurements used

The training count table for `151 TH Prkcd Grin2c Glut` is heavily zero-inflated: 1,205 of 1,674 training perturbations have `n_degs = 0`, the 95th percentile is only 18, and only 42 perturbations exceed 100 DEGs. RNA-processing comparators, however, are strongly enriched in the upper tail:

| target | `n_degs` |
| --- | ---: |
| Rnpc3 | 868 |
| U2af2 | 828 |
| Hnrnpu | 733 |
| Cdc40 | 624 |
| Tnpo3 | 618 |
| Prpf6 | 454 |
| Thoc1 | 303 |
| Snrnp70 | 213 |
| Tardbp | 210 |
| Hnrnpc | 122 |
| Hnrnpa2b1 | 11 |
| Son | 0 |

I compared a 17-gene RNA-processing cohort in the declared differential-expression parquet, restricted to `151 TH Prkcd Grin2c Glut`. The high-response spliceosome/RNP perturbations had the exact same significant-gene counts in the profile artifact as in the count table: `Cdc40` 624, `Hnrnpu` 733, `Prpf6` 454, `Rnpc3` 868, and `U2af2` 828. Their profiles were mutually positive and embedded in a dense RNA-processing neighborhood, so the hundreds-of-DEGs scale is not a one-off count-table artifact.

The strongest downward boundary is `Son`, the other nuclear-speckle scaffold named in the Srrm2 source card. `Son` has `n_degs = 0` in this exact focal class and the same-experiment Son report explicitly separates Son/Ylpm1 from broad RNA-processing-factor responses; `Ylpm1` is also nearly flat in this class with `n_degs = 1`.

U2af2 provides the broad positive side of the same comparison. Its report in the same corpus describes a broad response concentrated in this thalamic population and a same-direction neighborhood including `Prpf6`, `Cdc40`, and `Tpr`, connecting the high-count training profiles to spliceosome stress rather than to an arbitrary high-DEG state.

## Synthesis

`Srrm2` should be active in essentially all focal cells and the 21-28 day interval is long enough that edited cells are likely to lose much of the operative SRRM2 pool. That argues against treating the target like the many zero-count training perturbations.

I did not transfer the full U2AF2/RNPC3 scale directly. SRRM2 is a speckle/spliceosome scaffold, not the core U2 or U11/U12 splice-site-recognition machinery, and the closest assayed speckle scaffold boundary, `Son`, is silent in this cell class. I therefore placed the point below the core spliceosome analogs (`Prpf6`, `Cdc40`, `Hnrnpu`, `U2af2`, `Rnpc3`) but above the near-null Son/Ylpm1 branch and in the same order as the weaker broad RNA-processing responses (`Thoc1`, `Snrnp70`, `Tardbp`).

Point prediction: `384`.
