# DEG-count holdout prediction for 151 TH Prkcd Grin2c Glut

## Question and endpoint alignment

The requested value is the held-out `n_degs` for each target in the requested-target CSV, defined as the number of measured genes in `151 TH Prkcd Grin2c Glut` whose Wilcoxon Benjamini-Hochberg adjusted p value is below 0.05 after an acute P16 AAV-PHP.eB CRISPR-Cas9 loss-of-function perturbation.  The focal readout is directly observed for the non-held-out training perturbations in `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, while `Foxc1` itself is held out and has neither a training count nor a differential-expression signature in `training_de_all_cell_groups.parquet`.

I treated the count as an assay- and power-dependent transcriptional response breadth in recovered NeuN-positive nuclei.  Germline developmental phenotypes, glial/vascular phenotypes, and meningeal phenotypes are therefore mechanistic priors only when their cell type, developmental timing, and direct molecular consequence plausibly survive transfer to an acute perturbation in postmitotic thalamic glutamatergic neurons.

## Sources used

- Declared focal training counts: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression Parquet: `training differential-expression dataset`.
- Requested-target manifest: `single-target request for Foxc1`.
- Run-local measurement registry and dataset portrait, which establish that the Parquet measures measured-gene by target by neuronal-class differential expression in recovered nuclei, not raw expression, guide exposure, or survival before sampling.
- Internal same-experiment semantic layer: PerturbAI July `260713_sourceguard_1773_v1` Findings ledger and BioKG.  It was used to check for packaged `Foxc1` and `Foxc2` same-experiment interpretations; it is another representation of the same Perturb-seq experiment, not independent validation.
- External literature through PubMed E-utilities for Foxc1/Foxc2 function and tissue context.

## Dataset calculations

The requested manifest contains one target, `Foxc1`.  It is absent from the 1,674-row training-count file.

I summarized the focal training counts and then selected all available forkhead-box family perturbations plus a few neural crest, mesenchymal, vascular, or developmental transcription-factor counterexamples from the focal-count table:

```python
counts = pd.read_csv("151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv")
counts[counts.target_name.str.contains("^Fox", regex=True)]
```

The focal training-count distribution was highly zero-inflated: median 0, 75th percentile 1, mean 14.1, 95th percentile 18, and 469 of 1,674 perturbations had any FDR 0.05 DEG.  Large counts did occur in this cell group, led by `Uba5` 2677, `Tpr` 1768, `Sin3a` 1433, and `Rnpc3` 868, so a zero call is not just a global lack of detection in this class.

All forkhead-box perturbations present in the focal training endpoint had zero FDR 0.05 DEGs:

| training target | focal n_degs | relevance to Foxc1 |
| --- | ---: | --- |
| `Foxc2` | 0 | closest paralog and the best in-screen analog for FOXC1/FOXC2 mesenchymal and vascular developmental programs |
| `Foxa2` | 0 | developmental forkhead TF with dopaminergic/endodermal priors, but not a thalamic postmitotic-maintenance analog |
| `Foxe3` | 0 | non-neuronal forkhead TF, included as a family null control |
| `Foxi1` | 0 | epithelial/ionocyte forkhead TF, included as a family null control |
| `Foxj3` | 0 | broadly expressed forkhead TF, weak mechanistic analog |
| `Foxk2` | 0 | broadly expressed forkhead TF, weak mechanistic analog |
| `Foxl1` | 0 | mesenchymal forkhead TF, weak analog to non-neuronal Foxc1 action |
| `Foxl2` | 0 | forkhead TF with reproductive/endocrine priors |
| `Foxn1` | 0 | epithelial/thymic forkhead TF |
| `Foxp2` | 0 | a neuronal forkhead TF and counterexample: even a clearer neuronal forkhead perturbation was silent at FDR 0.05 here |
| `Foxp3` | 0 | immune forkhead TF |

To distinguish true null-looking signatures from near misses, I queried the Parquet only for the focal class and selected visible analogs, ordering measured genes within each perturbation by adjusted p value.  For `Foxc2`, the closest paralog, the best focal genes were `Entr1` and `Tmed7`, both with adjusted p value 0.809, and no row passed FDR 0.05 or even FDR 0.10 with 277 matched perturbed nuclei and 23,679 controls.  `Foxe3` likewise had a minimum adjusted p value of 0.603.  `Foxk2` had a self-transcript minimum adjusted p value of 0.146, and the other focal `Fox*` perturbations had minimum adjusted p values equal to 1.0 in the focal top rows.  Thus the Fox-family evidence was not a set of one- or two-gene borderline responses.

I also checked other developmental or non-neuronal transcription factors in the same focal count file.  `Pax6`, `Sox9`, `Ets1`, and `Twist2` all had `n_degs = 0` in `151 TH Prkcd Grin2c Glut`, reinforcing that genes with strong embryonic, mesenchymal, crest, vascular, or gliogenic priors do not generally give a broad postnatal thalamic-neuron signature merely because they are transcription factors.

## Same-experiment corpus evidence

The PerturbAI July BioKG query for a `Foxc1` target node returned no comparator rows, and `story-count --gene Foxc1` returned zero July Findings.  This absence means the packaged same-experiment corpus supplied no `Foxc1`-specific interpretation for this held-out target.

The corpus did contain `Foxc2` Findings.  The most relevant Finding, `Foxc2:F001`, summarizes that acute `Foxc2` loss of function was pan-null across all 23 recovered NeuN-positive neuronal groups.  Its evidence record for the focal class reports no FDR<0.10 downstream genes in `151 TH Prkcd Grin2c Glut` and a best downstream FDR of 0.809.  `Foxc2:F002` further notes that arterial VEGF-Dll4/Notch-Hey2, CXCR4, lymphatic NFATc1/ITGA9, and RhoA/ROCK cytoskeletal programs expected from endothelial FOXC2 biology were absent from the neuronal Foxc2 surface.  I used these Findings only to interpret the already-visible `Foxc2` null and not as an independent replicate.

## External biological priors

The strongest external evidence places Foxc1 action outside the assayed postnatal neuronal compartment:

- `Foxc1` and `Foxc2` encode closely related forkhead/winged-helix transcription factors with overlapping requirements in embryonic cardiovascular development, head mesoderm, and somites; double mutants have severe branchial-arch, vascular remodeling, and paraxial-mesoderm defects.  Kume et al. 2001, Genes & Development, DOI `10.1101/gad.907301`, PMID `11562355`.
- A hypomorphic Foxc1 mouse allele caused skull and cortical malformations through defective meningeal differentiation, radial-glial endfeet detachment, marginal-zone heterotopias, and cortical dyslamination during embryonic/postnatal development.  Zarbalis et al. 2007, PNAS, DOI `10.1073/pnas.0702618104`, PMID `17715063`.
- In Foxc1 mutant embryos, loss of dorsal forebrain meninges reduces meningeal retinoic-acid production; exogenous retinoic acid rescued aspects of the corticogenesis phenotype.  Siegenthaler et al. 2009, Cell, DOI `10.1016/j.cell.2009.10.004`, PMID `19879845`.
- Foxc1 hypomorphs impair tangential migration of cortical interneurons through defective meningeal `Cxcl12`, not through a cell-autonomous thalamic glutamatergic neuron mechanism.  Zarbalis et al. 2012, Neural Development, DOI `10.1186/1749-8104-7-2`, PMID `22248045`.
- Conditional work mapped Foxc1-dependent cerebrovascular growth phenotypes to neural-crest-derived meninges and brain pericytes, with retinoic-acid, WNT, and VEGF-A signals downstream.  Mishra et al. 2016, Developmental Biology, DOI `10.1016/j.ydbio.2016.09.019`, PMID `27671872`.
- `Foxc2`, the in-screen paralog, is expressed in lymphatic primordia, lymphatic collectors/capillaries, podocytes, and developing eyelids relative to Foxc1/VEGFR3/PROX1 markers.  Dagenais et al. 2004, Gene Expression Patterns, DOI `10.1016/j.modgep.2004.07.004`, PMID `15465483`.

The causal-transfer model therefore breaks at both intervention and exposure stages.  Embryonic Foxc1 loss perturbs meningeal/pericyte transcriptional programs, which then alter secreted RA, CXCL12, WNT, VEGF-A, and tissue architecture before neurons differentiate.  The requested experiment instead edits sparse NeuN-positive, mostly postmitotic neurons at P16 and samples recovered nuclei 3-4 weeks later; meninges, endothelial cells, pericytes, astrocytes, microglia, oligodendrocytes, and vascular cells are absent or under-sampled.  Nothing in the Foxc1 literature established an obligate maintenance function in juvenile thalamic glutamatergic neurons analogous to the high-count neuronal regulators in the training set.

## Target-specific prediction

`Foxc1`: the closest within-dataset analog is `Foxc2` and it was a clean zero in the focal class (`n_degs = 0`; best focal adjusted p value 0.809) and in all 23 neuronal groups at FDR 0.10.  All 11 focal forkhead perturbations in the training endpoint had `n_degs = 0`, including `Foxp2`, a more neuronal forkhead-family counterexample.  Other embryonic or non-neuronal lineage TFs (`Pax6`, `Sox9`, `Ets1`, `Twist2`) were also silent in this focal cell group.  External Foxc1 biology points primarily to embryonic meningeal, mesenchymal, pericyte, skull, vascular, and migration phenotypes that should not be exposed by sparse acute editing of postmitotic thalamic neurons.  I therefore predict no measured gene will cross FDR 0.05.

## Limits

`Foxc1` itself was completely held out, so this prediction extrapolates from `Foxc2` and other forkhead or developmental transcription factors rather than from a directly observed `Foxc1` signature.  The screen perturbs genes with mosaic AAV CRISPR and may recover only surviving nuclei; a severe pre-assay selection effect or a rare unannotated thalamic Foxc1 function could leave few or no DEGs.  Conversely, germline Foxc1 phenotypes are real but mostly occur through tissues and developmental windows that are not represented by this NeuN-enriched postnatal assay, so I did not transfer their large effects to the requested endpoint.
