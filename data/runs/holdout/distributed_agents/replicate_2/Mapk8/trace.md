# Reasoning Trace

## Question and resolved ambiguities

The task is to predict the held-out focal-cell endpoint for the requested
perturbations in `151 TH Prkcd Grin2c Glut` neurons.  In this run the manifest
contains a single held-out gene, `Mapk8`.

The endpoint is `n_degs`: the number of measured genes with
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` in the focal cell
group after sparse P16 AAV CRISPR-Cas9 loss of function.  I treated this as an
assay-specific response-breadth quantity, not as a generic estimate of gene
importance, viability, embryonic phenotype, or editing efficiency.

## Sources used

- Primary same-experiment endpoint table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Primary same-experiment differential-expression table:
  `[local file: training_de_all_cell_groups.parquet]`
- Held-out manifest:
  `[local file: 130_Mapk8.csv]`
- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`,
  searched for JNK, stress-MAPK, AP-1, and `Mapk9` claims over the same
  PerturbAI experiment.
- Distributed Agents Runtime `profile_neighbors`, used to compare signed log2-fold
  profiles of selected stress-MAPK/AP-1 training perturbations against all
  1,674 available focal training perturbations.
- PubMed literature searches for `Mapk8`/JNK1 pathway and neuronal knockout
  functions.

Key external mechanistic references:

- Davis 1999, PMID 10207617, DOI 10.1515/9781400865048.1: JNKs are
  stress/cytokine-activated MAPKs activated by MKK4 and MKK7 and signal through
  AP-1 transcriptional regulation.
- Weston and Davis 2007, PMID 17303404, DOI 10.1016/j.ceb.2007.02.001:
  review of the JNK pathway and isoform-dependent roles in survival, death,
  cancer, and metabolic signaling.
- Kuan et al. 1999, PMID 10230788, DOI 10.1016/s0896-6273(00)80727-8:
  `Jnk1/Mapk8` and `Jnk2/Mapk9` cooperate during embryonic brain apoptosis;
  single `Jnk1`, `Jnk2`, or `Jnk3` null mice survive, while combined `Jnk1`
  and `Jnk2` loss causes embryonic neural defects.
- Ham et al. 2000, PMID 11007936, DOI 10.1016/S0006-2952(00)00372-5:
  JNK/c-Jun apoptotic effects in neurons are cell-type and developmental-stage
  dependent.
- Westerlund et al. 2011, PMID 21297631, DOI 10.1038/nn.2755: JNK1 regulates
  embryonic cortical neuronal migration through phosphorylation of SCG10/Stmn2,
  a developmental phosphoprotein mechanism rather than a direct basal mRNA
  program in mature recovered nuclei.

## Computation over the training data

1. I read the requested-target CSV and confirmed that the only requested row is
   `Mapk8`.
2. I summarized the training endpoint table.  It contains 1,674 focal
   perturbations; 1,205 of them have `n_degs = 0`.  The distribution is highly
   sparse and skewed: median 0, 75th percentile 1, 90th percentile 2, 95th
   percentile 18, 99th percentile about 430, and maximum 2,677.  Therefore a
   zero prediction is common for the assay, but strong responses are detectable
   for the right perturbations.
3. I pulled exact `n_degs` for the represented MAPK/JNK/AP-1 comparators from
   the endpoint CSV.
4. For those comparators I filtered the parquet to
   `group_name == "151 TH Prkcd Grin2c Glut"` and read `names`, `gene_target`,
   `logfoldchanges`, `pvals_adj`, `n_pert_matched`, and `n_ctrl_matched`.  This
   verified the DEG counts directly from the focal DE rows and checked whether
   any comparator had a near-threshold expression pattern.
5. I used Distributed Agents Runtime `profile_neighbors` with the same focal context and
   all 1,674 training targets as the eligible universe for anchors
   `Mapk9`, `Map2k6`, `Taok1`, `Jund`, `Fosl2`, `Nr4a1`, `Map3k7`, `Map2k1`,
   and `Map2k2`.  This compared full signed `logfoldchanges` profiles and the
   leading positive/negative tails.  For the null JNK/AP-1 anchors the nearest
   profile neighbors were not pathway analogs, and the anchors had no
   significant positive or negative program.

The represented pathway table in the focal cell group was:

| training perturbation | focal `n_degs` | focal expression-pattern evidence |
| --- | ---: | --- |
| `Mapk9` | 0 | JNK2, the closest represented JNK paralog.  139 perturbed nuclei vs 23,679 controls; all 17,259 read genes were nonsignificant.  The smallest adjusted p-values were `Dus3l` and `Tpi1`, both q = 0.363, so the vector has no AP-1 or stress response near FDR 0.05. |
| `Map2k6` | 0 | Stress-MAPK MAP2K comparator upstream of p38 rather than JNK, included because the Distributed Agents same-experiment corpus grouped it with `Mapk9` and `Taok1` as a stress-MAPK-adjacent perturbation.  255 perturbed nuclei; smallest q = 0.841. |
| `Taok1` | 0 | MAP3K-family stress-kinase activator that can impinge on JNK/p38-like cascades.  131 perturbed nuclei; smallest q = 0.402. |
| `Map3k7` | 0 | Upstream MAP3K/NF-kB/JNK-p38 pathway node; a counterexample to assuming that MAPK-cascade membership is enough to create a focal DEG footprint.  160 perturbed nuclei; every measured gene had q = 1.0. |
| `Jund` | 0 | AP-1 family transcription factor downstream of JNK signaling.  261 perturbed nuclei; smallest q = 0.200. |
| `Fosl2` | 0 | Fos/AP-1 family comparator.  211 perturbed nuclei; every measured gene had q = 1.0. |
| `Nr4a1` | 0 | Immediate-early/activity-regulated transcription-factor comparator from the same AP-1/CREB/EGR neighborhood in the Distributed Agents corpus.  200 perturbed nuclei; every measured gene had q = 1.0. |
| `Nr4a3` | 0 | Related activity-regulated nuclear receptor.  218 perturbed nuclei; smallest q = 0.166. |
| `Map2k1` | 4 | ERK MAP2K positive counterexample with only a tiny signature: `Vgf`, `Ptpn5`, `Etv5`, and `Unc13a` were FDR-significant.  This shows MAPK nodes can be detected, but the effect was small and ERK-specific. |
| `Map2k2` | 0 | Paralogue of `Map2k1`; 282 perturbed nuclei; every measured gene had q = 1.0. |
| `Cdc42` | 1 | Small-GTPase input into PAK/JNK signaling; the sole DEG was the targeted transcript `Cdc42` itself. |
| `Rac1` | 0 | Small-GTPase input into PAK/JNK signaling; every measured gene had q = 1.0. |
| `Pak1`, `Pak2`, `Pak3` | 1, 0, 0 | Upstream PAK comparators.  `Pak1`'s only DEG was `Pak1` itself; `Pak2` and `Pak3` were flat. |
| `Mef2a`, `Mef2c`, `Mef2d` | 4, 1, 0 | MAPK-responsive transcription-factor counterexamples with at most one-to-four DEGs, not a shared JNK/AP-1 state. |

The most target-specific same-experiment corpus result was
`claim:73be997a6a0b095c36d2`, which states that basal loss of represented
stress-activated MAPK-adjacent signaling nodes does not produce a shared
neuronal transcriptomic module in this juvenile snRNA-seq screen.  Its basis
explicitly included `Map2k6`, `Mapk9`, and `Taok1`.  A second corpus claim over
`Fosl2`, `Jund`, and `Nr4a1` reported that represented CREB/AP-1/EGR and
related bZIP/MAPK perturbations do not form a shared postnatal neuronal
loss-of-function transcriptomic module.  These corpus claims are interpretations
of the same PerturbAI experiment, so I used them as within-dataset semantic
context, not as independent replication.

## Target-specific prediction

### `Mapk8`

`Mapk8` encodes JNK1, a stress-activated c-Jun N-terminal kinase.  A priori,
JNK1 could plausibly affect neuronal survival, AP-1 target genes, or cytoskeletal
states, because the JNK pathway is activated by MKK4/MKK7 and can regulate
AP-1/c-Jun transcription, and because genetic work links JNK isoforms to
developmental neuronal apoptosis and embryonic migration.  Those facts, however,
map imperfectly onto this endpoint:

- the screen perturbs postmitotic juvenile neurons at P16-P37/44, not embryonic
  cortical neurons;
- the cells are assayed basally rather than after axotomy, excitotoxicity,
  cytokine exposure, or another acute JNK-activating stimulus;
- the readout is nuclear RNA in recovered nuclei, whereas much of JNK1 biology
  is phosphorylation-dependent and cytoplasmic; and
- `Mapk9/JNK2` and the CNS-enriched `Mapk10/JNK3` could buffer partial loss of
  `Mapk8`.

The direct same-assay evidence points to no durable focal mRNA program for basal
JNK loss.  `Mapk9`, the assayed JNK paralog, had zero DEGs and no gene with
q < 0.36 despite 139 perturbed nuclei.  The stress-MAPK comparators `Map2k6`
and `Taok1`, which the Distributed Agents corpus identified as the closest represented
stress-MAPK/JNK-adjacent null module, also had zero DEGs.  The upstream MAP3K
`Map3k7` had zero DEGs.  Perturbing AP-1/immediate-early downstream factors
`Jund`, `Fosl2`, `Nr4a1`, and `Nr4a3` also yielded zero focal DEGs, arguing
against a stable AP-1-like compensation pattern under these assay conditions.
The only small nonzero nearby counts came from more distal or different-branch
nodes: ERK-branch `Map2k1` had four DEGs, `Cdc42` and `Pak1` each had only their
self transcript, and `Mef2a`/`Mef2c` had one-to-four DEGs that did not resemble
a stress-JNK module.

I therefore predict that held-out `Mapk8` lands on the no-DEG side of the
focal endpoint, with point prediction:

```tsv
target_name	predicted_n_degs
Mapk8	0
```

## Limits and extrapolation

- `Mapk8` itself was completely held out; no `Mapk8` differential-expression
  signature or observed count was present in either primary input.
- The strongest training analog is `Mapk9`, not `Mapk8` itself.  `Mapk8` and
  `Mapk9` are close JNK paralogs but not interchangeable in all neurons or
  stress contexts.
- `Mapk10/JNK3` and `Map2k7/MKK7`, arguably important CNS/JNK-pathway
  comparators, were not present in the focal training-count table available to
  this run.
- A zero predicted DEG count is not a claim that JNK1 is biologically
  irrelevant.  The same KO could have a phosphoprotein, cytoskeletal, survival,
  injury-response, or embryonic phenotype that this basal juvenile nuclear-RNA
  assay would miss.
- The Distributed Agents corpus claims are same-experiment summaries and help interpret
  the training measurements; they do not provide an independent experimental
  validation of the held-out `Mapk8` prediction.
