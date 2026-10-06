# Sox3 n_degs forecast for `151 TH Prkcd Grin2c Glut`

## Requested endpoint

- Target from the one-row manifest and biology bundle: `Sox3`.
- Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Declared training count table: 1,674 perturbations in the focal population; it does not contain `Sox3`.

## Evidence that set the forecast

1. **Exact focal expression of the target is very low.** In the declared Sox3 biology bundle, focal non-target nuclei had `521 / 23679` Sox3-expressing cells, `2.2003%` expressing cells, mean raw UMI `0.0239`, mean cp10k `0.01497`, and pseudobulk CPM `1.4981`. This makes a broad cell-autonomous Sox3-loss transcriptional response in recovered thalamic glutamatergic neurons less likely, though it does not prove a null because editing efficiency is not read directly from target RNA.

2. **The target-specific biological prior is developmental and underdetermined for an acute postnatal thalamic assay.** The Sox3 card supports SOX3 as an HMG-box nuclear transcription factor and records Sox3-null developmental ventral-diencephalic and hypothalamo-pituitary phenotypes. It does not contain a transferable acute P16-to-P37/P44 thalamic loss phenotype or quantitative SOX3 protein-clearance estimate. The Sox2 gene-swap evidence shows possible SOXB1 functional substitutability under engineered Sox3-locus control, but not natural postnatal thalamic compensation.

3. **The same-population training endpoint is zero-heavy.** In the focal count table, `1205 / 1674` training perturbations had `n_degs = 0`; the median was `0`, the 75th percentile was `1`, the 90th percentile was `2`, and only 83 perturbations exceeded 18 DEGs. The mean, `14.05`, is dominated by a small high-burden tail headed by broad essential or RNA-processing perturbations rather than by developmental TFs.

4. **Measured Sox and neural-developmental TF comparators stayed quiet in the same focal class.** The closest declared Sox-family training perturbations had focal counts `Sox2 = 2`, `Sox5 = 2`, `Sox4 = 0`, `Sox9 = 0`, `Sox10 = 0`, `Sox11 = 0`, `Sox17 = 0`, and `Sox18 = 0`. In the expression Parquet, the `Sox2` focal signature contained only `Tnnt1` and `Stam` at FDR < 0.05, the `Sox5` signature contained only `Dgkh` and `Tnnt1`, and `Sox4/Sox9/Sox10/Sox11` had no FDR-significant focal genes. A broader pattern match over named developmental transcription-factor families in the training table was also mostly null: 49 of 52 such entries were zero, with `Sox2` and `Sox5` at 2 as the only Sox-family nonzeros.

## Synthesis

I used the focal count table as the direct outcome distribution, the Parquet only to verify the sparse Sox comparator signatures, and the Sox3 bundle for target-specific observability and functional-stock priors. Sox3 is a transcription factor, so a realized knockout could matter where SOX3 is actively renewed, but its focal RNA reach is only 2.2% of non-target nuclei and the literature support is embryonic/developmental rather than an acute juvenile thalamic requirement. The measured Sox-family perturbations in this same endpoint cluster at 0-2 DEGs, with most at exactly 0. That makes a small nonzero count possible but keeps the mode at no FDR-significant focal response.

Point prediction: `0`.
