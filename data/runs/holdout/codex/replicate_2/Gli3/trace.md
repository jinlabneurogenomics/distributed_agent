# Trace

Target: `Gli3` in `151 TH Prkcd Grin2c Glut`.

Endpoint: `n_degs`, the number of measured genes in the focal thalamic glutamatergic class with BH-adjusted Wilcoxon `p < 0.05`.

## Evidence used

- Declared target biology bundle, `biology_bundles/Gli3.json`: the in-assay focal population contains detectable `Gli3` RNA in only 83 of 23,679 non-target nuclei, 0.350521559%, with mean expression 0.003210283 cp10k and pseudobulk 0.338790232 CPM. That makes any postnatal GLI3-dependent program very dilute in this aggregated class-level Wilcoxon contrast.
- The same bundle identifies GLI3 as a Hedgehog-pathway transcriptional regulator carried by full-length and processed repressor protein pools. Those pools are expected to turn over before the P37-P44 harvest after a P16 edit, so a successfully edited `Gli3`-expressing cell could lose GLI3 function; however, the closest mouse neural loss evidence is embryonic cortical progenitor deletion, not acute loss in postmitotic thalamic neurons, and compensation by `Gli1`/`Gli2` in this population is unresolved.
- Declared focal training count table, `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: the same endpoint is sparse across observed training perturbations, with 1,205 of 1,674 targets equal to zero, median 0, 75th percentile 1, and 95th percentile 18.
- Biologically adjacent training perturbations in the count table were quiet in this focal class: `Gli1`, `Gli2`, `Ptch1`, `Ptch2`, `Smo`, `Gpr161`, and `Ift88` all had `n_degs = 0`. Broader regulatory comparators just outside the core GLI module were also small rather than large: `Prkaca = 1`, `Gsk3b = 6`, and `Csnk2b = 25`.
- A same-cell-class profile comparison over those ten training perturbations from `training_de_all_cell_groups.parquet`, written to `evidence/hh_gli_profile_compare.json` and summarized in `evidence/hh_gli_profile_cohort.json`, agreed with the direct count table: seven of ten had no significant features, two had only 1-9 significant features, and one had 10-49. The selected cohort also had low signed top-tail recurrence across expression signatures, with mean positive top-tail overlap 0.04444444 and mean negative top-tail overlap 0.06622222, so the quiet core Hedgehog/GLI counts did not hide a coherent near-threshold module.

## Synthesis

`Gli3` has plausible intracellular target engagement if an expressing neuron is edited, but the exact focal-population reach is the dominant quantitative constraint: only about 0.35% of the assayed non-target nuclei show any `Gli3` RNA. The class-level DE test pools a much larger thalamic glutamatergic population, so even a real response in rare GLI3-positive cells is likely diluted below FDR detection. The developmental neural phenotype is also a poor timing and cell-state match for a P16 edit in already postmitotic thalamic neurons. The focal training table reinforces this: the GLI paralogs and several upstream Hedgehog/ciliary transducers with measured profiles all sit at zero, while the only nonzero adjacent regulatory rows are weak and nonspecific.

I therefore predict that the held-out `Gli3` perturbation will be a zero-burden target in `151 TH Prkcd Grin2c Glut`.
