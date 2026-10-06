# Edar n_degs forecast

Target: `Edar`

Focal population: `151 TH Prkcd Grin2c Glut`

Prediction: `n_degs = 0`

## Evidence used

- The held-out manifest contains only `Edar`; `Edar` is absent from the 1,674-row `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` training count table.
- The endpoint is a zero-heavy count in this cell class: in the training count table, 1,205/1,674 targets have `n_degs = 0`, the median is 0, the 75th percentile is 1, and the 90th percentile is 2. The high-count tail exists but is restricted to a small set of core, broadly active processes rather than being a generic outcome of perturbing a biological target.
- The Edar biology bundle gives essentially no direct assayed-population reach in the requested thalamic class: `Edar` was detected in 19/23,679 non-target nuclei, only 22 total UMIs, `pct_cells_expressing = 0.08023987499472106`, and pseudobulk CPM 0.0582. The exact in-assay reach supersedes broader qualitative expression priors for this endpoint.
- The functional-stock card supports that P16 editing can deplete newly synthesized EDAR by the P37-P44 harvest because EDAR is a renewable cell-surface TNFR-family signaling receptor. That establishes possible target engagement in the rare cells that express Edar, not broad pathway dependence of the whole recovered thalamic class.
- The source and observability cards place established Edar loss biology in developmental ectodermal derivatives. They did not find a postnatal thalamic-neuron loss phenotype, EDAR-specific neuronal turnover, or evidence that related receptors compensate in this context. Adult mouse thalamus expression from HPA/Allen is near the detection floor, consistent with the exact reach.
- Bundle-related training perturbations on the EDA/TNFR/NF-kappaB axis are also null in the focal group: `Eda`, `Chuk`, `Nfkb1`, `Ngfr`, `Tnfrsf1a`, `Tnfrsf11a`, `Tnfrsf13c`, `Tnfrsf4`, `Tnfrsf9`, and `Traf3` each have zero genes with BH-adjusted Wilcoxon `p < 0.05` in the declared Parquet for `151 TH Prkcd Grin2c Glut`.

## Reasoning

The count-table prior already puts the modal forecast at zero. Edar is still lower-risk than a generic training target for this endpoint because the target transcript is detected in only 0.08% of non-target nuclei from the exact focal population, so any direct cell-autonomous EDAR loss should be diluted almost completely in an aggregate recovered-nucleus differential-expression contrast. The biology bundle makes receptor turnover plausible over the 21-28 day edit window, but its positive evidence is about molecular realizability in successfully edited Edar-expressing cells; it does not provide matched postnatal thalamic demand or a broad pathway entry route. Null training outcomes for EDA/TNFR/NF-kappaB-axis perturbations in the same class reinforce that this receptor branch is unlikely to sit on the rare high-DEG tail here.

Balancing the zero-heavy empirical endpoint, the near-absent exact target expression, and the lack of matched neural phenotype support, the most likely integer DEG count is therefore 0.
