# Cacna1c DEG-count prediction

## Question and resolved ambiguities

The requested held-out target list contains one perturbation, `Cacna1c`. I interpreted the endpoint exactly as the task defines it: in `151 TH Prkcd Grin2c Glut` nuclei, predict the count of measured gene rows, including the self row if it passes, with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05`.

That convention differs from several Distributed Agents corpus findings, which often summarize *downstream* genes at FDR < 0.10. I therefore used the corpus for same-experiment biological interpretation, but recalibrated all numeric counts against `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`: the direct training endpoint in the focal cell group.
- `[local file: training_de_all_cell_groups.parquet]`: per-gene Wilcoxon statistics, used for exact focal-cell FDR rows and top DE features of analog perturbations.
- `[local file: 026_Cacna1c.csv]`: the ordered target manifest.
- Distributed Agents same-experiment corpus `perturbai-july-260713-sourceguard-1773-v1`, especially:
  - `claim:4a61b7cf2bb3e0766552`, which states that `Cacna1g` is the selective thalamic CaV-family transcriptional exception rather than a generic response of voltage-gated calcium-channel pore or auxiliary-subunit perturbations.
  - `Cacna1d:F003`, a cross-perturbation finding noting that `Cacna1d`, the represented L-type pore comparator, was weak and divergent, with `Cacna1c/CaV1.2` named as the missing closest L-type paralog.
  - `Cacnb2:F003`, a CaV beta-subunit contrast showing that most represented CaV relatives were flat or singleton responders and that the only multi-gene calcium-channel response in this neighborhood was beta-independent `Cacna1g`.
  - `Cacna1g:F001`, the positive thalamic T-type-channel finding.
  - `Cacna1a:F003`, which bounded the result away from a shared P/Q-, R-, L-, alpha2delta-, beta-, or gamma-subunit CaV RNA module.
- Distributed Agents runtime profile tools: I compared the focal `151 TH Prkcd Grin2c Glut` log-fold-change vectors for `Cacna1a`, `Cacna1d`, `Cacna1e`, `Cacna1g`, `Cacna2d1`, `Cacna2d2`, `Cacnb2`, and `Cacnb4`, then inspected `profile_compare_cav.json`.
- External channel biology:
  - Catterall 2011, "Voltage-Gated Calcium Channels", DOI `10.1101/cshperspect.a003947`, for the CaV pore and auxiliary-subunit organization.
  - Dolmetsch et al. 2001, "Signaling to the Nucleus by an L-type Calcium Channel-Calmodulin Complex Through the MAP Kinase Pathway", DOI `10.1126/science.1063395`, for the CaV1/L-type excitation-transcription connection.
  - Striessnig, Ortner, and Pinggera 2015, "Pharmacology of L-type Calcium Channels: Novel Drugs for Old Targets?", DOI `10.2174/1874467208666150507105845`, for the relationship of CaV1.2/CACNA1C and CaV1.3/CACNA1D as L-type channels.

## Computation over the supplied data

I first read the requested manifest and confirmed that it contains only `Cacna1c`. In the focal-cell training counts, the endpoint was highly zero-inflated: 1,205 / 1,674 training targets had `n_degs = 0`, 363 had 1-9 DEGs, 63 had 10-99, and 43 had at least 100. The median was 0, the 95th percentile was 18, and the maximum was 2,677.

For exact analog evidence, I used Parquet row-group metadata to avoid scanning the whole 616M-row DE table. The focal cell group was contained in row groups 546-580; I streamed those row groups, retained rows with `group_name == "151 TH Prkcd Grin2c Glut"`, and then filtered to biologically selected CaV, calcium-homeostasis, NMDA-receptor, and synaptic-release comparators. For each comparator I counted `pvals_adj < 0.05`, matching the endpoint CSV.

The core focal counts were:

| target | focal `n_degs` | focal FDR < 0.05 pattern | relevance to `Cacna1c` |
|---|---:|---|---|
| `Cacna1d` | 0 | no significant row | Closest represented L-type pore paralog to CaV1.2; strongest direct same-family counterexample. |
| `Cacna1a` | 0 | no significant row | P/Q-type high-voltage pore; bounds generic high-voltage CaV pore loss. |
| `Cacna1e` | 0 | no significant row | R-type high-voltage pore; another high-voltage CaV null in the same focal group. |
| `Cacna1g` | 12 | `Ptprn`, `Cacna1g`, `Stmn4`, `Cpne7`, `Ly6e`, `Jun`, `Zdhhc22`, `Iyd`, `Lrrc7`, `Serpine2`, `Notum`, `Irag1` | Low-voltage T-type CaV3.1 positive control; a thalamic channel perturbation can be detected, but this response did not extend to L-type or high-voltage channels. |
| `Cacna2d1` | 1 | self row only | alpha2delta auxiliary-subunit singleton; not a downstream program. |
| `Cacna2d2` | 0 | no significant row | alpha2delta auxiliary-subunit null. |
| `Cacnb2` | 0 | no significant row | beta2 auxiliary subunit for high-voltage channels, including L-type channels; argues against a CaV beta/L-type basal transcriptomic module. |
| `Cacnb4` | 1 | self row only | beta4 singleton; no downstream CaV beta-module. |
| `Cacng2` | 0 | no significant row | AMPA-receptor TARP/gamma-family boundary. |
| `Cacng3` | 0 | no significant row | AMPA-receptor TARP/gamma-family boundary. |
| `Calm1` | 14 | self plus sparse Rasgrp2/Peg3-linked changes | Calmodulin-positive control but not an L-type-specific phenocopy. |
| `Calm3` | 1 | self row only | Calmodulin paralog singleton. |
| `Atp2a2` | 187 | broad UPR/ISR-like response including `Ddit3`, `Chac1`, `Xbp1`, `Herpud1`, `Hspa5`, `Asns` | Calcium-homeostasis counterexample: broad in the same group, but ER SERCA2 stress, not plasma-membrane CaV1.2 loss. |
| `Atp2b2` | 1 | self row only | Plasma-membrane calcium pump singleton. |
| `Itpr1` | 0 | no significant row | ER calcium-release-channel null. |
| `Ryr2` | 0 | no significant row | ER calcium-release-channel null. |
| `Ryr3` | 0 | no significant row | ER calcium-release-channel null. |
| `Ppp3r1` | 9 | sparse calcineurin-regulatory response | Broader Ca2+/calmodulin branch, small and not a CaV phenocopy. |
| `Ppp3ca` | 4 | sparse calcineurin-catalytic response | Broader Ca2+/calmodulin branch, small and not a CaV phenocopy. |
| `Grin1` | 89 | clear NMDAR response | Ion-channel positive control showing receptor/channel perturbations can be visible. |
| `Grin2b` | 2 | self plus `Pianp` | NMDAR subunit-selectivity boundary. |
| `Grin2d` | 0 | no significant row | NMDAR subunit-selectivity boundary. |

The runtime profile comparison over the eight CaV pore/auxiliary comparators classified five as `no_significant_features`, two as `1_to_9_significant_features`, and only `Cacna1g` as `10_to_49_significant_features`. Its whole-vector log-fold-change correlations were not useful mechanistic evidence because the strongest pair feature examples were FDR = 1.0, low-expression tail artifacts shared by many null signatures; I therefore used the exact FDR counts and corpus-curated CaV contrasts rather than treating those raw logFC correlations as phenocopies.

## Target-specific reasoning

`Cacna1c` encodes CaV1.2, an L-type high-voltage calcium-channel pore-forming subunit. As an alpha1 CaV1 pore, the natural in-dataset comparators are first `Cacna1d`, the other represented L-type pore, then high-voltage pore genes `Cacna1a` and `Cacna1e`, and then high-voltage auxiliary beta and alpha2delta subunits `Cacnb2`, `Cacnb4`, `Cacna2d1`, and `Cacna2d2`.

The closest same-experiment evidence points to no focal FDR-significant genes. `Cacna1d` had `n_degs = 0` in `151 TH Prkcd Grin2c Glut`; the Distributed Agents `Cacna1d:F003` finding further reports that its rare effects elsewhere were single-gene and cell-group-restricted rather than a CaV1 activity-dependent program. `Cacnb2`, the beta subunit most associated with high-voltage CaV1/CaV2 channels, also had `n_degs = 0`, and its corpus finding explicitly notes that the expected CaV beta2/L-type excitation-transcription arm was absent. The other high-voltage pore comparators were equally flat in this focal group: `Cacna1a = 0` and `Cacna1e = 0`.

The main positive CaV counterexample was `Cacna1g` with 12 focal DEGs at FDR < 0.05. I did not transfer that count upward to `Cacna1c` because `Cacna1g` is a beta-independent, low-voltage T-type CaV3.1 pore with thalamic burst-firing biology, and Distributed Agents claim `claim:4a61b7cf2bb3e0766552` specifically synthesizes the same-experiment result as "Cacna1g is the reproducible multi-gene thalamic exception against a background of flat, singleton, divergent, or non-phenocopy calcium-channel relatives." `Cacna1c` is closer to the flat L-type/HVA side of that contrast than to the T-type `Cacna1g` exception.

I also treated larger calcium-stress responses as counterexamples rather than positive analogs. `Atp2a2` produced 187 DEGs in this focal group through an ER-stress/ISR program; `Atp2b2`, `Itpr1`, `Ryr2`, `Ryr3`, and `Fkbp1a` were 0- or 1-DEG responses. That branch says Ca2+ handling genes can be transcribed when the perturbation elicits ER stress, but it does not supply an L-type plasma-membrane channel analog.

External biology leaves a plausible route to a nonzero `Cacna1c` effect: CaV1.2 L-type channels can couple depolarization to MAPK/CREB-dependent transcription through local calmodulin signaling. However, this screen measured basal nuclear RNA 3-4 weeks after sparse P16 coding loss of function, not evoked depolarization, Ca2+ currents, CREB phosphorylation, or pharmacologic L-type blockade. Within that modality, the represented L-type comparator and the CaV beta2 branch were silent at FDR < 0.05. I therefore put `Cacna1c` in the zero class and chose the point estimate `0`.

## Limits

There is no direct `Cacna1c` signature or Distributed Agents target report in the exposed training corpus; this is a held-out extrapolation from neighboring CaV perturbations. The closest L-type paralog, `Cacna1d`, is informative but not interchangeable with CaV1.2, and L-type excitation-transcription coupling might have appeared under a stimulated electrophysiology or activity-regulated immediate-early-gene assay. The endpoint is also thresholded and power-dependent, so a target at the boundary between "no response" and "self-only/singleton" could toggle between 0 and 1 DEGs. The training data nevertheless put the mechanistically closest comparators on the flat side of the empirical distribution, so the final call is `Cacna1c = 0`.
