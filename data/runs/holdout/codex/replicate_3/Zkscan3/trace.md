# Zkscan3 n_degs forecast

Target and endpoint:

- Target manifest: `Zkscan3`.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- The forecast below uses the declared target biology bundle, the declared held-in `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, and measured held-in signatures from `training_de_all_cell_groups.parquet`. I did not use the held-out Zkscan3 signature or a held-out Zkscan3 DEG count.

Evidence that determined the point:

- The 1,674 held-in targets in the requested thalamic class are mostly silent on this endpoint: 1,205 have `n_degs = 0`, the median is 0, the 75th percentile is 1, the 90th percentile is 2, and only 66 targets exceed 25 DEGs. The empirical prior for a target without a specific high-response analogue is therefore very close to zero despite a long right tail.
- The exact biology bundle shows that focal-population Zkscan3 transcript is detectable rather than absent: 16,790 of 23,679 non-target nuclei express the gene, with 70.91% expressing, mean raw UMI 1.373, and pseudobulk CPM 86.04. I treated this as evidence that edited neurons can include Zkscan3-positive cells, but not as evidence for a high transcriptional footprint.
- The same bundle classifies ZKSCAN3 as a nuclear KRAB/SCAN C2H2 zinc-finger transcription regulator. A disruptive edit should stop new functional protein supply, but the P16-to-P37/P44 experiment does not directly remove preexisting protein; no target-specific protein half-life, chromatin residence, or post-edit clearance measurement was available, so functional stock at harvest is indeterminate.
- Mouse evidence in the bundle is not a matched postnatal thalamic loss-of-function phenotype. Germline Zkscan3-null mice were grossly viable with no marked autophagy-response phenotype in the reported assays, an erythroid phenotype shows that the gene can matter in another lineage, and Zkscan4 paralogy is only a proposed buffer without a same-context compensation test. I therefore used the biology as permissive for a small effect, not as a reason to jump to a large neural response.
- The closest assayed SCAN/zinc-finger-family training perturbations were all quiet in the count table: `Zkscan1 = 0`, `Zkscan16 = 0`, and `Zscan26 = 0`. The broader assayed `Zfp*` set was also mostly quiet: 25 of 30 named `Zfp`/`Zfpm` targets had `n_degs = 0`, with median 0; the nonzero exceptions were not specific SCAN-family analogues.
- I used `distributed_agents_runtime.profile_compare` on the full Parquet rows for `151 TH Prkcd Grin2c Glut` to check the measured 17,259-feature signatures of `Zkscan1`, `Zkscan16`, and `Zscan26` against a broader zinc-finger/chromatin cohort. All three SCAN/ZSCAN anchors had zero positive and zero negative significant features. More general zinc-finger or chromatin factors in that cohort ranged up to large responses (`Zbtb7a = 841`, `Zfp423 = 150`, `Zmynd8 = 74`), but their biology is less operation-specific for Zkscan3, and the quiet SCAN anchors did not reveal a coherent high-response measured-profile module that should override their exact zero counts.

Synthesis:

Zkscan3 is expressed in the focal thalamic population and is a transcription regulator, so I would not force a structural zero. However, the within-window functional depletion is unresolved, matched neural phenotype evidence is absent, close held-in SCAN/ZSCAN perturbations have measured zero-DEG signatures, and the requested class has a strongly zero-inflated held-in count distribution. I therefore put the point estimate at the modal and closest-family value rather than borrowing the long-tailed counts from broader chromatin regulators.

Predicted `n_degs`: 0
