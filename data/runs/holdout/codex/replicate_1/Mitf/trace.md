# Mitf n_degs forecast

## Target and endpoint

- Target from the one-row holdout manifest: `Mitf`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes in that population with BH-adjusted Wilcoxon `p < 0.05`.
- Point prediction: `0`.

## Evidence used

### Canonical target biology

The declared Mitf biology bundle identifies this packet target as Entrez Gene
667838, official symbol `Naip3`, with `Mitf` as an alias. I therefore treated it
as the Naip3 pseudogene locus, not as the distinct microphthalmia-associated
transcription-factor gene.

The selected source facts were:

- `mitf.operation.pseudogene`: NCBI classifies Gene 667838 as the Naip3
  pseudogene; genomic analysis found no Naip3 cDNA and loss of the
  exon-10-equivalent region that would preserve a coding transcript.
- `mitf.turnover.no_product`: no Naip3 protein product or target-specific
  protein-turnover entity is established.

The functional-stock card consequently has no identified pre-edit protein stock
to follow through the P16 to P37-P44 perturbation window. It remains
`indeterminate`, because an uncharacterized functional RNA is not formally
excluded, but there is no established product, renewal demand, postnatal
thalamic loss phenotype, or timing anchor that would make a broad recovered
neuronal RNA response expected.

### Exact focal-population reach

The exact non-target expression reach for the assayed feature in
`151 TH Prkcd Grin2c Glut` is low:

- mean CP10K: `0.11316049800311873`
- pseudobulk CPM: `11.823249737469993`
- mean raw UMI: `0.18864816926390474`
- expressing non-target nuclei: `3740 / 23679` (`15.794585920013514%`)

This establishes that the feature exists in the focal population but is sparse.
By the dataset guard, self-expression is not an editing-efficiency measurement;
I used it only as reach/context for a target whose functional object is already
unresolved.

### Training-count distribution

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains
1,674 biological training perturbations. Their same-endpoint counts are strongly
concentrated at zero:

- `1205 / 1674` have `n_degs = 0`.
- `1481 / 1674` have `n_degs <= 1`.
- `1546 / 1674` have `n_degs <= 5`.
- The median is `0`, the 75th percentile is `1`, and only `106 / 1674` reach
  `10` or more DEGs.

Thus the task-matched empirical default is already zero or one DEG; the large
tail is driven by genes with clear cell-intrinsic functions and is not a good
prior for a pseudogene target with no established operative stock.

### Training analog search

I used the closed mouse annotation and corpus-aware analog nominator against the
same 1,674-gene training universe.

- A literal `Mitf` query resolved to the canonical MITF transcription factor and
  returned melanocyte/KIT/RAF/BRAF comparators such as `Ep300`, `Kit`, `Raf1`,
  `Creb1`, `Bcl2`, and `Braf`. Those were discarded because they refer to the
  distinct MITF TF, whereas the declared packet target is Naip3.
- A query with the packet official symbol `Naip3` was preserved as unresolved
  and returned zero exact paralog, bidirectional corpus-comparator,
  narrow-module, direct-interaction, or broad-functional-fallback candidates in
  the training universe.

With no valid Naip3-like measured cohort, I did not transfer any endpoint
magnitude from the invalid MITF-TF neighbors.

## Synthesis

The prediction is anchored on the measured class-specific base rate and adjusted
by the biology bundle. In the focal thalamic class, a zero-DEG result is the
modal and median outcome among training perturbations. Mitf/Naip3 adds several
negative or unresolved pieces of biology: the target is a pseudogene with no
established protein-coding operation, no supported protein stock to deplete
over 21-28 days, no target-specific mouse postnatal neural loss phenotype, and
no curated Naip3 comparator in the training universe. The only counterweight is
low but detectable focal expression of the measured `Mitf` feature, which keeps
an unknown RNA effect possible but does not justify moving off the zero-count
mode.

I therefore predict that the held-out Mitf perturbation will have no measured
FDR-significant genes in `151 TH Prkcd Grin2c Glut`.
