# Direct forecast for Mpdz in 151 TH Prkcd Grin2c Glut

Target: `Mpdz`

Point prediction: `0`

## Evidence used

- The declared holdout manifest contains one target, `Mpdz`, and the focal
  endpoint is the number of BH-adjusted Wilcoxon `p < 0.05` genes in
  `151 TH Prkcd Grin2c Glut`.
- The selected same-experiment corpus has no `Mpdz` Findings or Claims
  exposed in the run-local release (`target_found=false`), so I used the
  biology-only bundle and the declared training measurements.
- Exact focal-population reach is not the limiting factor: `Mpdz` is measured
  and expressed in non-target focal nuclei
  (`65.0196%` of 23,679 nuclei; mean log1p CP10k `0.4895`; mean CP10k
  `0.8003`).
- The biological prior is weak for an acute postmitotic thalamic-neuron
  transcriptional footprint. The bundle identifies MPDZ as a large 13-PDZ
  junctional/polarity scaffold with strong mouse phenotypes in ependymal and
  choroid-plexus barrier contexts, not in the assayed NeuN-positive thalamic
  neurons. It also adjudicates functional stock by P37-P44 as
  `indeterminate`: editing should stop new MPDZ supply, but existing
  scaffolded complexes may persist and no target-specific neuronal turnover
  measurement was found.
- The focal training count table is strongly zero-inflated. Among 1,674
  training perturbations, 1,205 have `n_degs=0`, 276 have `n_degs=1`, only 65
  have 2-5 DEGs, and the top tail is dominated by broad RNA-processing,
  proteostasis, chromatin, or beta-catenin perturbations.
- I checked nearby structural or synaptic-scaffold / junction-associated
  training perturbations in the declared Parquet for the same group. They were
  observed with 108-280 matched perturbed nuclei and 17,259 measured rows each,
  so their null calls were not missing profiles. Their focal DEG counts were:

  | target | n_degs |
  | --- | ---: |
  | Crbn | 0 |
  | Ctnna2 | 0 |
  | Ctnna3 | 0 |
  | Ctnnbl1 | 1 |
  | Ctnnd2 | 1 |
  | Dlg4 | 1 |
  | Dlgap4 | 2 |
  | Homer2 | 0 |
  | Lrrc7 | 0 |
  | Magi2 | 0 |
  | Prkca | 0 |
  | Prkcg | 1 |
  | Shank2 | 0 |
  | Shank3 | 2 |
  | Sipa1l3 | 0 |
  | Syngap1 | 0 |

  `Ctnnb1` was excluded as a quantitative analog despite being
  junction-associated because its 383-DEG response reflects beta-catenin's
  transcriptional signaling role.

## Reasoning

The count distribution makes zero the modal forecast for ordinary biological
targets in this focal thalamic class. `Mpdz` is visible enough that a target
transcript change could in principle contribute a single DEG, but the atlas
portrait warns that self-transcript loss is not a reliable measure of edit
realization, and the matched structural-scaffold comparators mostly showed
zero or only self-dominated one-to-two-gene footprints. The source evidence
places Mpdz's strongest loss biology in non-neuronal barrier cells and leaves
acute depletion of pre-installed neuronal MPDZ complexes unresolved across the
21-28 day window. I therefore treated the high expression reach as confirming
assayability rather than a reason to move into the heavy response tail, and
used `0` as the most likely integer count.
