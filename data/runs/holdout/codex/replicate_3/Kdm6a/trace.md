# Direct forecast for Kdm6a

Target: `Kdm6a`

Cell group: `151 TH Prkcd Grin2c Glut`

Predicted `n_degs`: `0`

## Evidence used

### Target biology

- The declared canonical Kdm6a biology bundle reports that `Kdm6a` is observed in the focal in-assay non-target population: 14,887 of 23,679 nuclei express it, with 62.870% expressing, mean raw UMI 1.142, mean CP10K 0.726, and pseudobulk CPM 71.56.
- The same bundle calls the perturbation likely functionally realized by the P37-P44 harvest: KDM6A is an H3K27me2/3 demethylase and MLL3/4-complex component; existing protein is not instantly removed at editing, but acute postnatal hippocampal neuron deletion produced morphology phenotypes within 7-19 days and neuronal H3.3 is continuously renewed over a similar multi-week interval.
- The bundle also notes partial redundancy: UTY can preserve some noncatalytic KDM6A functions in embryonic contexts but lacks detectable H3K27 demethylase activity, and KDM6B is a second catalytic H3K27 demethylase whose buffering after postnatal Kdm6a loss is unresolved.

### Same-experiment training measurements

- The declared focal count table contains 1,674 training targets, of which 1,205 have `n_degs = 0`; the median is 0 and the 75th percentile is 1. Sparse or null focal responses are therefore common even in this high-yield thalamic population.
- The closest measured H3K27 eraser, `Kdm6b`, has `n_degs = 0` in the focal count table. The same-experiment corpus summarizes acute postnatal `Kdm6b` loss as FDR-null in all 23 recovered neuronal groups, and its `151 TH Prkcd Grin2c Glut` profile had no FDR<0.05 genes in the parquet-neighborhood run; the best whole-profile Pearson neighbor among 1,673 other eligible profiles was only `Rora` at 0.116.
- The closest assayed MLL3/4-family enhancer-side target, `Kmt2c`, also has `n_degs = 0` in the focal count table. The corpus reports that 15 of 16 measured `Kmt2c` groups had no downstream FDR<0.10 genes and the only nonzero group had a single cortical `Prnp` response. In the focal profile-neighborhood run, `Kmt2c` again had no FDR<0.05 genes and its best whole-profile Pearson neighbor was only 0.077.
- Broader chromatin regulators showed that the assay can detect postnatal chromatin perturbations in this same focal group, but those positive controls are not close KDM6A phenocopies. Representative focal `n_degs` were `Setd1a` 368, `Kmt2a` 24, `Kdm5c` 18, `Crebbp` 8, `Setd5` 9, while several nearby enhancer/HAT/demethylase comparators were still null: `Ep300`, `Kat6a`, `Kat6b`, `Kdm5b`, `Kdm4b`, `Kdm4c`, `Phf6`, and `Phf8` all had 0.

## Reasoning

The expression and stock evidence make `Kdm6a` a biologically real perturbation in the P16-to-P37/44 window, not an absent-target case. However, the requested endpoint is a strict BH-adjusted Wilcoxon DEG count in survivor-conditioned thalamic nuclei. For that endpoint, the direct training evidence from the same focal context is more predictive than the long-horizon developmental prior.

The measured branch of the H3K27/MLL3/4 neighborhood was quiet: `Kdm6b` was exactly zero in the focal count table and globally flat, and `Kmt2c` was exactly zero in the focal count table and almost entirely buffered across its measured groups. The active broad chromatin regulators demonstrate that `151 TH Prkcd Grin2c Glut` is not blind to chromatin perturbation, but they do not overcome the more specific KDM6/H3K4-enhancer evidence. Because `Kdm6a` itself, `Kmt2d`, and PRC2-core tests were absent from the training parquet, there remains uncertainty; the forecast is a sparse/null point rather than a confident mechanistic zero.

I therefore predicted no BH-adjusted FDR<0.05 genes for `Kdm6a` in `151 TH Prkcd Grin2c Glut`.
