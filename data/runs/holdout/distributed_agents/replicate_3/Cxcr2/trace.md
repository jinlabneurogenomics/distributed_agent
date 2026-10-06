## Question and resolved ambiguities

The requested held-out target list for this run contains one perturbation, `Cxcr2`. I interpreted `n_degs` as the exact focal-cell endpoint used in the training CSV: the number of measured genes with `pvals_adj < 0.05` after Benjamini-Hochberg correction in `151 TH Prkcd Grin2c Glut` cells.

The focal group name in the files is `151 TH Prkcd Grin2c Glut`, so I used that literal value when querying the parquet. A prediction of `0` means that no downstream measured gene is expected to pass FDR 0.05; it does not mean CXCR2 is unimportant in neutrophils, microglia, oligodendrocyte precursors, inflammation, development, or drug response.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`, the observed focal-cell DEG counts for 1,674 non-held-out perturbations.
- `[local file: training_de_all_cell_groups.parquet]`, queried at `group_name == "151 TH Prkcd Grin2c Glut"` for signed log2 fold-change and adjusted-p-value evidence for chemically and biologically related perturbations.
- Distributed Agents same-experiment corpus release `perturbai-july-260713-sourceguard-1773-v1`. `target_context("Cxcr2")` returned no direct held-out findings, as expected; I used the corpus findings and claims for the assayed chemokine/neuroimmune receptors `Ccr2`, `Cx3cr1`, and `Cxcr4`, especially the claim that represented chemokine receptors and Rac-arm perturbations did not create a common postmitotic neuronal transcriptional program in the NeuN-positive screen.
- PubMed for external biology:
  - Tsai et al. 2002, Cell, PMID 12176324, DOI 10.1016/S0092-8674(02)00838-3: CXCL1/CXCR2 signaling arrests oligodendrocyte precursor migration and helps position OPCs in developing mouse spinal cord.
  - Padovani-Claudio et al. 2006, Glia, PMID 16886211, DOI 10.1002/glia.20383: germline `Cxcr2` deficiency alters adult oligodendrocyte lineage cells, myelin, and white matter.
  - Lindner et al. 2008, Glia, PMID 18442092, DOI 10.1002/glia.20682: CXCR2 is constitutively expressed on OPCs and induced on macrophages/microglia during cuprizone demyelination, but `Cxcr2` knockout did not block remyelination in that model.
  - Van Damme et al. 1997, Journal of Leukocyte Biology, PMID 9365109, DOI 10.1002/jlb.62.5.563: CXCR2-family ELR+ CXC chemokines act as neutrophil chemoattractants and activators.

## Computational checks

I loaded the training-count CSV and searched for assayed chemokine receptors, inflammatory receptors, cytokine receptors, GPCRs, and proximal CXCR2 pathway genes. The focal `n_degs` counts were:

| training target | focal `n_degs` | why I treated it as relevant |
| --- | ---: | --- |
| `Ccr2` | 0 | chemokine GPCR whose principal biology is inflammatory monocyte/macrophage recruitment; a strong off-lineage comparator for basal neurons |
| `Cx3cr1` | 0 | chemokine/neuroimmune receptor concentrated on microglia in the brain |
| `Cxcr4` | 0 | the nearest assayed CXC chemokine GPCR with strong CNS developmental roles through the CXCL12/CXCR4/ACKR3 axis |
| `Csf1r`, `Csf3r` | 0, 0 | myeloid/granulocyte cytokine receptors, useful lineage counterexamples |
| `Ifnar1`, `Ifnar2`, `Ifngr1`, `Ifngr2` | 0, 0, 0, 0 | ligand-gated inflammatory JAK/STAT receptors |
| `Il1r1`, `Il6ra` | 0, 0 | cytokine receptors feeding inflammatory NF-kappaB/STAT signaling |
| `Tlr4`, `Nfkb1` | 0, 0 | innate receptor/core inflammatory transcriptional comparator |
| `Pik3cb`, `Pik3r1`, `Pik3r2` | 0, 0, 0 | PI3K components downstream of many GPCRs, including chemokine receptors |
| `Stat1`, `Stat3` | 1, 0 | cytokine/IFN transcriptional outputs; `Stat1`'s one focal DEG was `Stat1` itself |
| `Gnao1` | 1 | neuronal G-alpha subunit; the one focal DEG was `Gnao1` itself |

For the three assayed chemokine receptors in the focal group, I queried the parquet for all 17,259 measured genes:

| target | perturbed nuclei | control nuclei | FDR<0.05 genes | smallest focal FDR |
| --- | ---: | ---: | ---: | ---: |
| `Ccr2` | 170 | 23,679 | 0 | 1.000 |
| `Cx3cr1` | 258 | 23,679 | 0 | 1.000 |
| `Cxcr4` | 191 | 23,679 | 0 | 0.067 |

`Cxcr4` was the only one of these with even a near-miss in this focal cell group: `Pum1` log2FC `+0.45`, FDR `0.067`. That was still below the endpoint threshold, and the same-experiment Distributed Agents corpus described the wider `Cxcr4` response as only two isolated one-gene islands across its neuronal surface rather than a recurrent CXCR4 module.

I also compared signed focal `logfoldchanges` for a panel of 19 chemokine/cytokine/innate/PI3K/STAT/G-alpha perturbations with the Distributed Agents runtime. Among `Ccr2`, `Cx3cr1`, and `Cxcr4`, each profile had zero significant focal features. Top-200 tail overlap with inflammatory peers was low: for example, `Cxcr4` shared 15/200 positive-tail and 46/200 negative-tail genes with `Ccr2`, and only 12/200 to 21/200 positive-tail genes with the nearest immune-pathway peers. I therefore used their identical zero DEG counts as assay calibration, not as evidence for a coherent nonzero chemokine receptor signature.

## Target-specific reasoning

### `Cxcr2`

`Cxcr2` is a CXC chemokine GPCR for ELR+ chemokines such as CXCL1/CXCL2-related neutrophil chemoattractants. Its classic receptor-side biology is in granulocytes and inflammatory myeloid cells, and the CNS literature that gives it developmental relevance places much of the mouse brain-intrinsic signal in oligodendrocyte precursor cells and demyelination contexts. Tsai et al. showed that CXCL1/CXCR2 arrests OPC migration in developing spinal cord; Padovani-Claudio et al. found altered oligodendrocyte lineage and myelin structure in adult germline `Cxcr2` mutants; Lindner et al. observed CXCR2 on OPCs and inducibly on macrophages/microglia during demyelination.

Those functions are a poor match to this readout: AAV-PHP.eB CRISPR was delivered at P16, the sampled nuclei were NeuN-enriched neurons, and the focal group is a postmitotic glutamatergic neuronal population. Non-neuronal OPCs, oligodendrocytes, microglia, infiltrating neutrophils, and vascular compartments were deliberately absent or rare. CXCR2 loss could matter strongly in those missing compartments without inducing a cell-autonomous nuclear RNA state in `151 TH Prkcd Grin2c Glut`.

The best assayed within-dataset analogs support that interpretation:

- `Ccr2`, another chemokine GPCR with dominant inflammatory monocyte/macrophage biology, had `n_degs = 0` in the focal endpoint; all 17,259 focal genes had adjusted p-values equal to 1.0. The Distributed Agents `Ccr2` findings reported a pan-measured neuronal null and no meaningful positive or negative signature neighbor, consistent with Ccr2 being off-axis rather than weakly active in these neurons.
- `Cx3cr1`, a neuroimmune chemokine receptor whose receptor-positive brain compartment is microglia, had `n_degs = 0` in the focal endpoint and a smallest focal adjusted p-value of 1.0. The Distributed Agents corpus found that `Cx3cr1`, `Ccr2`, `Il10ra`, `Irf5`, and `P2ry14` were flat, with only isolated one-gene events for `P2ry12` and `Cxcr4`.
- `Cxcr4` is the most informative counterexample because it is a CXC chemokine receptor with clear neuronal migration/development biology, yet postnatal acute `Cxcr4` perturbation still had `n_degs = 0` in the focal group. Its closest focal event was `Pum1`, FDR `0.067`; across the corpus it was described as two isolated neuronal single-gene islands and no recovered CXCL12/CXCR4/ACKR3 migration program. I therefore did not extrapolate from "chemokine receptor" to a broad response.
- Upstream inflammatory receptor families and downstream effector lanes were also quiescent in the same focal count table: all six represented `Tlr` genes had `0` DEGs; all 16 represented interleukin receptors had `0`; `Csf1r` and `Csf3r` had `0`; `Ifnar1/2` and `Ifngr1/2` had `0`; `Pik3cb/Pik3r1/Pik3r2` and `Nfkb1` had `0`; the lone `Stat1` and `Gnao1` hits were self-transcript effects rather than inflammatory modules.

I therefore predict that acute sparse `Cxcr2` loss in the focal NeuN-positive neurons will be indistinguishable from the chemokine/neuroimmune receptor null class and will yield no FDR 0.05 downstream genes.

Prediction: `Cxcr2 = 0`.

## Limits

This is an extrapolation because `Cxcr2` itself was completely held out, no same-experiment `Cxcr2` signature was available, and the training set did not include the closest CXCR2 ligands or receptor-side paralogs `Cxcl1`, `Cxcl2`, `Cxcl5`, or `Cxcr1`. The analogs are family, lineage, or pathway comparators rather than a one-to-one receptor complex. A focal one-gene near-miss in `Cxcr4` shows that CXC receptors are not mathematically forced to have all adjusted p-values equal to 1.0, so a singleton `Cxcr2` event is possible. Finally, this prediction is scoped only to basal, sparse, P16 loss-of-function in NeuN-enriched juvenile neurons; it should not be read as a statement about systemic `Cxcr2` knockout, neutrophil chemotaxis, oligodendrocyte precursor migration, cuprizone/EAE models, or ligand-stimulated injury states.
