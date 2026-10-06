# Smarcb1 n_degs forecast

Target and endpoint:

- Target from the one-row manifest: `Smarcb1`.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05` in the declared training count table's focal class.
- I did not use a `Smarcb1` perturbation profile or `Smarcb1` endpoint count.

Biology used:

- The declared biology bundle places SMARCB1/BAF47 in the renewable mammalian SWI/SNF core module and finds no close mammalian paralog occupying the same SMARCB1 core position.
- The same bundle adjudicates the operative stock as `likely_substantially_depleted` by P37-P44 after a P16 disruptive edit: the edit should stop new SMARCB1 supply, the 21-28 day interval is long relative to the regional thalamic proteome turnover proxy, and the main uncertainty is a missing target-specific juvenile-neuron half-life.
- Exact in-assay non-target reach was material but not complete: `Smarcb1` was detected in 15,357 of 23,679 non-target nuclei in `151 TH Prkcd Grin2c Glut` (`64.8549%`), with mean raw UMI `1.1511`.

Training measurements and same-experiment context:

- The focal training count table contains 1,674 observed perturbations. It is very zero-inflated: 1,205 targets have `n_degs = 0`, the median is 0, the 75th percentile is 1, the 95th percentile is 18, and only 43 targets reach 100 DEGs.
- Deterministic analog nomination against the declared training universe put mSWI/SNF candidates at the top by exact complex, BAF/nBAF/pBAF module, and physical-interaction evidence rather than by symbol text. The source cohort I then checked was `Smarca4`, `Smarcc1`, `Smarce1`, `Smarcd1`, `Arid1a`, `Smarca2`, `Smarcc2`, `Arid1b`, `Arid2`, `Bcl11a`, `Bcl11b`, and `Bicra`.
- Their focal `n_degs` values were small to moderate: `Smarca4 = 0`, `Smarcc1 = 0`, `Smarce1 = 11`, `Smarcd1 = 1`, `Arid1a = 22`, `Smarca2 = 1`, `Smarcc2 = 185`, `Arid1b = 1`, `Arid2 = 56`, `Bcl11a = 0`, `Bcl11b = 0`, `Bicra = 0`.
- Corpus topology over those 12 same-family candidates was dense in the explicit report-comparator lane: all 12 were in one connected component with 48 connected pairs out of 66 possible pairs. The 10-node mSWI/SNF set excluding `Bcl11a`/`Bcl11b` was fully connected in that lane.
- The material packaged BAF Claim was `claim:845db620c0afdfc1b86a`: it describes a subunit-selective 151 TH Prkcd Grin2c Glut BAF/mSWI/SNF module, converging most clearly through `Smarcc2`, `Smarce1`, and `Arid1a`, with partial `Arid2` and weak or flat relatives such as `Smarca4`, `Smarca2`, `Smarcc1`, `Bicra`, and `Arid1b`. I treated `Smarcc2:F003`, `Arid1a:F004`, and `Smarce1:F006` as the main same-experiment summaries supporting that boundary.
- The report-derived expansion from the 12 candidates returned nine eligible neighbors. Its source-plus-expansion counts were mostly null or low except for boundary/contrast nodes `Psmb4 = 742` and `Chd4 = 100`; because these were contrast or negative-neighbor expansions rather than the same BAF-core operation, they were context, not point anchors.

Profile checks:

- I profiled the complete 21-node source-plus-expansion set in the declared Parquet with `group_name == "151 TH Prkcd Grin2c Glut"`, `gene_target` as the entity, `names` as features, `logfoldchanges` as the signed value, and `pvals_adj < 0.05` as response-breadth metadata.
- The 10-node BAF subcohort had matched profiles for all 45 pairs. Its profile topology was recurrent but not a license to pool everything: 43 of 45 selected pairs had at least one nearest-neighbor edge in the 21-node profile topology, yet significant-program overlap was concentrated around the responsive arm rather than all BAF relatives.
- In the four observed responsive BAF/PBAF anchors closest to the Claim's active arm, the exact counts were `Smarcc2 = 185`, `Arid2 = 56`, `Arid1a = 22`, and `Smarce1 = 11`; their log1p center is about 40 DEGs. The six quieter BAF relatives in the same exact-complex/module neighborhood had counts `0, 0, 1, 1, 1, 0`.

Synthesis:

`Smarcb1` is a one-gene, expressed core BAF subunit whose functional stock should decline by harvest, so I did not collapse it to the many training perturbations or to the quiet all-BAF median. At the same time, the focal assay shows strong subunit selectivity: even exact-complex BAF relatives are often flat, `Smarcc2` is the only high same-family anchor, and the direct mouse neural phenotype for `Smarcb1` is developmental and cerebellar rather than a matched P16 postmitotic thalamic requirement. I therefore placed `Smarcb1` in the active but lower/middle BAF range, close to the log center of `Smarce1`/`Arid1a`/`Arid2`/`Smarcc2` and below the `Smarcc2` upper anchor.

Predicted `n_degs`: 42
