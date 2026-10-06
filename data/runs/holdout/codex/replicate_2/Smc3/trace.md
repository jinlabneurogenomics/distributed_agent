# Smc3 n_degs forecast for 151 TH Prkcd Grin2c Glut

## Declared target and endpoint

- The one-row manifest target is `Smc3`.
- The endpoint is the count of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- The declared training count table contains 1,674 non-held-out targets for this cell group; `Smc3` is absent.

## Target biology used

The canonical `Smc3` biology bundle identifies SMC3 as an obligate ATPase-core component of the chromatin-loaded cohesin ring. A disruptive P16 edit is expected to stop new functional SMC3 supply; cohesin exchange is dynamic on the 21-28 day P16 to P37-P44 interval, so the functional-stock card adjudicates `functional_stock_by_harvest = likely_substantially_depleted`. The bundle also keeps the main caveat: pre-existing cohesin is not directly opened or destroyed by editing, and the neuronal SMC3 protein half-life is unknown.

The exact focal-population expression measurement supports reach in the assayed population: in non-target `151 TH Prkcd Grin2c Glut` nuclei, `Smc3` is detected in 17,963 of 23,679 nuclei, or 75.86%, with mean raw UMI 1.615. This was used only as context reach; target-transcript loss was not used as an editing-efficiency proxy.

## Same-experiment cohesin evidence

The same-experiment corpus was used as interpretation of the training experiment, not as independent replication. Its `Smc1a` and `Stag2` Findings report a restricted shared thalamic cohesin module in `151 TH Prkcd Grin2c Glut`, while `Stag1`, `Pds5a`, and `Hdac8` were flat or nonconvergent and `Ctcf` produced a broader CTCF-dominant program rather than phenocopying the measured cohesin perturbations.

The requested FDR<0.05 threshold was checked in the declared count table and expression Parquet for the material measured perturbations:

| training perturbation | n_degs at FDR<0.05 in 151 |
| --- | ---: |
| `Smc1a` | 24 |
| `Stag2` | 37 |
| `Stag1` | 0 |
| `Pds5a` | 0 |
| `Hdac8` | 0 |
| `Ncapd3` | 0 |
| `Prr12` | 0 |
| `Zfp609` | 0 |
| `Smchd1` | 0 |
| `Ctcf` | 270 |
| `Ctnnb1` | 383 |
| `Psmb4` | 742 |
| `Uba5` | 2677 |
| `Sin3a` | 1433 |

`Smc1a` and `Stag2` were the only represented direct cohesin-core or SA-subunit perturbations with a robust restricted response. In the Parquet, their FDR<0.05 programs shared 9 genes and all 9 had the same sign. A rank-profile comparison over 17,259 measured genes placed `Stag2` as the nearest selected whole-profile neighbor of `Smc1a` with Pearson 0.264 and cosine 0.266; `Ctnnb1`, `Ctcf`, `Psmb4`, and `Uba5` were weaker or broader context neighbors.

Across the whole 1,674-target training count table for `151 TH Prkcd Grin2c Glut`, the median target had 0 DEGs, the 75th percentile had 1, the 95th percentile had 18, and the 99th percentile had 430. Thus the `Smc1a`/`Stag2` counts are a real but compact response regime rather than a screen-wide broad-stress regime.

## Numeric synthesis

`Smc3` is closer to `Smc1a` than to `Stag1`, `Pds5a`, or `Hdac8`: SMC3 is a shared core ring component, whereas the quiet nodes are a paralogous SA subunit or cohesin-cycle regulators that the measured assay showed are not interchangeable with `Smc1a`/`Stag2`. I therefore used the `Smc1a`/`Stag2` scale as the direct quantitative anchor and treated the zero accessory perturbations as a warning against inflating every cohesin-related gene, not as scale-matched nulls for an obligate SMC3 core edit.

The geometric midpoint of the two direct positive counts is near 30:

`exp((log1p(24) + log1p(37)) / 2) - 1 = 29.8`.

Because SMC3 is the shared SMC core partner and is expressed through most of the focal non-target nuclei, I placed the point slightly above that midpoint but still close to the observed `Smc1a`/`Stag2` compact-cohesin regime and far below broad `Ctcf` or proteostasis/chromatin responder counts. The resulting direct forecast is:

`predicted_n_degs = 32`.
