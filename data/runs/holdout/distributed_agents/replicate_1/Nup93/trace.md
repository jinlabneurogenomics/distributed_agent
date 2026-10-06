# Question and endpoint

The task is to predict the held-out `n_degs` value for each requested genetic perturbation in `151 TH Prkcd Grin2c Glut` neurons. I interpreted `n_degs` as the exact training endpoint supplied in `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: the number of measured genes with `pvals_adj < 0.05` in the focal thalamic glutamatergic class after acute P16 AAV-PHP.eB CRISPR loss of function and P37-P44 snRNA-seq.

Only one requested target was present in `the single-target request`: `Nup93`. The target is held out, so no `Nup93` perturbation rows from `training_de_all_cell_groups.parquet` and no `Nup93` row from the focal-cell training count table were used.

# Sources used

- Declared direct measurements:
  - `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
  - `training differential-expression dataset`
- Run-local manifests: `task_bindings.json`, `coverage.json`, `capabilities.json`, and `measurement_registry.json`.
- Internal same-experiment interpretation corpus: `perturbai-july-260713-sourceguard-1773-v1`, used for Tpr and Ranbp2/Thoc1 report-derived Findings and Evidence. I treated this as a packaged interpretation of the same Perturb-seq experiment, not as independent replication.
- External literature:
  - Miller et al. 2000, Molecular Biology of the Cell, DOI `10.1091/mbc.11.10.3381`, PMID `11029043`.
  - Labade et al. 2016, Epigenetics & Chromatin, DOI `10.1186/s13072-016-0106-0`, PMID `27980680`.
  - Huang et al. 2022, Cell Research, DOI `10.1038/s41422-022-00633-x`, PMID `35301439`.
  - Marquez et al. 2020, Developmental Biology, DOI `10.1016/j.ydbio.2020.10.001`, PMID `33065118`.
  - Aksenova et al. 2020, Nature Communications, DOI `10.1038/s41467-020-18266-2`, PMID `32917881`.
  - Lee et al. 2020, Nucleic Acids Research, PMID `33091126`.
  - Lee et al. 2026, Nature Cell Biology, DOI `10.1038/s41556-026-01882-3`, PMID `41786887`.
  - Savas et al. 2012, Science, PMID `22300851`.

The scalar held-out count is absent from the declared inputs. It is not a ranked-output task, so the rank-calibration workbench, ordering validator, and predictive graph review were inapplicable and unavailable in the capability manifest.

# Computation over the training data

I first read the requested-target CSV and the training count CSV. The focal training table contained 1,674 non-held-out perturbations; 1,205 of them had `n_degs = 0`, the median was 0, the mean was 14.1, and the maximum was 2,677. This made a null prediction the prior for an arbitrary gene, but also left a very long tail for perturbations that cross a focal-cell vulnerability.

I then searched the focal training counts for represented nuclear-pore and nuclear-transport genes. No inner-ring `Nup*` target was present in the training count table. The most relevant represented genes were:

| training perturbation | focal `n_degs` | interpretation for Nup93 |
|---|---:|---|
| `Tpr` | 1,768 | Positive same-organelle analog: a nuclear-basket nucleoporin with a direct mRNA-export role. Very strong in the focal class, but not an obligate Nup93-complex subunit. |
| `Thoc1` | 303 | Positive functional analog through THO/TREX-coupled mRNA biogenesis and export; not a pore scaffold. |
| `Tnpo3` | 618 | Nuclear-transport positive comparator; mechanistically downstream/parallel rather than a structural NPC analog. |
| `Ranbp2` | 0 | Negative NPC counterexample: a cytoplasmic-filament/SUMO nucleoporin that was silent in the focal class despite having large effects in other neuronal populations. |
| `Kpna3` | 0 | Negative karyopherin/import counterexample. |
| `Xpo7` | 0 | Negative exportin counterexample, showing that transport annotation alone was not enough. |

For a narrow Parquet read, I filtered rows to `group_name == "151 TH Prkcd Grin2c Glut"` and the relevant positive/negative training targets. The FDR<0.05 counts reproduced the training CSV: `Tpr` had 1,768 significant genes; `Thoc1`, 303; `Tnpo3`, 618; `Ranbp2`, 0. The `Tpr` focal signature was broad and coherent rather than a single outlier gene: among its strongest rows were `Xpo1`, `Ranbp6`, `Nxf1`, `Ddx17`, `Srsf5`, `Pabpn1`, `Srrm2`, and `Rnpc3`, matching nuclear export and RNA-processing biology. The same focal slice for `Ranbp2` had minimum adjusted P value 0.202 and no FDR<0.05 genes.

I attempted a broader all-cell Parquet scan for `Tpr`, `Thoc1`, and `Ranbp2`, but stopped it after it was still scanning the full large table; the same-experiment corpus already supplied bounded all-cell summaries for those targets. The Tpr report recorded the same qualitative cross-cell structure: at FDR<0.10, `Tpr` was highly active in `151 TH Prkcd Grin2c Glut` and `155 MB Glut`, and the report emphasized recurrent alteration of `Ranbp6`, `Xpo1`, and `Nxf1`. The Ranbp2 report showed that Ranbp2 was not globally inert, but its main responses were in other cell groups, making the focal zero informative as a cell-context counterexample.

# Target-specific reasoning

## Nup93

`Nup93` encodes a core inner-ring nucleoporin. The molecular step of the perturbation is expected to impair the Nup93 inner-ring module rather than the nuclear basket: Nup93 complexes with Nup188 and Nup205 in vertebrate pores (Miller et al. 2000), four copies of Nup93 form part of the Xenopus inner-ring central scaffold with Nup188/Nup205/Nup155/NDC1-ALADIN (Huang et al. 2022), and Nup93 with Nup188/Nup205 can tether and repress the HOXA locus (Labade et al. 2016). Nup93 also has pore-associated RNA-output biology: a later imaging study placed NUP93 in an m6A/METTL3 axis for efficient mRNP export through nuclear pore complexes (Lee et al. 2026).

The most relevant positive within-dataset comparator was `Tpr`, because it is the represented nucleoporin whose perturbation generated a broad focal transcriptional response. `Tpr` is not in the same inner-ring subcomplex: it sits at the nuclear basket, and external degron/RNA-export work assigns TPR a specialized TREX-2/NXF1 export role (Aksenova et al. 2020; Lee et al. 2020). This reduces direct count transfer from 1,768; losing a TPR basket export factor is likely more immediately coupled to nuclear RNA accumulation than modestly editing a scaffold component of pre-existing pores.

The second positive comparator was `Thoc1` at 303 focal DEGs. THOC1 acts upstream in transcription-coupled mRNA packaging and export rather than as an NPC component, but the same-experiment corpus linked its response to splicing/export/nuclear-pore perturbations including `Tpr`, and the focal Parquet slice showed shared movement of mRNA-processing markers such as `Srrm2` and `Ogt`. `Tnpo3` at 618 showed that a transport-factor perturbation can land in an intermediate focal-response band.

`Ranbp2` was the main counterexample. It is a bona fide nucleoporin, but it occupies the cytoplasmic face and combines SUMO/transport/scaffold roles distinct from the Nup93 inner ring. Its focal `n_degs` was 0 even though Ranbp2 had cell-type-selective signals elsewhere. `Kpna3` and `Xpo7` were also 0, arguing against simply predicting a large count for any nuclear import/export gene.

The causal transfer I used was therefore:

`Nup93` loss -> partial impairment of inner-ring nuclear-pore scaffold plus Nup93-specific chromatin/export functions -> altered nuclear transport/RNA-processing/chromatin homeostasis in vulnerable thalamic neurons -> a survivor-conditioned snRNA-seq response breadth.

That chain predicts a nonzero count in the same direction as the `Tpr`/`Thoc1` export-RNA-processing program, but with lower confidence and lower magnitude than `Tpr`. The main reason to downgrade is intervention stage and protein persistence: many nuclear pore proteins are exceptionally long-lived in postmitotic brain cells (Savas et al. 2012), so the 3-4 week sparse CRISPR perturbation with modest average mRNA down-regulation may leave enough previously assembled inner-ring pore scaffold to buffer complete NPC disruption. The main reason not to set the count to zero is that NUP93 is central to the Nup93/Nup188/Nup205 inner ring and has documented mRNA-export and chromatin-tethering functions; this is a stronger endpoint-bearing connection to the focal `Tpr` and RNA-biogenesis signatures than the negative `Ranbp2`, `Kpna3`, or `Xpo7` comparisons provide.

I placed the point estimate at `620` DEGs: close to the intermediate `Tnpo3` band and above `Thoc1`, but well below `Tpr`'s 1,768-gene response. This is an extrapolation from represented pore/export analogs rather than a direct Nup93 within-dataset signature.

# Limits

No non-held-out perturbation in the focal training table was an obligate Nup93 inner-ring partner such as `Nup188`, `Nup205`, `Nup155`, `Nup35`, or `Ndc1`, so the estimate depends on imperfect transfer from `Tpr`, RNA-export factors, and negative transport/nucleoporin counterexamples. The Parquet contains differential expression in recovered nuclei only; it does not observe guide exposure, editing allele fraction, protein depletion, pre-assay depletion, nuclear export flux, pore number, ciliary defects, chromatin occupancy, or absolute RNA output. Several external Nup93 mechanisms come from proliferating cultured human cells, Xenopus embryos, or kidney/cilia systems, so they support a mechanistic prior but not the exact P16 postmitotic thalamic DEG count.
