# Pdhx direct DEG-count forecast

## Target and endpoint

- Target: `Pdhx`, from the one-row holdout manifest.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- Point prediction: `1`.

## Evidence used

### Declared Pdhx biology bundle

The target bundle reports exact focal-population expression for `Pdhx` in the
non-target cells of `151 TH Prkcd Grin2c Glut`: 16,772 of 23,679 nuclei
expressed the gene, or 70.8307%, with mean raw UMI 1.3984, mean CP10k 0.8700,
and pseudobulk CPM 87.6408. That makes `Pdhx` detectably expressed in the
assayed thalamic population, although expression reach is not a measure of edit
efficiency.

The same biology bundle adjudicates PDHX as an E3-binding structural component
of the mitochondrial pyruvate dehydrogenase complex. A disruptive P16 edit is
therefore expected to stop new PDHX supply while leaving pre-existing assembled
complexes until component turnover. The functional-stock card judged the
operative stock likely substantially depleted by P37-P44, but with only partial
evidence because PDHX-specific turnover in postmitotic thalamic neurons and the
residual-capacity threshold were not measured. The matched-phenotype prior is
also weak: human biallelic PDHX deficiency is neurologic and metabolic, but it
is constitutional rather than an acute postnatal mouse neuronal perturbation.

### Training count table

The training table for this exact endpoint contains 1,674 targets and does not
contain `Pdhx`. The empirical count distribution is highly concentrated near
zero:

| Statistic | `n_degs` |
| --- | ---: |
| zero-count targets | 1205 / 1674 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| max | 2677 |

The typed analog nomination over the actual 1,674-gene training universe pulled
forward a PDC/TCA/OXPHOS neighborhood rather than the high-burden splicing,
proteasome, or chromatin targets. Its closest biochemical candidates were quiet
in the count table:

| Training perturbation | relationship to the Pdhx prior | `n_degs` |
| --- | --- | ---: |
| `Dlat` | PDC core / pyruvate dehydrogenase module | 1 |
| `Pdha1` | PDC E1 alpha / pyruvate dehydrogenase module | 1 |
| `Dld` | E3 used by PDC and alpha-ketoglutarate dehydrogenase | 0 |
| `Dlst` | alpha-ketoglutarate dehydrogenase E2; TCA neighbor | 0 |
| `Mdh1` | malate dehydrogenase; TCA/malate-aspartate | 29 |
| `Mdh2` | mitochondrial malate dehydrogenase | 1 |
| `Idh3a` | TCA enzyme | 1 |
| `Ogdh` | TCA dehydrogenase | 0 |
| `Aco2` | TCA enzyme | 0 |
| `Sdha` | TCA/complex II | 1 |
| `Mpc1` | pyruvate import | 0 |
| `Suclg1` | TCA enzyme | 0 |
| `Sucla2` | TCA enzyme | 1 |
| `Ndufa6` | complex I | 1 |
| `Ndufs4` | complex I | 0 |
| `Ndufa12` | complex I | 0 |
| `Cox8a` | complex IV | 0 |
| `Ndufa4` | respiratory chain | 1 |
| `Ndufs7` | complex I | 0 |
| `Got2` | malate-aspartate shuttle / mitochondrial aminotransferase | 1 |

Among these 20 nominees, 10 had zero significant features, 9 had 1 DEG, and
only `Mdh1` had a 10-49 DEG response. The core PDC contacts most directly
related to `Pdhx`, `Dlat`, `Pdha1`, `Dld`, and `Dlst`, were at 1, 1, 0, and 0.

### Declared expression Parquet

I used the declared `training_de_all_cell_groups.parquet` for the same
`151 TH Prkcd Grin2c Glut` class to check the selected analogs rather than
using only the aggregate CSV. Each selected profile had 17,259 measured genes.
For the 0-1 DEG analogs above, the only significant rows were the target
transcripts themselves:

| Training perturbation | `n_pert_matched` | significant row in the Parquet |
| --- | ---: | --- |
| `Dlat` | 170 | `Dlat`, logFC -0.6735, adjusted `p = 2.81e-07` |
| `Pdha1` | 208 | `Pdha1`, logFC -1.0391, adjusted `p = 1.31e-06` |
| `Mdh2` | 206 | `Mdh2`, logFC -0.8399, adjusted `p = 7.37e-05` |
| `Idh3a` | 119 | `Idh3a`, logFC -0.8171, adjusted `p = 9.27e-11` |
| `Ndufa6` | 260 | `Ndufa6`, logFC -0.4316, adjusted `p = 0.00136` |
| `Sdha` | 195 | `Sdha`, logFC -0.7809, adjusted `p = 2.11e-12` |
| `Sucla2` | 151 | `Sucla2`, logFC -0.6587, adjusted `p = 5.12e-05` |
| `Got2` | 152 | `Got2`, logFC -0.6005, adjusted `p = 3.76e-05` |

`Dld`, `Dlst`, `Aco2`, `Ogdh`, `Mpc1`, and `Suclg1` had no adjusted
`p < 0.05` rows in the same Parquet query. `Mdh1` was the local outlier at 29
DEGs, with its self transcript the strongest call. This means the nearby
metabolic perturbations were usually either transcriptionally silent or
self-target-only at this endpoint.

### Same-experiment corpus and profile topology

The Pdhx analogs were not isolated annotations. In the same-experiment corpus,
the 20-member PDC/TCA/OXPHOS cohort formed one explicit-Finding-reference
component; the largest fully connected sets were 9-member PDC/TCA groups such
as `Aco2`, `Dlat`, `Dld`, `Dlst`, `Idh3a`, `Mdh2`, `Mpc1`, `Ogdh`, and
`Pdha1`. This corpus topology is a report-derived view of the same experiment,
not an independent replicate, but it supports treating the low counts above as
a coherent local measurement pattern.

A profile comparison over the same 20 nodes in `151 TH Prkcd Grin2c Glut`
also found no hidden large transcriptional branch: 10 profiles had no
significant features, 9 had 1-9, and 1 had 10-49. Pairwise cosine and Pearson
values among the PDC/TCA focal nodes were positive and showed no significant
direction conflicts, but the shared structure sat on top of sparse endpoint
activity rather than a recurrent high-DEG state.

## Synthesis

The strongest endpoint-matched evidence is the measured response of PDC and
adjacent mitochondrial carbon-flux genes in the exact thalamic class. Those
perturbations are much better analogs for `Pdhx` than the screen's heavy
splicing, proteostasis, or chromatin responders, and they cluster at 0 or 1 DEG
despite being represented by recovered matched nuclei.

`Pdhx` has good focal expression and is likely to be functionally perturbed by
harvest, so a pure 0 is not my best point estimate. However, the closest PDC
and TCA training perturbations show little to no downstream state in recovered
thalamic neurons; the single significant call, when present, is usually the
self transcript. Because `n_degs` includes the target gene and `Pdhx` is
detectably expressed in 70.8% of focal non-target nuclei, I predict a
self-transcript-only response:

`predicted_n_degs = 1`.
