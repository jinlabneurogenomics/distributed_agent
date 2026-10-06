# Direct DEG-count forecast for Ndufs1

## Target and endpoint

- Target manifest: `Ndufs1`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- The held-out target was absent from the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table.

## Target biology used

The declared Ndufs1 biology bundle makes NDUFS1 a nuclear-encoded 75-kDa core subunit in the N module of mitochondrial complex I. That favors a real loss-of-function prior: the protein sits in the electron-transfer path from NADH toward ubiquinone, the focal thalamic class directly expresses `Ndufs1`, and the card found no close paralog or subunit known to substitute for the NDUFS1 position.

The exact in-assay expression reach was substantial but not universal:

- `pct_cells_expressing = 70.1423`
- `mean_raw_umi = 1.4376`
- `pseudobulk_cpm = 90.1023`

The same bundle also argued against a large acute transcriptional program. P16 editing stops new NDUFS1 synthesis but does not poison complex I that was already assembled before editing, and the functional-stock conclusion was `partially_depleted_or_leading_edge` by P37-P44 with sparse timing evidence. I therefore treated realized complex-I loss as plausible within 21-28 days but likely diluted by residual installed complex, incomplete guide editing, and survivor-conditioned sampling.

## Training measurements used

The class-specific training count table had 1,674 perturbations. It was strongly zero-inflated:

- 1,205 / 1,674 targets had `n_degs = 0`.
- Median `n_degs = 0`.
- 90th percentile `n_degs = 2`.
- 95th percentile `n_degs = 18`.

I nominated training-available analogs from the curated mouse annotation store rather than by symbol prefix. The highest-specificity nominees were exact complex-I or paralog/complex partners, with exact CORUM, human-ortholog-projected CORUM, OXPHOS pathway, NADH dehydrogenase, and STRING physical evidence. The selected exact-complex cohort was internally coherent in the packaged same-experiment corpus: all 20 genes were represented, they formed one explicit-Finding-reference component, and 175 / 190 possible within-cohort pairs were connected.

Their observed same-class DEG burdens were the decisive quantitative evidence:

| comparator set | genes | `n_degs` |
| --- | --- | --- |
| closest NADH-dehydrogenase / N-module subunits present in training | Ndufs2, Ndufs8, Ndufs7, Ndufv1, Ndufv2 | 1, 1, 0, 0, 1 |
| other exact complex-I nominees in the leading cohort | Ndufs4, Ndufa10, Ndufb7, Ndufa6, Ndufa8, Ndufa4, Ndufb10, Ndufb8, Ndufa12, Ndufa9, Ndufb11, Ndufb9, Ndufb3, Ndufa11, Ndufc2 | 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1 |

Every exact complex-I nominee was therefore either 0 or 1 DEG in the count table. Adjacent respiratory-chain and assembly perturbations were also quiet in this class: `Ndufaf2 = 0`, `Ndufaf4 = 0`, `Ndufaf5 = 0`, `Uqcrb = 0`, `Uqcrfs1 = 0`, `Uqcrc2 = 1`, `Uqcrh = 0`, and `Uqcrq = 1`.

I also compared the exact complex-I cohort against the declared expression Parquet in the matched `151 TH Prkcd Grin2c Glut` context. All 20 profiles were present. The profile tool placed 9 profiles in `no_significant_features` and 11 in `1_to_9_significant_features`; at `pvals_adj < 0.05` there was no recurrent significant program among cohort pairs. Pairwise directionality showed a shared negative tail, with median negative-tail cosine contribution `0.7605`, but the corresponding top-tail overlap was shallow, median `0.12`, and the median significant-overlap coefficient was `0.0`. Thus the Parquet supported a weak, mostly subthreshold complex-I signature rather than a broad stress state.

## Synthesis

`Ndufs1` should not be projected to the high-DEG stress tail: the strongest task-matched respiratory-chain analogs all produced at most one significant gene in the focal thalamic class, despite being a dense complex-I cohort in the same experiment. The target-specific prior moves the forecast slightly above a hard null because Ndufs1 is expressed in about 70% of the assayed nuclei, occupies an irreplaceable core complex-I position, and should start losing newly supplied stock during the 21-28-day window. The stock card, however, leaves substantial residual installed complex plausible at harvest, which makes a large signature unlikely.

Balancing the analog mean near 0.5-0.6 DEGs with the expressed nonredundant target prior, I forecast **1** DEG.
