# Question

The requested held-out perturbation is `Ano3`. I interpreted the task as a point
prediction of the number of genes that would pass Benjamini-Hochberg FDR 0.05 in
the `151 TH Prkcd Grin2c Glut` differential-expression contrast after an acute
P16 AAV-CRISPR loss-of-function perturbation of the mouse gene. `n_degs` counts
all measured genes, including the target transcript itself if it is significant.

The ambiguity I resolved was that ANO3 is a membrane excitability and Ca2+
signaling gene, so the closest functional effects are electrical or
membrane-proximal. I therefore treated zero DEG counts in related ion-channel
perturbations as direct evidence for this RNA-breadth endpoint, but not as
evidence that the cells had no electrophysiological phenotype.

# Sources

- Declared focal training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression parquet:
  `training differential-expression dataset`.
- Requested targets:
  `single-target request for Ano3`.
- Same-experiment interpretation layer: `perturbai-july-260713-sourceguard-1773-v1`,
  specifically bounded Findings for `Kcnt1`, `Kcnt2`, `Cacna1g`, and `Scn1a`.
  This corpus is a packaged interpretation of the same Perturb-seq experiment,
  not independent replication of the parquet.
- External literature via NCBI PubMed:
  - Huang et al. 2013, Nat. Neurosci., PMID: 23872594,
    DOI: 10.1038/nn.3468.
  - Suzuki et al. 2013, J. Biol. Chem., PMID: 23532839,
    DOI: 10.1074/jbc.M113.457937.
  - Stamelou et al. 2014, Mov. Disord., PMID: 24442708,
    DOI: 10.1002/mds.25802.
  - Pedemonte and Galietta 2014, Physiol. Rev., PMID: 24692353,
    DOI: 10.1152/physrev.00039.2011.
  - Wang et al. 2021, Proc. Natl. Acad. Sci. USA, PMID: 33972431,
    DOI: 10.1073/pnas.2023342118.
  - Ousingsawat et al. 2024, Brain, PMID: 38079528,
    DOI: 10.1093/brain/awad412.
  - Ousingsawat et al. 2025, BMC Med., PMID: 39773217,
    DOI: 10.1186/s12916-024-03839-5.

# Computation Over The Training Data

I used the training count CSV to calibrate response breadth in `151 TH Prkcd
Grin2c Glut`, then filtered the parquet to that same `group_name` and to
mechanistically selected visible targets. No `Ano*` gene was present among the
1,674 training perturbations, so there was no direct same-family perturbation.
The scalar endpoint itself is directly observed for all selected analogs in the
count CSV.

The focal endpoint is sparse. Among 1,674 training targets, 1,205 were exactly
zero, the median was 0, the 75th percentile was 1, the 95th percentile was 18,
and only a long tail of mostly RNA-processing, proteostasis, or regulatory
perturbations reached hundreds to thousands of DEGs.

I then checked several channel neighborhoods in the count table:

| training group | visible genes | median `n_degs` | mean `n_degs` | nonzero genes |
|---|---:|---:|---:|---:|
| KNa/KCa channels: `Kcnt1`, `Kcnt2`, `Kcnn2`, `Kcnn3`, `Kcnma1` | 5 | 0 | 0.20 | 1 |
| chloride/Cl-transport genes: `Clcn3`, `Clcn4`, `Slc12a2` | 3 | 0 | 0.33 | 1 |
| voltage-gated Na/Ca channels | 11 | 1 | 1.64 | 6 |
| broader channels and receptors inspected | 41 | 0 | 2.95 | 16 |

For the focal parquet slices, the key analog counts were:

| target | `n_pert_matched` | focal `n_degs` | focal expression-pattern evidence |
|---|---:|---:|---|
| `Kcnt1` | 176 | 0 | `Kcnt1` itself was not significant; all adjusted p values in the slice were 1.0. |
| `Kcnt2` | 109 | 0 | `Kcnt2` itself was not significant; all adjusted p values in the slice were 1.0. |
| `Kcnn2` | 229 | 0 | no FDR genes; `Kcnn2` nominally fell but adjusted p was 1.0. |
| `Kcnn3` | 177 | 0 | no FDR genes; the target was the best nominal hit but adjusted p was 0.409. |
| `Kcnma1` | 183 | 1 | only `Kcnma1` itself passed FDR 0.05. |
| `Clcn3` | 91 | 0 | no FDR genes despite a nominal target-transcript decrease. |
| `Clcn4` | 169 | 1 | only `Clcn4` itself passed FDR 0.05. |
| `Scn1a` | 195 | 1 | only the target transcript passed in `151`. |
| `Scn1b` | 261 | 2 | the target and `Jun` passed. |
| `Scn2a` | 186 | 1 | only the target transcript passed. |
| `Scn8a` | 90 | 1 | only the target transcript passed. |
| `Cacna1a` | 117 | 0 | no FDR genes. |
| `Cacna2d1` | 143 | 1 | only the target transcript passed. |
| `Cacna1g` | 264 | 12 | a real thalamic response led by `Ptprn`, target loss, `Stmn4`, `Cpne7`, `Ly6e`, `Jun`, and `Zdhhc22`. |
| `Itpr1` | 203 | 0 | no FDR genes; the target adjusted p was 0.086. |
| `Ryr2` | 100 | 0 | no FDR genes. |
| `Slc12a2` | 197 | 0 | no FDR genes. |

# Target-Specific Prediction

## `Ano3`

**Biology used.** `Ano3` encodes anoctamin-3/TMEM16C, a TMEM16-family membrane
protein. The family contains Ca2+-activated Cl- channels as well as members
with phospholipid-scramblase and channel-regulatory functions (Suzuki et al.
2013; Pedemonte and Galietta 2014). In neurons, TMEM16C is not a transcription
factor or a core RNA/proteostasis gene. Huang et al. 2013 showed that TMEM16C
facilitates Slack/KCNT1 Na+-activated K+ currents in rat sensory neurons:
Tmem16c knockout reduced Slack expression, broadened action potentials, and
increased excitability. Wang et al. 2021 showed that loss of Tmem16c in rodent
central neurons increases susceptibility to hyperthermia-induced seizures and
impairs thermoregulation. Human ANO3 variants cause DYT24 craniocervical
dystonia with tremor (Stamelou et al. 2014), and newer variant studies support
a Ca2+ signaling mechanism that can impair activation of KCa channels through
store-operated Ca2+ entry and ORAI1 trafficking (Ousingsawat et al. 2024, 2025).

**Most relevant within-dataset analogs.** The closest measured perturbations are
not another anoctamin, because no visible training target starts with `Ano`.
The next strongest analogs are the KNa channels `Kcnt1` and `Kcnt2`, because
published ANO3/TMEM16C biology propagates through Slack/KCNT1 and more broadly
through K+ channel activation. Both were complete focal transcriptomic nulls:
`Kcnt1` had 0 DEGs from 176 matched perturbed nuclei and `Kcnt2` had 0 DEGs from
109. Same-experiment Findings report that `Kcnt1` loss was FDR-null in every
measured cell group and that `Kcnt2` had zero downstream genes at FDR < 0.10 in
all 22 recovered groups; the Kcnt2 report further notes that activity and
channel-compensation genes such as `Fos`, `Jun`, `Egr1`, `Npas4`, `Arc`,
`Bdnf`, `Hcn1`, `Hcn2`, `Scn1a`, `Scn2a`, `Scn8a`, `Kcnq2`, `Kcnq3`, `Kcnn2`,
and `Kcnn3` did not form an FDR-significant chronic activity program. Those
observations make it plausible that a KNa/K+ channel regulator can change
excitability without a broad steady-state snRNA-seq response 3 to 4 weeks after
P16 CRISPR.

`Kcnn2` and `Kcnn3`, the represented small-conductance Ca2+-activated K+
channels, were also 0-DEG targets, and `Kcnma1`, the large-conductance
Ca2+-activated K+ channel, yielded only a self-transcript hit. Because
Ousingsawat et al. link disease ANO3 variants to impaired KCa channel
activation, these KCa neighbors are useful counterweights against predicting a
large Ca2+-dependent activity signature.

**Counterexamples considered.** `Cacna1g` is the main channel counterexample in
`151`: Cav3.1 loss had 12 DEGs, including non-target genes such as `Ptprn`,
`Stmn4`, `Cpne7`, `Ly6e`, `Jun`, `Zdhhc22`, `Lrrc7`, and `Serpine2`. The
same-experiment Cacna1g report describes this as a narrow thalamic Cav3.1
response rather than a generic calcium-channel program; all represented
voltage-gated calcium-channel relatives in that comparison were 0 downstream
DEGs in the same focal group. I therefore used it to keep the `Ano3` prediction
from being confidently null, but not to transfer a 12-gene signature to ANO3,
which sits upstream of K+ channel regulation and phospholipid scrambling rather
than being the Cav3.1 alpha subunit that defines thalamic T-type currents.

`Scn1a`, `Scn2a`, and `Scn8a` were also effectively self-only in `151`, and the
same-experiment `Scn1a` report emphasized that a canonical axonal channelopathy
can be sharply buffered at the nuclear RNA endpoint. NMDA-receptor perturbation
is a looser counterexample: `Grin1` produced 89 focal DEGs, but `Grin2a` and
`Grin2b` produced only one and two. I did not treat `Grin1` as the main analog
because it removes an obligate excitatory synaptic receptor subunit rather than
a TMEM16C regulatory protein.

**Causal transfer.** The expected chain for `Ano3` is: CRISPR loss of `Ano3` in
P16 postmitotic thalamic glutamatergic neurons; reduced ANO3/TMEM16C membrane
activity, scrambling, or channel regulation; altered KNa/KCa or store-operated
Ca2+ signaling in only the cells that need this regulator; possible changes in
firing or local membrane physiology; survival and recovery of sparse edited
nuclei; finally Wilcoxon DE on nuclear RNA after P37-44 harvest. The strongest
links in that chain terminate before nuclear transcription. The training
endpoint says that deletion of downstream KNa/KCa channel components rarely
creates a detectable focal nuclear program. It also shows that channel effects
which are assay-visible in `151` are small, with the best mechanistically
related visible counterexample at 12 DEGs and most exact targets at 0 or 1.

I assign `Ano3` a zero/nonzero call of **zero**. The exact point prediction is
0 DEGs rather than 1 because `Ano3` was not represented as an expressed,
self-hit-like target in the training set, no anoctamin analog was available, and
the closest KNa partners were not even significant for their own target
transcripts in `151`. The prediction is driven primarily by the within-dataset
zero counts for `Kcnt1`, `Kcnt2`, `Kcnn2`, and `Kcnn3`; external ANO3 biology
only selects those genes as mechanistically appropriate analogs.

# Limits

This is extrapolation from functionally adjacent ion-channel perturbations, not
a direct paralog or same-complex transfer. The visible training universe lacked
`Ano1`, `Ano2`, other `Ano*` genes, `Orai1`, and `Kcnn4`, so important ANO3
neighbors were missing. ANO3 is associated with striatal and hypothalamic
physiology, while the requested readout is a thalamic glutamatergic class; that
does not break the causal chain, but it weakens expression and context
confidence. The Perturb-seq assay measured survivor-conditioned nuclear RNA,
not membrane currents, Ca2+ entry, phospholipid scrambling, dystonia, seizures,
or cell survival before nuclei were recovered. A nonzero single self-transcript
hit would be plausible if `Ano3` is well expressed and its disrupted alleles are
visible through transcript loss in these thalamic cells; the evidence above
argues only that a broad downstream response is unlikely.
