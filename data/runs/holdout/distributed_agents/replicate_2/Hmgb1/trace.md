# Prediction trace

## Question and resolved ambiguities

The held-out manifest for this run contains one perturbation, `Hmgb1`. I treated
the requested endpoint as the integer number of genes with BH-adjusted
Wilcoxon `pvals_adj < 0.05` in the focal `151 TH Prkcd Grin2c Glut` cell group
after sparse AAV CRISPR loss of the target gene.

I interpreted zero as "no measured transcript is expected to clear the
experiment's FDR threshold", not as absence of HMGB1 biology. I also interpreted
the extracellular alarmin/inflammation literature for HMGB1 as only weakly
transferable, because the experiment perturbs postmitotic neuronal nuclei in a
NeuN-enriched preparation rather than microglia, macrophages, astrocytes, or an
injury model with HMGB1 release.

## Sources used

- Requested targets:
  `[local file: 105_Hmgb1.csv]`.
- Training endpoint counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Training differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Distributed Agents same-experiment corpus release
  `perturbai-july-260713-sourceguard-1773-v1`. The corpus had no target-centered
  findings for `Hmgb1`, `Hmgb2`, or `Hmgb3`, so it did not provide a curated
  HMGB-neighborhood analog.
- NCBI PubMed E-utilities for external literature.

Key external references:

- Calogero et al. 1999, Nature Genetics, PMID:10391216,
  DOI:10.1038/10338. `Hmg1/Hmgb1` binds and bends DNA as a non-sequence-specific
  chromatin architectural protein; mice lacking Hmg1 are born but die from
  neonatal hypoglycaemia, and Hmg1-deficient cell lines can grow with specific
  transcription-factor defects rather than collapse of global chromatin.
- Tang et al. 2023, Nature Reviews Immunology, PMID:37322174,
  DOI:10.1038/s41577-023-00894-6. HMGB1 has nuclear DNA repair/chromatin roles,
  cytosolic stress-response roles, and extracellular DAMP/alarmin roles.
- Starkova et al. 2023, International Journal of Molecular Sciences,
  PMID:37176041, DOI:10.3390/ijms24098334. HMGB1 and HMGB2 are homologous HMGB
  chromatin proteins with overlapping DNA-binding architecture but divergent
  regulation and biological roles.

## Dataset computations

1. Loaded the one-column held-out manifest and confirmed that this run asks only
   for `Hmgb1`.
2. Loaded the focal training count CSV and used it as the observed endpoint for
   all non-held-out perturbations in `151 TH Prkcd Grin2c Glut`.
   - Training perturbations: 1,674.
   - Perturbations with `n_degs = 0`: 1,205.
   - Nonzero median: 1 DEG.
   - Nonzero 75th percentile: 7 DEGs.
   This makes the assay highly zero-inflated; isolated loss of a broadly
   expressed nuclear protein must be matched to quite strong analog evidence
   before predicting a wide response.
3. Queried the focal count table for HMGB and nearby chromatin-family genes.
   `Hmgb1`, `Hmgb2`, `Hmgb3`, `Hmgb4`, `Hmga1`, `Hmga2`, and `Hmgn1/2/3/5` are
   all absent from training, so no direct HMGB/HMG paralog count exists.
4. Filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` for a
   focused set of chromatin and transcriptional coregulator targets, then counted
   rows with `pvals_adj < 0.05` and inspected the top adjusted-p-value genes for
   each signature. Those counts agreed with the compact endpoint CSV.

Representative analog/counterexample signatures in the focal cell group:

| perturbation | observed n_degs | focal expression-pattern evidence |
| --- | ---: | --- |
| `Set` | 0 | no gene passed FDR among 163 matched perturbed nuclei |
| `Mbd2` | 0 | no gene passed FDR among 244 perturbed nuclei |
| `Mbd5` | 0 | no gene passed FDR among 116 perturbed nuclei |
| `Ep300` | 0 | no gene passed FDR among 155 perturbed nuclei |
| `Smarca4` | 0 | no gene passed FDR among 146 perturbed nuclei |
| `Smarca2` | 1 | only `Smarca2` itself passed FDR, consistent with little propagated response |
| `Setd2` | 1 | a singleton `Septin5` call rather than a broad chromatin state |
| `Crebbp` | 8 | small signature despite a general transcriptional coactivator function |
| `Mecp2` | 16 | modest neuronal chromatin response; top calls included `Nap1l5`, `Ache`, `Focad`, `Tnr` |
| `Setdb1` | 22 | modest heterochromatin/Atf7ip-related response; top calls included `Tasor`, `Pmvk`, `Atf7ip` |
| `Chd8` | 61 | clear remodeler response with target downregulation and top changes such as `Pnisr`, `Tmem50a` |
| `Chd4` | 100 | broader NuRD ATPase response with top calls such as `Begain`, `Cpne7`, `Zfp467` |
| `Smarcc2` | 185 | broad SWI/SNF-complex response with `Ptpn3`, `Reep2`, `Prkcd`, and `Smarcc2` among strongest calls |
| `Brd4` | 311 | broad BET/chromatin reader response with many high-significance calls |
| `Setd1a` | 368 | broad H3K4 methyltransferase-complex response dominated by many negative log-fold changes |

I also checked canonical extracellular HMGB1 receptor and autophagy/inflammasome
branches in the count table. Where present, they were uninformative in this
neuronal assay: `Tlr2`, `Tlr4`, `Ager`, `Nfkb1`, `Rel`, `Chuk`, `Tnfrsf1a`,
`Mapk1`, `Stat3`, `Becn1`, and `Atg5` each had 0 DEGs, while `Sqstm1` and
`Map1lc3a` each had 1 DEG.

## Target-specific reasoning

### Hmgb1

HMGB1 is an abundant non-histone chromatin protein that binds distorted DNA,
bends linear DNA, favors nucleosome entry/exit DNA, and assists selected
transcription factors. A complete germline knockout is lethal around birth, but
Calogero et al. showed that cells without Hmg1/Hmgb1 can still proliferate and
that the defect is specific transcriptional control rather than wholesale
failure of nuclear organization. Tang et al. additionally emphasize the
context-dependent split between nuclear HMGB1 functions and extracellular DAMP
functions.

The most appropriate direct analogs would have been `Hmgb2` or `Hmgb3`, but none
of the HMGB/HMGA/HMGN family members were present in the focal training counts.
I therefore used weaker within-dataset counterexamples: proteins that perturb
chromatin structure, chromatin-associated transcription, or nucleosome-remodeling
states in the same cell type.

Those analogs do not support a large count. Several global-looking chromatin
regulators were exactly silent in this assay (`Set`, `Mbd2`, `Mbd5`, `Ep300`,
`Smarca4`), and closely related remodeling-complex or chromatin-binding
perturbations were often very small (`Smarca2` = 1, `Setd2` = 1, `Crebbp` = 8,
`Mecp2` = 16, `Setdb1` = 22). The broad examples (`Setd1a`, `Brd4`, `Smarcc2`,
`Chd4`, `Chd8`) are catalytically active or large stable-complex subunits with
stronger evidence for acute, cell-autonomous transcriptional programs in the
observed profiles; they are useful upper-bound counterexamples rather than close
HMGB1 surrogates.

For the zero/nonzero decision, I down-weighted extracellular HMGB1 signaling
because the perturbation is a cell-autonomous loss of `Hmgb1` in sparse
postmitotic neurons, not necrotic release of HMGB1 or receptor blockade in
immune cells. The available receptor-side perturbations were themselves mostly
zero in the training table. I also down-weighted germline lethality because the
experiment is acute, mosaic, postnatal, and has partial target-RNA reduction.
With no direct HMGB paralog signature and no positive same-complex training
evidence, the best calibrated call is that `Hmgb1` will fall on the zero side of
this FDR-thresholded endpoint.

Prediction: `Hmgb1 -> 0` DEGs.

## Limits

- This is an extrapolation: the training set has no `Hmgb1`, `Hmgb2`, `Hmgb3`,
  `Hmgb4`, `Hmga`, or `Hmgn` perturbation in the focal count table.
- Chromatin analogs are mechanistically imperfect. The broad signatures from
  `Brd4`, `Setd1a`, `Smarcc2`, `Chd4`, and `Chd8` reflect reader, methyltransferase,
  or remodeler-complex biology that is more enzymatic or more complex-scaffolded
  than HMGB1 DNA bending.
- The parquet signatures were inspected only for biologically chosen analogs;
  a held-out target has no expression profile, so expression-profile nearest
  neighbors cannot be computed directly for `Hmgb1`.
- HMGB1 has substantial extracellular inflammatory biology, but this cell group
  and NeuN-enriched snRNA-seq assay provide little microglial or peripheral immune
  context, making those mechanisms uncertain for the measured endpoint.
