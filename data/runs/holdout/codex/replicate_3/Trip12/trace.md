# Trip12 direct DEG-count forecast

## Declared target and endpoint

- Target: `Trip12`, from the one-row declared manifest.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, defined as the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Declared observed training count table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Declared profile table: `[local file: training_de_all_cell_groups.parquet]`.

## Evidence used

### Trip12 biology bundle

The declared `Trip12` biology bundle reported exact focal-population expression: `Trip12` was detected in 23,379 of 23,679 non-target nuclei in `151 TH Prkcd Grin2c Glut` (`98.733%`; mean raw UMI 6.249; mean CP10k 3.942). This made target expression a positive reach signal, while the bundle explicitly warned that expression does not establish editing efficiency or dependence.

The same bundle adjudicated TRIP12 functional stock as `likely_substantially_depleted` by harvest. The key stock evidence was that TRIP12 is a HECT E3 ligase with ongoing catalytic activity and measured mouse-neuron protein half-lives of 25.733 and 29.106 hours; the P16-to-P37/P44 interval spans many such half-lives, so edited cells should clear most pre-existing ligase. The endpoint projection was weaker: the direct postnatal mouse-neural evidence was adult substantia-nigra Trip12 knockdown in an alpha-synuclein-PFF disease model over six months, and the card found no direct healthy acute postnatal mouse-neuron Trip12 loss series. The bundle also identified HUWE1 as a parallel E3 for some ubiquitin-fusion-degradation substrates, leaving partial buffering unresolved.

### Training count table

The focal count table contained 1,674 observed training perturbations and did not contain `Trip12`.

Its empirical distribution was sparse:

- 1,205/1,674 training perturbations had `n_degs = 0`.
- 469/1,674 were nonzero.
- The median was 0; the 75th percentile was 1.
- 132/1,674 had at least 5 DEGs, 106 had at least 10, 59 had at least 50, and 29 had at least 200.

The deterministic analogue nomination over the training universe found no exact complex or paralog candidate for `Trip12`; all 763 nominees were broad functional fallbacks. Among the training candidates sharing UPS/E3 annotations from KEGG `mmu04120` or GO ubiquitination terms, 55 were present; their median focal `n_degs` was 0, 21/55 were nonzero, and 6/55 had at least 10.

The closest HECT/E3 and E3-ligase comparators favored a very small count:

- `Huwe1`: 158 DEGs.
- `Marchf6`: 14.
- `Mib1`: 27.
- `Arih1`: 7.
- `Trim2`: 2.
- `Hectd4`, `Stub1`, `Fbxo11`, `Amfr`, `Fbxw7`: 1 each.
- `Ube3a`, `Hecw2`, `Herc1`, `Herc2`, `Ubr1`, `Ddb2`, `Rnf220`, `Ube2e2`: 0.

Thus the tight E3 cohort was centered near 0-1 DEG, with `Huwe1` a clear high-side outlier rather than the cohort center.

### Same-experiment corpus context

The same-experiment corpus supported treating `Huwe1` as an upper reference rather than a generic E3 donor. `Huwe1:F007` reported that the Huwe1 postmitotic signature was not a generic HECT/E3-ligase neurodevelopmental phenotype: `Ube3a`, `Hectd4`, `Herc2`, `Ubr1`, `Trp53`, `Myc`, and `Mycn` failed to reproduce the Huwe1 FDR-level module. `Ube3a:F003`, `Hectd4:F003`, and `Hecw2:F002` independently described the same family divergence: Huwe1 was readily transcriptionally visible, while Ube3a, Hectd4, Hecw2, Herc1, and Herc2 were flat or sparse in matched groups.

`Psmb4` and `Psmc1` were large proteasome-core controls in the focal count table, but `Psmb4:F008` reported that basal perturbation of accessory proteostasis and expected stress-regulator genes such as `Nfe2l1`, `Nfe2l2`, `Vcp`, `Atf6`, `Hspa5`, `Hspa8`, `Ube3a`, `Ube2e2`, `Usp48`, and `Sqstm1` did not reproduce the core `Psmb4` program. I therefore treated proteasome-core damage as an upper stress boundary, not a direct estimate for a substrate-selective E3 ligase.

### Parquet profile comparison

I computed a matched `151 TH Prkcd Grin2c Glut` profile comparison from the declared Parquet for 29 UPS/E3/proteostasis training perturbations. All requested profiles were present. In that bounded panel:

- 11/29 had no significant features.
- 11/29 had 1-9 significant features.
- 3/29 had 10-49 significant features.
- 4/29 had at least 50 significant features.

The direct HECT/E3 inspection confirmed that `Huwe1` had 158 DEGs in this group, while `Ube3a`, `Hecw2`, and `Herc2` had zero and `Hectd4` had one. The E3-only cohort was diffuse at the signed-profile level: across 153 available E3/E3 pairs the median positive top-tail overlap coefficient was 0.025 and the median negative coefficient was 0.03, with no recurrent significant-program overlap among most sparse nodes. HUWE1's focal RNA-processing and mitochondrial/redox features also did not recur at FDR level across the selected E3 peers.

## Synthesis

`Trip12` has strong focal-cell expression and its catalytic protein stock should be reachable within 21-28 days, so I did not use a zero-edit or zero-expression argument. However, the requested endpoint is survivor-conditioned nuclear RNA in healthy juvenile thalamic neurons, and the Trip12-specific biology only documents a substrate-level, post-translational E3 operation plus a long dopaminergic disease-model phenotype. It does not establish entry into the broad proteasome-failure state seen for `Psmb4`/`Psmc1`.

The measured training evidence put most comparable E3 perturbations at zero or one DEG. HUWE1 is the one HECT-family outlier, but the same-experiment corpus and the fresh Parquet comparison both showed that its 151-cell signature is target-specific and not shared by UBE3A/HECTD4/HECW2/HERC-family comparators. I therefore used HUWE1 only as proof that a HECT ligase can be visible under this screen, not as the magnitude anchor for Trip12.

Balancing high Trip12 reach and likely protein turnover against unresolved acute endpoint coupling and many quiet E3 comparators, I forecast an extremely sparse focal response: slightly above a hard null, but still in the 0-1-DEG regime that dominates nearby measured ligases.

Point prediction: `1`.
