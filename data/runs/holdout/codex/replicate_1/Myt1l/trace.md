# Myt1l prediction trace

## Requested endpoint

- Target: `Myt1l`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Withheld outcome status: the target profile and target count were not present in the declared count table or training parquet.

## Evidence used

1. **Biology-only target bundle**

   `Myt1l` was expressed in the exact focal non-target population: 23,238 of 23,679 non-target nuclei expressed the feature, or 98.14%, with mean raw UMI 6.24 and pseudobulk CPM 391.30. This supports reachability in the assayed cell class but was not treated as an editing-efficiency measure.

   The functional-stock adjudication called MYT1L a free/diffusible nuclear transcription-factor product whose new supply should stop after disruptive editing and whose operative stock was likely substantially depleted by P37-P44. The card also marked the evidence as partial because no endogenous postmitotic neuronal MYT1L half-life or direct P16-to-harvest clearance measurement was available.

   The observability card supported a postmitotic neuronal role from adult mouse brain and mouse hippocampal culture evidence, but with unresolved transfer to P16-edited thalamic glutamatergic neurons.

2. **Same-experiment corpus**

   `corpus.target_context` had no packaged Findings, Claims, or explicit comparator references for `Myt1l` in the selected PerturbAI July release. There was therefore no same-experiment semantic profile for this target to use.

3. **Training count table for `151 TH Prkcd Grin2c Glut`**

   The training table contained 1,674 perturbations and did not contain `Myt1l`. Its burden distribution was extremely zero-heavy:

   - 1,205 / 1,674 training perturbations had 0 DEGs.
   - The median was 0.
   - The mean was 14.05.
   - The 95th percentile was 18 DEGs.
   - Only 29 perturbations had more than 100 DEGs.

   This made a large count a special case requiring closer mechanistic support, not the default expectation.

4. **Typed mouse analog nomination**

   The analog nomination against the actual 1,674-gene training universe found no exact MYT-family paralog, no `Sin3b`, and no `Hdac2` in the training table. All 1,234 nominated available analogs were broad functional fallbacks through shared annotations, making them a transcription-factor context check rather than a close analog set.

   Among the top broad fallback candidates, the closest retinoic-acid and neurodevelopmental TF nominations were quiet in the requested class:

   - top 10: median 0, mean 0.3, maximum 2
   - top 20: median 0, mean 0.65, maximum 8
   - top 50: median 0, mean 10.42, with the mean pulled upward by the high-response `Ctnnb1` and `Tcf7l2`

5. **Expression-profile rows for task-matched training perturbations**

   The declared `training_de_all_cell_groups.parquet`, restricted to `151 TH Prkcd Grin2c Glut`, showed that the main nominated TFs and the chromatin/TF tail split sharply. The leading broad neurodevelopmental candidates were 0 to 2 DEGs, with `Crebbp` at 8. A separate broader regulatory tail was much larger: `Sin3a` 1,433; `Zbtb7a` 841; `Yy1` 720; `Cic` 576; `Thap11` 478; `Wac` 384; `Ctnnb1` 383; and `Tcf7l2` 106.

## Synthesis

`Myt1l` should not be treated like the many developmental TFs that are only weakly relevant or silent in this postnatal thalamic class: the exact bundle shows high in-class expression, MYT1L is an ongoing neuronal nuclear repressor, and the 21-28 day interval should be long enough for some functional-stock erosion. Those points move the forecast above the screen-wide zero mode.

At the same time, the strongest measured high-burden references were global chromatin or broadly coupled transcriptional regulators. MYT1L's reported SIN3B-HDAC2-associated repression makes the `Sin3a` phenotype directionally relevant, but MYT1L is a sequence-specific identity factor rather than the core co-repressor machinery itself, and the direct task-matched broad TF analogs near the top of the nomination were almost all null. The resulting forecast was a small but nonzero thalamic signature, just below the empirical 95th percentile of the training count distribution.

Predicted `n_degs`: 12
