# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question interpreted

The requested endpoint is the held-out value of `n_degs` for each perturbation in
`075_Ffar1.csv`: the number of measured genes in `151 TH Prkcd Grin2c Glut`
nuclei with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` after
sparse postnatal AAV-CRISPR loss of the target gene. I treated the supplied
training count CSV as the authoritative endpoint for non-held-out targets in
this cell group and the Parquet as the authoritative expression-signature matrix
for those same non-held-out perturbations. The held-out `Ffar1` profile itself
is absent from both inputs.

One ambiguity I resolved explicitly was that `n_degs` counts the significant
target transcript when the target is part of the measured-gene matrix; it is not
restricted to downstream genes. This matters because many weak GPCR and lipid
perturbations in this focal group have exactly one significant gene, usually the
target transcript itself.

## Sources used

- Differential-expression Parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Requested target manifest:
  `[local file: 075_Ffar1.csv]`.
- Distributed Agents same-experiment semantic corpus,
  release `perturbai-july-260713-sourceguard-1773-v1`. The release had no
  `Ffar1` Claim/Finding neighborhood, so I used its curated Plcb1, Grm5, and
  Prkca pathway contexts as same-assay evidence about basal GPCR/Gq/PLC/IP3/PKC
  signatures.
- PubMed literature on FFAR1/GPR40 mechanism and expression, especially Itoh et
  al. 2003, DOI `10.1038/nature01478`, PMID `12629551`; Usui et al. 2019, DOI
  `10.1038/s41598-019-52048-1`, PMID `31664108`; Petersen et al. 2023, DOI
  `10.1016/j.molmet.2023.101757`, PMID `37348738`; Dragano et al. 2023, DOI
  `10.1016/j.molmet.2023.101840`, PMID `38036170`; and the FFAR review by
  Kimura et al. 2019, DOI `10.1152/physrev.00041.2018`, PMID `31487233`.

## Dataset computations

I filtered the Parquet to `group_name == '151 TH Prkcd Grin2c Glut'` and used
the training target list as the eligible perturbation universe. That slice
contains 1,674 non-held-out perturbations and 17,259 measured genes. The
training endpoint is highly zero-inflated in this focal group: 1,205 of 1,674
targets have `n_degs = 0`, 363 have 1-9, 63 have 10-99, and 43 have at least
100.

For the held-out target I checked two things directly in the Parquet:

1. `Ffar1` was not a measured `names` feature in `151 TH Prkcd Grin2c Glut`.
   In contrast, `Ffar2`, `Ffar3`, and `Ffar4` did appear in the focal feature
   set. `Ffar1` appeared only in `191 MB P MY GABA` and `308 CB GABA`, making a
   cell-intrinsic Ffar1 RNA footprint in the requested thalamic class less
   plausible.
2. I computed endpoint counts and nearest observed profiles for mechanistic
   neighbors. The query was a direct count of focal rows with `pvals_adj < 0.05`
   by `gene_target`, followed by a runtime neighbor scan over signed
   `logfoldchanges` for Plcb1, Itpr1, Prkca, Prkcg, Gnas, Grm1, and Grm5.
   Those anchors were chosen before seeing the held-out answer because FFAR1 is
   a medium/long-chain fatty-acid GPCR coupled mainly to Gq/G11, PLC/IP3, ER
   calcium release, PKC, and in some contexts Gq-dependent cAMP signaling.

Key observed counts in the focal group were:

| Training target | `n_degs` | Why it was considered |
|---|---:|---|
| `Plcb1` | 0 | proximal Gq effector for IP3/DAG production |
| `Itpr1` | 0 | IP3 receptor and ER calcium-release effector |
| `Prkca` | 0 | conventional PKC effector of DAG/calcium signaling |
| `Prkcg` | 1 | conventional PKC paralog; only significant gene was `Prkcg` |
| `Grm1` | 1 | Gq-linked class-C GPCR; only significant gene was `Grm1` |
| `Grm5` | 0 | Gq-linked class-C GPCR and strong neuronal GPCR counterexample |
| `Gnas` | 0 | G-protein/cAMP counterexample |
| `Adcy1`, `Adcy3`, `Adcy5` | 0, 0, 0 | adenylyl cyclase/cAMP counterexamples |
| `Pde4b`, `Pde10a` | 0, 0 | cAMP phosphodiesterase counterexamples |
| `Cnr1`, `S1pr2` | 1, 0 | lipid-activated neuronal GPCR counterexamples |
| `Acsl4`, `Abhd12`, `Cpt1c` | 1, 1, 1 | fatty-acid/lipid metabolism perturbations; each singleton was self-target |
| `Ppara`, `Ppard`, `Pparg`, `Ppargc1a`, `Rxra` | 0, 0, 0, 0, 0 | fatty-acid-responsive transcription/metabolism controls |

The weak nonzero analogs were not evidence for a broader shared program. For
example, `Prkcg`, `Grm1`, `Acsl4`, `Abhd12`, and `Cpt1c` each had exactly one
FDR-significant focal-group feature, and that feature was the target transcript
for all five. `Cnr1` had a singleton `Srcap` hit. The measured focal profiles of
the Gq/PLC anchors were nearest to other zero or weak targets rather than to
broad responders; `Grm5`'s closest whole-profile neighbors included `Tnrc6a`,
`Mest`, `Glce`, `Tfg`, `Il1r1`, and `Flnb`, all with `n_degs = 0`, and
`Prkcg`'s nearest profiles were similarly dominated by 0- or 1-DEG targets.

The Distributed Agents corpus supported the same interpretation in the packaged semantic
layer over this experiment. Its high-confidence Plcb1 and Prkca findings and
the Grm5 context record that represented mGluR, PLC/IP3, PKC/CaMK, and nearby
postsynaptic perturbations were flat or nonconvergent at the basal neuronal RNA
level. The moderate GPCR/Gq/PLC Claim likewise states that represented
neuromodulatory GPCRs and proximal second-messenger effectors generally did not
form a shared basal nuclear-transcriptome module.

## Target-specific reasoning

### Ffar1

`Ffar1`, also known as `Gpr40`, encodes a GPCR activated by medium- and
long-chain free fatty acids. Itoh et al. showed that GPR40 is a long-chain fatty
acid receptor that amplifies glucose-stimulated insulin secretion in pancreatic
beta cells. Mechanistically, FFAR1 is mainly Gq/G11-linked: Usui et al.
connected beta-cell GPR40 activation to IP3R1/STIM1/Orai1 calcium entry, and
Petersen et al. showed in enteroendocrine models that FFAR1-induced cAMP
production also depended on Gq and ADCY2 rather than direct Gs coupling.
External work therefore made `Plcb1`, `Itpr1`, `Prkca`/`Prkcg`, and cAMP
effectors the most relevant measured same-assay neighbors; it did not nominate
a nuclear-splicing, proteasome, ubiquitin, or mitochondrial module like the
perturbations that dominate the high end of the count distribution.

The dataset-local evidence strongly favored no detectable response. First, the
target transcript itself was absent from the 17,259 measured genes in the focal
class, whereas multiple other low FFAR paralog transcripts passed the feature
filter there. That does not prove zero protein, because GPCR transcripts can be
low, but it makes a strong thalamic cell-autonomous knockout footprint unlikely
under a sparse postnatal design. Second, the represented pathway nodes were
quiet in exactly this endpoint: `Plcb1 = 0`, `Itpr1 = 0`, `Prkca = 0`,
`Prkcg = 1`, `Grm1 = 1`, `Grm5 = 0`, and `Gnas = 0`. The singletons mostly
reflected self-transcript hits that `Ffar1` cannot contribute in this focal
matrix because `Ffar1` is not a measured feature. Third, same-assay corpus
Claims indicated that even canonical neuronal Gq/PLC/IP3/PKC perturbations
failed to create durable basal snRNA modules across the represented receptors
and effectors.

The main counterweight is that Ffar1 biology is not pancreas-exclusive.
Reviews and direct studies report GPR40/FFAR1 expression and function in CNS
neurons, and Dragano et al. found hypothalamic Ffar1 to be functional in POMC
neurons. Those observations keep a thalamic neuronal effect biologically
possible. They are still an extrapolation to this task: hypothalamic POMC
neurons, pharmacologic FFAR1 agonism, and viral shRNA in adult metabolic
contexts are not the juvenile, sparse, Cas9 loss-of-function perturbation and
focal thalamic glutamatergic readout here.

Putting those pieces together, I predicted `Ffar1` to remain at the dominant
zero endpoint class rather than assign a one-gene self-hit-like count.

## Prediction limits

- No Ffar1-specific held-out expression profile or DEG count was available, and
  the Distributed Agents corpus release had no direct `Ffar1` Finding or Claim.
- Direct FFAR paralog knockouts (`Ffar2`, `Ffar3`, `Ffar4`) were also absent
  from the training target set, so the closest same-family perturbations could
  not be compared.
- Gq alpha subunits `Gnaq` and `Gna11` and beta-arrestins were not present in
  the focal training-count file, making `Plcb1`, `Itpr1`, `Prkca`, and GPCR
  receptor perturbations the available proxies.
- Absence of `Ffar1` from the focal feature set is a strong expression prior
  but not a direct protein measurement. Low-level receptor expression could
  still be physiologically meaningful and missed by nuclear RNA capture.
- The endpoint is a basal 3-4-week snRNA readout. FFAR1 effects on ligand-evoked
  calcium, CREB/ERK phosphorylation, secretion, or circuit physiology could be
  real without creating any FDR-level steady-state mRNA change.

