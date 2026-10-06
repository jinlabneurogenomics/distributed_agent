# Direct DEG-count forecast for Dnm2

## Target and endpoint

- Target: `Dnm2`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Prediction: `1`

## Evidence used

The declared one-row holdout manifest names `Dnm2`; `Dnm2` is not present in the
1,674-row focal training count table, and the target count/signature were not
queried or reconstructed.

The focal count table is extremely zero-heavy in this cell class. Of 1,674
training perturbations, 1,205 have `n_degs = 0`, 276 have `n_degs = 1`, 31 have
`n_degs = 2`, and 15 have `n_degs = 3`; the median is 0 and 1,527/1,674
training targets are at or below 3 DEGs.

The canonical biology bundle supports real target engagement but also attenuation
by other dynamins. DNM2 is a dynamic clathrin-endocytosis GTPase whose protein
stock should substantially clear over the 21-28 day P16-to-harvest interval:
postnatal hippocampal conditional loss reduced DNM2 protein by 92.5% at DIV18.
At the same time, effective postnatal `Dnm2` single loss left the tested
hippocampal synaptic-transmission readouts intact, and `Dnm1`/`Dnm3` can buffer
much of the assayed neuronal dynamin function. Exact non-target focal expression
shows the `Dnm2` transcript is present in 16,437/23,679 nuclei
(`69.415938%`, mean 0.845943 cp10k), so the target RNA is measurable in the
declared population even though self-transcript reduction is not a quantitative
editing-efficiency readout.

The closest measured paralog is `Dnm1`, and both the same-experiment corpus and
the Parquet support a self-only pattern for it. The packaged finding reports a
pervasive downstream-zero `Dnm1` signature at FDR < 0.10 across 22 measured
neuronal groups despite `Dnm1` transcript decrease in 21 groups. In the exact
focal Parquet slice at the requested p<0.05 threshold, the only significant
`Dnm1` feature is `Dnm1` itself
(`logfoldchanges = -0.712352`, `pvals_adj = 4.09e-25`; focal `n_degs = 1`).

Other represented training perturbations around the same synaptic/endocytic
axis are also tiny in the focal count table:

| target | focal n_degs | significant focal features at p<0.05 |
| --- | ---: | --- |
| `Dnm1` | 1 | self only |
| `Bin1` | 1 | self only |
| `Synj1` | 1 | self only |
| `Syp` | 1 | self only |
| `Syn1` | 1 | self only |
| `Stxbp1` | 1 | self only |
| `Cplx1` | 1 | self only |
| `Syn2` | 0 | none |
| `Cplx2` | 0 | none |
| `Cltc` | 3 | `Ero1b`, `Gabra4`, `Rbms1`; not `Cltc` itself |

Profile comparison within this 10-target cohort in `151 TH Prkcd Grin2c Glut`
found all profiles available, no member with more than 3 significant focal
features by the exact p<0.05 count-table endpoint, and no overlap in the
significant features of the five inspected non-null anchors. Those measured
profiles therefore supported using the cohort for scale, not for a broad shared
transcriptional module.

## Synthesis

`Dnm2` should be edited within the assay interval and is expressed broadly enough
for a self-transcript hit to be plausible. The stronger biological bearing,
however, is that single `Dnm2` loss is buffered by `Dnm1` and `Dnm3` in postnatal
neurons. The measured `Dnm1` paralog lands at one focal DEG and no downstream
DEGs, and the closest available synaptic/endocytic targets cluster at zero to
three focal DEGs rather than in the long right tail of the count distribution.

I therefore forecast a self-transcript-dominated response with essentially no
resolved downstream program in this thalamic glutamatergic population. The best
integer point is `1`; the main adjacent alternatives are `0` if the `Dnm2`
self-row is not significant and `2-3` if `Dnm2` picks up a very small
`Cltc`-like downstream tail.
