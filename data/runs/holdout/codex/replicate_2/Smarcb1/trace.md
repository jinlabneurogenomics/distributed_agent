# Direct forecast trace

## Target and endpoint

- Target: `Smarcb1`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

The focal target was absent from the declared focal count table and from the held-out-redacted all-cell Parquet. The forecast below uses the declared biology-only `Smarcb1` bundle, the focal training count table, curated SWI/SNF membership used only to choose comparator perturbations, and signed training profiles in the declared Parquet.

## Biology used for the target

The canonical biology bundle characterizes SMARCB1 as a renewable core subunit of mammalian SWI/SNF or BAF chromatin-remodeling complexes. The same bundle adjudicates functional SMARCB1 stock as likely to be substantially depleted by the 21-28 day P16-to-P37/P44 interval: disruptive editing should stop new protein supply, thalamic proteomes turn over over this time scale, and inducible Smarcb1 knockdown produces a gradual decline of SMARCB1 protein. This supports a real molecular perturbation by harvest rather than a stock that should mostly persist.

The in-assay expression reach is adequate but not complete: `Smarcb1` is detected in 15,357 of 23,679 matched non-target nuclei in the focal class, or 64.85%, with mean CP10K 0.718. This makes a thalamic survivor-state signature plausible, but it also leaves population dilution because the aggregate includes a target-negative minority.

Two biological caveats kept the estimate out of the `Smarcc2`-scale range. First, the direct neural loss evidence in the bundle is developmental cerebellar precursor deletion, not P16 editing of postmitotic thalamic neurons. Second, inducible Smarcb1 knockdown can leave residual SMARCA4-SMARCC1 core association, so the BAF machine is perturbed at a unique core position but not necessarily collapsed in the same way as the strongest measured scaffold-like training perturbation.

## Training evidence used

The focal training count table has 1,674 perturbations. It is sparse and highly skewed:

- median `n_degs`: 0
- zeros: 1,205 / 1,674
- mean: 14.05
- 95th percentile: 18
- 99th percentile: 436

Curated Reactome SWI/SNF chromatin remodeler membership contains these measured training perturbations in the focal count table after removing held-out `Smarcb1`:

| target | 151 TH `n_degs` |
|---|---:|
| Actg1 | 1 |
| Arid1a | 22 |
| Arid1b | 1 |
| Bcl11a | 0 |
| Bcl11b | 0 |
| Bicra | 0 |
| Smarca2 | 1 |
| Smarca4 | 0 |
| Smarcc1 | 0 |
| Smarcc2 | 185 |
| Smarcd1 | 1 |
| Smarce1 | 11 |

Thus the best mechanistic family is not uniformly active in this assay. The strongest member, `Smarcc2`, is a focal-class outlier for the family and sits at the 98.15th percentile of all training counts, while `Smarce1` and `Arid1a` give low-tens response scales at the 94.09th and 95.70th percentiles. The ATPases and the related SMARCC scaffold paralog are quiet in the exact class, so I discounted a direct transfer of the 185-gene `Smarcc2` count to `Smarcb1`.

The all-cell Parquet confirmed that the nontrivial SWI/SNF-family responses are concentrated in the requested class:

- `Smarcc2`: 185 DEGs in `151 TH Prkcd Grin2c Glut`; only singletons in three other classes.
- `Arid1a`: 22 DEGs in `151 TH Prkcd Grin2c Glut`; none elsewhere.
- `Smarce1`: 11 DEGs in `151 TH Prkcd Grin2c Glut`; none elsewhere.

Signed profile comparison among the 12 measured SWI/SNF training members showed partial concordance among the three nontrivial responses. `Smarcc2` and `Arid1a` shared 11 negative and 2 positive significant genes in the focal class, and `Smarcc2` and `Smarce1` shared 9 negative significant genes with no direction conflicts. The leading significant genes for `Smarcc2`, `Arid1a`, and `Smarce1` also recurred in the same focal negative program, including `Ptpn3` and `Begain`, with `Prkcd` also significant for `Smarcc2` and `Smarce1`. This supports using the low-tens BAF response as relevant rather than treating `Arid1a` and `Smarce1` as unrelated small effects.

At the same time, the profile topology did not make `Smarcc2` a clean magnitude donor. `Smarcc2`'s whole-profile nearest edges inside the supplied SWI/SNF cohort included quiet members such as `Actg1`, `Bcl11a`, `Smarca4`, and `Smarcc1`, and the cohort's leading positive features were mostly not shared across SWI/SNF peers. I therefore treated `Smarcc2` as evidence that BAF loss can reach a large focal response, not as an expected `Smarcb1` count.

## Numeric synthesis

`Smarcb1` has stronger realization and paralog evidence than many quiet family members, so zero or one DEG looked too low. Its closest low-count role analogues, however, were `Smarce1` at 11 and `Arid1a` at 22, with `Smarcc2` at 185 retained only as an upper, partially shared-state comparator. The resulting point estimate is a low-tens value near the high end of the global 95th-percentile region, but still far below the single `Smarcc2` outlier:

`predicted_n_degs = 18`
