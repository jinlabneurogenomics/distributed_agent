# Trace

## Target and endpoint

Target: `Kmt5b`

Cell class: `151 TH Prkcd Grin2c Glut`

Endpoint: `n_degs`, the number of measured genes in this class with
BH-adjusted Wilcoxon `p < 0.05`.

## Evidence used

### Declared biology bundle

The Kmt5b biology bundle identifies the perturbation as a P16 disruptive
CRISPR-Cas9 edit assayed at P37-P44 in postmitotic mouse thalamic neuronal
nuclei. The exact focal-population expression measurement shows that `Kmt5b`
was detectable in the assayed non-target population, with mean CP10K 0.7665,
mean raw UMI 1.201, 15,633 of 23,679 non-target nuclei expressing it
(`66.0%`), and target-contrast availability in the focal class.

The same bundle supports functional realization by harvest rather than a pure
latency/null prior: KMT5B supplies H4K20 methylation, juvenile PFC Kmt5b
knockdown reduced KMT5B protein and H4K20me2 within 14-20 days, and the
21-28-day screen interval is long enough to deplete the enzyme and the
renewable fraction of its marked chromatin substrate. I treated two pieces as
downward modifiers rather than nullifiers: KMT5B edits do not erase
pre-existing H4K20-methylated nucleosomes, and KMT5C/NSD2-like residual
activity could buffer part of the H4K20 state.

### Training count table

The declared focal-class count table contains 1,674 training perturbations.
It is zero-heavy in this cell class:

- median `n_degs`: 0
- mean `n_degs`: 14.05
- zero counts: 1,205 / 1,674
- `n_degs <= 5`: 1,546 / 1,674
- `n_degs >= 100`: 43 / 1,674
- maximum: 2,677

Thus the base rate alone favors a null or singleton response, and large
chromatin footprints are exceptional.

Counts for methyltransferase or chromatin-regulator training perturbations in
the same `151 TH Prkcd Grin2c Glut` table were heterogeneous:

| target | focal `n_degs` |
|---|---:|
| Nsd2 | 0 |
| Ash1l | 1 |
| Setd2 | 1 |
| Ehmt1 | 4 |
| Crebbp | 8 |
| Mecp2 | 16 |
| Setdb1 | 22 |
| Nsd1 | 23 |
| Kmt2a | 24 |
| Arid1a | 22 |
| Chd8 | 61 |
| Smarcc2 | 185 |
| Setd1a | 368 |
| Sin3a | 1,433 |

I weighted the direct methyltransferase-like entries more than remodeler,
HDAC-scaffold, or MLL/SET1A-complex outliers. The closest H4/H3 methylation
comparators therefore centered in the low range: `Nsd2` was flat, `Ash1l` and
`Setd2` were singletons, `Ehmt1` had 4 genes, and the stronger but still
contained `Setdb1`/`Nsd1`/`Kmt2a` cases were 22-24 genes.

### Declared expression Parquet and same-experiment corpus

I queried the declared all-cell training Parquet only for training nodes in
the focal class. It reproduced the low-to-moderate comparator counts above:
`Nsd2` had 0 significant focal genes, `Ash1l` 1, `Setd2` 1, `Ehmt1` 4,
`Setdb1` 22, `Nsd1` 23, and `Kmt2a` 24, whereas `Setd1a`, `Smarcc2`, and
`Sin3a` were much broader at 368, 185, and 1,433. The matched focal control
pool was 23,679 nuclei for all of these queried rows; the low counts were not
limited to a single underpowered perturbation because `Nsd2`, `Nsd1`, `Kmt2a`,
`Setd1a`, `Sin3a`, and `Smarcc2` each had more than 130 matched perturbed
nuclei.

A symmetric profile comparison over 39 observed chromatin regulators confirmed
that these training perturbations do not form one transferable chromatin
module: among the supplied chromatin cohort there were 15 null, 9 one-to-nine
gene, 8 ten-to-forty-nine gene, and 7 at-least-fifty gene responders. The
profile comparison showed mostly weak significant-program overlap, so I did
not average the high-burden Sin3a/Setd1a/Smarcc2 signatures into Kmt5b. The
packaged corpus was consistent with this boundary: Nsd2 had no robust
postnatal neuronal transcriptome across recovered neuronal groups at
FDR < 0.10, and H3K36-axis relatives did not converge on an interchangeable
postmitotic neuronal response.

## Synthesis

Kmt5b sits above the screen-wide null prior because it is expressed in the
focal class and the endpoint-blind biology bundle gives strong evidence that
loss of KMT5B enzyme and part of its H4K20me2 chromatin output should be
realized within the P16-to-P37/P44 window. That argues against copying the
flat `Nsd2` result as a point estimate.

The expected effect is still a contained thalamic transcriptional response,
not a broad collapse. The direct operation is a histone methyltransferase with
an already-installed mark, slow/stable chromatin carriers, and possible
KMT5C/NSD2 residual capacity. In the measured training table, the more
analogous chromatin writers and methylation-linked perturbations mostly ran
from 0 to 24 focal DEGs; large signatures belonged to more pleiotropic or
complex-level regulators.

I therefore placed Kmt5b near the top of the methyltransferase-like low-count
cluster but below the 22-24 gene `Setdb1`/`Nsd1`/`Kmt2a` cases, giving a
point forecast of 16 focal DEGs.
