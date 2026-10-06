# Cacna1c forecast

## Target and endpoint

- Target: `Cacna1c`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: count of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Point forecast: `12`

## Evidence used

### Biology-only Cacna1c bundle

The declared holdout manifest contains only `Cacna1c`. In the declared
biology-only bundle, the exact focal-population expression measurement showed
that `Cacna1c` is broadly detected in the same assayed thalamic class:

| quantity | value |
|---|---:|
| `pct_cells_expressing` in non-target cells | 98.49 |
| `mean_raw_umi` | 6.68 |
| `mean_log1p_cp10k` | 1.565 |
| `pseudobulk_cpm` | 418.84 |
| expressing non-target cells | 23,322 / 23,679 |

This made target reach a strong positive prior: dilution by target absence is
unlikely in the aggregated `151 TH Prkcd Grin2c Glut` population.

The same bundle identifies Cacna1c as the CaV1.2 alpha-1C pore-forming
voltage-gated L-type calcium-channel subunit, with the operative entity being a
dynamic plasma-membrane channel complex. Its functional-stock adjudication calls
the 21-28 day P16-to-harvest interval long enough that newly edited cells should
substantially lose CaV1.2 stock by harvest, despite initial persistence of
pre-edit surface and recycling-pool channels. The evidence is still partial:
the closest turnover measurement is not in juvenile thalamus, and Cacna1d
provides a related L-type route that may buffer some CaV1.2 loss.

### Training count table

The focal-class count table has 1,674 measured training perturbations and is
very sparse:

| statistic | `n_degs` |
|---|---:|
| mean | 14.05 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| zero-count targets | 1,205 / 1,674 |

I therefore did not treat high target expression plus plausible stock depletion
as enough for a broad response. A forecast above 20 would already be beyond the
95th percentile of all training perturbations in this class.

### Ca-channel and excitability comparators

I inspected the declared training measurements for calcium-entry,
calcium-handling, and excitability genes in `151 TH Prkcd Grin2c Glut`. Exact
counts from the training table were:

| comparator class | training targets and focal `n_degs` |
|---|---|
| high-voltage Ca-channel alpha subunits | `Cacna1a`: 0; `Cacna1d`: 0; `Cacna1e`: 0 |
| thalamic/auxiliary Ca-channel components | `Cacna1g`: 12; `Cacna2d1`: 1; `Cacna2d2`: 0; `Cacnb2`: 0; `Cacnb4`: 1 |
| Ca signaling and extrusion | `Atp2b1`: 22; `Atp2b2`: 1; `Atp2b3`: 1; `Calm1`: 14; `Calm2`: 0; `Calm3`: 1 |
| broader excitability comparators | `Grin1`: 89; `Grin2a`: 1; `Grin2b`: 2; most assayed `Kcn*`, `Scn*`, `Ryr*`, `Itpr*`, `Adcy*`, and `Camk*` targets: 0-1 |

For the most relevant exact Parquet rows, each comparator had 17,259 measured
genes in this cell class. The near-neighbor calcium counts were small but not
all null:

| target | FDR < 0.05 | FDR < 0.10 | median matched perturbed nuclei |
|---|---:|---:|---:|
| `Cacna1g` | 12 | 15 | 264 |
| `Atp2b1` | 22 | 27 | 146 |
| `Calm1` | 14 | 21 | 208 |
| `Cacna2d1` | 1 | 1 | 143 |
| `Cacnb4` | 1 | 1 | 176 |
| `Cacna1d` | 0 | 0 | 160 |
| `Cacna1a` | 0 | 0 | 117 |
| `Cacna1e` | 0 | 0 | 144 |

## Synthesis

The expression and stock evidence argue against a hard-zero forecast:
`Cacna1c` is present in nearly every assayed non-target nucleus, and a
CRISPR-disrupted CaV1.2 membrane channel should be functionally affected within
the 3-4 week assay window.

The measured training perturbations argue for a low count. Losses of ion
channels and calcium-signaling genes in the same thalamic class usually
produced no significant genes or single-gene traces; the strongest
mechanistically adjacent cases, `Cacna1g`, `Calm1`, and `Atp2b1`, landed in the
12-22 DEG range rather than in the hundreds. `Grin1` at 89 shows that an
excitability perturbation can exceed this range, but it removes the obligatory
NMDA receptor subunit and is a broader glutamatergic lesion than single L-type
CaV1.2 loss.

I therefore forecast a small but detectable CaV-linked response and used the
`Cacna1g` focal count as the closest numerical anchor, with a downward check
from silent `Cacna1d`/`Cacna1a`/`Cacna1e` and an upward check from
`Atp2b1`/`Calm1`.
