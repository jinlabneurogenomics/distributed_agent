# Mapk8ip1 direct `n_degs` forecast

## Target and focal population

- Target: `Mapk8ip1`.
- Requested cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes in this class with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

The declared target bundle is biology-only for this endpoint. It reports that
`Mapk8ip1` is strongly reachable in the exact focal population: in
non-targeting nuclei from `151 TH Prkcd Grin2c Glut`, `Mapk8ip1` was detected in
22,938 of 23,679 nuclei, or 96.87%, with mean raw UMI 4.76 and pseudobulk CPM
298.2. I used this as expression reach only, not as a quantitative measure of
editing efficiency.

## Biology prior

`Mapk8ip1` encodes JIP1, a dynamic neuronal scaffold and kinesin-associated
component for selected JNK signaling modules. The card adjudicates the P16
CRISPR perturbation as likely to substantially deplete operative JIP1 stock by
the P37-P44 harvest because successful edits stop new intact protein supply
over a 21-28 day window, while existing scaffold protein should gradually turn
over.

The same evidence keeps the expected transcriptional footprint small rather
than pan-cellular:

- the best direct mouse phenotypes are hippocampal stress-induced JNK signaling,
  stress lesions, apoptosis, and NMDAR-linked plasticity or learning, not a
  constitutive thalamic fate program;
- JIP1 is stimulus-selective and is not required for every JNK response;
- related JIP scaffolds remain possible buffers, even though single `Jip1` loss
  is not fully compensated in the assayed stress contexts;
- no target-specific JIP1 half-life or thalamic P16-to-P44 response clock was
  available.

## Training measurements used

The declared `151 TH Prkcd Grin2c Glut` count table contains 1,674 training
perturbations. It is very sparse: 1,205 of 1,674 targets have zero significant
features, the median is 0, the 75th percentile is 1, the 90th percentile is 2,
and only the heavy upper tail reaches broad responses above tens to hundreds of
DEGs.

For JNK/MAPK-proximal perturbations present in the table, the same-cell counts
were all quiet:

| perturbation | `n_degs` |
|---|---:|
| `Mapk9` | 0 |
| `Mapk1` | 0 |
| `Map2k1` | 4 |
| `Map2k2` | 0 |
| `Map2k6` | 0 |
| `Map3k7` | 0 |
| `Braf` | 4 |
| `Raf1` | 0 |
| `Pak1` | 1 |
| `Pak2` | 0 |
| `Pak3` | 0 |
| `Rac1` | 0 |
| `Cdc42` | 1 |

The low scale was also the usual behavior for available synaptic/NMDAR and
kinesin-adjacent perturbations that are plausible downstream contexts for JIP1:
`Camk2a` 0, `Camk2b` 1, `Dlg4` 1, `Grin2a` 1, `Grin2b` 2, `Kif5a` 1, and
`Kif5c` 1. I treated `Grin1` 89, `Dctn1` 75, and `Rab7` 501 as boundary
measurements rather than direct scale donors: those genes perturb core receptor,
dynactin, or late-endosomal machinery and are much broader than selective JIP1
scaffold loss.

I also compared the focal MAPK/synaptic nodes against the broad transport
boundaries in the exact 151-class Parquet profiles. `Mapk9` and `Mapk1` had 0
significant features, `Map2k1` had 4, `Grin2b` had 2, and `Dlg4` had 1. Their
whole-profile cosines against `Dctn1` and `Rab7` were near zero, so the
large-count `Dctn1` and `Rab7` profiles did not look like the local quiet
MAPK/NMDAR training signatures.

The raw Parquet self rows further support a one-gene rather than multi-gene
point: the 1-DEG `Dlg4`, `Kif5a`, `Kif5c`, and `Grin2a` perturbations each had a
significant self-target transcript in this class, whereas `Mapk9` and `Mapk1`
did not. Thus a high-expression, scaffold-local perturbation such as
`Mapk8ip1` can reasonably land at a self-only or self-plus-tiny response even
when pathway-local downstream genes are transcriptionally quiet.

## Point forecast

I forecast `Mapk8ip1` as a very small nonzero response. The expression reach and
likely functional-stock depletion argue against an absent or unassayable target,
but JIP1's selective stress/plasticity operation and the quiet JNK/MAPK,
NMDAR/post-synaptic, and kinesin-adjacent training perturbations argue strongly
against a tens-to-hundreds DEG burden. I therefore placed the point at one
FDR-significant measured gene, effectively a self/local RNA hit with little
resolved downstream transcription.

`predicted_n_degs = 1`
