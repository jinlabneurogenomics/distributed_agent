# DEG-count prediction trace

## Question and endpoint alignment

The requested endpoint is a scalar prediction for the held-out perturbation `Edar`: the number of measured genes in `151 TH Prkcd Grin2c Glut` cells with Wilcoxon Benjamini-Hochberg adjusted `pvals_adj < 0.05`.

I treated the training CSV as the direct endpoint for non-held-out targets and the Parquet rows as direct per-gene focal-cell differential-expression evidence for those same training perturbations. `Edar` itself was held out from both inputs, so its count is absent by design and must be inferred from non-held-out analogs plus biology of the EDA/EDAR pathway. The endpoint is a response-breadth statistic in recovered postnatal neuronal nuclei; it is not direct evidence for organismal ectodermal phenotypes, target transcript knockdown, viability, or developmental requirement.

## Sources

- Declared endpoint: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression table: `training differential-expression dataset`, restricted to `group_name == "151 TH Prkcd Grin2c Glut"`.
- Run-local manifest and context: `task_bindings.json`, `coverage.json`, `measurement_registry.json`, and the PerturbAI atlas dataset portrait.
- External pathway and mechanism knowledge from PubMed literature:
  - Mikkola and Thesleff 2003, DOI `10.1016/s1359-6101(03)00020-0`: EDA-A1 binds EDAR and mutations in EDA, EDAR, and pathway components cause hypohidrotic ectodermal dysplasia through impaired NF-kappaB signaling during ectodermal appendage development.
  - Morlon, Munnich, and Smahi 2005, PMID `16251197`, DOI `10.1093/hmg/ddi405`: EDARADD recruits the TAB2/TRAF6/TAK1 complex and activates IKK/NF-kappaB downstream of EDAR.
  - Lefebvre and Mikkola 2014, PMID `24928340`, DOI `10.1016/j.smim.2014.05.002`: review of the EDA/EDAR axis as a developmental TNF-family pathway for hair, tooth, and gland morphogenesis.

I did not use the same-experiment Findings graph to score or rank `Edar`: this is a one-gene count prediction with no ranked supervision, and the manifest explicitly made the predictive rank-calibration and predictive graph-review capabilities unavailable for this task class.

## Computation over the inputs

I read the endpoint CSV and counted 1,674 visible training perturbations in this focal class. The endpoint is highly sparse: 1,205/1,674 training targets had `n_degs = 0`, the median was 0, the 75th percentile was 1, the 90th percentile was 2, and the mean was pulled upward to 14.1 by a small heavy tail.

I then queried the focal-cell Parquet rows for EDAR ligand and downstream NF-kappaB/TNF-receptor pathway analogs present in training. For each training perturbation I computed the number of focal rows with `pvals_adj < 0.05`, the minimum adjusted p-value, and the matched perturbed/control nucleus counts. The relevant zero-DEG neighborhood was:

| training perturbation | biological relationship to EDAR | observed `n_degs` | focal expression-pattern evidence |
| --- | --- | ---: | --- |
| `Eda` | cognate EDAR ligand EDA-A1 | 0 | 17,259 genes tested; no FDR-significant genes; minimum adjusted p-value 1.0; 221 matched perturbed nuclei |
| `Chuk` | IKK-alpha subunit downstream of TAK1/IKK signaling | 0 | no FDR-significant genes; minimum adjusted p-value 0.727; 156 matched perturbed nuclei |
| `Map3k7` | TAK1 kinase connecting TRAF6/TAB2 to IKK | 0 | no FDR-significant genes; minimum adjusted p-value 1.0; 160 matched perturbed nuclei |
| `Nfkb1` | canonical NF-kappaB transcription factor | 0 | no FDR-significant genes; minimum adjusted p-value 1.0; 181 matched perturbed nuclei |
| `Rel` | canonical NF-kappaB family transcription factor | 0 | no FDR-significant genes; minimum adjusted p-value 0.140; 205 matched perturbed nuclei |
| `Traf3` | TNF-receptor/NF-kappaB adaptor, strongest for noncanonical antagonism | 0 | no FDR-significant genes; minimum adjusted p-value 1.0; 211 matched perturbed nuclei |
| `Tnfrsf1a`, `Tnfrsf11a`, `Tnfrsf13c`, `Tnfrsf4`, `Tnfrsf9` | other TNF receptor family members; broader counterexamples rather than direct EDAR substitutes | 0 for each | no FDR-significant genes for any of these focal perturbations |
| `Xiap` | ubiquitin ligase that can participate in NF-kappaB signaling | 0 | no FDR-significant genes; minimum adjusted p-value 0.303; 124 matched perturbed nuclei |

The maximally informative comparison is `Eda`: if endogenous EDA-A1/EDAR signaling were driving a broad transcriptional program in these postnatal thalamic glutamatergic nuclei, loss of the ligand would be expected to phenocopy loss of the receptor in the same direction, with the usual caveat that mosaic ligand perturbation is cell-autonomous only for ligand-producing assayed neurons. The direct EDAR adaptor `Edaradd`, the TRAF6 adaptor, and `Tab2` were not present as focal training perturbations, so I treated `Chuk`, `Map3k7`, `Nfkb1`, and `Rel` as downstream counterexamples rather than exact receptor-complex phenocopies.

## Target-specific reasoning

### Edar

EDAR is the receptor for ectodysplasin-A1, signals through EDARADD to TRAF6/TAB2/TAK1 and the IKK/NF-kappaB module, and is best established as a developmental ectodermal appendage pathway for hair follicles, teeth, and exocrine glands rather than as a postnatal thalamic glutamatergic neuron regulator. That external prior already makes a broad 3-to-4-week neuronal snRNA-seq effect unlikely after acute AAV-CRISPR at P16.

The within-dataset analogs point in the same direction. The held-out `Edar` perturbation removes the receptor; the closest available perturbation, `Eda`, removes its canonical ligand and produced zero FDR-significant genes in this exact focal cell group, with every adjusted p-value equal to 1.0. Downstream NF-kappaB signaling components visible in the training set (`Map3k7`, `Chuk`, `Nfkb1`, `Rel`) were also transcriptionally silent by the endpoint, and broader TNF-receptor-family perturbations such as `Tnfrsf1a` and `Tnfrsf11a` did not create a focal-cell DEG burden. Those are imperfect analogs because core NF-kappaB factors are shared by many receptors and can have redundant or context-specific inputs, but if partial loss of EDAR were uniquely activating a large NF-kappaB-dependent state in `151 TH Prkcd Grin2c Glut`, at least one adjacent ligand or downstream perturbation would be a plausible nonzero neighbor.

The causal transfer model is: acute `Edar` CRISPR loss reduces EDAR receptor function; any direct consequence would require EDAR expression and local EDA-A1 stimulation in these recovered neurons; signal would then propagate through EDARADD/TRAF6/TAB2/TAK1/IKK to NF-kappaB transcription factors; the readout would need a stable nuclear RNA state at P37-P44 in surviving thalamic glutamatergic nuclei. The EDA ligand and generic NF-kappaB training knockouts test adjacent stages of that chain and show no focal-cell response. I therefore predict no genes will pass FDR 0.05.

Predicted `Edar` `n_degs`: **0**.

## Limits

This estimate is strongest for a zero/nonzero call and weak for a hypothetical small nonzero magnitude: the focal endpoint has many exact zeros and a point prediction of 0 only means no measured gene is expected to cross the assay's FDR 0.05 threshold. There is no exact `Edaradd` or `Traf6` training perturbation to test the receptor's immediate intracellular adaptor complex, and TNF/NF-kappaB components are not one-to-one substitutes for a ligand-specific receptor. Germline or epithelial phenotypes of EDA/EDAR are developmental and largely outside the assayed postnatal neuronal compartment, so the prediction deliberately downweights those organismal priors relative to the silent EDA/NF-kappaB signatures measured in the same Perturb-seq experiment.
