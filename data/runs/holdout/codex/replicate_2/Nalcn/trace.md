# Nalcn n_degs forecast

## Declared target and endpoint

- Target manifest: `Nalcn`.
- Requested endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Declared measurement surface used for training observations:
  - `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
  - `training_de_all_cell_groups.parquet`, restricted to `group_name == "151 TH Prkcd Grin2c Glut"`
- The visible count table contains 1,674 training targets and no `Nalcn` row.

## Target biology

The canonical `Nalcn` biology bundle points upward from the screen-wide null mode but does not justify a broad stress/regulatory footprint:

- In the focal class, `Nalcn` is a measured and widely expressed transcript: 19,324 of 23,679 non-target nuclei express it, or 81.608%.
- Functional stock is expected to be `likely_substantially_depleted` over the P16 edit to P37-P44 harvest interval. The key support is that NALCN itself forms the neuronal background cation channel and a postnatal mouse neural knockdown produced target and functional changes on an 8-21 day clock.
- The loss phenotype is supported in another postnatal neural context, and no close paralog or same-context replacing channel was identified. That argues against treating `Nalcn` as an unexpressed or persistent-stock zero.
- The same evidence remains incomplete for the exact aggregate thalamic context: the timing anchor is from lateral parabrachial glutamatergic neurons, not the assayed thalamic class, and the bundle does not claim an exact thalamic Perturb-seq response size.

## Training count scale

The focal training count table is strongly zero-inflated:

- 469 / 1,674 training targets have any DEG.
- Median = 0; 75th percentile = 1; 90th percentile = 2; 95th percentile = 18.
- The largest counts are broad housekeeping/regulatory lesions, for example `Uba5 = 2677`, `Tpr = 1768`, `Sin3a = 1433`, spliceosome/proteasome components, and transcriptional regulators. I did not use that extreme upper tail for `Nalcn`.

The closest measured `Nalcn` channel-complex genes `Unc79`, `Unc80`, `Fam155a`, and `Fam155b` were absent from the training count table, so I used operation-adjacent thalamic excitability genes instead.

Voltage-channel and leak/excitability comparators were mostly weak:

| comparator set | visible members used | n_degs pattern |
|---|---|---|
| voltage/Ca/Na/HCN/KCNQ channels | `Cacna1a`, `Cacna1d`, `Cacna1e`, `Cacna1g`, `Hcn1`, `Hcn2`, `Scn1a`, `Scn2a`, `Scn8a`, `Kcnq2`, `Kcnq3` | median 1, mean 1.64, maximum 12 at `Cacna1g` |
| NMDA receptor subunits | `Grin1`, `Grin2a`, `Grin2b`, `Grin2d` | `Grin1 = 89`, but the other subunits were 0-2 |
| calcium-signaling/homeostasis effectors | `Atp2b1`, `Atp2b2`, `Atp2b3`, `Calm1`, `Calm2`, `Calm3`, `Ppp3ca`, `Ppp3cc`, `Ppp3r1` | median 1, with a modest upper bracket of `Ppp3r1 = 9`, `Calm1 = 14`, `Atp2b1 = 22` |

The exact Parquet rows in the focal class reproduced the table counts for these comparators. Their matched perturbed-nucleus counts were in a low hundreds regime for the main anchors, e.g. `Cacna1g` 264, `Calm1` 208, `Atp2b1` 146, `Ppp3r1` 93, and `Grin1` 247, with 23,679 matched controls.

## Profile interpretation

I compared 19 preselected training profiles spanning calcium channels, sodium channels, HCN/KCNQ channels, NMDA subunits, `Atp2b1`, `Calm1`, `Ppp3r1`, and `Gnas`, restricted to `151 TH Prkcd Grin2c Glut`.

The profile comparison found no missing training profiles. Response breadths for the main nonzero anchors were:

- `Grin1`: 89 significant genes, a clear upper-scale excitatory receptor comparator.
- `Atp2b1`: 22 significant genes.
- `Calm1`: 14 significant genes.
- `Cacna1g`: 12 significant genes.
- `Ppp3r1`: 9 significant genes.

Inspected pairwise views showed no shared FDR-significant genes between these modest anchors and the lower-count channel peers in the requested focal-vs-peer pairs. Several whole-profile Pearson/cosine values were positive, but the significant-program intersections were zero, so I treated these as loose magnitude anchors rather than as one coherent DEG module that should be averaged or extrapolated.

## Point synthesis

`Nalcn` should be above the zero/one channel median because it is expressed in 81.6% of the focal non-target nuclei, it supplies a nonredundant resting leak conductance, and its channel stock should be depleted by harvest. The perturbation still looks unlike the screen's high-count regulatory lesions, and the most proximal measured ion-channel perturbations show sparse signatures. `Grin1 = 89` is a useful upper boundary for a neuronal excitability gene with a broader synaptic receptor footprint, not a direct point anchor for a background leak channel.

I therefore placed `Nalcn` at the top of the observed thalamic voltage-channel range and inside the modest 9-22 calcium/excitability bracket. `Cacna1g = 12` is the nearest same-class thalamic channel scale, with `Ppp3r1 = 9`, `Calm1 = 14`, and `Atp2b1 = 22` supporting a low-double-digit rather than zero forecast.

Predicted `n_degs`: **12**.
