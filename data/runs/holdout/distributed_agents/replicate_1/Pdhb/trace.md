# DEG-count prediction for Pdhb in 151 TH Prkcd Grin2c Glut

## Question and endpoint

The requested held-out target is `Pdhb`. I treated the requested value as the
integer number of measured genes with `pvals_adj < 0.05` in the
`151 TH Prkcd Grin2c Glut` contrast against matched non-targeting controls.
The count includes the target transcript itself when that row passes the same
FDR cutoff, because the supplied training count table counts all measured
genes and the exact focal rows show `Pdha1` and `Dlat` each have one significant
row, their own transcript.

This is a scalar count prediction, not a ranking task. I therefore did not use
the rank-calibration workbench, graph-review, or ordering-validation tools,
which the run-local capability manifest marked unavailable for this endpoint.

## Sources used

- Declared DEG-count supervision:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression parquet:
  `training differential-expression dataset`.
- Requested-target manifest:
  `single-target request for Pdhb`.
- Run-local task context, input bindings, coverage summary, and capability
  manifest in `codex_runtime/pipeline`.
- Internal same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, specifically packaged Findings
  and resolved Evidence for `Pdha1`, `Dlat`, `Dld`, `Mpc1`, and `Dlst`.
- External mechanism references used to define the PDC relationship, not as
  independent measurements of this CRISPR assay:
  Patel et al. 2014, J Biol Chem, DOI `10.1074/jbc.R114.563148`, PMID
  `24798336`; Reactome reviewed 2024, "PDH complex synthesizes acetyl-CoA from
  PYR", stable identifier `R-HSA-9861559`; Ganetzky, McCormick, and Falk 2021,
  GeneReviews, NCBI Bookshelf `NBK571223`.

## Computational checks over the supplied data

The held-out manifest contains exactly one target:

| target_name |
| --- |
| Pdhb |

The training count table has 1,674 non-held-out targets. It is heavily
zero-inflated in the focal cell class: 1,205 targets are zero, 469 are nonzero,
the median is 0, the 75th percentile is 1, the 90th percentile is 2, and the
95th percentile is 18. That distribution makes one DEG a near-baseline weak
effect and makes large counts exceptional.

I queried the parquet for the exact focal-cell DE rows of represented pyruvate
dehydrogenase complex, 2-oxoacid dehydrogenase, TCA, and mitochondrial
carbon-flow comparators. At `pvals_adj < 0.05`, the most relevant rows were:

| training perturbation | relationship to Pdhb | observed focal `n_degs` | FDR<0.05 rows in the focal group |
| --- | --- | ---: | --- |
| `Pdha1` | E1 alpha partner of PDHB in PDC | 1 | `Pdha1`, log2FC -1.039, adjusted p = 1.31e-6 |
| `Dlat` | PDC E2 catalytic core | 1 | `Dlat`, log2FC -0.673, adjusted p = 2.81e-7 |
| `Dld` | shared E3 for PDC and other 2-oxoacid dehydrogenases | 0 | none; the best focal Dld row was its own transcript, adjusted p = 1 |
| `Mpc1` | mitochondrial pyruvate importer upstream of PDC | 0 | none |
| `Dlst` | E2 of the related OGDH complex | 0 | none |
| `Ogdh` | E1 of the related OGDH complex | 0 | none |
| `Bckdhb` | E1 beta of the related BCKDH complex | 0 | none |
| `Aco2` | TCA enzyme | 0 | none |
| `Idh3a` | TCA enzyme | 1 | `Idh3a` self transcript only |
| `Mdh2` | TCA enzyme | 1 | `Mdh2` self transcript only |
| `Sdha` | TCA/OXPHOS enzyme | 1 | `Sdha` self transcript only |

For the query, I filtered `group_name = '151 TH Prkcd Grin2c Glut'`, kept
rows whose `gene_target` was one of the curated comparators above, then counted
rows with `pvals_adj < 0.05`. The non-obvious point is that singleton positive
counts in this neighborhood are target-RNA effects, not coherent downstream
programs: the second-best `Dlat` row was `Jarid2` at adjusted p = 0.0577, and
the next rows for `Pdha1`, `Dld`, `Mpc1`, `Dlst`, `Aco2`, `Idh3a`, and `Mdh2`
all failed FDR 0.05.

## Same-experiment corpus evidence

The packaged `Pdha1` report states that measured PDC comparators `Dlat`, `Dld`,
and `Mpc1` were flat or nearly flat, and that related `Dlst`, `Ogdh`, `Sdha`,
and `Idh3a` perturbations were also sparse rather than forming a shared PDC or
TCA stress module. Its resolved evidence summarizes the same training-parquet
comparison: `Dlat` had 1 downstream gene over 22 groups, `Dld` had 0 over 21,
`Mpc1` had 0 over 21, `Dlst` and `Ogdh` had 2 over 22, `Sdha` had 2 over 23,
and `Idh3a` had 0 over 22 at FDR 0.10 outside self rows; `Pdhb`, `Pdhx`, `Pdk1`
to `Pdk4`, and `Pdp1`/`Pdp2` were not represented as training targets.

The packaged `Dlat` report makes the focal-cell comparison more direct:
`Dlat` had one FDR 0.10 downstream marker, `Jarid2`, in `151 TH Prkcd Grin2c
Glut`, but represented PDC, 2-oxoacid dehydrogenase, pyruvate-carrier, and TCA
comparators failed to phenocopy that `Jarid2` response in the same cell group.
The resolved evidence records 151-class signed-score cosines versus `Dlat` of
only 0.034 for `Pdha1`, 0.035 for `Dld`, 0.003 for `Mpc1`, -0.020 for `Ogdh`,
0.002 for `Aco2`, and -0.009 for `Idh3a`; `Jarid2` was FDR 1.0 in those
comparators.

The packaged `Dld` and `Mpc1` reports are important counterexamples. `Dld` is
the same E3 enzyme used by PDC, alpha-ketoglutarate dehydrogenase, and BCKDH,
yet it had zero FDR 0.10 genes across 21 measured neuronal groups and did not
induce `Atf4`, `Atf5`, `Ddit3`, `Trib3`, `Asns`, mitochondrial chaperones, or
redox genes. `Mpc1`, immediately upstream of PDC pyruvate entry, was likewise
a BH-supported transcriptomic null across 21 recovered groups. `Dlst` showed
the same pattern in the related OGDH complex: only two downstream FDR 0.10
singletons across the brain-wide surface and no coherent TCA or OGDH-complex
transcriptional module.

## Causal transfer to Pdhb

The causal chain I used was:

`Pdhb` CRISPR loss of function -> reduced PDH E1 beta function -> impaired
PDC conversion of pyruvate to acetyl-CoA -> possible changes in carbon flux,
lactate/pyruvate balance, acetyl-CoA-linked chromatin, mitochondrial stress,
or cell fitness -> survival and recovery of edited thalamic glutamatergic
nuclei -> nuclear DE row count at FDR 0.05.

Reactome and Patel et al. define PDHB as the E1 beta subunit in the same PDC
as PDHA1 and DLAT. Thus `Pdha1` and `Dlat` are the closest training analogs:
each should impair the same limiting PDC function in the same direction as
`Pdhb`. Both analogs had exactly one focal DEG at the task cutoff, and those
DEGs were the self transcript; `Dlat`'s only near-threshold downstream marker,
`Jarid2`, did not transfer to `Pdha1` or other metabolic comparators. The
appropriate transfer is therefore "same endpoint direction but very small
readout", not a broad pathway-level promotion.

`Dld`, `Mpc1`, `Dlst`, `Ogdh`, `Bckdhb`, `Aco2`, `Idh3a`, `Mdh2`, and `Sdha`
serve as counterexamples to a large metabolic-stress prediction. Some are
less direct than `Pdha1`/`Dlat`: `Dld` is reused by multiple enzyme complexes,
`Mpc1` is an importer rather than a PDC subunit, and `Dlst`/`Ogdh`/`Bckdhb`
operate in different 2-oxoacid dehydrogenase complexes. But all should have
registered a robust `Atf4`/`Ddit3`, UPRmt, lactate-handling, or TCA stress
program if this juvenile sparse CRISPR/snRNA assay were generally sensitive to
basal mitochondrial carbon-flow limitation. They did not.

## Target-specific prediction

### Pdhb

I predict `Pdhb` will be nonzero but at the one-gene floor: 1 DEG.

The zero/nonzero decision is driven by the exact PDC analogs. `Pdha1` and
`Dlat` are same-complex loss-of-function perturbations and both reached
FDR 0.05 in 151-class rows only through their own reduced transcript. `Pdhb`
should impair the same PDC step as `Pdha1`; PDHB disease is also a recognized
primary PDH-complex deficiency mechanism in GeneReviews. On the other hand,
the same-experiment downstream signatures do not support adding extra
secondary genes: `Pdha1` had no focal downstream FDR signal, the `Dlat`
`Jarid2` row was below FDR 0.10 but above the task's FDR 0.05 cutoff and was
not shared by other PDC/TCA comparators, and `Dld`/`Mpc1` were outright nulls.

So the point estimate is exactly `1`: a likely significant `Pdhb` self row or
one equivalent singleton, but no predicted broad mitochondrial, ISR, UPRmt,
lactate, or chromatin response in recovered `151 TH Prkcd Grin2c Glut` nuclei.

## Limits

`Pdhb` itself was absent from both declared inputs, so the self-transcript
component is extrapolated from `Pdha1` and `Dlat` rather than observed. The
CRISPR modality can make transcript loss and functional protein loss diverge;
`Dld` and `Mpc1` show that a mechanistically important mitochondrial target can
have no significant self row. Conversely, the assay observes only recovered
nuclear RNA 3-4 weeks after P16 editing, so the near-null training signatures
do not rule out PDH flux defects, lactate/pyruvate or acetyl-CoA changes,
electrophysiologic phenotypes, or selective loss of cells before sampling.
The final count should therefore be read as an assay-specific 151-class
FDR-count prediction, not as a statement that Pdhb loss is biologically benign.
