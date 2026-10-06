# Tnfrsf1b direct n_degs forecast

Target: `Tnfrsf1b`

Focal population: `151 TH Prkcd Grin2c Glut`

Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.

## Deciding evidence

- The canonical biology bundle supports realized molecular loss but only conditional endpoint coupling. TNFR2 is a renewable surface TNF receptor and its pre-edit stock is expected to be substantially depleted by the P37-P44 harvest after P16 editing, but the timing evidence is partial and the documented postnatal neuronal loss phenotype is from hippocampal excitotoxic challenge rather than unchallenged thalamic neurons.
- Exact in-assay reach is extremely low in the focal control population: 120 of 23,679 non-target nuclei expressed `Tnfrsf1b`, `pct_cells_expressing = 0.506778%`, `mean_raw_umi = 0.00536`, and `pseudobulk_cpm = 0.336`. This exact reach supersedes the qualitative bulk expression prior and makes any basal effect heavily restricted or diluted in the aggregated 151 thalamic neuronal class.
- The focal training count table is dominated by very small values: 1,205/1,674 training perturbations have `n_degs = 0`, 1,481/1,674 have `n_degs <= 1`, the median is 0, and the 90th percentile is 2. Thus a zero or singleton forecast is the natural local scale for a sparse receptor with weak basal engagement.
- The closest represented TNF/NF-kB/death-receptor/cytokine-receptor training perturbations are flat in the same focal class. The declared count table gives `n_degs = 0` for `Tnfrsf1a`, `Traf3`, `Nfkb1`, `Chuk`, `Fas`, `Ngfr`, `Ifnar1`, `Ifnar2`, `Ifngr1`, `Ifngr2`, `Il1r1`, `Il1rap`, `Rel`, `Stat2`, `Stat3`, `Tnfrsf11a`, `Tnfrsf13c`, `Tnfrsf4`, and `Tnfrsf9`; `Stat1` is the only screened item in this set with a singleton focal call. Direct Parquet aggregation over these genes confirmed zero BH<0.05 genes in the 151 class for the listed zero-count targets.
- The same-experiment corpus interprets those exact training results as a coherent basal-context silence rather than an isolated failed paralog: `Chuk:F003` and `Nfkb1:F002` place `Tnfrsf1a`, `Traf3`, `Chuk`, `Nfkb1`, `Rel`, TLR, and IL-1/TNF-side perturbations in a broadly silent unchallenged postnatal neuronal TNF/TLR/IL-1-to-IKK/NF-kB/JNK/p38 module; `Fas:F003` finds no reusable TNF-family death-receptor module; `Ngfr:F003` similarly reports flat or uncoupled p75/death/NF-kB neighbors; and `Stat1:F002` reports a flat unliganded IFN/STAT neighborhood. These corpus statements are interpretive views of the same training experiment, not independent replication.

## Synthesis

`Tnfrsf1b` is not rejected as an ineffective perturbation: its receptor stock should plausibly decline within 21-28 days. The limiting evidence is instead endpoint reach. Only about half a percent of recovered non-target focal nuclei contained detectable `Tnfrsf1b` RNA, and the supplied phenotypes require excitotoxic, inflammatory, glial-developmental, or other unmatched contexts. In the declared training measurements, the closest tonic receptor and downstream NF-kB/STAT axes are exact zeros or at most singleton responses in `151 TH Prkcd Grin2c Glut`.

A rare TNFR2-positive subpopulation could in principle contribute one or a few aggregate calls, so zero is uncertain rather than guaranteed. Still, the low exact reach plus task-matched quiet TNF/NF-kB/cytokine comparators put the forecast at the lower bound.

Predicted `n_degs`: **0**
