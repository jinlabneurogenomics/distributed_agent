# Direct Trhr DEG-count forecast

## Target and endpoint

Target: `Trhr`

Cell class: `151 TH Prkcd Grin2c Glut`

Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the focal cell class.

The declared count table for this cell class contains 1,674 training perturbations and does not contain `Trhr`. In that table, 1,205/1,674 perturbations have `n_degs = 0`, 276 have `n_degs = 1`, and only 193 have more than one DEG.

## Target biology

The exact Trhr focal-population reach in the declared `Trhr.json` biology bundle is extremely small: 155 of 23,679 non-target nuclei in `151 TH Prkcd Grin2c Glut` expressed Trhr, with 190 total Trhr UMIs, `pct_cells_expressing = 0.6546`, `mean_raw_umi = 0.0080`, and `mean_log1p_cp10k = 0.00355`.

The biology bundle identifies Trhr as a TRH class-A peptide GPCR acting through phosphatidylinositol/IP3-calcium/PKC signaling. A disruptive edit should block new functional receptor production, but the functional-stock adjudication is unresolved by P37-P44: endogenous neuronal TRHR degradation kinetics were not found, and trafficking/recycling evidence did not establish receptor-pool destruction. So the target has a plausible molecular operation, but in this assay window it combines very low local expression with indeterminate post-edit depletion of pre-existing receptor protein.

## Training evidence used

I used the deterministic annotation store only to choose prior-matched training perturbations, then read their focal `n_degs` from the declared count table.

- `Trhr` belongs to `functional_class:gpcr`, `MSigDB:CP:WIKIPATHWAYS` `WP_GPCRS_PEPTIDE`, GO `phospholipase C-activating G protein-coupled receptor signaling pathway`, KEGG `Neuroactive ligand-receptor interaction`, and Reactome `G alpha (q) signalling events`.
- Among 95 training targets in the curated GPCR functional class, 85 had `n_degs = 0`, the other 10 had `n_degs = 1`, and no GPCR had `n_degs > 1`.
- The narrower peptide-GPCR WikiPathways set was even quieter: 29/29 training targets had `n_degs = 0`.
- The GO phospholipase-C GPCR set had 37 training targets: 32 had `n_degs = 0`, five had `n_degs = 1`, and none had more than one.
- The Reactome peptide-ligand-binding set had 29 training targets: 28 had `n_degs = 0`; `App` was the only nonzero member, with `n_degs = 1`.

I also spot-checked the corresponding rows in `training_de_all_cell_groups.parquet` for the focal class. This Parquet is the same experimental representation used to make the count table, not independent replication, but it showed that the 29 WikiPathways peptide-GPCR training perturbations each had 17,259 measured focal rows and zero rows with `pvals_adj < 0.05`; the smallest adjusted p-value in that whole set was Cxcr4 at 0.067.

## Synthesis

Large focal signatures in this atlas are enriched for core, broadly used intracellular processes, whereas the training receptor perturbations closest to Trhr were virtually all exact zeros. Trhr also has lower expected detectability than many of those assayed receptors because only about 0.65% of matched focal non-target nuclei had any Trhr transcript, and the biology card does not establish that a P16 edit depletes the operative receptor pool by the P37-P44 harvest.

The most likely integer count is therefore the floor of the matched receptor distribution, not the one-DEG shoulder.

Predicted `n_degs`: 0
