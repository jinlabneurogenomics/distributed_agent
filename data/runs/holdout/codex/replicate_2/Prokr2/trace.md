target_name: Prokr2
predicted_n_degs: 0

## Evidence

The declared holdout manifest contains a single target, `Prokr2`, and the declared 151 TH Prkcd Grin2c Glut count table has 1,674 training perturbations; `Prokr2` is absent from that table.

The canonical Prokr2 biology bundle is endpoint-blind.  Its exact in-assay focal reach is very sparse: only 188 of 23,679 non-target nuclei in `151 TH Prkcd Grin2c Glut` express `Prokr2` at all, 0.794%, with 218 total raw UMIs, mean raw UMI 0.00921, mean CP10K 0.00602, and pseudobulk CPM 0.577.  The source card supports Prokr2 as a seven-transmembrane prokineticin GPCR with selected adult thalamic expression, and the functional-stock card favors substantial depletion of a renewed receptor pool by P37-P44 after a P16 edit, but the depletion timing is not measured in postmitotic thalamic neurons and the germline circadian phenotype does not establish a large 21-28 day thalamic transcriptional program.

The endpoint itself is zero-heavy in this cell class.  In the declared training count table, 1,205/1,674 perturbations are 0, the median is 0, the 75th percentile is 1, the 90th percentile is 2, and the mean of 14.05 is driven by a long tail of spliceosome, proteasome, ubiquitin, and transcription/chromatin perturbations.

I nominated training-available biological analogs for `Prokr2` from the declared training universe with the local gene-analog nomination skill.  `Prokr2` was absent from the same-experiment ledger and no exact-complex/paralog, reciprocal-corpus-comparator, narrow-module, or direct-interaction candidate was available; all 904 nominees were broad functional fallbacks.  I therefore used only the direct peptide/class-A GPCR subset as weak operation-matched context rather than using the full fallback list as a scalar proxy.

The bounded direct-receptor cohort
`Npy1r`, `Npy2r`, `Npy5r`, `Hcrtr2`, `Avpr1a`, `Avpr1b`, `Cckar`, `Oxtr`,
`Ghsr`, `Gnrhr`, `Htr2c`, `Adra2a`, `Htr2a`, `Cckbr`, `Kiss1r`, `Adra1a`,
`Htr7`, `Oprm1`, `Htr4`, and `Tacr3` all have `n_degs = 0` in the declared
151-class training table.  A symmetric profile comparison over these 20 nodes
in the declared Parquet, filtered to `151 TH Prkcd Grin2c Glut`, found matched
profiles for all 20 and `no_significant_features` for all 20 at
`pvals_adj < 0.05`.  Corpus topology did recover receptor-family substructure
among the same 20 nodes, but it was broad and report-derived: all 20 were in
one component with 33/190 explicit-Finding-reference pairs, and no pair brought
in target-specific Prokr2 outcome evidence.

## Synthesis

The same-assay expression reach was the strongest downward quantitative bearing: the perturbation is aggregated over a thalamic class in which less than 1% of control nuclei show detectable `Prokr2`, so any cell-autonomous receptor effect would be heavily diluted unless those rare cells underwent a very broad survivor transcriptional state.  The biology bundle makes within-window loss plausible, not absent, but leaves latency, thalamic coupling, and Prokr1 compensation unresolved.  Against that prior, the declared training measurements show that closely analogous neuronal peptide/GPCR receptors were uniformly below the BH 0.05 DEG threshold in this exact cell class.

I therefore forecast the modal low endpoint, with the small chance of a rare-subtype response not large enough to move the point estimate away from zero.
