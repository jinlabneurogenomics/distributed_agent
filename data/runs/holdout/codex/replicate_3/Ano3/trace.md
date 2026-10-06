# Ano3 direct DEG-count forecast

## Target and endpoint

- Target from the one-row holdout manifest: `Ano3`.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, counting measured genes with Wilcoxon BH-adjusted `p < 0.05`.
- Declared measured table: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, containing 1,674 training targets and excluding `Ano3`.
- Declared profile table: `training_de_all_cell_groups.parquet`; a direct filter for `gene_target == "Ano3"` returned zero rows, so no target profile was used.

## Biology that constrained the forecast

The canonical Ano3 biology bundle reports exact in-assay focal reach but no target outcome. `Ano3` is detected in the focal non-target thalamic neurons, yet sparsely: 2,987 of 23,679 nuclei express it, with mean raw UMI 0.1846 and mean log1p CP10K 0.0721. The source card supports ANO3/TMEM16C as an intracellular calcium-dependent phospholipid scramblase and a KCNT1/Slack-associated regulator of excitability, but the matched neural evidence is rat DRG rather than mouse thalamus. The functional-stock card is indeterminate by the 21-28 day harvest window because a disruptive P16 edit stops new ANO3 supply while pre-existing membrane protein and lipid/channel-associated state persistence are not measured.

Those facts make a focal transcriptional effect biologically possible, but favor a small burden: only a minority of recovered focal neurons have detectable Ano3 RNA, the best functional model is not thalamic, and no fast post-edit ANO3 protein-clearance clock is established.

## Training measurements used

The focal count table is concentrated at the floor:

- median = 0 DEGs;
- 75th percentile = 1 DEG;
- 1,205 / 1,674 training perturbations are zero;
- 1,546 / 1,674 are at most 5 DEGs;
- only 43 / 1,674 reach at least 100 DEGs.

Curated mouse annotation nomination found no training-available exact paralog, same-complex member, direct dependency, or narrow-module analogue for `Ano3`; all 745 nominated training-available genes were broad functional fallbacks. I therefore treated the top lipid-scrambling/phospholipid-transport nominees as weak but most relevant, and separately checked the KCNT/potassium-channel genes named by or closest to the Ano3 card.

| training perturbation | reason for inspection | focal `n_degs` | Parquet interpretation |
| --- | --- | ---: | --- |
| `Tmem63b` | strongest phospholipid-scramblase fallback, via GO `phospholipid scramblase activity` | 1 | one significant row, the self transcript |
| `Atp11c` | phospholipid translocation fallback | 0 | no focal BH-significant rows |
| `Atp8a2` | phospholipid translocation fallback | 0 | no focal BH-significant rows |
| `Atp9a` | phospholipid translocation fallback | 1 | one significant row, the self transcript |
| `Abca1` | phospholipid translocation/small-molecule transport fallback | 0 | no focal BH-significant rows |
| `Abca7` | phospholipid translocation/small-molecule transport fallback | 0 | no focal BH-significant rows |
| `Kcnt1` | Slack channel named in the Ano3 mechanism | 0 | no focal BH-significant rows |
| `Kcnt2` | Slack-family potassium-channel comparator | 0 | no focal BH-significant rows |
| `Kcnn2` | potassium-channel comparator | 0 | no focal BH-significant rows |
| `Kcnn3` | potassium-channel comparator | 0 | no focal BH-significant rows |
| `Kcnma1` | potassium-channel comparator | 1 | one significant row, the self transcript |
| `Kcnq2` | potassium-channel comparator | 1 | one significant row, the self transcript |
| `Kcnq3` | potassium-channel comparator | 1 | one significant row, the self transcript |

Broader calcium or ion-signaling nominees had occasional larger responses, but they were less operation-matched. `Calm1` had 14 DEGs and `Atp2b1` had 22; `Atp2a2` had 187 with ER-stress genes such as `Ddit3`, `Xbp1`, and `Herpud1`; NMDA receptor comparators ranged from self-only or nearly self-only (`Grin2a` = 1, `Grin2b` = 2) to a larger `Grin1` response of 89. I used these as boundaries rather than as Ano3 magnitude donors because ANO3 is neither a global calmodulin node, an ER calcium pump, nor a core glutamatergic receptor subunit.

## Synthesis

The closest task-matched evidence clustered at 0-1 DEG and often consisted only of the perturbed gene itself. Ano3's focal expression is real but sparse, and the biology bundle leaves the amount of ANO3 functional stock depleted by P37-P44 unresolved. That combination makes a large recovered-cell transcriptional program unlikely in `151 TH Prkcd Grin2c Glut`. Because nuclear self-target loss is not a reliable editing readout and Ano3 is lowly detected, I put the point forecast at the lower end of the 0-1 analogue range.

Predicted `n_degs`: 0
