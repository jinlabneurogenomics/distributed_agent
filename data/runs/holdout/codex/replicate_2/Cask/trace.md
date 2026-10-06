# Cask forecast trace

## Target and endpoint

- Target: `Cask`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- The focal count table contains 1,674 training perturbations and does not contain `Cask`; I used only the declared Cask biology bundle plus training rows from `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` and matching focal-group rows from `training_de_all_cell_groups.parquet`.

## Cask-specific biology

The canonical `Cask` biology bundle supports expression and realized protein loss in the focal context, but it does not imply a large nuclear-RNA program.

- Exact focal expression is present: in non-target `151 TH Prkcd Grin2c Glut` nuclei, `Cask` was detected in 14,967 / 23,679 cells, or 63.21%, with mean raw UMI 1.16, mean CP10K 0.72, mean log1p CP10K 0.455, and pseudobulk CPM 72.77.
- Functional stock adjudication was `likely_substantially_depleted`: CASK is a multidomain MAGUK-family pre/postsynaptic scaffold; disruptive editing stops new protein supply, and the 21-28 day edit-to-harvest window spans more than the 6.35-day culture half-life cited in the bundle.
- The realization prior is not a pure null: adult cortical CASK-negative neurons have a cell-autonomous synaptic physiology phenotype, pan-neuronal juvenile loss has a severe postnatal phenotype, and the bounded paralog search found no close CASK paralog with demonstrated same-context compensation.
- The main downward bearings are endpoint and context mismatch. The phenotype evidence is cortical or pan-neuronal rather than acute P16 thalamic `Prkcd/Grin2c` neurons, CASK loss primarily perturbs synaptic complexes, and survivor-conditioned snRNA-seq need not convert a synaptic physiology defect into many BH-significant nuclear transcript changes.

## Training-scale evidence

The focal count table is sparse overall:

- 1,205 / 1,674 training perturbations had `n_degs = 0`.
- The median was `0`, the 75th percentile was `1`, and the 90th percentile was `2`.
- The large tail was dominated by broad RNA-processing, proteostasis, and transcriptional/chromatin regulators, not by local synaptic scaffold perturbations.

I therefore selected the training perturbations closest to CASK's annotated operation and published phenotype rather than tail genes with generic severity:

| training target | rationale | n_degs |
|---|---:|---:|
| `Nrxn1` | CASK-binding neurexin family | 1 |
| `Nrxn2` | CASK-binding neurexin family | 0 |
| `Nrxn3` | CASK-binding neurexin family | 0 |
| `Caskin1` | CASK-associated synaptic scaffold axis | 1 |
| `Dlg4` | MAGUK/postsynaptic scaffold | 1 |
| `Grin2b` | NMDA receptor subunit implicated in CASK-loss synaptic phenotype | 2 |
| `Shank2` | postsynaptic scaffold | 0 |
| `Shank3` | postsynaptic scaffold | 2 |
| `Syngap1` | postsynaptic signaling scaffold | 0 |
| `Arhgef9` | inhibitory postsynaptic scaffold/signaling axis | 1 |
| `Camk2a` | CaMK synaptic signaling | 0 |
| `Camk2b` | CaMK synaptic signaling | 1 |
| `Camk2g` | CaMK synaptic signaling | 0 |

The median of this 13-target synaptic set is `1`, and the direct/proximal subset `Nrxn1/Nrxn2/Nrxn3/Caskin1/Dlg4/Grin2b` sums to 5 DEGs across 6 perturbations, for a mean of 0.83 and a median of 1. In the Parquet, the `1`-DEG analogs above were self-transcript-only in `151 TH Prkcd Grin2c Glut`; `Grin2b` had self plus `Pianp`, and `Shank3` had self plus `Uba5`. That pattern argues for a realized but tiny local signature, not for a broad downstream transcriptional state.

## Numeric synthesis

The exact expression reach and CASK protein turnover keep the forecast above a hard zero: CASK is measurably present in this population, and the 21-28 day harvest is long enough for a loss-of-resupply edit to deplete most renewable CASK pools. The same-experiment training scale pulls the estimate sharply downward because observed perturbations of neurexins, postsynaptic scaffolds, NMDA/synaptic signaling components, and adjacent MAGUK biology almost always yielded only the self target or no significant genes in this focal thalamic class.

I predict `n_degs = 1`, interpreting the expected signal as self-only or near self-only rather than as a multi-gene CASK-loss transcriptional program.
