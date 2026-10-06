# DEG-count prediction trace

## Question and resolved ambiguities

The manifest `[local file: 200_Rrn3.csv]` contains one held-out target:

| target_name |
|---|
| Rrn3 |

I interpreted the requested endpoint as the integer count of measured genes with `pvals_adj < 0.05` for the `Rrn3` CRISPR perturbation in `151 TH Prkcd Grin2c Glut` cells under the same Wilcoxon/Benjamini-Hochberg procedure used to make `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`. `Rrn3` itself was completely absent from both the training DE parquet as a `gene_target` and the training endpoint CSV, so the prediction has to be transferred from assayed perturbations rather than read directly.

The count endpoint is an FDR thresholded, power-dependent breadth metric. I therefore used the same-cell counts as calibration and did not treat loss of an essential nucleolar gene as automatically implying a large mRNA signature in surviving nuclei 3-4 weeks after sparse P16 AAV-CRISPR editing.

## Sources

- Input endpoint CSV: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Held-out manifest: `200_Rrn3.csv`.
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`. `Rrn3` had no direct target context in the corpus, but `Taf1b`, `Nop56`, `Rbm28`, and `Polr3b` had same-experiment claims and findings over nearby RNA-biogenesis perturbations.
- PubMed literature searches for Pol I initiation, TIF-IA/RRN3, SL1/TAF1B, neuronal nucleolar stress, and box C/D snoRNP/NOP56 biology.

External citations used for the mechanistic prior:

- Cavanaugh et al. 2002, DOI `10.1074/jbc.M201232200`: mouse Rrn3 is a Pol I-associated transcription-initiation factor whose phosphorylation regulates formation of the Rrn3-Pol I complex and rDNA transcription.
- Stepanchick et al. 2013, DOI `10.1074/jbc.M112.444265`: human Rrn3 is essential for rDNA transcription and bridges Pol I with the SL1-bound rDNA promoter.
- Naidu et al. 2011, DOI `10.1126/science.1207656`, and Knutson and Hahn 2011, DOI `10.1126/science.1207699`: TAF1B is an SL1/core-factor subunit and a TFIIB-like basal Pol I initiation factor.
- Parlato et al. 2008, DOI `10.1523/JNEUROSCI.2439-08.2008`: complete TIF-IA ablation in mouse neural progenitors or hippocampal neurons impaired nucleolar activity and increased p53, but nondividing adult hippocampal neurons underwent protracted rather than rapid degeneration.
- Kreiner et al. 2013, DOI `10.1038/cdd.2013.66`: conditional TIF-IA loss in striatal medium spiny neurons caused nucleolar stress, a transient p53/PTEN survival response, and later degeneration.
- Friedrich et al. 2005, DOI `10.1074/jbc.M501595200`: mammalian SL1 directs Pol I preinitiation-complex formation at rDNA promoters.
- Galardi et al. 2002, DOI `10.1128/MCB.22.19.6663-6668.2002`, Kiss et al. 2006, DOI `10.1101/sqb.2006.71.025`, and Hofler et al. 2021, DOI `10.1261/rna.077396.120`: NOP56 is a core box C/D snoRNP scaffold involved in fibrillarin-mediated rRNA 2'-O-methylation, a downstream ribosome-biogenesis function rather than a Pol I initiation factor.
- Bryant et al. 2021, DOI `10.1073/pnas.2017777118`: RBM28 is a conserved nucleolar 60S assembly factor whose hypomorphic biallelic variants cause a human ribosomopathy, making it a literature-obvious but not same-complex counterexample.

## Computational evidence from the inputs

1. I loaded the held-out manifest and confirmed it has exactly one unique target, `Rrn3`.
2. I loaded the `151 TH Prkcd Grin2c Glut` training counts. The focal endpoint is very sparse: 1205 of 1674 training perturbations have `0` DEGs, the median is `0`, the 75th percentile is `1`, the 95th percentile is `18`, and only 42 perturbations exceed 100 DEGs.
3. I inspected parquet row-group statistics rather than scanning the entire 616,253,184-row file. The focal cell group occupies row groups 547-580, totaling 29,213,425 rows, so I queried only those row groups for biologically nominated training perturbations.
4. I intersected the training target list with Pol I, SL1, nucleolar, snoRNP, and RNA-production candidates. The closest represented genes were sparse: `Taf1b`, `Nop56`, `Rbm28`, `Las1l`, `Bdp1`, `Polr3b`, `Myc`, and `Mycn`. Direct Pol I subunits and several ideal analogs were absent from the 1,674 training targets, including `Polr1a`, `Polr1b`, `Polr1c`, `Polr1d`, `Polr1e`, `Ubtf`, `Tbp`, `Taf1a`, `Taf1c`, `Taf1d`, `Fbl`, `Nop58`, `Npm1`, and `Ddx21`.
5. I pulled all focal-cell DE rows for the nominated available analogs and counted `pvals_adj < 0.05`, matching the supplied endpoint:

| comparator | focal `n_degs` | strongest focal signature evidence |
|---|---:|---|
| `Taf1b` | 0 | Core SL1/Pol I initiation perturbation; all queried focal genes were FDR-negative, with the best adjusted p-values equal to 1.0. |
| `Nop56` | 25 | A small RNA-processing/SR-splicing branch: `Rsrp1`, `Ddx17`, `Srsf5`, `Tcea2`, `Srsf11`, `Ddx5`, `Peg3` and others passed FDR. |
| `Rbm28` | 0 | Literature-obvious nucleolar 60S biogenesis comparator; best focal adjusted p-value was 0.543. |
| `Las1l` | 0 | Another 60S/rRNA-processing comparator noted in the corpus as flat. |
| `Bdp1` | 8 | Pol III initiation factor with a small aminoacyl-tRNA-synthetase/ISR-like branch, including `Ddit3`, `Mars1`, `Aars`, `Iars`, `Lars`, `Cars`, and `Yars`. |
| `Polr3b` | 8 | Pol III core-subunit comparator with a small thalamic homeostatic module, including `Adgrb1`, `Rap1gap`, `Pcp4`, `Slco3a1`, `Rap2a`, `Gas2`, and `Mgat5`. |
| `Myc` | 0 | Literature-obvious upstream growth/ribosome-biogenesis activator, flat in `151`. |
| `Mycn` | 0 | MYC-family comparator, flat in `151`. |

The Distributed Agents corpus supported the same interpretation. In release `perturbai-july-260713-sourceguard-1773-v1`, `Taf1b` was annotated as "mRNA-transcriptionally flat across the recovered juvenile neuronal surface"; its corpus comparison noted that `Nop56` and `Polr3b` can produce thalamic or midbrain-associated DE where `Taf1b` is flat, so the `Taf1b` null is not just because the assay is blind to RNA-biogenesis perturbations. A separate corpus claim over `Nop56` and `Rbm28` stated that postmitotic neuronal transcriptional responses to the assayed nucleolar ribosome-biogenesis perturbations were factor-specific and cell-type restricted rather than pan-neuronal. `Nop56`'s signal was modest and concentrated in `151`, while `Rbm28` and `Las1l` were flat; `Nop56` also lacked the broad canonical p53/UPR/autophagy signature expected from overt nucleolar stress.

## Rrn3-specific reasoning

`Rrn3`, also known as TIF-IA, is a dedicated Pol I initiation factor. It helps recruit Pol I to rDNA promoters by linking the polymerase to promoter-bound SL1/UBTF machinery, and its phosphorylation state regulates the active Pol I-RRN3 complex. A full TIF-IA loss can shut down 47S pre-rRNA synthesis, disorganize the nucleolus, activate p53, and, in conditional mouse models, eventually compromise postmitotic neurons.

Those external facts establish that `Rrn3` is biologically important, but the held-out endpoint is not a complete-knockout viability assay or a direct 47S pre-rRNA/nucleolar readout. The internal evidence argues that in this experiment Pol I-initiation stress often remained below the threshold for a broad captured mRNA response:

- The best same-machinery analog is `Taf1b`, an SL1 subunit required for Pol I preinitiation-complex formation. It produced `0` DEGs in the focal group despite 106 matched perturbed nuclei.
- The closest assayed upstream ribosome-biogenesis activators, `Myc` and `Mycn`, also produced `0` DEGs in the focal group.
- Downstream nucleolar factors gave mixed results: `Nop56` was positive but narrow at 25 DEGs, while `Rbm28` and `Las1l` were completely flat. Thus a nucleolar/ribosome-biogenesis label by itself did not imply an effect.
- Neighboring RNA-production machinery outside Pol I gave only small positive counts, `Bdp1 = 8` and `Polr3b = 8`, and their signatures were different from each other and from `Nop56`. They are evidence that the focal cells can report RNA-production lesions, but they are not evidence for a large shared Pol I-like response.
- `Trp53` itself had `0` focal DEGs, and the corpus specifically recorded that `Taf1b` and `Nop56` failed to induce canonical p53/nucleolar-stress sentinel mRNAs. That weakens the case for assigning `Rrn3` a large p53-driven DEG count.

On balance I predict `Rrn3` will look more like the flat same-machinery `Taf1b` perturbation than like the modest `Nop56` response. RRN3 is closer to the Pol I initiation lesion than NOP56, but `Nop56`'s 25-gene branch is a post-transcriptional RNA/SR-splicing and synaptic state rather than a generic rDNA-transcription program, and no direct evidence links it to held-out `Rrn3`.

## Prediction

| target_name | predicted_n_degs |
|---|---:|
| Rrn3 | 0 |

## Limits

This is an extrapolation across an incompletely represented Pol I neighborhood. None of `Polr1*`, `Ubtf`, `Tbp`, or the other SL1 subunits was available as a training perturbation, and the held-out `Rrn3` signature was absent by design. The same-experiment corpus had no direct `Rrn3` node. Complete TIF-IA knockout studies in hippocampal and striatal neurons show that a strong Pol I lesion can drive p53-linked nucleolar stress and later neurodegeneration, so a fully penetrant `Rrn3` knockout would not be expected to be biologically inert. The prediction of zero is specific to sparse AAV CRISPR editing, surviving NeuN+ nuclei, a protein-coding snRNA-seq readout 3-4 weeks after P16 injection, and the empirical behavior of `Taf1b` and other nearby perturbations in this assay.
