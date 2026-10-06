# Trace

## Question

The task asks for a point prediction of `n_degs` for each held-out perturbation in
`151 TH Prkcd Grin2c Glut` cells. I interpreted `n_degs` exactly as the count of
measured genes with `pvals_adj < 0.05` in the focal cell group after sparse
postnatal AAV-CRISPR loss of function. The requested file contains one held-out
mouse target, `Pomp`, and it is absent from both the supplied focal-cell training
count CSV and the supplied all-cell differential-expression Parquet.

This is a scalar held-out count prediction, not a ranking task. I therefore did
not use the ranked-prediction workbench, ordering validator, or predictive graph
review; the capability manifest marked all three as unavailable for this
endpoint. The endpoint is directly observed for training perturbations in the
count CSV, directly reconstructable for training perturbations from the Parquet,
and absent by design for Pomp.

## Sources Used

- Declared focal endpoint CSV:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
- Declared all-cell DE Parquet:
  `training differential-expression dataset`
- Requested-target CSV:
  `single-target request for Pomp`
- Run-local dataset portrait, task bindings, coverage, capabilities, and
  measurement registry under `codex_runtime/pipeline/`.
- Internal same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`. I used its bounded graph only to
  navigate to Psmb4/Psmc1/Nfe2l1 report records and then read the packaged
  Finding/Evidence/Reference summaries for those targets. I treated that corpus
  as a curated interpretation of the same experiment, not as independent
  replication or as a candidate score.
- External mechanism evidence:
  Reactome Pathway R-HSA-9907900, Proteasome assembly; UniProt Knowledgebase
  mouse PSMC1 and PSMB4 entries; Bard et al. 2018,
  DOI 10.1146/annurev-biochem-062917-011931; Fricke et al. 2007, PMID
  17948026, DOI 10.1038/sj.embor.7401091; Radhakrishnan et al. 2010, PMID
  20385086, DOI 10.1016/j.molcel.2010.02.029; Bedford et al. 2009, PMID
  19077533, DOI 10.4161/auto.5.2.7389.

## Numeric Calibration

The focal training CSV contains 1674 non-held-out biological targets. The
distribution of `n_degs` is highly zero-inflated: 1205 of 1674 targets are zero,
the median is zero, the 75th percentile is 1, the 90th percentile is 2, the 95th
percentile is 18, and the top counts are sparse outliers such as Uba5 2677, Tpr
1768, Sin3a 1433, Psmb4 742, Psmc1 430, Cdc40 624, Ufc1 572, and Nrf1 138.

I then queried the Parquet rows with
`group_name == "151 TH Prkcd Grin2c Glut"` for the relevant proteasome,
proteostasis, and stress targets and counted FDR-qualified rows with
`pvals_adj < 0.05`. That reproduced the supplied counts for the main anchors:

| training perturbation | focal `n_degs` | endpoint interpretation |
| --- | ---: | --- |
| Psmb4 | 742 | Direct 20S beta-core subunit loss; closest assayed structural proxy for impaired constitutive proteasome core assembly. |
| Psmc1 | 430 | Direct 19S ATPase subunit loss; orthogonal subcomplex of the same 26S proteasome. |
| Nfe2l1 | 0 | Mouse gene for the NFE2L1/TCF11 proteasome-recovery transcription factor; basal loss was not equivalent to damaging the proteasome. |
| Ufc1 | 572 | UFMylation E2, broader ER/proteostasis stress comparator but not a 20S or 19S proteasome component. |
| Uba5 | 2677 | UFMylation E1, very broad stress comparator and useful upper-bound counterexample. |
| Cdc40 | 624 | Spliceosomal perturbation with some shared downstream proteostasis compensation but no direct proteasome lesion. |
| Tpr | 1768 | Nuclear-pore perturbation with a broad downstream distress state, not a proteasome assembly analog. |

In the focal cell group, the two direct 26S proteasome perturbations were much
closer to each other than to Nfe2l1. Psmb4 and Psmc1 shared 215
FDR<0.05 genes and all 215 moved in the same direction. Psmb4 and Nfe2l1 shared
zero FDR<0.05 genes, and Psmc1 and Nfe2l1 shared zero. The marker-level rows
also supported direct proteasome insufficiency after Psmb4/Psmc1: Psmc4,
Psmc6, Psmd1, Psmd2, Psmd4, Sqstm1, Ddit3, Kifc2, Snrpn, and C1qtnf4 moved in
matching directions across Psmb4 and Psmc1, with Psmb4 additionally reaching
FDR 0.05 for Bax, Cdkn1a, Atp1a3, and Syt1.

The same-experiment corpus gave the same internal control at broader
FDR<0.10 resolution. Psmb4 and Psmc1 were reported as each other's strongest
direct-proteasome neighbor: a sparse-signature comparison found 5113 shared
Psmb4/Psmc1 significant gene-cell features across Psmb4-measured groups, 5107
of them same-direction, whereas Nfe2l1, Nfe2l2, Vcp, Atf6, Hspa5, Hspa8,
Hsp90ab1, Ube3a, Ube2e2, Usp48, and Sqstm1 did not phenocopy Psmb4. The Psmc1
report similarly described Psmb4 as the only other assayed constitutive
proteasome subunit and the single strong positive Psmc1 neighbor.

## Pomp Causal Analogy

POMP is the proteasome maturation protein, the mammalian Ump1/proteassemblin
ortholog. It binds proteasome alpha rings, recruits beta subunits stepwise, and
is required for maturation of the 20S catalytic core at the endoplasmic
reticulum. The assembled 26S proteasome consists of this 20S proteolytic core
capped by 19S regulatory particles; PSMB4 is a 20S beta-ring subunit and PSMC1
is a 19S ATPase. Thus the causal chain for Pomp is:

`Pomp CRISPR loss -> impaired new 20S core maturation -> lower functional 26S
proteasome capacity as old complexes turn over -> NFE2L1-dependent proteasome
bounce-back plus aggregate/lysosomal and ISR stress arms -> synaptic-function
withdrawal and possible pro-apoptotic RNA in recovered TH glutamatergic nuclei
-> hundreds of FDR-qualified genes in the Wilcoxon endpoint.`

This is a stronger transfer than simple pathway co-membership because the
positive anchors are physical subunits of the same limiting degradation machine:
Psmb4 impairs the proteolytic core itself and Psmc1 impairs ATP-dependent 19S
gating/unfolding. Reactome R-HSA-9907900 and the Bard 2018 26S proteasome
review place those parts in the same complex, while Fricke et al. 2007 show
that POMP is an essential 20S assembly factor that recruits the beta subunits.
The NFE2L1 evidence from Radhakrishnan et al. 2010 explains why proteasome
damage should up-regulate many PSM genes, but the dataset shows that removing
Nfe2l1 in unstressed neurons is not the same intervention as reducing the
proteasome itself. I used Nfe2l1 as a counterexample, not as a low-count anchor.

The predicted count, 600, is therefore between the two direct subcomplex
anchors: above Psmc1 430 because a POMP lesion is expected to bottleneck 20S
core formation upstream of all active beta subunits, but below Psmb4 742 because
POMP acts through new-core assembly rather than by mutating a mature catalytic
particle subunit. I did not borrow the larger Uba5 or Tpr counts; their broad
stress states include some Ddit3/Sqstm1/Pomp-like transcripts, but UFMylation
and nuclear-pore perturbations enter proteostasis indirectly and are not
obligate 26S assembly lesions. I also did not collapse the prediction to the
training median of zero, because both assayed direct 26S perturbations were
among the strongest responders in this exact focal-cell endpoint.

## Prediction

| target | predicted `n_degs` | rationale |
| --- | ---: | --- |
| Pomp | 600 | POMP is an essential 20S assembly chaperone, so its acute loss should converge with Psmb4 and Psmc1 proteasome-insufficiency signatures and induce a large nonzero proteasome-bounce-back/stress/synaptic-withdrawal response in `151 TH Prkcd Grin2c Glut`. |

## Limits

The precise count is extrapolated because no Pomp DE signature is present in
the supplied Parquet and Pomp is not represented in the July same-experiment
graph. POMP affects assembly of newly made 20S cores, so the observed 3-4 week
phenotype can depend on proteasome turnover, residual POMP protein, the fraction
of alleles edited, and survival of severely affected nuclei. The Parquet
contains normalized nuclear RNA from recovered nuclei, not proteasome activity,
ubiquitinated-protein burden, POMP protein, DNA indels, guide-exposure
denominators, or pre-harvest cell loss. The external POMP papers are mostly
non-neuronal biochemical systems, and the Psmc1 neurodegeneration evidence used
conditional germline alleles rather than sparse postnatal AAV CRISPR. Those
context gaps affect the magnitude, but they do not break the core causal link
from Pomp loss to reduced 20S/26S proteasome capacity.
