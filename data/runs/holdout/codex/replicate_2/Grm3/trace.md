# Grm3 prediction trace

Task endpoint: `n_degs` is the count of measured genes in `151 TH Prkcd Grin2c Glut` with Wilcoxon BH-adjusted `pvals_adj < 0.05`, including the perturbed transcript itself.

Target and reach:

- The one-row manifest target is `Grm3`.
- The canonical `Grm3` biology bundle reports exact non-target expression in the focal population: 2,034 / 23,679 nuclei express `Grm3`, `pct_cells_expressing = 8.5899`, `mean_raw_umi = 0.1119`, and pseudobulk CPM is 7.01. So the target is present but sparse in the aggregated thalamic glutamatergic class.
- The same bundle classifies 21-28 day functional-stock loss as `partially_depleted_or_leading_edge`: genome editing should stop new mGluR3 production, but pre-existing surface/recycling receptor can persist acutely and no direct juvenile thalamic 21-28 day depletion curve is available.
- The prior phenotype evidence supports that Grm3 can matter in postnatal neurons, but the closest deletion experiment was frontal cortex at >=6 weeks after Cre, later than this assay and in a different region.

Training measurements used:

- In the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, 1,205 / 1,674 training perturbations have `n_degs = 0`; the median is 0 and the 75th percentile is 1.
- The nearest measured metabotropic glutamate receptor targets in the same count table are almost silent in this exact class: `Grm1:1`, `Grm5:0`, `Grm6:0`, `Grm7:1`, `Grm8:0`. The total across those five rows is 2.
- A broader Gi/o receptor or cAMP-effector set is similarly quiet: `Gabbr1:1`, `Gabbr2:1`, `Gnao1:1`, `Adcy1:0`, `Adcy3:0`, `Adcy5:0`, `Pde1c:0`, `Pde4b:0`, `Pde4d:0`.
- The expression parquet confirms that the `Grm1` and `Grm7` one-hit rows in `151 TH Prkcd Grin2c Glut` are self-transcript hits, and that `Grm5`, `Grm6`, and `Grm8` have no `pvals_adj < 0.05` rows in this class. Thus the mGluR training analogs do not show a transferable downstream transcriptional program.
- Same-experiment packaged Findings agree with the row-level interpretation rather than adding independent replication: the selected release reports that `Grm1`, `Grm5`, `Grm7`, and `Grm8` were pan-null or near pan-null for downstream FDR-resolved basal snRNA responses, and that represented metabotropic-glutamate, PLC/IP3, PKC/CaMK, and postsynaptic-scaffold perturbations were mostly buffered.

Synthesis:

The dominant measured prior in this class is zero. `Grm3` has real biology, but its exact focal reach is low and regionally diluted, and its receptor stock is expected to be only partially depleted by P37-P44. The closest family-level Perturb-seq observations point to no sustained downstream nuclear-RNA module after sparse postnatal mGluR loss. The only plausible reason to predict a nonzero count is a detectable `Grm3` self-transcript reduction; because the transcript is present in only 8.6% of non-target nuclei, I would not round that probability above one half. I therefore predict no BH-significant measured genes.

Point prediction: `0`
