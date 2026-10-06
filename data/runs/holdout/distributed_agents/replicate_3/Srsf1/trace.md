## Question and interpretation

The requested held-out perturbation for this run was:

| target_name |
| --- |
| Srsf1 |

I interpreted the endpoint as the integer number of measured genes in `151 TH Prkcd Grin2c Glut` whose perturbed-versus-control Wilcoxon `pvals_adj` was below 0.05 after mouse `Srsf1` CRISPR loss of function. `Srsf1` was absent from both supplied training inputs, so I did not use a same-target expression signature.

The endpoint is a whole-gene snRNA-seq response-breadth count in surviving nuclei. I therefore treated splice-isoform biology as a prior on whether there should be a broad secondary abundance response, not as a direct DEG count.

## Sources used

- `training_de_all_cell_groups.parquet`: focal-cell log2 fold changes and adjusted p values for the non-held-out perturbations.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: the observed focal-cell `n_degs` for 1674 non-held-out perturbations.
- Requested-target manifest `223_Srsf1.csv`: confirmed that `Srsf1` was the only requested prediction.
- Distributed Agents internal corpus `perturbai-july-260713-sourceguard-1773-v1`: I queried `Srsf1` and the main RNA-processing analogs. There were no curated `Srsf1` findings in this release, but the corpus did contain same-experiment cards for `U2af2`, `Prpf6`, `Rnpc3`, `Snrnp70`, and `Tnpo3` describing a selective same-direction spliceosome/RNA-processing module.
- PubMed literature:
  - Wang, Takagaki and Manley 1996, DOI `10.1101/gad.10.20.2588`, PMID `8895660`: ASF/SF2/SRSF1 is an essential vertebrate SR protein; depletion caused incompletely processed pre-mRNA accumulation and cell death in a conditional DT40 system.
  - Li and Manley 2005, DOI `10.1016/j.cell.2005.06.008`, PMID `16096057`: ASF/SF2/SRSF1 depletion can cause transcription-associated R-loops and genome instability.
  - Kataoka, Bachorik and Dreyfuss 1999, DOI `10.1083/jcb.145.6.1145`, PMID `10366588`: transportin-SR/TNPO3 binds RS domains of SR proteins including ASF/SF2/SRSF1 and SC35/SRSF2 and mediates nuclear import of RS-domain proteins.
  - Long and Caceres 2009, DOI `10.1042/BJ20081501`, PMID `19061484`: SR proteins are conserved RS-domain splicing factors with roles in constitutive and alternative splicing plus mRNA export, NMD, and translation.

## Computations over the supplied data

I first summarized the training endpoint in the focal cell group. The 1674 training perturbations were strongly zero-inflated:

| statistic | `n_degs` |
| --- | ---: |
| mean | 14.1 |
| 25% | 0 |
| median | 0 |
| 75% | 1 |
| 90% | 2 |
| 95% | 18 |
| 99% | 436 |
| max | 2677 |

Thus any nonzero prediction above a few dozen DEGs has to come from a mechanistic analogy to the rare broad responders, not from the global prior.

I then queried focal training counts for RNA-splicing and RNA-binding genes. Direct `Srsf` paralogs were not represented, but several core or adjacent RNA-processing perturbations were:

| analog | focal `n_degs` | use in this prediction |
| --- | ---: | --- |
| `Rnpc3` | 868 | minor spliceosome factor; broad same-direction RNA-processing state in the internal corpus |
| `U2af2` | 828 | U2AF splice-acceptor factor; broad same-direction neighbor of `Prpf6`, `Cdc40`, `Rnpc3` |
| `Cdc40` | 624 | PRP17/CDC40 spliceosome-step factor; corpus links it with `Prpf6`, `U2af2`, `Snrnp70` |
| `Tnpo3` | 618 | direct nuclear import receptor for SR proteins; most SRSF1-proximal measured analog |
| `Prpf6` | 454 | U5 tri-snRNP factor; corpus anchors a selective spliceosome module |
| `Snrnp70` | 213 | U1 snRNP 70K factor; penetrant but weaker in the focal group |
| `Hnrnpc` | 122 | RNA-binding/splicing regulator, but hnRNP rather than SR/core spliceosome |
| `Hnrnpa2b1` | 11 | RBP counterexample with a tiny focal response |
| `Ddx3x` | 8 | RNA helicase counterexample with a tiny focal response |
| `Ddx39b` | 0 | TREX/export factor; important elsewhere but flat in this focal group |
| `Rbm28` | 0 | RBP/ribosome-biogenesis counterexample, flat in the focal group |
| `Snrpb` | 0 | Sm-core snRNP counterexample, flat despite snRNP membership |

To check that the high-count spliceosome analogs were expression-state neighbors and not merely a list of RNA genes, I used the Distributed Agents runtime `profile_compare` layer on 15 candidate perturbations, restricted to `group_name == "151 TH Prkcd Grin2c Glut"`. The comparison used 17,259 measured genes per target, `logfoldchanges` as the signed profile, and `pvals_adj < 0.05` as the significant-feature threshold. Important pairwise observations were:

- `U2af2` had 828 focal DEGs split 446 up and 382 down. It shared many same-direction FDR genes with `Rnpc3` and `Cdc40` in this cell group: 39 up plus 118 down with `Rnpc3`, and 31 up plus 82 down with `Cdc40`; the Pearson correlations on the full logFC vector were 0.586 and 0.607.
- `Prpf6` had 454 focal DEGs and also converged with `Rnpc3` and `Cdc40`: 35 up plus 83 down shared with `Rnpc3`, and 38 up plus 65 down shared with `Cdc40`; direction conflicts were only 9 and 4 significant genes.
- `Snrnp70` had a smaller but still clear signature of 213 DEGs, with 35 up plus 44 down shared with `Rnpc3` and 12 up plus 29 down shared with `Cdc40`.
- `Tnpo3` was broad in the same endpoint, with 618 DEGs. Its pairwise correlations to the core spliceosome factors were weaker than `Prpf6`/`U2af2` correlations, but it still shared 98 same-direction FDR genes with `Rnpc3` and 89 with `Cdc40`.
- Low-count RBP counterexamples had essentially no same-direction significant overlap with the broad factors. For example, `Ddx39b`, `Rbm28`, and `Snrpb` had zero focal DEGs and zero significant intersections with `U2af2` or `Prpf6`. `Ddx3x` had only eight DEGs and at most a handful of overlaps.

These observations match the Distributed Agents corpus findings: `Prpf6:F003`, `Rnpc3:F009`, `Snrnp70:F006`, `Tnpo3:F004`, and `U2af2:F005` describe convergence among selected spliceosome/RNA-processing perturbations, while the `Snrnp70:F007`, `U2af2:F006`, and `Tnpo3:F004` cards explicitly note that represented Sm, hnRNP, and generic transport/RBP perturbations do not all phenocopy that state.

## Srsf1 reasoning

`Srsf1` encodes ASF/SF2, a prototypical SR protein with RS and RNA-recognition domains. It is mechanistically closer to the penetrant arm of the training set than to the near-null RBP counterexamples for three reasons.

First, SRSF1 is not just a peripheral RBP. Wang, Takagaki and Manley showed that ASF/SF2 is essential for vertebrate cell viability and that its depletion causes accumulation of incompletely processed pre-mRNA. Long and Caceres review the broader point that the SR family participates in constitutive and alternative splicing as well as later mRNA-metabolism steps. Loss of an SR factor can therefore propagate from splicing to gene-abundance stress, which is exactly the class of secondary state recovered for `U2af2`, `Prpf6`, `Rnpc3`, `Cdc40`, and `Snrnp70` in the training data.

Second, the most SRSF1-proximal measured perturbation was `Tnpo3`. TNPO3/transportin-SR directly imports RS-domain SR proteins including ASF/SF2/SRSF1 (Kataoka, Bachorik and Dreyfuss 1999). In the corpus, `Tnpo3:F002` reports that `Tnpo3` responders down-regulated an SR-splicing/RNA-processing module led by `Srrm2`, `Srsf5`, `Srsf1`, `Srsf7`, `Srsf2`, `Akap8l`, `Clk1`, and `Cstf2`; `Tnpo3:F004` further reports same-direction convergence with `U2af2`, `Cdc40`, `Rnpc3`, `Snrnp70`, and `Thoc1`, but not with more generic nuclear transport targets. This makes `Tnpo3` a strong positive analog and puts an SRSF1/SR-protein branch inside a 618-DEG focal response.

Third, the dataset warns that physical complex membership alone overpredicts. `Snrpb` is an snRNP component but had 0 focal DEGs, `Ddx39b` is an RNA-export helicase but had 0 focal DEGs in this cell type, and `Hnrnpa2b1`/`Ddx3x` were nearly flat. Those counterexamples keep `Srsf1` below the very largest core U2/minor-spliceosome responses (`U2af2` 828 and `Rnpc3` 868). They do not support a zero call because SRSF1 is an SR splice regulator and a TNPO3 cargo, not an Sm-core or generic hnRNP target.

My zero/nonzero decision was therefore **nonzero**. For magnitude, I placed `Srsf1` in the same hundred-DEG regime as the selective spliceosome module, but slightly below `Tnpo3` and `Prpf6`: direct loss of one SR protein should be less pleiotropic than loss of the SR import receptor, U2AF2, or RNPC3, while still much broader than the 0 to 11 DEG RBP counterexamples. I used **420** as the integer point prediction.

## Limits

- No direct `Srsf1` signature, no direct `Srsf` paralog perturbation, and no `Clk` or `Tra2` perturbation was present in the training counts, so the prediction is extrapolated from TNPO3 and core spliceosome analogs.
- The expression profiles are whole-gene snRNA-seq signatures. They do not measure exon skipping, intron retention, R-loops, or SR-protein localization, all of which are primary effects expected for SRSF1 biology.
- The broad core-spliceosome counts span 213 to 868 DEGs in the same focal cell group. A point estimate within that band is necessarily uncertain because the assay is sensitive to guide efficiency, tolerated edit dosage, cell-state buffering, and survival of edited nuclei.
- The external essentiality literature is from cultured vertebrate cells and non-neuronal systems, whereas this assay is partial mosaic postnatal CRISPR in surviving mouse neurons. I used those papers only to decide that SRSF1 is capable of producing a real RNA-processing lesion, not to assign the exact DEG count.
