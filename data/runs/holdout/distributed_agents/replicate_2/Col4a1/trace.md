# Prediction trace

## Question and resolved ambiguities

The requested held-out perturbation list contains one target:

| target_name |
| --- |
| Col4a1 |

For `Col4a1`, I interpreted `n_degs` exactly as the number of measured genes in
`151 TH Prkcd Grin2c Glut` cells with Wilcoxon `pvals_adj < 0.05` after
acute AAV/CRISPR loss of the target. The count is an endpoint in this specific
NeuN-enriched, P16 to P37/P44, mosaic postmitotic assay, not a general estimate
of the importance of collagen IV in the brain or vasculature.

`Col4a1` and other held-out targets are absent from both inputs by design, so I
did not use a direct `Col4a1` signature. I treated detectable up-regulation of
`Col4a1` in another perturbation as evidence that the transcript is measurable
in this cell group, but not as evidence that perturbing `Col4a1` itself must
phenocopy the upstream perturbation.

## Sources used

- `[local file: 045_Col4a1.csv]`
  for the exact held-out target and order.
- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for observed training endpoint counts in the focal cell group.
- `[local file: training_de_all_cell_groups.parquet]`
  for focal-cell differential-expression rows in candidate analog perturbations.
- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`,
  especially target contexts and claims for `Bmal1`, `Nr1d1`, `Fbn1`, and
  `Adamts17`.
- Distributed Agents runtime profile analysis over selected focal-cell signatures,
  mainly to verify response breadth for `Bmal1`, `Nr1d1`, `Fbn1`, `Adamts17`,
  and `Hnrnpu`.
- NCBI PubMed literature for collagen IV biology and `COL4A1/COL4A2` brain
  disease.

## Computational checks

1. I loaded the requested-target manifest and confirmed that the only row is
   `Col4a1`.

2. I summarized the focal-cell training counts. The endpoint is strongly
   zero-inflated: among 1,674 training perturbations, 1,205 had zero DEGs,
   the median was 0, the 75th percentile was 1, the 95th percentile was 18,
   and only the far tail reached hundreds to thousands of DEGs. This makes a
   null prediction a common, calibrated outcome in this assay.

3. I queried the training-count CSV for matrix, collagen, integrin, and
   TGF/BMP genes. No `Col4a1` or `Col4a2` perturbation is present in the
   training set, so there is no direct collagen IV alpha1/alpha2 perturbation
   phenocopy. The represented nearby extracellular or receptor genes were
   mostly flat in `151 TH Prkcd Grin2c Glut`:

| training perturbation | focal `n_degs` | interpretation |
| --- | ---: | --- |
| Fbn1 | 0 | structural ECM / latent TGF-beta matrix analog; flat |
| Adamts17 | 0 | fibrillin/TGF-BMP matrix regulator; flat |
| Aebp1 | 0 | ECM/collagen-associated disease gene; flat |
| Itgb1 | 0 | major integrin beta chain and collagen/ECM receptor component; flat |
| Itga2, Itga4, Itga6, Itga7, Itga8, Itga9, Itga2b, Itgb2 | 0 each | integrin counterexamples; flat |
| Bmpr1a, Bmpr2, Tgfbr1, Tgfbr2, Smad3, Smad4, Smad6 | 0 each | basal receptor-SMAD pathway perturbations; flat |
| Smad2 | 1 | one isolated DEG, not a broad TGF-beta program |

4. I scanned the parquet only for `group_name == "151 TH Prkcd Grin2c Glut"`
   and the nominated analog targets, retaining `logfoldchanges`, `pvals_adj`,
   and matched cell counts. The key marker rows were:

| training perturbation | focal `n_degs` | `Col4a1` log2FC/q | `Col4a2` log2FC/q | `Pdgfa` log2FC/q |
| --- | ---: | ---: | ---: | ---: |
| Bmal1 | 103 | 0.593 / 0.0225 | 0.574 / 0.00406 | 0.965 / 1.37e-09 |
| Nr1d1 | 116 | 0.649 / 5.31e-06 | 0.456 / 0.00109 | 1.048 / 1.35e-16 |
| Hnrnpu | 733 | 1.216 / 2.54e-18 | 0.700 / 4.95e-07 | 0.370 / 0.0541 |
| Ppm1g | 3 | -0.539 / 0.0486 | -0.614 / 0.00539 | 0.0126 / 1 |
| Fbn1 | 0 | -0.0718 / 1 | -0.0280 / 1 | 0.0091 / 1 |
| Adamts17 | 0 | -0.257 / 1 | -0.115 / 1 | -0.127 / 1 |
| Itgb1 | 0 | -0.169 / 1 | -0.158 / 1 | 0.0866 / 1 |
| Bmpr1a | 0 | -0.139 / 1 | -0.102 / 1 | 0.104 / 1 |
| Smad4 | 0 | 0.125 / 1 | 0.129 / 1 | -0.201 / 1 |
| Tgfbr2 | 0 | 0.002 / 1 | -0.200 / 1 | 0.073 / 1 |

5. I used Distributed Agents Runtime `profile_compare` on `Bmal1`, `Nr1d1`, `Fbn1`,
   `Adamts17`, and `Hnrnpu` in the same focal cell group. It independently
   recovered the same response-breadth categories: `Bmal1`, `Nr1d1`, and
   `Hnrnpu` each had at least 50 significant genes, while `Fbn1` and
   `Adamts17` had no significant genes.

## Distributed Agents same-experiment evidence

The internal corpus had no target-centered `Col4a1` card, but it did contain
same-assay claims that explain how `Col4a1/Col4a2` appear in the training
surface.

- The corpus claim
  `Loss of Nr1d1 or Bmal1 can drive a shared Pdgfa/Col4a1/Col4a2-positive
  extracellular-remodeling transcriptional response in 151 TH Prkcd Grin2c
  Glut neurons` identifies `Col4a1` and `Col4a2` as downstream markers of
  clock perturbations in the focal cells. The direct rows confirm this:
  `Bmal1` has 103 DEGs and `Nr1d1` has 116 DEGs, with significant positive
  `Col4a1`, `Col4a2`, and `Pdgfa`.

- The `Nr1d1` target context reports that the `Nr1d1` response is an
  excitability, synaptic, metabolic, and secreted-matrix state. `Bmal1` was
  the strongest data-driven positive neighbor of `Nr1d1`, with 63 same-sign
  shared FDR hits, but the corpus also emphasizes that represented clock and
  REV-ERB/ROR relatives were not interchangeable. I therefore used `Bmal1` and
  `Nr1d1` as evidence that collagen IV transcripts are recruitable by a broad
  thalamic state, not as direct mechanistic analogs for a collagen IV knockout.

- `Hnrnpu` had 733 DEGs and strongly up-regulated `Col4a1/Col4a2`; the corpus
  claim for `Hnrnpu` and `Ppm1g` says that `Col4a1/Col4a2` recur across those
  contexts only as a restricted submodule, not as a strong shared global
  phenocluster. Consistent with that, `Ppm1g` had exactly three DEGs in the
  focal table, two of them `Col4a1` and `Col4a2`, and in the opposite
  direction from `Bmal1` and `Nr1d1`.

- The `Fbn1` and `Adamts17` contexts are the more relevant negative
  counterexamples. The corpus claim states that `Fbn1` and `Adamts17`
  perturbations do not engage a detectable extracellular-matrix-linked
  TGF-beta/BMP-SMAD module in postmitotic neurons. `Fbn1` was described as
  nearly globally buffered across assayed neuronal groups, with only one
  downstream FDR<0.10 row across 371,796 non-self tests, while `Adamts17`
  produced a pan-neuronal null surface with no non-self FDR<0.10 genes in any
  of 23 neuronal groups.

## External biological rationale

`COL4A1` and `COL4A2` encode collagen IV alpha chains that assemble mainly as
an alpha1-alpha1-alpha2(IV) heterotrimer in basement membranes. This is the
ancestral, broadly distributed collagen IV network and is distinct from a
short-lived neuron-intrinsic transcription factor complex (Kuo, Labelle-Dumais
and Gould 2012, DOI 10.1093/hmg/dds346; Favor et al. 2006, DOI
10.1534/genetics.106.064733).

Published mouse and human `COL4A1` brain phenotypes are dominated by basement
membrane and cerebrovascular pathology: `Col4a1` mutations can cause focal
vascular basement-membrane disruption, porencephaly, small-vessel disease, and
hemorrhage (Gould et al. 2005, DOI 10.1126/science.1109418; Gould et al.
2006, DOI 10.1056/NEJMoa053727). The severe alleles in much of this literature
are dominant collagen-domain missense alleles that inhibit collagen IV
secretion or cause intracellular collagen retention in vascular endothelial
cells and pericytes, while the requested experiment is a sparse CRISPR
loss-of-function perturbation in NeuN+ postmitotic nuclei. That mismatch
matters: this assay under-samples endothelial cells, pericytes, astrocytes,
smooth muscle cells, and other matrix-producing compartments that would be
expected to sense basement-membrane collagen defects most directly.

`Col4a1` mutant mice can show elevated TGF-beta signaling as part of central
nervous system vascular pathology (Branyan et al. 2022, DOI
10.1016/j.matbio.2022.11.007). However, the same Perturb-seq training data
tested many basal BMP/TGF receptor and SMAD nodes and found zero or singleton
responses in `151 TH Prkcd Grin2c Glut`, so I did not extrapolate a vascular
TGF-beta phenotype into a broad neuron-autonomous `Col4a1` RNA signature.

## Target-specific prediction

### Col4a1

The best direct structural analogs in the training set point to a null call.
`Fbn1`, `Adamts17`, `Aebp1`, `Itgb1`, additional integrins, and basal
TGF/BMP-SMAD receptors or transducers all had 0 DEGs in the focal group except
for `Smad2`, which had one isolated DEG. These perturbations are imperfect
because none is the `Col4a1`/`Col4a2` heterotrimer itself, but they test the
same broad class of extracellular-matrix and receptor-SMAD biology in the
same assay and show that such genes are usually buffered in postmitotic
NeuN-enriched neurons.

The positive `Col4a1/Col4a2` rows in `Bmal1`, `Nr1d1`, and `Hnrnpu` argue that
`Col4a1` is not an unmeasurable gene in this cell group. They do not argue that
loss of the collagen chain will induce a 100 to 700 gene upstream clock or
RNA-processing signature. `Ppm1g` is a useful boundary: it moved `Col4a1` and
`Col4a2` themselves at FDR<0.05 but yielded only three total DEGs, showing
that collagen IV transcript changes can appear as a tiny downstream submodule
without expanding into a matrix-remodeling state.

Mechanistically, a sparse CRISPR lesion in a secreted basement-membrane
component should be buffered more like `Fbn1` or `Adamts17` than like the
clock factors that induce `Col4a1` transcription. Because the disease biology
of `COL4A1` is heavily vascular and extracellular, because the collagen IV
alpha2 obligate-chain comparator was not in the training set, and because the
dominant human/mouse missense mechanism is not reproduced by a partial
postnatal neuronal loss-of-function perturbation, I predict no FDR-significant
genes in the held-out `Col4a1` row.

Predicted `n_degs`: 0.

## Limits

- The closest missing comparator is `Col4a2`; no direct alpha2(IV) loss
  signature was available in the training CSV or focal parquet.
- The experiment measures nuclear RNA only. It cannot directly detect collagen
  IV secretion, basement-membrane assembly, extracellular protein stability,
  vascular permeability, or non-cell-autonomous endothelial/pericyte responses.
- Most published `COL4A1/COL4A2` mechanisms involve dominant missense alleles,
  developmental vasculature, or non-neuronal matrix-producing cells. Mapping
  those data onto sparse acute CRISPR editing in postmitotic thalamic neurons
  is extrapolation.
- The expected response, if any, is small; distinguishing exactly 0 from one or
  two DEGs is within the noise of this Wilcoxon/FDR endpoint. The point
  prediction uses 0 because the nearest same-assay ECM and receptor-SMAD
  perturbations were flat and because the nonzero collagen IV observations in
  training are downstream markers of other broad perturbation states.
