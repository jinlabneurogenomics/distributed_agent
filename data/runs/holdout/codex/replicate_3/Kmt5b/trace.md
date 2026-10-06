# Direct Kmt5b DEG-count forecast

Target: `Kmt5b`

Cell class: `151 TH Prkcd Grin2c Glut`

Endpoint: measured genes with BH-adjusted Wilcoxon `p < 0.05`

Point forecast: **22**

## Evidence used

The declared biology-only bundle supports a real but partial acute perturbation. In the focal non-target thalamic nuclei, `Kmt5b` is available and fairly broadly expressed: mean CP10K = 0.766, mean raw UMI = 1.20, and 15,633 of 23,679 nuclei express it, or 66.0%. The same bundle adjudicates the P16-to-P37/P44 lesion as likely substantially depleting functional stock by harvest: juvenile mouse PFC shRNA reduced KMT5B protein and H4K20me2 within 14-20 days, shorter than this experiment's 21-28 day interval.

The same evidence also limits the expected size of the response. KMT5B acts through an installed H4K20 methylation state on nucleosomes. New KMT5B supply should stop after a productive disruptive edit, but pre-edit marked histone H4 can persist on stable canonical nucleosomes, an H3.3-rich fraction turns over over weeks, and KMT5C/NSD2 provide plausible residual or overlapping H4K20 chemistry. That made a zero response less likely than for a low-expression or unsupported target, but argued against borrowing the full scale of broad transcription/chromatin outliers.

The Kmt5b corpus context had no Findings, Claims, or explicit report references, so no same-experiment packaged Kmt5b report was available. I therefore used the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` as the scalar training surface. This focal table has 1,674 observed training targets; it is sparse, with 1,205 zeros, a median of 0, a 75th percentile of 1, a 90th percentile of 2, a 95th percentile of 18, 59 targets at 50 or more, and 15 targets at 500 or more.

The relevant observed chromatin and histone-regulatory counts in the focal table were:

| target | n_degs |
| --- | ---: |
| Nsd2 | 0 |
| Kmt2c | 0 |
| Dnmt3a | 0 |
| Ep300 | 0 |
| Kat6a | 0 |
| Kat6b | 0 |
| Mbd5 | 0 |
| Ehmt1 | 4 |
| Crebbp | 8 |
| Setd5 | 9 |
| Mecp2 | 16 |
| Kdm5c | 18 |
| Setdb1 | 22 |
| Nsd1 | 23 |
| Kmt2a | 24 |
| Chd8 | 61 |
| Chd4 | 100 |
| Smarcc2 | 185 |
| Brd4 | 311 |
| Setd1a | 368 |
| Sin3a | 1433 |

The raw Parquet profiles for 25 selected chromatin candidates in `151 TH Prkcd Grin2c Glut` also showed a split rather than a single shared chromatin module: 8 had no significant genes, 6 had 1-9, 5 had 10-49, and 6 had at least 50. The cohort diagnostic had little significant-program overlap across most pairs, so I treated the profile comparison as evidence for the scale distribution of related perturbations rather than as a phenocopy module to average.

Same-experiment report text for visible comparators sharpened that split. `Dnmt3a` and `Ep300` were packaged as flat or essentially flat chromatin cases. `Ehmt1` was a very sparse H3K9 writer response. `Setdb1` was a sparse H3K9 writer response with its strongest coding-gene effect in this 151 class, and `Kmt2a` was sparse and glutamatergic-biased with 25 of 30 downstream FDR<0.10 genes in this class. `Chd8` and `Chd4` were real but mechanistically broader remodeler responses, while `Brd4`, `Setd1a`, and `Sin3a` were larger global-regulator outliers.

## Synthesis

I placed `Kmt5b` above the focal-table zero/near-zero mass because it is expressed in the focal population and its enzyme plus renewable H4K20me2 carrier pool should be materially perturbed within the harvest window. I placed it below the `Chd8`/`Chd4`/BAF/bromodomain/SIN3 tail because KMT5B's installed mark introduces a stable residual pool, because possible KMT5C/NSD2 chemistry leaves same-locus compensation unresolved, and because the training table shows many acute chromatin perturbations are buffered despite canonical developmental roles.

The closest scalar anchors were the modest histone-mark perturbations `Setdb1`, `Nsd1`, `Kmt2a`, and `Kdm5c`, whose focal counts sit at 18-24, with `Ehmt1` and `Crebbp` as lower positive chromatin bounds. I chose the low-20s rather than the exact training median for that anchor set to reflect the unusually good focal expression and the juvenile in-vivo evidence that KMT5B protein and H4K20me2 decline within the assay window.
