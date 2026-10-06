# Sox3 direct n_degs forecast

## Target and endpoint

- Target from the declared one-row holdout manifest: `Sox3`.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05`.
- The declared count table and differential-expression Parquet are training-only for this task; `Sox3` was absent from the `151 TH Prkcd Grin2c Glut` count table and no same-experiment Sox3 Finding or Claim was exposed in the selected corpus release.

## Evidence used

1. `Sox3` in-assay reach is very low in the focal non-target population.
   The canonical Sox3 biology bundle reports 521 expressing nuclei among 23,679 matched non-target nuclei in `151 TH Prkcd Grin2c Glut`:
   `pct_cells_expressing=2.2002618353815615`, `mean_raw_umi=0.023903036445795854`, `mean_log1p_cp10k=0.011126909162247267`, and `pseudobulk_cpm=1.4980880571766322`.

2. The endpoint distribution in the 1,674 visible training perturbations is heavily concentrated at zero:
   1,205 targets had `n_degs=0`, 276 had `n_degs=1`, the median was 0, the 75th percentile was 1, and the 90th percentile was 2. Large signatures exist in this class, but they are rare and mostly far outside the developmental Sox-family biology.

3. The assayed Sox-family comparators were flat or tiny in this same class:
   `Sox2=2`, `Sox5=2`, and `Sox4`, `Sox9`, `Sox10`, `Sox11`, `Sox17`, and `Sox18` each had 0 genes at BH `p < 0.05`.
   The expression Parquet confirmed the exact 151-class hits were only `Sox2 -> Tnnt1, Stam` and `Sox5 -> Dgkh, Tnnt1`.

4. Same-experiment corpus Findings for those observed comparators interpret the Sox-family responses as sparse and target-specific rather than a reusable generic SOX/HMG-box transcriptional module: Sox2 and Sox5 both produced two-gene thalamic signatures, most represented Sox-family perturbations were flat, and the shared `Tnnt1` edge had opposite sign between Sox2 and Sox5. These corpus records are curated views of the same Parquet, not independent replication.

5. The target biology bundle gives no positive acute postnatal thalamic requirement that would overcome the low expression prior. SOX3 is a nuclear SOXB1 HMG-box developmental transcription factor; mouse loss phenotypes are embryonic ventral-diencephalic, hypothalamo-pituitary, and CNS-midline phenotypes rather than P16-to-P37/P44 thalamic neuronal phenotypes. SOX2 can replace SOX3 when engineered into the Sox3 locus, but the bundle reports no evidence that endogenous Sox2 compensation or SOX3 protein turnover in juvenile thalamic neurons can be quantified over the 21-28 day experimental window.

## Synthesis

The base rate already favors a zero or near-zero DEG count in `151 TH Prkcd Grin2c Glut`, and the exact Sox3 focal-population expression is near the floor. The two closest measured SOX perturbations show that rare two-gene thalamic outputs are possible, so I did not collapse the forecast to a technical null solely from developmental context. However, Sox2 and Sox5 are themselves only two-gene sparse, most other measured Sox-family perturbations are zero in the same class, and the corpus explicitly rejects a common Sox-family neuronal response. With no packaged Sox3 response, no acute thalamic causal phenotype, and only 2.2% target-positive non-target nuclei in the focal class, the most likely integer is the modal training value.

Predicted `n_degs`: `0`.
