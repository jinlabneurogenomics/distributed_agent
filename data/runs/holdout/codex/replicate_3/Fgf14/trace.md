# Fgf14 n_degs forecast

Target: `Fgf14`
Cell class: `151 TH Prkcd Grin2c Glut`
Forecasted `n_degs`: **1**

## Evidence used

- The declared holdout manifest contains one target, `Fgf14`; `Fgf14` is absent from both the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` and the declared `training_de_all_cell_groups.parquet` as a `gene_target`.
- The canonical biology-only bundle for `Fgf14` reports exact focal-population target reach in the matched non-target nuclei: the `Fgf14` measured feature is available in `151 TH Prkcd Grin2c Glut`, with 18,223 / 23,679 non-target nuclei expressing it, `pct_cells_expressing = 76.95848642256853`, `mean_log1p_cp10k = 0.6418727647047848`, and `mean_cp10k = 1.0979808321435434`.
- The same bundle characterizes FGF14 as an intracellular FHF that associates with voltage-gated sodium-channel alpha subunits and modulates channel availability/excitability. Its functional-stock adjudication calls the operative pool a dynamic complex component and concludes that functional stock is likely substantially depleted by the P37-P44 harvest after P16 editing, with partial evidence because the exact FGF14 half-life and persistence of specialized axonal/channel-bound pools are unknown.
- The closest measured FHF/Nav training perturbations in the `151 TH Prkcd Grin2c Glut` count table were sparse:

  | target | n_degs |
  |---|---:|
  | Fgf12 | 0 |
  | Fgf13 | 2 |
  | Scn1a | 1 |
  | Scn1b | 2 |
  | Scn2a | 1 |
  | Scn3a | 0 |
  | Scn8a | 1 |

  This cohort has mean `n_degs = 1.0` and median `n_degs = 1`.
- A broader channel/neural excitability set in the same table, adding `Ank2`, `Cacna1a`, and represented `Kcn*` targets, was even quieter: 29 targets had mean `n_degs = 0.45` and median `n_degs = 0`.
- Direct Parquet inspection in the focal cell class confirmed that the tiny counts above are not hiding broad downstream programs. `Fgf13` had two significant rows, the self transcript `Fgf13` and `Rell2`; `Scn1a`, `Scn2a`, and `Scn8a` were self-only; `Scn1b` was self plus `Jun`; `Fgf12`, `Scn3a`, `Cacna1a`, and `Ank2` had no BH < 0.05 rows.
- Same-experiment corpus context for the training FHFs reports that `Fgf12` and `Fgf13` perturbations were sparse and did not form a shared pan-Nav or Nav-complex RNA module with represented sodium-channel perturbations. This was used only to interpret measured training perturbations, not as independent replication.
- `Atp1a3` is an ion-homeostasis positive boundary in the same cell class, with `n_degs = 80` at BH < 0.05, but it is a Na/K pump alpha subunit with a distinct calcium-handling and membrane-homeostasis response in the corpus rather than a close FHF/Nav regulator analogue.

## Synthesis

The exact `Fgf14` reach argues against treating the perturbation as unobservable in this thalamic class, and expected depletion of a renewable intracellular channel regulator makes at least the self transcript or a very local downstream change plausible. The direct measured analogues nevertheless put the expected RNA burden near the floor: other represented FHFs and Nav-subunit targets overwhelmingly produced zero to two DEGs, often only their own target transcript, and packaged FHF/Nav contrasts specifically reject a transferable shared Nav-complex transcriptomic state. I therefore centered the forecast on the close-analogue median of one significant gene and did not borrow the much larger `Atp1a3` response.

Point prediction: **1**
