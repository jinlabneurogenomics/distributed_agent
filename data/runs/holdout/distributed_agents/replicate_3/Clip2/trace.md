# DEG-count prediction trace

## Question and resolved ambiguities

The requested held-out target list contains one mouse perturbation, `Clip2`, and
the requested endpoint is the integer `n_degs` in `151 TH Prkcd Grin2c Glut`:
the number of measured genes whose Benjamini-Hochberg-adjusted Wilcoxon
p-value is below 0.05 when the `Clip2` CRISPR perturbation is compared with its
matched non-targeting control.

I treated the count exactly as in the supplied training-count CSV:

- the self transcript is included if it passes FDR 0.05;
- the threshold is `pvals_adj < 0.05`, not the FDR 0.10 threshold used in some
  Distributed Agents report summaries;
- the perturbation is acute postnatal mosaic AAV-CRISPR loss of function in
  recovered NeuN-positive mouse nuclei, so germline phenotypes and
  morphologic cytoskeletal functions are priors rather than direct readouts;
- `151 TH Prkcd Grin2c Glut` is the thalamic glutamatergic focal cell group.

## Sources used

- Local input endpoint table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
  This gave the observed `n_degs` for 1,674 non-held-out targets in the focal
  class.
- Local input differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
  I used this both through the Distributed Agents runtime profile tools and directly
  for exact focal-cell significant rows for selected analogs.
- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`.
  `Clip2` itself has no selected-corpus finding, but the release has
  target-scoped reports for the relevant training perturbations `Dctn1`,
  `Dst`, `Map1b`, `Mapre2`, and `Tuba1a`.
- PerturbAI gene-annotation / analog-nomination store over the closed screen
  universe. `sets-for Clip2` placed `Clip2` in GO microtubule and plus-end
  annotations including `GO:0051010` microtubule plus-end binding,
  `GO:0031122` cytoplasmic microtubule organization, `GO:0035371`
  microtubule plus-end, `GO:0008017` microtubule binding, and the MSigDB
  hallmark set `MM3863` HALLMARK_MITOTIC_SPINDLE. The analog-nomination run
  found no exact paralog, exact complex, narrow pathway, or direct pinned
  interaction candidate in the 1,674-gene training universe; all available
  nominees were broad cytoskeleton or microtubule annotations.
- PubMed literature for CLIP2 / CLIP-115 biology:
  De Zeeuw et al. 1997, Neuron, DOI 10.1016/S0896-6273(00)80411-0,
  PMID 9427243; Hoogenraad et al. 2000, J Cell Sci,
  DOI 10.1242/jcs.113.12.2285, PMID 10825300; Akhmanova et al. 2001,
  Cell, DOI 10.1016/S0092-8674(01)00288-4, PMID 11290329; Hoogenraad
  et al. 2002, Nat Genet, DOI 10.1038/ng954, PMID 12195424; Stepanova
  et al. 2010, Curr Biol, DOI 10.1016/j.cub.2010.04.024, PMID 20471267;
  Vandeweyer et al. 2012, Am J Hum Genet, DOI 10.1016/j.ajhg.2012.04.020,
  PMID 22608712.

## Computation over the supplied data

The training endpoint distribution in the focal cell group is extremely
zero-heavy:

| class | training definition | count |
|---|---:|---:|
| none | `n_degs == 0` | 1205 |
| weak | `1 <= n_degs < 10` | 363 |
| medium | `10 <= n_degs < 100` | 63 |
| strong | `n_degs >= 100` | 43 |

I therefore used the curated analog search to choose biologically plausible
comparators, then inspected their actual signatures and counts rather than
assigning a generic cytoskeletal prior. The focal parquet has 17,259 measured
features for the main microtubule anchors. I pulled the exact FDR 0.05 rows
for broad `Clip2` comparators and also ran the Distributed Agents runtime signed-profile
comparison over 16 microtubule / MAP / kinesin / tubulin targets in the same
cell group. The runtime comparison used the full signed log-fold-change vector,
Pearson and cosine whole-profile views, and positive and negative top-500
feature-overlap views, retaining FDR counts as the activity signal.

Observed focal-cell counts for the useful training comparators were:

| training target | `n_degs` | focal-cell expression-pattern evidence |
|---|---:|---|
| `Dst` | 0 | broadest GO overlap with `Clip2`; no FDR 0.05 genes in the focal class; the Distributed Agents corpus reports no robust downstream response in any measured NeuN+ group |
| `Mapre2` | 1 | shared microtubule plus-end binding and plus-end localization; the only focal FDR 0.05 gene was `Mapre2` itself, log2FC -0.464, adjusted p 5.22e-4 |
| `Dctn1` | 75 | shared microtubule plus-end/cytoplasmic microtubule annotations through dynactin p150/Glued biology, but the focal signature was a sterol/SREBF program: `Insig1`, `Msmo1`, `Hmgcs1`, `Cyp51`, `Hmgcr`, `Fdft1`, `Fasn`, `Sqle`, `Dhcr24`, `Fdps`, `Ldlr` were all among the strongest genes |
| `Tuba1a` | 7 | alpha-tubulin loss caused a self-transcript plus tubulin-compensation module: `Tuba1a` down and `Tubb3`, `Tubb2a`, `Tuba4a`, `Tubb4a`, `Tubb4b`, `Tubb5` up |
| `Map1b` | 1 | microtubule-associated neuronal MAP; only `Map1b` itself passed FDR 0.05 |
| `Mapt` | 1 | neuronal MAP; only `Mapt` itself passed |
| `Map6` | 0 | neuronal microtubule stabilizer; no FDR 0.05 gene |
| `Kif1a`, `Kif5a`, `Kif5c`, `Kif21a` | 1 each | each was self-transcript-only at FDR 0.05 |
| `Kif1b`, `Kif2a`, `Kif3b` | 0 each | no focal FDR 0.05 gene |
| `Tubb4b`, `Tubb5` | 1 each | each was self-transcript-only |
| `Macf1`, `Camsap1`, `Ift88`, `Fmn1`, `Fmn2` | 0 each | no focal FDR 0.05 gene among additional broad cytoskeleton / microtubule nominees |

The runtime profile comparison gave the same qualitative result. In the
16-gene microtubule set, five nodes had no significant focal feature, ten had
only 1 to 9, and `Dctn1` was the lone at-least-50 outlier. Correlations within
the weak set did not reveal a broad hidden module: for example, `Mapre2` was
nearest to `Mapt` among the inspected peers by whole-profile Pearson
correlation, but both had only the self transcript significant; `Map1b` and
`Kif5a` were also mutually similar while both were self-only. `Dctn1` remained
only moderately similar to the kinesin / tubulin / MAP peers and its 49
positive and 26 negative significant genes were not shared by those weak
peers, supporting the corpus interpretation that `Dctn1` is a special
dynactin/sterol-response case rather than a generic CLIP2-like cytoskeletal
case.

## Target-specific reasoning

### `Clip2`

CLIP2, historically CLIP-115/CYLN2, is a neuronal CAP-Gly microtubule plus-end
linker. CLIP-115 was originally described as a brain-enriched microtubule
binding protein associated with dendritic lamellar bodies and homologous to
CLIP-170 (De Zeeuw et al. 1997, PMID 9427243). Its N-terminal MTB/CAP-Gly
region plus adjacent basic serine-rich regions are required for efficient
microtubule binding, and CLIP-115 can mark growing microtubule distal ends
similarly to CLIP-170 (Hoogenraad et al. 2000, PMID 10825300). CLIP family
proteins also interact with the +TIP network: CLASPs associate with CLIP-115
and CLIP-170 at growing microtubule ends (Akhmanova et al. 2001,
PMID 11290329), and depletion experiments in neuronal models show that CLIP-115
and CLIP-170 affect axonal microtubule growth rate and growth distance
(Stepanova et al. 2010, PMID 20471267).

Those facts make a microtubule-plus-end comparison biologically appropriate,
but the within-dataset evidence argues against a broad transcriptional
response in this assay:

- no exact `Clip2` paralog or narrow CLIP complex member was available in the
  training counts; `Clip1` was not a training perturbation in this task, and
  the available `Apc` CORUM projection corresponds to an APC-IQGAP1-CLIP-170
  human complex rather than to CLIP2 itself;
- `Dst`, the highest-priority GO-overlap candidate for `Clip2`, had zero
  focal FDR genes and was globally silent in the selected Distributed Agents report
  corpus;
- `Mapre2`, the closest perturbed plus-end binding protein, had one focal DEG,
  its own transcript, and the selected corpus reports no downstream
  FDR-supported neuronal response;
- `Map1b`, `Mapt`, several kinesins, and `Tubb4b`/`Tubb5` also landed at a
  self-transcript-only count of one, while `Map6`, `Kif1b`, `Kif2a`, and
  `Kif3b` were zero;
- `Tuba1a` and `Dctn1` are real counterexamples but are mechanistically
  narrower than the broad cytoskeletal label: `Tuba1a` triggered a tubulin
  autoregulation response, and `Dctn1` triggered a cholesterol/sterol
  compensation state. Neither state was reproduced by `Mapre2`, `Map1b`, or
  the canonical kinesins.

External mouse and human evidence also fits a weak call rather than a strong
one. Germline `Cyln2/Clip2` mutation in mouse can produce brain, hippocampal,
and motor-coordination defects with redistribution of CLIP-170 and dynactin at
growing microtubule tips (Hoogenraad et al. 2002, PMID 12195424), so CLIP2 is
not biologically inert. However, isolated human CLIP2 hemizygosity did not
recapitulate Williams-Beuren syndrome phenotypes in two siblings
(Vandeweyer et al. 2012, PMID 22608712), and the mouse result came from
developmental germline mutation rather than a sparse acute postnatal CRISPR
perturbation. In this single-nucleus endpoint, postmitotic plus-end defects
are quite plausibly handled subcellularly or developmentally rather than as a
large 3- to 4-week nuclear RNA program.

I therefore predict no broad downstream program for `Clip2`. The reason I do
not round all the way to zero is the repeated assay-local pattern that several
well-expressed microtubule transport genes had exactly one focal DEG, their
own target transcript. `Clip2` is a measured focal-cell gene in the parquet, so
a self-transcript call like `Mapre2`, `Map1b`, `Mapt`, `Kif5a`, or `Kif5c` is
slightly more likely than no call at all, but the downstream expectation is
near zero.

Point prediction: `Clip2 -> 1`.

## Limits

This is a deliberately weak positive prediction. The decisive limitation is
the lack of a trained exact paralog or CLIP2-containing complex perturbation:
all available training analogs came from broad GO or hallmark cytoskeleton
annotations. Whole-profile Pearson and cosine similarities among weak
near-null perturbations can be driven by nonsignificant log-fold-change tails,
so I used them only to reject hidden strong convergence, not to infer DEG
counts quantitatively. Target-transcript reduction is stochastic in this
AAV-CRISPR assay, and a self-only prediction for `Clip2` could easily be
observed as zero if the Clip2 transcript itself does not cross FDR 0.05.
