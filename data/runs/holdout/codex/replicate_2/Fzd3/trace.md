# Direct DEG-count forecast for Fzd3

## Target and endpoint

- Target: `Fzd3`
- Focal class: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes in this class with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Point prediction: `0`

## Evidence used

### Target biology bundle

The declared `Fzd3` biology bundle reports exact in-assay expression in the focal thalamic population: `Fzd3` is detected in `15,381 / 23,679` non-target nuclei, or `64.956%`, with mean `0.7779` cp10k and pseudobulk `77.65` cpm. This makes complete absence of transcript in the assayed cells unlikely, but it does not show target engagement or postnatal dependence.

The same bundle classifies FZD3 as a seven-pass plasma-membrane Wnt/planar-polarity receptor and judges the functional receptor stock as `likely_substantially_depleted` by P37-P44 after a P16 disruptive edit: an edit should halt receptor resupply, and ordinary neuronal membrane-protein turnover could deplete pre-existing protein over the 21-28 day interval. This is only partial-confidence evidence because no FZD3-specific neuronal half-life was found.

The loss-of-function phenotype evidence is developmental rather than matched to the assayed state. Constitutive mouse `Fzd3` loss disrupts embryonic forebrain tracts including thalamocortical and corticothalamic projections, but the bundle explicitly marks this as not testing postmitotic juvenile thalamic neurons. It also notes that `Fzd6` can partially substitute in engineered developmental settings, with no evidence that endogenous `Fzd6` compensates after P16 `Fzd3` editing.

Together, these facts support real lesion plausibility but not a strong expectation of an acute survivor-state RNA program in P16-P44 thalamic neurons.

### Focal training counts

The declared training table for `151 TH Prkcd Grin2c Glut` contains `1,674` perturbations and excludes `Fzd3`.

- `1,205 / 1,674` targets have `n_degs = 0`.
- The median is `0`; the 75th percentile is `1`; the 90th percentile is `2`.
- Only `42 / 1,674` targets exceed `100` DEGs, and those large responses are dominated by broadly disruptive nuclear/proteostasis factors such as `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, `Zbtb7a`, `U2af2`, and `Psmb4`.

That focal-class distribution makes a zero or single-gene result the default for a membrane receptor unless there is matched evidence for a strong postnatal thalamic program.

### Declared Parquet comparators

I queried the declared `training_de_all_cell_groups.parquet`; `Fzd3` was absent as a perturbation target, as expected for the holdout. In the focal class, other Frizzled and proximal noncanonical-Wnt receptor comparators were quiet:

| comparator | `n_degs` in `151 TH Prkcd Grin2c Glut` |
| --- | ---: |
| `Fzd2` | 0 |
| `Fzd4` | 0 |
| `Fzd6` | 0 |
| `Fzd9` | 0 |
| `Ryk` | 0 |
| `Ror1` | 0 |
| `Ror2` | 0 |
| `Lrp5` | 0 |
| `Celsr2` | 1 |
| `Lrp6` | 4 |
| `Gsk3b` | 6 |
| `Ctnnb1` | 383 |

The single `Celsr2` focal DEG was the self transcript, so it did not provide evidence for a downstream thalamic transcriptional program. A broader all-cell-group check showed that `Fzd2`, `Fzd4`, `Fzd6`, and `Fzd9` had zero significant genes in every assayed class in the training Parquet; `Ryk` and `Ror1` were also zero everywhere, while `Ror2` and `Lrp5` each had only one significant gene in one non-focal class. The much larger `Ctnnb1` response is less transferable because beta-catenin is an intracellular canonical-Wnt effector/transcriptional regulator rather than a Frizzled-family membrane receptor.

The nearest developmental axon-guidance or surface-receptor perturbations in the focal table likewise concentrated at 0 or 1 DEG; for example `Robo1`, `Epha4`, and `Plxna2` each had `1`, whereas `Dcc`, `Nrp1`, `Nrp2`, `Epha5`, `Ephb1`, `Robo2`, `Slit2`, and `Unc5d` had `0`.

## Synthesis

`Fzd3` has measurable transcript in the exact focal population and the receptor pool should often turn over within the perturbation window, so the edit is biologically plausible. The evidence that would make a sizable DEG count plausible is the embryonic thalamocortical/corticothalamic axon phenotype, but that evidence concerns circuit construction before the experiment rather than maintenance of recovered postmitotic thalamic neurons after P16.

The directly matched training data put Frizzled-family receptors and neighboring Wnt/PCP surface receptors at zero or nearly zero DEGs in this class, and the target-specific biology did not justify overriding that local pattern. I therefore kept the forecast at the focal distribution's modal low-response value rather than assigning a one-gene self-transcript-only response.

Final predicted `n_degs`: `0`
