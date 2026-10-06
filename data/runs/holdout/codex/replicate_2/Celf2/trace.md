# Celf2 n_degs direct forecast

## Evidence used

- **Declared target and endpoint.** The one-row holdout manifest names `Celf2`. The requested endpoint is the number of measured genes with BH-adjusted Wilcoxon `p < 0.05` in `151 TH Prkcd Grin2c Glut`.
- **Exact target reach.** In the declared Celf2 biology bundle for this focal population, Celf2 was available and broadly detected: 23,453 of 23,679 non-target nuclei expressed it, with mean raw target UMI `7.108`, mean log1p CP10K `1.627`, and pseudobulk CPM `445.49`. This makes a missing-expression explanation unlikely.
- **Functional realization prior.** The same bundle adjudicates CELF2 as a soluble nucleocytoplasmic RNA-binding/post-transcriptional regulator with continuously renewed functional pools. Functional stock is expected to be substantially depleted by the P37-P44 harvest after P16 editing, but only at low confidence because no Celf2-specific postmitotic neuronal protein half-life is known.
- **Biology-to-endpoint mismatch.** The strongest direct biology for CELF2 is alternative splicing or isoform choice. Mouse Celf2 loss changes Syntaxin isoforms, and cortical excitatory-neuron depletion alters an Ank3 microexon; those are target-proximal RNA-processing effects, but they need not appear as whole-gene abundance DE in a 10x single-nucleus Wilcoxon table.
- **Training count scale.** The focal training table is sparse: among 1,674 measured training targets, 1,205 had `n_degs = 0`, 469 had any DEG, 193 had at least 2 DEGs, and 132 had at least 5 DEGs. The median was 0, the 75th percentile was 1, the 95th percentile was 18, and the mean was 14.05 because a small upper tail reached hundreds to thousands of DEGs.
- **RNA-regulator comparators.** Severe core or broadly essential RNA-processing perturbations gave large whole-gene programs in this same cell class: `Rnpc3` 868, `U2af2` 828, `Hnrnpu` 733, `Prpf6` 454, `Snrnp70` 213, `Tardbp` 210, `Matr3` 149, and `Hnrnpc` 122 DEGs. By contrast, non-core or more buffered post-transcriptional perturbations were narrow or absent: `Dicer1`, `Fmr1`, `Adar`, `Rbm28`, and `Snrpb` each had 0; `Hnrnpdl` had 1; `Hnrnph2` and `Adarb1` had 4; `Hnrnpa2b1` had 11. Same-experiment corpus annotations also described `Dicer1` and `Fmr1` as buffered in this acute nuclear-RNA readout, while `Hnrnpc`, `Hnrnpu`, `Matr3`, and `Tardbp` carried real RNA-processing/stress signatures.
- **Observed-profile check.** A cohort comparison of 17 RNA-binding/post-transcriptional training profiles in the exact focal group confirmed that the broad spliceosome and hnRNP responders form overlapping but non-identical whole-gene programs. Those perturbations support RNA-processing vulnerability as an upper scale boundary, not a direct CELF2 scale transfer, because Celf2 is a paralog-specific splicing regulator and no measured CELF-family analog was available in the training count table.

## Synthesis

Celf2 is reachable in nearly every assayed non-target thalamic nucleus, and the operation should affect a renewable RNA-binding activity within the P16-to-P37/P44 window. That argues against treating it exactly like an unexpressed or stock-protected zero.

The broad RNA-splicing counts are poor point donors. `Rnpc3`, `U2af2`, `Prpf6`, `Snrnp70`, and `Hnrnpu` disrupt core spliceosome or ubiquitous RNP processes and produced hundreds of whole-gene abundance changes. CELF2 is more substrate-selective, and its most direct known outcomes are exon-usage changes that this endpoint mostly would not count. The quieter RNA-axis perturbations show that loss of an RNA regulator with clear prior biology can still be FDR-flat or nearly flat at the gene-abundance level.

I therefore placed the forecast at a very small nonzero count. One DEG captures the plausible self-transcript hit made likely by high Celf2 expression and matched power, while avoiding unsupported transfer of the large spliceosome/stress programs to a CELF-family splicing regulator.

Final predicted `n_degs`: **1**
