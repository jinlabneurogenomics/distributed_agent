# DEG-count prediction trace

## Question and endpoint alignment

The held-out target in this run is `Col25a1`.  I interpreted the task as a point
prediction of the exact focal endpoint used in the training CSV: the number of
measured transcripts with `pvals_adj < 0.05` after acute mosaic CRISPR loss of
function in `151 TH Prkcd Grin2c Glut` neurons.  The endpoint is directly
observed for the 1,674 training perturbations and absent for `Col25a1`, whose
own DE rows and count were removed from both declared inputs.

One ambiguity is whether the perturbed target transcript itself is included in
`n_degs`.  The training data show that it is: in the focal Parquet slice,
`App` has exactly one FDR < 0.05 row, and that row is the `App` self-transcript
with logFC -1.420 and FDR 8.41e-58.  Therefore a biologically flat perturbation
can still have `n_degs = 1` if its own RNA is expressed and depleted.

## Sources used

- Declared focal training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared DE Parquet:
  `training differential-expression dataset`.
- Requested-target manifest:
  `single-target request for Col25a1`.
- PerturbAI July `260713` same-experiment Finding/report-evidence corpus.  I
  used it for packaged interpretations of training perturbations only; this is
  not independent replication of the Parquet.
- NCBI PubMed E-utilities literature search for `COL25A1` / collagen XXV.

The scalar count task had no supplied ranked or partially ranked supervision, so
I did not invoke `dataset.perturbseq_features`, `corpus.predictive_graph_review`,
or `synthesis.ordering_validate`, all of which were unavailable for this task.

## Dataset calculations

I loaded the one requested target and the training CSV with `pandas`.  The focal
training distribution is sparse: 1,205 of 1,674 training targets have 0 DEGs
and 1,481 of 1,674 have at most 1 DEG.  This made a low count the null prior,
but I did not use the marginal distribution alone for the final target call.

For biologically relevant visible analogs I queried the focal rows of the DE
Parquet with DuckDB:

```sql
SELECT gene_target,
       COUNT(*) AS rows,
       SUM(CASE WHEN pvals_adj < 0.05 THEN 1 ELSE 0 END) AS n_degs_005,
       SUM(CASE WHEN pvals_adj < 0.10 THEN 1 ELSE 0 END) AS n_degs_010,
       MIN(pvals_adj) AS min_padj,
       ANY_VALUE(n_pert_matched) AS n_pert_matched,
       ANY_VALUE(n_ctrl_matched) AS n_ctrl_matched
FROM read_parquet(...)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
GROUP BY gene_target;
```

Each queried focal perturbation had 17,259 tested genes.  The directly relevant
focal counts and expression evidence were:

| training perturbation | biological relationship to `Col25a1` | focal `n_degs` | focal expression-pattern evidence |
| --- | --- | ---: | --- |
| `App` | collagen XXV/CLAC binds amyloid-beta and has been tied to APP biology | 1 | the only FDR < 0.10 focal row was `App` itself; best downstream FDR was 0.171 |
| `Adam10` | alpha-secretase for APP processing | 0 | no focal row at FDR < 0.10; `Col25a1` measured-gene row FDR 1 |
| `Psen1` | catalytic gamma-secretase component in APP processing | 0 | no focal row at FDR < 0.10; `Col25a1` measured-gene row FDR 1 |
| `Ptprd` | LAR-family receptor tyrosine phosphatase related to collagen XXV receptor biology | 0 | no focal row at FDR < 0.10; min focal FDR 0.143 |
| `Ptprf` | LAR-family receptor tyrosine phosphatase; nearest represented relative of PTP sigma/delta signaling | 0 | no focal row at FDR < 0.10 |
| `Dag1` | neuronal ECM receptor and dystroglycan complex core | 0 | no focal row at FDR < 0.10 |
| `Itgb1` | major ECM/integrin receptor for neuronal matrix adhesion | 0 | no focal row at FDR < 0.10 |
| `Lrp1` | neuronal lipoprotein/APP trafficking receptor context | 0 | no focal row at FDR < 0.10 |
| `Col11a1`, `Col2a1` | represented collagen perturbations | 0, 0 | both had no focal row at FDR < 0.10 |
| `Chn1`, `Mafb`, `Hoxa1`, `Ebf3` | represented cranial dysinnervation / axon-guidance / developmental-neuron genes | 0 each | all had no focal row at FDR < 0.10 |

The same-experiment App report added an important cross-cell check: across
371,796 tested non-`App` rows, `App` loss produced no downstream FDR < 0.10
gene in any recovered neuronal class despite broad `App` self-transcript
depletion.  Packaged reports for `Chn1`, `Dag1`, `Ebf3`, `Hoxa1`, `Ptprd`, and
`Ptprf` likewise described pan-measured or near-pan-measured downstream nulls.

## Target-specific reasoning

### `Col25a1`

Collagen XXV is a membrane-associated collagen with strong developmental motor
axon biology.  Germline `Col25a1` knockout mice die at birth with failed
intramuscular motor-axon elongation/branching and secondary loss of spinal
motoneurons (Tanaka et al. 2014, DOI 10.1523/JNEUROSCI.2440-13.2014, PMID
24453327).  Munezane et al. found that muscle-derived collagen XXV can interact
with PTP sigma/delta and guide intramuscular motor innervation (2019, DOI
10.1016/j.celrep.2019.11.112, PMID 31875546).  Human recessive `COL25A1`
variants cause congenital cranial dysinnervation or arthrogryposis phenotypes
consistent with this developmental wiring role (Shinwari et al. 2014, DOI
10.1016/j.ajhg.2014.11.006, PMID 25500261; Natera-de Benito et al. 2022, DOI
10.1002/humu.24333, PMID 35077597).

That biology raises a real prior for axon guidance and APP/ECM interactions, but
the causal chain is mismatched to this held-out endpoint.  The strongest
published phenotypes follow constitutive embryonic loss and depend heavily on
muscle-target innervation, whereas the Perturb-seq intervention is sparse P16
CRISPR in recovered NeuN+ postmitotic brain nuclei and the requested cell class
is thalamic glutamatergic, not an embryonic cranial or spinal motoneuron pool.
The dataset-visible perturbations that hit analogous stages of the chain were
flat: LAR-family phosphatases `Ptprd`/`Ptprf`, APP-processing genes
`App`/`Adam10`/`Psen1`, ECM receptors `Dag1`/`Itgb1`, and developmental
axon-guidance or cranial dysinnervation genes `Chn1`, `Mafb`, `Hoxa1`, and
`Ebf3` were all null in the focal class.  For `App`, the one counted DEG was the
target transcript itself and the same-experiment corpus showed no downstream
APP-family or AICD/secretase-feedback transcriptional program; APP-family
partial redundancy also makes single-gene APP perturbation mild relative to
compound loss (Heber et al. 2000, PMID 11050115).

An opposite prior comes from COL25A1 gain of function: neuronal over-expression
of human COL25A1 in transgenic mice increased BACE1, A beta deposition, and
astrocyte activation (Tong et al. 2009, DOI 10.1007/s10048-009-0201-5, PMID
19548013).  I treated this as weak counterevidence only.  It is an
over-expression/amyloid model with glial and plaque endpoints, not a sparse
postnatal loss-of-function measurement in thalamic neurons, and the represented
APP-processing perturbations in the training dataset were focal transcriptomic
nulls.

The final estimate is therefore `0`.  I expect acute `Col25a1` loss to be
either silent in this cell class or below the Wilcoxon/FDR detection threshold.
I also predict no counted self-DEG: `Col25a1` was measurable but not modulated
by any of the focal analog perturbations queried, the represented collagen
targets `Col11a1` and `Col2a1` did not self-deplete significantly in this focal
class, and the known collagen XXV developmental phenotype does not imply high,
stable postnatal `Col25a1` nuclear expression in `151 TH Prkcd Grin2c Glut`.

## Limits

This is an extrapolation from related but imperfect perturbations; there is no
visible same-experiment `Col25a1` signature.  The best mechanistic literature is
about developmental motor innervation, muscle-derived ligand activity, or APP
amyloid biology, none of which exactly matches acute loss in juvenile thalamic
glutamatergic neurons.  The declared Parquet provides differential expression
but not raw expression, guide indels, protein loss, collagen XXV shedding,
amyloid-beta binding, axon morphology, or depletion of pre-assay vulnerable
cells.  Severe selection or a structural synaptic phenotype could therefore be
missed by the recovered-nucleus DEG count.  Within those limits, the visible
APP/secretase, PTP receptor, ECM-receptor, and developmental axon-guidance
analogs all point to a zero-or-one regime, and the lack of support for a
`Col25a1` self-transcript contribution led me to choose zero rather than one.
