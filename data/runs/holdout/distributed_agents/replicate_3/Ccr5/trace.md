# Ccr5 DEG-count prediction

## Question and resolution

The requested held-out target file contains one target, `Ccr5`. I interpreted the task as a point prediction for the number of measured genes in the exact focal group `151 TH Prkcd Grin2c Glut`; all counts below refer only to that cell group and to the endpoint definition `pvals_adj < 0.05` in the training-count CSV. A prediction of 0 means no measured transcript, including the perturbed target transcript itself if present in the expression feature space, is expected to cross BH FDR 0.05.

`Ccr5` was a true holdout: it was absent from the 1,674-row focal `n_degs` CSV and had 0 rows as `gene_target` in `training_de_all_cell_groups.parquet`.

## Sources

- Differential expression parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Training endpoint CSV: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Holdout manifest: `[local file: 032_Ccr5.csv]`.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`, for Ccr2, Cx3cr1, Cxcr4, and P2ry12 perturbation reports. The corpus had no Ccr5 target card, so I used it only for observed training perturbations.
- Distributed Agents runtime profile comparison on focal `151 TH Prkcd Grin2c Glut` Wilcoxon-score vectors for `Ccr2`, `Cx3cr1`, `Cxcr4`, `P2ry12`, `P2ry14`, `Csf1r`, `Axl`, `Mertk`, `Il10ra`, `Irf5`, `Tlr4`, `Nfkb1`, `Stat1`, and `Stat3`.
- PubMed literature searches for Ccr5 chemokine-receptor biology and neuronal CCR5 phenotypes.

## Same-experiment computations

I used DuckDB predicate pushdown over the parquet to extract only the focal cell group and selected targets:

```sql
SELECT gene_target, names, scores, logfoldchanges, pvals_adj
FROM read_parquet('training_de_all_cell_groups.parquet')
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
```

The focal group is a dense 1,674 perturbation x 17,259 gene matrix. The training endpoint distribution is zero-heavy: 1,205/1,674 targets have 0 DEGs, the median is 0, the mean is 14.1, and only 106 targets have at least 10 DEGs. I therefore required either close observed relatives with nonzero responses or a compelling target-specific reason to move Ccr5 out of the null class.

The main focal-cell analogs were:

| training target | `n_degs` in focal cell group | focal DE and score evidence | reason for comparison |
| --- | ---: | --- | --- |
| `Ccr2` | 0 | 17,259 tested genes; minimum focal FDR was 1.0. Its Wilcoxon-score vector had near-zero Pearson correlations to `Cx3cr1` (-0.002) and `Cxcr4` (0.025) and no shared significant features. | Closest available CC chemokine receptor. The Distributed Agents Ccr2 report also found no FDR<0.10 genes in any of 22 recovered neuronal groups, and its Ccr2 vector had no meaningful global neighbor. |
| `Cx3cr1` | 0 | 17,259 genes; minimum focal FDR was 1.0. Score correlations to `Ccr2` and `Cxcr4` were -0.002 and 0.005. | Neuroimmune chemokine-family GPCR dominated by microglial CX3CL1-CX3CR1 biology; a useful counterexample for a receptor with strong brain biology that is displaced from NeuN-positive neuronal cell-autonomous RNA readouts. |
| `Cxcr4` | 0 | 17,259 genes; no focal FDR<0.05 hits. The closest focal gene was `Pum1`, FDR 0.067, so just above the endpoint threshold. | Chemokine GPCR with canonical CNS roles in migration and CXCL12 signaling; in the Distributed Agents Cxcr4 report, postnatal sparse Cxcr4 loss produced only isolated one-gene FDR<0.10 events across neurons and did not converge with Ccr2 or Rac-arm comparators. |
| `P2ry12` | 0 | Minimum focal FDR 1.0. | Microglia-lineage GPCR; Distributed Agents reported only a single borderline gene in another neuronal group and broader flatness among microglial receptors. |
| `P2ry14` | 0 | Minimum focal FDR 1.0. | Related immune P2Y GPCR used as another neuroimmune-receptor null. |
| `Csf1r`, `Axl`, `Mertk` | 0, 0, 0 | Focal minimum FDRs 1.0, 0.363, and 0.888. | Microglial and TAM/efferocytosis receptors; the Distributed Agents P2ry12 and Cx3cr1 reports use these as lineage controls and find flat NeuN-positive neuronal surfaces. |
| `Il10ra`, `Irf5`, `Tlr4`, `Nfkb1`, `Stat1`, `Stat3` | 0, 0, 0, 0, 1, 0 | `Il10ra`, `Irf5`, `Tlr4`, `Nfkb1`, and `Stat3` had no focal DEGs; `Stat1` had one DEG, the targeted `Stat1` transcript itself at FDR 0.027. | Downstream or parallel inflammatory signaling controls. They test whether an innate cytokine/NF-kappaB/STAT state is easy to evoke in this focal neuronal assay. It is not. |

I also scanned broader name classes in the focal endpoint. The six represented TLRs (`Tlr2`, `Tlr3`, `Tlr4`, `Tlr5`, `Tlr7`, `Tlr8`) all had `n_degs = 0`; 18 represented interleukin or TNF receptor targets all had `n_degs = 0`; and all five STAT/NF-kappaB entries except `Stat1` had 0. `Ccr5` was present as a measured expression feature, but across the 22 queried neuroimmune targets the minimum adjusted p value for measured `Ccr5`, `Ccl2`, `Ccl3`, `Ccl4`, `Ccl5`, `Ccl7`, `Ccl8`, `Ccl12`, `Cxcl12`, `Cxcl10`, `Fos`, `Jun`, `Nfkb1`, and `Stat3` was 1.0. Thus the observed Ccr2/Cx3cr1/Cxcr4 zeros were not hiding an induced chemokine or immediate-early inflammatory feedback program in this cell group.

For profile geometry I compared Wilcoxon `scores`, not raw `logfoldchanges`; raw log fold changes can be enormous for genes with near-zero counts even when FDR is 1.0. The score-based Distributed Agents runtime comparison marked `Ccr2`, `Cx3cr1`, and `Cxcr4` as `no_significant_features` and found zero shared significant features or significant-direction conflicts between those chemokine receptors and the immune-receptor controls listed above. This supports absence of a coherent focal-cell neuroimmune response rather than only absence of one particular direct DEG.

## Biology for Ccr5

CCR5 is a Gi-coupled CC-chemokine GPCR whose classic ligands include CCL3/MIP-1alpha, CCL4/MIP-1beta, and CCL5/RANTES; this receptor was cloned and functionally validated by Combadiere et al. 1996 (PMID 8699119, DOI 10.1002/jlb.60.1.147) and reviewed by Mueller and Strange 2004 (PMID 14592532, DOI 10.1016/s1357-2725(03)00172-9). That makes `Ccr2` the most direct in-dataset analog by receptor family and inflammatory CC-chemokine logic.

Ccr5 is not purely irrelevant to neurons. Zhou et al. 2016 showed that decreasing CCR5 function increased MAPK/CREB signaling, LTP, cortical plasticity, and hippocampus-dependent memory in mice (PMID 27996938, DOI 10.7554/eLife.20985). Joy et al. 2019 reported that neuronal CCR5 knockdown or maraviroc improved recovery after stroke/TBI with CREB and DLK signaling changes (PMID 30794775, DOI 10.1016/j.cell.2019.01.044). Those papers prevent treating Ccr5 as merely an off-lineage leukocyte marker.

However, the external Ccr5-positive contexts are a poor match for this endpoint. They involve cortex or hippocampus, injury- or HIV-peptide-associated ligand activation, shRNA/pharmacology or germline alleles in several experiments, and behavioral/synaptic repair phenotypes. The readout here is acute mosaic CRISPR loss of function delivered around P16, assayed 3-4 weeks later in healthy NeuN-enriched thalamic `Prkcd/Grin2c` glutamatergic nuclei. The same experiment already contains chemokine receptors with at least as obvious CNS priors (`Cxcr4`) and microglial/neuroimmune priors (`Cx3cr1`, `P2ry12`, `Csf1r`) and they are silent in this focal cell group.

## Target-specific prediction

`Ccr5`: I predict `0` DEGs. The decision is driven primarily by within-dataset evidence: `Ccr2`, the only observed same-CC receptor analog, has 0 focal DEGs and no all-neuronal program in the Distributed Agents corpus; `Cx3cr1` and `Cxcr4`, the other observed chemokine receptors, are also 0 in the focal endpoint with near-orthogonal score vectors; and a broader panel of neuroimmune GPCR, TLR, cytokine, TAM, CSF1R, NF-kappaB, and STAT controls is almost uniformly null. The external literature raises the prior that Ccr5 can signal in neurons, but its strongest phenotypes are synaptic/plasticity and injury-recovery contexts rather than a basal broad nuclear mRNA state in the assayed thalamic neurons. I therefore do not expect any gene to pass BH FDR 0.05 after Ccr5 perturbation in `151 TH Prkcd Grin2c Glut`.

## Limits

- No true same-complex or same-ligand Ccr5 analog was measured as a perturbation; `Ccr2`, `Cx3cr1`, and `Cxcr4` are family or pathway controls rather than Ccr5 paralogs.
- The Distributed Agents corpus has no Ccr5 holdout card, so Ccr5-specific same-experiment evidence is necessarily indirect.
- The experiment did not measure DNA indels, and average guide-level RNA knockdown is partial. A zero prediction is about the FDR-corrected snRNA-seq response, not proof that Ccr5 guides never edit or that CCR5 is biologically inert.
- Healthy P16-to-P37/P44 thalamic glutamatergic neurons do not reproduce the injured cortex, hippocampus, microglia, macrophage, or T-cell settings in which CCR5 signaling is well established.
