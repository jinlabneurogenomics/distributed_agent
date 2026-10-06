# Direct n_degs prediction for Bicc1

Target and endpoint: `Bicc1` in `151 TH Prkcd Grin2c Glut`; `n_degs` is the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

Evidence used:

- The declared manifest contains the single target `Bicc1`.
- The canonical biology bundle reports in-assay `Bicc1` expression in this focal class, with 9,519 of 23,679 matched non-target nuclei expressing the transcript, 40.20% expressing cells, mean raw UMI 0.610, mean CP10K 0.380, and pseudobulk CPM 38.21. This makes target engagement plausible in a substantial minority of the aggregated thalamic class, but it is not broad high expression across essentially all nuclei.
- The functional-stock card classifies Bicc1 as a cytoplasmic KH RNA-binding protein that forms SAM-dependent RNA-silencing polymers. A P16 disruptive edit stops new supply, but pre-existing polymeric material can persist; by P37-P44 the harvest window is best judged as `partially_depleted_or_leading_edge`, not assured near-clearance.
- The same source card discounts the strong constitutive mouse phenotype as a quantitative guide: the established Bicc1 loss phenotype is congenital renal/systemic disease with early postnatal death, not a matched postnatal thalamic neuron requirement.
- The training count table for this cell class is sparse: 1,205 of 1,674 training perturbations have `n_degs = 0`; the 75th percentile is 1, the 90th percentile is 2, and the 95th percentile is 18.
- A species-safe annotation nomination against the exact training universe found no close paralog, exact complex partner, or specific direct interactor for `Bicc1`; all 1,184 available nominees were broad functional fallbacks. The highest-priority useful fallback terms were mRNA catabolic process, RNA binding, and mRNA processing.
- Matched expression-profile review of the RNA/post-transcriptional fallback cohort in the declared Parquet showed a mixed low-to-high response distribution. The most operation-relevant low or moderate examples in this class were `Xrn1 = 20`, `Hnrnpa2b1 = 11`, `Ddx3x = 8`, `Ski = 2`, `Hnrnph2 = 4`, `Eif4a2 = 2`, `Ago1 = 1`, `Eif4h = 1`, and `Upf3b = 1`; `Reg1`, `Fmr1`, `Fxr1`, `Ago2`, `Dicer1`, `Cnot1`, `Tnrc6a`, `Tnrc6b`, `Syncrip`, and `Snrpb` were 0.
- The very large RNA-processing counts, for example `U2af2 = 828`, `Cdc40 = 624`, `Hnrnpu = 733`, `Tardbp = 210`, `Snrnp70 = 213`, `Matr3 = 149`, and `Hnrnpc = 122`, came from spliceosome or broad nuclear hnRNP states. Same-experiment Findings describe them as compensatory RNA-processing programs and pathway contrasts rather than phenocopies of narrow cytoplasmic RNA-silencing perturbations, so I treated them as upper-scale boundaries rather than direct magnitude donors.

Synthesis:

`Bicc1` has enough exact thalamic expression and no known close compensatory paralog to keep a strict zero from being forced. At the same time, the operative biology is a cytoplasmic bound-RNA silencing polymer with uncertain residual stock after 21-28 days, the matched mouse loss evidence is developmental and renal/systemic, and several acute post-transcriptional comparators in this postmitotic neuronal assay are transcriptionally silent. The relevant measured fallback distribution is therefore concentrated at 0-2 DEGs with occasional 8-20 DEG narrow responses. I placed `Bicc1` just above a null but below `Ddx3x`, `Hnrnpa2b1`, and `Xrn1`, giving a point prediction of 1 FDR<0.05 DEG.

No withheld `Bicc1` perturbation signature or outcome count was queried or used.
