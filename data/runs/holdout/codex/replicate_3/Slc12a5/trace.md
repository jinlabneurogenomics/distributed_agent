# Direct Slc12a5 n_degs forecast

## Forecast

`Slc12a5` in `151 TH Prkcd Grin2c Glut`: **1 DEG**.

## Evidence

- The declared holdout manifest names the single target as `Slc12a5`; `Slc12a5` is absent from the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, so no target count or target signature was used.
- The declared biology bundle gives strong focal reach: in the exact `151 TH Prkcd Grin2c Glut` non-target expression calculation, `Slc12a5` was detected in 22,251 of 23,679 nuclei, with 93.97% expressing nuclei, mean 2.56 cp10k, and 266 pseudobulk CPM.
- The same bundle supports actual functional realization before harvest: KCC2 is a renewable neuronal membrane K-Cl cotransporter; conditional mouse experiments show substantial KCC2 protein depletion within 10 days and functional phenotypes within the 21-28 day experimental window. The bundle also flags survivor conditioning as unresolved, so severe KCC2 loss can be muted by the recovered-nucleus readout.
- The focal training count table is sparse: 1,205 of 1,674 visible perturbations have `n_degs = 0`, 276 have `n_degs = 1`, 193 have at least 2, and the nonzero median is 1.
- Chloride/GABA/excitability perturbations measured in the same focal class are mostly zero or near one: `Slc12a2` 0, `Slc6a1` 0, `Slc32a1` 0, `Slc4a7` 0, `Slc9a9` 0, `Stk39` 0, `Wnk1` 0, `Wnk3` 1, `Clcn4` 1, `Gabra1` 1, `Gabrg2` 1, `Gabrd` 2, `Gabrb2` 4. `Cacna1g` is the closest thalamic excitability perturbation with a broader but still modest footprint at 12.

## Synthesis

The biological prior argues against a pure no-engagement forecast: `Slc12a5` is broadly expressed in the focal thalamic glutamatergic population, KCC2 stock should turn over within the 3-4 week perturbation window, and loss of KCC2 is not cleanly redundant with KCC3 in tested neurons. That makes one detectable feature plausible even if the effect is not a classical transcription-factor program.

The quantitative training evidence keeps the point near the floor. The most task-matched transporter, GABA receptor, and WNK/SPAK-side chloride-regulation perturbations in this class are concentrated at 0-1 significant genes, with their significant rows often being the targeted transcript itself rather than a broad downstream state. Since KCC2 loss primarily changes membrane chloride extrusion and excitability, while the endpoint counts nuclear RNA DE only in recovered nuclei, I expect a self or immediate local feature to pass BH FDR but not a wide stress or survival program.

The resulting point forecast is `n_degs = 1`.
