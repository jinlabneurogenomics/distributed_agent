# Kansl1 DEG-count forecast

## Target and endpoint

- Target: `Kansl1`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Forecast: `5`

## Evidence used

The declared target manifest contains one active target, `Kansl1`. The held-out
target outcome and signature were not present in the declared focal count table
or the declared training parquet.

The Kansl1 biology bundle supports target reach and a plausible post-edit
biological effect in the requested assay window:

- `Kansl1` is directly detected in the focal non-target population:
  `82.6344%` expressing cells, `mean_raw_umi = 2.0993`, and
  `mean_cp10k = 1.3116`.
- The target is a noncatalytic KAT8-containing NSL-complex component with a
  documented connection to STX17 transcription and autophagosome-lysosome
  fusion.
- Inducible Kansl1 deficiency in primary mouse neurons produced STX17 and
  mitophagy effects within days, so functional depletion by the P37-P44 harvest
  after P16 editing is plausible.
- The same card kept the numeric protein half-life, thalamic NSL kinetics, and
  Kansl1l compensation unresolved, so this is not strong evidence for a large
  transcriptional footprint.

The focal training-count table was sparse:

- `1674` training perturbations.
- `1205` had `0` DEGs.
- Median `n_degs` was `0`; mean was `14.05`.
- Only `106` had at least `10` DEGs, and only `43` had at least `100`.

Typed annotation nomination against the actual 1674-gene training universe
found only a few close or moderately close measured comparators. Their
`151 TH Prkcd Grin2c Glut` counts were:

| Comparator set | Genes | Focal `n_degs` |
|---|---|---|
| KAT8 or NSL/MSL closest | `Ogt`, `Msl2` | `4`, `0` |
| Other exact-complex or paralog tier | `Chd8`, `Kmt2a`, `Las1l` | `61`, `24`, `0` |
| Narrow HAT/WDR5 module | `Setd1a`, `Yeats2`, `H4c11`, `Ncoa1`, `Kat6b`, `Pax3`, `Brd1` | `368`, `0`, `0`, `0`, `0`, `0`, `4` |
| Direct STRING physical edge | `Mga` | `2` |

The exact-complex tier had median `4` DEGs and log1p back-transformed mean
`5.0`; the exact plus narrow plus direct set had median `0` and log1p
back-transformed mean `2.9`. A few broader chromatin regulators, especially
`Setd1a`, can produce many DEGs in this class, but they are WDR5/MLL1 or broad
HAT/chromatin comparators rather than a direct KANSL1/NSL operation. `Ogt` was
a useful boundary: it is an ortholog-projected NSL-complex candidate and was
strongly detected in other cell classes, yet had only `4` DEGs in the focal
thalamic class.

## Synthesis

The qualitative prior argues against a guaranteed null: `Kansl1` is expressed
in the class and its neuronal stock should be depleted within the CRISPR-to-
harvest interval. The task-matched quantitative evidence argues for a small
count rather than a broad chromatin collapse: the closest available KAT8/NSL/MSL
comparators were `0-4`, and most other narrow candidates were also `0`, with
only indirect WDR5/MLL1 comparators reaching tens to hundreds of DEGs.

I therefore placed Kansl1 slightly above the closest direct analog counts to
reflect its strong focal expression and direct neuronal loss evidence, but well
below the looser high-response chromatin outliers. The resulting point forecast
is:

`predicted_n_degs = 5`
