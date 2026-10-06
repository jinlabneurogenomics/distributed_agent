# Glmn n_degs forecast trace

## Declared target

- Target: `Glmn`, from the one-row holdout manifest `Glmn.csv`.
- Cell group: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

## Target biology used

- The declared biology bundle reports exact focal expression in the assayed non-target population: `Glmn` is detected in 17,055 of 23,679 non-target thalamic nuclei, 72.0% of cells, with mean raw UMI 1.41 and pseudobulk CPM 88.4. This made the perturbation reachable in the focal population, but I did not use target mRNA abundance as an editing-efficiency proxy.
- The curated operation is direct regulation of cullin-RING ligases: soluble GLMN binds the RBX1 RING domain and inhibits RBX1-associated CRL activity by masking the E2-binding surface.
- The functional-stock card is unresolved for the 21-28 day P16-to-P37/P44 interval: a disruptive edit should stop new functional `Glmn` production, but available evidence does not measure GLMN half-life, RBX1-bound residence, or depletion kinetics in postmitotic thalamic neurons.
- The strong mouse loss-of-function phenotype is embryonic and vascular/developmental rather than an induced young-postmitotic-neuron phenotype, so I treated it as weak evidence for a large acute thalamic snRNA-seq signature.
- The characterization search did not find a close `Glmn` paralog, which weakly supports functional observability but does not exclude CRL-network buffering.

## Same-experiment and training evidence

- Packaged same-experiment corpus context for `Glmn` was absent: `target_found = false`, with zero Findings, Claims, or explicit references. No Glmn outcome was available from the corpus.
- The declared training count table has 1,674 measured training perturbations for `151 TH Prkcd Grin2c Glut`. It is dominated by tiny DEG counts: 1,205/1,674 are `0`, 276/1,674 are `1`, the median is `0`, the 75th percentile is `1`, the 90th percentile is `2`, and the 95th percentile is `18`.
- The direct RBX1/CUL1 axis members `Rbx1`, `Cul1`, `Nedd8`, and other cullins were absent from the count table. The GLMN-linked SCF adaptor `Fbxw7` was present with `n_degs = 1`.
- Other represented F-box/Kelch E3-adaptor perturbations were also near-null in this focal group: `Fbxo11 = 1`, `Fbxo38 = 0`, `Klhl20 = 0`, and `Klhl7 = 0`.
- Same-experiment `Fbxw7` Findings describe only a single adjusted-significant downstream gene, `Trp53inp2`, in `151 TH Prkcd Grin2c Glut`; they also report absence of canonical FBXW7 substrate-output programs and no strong data-driven signature neighbor in the full target universe. That makes the best local CRL/F-box observation narrow rather than broadly transcriptional.
- I scanned the declared expression parquet for the `Fbxw7` profile against the 1,674 eligible training targets in the exact focal cell group. `Fbxw7` had one FDR-significant feature; its closest whole-profile neighbors were also low-count perturbations, for example `Kif1b = 0`, `Lgr4 = 0`, `Kcnc2 = 1`, `Gclm = 1`, and `Dlst = 0`, so the parquet neighborhood did not reveal a hidden broad CRL-like response state behind the one-gene count.

## Forecast

The focal cells express `Glmn` broadly enough that a CRISPR lesion could be seen, and the RBX1/CRL interaction leaves room for a real but compact postnatal response once newly synthesized GLMN is lost. I did not project a large count because the postnatal neuronal requirement is unproven, GLMN stock depletion by harvest is indeterminate, and the only assayed direct functional neighbor, `Fbxw7`, plus the available F-box/Kelch comparators were flat to one-gene events in the same group.

My point forecast is therefore a single adjusted-significant measured gene.
