# Reasoning trace

## Question and endpoint

I predicted the integer `n_degs` that would have been observed for the held-out
`Trem2` perturbation in `151 TH Prkcd Grin2c Glut` neurons. Here `n_degs` is the
number of measured genes with `pvals_adj < 0.05` in the focal cell group after
acute mosaic AAV CRISPR loss of function.

I treated the endpoint as directly observed for the 1,674 training
perturbations in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, and absent for `Trem2`.
The Parquet expression signatures for held-out genes are also absent, so all
`Trem2` reasoning is transfer from non-held-out perturbations plus external
gene-function evidence.

## Sources

- Declared endpoint table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression table:
  `training differential-expression dataset`.
- Requested-target manifest:
  `single-target request for Trem2`.
- Run-local PerturbAI atlas dataset portrait, task bindings, coverage summary,
  and capability manifest. I did not use same-experiment Finding summaries to
  score `Trem2`; the scalar count endpoint was available directly from the
  supplied training CSV and Parquet for all visible analogs.
- PubMed searches for external biological priors on TREM2. Key literature:
  Jonsson et al. 2012, NEJM, DOI `10.1056/NEJMoa1211103`, PMID `23150908`;
  Guerreiro et al. 2012, NEJM, DOI `10.1056/NEJMoa1211851`, PMID `23150934`;
  Mecca et al. 2018, IJMS, DOI `10.3390/ijms19010318`, PMID `29361745`;
  Wang et al. 2022, Cell, DOI `10.1016/j.cell.2022.09.033`, PMID `36306735`;
  Pocock et al. 2024, Neuropharmacology, DOI `10.1016/j.neuropharm.2024.110020`,
  PMID `38821351`.

## Quantitative calibration from the training endpoint

The focal training endpoint is highly sparse:

- 1,674 non-held-out perturbations had training counts.
- 1,205 of 1,674, or 71.98%, had `n_degs = 0`.
- The median was 0 and the 75th percentile was 1.
- The largest responses were rare and were dominated by broad neuronal genes
  such as `Uba5` with 2,677 DEGs, `Tpr` with 1,768, and `Sin3a` with 1,433.

I then searched the focal count table for genes near the TREM2 biology:

| training perturbation | observed focal `n_degs` | relationship to `Trem2` |
| --- | ---: | --- |
| `Csf1r` | 0 | microglial survival and lineage receptor |
| `P2ry12` | 0 | homeostatic microglial purinergic receptor |
| `Cx3cr1` | 0 | microglial fractalkine receptor |
| `Mertk` | 0 | myeloid phagocytic receptor |
| `Spi1` | 0 | PU.1 myeloid/microglial transcription factor |
| `Irf8` | 0 | myeloid/microglial transcription factor |
| `Cd14` | 0 | innate-immune LPS coreceptor |
| `Axl` | 0 | TAM-family myeloid phagocytic receptor |
| `Itgb2` | 0 | leukocyte integrin component |
| `H2-Eb1` | 0 | antigen-presentation gene |
| `Tlr2` | 0 | innate-immune receptor |
| `Tlr4` | 0 | innate-immune receptor |
| `Tlr7` | 0 | innate-immune receptor |
| `Tlr8` | 0 | innate-immune receptor |
| `Pld3` | 1 | lysosomal AD-risk gene, self-transcript-only DEG |
| `Cst3` | 1 | cystatin gene expressed in glia, self-transcript-only DEG |

`Trem2`, `Tyrobp/Dap12`, `Apoe`, `Cd33`, `Clec7a`, `Lpl`, `Laptm5`, `Aif1`,
`Tmem119`, and `Mpeg1` were not available as training perturbations, so I did
not impute from an exact same-complex training target. Among the available
analog perturbations, however, every TREM2-proximal microglia or innate-immune
training target had zero focal DEGs. The two one-DEG cases, `Pld3` and `Cst3`,
were not a TREM2 receptor-complex analog and the lone FDR-significant row was
the target transcript itself (`Pld3`, adjusted p-value `2.24e-16`; `Cst3`,
adjusted p-value `1.07e-27`), not a downstream focal-neuron response.

For the Parquet expression-pattern check, I selected the 35 row groups whose
`group_name` statistics spanned `151 TH Prkcd Grin2c Glut`, then aggregated
the exact focal rows for the analog list. This verified that each listed analog
had 17,259 measured genes in the focal class and no hidden downstream
signatures at FDR 0.05: for example, `Axl`, `Cd14`, `Csf1r`, `Cx3cr1`,
`H2-Eb1`, `Itgb2`, `P2ry12`, `Spi1`, `Tlr2`, `Tlr4`, `Tlr7`, and `Tlr8` all had
minimum adjusted p-values equal to 1.0 or otherwise far above 0.05; `Irf8`
bottomed out at adjusted p-value 0.121, and `Mertk` at 0.888. The matched
perturbed-cell counts for these zero-response analogs were within the assay
range observed for the focal class, roughly 89 to 258 nuclei, so the result is
consistent with lack of a neuronal transcriptional program rather than with one
single grossly absent comparison.

## Target-specific prediction

### Trem2 -> 0

`Trem2` encodes a lipid/damage-sensing immunoreceptor best known in microglia.
Heterozygous human TREM2 variants increase Alzheimer disease risk (Jonsson
2012; Guerreiro 2012), and TREM2 signals in microglia through adaptor complexes
including TYROBP/DAP12 and downstream SYK/PI3K/AKT/mTOR pathways to control
amyloid-, lipid-, and injury-responsive microglial states (Mecca 2018; Wang
2022; Pocock 2024). That places the direct molecular consequence of `Trem2`
loss in myeloid microglia, not in thalamic glutamatergic neurons.

For the Perturb-seq causal chain, the intervention is sparse AAV CRISPR editing
in a whole-brain preparation followed by NeuN-positive neuronal nuclei
enrichment and DEG testing inside recovered `151 TH Prkcd Grin2c Glut` nuclei.
The direct loss of a microglial surface receptor is therefore expected to be
largely outside the focal sampled cell class. For `Trem2` to produce a
nonzero DEG count here, it would need enough perturbation in a non-neuronal
microglial population to alter thalamic glutamatergic neurons in trans by
P37-P44, and those altered neurons would still need to be sampled in sufficient
numbers. The training data argue against that chain producing a detectable
signature in this assay: focal knockouts of `Csf1r`, `P2ry12`, `Cx3cr1`,
`Mertk`, `Spi1`, `Irf8`, `Cd14`, `Axl`, `Itgb2`, `H2-Eb1`, and several Toll-like
receptors all had `n_degs = 0`, despite representing microglial lineage,
homeostatic, phagocytic, antigen-presentation, and innate-immune functions.

External biology increases confidence that `Trem2` can matter profoundly in
microglia under amyloid, demyelinating, aging, or injury conditions, but those
contexts are not present as required second hits in this juvenile acute
neuronal Perturb-seq screen. Broad innate-immune pathway membership therefore
does not justify promoting `Trem2` above the zero class. I predict that no
measured gene passes BH FDR 0.05 in the focal neuronal class.

## Limits

The closest obligate adaptor `Tyrobp/Dap12` and strong disease-associated
partners such as `Apoe` were held out or absent from the visible training
endpoint, so the within-dataset comparison uses neighboring microglial and
innate-immune perturbations rather than the exact TREM2 complex. The screen
under-samples non-neuronal cells after NeuN enrichment, and DEG counts are
assay- and power-dependent; a predicted zero in thalamic recovered neurons does
not mean `Trem2` is biologically inert. The external TREM2 literature is heavily
weighted toward aged, amyloid, demyelination, or injury models, whereas the
requested experiment is an acute postnatal wild-type-brain CRISPR setting.
