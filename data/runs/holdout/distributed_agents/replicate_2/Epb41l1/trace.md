# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and resolved ambiguities

The held-out manifest contains one target, `Epb41l1`. I treated the task as a
point prediction of the total number of measured genes with
`pvals_adj < 0.05` after acute AAV-CRISPR loss of `Epb41l1` in
`151 TH Prkcd Grin2c Glut` nuclei. I used the endpoint exactly as it is encoded
in the training CSV: the count includes the perturbed gene's own transcript if
that row crosses FDR. I did not interpret weak self-RNA reduction as failed
editing, because this assay's mosaic frameshift modality often changes protein
function without strong nuclear mRNA depletion.

## Sources used

- Requested-target manifest:
  `[local file: 069_Epb41l1.csv]`.
- Focal-cell training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Training DE table:
  `[local file: training_de_all_cell_groups.parquet]`.
- Same-experiment semantic layer: Distributed Agents corpus
  `perturbai-july-260713-sourceguard-1773-v1`, especially high-confidence
  Claims `claim:0e5b111907d6d3ffebf7` for ankyrin/spectrin/adducin
  membrane-skeleton perturbations, `claim:a9367c3aeaad95bfae9c` for
  AMPAR/TARP/scaffold perturbations, `claim:60396794c5493932dc07` for
  postsynaptic scaffolds, `claim:52cb108e4006f73847a7` for
  mGluR/Homer/IP3R calcium-plasticity targets, and
  `claim:2eb3c1f67e285c7f7a99` for kainate receptors.
- Distributed Agents runtime `profile_compare`/`profile_inspect` over the focal-cell
  parquet rows for a curated 24-target analog cohort.
- PubMed-indexed literature on protein 4.1N/Epb41l1:
  Shen et al. 2000, DOI `10.1523/JNEUROSCI.20-21-07932.2000`, PMID
  `11050113`; Binda et al. 2002, DOI `10.1124/mol.62.3.507`, PMID
  `12181426`; Maximov et al. 2003, DOI
  `10.1016/S1044-7431(02)00027-1`, PMID `12676536`; Lin et al. 2009,
  DOI `10.1038/nn.2351`, PMID `19503082`; Wozny et al. 2009, DOI
  `10.1242/jcs.037382`, PMID `19225127`; Wang et al. 2020, DOI
  `10.1038/s41598-020-73795-6`, PMID `33046791`; Pushkin et al. 2023,
  DOI `10.1523/JNEUROSCI.0185-23.2023`, PMID `37845032`.

## Computational checks

The training count table has 1,674 non-held-out targets in the focal cell
group. It is very zero-inflated: 1,205/1,674 targets have `n_degs = 0`, the
median is 0, the 75th percentile is 1, the 90th percentile is 2, and only
43/1,674 have >=100 DEGs. Thus a point estimate above a few genes needs direct
evidence of a visible response family, not just a plausible neuronal function.

I scanned the parquet only for `group_name == "151 TH Prkcd Grin2c Glut"` and a
curated Epb41l1-neighborhood target set, then counted rows with
`pvals_adj < 0.05`, checked a more permissive `pvals_adj < 0.10` boundary, and
kept the lowest-FDR rows per perturbation. The query logic was:

```sql
SELECT gene_target,
       COUNT(*) AS measured,
       SUM(pvals_adj < 0.05)::INTEGER AS n_fdr05,
       SUM(pvals_adj < 0.10)::INTEGER AS n_fdr10,
       MIN(pvals_adj) AS min_fdr
FROM read_parquet(training_de_all_cell_groups.parquet)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
GROUP BY gene_target;
```

For every queried training target the focal-cell profile contained 17,259
measured genes and 119-282 matched perturbed nuclei against 23,679 matched
controls. The exact counts most relevant to `Epb41l1` were:

| neighborhood | training perturbations in `151` | observed `n_degs` |
| --- | --- | --- |
| spectrin/adducin/ankyrin/actin membrane skeleton | `Add1`, `Add2`, `Add3`, `Ank1`, `Ank2`, `Sptb`, `Sptan1`, `Actg1` | `0`, `0`, `0`, `0`, `0`, `0`, `1`, `1` |
| AMPAR/TARP/AMPAR-trafficking axis | `Gria1`, `Gria2`, `Gria3`, `Cacng2`, `Cacng3`, `Ica1`, `Rnf220` | `0`, `0`, `0`, `0`, `0`, `0`, `0` |
| PSD/synaptic adhesion scaffold | `Dlg4`, `Dlgap4`, `Homer2`, `Lrrc7`, `Nlgn3`, `Nrxn2` | `1`, `2`, `0`, `0`, `1`, `0` |
| IP3R and kainate-receptor branches that also bind 4.1N | `Itpr1`, `Grik1`, `Grik3` | `0`, `0`, `0` |

The few nonzero rows were mostly self-transcript calls rather than broad
downstream states: in the focal group `Sptan1` had only `Sptan1` itself at FDR
0.05; `Actg1` had only `Actg1`; `Dlg4` had only `Dlg4`; `Nlgn3` had only
`Nlgn3`; `Dlgap4` had `Dlgap4` plus `Vgf`. A profile comparison over the
24 analogs produced the same picture from signed expression profiles:
19/24 analogs had zero significant focal-cell features and 5/24 had only
one-to-few significant features; the inspected pairwise contrasts had no
shared significant positive or negative genes among the focal scaffold
representatives and their peers.

## `Epb41l1` reasoning

`Epb41l1` encodes protein 4.1N, a neuron-enriched member of the protein 4.1
FERM/SAB/CTD scaffold family. The external literature makes three mechanistic
neighborhoods plausible:

- AMPAR trafficking: 4.1N binds the GluR1/GluA1 C terminus and can link AMPARs
  to actin; disrupting the interaction lowers surface GluR1, and later work
  showed 4.1N-dependent, phosphorylation/palmitoylation-regulated GluR1
  insertion during plasticity (Shen et al. 2000; Lin et al. 2009).
- Other neuronal receptor/localization partners: 4.1N binds D2/D3 dopamine
  receptors and IP3R1, and regulates IP3R1 diffusion through the actin
  cytoskeleton in neuronal dendrites (Binda et al. 2002; Maximov et al. 2003;
  Fukatsu et al. 2004, DOI `10.1074/jbc.M408364200`, PMID `15364918`).
- Organismal and circuit phenotypes exist but are context-specific: germline
  4.1N loss affects the hypothalamic-pituitary-reproductive axis and GnRH axon
  localization (Wang et al. 2020), and acute 4.1N reduction impairs dentate
  gyrus granule-cell but not CA1 basal glutamatergic transmission in rat slice
  experiments (Pushkin et al. 2023). Conversely, a mouse line lacking 4.1G and
  retaining only low 4.1N in hippocampus had no basic hippocampal transmission
  or LTP defect, emphasizing compensation and cell-type dependence rather than a
  universal glutamatergic program (Wozny et al. 2009).

The training perturbations closest to those mechanisms are not broad
transcriptional responders in `151`. The same-experiment Distributed Agents corpus
summarizes this as high-confidence absence of a common ankyrin/spectrin/adducin
membrane-skeleton RNA program and high-confidence buffering of represented
AMPAR-core, AMPAR-trafficking, PSD, IP3R/calcium-plasticity, and kainate
receptor perturbations. The exact focal counts agree: every direct AMPAR/TARP
target was 0, `Itpr1`, `Grik1`, and `Grik3` were 0, and the physical
membrane-skeleton comparators were 0 except for `Sptan1` and `Actg1`
self-transcript singletons. This makes it unlikely that acute `Epb41l1`
frameshift in recovered thalamic glutamatergic neurons will elicit a multi-gene
homeostatic AMPAR, IP3R/calcium, kainate, or spectrin/actin compensation
program detectable by nuclear RNA.

I also considered but down-weighted other published 4.1N interactions.
`Slc12a5/KCC2`, `Cadm1/SynCAM1`, `Cask`, `Grik2`, and NETO-family kainate
auxiliary subunits were not represented as training targets in the focal CSV,
so they could not override the measured near-null AMPAR/IP3R/kainate scaffold
neighborhood. D2/D3 dopamine-receptor biology is less well matched to a
thalamic glutamatergic population, and the available `Drd2` perturbation itself
had `n_degs = 0` in `151`. Cancer-cell links between 4.1N and flotillin/Wnt,
PP1/JNK, or 14-3-3 were rejected as poor mechanistic transfer for postmitotic
neuronal nuclei; the represented 14-3-3 perturbations `Ywhae` and `Ywhaz` were
also only 0 and 1 DEG, respectively, in this cell group.

The remaining nonzero risk is a singleton self-transcript call. Some highly
expressed scaffold genes cross FDR only for their own transcript in this
endpoint, so `Epb41l1` could land at 1 even with no downstream response.
However, just as many nearby scaffolds with clear neuronal expression
(`Add1`, `Ank2`, `Itpr1`, `Gria3`, `Lrrc7`) did not cross the self-gene FDR
threshold, and `Epb41l1` has multiple protein isoforms and splice structures
that make guide-induced transcript loss uncertain. I therefore put the point
prediction on a completely flat focal response.

Predicted `n_degs`: **0**.

## Limits

- `Epb41l1` was held out and absent from both the supplied DE parquet and the
  training count CSV; the selected Distributed Agents corpus had no `Epb41l1` finding,
  claim, or graph neighborhood. The prediction is necessarily transfer from
  analogs.
- The best external evidence concerns receptor surface delivery, receptor
  diffusion, dendritic localization, synaptic currents, GnRH axons, or germline
  whole-animal phenotypes. None of those are direct measurements of a 3-4 week
  postnatal mosaic CRISPR nuclear-RNA signature in thalamic glutamatergic
  nuclei.
- Several close biochemical partners were not training perturbations, including
  `Cask`, `Cadm1`, `Slc12a5`, `Gria4`, `Cacng8`, `Cnih2`, `Cnih3`, `Pick1`,
  `Grik2`, `Neto1`, and `Neto2`.
- A point prediction of 0 is weakly distinguished from 1: the biology argues
  strongly against a broad downstream program, but the exact self-transcript
  FDR for held-out `Epb41l1` cannot be known from the training rows.
