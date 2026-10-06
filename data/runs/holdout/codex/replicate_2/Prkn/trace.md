# Prkn direct n_degs forecast

## Target and endpoint

- Target perturbation: `Prkn`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05`

## Biology prior from the declared bundle

The exact focal-population reach card shows that `Prkn` is present in the
assayed thalamic nuclei: 16,623 of 23,679 non-target nuclei expressed `Prkn`
and the mean non-target expression was 0.899 CP10K / 1.428 raw UMI. That makes
a self-transcript call possible in this class, but it does not measure editing
or downstream effect.

The functional-stock card argues against a large deterministic response. Parkin
is an activation-dependent RBR E3 ubiquitin ligase recruited by the PINK1 /
phospho-ubiquitin pathway, and a disruptive edit should stop new Parkin supply.
The existing cytosolic catalytic protein is not directly inactivated, however:
the declared mouse-neuron evidence only shows that endogenous Parkin persisted
through a six-hour translation block, far shorter than the P16-to-P37/44 assay
window. The same bundle also reports mixed postnatal neural observability:
adult germline `Prkn` loss has selective hippocampal synaptic and memory
phenotypes, whereas adult dopaminergic-neuron conditional loss produced no
major motor, survival, or transcriptional phenotype even by later time points.

I therefore treated the source as expressed and biologically reachable but
likely weakly or context-dependently realized in juvenile thalamic neurons,
rather than as a broad stress or proteostasis failure.

## Training-count scale

The declared 151-class count table contains 1,674 visible training perturbations
and is highly zero-inflated:

- median `n_degs` = 0
- 75th percentile = 1
- 1,205 / 1,674 targets have `n_degs = 0`
- 276 / 1,674 have `n_degs = 1`
- the mean is inflated to 14.05 by a small tail of core machinery perturbations

Self-transcript depletion is a major source of one-count outcomes in this
endpoint. Among 1,642 visible targets with a focal-class self row in the
Parquet, 319 had significant self transcript and 237 of the one-DEG outcomes
were self-only.

## Chosen biological comparators

I nominated Prkn analogs against the actual training universe using the
species-matched curated annotation and July PerturbAI corpus release. The
bounded high-specificity pool was dominated by PINK1/Parkin, mitophagy,
aggrephagy, and Parkinson-pathway genes. In the 151-class count table:

| comparator | relationship used for interpretation | n_degs |
| --- | --- | ---: |
| `Park7` | exact/paralog tier plus aggrephagy/Parkinson links | 1 |
| `Vcp` | narrow protein-quality-control modules | 2 |
| `Snca` | BIOCARTA_PARKIN_PATHWAY / Parkinson modules | 0 |
| `Sqstm1` | PINK1-PRKN mediated mitophagy / mitophagy | 1 |
| `Stub1` | aggrephagy / regulated-necrosis modules | 1 |
| `Xiap` | regulated-necrosis modules | 0 |
| `Tomm40` | exact/paralog tier plus mitophagy modules | 1 |
| `Map1lc3a` | PINK1-PRKN mediated mitophagy / mitophagy | 1 |
| `Atg5` | PINK1-PRKN mediated mitophagy / mitophagy | 0 |
| `Uchl1` | Parkinson pathway / ubiquitin binding | 1 |
| `Ogt` | stress-pathway narrow modules | 4 |
| `Chmp4b` | regulated necrosis / autophagy | 0 |

Across all 21 exact-complex/paralog or narrow-module nominees available in
training, the median `n_degs` was 1 and the sorted values were:

`0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 4, 7, 8, 25`.

The large-count Prkn-adjacent entries were broad boundaries rather than direct
scale donors: `Psmb4 = 742`, `Rab7 = 501`, and `Ctnnb1 = 383` represent loss of
core proteasome, late-endosomal, or Wnt / adhesion machinery, not acute loss of
a context-gated Parkin E3.

## Exact Parquet checks

The focal-class Parquet rows showed that most one-count close comparators were
self-only:

- `Park7`: only `Park7`, `pvals_adj = 0.0409`
- `Sqstm1`: only `Sqstm1`, `pvals_adj = 7.93e-4`
- `Stub1`: only `Stub1`, `pvals_adj = 0.0472`
- `Tomm40`: only `Tomm40`, `pvals_adj = 5.46e-7`
- `Map1lc3a`: only `Map1lc3a`, `pvals_adj = 6.46e-4`
- `Uchl1`: only `Uchl1`, `pvals_adj = 8.07e-60`

The same exact rows also confirmed that `Atg5`, `Snca`, `Xiap`, `Chmp4b`, and
`Vcp` did not clear self-transcript FDR in this class.

A symmetric 18-node signed-profile comparison of the close PINK1/Parkin and
broader boundary genes found no coherent significant downstream module among
the low-count comparators: significant-gene intersections between `Park7` and
the other low-count mitophagy/Parkinson nodes were zero, and their positive
top-tail overlap coefficients were only 0.02-0.08.

## Packaged same-experiment semantic checks

The selected corpus has no packaged same-experiment report for `Prkn`, so I
used it only to inspect comparator boundaries:

- `Park7` perturbation produced no FDR-significant downstream response in any
  of 23 recovered neuronal cell groups.
- `Snca` was near-pan-neuronally buffered, with 20 of 21 measured groups having
  no downstream FDR<0.10 gene.
- `Sqstm1` produced a sparse surface, and the 151-class response was one
  downstream mitochondrial ion-homeostasis gene rather than a canonical
  p62/NRF2/autophagy/proteasome/UPR program.
- `Atg5` did not recover a canonical autophagy, lysosome, p62, proteasome, or
  UPR/ISR transcript program.
- `Psmb4` and `Rab7` are explicit stress/proteasome/lysosome boundary states,
  explaining why their large counts should not be transferred to `Prkn`.

These Findings are same-experiment interpretations of the Parquet, not
independent validation.

## Synthesis

I predict that acute postnatal `Prkn` loss will be downstream-quiet in
`151 TH Prkcd Grin2c Glut`. The target is expressed broadly enough that its
own transcript could be the lone significant feature, and the closest
high-specificity analogs cluster around 0-1 DEGs with a median of 1. I therefore
place the point forecast at the self-only edge rather than at a multi-gene
mitochondrial or proteostasis response.

Predicted `n_degs`: **1**
