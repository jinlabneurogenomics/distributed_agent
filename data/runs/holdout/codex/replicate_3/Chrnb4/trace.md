# Chrnb4 direct n_degs forecast

## Declared target and endpoint

- Target: `Chrnb4`.
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `p < 0.05` in `151 TH Prkcd Grin2c Glut`.
- Training count table: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, 1674 training perturbations.
- Target biology source: canonical `Chrnb4` biology bundle, served with `target_outcome_exposed=false` and `labeled_neighbors_exposed=false`.

## Evidence used

### Chrnb4 biology and focal expression

The prediction-safe Chrnb4 bundle supports a real loss-of-function intervention: beta4 is a component of assembled beta4-containing nicotinic acetylcholine receptor channels, and a P16 edit should stop new beta4 production; existing receptor stock persists initially but is expected to decline substantially over the 21-28 day experiment.

The same bundle also makes the matched expression reach very small in the requested class. In non-target `151 TH Prkcd Grin2c Glut` nuclei, Chrnb4 was detected in 42 of 23,679 cells, with mean raw UMI 0.001900, mean CP10K 0.001288, and 45 total Chrnb4 UMIs. The external expression facts in the card point to strongest beta4/alpha3 expression in ventral medial habenula rather than broad thalamic coverage, so the exact in-assay expression reach is the most relevant scope evidence.

### Training nAChR and cholinergic perturbations

The focal count table is capable of large responses but is sparse overall:

- 1205 of 1674 training perturbations had `n_degs = 0`.
- 469 had at least one DEG.
- 106 had at least 10 DEGs.
- 43 had at least 100 DEGs.
- The maximum was 2677.

The cholinergic receptor neighborhood was nearly flat in the same endpoint:

| perturbation | `151 TH Prkcd Grin2c Glut` n_degs |
| --- | ---: |
| `Ache` | 1 |
| `Chrm2` | 0 |
| `Chrm3` | 0 |
| `Chrna1` | 0 |
| `Chrna2` | 0 |
| `Chrna3` | 0 |
| `Chrna4` | 2 |
| `Chrna6` | 0 |
| `Chrna7` | 0 |
| `Chrnb1` | 0 |
| `Chrnb2` | 1 |
| `Chrnb3` | 0 |
| `Chrnd` | 0 |
| `Chrne` | 0 |
| `Chrng` | 0 |

The closest represented biology is not an exact Chrnb4 donor, because Chrnb4 and Chrna5 were absent from the training Parquet. The most useful analogs were therefore `Chrna3`, the alpha subunit that co-occurs with beta4 in alpha3beta4-star receptors; `Chrnb2`, the other neuronal beta nAChR subunit in the training set; `Chrna4`, because it forms a well known alpha4beta2 receptor with Chrnb2; and `Ache` plus the other represented nAChR/mAChR receptors as pathway controls.

Packaged same-experiment Findings supported using these as a near-null boundary rather than a positive module:

- `Chrna3:F003`: represented nicotinic receptor family perturbations and `Ache` did not converge on a Chrna3-like transcriptional response; the report explicitly noted that the closest alpha3 partners `Chrnb4` and `Chrna5` were not testable in the training Parquet.
- `Chrnb2:F002`: literature-obvious nAChR relatives did not converge with Chrnb2; `Chrna3`, `Chrna6`, `Chrna7`, and `Chrnb3` were flat, while `Chrna2` and `Chrna4` had only isolated one-gene hits, and every shared-direction overlap with Chrnb2 was zero.
- `Chrna4:F003`: Chrnb2 and the represented nicotinic relatives did not phenocopy the isolated Chrna4 thalamic response.
- `Ache:F003`: fourteen represented nicotinic or muscarinic receptor perturbations produced only seven total FDR<0.10 downstream hits across 294 target-by-group tests.

I also generated a matched focal-cell profile comparison for `Ache`, `Chrm2`, `Chrm3`, `Chrna2`, `Chrna3`, `Chrna4`, `Chrna6`, `Chrna7`, `Chrnb2`, and `Chrnb3` from `training_de_all_cell_groups.parquet`.

- 7 of 10 compared cholinergic/nAChR nodes had no significant features at FDR<0.05 in `151 TH Prkcd Grin2c Glut`.
- The only nonzero members had 1 to 2 significant features.
- Across inspected `Chrna3`, `Chrnb2`, `Chrna4`, `Ache`, and `Chrna2` pairs against the other five receptor peers, significant-feature intersections were uniformly zero.

## Synthesis

Chrnb4 is biologically functional, but the requested aggregate class contains very little Chrnb4 RNA. A single nAChR subunit edit is therefore expected to affect only a tiny expressing subset of recovered nuclei, and related channel or cholinergic perturbations show that this receptor family can be electrophysiologically meaningful without producing a basal survivor-state mRNA program in this screen. The direct alpha3 and beta2 receptor comparators are exact focal-cell near-nulls, and the one weak `Chrna4` response was not reproduced by `Chrnb2` or by the rest of the nicotinic family.

Those observations make a large Chrnb4 count implausible and make even a small singleton response less likely than no recovered BH-significant genes. I therefore predict:

`predicted_n_degs = 0`
