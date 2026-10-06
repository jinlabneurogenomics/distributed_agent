# DEG-count prediction trace

## Question and endpoint

The requested prediction is the integer `n_degs` for each held-out perturbation in
`151 TH Prkcd Grin2c Glut` cells: the number of measured genes with
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` after sparse
AAV-PHP.eB CRISPR loss of function. The only requested held-out target in
`the single-target request` is `Gpr68`.

I treated the held-out `Gpr68` signature and count as absent from the declared
inputs, so the prediction had to be transferred from the 1,674 visible training
counts and selected focal-cell differential-expression rows for mechanistic
analogs. Counts include the target transcript itself when its adjusted
p-value passes 0.05; the endpoint is therefore "all significant measured
genes", not only downstream non-self genes. I did not use measured
self-transcript loss as an editing-efficiency filter, because the experiment
uses sparse indel-producing CRISPR and the dataset portrait notes that visible
nuclear target-RNA loss is not a quantitative knockout-strength readout.

## Sources used

- Declared focal training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared raw differential-expression parquet:
  `training differential-expression dataset`.
  I queried only focal-cell rows for targets selected from known GPR68
  receptor and second-messenger biology.
- Requested target manifest:
  `single-target request for Gpr68`.
- Internal same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, queried through
  `corpus.calibration` and `corpus.findings`. I used its curated Findings only
  for visible training perturbations such as `Gnas`, `Plcb1`, `Grm5`,
  `Gnao1`, and `Gpr158`.
- External literature:
  NCBI PubMed E-utilities was used for GPR68/proton-sensing GPCR mechanism and
  brain context. Key references were Sisignano, Fischer and Geisslinger 2021,
  DOI 10.3390/cells10082050; Wang et al. 2020, DOI
  10.1161/STROKEAHA.120.031479, PMID 33059544; Xu, Lin and Zha 2020, DOI
  10.1186/s13041-020-00672-8, PMID 32993733; Mohebbi et al. 2012, DOI
  10.1159/000338486, PMID 22508039; Frick et al. 2009, DOI
  10.1359/jbmr.081015, PMID 18847331; Schneider et al. 2012, DOI
  10.1021/cn300025a, PMID 22860225; and Yu et al. 2019, DOI
  10.1021/acs.jmedchem.9b00869, PMID 31298539.

## Quantitative calibration

I first read the requested manifest and the focal training-count CSV, verified
that `Gpr68` was not present in the training endpoint table, and summarized the
visible endpoint distribution. The focal endpoint is strongly zero inflated:
1,205 of 1,674 visible biological perturbations had `n_degs = 0`, the median
was 0, the 75th percentile was 1, the 90th percentile was 2, and only the 95th
percentile reached 18. Thus a membrane-receptor target starts with a strong
empirical prior of no FDR-significant basal nuclear RNA response unless a close
analog argues otherwise.

I then looked for direct relatives:

| analog class | represented focal training targets | observed `n_degs` in `151 TH Prkcd Grin2c Glut` | interpretation |
| --- | --- | ---: | --- |
| Proton-sensing GPCR paralogs | `Gpr4`, `Gpr65`, `Gpr132` absent | not available | The closest family-level transfer was not testable in the visible endpoint table. |
| Generic `Gpr*` receptor perturbations | `Gpr156`, `Gpr161`, `Gpr179`, `Gpr45`, `Gprc5b`, `Gpr158`, `Gprasp2` | 0 or 1 | `Gpr158=1` was a significant self-transcript call in the focal raw parquet (`logFC -0.991`, `FDR 3.39e-26`) without a broader downstream signature. |
| Gq/PLC receptor and effector branch | `Grm1=1`, `Grm5=0`, `Htr2a=0`, `Htr2b=0`, `Htr2c=0`, `Chrm3=0`, `Itpr1=0`, `Prkca=0`, `Plcb1=0` | 0 or 1 | GPR68 can signal through Gq/11 to PLC/IP3/calcium, but visible Gq-coupled receptors and PLC/calcium effectors were nearly all basal-null. The single `Grm1` count in the focal parquet was the `Grm1` self row (`logFC -0.438`, `FDR 4.28e-5`), not a downstream program. |
| Gs/cAMP branch | `Gnas=0`, `Gnal=0`, `Adcy1=0`, `Adcy3=0`, `Adcy5=0` | 0 | GPR68 allosteric agonists can potentiate proton signaling through a Gs route, but direct Gs and adenylyl-cyclase perturbations did not move the focal endpoint. |
| Other GPCR transducers and buffered receptor controls | `Gnao1=1`, `Grm7=1`, broad Htr/Drd/Opr/Npy receptor panels mostly 0 | 0 or 1 | The nonzero calls were isolated, often self-transcript, and did not indicate a hidden focal GPCR transcriptome. |

For the raw parquet checks I filtered to `group_name == "151 TH Prkcd Grin2c
Glut"` and pulled `names`, `gene_target`, `logfoldchanges`, `pvals_adj`,
`scores`, and matched perturbed-nucleus counts for the analog targets. This
confirmed that `Gnas` in 306 perturbed nuclei and `Plcb1` in 160 perturbed
nuclei had no focal FDR<0.05 genes; their largest Wilcoxon-score rows all had
`pvals_adj = 1`. The focal `Grm5`, `Gpr156`, `Gpr161`, `Gprc5b`, `Adcy1`,
`Adcy3`, and `Adcy5` surfaces were likewise all zero at FDR 0.05. The internal
July Findings for `Gnas`, `Plcb1`, `Grm5`, `Gnao1`, and `Gpr158` agreed with
this direct focal read: across the experiment, these GPCR or second-messenger
perturbations were interpreted as buffered or nearly null basal snRNA-seq
signatures rather than broad constitutive stress, CREB, PLC/calcium, or
activity-dependent transcriptional programs.

The main counterexamples in the same cell group were downstream nuclear or
growth-control targets rather than receptor-proximal targets: for example
`Creb1=10`, `Crebbp=8`, and the very large counts among spliceosome,
proteasome, or transcriptional-regulatory genes show that `151 TH Prkcd
Grin2c Glut` is capable of generating significant DEGs. They do not transfer
strongly to `Gpr68`, because GPR68 sits upstream at an extracellular
proton-gated receptor and was not stimulated by an acidification challenge in
this assay.

## Target-specific prediction

### Gpr68

**Biology transferred to the assay.** `Gpr68`, also called `Ogr1`, encodes one
of four proton-sensing GPCRs with `Gpr4`, `Gpr65/Tdag8`, and `Gpr132/G2a`
(Sisignano, Fischer and Geisslinger 2021). Acidic extracellular pH activates
OGR1/GPR68 through histidine-dependent proton sensing and can drive
Gq/11/phospholipase-C/IP3/calcium and PKC signaling in cell systems and
peripheral tissues (Frick et al. 2009; Mohebbi et al. 2012). GPR68 also has
brain-relevant literature: it is broadly present in neurons and can protect
against acidotic/ischemic neuronal injury through PKC signaling (Wang et al.
2020), contributes to hippocampal LTP and passive avoidance behavior in
knockout mice (Xu, Lin and Zha 2020), and was implicated in hippocampal neural
stem-cell responses to proneurogenic small molecules (Schneider et al. 2012).

**Within-dataset analogs.** The direct proton-sensing paralogs were absent from
the visible training endpoint, so I anchored on the proximal pathways that
would be expected if basal `Gpr68` loss had driven a stable nuclear response:

- `Plcb1` is the canonical PLC beta effector downstream of Gq/11 receptors and
  had `n_degs = 0` in the focal class; the July same-experiment corpus
  described it as a 22-group downstream null and noted that `Chrm3`, `Grm1`,
  `Grm5`, `Htr2a/b/c`, `Itpr1`, and `Prkca` likewise failed to produce a
  hidden Gq/PLC RNA module.
- `Grm5` is a neuronal Gq/PLC-coupled GPCR with expected Arc/Fos/Egr and
  synaptic-plasticity biology after stimulation, yet had `n_degs = 0` in the
  focal class and no downstream DEGs in the measured groups summarized by the
  July Findings.
- `Grm1` had one focal DEG, but the raw row was the `Grm1` self-transcript
  decrease; there was no downstream mGluR1-like transcriptional state to
  transfer.
- `Gnas`, `Gnal`, and `Adcy1/3/5` were all 0 in the focal class, arguing
  against a standing Gs/cAMP/CREB footprint from deleting a single upstream
  GPCR-pathway component.
- The nearest same-assay orphan receptor example, `Gpr158`, also had only a
  self-transcript event in this cell group and the internal corpus rejected a
  broad hidden GPCR/RGS/cAMP module.

**Zero/nonzero decision.** I predict `Gpr68` will have no genes below FDR 0.05
in `151 TH Prkcd Grin2c Glut`. The strongest reason is not that GPR68 is
biologically unimportant; it is that GPR68 is a ligand- and pH-gated membrane
sensor whose best-supported brain effects involve acute acidosis,
hippocampal synaptic physiology, PKC/cAMP signaling, or glial/progenitor
contexts. The held-out readout is an unstimulated, basal nuclear transcriptome
from surviving postmitotic neuronal nuclei 3-4 weeks after sparse P16 editing.
Training perturbations of Gq/PLC receptors, PLC/calcium effectors, and
Gs/adenylyl-cyclase components were repeatedly 0 in the exact focal endpoint.

A count of 1 is plausible if the `Gpr68` RNA itself happened to be sufficiently
expressed and knocked down in this thalamic group, as seen for `Grm1`,
`Grm7`, `Gnao1`, and `Gpr158`. I did not choose 1 because most visible GPCRs in
the training table were 0, `Gpr68` thalamic expression was not established from
the supplied data, and no same-experiment analog supported a non-self
downstream focal response. The final point prediction is therefore:

`Gpr68 -> 0`

## Limits and extrapolations

- The closest proton-sensing GPCR paralogs were not visible training
  perturbations, so the prediction rests on pathway transfer from other GPCR
  and second-messenger nodes rather than on a direct `Gpr4/Gpr65/Gpr132`
  within-dataset anchor.
- The declared parquet contains no raw per-nucleus UMI counts and no held-out
  `Gpr68` perturbation rows, so I could not verify basal `Gpr68` expression or
  the probability of a significant `Gpr68` self-transcript call in the exact
  target group.
- External GPR68 studies often used acidification, ischemia, peripheral
  tissues, hippocampus, neural progenitors, or whole-animal phenotypes. Those
  establish that GPR68 can matter, but they are imperfect proxies for sparse
  postnatal CRISPR loss in recovered thalamic glutamatergic nuclei at rest.
- The prediction would be weakest if extracellular pH signaling is tonically
  active in `151 TH Prkcd Grin2c Glut` neurons or if the `Gpr68` transcript is
  unusually detectable and guide-sensitive in this class. The training analogs
  argue that such a response, if present, is more likely to be zero or a
  one-gene self event than a broad DEG burden.
