# DEG-count prediction trace

## Question and endpoint

I interpreted the task as a point prediction of the number of FDR-significant whole-gene differential-expression calls for each held-out CRISPR loss-of-function target in `151 TH Prkcd Grin2c Glut` thalamic glutamatergic neurons.

The endpoint is `n_degs`: the count of measured genes with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` in perturbed nuclei versus the matched non-targeting controls. The requested target set contains one unranked target, `Rbfox1`; file order therefore only fixes output order. `Rbfox1` is absent both from the focal training-count CSV and from the declared differential-expression Parquet as a `gene_target`.

## Sources used

- Declared training DEG-count table: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, the authoritative endpoint for visible targets in the focal cell group.
- Declared all-cell differential-expression Parquet: `training_de_all_cell_groups.parquet`, queried with DuckDB for exact focal signatures and to check candidate comparator presence.
- Requested-target manifest: `b0030.csv`.
- PerturbAI whole-brain atlas July same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`, through the run-local Findings and Evidence ledgers. I treated this as an interpreted representation of the same experiment, not as independent validation.
- External PubMed literature for RBFOX biology:
  - Gehman et al. 2011, Nature Genetics, "The splicing regulator Rbfox1 (A2BP1) controls neuronal excitation in the mammalian brain", doi:10.1038/ng.841, PMID:21623373.
  - Lee et al. 2009, Genes & Development, "An inducible change in Fox-1/A2BP1 splicing modulates the alternative splicing of downstream neuronal target exons", doi:10.1101/gad.1837009, PMID:19762510.
  - Lee et al. 2015, Neuron, "Cytoplasmic Rbfox1 Regulates the Expression of Synaptic and Autism-Related Genes", doi:10.1016/j.neuron.2015.11.025, PMID:26687839.
  - Hamada et al. 2015, Molecular Autism, "Role of the cytoplasmic isoform of RBFOX1/A2BP1 in establishing the architecture of the developing cerebral cortex", doi:10.1186/s13229-015-0049-5, PMID:26500751.
  - Conboy 2016, Wiley Interdisciplinary Reviews: RNA, "Developmental regulation of RNA processing by Rbfox proteins", doi:10.1002/wrna.1398, PMID:27748060.

I did not use the disabled rank-calibration or predictive graph-review workbenches: the output here is a scalar count, not a ranked list with ranked or partially ranked supervision.

## Quantitative calibration

I first summarized the focal training endpoint. Among 1,674 visible biological perturbations, 1,205 had `n_degs = 0`, 469 were nonzero, the median was 0, the 75th percentile was 1, the 90th percentile was 2, the 95th percentile was 18, and the maximum was 2,677. Thus any nonzero prediction is already in the upper 28% of visible focal responses, and a prediction above about 20 requires evidence for a broad secondary abundance state rather than just known neuronal importance.

I then queried whether RBFOX paralogs were represented:

```sql
SELECT COUNT(*)
FROM parquet_scan('training_de_all_cell_groups.parquet')
WHERE gene_target IN ('Rbfox1','Rbfox2','Rbfox3');
```

This returned 0 rows, and `ILIKE 'Rbfox%'` returned no represented `gene_target`. There was therefore no same-family training perturbation with an observed 151-cell DEG count.

The most relevant visible RNA-processing counts in the focal cell group were:

| training target | `n_degs`, FDR<0.05 | Interpretation |
| --- | ---: | --- |
| `Rnpc3` | 868 | U11/U12 minor-spliceosome factor; very broad secondary abundance response. |
| `U2af2` | 828 | Major-spliceosome 3-prime splice-site factor; very broad response. |
| `Hnrnpu` | 733 | hnRNP plus chromatin-scaffold factor; broad response with RNA-processing, ISR/proteostasis, and synaptic-state modules. |
| `Cdc40` | 624 | activated spliceosome / PRP17 factor; broad response. |
| `Prpf6` | 454 | U4/U6-U5 tri-snRNP factor; broad response. |
| `Snrnp70` | 213 | U1 snRNP component; broad response. |
| `Tardbp` | 210 | sequence-specific RNA-binding protein, but TDP-43 has broad RNA metabolism and stress biology. |
| `Hnrnpc` | 122 | hnRNP C; weaker, still clearly nonzero and spliceosome-adjacent. |
| `Hnrnpa2b1` | 11 | hnRNP-family RNA-binding perturbation with a narrow focal signature. |
| `Atxn2` | 8 | RNA metabolism / stress-granule factor with a narrow focal signature, including `Srsf11` and `Rsrp1`. |
| `Adarb1` | 4 | RNA-editing enzyme with a very small focal abundance signature. |
| `Hnrnph2` | 4 | hnRNP-family RNA-binding perturbation with a tiny focal signature. |
| `Hnrnpdl` | 1 | nearly silent focal hnRNP-family perturbation. |
| `Aff2` | 0 | RNA/splicing-associated regulator with no broad steady-state abundance response. |

Raw Parquet inspection of `151 TH Prkcd Grin2c Glut` confirmed that the broad spliceosome/hnRNP signatures were real multi-gene programs rather than count-table artifacts: for example `Rnpc3` had extremely significant `Rnpc3`, `Amy1`, `Mapk8`, `Ap2a1`, `Pcyt2`, `Wdfy1`, and `Srp72` calls; `U2af2` had `Rsrp1`, `Srrm2`, `Atp2a2`, `Agrn`, and `Luc7l2`; `Cdc40` had `Srrm2`, `Ogt`, `Rack1`, `Pde4a`, `Tpr`, and `Leng8`; and `Prpf6` had `Ogt`, `App`, `Thy1`, `Snrpn`, and `Mapk10`. The same-experiment corpus independently summarized these as secondary RNA-processing, proteostasis, nuclear-transport, and synaptic-state abundance programs that converge among `Prpf6`, `Cdc40`, `U2af2`, `Snrnp70`, and `Rnpc3`, while warning that not every splicing target phenocopies: the Sm perturbation `Snrpb` was essentially flat.

## Target-specific reasoning

### `Rbfox1`

`Rbfox1` encodes a neuronal RNA-binding protein with nuclear isoforms that regulate UGCAUG-dependent alternative splicing and cytoplasmic isoforms that affect stability and translation of synaptic/autism-associated mRNAs. The external mouse literature predicts a real neuronal phenotype: CNS `Rbfox1` deletion caused neuronal hyperexcitability and seizures, with whole-transcriptome analysis showing many splicing changes but few changes in overall transcript abundance (Gehman et al. 2011). Depolarization can regulate Fox-1/Rbfox1 isoform choice and thereby tune neuronal splicing of ion-channel and synaptic transcripts (Lee et al. 2009), while cytoplasmic Rbfox1 controls synaptic mRNA abundance and translation in neurons (Lee et al. 2015). Developmental Rbfox1 perturbation affects cortical migration, axon extension, and dendritic/spine morphology (Hamada et al. 2015; Conboy 2016).

Those priors make a complete zero less likely than for an unrelated receptor or a development-only transcription factor, because RBFOX1 is neuronally expressed and can affect postmitotic synaptic RNA programs. They do not, however, justify placing `Rbfox1` with the 200 to 900 DEG core-spliceosome perturbations. `Rnpc3`, `U2af2`, `Cdc40`, `Prpf6`, and `Snrnp70` impair spliceosome assemblies or splice-site recognition itself, and the PerturbAI 151-cell signatures for those genes contain secondary collapse/compensation states over hundreds of whole-gene mRNAs. RBFOX1 is a sequence-specific regulatory RBP; its canonical endpoint is exon inclusion, and the strongest mouse CNS knockout evidence explicitly found limited total-mRNA abundance change despite many alternative-splicing changes. The declared 10x Flex V2 3-prime snRNA Wilcoxon table is therefore a weak proxy for the primary RBFOX1 molecular defect.

The nearest quantitative bracket is the lower RNA-binding tail rather than the core machinery: `Hnrnpa2b1` had 11 focal DEGs, `Atxn2` had 8, `Adarb1` and `Hnrnph2` had 4, `Hnrnpdl` had 1, and `Aff2` had 0. `Tardbp` and `Hnrnpc` were considered counterexamples because they are RNA-binding proteins rather than core snRNP parts, but both are broader stress/RNP perturbations in this screen; the same-experiment Hnrnpu and Hnrnpc reports also show that measured hnRNP-family perturbations were not interchangeable. The corpus contains several `Rbfox1`/`Rbfox2` abundance changes downstream of other perturbations, but these were isolated marker events, not evidence that `Rbfox1` knockout should generate a core-spliceosome-like whole-gene abundance state.

I therefore predict a small but nonzero 151-cell signature for `Rbfox1`, centered on the same scale as `Atxn2` and `Hnrnpa2b1`: enough secondary synaptic/RNA-processing abundance changes to clear FDR in the most responsive cell group, but far below the broad core-splicing and proteostasis-response counts.

Predicted count: **8**.

## Limits and uncertainty

- No `Rbfox1`, `Rbfox2`, or `Rbfox3` target perturbation is visible in the training data, so the prediction extrapolates from other RBPs and spliceosome factors rather than from a true paralog.
- The exact RBFOX1-regulated exon changes are not measured by the supplied gene-level 3-prime snRNA DE table. A strong isoform phenotype could still yield few or no whole-gene DEGs.
- External `Rbfox1` studies often use germline, CNS-wide, conditional, or in utero perturbations rather than sparse AAV CRISPR delivered at P16. Developmental migration phenotypes are therefore only weak priors for the P37-P44 survivor-conditioned thalamic abundance readout.
- The focal cell group is the most responsive class in the screen, which raises the chance of detecting a secondary signature, but the count remains assay- and power-dependent. The integer 8 should be read as a low-count point estimate, not as evidence that exactly eight named RBFOX1 targets are expected to change.
