# Task interpretation

The held-out target list for this run contains one perturbation, `Col25a1`.
The endpoint to predict is the integer number of genes with
`pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` after sparse
AAV-PHP.eB CRISPR loss of function.  I treated the training
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` values as the authoritative
observed counts for non-held-out perturbations, and used
`training_de_all_cell_groups.parquet` for focal-cell expression-pattern checks.
`Col25a1` is absent as a perturbation in both training files, so the estimate is
an extrapolation from represented collagen, extracellular-matrix, receptor-PTP,
APP-processing, and adhesion perturbations.

One ambiguity I resolved conservatively is that broad biological importance was
not enough to call a DEG response.  The readout is a postnatal neuronal nuclear
mRNA breadth endpoint after mosaic partial target loss; developmental germline
lethality, muscle phenotypes, extracellular protein functions, or Alzheimer's
plaque biochemistry were only used if they nominated assayed perturbations that
were mechanistically comparable in this experiment.

# Sources used

- Requested targets:
  `[local file: 044_Col25a1.csv]`.
- Focal training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Same-experiment differential expression:
  `[local file: training_de_all_cell_groups.parquet]`.
- Internal same-experiment Distributed Agents corpus:
  `perturbai-july-260713-sourceguard-1773-v1`.
- PubMed literature for Col25a1 / collagen XXV biology.

# Dataset calibration

The focal training set contained 1,674 non-held-out perturbations.  Its DEG-count
distribution is heavily zero-inflated:

| statistic | value |
| --- | ---: |
| mean | 14.05 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| nonzero targets | 469 / 1674 |

I then queried the focal cell group in the parquet for mechanistic analogs.  The
operation was:

```python
dataset = ds.dataset(training_de_all_cell_groups, format="parquet")
f = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut") &
    pc.field("gene_target").isin(candidate_targets)
)
table = dataset.to_table(
    columns=[
        "names", "scores", "logfoldchanges", "pvals_adj",
        "group_name", "gene_target", "n_pert_matched", "n_ctrl_matched",
    ],
    filter=f,
)
```

This read 17,259 measured genes per requested training perturbation and counted
`pvals_adj < 0.05` genes to check the CSV counts.  The relevant focal analogs
were:

| training perturbation | focal n_degs | focal FDR<0.10 genes | why it was inspected |
| --- | ---: | ---: | --- |
| `Col11a1` | 0 | 0 | one of the only two represented collagen genes |
| `Col2a1` | 0 | 0 | one of the only two represented collagen genes |
| `Itga2` | 0 | 0 | represented collagen receptor / ECM adhesion neighbor |
| `Adgrg6` | 0 | 0 | collagen/ECM and chondrogenic regulator comparator in the Distributed Agents corpus |
| `Sox5` | 2 | 2 | chondrogenic transcriptional regulator counterexample |
| `Sox9` | 0 | 0 | chondrogenic transcriptional regulator counterexample |
| `Runx2` | 0 | 0 | cartilage/bone ECM regulator counterexample |
| `Tgfbr1` | 0 | 0 | TGF-beta receptor ECM-remodeling comparator |
| `Tgfbr2` | 0 | 0 | TGF-beta receptor ECM-remodeling comparator |
| `Tgfbr3` | 0 | 0 | TGF-beta receptor ECM-remodeling comparator |
| `Smad2` | 1 | 1 | downstream TGF-beta signal transducer; single `Cpne7` hit only |
| `Smad3` | 0 | 0 | downstream TGF-beta signal transducer |
| `Smad4` | 0 | 0 | downstream TGF-beta signal transducer |
| `Smad6` | 0 | 0 | inhibitory BMP/TGF-beta pathway comparator |
| `Smad9` | 0 | 0 | BMP SMAD comparator |
| `Ptprd` | 0 | 0 | represented receptor-type PTP-delta, a putative collagen XXV receptor family member |
| `Ptprt` | 0 | 0 | receptor-type PTP counterexample |
| `Ptprc` | 0 | 0 | receptor-type PTP counterexample |
| `Adam10` | 0 | 0 | APP / membrane-protein processing comparator |
| `App` | 1 | 1 | amyloid-processing comparator; only the `App` self transcript was significant |
| `Psen1` | 0 | 0 | gamma-secretase / APP-processing comparator |
| `Sorl1` | 0 | 0 | APP-trafficking comparator |
| `Itm2b` | 1 | 1 | amyloid-related APP comparator; only the `Itm2b` self transcript was significant |

All 9 represented integrin targets in the count CSV had zero focal DEGs
(`Itga2`, `Itga2b`, `Itga4`, `Itga6`, `Itga7`, `Itga8`, `Itga9`, `Itgb1`,
`Itgb2`).  All 8 represented `Ptpr*` targets had zero or one focal DEG, with the
most relevant assayed receptor PTP, `Ptprd`, at zero; `Ptprs`, the other
reported collagen-XXV receptor, was not a perturbation target.

# Internal-corpus evidence

The Distributed Agents corpus did not contain direct `Col25a1` findings, which is
consistent with it being held out.  Relevant frozen claims and target contexts
were therefore used only for neighboring, non-held-out genes:

- `Col11a1`: Distributed Agents reported no FDR<0.10 downstream transcriptome in any
  measured postnatal NeuN+ brain neuronal group.  Its directly represented
  cartilage/ECM relatives or regulators, including `Col2a1`, `Itga2`, `Sox5`,
  `Sox9`, `Adgrg6`, `Tgfbr1`, `Tgfbr2`, `Tgfbr3`, `Smad2`, `Smad3`, `Smad4`,
  `Smad6`, and `Smad9`, yielded zero-to-singleton FDR responses rather than a
  recurring neuronal ECM signature.  A nominal-neighbor search for `Col11a1` was
  explicitly rejected by the corpus as noise-scale, not a hidden mechanistic
  module.
- `Col2a1`: Distributed Agents reported an essentially flat Col2a1 response in
  NeuN-enriched mouse neurons, with only two FDR<0.10 genes across 23 cell
  groups and no unfolded-protein, chondrocyte, SOX, or ECM-remodeling program.
  In the focal thalamic group, its observed count was zero.
- A lexical Distributed Agents search for collagen/ECM/integrin claims retrieved the
  frozen statement that cartilage-collagen perturbations do not induce a
  coherent chondrocyte-like ECM remodeling transcriptional program in sampled
  postnatal neuronal nuclei.
- The same corpus also contained a moderate-confidence claim that represented
  integrin and laminin-receptor perturbations do not produce a shared basal
  postmitotic neuronal adhesion or beta1/focal-adhesion transcriptional module,
  aside from isolated target-specific single-gene effects.
- For the PTP-delta/sigma receptor axis implicated by collagen XXV biology, the
  closest represented target was `Ptprd`; Distributed Agents' broader receptor-PTP claim
  found no shared acute postnatal neuronal snRNA-seq loss-of-function signature
  among represented receptor-type PTP perturbations.
- For amyloid/APP adjacency, Distributed Agents reported that represented APP-processing,
  secretase, Notch, synaptic-adhesion, and APP-trafficking perturbations are
  largely uncoupled from a shared juvenile neuronal nuclear RNA module.

The corpus evidence therefore points in the same direction as the raw focal
counts: analogous extracellular and membrane-processing perturbations are
buffered or at most singleton responders in this assay.

# Col25a1 biology and prediction

`Col25a1` encodes CLAC-P/collagen type XXV, a type II transmembrane collagen
originally purified as the precursor of the collagen-like Alzheimer amyloid
plaque component.  Hashimoto et al. cloned CLAC-P, showed neuronal expression,
furin-mediated shedding of the extracellular CLAC fragment, and binding of both
secreted and membrane-tethered forms to fibrillized Abeta (Hashimoto et al.,
2002, DOI: `10.1093/emboj/21.7.1524`, PMID: `11927537`).  Osada et al. further
mapped Abeta binding to a positively charged cluster in the collagenous domain
1 of CLAC and found that soluble CLAC can inhibit Abeta fibril elongation in
vitro (Osada et al., 2004, DOI: `10.1074/jbc.M413340200`, PMID: `15615705`).

The clearest organismal loss-of-function phenotype is earlier and more
peripheral than this Perturb-seq experiment.  Germline Col25a1-null mice fail
intramuscular motor-axon elongation and branching and die at birth from
respiratory failure after spinal motoneuron loss (Tanaka et al., 2014, DOI:
`10.1523/JNEUROSCI.2440-13.2014`, PMID: `24453327`).  A later mechanistic study
showed that muscle-derived collagen XXV interacts with motor-neuron PTP-sigma
and PTP-delta to attract motor axons, and that congenital cranial dysinnervation
mutations reduce that interaction (Munezane et al., 2019, DOI:
`10.1016/j.celrep.2019.11.112`, PMID: `31875546`).  Goncalves et al. also
reported a developmental muscle role for collagen XXV in myoblast fusion
(Goncalves et al., 2019, DOI: `10.1038/s41598-019-42296-6`, PMID: `30971718`).

Those mechanisms do not nominate a strong postmitotic thalamic neuronal mRNA
responder for four reasons.

First, the focal experiment perturbs postnatal NeuN+ brain neurons at P16-P44.
The strongest Col25a1-null phenotypes are embryonic/perinatal intramuscular
motor innervation and early myogenesis phenotypes, involving muscle-derived
collagen XXV and spinal/ocular motor-axon behavior rather than TH Prkcd Grin2c
glutamatergic thalamic neurons.

Second, the collagen/ECM class that was actually represented in the screen was
flat.  `Col11a1` and `Col2a1`, the only training perturbations beginning with
`Col`, both had zero focal DEGs and no gene at even FDR<0.10.  The Distributed Agents
corpus independently reported that their all-cell-group signatures were null or
near-flat and not part of a hidden collagen-like neuronal module.

Third, the candidate cell-surface receptor branch did not respond.  PTP-delta is
the assayed member of the Munezane receptor pair, and `Ptprd` had zero focal
DEGs with a minimum adjusted p-value of 0.143.  `Ptprt`, `Ptprc`, and the other
represented receptor-type PTPs were also zero or singleton perturbations.

Fourth, the Alzheimer's / Abeta connection is biochemical and overexpression- or
plaque-context dominated.  The relevant training counterexamples in
APP-processing and trafficking were also silent or target-self-only:
`Adam10 = 0`, `Psen1 = 0`, `Sorl1 = 0`, `App = 1` with only the `App`
self-transcript significant, and `Itm2b = 1` with only the `Itm2b`
self-transcript significant.

Together, the within-dataset evidence is stronger than the external evidence
for any broad Col25a1-responsive thalamic transcriptome.  I therefore predict
that `Col25a1` will behave like the represented collagen and receptor-PTP
counterexamples and have no genes passing FDR 0.05.

# Final point estimate

| target | predicted n_degs |
| --- | ---: |
| `Col25a1` | 0 |

# Limits

This is an extrapolation because no direct `Col25a1`, `Col13a1`, or `Ptprs`
perturbation was available in the training set or Distributed Agents corpus.  `Col25a1`
is not a fibrillar cartilage collagen, so `Col11a1` and `Col2a1` are not
paralogs or same-complex partners; they are useful mainly as represented
collagen/ECM negative controls in the same assay.  The putative collagen XXV
receptors PTP-sigma and PTP-delta come from developing motor neurons and target
muscle, not from juvenile thalamic neurons.  The prediction also cannot exclude
changes in extracellular matrix deposition, protein cleavage, Abeta binding,
motor-axon morphology, or developmental phenotypes, because the endpoint is
only nuclear mRNA differential expression in the assayed cell group.
