# Held-out DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

I interpreted the task as a scalar point prediction for each held-out CRISPR
loss-of-function target: the number of measured genes whose Wilcoxon
Benjamini-Hochberg-adjusted p-value would fall below 0.05 in the focal
`151 TH Prkcd Grin2c Glut` thalamic glutamatergic class. The target set for
this run contains one held-out perturbation, `Thbd`, and that perturbation is
absent from both the differential-expression Parquet and the focal training
DEG-count table. Requested-target order was therefore simply:

| target_name |
| --- |
| Thbd |

The endpoint is directly observed for the 1,674 non-held-out training
perturbations in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`; it is absent for `Thbd`.
The held-out prediction is therefore a transfer from the visible DEG counts and
visible expression signatures, not a readout of `Thbd` itself.

## Sources used

- Held-out manifest:
  `single-target request for Thbd`.
- Direct focal training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Differential-expression signatures from the declared Parquet:
  `training differential-expression dataset`.
- Run-local dataset portrait, measurement registry, task bindings, and coverage
  summaries under `codex_runtime/pipeline/`.
- PubMed literature records retrieved through NCBI E-utilities for the biology
  of thrombomodulin/protein C and TAM/protein-S signaling.
- The PerturbAI July 260713 same-experiment corpus coverage index was checked
  as run-local metadata. It did not provide a target-matched `Thbd` report in
  this run and was not used as independent endpoint evidence.

I did not use the same-experiment graph or multiplicity as a score. This is a
scalar DEG-count task with no ranked supervision, so the rank-calibration,
predictive graph-review, and ordering-validation capabilities were not
available or used.

## Quantitative calibration from visible perturbations

I first read the focal training count CSV and the held-out manifest. The focal
training endpoint is very sparse:

| quantity over visible targets | value |
| --- | ---: |
| training perturbations | 1,674 |
| `n_degs = 0` | 1,205 |
| `n_degs > 0` | 469 |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2,677 |

The default prior for an unsupported held-out perturbation in this cell class
is therefore zero or nearly zero, but I did not stop at that bulk rate. I next
looked for mechanistically nearby visible perturbations.

`THBD` encodes thrombomodulin, an endothelial transmembrane receptor that binds
thrombin and converts thrombin toward activation of protein C; activated
protein C, with protein S, limits factors Va and VIIIa and also signals through
endothelial protein C receptor and PAR-1 in endothelial/inflammatory settings
(Esmon 2003, DOI `10.1378/chest.124.3_suppl.26s`; Dahlback and Villoutreix
2005, DOI `10.1016/j.febslet.2005.03.001`). Modern reviews likewise place the
thrombomodulin/protein-C system on endothelial surfaces as part of vascular
coagulation homeostasis (Neubauer and Zieger 2021,
DOI `10.1007/s00441-021-03471-2`). Protein S is also a ligand for the TAM
receptors AXL, MERTK, and TYRO3, connecting this coagulation branch to
efferocytosis and inflammation rather than to a known thalamic glutamatergic
transcriptional complex (van der Meer et al. 2014,
DOI `10.1182/blood-2013-09-528752`).

Exact protein-C-pathway perturbations that would have been the best visible
comparators, such as `Proc`, `Procr`, `Pros1`, `F2r`, `F2rl1`, `F2rl2`, `F3`,
and `Tyro3`, were not in the supplied focal training-count table. I therefore
used the closest visible counterexamples: TAM receptors related through
protein-S signaling, endothelial/vascular receptor genes, and innate-immune or
hematopoietic receptors whose normal function is outside the recovered NeuN+
thalamic neurons.

For each candidate below I read its focal rows from the Parquet and counted
FDR-significant measured genes. Each had 17,259 measured genes in the focal
class and no adjusted-significant gene:

| visible perturbation | relationship tested | training `n_degs` | focal Parquet evidence |
| --- | --- | ---: | --- |
| `Axl` | TAM receptor activated by protein S/Gas6; closest visible protein-S-adjacent branch | 0 | 0 genes with `pvals_adj < 0.05`; smallest adjusted p-value 0.363 |
| `Mertk` | TAM receptor and efferocytosis/inflammation receptor | 0 | 0 genes with `pvals_adj < 0.05`; smallest adjusted p-value 0.888 |
| `Kdr` | VEGF receptor, endothelial/vascular receptor tyrosine kinase | 0 | 0 genes with `pvals_adj < 0.05`; smallest adjusted p-value 1.0 |
| `Flt4` | VEGF-C/VEGF-D vascular receptor | 0 | 0 genes with `pvals_adj < 0.05`; smallest adjusted p-value 0.363 |
| `Tek` | endothelial angiopoietin receptor Tie2 | 0 | 0 genes with `pvals_adj < 0.05`; smallest adjusted p-value 1.0 |
| `Eng` | endothelial TGF-beta coreceptor/endoglin | 0 | 0 genes with `pvals_adj < 0.05`; smallest adjusted p-value 1.0 |
| `Csf1r` | myeloid/microglial receptor, a non-neuronal immune counterexample | 0 | 0 genes with `pvals_adj < 0.05`; smallest adjusted p-value 1.0 |
| `Cx3cr1` | microglial chemokine receptor, a non-neuronal immune counterexample | 0 | 0 genes with `pvals_adj < 0.05`; smallest adjusted p-value 1.0 |
| `Mpl` | hematopoietic cytokine receptor, a blood-lineage counterexample | 0 | 0 genes with `pvals_adj < 0.05`; smallest adjusted p-value 1.0 |

I also queried the measured transcript `Thbd` across all 1,674 visible focal
training perturbations. No visible perturbation significantly changed `Thbd`
itself at FDR 0.05 in the focal class. Several rows had pseudocount-driven
extreme log-fold changes for very low counts but adjusted p-values of 1.0; I
treated those as non-evidence, consistent with the dataset portrait's warning
that low-expression log-fold changes are unstable.

## Target-specific biological prediction

### `Thbd`

The observed focal endpoint for the closest visible training perturbations is
uniformly zero. The TAM receptors `Axl` and `Mertk` are the best available
within-dataset tests of a protein-S-adjacent inflammatory branch; both are
complete focal zeros. The vascular receptors `Kdr`, `Flt4`, `Tek`, and `Eng`
test whether acute CRISPR against endothelial-surface biology tends to induce a
large cell-autonomous survivor-state in these NeuN+ thalamic glutamatergic
neurons; each is also a complete focal zero. Microglial or hematopoietic
surface receptors, `Csf1r`, `Cx3cr1`, and `Mpl`, provide weaker but directionally
similar negative counterexamples for genes whose primary in-vivo activity is
outside the assayed neuronal population.

Biologically, a strong response to `Thbd` in this assay would require one of
two events: either appreciable THBD function within postmitotic
`151 TH Prkcd Grin2c Glut` neurons, or a non-cell-autonomous vascular/coagulation
effect that propagates into sparsely edited, recovered thalamic neurons strongly
enough to produce dozens of within-class Wilcoxon discoveries. The external
literature instead identifies thrombomodulin as an endothelial thrombin/protein
C receptor in vascular homeostasis, while the input experiment FACS-enriched
NeuN+ nuclei and intentionally under-sampled endothelial, microglial, and other
non-neuronal populations. Cell-type atlas work such as Tabula Muris also
supports endothelial cells as a cross-organ transcriptional cell type distinct
from neurons (Tabula Muris Consortium 2018, DOI `10.1038/s41586-018-0590-4`).

That causal chain makes a broad focal neuronal response unlikely:

`Thbd` CRISPR -> loss of endothelial thrombomodulin/protein-C activity would be
the canonical direct molecular consequence, but the perturbation is assayed in
recovered NeuN+ thalamic glutamatergic nuclei -> no obligate thalamic neuronal
complex or required same-cell pathway partner is known -> visible endothelial,
TAM/protein-S-adjacent, microglial, and hematopoietic receptors all had
`n_degs = 0` in the focal class -> the expected number of FDR-significant genes
is zero.

I therefore predicted:

| target_name | predicted_n_degs |
| --- | ---: |
| `Thbd` | 0 |

## Limits and uncertainty

- The requested `Thbd` perturbation was fully held out, so its endpoint and
  expression signature were absent from the declared inputs. The prediction is
  a transfer from visible genes.
- The training set lacks direct `Thbd` pathway comparators `Procr`, `Proc`,
  `Pros1`, `F2r`, `F2rl1`, `F2rl2`, `F3`, and `Tyro3`; `Axl` and `Mertk` only
  test a protein-S/TAM branch, not the thrombin-thrombomodulin complex itself.
- The Parquet does not contain raw baseline expression or a guide-exposure
  denominator. I therefore did not use weak target-RNA changes or recovered
  nucleus counts as proof of editing failure or success.
- A severe vascular effect before NeuN+ recovery would be partly invisible in
  this survivor-conditioned neuronal readout. That limitation can hide biology,
  but it does not create evidence for FDR-significant thalamic glutamatergic
  DEGs in the recovered focal class.
