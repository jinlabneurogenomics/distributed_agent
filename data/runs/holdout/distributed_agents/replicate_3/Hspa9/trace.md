# Hspa9 DEG-count prediction for 151 TH Prkcd Grin2c Glut

## Question and resolved ambiguities

The task is to predict the held-out endpoint `n_degs` for each target in
`109_Hspa9.csv`. This run contains one requested target:

- `Hspa9`

I interpreted `n_degs` exactly as the training CSV defines it: the number of
measured genes in `151 TH Prkcd Grin2c Glut` with Wilcoxon
Benjamini-Hochberg-adjusted `pvals_adj < 0.05`. I did not exclude the
self-transcript row from the count, because the training endpoint includes any
measured gene passing the same FDR cutoff. When comparing mechanisms, however,
I separated self-only hits from downstream transcriptional responses.

The perturbation is sparse postnatal AAV CRISPR loss of function in recovered
NeuN-positive mouse nuclei. I treated flat target RNA as uninformative for
editing success and used it only as row-level DE evidence, consistent with the
dataset notes that target mRNA drop is not a quantitative engagement assay.

## Sources used

- Input held-out manifest:
  `[local file: 109_Hspa9.csv]`
- Exact training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Per-gene DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Same-experiment semantic corpus:
  Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`.
- Same-experiment profile tool:
  Distributed Agents runtime `profile_compare/profile_inspect` over the focal-cell
  parquet rows for selected training analogs.
- External biological knowledge:
  PubMed-indexed literature and MitoCarta3.0 for mitochondrial localization and
  pathway membership.

## Dataset computations

1. I loaded the 1,674 training DEG counts for `151 TH Prkcd Grin2c Glut` and
   confirmed that `Hspa9` is absent. The endpoint is highly zero-inflated:
   1,205 of 1,674 targets are zero; only 43 have at least 100 DEGs.
2. I scanned the focal-cell rows of the DE parquet with
   `group_name == "151 TH Prkcd Grin2c Glut"` and a target filter containing
   mitochondrial import, mitochondrial proteostasis, Fe-S, respiratory-chain,
   and Hsp70-family comparators. For each training perturbation I counted
   rows with `pvals_adj < 0.05` and sorted the leading rows by adjusted P value.
3. I computed a focal profile comparison for 13 mechanistic analogs
   (`Hspa8`, `Hspa5`, `Opa1`, `Lonp1`, `Dnajc19`, `Timmdc1`, `Clpp`, `Clpx`,
   `Yme1l1`, `Afg3l2`, `Nfs1`, `Abcb7`, `Tomm40`) using Wilcoxon scores as the
   signed profile value. Nine of the 13 had no significant focal features;
   `Opa1` had 37, `Hspa8` had 9, and `Hspa5` had 5. The null PAM/import and
   Fe-S targets had near-zero focal score correlations with the weak chaperone
   positives and no shared FDR-level features.
4. I used the Distributed Agents corpus to check the same perturbations across all
   neuronal classes so that a focal-cell zero was not mistaken for a global
   absence or vice versa.

## Target-specific reasoning

### `Hspa9`

**Biology.** `Hspa9` encodes mitochondrial Hsp70, also called mortalin or
Grp75. It is a MitoCarta3.0 mitochondrial matrix protein and the central Hsp70
ATPase of the TIM23/PAM import motor. Mammalian DNAJC19 and DNAJC15 stimulate
the mtHsp70 ATPase at the import channel, while GRPEL1/GRPEL2 are GrpE-like
nucleotide-exchange factors that regulate the mtHsp70 chaperone cycle
(Sinha et al. 2016, doi:10.1074/jbc.M116.738146, PMID 27330077; Srivastava et
al. 2017, doi:10.1074/jbc.M117.788463, PMID 28848044). HSPA9 also works with
the HSC20/ISCU Fe-S chaperone system; Hspa9 depletion in erythroid cells
impairs mitochondrial Fe-S assembly, alters IRP/IRE control, and blocks heme
synthesis and differentiation (Shan and Cortopassi 2015,
doi:10.1016/j.mito.2015.12.005, PMID 26702583; Maio and Rouault 2014,
doi:10.1016/j.bbamcr.2014.09.009, PMID 25245479; Maio and Rouault 2016,
doi:10.1039/c6mt00167j, PMID 27714045). Severe mitochondrial damage can be
relayed to ATF4 through the OMA1-DELE1-HRI pathway (Guo et al. 2020,
doi:10.1038/s41586-020-2078-2, PMID 32132707), so a nonzero ISR-like response
is biologically plausible if Hspa9 editing crosses a mitochondrial stress
threshold.

**Closest within-dataset comparators.**

| comparator | focal `n_degs` | focal expression-pattern evidence | relevance to `Hspa9` |
| --- | ---: | --- | --- |
| `Dnajc19` | 0 | No focal FDR genes; all leading rows had `pvals_adj = 1.0`. | A PAM J-protein that stimulates mitochondrial Hsp70 at the TIM23 import motor; direct import-motor analog, but partly buffered by DNAJC15 in mammals and not the core ATPase. |
| `Timmdc1` | 0 | No focal FDR genes; best row `Pcdhgb4`, FDR 0.434. | Complex-I assembly factor used as a mitochondrial inner-membrane/import-adjacent counterexample. |
| `Tomm40` | 1 | Only the self row passed: `Tomm40` logFC -0.923, FDR 5.46e-7; no downstream genes. | General mitochondrial preprotein import pore; argues that import membership alone gave no 151 stress program. |
| `Nfs1` | 0 | `Nfs1` self row was subthreshold, FDR 0.233; no downstream genes. | Core Fe-S biogenesis enzyme. HSPA9 connects to this branch through HSC20/ISCU. |
| `Abcb7` | 0 | No focal FDR genes; best row `Rpn1`, FDR 0.364. | Mitochondrial Fe-S export/iron-homeostasis comparator. |
| `Isca2` | 1 | Only the self row passed: `Isca2` logFC -0.700, FDR 0.027. | Late Fe-S maturation comparator; supports Fe-S branch sparsity. |
| `Clpp`, `Clpx` | 0, 0 | Neither had a focal FDR gene. | Matrix protease system; same mitochondrial matrix quality-control compartment but not the import motor. |
| `Lonp1` | 0 in 151 | Focal `Lonp1` had no FDR gene, although the corpus reports small Ddit3/Herpud1/Aldh1l2/Shmt2 stress responses in other neuronal classes. | Matrix protease positive in the broader atlas; shows mitochondrial matrix stress can be detected but is cell-class restricted. |
| `Yme1l1`, `Afg3l2` | 0, 0 | No focal FDR genes. | Inner-membrane AAA proteases and OPA1-processing counterexamples. |
| `Opa1` | 37 | Strong focal ATF4/ISR-like response: `Asns`, `Mars1`, `Chac1`, `Ddit3`, `Cars`, `Mthfd2`, `Slc7a5` up, with 26 up and 11 down FDR genes. | Positive mitochondrial-stress benchmark, but direct OPA1 loss is branch-specific and should not be averaged with buffered import/Fe-S nodes. |
| `Hspa8` | 9 | Cytosolic Hsp70 loss induced `Dnaja1`, `Hspa4l`, `Syt4`, `Hsp90aa1`, `Cct6a` up and `Fras1`, `Unc79`, `Leng8`, `Apba2` down. | Closest Hsp70-family training target; supports a weak chaperone counterinduction model. |
| `Hspa5` | 5 | ER BiP loss induced `Hsp90b1`, `Nfe2l1`, `Pdia4`, `Derl3` and down-regulated `Erc1`; several UPR-adjacent genes sat just above FDR 0.05. | Another Hsp70-family organelle chaperone; supports weak nonzero, not broad, chaperone stress. |
| `Hsp90ab1` | 1 | Self row only; no downstream FDR genes. | Abundant cytosolic chaperone counterexample. |

The Distributed Agents corpus provided the same qualitative guardrails across the wider
screen:

- It curated `Dnajc19` as mostly nonconvergent with DNAJ-family and proximal
  mitochondrial comparators; direct TIM23/PAM partners other than `Dnajc19`
  were largely absent from the target universe.
- It curated `Timmdc1`, NDUF perturbations, `Abcb7`, and `Nfs1` as broadly
  buffered or Fe-S/OXPHOS-nonconvergent in juvenile postmitotic neuronal
  snRNA-seq.
- It curated `Opa1` as a real ATF4/ISR-like mitochondrial stress positive and
  repeatedly used it as the counterexample proving that many other
  mitochondrially annotated targets do not automatically cross that threshold.
- It curated `Hspa8` and `Hspa5` as small, cell-restricted chaperone responses
  rather than members of a generic Hsp70/Hsp90/UPR signature.

**Zero/nonzero decision.** The import-motor and Fe-S evidence argues strongly
against a large count. `Dnajc19`, `Timmdc1`, `Nfs1`, `Abcb7`, `Clpp`, `Clpx`,
`Yme1l1`, `Afg3l2`, and `Lonp1` were all zero in the focal group, and the
same-experiment corpus repeatedly found no shared mitochondrial import, Fe-S,
respiratory-chain, or matrix-protease RNA module. Still, `Hspa9` is a more
central node than `Dnajc19`: it is the core ATPase used by both the protein
import/folding branch and the HSC20/ISCU Fe-S chaperone branch, with no obvious
matrix Hsp70 paralog replacing it. The two organellar Hsp70-family analogs
that are represented as training perturbations, `Hspa8` and `Hspa5`, both
crossed the focal FDR threshold weakly. I therefore predict a weak nonzero
signature rather than a strict zero.

**Approximate count.** I kept the point estimate below `Hspa5` and `Hspa8`
because most directly mitochondrial comparators were 0 or self-only and
because the `Opa1` response was a special inner-membrane/ISR state not shared
by the import and Fe-S branches. A count of 3 allows for the `Hspa9`
self-transcript and a couple of stress/chaperone genes to pass FDR without
promoting the perturbation into the 5 to 9 DEG class seen for `Hspa5` and
`Hspa8`.

Predicted `Hspa9` `n_degs`: **3**.

## Limits of the reasoning

- `Hspa9` itself was completely held out, so all expression-signature evidence
  is transferred from imperfect analogs. No represented training target is the
  same PAM ATPase or the same combined import plus Fe-S chaperone.
- `Dnajc19` is mechanistically close to the mitochondrial import motor but is a
  co-chaperone with a DNAJC15 paralog; its focal null may understate the effect
  of losing HSPA9 itself.
- `Opa1` and `Lonp1` show that mitochondrial stress can be transcribed in the
  atlas, but they perturb mitochondrial dynamics or matrix proteolysis rather
  than the HSPA9 ATPase cycle.
- Fe-S collapse, import blockade, mitochondrial membrane potential, HSPA9
  protein, DNA indels, and neuronal survival were not assayed directly. A
  severe primary defect could be invisible here if strongly edited cells were
  depleted before recovery or if protein turnover was too slow for a robust
  3 to 4 week nuclear RNA signature.
- The point estimate distinguishes the most likely response bin, not exact
  biology. Counts near zero are particularly sensitive to the single-cell
  sample size, BH correction, and whether the target self-transcript happens to
  pass FDR.
