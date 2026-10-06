# Hes7 n_degs direct forecast

## Declared target and endpoint

- Manifest target: `Hes7`, from the one-row declared manifest
  `[local file: Hes7.csv]`.
- Requested endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- Training count surface:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Training expression surface:
  `[local file: training_de_all_cell_groups.parquet]`.
- The holdout was intact for the forecast: `Hes7` was absent from the 1,674-row focal DEG-count table, and `gene_target = 'Hes7'` had zero rows in the training Parquet.

## Target biology used

The canonical `Hes7` biology bundle
`[local file: Hes7.json]`
was served as the `biology` view, with `target_outcome_exposed = false` and
`labeled_neighbors_exposed = false`.

HES7 is a short-lived bHLH transcriptional repressor in the mouse embryonic
presomitic-mesoderm segmentation clock. The card argues that a successful
disruptive edit should eliminate active pre-edit HES7 protein well before the
P37-P44 harvest because wild-type mouse HES7 turned over with an approximately
22-minute half-life in the tested segmentation system.

That stock-realization prior did not translate into a high class-151
transcriptional-response prior. The same bundle localized the established
operation and null phenotype to embryonic somitogenesis, found no postnatal
mouse neural loss test, and reported only very low adult mouse thalamic RNA
signal from atlas data. The exact in-assay focal reach was also extremely
small: in matched non-target `151 TH Prkcd Grin2c Glut` nuclei, `Hes7` had
106 total UMIs among 23,679 nuclei, with 102 nuclei expressing it, `0.4308%`
of the population, mean raw UMI `0.00448`, and pseudobulk CPM `0.2806`.

## Training perturbations used

The focal training counts were zero-heavy: among 1,674 visible perturbations,
1,205 had `n_degs = 0`, 1,481 had `n_degs <= 1`, and 1,512 had `n_degs <= 2`.
The median was `0`; the upper tail was small but large, with 106 perturbations
at `>= 10` DEGs and 19 perturbations at `>= 400` DEGs. The high tail was led by
broad RNA/protein homeostasis or transcriptional regulators such as `Uba5`,
`Tpr`, `Sin3a`, `Rnpc3`, `Zbtb7a`, `U2af2`, `Psmb4`, `Hnrnpu`, `Yy1`, and
`Elp1`, not by the embryonic segmentation-axis genes most relevant to `Hes7`.

Within the training table and exact focal Parquet rows, the closest visible
developmental and Notch/segmentation-axis checks were flat or nearly flat:

| gene_target | focal n_degs |
| --- | ---: |
| `Dll1` | 0 |
| `Notch1` | 0 |
| `Notch2` | 0 |
| `Notch4` | 0 |
| `Tbx6` | 0 |
| `Tbx1` | 0 |
| `Hesx1` | 0 |
| `Mesp2` | 1 |
| `Neurod1` | 0 |
| `Neurod2` | 0 |
| `Neurog3` | 0 |
| `Tcf3` | 0 |
| `Sox2` | 2 |

For this set, the Parquet confirmed that those aggregate counts were isolated
class-151 findings rather than large hidden signatures: every listed target
except `Mesp2` and `Sox2` had zero measured genes with adjusted `p < 0.05`;
`Mesp2` had only `Arih2` at adjusted `p = 0.0449566`.

## Forecast

I predict `Hes7` will have `0` BH-significant genes in
`151 TH Prkcd Grin2c Glut`.

The edit is physically capable of depleting HES7 in cells that truly produce
the protein, so this is not an editing-window null. The decisive bearings are
instead context and reach: the documented HES7 circuit is embryonic and
non-neural, exact baseline reach in the focal recovered neurons is below one
half-percent of matched non-target nuclei, and visible training perturbations
from the same developmental/Notch neighborhood were at the floor of the focal
DEG-count distribution. A one-gene response like `Mesp2` or `Sox2` remains
possible, but the integer point estimate is the distributional mode and the
matched biological-neighborhood count: `0`.
