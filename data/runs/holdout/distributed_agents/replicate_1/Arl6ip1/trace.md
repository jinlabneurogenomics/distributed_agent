# DEG-count prediction trace

## Question and endpoint

The held-out target list contains one perturbation, `Arl6ip1`, and the required
point estimate is the number of measured genes with BH-adjusted Wilcoxon
`pvals_adj < 0.05` in the `151 TH Prkcd Grin2c Glut` class after acute
postnatal AAV CRISPR loss of function.

I treated the training count CSV as a direct observation of the same scalar
endpoint for non-held-out perturbations. The `Arl6ip1` endpoint and signature
are absent by design, so the `Arl6ip1` value is inferred from biologically
matched training perturbations, their focal-cell DEG counts and signatures, and
external knowledge of ARL6IP1 function. I did not treat the requested CSV order
as a rank, and there was no ranking supervision.

## Sources used

- Input DEG-count training CSV:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Input differential-expression Parquet:
  `training differential-expression dataset`.
- Requested-target CSV:
  `single-target request for Arl6ip1`.
- Run-local PerturbAI dataset portrait and measurement registry in
  `codex_runtime/pipeline/`, used for schema, cell-type, and measurement
  semantics.
- Internal same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, used for the `Atl1`, `Reep1`,
  `Spast`, `Sec63`, `Hspa5`, and `Atp2a2` interpreted reports. These reports
  are grounded in the same Perturb-seq experiment, so I used them as packaged
  interpretation rather than independent replication.
- External literature:
  PubMed records for ARL6IP1 ER shaping, ER-phagy, hereditary spastic
  paraplegia, and ER-microtubule HSP genes:
  Foronda et al. 2023, Nature, doi:10.1038/s41586-023-06090-9,
  PMID:37225994; Byrne et al. 2022, Acta Neuropathologica Communications,
  doi:10.1186/s40478-022-01343-6, PMID:35346366; Fowler and O'Sullivan 2016,
  Human Molecular Genetics, doi:10.1093/hmg/ddw139, PMID:27170313; Park et al.
  2010, Journal of Clinical Investigation, doi:10.1172/JCI40979,
  PMID:20200447; Yamamoto and Sakisaka 2025, Journal of Biological Chemistry,
  doi:10.1016/j.jbc.2025.108493, PMID:40209949.

## Computation

I first read the training endpoint distribution for the focal class. It is
strongly zero-inflated: 469 of 1,674 training perturbations were nonzero, the
median count was 0, the 75th percentile was 1, the mean was 14.1, and the
largest broad responders included `Uba5` at 2677, `Tpr` at 1768, and `Sin3a`
at 1433 DEGs.

I then queried only the focal-cell rows from the DE Parquet for candidate
analogs. For each candidate I counted `pvals_adj < 0.05`, recorded the matched
perturbed-cell count, listed significant genes, and computed pairwise Pearson
correlations of focal-cell Wilcoxon score vectors among analogs to distinguish
real shared programs from near-null profiles. The direct endpoint counts from
the training CSV and the focal Parquet matched for these candidates.

The most relevant focal-class training observations were:

| training target | focal `n_degs` | significant genes at FDR<0.05 | n perturbed | role in the `Arl6ip1` prediction |
|---|---:|---|---:|---|
| `Retreg1` | 1 | `Retreg1` self only | 188 | FAM134B/RETREG1 is the ER-phagy receptor that physically clusters with ARL6IP1; self-only response argues against broad ER-phagy transcription. |
| `Reep1` | 1 | `Reep1` self only | 123 | ER-shaping HSP protein related to the ARL6IP1 structural-ER phenotype; self-only in the same thalamic class. |
| `Reep2` | 1 | `Reep2` self only | 169 | closest represented REEP paralog; self-only. |
| `Atl1` | 1 | `Atl1` self only | 138 | atlastin HSP ER-tubule GTPase; self-only in the focal class. |
| `Atl3` | 0 | none | 82 | atlastin paralog with no focal DEG. |
| `Spast` | 0 | none | 141 | canonical ER-microtubule HSP comparator; no focal DEG. |
| `Tfg` | 0 | none | 118 | ER export/HSP-adjacent comparator; no focal DEG. |
| `Kif5a` | 1 | `Kif5a` self only | 204 | HSP axonal-transport comparator; self-only. |
| `Kif5c` | 1 | `Kif5c` self only | 173 | neuronal kinesin comparator; self-only. |
| `Mff` | 0 | none | 133 | mitochondrial fission comparator for the ARL6IP1/Drp1 axis; no focal DEG. |
| `Sec63` | 11 | ER-client stress genes including `Hspa5`, `Canx`, `Hyou1`, `Chac1` | 72 | counterexample showing the assay can detect a small UPR/ERAD response. |
| `Hspa5` | 5 | ER chaperone/ERAD genes including `Hsp90b1`, `Pdia4`, `Derl3` | 47 | counterexample for BiP depletion. |
| `Atp2a2` | 187 | `Atp2a2`, `Ddit3`, `Chac1`, `Xbp1`, `Herpud1`, amino-acid/one-carbon ISR genes | 98 | strong ER-calcium/UPR counterexample. |

The focal score-vector correlations among the close ER-shaping analogs were
near zero, which is what I expected for targets with no downstream significant
program to align: `Atl1` versus `Reep1` r=0.012, `Atl1` versus `Spast` r=0.006,
`Reep1` versus `Retreg1` r=-0.004, and `Retreg1` versus `Spast` r=-0.008.
By contrast, the deliberately chosen ER-proteostasis controls had real positive
similarity, for example `Hspa5` versus `Atp2a2` r=0.365 and `Sec63` versus
`Atp2a2` r=0.128, consistent with a distinct detectable UPR axis.

## Target-specific reasoning

### `Arl6ip1`

External biology places ARL6IP1 in structural ER maintenance and ER-phagy.
Foronda et al. showed that ARL6IP1 is a reticulon-homology-domain ER-shaping
protein that interacts with FAM134B/RETREG1, is needed for heteromeric
ubiquitinated clusters during ER-phagy, and that `Arl6ip1` disruption in mice
expands ER sheets in sensory neurons with later degeneration. Byrne et al. and
Fowler and O'Sullivan found in Drosophila that `Arl6ip1` loss disrupts tubular
ER in long motor axons, perturbs ER-mitochondrial organization, and can be
partly rescued by increasing Drp1-mediated mitochondrial fission. Yamamoto and
Sakisaka showed that ARL6IP5 can redundantly shape ER membranes with ARL6IP1
and modulate FAM134B-mediated ER-phagy. Park et al. established the broader
HSP tubular-ER complex in which REEP1, spastin, and atlastin-1 coordinate ER
shape with microtubules.

The closest represented within-dataset analog was therefore `Retreg1`, because
RETREG1/FAM134B is the ER-phagy receptor that cooperates directly with ARL6IP1.
`Retreg1` produced exactly one focal DEG, its own target transcript, among 188
perturbed `151 TH Prkcd Grin2c Glut` nuclei. The next structural comparators
were the ER-shaping HSP genes: `Reep1` and `Reep2` were also self-only with one
DEG, while `Atl3`, `Spast`, and `Tfg` had zero DEGs. The internal July corpus
reports for `Atl1`, `Reep1`, and `Spast` independently summarized this as a
near-pan-measured absence of downstream ER-stress, autophagy/lysosome, BMP, or
shared HSP transcriptional programs. That is an important analog set because it
shares the intervention stage likely to matter for `Arl6ip1`: structural ER
and ER-microtubule defects in neurites that do not necessarily propagate to a
large steady-state nuclear RNA program in postnatal recovered neurons.

I down-weighted larger ER-stress counts as counterexamples rather than direct
analogs. `Atp2a2`, `Sec63`, and `Hspa5` all perturb luminal ER calcium or
client folding and induced UPR/ISR genes such as `Hspa5`, `Hsp90b1`, `Pdia4`,
`Ddit3`, `Chac1`, `Xbp1`, and `Herpud1`. Their counts of 187, 11, and 5 show
that a real ER proteostasis response is detectable in this cell group. However,
ARL6IP1 loss is primarily a membrane-shaping and ER-phagy-flux lesion, and the
dataset's `Atl1` and `Reep1` reports specifically found that analogous ER
shape perturbations did not switch on those UPR markers. The score-vector
correlations between structural-ER self-only targets and `Sec63`/`Hspa5` were
also near zero, so I did not assign `Arl6ip1` a Sec63-like multi-gene response.

The causal transfer model was:

`Arl6ip1` CRISPR loss of function -> reduced ARL6IP1 ER membrane-shaping and
FAM134B/RETREG1 ER-phagy clustering -> possible defects in ER sheet budding,
tubular ER continuity, lipid homeostasis, and ER-mitochondria coupling in
neurites -> survival/recovery of edited thalamic glutamatergic nuclei at
P37-P44 -> Wilcoxon DE over nuclear RNA in recovered nuclei.

At the molecular stage the external ARL6IP1 phenotype is clear. At the
propagation stage, though, the represented ER-shaping/HSP perturbations say the
defect is usually buffered from a broad nuclear transcriptome in this assay.
For the measured endpoint I therefore predicted no downstream FDR genes and a
low single-count endpoint driven by the possibility that the `Arl6ip1` target
transcript itself is detected, as happened for `Retreg1`, `Reep1`, `Reep2`,
`Atl1`, `Kif5a`, and `Kif5c`.

**Prediction for `Arl6ip1`: 1 DEG.**

## Limits and uncertainty

The prediction is extrapolative because `Arl6ip1`, `Arl6ip5`, `Ccpg1`,
`Tex264`, `Rtn1`, `Rtn2`, `Rtn3`, and `Rtn4` perturbation endpoints were absent
from the training count CSV. `Retreg1`, the mouse training symbol for
FAM134B/RETREG1, is the closest measured ER-phagy receptor but is not ARL6IP1
itself. The endpoint includes the perturbed transcript, so a point estimate of
1 is partly a prediction of target RNA visibility and not solely of downstream
biology. The experiment does not measure DNA indels, ARL6IP1 protein, ER
ultrastructure, axonal ER continuity, FAM134B ER-phagy flux, lipid-droplet
accumulation, ER-mitochondria contacts, edited-cell depletion, or long-term
axon degeneration. Those phenotypes could be real while producing no
BH-significant nuclear RNA signature in recovered P37-P44 NeuN-positive
thalamic neurons.
