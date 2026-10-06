# Q3 literature-agreement methods

## Eligibility

I filtered the full parquet to the manifest target `Srsf1` and the 23 allowed cell groups, then applied the downstream eligibility query:

```sql
lower(gene_target) = 'srsf1'
and group_name in (<allowed cell groups>)
and lower(names) <> lower(gene_target)
and pvals_adj < 0.10
```

The target transcript was excluded before counting downstream significant genes. All 23 allowed `Srsf1` cell groups had at least one non-target row with `pvals_adj < 0.10`, so 23 perturbation x cell-type pairs were eligible and 23 pair rows were emitted.

## Phenotype characterization

For each eligible pair I sorted non-target DE rows by adjusted p-value and inspected the leading positive and negative log-fold-change genes together with `n_pert_matched` and `n_ctrl_matched`. The dominant cross-cell response was a recurring RNA-processing/RBP-expression module, with genes such as `Fam193b`, `Arglu1`, `Rbm28`, `Dazap1`, `Ptbp2`, `Xpot`, `Hnrnpm`, `Hnrnpdl`, `Celf3`, `Nktr`, `Gpatch8`, `Slc30a9`, and `Srsf2` among the strongest hits depending on cell type. Larger responses, especially `052 Pvalb Gaba`, `054 CNU-MGE GABA`, `066 CNU-HYa HY GABA`, `110 CNU-HYa HY MM Glut`, `145 MH-LH TH Glut`, `151 TH Prkcd Grin2c Glut`, `155 MB Glut`, `191 MB P MY GABA`, and `217 P MY Pineal Glut`, also induced an amino-acid/integrated-stress-response tail including `Ddit3`, `Asns`, `Chac1`, `Psph`, `Shmt2`, `Aldh1l2`, aminoacyl-tRNA synthetases, and `Slc7a5`/`Slc3a2`.

The `Srsf1` target transcript itself was significant in 22 of 23 eligible pairs and nonsignificant only in `012 MEA LA CA1 DG Glut`; this was recorded as an engagement caveat but was not used to establish a null or a literature match.

## Literature search and flagging

I built the primary queries from the target name plus synonyms and the observed module genes: `SRSF1`, `ASF/SF2`, exact combinations of the top DE genes, `R-loop`, `genomic instability`, `mRNA export`, `RNPS1`, `nonsense-mediated decay`, `autoregulation`, `DDIT3`, `ASNS`, `CHAC1`, `ATF4`, and `mTORC1`. Searches used PubMed through the literature gateway and prioritized primary PubMed/PMC papers. Exact target-plus-top-gene queries were also run for the sparse or unusual responses in `012 MEA LA CA1 DG Glut`, `017 CA3 CA2-FC DG Glut`, `053 Sst Gaba`, `215 MB Dopa`, and `217 P MY Pineal Glut` so that low-hit pairs did not inherit the common RNA-processing interpretation by default.

The reviewed SRSF1 literature documents that SRSF1/ASF-SF2 binds nascent RNAs, prevents transcriptional R-loops, interacts with FANCD2 to support SRSF1-NXF1 mRNA export, can be partly buffered by RNPS1 in R-loop/genome-instability assays, autoregulates through post-transcriptional feedback, and is required for normal RNA expression and splicing in mouse spermatogonial stem cells. These papers provide a biologically specific bridge from `Srsf1` loss to RNA-processing stress, but they do not document the signed abundance changes of the observed neuronal downstream genes. I therefore used `Inferred`, with `indirect` plus species/cell-type/stage/modality context differences, whenever that recurring module was the central response.

For high-response pairs with induced amino-acid/stress genes, the SRSF1-to-mTORC1/translation literature was considered a secondary partial bridge. It was insufficient for `Agree` because the chain from SRSF1 loss to increased `Ddit3`, `Asns`, `Chac1`, one-carbon, and transporter mRNAs in juvenile postmitotic neurons was not experimentally documented.

## Adjacent decisions and multi-module pairs

`Agree` was reserved for a direct target-specific relationship or a complete cited chain predicting the observed direction; none of the eligible pairs met that bar. I did not assign `Disagree` because no searched prior gave a transferable signed expectation opposite to a sufficiently powered screen result. `No Literature` was used only for `017 CA3 CA2-FC DG Glut`, where the central response was limited to `Phf14` up, `Auts2` down, `Psma4` up, and `Itm2c` up and exact SRSF1/ASF-SF2 searches against those genes found no direct or biologically specific partial bridge.

When a pair contained several modules, I based the pair-level flag on the dominant FDR-supported response. The RNA-processing module drove all `Inferred` calls; the amino-acid/stress module was disclosed in the summaries and evidence for the cell types where it was prominent but did not change the pair-level flag.

## Review completeness

Total eligible pairs: 23. Emitted pair rows: 23. Incompletely reviewed pairs: 0. The lowest-confidence assignments are the smaller `012 MEA LA CA1 DG Glut`, `053 Sst Gaba`, `059 CNU-LGE LSX GABA`, `215 MB Dopa`, and `308 CB GABA` `Inferred` calls, because they contain only a subset of the shared RNA-processing genes, and the `017 CA3 CA2-FC DG Glut` `No Literature` call, because it had only four downstream DE genes and no clear recurrence-based module.
