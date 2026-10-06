# DEG-count prediction for held-out `Cntn1`

## Question and resolved ambiguities

The requested target CSV contains exactly one held-out perturbation:
`Cntn1`. I interpreted `n_degs` exactly as the focal training file defines it:
the number of measured genes, including the targeted gene itself if present,
with `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` nuclei.

The count is therefore allowed to be `1` when the only passing row is the
direct loss of the targeted transcript. This distinction matters here because
the strongest within-dataset signal around neuronal adhesion genes is
"self-transcript loss only", not a broader downstream state.

## Sources

Internal same-experiment data:

- Differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Focal training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Held-out manifest:
  `[local file: 043_Cntn1.csv]`
- Distributed Agents same-experiment corpus release
  `perturbai-july-260713-sourceguard-1773-v1`
- Distributed Agents run-local profile-comparison artifacts:
  `cntn1_candidate_profile_compare.json`,
  `cntn1_candidate_profile_inspect_core.json`, and
  `cntn1_candidate_profile_review.tsv`

External mechanism evidence was taken from PubMed-indexed literature:

- Rios et al. 2000, PMID:11069942, DOI:10.1523/JNEUROSCI.20-22-08354.2000:
  Contactin and Caspr form a neuronal cis complex targeted to paranodal
  junctions during myelination.
- Charles et al. 2002, PMID:11839274, DOI:10.1016/S0960-9822(01)00680-7:
  glial NF155/neurofascin binds the axonal paranodin/Caspr-contactin complex at
  the paranodal axoglial junction.
- Gollan et al. 2003, PMID:14676309, DOI:10.1083/jcb.200309147: Caspr regulates
  intracellular processing of contactin and its interaction with neurofascin.
- Poliak et al. 2001, PMID:11567047,
  DOI:10.1523/JNEUROSCI.21-19-07568.2001: CASPR2/Cntnap2 and Kv1 channels mark
  the juxtaparanodal domain adjacent to the Caspr/contactin paranodal barrier.
- Falk et al. 2002, PMID:12500940, DOI:10.1016/S0248-4900(02)00006-0:
  review of F3/contactin as a GPI-anchored neuronal IgCAM involved in axogenesis
  and myelinated-axon domain organization.

## Computation over the supplied data

1. Loaded the focal training count CSV and used it to calibrate the endpoint.
   Among 1,674 non-held-out perturbations, the distribution was highly sparse:
   median `n_degs = 0`, 469 perturbations were nonzero, the 95th percentile was
   18 DEGs, and a few global regulators such as `Uba5`, `Tpr`, `Sin3a`, `U2af2`,
   and proteasome/splicing factors occupied the high-count tail.

2. Queried the training counts for Contactin/CASPR, IgSF cell-adhesion,
   synaptic-adhesion, semaphorin/plexin, Robo/Slit, Eph/ephrin, and PTPR-family
   candidates. The closest represented targets were all at the floor:

   | training target | focal `n_degs` | interpretation |
   | --- | ---: | --- |
   | `Cntnap1` | 1 | closest measured Caspr partner |
   | `Cntnap2` | 1 | related contactin-associated/CASPR protein |
   | `L1cam` | 1 | IgSF neuronal adhesion |
   | `Chl1` | 1 | IgSF neuronal adhesion |
   | `Ncam1` | 1 | IgSF neuronal adhesion |
   | `Nrcam` | 2 | nodal/L1-family adhesion |
   | `Adam22` | 1 | LGI1/Kv1-associated adhesion complex |
   | `Nrxn1` | 1 | synaptic adhesion |
   | `Nlgn3` | 1 | synaptic adhesion |
   | `Cadm2` | 1 | synaptic adhesion |
   | `Ptprd` | 0 | synaptogenic receptor phosphatase |
   | `Ptprt` | 0 | receptor phosphatase |
   | `Dscam` | 0 | IgSF/guidance counterexample |
   | `Robo1` | 1 | axon-guidance counterexample |
   | `Robo2` | 0 | axon-guidance counterexample |

3. Read the focal parquet rows for these candidates. Each observed perturbation
   had 17,259 measured features. The direct computation was:

   ```python
   focal = de[
       (de.group_name == "151 TH Prkcd Grin2c Glut")
       & de.gene_target.isin(candidates)
   ]
   focal.groupby("gene_target").apply(lambda x: (x.pvals_adj < 0.05).sum())
   focal[focal.pvals_adj < 0.05]
   ```

   For the main comparators, every one-DEG profile was exactly a target-self
   profile:

   | training target | significant focal rows |
   | --- | --- |
   | `Cntnap1` | `Cntnap1` logFC -0.822, FDR 1.09e-11 |
   | `Cntnap2` | `Cntnap2` logFC -1.087, FDR 7.90e-06 |
   | `L1cam` | `L1cam` logFC -0.749, FDR 1.44e-24 |
   | `Chl1` | `Chl1` logFC -0.958, FDR 2.71e-02 |
   | `Ncam1` | `Ncam1` logFC -0.746, FDR 3.00e-10 |
   | `Adam22` | `Adam22` logFC -0.550, FDR 1.07e-09 |
   | `Nrxn1` | `Nrxn1` logFC -0.518, FDR 2.67e-23 |
   | `Nlgn3` | `Nlgn3` logFC -0.896, FDR 4.79e-11 |
   | `Cadm2` | `Cadm2` logFC -0.757, FDR 6.47e-16 |

   The only extra FDR event in this focused adhesion set was `Letm2` in `Nrcam`
   perturbation, with logFC 0.459 and FDR 0.049; the expected pathway genes were
   not coordinately recruited.

4. Ran Distributed Agents `profile_compare` on a 15-node candidate cohort
   (`Cntnap1`, `Cntnap2`, `L1cam`, `Chl1`, `Ncam1`, `Nrcam`, `Adam22`, `Nrxn1`,
   `Nlgn3`, `Cadm2`, and boundary adhesion/guidance nodes). The tool compared
   complete signed log-fold-change vectors and the FDR<0.05 tails. It found all
   15 profiles available; 11 had one to nine significant features and 4 had no
   significant features. In the inspected pairwise rows, `Cntnap1` and `Cntnap2`
   had no shared significant positive or negative features with the IgSF and
   synaptic-adhesion peers. Large absolute logFC ranks in these flat signatures
   usually had `pvals_adj = 1`, so I treated the FDR-supported self rows and
   absence of shared significant features as the reliable evidence rather than
   top raw logFC outliers.

5. Queried the Distributed Agents same-experiment corpus. `Cntn1` itself is absent from
   the release, but the corpus contains high- or moderate-confidence claims
   over the same experiment:

   - Claim `claim:5ee8ada8cf9231d12695`: CASPR/paranodal and Kv1-complex
     structural relationships do not translate into a shared basal neuronal
     nuclear mRNA response; anchored by `Cntnap1:F002` and `Cntnap2:F003`.
   - Claim `claim:dbd8cfcc41d3bc91166c`: acute perturbation of represented
     IgSF adhesion, ankyrin-coupling, and semaphorin/neuropilin-related targets
     does not produce a shared adjusted nuclear mRNA module; anchored by
     `L1cam:F003`, `Ncam1:F003`, and `Chl1:F002`.
   - Claim `claim:da426d57898fc5cde54d`: represented neurexin, neuroligin,
     LRRTM, GluD, CADM, and contactin-associated synaptic-adhesion perturbations
     lack a broad shared downstream DE module.

## Target-specific reasoning

### `Cntn1`

`Cntn1` encodes Contactin-1/F3, a GPI-anchored neuronal Ig-family adhesion
protein. The strongest external mechanism match is the paranodal axonal complex:
Contactin-1 forms a cis complex with Caspr/Cntnap1 that is targeted to
paranodal junctions (Rios et al. 2000), the complex interacts with glial
NF155/neurofascin at the axoglial junction (Charles et al. 2002), and Caspr
controls Contactin-1 processing and its binding behavior toward neurofascin
(Gollan et al. 2003). `Cntnap1` is therefore a more appropriate training analog
than generic cell-adhesion genes.

In the focal data, `Cntnap1` had `n_degs = 1` and its only FDR<0.05 row was
direct `Cntnap1` down-regulation. `Cntnap2`, a related contactin-associated
protein marking juxtaparanodal/Kv1 biology, was also `n_degs = 1`, again only
self. The Distributed Agents CASPR/Kv1 same-experiment claim explicitly reports that
`Cntnap1`, `Cntnap2`, `Kcna1`, `Kcna2`, and `Kcnab2` did not collapse onto a
shared basal neuronal nuclear mRNA state. This is the decisive within-dataset
evidence against a multi-gene paranodal compensation program.

Broader IgSF adhesion and nodal comparators were consistent with the same
answer. `L1cam`, `Chl1`, and `Ncam1` were singleton self hits, `Nrcam` had only
two focal DEGs, and axon-guidance or receptor-phosphatase comparators such as
`Dscam`, `Robo2`, `Ptprd`, and `Ptprt` were zero. The same-experiment Distributed Agents
claims around the L1/NCAM/NrCAM and neurexin/neuroligin/CADM neighborhoods
interpret these as flat or singleton-only structural receptor perturbations
rather than a recurrent downstream module.

The remaining decision was whether `Cntn1` should be exactly zero or exactly
one. Since the measured feature list includes `Cntn1`, and most expressed
IgSF/CASPR analogs in this cell type pass FDR only for their own target RNA, I
predict that `Cntn1` guide assignment will similarly register loss of the
`Cntn1` transcript itself. I do not predict a second or larger downstream
response.

**Prediction:** `Cntn1 = 1`.

## Limits and extrapolations

- `Cntn1` was genuinely held out: it was not present as a `gene_target` in the
  supplied parquet or as a `target_name` in the training count CSV, and it was
  not represented in the Distributed Agents target-scoped same-experiment corpus.
- The two most direct missing comparators are `Cntn2` and `Nfasc`; `Cntnap1` is
  the closest represented partner but is a transmembrane scaffold, whereas
  Contactin-1 is GPI-anchored.
- The experiment perturbs sparse postmitotic neuronal nuclei for 3-4 weeks and
  does not directly measure paranodal protein localization, saltatory
  conduction, glial NF155 biology, or oligodendrocyte responses. Germline
  paranodal phenotypes therefore need not appear as nuclear mRNA DEGs here.
- A one-DEG prediction depends on the hidden `Cntn1` guides reducing a
  sufficiently expressed `Cntn1` transcript in this focal cell group. If
  `Cntn1` baseline expression or guide-level knockdown is weaker than for
  `Cntnap1`, `L1cam`, or `Ncam1`, the true count could fall to zero.
