# Direct Jarid2 n_degs forecast

## Target and endpoint

- Target manifest: `Jarid2`.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes in this class with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Declared held-out status: `Jarid2` was absent from the `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` response-count table and from the declared `training_de_all_cell_groups.parquet` training profile rows.

## Evidence used

1. **Jarid2 biology-only bundle**

   The exact in-assay non-target expression reach is high: `Jarid2` was detected in 19,761 of 23,679 matched non-target nuclei in the focal class, or 83.45%, with mean raw UMI 2.118 and pseudobulk CPM 132.75. Thus the transcript itself is well measured in `151 TH Prkcd Grin2c Glut`.

   The functional-stock card does not support an acute, complete loss state by P37-P44. It calls JARID2 a PRC2/chromatin accessory with multiple functional pools and concludes `functional_stock_by_harvest = partially_depleted_or_leading_edge`: new JARID2 synthesis should stop after a disruptive P16 edit, but existing JARID2, preinstalled H3K27me3/locus states, unknown PRC2.2 residence, and MTF2-linked PRC2 recruitment can preserve part of the function. The observability card also says the direct neural loss evidence is developmental mouse retina/neural-tube evidence, not a matched postmitotic thalamic requirement.

2. **Training response-count distribution for the same class**

   The declared 151-class count table contains 1,674 observed training perturbations. It is zero-inflated: 1,205/1,674 have `n_degs = 0`, 1,481/1,674 have `n_degs <= 1`, the median is 0, the 90th percentile is 2, and only 106/1,674 reach 10 DE genes. Very large footprints exist but are rare and dominated the mean.

3. **Biology-matched training measurements**

   Direct PRC2-core and PRC2.2 comparators such as `Eed`, `Ezh1`, `Ezh2`, `Suz12`, `Aebp2`, `Mtf2`, `Phf1`, `Phf19`, `Rbbp4`, and `Rbbp7` are not in the declared count table, so I used broader measured chromatin regulators as weak analogs rather than a direct PRC2 average.

   Their 151-class counts split into a low/moderate chromatin set and broad high-yield transcriptional outliers:

   - closer low/moderate chromatin regulators: `Kdm6b = 0`, `Dnmt3a = 0`, `Arid1b = 1`, `Ehmt1 = 4`, `Brd1 = 4`, `Crebbp = 8`, `Atrx = 8`, `Setd5 = 9`, `Kdm5c = 18`, `Arid1a = 22`, `Setdb1 = 22`, `Kmt2a = 24`;
   - broader pleiotropic outliers: `Brd4 = 311`, `Setd1a = 368`, `Yy1 = 720`, `Sin3a = 1433`.

   A symmetric profile comparison on these measured donors in `151 TH Prkcd Grin2c Glut` reproduced the same activity split: two of the selected nodes had no significant features, several had 1-9 or 10-49, and only the broad outliers had at least 50. That made the high `Sin3a`/`Yy1`/`Setd1a` counts poor numeric anchors for a buffered PRC2 accessory.

4. **Singleton behavior in the declared Parquet**

   In the 151-class Parquet rows, the significant-row total at `pvals_adj < 0.05` matched the supplied count table exactly, at 23,526 rows. Among the 276 training targets with exactly one significant gene, 237 singleton calls, 85.9%, were self-transcript calls. `Arid1b`, the measured chromatin donor with `n_degs = 1`, was self-only.

## Synthesis

Jarid2 has strong expression reach, so a one-gene self-transcript footprint is plausible. Its downstream state should be much weaker than acute loss of spliceosome, proteasome, mediator, or global chromatin/transcriptional regulators: JARID2 is an accessory PRC2 recruitment/regulatory subunit, the P16-to-P37/P44 window only partially depletes the relevant stock, and alternative PRC2 recruitment plus pre-existing chromatin can buffer the loss.

The measured donors closest to this qualitative situation live near 0-24 DE genes rather than in the hundreds. Given the zero-inflated empirical distribution and the weak postmitotic PRC2-accessory projection, I would not forecast a broad downstream program. The high baseline expression keeps the prediction just above the modal zero because the included self-target transcript can plausibly be the only FDR-significant feature.

**Predicted `n_degs`: 1**
