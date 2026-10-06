# Fgf14 DEG-count forecast

Target: `Fgf14`
Cell group: `151 TH Prkcd Grin2c Glut`
Predicted `n_degs`: `1`

## Evidence used

- The declared target bundle reports exact focal-population expression for the
  withheld target: `Fgf14` was detected in 18,223 of 23,679 non-target nuclei in
  `151 TH Prkcd Grin2c Glut` (`76.958%`) with mean CP10K `1.09798`. The target
  transcript is therefore present and measurable in this focal population, while
  the bundle explicitly does not expose the held-out perturbation signature.
- The same biology bundle places FGF14 in the intracellular FHF family and
  describes it as a dynamic regulator of voltage-gated sodium-channel complexes.
  Its functional-stock adjudication concluded that a P16 disruptive edit should
  likely deplete newly renewed FGF14 by the P37-P44 harvest, but only with
  partial completeness because no matched endogenous FGF14 half-life in
  postmitotic thalamic neurons was available.
- The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains
  1,674 training perturbations. The focal count distribution is extremely
  sparse: median `0`, 75th percentile `1`, 95th percentile `18`, 99th percentile
  `430`, and 1,205 of 1,674 perturbations are zero.
- Directly related FHF and channel comparators queried from the declared
  `training_de_all_cell_groups.parquet` were small in the focal class:
  `Fgf12` had `0` DEGs and `Fgf13` had `2`; `Scn1a`, `Scn2a`, `Scn8a`, and
  `Scn1b` had `1`, `1`, `1`, and `2`; `Kcnq2` and `Kcnq3` each had `1`;
  `Cacna1a` had `0`; `Cacna1g` had `12`.
- I treated the larger counts for less direct excitability or identity genes as
  boundary cases rather than central comparators: `Atp1a3`, `Atp2a2`, and
  `Rora` had `80`, `187`, and `278` focal DEGs, but they implicate ATPase,
  ER-calcium, or nuclear-receptor programs rather than an FHF accessory
  regulator of Nav gating.

## Reasoning

The exact expression measurement makes a detectable perturbation possible, and
the 21-28 day P16-to-harvest interval should usually allow a renewable channel
regulator to turn over. That supports a nonzero point over a hard null.

At the same time, the best training analogs indicate that acute perturbation of
sodium-channel subunits, Kv subunits, and the closest assayed FHF paralogs
produced self-only or nearly self-only signatures in this thalamic focal class.
FGF14 loss is therefore much more likely to sit with the 0-2 DEG FHF/channel
group than with broad transcriptional, RNA-processing, proteostasis, or
cell-stress perturbations. I predict a detectable but tiny survivor-conditioned
RNA signature, centered on one significant measured gene.
