# Direct DEG-count forecast for Igf2r

Target perturbation: `Igf2r`

Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with
BH-adjusted Wilcoxon `p < 0.05`.

## Evidence used

- Declared target biology bundle for `Igf2r`: the target RNA was present in the
  focal population (`12,641 / 23,679` non-target nuclei expressing; `53.38%`,
  mean raw UMI `0.856`; perturbation contrast feature available). The functional
  stock card adjudicated IGF2R/CI-MPR as `likely_substantially_depleted` by the
  P37-P44 harvest because a disruptive edit should stop receptor resupply, CI-MPR
  turns over on a day scale in PC12 cells, and adult neuron-directed Cre reduced
  hippocampal receptor and function within two weeks.
- That biology argues Igf2r is an engaged, expressed target, but not an
  obviously catastrophic thalamic regulator. IGF2R is a multifunctional
  mannose-6-phosphate/IGF2 trafficking receptor; M6PR and other lysosomal cargo
  routes provide unresolved buffering for some hydrolase traffic, and the
  closest mature-neuron phenotype was adult hippocampal memory impairment rather
  than acute broad neuronal stress.
- The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table is
  strongly zero-inflated: `1,205 / 1,674` held-in targets have `0` DEGs, the
  median is `0`, the 75th percentile is `1`, the 90th percentile is `2`, and the
  95th percentile jumps to `18`. The large responses in this class are
  concentrated in spliceosome, proteasome/ubiquitin, transcriptional, and core
  trafficking regulators, e.g. `Uba5` at `2,677`, `Tpr` at `1,768`, `Sin3a` at
  `1,433`, and `Rab7` at `501`.
- I treated the closest measured comparators as IGF/insulin receptors and
  endolysosomal or M6P-cargo genes rather than broad essential complexes. In the
  focal training count table, `Igf1r`, `Insr`, `Sort1`, `Atp6v1a`, `Vps41`, and
  `Lamp2` have `0` DEGs; `Gaa`, `Ctsb`, and `Atp6v0a1` have `1`; `Atp6ap2` and
  `Mtor` have `2`. The only clear larger local responses in this hand-selected
  neighborhood were more central regulators: `Vps35` at `17`, `Vps54` at `31`,
  `Tsc2` at `86`, and `Rab7` at `501`.
- Direct parquet inspection of selected comparators in the exact focal class
  confirmed that the low-count analogs were genuinely quiet, not count-table
  artifacts: `Igf1r`, `Insr`, and `Sort1` each had `0` significant measured
  genes among `17,259`; `Gaa` and `Atp6v0a1` each had exactly `1`, and in both
  cases that feature was the perturbed gene itself. The profile comparison of
  the endolysosomal cohort likewise separated zero or self-only receptor/cargo
  profiles from `Vps35` and especially from the broad `Rab7` state.

## Synthesis

Igf2r should be expressed and functionally depleted by the harvest window, so I
did not put the forecast at a pure inexpressed-target null. At the same time,
the training perturbations most analogous to a single receptor or lysosomal
cargo branch are overwhelmingly at `0-1` DEGs in this class, while the training
perturbations that reach tens or hundreds are core endosomal, nutrient-signaling,
or proteostasis nodes with broader cell-state consequences.

The point estimate is therefore a minimal detectable response: most likely the
self transcript or one closely downstream lysosomal/trafficking feature, without
a broad thalamic stress signature.

Predicted `n_degs`: `1`
