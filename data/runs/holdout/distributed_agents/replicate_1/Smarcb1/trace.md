# DEG-count prediction for held-out Smarcb1

## Question and endpoint

I predicted the held-out `n_degs` for the `Smarcb1` perturbation in `151 TH Prkcd Grin2c Glut` cells. The endpoint is the focal-cell count of measured genes with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` after acute, sparse AAV-CRISPR loss of the requested gene in postnatal mouse neurons. Zero means no recovered nuclear transcript reached FDR 0.05; a positive value is a point estimate for this assay- and power-dependent response breadth.

The target list contains one unranked requested target, `Smarcb1`. I checked that it is absent from the focal training counts and absent as `gene_target` from the declared differential-expression Parquet, so no observed `Smarcb1` endpoint or signature was available in the supplied input.

## Sources used

- Declared training endpoint: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression matrix: `training differential-expression dataset`.
- Run-local held-out manifest: `single-target request for Smarcb1`.
- Same-experiment internal corpus: `perturbai-july-260713-sourceguard-1773-v1`, especially the Arid1a, Arid2, Smarca4, Smarcc1, Smarcc2, Smarcd1, and Smarce1 Finding/Evidence summaries. This corpus is an interpretation layer over the same Perturb-seq experiment, not independent replication.
- External mechanism literature:
  - Chen et al. 2020, Cell Discovery, doi:10.1038/s41421-020-00196-4, PMID:33024572, for evidence that a heterotrimeric SMARCB1-SMARCC2 subcomplex contributes to BAF assembly.
  - He et al. 2020, Science, doi:10.1126/science.aaz9761, PMID:32001526, and Mashtalir et al. 2020, Cell, doi:10.1016/j.cell.2020.09.051, PMID:33053319, for BAF structural models placing SMARCB1 at a nucleosome-facing interface with SMARCC/ARID1A scaffold modules.
  - Wu et al. 2007, Neuron, doi:10.1016/j.neuron.2007.08.021, PMID:17920018, and Staahl et al. 2013, Journal of Neuroscience, doi:10.1523/JNEUROSCI.1258-13.2013, PMID:23785148, for neuron-specific BAF complexes and the postmitotic switch from progenitor BAF toward nBAF.
  - Valencia et al. 2023, Nature Genetics, doi:10.1038/s41588-023-01451-6, PMID:37500730, and Vasko et al. 2021, Genes, doi:10.3390/genes12060937, PMID:34205270, for mSWI/SNF/BAF genes, including `SMARCB1`, as neurodevelopmental-disease/Coffin-Siris genes with subunit-specific genotype-phenotype relationships.

## Quantitative work

I first read the 1,674 visible focal-cell training counts. The distribution is zero-heavy: 469/1,674 perturbations are nonzero, the median is 0, the 75th percentile is 1, the 95th percentile is 18, the 99th percentile is 436, and the maximum is 2,677. Thus any estimate above roughly 20 DEGs is already a high-percentile response in this exact endpoint.

I then intersected the training set with BAF/SWI/SNF and adjacent chromatin targets and queried the Parquet only for those perturbations. The focal-cell FDR 0.05 counts were:

| training perturbation | `151 TH Prkcd Grin2c Glut` `n_degs` | interpretation for `Smarcb1` |
| --- | ---: | --- |
| `Smarcc2` | 185 | Strongest represented BAF response. SMARCC2/BAF170 is a scaffold/core-family component and the same-experiment corpus records same-direction convergence with `Arid1a` and `Smarce1`; Chen et al. specifically link SMARCB1-SMARCC2 to BAF assembly. This is the upper analog, but it is not exact because `Smarcc2` can affect assemblies and dosage relationships not identical to SMARCB1 loss. |
| `Arid2` | 56 | PBAF-specific ARID subunit with a clear 151 response. It shares part of the BAF thalamic module with `Smarcc2` but also carries ARID2/PBAF-specific adhesion and glycosylation outputs, so it is a useful moderate counterpoint rather than the primary `Smarcb1` analog. |
| `Arid1a` | 22 | cBAF ARID selector. In the internal corpus, `Arid1a` is closest to `Smarcc2` and `Smarce1` on its 151 FDR<0.10 genes; the overlap with `Smarcc2` is all same-direction and includes `Ptpn3`, `Begain`, `Ptprz1`, `Prkcb`, `Nexn`, and `Clstn2`. This is the best focal cBAF selector analog. |
| `Smarce1` | 11 | Small but robust core-like BAF response in the same cell group, overlapping `Smarcc2` and `Arid1a` on `Ptpn3`, `Begain`, `Lrrc7`, `Rasa4`, and related genes. It supports a nonzero cBAF-core response but also shows that a core subunit can produce only tens of DEGs. |
| `Smarcd1` | 1 | Weak same-module comparator: the corpus reports only a narrow 151 effect, with `Ankrd40` up and `Ptpn3` down at FDR<0.10. |
| `Arid1b` | 1 | ARID1A paralog in cBAF, but its acute postnatal neuronal effect is buffered; it is a strong counterexample to treating every cBAF subunit as equivalent. |
| `Smarca2` | 1 | Alternative ATPase; nearly flat in 151 and a counterexample to a generic BAF-core heuristic. |
| `Smarcc1` | 0 | SMARCC2 paralog BAF155; flat in the focal group despite the `Smarcc2` response. |
| `Smarca4` | 0 | BRG1 ATPase; flat in the focal group and across the recovered groups at FDR<0.10, arguing that `Smarcb1` should not inherit a broad BRG1 developmental phenotype. |
| `Bicra` | 0 | Noncanonical BAF-related target; flat in 151 and mechanistically more distant from SMARCB1-containing cBAF. |
| `Bcl11a`, `Bcl11b` | 0 | BAF-interacting neuronal factors queried as distant counterexamples; neither supports a `Smarcb1` count. |

For the active BAF comparators, direct Parquet rows in `151 TH Prkcd Grin2c Glut` confirmed a recurrent same-direction module rather than only similar totals. At FDR<0.10, `Arid1a` and `Smarcc2` shared 16 genes, all in the same direction; `Smarcc2` and `Smarce1` shared 12, all in the same direction; `Arid1a` and `Smarce1` shared 5, all in the same direction; `Arid2` overlapped `Smarcc2` on 20 genes, with 17 same-direction and 3 opposite. The recurring down-regulated thalamic markers included `Ptpn3`, `Begain`, `Lrrc7`, `Rasa4`, `Prkcb`, `Prkcd`, `Reep2`, and `Abhd12b`, with positive arms such as `Nexn`/`Clstn2` strongest in `Smarcc2` and `Arid1a`.

An all-cell-group Parquet scan over the represented BAF perturbations showed that these are focal 151 responses rather than a pan-neuronal chromatin-collapse state: `Arid1a`, `Arid2`, `Smarce1`, and `Smarcd1` had their only multi-gene FDR signal in `151 TH Prkcd Grin2c Glut`; `Smarcc2` had 185 FDR 0.05 genes in 151 and only one-gene hits in `066 CNU-HYa HY GABA`, `145 MH-LH TH Glut`, and `155 MB Glut`; `Smarcc1` was significant for only one gene in `155 MB Glut`; and `Smarca4`/`Bicra` had no FDR<0.10 hits in the represented groups.

## Target-specific prediction

### Smarcb1

`Smarcb1` encodes SNF5/INI1, a conserved mammalian BAF subunit with no close measured paralog that can be substituted one-for-one. Structural and biochemical studies put SMARCB1 in canonical BAF assemblies at an interface with SMARCC/ARID1A modules and nucleosomal H2A/H2B acidic patches, and Chen et al. showed that SMARCB1-SMARCC2 participates directly in BAF assembly. Its loss should therefore perturb the same cBAF scaffold that generated the observed thalamic `Smarcc2`/`Arid1a`/`Smarce1` signature. The causal transfer chain is: acute CRISPR disruption of `Smarcb1` -> reduced functional SNF5-containing cBAF complexes rather than an isolated DNA-binding factor -> impaired maintenance of cBAF-dependent chromatin access at a subset of thalamic neuronal loci -> recurrent down-regulation of synaptic, adhesion, kinase/phosphatase, and extracellular-interface genes in recovered `151 TH Prkcd Grin2c Glut` nuclei -> a positive FDR count.

The same chain does not justify assigning the full `Smarcc2` count of 185. `Smarcc2` is the broadest BAF response in this cell group and may include BAF170-specific dosage effects. Several very plausible BAF relatives were nearly flat: `Smarca4` and `Smarca2` show that a single ATPase subunit can be buffered, `Smarcc1` shows that the SMARCC scaffold paralogs are not interchangeable here, and `Arid1b`/`Smarcd1` show that membership in the thalamic module can collapse to one significant gene. The positive `Smarce1` and `Arid1a` counts instead place a plausible cBAF-core response in the 10-30 DEG range, with `Arid2` as a moderate 56-DEG upper counterexample. I therefore predicted a small but clearly nonzero focal response, somewhat above `Arid1a`/`Smarce1` because SMARCB1 is structurally closer to the SMARCC2 scaffold than an ARID selector, but far below `Smarcc2` because the training data reject simple one-complex-one-count transfer.

Final point prediction: **32 DEGs**.

## Limits

This is extrapolation from related perturbations: the declared input contains no `Smarcb1` rows, no DNA indel calls, no protein abundance, no chromatin accessibility, and no pre-assay abundance or survival endpoint. The BAF comparators come from the same Perturb-seq experiment and are excellent endpoint calibration but not independent replication. External SMARCB1 literature is mostly biochemical, embryonic, cancer, or human-genetic; it establishes that SMARCB1 is a cBAF/SWI-SNF component but does not directly measure sparse P16 CRISPR loss in postmitotic thalamic mouse neurons. The largest uncertainty is the balance between no-paralog cBAF disruption, which could make `Smarcb1` look like or exceed `Arid1a`, and survivor/dosage buffering, which made several famous BAF genes flat in this assay.
