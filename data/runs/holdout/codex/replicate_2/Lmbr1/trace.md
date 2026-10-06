# Lmbr1 151-class DEG-count forecast

## Target and endpoint

- Target: `Lmbr1`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Prediction: `0`

## Evidence used

### Biology-only Lmbr1 bundle

The declared `Lmbr1` biology bundle exposed exact target reach in `151 TH Prkcd Grin2c Glut` but no target outcome or labeled-neighbor outcomes.

- `Lmbr1` was measurable in the focal population: 8,203 of 23,679 non-target cells expressed it, `pct_cells_expressing = 34.6425`, `mean_cp10k = 0.27536`, and `pseudobulk_cpm = 28.7628`.
- The functional-stock adjudication was `indeterminate`. The disruptive edit should stop new LMBR1 synthesis, but the operative membrane-protein function, persistence, exchange rate, and renewal demand in P16-to-P37/P44 postmitotic thalamic neurons were not established.
- The strongest direct functional literature in the bundle concerned the Lmbr1/Shh/ZRS locus in embryonic limb development, not coding LMBR1 function in juvenile or adult neurons.
- The residual observability fields were unresolved rather than response-supporting: the best context was mouse non-neural/systemic, the phenotype evidence was non-neural or systemic only, developmental timing was not transferable to P16 neurons, postnatal relevance was developmental-evidence only, and possible redundancy through `Lmbr1l` was untested.

These facts argue against assigning Lmbr1 to a high-response class on biology alone. They do not prove a null: the transcript is present in about one third of the focal cells, and an unknown membrane-protein function could matter in that subset.

### Same-experiment corpus context

The selected July 260713 sourceguard corpus had no target-scoped `Lmbr1` Findings, Claims, or explicit comparator references. This was treated as a coverage fact, not as a negative measurement.

The one concrete route in the Lmbr1 card was its developmental Shh/ZRS association. In the same corpus, represented Hedgehog/PTCH-SMO-cilium-GLI perturbations were summarized in `claim:cdb20b21467eeac1c3c5`: acute single-node perturbations of Hedgehog receptors, SMO, GLI factors, Gpr161, ciliary transduction components, and co-receptors did not detectably recover a coordinated GLI/PTCH/HHIP transcriptional circuit in postnatal NeuN-positive nuclei. Material target-scoped Finding IDs supporting that boundary included `Gli2:F002`, `Ptch1:F002`, `Smo:F002`, and `Smo:F003`.

This corpus evidence was same-experiment interpretation, not independent replication. It was used only to decide that embryonic Shh-locus biology should not move the forecast upward in this postnatal 151-class endpoint.

### Declared training count table

The focal-class training table contained 1,674 visible perturbations and was heavily concentrated at zero:

- 1,205 / 1,674 training perturbations had `n_degs = 0`.
- 1,571 / 1,674 had `n_degs <= 10`.
- The 75th percentile was `1`, the 90th percentile was `2`, and the median was `0`.
- Only 43 / 1,674 had `n_degs >= 100`.

The `Lmbr1` target itself, `Lmbr1l`, and `Shh` were absent from the declared training count table. The available Hedgehog/ciliary-axis comparators in the same 151 class were locally quiet:

| training target | `n_degs` |
|---|---:|
| `Gli1` | 0 |
| `Gli2` | 0 |
| `Ptch1` | 0 |
| `Smo` | 0 |
| `Ptch2` | 0 |
| `Cdon` | 0 |
| `Dync2h1` | 0 |
| `Gpr161` | 0 |
| `Ift88` | 0 |
| `Kif3b` | 0 |
| `Adcy3` | 0 |
| `Lrp2` | 0 |
| `Mycn` | 0 |
| `Gnas` | 0 |
| `Prkaca` | 1 |

### Declared expression Parquet

The declared `training_de_all_cell_groups.parquet` was inspected only for the matched 151-class rows for the proximal Hedgehog perturbations `Gli1`, `Gli2`, `Ptch1`, and `Smo`. Each had 17,259 measured-gene rows in this cell class; each had:

- `0` genes with `pvals_adj < 0.05`;
- `0` genes with `pvals_adj < 0.10`;
- minimum `pvals_adj = 1.0`.

For the canonical Hedgehog readout genes `Gli1`, `Gli2`, `Gli3`, `Ptch1`, `Ptch2`, `Hhip`, `Smo`, and `Shh`, every inspected row under each of `Gli1`, `Gli2`, `Ptch1`, and `Smo` in `151 TH Prkcd Grin2c Glut` had `pvals_adj = 1.0`.

## Synthesis

The exact Lmbr1 expression reach shows the perturbation was not completely invisible in `151 TH Prkcd Grin2c Glut`, so the forecast was not reduced to zero solely because the target was unexpressed. The decisive considerations were instead:

- the bundle did not establish LMBR1 protein depletion, protein function, or a postnatal thalamic neuronal loss program by the P37-P44 harvest;
- the Shh/ZRS limb-development evidence follows a cis-regulatory embryonic axis that is mismatched to a coding LMBR1 lesion in postmitotic neurons;
- the closest represented Shh/Hedgehog/ciliary transcriptional comparators in the declared training measurements were at the zero or one-DEG floor in this exact class; and
- the focal count distribution has a zero median and a very low upper quartile.

The best point forecast is therefore the local floor:

`predicted_n_degs = 0`.
