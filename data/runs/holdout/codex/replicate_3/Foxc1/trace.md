# Foxc1 `n_degs` prediction

## Target and endpoint

- **Target:** `Foxc1`
- **Cell class:** `151 TH Prkcd Grin2c Glut`
- **Endpoint:** number of measured genes with BH-adjusted Wilcoxon `p < 0.05` in the focal class.
- **Permitted target prior used:** `biology_bundles/Foxc1.json`, through the canonical `biology` view, with no target DE signature, target DEG count, labeled neighbor outcomes, scalar prior, or calibrated probability.

## Evidence that set the prediction

1. **Foxc1 has vanishingly small exact reach in the assayed focal neurons.** The canonical bundle reports detectable `Foxc1` RNA in 154 of 23,679 non-target `151 TH Prkcd Grin2c Glut` nuclei, i.e. 0.650365% of cells, with mean raw UMI 0.00726, mean log1p CP10K 0.00311, and pseudobulk CPM 0.455. Because the endpoint is an aggregate survivor-conditioned snRNA-seq contrast over the focal neuronal class, this reach makes even a complete effect in the rare Foxc1-positive nuclei highly diluted.

2. **The biological prior supports stock clearance but not neuronal deployment.** FOXC1 is a renewable nuclear forkhead transcription factor, and the functional-stock card adjudicates pre-edit FOXC1 as likely substantially depleted by P37-P44 in any successfully edited cell that expressed the gene at P16. That removes durable-stock persistence as the main reason to expect quietness. The same bundle instead places Foxc1 function mainly in developmental meningeal, pericyte, and vascular compartments, reports low adult thalamic bulk signal with Allen regional non-detection, and states that its mouse loss phenotypes are developmental or neural-adjacent rather than direct evidence for a post-P16 thalamic neuronal requirement.

3. **The task-matched count table is zero-inflated at this threshold.** In the declared `151 TH Prkcd_Grin2c_Glut_deg_counts_training.csv` table, 1,205 of 1,674 training perturbations have `n_degs = 0`, the median is 0, the 75th percentile is 1, and the 90th percentile is 2. Thus a weak or poorly deployed perturbation is expected to land at zero rather than at a small positive count.

4. **Forkhead and developmental transcription-factor comparators also favor zero when they are not active in this cell class.** The closest declared paralog, `Foxc2`, has `n_degs = 0`. Every measured Fox-family training perturbation in the focal count table is zero: `Foxa2`, `Foxc2`, `Foxe3`, `Foxi1`, `Foxj3`, `Foxk2`, `Foxl1`, `Foxl2`, `Foxn1`, `Foxp2`, and `Foxp3` all have `n_degs = 0`. Other developmental or patterning TFs with poor expected deployment in thalamic postmitotic neurons are also mostly zero, including `Pax6`, `Nkx2-1`, `Otx2`, `Pitx2`, `Atoh1`, and `Tbr1`.

5. **The expression Parquet supports the zero counts for these analogs with full focal profiles.** Filtering `training_de_all_cell_groups.parquet` to `151 TH Prkcd Grin2c Glut` confirmed 17,259 measured rows apiece for the Fox-family analogs above and no BH-significant gene in any of them. For `Foxc2`, the closest family member, the focal profile had 277 matched perturbed nuclei versus 23,679 controls, zero adjusted-p hits, and a best adjusted p-value of 0.809.

## Synthesis

FOXC1 loss can plausibly be realized inside an edited Foxc1-expressing cell by the 21-28 day harvest, so the point is not forced to zero by protein persistence. The decisive constraint is instead that the exact focal population contains almost no Foxc1 RNA and the strongest biological localization evidence points outside NeuN-positive thalamic neurons. A thalamic neuronal perturbation can produce hundreds of DEGs when an expressed regulator is relevant in this class, as in `Tcf7l2` and `Rora`, but Foxc1 matches the Fox/fate-factor training perturbations that are transcriptionally silent in this context. I therefore predict no genes crossing BH-adjusted `p < 0.05`.

**Predicted `n_degs`: 0**
