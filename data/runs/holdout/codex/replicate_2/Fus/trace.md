# Fus direct n_degs forecast

## Target and endpoint

- Target: `Fus`, the single entry in the declared holdout manifest.
- Population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- The declared 151 count table contains 1,674 training targets and excludes `Fus`.

## Target biology used

- `Fus` is directly detected in the focal non-target nuclei: 23,569 of 23,679
  cells express it, with mean raw UMI 8.05, mean CP10K 5.12, and pseudobulk
  504.27 CPM. I used this only to establish target reach in the assayed
  population, not to infer editing efficiency.
- The functional-stock card calls FUS a dynamic nuclear RNA/DNA-binding and
  RNP-associated protein whose supply should clear within the P16 to P37-P44
  window; primary mouse-neuron knockdown depleted FUS protein and produced an
  RNA-regulatory consequence within 10 days.
- The observability card supports a postnatal neuronal effect outside thalamus
  and notes incomplete buffering by the FET relatives EWSR1 and TAF15, but the
  same evidence also warns that the exact thalamic half-life and
  survivor-conditioned response are not directly measured.

## Training evidence used

The 151 training-count distribution is very sparse:

- median `n_degs`: 0
- 75th percentile: 1
- 90th percentile: 2
- 95th percentile: 18
- maximum: 2,677
- 1,205 of 1,674 training targets have zero DEGs

So a forecast above tens of genes requires a target-specific reason rather than
being the default behavior of the screen.

I treated the visible RNA-processing/RBP targets as the main quantitative
brackets and checked their 151 profiles in the expression Parquet:

| training target | 151 `n_degs` | interpretation |
| --- | ---: | --- |
| `Rnpc3` | 868 | core spliceosome/RNA-processing perturbation |
| `U2af2` | 828 | core spliceosome/RNA-processing perturbation |
| `Hnrnpu` | 733 | broad hnRNP/chromatin-scaffold stress response |
| `Cdc40` | 624 | core spliceosome/RNA-processing perturbation |
| `Prpf6` | 454 | core spliceosome perturbation |
| `Snrnp70` | 213 | spliceosome perturbation |
| `Tardbp` | 210 | disease-linked nuclear RBP, moderate broad response |
| `Matr3` | 149 | disease-linked nuclear RBP, moderate broad response |
| `Hnrnpc` | 122 | hnRNP response, smaller than core spliceosome |
| `Hnrnpa2b1` | 11 | related nuclear RBP but sparse response |
| `Atxn2` | 8 | ALS/stress-granule relative, sparse response |
| `Ddx3x` | 8 | RNA helicase, sparse response |
| `Tia1` | 0 | ALS/stress-granule relative, flat response |
| `Fmr1` | 0 | RBP, flat response |

Same-experiment Findings were used as interpretation of those measured
training outcomes, not as independent replication. The useful constraints were:

- HNRNPU, HNRNPC, and HNRNPA2B1 Findings explicitly reject a generic hnRNP
  family phenocopy: abundant nuclear RBP loss can be broad, moderate, or nearly
  flat in the same P16 neuronal assay.
- TARDPB/MATR3/ATXN2/TIA1 Findings likewise report that ALS-linked or
  RNA-granule/RBP membership is not enough to imply a shared transcriptomic
  module; the measurable TDP-43 and Matrin3 responses did not transfer to most
  ALS/RBP relatives.
- MATR3 and TARDPB are therefore upper RBP comparators rather than a template
  for all FUS-like disease genes, while HNRNPA2B1/ATXN2/TIA1 bound the buffered
  side.

The local profile comparison of this RBP/spliceosome cohort in 151 confirmed the
same structure: `U2af2`, `Prpf6`, `Cdc40`, and `Rnpc3` form the large
RNA-processing branch with many shared significant features, whereas
`Tardbp`, `Matr3`, and `Hnrnpc` have weaker and only partially overlapping
signatures, and `Hnrnpa2b1`, `Atxn2`, `Ddx3x`, `Fmr1`, and `Tia1` are sparse or
flat.

## Synthesis

I expect a real FUS perturbation state because `Fus` is highly expressed in the
focal nuclei and the biological card makes persistence of the starting protein
stock unlikely by harvest. I discounted the core-spliceosome counts because FUS
is a dynamic RBP/transcription-splicing regulator, not an obligate spliceosome
component, and its closest FET relatives can compensate incompletely. I also
discounted a strict zero-to-10 prediction because mouse-neuron and postnatal
forebrain loss evidence argue that single `Fus` loss is not completely silent.

My point forecast is therefore a low-dozens response: above the sparse
HNRNPA2B1/ATXN2/TIA1 side of the RBP training set, but below the visible
HNRNPC/MATR3/TDP-43 branch and far below the core spliceosome branch.

Predicted `n_degs`: **48**
