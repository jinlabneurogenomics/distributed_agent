# Dcaf17 direct DEG-count prediction

## Target and endpoint

- Target manifest: `Dcaf17`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Point prediction: `0`

## Evidence used

The declared holdout manifest contains the single target `Dcaf17`, and `Dcaf17` is absent from the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` training count table.

The focal-expression part of the declared biology bundle says `Dcaf17` is present but not broad or abundant in the exact assayed class: 8,578 of 23,679 matched non-target nuclei express it, `pct_cells_expressing = 36.226`, `mean_raw_umi = 0.480`, `mean_log1p_cp10k = 0.212`, and `pseudobulk_cpm = 30.113`. This keeps a response biologically possible but makes target engagement hard to convert into a guaranteed class-wide snRNA-seq signature.

The functional-stock card is weak for an acute transcriptomic endpoint. DCAF17 is described as a putative nuclear/nucleolar CUL4-DDB1 substrate receptor with unresolved physiological substrates; the card concluded that a disruptive edit should stop new intact DCAF17 synthesis but would not immediately erase pre-existing protein or pre-assembled complexes, and no DCAF17 protein half-life or CRL4-DCAF17 residence-time measurement in postmitotic neurons was found. Human biallelic disease and mouse testis phenotypes establish that loss can matter, but neither fixes the 21-28 day stock-depletion clock in P16-edited thalamic neurons.

The declared training-count table for this same cell group is strongly zero-inflated: 1,205 of 1,674 targets have `n_degs = 0`, the median is 0, only 193 targets exceed 1 DEG, and only 128 exceed 5 DEGs. Therefore a weakly expressed target with no specific recurrent response-state analog should stay near the zero mode rather than the long upper tail.

The closest available CRL4/DCAF substrate-receptor comparators supported the same direction. In the `151 TH Prkcd Grin2c Glut` count table, `Ddb2 = 0`, `Dcaf8 = 0`, and the adjacent chromatin comparator `Dnmt3a = 0`; `Setdb1`, which has a real but mechanistically less direct protocadherin/HUSH/KRAB-neighbor response, is only `22`. Direct Parquet queries also found `Ddb2` had zero FDR<0.05 or FDR<0.10 genes in every recovered neuronal group, while `Dcaf8` had zero in the requested thalamic group and only a single 155 MB Glut self-transcript hit across all queried groups. The same-experiment corpus reports for `Ddb2` and `Dcaf8` interpret those surfaces as basal neuronal buffering of DDB2 and DCAF8 rather than as strong hidden CRL4/DCAF transcriptional programs.

## Synthesis

I do not see an evidence chain that moves `Dcaf17` away from the null mode. Its in-assay RNA reach is sufficient for a possible self or downstream hit, and Woodhouse-Sakati genetics prevents treating the gene as irrelevant, but the acute P16-P37/P44 neuronal stock is unresolved and the named training analogs for nearby CRL4/DCAF biology are flat in this assay. I therefore predict the most likely integer endpoint as:

`predicted_n_degs = 0`
