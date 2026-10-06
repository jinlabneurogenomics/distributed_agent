# DEG-count prediction trace

## Question

The requested held-out perturbation list contains one target:

| target_name |
|---|
| Taf1 |

I interpreted the endpoint as the exact `151 TH Prkcd Grin2c Glut` count of assayed genes with `pvals_adj < 0.05` after acute AAV-PHP.eB CRISPR loss of function in postnatal mouse neurons. I treated the endpoint as an assay-specific breadth measure, not as a direct essentiality or viability score. `Taf1` itself is absent from both the training count table and from the training DE parquet as a perturbation target.

## Sources used

- Training endpoint CSV: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Training DE parquet: `[local file: training_de_all_cell_groups.parquet]`
- Requested-target manifest: `[local file: 231_Taf1.csv]`
- Distributed Agents internal corpus: `perturbai-july-260713-sourceguard-1773-v1`. This release had no `Taf1` target page, but it did contain same-experiment finding summaries for `Brd4`, `Yy1`, `Sin3a`, and `Med15` that I used to check whether their observed training signatures were true mechanistic comparators or counterexamples.
- NCBI PubMed literature search for external TAF1/TFIID biology.

## Same-assay calibration

The focal training table has 1,674 perturbations. Most are null in this readout:

| statistic | n_degs |
|---|---:|
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| 99th percentile | 436 |
| max | 2677 |

There are 469 nonzero training targets, so an uncalibrated "important gene -> broad response" rule would badly overcall the endpoint.

I then filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` for TFIID-adjacent and broad transcriptional/chromatin controls and counted rows with `pvals_adj < 0.05`; those counts matched the training CSV. The relevant observations were:

| training perturbation | observed n_degs | expression-pattern evidence in 151 cells | interpretation for Taf1 |
|---|---:|---|---|
| `Taf1b` | 0 | no FDR genes | Name similarity is misleading. TAF1B is a SL1/RNA polymerase I factor rather than the core Pol II TFIID subunit TAF1; I treated it as a counterexample to superficial `Taf*` matching. |
| `Gtf2h5` | 0 | no FDR genes | A general TFIIH subunit can be silent in this screen, arguing that basal transcription-factor annotation alone is insufficient. It is not a close TFIID structural analog. |
| `Gtf2i` | 10 | a narrow idiosyncratic signature including target self-repression (`Gtf2i` log2FC -0.89), `Kcnk4`, `Rasgrp2`, `Catsperz`, `Notum` | A transcription-factor perturbation with good on-target mRNA signal can still be narrow. |
| `Med15` | 19 | mostly down-regulated neuronal/subtype genes; examples include `Prkcd`, `Pcp4`, `Lef1`, `Ptpn3`, `Atp2a2`, `Atp2b1`, `Grm1` | The best within-dataset model for a basal Pol II coactivator in this focal class: nonzero, coherent, but small. |
| `Med23` | 13 | overlaps `Med15` on down-regulated `Prkcd`, `Pcp4`, `Lef1`, `Grm1`, `Plekhg1`, `Atp2a2`, `Atp2b1`, `Ptpn3` | Supports a reproducible Mediator-sensitive 151-cell state in the 10-20 DEG range. |
| `Med13` | 11 | same down-regulated 151-cell module, including `Prkcd`, `Lrrtm1`, `Pcp4`, `Plekhg1`, `Atp2a2`, `Grm1`, `Ildr2`, `Kcnc2` | Kinase-module scaffolding converges with the small core Mediator response. |
| `Med13l` | 1 | only `Grm1` at FDR 0.05 in 151 | Even a close paralog of a Mediator responder can be nearly flat. |
| `Cdk8` | 0 | no FDR genes | Further boundary against assuming every Mediator or general transcription regulator responds. |
| `Ep300` | 0; `Crebbp` 8 | `Crebbp` had only eight genes; `Ep300` was flat | HAT/coactivator annotations are not enough to predict a broad effect in this assay. |
| `Brd4` | 311 | a larger program with strong decreases of differentiated neuronal genes, e.g. `Slco4a1`, `Pvalb`, `Hpca`, `Irag1`, `Fstl1`, and scattered inductions | TAF1 has bromodomains and participates in transcription initiation, but the Distributed Agents Brd4 context explicitly reported that Mediator, p300/CBP, and MYC-axis comparators did not phenocopy `Brd4`; I used `Brd4` as an upper-bound counterexample, not a direct template. |
| `Yy1` | 720 | broad mixed posterior-neuron response with recurrent RNA-processing/chromatin genes | YY1 can recruit or interface with basal transcription machinery, but the same-experiment Yy1 state sits near several chromatin regulators rather than a measured core TFIID-like module. |
| `Sin3a` | 1433 | broad stress/proteostasis/RNA-processing and metabolic response | Shows the 151-cell assay can report very wide chromatin-regulator states; SIN3A is mechanistically too different from TFIID to set the Taf1 scale. |

The Distributed Agents `Med15` context was especially useful because it had already compared directly measured Mediator perturbations in this same dataset: `Med13`, `Med15`, and `Med23` converge on the down-regulated 151-cell module, whereas `Med13l` and `Cdk8` do not phenocopy it. That made the 10-20 DEG Mediator band more credible than any single count. A small profile-neighborhood run over these candidate profiles gave the same qualitative result: `Med13`, `Med15`, and `Med23` cluster through the weak down-regulated focal-cell module, while the broad `Brd4`/`Yy1`/`Sin3a` signatures are much larger and mostly distinct at the FDR-gene level.

## External biology for Taf1

TAF1 is the largest integral TFIID subunit. Human TFIID is built from TBP and TAF1-13 and recognizes multiple core-promoter elements; structural work places TAF1 and TAF2 at downstream promoter DNA during Pol II pre-initiation complex assembly (Louder et al. 2016, DOI: 10.1038/nature17394). TAF1 itself contains promoter-contacting DNA-binding modules required for TFIID occupancy and cellular rescue in experimental systems (Wang et al. 2014, DOI: 10.1038/cr.2014.148; Curran et al. 2018, DOI: 10.1038/s41598-018-22879-5), and TFIID has also been implicated in RNA Pol II promoter-proximal pausing rather than just start-site selection (Fant et al. 2020, DOI: 10.1016/j.molcel.2020.03.008).

The neuronal prior is non-null. Human TAF1 dysregulation is linked to X-linked dystonia-parkinsonism through an intronic SVA insertion that alters TAF1 expression/splicing (Bragg et al. 2019, DOI: 10.1097/WCO.0000000000000708), and recent reviews summarize TAF1 as both a core Pol II factor and a gene whose missense or regulatory lesions cause neurodevelopmental and neurodegenerative phenotypes (Crombie et al. 2024, DOI: 10.1098/rsos.240790). Complete ubiquitous mouse `Taf1` loss is severe: a conditional mouse knockout produced embryonic lethality in males, consistent with intolerance of full null TAF1 depletion (Crombie et al. 2024, DOI: 10.1242/dmm.050741).

Those facts argue that acute `Taf1` loss should not be forced to zero. They do not argue for a thousand-DEG prediction: the experiment only achieved partial mRNA depletion on average, postmitotic neurons may have stable pre-existing TFIID protein, and broad Pol II factors can be buffered in steady-state snRNA endpoints.

## Target-specific prediction

### Taf1

`Taf1` has no direct TFIID paralog or same-complex partner represented in the training perturbations: `Tbp`, `Taf2-13`, `Gtf2a1/2`, `Gtf2b`, `Gtf2e1/2`, `Gtf2f1/2`, and most TFIIH subunits were held out or absent. I therefore weighted exact biology over name matching.

The closest useful positive comparators were the convergent Mediator subunits:

- `Med15`: 19 DEGs, dominated by down-regulation of focal neuronal markers and signaling genes.
- `Med23`: 13 DEGs, sharing `Prkcd`, `Pcp4`, `Lef1`, `Grm1`, `Plekhg1`, `Atp2a2`, `Atp2b1`, and `Ptpn3` with the Med15 direction.
- `Med13`: 11 DEGs, overlapping the same 151-cell down-module.

The most important counterexamples were:

- `Gtf2h5`: 0 DEGs, showing a represented basal-transcription subunit can be silent.
- `Cdk8`: 0 and `Med13l`: 1, showing that even a related Mediator kinase module is not interchangeable with the weak Med13/Med15/Med23 state.
- `Ep300`: 0, `Crebbp`: 8, `Myc`: 0, `Mycn`: 0, showing that central transcriptional coactivators or downstream pro-growth transcription factors are often buffered in the postmitotic endpoint.
- `Brd4`, `Yy1`, `Sin3a`: 311-1433 DEGs, showing that the assay can detect very broad transcriptional/chromatin responses but that these are separate programs, not generic consequences of hitting any core regulatory protein.

I predict `Taf1` will cross FDR in this 151-cell population because TAF1 is a uniquely central TFIID promoter-recognition subunit and has strong neuronal disease genetics. I kept the point estimate only modestly above the Mediator subunit band because no represented close TFIID perturbation shows a broad response and because the strongest measured chromatin signatures are mechanistically too stress-like or enhancer/chromatin-loop-like to borrow wholesale for TAF1.

**Prediction:** `Taf1 -> 24` DEGs.

## Limits

This is an extrapolation from imperfect analogs. The training set lacks `Tbp`, all Pol II core `Taf` subunits, and direct TAF1/TBP complex members, so there is no same-complex count to transfer. mRNA-level CRISPR down-regulation and protein depletion are unmeasured for held-out `Taf1`; TFIID may be stable enough that a true signature would be flat, or TAF1 depletion may be stronger than the Mediator analogs and drive a broad essential-gene response. Finally, X-linked dystonia-parkinsonism and complete mouse knockout literature constrain the biological plausibility of TAF1 sensitivity but differ from this sparse, juvenile, postmitotic, mosaic CRISPR assay.
