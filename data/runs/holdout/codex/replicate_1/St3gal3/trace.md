# Direct DEG-count prediction for St3gal3

## Target and focal context

- Target manifest: `St3gal3`.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, counting measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- The focal St3gal3 expression-reach bundle reports direct expression in this assayed class: 14,416 / 23,679 non-target nuclei expressing St3gal3, 60.88% expressing, mean 0.663 CP10k.
- The same biology-only bundle adjudicates St3gal3 functional stock as `likely_substantially_depleted` by the P37-P44 harvest, but through a delayed and partially buffered mechanism: the edit stops new ST3Gal-III enzyme supply, while pre-edit alpha-2,3-sialylated glycoproteins persist until their carriers turn over, with an unresolved long-lived-carrier tail and no matched thalamic acute-loss timing series.

## Training measurements used

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 non-held-out perturbations for this cell class. It is highly concentrated at zero:

| statistic | value |
|---|---:|
| zero-count perturbations | 1205 / 1674 |
| perturbations with `n_degs <= 1` | 1481 / 1674 |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| mean, inflated by high-response outliers | 14.054 |

I used the curated gene-analog nomination skill with the full declared training universe rather than symbol-prefix filtering. Its strongest narrow-module training candidates for St3gal3 were glycosylation or glycolipid genes, not exact ST3Gal-III paralogs in the same substrate/compartment:

| nominated comparator | typed relationship to St3gal3 | focal `n_degs` |
|---|---|---:|
| St3gal5 | sialyltransferase activity; sialic-acid/glycosphingolipid modules | 1 |
| Crppa | mannose-type O-glycan biosynthesis | 0 |
| Fktn | mannose-type O-glycan biosynthesis | 0 |
| Large1 | mannose-type O-glycan biosynthesis | 1 |
| Asah1 | glycosphingolipid metabolism | 0 |
| Ogt | other O-glycan biosynthesis; broad post-translational modification | 4 |

Hand-checked glycan/secretory-pathway comparators from the same training table were also mostly silent: B3gat3, Cog4, Cog5, Dpm1, Xylt1, Ext1, and Ext2 all had `n_degs = 0`, while Sptlc2 had `n_degs = 1`.

## Profile interpretation

Exact Parquet rows for the selected comparators in `151 TH Prkcd Grin2c Glut` confirmed that each perturbation had 17,259 measured genes in the focal group and reproduced the count-table calls. St3gal5, Large1, and Sptlc2 had only their own targeted transcript significant at FDR 0.05; Crppa, Fktn, Asah1, B3gat3, Cog4, Cog5, Dpm1, Ext1, Ext2, Stx5a, and Xylt1 had no significant measured genes in this focal class.

The broader reactive analogs were not strong quantitative donors for St3gal3:

- `Gfpt1` had 311 focal DEGs, but its profile was dominated by ER and integrated-stress-response genes such as Ddit3, Xbp1, Hspa5, Herpud1, Asns, Chac1, and aminoacyl-tRNA synthetases, consistent with hexosamine/ER-stress biology rather than terminal Golgi sialylation.
- `Ogt` was much weaker in the focal class with 4 DEGs and acts on intracellular O-GlcNAc rather than terminal Golgi alpha-2,3 sialylation of glycoprotein glycans.

Across all training cell classes in the declared Parquet, the closest focal comparators also stayed low: Crppa, Fktn, Dpm1, Ext1, Asah1, Cog4, Stx5a, and Xylt1 never had a significant gene in any assayed class; St3gal5, Large1, Sptlc2, B3gat3, and Ext2 never exceeded 1-2 significant genes in any assayed class.

## Synthesis

St3gal3 is expressed and its functional stock should decline enough over 21-28 days that complete invisibility is not the only plausible outcome. However, the perturbation is an acute, mosaic, survivor-conditioned loss of a terminal glycan-modifying enzyme with pre-installed glycan products and related ST3Gal family enzymes, and the available training genes closest to that chemistry overwhelmingly sit in the 0-1 DEG regime in this exact thalamic class. I therefore forecast no broad downstream transcriptional response, with the single expected DEG most plausibly representing the low-count/self-transcript regime rather than a multi-gene state shift.

Predicted `n_degs`: **1**
