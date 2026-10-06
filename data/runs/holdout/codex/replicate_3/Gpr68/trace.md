# Gpr68 n_degs forecast

## Target and endpoint

- Target: `Gpr68`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes in this class with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Point prediction: `0`

## Evidence used

### Gpr68 biology-only bundle

Source: `[local file: Gpr68.json]`

- Exact focal expression reach: `Gpr68` was detectable in `9377 / 23679` non-target nuclei in the focal class, or `39.6004898855526%`, with mean raw UMI `0.5872714219350479`, mean CP10K `0.3607139844693458`, and pseudobulk CPM `36.80638254964355`.
- Molecular operation: GPR68 is an extracellular proton-sensing GPCR that couples to heterotrimeric G-protein signaling. Related proton-sensing receptors are `Gpr4` and `Gpr65`, but the bundle reports no same-cell thalamic compensation evidence.
- Context of prior neural phenotypes: `Gpr68` loss has mouse-neural consequences in adult hippocampal physiology/behavior and in acidotic or ischemic challenge models, but these are not matched basal P16-to-P37/P44 thalamic edits.
- Functional-stock adjudication: a disruptive edit is expected to stop new receptor production while existing membrane receptor persists until internalization/degradation; meaningful depletion within 21-28 days is plausible but GPR68-specific neuronal surface-residence kinetics were not found.

### Focal-class training counts

Source: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`

- The focal-class training table contains 1,674 perturbations.
- It is strongly zero-inflated:
  - median `n_degs = 0`
  - 75th percentile `n_degs = 1`
  - 90th percentile `n_degs = 2`
  - 469 / 1,674 perturbations are nonzero
- The large upper tail is made of broad cell-essential/RNA-processing perturbations such as `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, and `U2af2`, which are not good mechanistic comparators for a basal upstream GPCR.

### Receptor and proximal signaling comparators

Source counts: focal count table above.

I used GPCRs and immediate G-protein second-messenger pathway members in the training table as low-level scale comparators:

```text
Adcy1 0
Adcy3 0
Adcy5 0
Gabbr1 1
Gabbr2 1
Gnas 0
Gpr156 0
Gpr158 1
Gpr161 0
Gpr179 0
Gpr45 0
Gprasp2 1
Gprc5b 0
Grm1 1
Grm5 0
Grm6 0
Grm7 1
Grm8 0
P2ry12 0
P2ry14 0
Plcb1 0
Prkca 0
Prkcg 1
Rgs6 0
```

These 24 focal-class comparators have median `n_degs = 0`, mean `0.2917`, and only 7 nonzero entries.

Source expression rows: `[local file: training_de_all_cell_groups.parquet]`

For the nonzero receptor/signaling comparators in `151 TH Prkcd Grin2c Glut`, the single significant row was always the perturbed gene's own transcript:

```text
Gabbr1 -> Gabbr1
Gabbr2 -> Gabbr2
Gpr158 -> Gpr158
Gprasp2 -> Gprasp2
Grm1 -> Grm1
Grm7 -> Grm7
Prkcg -> Prkcg
```

Thus the available GPCR/G-protein local training set supports at most a possible one-gene self-transcript count, not a multi-gene downstream thalamic state.

## Synthesis

`Gpr68` is expressed in the focal class and receptor depletion over the edit window is plausible, so I did not treat it as absent or unreachable. The endpoint, however, is a basal survivor-conditioned nuclear transcriptional response. GPR68's strongest documented phenotypes are hippocampal or acidotic/ischemic, and proton-sensing GPCR loss has no matched evidence for a strong transcriptional program in healthy juvenile thalamic glutamatergic neurons.

The exact training counts put receptor signaling perturbations very near the zero/one boundary in this cell class. Their rare nonzero calls are explained by self-transcript loss rather than downstream DE, while upstream receptor loss should be weaker and more context-gated than loss of shared signaling nodes such as `Gnas`, `Adcy1`, `Adcy3`, `Adcy5`, `Plcb1`, `Prkca`, or `Rgs6`, all of which were zero in the focal table.

Because a `Gpr68` self-transcript call is possible but unsupported by any target-specific measured knockdown in the declared inputs, and because the nearest biological scale comparators have a modal count of zero, the final point forecast is:

```text
0
```
