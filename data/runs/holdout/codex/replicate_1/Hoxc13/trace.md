# Direct outcome-blind forecast for Hoxc13

## Endpoint

- Target: `Hoxc13`
- Cell population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Point prediction: `0`

## Evidence used

1. The declared biology-only Hoxc13 bundle reports effectively absent focal-population expression: 2 expressing nuclei among 23,679 matched non-target `151 TH Prkcd Grin2c Glut` nuclei, `pct_cells_expressing = 0.0084463`, `pseudobulk_cpm = 0.0052936`, and `mean_raw_umi = 0.000084463`.

2. The same bundle supports Hoxc13 as a free nuclear DNA-binding transcription factor whose protein stock should substantially decline during the P16-to-P37/P44 edit window if the gene is productively edited and expressed. That realization prior is conditional on target expression. The observed expression reach says the assayed thalamic glutamatergic population had essentially no Hoxc13 transcript to begin with.

3. The external/source-card biology in the bundle is non-neural: strong Hoxc13 phenotypes and expression are in hair follicles, vibrissae, nails, tongue papillae, tail, and other ectodermal appendage contexts. The card found no postnatal thalamic-neuron conditional-loss evidence. That makes a large immediate survivor-conditioned RNA program in `151 TH Prkcd Grin2c Glut` biologically unsupported.

4. The exact `151 TH Prkcd Grin2c Glut` training count table is sparse: 1,205 of 1,674 training perturbations have `n_degs = 0`, the median is 0, and the 75th percentile is 1. Large counts exist in this population, but they are concentrated in active neuronal or broadly essential regulators, not in off-context Hox programs.

5. Training Hox-family comparators in the declared table were all null in the same endpoint: `Hoxa1 = 0`, `Hoxa13 = 0`, `Hoxa3 = 0`, `Hoxb8 = 0`, `Hoxd10 = 0`, and `Hoxd13 = 0`. `Hoxa13` and `Hoxd13` are the assayed group-13 relatives noted in the Hoxc13 biology card, so they are the closest count-table boundaries for an off-context Hox perturbation.

6. A direct filter of `training_de_all_cell_groups.parquet` for those six Hox comparators in `151 TH Prkcd Grin2c Glut` recovered 103,554 measured-gene rows and confirmed 0 genes with `pvals_adj < 0.05` for every Hox comparator. Their minimum adjusted p-values were far from the endpoint threshold: `Hoxb8` was lowest at 0.879665 and the remaining Hox comparators had minimum adjusted p-values of 1.0.

## Synthesis

`Hoxc13` has a molecular operation that could be realized on the experimental timescale, but the focal thalamic class supplies essentially no target expression and the known loss biology is in epithelial appendage programs rather than postmitotic neurons. The best in-endpoint empirical boundaries, including the group-13 relatives `Hoxa13` and `Hoxd13`, were all completely quiet in `151 TH Prkcd Grin2c Glut`. I therefore predict no BH-significant measured genes for the withheld Hoxc13 perturbation.
