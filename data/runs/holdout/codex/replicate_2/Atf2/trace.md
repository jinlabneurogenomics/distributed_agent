# Atf2 n_degs forecast

## Target and endpoint

- **Target:** `Atf2`, the sole row of the declared holdout manifest.
- **Cell class:** `151 TH Prkcd Grin2c Glut`.
- **Endpoint:** `n_degs`, the number of measured genes in that class with Wilcoxon `pvals_adj < 0.05`.
- **Primary quantitative inputs:** the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table and the declared `training_de_all_cell_groups.parquet` Parquet.
- **Target-outcome guard:** I did not query any `Atf2` perturbation signature or same-experiment `Atf2` report; the `Atf2` biology bundle was used only for endpoint-blind biology and exact non-target expression reach.

## Evidence used

### Biology of the held-out perturbation

The canonical `Atf2` biology bundle makes functional perturbation in this assay plausible but not predictive of a large basal postnatal thalamic response.

- `Atf2` is well within the focal expression window: in non-target `151 TH Prkcd Grin2c Glut` nuclei, Atf2 was detected in **20,531 / 23,679 cells = 86.7%**, with mean CP10k **1.499** and mean raw UMI **2.365**.
- ATF2 is a dynamic nuclear CRE/AP-1 bZIP transcription factor whose activity depends on phosphorylation and homo- or heterodimerization, with `Jun` and `Atf7` named as related genes in the source card.
- The functional-stock adjudication calls the pre-edit protein pool **likely substantially depleted** by the P37-P44 harvest after P16 editing: measured ATF2 turnover is hours-scale in cultured-cell pulse-chase data, far shorter than the 21-28 day assay window.
- The positive neural loss evidence is developmental and mismatched: neuron-specific mouse `Atf2` loss caused embryonic cranial motoneuron degeneration, but the bundle explicitly leaves postnatal thalamic demand, latency, and Atf7 compensation unresolved.

### Training response scale

The focal training count table is extremely sparse. Among **1,674** visible perturbations in `151 TH Prkcd Grin2c Glut`, **1,205** had `n_degs = 0`; the median was **0**, the 75th percentile was **1**, the 90th percentile was **2**, and the 95th percentile was **18**. The very large tail was dominated by broad RNA/proteostasis/chromatin perturbations such as `Uba5` = 2677, `Tpr` = 1768, `Sin3a` = 1433, `Rnpc3` = 868, and `Zbtb7a` = 841, not by basal AP-1/ATF-family transcription factors.

The closest available training perturbations to ATF2's bZIP/AP-1/CRE/stress-regulated biology were zero or weak in the same endpoint. Direct Parquet queries in the focal class confirmed 17,259 measured genes for each of these perturbations and the following FDR<0.05 counts:

| comparator | `n_degs` in `151 TH Prkcd Grin2c Glut` | interpretation for Atf2 |
| --- | ---: | --- |
| `Jund` | 0 | AP-1/JUN family comparator; locally silent |
| `Fosl2` | 0 | AP-1/FOS family comparator; locally silent |
| `Atf6` | 0 | ATF-family stress bZIP comparator; locally silent |
| `Nfe2l1`, `Nfe2l2` | 0 each | CNC-bZIP stress comparators; locally silent |
| `Maf`, `Mafa`, `Mafb` | 0 each | large-Maf bZIP comparators; locally silent |
| `Mafg` | 1 | small-Maf bZIP comparator; a single `Lamp2` event |
| `Nr4a1`, `Nr4a3`, `Egr2` | 0 each | immediate-early/activity-regulated comparators; locally silent |
| `Mapk1`, `Mapk9`, `Map2k2` | 0 each | represented upstream MAPK comparators; locally silent |
| `Map2k1` | 4 | small MAPK-pathway signature, still far below the 95th percentile |
| `Creb1` | 10 | small CRE-family thalamic signature, centered on `Crem` induction |

The same-experiment corpus release, treated as interpretation of the training experiment rather than independent replication, was directionally consistent with this sparse readout:

- `Jund:F001` reports that `Jund` loss was buffered across basal postnatal neurons, with 22 of 23 measured groups having no downstream FDR<0.10 genes.
- `Fosl2:F001` reports that `Fosl2` loss was almost completely buffered in P16-to-P37/P44 postmitotic neurons.
- `Fosl2:F003` and `Jund:F003` report that represented AP-1/JUN and broader bZIP/MAPK relatives did not phenocopy one another.
- `Atf6:F001` reports a corrected-transcriptome null for `Atf6`.
- `Nfe2l2:F001` reports an acute postnatal neuronal null for `Nfe2l2`.
- `Creb1:F002` identifies the broadest `Creb1` response as the same thalamic class, but that exact endpoint is still only a 10-gene response at FDR<0.05.
- Corpus claim `claim:a62639e575be48d95664` summarizes the measured CREB/AP-1/EGR/bZIP/MAPK neighborhood as divergent, sparse, or absent rather than a shared postnatal neuronal loss-of-function module.

### Profile comparison

I compared the full signed Parquet profiles of 17 selected AP-1/bZIP/CRE/MAPK-related measured targets in `151 TH Prkcd Grin2c Glut`: `Atf6`, `Creb1`, `Egr2`, `Fosl2`, `Jund`, `Maf`, `Mafa`, `Mafb`, `Mafg`, `Map2k1`, `Map2k2`, `Mapk1`, `Mapk9`, `Nfe2l1`, `Nfe2l2`, `Nr4a1`, and `Nr4a3`.

That cohort had **14/17** nodes with no significant features, **2/17** with one to nine significant features, and **1/17** with 10 to 49 significant features. The cohort diagnostic found no recurring significant program among the nonzero nodes: the positive and negative significant-program overlap coefficients were both **0.0**. I therefore treated the `Creb1`, `Map2k1`, and `Mafg` counts as small isolated responses, not as evidence for a coherent AP-1/bZIP module that should be transferred upward to `Atf2`.

## Synthesis

The `Atf2` edit should have enough time and expression reach to remove newly supplied ATF2 function in many assayed nuclei, so I did not dismiss it as an expression-negative or protein-stock-protected perturbation. The limiting issue is endpoint demand: the direct neural loss precedent is embryonic brainstem, Atf7 redundancy in juvenile thalamus is unknown, and the measured postnatal basal AP-1/bZIP/stress neighborhood is overwhelmingly flat in exactly the requested thalamic class.

I therefore placed `Atf2` at the modal value of the closest measured biology rather than at the screen-wide mean, the `Creb1` value, or the high-yield tail. The strongest upward analog was `Creb1` at 10 genes, but ATF2 is a stress/AP-1 bZIP factor rather than CREB1 itself, and the local `Jund`/`Fosl2`/`Atf6`/`Nfe2l1`/`Nfe2l2`/MAPK comparisons all argue that pathway membership alone is not enough to produce a detectable basal survivor transcriptome.

**Predicted `n_degs`: 0**
