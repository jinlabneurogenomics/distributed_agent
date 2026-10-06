target: Clcn5
cell_group: 151 TH Prkcd Grin2c Glut

Evidence used

- The declared target is Clcn5, and the requested endpoint is the number of measured genes in 151 TH Prkcd Grin2c Glut with Wilcoxon BH-adjusted p < 0.05.
- The Clcn5 biology bundle reports exact in-assay expression in this population but no target expression contrast or target outcome: 6,645 of 23,679 non-target nuclei expressed Clcn5, with mean CP10K 0.2259, mean raw UMI 0.3628, and pseudobulk CPM 22.74. This establishes real but minority/narrow target reach in the focal thalamic population.
- The same bundle says ClC-5 is a renewable endosomal 2Cl-/H+ exchanger. A P16 disruptive edit should plausibly reduce the functional stock by the P37-P44 harvest, but the direct mouse phenotype is renal proximal-tubule endocytosis; no acute postnatal thalamic-neuron loss phenotype or ClC-5-specific neuronal turnover was available.
- In the declared 151-count training table, the class endpoint is highly floor-skewed: 1,205/1,674 training perturbations had 0 DEGs, 1,481/1,674 had <=1 DEG, 1,512/1,674 had <=2 DEGs, the median was 0, and the 75th percentile was 1.
- The closest measured chloride/endosomal perturbations in the same declared Parquet were also nearly silent in 151 TH Prkcd Grin2c Glut at p_adj < 0.05: Clcn3 = 0, Clcn4 = 1, Atp6v0a1 = 1, Atp6v1a = 0, Atp6v1b2 = 0, Atp6v1e1 = 0, Atp6ap2 = 2, Ocrl = 0, Lrp2 = 0, Lamp2 = 0, Becn1 = 0, Atg5 = 0, Ap1b1 = 1, Ap1s2 = 0, and Ap3b1 = 0. For the 1-DEG hits in this neighborhood, the Parquet showed self-transcript detection rather than a broader downstream program.
- Same-experiment corpus Findings for training perturbations agreed qualitatively that acute Clcn3 and Clcn4 losses were buffered across recovered neuronal groups and lacked the expected lysosomal/autophagy, ISR/UPR, or synaptic-marker programs; Atp6v0a1 was self-detected without a downstream FDR<0.10 response, and Atp6ap2 was nearly silent rather than Rab7-like.

Synthesis

I treated Clcn5 as a likely realized, low-reach endosomal transporter loss rather than as a stock-persistence null. The exact thalamic reach is enough for an effect in edited Clcn5-positive neurons, but it is dilute for an aggregated 151-class snRNA endpoint. The nearest operation-level training evidence is the endosomal ClC/V-ATPase surface, not the much larger Rab7 late-endosomal stress state or the modest Vps35/Vps54 trafficking states; those broader machinery lesions are qualitatively different and the same-experiment corpus explicitly separated them from V-ATPase/ClC exchanger loss.

The resulting expectation is at the floor: no robust downstream Clcn5 program in this focal class, with the main way to reach n_degs = 1 being a self-transcript-only detection event. Because self-knockdown is not a stable quantitative proxy and Clcn5 expression is low and minority-distributed, I placed the point at 0 rather than 1.
