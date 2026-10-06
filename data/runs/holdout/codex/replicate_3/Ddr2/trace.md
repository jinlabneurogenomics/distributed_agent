target: Ddr2
cell class: 151 TH Prkcd Grin2c Glut

Evidence used:

- Declared endpoint: number of measured genes in the focal class with BH-adjusted Wilcoxon p < 0.05.
- The held-out manifest names Ddr2; Ddr2 is absent from the 1,674-row focal-class training count table.
- In the exact focal non-target population, Ddr2 was detected in 129 / 23,679 nuclei, pct_cells_expressing = 0.5447865%, mean_raw_umi = 0.0067993, mean_log1p_cp10k = 0.0027341, and pseudobulk_cpm = 0.4261346.
- The Ddr2 biology bundle supports a plausible molecular loss after P16 editing: Ddr2 encodes a collagen-activated receptor tyrosine kinase, existing mature receptor is expected to turn over rather than persist for 21-28 days, and the functional-stock call is likely_substantially_depleted by P37-P44. The bundle is only partial for this endpoint, because Ddr2 null phenotypes are mainly mesenchymal/systemic and do not establish a postmitotic thalamic-neuron requirement, Ddr1 is only an unresolved paralog/buffering concern, and collagen engagement in these neurons is not established.
- The focal count table is dominated by exact zeros: 1,205 / 1,674 training perturbations have n_degs = 0, the median is 0, the 75th percentile is 1, and the 90th percentile is 2, with a small heavy tail from broadly active machinery genes.
- A hand-curated Ddr2-like panel of matrix/cell-surface/RTK signaling perturbations in the same count table was even quieter than the background: 34 / 37 were zero. The only nonzero members were Epha4 = 1, Ntrk2 = 3, and Lrp6 = 4; Axl, Ephb2, Fgfr1, Fgfr2, Fgfr3, Igf1r, Insr, Kdr, Mertk, Met, Pdgfrb, Ret, Ror1, Ror2, Tek, Dag1, Itgb1, and several Itga/Lrp targets were zero.
- Direct Parquet checks in the focal class for nearby observed receptors were concordant: Ephb2, Fgfr1, Insr, Itgb1, Lrp1, Met, and Ror2 each had 0 / 17,259 significant measured genes.

Reasoning:

Ddr2 loss is likely realized at the protein-stock level wherever biallelic editing hits cells that actively depend on DDR2, so I did not treat the target as an edit-failure null. The limiting evidence is focal reach and demand: the transcript is seen in only about half a percent of non-target thalamic glutamatergic nuclei, and the curated biology does not show that juvenile postmitotic thalamic neurons broadly use collagen-DDR2 signaling. That makes a class-aggregated survivor snRNA signature easier to dilute below FDR even if rare Ddr2-positive cells respond.

The observed training distribution also says that zero is the modal outcome in this cell class, and the most mechanism-adjacent observed surface-receptor and ECM-linked perturbations stay at 0-4 DEGs rather than entering the heavy machinery-gene tail. Combining the very low exact focal expression with those quiet local comparators, I forecast the held-out count at the floor.

predicted_n_degs = 0
