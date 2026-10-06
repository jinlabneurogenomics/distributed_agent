# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

I interpreted the task as a scalar prediction for the single held-out target in
`the single-target request`, `Gpr12`. The requested value is the number of assayed genes whose
Benjamini-Hochberg-adjusted Wilcoxon p-value is below 0.05 in the focal
`151 TH Prkcd Grin2c Glut` neuronal group after acute, sparse, postnatal
AAV-CRISPR loss of `Gpr12`.

`Gpr12` is absent as a `target_name` from
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` and absent as a
`gene_target` from the differential-expression parquet, so its own count and
signature are not directly observed in the supplied input. I therefore treated
the training `n_degs` values and focal-cell differential-expression signatures
of mechanistic analogs as direct evidence for this assay's response scale, and
external GPR12/G-protein literature as prior information about which training
perturbations are relevant.

## Sources used

- Declared DE dataset:
  `training differential-expression dataset`.
  I queried raw focal-cell rows for selected training targets and summarized
  FDR-significant genes, minimum adjusted p-values, nominal p-values, Wilcoxon
  scores, log-fold changes, and matched perturbed/control nucleus counts.
- Declared 151-cell training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  This table supplied the observed endpoint for 1,674 non-held-out targets.
- Requested target manifest:
  `single-target request for Gpr12`.
- Run-local metadata:
  `task_bindings.json`, `coverage.json`, `measurement_registry.json`, and
  `capabilities.json`.
- Same-experiment internal corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, especially the `Gnas` and
  `Gpr158` Finding ledger entries. This corpus is a packaged interpretation of
  the same Perturb-seq experiment, not an independent replicate.
- External literature found through NCBI PubMed:
  Uhlenbrock, Gassenhuber and Kostenis 2002, DOI
  `10.1016/s0898-6568(02)00041-4`, PMID `12220620`; Hinckley et al. 2005,
  DOI `10.1016/j.ydbio.2005.08.019`, PMID `16229830`; Tanaka et al. 2007,
  DOI `10.1074/jbc.M700911200`, PMID `17284443`; Martin, Steurer and Aronstam
  2015, DOI `10.1371/journal.pone.0138463`, PMID `26384023`; Brown, Laun and
  Song 2017, DOI `10.1016/j.bbrc.2017.09.001`, PMID `28888984`; Morales, Isawi
  and Reggio 2018, DOI `10.1080/03602532.2018.1428616`, PMID `29390908`; and
  Li et al. 2022, DOI `10.1016/j.scib.2022.12.023`, PMID `36593162`.

The target list is unranked and the task is a scalar/count prediction. The
rank-calibration workbench, predictive graph review, and ordering validator
were therefore unavailable by manifest policy and were not used.

## Quantitative calibration from the focal cell group

The 1,674 visible training targets in `151 TH Prkcd Grin2c Glut` are heavily
zero-inflated:

- median `n_degs`: 0
- 75th percentile: 1
- 90th percentile: 2
- 95th percentile: 18
- 469/1,674 targets have any FDR-significant gene

I then queried the focal-cell rows of the parquet for GPCR, G-protein, adenylyl
cyclase, PKA, phosphodiesterase, and metabotropic-glutamate training
perturbations that could plausibly bracket a constitutively active Gs-linked
receptor such as GPR12. The endpoint counts in the focal group were:

| training target | focal `n_degs` | expression-pattern evidence |
| --- | ---: | --- |
| `Gnas` | 0 | no focal FDR genes; self row `pvals_adj = 1` |
| `Adcy1` | 0 | no focal FDR genes; self row `pvals_adj = 1` |
| `Adcy3` | 0 | no focal FDR genes; self row `pvals_adj = 0.112` |
| `Adcy5` | 0 | no focal FDR genes; self row `pvals_adj = 1` |
| `Pde1c` | 0 | no focal FDR genes; minimum adjusted p-value `0.180` |
| `Pde4b` | 0 | no focal FDR genes; minimum adjusted p-value `0.922` |
| `Pde4d` | 0 | no focal FDR genes; minimum adjusted p-value `1` |
| `Pde10a` | 0 | no focal FDR genes; minimum adjusted p-value `0.304` |
| `Rgs6` | 0 | no focal FDR genes; self row `pvals_adj = 1` |
| `Gnb5` | 0 | no focal FDR genes by the training count table |
| `Rapgef2` | 0 | no focal FDR genes by the training count table |
| `Rapgef4` | 0 | no focal FDR genes by the training count table |
| `Drd2` | 0 | no focal FDR genes; minimum adjusted p-value `1` |
| `Drd4` | 0 | no focal FDR genes; minimum adjusted p-value `1` |
| `Drd5` | 0 | no focal FDR genes; minimum adjusted p-value `1` |
| `S1pr2` | 0 | no focal FDR genes; self row `pvals_adj = 1` |
| `Gpr156` | 0 | no focal FDR genes; self row `pvals_adj = 1` |
| `Gpr161` | 0 | no focal FDR genes; self row `pvals_adj = 1` |
| `Gpr179` | 0 | no focal FDR genes; self row `pvals_adj = 1` |
| `Gpr45` | 0 | no focal FDR genes; self row `pvals_adj = 1` |
| `Gprc5b` | 0 | no focal FDR genes; self row `pvals_adj = 1` |
| `Gnao1` | 1 | exactly one focal DEG, the `Gnao1` target transcript |
| `Gpr158` | 1 | exactly one focal DEG, the `Gpr158` target transcript |
| `Gprasp2` | 1 | exactly one focal DEG, the `Gprasp2` target transcript |
| `Prkaca` | 1 | exactly one focal DEG, the `Prkaca` target transcript |
| `Prkar1a` | 1 | exactly one focal DEG, the `Prkar1a` target transcript |

The focal expression-pattern evidence therefore says that the basal GPCR/cAMP
surface is nearly flat in this cell group. The few nonzero GPCR/cAMP analogs
do not show a shared downstream response: their sole FDR gene is the targeted
transcript. This matters because the requested endpoint counts the self gene if
it passes FDR, but the dataset context warns that measured self-knockdown is a
noisy CRISPR QC surface rather than an editing-strength measurement. Among all
focal rows with `names = gene_target`, 319/1,642 target transcripts passed
FDR 0.05; a one-gene self-only count is possible for `Gpr12`, but still not the
modal outcome.

The same-experiment corpus supported this quantitative interpretation. Its
`Gnas` report found that resting `Gnas` loss did not induce a canonical
cAMP/CREB immediate-early module and did not phenocopy `Gnal`, `Gnao1`,
`Adcy1`, `Adcy3`, `Adcy5`, `Pde10a`, `Pde4b`, `Pde4d`, `Prkaca`, `Prkar1a`,
`Rapgef2`, `Rapgef4`, `Creb1`, or `Crebbp`. Its `Gpr158` report found a nearly
null GPCR/RGS-scaffold transcriptome across juvenile NeuN-positive brain, with
related RGS7-complex, class-C GPCR, and cAMP-pathway perturbations failing to
phenocopy `Gpr158`. I used these reports as same-experiment interpretation of
why the direct biochemical analogs are weak transcriptional comparators, not
as independent observations.

## Target-specific reasoning

### Gpr12

External mechanism. `Gpr12` encodes an orphan class-A GPCR in the GPR3/GPR6/GPR12
subfamily. Heterologous systems showed high constitutive coupling to
adenylyl-cyclase/cAMP, with S1P-family lipids proposed as modulators by
Uhlenbrock et al. 2002 and GPR12/GPR3 involvement in rodent oocyte cAMP control
by Hinckley et al. 2005. Tanaka et al. 2007 further showed that neural
overexpression of GPR3, GPR6, or GPR12 elevates cAMP and can promote neurite
outgrowth through Gs, PKA, and RhoA; Martin et al. 2015 and Morales et al. 2018
placed GPR12 among constitutively active cannabinoid/lysophospholipid-related
orphan receptors; Brown et al. 2017 identified cannabidiol as a GPR12 inverse
agonist in a cAMP assay; and Li et al. 2022 resolved a human ligand-free
GPR12-Gs structure that explains its intrinsically high basal activity.

Training analogs. The best within-dataset proxies for losing a receptor with
basal Gs/cAMP output are loss of the Gs transducer (`Gnas`), the adenylyl
cyclases (`Adcy1`, `Adcy3`, `Adcy5`), PKA subunits (`Prkaca`, `Prkar1a`), cAMP
hydrolysis genes (`Pde1c`, `Pde4b`, `Pde4d`, `Pde10a`), and other neuronal GPCR
or GPCR-associated proteins (`Gpr158`, `Gpr179`, `Gprasp2`, `Gpr156`, `Gpr161`,
`Gpr45`, `Gprc5b`, `S1pr2`, `Rgs6`, `Gnb5`, `Drd2`, `Drd4`, `Drd5`, `Grm1`,
`Grm5`, `Grm6`, `Grm7`, `Grm8`). These are not perfect paralogs of GPR12:
`Gpr3` and `Gpr6` were not visible training targets in this count table, and
the other GPCRs have different ligand coupling and expression domains. They do,
however, test the relevant intervention chain:

`Gpr12` loss -> less tonic GPCR signaling through Gs/cAMP/PKA in cells that
express it -> possible CREB/immediate-early or synaptic-transcription
propagation -> postnatal thalamic glutamatergic survivor nuclei -> Wilcoxon
DEGs.

In the observed 151-cell data, the common pathway nodes upstream and downstream
of cAMP were silent or self-only. Direct `Gnas` loss had zero DEGs despite
`Gnas` being the central Gs-alpha coupling point. `Adcy1`, `Adcy3`, and `Adcy5`
also had zero DEGs; `Prkaca` and `Prkar1a` had one DEG each, but that DEG was
only the perturbed target transcript. `Creb1` and `Crebbp` were modestly
nonzero at 10 and 8 DEGs, showing that the assay can detect transcriptional
rewiring when a nuclear CREB-axis perturbation is actually reached, but the
membrane receptor/G-protein/cAMP perturbations did not propagate to that state.

Zero/nonzero decision. `Gpr12` has a stronger basal cAMP rationale than a
purely ligand-gated GPCR, so I did not treat arbitrary receptor zeros as
sufficient by themselves. The decisive within-dataset evidence is that the
basal cAMP pathway around `Gnas` and the adenylyl cyclases is itself
transcriptionally buffered in this cell group. Sparse P16 CRISPR loss of one
orphan receptor is likely to have smaller and more cell-state-restricted
effects than loss of the shared `Gnas` or `Adcy` nodes. A self-transcript-only
hit could make the integer one rather than zero, because `Gpr12` is detectable
as a measured gene in the focal group in the training parquet; however, the
empirical self-gene FDR rate is low enough, and unrelated GPCR self rows such
as `Gpr156`, `Gpr161`, `Gpr179`, `Gpr45`, and `Gprc5b` all failed FDR, that I
did not assign a guaranteed self DEG.

My point prediction for `Gpr12` is therefore `0` DEGs in `151 TH Prkcd Grin2c
Glut`.

## Limits and extrapolation

The requested endpoint is assay- and power-dependent, and the hidden `Gpr12`
signature is absent from the declared input. The conclusion is driven mainly
by the within-dataset flatness of cAMP/GPCR analogs in the focal thalamic
population; the exact `Gpr12` self-transcript response is the main remaining
uncertainty. External GPR12 literature mostly uses heterologous overexpression,
oocytes, structural biochemistry, or cultured neurons, which establish a
Gs/cAMP mechanism but do not prove that acute mosaic loss in postnatal mouse
thalamic glutamatergic neurons creates a broad steady-state nuclear RNA
signature. Conversely, a predicted zero here should not be read as absence of
GPR12 protein function, cAMP coupling, electrophysiological effects, or
behavioral relevance.
