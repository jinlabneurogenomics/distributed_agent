# Rnf13 DEG-count prediction

## Question and resolved ambiguities

The requested endpoint is a point prediction of `n_degs` for each completely
held-out perturbation in `151 TH Prkcd Grin2c Glut`, where `n_degs` is the
number of measured mouse genes with Scanpy Wilcoxon Benjamini-Hochberg
`pvals_adj < 0.05` in the focal thalamic glutamatergic cell group.  The
requested manifest contained one held-out target, `Rnf13`, so there was no
ranked or partially ranked supervision to preserve.

I treated a predicted zero as "no gene crosses this FDR threshold in this
assay", not as evidence that Rnf13 has no neuronal biology.  If the Rnf13
self-transcript were significant in the withheld experiment it would count in
the endpoint, matching the supplied training counts.

## Sources used

- Declared training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression Parquet:
  `training differential-expression dataset`.
- Requested-target CSV:
  `single-target request for Rnf13`.
- Internal same-experiment semantic layer: PerturbAI atlas July
  260713/sourceguard/1773 v1 Findings ledger, queried only for non-held-out
  training analogs and counterexamples.  I used the packaged summaries for
  `Amfr`, `Ap3b1`, `Atf6`, `Hspa5`, `Marchf6`, `Mib1`, `Rab7`, `Rnf216`, and
  `Rnf220`; these reports are interpretations of the same experiment and were
  not counted as independent replication.
- NCBI PubMed was searched for external RNF13 and MARCH6/RAB7 mechanism papers.

The output files were generated in the working run directory.  I did not query
same-experiment full reports or Findings for the held-out gene `Rnf13`.

## Dataset calibration

The focal training count table contains 1,674 non-held-out perturbations.  Its
response breadth is highly zero-inflated:

| summary | value |
| --- | ---: |
| perturbations with 0 DEGs | 1,205 |
| perturbations with exactly 1 DEG | 276 |
| nonzero perturbations | 469 |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |

For biologically selected analogs, I queried the Parquet at
`group_name == "151 TH Prkcd Grin2c Glut"` and counted rows with
`pvals_adj < 0.05`; each queried perturbation had 17,259 measured genes and
23,679 matched controls in this group.  The focal counts agreed with the
training CSV.

| training perturbation | focal `n_degs` | expression-pattern evidence in the focal group | relationship to Rnf13 |
| --- | ---: | --- | --- |
| `Rnf216` | 0 | no focal FDR hits | Ubiquitin ligase disease gene; the July corpus also reports no downstream FDR<0.10 genes in any recovered neuronal group. |
| `Rnf220` | 0 | no focal FDR hits | RING-family ubiquitin ligase; pan-neuronal transcriptional buffering in the July corpus. |
| `Amfr` | 1 | only `Amfr` itself was significant, LFC -1.045 | ER/Golgi RING ERAD E3 ligase; closer to RNF13 as a membrane E3 than core proteasome genes. |
| `Atf6` | 0 | no focal FDR hits | Canonical ER-stress transcription factor; a negative control for tonic basal UPR release. |
| `Hspa5` | 5 | `Hsp90b1`, `Nfe2l1`, `Pdia4`, and `Derl3` were up; `Erc1` was down | Positive control that the assay can see a small ER chaperone/ERAD response. |
| `Vcp` | 2 | weak `Rasgef1b` up and `Nsmf` down hits | ERAD/protein-extraction AAA ATPase; low count argues against generic ERAD loss producing many DEGs. |
| `Marchf6` | 14 | compact sterol/SREBP2 module: `Insig1`, `Dhcr24`, `Cyp51`, `Msmo1`, `Hmgcr`, `Fdft1`, `Hmgcs1`, `Ldlr`, `Sqle`, `Srebf2`, and related genes up | ER-membrane E3 that specifically gates cholesterol-synthesis enzymes; a partial counterexample because it is a membrane E3 but its expression program is substrate-specific. |
| `Mib1` | 27 | same sterol genes were up, with larger LFCs than `Marchf6` | E3 ligase counterexample whose focal effect converged on sterol biology despite a different known Notch function. |
| `Ap3b1` | 0 | no focal FDR hits | The AP-3 adaptor is directly relevant because RNF13's dileucine motif supports AP-3-dependent endolysosomal localization. |
| `Lamp2` | 0 | no FDR hit; `Lamp2` self-transcript was near the threshold at q = 0.0537 | Lysosomal membrane counterexample. |
| `Sqstm1` | 1 | only the `Sqstm1` transcript was significant | p62/autophagy/Nrf2 node implicated in some RNF13 gain- and loss-of-function studies, but not a broad focal DEG response. |
| `Stx1b` | 0 | no focal FDR hits | Synaptic vesicle/SNARE counterexample; RNF13 has been reported to regulate Snapin-SNAP25 SNARE assembly. |
| `Rab7` | 501 | a broad lysosomal and stress state, including `Atp6v1b2`, `Ptgds`, `Dpp7`, `Scpep1`, `Insig1`, and `Atp2a2` | Terminal late-endosome/autophagosome-lysosome GTPase counterexample showing the assay can detect catastrophic endolysosomal stress. |

The decisive within-dataset pattern is that broad responses occurred when
perturbations directly hit core, limiting cellular functions, such as the
`Rab7` late endosome/autophagy axis or the `Marchf6`/`Mib1` sterol module.  In
contrast, several E3 ligases, a proximal ERAD ligase, AP-3 cargo sorting, and
individual synaptic or lysosomal membrane perturbations were silent or had only
one to five DEGs.

## Biological transfer to Rnf13

RNF13 is a membrane-associated RING E3 ubiquitin ligase.  Bocock et al. showed
that murine RNF13 is a type-I endosomal/lysosomal membrane protein whose RING
domain can be proteolytically released to the cytoplasm and mediate
ubiquitination (Bocock et al., 2009, DOI: 10.1111/j.1742-4658.2009.06913.x).
RNF13 can also participate in neuronal synaptic biology: germline Rnf13-null
mice had impaired spatial learning and altered hippocampal synaptic vesicle
ultrastructure, and RNF13 promoted Snapin ubiquitination and Snapin-SNAP25
association (Zhang et al., 2012, DOI: 10.1007/s00018-012-1103-5).  Human
RNF13 variants have been linked to developmental and epileptic encephalopathy
through altered AP-3 association and endolysosomal targeting (Cabana et al.,
2021, DOI: 10.3390/cells10113063), and biallelic splice variants were reported
in a recessive ALS pedigree (Khani et al., 2022, DOI:
10.1136/jmg-2022-108645).

These mechanisms make a neuronal phenotype plausible, but they do not imply a
large acute nuclear RNA response in the P16-to-P37/P44 sparse CRISPR design:

- Intervention: four CRISPR guides perturb Rnf13 in postmitotic neurons; the
  mean platform-wide knockdown is partial at the mRNA level, and protein loss is
  unmeasured.
- Direct consequence: loss of an endolysosomal RING E3 and altered substrate
  ubiquitination, AP-3-dependent localization, and possibly Snapin/SNARE
  regulation.
- Propagation: the nearest measured branch in the training set is AP-3 cargo
  selection (`Ap3b1`) and selective lysosomal/synaptic components (`Lamp2`,
  `Stx1b`, `Sqstm1`), all of which were flat or almost flat.  The training
  branch that was strongly transcriptional was `Rab7`, a more central late
  endosome/autophagy-lysosome GTPase.  RNF13 is not an obligate component of
  that Rab7 fusion machinery.
- Exposure and sampling: Rnf13 disease reports involve chronic development,
  germline alleles, or dominant mistargeted variants.  The focal assay is
  juvenile, mosaic, and survivor-conditioned, and would miss purely
  physiological, protein-trafficking, or slowly degenerative effects.
- Measured endpoint: `n_degs` counts BH-significant nuclear RNA shifts; it is
  not a direct readout of vesicle morphology, SNARE assembly, ubiquitination,
  lysosomal positioning, or synaptic function.

The ER-stress branch is also insufficient to move the count upward.  RNF13
overexpression or knockdown can affect IRE1alpha-JNK apoptosis under ER stress
(Arshad et al., 2013, DOI: 10.1074/jbc.M112.368829; Arshad et al., 2013, DOI:
10.3109/10799893.2013.863920), but this screen did not impose tunicamycin,
thapsigargin, ischemia, or a TLR/innate immune challenge.  In the basal
postnatal neuronal data, `Atf6` was 0, `Vcp` was 2, and `Amfr` was 1 in the
same focal group, whereas the Marchf6 sterol program had a known SQLE/HMGCR
substrate basis (Zelcer et al., 2014, DOI: 10.1128/MCB.01140-13; Chua et al.,
2019, DOI: 10.1042/BCJ20190418) that is not established for RNF13.

## Point prediction

I therefore predicted that `Rnf13` behaves like the buffered AP-3/endolysosomal
and ubiquitin-ligase analogs, not like `Rab7` or the sterol E3 outliers.  The
closest integer point is:

| target | predicted `n_degs` |
| --- | ---: |
| `Rnf13` | 0 |

## Limits

The prediction is an extrapolation because no close PA-TM-RING paralog such as
`Rnf167` was present in the focal training count table, and the held-out
`Rnf13` expression signature was unavailable by construction.  Rnf13 may affect
synaptic vesicle assembly, dendritic organelle distribution, p62/NRF2, STING,
or IRE1alpha without creating a BH-significant mRNA signature in recovered
thalamic neurons.  Conversely, a low-count call could miss a compact module if
Rnf13 has an unexpectedly nonredundant substrate in `151 TH Prkcd Grin2c Glut`.
The best measured counterexample is `Rab7`, but transfer from Rab7 would require
RNF13 loss to cause the same terminal late-endosomal fusion failure; the
available AP-3 and selective lysosome/synapse perturbations argue against that
chain.  None of the within-dataset signatures is independent biological
replication, because the Parquet and July Findings corpus are two
representations of the same PerturbAI experiment.
