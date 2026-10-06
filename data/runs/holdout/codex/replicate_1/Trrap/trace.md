# Trrap DEG-count forecast

## Target and endpoint

- Target: `Trrap`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`

## Evidence used

### Target biology

The declared biology bundle reports that `Trrap` is directly detectable in the focal
non-target population: 21,438 of 23,679 nuclei express the target transcript
(`90.5359%`), with mean raw UMI `2.9008` and pseudobulk CPM `181.806`.

The same bundle classifies TRRAP as a renewable chromatin-complex scaffold in
NuA4/TIP60 and SAGA/STAGA-family HAT complexes. Its functional-stock card favors
substantial loss of operative TRRAP by the P37-P44 harvest after a P16 edit:
pre-existing protein should persist initially, but postnatal neuronal deletion
data show molecular remodeling during early postnatal life and a structural
Purkinje-cell consequence by about one month. This made a strict null less
likely than for weakly expressed or permanently installed targets, but the
evidence was not a synchronized P16 thalamic time course.

### Training endpoint table

The 151 TH training table contains 1,674 perturbations. It is zero-heavy:

- `1205 / 1674` training perturbations have `0` DEGs.
- The median is `0`.
- The 75th percentile is `1`.
- The 95th percentile is `18`.
- The 99th percentile is about `436`.

Training perturbations used as scale references in the focal class had these
exact `p_adj < 0.05` DEG counts:

| target | n_degs | interpretation |
|---|---:|---|
| `Ep300` | 0 | broad HAT coactivator boundary |
| `Atxn7` | 0 | SAGA-family component boundary |
| `Kat6a` | 0 | MYST/HAT catalytic boundary |
| `Kat6b` | 0 | MYST/HAT catalytic boundary |
| `Brd1` | 4 | HAT scaffold boundary |
| `Crebbp` | 8 | p300/CBP coactivator boundary |
| `Kmt2a` | 24 | weaker chromatin activator |
| `Arid2` | 56 | moderate chromatin-remodeling row |
| `Bptf` | 65 | moderate chromatin-remodeling row |
| `Chd4` | 100 | moderate chromatin-remodeling row |
| `Ctcf` | 270 | strong chromatin genome-organization row |
| `Brd4` | 311 | strong acetyl-reader/transcriptional row |
| `Setd1a` | 368 | strong chromatin-activation row |
| `Phf12` | 403 | strong SIN3-HDAC recruiter row |
| `Yy1` | 720 | very strong transcription/chromatin regulator row |
| `Sin3a` | 1433 | extreme corepressor-scaffold row |

### Same-experiment packaged context over training perturbations

The internal corpus was used only for represented training targets, not for a
`Trrap` report. The `Brd1:F005` Finding was a key downward boundary: represented
MYST/HAT comparators did not phenocopy `Brd1`; `Kat6a`, `Kat6b`, and `Ep300`
were flat, and `Crebbp` was restricted rather than Brd1-like. The `Ash1l:F004`
Finding gave the analogous chromatin-mark warning: weak or null H3K36/PRC2-axis
rows coexist with broad `Setd1a` and `Sin3a` responses, so a chromatin-regulator
annotation is not sufficient to predict a high endpoint.

The corpus also supported a positive chromatin-state branch. `Brd4` had a real,
151-enriched transcriptional response but did not phenocopy represented p300/CBP,
Mediator, or MYC-axis comparators. `Phf12`, `Setd1a`, and `Sin3a` reports each
showed broad but structured postnatal neuronal responses. These findings put
TRRAP between two regimes: a narrow HAT/coactivator regime that was often
buffered in this assay, and a stronger broad chromatin-state regime.

### Focused 151 TH profile analysis

I projected 13 selected, training-only chromatin/cofactor perturbations from the
151 TH rows of `training_de_all_cell_groups.parquet` and compared their local
profiles. The exact cohort was:

`Sin3a`, `Yy1`, `Brd4`, `Setd1a`, `Phf12`, `Ctcf`, `Chd4`, `Bptf`, `Arid2`,
`Kmt2a`, `Crebbp`, `Ep300`, `Atxn7`

Within that focused cohort, the profile comparison recovered:

- `9` targets with at least 50 significant focal-class features
- `1` target with 10-49 significant features
- `1` target with 1-9 significant features
- `2` targets with no significant features

The cohort had a stronger recurrent negative tail than positive tail: across all
78 available pairs, the mean top-tail overlap coefficient was `0.2477` for
negative features versus `0.1208` for positive features, and the mean
same-direction cosine contribution was `0.7527` on the negative side. That
supports a shared down-regulated neuronal/chromatin response axis among several
responsive rows, but null rows such as `Ep300` still remained profile-correlated
at subthreshold effect sizes, so pairwise correlation was not treated as enough
to override the count table.

## Synthesis

Upward bearings:

- `Trrap` is broadly expressed in the exact focal class.
- TRRAP is not a single narrow acetyltransferase; it is a shared scaffold used
  by multiple HAT complexes and recruited to ongoing promoter regulation.
- The functional-stock card favors loss of most operative scaffold capacity
  within the experiment window.

Downward bearings:

- Direct HAT/coactivator training rows in 151 TH were mostly null or tiny
  (`Ep300`, `Atxn7`, `Kat6a`, `Kat6b`, `Brd1`, `Crebbp`).
- Same-experiment reports explicitly warn that generic MYST/HAT or p300/CBP
  weakening did not explain nearby chromatin responses.
- The matched experiment is basal, sparse, survivor-conditioned P16 loss in
  postmitotic thalamic neurons, not the complete early developmental deletion
  used in much of the external TRRAP evidence.

Those considerations made a 0-10 DEG forecast too low, because Trrap has higher
reach and broader scaffold biology than the null HAT rows. They also made the
300-1400 DEG chromatin tail too high, because that tail is driven by SIN3,
YY1, BRD4, PHF12, SETD1A, and CTCF states rather than by represented HAT
coactivator loss.

I therefore placed `Trrap` in the moderate chromatin-regulator band, close to
`Bptf`/`Arid2`/`Chd8`/`Zmynd8` rather than the p300/CBP nulls or the `Sin3a`
extreme, and used a point estimate of `74` DEGs.
