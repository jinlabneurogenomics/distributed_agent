# DEG-count prediction trace

## Question and resolved ambiguities

The held-out target manifest contains one requested perturbation:

```text
Nav3
```

I predicted the number of genes that would have `pvals_adj < 0.05` after acute
AAV-PHP.eB CRISPR loss of `Nav3` in the `151 TH Prkcd Grin2c Glut` population.
I treated `151 TH Prkcd Grin2c Glut` as the thalamic glutamatergic Allen class
described in the run context, and I used the training CSV as the exact endpoint
definition because its counts are already the FDR 0.05 counts in that cell
group. The perturbation was held out, so I did not use any `Nav3` differential
expression rows. The same-experiment Distributed Agents corpus also had no `Nav3`
target node, Findings, or Claims; that absence was treated as missing coverage,
not as evidence for a null.

One important bookkeeping point is that the endpoint counts the targeted
transcript itself if that row passes FDR. Several pathway neighbors have
`n_degs = 1` solely because their own transcript was depleted. I used those
singletons as evidence that the guide set can be detected, but not as evidence
for a broad downstream expression state.

## Sources used

- Exact requested target: `144_Nav3.csv`.
- Exact endpoint for observed training perturbations:
  `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Full differential-expression parquet:
  `training_de_all_cell_groups.parquet`.
- Distributed Agents same-experiment semantic corpus release
  `perturbai-july-260713-sourceguard-1773-v1`.
- Distributed Agents mouse gene-annotation store over `genes.parquet`,
  `gene_membership.parquet`, and `gene_relationships.parquet`, including Gene
  Ontology membership terms for microtubule binding, microtubule-end
  localization, microtubule-cytoskeleton organization, and nervous-system
  development.
- PubMed literature for NAV3 and mechanistic analogs:
  Maes et al. 2002, DOI `10.1006/geno.2002.6799`; Ghaffar et al. 2024, DOI
  `10.1038/s42003-024-06466-1`; Kakar et al. 2024, DOI
  `10.1007/s00439-024-02718-6`.
- Same-experiment corpus references for observed comparators, including
  Dock3/Rac/WAVE studies and reviews (Namekata et al. 2010, DOI
  `10.1073/pnas.0914514107`; Namekata et al. 2012, DOI
  `10.1523/JNEUROSCI.4884-11.2012`; Rottner et al. 2021, DOI
  `10.1016/j.cub.2021.01.086`), netrin/DCC references
  (Rajasekharan and Kennedy 2009, DOI `10.1186/gb-2009-10-9-239`; Fazeli et
  al. 1997, PMID `9126737`; Finci et al. 2015, PMID `25881791`), Rac1
  references (Hua et al. 2015, DOI `10.1186/s13064-015-0049-3`; Reactome
  `R-HSA-2029465` and `R-HSA-2029456`), MACF1 references (Mouse Genome
  Informatics `MGI:108559`; Chen et al. 2006, PMID `16815997`; Goryunov et al.
  2010, PMID `20170731`; Ka et al. 2014, PMID `25224226`; Ka et al. 2017,
  PMID `27756764`), and TUBA1A/tubulin-autoregulation references (Lin et al.
  2020, PMID `31727855`; Aiken et al. 2017, PMID `29057214`).

## Dataset calibration

I first verified that `Nav3` is absent from the training count table and from
the focal rows of the held-out parquet. The training table contains 1,674
non-held-out targets in `151 TH Prkcd Grin2c Glut`; 469 had a nonzero FDR 0.05
count. The distribution is sharply zero-inflated and heavy-tailed:

```text
median = 0
75th percentile = 1
90th percentile = 2
95th percentile = 18
99th percentile = 436
max = 2677
```

For candidate comparators, I filtered the parquet to

```text
group_name == "151 TH Prkcd Grin2c Glut"
gene_target in selected Nav3 mechanistic analogs
```

and then counted rows with `pvals_adj < 0.05` and inspected the leading
FDR-ranked genes. The count in this cell group was the primary numerical
calibration; the corpus was used to check whether those perturbations were
mechanistically interpretable or known to be flat for the same reason.

## Target-specific reasoning

### Nav3

**External function.** `Nav3` encodes neuron navigator 3, one of the
vertebrate homologs of the `unc-53` cell-guidance family (Maes et al. 2002).
The Distributed Agents annotation store places mouse `Nav3` in microtubule organization,
negative regulation of microtubule depolymerization, positive regulation of
microtubule polymerization, microtubule binding, and the microtubule-end
compartment. Recent human genetic work connects NAV3 variants to
neurodevelopmental disorders and reports NAV3 expression in postmitotic
excitatory and inhibitory neurons; pathogenic NAV3 variants impair
microtubule-stabilizing activity, and zebrafish `nav3` knockdown perturbs
neural growth and behavior (Ghaffar et al. 2024; Kakar et al. 2024).

That biology pointed to three observed training neighborhoods:

1.  Local actin/Rac/WAVE/PAK effectors used by neurite and growth-cone systems.
2.  Netrin, Slit/Robo, IgSF-CAM, and semaphorin/plexin axon-guidance receptors.
3.  Microtubule plus-end, cytolinker, tubulin, and motor/transport genes.

**Dock3/Rac/WAVE neighborhood.** `Dock3` is a Rac GEF that stimulates axonal
outgrowth through WAVE recruitment and GSK3b/CRMP2-linked microtubule assembly
in retinal ganglion neuron assays. In the focal class, however, `Dock3`
produced **0** FDR 0.05 genes; its best row was `Bap1`, log2FC -1.21,
FDR 0.584, with 69 perturbed nuclei. `Rac1` also produced **0** focal DEGs
with a minimum focal FDR of 1.0. Direct downstream or adjacent nodes were all
flat or self-only: `Cdc42` **1**, only `Cdc42` down; `Pak1` **1**, only `Pak1`
down; `Pak2` **0**; `Pak3` **0**; `Limk1` **0**; `Tiam1` **0**; `Kalrn` **0**;
`Cfl2` **0**; `Cyfip1` **0**; `Cyfip2` **1**, only `Cyfip2` down. The
Distributed Agents corpus independently summarized the same-experiment result as a
buffered Rac/Cdc42-linked actin-cytoskeleton sector, with `Dock3` producing no
robust downstream snRNA-seq response and represented Rac/Cdc42/PAK/WRC/GEF/GAP
relatives failing to form a shared Cdc42- or Rac1-like transcriptomic module.

This argues that a NAV3 growth-cone or local actin/microtubule function is
unlikely to yield a broad nuclear RNA response in recovered P16-to-P37
postmitotic neurons.

**Axon-guidance receptor neighborhood.** The guidance receptors most
analogous to a UNC-53/NAV cell-guidance role were also nearly silent in the
exact endpoint. `Dcc` was **0** in the focal class, with FDR 1.0 for every
focal row; `Slit2` was **0**; `Robo2` was **0**; `Robo4` was **0**; `Unc5d`
was **0**. Several adhesion/guidance receptors had only self-transcript calls:
`Robo1` **1**, only `Robo1` down; `Unc5c` **1**, only `Unc5c` down; `L1cam`
**1**, only `L1cam` down; `Chl1` **1**, only `Chl1` down; `Ncam1` **1**, only
`Ncam1` down; `Cntnap1` **1**, only `Cntnap1` down; `Cntnap2` **1**, only
`Cntnap2` down; `Epha4` **1**, only `Epha4` down; `Sema5a` **1**, only
`Sema5a` down. `Nrcam` had **2**, its own transcript plus `Letm2`. The
same-experiment Dcc Claim in the Distributed Agents corpus made the broader point: P16
postmitotic perturbations across netrin/DCC/UNC5/DSCAM and Slit/Robo
neighborhoods did not produce a convergent soma-detectable guidance
transcriptome.

NAV3 is mechanistically closer to intracellular neurite navigation than to a
ligand receptor, but this comparator set is useful as a boundary: many genes
with dramatic wiring or adhesion phenotypes outside snRNA-seq did not show more
than a self transcript in this assay.

**Microtubule/cytolinker neighborhood.** The focal data did show that the assay
can detect a subset of cytoskeletal states. `Tuba1a` produced **7** DEGs:
`Tuba1a` down and `Tubb3`, `Tubb2a`, `Tuba4a`, `Tubb4a`, `Tubb4b`, and `Tubb5`
up. That is the expected tubulin-dosage/autoregulation program rather than a
generic growth-cone program, and the corpus explicitly treats it as a
Tuba1a-specific tubulin-isotype compensation response. The direct tubulin
paralogs were far smaller in the endpoint: `Tuba4a` **2**, `Tubb4b` **1**,
`Tubb5` **1**. Other microtubule-associated genes were null or self-only:
`Map6` **0**, `Map1b` **1**, `Kif2a` **0**, `Nin` **0**, and `Ttll5` **0**.
`Dctn1` was a true positive counterexample with **75** focal DEGs, but its
leading genes were a sterol/lipid response (`Insig1`, `Msmo1`, `Hmgcs1`,
`Cyp51`, `Hmgcr`, `Fdft1`, `Fasn`) plus `Dctn1` depletion. That program is a
core dynactin/transport stress state, not a NAV3-like plus-end navigator
signature.

I also checked `Macf1`, the microtubule-actin crosslinker. It was just below
the endpoint threshold in this focal class: `Atp1a3` log2FC -0.286, FDR
0.0532, so **0** genes at FDR 0.05. The Distributed Agents Macf1 Findings summarize a
near-global postnatal snRNA null, a lack of Wnt/beta-catenin transcription
despite detectable `Ctnnb1`, `Gsk3b`, and `Lrp6` responses, and no generic
cytolinker module with `Dst`, `Plec`, or `Map1b`. NAV3 is at least as likely
as MACF1 to act through local cytoskeletal geometry rather than a broad basal
nuclear transcriptome.

**Zero versus nonzero decision.** I predicted zero DEGs. The nonzero analogs
most relevant to NAV3 were mostly self-transcript singletons, while the
stronger `Tuba1a` and `Dctn1` cases are biologically special: TUBA1A depletion
engages tubulin autoregulation, and dynactin loss engages a sterol/lipid state.
NAV3 is not a tubulin isotype, not a core dynactin subunit, and not a
transcription factor or proteostasis factor of the sort that dominated the
large training-count tail. Its most direct predicted phenotypes are neurite
growth, microtubule plus-end behavior, migration, and morphology, all endpoints
that this single-nucleus RNA assay samples only indirectly.

My point prediction is therefore:

```text
Nav3 -> 0
```

## Limits

- `Nav3` itself was held out from both the parquet and the training DEG-count
  CSV, and it was not covered by the same-experiment Distributed Agents corpus, so this
  prediction is extrapolation from pathway neighbors rather than a measured
  same-target signature.
- The neuron-navigator paralogs were not available as clean training
  perturbations in this run. The comparison therefore falls back to Dock/Rac,
  axon-guidance, MACF1/cytolinker, and tubulin/microtubule genes rather than a
  direct NAV-family paralog.
- A one-gene self-transcript event is hard to predict. The true `Nav3` endpoint
  could be `1` if the gRNAs happened to reduce nuclear `Nav3` mRNA strongly
  enough even without any downstream response.
- snRNA-seq from recovered NeuN+ nuclei misses axon shafts, growth cones,
  dendritic spines, local protein localization, Rac-GTP/PAK/cofilin
  phosphorylation, microtubule plus-end dynamics, and structural wiring. Those
  are likely closer to NAV3 biology than steady-state somatic nuclear RNA.
- The perturbation is acute, mosaic P16 loss of function. It need not mimic
  germline NAV3 human variants, zebrafish embryonic knockdown, or long-term
  consequences of altered neuronal morphology.
