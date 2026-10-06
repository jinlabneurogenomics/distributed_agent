# Prokr2 direct n_degs forecast

## Target and endpoint

- **Target:** `Prokr2`
- **Cell class:** `151 TH Prkcd Grin2c Glut`
- **Endpoint:** count of measured genes with BH-adjusted Wilcoxon `p < 0.05`

The declared training count table contains 1,674 non-held-out perturbations for this cell class and does not contain `Prokr2`.

## Evidence used

### Canonical Prokr2 biology bundle

- `Prokr2` encodes a ligand-responsive seven-transmembrane prokineticin GPCR.
- The functional-stock card calls substantial depletion by the P37-P44 harvest likely after a disruptive P16 edit, because the receptor is a trafficked membrane protein with ongoing biosynthetic supply and degradation rather than a permanently installed neuronal structure.
- The focal-class expression measurement is extremely sparse: among 23,679 matched non-target nuclei in `151 TH Prkcd Grin2c Glut`, only 188 expressed `Prokr2`, or 0.794%; mean raw expression was 0.0092 UMI per nucleus, with pseudobulk 0.577 CPM.
- Adult expression evidence supports selected thalamic nuclei rather than uniform thalamic expression, so the atlas class likely aggregates many cells outside the directly Prokr2-responsive pool.

I treated the expression measurement as a reach constraint, not as editing efficiency. Even if edited Prokr2+ cells lose receptor function over 21-28 days, the affected cells should be a very small fraction of the recovered focal population, and the transcript itself is too rare to provide a robust self-DE row.

### Focal-class training counts

From `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`:

- 1,205 / 1,674 perturbations had `n_degs = 0`.
- 469 / 1,674 had any DEG.
- The median and 90th percentile were 0 and 2, respectively.
- Only 106 perturbations had at least 10 DEGs, and only 43 had at least 100.
- The high tail was headed by broadly disruptive nuclear or proteostasis targets such as `Uba5` at 2,677, `Tpr` at 1,768, `Sin3a` at 1,433, `Rnpc3` at 868, `Zbtb7a` at 841, and `Psmb4` at 742.

This puts an ordinary, sparse receptor perturbation much closer to the point mass at zero than to the heavy response tail.

### Receptor perturbations measured in the same Parquet

I selected 44 receptor or receptor-like GPCR perturbations from the training table:
`Avpr1a`, `Avpr1b`, `Cnr1`, `Crhr1`, `Drd2`, `Drd4`, `Drd5`, `Gabbr1`, `Gabbr2`, `Galr1`, `Gpr156`, `Gpr158`, `Gpr161`, `Gpr179`, `Gpr45`, `Gprc5b`, `Grm1`, `Grm5`, `Grm6`, `Grm7`, `Grm8`, `Htr1a`, `Htr1b`, `Htr1f`, `Htr2a`, `Htr2b`, `Htr2c`, `Htr4`, `Htr6`, `Htr7`, `Mc1r`, `Mc2r`, `Npy1r`, `Npy2r`, `Npy5r`, `Ntsr1`, `Oprd1`, `Oprk1`, `Oprm1`, `Oxtr`, `P2ry12`, `P2ry14`, `Sstr5`, and `Tacr3`.

Their same-cell-class DEG burden was:

- 38 / 44 with `n_degs = 0`
- 6 / 44 with `n_degs = 1`
- mean `n_degs = 0.136`
- maximum `n_degs = 1`

A Parquet profile comparison of the same 44 perturbations in `151 TH Prkcd Grin2c Glut` confirmed 38 profiles with no significant feature and 6 profiles with 1-9 significant features. Querying the significant rows showed that five of the six singleton responses were the edited transcript itself:

| perturbation | significant gene | note |
| --- | --- | --- |
| `Cnr1` | `Srcap` | only non-self receptor-cohort singleton |
| `Gabbr1` | `Gabbr1` | self transcript |
| `Gabbr2` | `Gabbr2` | self transcript |
| `Gpr158` | `Gpr158` | self transcript |
| `Grm1` | `Grm1` | self transcript |
| `Grm7` | `Grm7` | self transcript |

Because `Prokr2` has only 0.794% baseline detection in the focal non-target cells, I did not expect even a self-transcript singleton to survive FDR.

## Synthesis

The biology bundle supports real functional target engagement on a multiweek window, but only for a very sparse Prokr2-expressing subset inside an aggregated thalamic glutamatergic population. Prokr2 is also a ligand-dependent GPCR rather than a broad cell-autonomous chromatin, RNA-processing, ribosomal, or proteostasis factor, and same-assay receptor perturbations in this population were almost always null after BH correction. The rare nonzero receptor counts were mostly self-DE rows, which are less likely for Prokr2 because its focal expression is far below 1% of non-target cells.

I therefore predict that the held-out `Prokr2` perturbation produced no FDR-significant measured genes in `151 TH Prkcd Grin2c Glut`.

**Predicted `n_degs`: 0**
