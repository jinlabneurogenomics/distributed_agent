# Prediction trace

## Question and resolved ambiguities

The held-out manifest for this run contains one target:

| requested target | focal cell group |
| --- | --- |
| Camk4 | `151 TH Prkcd Grin2c Glut` |

I interpreted `n_degs` exactly as the number of measured genes whose focal-cell Wilcoxon `pvals_adj` is below 0.05 after perturbing that target. The count includes the target transcript itself if the knockout measurably lowers its own RNA. `Camk4` is absent from both the training endpoint CSV and from `gene_target` in the differential-expression parquet, so I did not use a `Camk4` profile or count.

I treated the endpoint as an assay- and power-dependent breadth count rather than as a direct measure of biological importance. In this AAV CRISPR design, many real, expressed neuronal targets have zero or one FDR-significant gene, either because the biology is buffered in the unstimulated postnatal state or because the mosaic perturbation produces a weak partial mRNA effect.

## Sources used

- Input training count table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"`.
- Requested-target manifest: `[local file: 029_Camk4.csv]`.
- Same-experiment Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`. `target_context(Camk4)` returned no direct Camk4 findings or claims, so it did not provide a same-experiment curated Camk4 mechanism.
- Distributed Agents runtime observed-profile tools. I compared a caller-declared focal-cell cohort of calcium/CaM, NMDA receptor, CREB, PKA, calcineurin, and MEF2 perturbations and then inspected the compact pair tables.
- NCBI PubMed for public mechanism around CaMKIV, CaMKK, CREB, BDNF, LTP, and germline Camk4 phenotypes.

## Dataset calibration

The focal training endpoint is highly zero-inflated:

| statistic | value |
| --- | ---: |
| training perturbations | 1,674 |
| zero-DEG perturbations | 1,205 |
| nonzero perturbations | 469 |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2,677 |

Thus a count in the 5-15 range is already above most perturbations in this focal cell type, while the very broad responses are driven by chromatin, RNA-processing, proteasome/ubiquitin, or essential trafficking genes rather than by the neuronal activity pathway.

For the focal parquet rows I computed, for a curated set of mechanistic neighbors, each perturbation's number of `pvals_adj < 0.05` rows, target self-row log fold change, and leading significant rows. I also ran `profile_compare` over the same set using signed `logfoldchanges` and `pvals_adj < 0.05` to check whether these candidate analogs formed a convergent FDR-level module. The central observation from the profile comparison was sparse convergence: among 24 calcium/CREB-adjacent profiles, 10 had no significant genes, 11 had 1-9, 2 had 10-49, and only `Grin1` had at least 50.

## Camk4

### Same-dataset analogs and counterexamples

`Camk4` is a Ca2+/calmodulin-dependent kinase, activated through the CaMKK/CaMKI/CaMKIV cascade, that can signal to nuclear CREB. CaMKK1/2 and CaMKI were not available as training perturbations, so the closest within-dataset evidence came from upstream Ca2+/calmodulin genes, NMDA/Ca-channel genes that can feed Ca2+ into the pathway, PKA/CREB transcriptional components, and the calcineurin/MEF2 branch that shares Ca2+/calmodulin dependence but is not a direct Camk4 phenocopy.

| training perturbation | observed `n_degs` | focal-cell evidence and interpretation |
| --- | ---: | --- |
| `Camk2a` | 0 | CaMK family comparator, but mainly a synaptic CaMKII rather than nuclear CaMKIV; no FDR genes despite 122 perturbed nuclei and weak self-row depletion, `Camk2a` log2FC -0.16, FDR 1. |
| `Camk2b` | 1 | CaMKII paralog. The only FDR gene was the target itself, log2FC -0.44, FDR 1.27e-10. This shows target engagement in the pathway can still leave no downstream FDR signature. |
| `Camk2g` | 0 | CaMKII paralog with no FDR genes; its self row was log2FC -0.66 but not FDR-significant, likely reflecting lower usable expression or power. |
| `Camkmt` | 0 | CaMKMT modifies calmodulin rather than acting as CaMKIV; zero DEGs make it a weak negative comparator. |
| `Calm1` | 14 | Direct upstream calmodulin gene. It had strong self depletion, log2FC -0.92, FDR 1.67e-34, and 13 additional FDR genes such as `Rasgrp2`, `Peg3`, `Aifm3`, `Tuba1b`, and `Resp18`. This is the broadest direct CaM/CaMK training hit. |
| `Calm2` | 0 | Redundant calmodulin paralog, no FDR genes and no significant self depletion. |
| `Calm3` | 1 | Redundant calmodulin paralog; the sole hit was `Calm3` itself, log2FC -0.97, FDR 5.38e-25. |
| `Creb1` | 10 | Downstream activity-dependent transcription factor. FDR genes included `Crem`, `Tmem181a`, `Txndc12`, `Chkb`, `Nceh1`, `Ppox`, `Vwc2l`, `Rnf139`, and `Sez6l2`. This is a good ceiling-like comparator because CREB integrates CaMKIV plus PKA/ERK/MSK inputs. |
| `Crebbp` | 8 | CREB coactivator and histone acetyltransferase; only eight FDR genes and no strong self-depletion. It supports a narrow transcriptional-output expectation for partial disruption of CREB-mediated transcription in this cell group. |
| `Ppp3ca` | 4 | Calcineurin catalytic subunit, another CaM-dependent enzyme; strong self depletion, log2FC -0.48, FDR 6.35e-12, but only four total FDR genes. It is mechanistically adjacent but can oppose CaMK signaling. |
| `Ppp3r1` | 9 | Calcineurin regulatory subunit with nine FDR genes, including target self-depletion, `Pcsk1n`, `Ptprs`, `Atp2a2`, and `Coro6`. It suggests that a CaM-dependent nuclear signaling change can be detectable but still below 10 DEGs. |
| `Mef2a`, `Mef2c`, `Mef2d` | 4, 1, 0 | MEF2 transcription factors are calcium-regulated developmental/activity factors but not direct CaMKIV paralogs. Their focal perturbations were extremely sparse. |
| `Grin1` | 89 | Obligatory NMDA receptor subunit and the one broad calcium-entry analog. It produced target self-depletion plus many synaptic/neuroendocrine genes such as `Scg2`, `Stmn4`, `Kctd16`, `Gpm6a`, `Tspan7`, and `Jun`. I treated it as an upper boundary rather than a Camk4 phenocopy because loss of NMDAR signaling perturbs ion flux and synaptic signaling upstream of many cascades. |
| `Grin2a`, `Grin2b`, `Grin2d`, `Grin3a` | 1, 2, 0, 0 | NMDAR subunit perturbations other than `Grin1` were self-only or nearly flat, showing that a calcium-input gene can be buffered when it is non-obligate or redundant. |
| `Cacna1g` | 12 | The only voltage-gated Ca-channel subunit in the 5-20 DEG band; other tested `Cacna` and auxiliary channel targets were 0 or 1. This is relevant as another calcium-entry comparison but does not argue for a broad response. |
| `Ntrk2`, `Braf`, `Map2k1`, `Prkaca`, `Prkar1a`, `Gsk3b`, `Hdac5`, `Ep300` | 3, 4, 4, 1, 1, 6, 0, 0 | Alternative routes to CREB or activity-regulated transcription were modest to flat. These counterexamples argue against assigning a high DEG count solely because `Camk4` can impinge on CREB. |

In the runtime pair table, the core profiles did not share a set of significant genes: for `Camk2a`, `Camk2b`, `Calm1`, `Creb1`, and `Grin1` against the ten closest selected peers, positive-significant intersections were zero in every inspected pair and negative-significant intersections were at most one. Whole-profile Pearson/cosine values were moderate, but with so few FDR genes those correlations mostly reflect weak signed tails and are not strong phenocopy evidence. This made the DEG-count calibration more informative than any particular neighbor's rank.

As an additional sanity check, `Camk4` itself was present as a measured gene in all 1,674 focal training profiles, and other perturbations almost never shifted it: median adjusted p-value was 1.0, mean log2FC was -0.015. The training data therefore did not reveal a recurrent upstream program that strongly changes Camk4 expression in this resting focal group.

### External mechanism

Public evidence places CaMKIV in a nuclear Ca2+/CaM signaling route to CREB and activity-regulated transcription:

- Soderling 1999, DOI `10.1016/s0968-0004(99)01383-3`, reviewed the CaMKK-CaMKI/CaMKIV cascade and the ability of nuclear CaMKIV to regulate transcription through CREB phosphorylation.
- Shieh et al. 1998, DOI `10.1016/s0896-6273(00)81011-9`, showed that constitutively active CaM kinase IV, but not CaM kinase II, activates the calcium-responsive BDNF exon III promoter through an intact CRE/CREB element in cortical neurons.
- Kasahara et al. 2001, DOI `10.1074/jbc.M100247200`, observed transient nuclear CaMKIV activation, CREB phosphorylation, and c-Fos induction during rat hippocampal LTP, linking CaMKIV to activity-dependent CREB-regulated expression.
- Fukushima et al. 2008, DOI `10.1523/JNEUROSCI.2625-08.2008`, found that forebrain CaMKIV overexpression increased learning-induced CREB activity and improved memory formation in mice.
- Takao et al. 2010, DOI `10.1371/journal.pone.0009460`, reported that germline CaMKIV knockout mice had relatively selective behavioral abnormalities with intact spatial reference and working memory, consistent with partial redundancy or compensation in vivo.

### Zero/nonzero decision

The biological prior is not zero: a loss of CaMKIV should be able to perturb CREB-linked activity transcription in postmitotic neurons. However, this assay profiles unstimulated juvenile-to-young-adult nuclei after sparse acute AAV CRISPR, not depolarized cultured neurons or a germline forebrain overexpression model. The direct same-dataset CaM/CaMK, CREB, PKA, calcineurin, MEF2, Ntrk/MAPK, and channel perturbations nearly all landed between 0 and 14 DEGs; several were self-only despite strong target RNA knockdown. `Grin1` at 89 is a real calcium-pathway counterexample, but I downweighted it because an obligate NMDA receptor subunit is upstream of many calcium- and synapse-dependent processes, whereas CaMKIV is one nuclear branch with CREB redundancy through PKA/ERK/MSK.

I therefore predicted a detectable but narrow response, slightly below `Creb1`/`Crebbp`/`Ppp3r1` and much below `Grin1`:

| target | prediction |
| --- | ---: |
| `Camk4` | 6 |

## Limits

The strongest limitation is that `Camk4` itself was held out, and CaMKK1/2 were not available as observed perturbations, so no training signature directly tests the immediate upstream kinase of CaMKIV. Many low-count training profiles are dominated by target self-depletion and a few idiosyncratic FDR calls, which makes pairwise signature overlap a weak guide. The PubMed evidence mostly comes from hippocampal or cortical neurons under depolarization/LTP, or from constitutive Camk4 loss or overexpression, while the requested assay is acute, partial, sparse CRISPR loss of function in a specific thalamic glutamatergic population under baseline conditions. The exact count is therefore an extrapolation; the confident part of the prediction is that `Camk4` should be far closer to the 0-14 DEG calcium/CREB cluster than to the broad RNA-processing or proteostasis hits in the training endpoint.
