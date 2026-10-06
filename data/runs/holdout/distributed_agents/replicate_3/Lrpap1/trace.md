# Lrpap1 prediction trace

## Question and resolved ambiguities

The manifest for this run contains one held-out perturbation, `Lrpap1`. I interpreted the requested value as:

- the number of measured genes in `151 TH Prkcd Grin2c Glut`
- whose Wilcoxon Benjamini-Hochberg adjusted p value is `< 0.05`
- after acute, sparse, AAV CRISPR loss of the named target
- with `Lrpap1` absent from both the raw training DE parquet and the focal-cell training-count CSV.

I therefore treated focal-cell `n_degs` from the CSV as the calibration target and used the parquet only for same-experiment expression patterns among non-held-out perturbations. I did not use the target transcript fold change as evidence for editing strength, because this assay's target mRNA depletion is not a quantitative editing-efficiency readout.

## Sources used

- Same-experiment DE parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Same-experiment focal-cell endpoint: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Held-out manifest: `[local file: 128_Lrpap1.csv]`.
- Distributed Agents same-experiment semantic corpus `perturbai-july-260713-sourceguard-1773-v1`, especially target contexts for `Lrp1`, `Lrp2`, `Lrp6`, `Lrp8`, `Dab1`, `Reln`, `Vldlr`, `Sorl1`, and `Sort1`.
- Distributed Agents runtime `profile_neighbors`, used to compare `Lrp1`, `Lrp2`, `Lrp6`, `Lrp8`, `Vldlr`, `Dab1`, `Reln`, `Sorl1`, and `Sort1` signed log-fold-change profiles with all 1,674 eligible training targets in the matched `151 TH Prkcd Grin2c Glut` context.
- Public literature from PubMed:
  - Willnow, Armstrong, Hammer, and Herz 1995, PNAS, DOI `10.1073/pnas.92.10.4537` / PMID `7538675`: RAP deficiency reduces mature processed LRP in liver and brain in vivo, supporting RAP as a stabilizing escort for LRP.
  - Bu and Rennke 1996, Journal of Biological Chemistry, DOI `10.1074/jbc.271.36.22218` / PMID `8703036`: the 39 kDa receptor-associated protein, encoded by `LRPAP1`, is a folding chaperone for LRP and prevents improper aggregation of ligand-binding repeats.
  - Sarti, Farquhar, and Orlando 2000, Experimental Cell Research, DOI `10.1006/excr.2000.4993` / PMID `11035914`: RAP is primarily an ER chaperone needed for folding/exocytic trafficking of LDL-receptor-family proteins including LRP and megalin/LRP2.
  - Pan et al. 2004, Journal of Cell Science, DOI `10.1242/jcs.01381` / PMID `15383619`: RAP binds LDL-receptor-family members, antagonizes their ligand binding, and can be transported by LRP1/LRP2 systems at the blood-brain barrier, reinforcing that the main known biology is LDL-receptor-family handling rather than a stand-alone nuclear program.

## Computations over the training data

1. I verified that the manifest has only `Lrpap1`, and that `Lrpap1` has no row in either training surface.
2. I read the focal-cell training-count CSV and extracted counts for LDL-receptor-family, Reelin, and sorting-receptor comparators.
3. I filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and the receptor comparators listed below, using Arrow rather than reading the entire 616,253,184-row parquet:

```python
expr = (
    (ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & ds.field("gene_target").isin(targets)
)
table = dset.to_table(
    columns=["names", "gene_target", "logfoldchanges", "pvals_adj",
             "n_pert_matched", "n_ctrl_matched"],
    filter=expr,
)
```

4. For each comparator, I counted `pvals_adj < 0.05` in the focal class and checked the actual significant genes, if any.
5. I compared the unthresholded signed log-fold-change profiles among the receptor candidates to look for low-amplitude shared structure that might be hidden under the FDR threshold. Each direct comparator had 17,259 measured genes in this focal class and 106-230 matched perturbed nuclei against 23,679 matched control nuclei.
6. I used Distributed Agents `profile_neighbors` with the same focal context and all 1,674 training targets as the eligible universe. The top whole-profile and signed-tail neighbors of `Lrp1`, `Lrp2`, `Lrp8`, `Vldlr`, `Dab1`, `Reln`, `Sorl1`, and `Sort1` were mostly unrelated 0-DEG or 1-DEG perturbations; occasional high-count targets appeared only in one signed tail and were not stable, whole-profile phenocopies.

## Same-experiment analogs

| training perturbation | focal `n_degs` | why it mattered |
| --- | ---: | --- |
| `Lrp1` | 0 | Direct RAP/LRPAP1 client and the main LDL-receptor-related receptor with mature receptor reduced in RAP-deficient brain in Willnow et al. The focal-class parquet had no FDR<0.05 genes for `Lrp1`. The Distributed Agents corpus further reports that the screen saw only a highly restricted `Vgf` response outside this thalamic class and that `Lrp1` did not induce the detectable ER-stress/UPR module seen after `Manf`. |
| `Lrp2` | 0 | Megalin/LRP2 is another major RAP chaperone client. It was completely flat in `151 TH Prkcd Grin2c Glut`; corpus context says acute P16 `Lrp2` perturbation had no BH-corrected neuronal response in any recovered cell group and did not phenocopy LDLR-family, Reelin, SHH, or Wnt targets. |
| `Lrp4`, `Lrp5`, `Lrp8`, `Vldlr` | 0 each | These LDL-receptor-family relatives test whether family membership or Reelin-receptor biology creates a hidden receptor-loss mRNA state. All were zero in the focal count table. `Lrp8` and `Vldlr` were also part of a corpus claim that the represented Reelin signaling core is transcriptionally buffered in the P16 mosaic neuronal snRNA-seq readout. |
| `Reln`, `Dab1` | 0 each | These are not RAP clients, but they are mechanistic partners of `Lrp8`/`Vldlr` and strong counterexamples to transferring canonical developmental Reelin biology into this postmitotic RNA endpoint. Both were zero in the focal class. The corpus reports broad flatness of the measured Reelin ligand/receptor/adaptor/kinase core after P16 sparse perturbation. |
| `Sorl1`, `Sort1` | 0 each | Sorting receptors and APP/endosomal comparators ask whether a cargo-receptor trafficking defect rather than a pure LDLR-family effect might be visible. Both had 0 focal DEGs; corpus contexts describe `Sorl1` as downstream-null across measured neuronal groups and `Sort1` as buffered in the `151` class despite detectable `Sort1` RNA depletion. |
| `Lrp6` | 4 | The one LDLR-family member with a nonzero focal count. Its four FDR<0.05 genes in the parquet were `Nrbp2`, `Nsmf`, `Atrnl1`, and `Chgb`. I treated it as a weak counterexample rather than a close analog: the corpus places `Lrp6` in a selective thalamic Wnt/beta-catenin branch with `Ctnnb1`, while `Lrp1`, `Lrp2`, `Lrp4`, `Lrp5`, `Lrp8`, `Vldlr`, `Sorl1`, and `Sort1` did not phenocopy that Wnt state. |
| `Manf`, `Hspa5`, `Sec63`, `Amfr` | 3, 5, 11, 1 | Generic ER/proteostasis comparators. I did not transfer a broad ER-stress count to `Lrpap1`: the public literature makes RAP a receptor-specific ER folding/escort factor, and the same-experiment `Lrp1` context explicitly reports that `Lrp1`-associated outputs were uncoupled from detectable UPR genes. |

The exact focal-class raw counts for the most relevant receptor panel were:

| target | `n_degs` at FDR<0.05 |
| --- | ---: |
| `Dab1` | 0 |
| `Lrp1` | 0 |
| `Lrp2` | 0 |
| `Lrp4` | 0 |
| `Lrp5` | 0 |
| `Lrp6` | 4 |
| `Lrp8` | 0 |
| `Reln` | 0 |
| `Sorl1` | 0 |
| `Sort1` | 0 |
| `Vldlr` | 0 |

The pairwise Pearson correlations among these zero and near-zero `logfoldchanges` vectors ranged from about 0.61 to 0.70. That initially looked coherent, but the profile-neighbor expansion showed the same background structure connected many unrelated FDR-null signatures. I therefore treated the shared low-amplitude ranks as evidence that these perturbations live near the null manifold, not as evidence for a latent high-count pathway.

## Target-specific reasoning

### `Lrpap1`

`Lrpap1` encodes RAP, an ER-resident escort and folding chaperone for LRP-family receptors. The most direct expected consequence of loss is impaired maturation/trafficking or premature ligand binding of large LDL-receptor-family clients, not loss of a transcription factor or collapse of a core housekeeping machine. Bu and Rennke showed that RAP prevents aggregation and supports proper folding of LRP ligand-binding domains; Willnow et al. showed RAP deficiency reduces mature processed LRP in liver and brain; and Sarti et al. summarized RAP's necessary role in folding/exocytic trafficking of LRP and megalin/LRP2.

That external biology makes `Lrp1` and `Lrp2` the best within-dataset analogs. Both are FDR-null in `151 TH Prkcd Grin2c Glut`, and the Distributed Agents corpus treats them as weak or absent transcriptomic responders in this juvenile NeuN+ screen. The surrounding receptor and pathway perturbations strengthen the zero call: `Lrp4`, `Lrp5`, `Lrp8`, `Vldlr`, `Reln`, `Dab1`, `Sorl1`, and `Sort1` also had zero focal DEGs, and corpus findings reject a simple LDLR-family, Reelin-core, APP-sorting, or sortilin/lysosome RNA module in this assay.

`Lrp6` argues only for a tiny possible nonzero tail, not for a broad effect. Its focal response had just four FDR<0.05 genes and was annotated as a selective Wnt/beta-catenin state with `Ctnnb1`, whereas `Lrpap1` is not a selective Wnt co-receptor and the nearby LRP/LDLR-family targets did not share the `Lrp6` state. Similarly, generic ER chaperone perturbations are imperfect analogs because RAP has a narrow receptor-client set; direct `Lrp1` perturbation did not induce the Manf/Hspa5 UPR module that the assay can detect.

I therefore expect sparse `Lrpap1` loss in recovered postnatal thalamic glutamatergic neurons to fall below the FDR<0.05 detection threshold. The point prediction is `0` DEGs.

## Limits and extrapolations

- `Lrpap1` itself was completely held out, so there is no direct same-experiment `Lrpap1` signature, target RNA movement, or matched perturbed-nucleus count.
- The best analogs are client receptors rather than the chaperone itself. A chaperone loss can affect multiple receptors at once, so a small emergent effect is possible even when the individual clients are flat.
- The experiment measures nuclear RNA in recovered NeuN+ juvenile neurons. RAP/LRP biology involving epithelial megalin, vascular LRP1, choroid plexus, kidney, ligand uptake, protein trafficking, or chronic aging/proteopathy is mostly outside the assayed endpoint.
- The within-dataset analogs had 106-230 focal perturbed nuclei; a weak response could remain below FDR in one perturbation and cross threshold in another because of power or guide activity.
- I used `Lrp6` as a counterexample, not a close proxy. If RAP unexpectedly affected an LRP6-like Wnt branch in `151 TH Prkcd Grin2c Glut`, the true count could be a few genes rather than zero, but the receptor panel and biology make that less likely than a null call.
