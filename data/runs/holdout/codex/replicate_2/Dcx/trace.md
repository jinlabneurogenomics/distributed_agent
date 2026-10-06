# Dcx DEG-count forecast

## Target and endpoint

The one-row holdout manifest names `Dcx`, and the requested endpoint is the
number of genes with BH-adjusted Wilcoxon `p < 0.05` in
`151 TH Prkcd Grin2c Glut`.

The prediction uses these declared same-experiment inputs:

- focal training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- training DE profiles:
  `[local file: training_de_all_cell_groups.parquet]`
- Dcx biology bundle:
  `[local file: Dcx.json]`

I treated the report corpus as an interpreted view of the same experiment, not
as an independent replicate.

## Dcx biology

The Dcx bundle gives mixed but mostly low-burden evidence for the exact
P16-to-P37/P44 thalamic setting.

- The exact non-target expression reach in `151 TH Prkcd Grin2c Glut` is not
  absent: `Dcx` is detected in 11,066 of 23,679 non-target nuclei
  (`46.7334%`), with `mean_raw_umi = 0.8412` and
  `mean_cp10k = 0.5437`.
- The stock card concludes that, in a Dcx-expressing edited neuron,
  pre-existing DCX protein is likely substantially depleted by harvest because
  DCX is a renewable microtubule-associated protein and a neuronal pulse-chase
  proxy measured turnover on an hours scale.
- The phenotype and expression evidence does not establish a broad mature
  thalamic requirement: positive single-gene mouse loss evidence is mainly
  developmental hippocampal lamination; adult dentate-gyrus acute loss did not
  change the measured newborn-neuron survival, differentiation, or fate
  outcomes; late postnatal/adult expression is described as concentrated in
  immature or neurogenic populations rather than pan-thalamic mature neurons.
- Dclk1/Dclk2 redundancy is known in developing hippocampus, but the bundle
  explicitly leaves compensation in the assayed mature thalamic context
  unresolved.

The same-experiment corpus had no target report, Claim, or explicit comparator
for `Dcx` in this release, so it did not add target-specific experimental
interpretation.

## Same-cell training scale

The focal count table contains 1,674 training perturbations. Its distribution
is heavily concentrated near zero:

- `1205 / 1674` have `n_degs = 0`.
- `276 / 1674` have `n_degs = 1`.
- `193 / 1674` have `n_degs > 1`.
- median = `0`, 75th percentile = `1`, 90th percentile = `2`, 95th percentile
  = `18`.

Because the endpoint includes the edited transcript itself, I also checked the
self row in the focal Parquet profiles. There were 319 training perturbations
with a significant self transcript; 237 of the 276 one-DEG perturbations were
self-only. This makes `1` a plausible outcome for a transcriptionally flat
target whose own RNA is knocked down, but self-RNA loss is not reliable enough
in this atlas to forecast a self-only hit from Dcx expression alone.

## Comparator evidence from available training genes

The closest DCX-family comparators were not available as training
perturbations in this table: `Dclk1`, `Dclk2`, `Map2`, and `Tubb3` were absent.
The typed gene-analog nomination step therefore found no available exact
paralog or reciprocal corpus comparator for `Dcx`; the available candidates
were weaker Reelin/LIS1, beta-cell-module, developmental, synaptic, and
microtubule fallbacks.

The best narrow-module nominees were flat in the focal endpoint:

| comparator | relation retained by the nomination | focal n_degs |
|---|---|---:|
| `Lrp8` | BIOCARTA_LIS1_PATHWAY / developmental | 0 |
| `Reln` | BIOCARTA_LIS1_PATHWAY / developmental | 0 |
| `Pax6` | narrow module plus broad developmental | 0 |
| `Pak3` | narrow module plus synaptic fallback | 0 |
| `Stxbp1` | narrow module plus synaptic fallback | 1 |

Microtubule-adjacent fallbacks were also mostly self-only or nearly flat:
`Map1b = 1`, `Mapt = 1`, `Stmn2 = 1`, `Kif5a = 1`, `Kif1a = 1`,
`Tuba1a = 7`, `Map6 = 0`, and `Mapre2 = 1`.

Expanding the small Lrp8/Reln and Map1b/Mapt report neighborhoods returned 16
eligible multi-source training genes. Their counts summed to only 21, with
seven zeros and most nonzeros at one DEG. In the exact `151 TH Prkcd Grin2c Glut`
Parquet rows, the expanded microtubule and Reelin/Lrp8 comparators again
showed either no significant genes or a self-transcript-dominated one-gene
footprint.

## Synthesis

The training prior for this cell group starts at zero; the most defensible
available developmental and microtubule comparators stay at `0` or `1`; and
the Dcx bundle gives no evidence for a mature thalamic downstream program
large enough to move Dcx toward the long right tail. Exact Dcx RNA reach keeps
target engagement biologically possible, but in this design it is more likely
to produce no detectable DE or, at most, a self-transcript-only hit.

I therefore forecast the lower member of the near tie:

`predicted_n_degs = 0`
