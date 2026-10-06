# Direct n_degs forecast for Arsb

## Target and endpoint

- Target: `Arsb`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Forecast: `0`

## Evidence used

The declared biology bundle maps the supplied `Arsb`/`ArsB` identity to `Slurp1`, a small secreted Ly6/uPAR-family extracellular protein with predicted acetylcholine-receptor activator activity. I therefore treated the perturbation as loss of a secreted extracellular Slurp1 stock, not as loss of a lysosomal arylsulfatase.

The same bundle reports exact focal-population target expression in `151 TH Prkcd Grin2c Glut`: `Arsb` was detected in 9,021 of 23,679 non-target cells, with `pct_cells_expressing = 38.097`, `mean_raw_umi = 0.541`, `mean_log1p_cp10k = 0.2266`, and `pseudobulk_cpm = 33.93`. This makes the target transcript present in the assayed class, but still low, and the bundle explicitly separates expression reach from editing efficiency or functional dependence.

The functional-stock card was unresolved rather than strongly positive: a disruptive P16 edit should stop new intact Slurp1 production from edited expressing cells, but it does not inactivate pre-edit extracellular Slurp1; the card found no target-specific clearance or extracellular-residence measurement that could show substantial local depletion by the P37-P44 harvest. Its mouse loss phenotype evidence is dominated by skin/systemic phenotypes, with no matched postnatal thalamic neuronal requirement.

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table is heavily concentrated at zero: among 1,674 training perturbations, 1,205 had `n_degs = 0`, the median was 0, the 75th percentile was 1, and the 90th percentile was 2. Thus the class has a long positive tail, but the default prediction for a weakly supported, non-core neuronal perturbation is the floor.

I used the gene-annotation store to locate deterministic training comparators for the declared Slurp1 activity. The narrow `GO:0030549` acetylcholine-receptor-activator set contained `Arsb` itself but no held-in measured analog. There were also no `Slurp`, `Ly6`, `Lypd`, or `Lynx` family members in the 1,674-row class count table. I therefore treated acetylcholine receptor signaling genes as fallback context rather than direct analogs. In `GO:0095500`, 16 members were present in the class table and 12/16 were zero; the measured receptor/acetylcholine fallback nodes were:

| training perturbation | n_degs |
| --- | ---: |
| `Chrm3` | 0 |
| `Chrna3` | 0 |
| `Chrna7` | 0 |
| `Ache` | 1 |
| `Chrnb2` | 1 |
| `Chrna4` | 2 |

I also checked broader extracellular-region annotations. They were too heterogeneous to transfer directly, but still quiet as a scale check: 92 of 123 present `GO:0005576` extracellular-region perturbations were zero and their median count was 0.

Finally, I read the training Parquet for the six acetylcholine/receptor fallback nodes in the exact cell class with `dataset.candidate_profile_review`. The all-pair cohort comparison had no overlapping significant positive program and zero negative significant overlap where such overlap was defined; the mean top-tail overlap coefficients were 0.066 for positive tails and 0.112 for negative tails. This made the six genes near-null scale references, not a coherent expression module that would justify lifting `Arsb`.

## Synthesis

The focal cells express `Arsb`, so a one-DEG outcome is plausible. But the biology bundle gives no evidence that P16 sparse thalamic editing removes enough extracellular Slurp1 stock by harvest to create a synchronized cell-autonomous state, direct Slurp/Ly6 comparators are absent from training, and the closest acetylcholine-receptor fallback perturbations sit at 0-2 DEGs without a recurrent significant profile. I therefore put the point forecast at the zero floor rather than lifting it to the small nonzero range.
