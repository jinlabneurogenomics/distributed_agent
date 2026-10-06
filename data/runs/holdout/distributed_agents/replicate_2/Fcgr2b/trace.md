# Fcgr2b held-out DEG-count prediction

## Question and interpretation

The requested manifest contains one held-out target, `Fcgr2b`. I interpreted the task as a point prediction for the number of measured genes that would satisfy `pvals_adj < 0.05` after acute AAV/CRISPR loss of `Fcgr2b` in the focal neuronal group `151 TH Prkcd Grin2c Glut`. The held-out `Fcgr2b` perturbation itself is absent from both supplied training inputs, so the target row cannot be looked up; only non-held-out perturbations can be used to calibrate the likely count.

The main ambiguity is whether immune-lineage Fc-gamma receptor biology should be transferred into the NeuN-enriched neuronal readout. I resolved that in favor of a neuronal-context prediction: `n_degs` is a within-assay single-nucleus endpoint in recovered thalamic glutamatergic neurons, not a measurement of Fc-gamma effector-cell function in B cells, macrophages, or microglia.

## Sources used

- Raw same-experiment DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Focal-cell training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Requested-target manifest:
  `[local file: 074_Fcgr2b.csv]`
- The Distributed Agents same-experiment semantic corpus, release `perturbai-july-260713-sourceguard-1773-v1`.
- The Distributed Agents run-local observed-profile tools for a focal-cell comparison of immune/Fcgr-related training signatures.
- PubMed literature for Fc-gamma receptor IIB / Fcgr2b function and microglial Fc-receptor context.
- Background gene-function annotations from MGI / Alliance of Genome Resources and UniProtKB, used only to confirm that mouse `Fcgr2b` encodes the inhibitory low-affinity IgG Fc receptor CD32B/Fc-gamma RIIB.

## Computations over the training data

The manifest was first read directly and contains exactly:

```tsv
target_name
Fcgr2b
```

I loaded the focal training-count CSV and summarized the empirical count scale:

- 1,674 non-held-out perturbations are available in `151 TH Prkcd Grin2c Glut`.
- 1,205 / 1,674, or 72.0%, have `n_degs = 0`.
- 363 additional targets have only 1-9 DEGs.
- The distribution is highly skewed; the median is 0, the 90th percentile is 2, and only 43 training perturbations have at least 100 DEGs.

I then filtered the DE parquet to the focal cell group and several Fcgr2b-relevant immune-lineage comparators. For each `gene_target`, I counted rows with `pvals_adj < 0.05` and checked that the result matched the training endpoint where the target was present.

| training target | focal observed `n_degs` | reason for considering it |
| --- | ---: | --- |
| `Fcgr4` | 0 | only Fc-gamma receptor family perturbation represented in the focal training-count CSV |
| `Axl` | 0 | TAM/phagocytic receptor; microglial phagocytosis axis |
| `Mertk` | 0 | TAM paralog / efferocytosis comparator for `Axl` |
| `Csf1r` | 0 | canonical microglial lineage/survival receptor |
| `Cx3cr1` | 0 | neuron-to-microglia fractalkine receptor, microglial/off-neuronal comparator |
| `P2ry12` | 0 | homeostatic microglial purinergic receptor |
| `Spi1` | 0 | PU.1, a myeloid-lineage transcription-factor comparator |
| `Tlr2` | 0 | innate immune pattern-recognition receptor |
| `Tlr4` | 0 | innate immune pattern-recognition receptor |
| `Tlr7` | 0 | innate immune pattern-recognition receptor |
| `Ifngr1` | 0 | interferon-gamma receptor |
| `Ifngr2` | 0 | interferon-gamma receptor |
| `Irf1` | 0 | interferon / antigen-presentation transcriptional regulator |
| `Irf8` | 0 | myeloid and interferon regulatory factor |
| `Irf9` | 0 | interferon-stimulated-gene regulator |
| `Nfkb1` | 0 | inflammatory NF-kB pathway target |
| `Stat1` | 1 | the lone focal FDR hit was `Stat1` itself, not a broad IFN/MHC module |

Within the training set, `Fcgr4` was the only `Fcgr*` perturbation; `Fcgr1`, `Fcgr3`, `Fcer1g`, `Lyn`, and `Syk` were not available as perturbed training targets. I therefore treated the Fcgr comparison as close but incomplete, and used the broader myeloid and inflammatory panel above as a boundary rather than as redundant copies of `Fcgr2b`.

I also checked measured Fc-receptor and microglial transcripts as DE features across all 1,674 training perturbations in the focal cell group. `Fcgr2b`, `Fcgr1`, `Fcgr3`, `Fcgr4`, `Fcer1g`, `Tyrobp`, `Trem2`, `Axl`, `Csf1r`, `Mertk`, `P2ry12`, and `Spi1` each had 1,674 rows and zero adjusted-significant appearances as measured genes in `151 TH Prkcd Grin2c Glut`. That does not provide baseline expression counts, but it is consistent with the Fc-receptor / microglial axis being transcriptionally absent or below DE resolution in these neuronal nuclei.

Finally, I used the Distributed Agents profile-comparison tool on a focal cohort
`Axl, Csf1r, Cx3cr1, Fcgr4, Mertk, P2ry12, Spi1, Tlr2, Tlr4, Tlr7`.
All ten nodes were available and all ten were classified as having no FDR 0.05 significant features. Inspecting the `Fcgr4`-centered projection confirmed zero positive or negative significant features for every `Fcgr4` pair; any whole-profile correlations among these all-flat signatures were therefore treated as shared inactivity rather than as a transferable expression program.

## Same-experiment corpus evidence

`Fcgr2b` itself has no target report or claim in Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`, so there was no hidden held-out result to use. Its absence was handled as missing annotation.

The corpus did, however, contain a high-confidence `Fcgr4` report:

- `Fcgr4:F001`: `Fcgr4` loss of function produced no robust cell-autonomous transcriptional response in any measured NeuN-enriched neuronal group.
- `Fcgr4:F002`: whole-parquet signature comparison found no meaningful signed transcriptomic neighbor for `Fcgr4`; the highest absolute Pearson correlations in the report were no larger than 0.031.
- `Fcgr4:F003`: most core Fc-gamma receptor comparators, including `Fcgr1`, `Fcgr2b`, `Fcgr3`, `Fcer1g`, `Syk`, `Lyn`, and `Hck`, were not perturbation targets, so the `Fcgr4` null is not a full test of Fc-receptor redundancy.
- `Fcgr4:F004`: the neuronal null should not be used to dismiss Fc-gamma receptor biology in antibody effector or inflammatory CNS settings; rather, it marks a mismatch between Fcgr effector biology and this healthy NeuN-positive neuronal assay.

The same corpus also contains claim `claim:8bd7e3c8a73422ba8b45`, which states that represented microglial and neuroimmune receptor perturbations do not produce recurrent cell-autonomous neuronal nuclear transcriptional programs in the NeuN-positive screen. Its direct contributions include `Cx3cr1`, `P2ry12`, `Mertk`, `Csf1r`, `Axl`, and `Spi1` reports, all of which place microglial or myeloid receptor biology outside the sampled healthy neuronal compartment.

That corpus evidence was used as same-experiment support for the direction of transfer: it argues for a zero or near-zero prediction for another Fc/myeloid receptor in this neuronal group, while explicitly warning that such a prediction is not a claim that Fcgr2b lacks immune or microglial function.

## External Fcgr2b biology

MGI, Alliance of Genome Resources, and UniProtKB annotate mouse `Fcgr2b` as the inhibitory low-affinity receptor for the Fc portion of IgG, also known as CD32B or Fc-gamma RIIB. Its cytoplasmic immunoreceptor tyrosine-based inhibitory motif counterbalances activating Fc receptors in antibody-bound immune contexts.

The literature places this receptor primarily in immune effector biology:

- Espeli, Smith and Clatworthy 2016 reviewed Fc-gamma RIIB as an inhibitory receptor controlling B-cell, myeloid, dendritic-cell and innate inflammatory signaling, including autoantibody and immune-complex responses. DOI: `10.1111/imr.12368`; PMID: `26683154`.
- Barlev et al. 2022 showed that B-cell-intrinsic Fc-gamma RIIB limits marginal-zone B-cell activation and IgG3 autoantibody production, reinforcing that a major Fcgr2b loss-of-function consequence is humoral/immune rather than neuronal. DOI: `10.1172/JCI157250`; PMID: `35819855`.
- Seeling et al. 2023 found Fc-gamma RIIB-dependent IgG signaling in monocyte / osteoclast inflammatory remodeling, again in Fc/immune-effector cells. DOI: `10.1016/j.immuni.2023.02.019`; PMID: `36948194`.
- Matuszewska et al. 2022 detected `Fcgr2b` among phagocytosis-related transcripts in BV2 microglia and showed that BET inhibition suppresses a broader microglial phagocytosis gene panel. DOI: `10.3390/ijms24010013`; PMID: `36613460`.

These references support `Fcgr2b` as a real receptor with microglial/myeloid/B-cell functions, but they do not provide a reason to expect an acute, cell-autonomous FDR 0.05 RNA signature in postmitotic thalamic glutamatergic neurons.

## Target-specific prediction

### Fcgr2b

The decisive within-dataset analog is `Fcgr4`, the only Fc-gamma receptor family member perturbed in the training set. It has:

- observed focal `n_degs = 0`;
- all 17,259 focal measured-gene rows at `pvals_adj >= 1.0` in the raw parquet;
- no meaningful whole-parquet signature neighbor in its curated same-experiment report; and
- a corpus caveat that the proper Fcgr1/Fcgr2b/Fcgr3/Fcer1g/Syk/Lyn module was mostly absent as direct perturbations.

The best same-assay contextual analogs and counterexamples are also flat: `Axl`, `Mertk`, `Csf1r`, `Cx3cr1`, `P2ry12`, `Spi1`, `Tlr2`, `Tlr4`, and `Tlr7` all have focal `n_degs = 0`. Corpus claim `claim:8bd7e3c8a73422ba8b45` ties those individual nulls into a repeated pattern: microglial, phagocytic and neuroimmune receptors were lineage-displaced in this NeuN-positive postnatal screen rather than forming weak detectable neuronal expression modules.

External biology points in the same direction. `Fcgr2b` is an inhibitory IgG Fc receptor operating through immune-complex and Fc-effector pathways in B cells and myeloid cells. The focal cells are healthy, postmitotic thalamic glutamatergic neurons isolated by NeuN enrichment; B cells, macrophages, microglia and antibody immune-complex challenge are not the assayed context. I therefore expect no gene to pass focal-cell BH FDR 0.05 after `Fcgr2b` perturbation.

Point prediction: `0`.

## Limits of the reasoning

- The direct held-out `Fcgr2b` signature and endpoint are absent by design, so the prediction is an extrapolation from neighbors.
- `Fcgr4` is an activating mouse Fc-gamma receptor, whereas `Fcgr2b` is inhibitory and signals through different cytoplasmic logic; the Fc-family analogy is close by ligand class but imperfect by signaling direction.
- Most canonical Fcgr2b pathway members were not perturbed in the training universe, so direct redundancy through `Fcgr1`, `Fcgr3`, `Fcer1g`, `Lyn`, or `Syk` could not be tested.
- The assay does not measure DNA editing, immune-complex exposure, glial responses, or B/myeloid phenotypes. A zero prediction here means no expected FDR-significant neuronal nuclear RNA signature in recovered `151 TH Prkcd Grin2c Glut` nuclei, not an absence of Fcgr2b function in microglia, macrophages, B cells, autoimmunity, or inflamed brain.
- Because 72% of the training targets have zero focal DEGs, the squared-log endpoint is calibrated to a sparse screen; distinguishing a true zero from one or two weak DEGs is intrinsically uncertain.
