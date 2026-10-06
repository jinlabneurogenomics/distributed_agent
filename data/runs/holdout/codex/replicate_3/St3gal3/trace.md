# Direct forecast for St3gal3 in 151 TH Prkcd Grin2c Glut

## Endpoint and target

- Endpoint: number of `151 TH Prkcd Grin2c Glut` measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Held-out target: `St3gal3`, from the one-row manifest.
- I used the declared target biology bundle, the `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` count table, and targeted rows from the declared `training_de_all_cell_groups.parquet`. I did not use the withheld St3gal3 DE signature or count.

## Target biology

The St3gal3 bundle supports a real but probably buffered acute perturbation:

- Exact focal-population reach is high enough that target absence is not the main reason to expect a null: in matched non-target `151` cells, `St3gal3` was detected in 14,416 of 23,679 nuclei, 60.88%, with mean CP10K 0.663 and mean raw UMI 1.065.
- ST3Gal-III is a Golgi enzyme that installs alpha-2,3 sialic acid on type I/II lactosamine motifs, mainly on glycoprotein glycans. The functional-stock card judged that active enzyme plus newly renewed carrier glycans should be substantially depleted over the 21-28 day P16-to-P37/P44 window.
- Existing modified carrier proteins can persist after editing, individual carrier kinetics are not known, and other ST3Gal enzymes have overlapping acceptor classes. Those facts make a broad, immediate nuclear RNA response less likely than for upstream ER glycosylation-supply lesions.

## Training measurements that set the scale

The count table for this exact cell class is dominated by silent or near-silent perturbations:

- 1,205 of 1,674 training targets had `n_degs = 0`.
- 1,481 of 1,674 had `n_degs <= 1`.
- The median was 0, the 75th percentile was 1, and the 90th percentile was 2.
- The mean, 14.05, was inflated by a small long tail, so it is a poor prior for a terminal sialyltransferase.

I then checked same-class Parquet rows for glycan, Golgi, lysosomal glycosylation, and related secretory-pathway targets present in training:

- Directly adjacent terminal or carrier-processing examples were flat or one-hit in `151`: `St3gal5 = 1`, `Gaa = 1`, `Large1 = 1`, `B3gat3 = 0`, `Dpm1 = 0`, `Fktn = 0`, `Glce = 0`, `Gnptab = 0`, `Gnptg = 0`, `Hs6st2 = 0`, `Pign = 0`, `Tmem165 = 0`, and `Xylt1 = 0`.
- The significant rows for `St3gal5`, `Gaa`, and `Large1` were only the cognate self transcript in this class, consistent with a biochemical glycan lesion being visible to the guide/readout but not spreading into a large survivor RNA program.
- The broad exceptions, `Gfpt1 = 311` and `Dhdds = 116`, were not good point analogues for St3gal3. Their Parquet hits and corpus reports were dominated by ER quality-control and ISR/UPR genes such as `Hspa5`, `Hsp90b1`, `Sdf2l1`, `Herpud1`, `Ddit3`, `Chac1`, `Asns`, and amino-acid/one-carbon response genes, as expected for hexosamine or dolichol supply failures upstream of N-linked glycoprotein folding rather than loss of one terminal sialyltransferase.

## Synthesis

St3gal3 is expressed in the assayed non-target thalamic nuclei and the biology bundle argues that loss of catalytic function can be realized within the multiweek window, so I did not assign a hard zero. However, the most scale-matched observed perturbations in terminal glycosylation or ganglioside-related biology were almost all 0-1 DEG profiles; only broader precursor-supply perturbations induced the large ER-stress states.

I therefore put the forecast at a single narrow FDR-significant feature, plausibly the target transcript itself or one nearby secondary responder, rather than a Dhdds/Gfpt1-like stress program.

Predicted `n_degs`: **1**
