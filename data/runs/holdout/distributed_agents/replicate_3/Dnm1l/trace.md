# Reasoning trace

## Question and resolved ambiguities

I interpreted the requested endpoint as the focal-cell count

`sum(pvals_adj < 0.05)`

for every held-out `gene_target` in `151 TH Prkcd Grin2c Glut`, using the same
Wilcoxon/BH differential-expression table as the training targets.  The run
manifest contained one requested target, `Dnm1l`.  `Dnm1l` is not present as a
training perturbation in either input file, so its exact signature could not be
looked up.  I treated zero as a prediction that no measured gene would pass FDR
0.05, not as a statement that DRP1 has no neuronal function.

## Sources used

- The requested-target manifest:
  `[local file: 059_Dnm1l.csv]`.
- The training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- The full training DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`; `Dnm1l`
  itself had no held-out-safe corpus node, so I used corpus findings for
  training analogs and boundaries: `Mff:F001-F004`, `Opa1:F001-F009`,
  `Yme1l1:F001-F004`, `Rhot1:F001-F003`, `Rab7:F001-F011`, and
  `Dctn1:F001-F009`.
- A run-local Distributed Agents runtime comparison,
  `dnm1l_mito_compare.json`, over the `151 TH Prkcd Grin2c Glut` profiles of
  `Mff`, `Opa1`, `Yme1l1`, `Rhot1`, `Dnm1`, `Atg5`, `Atg16l1`, `Park7`,
  `Rab7`, `Dctn1`, and `Nrf1`.
- NCBI PubMed primary literature:
  Otera et al. 2010, DOI `10.1083/jcb.201007152`, PMID `21149567`;
  Wakabayashi et al. 2009, DOI `10.1083/jcb.200903065`, PMID `19752021`;
  Loson et al. 2013, DOI `10.1091/mbc.E12-10-0721`, PMID `23283981`;
  Palmer et al. 2013, DOI `10.1074/jbc.M113.479873`, PMID `23921378`;
  Itoh et al. 2019, DOI `10.7554/eLife.44739`, PMID `31603426`.

## Computation over the training data

The training count table had 1,674 non-held-out perturbations in the focal
cell group.  It was very zero-inflated: 1,205 of 1,674 had `n_degs = 0`, the
median was 0, the 75th percentile was 1, and the 95th percentile was 18.
Therefore a generic mitochondrial annotation was not enough to justify a large
positive count.

I read only the `151 TH Prkcd Grin2c Glut` row groups from the 8 GB parquet
with a `group_name == "151 TH Prkcd Grin2c Glut"` filter, yielding 28,891,566
rows: 1,674 targets x 17,259 measured genes.  I then checked
`pvals_adj < 0.05` counts and leading focal-cell genes for each
mechanistically relevant training perturbation.

Observed focal counts in the closest mitochondrial and organelle neighborhoods:

| training target | `n_degs` in `151` | expression-pattern evidence | use for `Dnm1l` |
|---|---:|---|---|
| `Mff` | 0 | No focal gene passed FDR 0.05.  The Distributed Agents Mff finding also reported no FDR<0.10 downstream response in any recovered neuronal group and explicit absence of the Opa1 ATF4-like module. | Most direct represented outer-membrane fission analog, because MFF recruits DRP1.  Its null profile argues that partial loss of one recruitment receptor is buffered at the nuclear-RNA level. |
| `Opa1` | 37 | Focal up-regulation of the ATF4/ISR-like amino-acid program, led by `Asns`, `Mars1`, `Chac1`, `Ddit3`, `Cars`, `Mthfd2`, `Slc7a5`, plus down-regulation of the `Opa1` transcript. | Positive mitochondrial-dynamics benchmark.  It shows this cell type and assay can detect mitochondrial stress, but OPA1 is an inner-membrane fusion/cristae GTPase and is not a same-complex phenocopy of DRP1 loss. |
| `Yme1l1` | 0 | No focal FDR genes and no shared FDR-level Opa1 ISR genes in the corpus. | OPA1-processing inner-membrane protease; a strong counterexample to "OPA1-related" or mitochondrial-protease labels being sufficient for a broad response. |
| `Rhot1` | 0 | No focal FDR genes; corpus reports no common nuclear program across Miro/TRAK and kinesin transport genes. | Mitochondrial positioning and turnover-adjacent, but flat.  This bounds the expectation that local mitochondrial distribution defects need to become soma-detectable RNA changes. |
| `Atg5`, `Atg16l1` | 0, 0 | No focal FDR genes.  Other basal mitophagy/autophagy comparators were also tiny: `Sqstm1` 1, `Vps41` 0, `Map1lc3a` 1. | DNM1L-mediated fission feeds mitochondrial quality control, but training autophagy perturbations did not create a Rab7-like stress program in this cell type. |
| `Dnm1` | 1 | The sole FDR gene was `Dnm1` itself. | Dynamin-family paralog but vesicle-endocytosis rather than organelle fission; useful mainly as a reminder that the focal endpoint often records only a self-transcript after perturbing a trafficking GTPase. |
| `Rab7` | 501 | Broad late-endosomal/lysosomal, V-ATPase, stress, and sterol response led by `Atp6v1b2`, `Ptgds`, `Dpp7`, `Scpep1`, `Dusp1`, `Insig1`, and `Atp6v0b`. | A strong organelle-stress upper comparator, not a direct Dnm1l analog; it implies that the assay can report endolysosomal failure when it is severe. |
| `Dctn1` | 75 | SREBF2-like sterol/lipid response led by `Insig1`, `Msmo1`, `Dctn1`, `Hmgcs1`, `Cyp51`, and `Hmgcr`. | Retrograde organelle-transport counterexample: related to axonal logistics but a sterol-feedback state rather than a fission state. |
| `Nrf1` | 138 | A broad nuclear transcription-factor response, not a selective mitochondrial-fission program. | Too indirect and transcription-factor-like to set the Dnm1l magnitude. |

Additional represented mitochondrial genes around OXPHOS, proteases, and
cristae were mostly zero or singletons in the same focal endpoint: `Aco2`,
`Afg3l2`, `Agk`, `Clpp`, `Clpx`, `Coa8`, `Cox11`, `Cox4i1`, `Dnajc19`, `Gfm2`,
`Lonp1`, `Micos13`, `Micu1`, `Ndufs4`, `Ndufv1`, `Ppargc1a`, `Timmdc1`,
`Uqcrb`, `Uqcrh`, and `Yme1l1` were all 0; `Chchd2`, `Dap3`, `Isca2`,
`Ndufa4`, `Ndufs2`, `Ndufs8`, `Park7`, `Sdha`, `Slc25a46`, `Sod2`, `Sucla2`,
`Tomm40`, and `Uqcrq` were all 1.  That made `Opa1` the clear local
mitochondrial-stress exception rather than the expected count for every
important mitochondrial gene.

## Dnm1l-specific biological reasoning

External biology pushes `Dnm1l` upward relative to `Mff`.  DRP1/DNM1L is the
central cytosolic dynamin-family GTPase that constricts mitochondria and
peroxisomes; MFF, FIS1, MiD49/MIEF2, and MiD51/MIEF1 are recruiters or
receptors on the organelle surface.  Mff knockdown releases DRP1 from the outer
mitochondrial membrane and elongates mitochondria (Otera et al. 2010), but
several receptors can recruit DRP1, including MiD49 and MiD51 acting
independently of Mff and Fis1 (Loson et al. 2013; Palmer et al. 2013).  A
`Dnm1l` knockout removes the shared GTPase step downstream of these adaptors,
so it should be harder to buffer than the `Mff` perturbation that had 0 DEGs.

At the same time, the experiment is an acute, mosaic, partial postnatal CRISPR
assay.  Severe full-loss references are not direct effect-size estimates here:
complete mouse Drp1 loss is embryonic lethal and brain-specific ablation
disrupts cerebellar/Purkinje development (Wakabayashi et al. 2009), whereas
the supplied data measure surviving juvenile NeuN-enriched nuclei after sparse
AAV editing.  The focal training profiles show that many mitochondrial and
organelle-transport insults stay below FDR even when their protein products
have essential local functions.  Itoh et al. 2019 further showed that a
brain-specific DNM1L isoform regulates postsynaptic endocytosis and dendrite
formation independently of mitochondrial division, which supports neuronal
relevance but points to a synaptic/structural phenotype that may not yield many
bulk nuclear DEGs.

The run-local comparison also discouraged promoting `Dnm1l` into a Rab7- or
Dctn1-sized response.  `Mff`, `Yme1l1`, `Rhot1`, `Atg5`, and `Atg16l1` had no
significant focal features, and `Dnm1`/`Park7` had only a single feature each.
`Opa1` shared only a small ATF4/stress subset with the broad `Rab7` state
within the inspected cohort, while its direct OPA1-processing and fission
neighbors were flat in the Distributed Agents corpus.

## Prediction

I predict a real but very narrow focal response for `Dnm1l`: likely the
`Dnm1l` self-transcript plus at most one or two secondary mitochondrial or
postsynaptic stress transcripts.  That is above the direct `Mff` receptor null
because DRP1 is the enzymatic fission node, but far below `Opa1` because the
training set repeatedly shows that postnatal neuronal nuclear RNA does not
mirror every mitochondrial-dynamics or quality-control defect.

Point prediction: `Dnm1l -> 2` DEGs.

## Limits

The strongest limitation is that the closest same-complex molecules were not
all observed as training targets: `Fis1`, `Mief1/MiD51`, `Mief2/MiD49`,
`Mfn1`, `Mfn2`, `Oma1`, `Pink1`, and `Prkn` were absent from the focal training
count table.  `Mff` is a real DRP1 receptor but not equivalent to deleting
DRP1 itself.  The prediction is also blind to editing efficiency, frameshift
rate, protein half-life, mitochondrial morphology, peroxisomal fission, axonal
transport, survival loss, and transient responses before the 3-4 week harvest.
For those reasons the positive/zero call is more secure than the exact integer.
