# Pum1 direct DEG-count forecast

## Declared target and endpoint

- Target: `Pum1`, from the one-row holdout manifest.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, i.e. the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- Declared outcome status: `Pum1` is absent from the 1,674-row training count table, and no `Pum1` rows are present in the declared `training_de_all_cell_groups.parquet`.

## Target biology used

The canonical biology-only bundle identifies Pum1 as a cytoplasmic, sequence-specific RNA-binding regulator that binds Pumilio response elements and represses many target mRNAs through translation and mRNA-stability mechanisms. In mouse brain iCLIP, 1,874 genes were Pum1-associated and 694 were shared with Pum2, but Pum1/Pum2 loss raised protein abundance for many targets without changing most target transcript abundances. That made a very large snRNA-seq mRNA signature less likely than for a direct transcription, spliceosome, or RNA-export perturbation.

The focal expression measurement supports technical reach in the exact endpoint population: in matched non-target `151 TH Prkcd Grin2c Glut` cells, `Pum1` was detected in 17,156 of 23,679 nuclei, or 72.45%, with mean log1p CP10K 0.554 and pseudobulk CPM 89.39. The functional-stock adjudication also supports that a P16 edit should substantially reduce the renewable Pum1 protein pool by the P37-P44 harvest window, while preserving uncertainty because no Pum1-specific neuronal protein half-life was found.

The bundle gives moderate biological support but not thalamic transcriptome proof: Pum1 single loss has a postnatal mouse neural phenotype despite partial Pum2 redundancy, yet the cleanest phenotype was cerebellar and progressive, and the direct Pum1 action is often post-transcriptional at the protein layer.

## Training measurements used

The 151-class training count table is extremely zero-inflated:

- 1,205 / 1,674 training perturbations had `n_degs = 0`.
- The median was 0 and the 75th percentile was 1.
- Only 42 / 1,674 exceeded 100 DEGs.

I therefore treated a large count as requiring a close high-yield analogue rather than as the default for an expressed neuronal gene.

The closest measured post-transcriptional and cytoplasmic-RNA regulators were nearly all quiet in the exact endpoint:

| training perturbation | relevant role | n_degs |
|---|---|---:|
| `Fmr1` | neuronal RNA-binding / translation regulation | 0 |
| `Ago2` | cytoplasmic RNA silencing | 0 |
| `Dicer1` | miRNA biogenesis | 0 |
| `Cnot1` | mRNA deadenylation / post-transcriptional repression scaffold | 0 |
| `Msi1` | RNA-binding translational regulator | 0 |
| `Ago1` | cytoplasmic RNA silencing | 1 |
| `Eif4g1` | translation initiation | 1 |
| `Eif4h` | translation initiation | 1 |
| `Eif4a2` | translation initiation helicase | 2 |
| `Ddx3x` | RNA helicase with translation/RNA roles | 8 |

By contrast, the high RNA-processing tail was dominated by nuclear spliceosome, hnRNP, or RNA-export factors such as `Hnrnpc = 122`, `Tardbp = 210`, `Hnrnpu = 733`, `Rnpc3 = 868`, `U2af2 = 828`, `Cdc40 = 624`, `Prpf6 = 454`, and `Thoc1 = 303`. I interpreted those as mechanistically mismatched upper references: loss of core nuclear RNA processing creates a broad mRNA-state perturbation, whereas Pum1 primarily derepresses bound messages at the translational level.

## Synthesis

The exact expression reach and likely depletion of Pum1 protein make a pure technical null too conservative. However, the mechanism points away from the high-spliceosome branch, and the available cytoplasmic RNA-silencing/translation comparators center at zero to one significant gene in this same thalamic population. Pum2 redundancy and the protein-dominant derepression of many Pum1 targets both push the forecast down; high in-assay expression and single-loss neural relevance push it just above the all-target median.

I therefore place `Pum1` at the small nonzero edge of the quiet-post-transcriptional group and predict:

`n_degs = 1`
