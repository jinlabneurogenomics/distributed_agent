# DEG-count prediction trace

## Question and endpoint

The run asks for one point prediction: the number of genes expected to pass
BH-adjusted Wilcoxon `pvals_adj < 0.05` after knockout of the held-out mouse
target `Trrap` in `151 TH Prkcd Grin2c Glut` neurons.  I interpreted `151 TH`
as the Allen-style thalamic glutamatergic focal class, not tyrosine hydroxylase.

`Trrap` was held out from both supplied inputs, so the `n_degs` endpoint and the
actual `Trrap` expression signature are absent from the declared training data.
The endpoint is directly observed only for the 1,674 non-held-out training
perturbations in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.  The all-cell Parquet was
used as direct same-experiment signature evidence for those non-held-out
analogs.  I did not use target RNA knockdown as an editing-efficiency weight,
because the dataset context notes that measured nuclear self-knockdown is not
correlated with downstream transcriptional effect in this experiment.

## Sources used

Internal same-experiment sources:

- The declared DEG-count training table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- The declared differential-expression Parquet:
  `training differential-expression dataset`.
- The selected same-experiment PerturbAI corpus release
  `perturbai-july-260713-sourceguard-1773-v1`, queried for reports on
  training comparators such as `Atxn7`, `Ep300`, `Chd8`, `Brd4`, and `Setd1a`.
  I used this only as packaged interpretation of the same experiment, not as an
  independent replicate.

External biological context:

- CORUM 3.0 complex annotations and primary structural studies place mammalian
  TRRAP in the NuA4/TIP60 or TIP60-EP400 histone acetyltransferase and H2A.Z
  exchange assembly and in SAGA/STAGA coactivator complexes.
- Grant et al. 1998, Mol Cell, DOI `10.1016/s1097-2765(00)80300-7`, and Park
  et al. 2001, Genes Dev, DOI `10.1101/gad.900101`: Tra1/TRRAP is a structural
  HAT-complex cofactor.
- McMahon et al. 1998, Cell, DOI `10.1016/s0092-8674(00)81479-8`, and
  Nikiforov et al. 2002, Mol Cell Biol, DOI `10.1128/MCB.22.14.5054-5063.2002`:
  TRRAP is recruited by MYC-family and E2F transactivation domains, but some
  MYC output is TRRAP independent.
- Ard et al. 2002, Mol Cell Biol, DOI
  `10.1128/MCB.22.16.5650-5661.2002`: p53 can recruit TRRAP-containing
  acetyltransferase complexes for Mdm2 activation.
- Yang et al. 2024, Science, DOI `10.1126/science.adl5816`; Chen et al. 2024,
  Nat Commun, DOI `10.1038/s41467-024-51259-z`; Li et al. 2024, Nature, DOI
  `10.1038/s41586-024-08011-w`: mammalian NuA4/TIP60 architecture, with EP400
  as the main scaffold and TRRAP as an activator-binding module.
- Tapias et al. 2021, eLife, DOI `10.7554/eLife.61531`, and Yin et al. 2022,
  Comput Struct Biotechnol J, DOI `10.1016/j.csbj.2022.12.024`: Trrap loss in
  neuronal or adult neural-stem contexts can act through SP1 and microtubule
  programs, but those data come from complete/developmental or longer-window
  systems rather than the P16 sparse mosaic Perturb-seq assay.
- Meert et al. 2025, iScience, DOI `10.1016/j.isci.2025.111978`: CHD8 and TRRAP
  co-bind MYC/E2F promoters in human neural stem cells, giving a mechanistic
  reason to compare held-out `Trrap` with the observed `Chd8` perturbation while
  also marking a cell-cycle/progenitor difference from postmitotic TH neurons.
- Cogne et al. 2019, Am J Hum Genet, DOI `10.1016/j.ajhg.2019.01.010`: de novo
  human TRRAP missense variants cause autism/intellectual-disability spectra
  and altered neuronal or ion-transport expression in fibroblasts, supporting
  neural relevance but not fixing this acute mouse DEG count.

## Quantitative checks over supplied data

The focal training table has 1,674 non-held-out targets.  It is extremely
zero-inflated in this endpoint:

- 1,205 of 1,674 targets had `n_degs = 0`.
- The median was 0, the 75th percentile was 1, the 90th percentile was 2, the
  95th percentile was 18, and the maximum was 2,677.

I then checked whether mechanistically plausible TRRAP relatives were present
in the focal training table and read the corresponding `151 TH` Parquet rows.
The principal FDR0.05 counts were:

| Training perturbation | 151 TH `n_degs` | Expression-pattern evidence and role |
| --- | ---: | --- |
| `Atxn7` | 0 | The only represented SAGA/STAGA-family subunit among close TRRAP HAT-complex comparators.  The corpus also reports zero downstream FDR0.10 genes for `Atxn7` across 20 measured groups, with near-zero score-cosine neighbors.  This is a counterexample: a SAGA-associated target can be completely buffered in the P16 postmitotic screen. |
| `Ep300` | 0 | A HAT coactivator, but KAT3 rather than NuA4/SAGA.  The all-cell same-experiment report found no downstream FDR0.10 genes in 21 groups, arguing that HAT biology alone does not imply a broad basal postmitotic signature. |
| `Crebbp` | 8 | Weak focal response from the KAT3 paralog of EP300.  Its small signature, together with `Ep300=0`, was a counterexample to a generic enhancer-acetyltransferase response. |
| `Kat6a`, `Kat6b` | 0, 0 | MYST-family acetyltransferases outside the TRRAP assemblies; both were flat in the focal cell group.  These are weak analogs but useful negative controls for the idea that every chromatin acetyltransferase perturbation creates many TH DEGs. |
| `Myc`, `Mycn`, `E2f1` | 0, 0, 0 | Direct TRRAP transcription-factor clients in cycling systems.  Their focal flatness indicates that the MYC/E2F cell-cycle arm is not detectably active in recovered postmitotic `151 TH` nuclei. |
| `Chd8` | 61 | A transcription/chromatin regulator linked externally to TRRAP at MYC/E2F promoters in neural stem cells.  In this PerturbAI corpus, `Chd8` had a restricted subcortical response dominated by `151 TH` and `155 MB`, with RNA-processing genes such as `Pnisr`, `Usp11`, `Dus3l`, and `Luc7l3` in the focal signature. |
| `Kmt2a`, `Med13`, `Med15`, `Med23` | 24, 11, 19, 13 | Other RNA Pol II co-regulator perturbations with modest focal responses.  They show that general transcriptional coactivator/scaffold genes can give low-tens DEG counts rather than either 0 or hundreds in this assay. |
| `Brd4`, `Setd1a`, `Ctcf`, `Sin3a` | 311, 368, 270, 1,433 | Broad chromatin/transcriptional regulators with much larger `151 TH` footprints.  Same-experiment reports show they run through distinct modules such as BRD4-linked neuronal maintenance, SETD1A-linked mitochondrial/ER/cilium repression, and SIN3A corepressor derepression.  These are counterexamples against using all chromatin regulators as one quantitative class. |

The focal Parquet contained 17,259 measured genes for 1,674 targets, with
`n_pert_matched` ranging from 23 to 419 and a common `n_ctrl_matched` of 23,679
in `151 TH Prkcd Grin2c Glut`.  For selected analogs I sorted by adjusted
p-value within the focal group and confirmed that the CSV counts match the
number of `pvals_adj < 0.05` rows: for example, `Chd8` had 61 FDR genes headed
by `Pnisr`, `Tmem50a`, `Chd8`, `Man2c1`, and `Usp11`; `Setd1a` had 368 FDR
genes headed by `Itfg1`, `Foxred1`, `Nprl3`, `Sfi1`, and `Tafazzin`; and
`Atxn7`, `Ep300`, `Myc`, `Mycn`, and `E2f1` had no focal FDR0.05 gene.

## Trrap prediction

`Trrap` is not a paralog of an observed training target, and none of the best
biochemical proxies for the mammalian NuA4/TIP60 core were present in the
training count table (`Kat5`, `Ep400`, `Dmap1`, `Ing3`, `Actl6a`, `Ruvbl1`, and
`Ruvbl2` were absent).  That makes the prediction an extrapolation from weaker
neighbors.

The zero/nonzero decision is positive.  TRRAP is a large nonredundant
activator-binding pseudokinase scaffold shared by multiple HAT complexes, and
external complete-loss systems show neural and transcriptional dependence.
The `Atxn7=0`, `Ep300=0`, and `Kat6a/Kat6b=0` training observations prevent a
high count solely from "chromatin acetylation" or "SAGA/NuA4 membership", but
they do not make `Trrap` dispensable: Atxn7 is a SAGA deubiquitinase-module
subunit with ATXN7L-family buffering possibilities, KAT3 and KAT6 complexes do
not share TRRAP's activator-docking role, and the mammalian TIP60 structural
work places TRRAP as a distinct module rather than as the catalytic HAT itself.

The main downward adjustment is the experimental window.  The strongest known
TRRAP outputs are MYC/E2F proliferation genes in cycling cells, p53 checkpoints,
embryonic stem-cell maintenance, and adult neurogenesis.  The supplied assay
perturbed sparse NeuN-positive neurons after P16 and sampled surviving nuclei
3-4 weeks later.  In the training data the represented direct clients `Myc`,
`Mycn`, and `E2f1` were all `0` in the focal class, so I did not project a
progenitor-like or tumor-like TRRAP collapse onto thalamic postmitotic cells.
The Purkinje-neuron SP1/microtubule literature keeps a neuronal maintenance
prior alive, but the published effect used complete Trrap deletion and an older
cell type and therefore supports a moderate signature, not a `Sin3a`-scale
thousand-gene response.

I treated `Chd8=61` as the nearest quantitative anchor because CHD8 physically
and genomically couples to a TRRAP/MYC/E2F promoter axis in neural stem cells
and because `Chd8` in this dataset was a real but restricted subcortical
responder.  The low-tens counts from `Kmt2a`, `Med15`, `Med23`, `Med13`, and
`Creb1` set the lower side of the same broad Pol-II co-regulator class, whereas
`Brd4`, `Setd1a`, `Ctcf`, and `Sin3a` are broader but mechanistically less
direct and show different within-dataset modules.  Balancing a nonzero
TRRAP-module prior against the absence of close observed complex subunits and
the flat MYC/E2F/KAT3/SAGA-DUB comparators led to a point prediction just below
the `Chd8` focal response: 47 DEGs.

## Limits and uncertainty

This is a one-target extrapolation.  The two closest mammalian TIP60/SAGA
biochemical subassemblies were largely not represented among the non-held-out
training targets, and the held-out `Trrap` signature itself was not available
for cosine, overlap, or residual checks.  The strongest external TRRAP biology
comes from cycling stem, progenitor, transformed, or complete-knockout systems;
those are mechanistically informative but differ from acute mosaic CRISPR in
postmitotic thalamic neurons.  The DEG count is also power- and recovery-
dependent, so the integer estimate should be read as expected response breadth
under this specific Wilcoxon/FDR assay, not as total TRRAP biological
importance.
