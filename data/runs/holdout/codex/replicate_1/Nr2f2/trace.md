## Prediction trace

Target: `Nr2f2` in `151 TH Prkcd Grin2c Glut`.

Endpoint: `n_degs`, the number of measured genes in this focal population with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

Declared inputs used:

- `Nr2f2.csv`: one held-out manifest row, `Nr2f2`.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: visible training counts for 1,674 targets in the exact focal population.
- `training_de_all_cell_groups.parquet`: training-only differential-expression rows, queried only for measured training targets in `151 TH Prkcd Grin2c Glut`.
- `biology_bundles/Nr2f2.json`, also served through `characterization_bundle(target="Nr2f2", view="biology")`: prediction-safe target biology, exact focal expression reach, and functional-stock adjudication with no target outcome or labeled-neighbor outcomes exposed.
- Same-experiment corpus `target_context` records for measured training comparators `Rora`, `Nr2f1`, and `Rorb`; these were used to interpret those already visible training perturbations, not as independent replication.

The focal count table is strongly zero-inflated and heavy-tailed. Among the 1,674 visible training targets, 1,205 had `n_degs = 0`; the median was 0, the 75th percentile was 1, the 90th percentile was 2, the 95th percentile was 18, and a few broad perturbations reached hundreds or thousands of DE genes. The unconditional mean, 14.05, is therefore not a good forecast for a target without evidence for a large survivor-state program.

The prediction-safe `Nr2f2` bundle argues for biological reach but not for a large acute maintenance phenotype. NR2F2 is a sequence-specific nuclear-receptor transcription factor, and in the focal non-target population `Nr2f2` was detected in 12,024 of 23,679 nuclei, with 50.78% expressing cells, mean 0.714 CP10K, and pseudobulk 74.8 CPM. That makes a true effect plausible in `151`. The counterweights are that the mouse causal loss evidence is developmental cerebellum or hippocampus rather than acute juvenile thalamus, the post-edit depletion of pre-existing NR2F2 receptor stock by P37-P44 is unresolved, and related `Nr2f1` can overlap functionally in development without a demonstrated post-P16 thalamic compensation model.

Measured focal-population analogs put the most weight on a low single-digit count. The close paralog `Nr2f1` had 2 DE genes in this exact count table; `Nr2c2` and `Thra` each had 3; `Nr1d2` had 1; and `Rorb`, `Rorc`, `Rarb`, `Rarg`, `Rxra`, `Thrb`, `Ar`, `Ahr`, and `Arnt` were all 0. The high nuclear-receptor/circadian responders, `Rora` at 278 and `Nr1d1` at 116, looked like specific thalamic output programs rather than a family-wide scale. Corpus summaries reinforced that interpretation: `Rora` loss produced a broad down-dominant 151 signature that `Rorb`/`Rorc` did not phenocopy, while `Nr2f1` was summarized as a sparse postnatal neuronal response with only `Sorl1` and `Sema7a` crossing FDR<0.10 in 151.

I therefore predicted a detectable but very small focal response. The exact target expression moves `Nr2f2` above the fully flat analogs, while developmental timing, unresolved receptor-stock turnover, mosaic postmitotic editing, and the sparse `Nr2f1`/`Nr2c2` measurements keep it far below the broad `Rora`/`Nr1d1` class.

Predicted `n_degs`: 3
