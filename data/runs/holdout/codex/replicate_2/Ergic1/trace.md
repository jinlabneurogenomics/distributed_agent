# Ergic1 direct n_degs forecast

Target and endpoint:

- Manifest target: `Ergic1`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Declared measurement inputs used: the one-row holdout manifest, `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, `training_de_all_cell_groups.parquet`, the canonical Ergic1 biology bundle, and same-experiment corpus Findings for measured training comparators only.
- The withheld Ergic1 focal DE profile and the Ergic1 focal `n_degs` were not used.

## Target biology

The canonical Ergic1 bundle gives strong expression reach but unresolved functional realization in this exact experiment. In the matched non-target 151 population, `Ergic1` was available and expressed in 22,288 of 23,679 nuclei, `pct_cells_expressing = 94.1256`, `mean_raw_umi = 3.969`, and `mean_log1p_cp10k = 1.1445`. That makes the target transcript readily detectable in the assayed thalamic neurons.

The same bundle characterizes ERGIC1 as a cycling ER-ERGIC-Golgi membrane protein that interacts with/stabilizes ERGIC3, with homozygous constitutive mouse disruption causing complete-penetrance preweaning lethality. Those facts argue that Ergic1 is a real early-secretory-pathway perturbation, not an unexpressed or biologically inert locus.

The limiting target-specific evidence is that a P16 CRISPR edit stops new ERGIC1 synthesis but does not acutely remove the pre-existing ERGIC/ER/Golgi membrane pool. The biology card adjudicated `functional_stock_by_harvest = indeterminate`, with no target-specific half-life or post-edit clearance clock and no matched thalamic compensation test for ERGIC2/ERGIC3. I therefore treated the high expression as upward evidence for reach, but not as proof that most recovered P37-P44 neurons had a large ERGIC1-loss transcriptome.

## Training evidence

The declared 151 training count table contains 1,674 non-Ergic1 perturbations. It is sparse overall: 1,205 of 1,674 targets have `n_degs = 0`, the median is 0, the 90th percentile is 2, the 95th percentile is 18, and the mean is 14.05 because of a small high-count tail.

Exact Ergic-family targets were not available as count donors: `Ergic1`, `Ergic2`, and `Ergic3` had no rows in the focal training count table. I therefore used present ER/Golgi trafficking perturbations as rough same-compartment training examples rather than as one-to-one analogs.

Closest early-secretory-pathway training targets in the count table were almost all null in the focal class:

| perturbation set | targets present | focal `n_degs` |
| --- | --- | --- |
| COPII/ER export | `Sec23a`, `Sar1b` | 0, 0 |
| COPI/retrograde Golgi-ER | `Copa`, `Copg1` | 0, 1 |
| COG Golgi tethering | `Cog4`, `Cog5` | 0, 0 |
| TRAPP tethering/Rab activation | `Trappc6b`, `Trappc9`, `Trappc10` | 0, 0, 0 |
| ERGIC/Golgi-adjacent cargo or SNARE genes | `Lman2l`, `Stx5a`, `Stx16` | 0, 0, 1 |

Across those 12 closest trafficking examples, 10 were zero, the median was 0, the mean was 0.17, and the maximum was 1. Filtering the raw Parquet to `151 TH Prkcd Grin2c Glut` confirmed the same counts; the two nonzero cases were self-target-only signals: `Copg1` had only `Copg1` significant and `Stx16` had only `Stx16` significant. Their profiles therefore do not show a broader ERGIC stress state that would lift Ergic1 above zero.

I also checked nearby ER-proteostasis boundary perturbations. `Atf6`, `Vcp`, `Hspa5`, and `Sec63` had focal counts of 0, 2, 5, and 11. Their median was 3.5 and their maximum was 11, still small on the 151 scale. The significant rows show that `Sec63` and `Hspa5`, unlike the COPII/COPI/TRAPP examples, directly evoke ER chaperone or UPR genes: for example `Sec63` made `Hspa5`, `Canx`, `Hyou1`, and `Chac1` significant, while `Hspa5` made `Hsp90b1`, `Nfe2l1`, `Pdia4`, and `Derl3` significant. Same-experiment packaged Findings for `Sec63` likewise describe a selective 151 ER-chaperone/UPR transcriptome and partial phenocopy by `Hspa5`.

## Synthesis

Ergic1 sits upstream of membrane trafficking through the early secretory system, so I gave most weight to the ERGIC/COPI/COPII/TRAPP/SNARE training perturbations rather than to the `Sec63`/`Hspa5` ER client-folding stressors. Those closest measured neighbors are overwhelmingly 0 and, where nonzero, only self-transcript hits. The Ergic1 bundle supplies excellent expression reach and broad organismal importance, but same-context neuronal demand, ERGIC1 stock depletion by harvest, and ERGIC2/ERGIC3 compensation are unresolved. That uncertainty leaves room for a small positive tail count, but the best point estimate remains a focal near-null outcome.

Point forecast: `Ergic1` `n_degs = 0`.
