# Direct DEG-count forecast for `Arsb`

Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, counted as measured genes with
BH-adjusted Wilcoxon `pvals_adj < 0.05`.

Prediction: `0`.

## Evidence that set the scale

- The one-row holdout manifest and the canonical biology bundle both identify
  the target as `Arsb`.
- The target bundle maps the assayed `Arsb` symbol to mouse Slurp1 / ArsB, a
  small secreted Ly6/uPAR-family extracellular protein. Its physiological
  receptor-level operation in P16-P44 thalamic neurons is not established.
- Exact focal-population expression shows that the `Arsb` measured feature is
  present but weak in this class: 9,021 of 23,679 non-target cells express it
  in `151 TH Prkcd Grin2c Glut` (`38.10%`), with mean raw UMI `0.541`,
  pseudobulk CPM `33.93`, and mean log1p-CP10K `0.227`.
- The functional-stock card concluded that a disruptive edit should stop new
  Slurp1 production in edited expressing cells, but would not directly
  neutralize already secreted extracellular Slurp1. No quantitative Slurp1
  clearance or residence time was found for mouse brain, thalamus, keratinocyte
  medium, blood, or another transferable compartment, so stock depletion by the
  P37-P44 harvest remains indeterminate.
- Prior causal evidence is mismatched to this endpoint: constitutive Slurp1
  loss causes postnatal skin/systemic phenotypes and hind-limb clasping in
  mice, but the phenotype was not localized to a central neuronal mechanism,
  and public adult mouse thalamus data reported no regional Slurp1 signal.
- The declared `151 TH Prkcd Grin2c Glut` training table contains 1,674
  measured targets. It is very sparse: 1,205 targets (`71.98%`) have
  `n_degs = 0`; the median is 0, the 75th percentile is 1, the 90th percentile
  is 2, and only the 95th percentile reaches 18.
- I used the expression Parquet in the exact cell class to inspect low-footprint
  secreted/receptor-modulatory comparators available in the training table.
  `Nrg1` had 0 DEGs, `Slit2` had 0, `Nrg3` had 1, `Ache` had 1, `Cck` had 1,
  `Chrnb2` had 1, `Grin2a` had 1, `Chrna4` had 2, and `Grin2b` had 2. In most
  one-DEG cases the only significant feature was the perturbed transcript
  itself.

## Synthesis

`Arsb` has measurable RNA in the focal thalamic glutamatergic class, so a
self-transcript hit or a very small local response is possible. I did not treat
self-RNA loss as editing efficiency or downstream-effect strength.

The biology points downward from that weak expression prior: Slurp1 is a
diffusible secreted product rather than a cell-intrinsic neuronal regulator;
the local receptor process is unresolved; mosaic loss in only edited cells can
be buffered by pre-edit extracellular protein or unedited neighboring sources;
and the matched postnatal thalamic cell-autonomous loss phenotype is missing.
Within this high-yield class, training perturbations with more obvious
neuronal receptor or ligand connections commonly landed at 0-1 significant
genes, often just the targeted transcript. I therefore place `Arsb` below that
one-gene boundary and use an integer point forecast of zero.
