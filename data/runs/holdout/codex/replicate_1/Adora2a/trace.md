# Adora2a n_degs forecast

Target and endpoint:

- Target: `Adora2a`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05` in the focal population

Held-out-safe target biology:

- The biology bundle supports functional realization: `Adora2a` encodes the A2A membrane GPCR, disruptive editing should stop new receptor supply, receptor pools are dynamically renewed, and substantial functional-stock depletion over 21-28 days is favored in successfully edited expressing cells.
- Exact in-assay reach is very low in the focal population: 434 of 23,679 matched non-target nuclei expressed `Adora2a` in `151 TH Prkcd Grin2c Glut`, or 1.83%; mean raw target UMI was 0.0315 and pseudobulk CPM was 1.97. This makes a focal bulk survivor-state DE signature easy to dilute even if the edit works in the rare expressing nuclei.

Training-count scale in `151 TH Prkcd Grin2c Glut`:

- The declared count table has 1,674 training targets. It is strongly zero-inflated: 1,205 targets had 0 DEGs, 1,481 had at most 1 DEG, the median was 0, the 90th percentile was 2, and the mean was 14.05 because a small upper tail reached 2,677 DEGs.
- The upper tail was dominated by broad RNA-processing, chromatin, transcriptional, and proteostasis perturbations such as `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, `Zbtb7a`, `U2af2`, and `Psmb4`, so it was not the right quantitative scale for a sparsely expressed neuronal GPCR.

Training perturbations used as comparators:

- The typed gene-analog nomination placed purinergic, dopaminergic, adrenergic, adenylyl-cyclase, and cAMP regulators near `Adora2a` through Reactome/GO GPCR annotations, projected CORUM A2A receptor complexes, and STRING/annotation links.
- I gave most weight to the local GPCR/cAMP comparators rather than to broad synaptic fallbacks. In the focal count table, all of these selected measured comparators were zero: `P2ry12`, `Drd2`, `Drd4`, `Adra2a`, `Adcy1`, `Adcy3`, `Adcy5`, `Gnas`, `Gnal`, `Htr1a`, `Adrb2`, `Adrb3`, `Pde4b`, `Pde4d`, and `Pde10a`.
- Direct inspection of the declared Parquet rows in `151 TH Prkcd Grin2c Glut` confirmed 17,259 measured-gene rows for each of those 15 comparators and no BH-significant genes for any of them.
- A same-corpus explicit-Finding topology audit showed that the adenylyl-cyclase / dopamine / adrenergic / G-protein subset is not just a symbol pattern: 9 of 10 inspected GPCR/cAMP comparators formed one connected component with 26 explicit report-reference pairs. That topology was used only to support biological grouping; the measured focal DEG counts remained the endpoint evidence.

Synthesis:

`Adora2a` has plausible on-target receptor loss by harvest, but the focal class expresses it in only about 2% of recovered non-target nuclei and the most directly relevant measured GPCR/cAMP training perturbations were all transcriptionally silent at FDR 0.05 in the same focal population. A small nonzero count is biologically possible if the rare expressing cells are unusually responsive, but the endpoint is class-aggregated and BH-thresholded, so the most likely observed count is at the zero mode.

Point prediction: `0`
