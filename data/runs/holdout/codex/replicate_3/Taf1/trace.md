# Direct n_degs forecast for Taf1

## Target and endpoint

- Manifest target: `Taf1`.
- Requested cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes in that class with Wilcoxon `pvals_adj < 0.05`.
- Declared target bundle provenance states that endpoint values were not used in the biological cards, and the served `biology` view reported `target_outcome_exposed=false` and `labeled_neighbors_exposed=false`.

## Target biology used

The canonical `Taf1` bundle supports target reach in the exact assayed population: in non-targeting `151 TH Prkcd Grin2c Glut` nuclei, `Taf1` was detected in 19,528 of 23,679 cells, or 82.47%, with mean log1p(CP10K) 0.733 and pseudobulk 127.2 CPM. Thus lack of baseline expression should not force a zero prediction.

The same bundle identifies TAF1 as the largest TFIID subunit, a promoter-recognition / RNA polymerase II preinitiation-complex scaffold with annotated catalytic activities. A P16 frameshift edit should stop new intact TAF1 supply in edited cells, and the card did not find a close mouse paralog with established neuronal compensation.

The major downward uncertainty is within-window functional stock. The functional-stock adjudication concluded `functional_stock_by_harvest=indeterminate`: pre-existing TAF1 protein and TFIID-bound pools can persist after the edit, and no TAF1 degradation half-life, TFIID exchange time, or postmitotic thalamic loss timing was found. The loss phenotypes were developmental or disease-allele contexts, not acute P16 thalamic-neuron knockouts. Survivor conditioning could also attenuate a severe basal-transcription lesion.

## Training measurements used

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 measured training perturbations. Its DEG-count distribution is very sparse:

- 1,205 / 1,674 training perturbations had `n_degs = 0`.
- median = 0, 75th percentile = 1, 95th percentile = 18, 99th percentile = 430.
- The maximum high-count responses were `Uba5` 2677, `Tpr` 1768, and `Sin3a` 1433.

The most operation-proximal visible low-level transcription machinery examples were quiet to modest in this exact class:

| training perturbation | reason kept visible | `n_degs` |
|---|---:|---:|
| `Gtf2h5` | general TFIIH subunit | 0 |
| `Taf1b` | TAF1-family Pol I factor, not TFIID | 0 |
| `Med13l` | Mediator kinase-module relative | 1 |
| `Med13` | Mediator kinase-module subunit | 11 |
| `Med23` | Mediator tail subunit | 13 |
| `Med15` | Mediator tail subunit | 19 |

I used the declared parquet through `profile_compare` in `151 TH Prkcd Grin2c Glut` for those genes plus chromatin / transcriptional upper-bracket rows `Sin3a`, `Yy1`, `Brd4`, `Setd1a`, `Ctcf`, and `Smarcc2`. The parquet-derived activity table recapitulated the count split: the GTF/Mediator side was 0, 0, 1, 11, 13, 19 significant genes, while the upper chromatin rows were 185-1433. The selected cohort had stronger shared negative-tail overlap than positive-tail overlap, but the broad chromatin rows were not a tight TAF1-like state.

Packaged same-experiment Findings supported that interpretation. `Med13`, `Med15`, and `Med23` formed a sparse 151-thalamic module dominated by down-regulated synaptic, calcium, ion-handling, and subtype-identity genes. In contrast, `Brd4`, `Yy1`, `Setd1a`, `Ctcf`, and `Sin3a` each had larger, more specific posterior/chromatin, proteostasis, RNA-processing, or clustered-protocadherin programs; those reports are useful upper-state brackets, not direct TFIID magnitude donors.

## Synthesis

The forecast should be nonzero because `Taf1` is expressed in most focal thalamic nuclei, is a central TFIID component, and lacks an obvious same-species neuronal paralog. It should also stay far below the hundreds-to-thousands chromatin/stress rows because acute depletion of the pre-existing TAF1/TFIID functional pool by P37-P44 is unresolved, and the closest measured Pol II/Mediator comparators were sparse rather than broad.

I therefore placed `Taf1` just above the observed Mediator/GTF branch and just above the whole-training 95th percentile, while keeping it within the 10-49 DEG activity regime rather than the broad >=50 regime.

Predicted `n_degs`: 24
