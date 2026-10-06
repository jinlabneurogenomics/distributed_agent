# Ahdc1 direct DEG-count forecast

Target and endpoint:

- `gene_target`: `Ahdc1`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`

## Evidence used

The declared holdout manifest contains only `Ahdc1`, and `Ahdc1` is absent from
the visible 1,674-row training count table. The training distribution for this
cell group is sparse: 1,205 / 1,674 visible perturbations have `n_degs = 0`, the
median is 0, the 75th percentile is 1, and the 95th percentile is 18. Thus the
baseline expectation for any non-core target is 0-1 DEGs, with a long right tail
reserved for a small minority of broad responders.

The canonical Ahdc1 biology bundle supplies a mixed perturbability prior:
Ahdc1 is expressed in the exact assayed population, with 15,863 of 23,679
non-target nuclei expressing it, `pct_cells_expressing = 66.991849`, mean
CP10K `0.805955`, and pseudobulk CPM `79.814214`. That expression reach argues
against an expression-limited zero. Mechanistically, AHDC1/Gibbin is a
chromatin-associated enhancer/promoter regulator and no close mouse paralog or
tested same-context compensator was found, which also nudges the prediction
above a completely silent target.

The same biology bundle also limits the expected magnitude. Direct mechanistic
evidence is from differentiating human stem-cell and epithelial/mesodermal
contexts, not postmitotic mouse thalamic neurons; mouse and human loss
phenotypes are developmental or systemic and do not time a P16 neuronal edit;
and the functional-stock adjudication calls AHDC1 loss by P37-P44
`partially_depleted_or_leading_edge`, because new protein supply should stop
but pre-existing chromatin-bound protein and maintained chromatin states may
persist.

I compared visible chromatin and transcriptional controls in the matched
Parquet context rather than borrowing a broad chromatin count wholesale. Core
maintenance regulators can be very large in this cell group: `Yy1 = 720`,
`Phf12 = 403`, `Wac = 384`, `Setd1a = 368`, `Brd4 = 311`, `Ctcf = 270`,
`Smarcc2 = 185`, and `Chd4 = 100`. However, closer "developmental regulator
not constitutively required here" controls are often silent or tiny:
`Gata3 = 0`, `Satb2 = 0`, `Smarca4 = 0`, `Stag1 = 0`, `Auts2 = 1`,
`Ash1l = 1`, `Mbd5 = 0`, `Pogz = 0`, `Tcf4 = 0`, `Dnmt3a = 0`, and
`Kat6a = 0`. Same-experiment corpus reports for visible controls reinforce the
boundary: `Gata3` was almost completely buffered and represented GATA-family
targets did not form a shared postmitotic neuronal module, while `Smarca4` was
flat even though other BAF/PBAF accessory subunits responded.

The matched Parquet profile comparison of selected chromatin controls also
showed that this comparator set was not one transferable module. Across 136
selected pairs, mean top-tail overlap was only 0.071 for the positive tail and
0.133 for the negative tail, so the high-count `Yy1`/`Brd4`/`Ctcf`/`Setd1a`
nodes are evidence that the assay can observe some architectural regulators,
not quantitative analogs for Ahdc1.

## Synthesis

The point estimate is a very small but nonzero footprint. Ahdc1 has enough
thalamic expression and nuclear regulatory biology to sit slightly above a
generic training-table zero, but its available loss evidence is mostly
developmental, its functional stock is only partially resolved in a 21-28 day
postnatal edit, and visible postmitotic developmental TF/chromatin perturbations
often collapse to singleton or zero responses. I therefore placed Ahdc1 at the
training table's upper quartile rather than in the broad chromatin tail.

Predicted `n_degs`: 1
