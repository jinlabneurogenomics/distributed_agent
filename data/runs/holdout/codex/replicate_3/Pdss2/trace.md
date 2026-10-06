# Direct Pdss2 forecast

Target: `Pdss2`

Cell class: `151 TH Prkcd Grin2c Glut`

Predicted `n_degs`: `0`

## Evidence used

- The declared one-row manifest names `Pdss2`; `Pdss2` is absent from the 1,674-row training count table and has no rows in the declared training Parquet, so no held-out endpoint or held-out signature was used.
- The target biology bundle shows measurable focal-population reach: `Pdss2` was detected in 12,352 of 23,679 non-target `151 TH Prkcd Grin2c Glut` nuclei, or 52.16%, with mean CP10K 0.501. This made a true perturbation effect biologically reachable, not ruled out by absence of target RNA.
- The same bundle places the perturbation in mitochondrial CoQ biosynthesis: Pdss2/Pdss1 synthase supplies the CoQ polyisoprenoid side chain. A P16 disruptive edit should stop new Pdss2-dependent synthesis, and product stock is expected to decline substantially by P37-P44, but pre-existing synthase and CoQ are not chemically eliminated at editing; the closest postnatal neural Pdss2 phenotype was a many-month Purkinje-cell degeneration rather than a 21-28 day thalamic neuron response.
- The declared `151 TH Prkcd Grin2c Glut` count table is strongly zero-inflated: 1,205 of 1,674 training perturbations have `n_degs=0`, the median is 0, and only 193 targets have more than one DEG.
- The most direct measured pathway neighbor in the training table, `Coq5`, has `n_degs=0` in `151 TH Prkcd Grin2c Glut`. Same-experiment corpus Findings also summarize `Coq5` as a pan-neuronal buffered transcriptomic surface with no FDR-resolved CoQ-biosynthesis marker.
- Other proximal mitochondrial electron-transfer comparators were nearly flat in the same class at the requested `pvals_adj < 0.05` threshold:
  - represented complex III targets `Cyc1`, `Ttc19`, `Uqcrb`, `Uqcrc2`, `Uqcrfs1`, `Uqcrh`, and `Uqcrq` summed to 4 DEGs, with no member above 1;
  - represented complex IV targets `Coa8`, `Cox11`, `Cox4i1`, `Cox5a`, `Cox6a1`, `Cox7b`, `Cox8a`, and `Ndufa4` summed to 2 DEGs, with no member above 1;
  - represented complex I and complex-I assembly targets from the corpus complex-I claim summed to 7 DEGs across 16 targets, again with no member above 1.
- A direct profile comparison over 40 CoQ/OXPHOS/mitochondrial proteostasis targets in the exact thalamic class gave 24 targets with no significant genes, 15 targets with only 1-9, and a single larger boundary, `Opa1`, with 37. `Opa1` is informative mainly as a boundary because its corpus Findings place it in an ATF4/ISR-like mitochondrial dynamics stress state, while the complex I, III, IV, and `Coq5` ledgers repeatedly report flat, singleton, or nonconvergent respiratory-chain surfaces.

## Synthesis

`Pdss2` is not an expression-null or an implausible edit: the target RNA is present in roughly half of recovered thalamic neurons, and CoQ resupply should begin to fail during the P16-to-P37/P44 window. That evidence argues against treating the perturbation as completely unreachable.

The endpoint, however, is acute survivor-conditioned nuclear snRNA differential expression. In the declared training data, direct CoQ biosynthesis and respiratory-chain perturbations are usually buffered on that endpoint in this exact class, even when their genes should matter for mitochondrial function. The strongest local analogue, `Coq5`, is exactly zero; the broader OXPHOS cohort is zero-or-singleton; and the only clearly larger mitochondrial response in this neighborhood, `Opa1`, represents a different mitochondrial dynamics/ISR route that the same-experiment corpus explicitly separates from generic OXPHOS loss.

I therefore put the point forecast at the zero mode/median of the CoQ/OXPHOS analogs rather than lifting it toward the global training mean or toward the `Opa1` boundary.
