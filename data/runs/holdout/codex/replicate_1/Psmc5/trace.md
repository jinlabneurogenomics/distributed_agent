# Psmc5 direct n_degs forecast

## Declared target and endpoint

- Manifest target: `Psmc5` from `Psmc5.csv`.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the held-out `Psmc5` perturbation.
- Target outcome exclusion: the `Psmc5` target signature and target DEG count were not used.

## Biology-only target evidence

The canonical `Psmc5` biology bundle identifies PSMC5/Rpt6 as a 19S-base AAA ATPase in the heterohexameric 26S proteasome ATPase ring. Its exact focal expression reach is high in the relevant non-target nuclei: mean CP10K = 1.641, pseudobulk CPM = 165.690, and 20,831 of 23,679 non-target nuclei expressed the feature, or 87.97%.

The functional-stock card calls the P16-to-P37/P44 window long enough for a major PSMC5-dependent defect. Existing assembled proteasomes can buffer an acute lesion for about a week, but sustained neuronal Psmc5 knockdown caused marked target loss plus ubiquitin accumulation by day 14 in rat hippocampal neurons. The card therefore concludes that editing is likely to substantially deplete operative PSMC5-dependent stock by the 21-28 day harvest, with species, region, and siRNA-to-CRISPR uncertainty.

## Training measurements used

The declared focal count table contains 1,674 non-held-out training targets. It is sparse overall: median `n_degs` = 0, the 95th percentile is 18, the 99th percentile is 430, and only 59 targets have at least 50 DEGs.

The most direct training anchors are the only other assayed constitutive 26S proteasome subunits visible in the focal count table:

| target | focal n_degs | up | down | n_pert_matched | n_ctrl_matched |
| --- | ---: | ---: | ---: | ---: | ---: |
| `Psmc1` | 430 | 231 | 199 | 89 | 23679 |
| `Psmb4` | 742 | 357 | 385 | 62 | 23679 |

Both are extreme relative to the 1,674-target distribution: `Psmb4` is the 7th largest focal burden and `Psmc1` is the 18th largest. A few protein-homeostasis perturbations were large but less direct (`Uba5` 2,677; `Ufc1` 572), while several related autophagy/ubiquitin nodes were tiny or absent (`Usp48` 10, `Arih1` 7, `Vcp` 2, `Sqstm1` 1, `Uchl1` 1, `Atg5` 0, `Atg16l1` 0).

Exact parquet inspection in `151 TH Prkcd Grin2c Glut` found that the `Psmc1` and `Psmb4` FDR < 0.05 sets overlap on 215 genes and all 215 are in the same direction. A profile comparison over the selected proteostasis training cohort gave the direct `Psmc1`-`Psmb4` pair Pearson = 0.611, Spearman = 0.431, cosine = 0.671, positive significant overlap 88 genes, negative significant overlap 127 genes, and 0 significant direction conflicts.

## Same-experiment corpus checks

The corpus Findings for the two structural anchors support using `Psmc1` and `Psmb4` as direct 26S-failure scale anchors rather than treating every proteostasis-related target as equivalent.

- `Psmc1:F007`, release `perturbai-july-260713-sourceguard-1773-v1`, source-record SHA256 `76fe0a30289f724499f8429af4d333816a40b69fdaa7f03238de28aa54ab6fa8`: `Psmb4` was the single strong positive `Psmc1` signature neighbor, consistent with convergence between 19S ATPase and 20S beta-core lesions.
- `Psmb4:F007`, source-record SHA256 `2c1868f3f2f5a67b13399c0d6b8075f7db4141d5918ddf72411f8143c956a6b6`: across the same-experiment report universe, `Psmc1` was the top `Psmb4` neighbor and the 20S/19S signatures agreed in sign for 5,107 of 5,113 shared FDR < 0.10 features.
- `Psmc1:F008`, source-record SHA256 `aff131527337d11adb6bdea9c1518944918c484d0c5e5201fbaa62e732dd5811`, and `Psmb4:F008`, source-record SHA256 `164524acd27d2ac87f54372666072bd0df0e5bc369b62c99683498e757613be4`: accessory proteostasis or stress-sensor perturbations such as `Nfe2l1`, `Vcp`, `Uchl1`, `Uba5`, `Usp48`, `Sqstm1`, and heat-shock or ER-stress genes did not reproduce the direct core-proteasome programs.

## Forecast

`Psmc5` is a core 19S ATPase like `Psmc1`, not an upstream stress regulator or an accessory branch component, and the focal target transcript is broadly present. That places the target in the same high-response structural-proteasome bracket as `Psmc1` and `Psmb4`. I did not use the larger `Uba5` count as a numeric anchor because `Uba5` is UFMylation, not the 26S proteasome, and the corpus/profile evidence shows that broad proteostasis relatives need not phenocopy direct 26S damage.

The point estimate is set near the geometric middle of the two direct structural anchors, with a slight pull toward the lower 19S ATPase anchor because PSMC5 has an installed assembled-proteasome pool that can buffer immediate loss:

```
geometric mean of Psmc1 and Psmb4 counts = exp((log1p(430) + log1p(742)) / 2) - 1 = 566
final point after mild downward rounding = 560
```

Predicted `n_degs`: **560**
