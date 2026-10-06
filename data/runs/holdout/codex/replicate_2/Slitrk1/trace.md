# Slitrk1 direct DEG-count forecast

## Target and endpoint

- **Target:** `Slitrk1`
- **Population:** `151 TH Prkcd Grin2c Glut`
- **Endpoint:** `n_degs`, the count of measured genes with Wilcoxon `pvals_adj < 0.05`

## Evidence used

### Target biology

Source: declared `Slitrk1` biology bundle served in canonical `biology` view.

- `Slitrk1` is detectable in the focal class: 20,550 of 23,679 non-target nuclei express the gene, for **86.8%** expressing nuclei; mean expression is **3.11 raw UMI** and **0.944 mean log1p CP10K**.
- The source card supports SLITRK1 as a **postsynaptic, single-pass synaptic adhesion protein** that interacts with presynaptic LAR-family receptor phosphatases.
- Functional-stock adjudication concluded that existing SLITRK1 should be **likely substantially depleted** by the P37-P44 harvest window after a disruptive P16 edit, with adult neuronal conditional deletion giving the closest two-to-three-week timing evidence.
- The selected same-experiment corpus release had no `Slitrk1` Finding or Claim, so the forecast did not use a packaged Slitrk1 report.

Interpretation: the target is expressed and the perturbation should become functional in edited expressing neurons, so this is not demoted to an expression-missing or stock-persistent null. Its best-supported molecular role is local synaptic adhesion rather than core transcription, RNA processing, proteostasis, or excitability control expected to yield a broad nuclear RNA program.

### Training count distribution

Source: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.

- 1,674 labeled training perturbations were present for this population.
- Distribution of `n_degs`: median **0**, 75th percentile **1**, 90th percentile **2**, 95th percentile **18**, 99th percentile **436**, maximum **2677**.
- **1,205 / 1,674** training perturbations had `n_degs = 0`; **1,571 / 1,674** had `n_degs <= 10`.

Interpretation: very large signatures occur in this thalamic class, but they are a sparse right tail. A high count needs a close reason to map Slitrk1 onto that tail.

### Mechanistic training perturbations

Source: the count table above, checked against `[local file: training_de_all_cell_groups.parquet]` with `group_name = '151 TH Prkcd Grin2c Glut'`.

Closest labeled synaptic-adhesion / synapse-organization examples:

| training perturbation | focal `n_degs` |
| --- | ---: |
| `Ptprd` | 0 |
| `Ptprf` | 0 |
| `Nrxn1` | 1 |
| `Nrxn2` | 0 |
| `Nrxn3` | 0 |
| `Nlgn3` | 1 |
| `Lrrtm1` | 1 |
| `Lrrtm3` | 0 |
| `Lrrtm4` | 0 |
| `Shank2` | 0 |
| `Shank3` | 2 |
| `Dlg4` | 1 |
| `Dlgap4` | 2 |
| `Grid2` | 0 |

For `Nrxn1`, `Nlgn3`, and `Dlg4`, the single FDR-significant gene in the focal class was the self transcript; there was no broad downstream transcriptional module at `q < 0.05`, and each had exactly one gene even at `q < 0.10`. Direct NMDA receptor perturbation can be larger in the same class, for example `Grin1` had 89 DEGs, but the receptor-subunit mechanism is not as close to SLITRK1 as the adhesion/scaffold examples.

## Forecast synthesis

The count should stay near the quiet synaptic-adhesion group, because Slitrk1 loss is expected to perturb existing synapses locally rather than impose a cell-wide transcriptional stress state. Exact focal expression and likely stock depletion make a pure no-engagement zero less compelling, and the nearest expressed adhesion genes often produce either only the self transcript or one isolated secondary gene. I therefore forecast **one** significant measured gene rather than a broad response.

`predicted_n_degs = 1`
