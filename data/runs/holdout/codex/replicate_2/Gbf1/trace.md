# Direct forecast for Gbf1

## Target and endpoint

- Target: `Gbf1`, the single gene in the declared one-row holdout manifest.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, defined as measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05`.
- The training count table has 1,674 focal-class perturbations and does not contain `Gbf1`.

## Evidence that determined the point

### Gbf1 biology bundle

The canonical `Gbf1` bundle supports a realized molecular perturbation: GBF1 is a cycling ARF guanine-nucleotide exchange factor at the cis-Golgi/ERGIC that initiates ARF-dependent COPI recruitment, and the functional-stock adjudication concluded that pre-edit GBF1 protein should be substantially depleted over the P16-to-P37/P44 window if editing is productive. The exact focal-population expression card also shows that `Gbf1` RNA is measurable in this class, with 20,134 of 23,679 non-target nuclei expressing the gene, or 85.03%.

That raises the prior above an unexpressed or persistent-stock target, but it does not by itself select a broad UPR, COPI-collapse, or proteostasis transcriptional state. The same card explicitly leaves postnatal thalamic requirement, compensation by related ARF-GEF pathways, and survivor conditioning unresolved.

### Matched training measurements

The focal count table is extremely sparse: 1,205/1,674 training perturbations are zero, the median is 0, the 75th percentile is 1, and the 90th percentile is 2. Large counts exist, but they are rare and therefore need direct support from a matched biological neighborhood rather than from the overall mean.

The closest measured early-secretory and Golgi-traffic perturbations in the focal class were flat or singleton-only:

| target | focal `n_degs` |
|---|---:|
| `Copa` | 0 |
| `Copg1` | 1 |
| `Sec23a` | 0 |
| `Sar1b` | 0 |
| `Stx5a` | 0 |
| `Stx16` | 1 |
| `Cog4` | 0 |
| `Cog5` | 0 |
| `Tfg` | 0 |
| `Trip11` | 0 |
| `Tmem165` | 0 |

Direct Parquet counts for the same focal group confirmed these values while retaining matched-cell context; for example, `Copa` had 75 matched perturbed nuclei and 0 FDR<0.05 genes, `Sec23a` had 307 and 0, `Stx5a` had 113 and 0, and `Copg1` had 234 with only the `Copg1` self-transcript significant. The same-experiment corpus summarized the same pattern in `Copa:F004`, `Copg1:F003`, `Sec23a:F003`, `Stx5a:F003`, and the Claim `claim:6a94b158a9de9a66a6c3`: represented ER-Golgi, COPI/COG/SNARE, and Golgi perturbations were repeatedly flat, singleton-only, or non-convergent rather than forming a shared broad secretory-pathway module in postmitotic neurons.

The focal assay was not globally insensitive. In the same `151 TH Prkcd Grin2c Glut` count table, `Gfpt1` had 311 DEGs, `Rab7` had 501, `Psmc1` had 430, and `Psmb4` had 742; milder ER/endosomal comparators such as `Hspa5`, `Sec63`, `Vps35`, and `Vps54` had 5, 11, 17, and 31. I treated those as stress or late-trafficking boundaries rather than point analogues for `Gbf1`, because the same-experiment COPI and early-secretory perturbations did not enter those broad states.

## Synthesis

`Gbf1` is plausibly hit within the experimental window and is upstream of COPI recruitment, so it is not a generic no-expression zero. The best task-matched quantitative evidence, however, is the measured COPI/ER-Golgi neighborhood, whose focal-class log-signature burden is essentially null despite adequate recovered-cell counts for several members and despite the screen's ability to detect ER, lysosomal, and proteostasis programs when those states are reached.

The point forecast therefore follows the direct early-secretory panel rather than the off-axis high-response stress perturbations. Because the only nonzero direct entries were isolated self-transcript singletons, and because self-transcript loss is not a reliable quantitative engagement readout in this assay, the rounded focal prediction is:

`predicted_n_degs = 0`
