## Prediction

Target: `Klrk1`

Predicted `n_degs` in `151 TH Prkcd Grin2c Glut`: **0**

## Evidence used

### Declared target biology

The declared holdout manifest contains the single target `Klrk1`.
The endpoint is the number of measured genes with BH-adjusted Wilcoxon
`pvals_adj < 0.05` in the focal thalamic glutamatergic class
`151 TH Prkcd Grin2c Glut`.

The canonical biology bundle for `Klrk1` supports a real molecular edit but a
poor target-context prior:

- `Klrk1` encodes NKG2D, a cell-surface activating receptor whose established
  biology is in NK cells and activated cytotoxic lymphocytes.
- NKG2D signals through DAP10/DAP12 adaptor complexes and pre-edit receptor
  stock should mostly clear within the 21-28 day experiment window, so a
  successful edit should be functionally realized wherever the receptor is
  being renewed.
- The established mouse phenotypes are immune, tumor-surveillance, infection,
  or immune-mediated neuroinflammatory phenotypes, not healthy
  thalamic-neuron-autonomous phenotypes.

The exact in-assay expression reach in the focal non-target population is
nearly absent:

- total `Klrk1` UMI in the 23,679 focal non-target nuclei: `6`
- expressing nuclei: `6 / 23679 = 0.0253389%`
- mean raw UMI: `0.000253389`
- pseudobulk CPM: `0.0158808`
- mean log1p CP10K: `0.000125608`

Thus the perturbation should disable a dynamic receptor complex if it is
present, but there is little evidence that the receptor is materially present
or demanded in the recovered thalamic neuronal population.

### Training count table

The focal training table has 1,674 measured training perturbations.
Its count distribution is sparse:

- `1205 / 1674 = 71.98%` have `n_degs = 0`
- `276 / 1674 = 16.49%` have `n_degs = 1`
- median `n_degs = 0`
- 75th percentile `= 1`
- 90th percentile `= 2`
- 95th percentile `= 18`

I treated the global skew as a baseline only, then checked perturbations whose
biology is closer to `Klrk1`: immune-lineage receptors, antigen receptor
subunits, cytokine receptors, and TLRs that are in the declared training table.
Direct receptor/adaptor comparators in the same focal endpoint were all zero:

`Ccr2`, `Cd14`, `Cd27`, `Cd3d`, `Cd3e`, `Cd3g`, `Cd4`, `Cd40`, `Cd79a`,
`Cd79b`, `Csf1r`, `Csf3r`, `Fcgr4`, `Ifnar1`, `Ifnar2`, `Ifngr1`, `Ifngr2`,
`Il10ra`, `Il12b`, `Il12rb1`, `Il17ra`, `Il17rd`, `Il1r1`, `Il1rap`,
`Il1rapl1`, `Il1rapl2`, `Il21r`, `Il23r`, `Il2ra`, `Il2rb`, `Il2rg`,
`Il31ra`, `Il4ra`, `Il6ra`, `Il6st`, `Tlr2`, `Tlr3`, `Tlr4`, `Tlr5`, `Tlr7`,
and `Tlr8` each had `n_degs = 0`.

The broader immune signaling controls were also quiet in this class:
`Stat2`, `Stat3`, and `Stat4` had `0`; `Stat1` had only `1`.

### Parquet check

I re-read the declared differential-expression Parquet for the same focal
cell class and comparator genes. Each selected comparator had 17,259 tested
features in `151 TH Prkcd Grin2c Glut`; the Parquet rows reproduced zero
BH-significant genes for all listed immune receptor/adaptor comparators and a
single significant feature for `Stat1`.

## Synthesis

The exact target expression measurement is the decisive evidence. `Klrk1`
is not just low in the focal non-target nuclei; it is represented by only six
UMIs across the whole thalamic population used for the contrast. The stock
adjudication argues that the CRISPR lesion is not masked by a long-lived
protein reservoir, but it cannot create a transcriptional response in cells
that do not renew or use the receptor.

The declared training endpoint strongly supports the same placement. Most
perturbations are silent in this class, and the training targets that best
match `Klrk1` as immune-cell receptors or immune stimulus receptors are
consistently at `n_degs = 0`, despite being assayed over the same 17,259
features and the same focal cell class.

Rare real expression or a guide-intrinsic effect could in principle produce
one significant feature, but the focal reach and comparator measurements both
put the most likely count at the zero floor. I therefore used:

```text
predicted_n_degs = 0
```
