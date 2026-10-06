# Crebrf forecast

## Target and endpoint

- Target: `Crebrf`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with Wilcoxon BH-adjusted `p < 0.05`
- Prediction: `5`

## Evidence used

The declared holdout manifest contains only `Crebrf`, and `Crebrf` is absent
from the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` training
count table. The selected same-experiment corpus also has no `Crebrf` Findings,
Claims, or explicit comparator references in the July sourceguard release, so
the prediction used the supplied canonical biology bundle plus matched training
perturbations rather than a target report.

The exact focal-population expression card shows that `Crebrf` RNA is measured
in `151 TH Prkcd Grin2c Glut` non-target nuclei:

- `pct_cells_expressing = 69.52996325858355`
- `n_cells_expressing = 16464` of `23679`
- `mean_cp10k = 0.8675860749706191`
- `mean_raw_umi = 1.3510283373453271`

This supports broad enough target reach that a `Crebrf` effect would not be
obviously lost through rare-cell dilution. I did not use self-target RNA as an
editing-efficiency estimate.

The biology bundle places CREBRF as a soluble nuclear transcriptional
coregulator for CREB3-family and glucocorticoid-receptor-associated responses.
Its functional-stock card calls operative CREBRF likely substantially depleted
by P37-P44 because new synthesis should stop after editing and the protein is
proteasome-sensitive, but the evidence is partial and comes from ectopic
Neuro2a kinetics rather than an endogenous juvenile thalamic time course. The
closest phenotype evidence is adult global Crebrf-null behavior/HPA physiology,
not acute thalamic postmitotic neuronal loss; no close paralog was found, but
network buffering remains unresolved.

The focal training count table is strongly sparse: among 1,674 measured
training targets, 1,205 have `n_degs = 0`, 1,481 have `n_degs <= 1`, the median
is 0, the 75th percentile is 1, and only 103 targets exceed 10 DEGs. This made
a large count inappropriate without a very close high-response comparator.

I treated the following same-class training counts as the most relevant direct
scale anchors:

| perturbation | reason for inclusion | `n_degs` |
|---|---:|---:|
| `Atf6` | represented basal ER/CREB3-like UPR sensor branch | 0 |
| `Creb1` | CREB-family nuclear transcriptional node | 10 |
| `Crebbp` | CREB/KAT3 coactivator with a thalamic response | 8 |
| `Ep300` | KAT3 paralog of `Crebbp` | 0 |
| `Ncoa1` | p160 nuclear receptor coactivator | 0 |
| `Ncoa3` | p160 nuclear receptor coactivator | 0 |
| `Nr3c1` | glucocorticoid receptor itself | 0 |
| `Hspa5` | positive control for an ER quality-control response | 5 |

Those anchors had five exact nulls and three small responses at the task's
FDR<0.05 threshold. `Hspa8` and `Klf9`, used as adjacent but less direct
stress/glucocorticoid context checks, were also still small at 9 and 19 DEGs.

The packaged Findings reinforced the same interpretation:

- `Atf6` was transcriptionally flat across recovered basal neuronal groups,
  and an internal `Hspa5` contrast showed that the assay could detect an ER
  folding/ERAD program in `151 TH Prkcd Grin2c Glut`.
- `Creb1` and `Crebbp` produced restricted thalamic programs rather than large
  generic CREB/KAT3 activity-state collapse.
- `Ep300` did not produce a corrected steady-state neuronal response, and
  single `Crebbp`, `Ep300`, and `Creb1` perturbations were explicitly
  noninterchangeable.
- `Nr3c1`, `Ncoa1`, `Ncoa3`, and assayed steroid-receptor relatives were
  largely weak or silent under basal postnatal conditions, with no shared
  unliganded neuronal steroid-receptor module.

Matched profile comparison in `151 TH Prkcd Grin2c Glut` separated these
quiet/direct anchors from high-burden chromatin or transcriptional machinery
perturbations. In the same table, broad controls such as `Nr1d1`, `Nrf1`,
`Brd4`, `Ctcf`, `Yy1`, `Zbtb7a`, and `Sin3a` ranged from 116 to 1,433 DEGs,
whereas the CREB3/glucocorticoid-adjacent set remained at 0-10 except for
`Klf9` at 19. Significant-gene intersections between the low direct anchors
and the high controls were mostly absent, so I treated the high controls as
upper-state contrasts rather than quantitative analogs.

## Synthesis

I expect functional `Crebrf` loss to be realized in many assayed thalamic
neurons, because the target is expressed in about 70% of focal non-target
nuclei and its soluble CREBRF stock should turn over within the 21-28 day
window. That argues against forcing the prediction to the training-table
median of zero.

The expected transcriptional coupling is still weak. CREBRF is a CREB3/GR
coregulator, not a core ER chaperone, proteasome component, RNA-processing
factor, or global chromatin scaffold. The most relevant basal training
perturbations in the same class were null to low at FDR<0.05, and the corpus
records repeatedly show that UPR sensors, p300/CBP/CREB, and steroid-receptor
cofactors do not form one high, interchangeable postnatal neuronal module in
this assay.

Balancing high target reach and plausible within-window depletion against that
low observed comparator scale, I chose a low nonzero point: **5 DEGs**.
