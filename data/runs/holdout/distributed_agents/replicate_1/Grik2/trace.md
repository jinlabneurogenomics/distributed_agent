# Grik2 DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

The requested prediction is the held-out value of `n_degs` for a `Grik2`
CRISPR loss-of-function perturbation in `151 TH Prkcd Grin2c Glut` neurons.
Here `n_degs` means the number of measured genes in that focal cell group whose
Wilcoxon Benjamini-Hochberg adjusted p-value is below 0.05. `Grik2` was held out
from both declared inputs, so its own focal signature and count are absent. I
therefore treated the focal training DEG counts as direct observations for
non-held-out perturbations and as the quantitative transfer basis for the
unobserved `Grik2` endpoint.

Two ambiguities were resolved as follows:

- The count includes any measured gene passing FDR 0.05, including the
  perturbed transcript itself. This matters because several receptor
  perturbations have exactly one DEG and that DEG is their own target RNA.
- I did not use self-target log-fold change as an editing-efficiency filter.
  The dataset portrait explicitly notes that target transcript decrease is not
  calibrated to DNA editing or protein loss in this mosaic CRISPR/snRNA-seq
  assay.

## Sources used

- Declared Perturb-seq Parquet:
  `training differential-expression dataset`.
- Declared focal training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared held-out target manifest:
  `single-target request for Grik2`.
- Run-local dataset portrait, task bindings, coverage summary, and measurement
  registry under `codex_runtime/pipeline/`.
- Internal same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, via the bounded
  `corpus.calibration` and `corpus.findings` operations.
- External literature from NCBI PubMed:
  Tomita and Castillo 2012, DOI `10.1113/jphysiol.2011.221101`, PMID
  `22431337`; Micheau et al. 2014, DOI `10.1002/hipo.22290`, PMID `24753134`;
  Stolz et al. 2021, DOI `10.1016/j.ajhg.2021.07.007`, PMID `34375587`;
  Dhingra et al. 2022, DOI `10.1007/978-3-031-00793-4_10`, PMID `36151381`;
  Mennesson et al. 2019, DOI `10.1038/s41386-019-0344-5`, PMID `30770891`.

The endpoint for `Grik2` itself is absent from the declared inputs by design.
The same-experiment corpus is an interpreted representation of the same screen,
not independent replication; I used it to constrain analog choice, not to score
`Grik2` by graph frequency or report coverage.

## Computation over the declared dataset

I first read the training count CSV and checked the held-out manifest. The
manifest contains a single requested target, `Grik2`, and the training table has
no `Grik2` row.

The focal count distribution was very sparse:

- 1,674 non-held-out training perturbations.
- 469 had `n_degs > 0`.
- Median `n_degs = 0`, 75th percentile `= 1`, 90th percentile `= 2`,
  95th percentile `= 18`, maximum `= 2677`.

For exact expression-pattern evidence around candidate analogs, I read only
the `151 TH Prkcd Grin2c Glut` row groups from the Parquet and recalculated
counts for receptor, scaffold, and ion-channel training perturbations as:

```python
sig = focal_rows["pvals_adj"] < 0.05
n_degs = sig.groupby(focal_rows["gene_target"]).sum()
```

The focal row groups showed a shared control pool of 23,679 matched nuclei.
Matched perturbed nuclei for the main kainate analogs were sufficient for a
thresholded call but not identical: 127 for `Grik1`, 192 for `Grik3`, 222 for
`Grik4`, and 216 for `Grik5`.

## Biologically relevant training analogs and counterexamples

`Grik2` encodes GluK2, one of the low-affinity GluK1-GluK3 kainate receptor
subunits that can form functional homomeric channels and can co-assemble with
high-affinity GluK4/GluK5 subunits; native kainate receptor kinetics are also
modulated by NETO1/NETO2 auxiliary subunits. That makes measured kainate-family
knockouts the closest within-dataset analogs. The external receptor literature
supports Grik2 as a real synaptic/circuit gene, not as a nuclear transcriptional
regulator: germline or allelic `Grik2`/GluK2 disruption affects behavior and
human GRIK2 channel variants cause neurodevelopmental disorders, but those
phenotypes are expected to propagate through receptor gating, trafficking,
synaptic transmission, and circuit adaptation before reaching any snRNA-seq
state.

Focal `151` evidence from the training counts:

| training target | focal `n_degs` | expression-pattern evidence in `151` |
|---|---:|---|
| `Grik1` | 0 | No measured gene below FDR 0.05; even the lowest adjusted p-value was 1.0. |
| `Grik3` | 0 | No focal DEG; the best focal adjusted p-value was 0.147 for `Ltbp3`, not a kainate marker. |
| `Grik4` | 0 | No focal DEG; best adjusted p-value was 0.565 for `Icmt`. |
| `Grik5` | 1 | The only focal DEG was `Grik5` itself, down at adjusted p = 4.5e-4; no downstream gene approached FDR. |
| `Gria1`/`Gria2`/`Gria3` | 0/0/0 | AMPA receptor subunit knockouts were flat in the focal group. |
| `Grid1`/`Grid2` | 1/0 | `Grid1` counted only its own transcript; `Grid2` was flat. |
| `Dlg4`, `Shank2`, `Shank3` | 1, 0, 2 | PSD/scaffold perturbations gave self-only or two-gene signatures, not a large shared postsynaptic state. |
| `Grin2a`, `Grin2b`, `Grin2d` | 1, 2, 0 | GluN2 subunits were weak in the focal class. |
| `Grin1` | 89 | `Grin1` was the clear large-response ionotropic receptor outlier, with a coordinated 151 signature including `Scg2`, `Stmn4`, `Kctd16`, `Gpm6a`, `Erc2`, `Igf1`, and `Syt11`. |

The July same-experiment corpus gave the same transfer boundary at an
FDR 0.10, all-cell-group interpretation layer. Its `Grik1`, `Grik3`, `Grik4`,
and `Grik5` reports state that the represented kainate subunits did not form a
shared RNA module: `Grik1`, `Grik4`, and `Grik5` were globally flat after
excluding target RNA, while `Grik3` had only three isolated hits in cortical
groups and no coherent activity-gene, Grin/Gria compensation, or kainate
signature. The corpus also contrasted that with NMDAR biology, where `Grin1`,
`Grin2a`, and `Grin2b` can induce activity/synaptic programs in particular
classes. This argues that receptor-family membership alone is not sufficient
to transfer the 89-DEG `Grin1` state to `Grik2`.

## Target-specific causal reasoning

### `Grik2`

My causal model is:

`Grik2` CRISPR loss of function -> reduced GluK2-containing kainate receptor
function in successfully edited neurons -> altered post- or presynaptic
kainate signaling in the subset of thalamic `Prkcd`/`Grin2c` glutamatergic
neurons that express the receptor and required partners -> 3-4 weeks of circuit
and cell-autonomous adaptation among surviving NeuN-positive nuclei -> Wilcoxon
DEGs in the recovered nuclear RNA profile.

At the molecular first step, `Grik2` is not interchangeable with the measured
high-affinity `Grik4`/`Grik5` subunits, because GluK4/5 are obligate
heteromeric partners, whereas GluK2 can form GluK2-containing channels. It is
also not an obligate core equivalent of `Grin1`: all conventional NMDARs need
GluN1, but many kainate receptors can use GluK1 or GluK3 in other assemblies.
The most appropriate same-assay prior is therefore the measured kainate group
rather than the NMDAR outlier.

That within-dataset prior is strongly sparse. `Grik1`, `Grik3`, and `Grik4`
all had zero focal DEGs; `Grik5` had one self-transcript hit and no downstream
program. The internal corpus shows that this flatness is not only a focal
artifact: across recovered cell groups the measured kainate perturbations
stayed null or nearly null at a looser FDR 0.10 threshold. Because the
`Grik5` focal count is self-only, it does not provide strong evidence that
GluK5 loss drove a broader kainate-to-nucleus state in the focal thalamic class.

The external literature prevents interpreting the prediction as a biological
null. Grik2/GluK2 knockout mice have behavioral and hippocampal network
phenotypes (Micheau et al. 2014), human GRIK2 channel variants are pathogenic
(Stolz et al. 2021), and Neto auxiliary proteins can tune GluK2-containing
kainate receptor gating and localization (Tomita and Castillo 2012; Mennesson
et al. 2019). Those data support synaptic and circuit consequences, but they do
not establish that acute sparse `Grik2` loss in juvenile thalamic glutamatergic
neurons should trigger an FDR-detectable nuclear RNA program under this screen's
power and survivor-conditioned sampling.

I therefore predicted that `Grik2` falls on the same side of the zero/singleton
boundary as `Grik1`, `Grik3`, and `Grik4`, rather than producing a
`Grin1`-like response. The point prediction is `0` DEGs.

## Limits and uncertainty

- `Grik2`, `Neto1`, `Neto2`, `Cnih2`, and `Cnih3` were not represented as
  training perturbations, so the exact GluK2/auxiliary-subunit assembly most
  relevant to native kainate receptors was partly unobserved.
- The endpoint is a thresholded, assay-powered DEG count. A prediction of zero
  means no gene is expected to pass BH FDR 0.05 in this focal cell class, not
  that GluK2 loss has no electrophysiological or behavioral effect.
- The kainate subunit analogs are the best local comparators but are imperfect:
  low-affinity subunits differ in distribution and trafficking, and
  high-affinity GluK4/5 subunits require GluK1-GluK3 partners.
- Self-transcript hits were common among weak receptor signatures, so the
  prediction is cutoff-sensitive. If the held-out `Grik2` target RNA were
  measurably depleted in this thalamic class, the hidden count could easily be
  a singleton despite no downstream response.
