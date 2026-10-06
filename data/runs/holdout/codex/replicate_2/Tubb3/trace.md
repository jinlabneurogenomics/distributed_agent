# Direct DEG-count forecast

## Target and endpoint

- target: `Tubb3`
- focal cell class: `151 TH Prkcd Grin2c Glut`
- endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- prediction: `1`

## Evidence used

The declared biology bundle showed that `Tubb3` is well expressed in the focal
population: 23,097 of 23,679 matched non-targeting nuclei expressed the gene
(`97.54%`), with mean raw UMI `7.31` and mean CP10k `4.40`. This made a
self-transcript call plausible if a functional edit reduced newly transcribed
`Tubb3`. The same bundle also argued against a large downstream program:
TUBB3 is a beta-tubulin incorporated into alpha/beta heterodimers and the
microtubule lattice, but the operative microtubule pool contains other
beta-tubulin isotypes; germline adult neural `Tubb3` loss preserved pan
beta-tubulin levels and baseline neural function through compensation, while
the acute P16-to-P37/P44 thalamic timing of that compensation is not directly
known.

The focal training count table contained 1,674 non-target rows. Its distribution
was zero-inflated and skewed: 1,205 rows had `n_degs = 0`, the median was `0`,
the 75th percentile was `1`, the 90th percentile was `2`, and the top large
responses were spliceosome, proteostasis, or regulatory genes rather than
structural tubulin genes.

The closest measured tubulin and microtubule perturbations in the same focal
class were sparse:

| comparator | focal `n_degs` |
| --- | ---: |
| `Tubb4b` | 1 |
| `Tubb5` | 1 |
| `Tuba4a` | 2 |
| `Tuba1a` | 7 |
| `Map1b` | 1 |
| `Mapt` | 1 |
| `Stmn2` | 1 |

The expression Parquet confirmed the same focal pattern at gene level. `Tubb4b`
and `Tubb5` each had only their own transcript below FDR `0.05` in
`151 TH Prkcd Grin2c Glut` despite strong self decreases
(`Tubb4b` logFC `-0.60`, adjusted `p = 1.07e-07`; `Tubb5` logFC `-1.48`,
adjusted `p = 7.71e-23`). `Tuba1a` was the main exception: the focal class had
the `Tuba1a` self row plus up-regulation of `Tubb3`, `Tubb2a`, `Tuba4a`,
`Tubb4a`, `Tubb4b`, and `Tubb5` at FDR `0.05`.

The same-experiment corpus supported interpreting those rows as a real
isotype-specific contrast rather than a power artifact. Packaged findings
reported that `Tubb4b` was transcriptionally buffered across recovered neuronal
groups, that `Tubb5` self-decrease was often uncoupled from tubulin paralog,
p53, ISR, or UPR induction, and that `Tuba1a`, not the assayed beta-tubulin
targets, elicited the multi-tubulin feedback state in `151 TH Prkcd Grin2c Glut`
and Pvalb neurons.

## Synthesis

`Tubb3` should be assayed in nearly every focal nucleus and its own transcript is
high enough that the self row can plausibly cross FDR. The dominant uncertainty
is functional and post-transcriptional: a disruptive edit removes new TUBB3
protein supply but does not poison pre-existing soluble or lattice-incorporated
tubulin, and compensation by other beta-tubulin isotypes makes a large
downstream nuclear RNA state unlikely in the 3-4 week postmitotic window.

The selected training perturbations therefore pulled the forecast away from the
global zero mode but kept it close to the beta-tubulin and MAP self-only rows.
I treated the `Tuba1a` multi-paralog response as a narrow alpha-tubulin exception
and did not project its 7-gene count onto `Tubb3`. The resulting point forecast
is one FDR-significant measured gene: the `Tubb3` self transcript, with no robust
non-self program.
