# DEG-count prediction trace

## Question and resolved ambiguities

The held-out manifest for this run contains one requested perturbation, `Kcnab1`. I interpreted the task as asking for a point prediction for the number of measured genes in `151 TH Prkcd Grin2c Glut` cells with BH-adjusted Wilcoxon `pvals_adj < 0.05` after acute AAV-CRISPR loss of `Kcnab1`. The count is assay-specific and includes the perturbed transcript itself if that row passes the FDR cutoff; it is not a count of only downstream genes.

`Kcnab1` is absent from both supplied training tables, so the prediction below is transfer from non-held-out perturbations. I used the same requested-target spelling and preserved the manifest order in `answer.txt`.

## Sources used

* `training_de_all_cell_groups.parquet`: per-gene Wilcoxon statistics. I filtered it to the focal group and to biologically nominated channel/Kv-complex perturbations, then recomputed `sum(pvals_adj < 0.05)` as a consistency check against the training count CSV.
* `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: the observed endpoint for visible training perturbations.
* `117_Kcnab1.csv`: the held-out target list.
* Distributed Agents selected same-experiment corpus `perturbai-july-260713-sourceguard-1773-v1`: I queried `Kcnab2`, `Kcna1`, and `Kcna2` Findings/Claims and candidate-set topology. `Kcnab1` itself was absent as a corpus target, which is consistent with it being held out here.
* Distributed Agents gene-annotation and gene-analog stores: GO, Reactome, WikiPathways/MSigDB, native/projected CORUM, and pinned STRING v12.0 physical-network relationships over the closed mouse gene universe. The analog nomination record placed `Kcnab2` first for `Kcnab1` and nominated the visible voltage-gated potassium-channel genes as the leading narrow-module comparison set.
* NCBI Gene/PubMed plus STRING API for external biological checks. NCBI Gene ID 16497 describes mouse `Kcnab1` as "potassium voltage-gated channel, shaker-related subfamily, beta member 1" with synonyms including `Kvbeta1.1`. Wissmann et al. 1999 showed that the Kvbeta1.1 N terminus can confer fast N-type inactivation on Kv1.1 channels, DOI `10.1074/jbc.274.50.35521`, PMID `10585425`. Swain et al. 2015 showed Ca2+/calmodulin regulation of Kvbeta1.1-mediated inactivation of Kv channels, DOI `10.1038/srep15509`, PMID `26487174`.

## Computational steps

I first verified that the manifest contains only `Kcnab1`, then summarized the training endpoint. The focal count table has 1,674 perturbations, a median of 0 DEGs, 1,205 zeros, and a very long right tail, so a one-gene response is already near the floor of this assay.

I used the curated analog nomination for `Kcnab1` to avoid choosing genes purely by symbol prefix. The strongest relevant available candidates were `Kcnab2` and the voltage-gated potassium-channel Reactome module members, especially `Kcna1`, `Kcna2`, `Kcnb1`, `Kcnb2`, `Kcnc1`, `Kcnq1`, `Kcnq2`, `Kcnc2`, `Kcnc3`, and `Kcnh5`. I then filtered the parquet in the focal group for these candidates and counted FDR-significant rows.

The focal DEG counts for the main channel comparators were:

| training perturbation | focal `n_degs` | focal expression evidence |
| --- | ---: | --- |
| `Kcnab2` | 1 | the only FDR row was self, `Kcnab2` log2FC = -0.744, score = -8.73, q = 4.38e-14; the next two genes had q = 0.302 |
| `Kcna1` | 0 | no FDR rows; best q = 0.357 |
| `Kcna2` | 0 | no FDR rows; all q = 1.0 in this group |
| `Kcnb1` | 0 | no FDR rows; all q = 1.0 in this group |
| `Kcnb2` | 0 | no FDR rows |
| `Kcnc1` | 0 | no FDR rows; best q = 0.582 |
| `Kcnc2` | 1 | the one FDR row was self, `Kcnc2` q = 4.65e-5 |
| `Kcnc3` | 1 | the one FDR row was self, `Kcnc3` q = 6.16e-7 |
| `Kcnd3` | 0 | no FDR rows; best q = 0.0905 |
| `Kcnq2` | 1 | the one FDR row was self, `Kcnq2` q = 2.12e-28 |
| `Kcnq3` | 1 | the one FDR row was self, `Kcnq3` q = 0.00717 |

I also compared the signed Wilcoxon-score profiles for ten channel candidates with the Distributed Agents runtime profile tool in the same focal group. `Kcnab2`, `Kcna1`, and `Kcna2` did not show a coherent hidden program: Pearson correlations were 0.041 for `Kcnab2`/`Kcna1`, 0.026 for `Kcnab2`/`Kcna2`, and -0.005 for `Kcna1`/`Kcna2`, with zero shared FDR-significant features. `Kcnq2`/`Kcnq3` were also weakly related in the expression readout despite being a direct channel pair, with Pearson 0.041. This supports using the count floor of these perturbations rather than averaging a shared multigene profile.

The selected Distributed Agents corpus agrees with this quantitative readout. Its `Kcnab2:F004` Finding states that the represented Kv1 alpha-subunit perturbations `Kcna1` and `Kcna2` were as transcriptionally flat as `Kcnab2`, and that broader potassium-channelopathy genes `Kcnb1` and `Kcnq2` produced only sparse, non-overlapping downstream hits; it explicitly lists `Kcnab1`/`Kcnab3` as expected but absent comparators. Two higher-order Claims summarize the same pattern: represented voltage-gated potassium-channel/Kv-complex perturbations do not yield a robust shared neuronal nuclear mRNA program, and Kv1/CASPR/paranodal structural relationships do not translate into a shared basal mRNA response in this screen.

## Target-specific reasoning

### Kcnab1

`Kcnab1` encodes the Kv beta 1 auxiliary subunit. Its closest visible perturbation in the deterministic Distributed Agents analog nominations was `Kcnab2`, another cytosolic Kv beta subunit in the Reactome mouse voltage-gated potassium-channel pathway. Both genes are annotated to potassium channel regulator activity and the voltage-gated potassium-channel complex; `Kcnab1` itself is in Reactome `R-MMU-1296072` / "Voltage gated Potassium channels" and `R-MMU-1296071` / "Potassium Channels". External channel biology also points to an electrophysiological role: the Kvbeta1.1 N terminus mediates fast N-type inactivation of Kv1 channels (Wissmann et al. 1999, PMID `10585425`), and the same beta-subunit mechanism can be modulated by Ca2+/calmodulin (Swain et al. 2015, PMID `26487174`).

The appropriate training analogs argue for almost no nuclear mRNA response. In `151 TH Prkcd Grin2c Glut` cells, `Kcnab2` had exactly one significant row and that row was the on-target `Kcnab2` transcript. The direct Kv1 alpha subunits `Kcna1` and `Kcna2`, which are mechanistically closer than generic ion channels, had 0 focal DEGs. The same floor-level behavior extended to more distant voltage-gated K+ channels: `Kcnb1 = 0`, `Kcnb2 = 0`, `Kcnc1 = 0`, `Kcnd3 = 0`, `Kcnq2 = 1`, and `Kcnq3 = 1`. The 1-count cases were mostly self-transcript detections rather than downstream activity-response signatures.

I therefore predict no secondary transcriptional program for `Kcnab1`. I nevertheless predict a count of 1 rather than 0 because the single nearest Kv beta training analog, `Kcnab2`, crossed FDR only through self-RNA loss, and `Kcnab1` is itself a measured gene in the focal group. The point estimate is a target-transcript call, not a claim that Kvbeta1 loss should induce an activity-regulated `Fos`/`Junb`/`Egr1`/`Npas4` state.

## Limits and uncertainty

The main weakness is that `Kcnab1` was fully held out: there is no observed `Kcnab1` perturbation vector in the parquet, and the Distributed Agents same-experiment corpus has no `Kcnab1` target card to inspect. `Kcnab2` is the best beta-subunit analog in training, but Kv beta isoforms have distinct N termini and channel effects, and projected CORUM KCNAB1 complexes primarily involve KCNA5/RACK1 rather than a mouse complex measured directly in this focal population.

The predicted nonzero count also depends on whether the CRISPR guides generated enough `Kcnab1` mRNA depletion in `151 TH Prkcd Grin2c Glut` nuclei to survive 17k-gene multiple testing. The analogs show that many channel perturbations with true electrical functions were 0 or 1 in this endpoint, so a realized `Kcnab1` value of 0 would be unsurprising. What I do not see is evidence for a value much above 1: visible Kv beta, Kv1, Kv2, Kv3, and KCNQ perturbations lack shared downstream DEGs at FDR 0.05, and the primary biology of `Kcnab1` is channel gating/localization rather than a transcription-factor-like nuclear regulatory role.
