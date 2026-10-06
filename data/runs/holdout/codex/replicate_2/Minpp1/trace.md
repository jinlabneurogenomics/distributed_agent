target_name: Minpp1
predicted_n_degs: 1

Evidence used

- The held-out manifest and canonical biology bundle both identify `Minpp1`; `Minpp1` is absent from the declared `151 TH Prkcd Grin2c Glut` training count table.
- Exact target reach in the held-out focal population is positive: 16,758 / 23,679 non-target nuclei expressed `Minpp1` in `151 TH Prkcd Grin2c Glut` (70.77%; mean 0.899 CP10K, mean raw UMI 1.466). This supports reach of the perturbation in the assayed population but was not treated as an editing-efficiency measurement.
- The biology-only bundle characterizes MINPP1 as a renewable ER-lumen inositol-polyphosphate phosphatase. Loss eliminates continuing supply of a soluble-metabolite enzyme with a mouse epithelial half-life of about 14.7 h, so pre-edit catalytic stock is expected to clear within the 21-28 d P16-to-harvest window. Counterweight: the closest neural phenotypes are germline/developmental and conflicting or mild, and postnatal thalamic dependence is unresolved.
- The focal-class training table is strongly zero-inflated: 1,205 / 1,674 training targets have `n_degs = 0`, the median is 0, the 90th percentile is 2, the 95th percentile is 18, and only 43 targets exceed 100 DEGs. A target-specific positive response therefore needs more than target expression and functional realization.
- Training genes intersecting the Minpp1 pathway were almost transcriptionally quiet in the same class. Primary soluble inositol/phosphoinositide comparators had counts:
  - `Inpp5k` 0
  - `Ocrl` 0
  - `Plcb1` 0
  - `Ppip5k2` 0
  - `Synj1` 1
  - `Pi4kb` 1
  - `Bpnt2` 1
  - `Dgke` 1
  The mean and median over this closer set were both 0.5.
- Broader ER-homeostasis comparators remained small in aggregate: `Atf6` 0, `Hspa5` 5, `Edem3` 0, `Sec63` 11, `Sil1` 0, `Manf` 3, `Bcap31` 1, `Copa` 0, `Copg1` 1, `Stx5a` 0, `Tango2` 0, `Tmem165` 0; median 0 and mean 1.75.
- Calcium-handling genes included clear larger outliers, especially `Atp2a2` at 187 and `Atp2b1` at 22, but the matched bridge from Minpp1 loss to an acute thalamic calcium-pump-like state was weak. More receptor/second-messenger genes stayed small: `Itpr1` 0, `Calm2` 0, `Micu1` 0, `Ryr2` 0, `Ryr3` 0, `Atp2b2` 1, `Atp2b3` 1, `Calm3` 1, `Ppp3ca` 4, `Ppp3r1` 9, `Calm1` 14.
- A profile comparison over 14 selected inositol, ER, and calcium comparators in `151 TH Prkcd Grin2c Glut` confirmed low measured activity for the closest IP genes: `Inpp5k`, `Ocrl`, `Plcb1`, and `Ppip5k2` had zero significant features among 17,259 measured genes, and `Synj1` had one. Pairwise significant-feature intersections between those five and broader ER/calcium peers were all zero in the inspected table, so the broader, higher-count `Atp2a2` profile did not provide a coherent shared significant program to transfer to `Minpp1`.

Synthesis

I set the point above zero because `Minpp1` is expressed in the exact focal cells, is expected to be functionally depleted by harvest, has no close paralog, and controls IP5/IP6 pools rather than a one-shot developmental structure. I kept it at the near-zero edge because the best matched training perturbations in inositol-phosphate metabolism were 0-1 DEG in this thalamic class, the ER-stress comparators were mostly silent or single-digit, and the stronger calcium/ER ATPase outliers represented a more direct calcium-store failure than Minpp1 loss. The resulting direct forecast is a low positive response of 1 BH-significant gene.
