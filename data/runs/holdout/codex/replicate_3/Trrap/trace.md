# Direct forecast trace for Trrap

## Target and endpoint

- **Target:** `Trrap`
- **Cell class:** `151 TH Prkcd Grin2c Glut`
- **Endpoint:** `n_degs`, the number of measured genes in the declared 151 training/holdout count surface with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- **Declared target profile status:** the held-out `Trrap` 151 signature and `Trrap` 151 DEG count were not present in the count table or in the training DE parquet used for quantitative comparison.

## Evidence used

### Biology-only Trrap bundle

The declared `Trrap` bundle, served as the `biology` characterization view with `target_outcome_exposed=false`, supports a perturbation that should be reachable in this assay rather than a permanently pre-installed developmental state.

- `Trrap` RNA was detected in the exact focal non-target population: 21,438 of 23,679 nuclei, 90.54% expressing; mean raw UMI 2.90; pseudobulk CPM 181.81.
- TRRAP is annotated as a large noncatalytic scaffold in NuA4/TIP60- and SAGA/STAGA-family HAT/chromatin-regulatory complexes.
- The functional-stock adjudication calls the operative entity a `dynamic_complex_component`; a P16 disruptive edit should stop new TRRAP supply while pre-existing complex stock clears.
- The same card concludes `functional_stock_by_harvest=likely_substantially_depleted`, with evidence completeness marked partial: efficient neuronal protein loss and broad molecular remodeling have been seen during early postnatal conditional deletion, and Purkinje-neuron structural consequences appear on a weeks time scale, but neither experiment is synchronized P16 thalamic deletion.

I treated this as upward evidence relative to the atlas-wide and 151-class baseline of a zero DEG call.

### 151 TH Prkcd Grin2c Glut training count table

The declared 151 count table contains 1,674 non-target training perturbations. Its distribution is very sparse:

- 1,205 / 1,674 training targets have `n_degs = 0`.
- Median `n_degs` is 0; the 75th percentile is 1; the 90th percentile is 2; the 95th percentile is 18.
- The mean is 14.05 only because of a long tail headed by a few very large perturbations such as `Uba5` 2677, `Tpr` 1768, and `Sin3a` 1433.

For curated mouse chromatin regulators available in this same table, 95 / 138 are zero in this cell class, with median 0, 75th percentile 1, 90th percentile 44.2, and 95th percentile 276. The class can detect some chromatin perturbations, but chromatin-regulator identity alone is not enough to place a target in the large-count tail.

### Trrap-near observed perturbations

Most canonical NuA4/SAGA partners around TRRAP were not in the 151 training table. The exact co-complex or directly interacting observed perturbations that were available landed low:

| Training perturbation | Biological relation to TRRAP used here | 151 `n_degs` |
|---|---:|---:|
| `Atxn7` | recurrent exact STAGA/TFTC co-complex member and physical interactor | 0 |
| `Myc` | exact MYC-KAT2A-TRRAP co-complex member and physical interactor | 0 |
| `Med23` | exact TFTC-type HAT co-complex member | 13 |
| `Med13` | exact TFTC-type HAT co-complex member | 11 |
| `Tubb5` | exact TIP60-C co-complex member | 1 |
| `Esr1` | exact TFTC-type HAT co-complex member | 0 |
| `Prkdc` | exact H2A.Z p400/TIP60 co-complex member | 0 |

Other assayed HAT/coactivator-adjacent chromatin perturbations were also small in the same cell class: `Ep300` 0, `Kat6a` 0, `Kat6b` 0, `Brd1` 4, and `Crebbp` 8. Same-experiment corpus Findings for `Atxn7` also summarized it as transcriptomically buffered across the assayed postmitotic neuronal panel; lexical corpus retrieval found no direct `Trrap` report/Claim records in the selected release.

### Profile check

I compared a caller-selected cohort of HAT-adjacent and active chromatin-regulator training perturbations in the declared parquet for `151 TH Prkcd Grin2c Glut`.

- The endpoint counts recovered from the parquet matched the count table for the comparators above.
- `Atxn7`, `Ep300`, `Kat6a`, `Kat6b`, and `Myc` had no FDR 0.05 significant features despite matched perturbed-cell counts of 124, 155, 170, 150, and 210 respectively, so their quiet calls were not simply the lowest-power cases in the cohort.
- Genome-wide weak-vector similarities were not decision-grade by themselves; FDR-supported intersections between the quiet HAT-adjacent perturbations and active chromatin regulators were empty or tiny. For example, `Atxn7` shared zero FDR-supported positive or negative features with `Setd1a`, `Chd4`, `Setdb1`, and `Zmynd8` in the inspected profile table.

## Synthesis

The strongest upward evidence is that `Trrap` is broadly expressed in the focal nuclei, has no close replacement scaffold in the bundle, and should lose a renewable chromatin/HAT-complex function over the 21-28 day editing window. That made a strict zero forecast too conservative.

The strongest downward evidence is quantitative and local: the represented SAGA/TFTC/TIP60 neighbors do not show a broad acute thalamic signature, and `Atxn7`, the most recurrent exact SAGA/STAGA/TFTC co-complex training target, is completely buffered in this cell class. The `Med13`/`Med23` 11-13 DEG counts are the nearest nonzero exact co-complex scale anchors. Larger chromatin responses such as `Sin3a`, `Brd4`, `Setd1a`, and `Chd4` establish assay detectability but are different repressive or reader/writer modules rather than direct TRRAP scaffold loss.

I therefore placed `Trrap` just above the measured TFTC/Mediator-adjacent local donors, high enough to reflect its broader scaffold role and high exact expression but below the recurrent large chromatin tail.

**Predicted `n_degs`: 16**
