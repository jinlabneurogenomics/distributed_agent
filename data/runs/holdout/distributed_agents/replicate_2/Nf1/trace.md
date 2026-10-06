# DEG-count prediction trace

## Question and resolved ambiguities

The requested held-out target file contains one perturbation:

| target_name |
|---|
| Nf1 |

I interpreted the endpoint exactly as the task defines it: the number of measured genes in `151 TH Prkcd Grin2c Glut` whose Wilcoxon `pvals_adj` is below 0.05 for the held-out `Nf1` perturbation. Counts include the target transcript itself if it passes the FDR threshold. I used `0` to mean that no measured gene is expected to pass the 0.05 adjusted-p cutoff in this cell group, not that NF1 biology is absent.

## Sources used

- Supplied training DEG counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Supplied differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Requested-target manifest:
  `[local file: 148_Nf1.csv]`
- Internal same-experiment semantic layer: Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`.
- PubMed-indexed external literature used only to place `Nf1` in the RAS/MAPK/SPRED pathway:
  - Scheffzek and Shivalingaiah 2019, Cold Spring Harbor Perspectives in Medicine, DOI `10.1101/cshperspect.a031500`.
  - Stowe et al. 2012, Genes & Development, DOI `10.1101/gad.190876.112`.
  - Yan et al. 2020, Cell Reports, DOI `10.1016/j.celrep.2020.107909`.
  - Bergoug et al. 2020, Cells, DOI `10.3390/cells9112365`.
  - Xie et al. 2016, Current Biology, DOI `10.1016/j.cub.2016.09.010`.

## Dataset computations

The full parquet has 616,253,184 rows, so I used row-group metadata and predicate pushdown by `group_name` to avoid scanning all cell groups:

```python
pq.read_table(
    parquet_path,
    filters=[
        ("group_name", "=", "151 TH Prkcd Grin2c Glut"),
        ("gene_target", "in", pathway_targets),
    ],
    columns=["names", "gene_target", "logfoldchanges", "pvals_adj",
             "n_pert_matched", "n_ctrl_matched"],
)
```

For focal pathway candidates I read 517,770 `(gene, perturbation)` rows covering 30 training perturbations. I then:

- Counted focal DEGs with `pvals_adj < 0.05` to confirm exact counts against the training-count CSV.
- Listed FDR-significant genes for BRAF/MEK/SHOC2/NTF3-TRK and mTOR analogs.
- Checked signed log2 fold changes and adjusted p-values for `Vgf`, `Ptpn5`, `Unc13a`, `Etv5`, `Atp2a2`, `Cul7`, `Fos`, `Egr1`, `Arc`, `Dusp6`, and `Spry2`.
- Ran a Distributed Agents runtime profile comparison for a declared Ras/MAPK/PI3K cohort in the focal group using `logfoldchanges` as the signed profile and `pvals_adj < 0.05` as the significance layer. That compared whole-profile similarity and FDR-level overlap among `Braf`, `Map2k1`, `Ntrk2`, `Shoc2`, `Spred1`, `Spred2`, `Rasa2`, `Syngap1`, `Sos1`, `Hras`, `Kras`, `Raf1`, `Map2k2`, `Mapk1`, `Ptpn11`, `Tsc2`, and `Mtor`.

## Target-specific evidence and reasoning

### Nf1

`Nf1` encodes neurofibromin, a major Ras GTPase-activating protein that accelerates GTP hydrolysis by RAS and thereby restrains RAS/MAPK signaling. SPRED-family proteins recruit neurofibromin to the plasma membrane and position it with active RAS; Legius syndrome SPRED1 loss and NF1 loss converge on this negative-regulatory mechanism. Those external facts make RasGAP and SPRED losses, not RAF/MEK losses, the cleanest sign-matched training analogs for `Nf1`.

Training perturbations most relevant to loss of a RAS brake were silent in the requested cell type:

| training perturbation | focal `n_degs` | why it mattered |
|---|---:|---|
| `Spred1` | 0 | Closest measured NF1 recruiter; Distributed Agents corpus records a high-confidence pan-measured-neuronal null and a direct contrast in which the expected Spred1 hyper-ERK/activity RNA program was absent despite detectable `Braf`/`Map2k1` signatures. In the focal rows, `Vgf` logFC was only `+0.102` and `Ptpn5`, `Unc13a`, `Etv5`, `Dusp6`, `Spry2`, `Fos`, and `Egr1` were all FDR 1.0. |
| `Spred2` | 0 | SPRED paralog and same negative-regulator class; Distributed Agents corpus records reciprocal `Spred1`/`Spred2` flatness for single acute postmitotic perturbations. No focal FDR genes. |
| `Rasa2` | 0 | RasGAP comparator; Distributed Agents corpus records a uniformly flat neuronal `Rasa2` surface and absence of canonical Fos/Jun/Egr, Dusp/Spry, and Etv feedback after loss. In the focal rows, `Vgf` was `+0.094` with adjusted p-value 1.0. |
| `Syngap1` | 0 | Neuronal synaptic RasGAP. It was also null in the focal count table, arguing that single RasGAP loss is often buffered in this endpoint. |
| `Lztr1` | 1 | Noonan/RASopathy negative regulator through ubiquitin-ligase control of RAS-family proteins. Its only focal DEG was the self transcript `Lztr1`, so it did not provide a downstream ERK-output match. |

The small positive branch of the pathway was visible but had the opposite perturbation sign for an `Nf1` loss forecast:

| training perturbation | focal `n_degs` | expression-pattern evidence |
|---|---:|---|
| `Braf` | 4 | `Atp2a2`, `Ptpn5`, `Vgf`, and `Unc13a` were all down-regulated. The profile comparison found `Braf` and `Map2k1` shared three of their four negative FDR genes: `Vgf`, `Ptpn5`, and `Unc13a`. |
| `Map2k1` | 4 | `Vgf`, `Ptpn5`, `Unc13a`, and `Etv5` were down-regulated, matching the BRAF-to-MEK thalamic module. |
| `Ntrk2` | 3 | Shared `Vgf` and `Atp2a2` down-regulation with `Braf`, consistent with a weak neurotrophin/RAF output. |
| `Shoc2` | 1 | Shared only `Vgf` down-regulation with `Braf`, `Map2k1`, and `Ntrk2`. |

The Distributed Agents same-experiment corpus summarizes the same pattern as a restricted `Braf`/`Map2k1` thalamic branch rather than a broad RAS/MAPK module: direct pathway relatives `Kras`, `Hras`, `Raf1`, `Map2k2`, `Mapk1`, `Ptpn11`, `Sos1`, and `Rasa2` were flat or nonconvergent. The focal training table agrees: `Hras`, `Kras`, `Raf1`, `Map2k2`, `Mapk1`, `Ptpn11`, `Rapgef2`, `Fgfr1`, `Fgfr2`, `Fgfr3`, `Fgfrl1`, `Alk`, `Pak2`, `Pik3cb`, `Pik3r1`, `Pik3r2`, and `Akt3` each had `0` DEGs at FDR 0.05. `Sos1` had `0` at FDR 0.05, with only a `Cul7` singleton at the looser FDR 0.10 layer in the corpus.

I considered whether NF1 could propagate through PI3K-AKT-mTOR rather than ERK. The focal data argue against borrowing the high `Tsc2` count wholesale: `Tsc2` itself had 86 focal DEGs and a sterol/lysosomal mTORC1 signature, but upstream `Akt3`, `Pik3cb`, `Pik3r1`, and `Pik3r2` were all zero and `Mtor` had only 2 DEGs. The Distributed Agents `Tsc2` findings likewise treat strong `Tsc2` loss as a position-specific mTORC1 response, not a generic upstream PI3K/RAS phenotype.

The zero/nonzero decision is therefore driven mainly by within-dataset evidence. If acute `Nf1` loss in these recovered postmitotic nuclei produced sustained hyper-RAS transcription, the closest measured losses of RAS-negative regulators, `Spred1`, `Spred2`, `Rasa2`, `Syngap1`, and `Lztr1`, should have shown at least a small shared ERK-feedback, immediate-early, VGF, DUSP/SPRY, or ETV program. They did not. Downstream positive-branch losses prove that the assay can see a very small RAF/MEK/VGF module in `151 TH Prkcd Grin2c Glut`, but the sign and mechanism are not appropriate enough to predict a 4-gene `Nf1` response. I predict `Nf1` will be below the FDR 0.05 endpoint threshold in this focal group.

Predicted count:

| target_name | predicted_n_degs |
|---|---:|
| `Nf1` | 0 |

## Limits and extrapolation

- `Nf1` itself, `Nras`, `Araf`, `Mapk3`, `Rasa1`, `Rasa3`, `Dusp6`, `Etv5`, `Cul3`, and direct `Tsc1`/`Rheb` perturbations were not available as training anchors in the supplied focal count table, so the prediction relies on nearby but imperfect single-node perturbations.
- The external NF1 literature is dominated by developmental, tumor, germline, conditional, pharmacologic, or evoked-signaling contexts. The benchmark is sparse P16 AAV CRISPR loss of function in recovered NeuN+ nuclei at P37-P44 and measures steady-state nuclear RNA, not Ras-GTP, phospho-ERK, phospho-S6, synaptic physiology, or behavior.
- SPRED1/2 silence does not prove complete redundancy of every NF1-recruitment route, and NF1 is more direct than SPRED loss. This is the main reason for residual uncertainty.
- The raw focal signatures for several zero-DEG neighbors contain subthreshold log-fold changes in pathway genes, but adjusted p-values were 1.0 for the ERK reporters in `Spred1`, `Spred2`, and `Rasa2`. I treated those as insufficient for the count endpoint rather than as hidden evidence for a small nonzero prediction.
- `n_degs` is an FDR and power dependent breadth statistic; it can drop from a real biochemical perturbation to zero after multiple-test correction. The prediction is therefore specifically a point forecast for BH-adjusted Wilcoxon `pvals_adj < 0.05`, not a claim that NF1 editing has no biochemical effect.
