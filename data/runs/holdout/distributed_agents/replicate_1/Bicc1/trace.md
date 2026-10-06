# DEG-count prediction trace

## Question and endpoint

I interpreted the task as a scalar prediction for the held-out `Bicc1`
perturbation in `151 TH Prkcd Grin2c Glut` neurons. The predicted value is the
integer number of measured genes expected to pass BH-adjusted Wilcoxon
`pvals_adj < 0.05` in the focal cell group after sparse P16 AAV-CRISPR loss of
function. `Bicc1` was held out, so I did not have its expression signature or
true DEG count; the endpoint is absent for the requested target and directly
observed only for the 1,674 non-held-out training perturbations.

The ambiguity I resolved was how to treat BICC1's RNA-binding annotation. BICC1
is an RNA-binding protein, but its best-established mammalian biology is a
selective BICC1/ANKS/ciliary-polycystin RNA-regulatory axis, not core spliceosome
or ubiquitous hnRNP function. I therefore weighted Bicc1-neighboring ciliary,
polycystin, Dicer/miRISC, and CCR4-NOT perturbations more heavily than generic
RNA-binding proteins that gave large training signatures.

## Sources used

- Declared focal DEG-count training table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression parquet:
  `training differential-expression dataset`.
- Requested target manifest:
  `single-target request for Bicc1`.
- Run-local bindings, coverage, and capability manifests under
  `codex_runtime/pipeline`.
- Same-experiment semantic corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, queried with
  `corpus.findings` / `corpus.calibration`. This was used as packaged
  interpretation of the same PerturbAI experiment for visible training
  perturbations only, not as independent replication.
- External literature via NCBI PubMed E-utilities. The key BICC1 mechanism papers
  were Mahone et al. 1995, DOI 10.1002/j.1460-2075.1995.tb07196.x,
  PMID 7538070; Piazzon et al. 2012, DOI 10.1093/jmcb/mjs027, PMID 22641646;
  Rothe et al. 2017, DOI 10.1016/j.str.2017.12.002, PMID 29290488; Maerker et
  al. 2021, DOI 10.1038/s41467-021-25464-z, PMID 34531379; Minegishi et al.
  2021, DOI 10.1038/s41467-021-24295-2, PMID 34210974; Rothe et al. 2023, DOI
  10.1371/journal.pbio.3002302, PMID 37733651; and Tran et al. 2026, DOI
  10.7554/eLife.106342, PMID 41677782.

## Quantitative calibration

I read the training count CSV and summarized its empirical distribution in the
focal cell group:

- 1,674 visible biological targets.
- Median `n_degs = 0`.
- 1,205/1,674 targets, or 72.0%, had no FDR 0.05 DEGs.
- The 75th percentile was 1 DEG and the 90th percentile was 2 DEGs.
- The high tail was sparse: examples included `Uba5 = 2677`, `Tpr = 1768`,
  `Sin3a = 1433`, `Rnpc3 = 868`, `Zbtb7a = 841`, `U2af2 = 828`,
  `Psmb4 = 742`, and `Hnrnpu = 733`.

For visible analogs, I filtered the parquet to rows with
`group_name == "151 TH Prkcd Grin2c Glut"` and counted per target how many
measured genes had `pvals_adj < 0.05`. I also recorded the minimum adjusted
p-value as a guard against calling a noisy singleton "nearly significant" when
the whole focal-cell signature was flat.

## Bicc1 comparator evidence and prediction

### Most direct ciliary/polycystin-side comparators

The strongest within-dataset analogs are perturbations of the ciliary and
polycystin neighborhood that externally connects to BICC1 through ANKS3/ANKS6,
PC1/PC2, Dand5, and miRNA/CCR4-NOT-mediated silencing. All were essentially
silent in the exact focal cell group:

| training target | observed focal `n_degs` | focal-cell expression evidence |
|---|---:|---|
| `Pkd1` | 0 | 0 BH genes; minimum adjusted p = 1.0 |
| `Cep290` | 0 | 0 BH genes; minimum adjusted p = 0.650 |
| `Rpgrip1l` | 0 | 0 BH genes; minimum adjusted p = 0.184 |
| `Bbs5` | 0 | 0 BH genes; minimum adjusted p = 0.220 |
| `Ift43` | 0 | 0 BH genes; minimum adjusted p = 0.847 |
| `Ift81` | 0 | 0 BH genes; minimum adjusted p = 0.391 |
| `Ift88` | 0 | 0 BH genes; minimum adjusted p = 1.0 |
| `Kif3b` | 0 | 0 BH genes; minimum adjusted p = 1.0 |
| `Dync2h1` | 0 | 0 BH genes; minimum adjusted p = 0.348 |
| `Ttc21b` | 0 | 0 BH genes; minimum adjusted p = 0.459 |
| `B9d1` | 0 | 0 BH genes; minimum adjusted p = 1.0 |
| `Cspp1` | 0 | 0 BH genes; minimum adjusted p = 1.0 |
| `Lztfl1` | 0 | 0 BH genes; minimum adjusted p = 0.195 |
| `Tbc1d32` | 0 | 0 BH genes; minimum adjusted p = 1.0 |
| `Rpgr` | 0 | 0 BH genes; minimum adjusted p = 0.648 |
| `Iqcb1` | 0 | 0 BH genes; minimum adjusted p = 1.0 |

The July same-experiment corpus reinforced that this was not a single-target
artifact. `Pkd1:F001` reported fully buffered Pkd1 loss across postnatal
neuronal groups; `Pkd1:F003` specifically noted that ciliary trafficking and
assembly perturbations did not create a broad Pkd1-like response. `Cep290:F001`
called Cep290 FDR-flat across 20 assayed postmitotic neuronal groups, and
`Cep290:F003` reported absence of expected ciliary GPCR, BBSome/IFT and
Hedgehog effector transcription. `Rpgrip1l:F001` and `Rpgrip1l:F004` likewise
described a cross-brain absence for Rpgrip1l and mostly flat represented
ciliogenesis/Hedgehog comparators. `Bbs5:F003` and `Ift88:F003` showed that
membership in the BBS/IFT/ciliary transport pathway mainly converged by
transcriptional buffering, not by a shared DEG program.

Those are appropriate analogs because BICC1 is a KH-domain RNA-binding protein
that assembles SAM-domain ribonucleoprotein complexes with the ciliopathy
proteins ANKS3 and ANKS6. BICC1 also interacts genetically and physically with
PKD1/PKD2 biology in cystogenesis, and in left-right organizers it links Pkd2
flow sensing to post-transcriptional Dand5 repression. In a simple causal
chain, the perturbation would be Bicc1 loss; the direct molecular consequence is
loss of specific KH/SAM-mediated RNP scaffolding and mRNA silencing; propagation
would occur through BICC1-ANKS-polycystin/ciliary signaling, Wnt/cAMP/Dand5
targets, or stress-granule-like RNA granules; the measured endpoint would only
move if that subcellular/post-transcriptional disruption generated stable
nuclear mRNA changes in surviving thalamic glutamatergic nuclei. The visible
Pkd1, transition-zone, BBSome, and IFT perturbations hit the same propagated
compartment in the same acute postmitotic assay and did not move the focal
endpoint.

### RNA-silencing and generic RNA-binding counterexamples

BICC1 has mechanistic links to miRNA-induced silencing: it binds target mRNAs,
can recruit miRNAs from Dicer, and uses Argonaute/TNRC6A/GW182- and
CCR4-NOT-linked silencing for targets such as AC6 in kidney models. I therefore
checked the represented miRNA and decay nodes rather than assuming every RBP
perturbation should be broad:

| training target | observed focal `n_degs` | focal-cell expression evidence |
|---|---:|---|
| `Dicer1` | 0 | 0 BH genes; minimum adjusted p = 0.271 |
| `Ago2` | 0 | 0 BH genes; minimum adjusted p = 0.214 |
| `Tnrc6a` | 0 | 0 BH genes; minimum adjusted p = 1.0 |
| `Tnrc6b` | 0 | 0 BH genes; minimum adjusted p = 1.0 |
| `Cnot1` | 0 | 0 BH genes; minimum adjusted p = 0.721 |
| `Ago1` | 1 | one focal-cell BH gene, `Kif13b` |
| `Fmr1` | 0 | 0 BH genes; minimum adjusted p = 1.0 |
| `Ddx3x` | 8 | a sparse synaptic/neurite set led by `Ypel3`, `Grin2b`, `Synpo2`, `Plekhg1` |
| `Hnrnpc` | 122 | broad RNA-processing signature |
| `Hnrnpu` | 733 | very broad RNA-processing signature |

The Ago/Dicer/TNRC6/CNOT results are the useful comparators: they show that
single-gene perturbation of a post-transcriptional repression pathway is mostly
buffered on the mature neuronal mRNA axis. Generic hnRNPs are counterexamples,
not close analogs. `Hnrnpc` and `Hnrnpu` cause hundreds of DEGs in the same cell
group, so the screen can detect severe RNA-regulatory perturbations; however,
their nuclear RNA-processing functions are not the selective cytoplasmic
BICC1/ANKS/ciliary RNP function. `Ddx3x` is closer to RNA remodeling and
neurodevelopment than to BICC1's polycystin/ciliary branch, and even there the
focal response was only eight genes.

The July corpus agreed with this separation. `Dicer1:F001` and `Ago2:F001`
found no BH-corrected or robust pan-neuronal downstream mRNA program after
acute Dicer1 or Ago2 loss; `Dicer1:F002`, `Ago2:F003`, and `Tnrc6a:F003`
reported that the represented miRNA/RISC/GW182 nodes were flat or tiny rather
than a shared broad derepression module; and `Cnot1:F004` showed that upstream
miRISC/TNRC6 factors did not phenocopy the modest Cnot1 signature outside the
focal cell group.

### Wnt, mTOR, cAMP, and Hedgehog counterexamples

BICC1 and polycystin biology have published connections to Wnt, cAMP/PKA, TOR,
and Dand5/Nodal signaling, but the training data argue against copying those
large or developmental responses into Bicc1:

| training target | observed focal `n_degs` | interpretation |
|---|---:|---|
| `Ctnnb1` | 383 | canonical beta-catenin loss is visible in this thalamic class |
| `Tsc2` | 86 | mTORC1-side perturbation is visible |
| `Mtor` | 2 | direct Mtor loss is weak |
| `Adcy1` | 0 | cAMP side node flat |
| `Adcy3` | 0 | ciliary GPCR/cAMP side node flat |
| `Adcy5` | 0 | cAMP side node flat |
| `Gnas` | 0 | cAMP G protein side node flat |
| `Stat3` | 0 | STAT side node flat |
| `Gli1` | 0 | Hedgehog effector flat |
| `Gli2` | 0 | Hedgehog effector flat |
| `Smo` | 0 | Hedgehog receptor-side node flat |
| `Ptch1` | 0 | Hedgehog receptor-side node flat |
| `Ptch2` | 0 | Hedgehog receptor-side node flat |

This is a counterexample set rather than a promoter set. The Pkd1 report in the
internal corpus separated Pkd1 from both Tsc2-responsive mTORC1/SREBP/lysosomal
transcription (`Pkd1:F004`) and Ctnnb1 beta-catenin transcription
(`Pkd1:F005`). BICC1 can regulate Wnt and cAMP outputs in developing epithelia,
but its obligate downstream branch in the postnatal thalamic nuclear RNA
readout is not canonical Ctnnb1, Tsc2, or Hedgehog transcription.

### Final zero/nonzero decision

I predicted a true zero for `Bicc1`. The decision is driven primarily by
within-dataset evidence: the focal class shows zeros for Pkd1, Cep290,
Rpgrip1l, Bbs/IFT/KIF/dynein ciliary genes, and Dicer/Ago/TNRC6/CNOT RNA
silencing nodes. External BICC1 literature was needed to decide that those are
the correct visible analogs and that the high-count hnRNP and beta-catenin
training perturbations are mechanistic counterexamples rather than estimates.

The exact point prediction was:

| held-out target | predicted `n_degs` |
|---|---:|
| `Bicc1` | 0 |

## Limits and extrapolation

This is an extrapolation from related perturbations, not a direct measurement
of Bicc1. Bicc1's immediate partners `Anks3`, `Anks6`, `Nek8`, and `Pkd2` were
not present in the focal training-count table, so the most direct ANKS6/ANKS3
and PC2 links could not be tested. The parquet is a nuclear RNA readout from
recovered NeuN+ nuclei; it would miss ciliary trafficking, cilium length,
protein translation, cAMP flux, left-right-organizer Dand5 decay, renal or
pancreatic epithelial cystogenesis, and protein-level synaptic effects unless
they secondarily changed abundant nuclear mRNAs by P37-P44. The held-out
experiment could produce a one- or two-gene idiosyncratic DEG call, as `Ago1`
and several ciliary pathway perturbations sometimes do elsewhere, but the
weight of the focal-cell analog evidence is below the FDR 0.05 threshold.
