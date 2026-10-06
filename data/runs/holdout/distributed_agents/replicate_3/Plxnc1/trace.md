# Plxnc1 DEG-count prediction trace

## Question and interpretation

The requested held-out target file contains one perturbation:

| target_name |
|---|
| Plxnc1 |

The task is to predict the `n_degs` endpoint for loss of `Plxnc1` in `151 TH Prkcd Grin2c Glut` cells. I interpreted `n_degs` literally as the count of measured genes, including the perturbed gene's own transcript when it is measured, with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` in this one focal cell group.

`Plxnc1` was held out as a perturbation target. It was therefore not used as a training `gene_target`, but `Plxnc1` itself remains a measured transcript in the focal profiles of held-in perturbations.

## Sources used

- `[local file: training_de_all_cell_groups.parquet]`
  - Used for focal-cell Wilcoxon scores, adjusted p-values, log2 fold changes, and matched perturbed/control nucleus counts for held-in perturbations.
- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  - Used for the exact focal endpoint, `n_degs`, for all 1,674 held-in training targets.
- `[local file: 179_Plxnc1.csv]`
  - Used for the requested held-out target and row order.
- Distributed Agents same-experiment semantic corpus, release `perturbai-july-260713-sourceguard-1773-v1`
  - `Plxnc1` itself had no curated corpus report in this release.
  - Corpus reports for held-in `Plxna1`, `Plxna2`, `Plxnd1`, and `Sema5a` were used as an internal, same-experiment interpretation layer over the parquet.
- Distributed Agents runtime profile comparison over the raw parquet
  - Compared the signed Wilcoxon-score vectors for held-in semaphorin/plexin/neuropilin and cytoskeletal candidates in `151 TH Prkcd Grin2c Glut`.
- External literature
  - Tamagnone et al. 1999, PMID 10520995, DOI `10.1016/S0092-8674(00)80063-X`: plexins are semaphorin receptors, including receptors for transmembrane, secreted, and GPI-anchored semaphorins.
  - Pasterkamp et al. 2003, PMID 12879062, DOI `10.1038/nature01790`: semaphorin 7A can regulate axon outgrowth through integrins and MAPK signaling, establishing Sema7A as a neuronal outgrowth cue.
  - Scott et al. 2009, PMID 18987670, DOI `10.1038/jid.2008.329`: Plexin-C1 is a Sema7A receptor linked to cofilin regulation, consistent with cytoskeletal rather than canonical transcription-factor biology.

## Computational steps

I summarized the training endpoint in the focal cell group. The distribution is very zero-inflated:

| statistic | value |
|---|---:|
| held-in targets | 1,674 |
| `n_degs = 0` | 1,205 |
| `n_degs > 0` | 469 |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2,677 |

For mechanistic candidates, I filtered the parquet to:

```text
group_name == "151 TH Prkcd Grin2c Glut"
and gene_target in the selected held-in analog/counterexample set
```

and counted `pvals_adj < 0.05` genes. I also noted whether the only FDR call was the target's own transcript. This is important because the endpoint includes self-transcript rows, while a self-only hit is much weaker evidence for a downstream transcriptional response than a multi-gene off-target program.

Finally, I used the Distributed Agents runtime to compute signed Wilcoxon-score profile similarity among `Plxna1`, `Plxna2`, `Plxna4`, `Plxnd1`, `Nrp1`, `Nrp2`, `Sema4d`, `Sema5a`, `Sema6a`, `Dpysl5`, `Rac1`, `Itgb1`, and `Fyn` in the focal group. That gives direct expression-pattern evidence from the parquet rather than using family membership alone.

## Plxnc1-specific evidence

### Biological prior

`Plxnc1` encodes Plexin-C1, a member of the plexin family of semaphorin receptors. The most direct ligand is Sema7A, which is not represented as a held-in perturbation target here, and the represented direct receptor set is therefore incomplete. The relevant prior is still guidance and adhesion/cytoskeletal signaling: Sema7A can affect axon outgrowth through integrin/MAPK pathways, and Plexin-C1 itself has been linked to cofilin regulation. This made held-in plexins, semaphorins, neuropilins, and small-GTPase/cytoskeletal nodes the right within-dataset comparators, but it did not supply a reason to expect a broad nuclear RNA state 3-4 weeks after acute P16 mosaic CRISPR.

### Held-in focal-cell analogs

| held-in target | focal `n_degs` | focal expression evidence | relationship to `Plxnc1` |
|---|---:|---|---|
| `Plxna1` | 0 | no genes at FDR 0.05 | Plexin receptor family member; Distributed Agents corpus says measured plexin, neuropilin, and semaphorin relatives did not phenocopy `Plxna1` and had near-zero full-signature correlations. |
| `Plxna2` | 1 | the only focal FDR gene was the self row, `Plxna2`, down at log2FC -0.596, adjusted p = 0.024 | Plexin receptor family member; same-experiment corpus reports no convergence with `Plxna1`, `Plxna4`, `Plxnd1`, `Nrp1`, `Nrp2`, `Sema4d`, `Sema5a`, or `Sema6a`. |
| `Plxna4` | 0 | no focal FDR genes; its self row was negative but not significant after BH correction | Plexin receptor family member and semaphorin receptor. Its flat focal count is a direct counterexample to assigning a nonzero count to every plexin. |
| `Plxnd1` | 0 | no focal FDR genes | Another plexin receptor. The corpus reports no downstream DE in any of 22 recovered neuronal groups and no convergence with represented semaphorin/plexin-family perturbations. |
| `Nrp1` | 0 | no focal FDR genes | Semaphorin co-receptor for Plexin-A/D signaling. Same pathway level, not a direct C1 receptor. |
| `Nrp2` | 0 | no focal FDR genes | Semaphorin co-receptor. Useful as a pathway boundary because its own acute perturbation was flat. |
| `Sema4d` | 0 | no focal FDR genes | Held-in semaphorin ligand, but not the Sema7A ligand for Plexin-C1. |
| `Sema5a` | 1 | the only focal FDR gene was the self row, `Sema5a`, down at log2FC -0.915, adjusted p = 3.94e-9 | Held-in semaphorin ligand. The corpus notes that Sema5A/Plexin-A-family perturbations were sparse and nonconvergent. |
| `Sema6a` | 0 | no focal FDR genes | Held-in semaphorin ligand for Plexin-A biology. |
| `Dpysl5` | 0 | no focal FDR genes | CRMP-family cytoskeletal effector downstream of semaphorin signaling; flat in this focal group. |
| `Rac1`, `Itgb1`, `Fyn`, `Limk1`, `Pak2`, `Pak3`, `Met` | 0 each | no focal FDR genes | Downstream or adjacent adhesion, integrin, kinase, and actin-regulatory candidates; all were quiet in this endpoint. |
| `Pak1`, `Robo1` | 1 each | focal self-row only | Cytoskeletal/guidance neighbors that show single self-transcript calls can occur without a downstream program. |

The raw-profile runtime comparison reinforced the count table. Within the semaphorin/plexin/neuropilin/cytoskeletal cohort, 11 of 13 inspected profiles had no significant focal features. `Plxna2` and `Sema5a` had one significant feature each, both their own transcripts. Across 48 inspected candidate pairs, significant-gene intersections were zero. Wilcoxon-score whole-profile similarities were also tiny: for example, `Plxna1` against `Plxna4`, `Plxnd1`, `Sema5a`, `Rac1`, `Itgb1`, and `Fyn` had cosine values from 0.0008 to 0.0399, and `Plxna2` had the largest candidate cosine to `Itgb1` at only 0.0656 with no FDR overlap. The nearest all-universe focal neighbors to `Plxna1` had whole-profile cosines of only 0.05-0.07 and were not semaphorin relatives, which is noise-scale for this sparse profile.

The Distributed Agents same-experiment corpus claim over `Dpysl5`, `Nrp1`, `Nrp2`, `Plxna1`, `Plxna2`, `Plxna4`, `Sema4d`, `Sema5a`, and `Sema6a` summarizes the broader version of this result: represented semaphorin-plexin-neuropilin perturbations in the postnatal neuronal screen did not form an interchangeable shared acute neuronal mRNA-signature module. I treated that as same-experiment support for a near-null `Plxnc1` call, not as proof that Plexin-C1 has no wiring function.

### Decision

The nonzero case for `Plxnc1` would have to come from one of two places:

1. A downstream Sema7A/Plexin-C1 transcriptional response in thalamic glutamatergic neurons.
2. A significant negative `Plxnc1` self-transcript row with no downstream DE, analogous to the single self-row counts for `Plxna2` or `Sema5a`.

The first case is weak. The closest held-in plexin and semaphorin pathway perturbations were flat or self-only in the exact endpoint, and their focal score vectors did not converge. The second case is possible, because `n_degs` counts self rows, but it is not predictable enough to round the point estimate up to 1: in the focal group, `Plxna1`, `Plxna4`, `Plxnd1`, `Nrp1`, `Nrp2`, `Sema4d`, and `Sema6a` all failed to create even a self-row FDR call. `Plxnc1` as a measured gene was also usually stable across held-in focal perturbations, with median adjusted p-value 1.0 and only three of 1,674 held-in perturbations moving the `Plxnc1` row at FDR 0.05.

I therefore predicted no measured genes passing FDR 0.05:

| target_name | predicted_n_degs |
|---|---:|
| Plxnc1 | 0 |

## Limits

- `Sema7a`, `Plxnb1`, and `Plxnb2` were absent from the held-in focal count table, so the exact Plexin-C1/Sema7A axis was not directly observed as a matched perturbation.
- Plexin-C1 may affect axon guidance, neurite outgrowth, adhesion, or cofilin/actin state without leaving a stable single-nucleus mRNA footprint in recovered thalamic neurons.
- The comparison is postnatal and survivor-conditioned; it does not test embryonic tract formation, olfactory bulb or hindbrain biology, glia, vascular cells, immune cells, or cell morphology.
- A single significant `Plxnc1` self-row remains plausible. Because self-transcript loss is noisy in this CRISPR readout and biologically adjacent perturbations were mostly zero, the integer point prediction stays at zero rather than one.
