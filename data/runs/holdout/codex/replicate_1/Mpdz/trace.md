target_name: Mpdz
target_context: 151 TH Prkcd Grin2c Glut

# Evidence used

- Declared inputs: the one-row manifest names `Mpdz`; the focal training count
  table is
  `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, with 1,674
  non-held-out targets and two columns, `target_name` and `n_degs`; the row-level
  training DE input is `training_de_all_cell_groups.parquet`.
- Training-count background in the exact focal population is strongly
  zero-heavy: 1,205/1,674 targets have 0 DEGs at BH-adjusted Wilcoxon
  p < 0.05, 276 have 1 DEG, the median is 0, the mean is 14.05, the 90th
  percentile is 2, and only 69 targets have at least 25 DEGs.
- The Mpdz canonical biology bundle reports exact focal expression in
  non-target 151 TH Prkcd Grin2c Glut nuclei: 15,396/23,679 nuclei express
  Mpdz, mean raw UMI is 1.2506, mean CP10k is 0.8003, and the feature is
  available. This establishes that a self-transcript DE row is measurable in
  this class, but it is not an observed Mpdz perturbation result.
- The same bundle places MPDZ as a 13-PDZ-domain scaffold incorporated into
  junctional/polarity/receptor assemblies. Mouse loss phenotypes are strongest
  in ependymal and choroid-plexus barrier cells; Patj/Inadl is a structural
  paralog; an acute P16 edit stops new MPDZ supply without directly dismantling
  installed MPDZ complexes. The bundle found no target-specific neuronal MPDZ
  turnover or residence time, so functional depletion by P37-P44 is
  indeterminate.
- The closest named partners or paralogs from the bundle, `Mpp5`/Pals1 and
  `Patj`, are absent from the 151 training count table, so there is no direct
  scale donor.
- I therefore checked indirect, training-observed scaffold, synaptic-adhesion,
  catenin/adhesion, and Rac/Cdc42-axis comparators in the declared 151 count
  table:

  | target | 151 n_degs | interpretation for Mpdz |
  |---|---:|---|
  | Cadm2 | 1 | synaptic adhesion, self-only/downstream-flat corpus profile |
  | Cdc42 | 1 | polarity/actin GTPase, self-only in 151 and downstream-flat corpus profile |
  | Celsr2 | 1 | adhesion/planar-polarity context, low-count self row |
  | Ctnna2 | 0 | cadherin/catenin context, quiet |
  | Ctnna3 | 0 | cadherin/catenin context, quiet |
  | Ctnnd2 | 1 | cadherin/catenin context, low-count self row |
  | Dlg4 | 1 | multi-PDZ PSD scaffold, self-only/downstream-flat corpus profile |
  | Dlgap4 | 2 | PSD scaffold with only one downstream 151 gene |
  | Myo5a | 1 | local cytoskeletal transport, self row |
  | Myo6 | 0 | local cytoskeletal transport, quiet |
  | Myo9a | 0 | Rho/myosin axis, quiet |
  | Rack1 | 2 | scaffold context, sparse |
  | Rac1 | 0 | Rac/Cdc42 axis, quiet in 151 |
  | Ctnnb1 | 383 | boundary: adhesion-adjacent but has a direct Wnt/TCF transcriptional branch not shared by Mpdz |

- Same-experiment corpus Findings, used as semantic interpretation rather than
  independent measurement, reinforced the count-table pattern: `Cadm2`, `Dlg4`,
  and `Cdc42` were downstream-flat despite self-transcript reductions in some
  groups; `Rac1` was largely buffered with only isolated singleton events away
  from 151; represented synaptic-adhesion, PSD, and Rac/Cdc42-actin relatives
  lacked a shared broad nuclear RNA module; `Dlgap4` was the sparse PSD
  exception; `Ctnnb1` was a thalamic Wnt/TCF responder and therefore a
  boundary rather than a magnitude analogue.
- A matched observed-profile comparison over the 14 comparator targets above
  in `151 TH Prkcd Grin2c Glut` confirmed the split visible in the counts:
  5/14 were completely FDR-flat, 8/14 had only 1-9 significant features, and
  only `Ctnnb1` had >=50 significant features. The lossless comparison is
  `workbench/mpdz_training_analogs_profile_compare.json`, with flat inspection
  in `workbench/mpdz_training_analogs_profile_inspect.json`.

# Synthesis

The forecast is anchored near zero because Mpdz is a postnatal structural
scaffold target with no exact represented partner, no demonstrated harvest-time
loss of installed neuronal MPDZ assemblies, and the closest measured structural,
adhesion, and Rac/Cdc42-axis perturbations in this class are null or
target-transcript-only. `Ctnnb1` shows that the 151 class can mount a large
adhesion-related transcriptional response, but the Ctnnb1 state is driven by
beta-catenin/Wnt transcriptional machinery rather than by junctional scaffold
loss, so I used it only as an upper boundary.

The reason to choose 1 rather than 0 is the exact focal expression of Mpdz:
the gene is measured in 65.0% of non-target 151 nuclei, and several expression-
reachable scaffold or adhesion perturbations with no downstream RNA program
still contribute exactly their own significantly reduced transcript to the
BH<0.05 count. Thus the most likely point is a single significant feature,
not a multi-gene downstream state.

predicted_n_degs: 1
