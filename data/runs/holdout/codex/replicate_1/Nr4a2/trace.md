target_name: Nr4a2
predicted_n_degs: 0

Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05`.

Evidence used:

- The declared manifest and biology bundle identify a single target, `Nr4a2`. The bundle is endpoint-blind and reports `target_outcome_exposed=false` in the canonical biology view.
- Functional stock supports real loss of function if a `151 TH Prkcd Grin2c Glut` neuron expresses and uses NR4A2: NR4A2 is a nuclear transcriptional regulator, endogenous Nurr1 is short-lived, mature-neuron deletion can nearly eliminate nuclear protein within one week, and the 21-28 day Perturb-seq interval should be long enough to deplete newly edited cells of functional protein.
- The exact focal-population expression reach is low. In the non-target nuclei for `151 TH Prkcd Grin2c Glut`, `Nr4a2` is detected in 1,584 of 23,679 nuclei, or 6.69%, with mean raw expression of 0.089 UMI per nucleus and pseudobulk expression of 5.61 cpm. That makes any Nr4a2-dependent state likely to be diluted in the class-aggregated perturbation contrast.
- The training count table is zero-inflated in this focal population: 1,205 of 1,674 training perturbations have zero DEGs; the median is 0, the 75th percentile is 1, the 90th percentile is 2, and only 59 targets exceed 50 DEGs.
- The most directly relevant assayed paralogs, `Nr4a1` and `Nr4a3`, both had `n_degs = 0` in the declared `151 TH Prkcd Grin2c Glut` training table. Direct Parquet checks in the same group recovered no significant genes for either target, with ordinary matched perturbed-cell counts for this screen slice (`Nr4a1`: 200 perturbed nuclei; `Nr4a3`: 218 perturbed nuclei; 23,679 matched controls).
- Some nuclear receptors and transcriptional regulators are large thalamic responders in training, for example `Rora` at 278 DEGs, `Tcf7l2` at 106 DEGs, and `Zfp423` at 150 DEGs. I treated those as evidence that the assay can see broad thalamic transcription-factor dependencies, but not as close analogs of `Nr4a2` because the biology bundle localizes the strongest established Nr4a2 programs to midbrain dopamine neurons and restricted habenular/diencephalic contexts rather than to a broadly expressed thalamic maintenance factor.

Synthesis:

Successful editing should remove NR4A2 protein on the screen timescale, so the point estimate should not be forced to a null for stock-persistence reasons. The limiting factor is instead reach: only a small minority of the aggregated thalamic nuclei show target transcript, and the two closest NR4A-family training perturbations were transcriptionally silent in this exact population. Against a training distribution whose first three quartiles are 0, 0, and 1 DEG, the best integer forecast is therefore a no-detectable-response outcome.
