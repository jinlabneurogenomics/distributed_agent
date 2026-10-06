# Held-out DEG-count prediction

## Question and endpoint

The requested manifest contains one held-out target, `Atf2`. I interpreted the task as a point prediction for the number of measured genes that will have `pvals_adj < 0.05` after `Atf2` CRISPR loss-of-function in `151 TH Prkcd Grin2c Glut` nuclei. I treated the value as the assay endpoint from the same Scanpy Wilcoxon/BH pipeline used for the training counts: zero means no measured downstream gene crosses the adjusted-p threshold in this focal cell group, not that ATF2 is biologically irrelevant or that the gRNAs failed to cut.

The target was absent from both supplied training inputs, so I inferred it from non-held-out perturbations of AP-1/ATF/CREB relatives, MAPK inputs, and other activity/stress transcriptional regulators, then calibrated the final count to their observed focal-cell DEG counts.

## Sources used

- `training_de_all_cell_groups.parquet`: per-gene signed Wilcoxon differential-expression statistics for all non-held-out perturbations.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: focal-cell DEG counts for 1,674 non-held-out perturbations. This distribution is sparse: 1,205/1,674 training targets have 0 DEGs, the median is 0, the 75th percentile is 1, and only the largest 5% exceed 18 DEGs.
- `019_Atf2.csv`: requested target order; it contains only `Atf2`.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`, via `target_context` and `candidate_set_topology`.
- Distributed Agents run-local profile tools. I compared a 16-target ATF/CREB/AP-1/MAPK analog cohort in `151 TH Prkcd Grin2c Glut` using `logfoldchanges` as the signed profile and `pvals_adj < 0.05` as the significant-feature threshold.
- Independent PubMed literature for ATF2 biology:
  - Gozdecka and Breitwieser 2012, DOI `10.1042/BST20110630`, PubMed `22260696`: review of ATF2 and ATF7 as AP-1-family MAPK-regulated transcription factors.
  - van Dam et al. 1995, DOI `10.1002/j.1460-2075.1995.tb07168.x`, PubMed `7737130`: stress-activated protein kinases phosphorylate ATF2 on Thr69/Thr71 and induce `c-jun` through c-Jun/ATF2 sites.
  - Liu et al. 2006, DOI `10.1038/sj.emboj.7601020`, PubMed `16511568`: ATF2 and c-Jun dimerization/nuclear localization mutually regulate c-Jun promoter activity.
  - Yuan et al. 2009, DOI `10.1128/MCB.01344-08`, PubMed `19255142`: c-Jun/ATF2 heterodimers participate in neuronal apoptosis after trophic deprivation.
  - Ackermann et al. 2011, DOI `10.1371/journal.pone.0019090`, PubMed `21533046`: neuron-specific Atf2 loss causes embryonic brainstem motoneuron degeneration and altered JNK/p38 stress-kinase activity.
  - Maekawa et al. 2009, DOI `10.1038/emboj.2009.318`, PubMed `19893493`: ATF7, a close ATF2 relative, can connect p38 signaling to stress-dependent transcriptional derepression in raphe neurons.

## Computational checks

I first intersected obvious ATF2 pathway and family symbols with the 1,674 training-count targets. The focal DEG counts were:

| training perturbation | focal `n_degs` | relevance to `Atf2` |
|---|---:|---|
| `Creb1` | 10 | CRE/ATF-family bZIP transcription factor; closest represented nuclear CRE-family positive comparator |
| `Crebbp` | 8 | CBP coactivator used by CREB/AP-1/ATF programs |
| `Jund` | 0 | represented JUN/AP-1 dimerization relative |
| `Fosl2` | 0 | represented FOS/AP-1 dimerization relative |
| `Atf6` | 0 | same ATF name family but UPR branch; a weak counterexample, not a close ATF2 paralog |
| `Mapk9` | 0 | JNK2, upstream stress kinase for ATF2/JUN signaling |
| `Mapk1` | 0 | ERK2/MAPK comparator |
| `Map2k6` | 0 | p38-pathway MAP2K comparator |
| `Map3k7` | 0 | stress/NF-kB/JNK/p38-adjacent MAP3K comparator |
| `Maf` | 0 | bZIP/AP-1-family relative |
| `Mafb` | 0 | bZIP/AP-1-family relative |
| `Nfe2l2` | 0 | CNC/bZIP stress-response comparator |
| `Mafg` | 1 | small-MAF/CNC bZIP comparator |
| `Mef2a` | 4 | activity/MAPK-responsive transcription factor |
| `Mef2c` | 1 | activity/MAPK-responsive transcription factor |
| `Map2k1` | 4 | MEK1; its DEGs were `Vgf`, `Ptpn5`, `Etv5`, `Unc13a` |
| `Ntrk2` | 3 | BDNF/TrkB receptor upstream of ERK/CREB in stimulated neurons |
| `Prkaca` | 1 | PKA catalytic subunit; only `Prkaca` itself crossed FDR |
| `Camk2b` | 1 | calcium/CaMK comparator; only `Camk2b` itself crossed FDR |

For the 16-node analog cohort that included the most direct rows above, `profile_compare` confirmed 7/16 had no FDR-significant features and 8/16 had only 1-9 features in the focal group. `Creb1` and `Crebbp` were the only cohort members with more than a few downstream FDR hits, with 10 and 8 significant genes respectively. Direct parquet filtering of `pvals_adj < 0.05` recovered the exact `Creb1` and `Crebbp` focal signatures: `Creb1` had `Crem` up plus a small set including `Tmem181a`, `Txndc12`, `Chkb`, `Nceh1`, `Ppox`, `Rnf139`, `Sez6l2`, and `Vwc2l` down; `Crebbp` had 8 different hits including `Stxbp2` up and `Rtn4rl1`, `Dgkz`, `Rbfox2`, and `Stmn4` down. The two signatures did not share an FDR-significant gene within the inspected analog cohort, and the null AP-1/JNK nodes did not reveal a hidden shared significant feature set.

I also directly inspected the focal log-fold changes of AP-1/ATF readout genes after these analog perturbations. `Creb1` loss increased `Crem` at FDR `3.8e-07`, showing that a CRE-family response can be detected in this cell group. By contrast, `Atf2`, `Atf7`, `Jun`, `Junb`, `Jund`, `Fos`, `Fosb`, `Fosl2`, `Atf3`, and `Atf4` were FDR-null in the represented AP-1/JNK/MAPK perturbations, consistent with the same-experiment Distributed Agents findings that `Jund`, `Fosl2`, and `Mapk9` loss are broadly buffered and nonconvergent in postnatal basal neuronal snRNA-seq.

## Target-specific reasoning

### `Atf2`

ATF2 is a stress- and MAPK-regulated bZIP transcription factor. Literature makes it a plausible neuronal regulator: JNK and p38 can phosphorylate ATF2, ATF2 forms functional heterodimers with c-Jun at CRE/AP-1-like sites, ATF2/c-Jun participates in neuronal apoptosis models, and neuron-specific Atf2 deletion disrupts embryonic brainstem motoneuron survival. Those data argue against treating `Atf2` as an arbitrary unexpressed or biologically inert gene.

The same-experiment analogs, however, point to strong buffering for exactly the basal postnatal context assayed here:

- Direct `Atf2` paralogs were not represented. `Atf7`, the closest functional backup, was absent as a perturbation target, so the best represented nuclear CRE-family comparator was `Creb1`, with only 10 focal DEGs.
- `Crebbp`, a broadly used coactivator for CREB/AP-1/ATF activity, had 8 focal DEGs and did not reproduce the `Creb1` `Crem`-centered response.
- The represented AP-1 dimerization relatives `Jund` and `Fosl2` both had 0 focal DEGs; Distributed Agents corpus findings for `Jund:F001-F003` and `Fosl2:F001-F004` describe nearly complete buffering and nonconvergence across basal postnatal neurons.
- Upstream stress-MAPK candidates were also silent in the focal cell group: `Mapk9`, `Map2k6`, `Map3k7`, and `Mapk1` all had 0 DEGs. The Distributed Agents `Mapk9` context specifically records no downstream FDR response and no AP-1/immediate-early, apoptosis, or autophagy transcript program after single JNK2 loss.
- Other activity/stress transcription factors and bZIP neighbors were either zero (`Atf6`, `Maf`, `Mafb`, `Nfe2l2`, `Egr2`, `Nr4a1`, `Nr4a3`) or singleton/few-hit effects (`Mafg`, `Mef2a`, `Mef2c`).

The internal corpus topology connected `Creb1`, `Fosl2`, `Jund`, `Mafg`, `Map2k6`, `Mapk9`, `Nfe2l2`, and `Atf6` through explicit same-experiment comparator findings, but those links were mostly negative contrasts: represented CREB/AP-1/EGR/bZIP/MAPK perturbations did not form a shared postnatal neuronal loss-of-function module. I therefore used `Creb1` and `Crebbp` as an upper bound for a detectable CRE/ATF-axis effect, while using `Jund`, `Fosl2`, and `Mapk9` as the more direct counterexamples for a single AP-1/stress-responsive factor under unstimulated juvenile conditions.

My point prediction is no significant genes for `Atf2` in `151 TH Prkcd Grin2c Glut`. Mechanistically, a weak positive response of one or a few genes would not be surprising, but the expected center of mass is below one FDR 0.05 hit because the nearest represented AP-1 and JNK lesions were exactly zero, p38/JNK activation is normally stimulus-gated, and ATF2 has likely compensation by unperturbed ATF7/JUN/FOS/CREB-family partners in a sparse mosaic loss-of-function assay.

## Limits

- There is no observed `Atf2` signature in either input and no `Atf2` entry in the Distributed Agents same-experiment corpus.
- `Atf7`, `Atf3`, `Atf4`, `Jun`, `Junb`, `Fos`, `Fosb`, `Fosl1`, `Mapk8/Jnk1`, `Mapk10/Jnk3`, `Mapk14/p38`, `Map2k4`, and `Map2k7` were not training perturbations, so the most direct AP-1 and JNK/p38 redundancy tests are missing.
- The strongest external ATF2 literature comes from embryonic knockouts, injury/apoptosis, immune stimulation, stress, cancer, or reporter assays. Those support ATF2's pathway identity but are imperfect matches to P16 AAV sparse CRISPR in unstimulated, postmitotic juvenile thalamic glutamatergic neurons.
- The prediction extrapolates from small or null signatures. A rare ATF2-dependent subpopulation, an effect visible only at protein/phosphorylation/chromatin level, or a few individual downstream RNAs could be missed by this cell-group Wilcoxon endpoint.
