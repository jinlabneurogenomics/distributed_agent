# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

The requested held-out target list contains one perturbation, `Nav3`. I interpreted the task as a scalar prediction of the count of measured nuclear genes with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` after acute mosaic CRISPR loss of `Nav3` in juvenile mouse `151 TH Prkcd Grin2c Glut` neurons. The count includes the perturbed gene itself when its own mRNA passes the same FDR threshold; it is not limited to downstream genes.

`Nav3` was absent from the supplied training count CSV and from the `gene_target` column of the supplied differential-expression Parquet, as expected for a held-out perturbation. It was present as a measured `names` feature in all 1,674 visible focal-cell training perturbations, so a self-transcript FDR hit is experimentally possible.

## Sources

Internal run-local inputs:

- `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed focal-cell `n_degs` for 1,674 non-held-out perturbations.
- `training differential-expression dataset`: per-gene Wilcoxon statistics for the same non-held-out perturbations.
- `single-target request for Nav3`: requested target list, containing only `Nav3`.
- PerturbAI atlas July semantic corpus `perturbai-july-260713-sourceguard-1773-v1`: compact `Map1b`, `Ctnnb1`, and `Dctn1` Findings used to interpret the same experiment's expression patterns.

External literature:

- Sandeep et al. 2023, Mol Cell Neurosci, DOI `10.1016/j.mcn.2023.103905`: review of NAV family proteins as microtubule plus-end tracking/cytoskeletal proteins involved in neurite outgrowth, neuronal migration, and neurodevelopment.
- Ghaffar et al. 2024, Commun Biol, DOI `10.1038/s42003-024-06466-1`, PMID `38977784`: human NAV3 variants cause neurodevelopmental phenotypes; mouse brain `Nav3` is expressed across postmitotic excitatory, inhibitory, and sensory neurons; pathogenic NAV3 variants impaired microtubule stabilization and zebrafish `nav3` knockdown caused neurodevelopmental morphology defects rescued by wild-type NAV3.
- Kakar et al. 2024, Hum Genet, DOI `10.1007/s00439-024-02718-6`, PMID `39708122`, and Umair et al. 2024, Mol Genet Genomic Med, DOI `10.1002/mgg3.2473`, PMID `39038237`: biallelic NAV3 loss-of-function/splicing variants support NAV3 as a recessive human neurodevelopmental-disorder gene.
- Accogli et al. 2022, Cerebellum, DOI `10.1007/s12311-022-01379-3`, PMID `35218524`: the related neuron-navigator family member NAV2 is conserved for CNS development, cytoskeletal dynamics, migration, and neurite outgrowth, but its strongest organismal phenotypes are developmental and cerebellar.

## Dataset calculations

I treated the training `n_degs` CSV as the authoritative endpoint values for visible perturbations, and used Parquet predicates on `group_name == "151 TH Prkcd Grin2c Glut"` to inspect the actual genes underlying candidate analogs. The focal distribution is sparse: among 1,674 training targets, the median was 0, the 75th percentile was 1, only 469 targets were nonzero, and the maximum was 2,677.

To calibrate whether a one-gene count can be purely an on-target mRNA effect, I also queried focal rows where `names = gene_target`. There were 1,642 visible targets with a self row, 319 had a significant self transcript, and 237 of the 1,450 targets with `n_degs <= 1` had a significant self transcript. None of the 1,175 targets with `n_degs = 0` had a significant self transcript. Thus, when a structurally important but downstream-flat target registers in this assay, `n_degs = 1` often means "self only."

The training targets most closely related to `Nav3` by mechanism were:

| training target | focal `n_degs` | expression-pattern evidence in the focal cell group | relevance to `Nav3` |
|---|---:|---|---|
| `Map1b` | 1 | `Map1b` itself was the only FDR<0.05 gene (`log2FC = -0.358`, `padj = 1.06e-05`). The July corpus reports a transcript-self-only response in both 151 and 155 and no robust downstream tubulin-tyrosination, axon-growth, neuronal-migration, or GSK3/MAP1B RNA module. | Like NAV3, MAP1B is a neuronal microtubule/axon-growth effector whose best-established phenotypes are structural and post-transcriptional. |
| `Mapt` | 1 | `Mapt` itself was the only significant row (`log2FC = -0.533`, `padj = 1.43e-05`). | Neuronal microtubule-associated protein; a negative counterexample to expecting all cytoskeletal perturbations to make broad transcriptional signatures. |
| `Map6` | 0 | No gene passed FDR; the target row had `padj = 0.33`. | Structural microtubule biology without a focal nuclear response. |
| `Mapre2` | 1 | `Mapre2` itself was the only FDR hit (`log2FC = -0.464`, `padj = 5.22e-04`). | EB-family microtubule plus-end biology is closer to the NAV3 localization axis than to Wnt or stress signaling, yet remained self-only. |
| `Map1lc3a` | 1 | `Map1lc3a` itself was the only FDR hit (`log2FC = -0.565`, `padj = 6.46e-04`). | Cytoskeletal/autophagy-adjacent comparator; no compensatory nuclear cascade. |
| `Tuba1a` | 7 | Significant self decrease and a small beta-tubulin/alpha-tubulin compensation signature: `Tubb3`, `Tubb2a`, `Tuba4a`, `Tubb4a`, `Tubb4b`, and `Tubb5` were the other FDR<0.05 genes. | A counterexample showing that a core tubulin subunit can cross into a modest transcriptional feedback program; it is more core and more dosage sensitive than a NAV-family accessory factor. |
| `Dctn1` | 75 | Strong up-regulation of a sterol/SREBP-like module in the same focal cells, led by `Insig1`, `Msmo1`, `Hmgcs1`, and `Cyp51`; the July corpus reports 450 downstream DE genes across the Map1b-matched groups. | Counterexample: some microtubule-transport perturbations are detected broadly, but dynactin impairment is a retrograde-organelle-transport stress that is not the same causal stage as NAV3-mediated neurite guidance. |
| `Dcc`, `Unc5c`, `Unc5d`, `Neo1` | 0, 1, 0, 0 | Netrin-receptor knockouts were null or self-only. `Unc5c` had exactly one DEG, itself (`log2FC = -0.536`, `padj = 2.04e-04`); `Dcc`, `Unc5d`, and `Neo1` had none. | NAV proteins are homologous to the UNC-53 guidance family but are not themselves canonical netrin receptors. The null/self-only netrin-receptor outcomes argue against a broad axon-guidance RNA state after postnatal partial loss. |
| `Robo1`, `Robo2`, `Robo4`, `Slit2` | 1, 0, 0, 0 | Slit/Robo perturbations were null or self-only; `Robo1`'s sole hit was `Robo1` (`log2FC = -0.538`, `padj = 2.72e-06`). | A second axon-guidance counterexample independent of netrin signaling. |
| `Epha2`, `Epha3`, `Epha4`, `Epha5`, `Ephb1`, `Ephb2`, `Sema4d`, `Sema5a`, `Sema6a`, `Plxna1`, `Plxna2`, `Plxna4`, `Plxnd1`, `Ncam1`, `L1cam` | all 0 or 1 | Eph, semaphorin/plexin, NCAM, and L1CAM perturbations were all null or self-only; `Epha4`, `Sema5a`, `Plxna2`, `Ncam1`, and `L1cam` had only their own target transcript significant. | These are neuron-surface guidance/recognition genes. Their focal-cell flatness suggests that partial P16 loss of axon-guidance machinery in surviving postmitotic neurons rarely creates a large secondary transcriptome. |
| `Ctnnb1` | 383 | The July corpus reports a strong 151-class Wnt/adhesion and excitability response with loss of `Axin2`, `Lef1`, `Nkd1`, `Notum`, receptor/channel genes, and adhesion/guidance transcripts. | Important counterexample but not a direct analog: beta-catenin is a transcriptional Wnt effector and cadherin component, so its knockout is expected to change RNA programs much more directly than NAV3 loss. |

## `Nav3` prediction

`Nav3` encodes a large neuron-navigator cytoskeletal protein rather than a transcription factor, chromatin regulator, spliceosome factor, proteasome factor, sterol regulator, or core metabolic enzyme. External evidence supports an important role in neuronal morphogenesis and disease: pathogenic NAV3 variants impair microtubule stabilization and cause neurodevelopmental phenotypes, and the broader NAV family participates in neurite outgrowth and neuronal migration. That evidence makes `Nav3` biologically real, but most of it comes from germline human genetics, zebrafish embryos, or overexpression/knockdown morphology assays rather than acute postmitotic mouse thalamic neurons assayed by nuclear RNA.

The causal transfer model is therefore:

`Nav3` CRISPR loss in sparse postmitotic neurons -> reduced NAV3 cytoskeletal/microtubule plus-end function -> possible local neurite, migration, or morphology defects -> survival and recovery of the perturbed nuclei over 3-4 weeks -> Wilcoxon DE on nuclear RNA in recovered `151 TH Prkcd Grin2c Glut` nuclei.

The direct molecular and morphology stages are supported by external NAV3 biology; the propagation step into a broad thalamic nuclear expression program is not. Training perturbations that hit analogous guidance or microtubule accessory functions overwhelmingly stopped at zero or one FDR hit in the focal group. The most relevant positive expectations are that `Nav3` is detectable in the focal population and that self-only counts are common for expressed structural genes. The strongest negative expectations are that `Map1b`, `Mapt`, `Mapre2`, `Unc5c`, `Robo1`, `Epha4`, `Sema5a`, `Plxna2`, `Ncam1`, and `L1cam` did not generate downstream FDR<0.05 cascades, despite on-target transcript suppression in many of those cases.

I therefore predict a nonzero but minimal count:

- `Nav3`: **1 DEG**, representing an expected on-target `Nav3` mRNA decrease and no confidently predicted downstream genes at FDR<0.05.

## Limits

The largest uncertainty is the self-transcript term: `Nav3` is measurable in the focal cell group, but the training data show that self rows are significant for only 319 of 1,642 visible targets, so a true zero would be unsurprising if guide cutting left nuclear `Nav3` RNA mostly unchanged. The downstream prediction is also an extrapolation because neither `Nav1` nor `Nav2` was present in training. Dctn1 proves that this dataset can convert some microtubule/transport defects into sizeable nuclear homeostatic programs, but its sterol and retrograde-transport biology is candidate-specifically different from a NAV3 neurite-guidance loss. Conversely, germline or embryonic NAV3/NAV2 phenotypes establish a developmental requirement without proving a postnatal DEG burden after partial CRISPR loss in surviving thalamic glutamatergic neurons.
