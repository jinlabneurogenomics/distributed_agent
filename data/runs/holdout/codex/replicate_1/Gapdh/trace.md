# Gapdh forecast for 151 TH Prkcd Grin2c Glut

## Target and endpoint

- Held-out target: `Gapdh`.
- Focal population: `151 TH Prkcd Grin2c Glut`, the thalamic glutamatergic class requested by the task.
- Endpoint: `n_degs`, the number of measured genes in this population with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

## Evidence used

- The declared one-row manifest and the run-local task bindings identify `Gapdh` as the only target to predict.
- The `Gapdh` biology bundle is outcome-blind. It supports likely depletion of functional soluble Gapdh protein by harvest because a P16 disruptive edit should stop new catalytic Gapdh production, the assayed P37-P44 interval spans multiple typical mouse-brain protein lifetimes, and the close `Gapdhs` glycolytic isozyme is germ-cell restricted rather than a neural replacement. It also leaves several endpoint-critical quantities unresolved: no direct juvenile thalamic Gapdh protein time course, no acute postnatal neuronal loss experiment, unknown survivor conditioning, and unknown affected fraction after sparse editing.
- The exact focal-population expression reach in that bundle has `feature_available=false` and `feature_status=excluded_as_unused_gene` for `Gapdh`, so this target has no measured self-transcript row that could contribute a one-gene DE call.
- The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 training perturbations and no `Gapdh` row. Its focal-population outcome distribution is sparse: 1,205/1,674 targets have `n_degs = 0`; the median is 0; the 75th percentile is 1; and only 106/1,674 have at least 10 DEGs.
- I inspected direct training analogues for central glycolysis and adjacent energy metabolism in the same count table. `Hk1`, `Gpi1`, `Tpi1`, `Pdha1`, `Dlat`, `Mdh2`, `Idh3a`, and `Sdha` each have one DEG; `Eno1`, `Aco2`, `Dld`, `Ndufv1`, `Cox4i1`, and `Slc2a1` have zero.
- I then checked the declared training Parquet for a 30-target core metabolic cohort in `151 TH Prkcd Grin2c Glut`. Among the 17 targets in that cohort with exactly one significant feature, 16 were self-transcript calls: `Cox5a`, `Dlat`, `Gpi1`, `Hk1`, `Idh3a`, `Mdh2`, `Ndufa10`, `Ndufa4`, `Ndufa6`, `Ndufb8`, `Ndufc2`, `Ndufs2`, `Ndufs8`, `Pdha1`, `Sdha`, and `Tpi1`. The only non-self singleton was `Ndufv2`, whose one significant measured gene was `Cdc40`.

## Synthesis

`Gapdh` is a real, continuously used glycolytic enzyme rather than a dead target, so I did not treat the perturbation as an impossible edit or a neutral safe-target-like operation. However, under this assay the best same-context evidence argues for almost no detected downstream RNA footprint after perturbing single core energy-metabolism enzymes in recovered thalamic neurons. The closest glycolytic singletons, `Hk1`, `Gpi1`, and `Tpi1`, were counted solely because their own transcripts decreased, and the target self-feature route is absent for `Gapdh`.

That makes the generic 0/1 prior from the training distribution more informative than the long right tail from spliceosome, proteasome, chromatin, or ER-stress regulators. `Gapdh` could still have an unmeasured metabolic or survival effect, but the requested endpoint is FDR-significant nuclear DE among recovered nuclei, and the self-feature exclusion removes the most common one-gene signal seen in its closest measured analogues.

Predicted `n_degs`: **0**.
