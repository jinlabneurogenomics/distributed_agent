# DEG-count prediction trace

## Question and endpoint

The requested target set contains one held-out perturbation, `Hes7`. I interpreted
the task as a point prediction for the number of measured genes that would pass
`pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` nuclei if `Hes7` had been
included in the acute AAV-CRISPR Perturb-seq screen. `Hes7` itself is absent as
a perturbation from both the DE Parquet and the focal training count CSV, so its
own signature is not directly observed; the endpoint is directly observed only
for the 1,674 non-held-out training targets.

The requested output is a scalar count, not a ranking. I therefore did not use
the rank-calibration, graph-review, or ordering-validation workbenches, which
the run-local capability manifest also marked unavailable for this unranked
DEG-count task.

## Sources used

- Declared training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression table:
  `training differential-expression dataset`.
- Run-local measurement registry and coverage summaries under
  `codex_runtime/pipeline/`.
- Same-experiment internal corpus:
  `perturbai-july-260713-sourceguard-1773-v1`. I used it only as packaged
  interpretation of the same Perturb-seq experiment, principally the `Notch1`
  report finding that canonical HES/HEY/NICD-RBPJ-MAML Notch targets were not
  recovered after `Notch1` perturbation in the sampled neuronal groups. This is
  not independent replication of the Parquet.
- Independent biological literature retrieved through NCBI PubMed:
  Bessho et al. 2001, DOI `10.1046/j.1365-2443.2001.00409.x`, PMID `11260262`;
  Bessho et al. 2003, DOI `10.1101/gad.1092303`, PMID `12783854`;
  Ohtsuka et al. 1999, DOI `10.1093/emboj/18.8.2196`, PMID `10205173`;
  Kageyama et al. 2012, DOI `10.1002/wdev.46`, PMID `23799565`;
  Hayashi et al. 2018, DOI `10.1074/jbc.RA118.003728`, PMID `29895619`;
  Sparrow et al. 2008, DOI `10.1093/hmg/ddn272`, PMID `18775957`.

## Quantitative calibration from the supplied data

The focal training table has 1,674 non-held-out targets. Its distribution is
mostly zero or near-zero:

| summary | value |
|---|---:|
| zero-DEG targets | 1,205 / 1,674 |
| one-DEG targets | 276 / 1,674 |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| mean | 14.05 |
| max | 2,677 |

The mean is dominated by a small high-yield tail, so a biologically unsupported
target should not be assigned a nonzero count just because some perturbations
produce broad transcriptional states in this cell class.

I then scanned only the focal cell group in the Parquet for `Hes7`-related
available training perturbations and recomputed
`sum(pvals_adj < 0.05)` to confirm the focal counts and inspect boundary
significance. The closest available Notch/segmentation-clock genes were:

| training perturbation | relationship to `Hes7` | `n_degs` in focal class | focal signature evidence |
|---|---|---:|---|
| `Notch1` | upstream canonical Notch receptor; Notch/RBPJ can activate `Hes7` in presomitic mesoderm | 0 | 17,259 measured genes, 143 matched perturbed nuclei, minimum adjusted p = 1.0 |
| `Notch2` | alternate Notch receptor | 0 | 278 matched perturbed nuclei, minimum adjusted p = 1.0 |
| `Notch4` | alternate Notch receptor | 0 | 324 matched perturbed nuclei, minimum adjusted p = 0.490 |
| `Dll1` | Notch ligand used in developmental oscillators | 0 | 250 matched perturbed nuclei, minimum adjusted p = 0.678 |
| `Tbx6` | PSM T-box input to the `Hes7` enhancer, not a postmitotic-neuron factor | 0 | 240 matched perturbed nuclei, minimum adjusted p = 1.0 |
| `Mesp2` | somitogenesis output downstream of the Notch/FGF clock | 1 | 340 matched perturbed nuclei, minimum adjusted p = 0.045 |
| `Fgfr1`, `Fgfr2`, `Fgfr3` | FGF inputs to PSM Hes7-clock circuitry | 0, 0, 0 | each had no focal FDR-significant gene |
| `Neurod1`, `Neurod2`, `Neurog3` | bHLH developmental factors, more distant than HES/Notch | 0, 0, 0 | each had no focal FDR-significant gene |
| `Tcf3`, `Tcf4`, `Tcf12`, `Tcf20` | E-protein / TCF-family transcriptional comparators, not direct Hes7-clock paralogs | 0, 0, 0, 0 | each had no focal FDR-significant gene |

Two Wnt-associated counterexamples, `Ctnnb1` and `Tcf7l2`, had broad focal
responses of 383 and 106 DEGs respectively. I treated them as counterexamples
rather than `Hes7` analogs: beta-catenin and TCF7L2 are broadly used signaling
and transcriptional regulators in neurons, whereas mouse `Hes7` is a much more
restricted oscillatory bHLH repressor in presomitic mesoderm. Hayashi et al.
show that Wnt/T-box/RBPJ inputs cooperate at a PSM-specific `Hes7` enhancer, so
adult neuronal `Ctnnb1` loss is not expected to phenocopy `Hes7` loss in the
same direction.

As a measured transcript, `Hes7` was present in the Parquet across the 1,674
training perturbations in this focal class, but it was never an FDR-significant
DE gene. I did not use its very large nonsignificant log-fold changes as effect
evidence because the dataset portrait warns that large fold changes for weakly
detected transcripts can be pseudocount-dominated.

## Target-specific reasoning

### `Hes7`

`Hes7` encodes a HES-family basic helix-loop-helix transcriptional repressor.
Bessho et al. identified mouse `Hes7` as a Notch-regulated repressor expressed
specifically and dynamically in presomitic mesoderm, and Bessho et al. later
showed that HES7 autorepression and rapid protein turnover are core to the
segmentation clock. Human HES7 variants cause spondylocostal dysostosis by
disrupting this Notch-linked segmentation program, which anchors the gene's
validated disease biology in axial mesoderm rather than in mature thalamic
glutamatergic neurons.

The neuronal Notch prior points mostly to `Hes1` and `Hes5`: Ohtsuka et al.
showed that HES1/HES5 mediate Notch inhibition of mammalian neural precursor
differentiation. That does not transfer strongly to `Hes7`, whose robust
enhancer logic requires a PSM combination of E-box, T-box/TBX6, and RBPJ sites
and is repressed by PSM factors including HES7 itself. In the supplied screen,
loss of upstream receptors `Notch1`, `Notch2`, `Notch4` and ligand `Dll1`
caused no focal DEGs, arguing that acute sparse disruption of canonical Notch
components did not reveal a HES7-like fate-maintenance program in recovered
`151 TH Prkcd Grin2c Glut` nuclei. The internal July corpus reached the same
same-experiment interpretation for `Notch1`: canonical HES/HEY/RBPJ/MAML target
responses were absent in the neuronal screen.

The segmentation-clock comparators available in training also point to a null
or at most singleton response. `Tbx6` and the three FGF receptors had zero
focal DEGs, and `Mesp2` had exactly one. More distant developmental bHLH genes
such as `Neurod1`, `Neurod2`, and `Neurog3` were also zero. These are imperfect
analogs because they are not paralogous HES repressors, but they are useful
negative controls for the idea that every developmental transcription-factor
knockout is conspicuous in this assay.

Given the endpoint's high zero mass in training, the absence of a directly
assayed close HES paralog, and the strong external evidence that `Hes7`
function is normally confined to an embryonic presomitic-mesoderm oscillator, I
predict no FDR 0.05 transcriptional response in postnatal thalamic
glutamatergic cells after acute `Hes7` loss.

Prediction: `Hes7 -> 0`.

## Limits and uncertainty

This prediction is an extrapolation. The screen does not contain `Hes1`,
`Hes5`, `Rbpj`, `Lfng`, or `Dll3` as training perturbations in this focal
endpoint, so the closest HES-family and several segmentation-clock perturbation
analogs are missing. The available Notch receptors and `Dll1` are upstream
components rather than the HES7 transcriptional repressor itself, and a
cell-autonomous viral knockout of a lowly expressed transcription factor is not
identical to disrupting ligand/receptor signaling between cells. The endpoint
also counts BH-significant genes among recovered nuclei; it can miss phenotypes
that affect survival, abundance, synaptic physiology, or a rare anatomical
subset without creating a broad recovered-nucleus RNA signature. Despite those
limitations, both the training data and the external developmental biology
make a zero count more likely than a nonzero response.
