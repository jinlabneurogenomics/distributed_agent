# Direct Lmx1a n_degs forecast

## Target and endpoint

- Target from the one-row holdout manifest: `Lmx1a`.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

## Evidence used

1. The canonical biology bundle identifies Lmx1a as a LIM-homeodomain nuclear transcription factor whose active protein stock is expected to be renewed rather than permanently installed. A disruptive P16 edit should stop new full-length Lmx1a production, and the bundle judged the functional stock likely substantially depleted by the P37-P44 harvest in genuinely edited, Lmx1a-expressing cells.

2. Exact focal expression is almost absent in the assayed population. In non-target `151 TH Prkcd Grin2c Glut` nuclei, the bundle reports:

   - `n_cells_expressing = 19`
   - `n_non_target_cells = 23679`
   - `pct_cells_expressing = 0.08023987499472106`
   - `total_target_umi = 21`
   - `mean_raw_umi = 0.0008868617762574433`
   - `mean_cp10k = 0.0006364128535530314`
   - `pseudobulk_cpm = 0.05558277243941569`

   This exact reach supersedes the qualitative thalamic-expression prior. It means nearly all recovered focal-class nuclei have no detectable Lmx1a transcript, so any cell-autonomous transcription-factor loss in the rare positive cells would be heavily diluted in the class-level differential-expression test.

3. The external-expression and phenotype facts in the same bundle do not argue for a broad postnatal thalamic dependency. Persistent postnatal Lmx1a expression was mapped mainly to selected hypothalamic, ventral-midbrain, and hindbrain/subthalamic populations, and an adult thalamic single-cell dataset detected Lmx1a in only 5 of 1,972 thalamic projection neurons. The clearest single-gene loss phenotype is embryonic neural patterning; the postmitotic maintenance evidence is combined `Lmx1a`/`Lmx1b` loss in adult midbrain dopaminergic neurons, not isolated `Lmx1a` loss in thalamus.

4. The declared `151 TH Prkcd Grin2c Glut` training count table has 1,674 measured training perturbations. Its endpoint distribution is highly zero-inflated:

   - 1,205 / 1,674 have `n_degs = 0`
   - 1,481 / 1,674 have `n_degs <= 1`
   - median `n_degs = 0`

   Thus a zero call is not a special outlier even in this high-yield class.

5. Same-context training analogues from the Lmx/dopaminergic and embryonic identity-factor neighborhoods were flat in the declared count table:

   - `Lmx1b`, the assayed close paralog: `n_degs = 0`
   - midbrain-dopamine and organizer regulators `Foxa2`, `Pitx3`, `Otx2`, `En1`, `En2`, `Pbx1`, `Pbx3`, `Gli1`, `Gli2`, `Nkx2-1`: all `n_degs = 0`
   - LIM/homeodomain or adjacent identity factors `Isl1`, `Lhx3`, `Lhx4`, `Phox2a`, `Phox2b`, `Mnx1`, `Agrp`, `Ptf1a`, `Neurod1`, `Atoh1`, `Tcf3`, `Tcf4`, `Pou4f3`: all `n_degs = 0`

6. Direct Parquet checks in `151 TH Prkcd Grin2c Glut` confirmed that those chosen comparators were not hiding near-FDR structure. For each listed comparator there were 17,259 tested measured genes; all except `Ache` had zero genes even at `pvals_adj < 0.10`. Representative minimum adjusted p-values were `1.0` for `Lmx1b`, `Foxa2`, `En1`, `En2`, `Gli1`, `Gli2`, `Nkx2-1`, `Pbx1`, `Pbx3`, `Atoh1`, `Neurod1`, `Ptf1a`, and `Tcf12`; `Pitx3` had minimum `0.751`, and `Isl1` had minimum `0.143`.

7. Packaged same-experiment corpus records reinforced the interpretation of those zeros. `Lmx1b:F001` reported that acute `Lmx1b` CRISPR was a pan-taxonomy transcriptional null across all recovered neuronal groups, and `Lmx1b:F002` reported no convergence between `Lmx1b` and represented midbrain-dopamine network perturbations. The `Isl1` corpus claim `claim:ad17b0adb8d721b08f70` summarized repeated flatness or lack of convergence across represented LIM-homeodomain, LDB/LIM-axis, and embryonic identity-factor perturbations in recovered postmitotic neuronal classes.

## Synthesis

The lesion should be real where P16-edited thalamic neurons are actually using Lmx1a, because Lmx1a is a renewable transcription-factor protein and the harvest is 21-28 days later. The decisive limitation is reach: only 0.080% of focal non-target nuclei contained any Lmx1a UMI, and the entire group contained 21 target UMIs among 23,679 nuclei. A large regulatory change confined to such a rare subset would be averaged down below the group-level Wilcoxon/BH threshold unless it spread into a much larger Lmx1a-negative population, and the bundle gives no mechanism for such non-cell-autonomous spread.

The measured training surface points the same way. The closest observed paralog and represented developmental transcription-factor comparators were exactly zero in the same focal count endpoint and flat in the raw Parquet; corpus summaries interpret this as a broader inactivity or buffering of embryonic identity programs in the acute P16 postmitotic assay rather than a single failed target. Because the generic prior in this focal class is already mostly zero and the target-specific biology is weaker than the flat `Lmx1b`/LIM-homeodomain neighborhood, the most likely integer is no significant genes. I keep a small chance of a one-gene idiosyncratic hit from rare-cell leakage or noise, but not enough to move the point estimate above zero.

Predicted `n_degs`: 0
