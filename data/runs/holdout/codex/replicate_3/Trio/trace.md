# Trio n_degs prediction

## Target and endpoint

- Target: `Trio`, the single row in the declared `Trio.csv` manifest.
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` for `151 TH Prkcd Grin2c Glut`.
- Declared measurement table: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, 1,674 training perturbations.
- Declared profile table: `training_de_all_cell_groups.parquet`; only training perturbations were queried.

## Trio biology

The endpoint-blind Trio bundle shows strong focal expression reach: in matched non-target `151 TH Prkcd Grin2c Glut` nuclei, `Trio` was detected in 23,586 of 23,679 nuclei, or 99.607%, with mean raw UMI 9.135 and pseudobulk CPM 572.534. The same bundle adjudicates TRIO protein as likely substantially depleted by harvest because the P16 to P37-P44 interval spans many measured TRIO protein half-lives.

That argues that `Trio` is available and the perturbation can plausibly realize by harvest. It does not by itself imply a large nuclear RNA response: the direct mouse neural phenotype evidence is developmental cortical/hippocampal, the acute postnatal thalamic setting is unresolved, and the card notes possible Kalirin overlap for some excitatory-synapse functions.

## Training analogs

I used the annotation-backed gene analog nominee tool with `Trio`, mouse species, and the exact 1,674-gene training universe. The strongest non-fallback candidates were 15 members of netrin/DCC/Rac and Rho-family GTPase modules:

`Rac1`, `Fyn`, `Cdc42`, `Pik3r1`, `Limk1`, `Pak1`, `Arhgap32`, `Pik3r2`, `Kalrn`, `Dscam`, `Sos1`, `Fgd4`, `Chn1`, `Ocrl`, `Arhgef9`.

Same-experiment topology over these 15 candidates found a 12-gene component centered on the Rac/Cdc42/Kalrn/Pak/Limk/GEF/GAP genes. Resolved training Findings for `Rac1:F003`, `Kalrn:F002`, `Cdc42:F003`, and `Pak1:F004` all point in the same qualitative direction: represented Rac/Cdc42-linked actin-cytoskeleton perturbations were flat, singleton, or nonconvergent in juvenile neuronal snRNA-seq rather than forming a recurrent shared nuclear mRNA module.

## Measured focal responses of the analogs

In the declared count table, the 15 non-fallback analogs had counts:

| target | n_degs |
|---|---:|
| Rac1 | 0 |
| Fyn | 0 |
| Cdc42 | 1 |
| Pik3r1 | 0 |
| Limk1 | 0 |
| Pak1 | 1 |
| Arhgap32 | 0 |
| Pik3r2 | 0 |
| Kalrn | 0 |
| Dscam | 0 |
| Sos1 | 0 |
| Fgd4 | 0 |
| Chn1 | 0 |
| Ocrl | 0 |
| Arhgef9 | 1 |

Twelve of the 15 had zero `FDR < 0.05` genes and the three nonzero cases had exactly one. Direct Parquet aggregation confirmed that the single significant gene for `Cdc42`, `Pak1`, and `Arhgef9` was the corresponding targeted transcript itself; `Dscam`, `Fyn`, and `Sos1` had only one feature below `FDR < 0.10` and none below `FDR < 0.05`. Two additional explicit GEF/GAP comparators mentioned by the same-experiment Rac/Cdc42 reports, `Dock3` and `Arhgap18`, were also zero in the focal count table.

Profile comparison of the 15-gene analog cohort in `151 TH Prkcd Grin2c Glut` likewise found 12 nodes with no significant features and 3 nodes with 1 to 9 significant features. The closest Rho-family focal profiles showed weak whole-profile similarity and small signed top-feature overlaps, but no shared FDR-significant feature set.

For context, the full training endpoint was also highly sparse: 1,205 of 1,674 training perturbations were zero; the median was 0; the 75th percentile was 1; and only 43 training perturbations reached at least 100 DEGs. The narrow Trio analogs are therefore at the quiet end even relative to this sparse background.

## Synthesis

The Trio biology bundle makes a failed-expression or unreached-stock explanation unlikely: `Trio` is strongly detected in the assayed thalamic nuclei, and the protein stock should mostly clear by 21-28 days. However, the best task-matched evidence is that acute loss of the represented Rac/Cdc42/RhoGEF/RhoGAP actin-signaling neighborhood usually leaves little or no recurrent nuclear RNA footprint in the focal class. The only `FDR < 0.05` analog hits in this class were singleton self-transcript hits, which I treated as QC-like and not as a transferable downstream response.

I therefore predict that held-out `Trio` will land in the same buffered regime, with no confidently significant measured gene in `151 TH Prkcd Grin2c Glut`.

Predicted `n_degs`: 0
