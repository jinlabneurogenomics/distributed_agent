# Trem2 direct `n_degs` forecast

## Target and endpoint

- Target: `Trem2`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: count of measured genes with BH-adjusted Wilcoxon `p < 0.05`

## Evidence used

1. The canonical Trem2 biology bundle reports extremely low focal-population Trem2 RNA in non-target nuclei from `151 TH Prkcd Grin2c Glut`: 110/23679 nuclei expressing, 0.4645% expressing, mean raw UMI 0.00473, mean CP10K 0.00304, and pseudobulk CPM 0.296. This is effectively a near-absent target in the NeuN-positive thalamic nuclei whose recovered transcriptome defines the endpoint.

2. Trem2 biology points in opposite directions depending on which cell type is considered. If a Trem2-expressing microglial cell were productively edited, the main full-length TREM2/TYROBP surface-receptor pool is expected to be depleted within the 21-28 day P16-to-P37/P44 assay window. However, the direct receptor biology is microglial/myeloid rather than intrinsic to neurons, and the assayed population is recovered NeuN-positive thalamic neurons. The reported neural phenotypes are indirect, microglia-mediated, mostly hippocampal or injury contexts, and not a direct match to an acute thalamic neuronal readout.

3. The declared `151 TH Prkcd Grin2c Glut` training count table is sparse: 1205/1674 training perturbations have `n_degs = 0`, the median is 0, the 75th percentile is 1, and the 90th percentile is 2. A target with almost no focal RNA and no strong intrinsic neuronal mechanism should therefore sit at the zero atom rather than inherit the heavy upper tail from neuronal housekeeping, splicing, proteasomal, or chromatin targets.

4. Available immune or microglial training perturbations that share the broad mismatch between the target's main biology and recovered neurons were also quiet in this focal class: `Csf1r`, `Cx3cr1`, `Irf8`, `P2ry12`, `Ptprc`, `Sall1`, `Spi1`, `Tlr2`, and `Tlr4` each have 0 DEGs; `Cst3` has 1. `Tyrobp`, the closest Trem2 adaptor, is not present in the training count table, so this is a boundary check rather than a direct receptor-complex analogue.

## Synthesis

The strongest bearing is downward: Trem2 has negligible direct expression in the measured neuronal nuclei, and perturbing a microglial surface receptor is poorly coupled to a survivor-conditioned NeuN-positive thalamic transcriptional signature. The main upward bearing is that genuine Trem2 loss can perturb postnatal neural tissue indirectly through microglia, but the focal assay excludes most microglia, and the bundle does not establish a P16 acute thalamic neuron response. Against a count table whose mass is already concentrated at zero, the expression mismatch makes any indirect response unlikely to cross BH FDR for even one measured gene.

Predicted `n_degs`: 0
