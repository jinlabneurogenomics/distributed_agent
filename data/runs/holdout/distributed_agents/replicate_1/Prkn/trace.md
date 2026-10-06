# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

The requested output is an integer prediction of `n_degs` for each held-out perturbation in the focal thalamic glutamatergic class `151 TH Prkcd Grin2c Glut`, where `n_degs` is the count of measured mouse genes with Wilcoxon Benjamini-Hochberg `pvals_adj < 0.05`. I treated the adjusted-p-value threshold as strict `<0.05`; the count includes the target transcript itself if it passes FDR. The held-out expression profile for `Prkn` was not in either declared input, and `Prkn` also had no packaged target report in the selected internal corpus, so I inferred its count from visible training perturbations and external PINK1/Parkin biology.

## Sources used

* Declared DE Parquet: `training differential-expression dataset`.
* Declared focal training counts: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
* Requested-target manifest: `single-target request for Prkn`, containing only `Prkn`.
* Run-local manifests in `codex_runtime/pipeline`, especially `task_bindings.json`, `coverage.json`, `measurement_registry.json`, and `capabilities.json`.
* Internal same-experiment semantic corpus `perturbai-july-260713-sourceguard-1773-v1`, queried only for visible training analog reports: `Park7`, `Atp13a2`, `Snca`, `Uchl1`, `Tomm40`, `Mff`, and `Opa1`. The corpus is a curated interpretation of the same Perturb-seq experiment, not an independent replication.
* External PubMed literature for mechanism: Narendra et al. 2008, J Cell Biol, doi:10.1083/jcb.200809125; Wang et al. 2011, Cell, doi:10.1016/j.cell.2011.10.018; Pickrell and Youle 2015, Neuron, doi:10.1016/j.neuron.2014.12.007; Lazarou et al. 2015, Nature, doi:10.1038/nature14893; Filograna et al. 2024, NPJ Parkinsons Dis, doi:10.1038/s41531-024-00707-0.

Ranking-only workbench capabilities were unavailable and inappropriate for this scalar count endpoint, so I did not use `dataset.perturbseq_features`, `corpus.predictive_graph_review`, or `synthesis.ordering_validate`.

## Quantitative checks

I first read the focal training-count CSV to calibrate the count scale. Among 1,674 non-held-out focal perturbations, the median `n_degs` is 0, 469 have any FDR<0.05 hit, and the upper tail is very skewed: 75th percentile 1 DEG, 90th percentile 2 DEGs, 95th percentile 18 DEGs, maximum 2,677 DEGs. A prediction of zero or one is therefore a normal outcome, not an outlier.

I then queried the declared Parquet directly, filtering to the focal group and visible mitochondrial quality-control, Parkinson, autophagy, ubiquitin, and stress comparators. The operation was a direct aggregation:

```sql
SELECT gene_target,
       SUM(CASE WHEN group_name = '151 TH Prkcd Grin2c Glut'
                 AND pvals_adj < 0.05 THEN 1 ELSE 0 END) AS focal_n_degs,
       COUNT(DISTINCT CASE WHEN pvals_adj < 0.05 THEN group_name END) AS groups_with_degs,
       SUM(CASE WHEN pvals_adj < 0.05 THEN 1 ELSE 0 END) AS all_group_degs
FROM read_parquet(:training_de)
WHERE gene_target IN (...)
GROUP BY gene_target;
```

The visible perturbations closest to Parkin biology were flat in the focal class:

| visible training target | focal `n_degs` at FDR<0.05 | same-experiment interpretation |
| --- | ---: | --- |
| `Park7` | 1 | The single focal hit is `Park7` itself; its same-experiment report found 0 downstream FDR<0.10 genes in all 23 measured cell groups and no NRF2, UPR/ISR, autophagy, or PINK1/Parkin sentinel induction. |
| `Atp13a2` | 1 | The single focal hit is `Atp13a2` itself despite 335 matched perturbed nuclei; the report found 0 downstream FDR<0.10 genes in all 23 cell groups and no lysosomal, autophagy, TFEB/SYT11, synuclein, UPR, or redox sentinel response. |
| `Snca` | 0 | No focal FDR<0.05 genes; the report found only one weak downstream FDR<0.10 call across 21 measured groups and no broad synaptic or Parkinson-like response. |
| `Uchl1` | 1 | The focal hit is `Uchl1` itself; its only downstream FDR<0.10 gene across the report was `Ctif` in another cell group, and canonical proteostasis/autophagy/UPR markers did not respond. |
| `Tomm40` | 1 | The focal hit is `Tomm40` itself; same-experiment Tomm40 profiles were almost entirely null, including no proteasome bounceback and no TOM/TIM paralog response. |
| `Rhot1` | 0 | Miro1 is an outer-membrane substrate targeted by PINK1/Parkin for degradation, but `Rhot1` had 0 focal DEGs and 0 DEGs across all measured groups. |
| `Mff` | 0 | A mitochondrial fission-factor perturbation had 0 focal DEGs and 0 DEGs across all measured groups. |
| `Atg5`, `Becn1`, `Nfe2l2` | 0, 0, 0 | Macroautophagy and antioxidant-response comparators were focal-null. |
| `Sqstm1`, `Ndufs2`, `Lonp1` | 1, 1, 0 | Broader autophagy/mitochondrial stress comparators were still absent or self-only in the focal endpoint. |

The useful positive counterexamples were mechanistically farther away. `Opa1`, an inner-membrane fusion/cristae GTPase, had 37 focal FDR<0.05 genes with an amino-acid/ATF4 integrated-stress signature (`Asns`, `Mars1`, `Chac1`, `Ddit3`, `Mthfd2`, and `mt-Co2`). `Vps35` had 17 focal DEGs in a retromer/vesicular-trafficking response, `Bap1` had 16, `Usp48` had 10, `Hspa5` had 5, and the core proteasome perturbation `Psmb4` had 742. These show that this cell class can report proteostasis or mitochondrial stress when the perturbed node creates that state, but they are not same-step analogs of acute Parkin loss.

## `Prkn` rationale

`Prkn` encodes the Parkin RBR E3 ligase. In the causal chain relevant here, loss of Parkin blocks amplification of PINK1-generated phospho-ubiquitin on damaged mitochondria and reduces ubiquitination of outer-membrane proteins and autophagy-receptor recruitment. PINK1 can still mark depolarized mitochondria and recruit NDP52/OPTN directly, so Parkin loss is not equivalent to removing the autophagy machinery itself (Lazarou et al. 2015). Parkin can also promote Miro/Rhot degradation and mitochondrial arrest after damage (Wang et al. 2011). Thus direct molecular engagement is plausible, but the major downstream transcriptional consequences should appear only when thalamic postmitotic neurons experience enough mitochondrial damage for this pathway to become limiting.

The visible training perturbations argue against a large basal effect in this 3-4 week sparse CRISPR design. `Park7`, `Atp13a2`, `Snca`, and `Uchl1` are Parkinson-associated or ubiquitin/lysosome-linked but gave only 0 or self-only focal FDR<0.05 hits. `Rhot1`, a Parkin substrate in the mitochondrial motility arm, was completely silent. `Mff` was also silent even though mitochondrial morphology genes can be essential under other conditions. Conversely, the focal class did react to `Opa1` with 37 DEGs, but that program was an inner-membrane fusion and OMA1-DELE1-HRI/ATF4 integrated-stress response; Opa1 report checks found classical `Pink1`, `Prkn`, `Sqstm1`, `Hspd1`, `Hspe1`, and `Clpp` markers absent from that program. I therefore used `Opa1` as an upper-bound mitochondrial-stress counterexample, not as a direct quantitative analog.

External evidence supports the same direction. Parkin is recruited to impaired mitochondria and mediates their autophagic elimination in damaged-mitochondrion assays (Narendra et al. 2008), and PINK1/Parkin are central in ubiquitin-dependent mitophagy (Pickrell and Youle 2015). But mammalian Parkin-deficient models frequently lack large basal brain or dopaminergic transcriptional/OXPHOS phenotypes; Filograna et al. found that loss of PARKIN did not affect OXPHOS capacity or mtDNA in aged mouse brain, heart, or skeletal muscle, and adult induced loss in dopaminergic neurons produced no major transcriptional change (Filograna et al. 2024). The requested experiment is acute juvenile CRISPR in surviving NeuN+ thalamic glutamatergic nuclei, without an imposed mitochondrial toxin or mtDNA mutator background, so a stress-conditioned PINK1/Parkin defect should be weak.

I predicted `Prkn` at 0 rather than 1 because the focal count will only become 1 if the `Prkn` transcript itself is both detectable and corrected at FDR<0.05. Several low-breadth analogs owed their entire count of 1 to an abundant self transcript; `Snca`, `Mff`, and many self rows in the inspected reports showed that even negative self logFC often remains nonsignificant. `Prkn` is a large, lowly expressed neuronal transcript, and random visible perturbations in the focal Parquet altered `Prkn` rarely and with a mean logFC essentially zero, so I did not add a self-only hit in the point estimate.

Final point prediction: `Prkn` = 0.

## Limits

This is an extrapolation because the held-out Prkn perturbation was absent from the supplied DE and count inputs, `Pink1` was also absent as a perturbation target, and there was no internal Prkn report. The strongest external PINK1/Parkin phenotypes are often stress-, age-, dopaminergic-, or non-mammalian-context dependent, none of which is the exact focal thalamic sparse-CRISPR condition. I used same-experiment analogs to bound the likely DEG count, but Parkinson-family membership alone was not treated as a score: `Vps35` and `Opa1` demonstrate that some related endosomal or mitochondrial nodes can be visible while Park7/Atp13a2/Snca/Rhot1/Mff remain null. The zero/nonzero boundary is most sensitive to the self-transcript row, not to a strong predicted downstream response; if the Prkn guides happened to give an FDR-significant measured Prkn decrease, the true count could be 1 even with no downstream program.
