# Pou6f1 forecast for `151 TH Prkcd Grin2c Glut`

## Requested target

- Manifest target: `Pou6f1`
- Endpoint: count of measured genes in `151 TH Prkcd Grin2c Glut` with Wilcoxon BH-adjusted `p < 0.05`
- Prediction: `0`

## Evidence used

The canonical Pou6f1 biology bundle supports target presence but not a strong same-context response prior. `Pou6f1` is measured in the focal class and is present in a sizable minority of control nuclei: mean raw UMI `0.646`, mean CP10k `0.414`, and `10239 / 23679 = 43.24%` of non-target nuclei expressing. A disruptive edit should stop production of intact DNA-binding POU6F1 and the free nuclear TF stock is expected to substantially decline by P37-P44 after P16 editing, but the nearest functional evidence is postnatal olfactory-bulb granule-neuron loss, not thalamic `Prkcd`/`Grin2c` glutamatergic neurons. The bundle also left latency in the exact 21-28 day window and possible class-6 buffering by `Pou6f2` unresolved.

The focal training count table is strongly sparse. In `151 TH Prkcd Grin2c Glut`, `1205 / 1674` training perturbations had `n_degs = 0`, `1481 / 1674` had `n_degs <= 1`, and the median among nonzero responses was only `1`. Thus the base rate in this endpoint favors a zero or singleton count unless either same-context biology or measured training analogues point to a broader survivor transcriptomic state.

The measured POU-family training perturbations pointed to a focal null:

| target | `151 TH Prkcd Grin2c Glut` `n_degs` |
| --- | ---: |
| `Pou6f2` | 0 |
| `Pou2f1` | 0 |
| `Pou2f2` | 0 |
| `Pou3f3` | 0 |
| `Pou3f4` | 0 |
| `Pou4f3` | 0 |
| `Pou5f1` | 0 |

The all-cell-group DE parquet gave the same qualitative picture rather than revealing that the focal class was the single quiet exception. At the task threshold, `Pou6f2` had `0` DEGs in all 23 measured classes; `Pou2f1`, `Pou2f2`, `Pou4f3`, and `Pou5f1` had `0` in every class where they were recovered; `Pou3f3` had only two singleton-class DEGs across the atlas and none in the focal class; `Pou3f4` had none at `p_adj < 0.05` in the recovered classes. The same-experiment Finding ledger summarizes the same surface at FDR 0.10: `Pou6f2` produced no downstream genes in any of 23 groups and did not reveal a generic POU-family postnatal neuronal response, while other measured POU factors were pan-buffered or near-null. I treated these reports as curated interpretations of the same experiment, not as an independent replicate.

I also checked whether the zero POU counts still hid a shared low-amplitude profile that would make Pou6f1 more likely to carry a coherent subthreshold response. A caller-declared profile comparison of the focal class across `Pou6f2`, `Pou2f1`, `Pou2f2`, `Pou3f3`, `Pou3f4`, `Pou4f3`, `Pou5f1`, `Foxp2`, `Neurod2`, and `Ncam1` found `9 / 10` nodes with no significant feature and the remaining control had one. The focal inspection rows for `Pou6f2`, `Pou2f1`, `Pou2f2`, `Pou3f3`, and `Pou3f4` each had `0 / 17259` significant features; their pairwise whole-profile Pearson and cosine values against the quiet peer set were all close to zero, with no shared significant positive or negative feature intersections.

## Synthesis

Pou6f1 has enough baseline expression and expected protein turnover that a detectable focal-class effect is biologically possible. I still forecast a null count because the evidence for a POU6F1-dependent transcription-maintenance program is displaced from the assayed thalamic neurons, the screen-wide focal endpoint is zero-inflated, and the most relevant measured family members, including the close class-6 paralog `Pou6f2`, were transcriptional nulls in exactly this P16-to-P37/P44 postmitotic neuronal assay. I did not promote the estimate to `1` for a self-transcript-only call because none of the measured POU self-gene rows in the focal parquet were BH-significant.
