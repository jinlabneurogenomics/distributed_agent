# Pomp DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

I interpreted the task as a point prediction for the held-out perturbation list in
`181_Pomp.csv`. The manifest contained exactly one target:

```text
Pomp
```

The endpoint is `n_degs`, the number of measured transcripts with
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` in the focal
`151 TH Prkcd Grin2c Glut` group. I treated the count as assay-specific: it
reflects this sparse AAV CRISPR loss-of-function experiment, 3-4 week timing,
recovered NeuN+ nuclei, and the single-nucleus Wilcoxon test. I did not treat
the count as a direct estimate of knockout efficiency or cell viability.

I also resolved two important ambiguities explicitly:

- The held-out `Pomp` perturbation itself is absent from both input files, so no
  row for `Pomp` as `gene_target` was used.
- A perturbation with no significant genes in the supplied count CSV is still
  informative in this assay. It is not automatic evidence that the gene is
  biologically irrelevant; many stress-sensor and ubiquitin-pathway knockouts
  are silent under basal P16-to-P37/44 neuronal conditions.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for observed training `n_degs` in the focal group.
- `[local file: training_de_all_cell_groups.parquet]`
  for same-experiment signed log2 fold-change profiles.
- `[local file: 181_Pomp.csv]`
  for the requested target.
- Distributed Agents corpus MCP, release
  `perturbai-july-260713-sourceguard-1773-v1`. The corpus had no direct
  `Pomp` target record, but had detailed Psmb4, Psmc1, Nfe2l1, and Vcp
  same-experiment interpretations that I used to separate direct proteasome
  injury from generic proteostasis stress.
- PubMed through NCBI E-utilities for public POMP/proteasome-assembly
  literature.

## Computation over the training data

First I enumerated focal-group counts for proteasome and proteostasis
perturbations represented in the non-held-out set. Direct proteasome-core
coverage was sparse but very informative:

| training perturbation | focal `n_degs` | interpretation for POMP |
| --- | ---: | --- |
| `Psmb4` | 742 | constitutive 20S beta-7 core subunit; the best assayed analog for loss of 20S core biogenesis |
| `Psmc1` | 430 | 19S AAA-ATPase subunit; orthogonal core 26S proteasome damage |
| `Nfe2l1` | 0 | proteasome bounce-back transcription factor NRF1; loss alone did not phenocopy core damage at FDR 0.05 |
| `Nfe2l2` | 0 | NRF2 oxidative-stress paralog/pathway relative; a counterexample against assigning a large response to any CNC-bZIP stress gene |
| `Vcp` | 2 | p97 segregase needed for ERAD and NFE2L1 processing, but nearly flat in the same endpoint |
| `Usp48` | 10 | deubiquitinase / proteostasis-side node; weak |
| `Hspa5` | 5 | ER BiP chaperone; weak ER-stress comparator |
| `Hspa8` | 9 | cytosolic Hsc70 chaperone; weak |
| `Ube2e2` | 0 | ubiquitin E2; flat |
| `Ube3a` | 0 | ubiquitin E3; flat |

Across all 1,674 non-held-out perturbations in the focal count CSV, 1,205 had
zero DEGs and only 59 had at least 50. `Psmb4` and `Psmc1` are therefore in a
small high-response tail rather than near the training prior mean.

I then used `mcp__distributed_agents_runtime.profile_compare` on the log2 fold-change
profiles for the ten proteostasis candidates above, filtered to
`group_name == "151 TH Prkcd Grin2c Glut"`, with `gene_target` as the profiled
entity, `names` as the feature, `logfoldchanges` as the signed value, and
`pvals_adj < 0.05` as the significance definition. That recovered exactly the
training endpoint counts: 742 significant features for `Psmb4`, 430 for
`Psmc1`, 10 for `Usp48`, 9 for `Hspa8`, 5 for `Hspa5`, 2 for `Vcp`, and 0 for
`Nfe2l1`, `Nfe2l2`, `Ube2e2`, and `Ube3a`.

Within that hand-built proteostasis set, `Psmb4` and `Psmc1` were the only
high-count nodes and they were each other's nearest direct proteasome neighbor:

- whole-profile Pearson between `Psmb4` and `Psmc1`: 0.611
- whole-profile cosine: 0.671
- shared top-500 up features: 163
- shared top-500 down features: 148

I also searched `Psmb4` and `Psmc1` against all 1,674 eligible training
perturbations. Whole-profile correlations produced high-ranking but
non-mechanistic neighbors such as `Ndufs4`, `Alx1`, `Npy2r`, and `Adam22`,
several of which have 0 or 1 focal DEG. Positive-tail searches repeatedly
recovered `Vcp` near both proteasome anchors, but `Vcp` itself had only 2
DEGs. I therefore used the all-target search as a specificity check rather than
as a count-averaging rule: same-direction tail overlap can mark a sliver of a
stress state without implying similar response breadth.

## Internal same-experiment corpus evidence

The Distributed Agents corpus had no direct `Pomp` entry, so the POMP prediction is an
extrapolation. The most relevant corpus records were for the observed
proteasome perturbations:

- `Psmb4` findings reported a broad postmitotic proteasome-insufficiency state,
  with 20S/19S/PA200 proteasome bounce-back, ISR/heat-shock/redox genes
  including `Ddit3`, `Ppp1r15a`, `Hspa1a/Hspa1b`, `Hspb1`, `Hmox1`, `Mt1`,
  and `Mt2`, a p53/apoptosis-like module, lysosome/autophagy compensation, and
  repression of synaptic/neuronal-activity transcripts.
- `Psmc1` findings independently described the same class of response:
  proteasome and ubiquitin bounce-back, endolysosomal/autophagy genes,
  HSP/ISR genes, p53/redox arms, and down-regulation of mature neuronal
  function genes.
- A high-confidence `Psmb4` finding noted that `Psmc1` was the strongest
  direct positive neighbor of `Psmb4`; a high-confidence `Psmc1` finding made
  the reciprocal point, calling `Psmb4` the single strong positive
  same-complex neighbor.
- The `Psmb4` and `Psmc1` contexts also cautioned that stress regulators and
  accessory proteostasis genes such as `Nfe2l1`, `Nfe2l2`, `Vcp`, `Atf6`,
  `Hspa5`, `Hspa8`, `Ube3a`, `Ube2e2`, `Usp48`, and `Sqstm1` did not
  reproduce the core proteasome program under basal perturbation.
- `Nfe2l1` was especially important as a counterexample: the same corpus
  states that basal `Nfe2l1` loss did not recover the canonical proteasome
  bounce-back or aggrephagy program, even though NFE2L1 is the expected
  regulator once proteasomes are stressed.
- `Vcp` had a sparse, cell-restricted response and did not itself induce the
  canonical UPR, heat-shock, proteasome bounce-back, ERAD, p62/LC3, lysosomal,
  or TDP-43 transcripts at FDR level in the measured groups.

This corpus evidence made the zero/nonzero decision hinge on POMP's biochemical
position. If POMP were merely an upstream stress sensor like `Nfe2l1`, `Vcp`,
or `Hspa5`, I would have predicted a near-zero count. It is not: it is an
obligate assembly chaperone for the 20S core particle.

## External biology used for POMP

POMP, also called proteassemblin or hUmp1, is not a structural 20S alpha/beta or
19S ATPase subunit. It transiently associates with mammalian preproteasomes and
is required for normal 20S proteasome assembly:

- Griffin et al. identified mammalian proteassemblin as a Ump1 homolog present
  in preproteasomes rather than mature 20S proteasomes, supporting a role in
  normal mammalian proteasome assembly (2000,
  DOI: `10.1006/mcbr.2000.0213`, PMID: `10891394`).
- Fricke, Heink, Steffen, Kloetzel, and Kruger showed that POMP binds alpha
  rings, recruits beta subunits stepwise, and mediates assembly of mammalian
  20S precursor complexes at the ER (2007, DOI: `10.1038/sj.embor.7401091`,
  PMID: `17948026`).
- Dahlqvist, Torma, Badhai, and Dahl found that siRNA silencing of POMP in
  keratinocyte models decreased proteasome subunits and, with prolonged
  silencing, induced CHOP/ER-stress consistent with proteasome insufficiency
  (2012, DOI: `10.1371/journal.pone.0029471`, PMID: `22235297`).
- Human genetics places POMP on the same proteasome-insufficiency disease axis
  as core proteasome subunits: Brehm et al. reported additive loss-of-function
  variants affecting `PSMA3`, `PSMB4`, `PSMB8`, `PSMB9`, and `POMP` in
  proteasome-associated autoinflammatory syndrome with impaired assembly and
  increased type I interferon (2015, DOI: `10.1172/JCI81260`,
  PMID: `26524591`), and Poli et al. described dominant-negative POMP
  truncations that perturb proteasome assembly in an immune dysregulatory
  syndrome (2018, DOI: `10.1016/j.ajhg.2018.04.010`, PMID: `29805043`).

## Target-specific prediction

### `Pomp`

I predict `Pomp` will be clearly nonzero and in the same high-response regime as
direct proteasome damage, not in the 0-10 range seen for isolated stress
regulators.

The closest observed analog is `Psmb4` with 742 focal DEGs. Both POMP and PSMB4
are tied to 20S core biogenesis: POMP helps assemble beta subunits onto alpha
rings, while PSMB4/beta-7 completes the beta ring and the mature core. The other
observed structural anchor, `Psmc1`, gives 430 focal DEGs and validates that
the 151 thalamic group responds strongly to loss of either side of the 26S
proteasome. The `Psmb4`/`Psmc1` expression-pattern agreement in the same
profile comparison, with a 0.611 whole-profile Pearson and 0.326/0.296 overlap
of the top 500 induced/repressed features, supports treating them as the right
calibration points for an assembly factor that should lower proteasome capacity.

The main counterexamples are `Nfe2l1` at 0 DEGs, `Nfe2l2` at 0, `Vcp` at 2,
`Hspa5` at 5, `Hspa8` at 9, and `Usp48` at 10. I used these to avoid a generic
"proteostasis gene => many DEGs" rule. They are poor positive analogs because
they are sensors, adaptive effectors, or branch factors; under basal conditions
their deletion did not itself create the severe 20S/26S proteotoxic lesion that
`Psmb4` and `Psmc1` created. POMP sits upstream of proteasome-core production,
so its loss should be closer to `Psmb4` than to `Nfe2l1`.

I placed the count near the `Psmb4`/`Psmc1` midpoint. The
downward adjustment from 742 reflects that POMP is a transient assembly
chaperone rather than a stoichiometric mature-core subunit: residual POMP
protein and pre-existing proteasomes may buffer a partial AAV CRISPR loss better
than direct targeting of a core subunit. The upward pressure relative to weak
counterexamples comes from the fact that every newly assembled 20S core needs
POMP, and a 3-4 week postnatal window should give edited neurons time to feel
loss of new proteasome assembly.

Point prediction: `560`.

## Limits

- `Pomp` was absent from the Distributed Agents target corpus and from the supplied
  parquet, so there is no observed POMP transcriptome in any cell type in these
  inputs. The prediction is extrapolated from same-experiment proteasome
  subunits plus external mechanism.
- Only two direct constitutive proteasome subunits, `Psmb4` and `Psmc1`, were
  represented as strong focal training analogs. The training set did not include
  a panel of `PSMA`, `PSMB`, `PSMC`, `PSMD`, or `PSMG` perturbations that would
  quantify where POMP sits within proteasome biogenesis.
- Mature neuronal proteasomes may be long-lived. The assay harvest at 3-4 weeks
  post-perturbation is probably long enough for an assembly defect to matter,
  but the exact half-life in the focal 151 TH neurons was not measured.
- snRNA-seq reports nuclear RNA in surviving NeuN+ nuclei. If POMP loss caused
  early dropout of the most severely edited cells, the recovered signature could
  undercount the biological severity; if residual POMP sufficed, the DEG count
  could fall toward the weak proteostasis comparators.
- Counts are thresholded at FDR 0.05 and are therefore sensitive to perturbation
  cell counts, guide performance, and variance. I used `Psmb4` and `Psmc1` for
  local calibration, but a difference of a few hundred DEGs within this
  high-response class should be read as uncertain.
