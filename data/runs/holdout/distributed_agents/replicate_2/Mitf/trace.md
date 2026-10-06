# Reasoning trace

## Question and resolved ambiguities

The held-out target list for this run contains one perturbation, `Mitf`.  I
therefore predicted the number of genes that would pass
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` after acute sparse
CRISPR loss of `Mitf` in `151 TH Prkcd Grin2c Glut` neurons.

`Mitf` itself is completely held out as a perturbation target, so I did not use
any `gene_target == Mitf` rows from the parquet or any observed `Mitf` count.
The decision was a transfer from non-held-out perturbations in the same
experiment, with external biology used only to choose which observed
perturbations are relevant analogs or counterexamples.

## Sources

- Input endpoint CSV:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest:
  `[local file: 138_Mitf.csv]`.
- Distributed Agents corpus MCP, release
  `perturbai-july-260713-sourceguard-1773-v1`, queried for claims and
  perturbation-centered findings around `Mc1r`, `Lrmda`, `Rab7`, `Tsc2`,
  `Atg5`, and `Becn1`.
- Distributed Agents runtime profile comparison over the local focal-cell DE rows,
  using Wilcoxon `scores` as signed expression vectors and `pvals_adj < 0.05`
  as the significance cutoff.
- External literature from NCBI PubMed:
  - Goding and Arnheiter, 2019, *Genes & Development*,
    DOI `10.1101/gad.324657.119`, PMID `31123060`: MITF is a bHLH-Zip
    MiT/TFE transcription factor and a central regulator of melanocyte and
    melanoma biology.
  - Yardman-Frank and Fisher, 2020, *Experimental Dermatology*,
    DOI `10.1111/exd.14260`, PMID `33320376`: the canonical
    alpha-MSH/MC1R/cAMP pathway induces melanocyte MITF and melanogenesis.
  - Sardiello et al., 2009, *Science*, DOI `10.1126/science.1174447`,
    PMID `19556463`: TFEB regulates the CLEAR lysosomal gene network.
  - Settembre et al., 2011, *Science*, DOI
    `10.1126/science.1204592`, PMID `21617040`: TFEB couples autophagy to
    lysosomal biogenesis.

## Computation over the training data

I first loaded the focal-cell endpoint CSV to establish the scale of this
assay.  There are 1,674 non-held-out targets in `151 TH Prkcd Grin2c Glut`;
the distribution is strongly zero-inflated:

| statistic | `n_degs` |
|---|---:|
| mean | 14.05 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| 99th percentile | 436 |
| max | 2677 |

I then filtered the parquet to
`group_name == "151 TH Prkcd Grin2c Glut"` and a hand-picked set of observed
`Mitf`-relevant comparators: pigment-lineage genes, MC1R/cAMP/CREB genes,
MiT/bHLH-Zip-adjacent genes, autophagy genes, and endolysosomal or mTOR
counterexamples.  Counts recomputed directly from the parquet matched the
training-count CSV.

I also ran a Distributed Agents runtime profile comparison on the same focal rows for
`Mc1r`, `Lrmda`, `Rab7`, `Tsc2`, `Vps35`, `Atg5`, `Atg16l1`, `Becn1`,
`Rb1cc1`, `Lamp2`, `Ctsb`, `Mtor`, `Creb1`, `Prkar1a`, and `Usf1`.  Each
profile used the signed Wilcoxon `scores` over 17,259 measured genes.  The
purpose was to check whether null or sparse same-pathway perturbations had
hidden whole-profile similarity to the broad `Rab7` or `Tsc2` lysosomal states.

## Target-specific reasoning for `Mitf`

### Direct pigment and melanocyte-lineage evidence

MITF is best known as a melanocyte-lineage transcription factor, with the
MC1R/cAMP axis as a classic upstream regulator of MITF-driven pigment genes
(Goding and Arnheiter 2019; Yardman-Frank and Fisher 2020).  The focal screen
sampled NeuN-positive postnatal brain nuclei, not melanocytes, retinal pigment
epithelium, mast cells, osteoclasts, or other lineages in which MITF biology is
canonical.  The closest observed pigment-pathway tests in the training data
were all flat in the focal thalamic glutamatergic population:

| observed target | focal `n_degs` | focal expression-pattern evidence | interpretation for `Mitf` |
|---|---:|---|---|
| `Mc1r` | 0 | Top-ranked rows in the parquet all had `pvals_adj = 1`; full-score cosines against lysosome/autophagy peers were near zero, e.g. `Mc1r` vs `Vps35` cosine `0.0216`, vs `Becn1` `-0.0045`, vs `Atg16l1` `-0.0016`. | MC1R is an upstream melanogenic receptor whose canonical output is MITF-linked pigmentation, so this is a relevant pigment-axis analog. Its null focal signature argues that the focal neurons do not carry a basal melanogenic transcriptional program. |
| `Lrmda` | 0 | No FDR genes; the two smallest adjusted p-values were still `0.907`, and cosines to candidate autophagy or lysosomal peers were similarly tiny, with all queried peer cosines between about `-0.013` and `0.037`. | LRMDA/C10orf11 is a pigmentation and melanosome/LRO-associated gene. A second independent pigment-lineage node remaining null supports lineage mismatch rather than a single failed `Mc1r` perturbation. |
| `Sox10` | 0 | No FDR genes in the focal count CSV. | SOX10 is an upstream neural-crest/melanocyte regulator; its zero count is a weak but directionally useful developmental-lineage counterpoint. |
| `Pax3` | 0 | No FDR genes in the focal count CSV. | PAX3 is another neural-crest and melanocyte-lineage regulator upstream of MITF; it was silent in this postmitotic thalamic readout. |

The Distributed Agents corpus directly matched this interpretation.  Its high-confidence
claim for `Mc1r` and `Lrmda` states that canonical melanogenic and melanosome
transcriptional programs are not recovered from either perturbation in
NeuN-positive neuronal nuclei.  The underlying `Mc1r` findings report zero
FDR<0.10 downstream genes in all 23 recovered neuronal cell groups and absence
of the expected MC1R/cAMP/MITF-linked pigment-gene program.  The underlying
`Lrmda` findings likewise report no robust downstream response in 22 recovered
groups, absence of a pigmentation/melanosome marker panel, and no meaningful
dataset-wide signature neighbor.

That is the strongest within-dataset evidence for a zero call.

### cAMP/CREB branch

MC1R can reach MITF through cAMP/PKA/CREB in melanocytes, but the assayed
cAMP/CREB branch was not a broad transcriptional driver in the focal cells.

| observed target | focal `n_degs` | focal pattern |
|---|---:|---|
| `Adcy1` | 0 | no FDR genes |
| `Adcy3` | 0 | no FDR genes |
| `Adcy5` | 0 | no FDR genes |
| `Prkaca` | 1 | the only FDR gene was `Prkaca` itself |
| `Prkar1a` | 1 | the only FDR gene was `Prkar1a` itself |
| `Creb1` | 10 | a small response, led by `Crem`, not a pigment program |

The Distributed Agents `Mc1r` context makes the same boundary: represented adenylyl
cyclases and PKA nodes were flat despite some target-RNA drops, while direct
`Creb1` perturbation produced only a small `Crem`-centered response.  This
makes it inappropriate to inflate the `Mitf` estimate on the assumption that
the canonical melanocyte cAMP-to-MITF circuit is tonically engaged in these
neurons.

### MiT/TFE, lysosome, and autophagy evidence

The exact MiT/TFE paralogs `Tfeb`, `Tfe3`, and `Tfec` were not present as
training perturbations in the focal endpoint table.  I therefore used weaker
downstream and pathway-adjacent evidence.  The lysosome/autophagy connection is
real for TFEB/MiT-family biology in other contexts: TFEB coordinates the CLEAR
lysosomal network and an autophagy/lysosomal-biogenesis program (Sardiello et
al. 2009; Settembre et al. 2011).  However, the focal training data separate
core autophagy or pigment/LRO loss from strong endolysosomal stress.

| observed target | focal `n_degs` | why it is or is not an analog |
|---|---:|---|
| `Atg5` | 0 | Core LC3-lipidation autophagy component; no focal FDR genes and no broad whole-profile similarity to other candidate peers. Corpus findings show `Atg5` is nearly flat in postnatal neurons and does not induce a canonical autophagy, lysosome, p62, proteasome, UPR, or ISR transcriptome. |
| `Atg16l1` | 0 | Same LC3-lipidation complex neighborhood; flat in the focal group, a counterexample to treating all autophagy genes as transcriptionally equivalent. |
| `Becn1` | 0 | Upstream VPS34/Beclin autophagy scaffold; flat in this focal group and only a restricted responder in other cell groups. |
| `Lamp2` | 0 | Lysosomal membrane target; its strongest focal row was `Lamp2` itself but missed FDR 0.05 (`pvals_adj = 0.0537`). |
| `Ctsb` | 1 | The one FDR gene was `Ctsb` itself, with no downstream lysosomal response. |
| `Rb1cc1` | 4 | Small ER/proteostasis-skewed focal response, far below a broad lysosomal stress program. |
| `Vps35` | 17 | A modest retromer response and useful positive control that endosomal perturbations can be detected, but not a pigment/MITF phenocopy. |
| `Rab7` | 501 | A strong late-endosomal/lysosomal and sterol-compensation perturbation. This is a counterexample, not a close `Mitf` analog: it directly perturbs late-endosome traffic and creates a broad stress state. |
| `Tsc2` | 86 | A strong mTORC1 metabolic/endolysosomal stress perturbation; mechanistically upstream of lysosome-nutrient signaling but opposite in nature to loss of a mostly lineage-restricted MITF transcription factor. |
| `Mtor` | 2 | Direct `Mtor` loss was sparse, supporting the corpus point that not every textbook mTOR/lysosome perturbation creates a broad RNA signature. |

The runtime profile comparison quantified the separation.  In 151 TH
Prkcd/Grin2c neurons, `Rab7` had 311 positive plus 190 negative significant
genes and `Tsc2` had 58 positive plus 28 negative significant genes.  `Mc1r`,
`Lrmda`, and `Atg5` had zero.  `Mc1r`/`Lrmda` shared no FDR-level intersections
with the lysosomal or autophagy peers because they had no FDR-level genes, and
their whole-profile correlations to the nonzero `Rab7`, `Tsc2`, `Vps35`,
`Mtor`, `Creb1`, and `Usf1` signatures were all tiny.  This argues against a
hidden low-amplitude lysosome-like pattern that should be extrapolated to
`Mitf`.

The Distributed Agents corpus also argues against a generic lysosomal extrapolation.  A
high-confidence claim over `Gnptab`, `Manba`, `Ppt1`, `Psap`, `Sort1`, and
`Tmem106b` states that acute perturbation of represented lysosomal
disease-related genes does not elicit a shared neuronal lysosomal-stress,
autophagy, TFEB/MiT, ISR, or UPR nuclear RNA program.  In the focal group those
same targets were `0`, `0`, `1`, `1`, `0`, and `1` DEGs, respectively.  The
corpus separates the large `Rab7` and `Tsc2` states as target-specific
late-endosomal or mTORC1 stress rather than as the expected outcome of every
lysosome-adjacent target.

### Prediction

I predict `Mitf` will have no FDR<0.05 downstream genes in the held-out focal
readout:

| target | predicted `n_degs` | rationale |
|---|---:|---|
| `Mitf` | 0 | The best in-dataset pigment-axis perturbations, `Mc1r` and `Lrmda`, had exactly 0 focal DEGs and were globally null across recovered NeuN-positive groups in the Distributed Agents corpus. Upstream melanocyte-lineage regulators `Sox10` and `Pax3`, MC1R/cAMP nodes, and core autophagy or lysosome nodes were also zero or singleton-scale in the focal group. Large endolysosomal responses existed for `Rab7` and `Tsc2`, but they were mechanistically distinct stress states with near-zero full-profile similarity to the pigment nulls. Because the experiment is acute postnatal neuronal CRISPR rather than a melanocyte assay, the canonical MITF pigment program should be lineage-silent here. |

## Limits of the reasoning

- There was no direct `Mitf` perturbation row and no assayed `Tfeb`, `Tfe3`, or
  `Tfec` loss-of-function row in the focal training-count table, so the
  MiT/TFE inference is indirect.
- A zero prediction is a statement about adjusted single-nucleus RNA DEGs in
  this assay only.  It does not rule out MITF protein function, rare subnuclear
  expression, developmental effects before P16, non-neuronal roles, or
  post-transcriptional lysosomal phenotypes.
- The focal group has unusually high responses for some perturbations, and
  `Rab7`/`Tsc2` show that late endosome and mTOR stress can be detected in
  these cells.  I rejected those as primary analogs because their observed
  signatures and corpus annotations are target-specific stress states rather
  than pigment/MITF-lineage programs, but that is still an extrapolation from
  neighboring biology rather than a direct MITF-family perturbation.
- The counts are assay- and power-dependent.  Matched perturbed-cell counts for
  the focal comparators ranged from roughly 93 to 261 in the queried set; a
  very small `Mitf` response could fall below FDR even if target editing
  occurred.
