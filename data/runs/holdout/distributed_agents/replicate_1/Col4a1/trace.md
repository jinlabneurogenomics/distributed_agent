# Col4a1 DEG-count prediction

## Question and endpoint

The target was to predict the held-out `n_degs` for `Col4a1` in `151 TH Prkcd Grin2c Glut` cells. I treated `n_degs` as exactly the training endpoint: the number of measured genes in that focal cell class with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` after acute mosaic AAV-PHP.eB CRISPR loss of function. `Col4a1` and the obligate partner `Col4a2` were confirmed absent as `gene_target` rows in the DE parquet and `Col4a1` was absent from the focal training-count CSV, so there was no direct expression signature to read or score.

## Sources

- Declared quantitative inputs: `training differential-expression dataset` and `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Requested targets: `single-target request for Col4a1`.
- Internal same-experiment corpus: PerturbAI July 260713 sourceguard 1773 v1 Findings and Evidence ledgers, queried through `corpus.findings`, `corpus.calibration`, `corpus.report_evidence`, and the bounded BioKG graph only to ask whether `Col4a1` appeared as a comparator. The graph result had no `Col4a1` comparator Finding; graph topology was not used as a score.
- External literature from PubMed for COL4A1/COL4A2 basement-membrane biology:
  - Kuo, Labelle-Dumais and Gould 2012, doi:10.1093/hmg/dds346, PMID 22914737.
  - Jeanne and Gould 2016, doi:10.1016/j.matbio.2016.10.003, PMID 27794444.
  - Mao et al. 2025, doi:10.1083/jcb.202409153, PMID 40279671.
  - Pokhilko et al. 2021, doi:10.1177/0271678X211004307, PMID 33730931.

The ranking-specific `dataset.perturbseq_features`, `corpus.predictive_graph_review`, and `synthesis.ordering_validate` capabilities were not available for this scalar count task and were not invoked.

## Quantitative comparisons

I used the focal-cell training-count table to inspect extracellular-matrix, collagen, integrin, vascular-receptor, and mural/endothelial analogs. The direct type IV collagen partner `Col4a2`, other type IV collagen alpha chains, basement-membrane laminins, `Nid1`, and `Hspg2` were not training targets, so they could not be used as measured same-complex analogs.

The measured focal counts instead supported a flat response for the queryable adjacent biology:

| training perturbation | relationship to `Col4a1` | observed focal `n_degs` |
|---|---|---:|
| `Col2a1` | structural collagen comparator, not a type IV basement-membrane partner | 0 |
| `Col11a1` | structural collagen comparator, not a type IV basement-membrane partner | 0 |
| `Itgb1` | core neuronal ECM receptor beta subunit | 0 |
| `Itga2` | collagen/ECM-binding integrin alpha family member | 0 |
| `Itga6` | laminin-binding integrin alpha family member | 0 |
| `Itga8` | beta1-pairing ECM integrin alpha family member | 0 |
| `Kdr` | VEGFR2, endothelial angiogenic receptor | 0 |
| `Tek` | Tie2, endothelial receptor tyrosine kinase | 0 |
| `Pdgfrb` | pericyte/vascular mural receptor | 0 |
| `Abcc9` | mural-cell KATP channel gene | 0 |
| `Cspg4` | pericyte/NG2 marker | 0 |
| `Flt4`, `Nrp1`, `Nrp2`, `Plxnd1` | VEGF/Sema vascular signaling comparators | 0 each |

I then queried the focal rows in the Parquet for these analogs. In `151 TH Prkcd Grin2c Glut`, all of `Abcc9`, `Adamts17`, `Col11a1`, `Col2a1`, `Itga2`, `Itga2b`, `Itga4`, `Itga6`, `Itga7`, `Itga8`, `Itga9`, `Itgb1`, `Itgb2`, `Kdr`, `Pdgfrb`, and `Tek` had 0 genes at both FDR < 0.05 and FDR < 0.10. Most minimum adjusted p-values were exactly 1.0; the lowest for this set was 0.274 for `Adamts17`, far above the requested 0.05 threshold. The matched-cell counts were not the limiting problem in the focal class: examples included 110 perturbed `Itgb1`, 167 `Kdr`, 184 `Tek`, 195 `Pdgfrb`, 154 `Itga2`, 165 `Itga6`, and 304 `Col2a1` nuclei versus 23,679 controls.

The Parquet also showed that `Col4a1` and `Col4a2` can be detected as measured transcripts in this focal class under very broad regulator perturbations: `Col4a1` was significant after `Hnrnpu`, `Rnpc3`, `Nr1d1`, `Cic`, `Ppm1g`, `Thoc1`, `Cdc40`, `Bmal1`, and `Snrnp70`; `Col4a2` was significant after several RNA-processing or transcriptional regulators including `Elp1`, `Hnrnpu`, `Tardbp`, `Zbtb7a`, `Ppm1g`, `Gigyf2`, `Thoc1`, and `Bmal1`. Those are counterexamples to a simple "COL4A genes are never measurable" explanation, but they are not mechanistic analogs of losing a secreted basement-membrane chain: in the focal training counts, `Hnrnpu`, `Rnpc3`, `Elp1`, `Zbtb7a`, and `Cic` caused hundreds of DEGs and acted as broad nuclear regulators.

## Same-experiment corpus evidence

The selected July sourceguard corpus had no direct `Col4a1` report and no BioKG `REPORTS_GENE` comparator hit for `Col4a1`, so the internal report layer did not supply a held-out signature by leakage.

It did provide relevant same-experiment interpretations for adjacent training targets:

- `Itgb1`: July Finding `Itgb1:F001` summarized 21 recovered neuronal groups with zero downstream genes at FDR < 0.10, including `151 TH Prkcd Grin2c Glut` with 110 perturbed cells and 0 downstream genes. `Itgb1:F002` compared represented integrin subunits and found that `Itga2`, `Itga2b`, `Itga4`, `Itga7`, `Itga9`, and `Itgb2` had no FDR-supported downstream genes, while `Itga6` and `Itga8` had only isolated one-gene effects in other cell classes. This makes beta1/integrin extracellular-matrix signaling an experimentally measured null or near-null family in the same acute postnatal neuronal assay.
- `Kdr`: July Finding `Kdr:F001` reported an almost completely flat neuronal surface, with no canonical VEGF/endothelial transcriptional program; in the focal class, `Kdr:E018` had 167 perturbed cells and 0 downstream genes at FDR < 0.10 with minimum adjusted p = 1.0. `Kdr:F005` explicitly warned that the neuronal null should not be read as a vascular null because the assay enriched NeuN+ nuclei.
- `Pdgfrb`: July Finding `Pdgfrb:F001` reported no robust downstream response in the measured NeuN+ neuronal groups and interpreted that result as consistent with the major adult brain role of PDGFR-beta being vascular mural/pericyte biology rather than acute neuronal transcription.

These same-experiment reports are derived from the same DE dataset, so I used them for interpretation and for their bounded, checked comparator lists, not as independent replication.

## Biological rationale for `Col4a1`

External biology sets a vascular basement-membrane prior for `Col4a1`. COL4A1 and COL4A2 form collagen IV alpha1-alpha1-alpha2 heterotrimers that are fundamental constituents of basement membranes, and dominant COL4A1/COL4A2 mutations cause multisystem disease with a strong cerebrovascular-small-vessel component (Kuo et al. 2012; Jeanne and Gould 2016). Proteomic enrichment of human and mouse cerebrovascular ECM identifies COL4A1/COL4A2 within the brain vascular matrisome and links that matrix to cerebrovascular disease genes (Pokhilko et al. 2021). A mouse tagged/null Col4a1 allele further showed active COL4A1 turnover in postnatal cerebrovascular basement membranes, but also that heterozygous Col4a1 deletion was substantially less pathogenic than dominant missense alleles (Mao et al. 2025).

The expected causal chain for the held-out perturbation is therefore:

`Col4a1` CRISPR in sparse NeuN+ postmitotic neurons -> reduced production of a secreted type IV collagen alpha1 chain in any edited neuron expressing it -> possible change in local extracellular basement-membrane collagen IV assembly only if that neuron is a limiting source -> weak or no propagation to endothelial/pericyte basement membrane, because those lineages are not the perturbed, recovered NeuN+ compartment -> little survivor-conditioned nuclear RNA response in thalamic glutamatergic nuclei.

That chain differs from a dominant missense COL4A1 disease allele, where retained mutant procollagen, ER stress, extracellular matrix deficiency, vascular smooth muscle or endothelial dysfunction, and developmental basement-membrane defects can all matter. This experiment is a partial, acute loss-of-function screen in postnatal recovered neurons; it is not a vascular-cell Col4a1 deletion, a germline collagen IV mutant, or a gain-of-toxic-chain model.

Given that the closest measured ECM receptor arm (`Itgb1` and integrin alpha partners) and vascular/pericyte arms (`Kdr`, `Tek`, `Pdgfrb`, `Abcc9`, `Cspg4`) are null in the focal class, a broad COL4A1-induced thalamic transcriptional program is unlikely. I therefore predicted a true zero rather than a small nonzero singleton.

## Limits

- The strongest mechanistic partner, `Col4a2`, and the canonical basement-membrane genes `Lama1/Lamb1/Lamc1/Nid1/Hspg2` were absent from the training perturbations, so the prediction relies on more distant collagen, integrin, and vascular analogs.
- NeuN+ FACS largely removed endothelial cells, pericytes, vascular smooth muscle, astrocytes, and microglia. The prediction is only for recovered `151 TH Prkcd Grin2c Glut` nuclei and should not be read as a prediction about cerebrovascular basement-membrane structure or hemorrhage risk.
- The Parquet has no raw UMI matrix and no baseline abundance; `Col4a1` downstream FDR hits after broad nuclear regulators prove measurability under large perturbations but do not quantify whether thalamic neurons are a physiologic source of COL4A1 protein.
- The DEG count is assay- and power-dependent. Low target-RNA depletion in a self row would not prove failed editing; conversely, a predicted zero means no measured transcript is expected to pass FDR 0.05, not that the edited cells have no local extracellular phenotype.

## Final point prediction

`Col4a1`: **0** DEGs.
