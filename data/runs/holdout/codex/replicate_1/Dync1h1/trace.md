# Direct `n_degs` prediction for `Dync1h1`

## Target and endpoint

- Target from the one-row holdout manifest: `Dync1h1`.
- Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with Wilcoxon `pvals_adj < 0.05`.
- Declared count table used for observed training endpoints: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared expression table used for profile checks: `training_de_all_cell_groups.parquet`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"`.
- `Dync1h1` itself was absent from the training count table and was not queried as an outcome profile.

## Biology bundle

The target bundle marks `Dync1h1` as the force-generating heavy-chain/scaffold component of cytoplasmic dynein-1. The CRISPR operation is expected to truncate or stop new functional DYNC1H1 production; pre-existing heavy-chain pools are not destroyed immediately, but the functional-stock card concludes that operative dynein-1 stock is likely substantially depleted by the 21-28 day harvest window.

The exact focal-population reach is strong: in non-target `151 TH Prkcd Grin2c Glut` nuclei, `Dync1h1` is detected in 23,457 of 23,679 nuclei, with 99.06% of cells expressing and mean log1p CP10k of 1.717. This supports reach of the perturbation in the focal population but was not used as an editing-efficiency surrogate.

The main downward caveats are that old DYNC1H1 protein can persist after gene deletion in some retinal pools and that the best timed mouse evidence comes from photoreceptors rather than juvenile thalamic neurons. Those caveats make a `Rab7`-scale lysosomal collapse unlikely, but not a complete null.

## Local training measurements

The focal count table is sparse overall:

- 1,674 training perturbations.
- Median `n_degs` = 0.
- Mean `n_degs` = 14.05.
- 75th/90th/95th/99th percentiles = 1/2/18/430.
- 469 of 1,674 targets were nonzero; only 43 reached at least 100 DEGs.

Mechanistically relevant or boundary perturbations in the focal count table were:

| training target | focal `n_degs` | interpretation |
|---|---:|---|
| `Dctn1` | 75 | closest measured dynein/dynactin motor-complex analog |
| `Rab7` | 501 | late endosome/lysosome stress, broader than a dynein motor perturbation |
| `Vps54` | 31 | visible Golgi/retrograde trafficking response restricted to 151 |
| `Vps35` | 17 | modest canonical retromer/endosomal response |
| `Mib1` | 27 | closest Dctn1 positive-tail neighbor in the all-training profile neighborhood |
| `Marchf6` | 14 | Dctn1 sterol-response neighbor |
| `Selenoi` | 5 | Dctn1 sterol-response neighbor |
| `Depdc5` | 13 | Dctn1/Rab7 sterol/endolysosomal neighbor |
| `Tsc2` | 86 | Dctn1/Rab7/mTOR-linked neighbor with a stronger positive state |
| `Cltc` | 3 | core endocytic perturbation but weak in this group |
| `Kif1a`, `Kif5a`, `Kif5c`, `Klc1`, `Klc2` | 1 each | kinesin anterograde motor boundaries |
| `Dync2h1`, `Dync2i1` | 0 each | distinct ciliary dynein-2 boundaries |
| `Atg5`, `Becn1`, `Sqstm1` | 0, 0, 1 | autophagy-initiation/cargo boundaries |

Direct counts recomputed from the Parquet for the most material entries matched the count table: `Dctn1` 75, `Rab7` 501, `Vps54` 31, `Vps35` 17, `Cltc` 3, both dynein-2 entries 0, and kinesin/autophagy controls at 0-1.

## Profile and corpus interpretation

The same-experiment Dctn1 report identifies the main Dctn1 consequence as a recurrent SREBF2-like cholesterol biosynthesis and uptake module, not direct up-regulation of dynein/dynactin components or a generic injury program. In the exact focal Parquet profile, `Dctn1` had 75 significant genes split into 49 positive and 26 negative calls; its highest positive features were sterol genes including `Insig1`, `Msmo1`, `Hmgcs1`, `Cyp51`, `Hmgcr`, and `Fdft1`.

`Rab7` had a much larger focal surface: 501 significant genes, 311 positive and 190 negative. Its corpus report describes recurrent late-endosomal/lysosomal, V-ATPase, sterol/lipid, UPR/ISR, proteasome, and synaptic downshift arms. I treated this as an upper stress reference for organelle trafficking failure, because DYNC1H1 loss should disturb retrograde cargo movement upstream but need not reproduce a direct late-endosomal Rab7 loss.

`Vps35` and `Vps54` bounded the expected scale for trafficking lesions that are visible but not Rab7-like. `Vps35` produced a focal retromer/endosomal response without a broad lysosomal stress program, while `Vps54` produced a 151-restricted Golgi/retrograde trafficking state biased toward neuronal signaling and neurite transcripts. Their focal `n_degs` values, 17 and 31, are lower than Dctn1 but show that trafficking perturbations can be detectable in this cell class.

The all-training profile neighborhood of `Dctn1` did not point to a hidden same-scale motor family. Its nearby positive-tail neighbors were mostly the small-to-moderate sterol/traffic entries `Mib1` 27, `Marchf6` 14, `Selenoi` 5, and `Depdc5` 13, with `Tsc2` 86 as a higher mTOR-linked comparator. Represented ciliary dynein-2, kinesin, clathrin, and core autophagy perturbations were flat or nearly flat and had no meaningful same-direction significant overlap with `Dctn1`.

## Synthesis

`Dync1h1` should be closer to `Dctn1` than to the zeros: it is the dynein-1 heavy chain, is present in essentially all focal nuclei, and the target-specific functional-stock card supports material loss over the screen window. But there is no exact dynein-1 heavy-chain donor in training, and the Dctn1 sterol module is a secondary survivor-cell state whose amplitude could be weakened by DYNC1H1 protein persistence and by survivor conditioning.

I therefore placed the point slightly below the direct `Dctn1` anchor of 75, above the Vps54/Vps35 and Dctn1-neighbor 5-31 range, and far below the 501-gene `Rab7` late-lysosomal collapse.

Predicted `n_degs`: **64**.
