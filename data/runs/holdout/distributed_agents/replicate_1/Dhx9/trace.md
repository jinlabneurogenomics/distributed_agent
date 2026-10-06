# Question and endpoint

The task asks for a point prediction for the held-out `Dhx9` perturbation in `151 TH Prkcd Grin2c Glut` thalamic glutamatergic neurons. The endpoint is the integer count of measured genes with `pvals_adj < 0.05` in the held-out contrast. I treated `Dhx9` itself as absent by design: its DEG count and its 151-cell expression signature were not used or searched for in the training CSV or differential-expression parquet.

The held-out count is directly observed for training perturbations only. For `Dhx9`, the supplied data contain no validated proxy signature; the prediction therefore combines the training endpoint for mechanistic comparators with external DHX9 biology. The July PerturbAI same-experiment corpus was used as a bounded interpretation layer over visible reports, not as independent replication.

# Sources

- Declared training endpoint: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression input: `training differential-expression dataset`, queried only for `group_name = '151 TH Prkcd Grin2c Glut'` and the RNA-processing comparators below.
- Requested-target manifest: `single-target request for Dhx9`, which contained exactly `Dhx9`.
- Internal corpus: `perturbai-july-260713-sourceguard-1773-v1`; I queried its Findings ledger and summary-first direct-evidence index for `Ddx3x`, `Hnrnpu`, `Nop56`, `Prpf6`, `Rnpc3`, and `U2af2`.
- External PubMed literature for DHX9/RNA helicase A biology:
  - Lee et al. 1998, PNAS, DOI `10.1073/pnas.95.23.13709`, PMID `9811865`: mouse RNA helicase A homozygous knockout is early embryonic lethal with marked embryonic-ectoderm apoptosis.
  - Cristini et al. 2018, Cell Reports, DOI `10.1016/j.celrep.2018.04.025`, PMID `29742442`: DHX9 is an RNA/DNA-hybrid interactor that suppresses R-loop-associated DNA damage and supports transcriptional termination.
  - Chakraborty et al. 2018, Nature Communications, DOI `10.1038/s41467-018-06677-1`, PMID `30341290`: DHX9 can also promote R-loop formation when RNA splicing is impaired, coupling RNA processing to chromatin/RNA polymerase II behavior.
  - Yuan et al. 2021, Nucleic Acids Research, DOI `10.1093/nar/gkab642`, PMID `34329467`: TDRD3 recruits/stimulates DHX9 at promoters to resolve R-loops.
  - Yamada et al. 2023, European Journal of Medical Genetics, DOI `10.1016/j.ejmg.2023.104804`, PMID `37369308`: heterozygous loss-of-function DHX9 variants can cause a neurodevelopmental disorder, and the orthologous heterozygous mouse edit altered body size, emotionality, and cardiac conduction.

# Quantitative calibration from training data

I first summarized the focal-cell training count table. It contained 1,674 unique training targets. The distribution was zero-inflated: median `n_degs = 0`, 75th percentile `= 1`, 90th percentile `= 2`, 95th percentile `= 18`, 99th percentile `= 436.48`, maximum `= 2677`, and 469 of 1,674 targets had any DEG. Thus most individual CRISPR perturbations were transcriptionally silent at FDR 0.05 in this cell group, but the assay could detect very broad responses to selected RNA-metabolism genes.

For the mechanistically relevant comparator band, I queried the declared parquet with:

```sql
SELECT names, gene_target, scores, logfoldchanges, pvals_adj
FROM read_parquet($parquet)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...RNA-processing comparators...)
```

The focal 151-cell DEG counts recovered from the parquet for selected comparators were:

| training perturbation | `n_degs` | expression-pattern evidence and use for `Dhx9` |
| --- | ---: | --- |
| `Rnpc3` | 868 | Core minor-spliceosome loss was extremely broad in 151 cells; top changes included `Rnpc3` and `Amy1` down with `Mapk8`, `Ap2a1`, `Pcyt2`, `Srp72`, and `Wdfy1` up. It had 194 FDR genes overlapping `U2af2`, 136 with `Cdc40`, and 127 with `Prpf6`, so it defines a bona fide spliceosome-stress program rather than a generic RNA-helicase prior. |
| `U2af2` | 828 | A core 3-prime splice-site factor; the 151 signature decreased `Rsrp1`, `Srrm2`, `Atp2a2`, `Agrn`, `Ogt`, and `Luc7l2` while inducing export/transport genes such as `Map7d1`, `Nxf1`, `Xpot`, and `Cmtr1` in the same-experiment report. This is stronger than expected for `Dhx9`, because DHX9 is an R-loop/RNA-DNA helicase and transcriptional regulator, not an obligate spliceosome subunit. |
| `Hnrnpu` | 733 | The same-experiment report describes a compensatory RNA-processing module convergent with `Prpf6`, `U2af2`, `Rnpc3`, and `Cdc40`, plus proteostasis and synaptic/neurite branches. `Hnrnpu` is the best nuclear RNA/DNA-binding analog because it combines chromatin scaffolding with RNA processing, but its 151 signature was much broader than weak helicase comparators and included a strong positive self-transcript/adaptive branch. |
| `Cdc40` | 624 | Another broad spliceosome-stage stressor; it shared RNA-processing and synaptic-state genes with `U2af2`/`Prpf6`. It is a useful upper-bound counterexample rather than a direct analog. |
| `Tnpo3` | 618 | Nuclear import of SR splicing factors; it converged with the `Nop56` 151-cell negative RNA-processing branch in the same-experiment corpus. It shows that perturbing traffic into nuclear splicing machinery can be broad, but the function is still closer to SR-factor localization than to DHX9. |
| `Prpf6` | 454 | A U5 tri-snRNP spliceosome factor. The same-experiment report recorded a compensatory RNA-processing module and convergence with `Cdc40`, `U2af2`, `Snrnp70`, and `Rnpc3`; the 151 signature also carried p53/proteostasis/synaptic branches. This argues that direct splicing collapse would be visible, but not that every nuclear RNA helicase should have hundreds of DEGs. |
| `Hnrnpc` | 122 | An abundant hnRNP perturbation with a moderate 151 response. Its limited 33-gene FDR overlap with `Hnrnpu` and the corpus statement that hnRNP-family perturbations did not phenocopy `Hnrnpu` make it a counterexample to generic abundant-RNP extrapolation. |
| `Nop56` | 25 | Nucleolar box C/D snoRNP/rRNA-processing loss produced a narrow 151 response dominated by decreased RNA-processing/SR-splicing transcripts (`Rsrp1`, `Ddx17`, `Srsf5`, `Srsf11`, `Ddx5`, `Srsf6`, `Pabpn1`, `Clk4`, `Srrm2`, `Fus`, `Hnrnpu`) and only 25 FDR genes at 0.05. This is a closer scale prior for a nuclear helicase that is important but not itself a core spliceosome component. |
| `Ddx3x` | 8 | The nearest visible DExD/H helicase perturbation with a corpus report. It produced only 8 FDR<0.05 genes in 151 cells (`Ddx3x`, `Ypel3`, `Grin2b`, `Synpo2`, `Plekhg1`, `Tcea2`, `Tmsb10`, `Ccdc136`) and was not phenocopied by `Ddx39b` or translation-initiation relatives. This is a weak-helicase lower-bound prior. |
| `Eif4a2`, `Eif4g1`, `Eif4h`, `Ddx39b` | 2, 1, 1, 0 | These were nearly flat in the same endpoint. They argue strongly against assigning a broad response solely from DExD/H helicase or RNA-translation membership. |

Pairwise score correlations within 151 cells were positive but modest even among broad spliceosome perturbations (`Rnpc3` versus `Prpf6` `r = 0.278`; `Rnpc3` versus `U2af2` `r = 0.203`; `Rnpc3` versus `Cdc40` `r = 0.177`), and almost absent for `Ddx3x` versus `Hnrnpu`, `Hnrnpc`, or `Ddx39b` (`r` approximately 0.0). I therefore used the counts as coarse response-breadth anchors, not as a literal nearest-neighbor average.

# Target-specific reasoning for `Dhx9`

DHX9/RNA helicase A is a nuclear DExH helicase with RNA/DNA-hybrid, R-loop, and transcriptional roles. The external evidence makes complete `Dhx9` loss clearly deleterious during development: germline RHA-null mice die around gastrulation with embryonic-ectoderm apoptosis, and heterozygous human DHX9 loss-of-function variants have now been linked to neurodevelopmental disease. Its chromatin/R-loop work also links it to RNA Pol II and promoter control rather than to one narrow cytoplasmic translation-initiation branch. Those facts push the prediction away from a confident zero.

The acute PerturbAI endpoint, however, is a 3-4 week, sparse P16 neuronal CRISPR readout among recovered NeuN-positive nuclei. R-loop-associated replication stress is muted in postmitotic neurons relative to proliferating embryonic ectoderm or intestinal stem cells, and the same dataset shows that strong developmental essentiality does not automatically produce a broad survivor-state nuclear RNA signature. Among training genes, direct DExD/H or helicase-like analogs were small: `Ddx3x` had 8 DEGs, `Ddx39b` had 0, and translation-initiation relatives had 0-2. The stronger nuclear RNP responses bracket `Dhx9` from above but are imperfect: `Hnrnpu` is a chromatin/RNA scaffold and disease gene with a 733-DEG thalamic response, while `Hnrnpc` was only 122 and did not phenocopy `Hnrnpu`. Core spliceosome lesions (`Rnpc3`, `U2af2`, `Cdc40`, `Prpf6`) were far broader, but DHX9 is not an obligate U2/U5/minor-spliceosome subunit.

I therefore predicted a real but small 151-cell response, closer to `Ddx3x` and `Nop56` than to `Hnrnpu` or spliceosome factors. The expected intervention chain is: partial mosaic `Dhx9` disruption -> weaker DHX9 helicase activity at RNA-DNA hybrids/promoters and some RNA-processing contexts -> local transcription/R-loop stress in vulnerable thalamic neurons -> a small survivor-state RNA-processing/synaptic marker set. I do not expect the perturbation to reach the broad p53/proteostasis/apoptosis branch seen for `Prpf6` or the broad HNRNPU chromatin/RNA scaffold response. The point estimate is `12` DEGs, a nonzero but sub-95th-percentile response in the focal-cell training distribution.

# Limits

The main uncertainty is that no `Dhx9` expression signature exists in the supplied inputs. The prediction transfers from related RNA-processing perturbations that occupy different biochemical stages: a DEAD-box translation/RNP helicase (`Ddx3x`), a box C/D nucleolar factor (`Nop56`), hnRNP/chromatin factors, and core spliceosome genes. The broad training responses demonstrate assay sensitivity to nuclear RNA perturbations but do not prove DHX9 will converge on the same genes. Conversely, the near-null `Ddx3x`, `Ddx39b`, and eIF4F relatives show that helicase-family membership is not enough to call an effect absent or present. External DHX9 studies mostly use embryonic, cycling, cancer, or engineered systems, so their R-loop and lethality mechanisms are priors for molecular function, not direct measurements of postnatal thalamic glutamatergic survivor nuclei.
