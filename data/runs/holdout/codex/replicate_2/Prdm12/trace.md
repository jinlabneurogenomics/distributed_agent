# Prdm12 direct forecast

## Target and endpoint

- Manifest target: `Prdm12`
- Requested context: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes in this focal class with BH-adjusted Wilcoxon `p < 0.05`
- Point forecast: `0`

## Evidence used

### Exact Prdm12 reach in the focal assay

The declared `biology_bundles/Prdm12.json` card reports essentially absent
baseline Prdm12 RNA in the matched non-target nuclei for
`151 TH Prkcd Grin2c Glut`:

- `n_non_target_cells`: 23,679
- `n_cells_expressing`: 30
- `pct_cells_expressing`: 0.1266945395%
- `total_target_umi`: 34
- `mean_raw_umi`: 0.0014358714
- `mean_log1p_cp10k`: 0.0006061184
- `pseudobulk_cpm`: 0.0899911554

This exact in-assay reach was the strongest piece of endpoint-facing evidence.
Even if a guide disrupts Prdm12 efficiently, almost none of the nuclei in the
aggregated recovered thalamic class appear to contain active Prdm12 transcript
at baseline.

### Prdm12 functional biology

The same card adjudicates PRDM12 as a dynamic nuclear transcriptional regulator
whose functional stock is likely substantially depleted by the P37-P44 harvest
after P16 editing. That supports the possibility of a real perturbation where
PRDM12 is present. It is also qualified by:

- no target-specific PRDM12 protein half-life or chromatin-residence estimate in
  postmitotic neurons;
- adult functional evidence from peripheral nociceptors and hypothalamic Pomc
  neurons rather than this thalamic population;
- postnatal Prdm12 expression in a restricted zona-incerta/thalamic-associated
  domain rather than broad thalamic coverage.

So the operation should be biologically meaningful in the rare expressing cells,
but the card does not support a large class-aggregate transcriptional footprint.

### Held-in endpoint distribution

The declared training table
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` contains 1,674 held-in
targets. It is highly zero-inflated:

- 1,205 / 1,674 targets have `n_degs = 0`;
- median `n_degs = 0`;
- 75th percentile `n_degs = 1`;
- 90th percentile `n_degs = 2`;
- only 58 / 1,674 exceed 50 DEGs.

I recomputed the focal-class DEG totals directly from
`training_de_all_cell_groups.parquet`; the 1,674 per-target counts exactly
matched the declared count table. The focal class has 17,259 measured-gene rows
per retained target in this Parquet slice.

The observed matched perturbed-nucleus counts for held-in targets in this focal
class ranged from 23 to 419, with a median of 177. At the Prdm12 baseline
expression fraction of 0.1267%, a typical matched perturbed cohort would contain
far below one Prdm12-RNA-positive nucleus. This makes a BH-significant
whole-class signature unlikely unless the true functional target population is
much larger than the exact non-target expression measurement implies.

### Training perturbations used as biological comparators

Typed analog nomination against the actual 1,674-gene training universe found
no close Prdm12 paralog, complex partner, direct dependency, narrow module, or
bidirectional same-corpus comparator. Prdm12 itself was also absent from the
same-experiment Finding and Claim corpus.

The nominator returned only broad functional-fallback comparators, mostly genes
sharing neuronal or RNA-polymerase-II transcription-factor annotations. Among
its first ten available candidates, 9 of 10 had zero focal-class DEGs:

| candidate | focal `n_degs` |
| --- | ---: |
| Gata3 | 0 |
| Ctnnb1 | 383 |
| Nfix | 0 |
| Foxa2 | 0 |
| Nfia | 0 |
| Nfib | 0 |
| Isl1 | 0 |
| Smad4 | 0 |
| Pax6 | 0 |
| Pparg | 0 |

The explicit-report topology over that top broad-fallback set was fragmented
into five components with only 6 connected pairs among 45 possible pairs, so I
did not treat it as a tight transferable module.

Other broad Prdm-family fallbacks were mostly silent in the same endpoint:

- `Prdm16`: 0
- `Prdm5`: 0
- `Prdm2`: 0
- `Prdm10`: 52

`Prdm10` was the one active PRDM-family fallback, but its same-experiment
Parquet profile was broader, with significant genes in many cell classes, and
the analog evidence for all four PRDM genes was only broad functional annotation
rather than close paralogy or shared same-experiment structure.

## Synthesis

The direct endpoint prior in `151 TH Prkcd Grin2c Glut` is already a zero DEG
for most targets. PRDM12 being a transcriptional regulator raises the
possibility of a real downstream program, but the exact focal expression
measurement pushes the forecast back down: only 30 of 23,679 matched control
nuclei expressed Prdm12, with 34 total UMIs. In an assay that tests the whole
aggregated recovered class, a rare Prdm12-positive subpopulation is expected to
be diluted below FDR detection.

The held-in biology checks agree with that interpretation. Broad developmental
or transcription-factor analogs are usually silent in this cell class, close
Prdm12 analog evidence was absent, and three of four PRDM-family fallback
candidates had zero focal-class DEGs. A small nonzero signature remains possible
if Prdm12 had an undetected low-RNA functional population or a persistent P16
state not visible at harvest, but the exact reach and training endpoint
distribution make zero the most defensible integer forecast.

Therefore:

`predicted_n_degs = 0`
