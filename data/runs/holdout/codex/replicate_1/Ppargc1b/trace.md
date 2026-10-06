# Ppargc1b forecast for `151 TH Prkcd Grin2c Glut`

## Endpoint

- Target manifest: `Ppargc1b`
- Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `p < 0.05`
- Declared training count table: 1,674 measured training perturbations; median `n_degs = 0`, 75th percentile `= 1`, 90th percentile `= 2`, 95th percentile `= 18`

The forecast below uses the declared training count table and the declared training Parquet only. `Ppargc1b` itself was absent from both measured training surfaces, so no target DEG count or target expression signature was used.

## Biology prior for Ppargc1b

The supplied biology bundle places PGC-1beta in a real but context-uncertain response regime.

- The exact focal-population expression reach is substantial: `Ppargc1b` was detected in `13,862 / 23,679` matched non-target nuclei in this thalamic class, or `58.5413%`, with mean raw UMI `1.0221`, mean log1p CP10k `0.4072`, and pseudobulk CPM `64.0578`.
- The target product is a dynamic nuclear transcriptional coactivator rather than an installed structural component or stable covalent product.
- The functional-stock card adjudicated that a disruptive P16 edit should stop new PGC-1beta production and likely substantially deplete target-derived coactivator stock over the P37-P44 harvest window.
- The strongest caveat is endpoint transfer: the nearest neural loss data are germline and in other brain regions, and `Ppargc1a` can buffer PGC-1 programs in a tissue-dependent way.

This argues against a pure expression-missing null, but it does not justify mapping Ppargc1b to the high end of the `151` DEG distribution.

## Training comparators

Typed analog nomination against the actual 1,674-gene training universe put six available genes in the narrow WP mitochondrial-gene-expression community shared with `Ppargc1b`:

| comparator | typed relation to Ppargc1b | observed `151` n_degs |
|---|---|---:|
| `Ppargc1a` | PGC-1 paralog / shared mitochondrial gene-expression module | 0 |
| `Creb1` | shared mitochondrial gene-expression module | 10 |
| `Nrf1` | shared module plus STRING physical edge to PGC-1beta | 138 |
| `Esrra` | shared module plus STRING physical edge to PGC-1beta | 57 |
| `Ppp3ca` | shared mitochondrial gene-expression module | 4 |
| `Myef2` | shared mitochondrial gene-expression module | 3 |

The exact significant-gene split from the training Parquet in `151 TH Prkcd Grin2c Glut` was:

| comparator | FDR<0.05 genes | up | down |
|---|---:|---:|---:|
| `Ppargc1a` | 0 | 0 | 0 |
| `Myef2` | 3 | 3 | 0 |
| `Ppp3ca` | 4 | 1 | 3 |
| `Creb1` | 10 | 3 | 7 |
| `Esrra` | 57 | 16 | 41 |
| `Nrf1` | 138 | 23 | 115 |

The module median was therefore 7 DEGs and its log1p mean was about 10 DEGs, but the active members were nuclear transcription factors rather than PGC-1 coactivators.

## Same-experiment semantic context

The packaged findings for training genes supported a node-specific interpretation of this pathway. In the same dataset, the PGC/ERR/PPAR/NRF mitochondrial network did not behave as a single transferable block: `Esrra` had a detectable partial oxidative-metabolism signature in `151 TH Prkcd Grin2c Glut`, whereas `Ppargc1a`, the ESRR paralogs, PPAR neighbors, and `Nrf1`-related perturbations were flat or divergent rather than phenocopying each other.

That matters for `Ppargc1b` because a single non-DNA-binding PGC coactivator loss should be pulled closer to the flat `Ppargc1a`/PPAR side than to direct loss of the DNA-binding `Nrf1` or `Esrra` nodes. Profile comparison of the six narrow-module genes was consistent with that caution: their individual significant programs overlapped poorly, with positive significant overlaps always zero and most negative significant overlaps zero or near zero.

## Synthesis

`Ppargc1b` has enough expression and stock turnover to plausibly score above the all-target median of zero, so I did not use the genome-wide default. The closest observed PGC/PPAR coactivator side, however, is mostly silent in `151`; the six-gene narrow module has three members at 0-4 DEGs, one member at 10, and two higher, node-specific transcription-factor responses at 57 and 138.

I therefore forecast a low single-digit-to-low-double-digit response and use the narrow-module midpoint, nudged upward from the 0-4 coactivator/weak-module values because `Ppargc1b` is broadly expressed in the focal non-target nuclei:

`predicted_n_degs = 8`
