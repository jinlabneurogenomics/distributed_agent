# Direct forecast for Gata2 in 151 TH Prkcd Grin2c Glut

## Endpoint

- Target: `Gata2`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Quantity predicted: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.

## Evidence used

### Biology-only Gata2 bundle

The canonical target bundle characterizes GATA2 as a renewable free nuclear
GATA-family DNA-binding transcription regulator. A coding-disruptive edit at
P16 should stop new functional GATA2 production, and the 21-28 day interval to
P37-P44 harvest is long enough that the pre-edit protein pool is favored to
substantially decline. That makes the perturbation biologically realizable if
the assayed neurons actually require Gata2.

The exact focal-population expression reach is the limiting observation. In
non-target nuclei from `151 TH Prkcd Grin2c Glut`, `Gata2` had:

- 35 expressing nuclei among 23,679 non-target nuclei
- 0.1478% of nuclei expressing
- 38 total target UMIs
- mean raw UMI 0.00160
- pseudobulk CPM 0.1006

The broader source evidence is also only weakly matched to this cell class:
the strongest mouse neural loss phenotype is an embryonic midbrain
GABAergic-selector phenotype, not postnatal thalamic neuronal maintenance, and
adult neural expression was reported as regionally restricted with only low
bulk thalamic signal. The bundle therefore supports target engagement in
principle but gives little reason to expect that an aggregate thalamic class in
which under 0.2% of recovered nuclei express `Gata2` will produce a detectable
class-wide Wilcoxon signature.

### Matched training endpoint

The declared count table contains 1,674 observed training perturbations for
this exact endpoint. Its distribution is extremely zero-heavy:

- 1,205 / 1,674 training targets had `n_degs = 0`
- median `n_degs = 0`
- 75th percentile `n_degs = 1`
- 90th percentile `n_degs = 2`
- 106 / 1,674 had `n_degs >= 10`

The closest observed GATA-family training perturbations were all focal nulls:

| target | matched `n_degs` |
| --- | ---: |
| `Gata1` | 0 |
| `Gata3` | 0 |
| `Gata4` | 0 |
| `Gata6` | 0 |

`Gata3` is the closest named vertebrate paralog in the source card and `Gata1`
is also in the GATA123 family; these are not expression-reach matches, but they
are the only assayed same-family anchors in the count table.

### Matched expression profiles

I compared the full `151 TH Prkcd Grin2c Glut` Parquet expression signatures
for `Gata1`, `Gata3`, `Gata4`, and `Gata6`. All four profiles were present, and
all four had:

- `significant_feature_count = 0`
- `response_activity_status = no_significant_features`

The profile check did not reveal a reproducible near-threshold GATA-family
state hidden behind the scalar counts; the largest signed per-gene effects in
these 0-DEG GATA profiles all had adjusted p-values of 1.0.

## Synthesis

The point forecast is controlled by focal reach rather than by the intrinsic
importance of GATA2 during development. GATA2 is a short-window-realizable
transcription-factor perturbation, but the exact thalamic single-nucleus data
show essentially no `Gata2` transcript in the recovered cells. Any true
perturbation in the tiny expressing subset would be diluted across the
aggregated class used by the Wilcoxon contrast, and the assayed GATA-family
training perturbations all had zero significant genes in the same endpoint.

I therefore predict no BH-significant measured genes.

Predicted `n_degs`: **0**
