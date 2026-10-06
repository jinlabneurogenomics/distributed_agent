# Reasoning trace

## Question and resolved ambiguities

The requested held-out target file contains one perturbation:

```tsv
target_name
Zkscan3
```

I interpreted the endpoint as the focal-cell count of measured genes with
`pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` for an acute, sparse, AAV
CRISPR loss-of-function perturbation of mouse `Zkscan3`. The number to predict
is therefore an assay-specific count of FDR-significant nuclear RNA changes,
not a score for ZKSCAN3 biological importance, autophagic flux, viability, or
editing efficiency. All computations below used exactly
`group_name == "151 TH Prkcd Grin2c Glut"`.

## Sources used

- Input endpoint CSV:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Input differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Input requested-target manifest:
  `[local file: 272_Zkscan3.csv]`
- Distributed Agents same-experiment corpus, release
  `perturbai-july-260713-sourceguard-1773-v1`, queried for held-out
  `Zkscan3`, represented `Zkscan1`/`Zkscan16`, SCAN/KRAB-ZFP claims, and
  mTOR/autophagy/lysosome claims.
- Distributed Agents runtime focal-profile comparison. I attempted to use the runtime
  profile-neighbor artifact for `Zkscan1`, `Zkscan16`, `Setdb1`, `Mtor`,
  `Atg5`, and `Tsc2`; the profile artifact was written, but the flat-table
  inspector rejected this artifact schema. I therefore recomputed the needed
  bounded FDR summaries directly from the parquet with `pyarrow.dataset`.
- NCBI PubMed literature searches for ZKSCAN3. Key papers used:
  Chauhan et al. 2013, Molecular Cell, DOI `10.1016/j.molcel.2013.01.024`,
  PMID `23434374`; Li et al. 2023, International Journal of Molecular
  Sciences, DOI `10.3390/ijms24097786`, PMID `37175493`; Pan and Valapala
  2021, Cells, DOI `10.3390/cells10102504`, PMID `34685484`; Hu et al.
  2020, Nucleic Acids Research, DOI `10.1093/nar/gkaa425`, PMID `32427330`;
  Ouyang et al. 2023, Physiological Reports, DOI `10.14814/phy2.15686`,
  PMID `37144628`.

## Dataset calculations

The focal training CSV contains 1,674 non-held-out perturbations. It is highly
zero-inflated: 1,205 perturbations have `n_degs = 0`, the median is 0, the 75th
percentile is 1, and the 95th percentile is 18. A small minority of essential
or broad chromatin/RNA-processing perturbations form the long tail
(`Uba5`, 2,677; `Tpr`, 1,768; `Sin3a`, 1,433; `Rnpc3`, 868; `Zbtb7a`, 841).

I then filtered the DE parquet to:

```python
(group_name == "151 TH Prkcd Grin2c Glut") &
gene_target.isin(relevant_comparators)
```

and counted rows per `gene_target` with `pvals_adj < 0.05`. This both verified
the endpoint counts in the CSV and exposed which individual transcripts drove
the rare nonzero comparator profiles.

Observed focal counts for the biologically relevant comparators were:

```tsv
target_name	n_degs	reason_for_query
Zkscan1	0	represented KRAB/SCAN/Zn-finger family member
Zkscan16	0	represented KRAB/SCAN/Zn-finger family member
Zscan26	0	represented SCAN/Zn-finger family member
Zfp397	0	represented SCAN/C2H2 comparator from the corpus KRAB/SCAN claim
Zfp664	0	represented C2H2 comparator from the corpus KRAB/SCAN claim
Zfp612	1	weak represented C2H2 comparator; only Notum passed FDR
Zfp1	0	KRAB/C2H2 comparator in Setdb1 corpus contrasts
Zfp846	0	KRAB/C2H2 comparator in Setdb1 corpus contrasts
Zfp950	0	KRAB/C2H2 comparator in Setdb1 corpus contrasts
Setdb1	22	broad KRAB/KAP1-adjacent heterochromatin effector
Chd4	100	NuRD chromatin-repression effector; active in this cell group
Mecp2	16	heterochromatin/methyl-CpG comparator
Mtor	2	autophagy- and mTOR-axis comparator
Tsc2	86	mTORC1 negative regulator; strong pathway counterexample
Atg5	0	core autophagy comparator
Atg16l1	0	core autophagy comparator
Becn1	0	autophagy initiation comparator
Rb1cc1	4	autophagy initiation comparator
Ppt1	1	lysosomal disease comparator
Psap	1	lysosomal disease comparator
Tmem106b	1	lysosomal disease comparator
Atp6ap2	2	V-ATPase/lysosomal comparator
Rab7	501	endolysosomal trafficking counterexample with a broad response
```

The focal FDR-significant overlaps also argued against pooling the active
chromatin or lysosomal perturbations as if they were one generic signature.
`Setdb1` and `Chd4` shared only 4 FDR genes; `Chd4` and `Mecp2` shared 2;
`Chd4` and `Tsc2` shared 4; `Tsc2` and `Rab7` shared 38 despite the large
`Rab7` count. The two observed `Zkscan` perturbations and `Zscan26` had no
focal FDR genes at all. Canonical ZKSCAN3 autophagy/lysosome targets that are
measured in the dataset, including `Map1lc3b`, `Wipi2`, `Lamp1`, `Lamp2`,
`Ctsb`, `Ctsd`, `Sqstm1`, `Tfeb`, and `Atg5`, were all FDR-flat
(`pvals_adj = 1.0`) after `Zkscan1`, `Zkscan16`, `Zscan26`, `Atg5`, and `Mtor`
perturbation in the focal cell group.

## Same-experiment corpus evidence

The Distributed Agents corpus had no target context for the held-out `Zkscan3`, which is
consistent with it being absent from the training universe. It did contain
useful in-experiment summaries for the represented relatives:

- For `Zkscan1`, the corpus reported an all-null postnatal neuronal DE surface:
  every recovered neuronal group had zero downstream genes even at FDR 0.10.
  It further reported that `Zkscan16` and `Zscan26` did not phenocopy
  `Zkscan1`, with near-zero full-score correlations.
- For `Zkscan16`, the corpus summarized a two-gene, two-cell-class surface
  outside the focal 151 group, and no broad neuronal transcriptional program.
  It explicitly contrasted `Zkscan16` with `Zkscan1`, `Zscan26`, `Setdb1`, and
  `Mecp2`, concluding that the isolated `Zkscan16` hits should not be read as a
  generic KAP1/SETDB1 or MeCP2 program.
- A moderate-confidence SCAN/C2H2/KRAB corpus claim states that represented
  SCAN/C2H2/KRAB-associated zinc-finger perturbations do not define an
  interchangeable shared neuronal transcriptomic regulon in this screen; its
  target set included `Zfp397`, `Zfp612`, `Zfp664`, `Zkscan1`, `Zkscan16`, and
  `Zscan26`.
- The corpus also separated Setdb1-sensitive and autophagy/lysosome-associated
  responses from generic family membership: individual KRAB/C2H2 ZFP
  perturbations were flat despite a detectable `Setdb1` neuronal response, and
  represented autophagy/lysosome perturbations were not transcriptomically
  interchangeable in this postnatal neuronal assay.

Those claims made the two strongest positive comparators for `Zkscan3`
negative: same-domain ZKSCAN/SCAN perturbations were null or singleton, and a
generic KRAB-ZFP-to-SETDB1 interpretation was not supported by the actual
training signatures.

## External ZKSCAN3 biology

ZKSCAN3 is a KRAB/SCAN/C2H2 zinc-finger transcription factor. Chauhan et al.
identified human ZKSCAN3 as a transcriptional repressor of autophagy and
lysosomal biogenesis/function, with knockdown derepressing a regulon of more
than 60 autophagy or lysosomal genes and direct repression of targets including
`MAP1LC3B` and `WIPI2` (Chauhan et al. 2013, DOI
`10.1016/j.molcel.2013.01.024`, PMID `23434374`). That result made autophagy
and lysosome genes the main mechanistic axis to test in the training data.

The same literature is strongly context-dependent, however. Pan and Valapala
found derepression of only some ZKSCAN3 targets and increased autophagy flux in
retinal pigment epithelial cells after siRNA knockdown (Pan and Valapala 2021,
DOI `10.3390/cells10102504`, PMID `34685484`). Li et al. generated complete
ZKSCAN3 knockouts in HeLa and HK-2 cells and found that loss of ZKSCAN3 did not
significantly promote autophagic or lysosomal gene expression, arguing that it
is not an essential universal repressor of that regulon (Li et al. 2023, DOI
`10.3390/ijms24097786`, PMID `37175493`). Hu et al. assigned ZKSCAN3 an
autophagy-independent role in heterochromatin maintenance in senescent human
mesenchymal stem cells (Hu et al. 2020, DOI `10.1093/nar/gkaa425`, PMID
`32427330`). Cardiomyocyte-specific mouse `Zkscan3` loss modulated pressure
overload remodeling and autophagy-related transcripts in a stressed heart
context rather than establishing a broad basal neuronal RNA phenotype (Ouyang
et al. 2023, DOI `10.14814/phy2.15686`, PMID `37144628`).

Thus external biology gave two possible expectations: weak derepression of an
autophagy/lysosome gene set, or complete buffering when the relevant ZKSCAN3
repressor complex is not limiting in the assayed state. The in-dataset evidence
favored the second expectation for basal, juvenile-to-young-adult, postmitotic
thalamic glutamatergic neurons.

## Target-specific prediction

### Zkscan3

Biologically relevant training perturbations:

- `Zkscan1`, `Zkscan16`, and `Zscan26`: the closest represented
  SCAN/KRAB-associated zinc-finger comparators. All had `n_degs = 0` in
  `151 TH Prkcd Grin2c Glut`; the same-experiment corpus also reported that
  they failed to phenocopy one another across the wider neuronal panel.
- `Zfp397`, `Zfp664`, `Zfp612`, `Zfp1`, `Zfp846`, and `Zfp950`: broader
  KRAB/C2H2 or SCAN/C2H2 checks. The counts were 0, 0, 1, 0, 0, and 0,
  respectively, so the training set did not support a common KRAB-ZFP response
  that could be transferred to an unobserved KRAB/SCAN target.
- `Setdb1`, `Chd4`, and `Mecp2`: active repressive-chromatin counterexamples
  with counts of 22, 100, and 16. Their nonzero profiles show the focal cell
  group can report chromatin perturbations, but their significant genes were
  not shared with the Zkscan/Zscan profiles and the corpus describes them as
  separable from individual assayed KRAB-ZFP perturbations.
- `Mtor`, `Tsc2`, `Atg5`, `Atg16l1`, `Becn1`, `Rb1cc1`, and `Rab7`: pathway
  checks for ZKSCAN3's published autophagy/lysosome activity. `Mtor`, `Atg5`,
  `Atg16l1`, and `Becn1` were 0 to 2 DEGs in the focal group; `Rb1cc1` had 4.
  `Tsc2` and `Rab7` were nonzero counterexamples, proving that mTOR/lysosomal
  transcriptional responses can be detected, but their responses reflect
  mTORC1 disinhibition and endolysosomal trafficking stress rather than a
  ZKSCAN3-like sequence-specific transcription-factor loss.

The zero/nonzero decision was driven primarily by the within-dataset evidence.
The closest represented DNA-binding family members were exact zeros in the
focal endpoint; broader KRAB/C2H2 zinc fingers were almost all zero; and
core autophagy-gene perturbations did not mobilize the focal 151 state.
External ZKSCAN3 papers justify checking the autophagy/lysosome genes but do
not override the cell-context specificity, especially given complete ZKSCAN3
knockout cells that lacked broad autophagy-lysosome derepression.

I therefore predict that acute sparse `Zkscan3` loss will not yield any gene
passing the focal Benjamini-Hochberg FDR 0.05 cutoff.

Point prediction: `0`

## Limits

`Zkscan3` itself is not represented in the training DE matrix or the Distributed Agents
same-experiment corpus, so this is an extrapolation from paralogs, broad
domain-family members, KRAB/SETDB1-adjacent chromatin perturbations, and
autophagy/lysosome counterexamples. `Trim28/Kap1`, TFEB-family transcription
factors, and the full ZKSCAN3 direct target set were not perturbations in the
available focal training table, and gene-level snRNA-seq cannot read out
repeat derepression, ZKSCAN3 protein localization, autophagic flux, lysosomal
activity, or long-term storage phenotypes. The prediction also assumes that the
acute mosaic P16-to-P37/P44 neuronal CRISPR setting remains closer to the flat
basal training perturbations than to stressed RPE, cardiomyocyte, tumor, or
neurodegeneration models in which ZKSCAN3 effects can be larger.
