# Ndufa13 DEG-count forecast

Target: `Ndufa13`

Focal population: `151 TH Prkcd Grin2c Glut`

Endpoint: number of measured genes in the focal perturbation contrast with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

## Evidence used

- The run binding manifest identifies `Ndufa13` as the single held-out task target and the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table as the focal training count table. `Ndufa13` is absent from the 1,674-row training table and from the declared training Parquet as a `gene_target`, so the forecast used only training perturbations plus the outcome-blind biology bundle.
- The canonical `Ndufa13` biology bundle reports strong focal target reach: in non-target `151 TH Prkcd Grin2c Glut` nuclei, `Ndufa13` is detected in 22,743 of 23,679 nuclei, or 96.047%, with mean raw UMI 4.51 and pseudobulk CPM 282.95.
- The same bundle places NDUFA13 in the mitochondrial inner-membrane complex-I holoenzyme. The perturbation should stop new NDUFA13 production, but the operative stock is installed complex I; the closest neuronal mitochondrial-protein turnover proxy has a median half-life near 25.7 days, comparable to the P16-to-P37/P44 interval. That makes a realized effect plausible but likely partial or leading-edge at harvest rather than an acute, complete loss of all complex-I activity.
- The focal training table is sparse overall: 1,205 of 1,674 training perturbations have `n_degs = 0`, and 1,481 of 1,674 have `n_degs <= 1`.
- The closest same-complex training perturbations were 19 other measured complex-I structural `Nduf*` subunits:
  `Ndufa10`, `Ndufa11`, `Ndufa12`, `Ndufa6`, `Ndufa8`, `Ndufa9`,
  `Ndufb10`, `Ndufb11`, `Ndufb3`, `Ndufb7`, `Ndufb8`, `Ndufb9`,
  `Ndufc2`, `Ndufs2`, `Ndufs4`, `Ndufs7`, `Ndufs8`, `Ndufv1`, and
  `Ndufv2`. Their focal counts were nine zeros and ten ones; none exceeded one DEG.
- Adjacent respiratory-chain training targets behaved the same way. The three complex-I assembly factors `Ndufaf2`, `Ndufaf4`, and `Ndufaf5` all had zero DEGs. Six complex-IV genes had five zeros and one one; five complex-III genes had three zeros and two ones.
- A direct Parquet check of the 19 structural complex-I subunits in `151 TH Prkcd Grin2c Glut` found 10 significant rows total. Nine were the targeted transcript itself (`Ndufa10`, `Ndufa6`, `Ndufb10`, `Ndufb11`, `Ndufb8`, `Ndufb9`, `Ndufc2`, `Ndufs2`, `Ndufs8`), and the remaining one-gene case was `Ndufv2` with significant `Cdc40`. Thus the direct analogs support a zero-or-one result, not a multi-gene mitochondrial stress program.
- A symmetric profile comparison over those 19 complex-I structural targets had complete pairwise coverage and classified 9 profiles as having no significant features and 10 as having only 1-to-9 significant features. The fixed-cohort diagnostic found no positive significant-program overlap across the 171 pairs and zero median negative significant-program overlap, consistent with isolated self-transcript events rather than a recurring high-count state.

## Synthesis

The biology says `Ndufa13` editing is expressed and mechanistically meaningful, but the stock that must be depleted is a preinstalled respiratory complex with turnover on the scale of the assay window. The training measurements say the closest complex-I structural losses in the exact focal population almost never produce downstream BH-significant transcriptional programs by P37-P44; their one-DEG outcomes are usually just significant loss of the target transcript. `Ndufa13` has enough focal mRNA prevalence for the self row to plausibly pass BH correction, so I place it slightly above the all-training median of zero, but the absence of any >1-DEG complex-I structural analog argues against forecasting a broader program.

Predicted `n_degs`: **1**
