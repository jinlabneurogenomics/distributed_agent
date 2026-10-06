# Ddx23 direct DEG-count forecast

## Endpoint

- Target: `Ddx23`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Quantity: measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Point forecast: `480`

## Evidence used

The Ddx23 biology bundle supports a real perturbation by harvest rather than a
stock-persistence null. In the exact focal population, Ddx23 was detected in
18,481 of 23,679 non-target nuclei, 78.0% of the population, with mean raw UMI
1.71 and mean log1p CP10K 0.644. The same bundle places DDX23 in recurrent
U5/tri-snRNP and spliceosomal B-complex function, with R-loop-control
annotation, and adjudicates the existing protein stock as likely substantially
depleted across the 21-28 day P16-to-P37/P44 interval. That adjudication rests
on the dynamic, repeatedly renewed molecular operation and mouse-cell DDX23
half-lives of 39.06-61.43 h, while acknowledging that those half-lives are from
non-neural mpkCCD cells.

The declared training count table for this exact cell group is sparse overall:
among 1,674 training perturbations the median is 0 DEGs, the 75th percentile is
1, the 95th percentile is 18, and the 99th percentile is 430. Ddx23 therefore
should not be forecast from the global mean. The relevant high-count branch is
RNA splicing and RNA processing:

| training target | relationship to Ddx23 prior | `n_degs` in 151 |
| --- | --- | ---: |
| `Rnpc3` | spliceosome/minor-spliceosome RNA processing | 868 |
| `U2af2` | spliceosome splice-site recognition | 828 |
| `Hnrnpu` | RNA-processing-associated nuclear RNP target | 733 |
| `Cdc40` | spliceosome catalytic-step factor | 624 |
| `Prpf6` | U5/tri-snRNP, the closest measured Ddx23 complex neighbor | 454 |
| `Thoc1` | coupled splicing/export pathway | 303 |
| `Snrnp70` | U1 snRNP spliceosome factor | 213 |

Profile comparison on the declared Parquet for these RNA-processing targets
confirmed that the strongest spliceosome perturbations were not isolated count
outliers. `Prpf6`, `Rnpc3`, `U2af2`, `Cdc40`, and `Snrnp70` all had at least 50
significant features in the profile tool, with 213-868 significant genes in
the same BH 0.05 definition. Same-experiment Finding context for the training
targets summarized a recurrent same-direction RNA-splicing /
RNA-processing module among `Prpf6`, `Rnpc3`, `Cdc40`, `U2af2`, and `Snrnp70`
in midbrain/thalamic responders.

There are important downward boundaries. The Ddx23 bundle has no postnatal
thalamic conditional phenotype and no direct mouse-neuron turnover experiment.
Within the Ddx23 GO/KEGG/Reactome neighborhoods represented in the training
set, not every spliceosome-adjacent perturbation was large: `Hnrnpc` had 122
DEGs, `Hnrnpa2b1` 11, `Hspa8` 9, `Ddx39b` 0, and `Snrpb` 0. The flat `Snrpb`
contrast had 179 matched perturbed nuclei in the exact Parquet context, so it
is not simply an obvious underpowered zero. Because `Ddx23` is a U5/tri-snRNP
helicase with continuous demand and no identified close backup, I weighted this
low Sm-core boundary less heavily than the closer `Prpf6`/`Cdc40`/`U2af2`
branch.

## Synthesis

The closest measured training anchor is `Prpf6`, a U5/tri-snRNP spliceosome
factor with 454 DEGs despite only 72 matched perturbed nuclei in this cell
group. The broader high branch of `Rnpc3`, `U2af2`, `Cdc40`, `Prpf6`, `Thoc1`,
and `Snrnp70` has a log1p mean around 486 DEGs and an arithmetic center near
550. I therefore place Ddx23 near the direct U5 anchor and below the most
extreme `Rnpc3`/`U2af2` responses, while keeping it well above the sparse
screen-wide background.

Predicted `n_degs` = `480`.
