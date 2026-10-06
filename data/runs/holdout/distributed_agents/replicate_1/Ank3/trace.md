# Ank3 DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

The task asks for one integer prediction for each perturbation in the requested-target manifest. This run contained exactly one held-out target:

```tsv
target_name
Ank3
```

The endpoint is `n_degs`, the number of measured genes in `151 TH Prkcd Grin2c Glut` cells with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05`. The count includes the perturbed gene's own mRNA when it is measured and significant; this is why many sparse training perturbations have `n_degs = 1` consisting only of the self-transcript row. `Ank3` itself was fully held out: I verified that no `gene_target = 'Ank3'` row is present in the supplied DE Parquet, and it is absent from the training DEG-count CSV.

I interpreted `151 TH Prkcd Grin2c Glut` as the focal thalamic glutamatergic class defined by the dataset label, not tyrosine-hydroxylase dopaminergic cells.

## Sources used

- Declared differential-expression Parquet: `training differential-expression dataset`
- Declared focal training counts: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
- Requested-target manifest: `single-target request for Ank3`
- Dataset portrait and measurement registry in `codex_runtime/pipeline`, used to keep the interpretation restricted to sparse P16 postmitotic AAV-CRISPR loss of function and survivor-conditioned 10x Flex snRNA differential expression.
- PerturbAI July same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`, used for compact packaged interpretation of measured training perturbations such as `Ank1`, `Ank2`, `Sptan1`, `Nrcam`, `Scn2a`, and `Kcnq2`. This corpus is another representation of the same experiment, not independent validation.
- NCBI PubMed literature for the ankyrin-G/AIS mechanism.

## Computations over the declared data

I read the focal training CSV directly and computed the scale of `n_degs` over 1,674 non-held-out targets. The distribution was sparse and strongly outlier-skewed:

```text
min = 0
median = 0
75th percentile = 1
90th percentile = 2
95th percentile = 18
99th percentile = 436.5
max = 2677
nonzero targets = 469 / 1674
```

The high counts belonged to broad nuclear or proteostasis regulators, for example `Uba5` 2677, `Tpr` 1768, `Sin3a` 1433, `Rnpc3` 868, and `Zbtb7a` 841. I therefore treated the genome-wide mean of 14 as a poor prior for a membrane scaffold such as `Ank3`.

I then queried the Parquet with DuckDB, restricted to `group_name = '151 TH Prkcd Grin2c Glut'`, for represented ankyrin/spectrin/AIS/adhesion/channel comparators. The relevant exact focal counts were:

| training target | observed `n_degs` in 151 | focal FDR-significant rows |
|---|---:|---|
| `Ank1` | 0 | none |
| `Ank2` | 0 | none |
| `Ank` | 1 | `Ank` self row |
| `Sptan1` | 1 | `Sptan1` self row |
| `Sptb` | 0 | none |
| `Add1` | 0 | none |
| `Add2` | 0 | none |
| `Add3` | 0 | none |
| `Actg1` | 1 | count 1 in the training CSV |
| `Mapre2` | 1 | count 1 in the training CSV |
| `L1cam` | 1 | count 1 in the training CSV |
| `Chl1` | 1 | count 1 in the training CSV |
| `Nrcam` | 2 | `Nrcam` self row and `Letm2` up |
| `Cntnap1` | 1 | `Cntnap1` self row |
| `Cntnap2` | 1 | `Cntnap2` self row |
| `Nrp1` | 0 | none |
| `Nrp2` | 0 | none |
| `Scn1a` | 1 | `Scn1a` self row |
| `Scn1b` | 2 | `Scn1b` self row and `Jun` up |
| `Scn2a` | 1 | `Scn2a` self row |
| `Scn3a` | 0 | none |
| `Scn8a` | 1 | `Scn8a` self row |
| `Kcnq1` | 0 | none |
| `Kcnq2` | 1 | `Kcnq2` self row |
| `Kcnq3` | 1 | `Kcnq3` self row |

For the nearest structural ankyrin/spectrin comparators, the exact focal self rows were:

| training target | self log2FC in 151 | self FDR in 151 |
|---|---:|---:|
| `Ank1` | 0.209 | 1.000 |
| `Ank2` | -0.127 | 1.000 |
| `Sptan1` | -0.529 | 2.03e-13 |
| `Nrcam` | -0.650 | 2.94e-15 |
| `Kcnq2` | -0.776 | 2.12e-28 |

This matters because the held-out count for `Ank3` can be nonzero even if no downstream gene responds, provided the `Ank3` self-transcript row crosses FDR. Conversely, the `Ank1` and `Ank2` zeros show that ankyrin family membership alone does not guarantee even a self call.

## Biological analogs and counterexamples

### Ankyrin paralogs

`Ank2` is the cleanest in-dataset ankyrin paralog counterexample. In the July same-experiment corpus, `Ank2` was described as a pan-null transcriptional perturbation: all 23 recovered neuronal groups had zero downstream FDR<0.10 genes. The focal class had 218 perturbed nuclei, `Ank2` log2FC -0.127, FDR 1.000, and zero genes at the task's FDR<0.05 endpoint. The expected AnkB440 biology is axon guidance, L1CAM/neuropilin/Sema3A surface signaling, cofilin phosphorylation, axonal organelle transport, and synaptic membrane proteome regulation; those are local cytoskeletal, phosphorylation, localization, or electrophysiology phenotypes rather than an obligate cell-wide nuclear RNA state.

`Ank1` is the other represented ankyrin family member and was also zero in `151 TH Prkcd Grin2c Glut`. Across the same-experiment corpus, its only FDR<0.10 downstream event was a single `B4galnt1` decrease in the non-focal `217 P MY Pineal Glut` class; represented ankyrin, spectrin, adducin, and Kv3-channel neighbors did not converge as a shared RNA module. That weakens any argument that reducing an ankyrin scaffold generically triggers a large acute transcriptional response in this assay.

These two zeros are strong within-dataset evidence against predicting a multi-gene `Ank3` footprint.

### AIS cytoskeleton and membrane partners

Ankyrin-G is not merely interchangeable with AnkR or AnkB: the giant AnkG isoform is a master scaffold for the axon initial segment, where it recruits beta-IV spectrin, neurofascin-186, voltage-gated sodium channels, Kv7 channels, and actin/microtubule-associated machinery. Yang et al. 2019 showed that neurodevelopmental mutations in giant ankyrin-G disrupt ordered ankyrin-G/beta-IV-spectrin assembly at the AIS and alter the AIS lattice through a phosphorylation-regulated conformational transition (PMID 31451636, DOI 10.1073/pnas.1909989116). Freal et al. 2016 showed that 480 kDa AnkG cooperates with EB proteins to assemble the AIS in rodent hippocampal neurons (PMID 27098687, DOI 10.1523/JNEUROSCI.3219-15.2016). Leterrier et al. 2017 showed that ankyrin-G membrane partners such as Nav channels and neurofascin-186 help establish and maintain ankG at the AIS (PMID 28184187, DOI 10.3389/fncel.2017.00006). He et al. 2022 resolved the AnkG/neurofascin interaction and showed that disrupting that complex abolishes Nfasc AIS enrichment in cultured mouse hippocampal neurons (PMID 35850303, DOI 10.1016/j.jbc.2022.102272). Berger et al. 2018 further placed ankyrin-G and beta-IV spectrin in a submembranous actin/myosin-II AIS assembly and plasticity mechanism (PMID 29395909, DOI 10.1016/j.neuron.2017.12.039).

Those sources make `Sptan1`, `Nrcam`, `L1cam`, `Chl1`, `Cntnap1`, `Cntnap2`, `Scn1a`, `Scn2a`, `Scn8a`, `Kcnq2`, and `Kcnq3` mechanistically more relevant than broad nuclear outliers, but the local training data show that even direct AIS or axonal membrane perturbations are transcriptionally buffered. `Sptan1` had one DEG in the focal class, its own down-regulated transcript, and the July corpus describes only two isolated non-target genes across all 23 cell groups. `Nrcam` had two focal DEGs, a self row plus `Letm2`, and its report emphasized near-absent downstream DE despite measured target knockdown. Sodium and Kv7 channel perturbations likewise had one or two focal DEGs dominated by the self transcript. These are useful analogs for the count scale, but not evidence for a shared downstream expression pattern.

### Other focal outliers

I did not transfer the hundreds-to-thousands of DEG counts from `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, `Zbtb7a`, `Psmb4`, or similar outliers. They are broad regulators of protein homeostasis, nuclear transport, splicing/chromatin, or transcription and they are not mechanistic analogs for postmitotic AnkG loss at the AIS. Their responses show that the `151` class had power to call large effects; they do not establish that an axon scaffold should have a large nuclear RNA footprint.

## Prediction for Ank3

My causal model was:

`Ank3` CRISPR loss of function -> reduced ankyrin-G scaffold protein at the AIS and nodes -> disorganization of beta-IV-spectrin, neurofascin/Nav/Kv7 clusters, EB/microtubule and actin periodic structure -> altered intrinsic excitability and AIS plasticity in recovered neurons -> possible homeostatic nuclear RNA response sampled 3-4 weeks after P16 editing.

The last arrow is the weakest part of the chain. The best direct training evidence says that this screen does not usually convert acute perturbation of ankyrin/spectrin/adhesion/channel genes into multi-gene nuclear DE. `Ank1` and `Ank2` are focal zeros; direct membrane partners and clients sit in the 0-2 range; and the few non-self genes such as `Letm2`, `Jun`, and `Agap2` are isolated rather than an AIS module.

I therefore predicted no robust downstream transcriptional program for `Ank3`. I nevertheless set the point count to 1, not 0, because ankyrin-G is a broadly neuronal and focal-cell-relevant AIS scaffold, and the represented focal AIS/channel/neurexin-neighborhood perturbations with clear target expression frequently contributed exactly one significant row through the self transcript (`Sptan1`, `Nrcam`, `Cntnap1`, `Cntnap2`, `Scn1a`, `Scn2a`, `Scn8a`, `Kcnq2`, `Kcnq3`). The `Ank1` and `Ank2` zeros are serious counterexamples because neither ankyrin paralog's self row was FDR-significant in the focal class; the single-count call for `Ank3` is driven by the stronger expectation of AnkG expression in thalamic glutamatergic neurons, not by any observed `Ank3` signature.

Final point prediction:

```tsv
target_name	predicted_n_degs
Ank3	1
```

## Limits

- The requested endpoint for `Ank3` is absent from the declared inputs. All reasoning is transfer from non-held-out perturbations plus external AIS biology.
- DNA indel rates and ankyrin-G protein loss are not measured. Self-transcript FDR is variable across genes and cannot be used as an editing-efficiency estimate.
- The best physical AnkG partners, especially `Nfasc`, `Sptbn4`, and `Sptbn1/2`, were not represented as training perturbations in the focal count table I inspected, so the analog set is incomplete.
- External AIS studies usually measured embryonic or cultured-neuron assembly, protein localization, morphology, and electrophysiology. The task endpoint is a sparse nuclear RNA snapshot from recovered postmitotic neurons after mosaic P16 AAV perturbation.
- `Ank3 = 1` is a boundary prediction. The evidence is strong against a large count but weaker on whether the self row itself would pass BH FDR in the held-out `151` contrast.
