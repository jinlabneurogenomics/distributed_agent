# Ccr5 direct n_degs forecast

## Target and endpoint

- Target: `Ccr5`, from the declared one-row holdout manifest.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, i.e. the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- Same-experiment outcome status: the Ccr5 focal expression signature and Ccr5 focal DEG count were not used; the forecast used the declared biology-only bundle, the training count table, and selected non-Ccr5 rows from the declared expression Parquet.

## Evidence used

1. **Exact focal-population Ccr5 reach**

   In the biology bundle, exact control expression for `Ccr5` in `151 TH Prkcd Grin2c Glut` is extremely sparse: 76 of 23,679 matched non-target nuclei expressed any Ccr5 UMI, totaling 86 UMIs. The mean raw expression is 0.0036319 UMI per nucleus, the mean log1p CP10K is 0.0016289, and pseudobulk expression is 0.2276 CPM. This exact in-assay expression supersedes the weaker regional-expression prior for deciding whether the thalamic assayed population has much Ccr5-bearing substrate.

2. **Functional-stock biology**

   The canonical card supports successful molecular realization where Ccr5 is actually used: CCR5 is a cell-surface chemokine GPCR with dynamic endocytosis/recycling, heterologous receptor turnover on an hour timescale, and adult neural knockdown effects within a compatible time window. Thus the P16 edit should deplete receptor stock by P37-P44 in edited Ccr5-expressing neurons. This argues against a long-lived-protein explanation for complete silence, but it does not overcome the very small focal expression reach.

3. **Training count distribution**

   The focal training count table contains 1,674 measured perturbations. It is highly zero-inflated for this endpoint: 1,205/1,674 have `n_degs = 0`, the median is 0, the 75th percentile is 1, and 1,481/1,674 have at most one DEG. The high-count tail is real but concentrated in broad regulatory and essential-machinery genes, not in sparsely detected surface-receptor perturbations.

4. **Selected receptor comparators from the declared Parquet/count table**

   The closest named paralog in the Ccr5 biology bundle, `Ccr2`, has `n_degs = 0` in the focal count table and no BH-significant focal rows in the Parquet. Other immune or chemokine-adjacent receptor perturbations available in the same focal training endpoint were also quiet: `Cx3cr1 = 0`, `Cxcr4 = 0`, `P2ry12 = 0`, `P2ry14 = 0`, and `S1pr2 = 0`. Two broader GPCR-family comparators had count 1 (`Gpr158`, `Gprasp2`), but the only significant row in each case was the perturbed transcript itself, not a multi-gene downstream state.

## Synthesis

Ccr5 is biologically editable within the experimental window, but the focal thalamic glutamatergic population has almost no detectable baseline Ccr5 transcript: only about 0.32% of non-target nuclei contain any UMI. In this screen, the background expectation for a perturbation without a broadly expressed, cell-intrinsic regulatory role is already zero or one DEG, and the most relevant receptor/paralog controls land at zero. Because the sparse Ccr5 reach also makes even the self-transcript hit hard to detect, I place the forecast at the zero end rather than the one-DEG shoulder.

Predicted `n_degs`: **0**
