# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and resolved ambiguities

The requested held-out target was `Sec31a` only. I interpreted the endpoint as the exact focal-cell count used in the supplied training CSV: the number of measured genes with `pvals_adj < 0.05` after the target was perturbed in `151 TH Prkcd Grin2c Glut` neurons. The count includes the target transcript if that row passes the same FDR cutoff; it is not restricted to downstream genes.

`Sec31a` was absent as a `gene_target` from the supplied training DEG Parquet and absent from the focal training-count CSV, so its own DEG count and expression signature were not used. File order was not a rank; the requested-target file had one row, which I preserved in `answer.txt`.

## Sources

- Declared Perturb-seq training data:
  - `training differential-expression dataset`
  - `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
  - requested-target manifest `single-target request for Sec31a`
- Run-local task/dataset metadata: `task_bindings.json`, `coverage.json`, `capabilities.json`, and the PerturbAI atlas dataset portrait.
- Same-experiment semantic corpus: `perturbai-july-260713-sourceguard-1773-v1`, including Findings and bounded full reports for `Sec23a`, `Sar1b`, `Sec63`, `Copa`, and `Copg1`. This corpus is an interpreted representation of the same Perturb-seq experiment, not an independent replicate.
- External COPII literature from PubMed:
  - Haucke 2003, *Trends in Cell Biology*, DOI `10.1016/S0962-8924(02)00011-9`, PMID `12559754`.
  - Stagg et al. 2006, *Nature*, DOI `10.1038/nature04339`, PMID `16407955`.
  - Townley et al. 2008, *Journal of Cell Science*, DOI `10.1242/jcs.031070`, PMID `18713835`.
  - Routledge, Gupta and Balch 2010, *Molecular Membrane Biology*, DOI `10.3109/09687688.2010.524894`, PMID `21054154`.
  - Reactome pathway `COPII-mediated vesicle transport`, R-HSA-204005, used as pathway-definition context for the canonical Sar1/Sec23-Sec24/Sec13-Sec31 ER-exit machinery.

## Computation over the supplied training set

I first calibrated the scalar endpoint from the focal training CSV rather than building a ranked workbench: this run has no ranked or partially ranked supervision, and `dataset.perturbseq_features`, `corpus.predictive_graph_review`, and `synthesis.ordering_validate` were disabled by the capability manifest for this task type.

The focal training distribution had 1,674 non-held-out biological targets:

| statistic | `n_degs` |
|---|---:|
| mean | 14.05 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2677 |

Thus a zero prediction is the baseline for a target unless the held-out gene maps to a strong, assayed responder module.

I then queried the focal rows for COPII and adjacent ER/Golgi-traffic targets represented in training. The query grouped only `group_name = '151 TH Prkcd Grin2c Glut'` rows and counted `pvals_adj < 0.05`; it also checked a fixed UPR/ER-stress panel (`Hspa5`, `Hsp90b1`, `Pdia4`, `Hyou1`, `Herpud1`, `Dnajb9`, `Atf4`, `Ddit3`, `Xbp1`, `Chac1`, `Asns`) and a small COPII-transcript panel (`Sec13`, `Sec23a`, `Sec24d`, `Sec31a`, `Sar1b`).

| training target | focal perturbed nuclei | observed `n_degs` | minimum focal q | ER-stress panel q<0.05 | COPII panel q<0.05 |
|---|---:|---:|---:|---:|---:|
| `Sec23a` | 307 | 0 | 0.8735 | 0 | 0 |
| `Sar1b` | 112 | 0 | 0.1085 | 0 | 0 |
| `Sec63` | 72 | 11 | 0.000631 | 3 | 0 |
| `Copa` | 75 | 0 | 0.3644 | 0 | 0 |
| `Copg1` | 234 | 1 | 9.24e-17 | 0 | 0 |
| `Tango2` | 188 | 0 | 1 | 0 | 0 |

The most important exact focal rows were:

- `Sec23a`: the strongest row was the `Sec23a` target transcript itself, logFC -0.351, Wilcoxon p `5.06e-05`, q `0.8735`; every measured gene was nonsignificant. `Hspa5`, `Pdia4`, `Hyou1`, `Herpud1`, `Ddit3`, `Atf4`, `Xbp1`, `Hsp90b1`, `Sec31a`, `Sec13`, `Sec24d`, and `Sar1b` all had q = 1.
- `Sar1b`: the strongest row was the `Sar1b` target transcript, logFC -0.615, p `6.29e-06`, q `0.1085`; every downstream and every UPR/COPII marker row was nonsignificant.
- `Sec63`: in the same cell group and with fewer perturbed nuclei, `Sec63` induced a detectable ER-stress/chaperone state: `Hspa5` q `0.000631`, `Hyou1` q `0.00876`, `Chac1` q `0.0179`, with `Pdia4` and `Hsp90b1` as near-threshold UPR markers at q `0.0688`.
- `Copa`: the closest focal rows had q `0.364` or worse, and `Hspa5`, `Herpud1`, `Ddit3`, `Atf4`, `Sec31a`, `Sec23a`, `Sec13`, `Sec24d`, and `Sar1b` were all q = 1.
- `Copg1`: the single focal DEG was the target transcript `Copg1` itself, logFC -0.668, q `9.24e-17`; there was no downstream or ER-stress response.
- `Rab7` was used only as a counterexample to a blanket "vesicle genes are flat" rule: it produced 501 focal DEGs but represents late endosomal/lysosomal trafficking rather than COPII ER export.

## Target-specific prediction

### `Sec31a`

`Sec31a` encodes an outer COPII coat component. The canonical causal chain for a strong SEC31A loss would be:

`Sec31a` CRISPR loss of function -> impaired SEC13/SEC31 outer-cage assembly at ER exit sites -> inefficient export from the ER, especially for demanding cargo -> ER client retention and a possible UPR/ISR or compensatory COPII transcriptional program -> recovered thalamic glutamatergic nuclei with FDR-significant expression changes.

External literature supports the first two links. COPII vesicle formation uses stepwise Sar1 recruitment of the Sec23/Sec24 inner coat followed by the Sec13/Sec31 outer cage (Haucke 2003, PMID `12559754`; Stagg et al. 2006, PMID `16407955`). Routledge et al. 2010 describe Sar1, Sec12, Sec23-Sec24, and Sec13-Sec31 as the minimal COPII machinery for ER exit (PMID `21054154`). Townley et al. 2008 showed that depletion of the Sec13/31 module preferentially disrupts collagen secretion and craniofacial development, placing SEC13/SEC31 loss in a high-secretory, embryonic cargo axis rather than in a generic transcriptional stress axis in all cells.

The direct Perturb-seq analogs point to little or no recovered-cell RNA response in `151 TH Prkcd Grin2c Glut`:

- `Sec23a` is the closest measured COPII coat perturbation. It is not the same subcomplex as SEC31A, but it sits directly upstream of SEC13/SEC31 recruitment. If a single core COPII lesion were sufficient to create sustained ER-export stress in these P16-edited neurons, `Sec23a` should have been a plausible responder; instead it had 307 focal perturbed nuclei, `n_degs = 0`, no UPR/ISR marker induction, and a same-experiment Finding reporting no downstream FDR response in any of the 23 measured neuronal groups.
- `Sar1b` is the small GTPase that starts the same COPII assembly chain. It has `n_degs = 0` in the focal class, no UPR/COPII marker response, and same-experiment Findings reporting no downstream response in any of 20 recovered neuronal groups. The caveat is that SAR1 has paralogs, so a `Sar1b` single perturbation can be more buffered than an obligate coat-cage defect.
- `Sec63` is a counterexample at the ER-proteostasis stage. It does not build the COPII cage; it works with the ER translocon/BiP system, so it is not a direct phenocopy. Its 11 focal DEGs nevertheless show that this cell group and snRNA-seq readout can detect an ER stress/chaperone program when a perturbation produces one. The absence of `Hspa5`, `Hyou1`, `Pdia4`, `Hsp90b1`, `Atf4`, `Ddit3`, and `Xbp1` changes after `Sec23a`/`Sar1b` therefore weighs against predicting a hidden large UPR for `Sec31a`.
- `Copa` and `Copg1` are retrograde COPI rather than anterograde COPII components, so they are weaker analogs. They are useful mainly as negative controls for the broad coatomer-stress idea: `Copa` had zero focal DEGs, and `Copg1` had only one focal DEG, its own transcript, despite acting in ER/Golgi trafficking.
- `Tango2` was another ER/Golgi-associated training gene with zero focal DEGs; because it is not the metazoan large-cargo ER-exit factor `TANGO1/Mia3`, I treated it as only a loose counterexample.
- `Rab7`, with 501 focal DEGs, prevents overgeneralization. The training data can yield a large trafficking-related state, but that late endosomal/lysosomal state is not the same direct molecular consequence as loss of the COPII outer coat.

I therefore predicted a nonresponse, `predicted_n_degs = 0`. The zero is driven mostly by within-dataset COPII evidence from `Sec23a` and `Sar1b`, reinforced by the COPI near-nulls and by the lack of a COPII/UPR marker program in those perturbations. External COPII knowledge was used to decide that `Sec23a` and `Sar1b` are mechanistically appropriate comparators for `Sec31a` and that `Sec63` is a readout counterexample rather than a same-complex analog.

## Limits

- This is an extrapolation from inner-coat and Sar1 perturbations to the SEC13/SEC31 outer cage. `Sec31a` itself, `Sec13`, `Sec31b`, and `Sec24*` paralogs were not non-held-out training perturbations in the supplied focal count table.
- `Sec31a` may have fewer redundant partners than `Sec23a` or `Sar1b`; if SEC31A is uniquely required in these neurons, the two observed COPII zeros could underpredict it.
- Conversely, the experiment is a sparse, mosaic, P16 CRISPR assay of NeuN+ nuclei recovered 3-4 weeks later. Complete biallelic loss in high-secretory embryonic or mesenchymal cells could give a much stronger COPII phenotype than this endpoint.
- snRNA-seq would not directly report ER-exit-site morphology, local dendritic secretion, secretory cargo flux, or selective death before harvest. It should, however, report a sustained UPR/ISR state in recovered cells, and the `Sec63` comparison shows that at least part of that state is detectable in the focal group.
- The prediction includes possible self-transcript significance. `Sec23a` and `Sar1b` both showed sub-FDR own-transcript decreases in the focal group, while `Copg1` counted one DEG from its own transcript only. That makes `Sec31a = 1` a plausible miss mode even if there is no downstream response; I still chose `0` because the closest COPII target-transcript rows did not pass FDR 0.05.
