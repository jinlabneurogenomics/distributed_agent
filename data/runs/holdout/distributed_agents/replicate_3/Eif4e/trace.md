# Question and resolved scope

The requested held-out target list contains one mouse gene, `Eif4e`. I predicted the
number of genes that would have `pvals_adj < 0.05` in the held-out
`151 TH Prkcd Grin2c Glut` readout after P16 AAV-PHP.eB CRISPR
loss of function, using only non-held-out signatures and counts plus external
biology.

I treated `n_degs` exactly as the supplied training CSV does: it is the count of
measured nuclear RNA features passing Benjamini-Hochberg FDR 0.05 in this one
cell group. Self-transcript depletion is included in that endpoint when it
passes FDR, so small counts of 1-2 can mean "target RNA only" or one target RNA
plus one downstream marker.

The main ambiguity is that `Eif4e` is biochemically central, whereas this
Perturb-seq experiment is an acute, sparse, partially depleting, postnatal
snRNA-seq assay. I therefore did not equate organismal essentiality, protein
synthesis, or synaptic physiology with a broad nuclear RNA abundance response.

# Sources used

- Training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Training DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Held-out manifest:
  `[local file: 068_Eif4e.csv]`
- Distributed Agents internal same-experiment corpus, release
  `perturbai-july-260713-sourceguard-1773-v1`. `Eif4e` itself was absent, as
  expected for a held-out target, but the corpus contained curated findings for
  assayed `Eif4g1`, `Eif4a2`, `Eif4h`, `Mtor`, `Tsc2`, `Fmr1`, and other
  translation-control neighbors.
- PubMed literature fetched through NCBI E-utilities:
  - Sonenberg and Hinnebusch 2009, PMID 19239892, DOI
    `10.1016/j.cell.2009.01.042`
  - Napoli et al. 2008, PMID 18805096, DOI `10.1016/j.cell.2008.07.031`
  - Huang and Manning 2008, PMID 18466115, DOI `10.1042/BJ20080281`
  - Thoreen et al. 2012, PMID 22552098, DOI `10.1038/nature11083`
  - Gkogkas et al. 2012, PMID 23172145, DOI `10.1038/nature11628`
  - Santini et al. 2012, PMID 23263185, DOI `10.1038/nature11782`

# Computational evidence

I first verified that the requested manifest contains only:

| target | held out from training |
| --- | --- |
| `Eif4e` | yes |

The focal training count table has 1,674 non-held-out perturbations. The endpoint
is very sparse: 1,205/1,674 targets have 0 DEGs, the median is 0, the 75th
percentile is 1, and the 90th percentile is 2. Only 106 targets have at least 10
DEGs. That distribution matters because a point prediction of 1 or 2 is already
above most perturbations in this focal group.

I then queried the focal rows of the parquet for assayed translation-initiation,
FMRP/CYFIP, elongation, and mTOR/TSC neighbors of `Eif4e`. The exact
`151 TH Prkcd Grin2c Glut` DEG counts were:

| training perturbation | n_degs | relationship to Eif4e |
| --- | ---: | --- |
| `Eif4a2` | 2 | eIF4A helicase in the eIF4F cap-initiation module |
| `Eif4g1` | 1 | eIF4G scaffold that binds eIF4E |
| `Eif4h` | 1 | accessory factor for eIF4A/eIF4F helicase activity |
| `Mtor` | 2 | upstream kinase that controls 4E-BP/eIF4E-eIF4G availability |
| `Rptor` | 0 | mTORC1 scaffold, positive arm |
| `Akt3` | 0 | upstream PI3K/AKT input to mTORC1 |
| `Tsc2` | 86 | negative regulator of Rheb/mTORC1 |
| `Fmr1` | 0 | local-translation repressor connected to eIF4E through CYFIP1 |
| `Cyfip1` | 0 | eIF4E-binding FMRP partner |
| `Cnot1` | 0 | CCR4-NOT/post-transcriptional regulator |
| `Ddx3x` | 8 | RNA helicase, translation-initiation related but not eIF4F-wide |
| `Eef2` | 9 | elongation factor rather than cap-initiation factor |
| `Eif2ak4` | 0 | integrated-stress-response kinase |
| `Eif5a` | 0 | translation elongation/termination factor |
| `Fkbp1a` | 1 | weak mTOR-adjacent comparator |

For the most relevant direct comparators, I also inspected the actual
FDR-significant features in the focal parquet:

| perturbation | focal FDR < 0.05 genes |
| --- | --- |
| `Eif4a2` | `Eif4a2` down, `Cadm4` down |
| `Eif4g1` | `Eif4g1` down |
| `Eif4h` | `Hexim1` up |
| `Mtor` | `Rims3` up, `Tmed8` down |
| `Fkbp1a` | `Fkbp1a` down |
| `Rptor`, `Akt3`, `Fmr1`, `Cyfip1`, `Cnot1`, `Eif2ak4`, `Eif5a` | none |
| `Ddx3x`, `Eef2` | 8 and 9 sparse genes, respectively, including `Ddx3x` self-depletion for `Ddx3x` |
| `Tsc2` | 86 genes, including sterol and lysosomal/metabolic entries such as `Cyp51`, `Pik3r3`, `Slc2a6`, `Ldlr`, `Msmo1`, `Atp6v0b`, `Lamp2`, `Rragd`, and `Ddit4` |

I used `mcp__distributed_agents_runtime.profile_compare` on these 15 pathway-adjacent
targets with `gene_target` as the profile entity, measured genes as features,
`logfoldchanges` as signed values, `pvals_adj < 0.05` as the significance
threshold, and `group_name = 151 TH Prkcd Grin2c Glut` as the exact context.
The run-local comparison reported:

- 7 of the 15 inspected translation-control/mTOR neighbors had no significant
  focal features.
- 7 had only 1-9 significant focal features.
- `Tsc2` was the only one with at least 50 significant focal features.

The expression-pattern comparison supported the same conclusion as the counts.
`Eif4a2` and `Eif4g1` were the closest direct eIF4F pair within the inspected
cohort by full-vector correlation, but both signatures were nearly flat and they
shared no FDR-significant non-self downstream feature. `Tsc2` was clearly active
but did not phenocopy `Mtor`, `Rptor`, or direct eIF4F loss; it is a counterexample
showing assay detectability for mTOR/TSC biology, not a template for `Eif4e`.

# Internal-corpus evidence

The Distributed Agents corpus had no held-out `Eif4e` findings, so I did not use any
same-experiment `Eif4e` readout. It did contain several relevant
non-held-out findings:

- The `Eif4g1` report concluded that loss of the core eIF4F scaffold produced
  no downstream FDR-level neuronal nuclear RNA response and that the
  eIF4F/Mtor/Rptor arm was flat or extremely weak whereas `Tsc2` was broad.
- The corpus claim `claim:d9c5c745caea54cd56a7` states that represented
  translation-factor, cap-initiation, RNA-helicase, and mTOR-adjacent
  perturbations do not produce a generic shared postmitotic neuronal nuclear
  mRNA signature.
- The `Mtor` report found only a small TH/midbrain RNA response and emphasized
  that canonical same-pathway perturbations such as `Rptor`, `Fkbp1a`, `Akt3`,
  and PI3K subunits did not phenocopy `Mtor`.
- The `Tsc2` report curated the broad positive response as mTORC1/SREBP/lysosomal
  engagement in susceptible caudal neurons.
- The `Fmr1` and `Cyfip1` reports emphasized that FMRP/CYFIP/local-translation
  genes were flat or near-flat at this nuclear RNA endpoint.

These findings are important because they are same-assay statements over the
held-out gene's mechanistic neighborhood rather than generic gene annotations.

# Biological rationale for Eif4e

EIF4E is the 5-prime cap-binding subunit of eIF4F; eIF4G acts as the scaffold
that links EIF4E and EIF4A, and 4E-BP proteins suppress cap-dependent initiation
by competing with EIF4G for EIF4E binding. This relationship is the canonical
mTORC1-4E-BP-eIF4E control point described by Sonenberg and Hinnebusch 2009 and
functionally resolved for mTORC1 TOP/TOP-like mRNA translation by Thoreen et al.
2012. Upstream, the TSC1/TSC2 complex is a Rheb GAP and inhibits mTORC1
signaling (Huang and Manning 2008).

The closest assayed loss-of-function analogs in this screen are therefore
`Eif4g1`, `Eif4a2`, `Eif4h`, `Mtor`, and `Rptor`, not high-count generic
stressors. In the focal cell group, those genes gave 1, 2, 1, 2, and 0 DEGs. The
two exact eIF4F core genes with target-self depletion, `Eif4a2` and `Eif4g1`,
look especially informative: their counts are basically the edited transcript
itself plus at most one downstream gene. That argues that a CRISPR hit to
`Eif4e`, another core eIF4F component, should be nonzero if its own nuclear RNA
is depleted but should not explode into a Tsc2-like response.

`Tsc2` is the main positive counterexample. It is biologically linked to the
same mTORC1/4E-BP/eIF4E axis, and `Tsc2` loss yielded 86 focal DEGs here, but
the direction is disinhibition of mTORC1 rather than removal of a cap-initiation
factor. The assayed loss-of-function positive mTORC1 arm, `Mtor` and `Rptor`,
stayed at 2 and 0 DEGs. This makes the broad `Tsc2` sterol/lysosomal program an
excess-growth-signaling state rather than an expected output of partial
`Eif4e` depletion.

FMRP/CYFIP provides another route to EIF4E. CYFIP1 binds EIF4E as a translational
repressor with FMRP (Napoli et al. 2008), and eIF4E overactivity or loss of
4E-BP2 can perturb mouse neuronal translation and autism-related behaviors
(Gkogkas et al. 2012; Santini et al. 2012). In the present snRNA-seq dataset,
however, `Fmr1` and `Cyfip1` both had 0 DEGs in `151 TH Prkcd Grin2c Glut`.
That is good evidence that this endpoint is poor at reading out local
translation and synaptic physiology when they do not secondarily alter nuclear
mRNA levels.

Taken together, I predict `Eif4e` is not a zero because its own transcript is
likely detectable and knocked down, as seen for `Eif4a2` and `Eif4g1`. I also
predict it remains at the floor of the nonzero distribution because every direct
cap-initiation loss-of-function comparator was buffered in this cell class.

# Prediction

| target | predicted_n_degs | rationale |
| --- | ---: | --- |
| `Eif4e` | 1 | direct eIF4F component; closest measured eIF4F losses were 1-2 DEGs and mostly self-transcript effects; mTOR/TSC and FMRP/CYFIP counterexamples argue against either 0 from failed relevance or a broad Tsc2-like program |

# Limits

- `Eif4e` itself had no supplied signature or Distributed Agents finding; the prediction
  is an extrapolation from other cap-initiation genes.
- `Eif4g1`, `Eif4a2`, and `Eif4h` are strong biochemical analogs but not
  redundant copies of EIF4E. The screen lacked `Eif4ebp1`, `Eif4ebp2`, `Eif4b`,
  `Eif4a1`, `Pten`, `Rheb`, and `Rps6kb1`, so several ideal direction controls
  were unavailable.
- snRNA-seq does not measure ribosome occupancy, local dendritic translation,
  synaptic proteins, phosphorylation of 4E-BP/S6K, or cell size. EIF4E could
  have protein-level effects invisible to `n_degs`.
- A one-DEG point call is necessarily fragile because it can hinge on whether
  the edited target transcript itself passes FDR in this cell group.
