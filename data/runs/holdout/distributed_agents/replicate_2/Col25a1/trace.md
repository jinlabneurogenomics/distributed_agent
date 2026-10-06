# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and resolved ambiguities

The task asks for the held-out endpoint for each gene in
`044_Col25a1.csv`: the integer number of measured genes with
`pvals_adj < 0.05` after the target is knocked out in `151 TH Prkcd Grin2c
Glut` cells. The manifest contains a single requested target, `Col25a1`, and
`Col25a1` is absent from the focal training-count CSV as expected.

I interpreted the endpoint as the exact assay- and cell-group-specific
Benjamini-Hochberg count, including the target transcript if that row would be
significant. I did not treat a lack of `Col25a1` self-downregulation in the
training data as failed editing, because `Col25a1` itself was held out and
because the dataset context notes that measured target RNA is an imperfect
guide-engagement proxy.

## Sources used

- Raw same-experiment DE table:
  `[local file: training_de_all_cell_groups.parquet]`.
- Focal-cell training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Held-out target manifest:
  `[local file: 044_Col25a1.csv]`.
- The run-local dataset portrait and measurement registry, especially the
  caveats about sparse mosaic P16 CRISPR, survivor-conditioned NeuN+ snRNA-seq,
  and weak interpretability of the target transcript alone.
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`.
  `target_context(Col25a1)` returned no direct same-experiment claims, so I
  used the corpus only for pathway-near training perturbations. Relevant frozen
  Claims included:
  - `claim:8776fdbf2cceaae9902f`: represented integrin and laminin-receptor
    perturbations do not form a shared basal neuronal adhesion module.
  - `claim:a16c0edba1df304aaa48`: represented APP-processing, secretase,
    Notch, synaptic-adhesion, and APP-trafficking perturbations are largely
    uncoupled from a shared juvenile neuronal nuclear RNA module.
  - `claim:fea40917ad49d48e4705`: represented IL1RAP/IL1RAPL-PTPdelta
    synaptic-adhesion perturbations are not a shared postnatal neuronal mRNA
    module.
  - `claim:a457807c15e3a9a8f204`: netrin/DCC and Slit/Robo axon-guidance
    perturbations do not produce a convergent robust neuronal-soma RNA module.
  - `claim:9aea411fa0e464068554`: represented muscle AChR/NMJ pathway genes,
    including `Lrp4` and `Musk`, do not recover a shared NMJ transcriptional
    module in postnatal brain neurons.
- NCBI PubMed for public `COL25A1` biology:
  - Hashimoto et al., 2002, EMBO J, doi:10.1093/emboj/21.7.1524,
    PMID:11927537: discovered CLAC-P/collagen XXV as a type-II transmembrane,
    neuron-expressed collagen whose extracellular domain is furin-cleaved and
    binds fibrillar amyloid beta.
  - Osada et al., 2004, J Biol Chem, doi:10.1074/jbc.M413340200,
    PMID:15615705: mapped CLAC/amyloid-beta binding to the collagenous domain
    and showed in-vitro effects on Abeta fibril elongation.
  - Tanaka et al., 2014, J Neurosci, doi:10.1523/JNEUROSCI.2440-13.2014,
    PMID:24453327: Col25a1 knockout mice die neonatally from failed
    intramuscular motor-axon elongation, respiratory failure, and secondary
    spinal motor-neuron apoptosis.
  - Wakabayashi, 2021, Front Mol Neurosci, doi:10.3389/fnmol.2020.635375,
    PMID:33536873: reviewed collagen XXV as a MACIT transmembrane collagen
    specialized for neuromuscular development.
  - Natera-de Benito et al., 2022, Hum Mutat, doi:10.1002/humu.24333,
    PMID:35077597: reported recessive human `COL25A1` variants causing
    congenital cranial dysinnervation/arthrogryposis and summarized the
    collagen XXV interaction with motor-neuron PTPsigma/PTPdelta receptors.

## Computational checks

I used the focal training-count CSV to calibrate the response scale. The
distribution is zero-inflated: 1,205 of 1,674 training perturbations have
`n_degs = 0`, 276 have exactly one DEG, 87 have 2-9 DEGs, 63 have 10-99 DEGs,
and 43 have at least 100.

I then read the Parquet through `pyarrow.dataset` filters rather than loading
all 616M rows. The main queries were equivalent to:

```python
filter = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(candidate_targets)
)
```

and a second filtered query inspected self rows where `names == gene_target`.
This recovered 17,259 measured features for each selected target, the same
`pvals_adj < 0.05` counts as the CSV, and the best raw-p rows for each
candidate. I also computed self-target significance across focal training
targets by scanning rows whose measured gene was a training target; only 319 of
1,642 available self rows passed focal FDR 0.05, so a measured target mRNA is
not sufficient for a one-gene prediction.

I used the Distributed Agents runtime `profile_compare` tool on a hand-nominated cohort
of pathway-near observed targets
`Col11a1, Col2a1, Itgb1, Itga2, Itga6, Ptprd, Adam10, App, Ache, Musk, Lrp4,
Nrxn1, Dcc, Robo1, Plxna1` in the exact focal context. Eleven of the fifteen
had no significant focal feature and the other four were in the
`1_to_9_significant_features` bucket. Pairwise significant-feature
intersections among the inspected collagen/ECM/proteolysis/adhesion anchors
were zero; no hidden broad `Col25a1`-like module appeared.

## Target-specific reasoning

### `Col25a1`

**Mechanism expected from outside biology.** `Col25a1` encodes collagen
XXV/CLAC-P, an unusual type-II transmembrane collagen. The literature gives it
two clear biochemical or developmental settings: APP/A-beta binding after
furin ectodomain shedding, and embryonic neuromuscular innervation. The latter
is compelling genetically: germline Col25a1-null mice fail to extend motor
axons inside muscle and die at birth, and human recessive variants cause a
peripheral motor-innervation disorder. Those observations make `Col25a1` a
real cell-surface/ECM gene, but they do not predict an acute, cell-autonomous
nuclear RNA program in P16-P37/P44 thalamic glutamatergic neurons.

**Closest within-dataset analogs and counterexamples.**

| training perturbation(s) | focal `n_degs` | expression-pattern evidence | why this comparison matters |
|---|---:|---|---|
| `Col11a1`, `Col2a1` | 0, 0 | Neither collagen target had any focal FDR < 0.05 row. Their self rows were not significant: `Col11a1` logFC -0.172, adj. p = 1.0; `Col2a1` logFC +2.202, adj. p = 1.0. | They are the only collagen genes in the focal training endpoint. They are imperfect because they are fibrillar rather than MACIT collagens, but they show that collagen-family perturbation alone was not an active thalamic RNA-response class. |
| `Itga2`, `Itga4`, `Itga6`, `Itga7`, `Itga8`, `Itga9`, `Itgb1`, `Itga2b`, `Itgb2` | all 0 | The focal Parquet confirmed zero FDR genes for the inspected collagen/laminin receptors `Itga2`, `Itga6`, and `Itgb1`; all top raw-p rows had adj. p > 0.05. The same-experiment corpus separately summarized represented integrin and laminin-receptor perturbations as lacking a shared postmitotic neuronal adhesion module. | Integrin/focal-adhesion signaling is a natural route by which an ECM collagen perturbation might remodel transcription. In this assay that route was mostly silent. |
| `Ptprd`; receptor-PTP neighborhood | 0 for `Ptprd`; `Ptprc`, `Ptprf`, `Ptpro`, `Ptprt` also 0 and `Ptprm`, `Ptprn`, `Ptprn2` only 1 | `Ptprd` had zero focal FDR genes; the self row was only nominal, logFC -0.158, adj. p = 1.0. The corpus reports that represented receptor-type PTP and IL1RAP/IL1RAPL-PTPdelta perturbations do not form a shared acute neuronal RNA signature. | Collagen XXV can signal through motor-neuron PTPsigma/PTPdelta receptors in the developmental NMJ setting. `Ptprs` was not available in the count table, but `Ptprd` is the closest represented receptor and was RNA-quiet. |
| `Musk`, `Lrp4`, `Ache` | 0, 0, 1 | `Musk` and `Lrp4` had no focal FDR genes; `Ache` had exactly one, its own transcript, logFC -0.674 and adj. p = 0.00415. | These are not `Col25a1` partners in thalamus, but they test whether canonical NMJ genes generally create a brain-neuron endplate-like transcriptional program. The corpus concluded they do not. |
| `Adam10`, `App` | 0, 1 | `Adam10` had no focal FDR genes. `App` had one, its own transcript, logFC -1.420 and adj. p = 8.4e-58; no downstream APP-processing module was present. | CLAC-P is furin-shed and its ectodomain binds fibrillar Abeta, so the APP/secretase axis is a plausible amyloid-side comparator. Same-experiment evidence argues that these biochemical relationships are not reported as broad juvenile neuronal snRNA-seq responses. |
| `Dcc`, `Robo1`, `Plxna1`, `Nrxn1`, `Nrxn2`, `Nrxn3`, `Nlgn3` | `Dcc` 0, `Robo1` 1, `Plxna1` 0, `Nrxn1` 1, `Nrxn2` 0, `Nrxn3` 0, `Nlgn3` 1 | In the inspected focal rows, `Nrxn1` and `Robo1` each had exactly one significant feature and it was the self transcript; `Dcc` and `Plxna1` had zero. Corpus claims over axon-guidance and synaptic-adhesion neighborhoods likewise report flat, singleton, or nonconvergent somatic signatures. | `Col25a1` is a neuronal surface/axon-development factor. These genes are broader controls for whether acute loss of a structural axon/synapse cue triggers a detectable nuclear mRNA response; most do not. |

The Parquet rows for low or zero responders contain some very large nominal
logFC values for non-neuronal or rare transcripts with adj. p = 1.0. I treated
those as low-expression/pseudocount artifacts, consistent with the dataset
portrait, and relied on adjusted significance plus recurrence across
mechanistic comparators.

**Zero/nonzero call.** The focal training data contain no close positive
`Col25a1` analog. Direct collagen perturbations are zero, the represented
ECM/integrin and PTP-receptor neighborhoods are zero or singleton-only, and the
APP-processing route that could have connected CLAC-P to amyloid biology is
flat at the nuclear RNA level. The only argument for a nonzero count is the
possibility that acute `Col25a1` CRISPR lowers the measured `Col25a1` transcript
itself. Because focal self rows are significant for only a minority of training
targets and because the available collagen self rows were not significant, I
placed that possibility below the zero threshold.

## Prediction

I predict no focal FDR-significant genes for `Col25a1`:

| target_name | predicted_n_degs |
|---|---:|
| Col25a1 | 0 |

## Limits

- `Col25a1` itself had no same-experiment corpus record and no observed
  training signature, so this is an extrapolation from nearby ECM, adhesion,
  axon-guidance, NMJ, and APP-processing perturbations.
- The assayed cell type is thalamic glutamatergic; published `Col25a1`
  phenotypes are dominated by embryonic intramuscular motor innervation and
  muscle-derived collagen XXV. A lower motor-neuron, muscle, disease, or
  embryonic readout could be very different.
- `Col11a1` and `Col2a1` are collagens but not MACIT transmembrane collagens,
  and `Col13a1`/`Col23a1` were unavailable as focal training perturbations.
- The experiment measures nuclear RNA in recovered NeuN+ nuclei, not cell
  surface collagen shedding, amyloid peptides, matrix deposition, PTP receptor
  activity, synaptic architecture, axon branching, NMJ formation, or protein
  abundance.
- The point prediction is therefore best read as "no FDR 0.05 snRNA-seq DEG in
  this focal assay," not as biological unimportance of `Col25a1`.
