# Question and resolved ambiguities

The held-out manifest for this run contains one perturbation:

```text
Trem2
```

I interpreted the requested endpoint as the integer count of measured genes in `151 TH Prkcd Grin2c Glut` whose Wilcoxon `pvals_adj` would fall below 0.05 after an acute, sparse AAV-CRISPR loss of `Trem2`, matching the training-count file. I did not treat `n_degs` as a statement about edit formation, organismal phenotype, microglial viability, or target RNA down-regulation. The focal cell group is a NeuN-positive neuronal thalamic glutamatergic group; because microglia were deliberately absent or strongly depleted, the relevant question for `Trem2` is whether an immune/microglial receptor perturbation has an autonomous neuronal nuclear RNA response under basal juvenile conditions.

# Sources used

Primary same-experiment inputs:

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- `[local file: training_de_all_cell_groups.parquet]`
- `[local file: 244_Trem2.csv]`

Internal same-experiment knowledge:

- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`, using `target_context`, `expand_candidate_set`, and `candidate_set_topology` for represented immune/microglial perturbations.
- Distributed Agents runtime observed-profile tools, using `profile_compare`, `profile_inspect`, and `profile_cohort` on the focal `151 TH Prkcd Grin2c Glut` log-fold-change profiles.

External biology:

- NCBI PubMed searches over independent literature.
- Mecca et al. 2018, DOI `10.3390/ijms19010318`, PMID `29361745`: TREM2-DAP12 and CX3CL1-CX3CR1 are microglial axes in the CNS; TREM2 interacts with DAP12 to promote microglial activation, phagocytosis, and survival.
- Zhao et al. 2018, DOI `10.1016/j.neuron.2018.01.031`, PMID `29518356`: TREM2 binds amyloid-beta oligomers, the TREM2-DAP12 interaction is ligand-regulated, and TREM2 signals to SYK/GSK3-beta in microglia.
- Nugent et al. 2020, DOI `10.1016/j.neuron.2019.12.007`, PMID `31902528`: TREM2 is a microglial lipid sensor required for the transcriptional and cholesterol-handling response to chronic myelin phagocytosis.
- Konishi and Kiyama 2020, DOI `10.1016/j.neuint.2020.104878`, PMID `33049336`: review of the TREM2/DAP12 complex on microglial plasma membranes in homeostasis, development, and aging.
- Wang et al. 2022, DOI `10.1016/j.cell.2022.09.033`, PMID `36306735`: TREM2-family plaque responses use DAP12/SYK-dependent and DAP10-dependent signaling to produce disease-associated microglial states.

# Same-experiment computations

I read the requested-target CSV and confirmed that only `Trem2` needed a prediction. I then read the focal training count table and summarized its empirical response scale:

- Training perturbations in `151 TH Prkcd Grin2c Glut`: 1,674.
- Median `n_degs`: 0.
- Nonzero `n_degs`: 469; therefore 1,205 training perturbations were exactly zero.
- 75th percentile: 1 DEG.
- 95th percentile: 18 DEGs.
- Maximum: 2,677 DEGs.

The distribution is strongly zero-inflated, so a held-out target should only be assigned a positive count if there is either a close neuronal same-pathway analog or a strong reason to expect a basal cell-autonomous thalamic neuronal program.

For the mechanistic analogs and counterexamples, I used the parquet in two ways.

First, I queried the focal-group rows for a curated TREM2-relevant panel:

| target | focal observed `n_degs` | expression-pattern evidence in `151 TH Prkcd Grin2c Glut` |
|---|---:|---|
| `Csf1r` | 0 | 17,259 readout genes, 0 with `pvals_adj < 0.05`, minimum adjusted p = 1.0 |
| `Cx3cr1` | 0 | 17,259 readout genes, 0 significant, minimum adjusted p = 1.0 |
| `P2ry12` | 0 | 17,259 readout genes, 0 significant, minimum adjusted p = 1.0 |
| `Spi1` | 0 | 17,259 readout genes, 0 significant, minimum adjusted p = 1.0 |
| `Abca7` | 0 | 17,259 readout genes, 0 significant, best adjusted p = 0.334 |
| `Abca1` | 0 | 17,259 readout genes, 0 significant, minimum adjusted p = 1.0 |
| `Axl` | 0 | 17,259 readout genes, 0 significant, best adjusted p = 0.363 |
| `Mertk` | 0 | 17,259 readout genes, 0 significant, best adjusted p = 0.888 |
| `Tlr2` | 0 | 17,259 readout genes, 0 significant, minimum adjusted p = 1.0 |
| `Tlr4` | 0 | 17,259 readout genes, 0 significant, minimum adjusted p = 1.0 |
| `Ccr2` | 0 | count-table zero in the focal group |
| `P2ry14` | 0 | count-table zero in the focal group |
| `Cd14` | 0 | count-table zero in the focal group |
| `Cd36` | 0 | count-table zero in the focal group |
| `C3` | 0 | count-table zero in the focal group |
| `Irf3`, `Irf5`, `Nfkb1`, `Rel`, `Traf3`, `Map3k7`, `Chuk`, `Il1r1`, `Itgb2` | all 0 | count-table zero in the focal group |

The closest exact TREM2 signalosome members in public biology, including `Tyrobp/Dap12`, `Syk`, `Plcg2`, `Inpp5d`, and `Apoe`, were not represented as training perturbations in this focal count table. That forced the transfer to use lineage and pathway neighbors rather than an obligate same-complex knockout.

Second, I used the runtime profile tools with the focal parquet rows, `entity_column = gene_target`, `feature_column = names`, `value_column = logfoldchanges`, `significance_column = pvals_adj`, and `significance_threshold = 0.05`. The 10-node immune/microglial analog panel `Csf1r, Cx3cr1, P2ry12, Spi1, Abca7, Abca1, Tlr2, Tlr4, Axl, Mertk` had zero significant features for every node. Across its 45 pairwise focal-group comparisons, the significant-program-overlap count was zero. The top-tail overlaps among the nonsignificant ranks were shallow: mean positive-tail overlap coefficient 0.073 and mean negative-tail overlap coefficient 0.137. Thus the relevant training perturbations were not hiding a shared low-FDR or near-threshold module that could justify a small positive prediction for `Trem2`.

The Distributed Agents corpus had no direct `Trem2` entry, so I expanded from represented first-hop microglial/AD anchors (`Csf1r`, `Cx3cr1`, `P2ry12`, `Abca7`) into the eligible training universe. It nominated six recurrent candidates:

| candidate | disposition | reason |
|---|---|---|
| `Spi1` | keep | Myeloid/microglial transcriptional regulator; focal `n_degs = 0` and no focal significant features. |
| `Axl` | keep | TAM phagocytic receptor, biologically adjacent counterexample to TREM2-mediated phagocytosis; focal `n_degs = 0`. |
| `Mertk` | keep | TAM phagocytic receptor and strong AXL partner/counterexample; focal `n_degs = 0`. |
| `Ccr2` | keep | Immune chemokine receptor counterexample, less close to TREM2 than CX3CR1/P2RY12; focal `n_degs = 0`. |
| `P2ry14` | keep | P2Y-family immune receptor next to `P2ry12`; useful as a broad lineage counterexample; focal `n_degs = 0`. |
| `Unc13b` | reject | It appeared only through near-zero flat-profile neighbor findings for `Abca7`/`Csf1r`, not through microglial TREM2 mechanism. I did not use it to set the estimate. |

Topology over the expanded 10-node candidate set showed a connected report graph and a fully connected seven-node core containing `Abca7, Axl, Csf1r, Cx3cr1, Mertk, P2ry12, Spi1`; all seven had `0` focal DEGs. I used that as same-experiment evidence that screened microglial, phagocytic, and AD-related receptors were collectively silent in this neuronal context.

# Target-specific reasoning

## Trem2

TREM2 is a myeloid/microglial surface receptor rather than a thalamic glutamatergic neuronal transcription factor. Its best-characterized CNS effects require receptor-positive microglia, the DAP12/TYROBP and DAP10 adapters, SYK-family signaling, lipids or amyloid/myelin ligands, and phagocytic or plaque/injury/demyelination settings. The current assay is deliberately different: AAV CRISPR at P16, sparse mosaic loss of function, healthy juvenile-to-young-adult brain, NeuN-positive nuclear enrichment, and a readout in `151 TH Prkcd Grin2c Glut` neurons. A direct TREM2-DAP12 microglial program therefore has no obvious cell type in which to appear.

Within the same dataset, the relevant represented microglial-lineage analogs all support a zero:

- `Csf1r`, a central microglial survival receptor, had `0` focal DEGs and a focal minimum adjusted p of `1.0`. The Distributed Agents `Csf1r` report explicitly noted that `Csf1r`, `Cx3cr1`, `Spi1`, and `Irf8` were flat in the NeuN-positive neuronal readout and that `Trem2`/`Tyrobp` themselves were absent as perturbation targets.
- `Cx3cr1`, the microglial fractalkine receptor, had `0` focal DEGs and all adjusted p-values equal to `1.0` in the focal group. This is a strong cell-lineage counterexample because CX3CL1-CX3CR1 is another neuron-microglia signaling axis whose productive receptor side is microglial.
- `P2ry12` and `P2ry14`, homeostatic/microglial purinergic receptors, both had `0` focal DEGs. The corpus linked `P2ry12` with `Cx3cr1`, `Csf1r`, `Axl`, and `Mertk` as a shared flat neuronal surface rather than a recurrent RNA module.
- `Spi1` had `0` focal DEGs. Because PU.1/SPI1 is a core myeloid transcriptional regulator, its flat profile argues that the screen did not contain the myeloid state that would make an immune receptor perturbation visible.
- `Axl` and `Mertk`, TAM-family phagocytic receptors that are pathway-adjacent to apoptotic-cell clearance, each had `0` focal DEGs. These are not TREM2 subunits, but they test the idea that a microglial phagocytic receptor might drive an autonomous neuronal state in the same screen; it did not.
- `Abca7` and `Abca1`, lipid/phagocytosis and AD-related comparators, both had `0` focal DEGs. Their profiles lacked a lysosomal or cholesterol-efflux compensation program even though the same dataset can detect strong sterol/endolysosomal programs after targets such as `Srebf2` or `Rab7`.
- `Tlr2`, `Tlr4`, `Cd14`, `Cd36`, `C3`, and NF-kappaB/IRF-pathway targets were also zero in the focal group, giving broad counterevidence against a tonic innate-inflammatory module in unstimulated neurons.

The only counterpressure is that TREM2 biology is real and potent in the correct compartment: TREM2 loss alters amyloid-plaque microglia, DAM induction, and lipid handling in disease or demyelination models. That biology is displaced from this assay rather than disproven by it. There is also no exact `Tyrobp` or `Syk` knockout in the training set, so the estimate extrapolates from nearby immune receptors and microglial lineage regulators. Even with those caveats, every dataset-visible analog in the focal group is a zero and none carries an FDR-supported expression pattern. I therefore predicted no BH-significant genes for `Trem2` in `151 TH Prkcd Grin2c Glut`.

Final point prediction:

| target | predicted `n_degs` |
|---|---:|
| `Trem2` | 0 |

# Limits

The evidence is strong for the assayed neuronal compartment but indirect for TREM2 itself. The same-experiment data do not include `Trem2`, `Tyrobp`, `Syk`, `Plcg2`, `Inpp5d`, or `Apoe` as perturbations, so the prediction relies on lineage analogs and phagocytic/innate-immune counterexamples. NeuN enrichment means the experiment could easily miss microglial TREM2 effects that would be obvious in microglia or after amyloid, myelin, apoptotic-cell, injury, or aging challenges. The CRISPR design also measured transcriptomes, not DNA indels, receptor surface protein, phagocytosis, plaque compaction, or cholesterol flux. Thus `0` should be read as a prediction for this exact focal Wilcoxon DEG endpoint, not as a claim that TREM2 is biologically inert in brain.
