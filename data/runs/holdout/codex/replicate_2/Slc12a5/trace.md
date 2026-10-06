# Slc12a5 direct DEG-count forecast

Target: `Slc12a5`

Cell class: `151 TH Prkcd Grin2c Glut`

Predicted `n_degs`: `1`

## Evidence used

### Target biology and reach

The canonical biology bundle for `Slc12a5` supports functional reach in the
focal thalamic population:

- Exact non-target expression in `151 TH Prkcd Grin2c Glut` was high:
  `22,251 / 23,679` nuclei expressed `Slc12a5`, with
  `pct_cells_expressing = 93.9693`, `mean_raw_umi = 4.2467`, and
  `mean_log1p_cp10k = 1.1689`.
- KCC2/Slc12a5 is a neuron-enriched K-Cl cotransporter that maintains low
  intracellular chloride for hyperpolarizing GABAergic inhibition.
- The P16 edit has a biologically plausible chance to deplete operative KCC2 by
  P37-P44: the declared functional-stock adjudication called KCC2 a
  continuously renewed membrane/intracellular pool and concluded
  `functional_stock_by_harvest = likely_substantially_depleted`, based on mouse
  conditional-loss studies with substantial protein loss inside the 21-28 day
  screen interval.
- The main uncertainty is readout coupling. Prior KCC2 loss phenotypes are
  electrophysiological, seizure, and survival phenotypes mostly in hippocampal,
  forebrain, or cerebellar neurons. They establish that loss can matter in
  mature neurons, but not that surviving thalamic relay nuclei must mount a
  large nuclear RNA program.

### Same-class endpoint distribution

The declared training table for `151 TH Prkcd Grin2c Glut` contains 1,674
observed biological perturbations.

- Distribution of `n_degs`: median `0`, mean `14.05`, 75th percentile `1`,
  90th percentile `2`, 95th percentile `18`, maximum `2677`.
- Only `469 / 1674` training targets had any BH-adjusted Wilcoxon hit in this
  class.

The closest same-cell-class functional analogs I used were neuronal membrane
transport, inhibitory synapse, excitatory synapse, and channel/scaffold
perturbations:

| target | n_degs |
| --- | ---: |
| Slc12a2 | 0 |
| Slc6a1 | 0 |
| Gabra1 | 1 |
| Gabrb2 | 4 |
| Gabrg2 | 1 |
| Arhgef9 | 1 |
| Grin1 | 89 |
| Grin2a | 1 |
| Grin2b | 2 |
| Gria1 | 0 |
| Kcnq2 | 1 |
| Kcnq3 | 1 |
| Scn2a | 1 |
| Scn8a | 1 |
| Shank2 | 0 |
| Shank3 | 2 |
| Dlg4 | 1 |

This cohort had a median of `1` DEG; `16 / 17` targets were at `0-4` DEGs and
only the obligatory NMDA receptor subunit `Grin1` produced a broader response
at `89` DEGs.

### Parquet profile check

I queried the declared training expression Parquet for the same analog cohort in
`151 TH Prkcd Grin2c Glut`.

- The runtime comparison classified 4 analog profiles as having no significant
  features, 12 as having 1-9 significant features, and only `Grin1` as having at
  least 50 significant features.
- Direct Parquet rows showed that most one-DEG examples were self-transcript
  calls: `Gabra1`, `Gabrg2`, `Arhgef9`, `Dlg4`, `Grin2a`, `Kcnq2`, `Kcnq3`,
  `Scn2a`, and `Scn8a` had only their own target transcript at
  `pvals_adj < 0.05`.
- Low-count profiles did not share a strong significant program across the
  136 pairwise analog comparisons; the selected cohort's positive and negative
  significant-overlap coefficients were both `0`.

## Synthesis

`Slc12a5` should be reachable in the assayed class: it is expressed in nearly
all focal nuclei, encodes a required renewable membrane transporter, and KCC2
protein can be depleted on the screen's time scale. Those facts push the
forecast above a hard zero, especially because the endpoint includes the target
transcript itself and the training Parquet showed many low-burden synaptic
perturbations with exactly one self-transcript DEG.

I did not project a broad `Grin1`-like response onto `Slc12a5`. KCC2 loss has a
clear electrophysiological phenotype, but most observed receptor, GABAergic,
ion-channel, and synaptic-scaffold perturbations in this thalamic class had
zero to a few DEGs; their few calls were mostly self knockdown rather than a
coherent downstream state. Survivor conditioning also weakens any expectation
that severe chloride dysregulation must appear as many recovered-cell nuclear
RNA changes.

The resulting direct point forecast is:

```tsv
target_name	predicted_n_degs
Slc12a5	1
```
