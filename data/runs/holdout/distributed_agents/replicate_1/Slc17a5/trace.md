# Slc17a5 DEG-count prediction

## Question and endpoint

I interpreted the task as a scalar prediction for one completely held-out perturbation, `Slc17a5`, in the focal `151 TH Prkcd Grin2c Glut` neuronal cell group. The endpoint is exactly the training-table definition: the number of measured genes in the focal cell group with `pvals_adj < 0.05` after Benjamini-Hochberg correction in the Scanpy Wilcoxon contrast of perturbed versus matched non-targeting controls. The count includes the perturbed transcript itself if that row passes FDR.

The held-out endpoint is absent: `Slc17a5` is not in the focal training-count CSV and not present as a `gene_target` in the Parquet. The Parquet is direct evidence for the measured training perturbations and context evidence for whether `Slc17a5` RNA is normally variable in this cell group, but it does not contain an observed `Slc17a5` knockout signature.

## Sources used

- Declared DE Parquet: `training differential-expression dataset`.
- Declared focal training DEG counts: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Requested held-out target manifest: `single-target request for Slc17a5`.
- Run-local metadata: `task_bindings.json`, `coverage.json`, `capabilities.json`, `measurement_registry.json`, and the PerturbAI atlas dataset portrait in `dataset_context.md`.
- Internal same-experiment corpus: the July 260713 sourceguard PerturbAI Finding ledger, queried through `findings-ledger-skill`, for report-grounded interpretations of measured `Atp6v0a1`, `Lamp2`, `Ppt1`, and `Rab7` perturbations. This corpus is an interpretation layer over the same experiment, not an independent replicate.
- External literature from PubMed for the biological prior on SLC17A5/sialin and lysosomal compensation.

The prediction is not a ranked-output task and it has no ranked or partial-ranked gene supervision. The `dataset.perturbseq_features`, `corpus.predictive_graph_review`, and `synthesis.ordering_validate` capabilities were therefore unavailable by manifest and were not used.

## Computations over the training data

The focal training table had 1,674 non-held-out perturbations. Its response-breadth distribution was sparse:

| category | perturbations |
|---|---:|
| `n_degs = 0` | 1,205 |
| `n_degs = 1` | 276 |
| `n_degs = 2..5` | 65 |
| `n_degs = 6..20` | 50 |
| `n_degs > 20` | 78 |

I searched the training target names for direct and pathway analogs: `Slc17*` family members, sialic-acid biosynthetic/catabolic genes (`Gne`, `Nans`, `Cmas`, `Neu*`, `St3gal*`), V-ATPase genes, lysosomal hydrolases and membrane genes, autophagy genes, endolysosomal traffic genes, and glutamate receptor/synaptic genes. Close sialin-pathway coverage was limited. The only visible sialylation target in that list was `St3gal5`, with `n_degs = 1`; none of `Gne`, `Nans`, `Cmas`, `Neu1`, or `Slc17a6/7/8/9` were in the focal training count file.

For biologically plausible measured analogs, I streamed only the `151 TH Prkcd Grin2c Glut` row groups of the Parquet and tabulated all genes with `pvals_adj < 0.05`. Each measured focal target had 17,259 tested expression rows. This was used to separate real downstream programs from one-gene self hits:

| measured perturbation | focal `n_degs` | expression-pattern evidence in `151 TH Prkcd Grin2c Glut` |
|---|---:|---|
| `Atp6v0a1` | 1 | only `Atp6v0a1` itself passed FDR, log2FC -0.640, adjusted p = 4.52e-12 |
| `Atp6v1a` | 0 | no FDR genes |
| `Atp6v1b2` | 0 | no FDR genes |
| `Atp6v1e1` | 0 | no FDR genes |
| `Lamp2` | 0 | no FDR genes; `Lamp2` itself was just subthreshold, adjusted p = 0.0537 |
| `Ppt1` | 1 | only `Ppt1` itself passed FDR, log2FC -0.536, adjusted p = 1.34e-05 |
| `Ctsb` | 1 | only `Ctsb` itself passed FDR, log2FC -1.480, adjusted p = 8.54e-43 |
| `St3gal5` | 1 | only `St3gal5` itself passed FDR, log2FC -0.788, adjusted p = 1.96e-14 |
| `Sqstm1` | 1 | only `Sqstm1` itself passed FDR, log2FC -0.565, adjusted p = 7.93e-04 |
| `Rb1cc1` | 4 | small ER/autophagy initiation response: `Hspa5`, `Calr`, `Rb1cc1`, `Pdia6` |
| `Vps35` | 17 | modest retromer/traffic response including `Vps35` self-down and `Grin2b` down |
| `Tsc2` | 86 | mTOR/TSC-linked response; a larger counterexample, not the same causal sign as loss of a single lysosomal exporter |
| `Rab7` | 501 | broad late-endosome/lysosome stress signature, led by `Atp6v1b2`, `Ptgds`, `Dpp7`, `Scpep1`, `Dusp1`, `Insig1`, and `Atp6v0b` |

I also queried the `Slc17a5` measured-expression row across all 1,674 focal training contrasts. `Slc17a5` was present in every contrast, its median log2FC under unrelated perturbations was -0.0016, and none of those contrasts had an adjusted p-value below 0.05 for `Slc17a5`; the best unrelated adjusted p-value was 0.0577 in `Tpr`-perturbed cells. This makes `Slc17a5` a real tested gene in the focal class, while arguing that it is not a generic readout of the broad stress programs that dominate high-count perturbations.

## Biological transfer model

`Slc17a5` encodes sialin, a proton-coupled lysosomal exporter for free sialic acid. Pathogenic SLC17A5 variants cause free sialic acid storage disorders, including infantile sialic acid storage disease and Salla disease, by trapping free sialic acid in lysosomes; affected patients have neurodevelopmental and neurodegenerative features with hypomyelination and cerebellar/corpus-callosum abnormalities (Verheijen et al. 1999, DOI: 10.1038/70585; Huizing et al. 2021, DOI: 10.1016/j.neulet.2021.135896). Sialin has also been reported in neuronal processes and at extralysosomal neuronal membranes (Aula et al. 2004, DOI: 10.1016/j.nbd.2003.11.017) and to catalyze vesicular uptake of aspartate/glutamate or NAAG in some experimental systems (Miyaji et al. 2008, DOI: 10.1073/pnas.0804015105; Lodder-Gadaczek et al. 2013, DOI: 10.1042/BJ20130300), although vesicular aspartate release independent of sialin has also been reported (Morland et al. 2012, DOI: 10.1096/fj.12-206300).

The transfer chain I used was:

1. AAV CRISPR loss of `Slc17a5` at P16 partially disrupts sialin in postmitotic thalamic glutamatergic neurons.
2. The direct expected molecular consequence is reduced free-sialic-acid export from lysosomes, with possible changes in sialic-acid recycling, storage, and in some neurons vesicular acidic amino-acid handling.
3. Only if that perturbation is strong and persistent enough should it propagate into TFEB/CLEAR lysosomal biogenesis, sterol handling, autophagy, or ISR/UPR transcription. TFEB can drive coordinated autophagy/lysosome transcripts (Settembre et al. 2011, DOI: 10.1126/science.1204592); lysosomal V-ATPase and Rag/Ragulator signaling can couple luminal amino-acid state to mTORC1 (Zoncu et al. 2011, DOI: 10.1126/science.1207056); and RAB7 controls late-endosomal/lysosomal trafficking and lysosome positioning/function (Guerra and Bucci 2016, DOI: 10.3390/cells5030034).
4. The experiment measures nuclear RNA only in surviving, recovered, class-assigned neurons 3-4 weeks later, so chronic storage, lipid composition, myelination, or vesicle physiology can be missed even when the direct transporter biology is real.

## Target-specific prediction for `Slc17a5`

The strongest within-dataset signal was the near-null behavior of perturbations that should disturb lysosomal degradation or acidification but do not necessarily create a large nuclear RNA response in this acute postnatal setting. `Atp6v0a1` is a V-ATPase subunit with a direct lysosome-acidification role; in the focal class its single DEG was only its own transcript. `Atp6v1a`, `Atp6v1b2`, and `Atp6v1e1` were all zero. `Lamp2` was also zero despite being a lysosomal membrane disease gene, and its same-experiment corpus report noted absence of corrected lysosome, autophagy, proteasome, UPR/ISR, and redox marker programs after acute `Lamp2` loss. `Ppt1` and `Ctsb` were both one-gene self hits; the `Ppt1` report likewise described a pan-neuronal downstream null rather than a neuronal-ceroid-lipofuscinosis-like transcriptome. These are the closest endpoint analogs for a single lysosomal storage or lysosomal membrane perturbation.

`St3gal5` is not a lysosomal transporter, but it is a sialic-acid/ganglioside enzyme and was a useful counterweight against predicting a complete lack of target self-detection: its focal signature contained one DEG, `St3gal5` itself. The generic solute-carrier set was mostly equally small: `Slc1a1`, `Slc1a2`, `Slc22a17`, `Slc25a12`, `Slc25a4`, `Slc25a46`, and `Slc9a7` each had `n_degs = 1`, while most other measured `Slc*` perturbations were zero. Glutamatergic synaptic comparators were not good positive analogs: `Grin1` gave 89 DEGs, but `Slc17a5` is not the core NMDA receptor subunit; subunit perturbations `Grin2a` and `Grin2b` had only 1 and 2 DEGs, and `Syp`/`Syn1` were self-only one-gene hits.

The main counterexamples were `Rab7`, `Tsc2`, and `Vps35`. I did not transfer `Rab7`'s 501-gene focal count because Rab7 loss impairs a central late-endosomal GTPase and broadly induced lysosomal, sterol, ISR/UPR, autophagy, redox, proteasome, and synaptic-remodeling transcripts in the same corpus. That is a propagation event from blocked late-endosome/lysosome traffic and organelle stress, not just the storage of one acidic sugar species. `Tsc2` acts on mTORC1 with the opposite biochemical sign from reducing lysosomal export, and `Vps35` retromer loss is closer to global protein sorting than to a metabolite exporter. These larger perturbations show that the focal cell class can mount a large nuclear response, but they do not justify assigning such a response to `Slc17a5`.

The point estimate is therefore `1`: I expect acute `Slc17a5` CRISPR to be small enough that no downstream lysosomal or synaptic program crosses BH FDR 0.05, but I expect the `Slc17a5` transcript itself to be expressed in these neurons and to be capable of becoming the lone significant row, as with `Atp6v0a1`, `Ppt1`, `Ctsb`, and `St3gal5`.

## Limits

This is an extrapolation from mechanism and neighbors, because there is no directly observed held-out `Slc17a5` expression signature. The training set lacks the tightest biochemical comparators in sialic-acid synthesis and recycling (`Gne`, `Nans`, `Cmas`, `Neu1`) and lacks vesicular glutamate transporter family members `Slc17a6`, `Slc17a7`, `Slc17a8`, and `Slc17a9`. A one-gene prediction is also sensitive to self-transcript detectability and guide behavior, neither of which can be read from the held-out DE file. Finally, known SLC17A5 disease phenotypes involve chronic biallelic dysfunction, storage, development, glia/myelination, and sometimes non-transcriptional vesicle physiology; a sparse P16 neuronal CRISPR perturbation assayed only by nuclear RNA can miss those endpoints entirely.
