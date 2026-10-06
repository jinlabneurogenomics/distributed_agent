# Dnajc6 n_degs prediction for 151 TH Prkcd Grin2c Glut

## Target and endpoint

- Held-out perturbation: `Dnajc6`.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- The same-experiment corpus has no packaged `Dnajc6` target report, Claim, Finding, or explicit reference in this release, so the target count was not available from the report layer.

## Biology used

The declared Dnajc6 bundle supports a reachable but buffered acute perturbation.
Dnajc6/auxilin is a recyclable clathrin-uncoating cochaperone that recruits
Hsc70/HSPA8 to clathrin-coated vesicles. A P16 disruptive edit should stop new
auxilin production, and the P16 to P37-P44 window spans multiple half-lives of
the closest measured synaptic-protein turnover proxy, so functional auxilin is
likely substantially depleted by harvest.

The focal thalamic class also has exact target reach: Dnajc6 was detected in
21,198 of 23,679 matched non-target nuclei, 89.52% expressing, with mean
1.8656 CP10K. I therefore did not treat the perturbation as expression-limited.

The main downward bearing was buffering and endpoint coupling. The biology card
notes direct same-context compensation by the homologous cochaperone GAK, and
the mouse phenotype evidence is from germline or non-thalamic postnatal neural
contexts. Those facts favor some synaptic-vesicle physiology effect but a weak
survivor-conditioned nuclear RNA signature.

## Training measurements used

The declared 151-class training count table contains 1,674 targets; 1,205 have
`n_degs = 0`, the median is 0, the 75th percentile is 1, and the 90th
percentile is 2. The distribution is therefore zero-heavy even before asking
for Dnajc6-specific attenuation.

I used Dnajc6's immediate clathrin/Hsc70 biology and the nearest represented
presynaptic vesicle/endocytosis genes as the quantitative scale. Exact
151-class counts at BH `p < 0.05` were:

| perturbation | n_degs |
| --- | ---: |
| `Cltc` | 3 |
| `Hspa8` | 9 |
| `Dnm1` | 1 |
| `Synj1` | 1 |
| `Syn1` | 1 |
| `Syp` | 1 |
| `Cplx1` | 1 |
| `Dnajc5` | 1 |
| `Stxbp1` | 1 |
| `Syn2` | 0 |
| `Unc13a` | 0 |
| `Unc13b` | 0 |
| `Unc13c` | 0 |
| `Syt2` | 0 |

The focal Parquet rows confirmed these counts against 17,259 measured features
per target. In the sparse direct vesicle genes, the lone significant feature
was often the perturbed transcript itself: for example Dnm1, Synj1, Cplx1, Syp,
Syn1, Stxbp1, Dnajc5, and Bin1 each had exactly one 151-class DEG and it was
the self transcript. In contrast, `Hspa8` had a small 9-gene cytosolic
proteostasis/chaperone counterinduction in this class, and `Cltc` had a
3-gene response with negative Rbms1, Ero1b, and Gabra4 hits.

The packaged same-experiment Findings matched that scale rather than pointing
to a hidden broad endocytic program: Cltc is an active core-coat perturbation
that is not phenocopied by Hspa8, Dnm1, Synj1, or several presynaptic/endocytic
neighbors; Hspa8 has a small, sharply cell-type-restricted HSP/cochaperone
response; and Dnm1/Synj1-like perturbations can be essentially downstream-flat
by FDR in this acute postnatal neuronal snRNA-seq assay.

## Forecast

Dnajc6 sits on the low side of this local scale. It is more specific and GAK-
buffered than core `Cltc`, and loss of the HSPA8 partner is broader than loss
of auxilin alone. The exact focal expression keeps a pure unreachable zero from
being the best point, but the direct endocytosis and presynaptic comparators
cluster at 0 to 1 significant genes in the same cell class.

I therefore predict a single BH-significant measured gene.
