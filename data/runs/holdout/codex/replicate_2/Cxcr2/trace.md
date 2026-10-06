# Cxcr2 n_degs prediction

Target: `Cxcr2` in `151 TH Prkcd Grin2c Glut`.

Prediction: `0` measured genes with BH-adjusted Wilcoxon `p < 0.05`.

Evidence that determined the point prediction:

- The declared manifest contains a single target, `Cxcr2`; `Cxcr2` is absent from the declared 1,674-row `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- The canonical `Cxcr2` biology bundle reports exact focal-population reach for `151 TH Prkcd Grin2c Glut`: 0 Cxcr2 UMIs in 23,679 non-target nuclei, 0 expressing nuclei, 0.0 pct cells expressing, mean raw UMI 0.0, mean CP10K 0.0, and pseudobulk CPM 0.0.
- The same bundle supports target realization only conditionally: a disruptive edit should eventually deplete functional CXCR2 receptor stock over the 21-28 day P16-to-P37/P44 window, but the underlying trafficking evidence is heterologous and "does not address whether thalamic neurons express the receptor or whether any aggregate effect is visible."
- The declared training count table for this exact cell class is sparse: 1,205/1,674 targets have `n_degs = 0`; the median is 0; 1,481/1,674 have `n_degs <= 1`; 1,512/1,674 have `n_degs <= 2`.
- I used the declared Parquet to check nearby receptor / inflammatory-signaling training perturbations in `151 TH Prkcd Grin2c Glut`. In that exact context, 24 of 25 selected receptor-like rows had zero significant genes among 17,259 measured genes: `Adra1a`, `Adra2a`, `Adra2b`, `Adrb2`, `Adrb3`, `Ager`, `Agtr1a`, `Agtr2`, `Ahr`, `Alk`, `Avpr1a`, `Avpr1b`, `Axl`, `Tnfrsf11a`, `Tnfrsf13c`, `Tnfrsf1a`, `Tnfrsf4`, `Tnfrsf9`, `Trpa1`, `Trpm3`, `Trpm7`, `Trpv1`, `Tshr`, and `Vdr` all had 0; `Ache` had 1.

Reasoning:

`Cxcr2` is a chemokine GPCR with known mouse immune and oligodendrocyte-lineage biology, not an established healthy postnatal thalamic neuronal regulator. The focal expression measurement is stronger than that literature prior for this endpoint: Cxcr2 was not detectably expressed in any of the 23,679 matched non-target nuclei from the target neuronal class. Stopping synthesis of a receptor can only deplete an operative receptor pool where that pool exists, so the functional-stock call does not overcome the absence of focal Cxcr2 RNA.

The training endpoint is already zero-inflated in this high-yield class, and the receptor-like comparators I checked were almost uniformly null even when the Parquet had a full 17,259-gene test vector for the perturbation. Combining the exact no-detectable-expression reach with those local outcomes makes a below-threshold or absent transcriptional response more plausible than even a one-gene call. I therefore predict `Cxcr2` will have `n_degs = 0`.
