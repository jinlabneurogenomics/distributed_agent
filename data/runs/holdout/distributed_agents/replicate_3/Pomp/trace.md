# Predicting held-out DEG breadth for `Pomp`

## Question and interpretation

The requested held-out perturbation was `Pomp`. I interpreted `n_degs` as the
number of measured genes in `151 TH Prkcd Grin2c Glut` with
`pvals_adj < 0.05` in the supplied Wilcoxon DE output. `Pomp` is absent from the
training-count table and from the DE parquet as a `gene_target`, so its count
had to be inferred from non-held-out perturbations.

I treated the count as an assay-specific breadth endpoint, not as a direct
measure of target essentiality or editing. In particular, the sparse AAV
CRISPR design, 3-4 week post-perturbation harvest, postmitotic NeuN+ sampling,
and possible survivor bias all matter when transferring from external biology.

## Sources used

- Raw focal-cell DE rows from
  `[local file: training_de_all_cell_groups.parquet]`.
- Training endpoint counts from
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Held-out target manifest
  `[local file: 181_Pomp.csv]`.
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`, especially the `Psmb4`,
  `Psmc1`, `Nfe2l1`, and `Nrf1` finding summaries and the high-confidence
  corpus claim that direct proteasome-subunit perturbations induce a
  proteostasis/HSP/ISR/synaptic-withdrawal program whereas adjacent stress
  regulators and accessory proteostasis genes do not generally reproduce that
  state.
- Offline mouse gene annotations built from GO, KEGG, Reactome, CORUM v5, MGI
  one-to-one orthology, and STRING v12.0.
- External literature:
  - Kruger, Kloetzel, and Enenkel 2001, DOI
    `10.1016/s0300-9084(01)01241-x`, PMID `11295488`: Ump1/POMP is a
    proteasome maturation factor associated with 20S precursor intermediates
    and degraded on final 20S maturation.
  - Jayarapu and Griffin 2004, DOI `10.1016/j.bbrc.2003.12.119`, PMID
    `14733938`: human proteassemblin/POMP physically interacts with 20S beta
    subunits including beta7-like subunit surfaces, supporting a direct
    preproteasome assembly role.
  - Radhakrishnan et al. 2010, DOI `10.1016/j.molcel.2010.02.029`, PMID
    `20385086`: mammalian NFE2L1/NRF1 drives transcriptional proteasome
    recovery after proteasome inhibition, a useful prior for interpreting
    proteasome-subunit rebound rather than for treating basal `Nfe2l1` LoF as
    a structural proteasome phenocopy.
  - Zieba et al. 2017, DOI `10.1016/j.jdermsci.2017.04.009`, PMID
    `28728908`: POMP is required for efficient proteasome assembly in human
    keratinocytes; POMP silencing inhibited assembly and induced apoptosis.

## Computational checks

I first summarized the supplied focal-cell training counts. Of 1,674
non-held-out perturbations, 1,205 were zero, only 43 had at least 100 DEGs, 19
had at least 400, and 9 had at least 700. Thus any several-hundred prediction
is in the far right tail of this endpoint.

I then filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and
to proteasome/proteostasis candidates. The closest direct proteasome members in
the training universe were:

| training target | focal `n_degs` | reason for comparing to `Pomp` |
| --- | ---: | --- |
| `Psmb4` | 742 | 20S core beta subunit; a direct structural lesion in the particle whose maturation requires POMP |
| `Psmc1` | 430 | 19S AAA ATPase subunit; an independent 26S proteasome structural lesion |
| `Elp2` | 150 | annotated only in broader GO proteasome-assembly regulation; mainly a proteostasis/translation-stress comparator, not a direct core-assembly analog |
| `Nrf1` | 138 | broad stress/proteostasis neighbor in the same corpus, but official mouse `Nrf1` is nuclear respiratory factor 1, not NFE2L1 |
| `Nfe2l1` | 0 | canonical proteasome bounce-back transcription factor; basal LoF is a counterexample rather than a POMP analog |
| `Sec63`, `Hspa5`, `Hspa8`, `Hsf1`, `Usp48`, `Vcp`, `Atg5`, `Sqstm1`, `Ube2e2`, `Ube3a`, `Atf6`, `Nfe2l2` | 0-11 | adjacent ER stress, chaperone, autophagy, ubiquitin, and UPR/NRF branches that stayed weak or silent in this focal group |

Within the focal DE rows, `Psmb4` and `Psmc1` had 215 shared
FDR<0.05 downstream genes and all 215 moved in the same direction. Shared
strong features included `Kifc2`, `C1qtnf4`, `Psmd4`, `Gria2`, `Nrxn1`,
`Sqstm1`, and `Ddit3`; `Psmb4` also up-regulated other proteasome transcripts
such as `Psmc4`, `Psmd1`, and `Psmd4`. This made the two subunits a coherent
proteasome-insufficiency state rather than two unrelated broad signatures.

The Reactome `Proteasome assembly` and KEGG `Proteasome` mouse sets contained
`Pomp`, `Psmb4`, and `Psmc1`, but among non-held-out training targets only
`Psmb4` and `Psmc1` were in those sets. The GO `proteasome assembly` set added
`Elp2`, but `Elp2` is not a core particle or POMP-like assembly chaperone, so I
used it only as a loose lower-bound stress comparator.

## Target-specific reasoning

### `Pomp`

`Pomp` encodes the proteasome maturation protein, the mammalian ortholog of
Ump1. External work places it inside 20S core biogenesis: it binds precursor
complexes, contacts beta-subunit surfaces, and is degraded as newly assembled
20S particles mature. That biology is much closer to the held-in structural
proteasome hits than to `Nfe2l1`, `Hsf1`, `Atf6`, or `Vcp`: knocking out POMP
should reduce formation of new catalytic 20S cores, whereas knocking out a
stress sensor in otherwise basal neurons often removes a downstream
transcriptional branch without creating the upstream proteotoxic load.

The same-experiment evidence supports that distinction. `Psmb4` and `Psmc1`
were both strong, sign-concordant responders in the focal cell type, with 742
and 430 DEGs respectively, and the Distributed Agents corpus reports proteasome-subunit
loss inducing proteasome rebound, chaperone/ISR, autophagy/ubiquitin-handling,
redox/p53-like, and synaptic-withdrawal arms. By contrast, direct perturbation
of the canonical bounce-back TF `Nfe2l1` had zero focal FDR<0.05 genes, and
UPR, HSF1, NRF2, VCP, autophagy, and ubiquitin-branch perturbations were also
near-zero. That argues against assigning POMP a generic proteostasis average
and in favor of anchoring it to `Psmb4`/`Psmc1`.

I predicted a high nonzero count, below `Psmb4` but comparable to the
geometric midpoint of `Psmb4` and `Psmc1`. The downward adjustment reflects
that POMP is an assembly factor rather than a stoichiometric assayed core
subunit, that pre-existing neuronal proteasomes could buffer partial acute
loss, and that the actual held-out `Pomp` matched perturbed-cell count is
unknown. The zero/nonzero decision is driven by the direct 20S assembly
mechanism plus the strong within-dataset `Psmb4`/`Psmc1` convergence; the exact
integer is extrapolation from only two very close structural proteasome
anchors.

Predicted `Pomp n_degs`: **520**.

## Limits

The main limitation is that there was no held-in `Psmg`, `Psma`, or other
POMP-like assembly-chaperone perturbation in the focal training counts. The
nearest counts are one 20S beta subunit and one 19S ATPase subunit, so the
prediction has to assume that blocking 20S assembly is read out similarly to
losing a mature 26S proteasome component after 3-4 weeks in postnatal neurons.

External POMP literature is mostly yeast or non-neuronal mammalian cell work;
it establishes mechanism, but not the dose-response or survival bias of sparse
postmitotic mouse neuronal CRISPR. Finally, the DE endpoint is sensitive to
the unobserved number of recovered `Pomp`-perturbed nuclei and to FDR
thresholding, so I consider the hundreds-scale class more secure than the
specific point value of 520.
