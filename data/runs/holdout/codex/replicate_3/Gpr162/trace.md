# Gpr162 n_degs forecast

Target and endpoint: `Gpr162` in `151 TH Prkcd Grin2c Glut`; predict the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.

Evidence used:

- The declared holdout manifest contains only `Gpr162`; the supplied focal count table contains 1,674 non-held-out training perturbations.
- In the exact focal population, baseline `Gpr162` expression is available and broad: 23,598 of 23,679 non-target nuclei express the gene, `pct_cells_expressing = 99.6579`, `mean_cp10k = 6.3806`, and `mean_log1p_cp10k = 1.9357`. This makes lack of target expression a poor explanation for a predicted null response, but it does not prove that receptor loss drives a transcriptional program.
- The target biology bundle supports only a weak-to-moderate realization prior. GPR162 is a seven-transmembrane receptor with CART-responsive GNA13-associated signaling demonstrated outside brain; adult mouse CNS and thalamic expression are established; a 7-day adult-rat intracerebroventricular antisense experiment showed a feeding phenotype. Against that, no direct mouse postnatal thalamic loss phenotype or GPR162-specific neuronal turnover measurement was found, GPR153 paralogy has no demonstrated compensation test, and the receptor stock conclusion is therefore "likely substantially depleted" but sparse and low-confidence.
- The focal training endpoint is zero-inflated. Of 1,674 measured training targets, 1,205 are `0` DEGs, 1,481 are `<= 1`, and 1,546 are `<= 5`; only 66 targets exceed 25 DEGs.
- Large focal signatures are dominated by core RNA-processing, proteostasis, chromatin, and essential cellular regulators: the largest counts in the declared table include `Uba5` 2677, `Tpr` 1768, `Sin3a` 1433, `Rnpc3` 868, `Zbtb7a` 841, `U2af2` 828, and `Psmb4` 742. `Gpr162` is not in that mechanistic class.
- A receptor-like training subset was much quieter than the genome-scale table. Among 41 GPCR-like receptor perturbations in the declared focal count table, 36 had 0 DEGs and the remaining 5 had exactly 1 DEG; the mean count in that subset was 0.122. The stricter visible `Gpr*` subset had seven targets, five zeros, and two one-DEG cases.
- Direct Parquet rows for those GPCR-like receptor perturbations in `151 TH Prkcd Grin2c Glut` recovered enough perturbed nuclei to make the receptor subset interpretable rather than uniformly unpowered: the five one-DEG cases had 179 to 255 matched perturbed nuclei, while the zero-DEG receptor cases spanned 67 to 351 matched perturbed nuclei against the same 23,679 matched controls.

Synthesis:

`Gpr162` has high thalamic transcript reach and is probably a renewable receptor pool by the P37-P44 harvest, so I did not set the value to zero because the perturbation is unreachable. The decisive evidence was instead endpoint scale: in this focal class, ordinary receptor perturbations almost always produced no BH-significant downstream gene even with comparable matched-cell recovery, whereas broad multi-hundred to multi-thousand DEG signatures came from essential RNA, proteostasis, and chromatin machinery. The prior neural evidence for GPR162 is too indirect to move it out of that quiet receptor regime. I therefore use the modal and mechanistically matched integer forecast, `0`.
