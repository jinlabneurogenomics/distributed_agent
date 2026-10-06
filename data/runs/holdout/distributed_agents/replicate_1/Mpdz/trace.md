# DEG-count prediction trace

## Question and endpoint

The requested held-out perturbation list contains one mouse target:

| target_name |
| --- |
| Mpdz |

I interpreted the task as a point prediction of the number of genes that would
pass `pvals_adj < 0.05` for an acute P16 AAV-CRISPR loss-of-function
perturbation of `Mpdz`, measured 3-4 weeks later by snRNA-seq in recovered
`151 TH Prkcd Grin2c Glut` neuronal nuclei. The readout is an assay- and
power-dependent DEG count, not the severity of germline loss of function, not a
protein-localization phenotype, and not viability before NeuN sorting.

The held-out `Mpdz` signature and its true count are absent from both supplied
inputs, so the endpoint is absent for `Mpdz` but directly observed for the
training perturbations.

## Sources used

- Declared training endpoint table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared Perturb-seq differential-expression table:
  `training differential-expression dataset`.
- Run-local requested-target manifest:
  `single-target request for Mpdz`.
- Run-local dataset portrait, task bindings, evidence coverage, capability
  manifest, and measurement registry under `codex_runtime/pipeline/`.
- Internal same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, specifically the bounded
  Findings ledger for visible comparators such as `Magi2`, `Grin1`, `Tsc2`,
  and `Ctnnb1`.
- NCBI PubMed searches and abstracts for external mechanism checks.

## Quantitative calibration from training perturbations

The focal training table has 1,674 non-held-out perturbations. It is strongly
zero-heavy:

| statistic | value |
| --- | ---: |
| zero-count perturbations | 1,205 / 1,674 |
| positive perturbations | 469 / 1,674 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2,677 |

The high tail was dominated by broad nuclear stress, RNA-processing,
proteostasis, transport, and transcriptional-regulator perturbations:
`Uba5=2677`, `Tpr=1768`, `Sin3a=1433`, `Rnpc3=868`, `Zbtb7a=841`,
`U2af2=828`, `Psmb4=742`, `Hnrnpu=733`, `Yy1=720`, and `Elp1=645`.

I then checked training perturbations that are functionally closer to MPDZ:
PDZ/MAGUK and synaptic scaffolds, synaptic adhesion or glutamate receptor
components that can use scaffold-localized signaling, and Wnt/planar-cell
polarity members that are adjacent to the epithelial-junction phenotypes of
MPDZ. Their directly observed focal counts were:

| training perturbation | focal n_degs | relationship to Mpdz |
| --- | ---: | --- |
| `Magi2` | 0 | large synaptic PDZ scaffold; useful buffered-scaffold comparator |
| `Shank2` | 0 | postsynaptic density scaffold |
| `Shank3` | 2 | postsynaptic density scaffold |
| `Dlg4` | 1 | PSD95 MAGUK scaffold |
| `Nlgn3` | 1 | synaptic adhesion molecule |
| `Nrxn1` | 1 | synaptic adhesion molecule |
| `Nrxn2` | 0 | synaptic adhesion molecule |
| `Nrxn3` | 0 | synaptic adhesion molecule |
| `Grin2a` | 1 | NMDAR subunit, less obligate than `Grin1` |
| `Grin2b` | 2 | NMDAR subunit and MUPP1-proximal biology |
| `Cacng2` | 0 | AMPAR auxiliary subunit, scaffolded at the PSD |
| `Cacng3` | 0 | AMPAR auxiliary subunit, scaffolded at the PSD |
| `Gria1` | 0 | AMPAR subunit |
| `Gria2` | 0 | AMPAR subunit |
| `Gria3` | 0 | AMPAR subunit |
| `Celsr2` | 1 | planar-cell-polarity receptor homolog |
| `Prickle1` | 0 | planar-cell-polarity component |
| `Fzd2` | 0 | Frizzled/Wnt receptor |
| `Fzd4` | 0 | Frizzled/Wnt receptor |
| `Fzd6` | 0 | Frizzled/Wnt/PCP receptor |
| `Fzd9` | 0 | Frizzled/Wnt receptor |

For expression-pattern evidence, the Parquet query over the focal cell group
confirmed that the listed close scaffolding and receptor perturbations were
either fully FDR-flat or had only one to two significant rows; for example,
`Dlg4`'s only focal FDR<0.05 row was `Dlg4` itself
(`log2FC=-0.444`, `p_adj=1.15e-08`). The same-experiment `Magi2` report was
also pan-neuronally flat: the July 260713 corpus summarized `Magi2` loss as
having no FDR<0.10 downstream response in 21 recovered neuronal groups, no
AMPAR/NMDAR/TARP/neuroligin/neurexin/dystroglycan/inhibitory-synapse
transcriptional program, and no strong signed-Wilcoxon cosine neighbor.

I treated the larger `Grin1`, `Ctnnb1`, and `Tsc2` counts as counterexamples,
not as high predictions for `Mpdz`. They show that this same thalamic class can
produce a large nuclear response when the intervention changes an obligate
receptor-to-nucleus, beta-catenin/Wnt-cadherin, or mTORC1 metabolic program:
`Grin1=89`, `Tsc2=86`, and `Ctnnb1=383` at FDR 0.05 in the training endpoint.
Those perturbations have direct signaling roles with known transcriptional
outputs. MPDZ is a scaffold for protein localization at junctional or synaptic
microdomains, so the stronger causal prior from the observed training set is
the buffered scaffold group rather than these nuclear-output counterexamples.

## External mechanism used for Mpdz

MPDZ/MUPP1 is a 13-PDZ-domain scaffold. Two major literatures are relevant but
their relationships to this readout are different.

First, severe `Mpdz` loss causes hydrocephalus through epithelial and ependymal
junctional biology. Feldner et al. 2017 generated mouse models and found that
global or Nestin-positive `Mpdz` loss impaired ependymal integrity, reduced the
interacting polarity protein Pals1, caused ependymal denudation and reactive
astrogliosis, and led to aqueductal stenosis
(EMBO Mol Med, DOI 10.15252/emmm.201606430; PMID 28500065). Yang et al. 2019
found that murine MPDZ-linked hydrocephalus involved choroid-plexus
hyperpermeability and increased CSF protein after `Mpdz` loss
(EMBO Mol Med, DOI 10.15252/emmm.201809540; PMID 30518636). Those results make
`Mpdz` biologically important, but the causal chain goes through choroid plexus,
epithelial barrier, ependyma, CSF flow, and gliosis. The PerturbAI task
samples NeuN-positive juvenile neurons after sparse postmitotic AAV editing and
largely excludes the epithelial and glial compartments, so this strong
external phenotype is a poor direct basis for a large `151 TH Prkcd Grin2c
Glut` nuclear DEG count.

Second, MPDZ has local neuronal scaffold functions. Krapivinsky et al. 2004
described a SynGAP-MUPP1-CaMKII complex at hippocampal synapses that regulates
p38 MAPK activity and NMDA-receptor-dependent AMPAR potentiation
(Neuron, DOI 10.1016/j.neuron.2004.08.003; PMID 15312654). Rama et al. 2008
showed that disrupting MUPP1-SynGAPalpha interaction modulated EPSCs without
occluding LTP (Mol Cell Neurosci, DOI 10.1016/j.mcn.2008.02.007; PMID
18417361). Estevez et al. 2008 found that MUPP1 binds the neuronal RhoA GEF
Tech in a PDZ-dependent fashion in rat hippocampal and cortical extracts
(J Neurochem, DOI 10.1111/j.1471-4159.2008.05472.x; PMID 18537874).
Li et al. 2011 localized AF6 and MUPP1 with Cx36-containing neuronal gap
junctions in rodent brain (Eur J Neurosci, DOI
10.1111/j.1460-9568.2011.07947.x; PMID 22211808). Tanabe et al. 2015 showed
that GPR37 forms a CASPR2-MUPP1 receptor complex in mouse brain and primary
hippocampal neurons (J Neurochem, DOI 10.1111/jnc.13168; PMID 25977097).

These neuronal studies support a real synaptic role but mainly at the level of
protein complex localization, channel/receptor traffic, and dendritic
structure. The visible acute CRISPR perturbations of analogous synaptic
scaffolds and receptors were FDR-flat or had one to two focal DEGs, arguing
that such local synaptic scaffolding defects often do not expand into a broad
steady-state nuclear transcriptome in this assay.

## Target-specific prediction

### Mpdz

Most relevant within-dataset analogs:

- `Magi2`, another large PDZ-domain synaptic scaffold, had `n_degs=0` in the
  focal endpoint and was summarized by the same-experiment corpus as lacking a
  robust downstream DE surface across recovered neuronal groups.
- `Dlg4`, `Shank2`, `Shank3`, `Nlgn3`, `Nrxn1`, `Nrxn2`, `Nrxn3`,
  `Grin2a`, `Grin2b`, `Cacng2`, `Cacng3`, and `Gria1-3` bracketed the
  postsynaptic receptor/adhesion neighborhood and ranged from 0 to 2 focal
  DEGs except for the obligatory NMDAR subunit `Grin1`.
- `Celsr2`, `Prickle1`, `Fzd2`, `Fzd4`, `Fzd6`, and `Fzd9` bracketed planar
  cell polarity and Wnt-receptor biology near MPDZ's epithelial polarity
  literature and were also 0 to 1 focal DEGs.
- `Grin1`, `Tsc2`, and `Ctnnb1` were informative counterexamples with many
  DEGs, but each has a direct, established transcription-coupled signaling
  axis absent from the MPDZ local-scaffold model.

Zero/nonzero rationale: `Mpdz` is predicted to be nonzero only if acute
neuronal loss of the scaffold destabilizes enough NMDAR/AMPAR, RhoA, CASPR2,
or electrical-synapse signaling in this thalamic glutamatergic group to drive a
coordinated nuclear adaptation. The training data argue against that: the
closest synaptic scaffold and adhesion perturbations mostly stay at zero, the
one available large PDZ scaffold `Magi2` is completely buffered in the focal
endpoint, and the epithelial/ependymal hydrocephalus mechanism is poorly
sampled by NeuN-positive nuclei. I therefore predict no genes crossing FDR
0.05.

Point prediction: `0` DEGs.

## Limits and uncertainty

This prediction is extrapolative because `Mpdz` itself and its expression
signature were held out. The closest epithelial tight-junction partners
`Mpp5/Pals1`, `Crb1/2/3`, `Pard3`, and `Tjp1-3` were not visible training
targets in the supplied focal endpoint table, so I used synaptic PDZ
scaffolds, receptor components, and the Wnt/PCP edge as imperfect neuronal
analogs. External MPDZ work often uses germline, conditional developmental, or
cultured-cell perturbations, while the screen is sparse postnatal AAV-CRISPR;
phenotypes requiring earlier neuroepithelial morphogenesis, choroid-plexus
barrier failure, ependymal loss, glial reaction, or whole-brain CSF changes
would not be directly reproduced in single postmitotic thalamic neurons.

The endpoint is also thresholded. A count prediction of zero means the expected
steady-state nuclear response is below the FDR<0.05 detection boundary in this
cell group, not that MPDZ has no local synaptic or junctional function.
