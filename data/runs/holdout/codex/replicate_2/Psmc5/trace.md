# Direct forecast trace

## Target and endpoint

- Held-out manifest target: `Psmc5`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

The declared focal training table contains 1,674 perturbations; `Psmc5` is absent. Its count distribution is extremely sparse overall, with median 0 and mean 14.1, but the right tail contains direct proteasome subunit observations: only 29/1,674 training targets have at least 200 DEGs in this cell group, and both available proteasome subunit perturbations are in that tail.

## Psmc5 biology

The declared Psmc5 biology bundle identifies PSMC5/Rpt6 as a distinct AAA ATPase in the 19S base of the 26S proteasome, one of the six non-interchangeable PSMC ATPases in the substrate-unfolding/translocation ring. Exact in-assay reach is high in the focal non-target population: Psmc5 RNA was detected in 20,831/23,679 nuclei, 87.97% expressing, with pseudobulk CPM 165.69.

The functional-stock card treats Psmc5 loss as likely realized within the P16-to-P37/P44 assay window: new intact Rpt6 supply should stop after editing; pre-existing 26S proteasomes can buffer early loss, with rat CA1 retaining bulk proteasome activity at day 7 after Psmc5 knockdown; sustained neuronal knockdown nevertheless reduced PSMC5 to about 13% of control and accumulated ubiquitinated protein by day 14. Thus I used direct 26S-subunit knockouts as the main scale anchors but kept the forecast below the stronger 20S-core perturbation to allow for installed-complex buffering and Psmc5-specific uncertainty.

## Training evidence used

From the `151 TH Prkcd Grin2c Glut` training count table:

| target | focal `n_degs` |
| --- | ---: |
| `Psmc1` | 430 |
| `Psmb4` | 742 |

The Parquet reproduces those focal counts at `pvals_adj < 0.05`:

| target | DEGs | up | down | matched perturbed nuclei |
| --- | ---: | ---: | ---: | ---: |
| `Psmc1` | 430 | 231 | 199 | 89 |
| `Psmb4` | 742 | 357 | 385 | 62 |

Those two responses also share 215 significant focal genes, all in the same direction, with log-fold-change correlation 0.987 across the shared significant set. A focal profile-neighborhood scan over all 1,674 training targets recovered the same relationship from the positive stress arm: `Psmb4` was the top positive-tail neighbor of `Psmc1`, and `Psmc1` was the top positive-tail neighbor of `Psmb4`, sharing 124 of their top 400 positive features.

The same-experiment Findings place both perturbations in the same state: direct proteasome damage induces proteasome bounce-back, heat-shock/ISR, autophagy/lysosome, redox and p53/apoptosis-risk arms plus synaptic/neuronal-function down-regulation. I treated accessory or upstream proteostasis perturbations as non-scale-matched boundaries, because the count table and packaged comparisons both show that basal loss of `Nfe2l1`, `Vcp`, `Hsf1`, `Hspa5`, `Hspa8`, `Nfe2l2`, `Atf6`, and ubiquitin-pathway regulators generally did not phenocopy the core proteasome-subunit program in this assay.

## Point synthesis

`Psmc5` is closer in operation to `Psmc1` than to `Psmb4`: both PSMC5 and PSMC1 are 19S AAA ATPase-ring subunits, whereas PSMB4 is a 20S core beta subunit whose observed program was larger. The high focal Psmc5 expression and the 21-28 day window argue against shrinking to the all-target background; the day-7 persistence of installed proteasome activity and the absence of a same-subunit Psmc5 observation argue against simply copying the 742-gene `Psmb4` count.

I therefore placed the point in the upper part of the direct 19S-to-20S bracket, closer to `Psmc1` than an equal arithmetic average:

```
Psmc1 = 430
Psmb4 = 742
forecast = 520
```

This is a biology-weighted interpolation among direct 26S-subunit responses in the same focal cell class; it does not use the withheld `Psmc5` expression signature or target count.
