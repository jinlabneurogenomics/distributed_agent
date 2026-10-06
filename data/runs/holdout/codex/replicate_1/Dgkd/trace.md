# Direct `n_degs` Forecast for `Dgkd`

## Endpoint

- **Target:** `Dgkd`, from the one-row holdout manifest
  `[local file: Dgkd.csv]`.
- **Cell class:** `151 TH Prkcd Grin2c Glut`, an exact match to the thalamic glutamatergic class in the task bindings.
- **Endpoint:** number of focal-class measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- **Training count surface:** `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`, containing 1,674 non-target training perturbations.
- **Raw expression surface used for profile checks:** `[local file: training_de_all_cell_groups.parquet]`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"` for a 15-node DAG/PIP2/PKC/synaptic-vesicle analogue cohort.

## `Dgkd` Biology Used

The declared prediction-safe biology bundle maps the assigned `Dgkd` target to
current mouse `Dgkq` / DGKtheta and keeps it distinct from DGKdelta. The enzyme
phosphorylates diacylglycerol to phosphatidic acid in a synaptic-lipid context.

Exact focal-class reach is moderate rather than absent: the in-assay non-target
expression summary reports `Dgkd` in **11,627 / 23,679** focal non-target nuclei
with **49.10%** of cells expressing, mean log1p CP10K **0.314**, and mean raw UMI
**0.752**. This supports target accessibility in the assayed class, while the
dataset portrait cautions that target-transcript abundance is not editing
efficiency.

The functional-stock card calls DGKtheta **likely substantially depleted** over
the 21 to 28 day P16-to-P37/P44 editing window: full-length protein has an
hours-scale turnover estimate in mouse cell lines, and the operative stock is a
renewed catalytic enzyme pool. The best neural loss evidence is nevertheless a
stimulus-evoked synaptic-vesicle endocytosis defect in cultured mouse
cortical/hippocampal neurons, not an acute postnatal thalamic loss experiment or
a broad transcriptional failure state. Other DGK isoforms remain present, and
DGKtheta-null mice lacked a gross viability phenotype in the cited mouse study.

Together, those target priors argued for a real but local synaptic/lipid
perturbation: enough expression and turnover to avoid treating the target as
unreachable, but no evidence for the kind of severe proteostasis, spliceosome,
transcription-factor, or mitochondrial state that produced the largest DEG
burdens in this cell class.

## Training Measurements That Anchored the Scale

The focal count table is extremely zero-inflated:

| statistic | `n_degs` |
|---|---:|
| targets | 1,674 |
| zero-DEG targets | 1,205 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2,677 |

I nominated training analogues with the local curated annotation/corpus
nomination helper and then inspected their focal counts. The only three
non-fallback narrow-module nominees were all in Reactome `Effects of PIP2
hydrolysis` and were sparse:

| training target | nomination relation to `Dgkd` | focal `n_degs` |
|---|---|---:|
| `Dgke` | narrow module; ATP-dependent diacylglycerol kinase activity | 1 |
| `Itpr1` | narrow module; PIP2 hydrolysis | 0 |
| `Abhd12` | narrow module; PIP2 hydrolysis | 1 |

The closest broad biochemical and synaptic fallbacks were also mostly at zero
or one DEG in the same focal count table:

| training target | biological role used as context | focal `n_degs` |
|---|---|---:|
| `Agk` | glycerolipid / DGK-adjacent kinase fallback | 0 |
| `Prkcg` | DAG-dependent PKC | 1 |
| `Prkca` | DAG-dependent PKC | 0 |
| `Plcb1` | PLC / phosphoinositide signaling | 0 |
| `Pik3r1` | PI3K regulatory subunit | 0 |
| `Pik3r2` | PI3K regulatory subunit | 0 |
| `Pik3cb` | PI3K catalytic subunit | 0 |
| `Mtor` | broad PI3K/mTOR signaling | 2 |
| `Syp` | synaptic vesicle marker in the fallback pool | 1 |
| `Dnm1` | synaptic-vesicle endocytosis fallback | 1 |
| `Calm1` | Ca2+/synaptic-vesicle regulation fallback | 14 |
| `Creb1` | downstream activity-responsive transcription factor | 10 |

Those counts put the chemically closest DGK/PIP2/PLC/PKC neighborhood at
approximately the 75th to 90th percentile of the focal training distribution,
not in the high-response tail. The few larger nearby counts came from broader
calcium/activity or transcriptional fallbacks and did not represent the same
proximal lipid-kinase operation.

## Matched Focal Profile Check

The run-local observed-profile comparison over
`Dgke, Agk, Itpr1, Abhd12, Prkcg, Prkca, Plcb1, Pik3r1, Pik3r2, Pik3cb, Mtor,
Syp, Dnm1, Calm1, Creb1` was restricted to the declared focal class and used
`logfoldchanges` with `pvals_adj < 0.05`. All 15 training profiles were present.

The cohort remained weak at the row-level expression surface:

- **7 / 15** selected profiles had no significant focal feature.
- **6 / 15** selected profiles had 1 to 9 significant focal features.
- **2 / 15** selected profiles had 10 to 49 significant focal features.
- For the tightest inspected focal nodes, the exact significant-feature counts
  were `Dgke = 1`, `Itpr1 = 0`, `Abhd12 = 1`, `Prkca = 0`, and `Plcb1 = 0`,
  matching the count table.

The pairwise focal-profile inspection did not reveal a shared significant
module among the tight candidates: the one significant negative feature in
`Dgke` did not intersect the significant feature sets of its inspected peers,
while `Itpr1`, `Prkca`, and `Plcb1` had no significant focal features at all.
Thus the quantitative expression surface reinforced a sparse expected response
instead of justifying transfer from a larger broad-pathway outlier.

## Point Synthesis

Upward bearings:

- `Dgkd` is expressed in roughly half of the focal thalamic non-target nuclei.
- The protein stock should be mostly replaceable within the P16-to-P37/P44
  window.
- DGKtheta has a real catalytic neuronal phenotype, so a complete transcriptional
  null is not forced.

Downward bearings:

- The established phenotype is local, evoked synaptic-vesicle endocytosis, with
  no matching acute postnatal thalamic transcriptional syndrome.
- The nearest measured DGK/PIP2 targets were `0`, `1`, and `1` DEGs.
- DAG-dependent PKC, PLC, PI3K, `Mtor`, and immediate vesicle fallbacks were
  also mostly `0` to `2` DEGs in the same cell class.
- The focal training distribution has median `0`, 75th percentile `1`, and 90th
  percentile `2`.

I therefore treated `Dgkd` as reachable but expected to produce only a tiny
survivor-conditioned nuclear RNA footprint. The one-count value preserves the
slight upward evidence from expression, stock turnover, and the observed
`Dgke`/`Abhd12` weak responses without moving toward broad high-count lipid or
activity fallbacks.

**Predicted `n_degs`: 1**
