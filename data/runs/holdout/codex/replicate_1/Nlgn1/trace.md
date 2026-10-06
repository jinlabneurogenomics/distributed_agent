# Direct DEG-count forecast for Nlgn1

Target: `Nlgn1`

Cell class: `151 TH Prkcd Grin2c Glut`

Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.

## Evidence used

- The one-row holdout manifest names `Nlgn1`; the `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 other targets and does not contain `Nlgn1`.
- The declared Nlgn1 biology bundle reports exact in-assay focal expression in `151 TH Prkcd Grin2c Glut`: 10,867 of 23,679 non-target nuclei express `Nlgn1` (45.893%), with mean CP10K 0.449 and pseudobulk CPM 44.731. This supports target reach in the focal assayed population, but is only expression reach, not an Nlgn1 outcome.
- The same bundle adjudicates functional stock as likely substantially depleted by harvest. NLGN1 is a dynamic postsynaptic transmembrane adhesion/scaffold component at glutamatergic synapses; mouse postnatal CA1 conditional deletion at P21 produced an NLGN1-dependent functional loss within 2-3 weeks, matching the P16 to P37-P44 elapsed window in broad timing if not in exact thalamic region.
- The focal training count distribution is sparse: 1,205/1,674 targets are zero, the median is 0, the 75th percentile is 1, the 90th percentile is 2, and only 128/1,674 exceed 5 DEGs. A high value therefore needs strong endpoint-matched support.
- Species-safe typed analog nomination over the training universe prioritized the neurexin/neuroligin/synaptic organizer neighborhood. Non-fallback Nlgn1 nominees and their observed focal `n_degs` were low: `Nlgn3` 1, `Nrxn1` 1, `Nrxn2` 0, `Nrxn3` 0, `Lrrtm1` 1, `Lrrtm3` 0, `Lrrtm4` 0, `Dlg4` 1, `Shank3` 2, `Dlgap4` 2, `Magi2` 0, `Grm1` 1, `Grm5` 0, and `Grin2d` 0. Their median is between 0 and 1 and their mean is 0.64.
- Corpus explicit-Finding topology over that specific nominee set put the neurexin/neuroligin/LRRTM/PSD scaffold genes in a connected same-experiment report component, while broad co-annotation candidates such as `Crhr1` were not supported as close report comparators.
- Direct filtered rows from the declared training Parquet showed that most low positive focal counts in the close set were self-transcript threshold crossings rather than broad downstream programs:
  - `Nlgn3`: 1 DEG, `Nlgn3` itself, logFC -0.896, adjusted p 4.79e-11.
  - `Nrxn1`: 1 DEG, `Nrxn1` itself, logFC -0.518, adjusted p 2.67e-23.
  - `Dlg4`: 1 DEG, `Dlg4` itself, logFC -0.444, adjusted p 1.15e-08.
  - `Grm1`: 1 DEG, `Grm1` itself, logFC -0.438, adjusted p 4.28e-05.
  - `Shank3`: 2 DEGs, including `Shank3` itself.
  - `Dlgap4`: 2 DEGs, including `Dlgap4` itself.
  - `Lrrtm4`, `Nrxn2`, `Nrxn3`, `Grm5`, `Lrrtm3`, `Magi2`, `Grin2d`, and `Crhr1` had no focal significant genes.
- `Grin1` was the outlier among broader synaptic annotations, with 89 focal DEGs. I treated it as an NMDA-receptor-core boundary rather than as the scale analog for Nlgn1 because the closer adhesion and scaffold perturbations above were consistently 0-2.

## Synthesis

Nlgn1 is expressed in a large enough fraction of the focal non-target thalamic nuclei that an edited transcript could plausibly clear the Wilcoxon/BH threshold, and its synaptic surface stock should be renewed within the experiment. That argues against treating Nlgn1 as unreachable or biologically inert.

The task-matched quantitative evidence points the other way on breadth. The closest training perturbations in the neurexin/neuroligin/LRRTM neighborhood have almost no downstream nuclear-RNA response in `151 TH Prkcd Grin2c Glut`; when they are positive, the count is usually the perturbed transcript itself. A broad Grin1-like program is possible for central ionotropic receptor loss but is not the expected scale for an adhesion molecule whose mature-neuron phenotypes can be electrophysiologic without structural synapse elimination.

I therefore placed Nlgn1 just above zero: likely enough for one significant row, but with little support for multiple downstream DEGs.

Predicted `n_degs`: 1
