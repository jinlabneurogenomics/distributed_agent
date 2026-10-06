# DEG-count holdout prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

The requested task is to predict the held-out `n_degs` for each missing perturbation in the focal `151 TH Prkcd Grin2c Glut` thalamic glutamatergic class. I interpreted `n_degs` exactly as the count of measured genes with `pvals_adj < 0.05` in the supplied Wilcoxon differential-expression contrasts for recovered nuclei in this cell class.

The endpoint is directly observed for the non-held-out training perturbations in `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`; it is absent by design for `Pcdh15`. The held-out `Pcdh15` signature itself is absent, so the prediction is a transfer from (1) focal-cell DEG counts and DE signatures of related training perturbations and (2) outside knowledge of PCDH15 biology.

## Sources used

- Declared DEG-count training table: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, 1,674 non-held-out perturbations with focal `n_degs`.
- Declared differential-expression Parquet: `training_de_all_cell_groups.parquet`, queried only for exact focal rows of biologically related training perturbations and for the behavior of the measured `Pcdh15` transcript under other perturbations.
- Run-local dataset metadata: `codex_runtime/pipeline/dataset_context.md`, `task_bindings.json`, `coverage.json`, `capabilities.json`, and `measurement_registry.json`.
- Selected internal corpus: `perturbai-july-260713-sourceguard-1773-v1`. I used `corpus.calibration` for release semantics and `corpus.report_evidence` for the packaged `Pcdh19` report, which is a same-experiment interpretation of the Parquet, not independent replication. The graph contained no `Pcdh15` `Gene` or `TargetGene` node in this release.
- External literature retrieved from PubMed / NCBI E-utilities on 2026-09-03:
  - Washington et al. 2005, DOI `10.1016/j.heares.2004.09.014`, showed that an ENU Ames-waltzer `Pcdh15` allele causes hair-cell dysfunction and abnormal stereocilia development.
  - Geng et al. 2013, DOI `10.1523/JNEUROSCI.4514-12.2013`, mapped a `Pcdh15` missense mutation disrupting the CDH23-PCDH15 EC1/EC2 "handshake" and tip-link function.
  - Pepermans and Petit 2015, DOI `10.1016/j.heares.2015.05.005`, reviewed PCDH15 isoforms in the organ of Corti and their role with CDH23 in the hair-cell tip link.
  - Dionne et al. 2018, DOI `10.1016/j.neuron.2018.07.006`, showed that PCDH15 cis-dimerization is important for hair-cell mechanotransduction.
  - Reiners et al. 2005, PMID `15928608`, reported Pcdh15 interaction with harmonin and localization of Usher-protein complexes in mammalian photoreceptors.
  - Ye et al. 2014, DOI `10.1111/gbb.12119`, implicated `Pcdh15` in a mouse midbrain serotonin-transporter genetic network and found serotonergic effects in a functional-null line.

## Quantitative extraction

The training count table showed a sparse focal response overall: median `n_degs = 0`, 75th percentile `= 1`, and 95th percentile `= 18`, with broad outliers restricted to genes such as `Uba5`, `Tpr`, `Sin3a`, spliceosome, proteasome, and transcriptional regulators.

I then queried the Parquet for focal `151 TH Prkcd Grin2c Glut` rows of `Pcdh15`-relevant adhesion and synaptic-organizer perturbations:

```python
import pyarrow.compute as pc
import pyarrow.dataset as ds

dataset = ds.dataset(
    "supplied training inputs"
    "training_de_all_cell_groups.parquet",
    format="parquet",
)
f = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(targets)
)
table = dataset.to_table(
    columns=[
        "names", "scores", "logfoldchanges", "pvals_adj",
        "gene_target", "n_pert_matched", "n_ctrl_matched",
    ],
    filter=f,
)
```

The closest perturbations in the training set were all null or one-gene signatures:

| Training perturbation | Focal `n_degs` | Focal expression evidence | Relevance to `Pcdh15` |
|---|---:|---|---|
| `Pcdh19` | 0 | 0 genes at FDR < 0.05; minimum adjusted p-value 1.0 with 137 matched perturbed nuclei. The packaged report also called `Pcdh19` null across measured neuronal groups at FDR < 0.10. | Only `Pcdh*` perturbation present in the training table and a non-clustered protocadherin. It is a developmental/adhesion paralog-level analog, although it has epilepsy- and GABA-receptor biology not shared by PCDH15. |
| `Adgrv1` | 0 | 0 genes at FDR < 0.05; minimum adjusted p-value 1.0 with 225 matched perturbed nuclei. | Usher/hair-bundle surface protein, but part of ankle-link rather than CDH23-PCDH15 tip-link machinery. A weak positive analog and a useful counterexample against broad hair-bundle-gene transfer in this neuronal screen. |
| `Dscam` | 0 | 0 genes at FDR < 0.05; minimum adjusted p-value 0.0897 with 124 matched perturbed nuclei. | Neuronal cell-adhesion molecule with dendrite/axon self-avoidance biology; relevant as a large membrane adhesion counterexample. |
| `Nrxn2`, `Nrxn3` | 0, 0 | 0 genes at FDR < 0.05; minima 0.165 and 0.0908. | Synaptic adhesion/organizer genes; mechanistically not tip-link proteins, but stronger neuronal synaptic comparators than PCDH15 itself in thalamic glutamatergic neurons. |
| `Lrrtm3`, `Lrrtm4` | 0, 0 | 0 genes at FDR < 0.05; minimum adjusted p-values 1.0 and 1.0. | Leucine-rich synaptic adhesion proteins; counterexamples for postsynaptic adhesion perturbations. |
| `Ptprd`, `Ptprt`, `Ptprf`, `Ptpro` | 0, 0, 0, 0 | 0 genes at FDR < 0.05; minimum adjusted p-values 0.143, 1.0, 1.0, and 1.0. | Receptor-type phosphatases with extracellular adhesion-like roles; counterexamples for membrane signaling/adhesion perturbations. |
| `Nrxn1`, `Nlgn3`, `Cntnap1`, `Cntnap2`, `Cadm2`, `Tenm3`, `Ptprm` | 1 each | The only FDR < 0.05 gene was the perturbed transcript itself in each case. | These show that even known synaptic-adhesion genes in this focal group usually generated no resolved downstream program. Because `Pcdh15` is held out, a self-only knockdown would be the main route to predicting exactly one DEG. |
| `Lrrtm1` | 1 | One non-self gene, `R3hdm2`, passed at adjusted p = 0.0269. | A weak counterexample showing an occasional isolated downstream hit, not a broad signature. |

I also checked whether the focal `Pcdh15` transcript was commonly altered by other training perturbations. Across 1,674 training perturbations, `Pcdh15` passed FDR < 0.05 once, after `Atp2a2` perturbation; the next-smallest `Pcdh15` adjusted p-value was 0.132. This argues that `Pcdh15` was measurable but was not a recurrent component of a high-yield focal transcriptional program.

The hair-cell tip-link cofactor set most relevant from the literature was almost completely absent from the training perturbation table: `Cdh23`, `Ush1c`, `Ush1g`, `Myo7a`, `Lhfpl5`, `Tmc1`, `Tmc2`, `Tmie`, `Cib2`, `Cib3`, `Whirn`, and `Ush2a` were not training targets. `Adgrv1`, a much looser Usher/ankle-link comparator, was present and had `n_degs = 0`.

## Target-specific reasoning

### `Pcdh15`

The causal chain for the requested experiment is acute partial CRISPR loss of `Pcdh15` in sparse postnatal neurons -> reduced/disrupted PCDH15 protein in cells that express the screened isoforms -> loss of PCDH15 extracellular adhesion complexes -> changes in local sensory/synaptic architecture if the interacting machinery is present -> survival and recovery of the edited thalamic glutamatergic nuclei -> Wilcoxon DEG burden among recovered nuclei.

PCDH15 has an obligate, endpoint-bearing role in inner-ear hair cells: PCDH15 and CDH23 form the lower and upper portions of stereociliary tip links, PCDH15 structural interfaces tune mechanotransduction, and `Pcdh15` mutant animals have early hair-bundle disorganization, deafness, and vestibular phenotypes. That direct molecular consequence does not transfer cleanly to the assayed endpoint. The Perturb-seq experiment captured NeuN-enriched forebrain/midbrain/hypothalamic neurons, not inner-ear hair cells or photoreceptors, and the necessary CDH23-PCDH15 hair-bundle apparatus was not represented among strong focal analogs.

The within-dataset analog that most closely matches the gene family, `Pcdh19`, was completely null in the focal class despite 137 matched perturbed nuclei; its same-experiment report was also null across neuronal groups at the looser FDR < 0.10 threshold. `Pcdh19` is not a perfect PCDH15 surrogate because PCDH19 participates in cortical developmental cell-adhesion and GABAergic mechanisms rather than the CDH23 tip link, but it is still the only assayed non-clustered protocadherin perturbation and it shows that protocadherin loss did not automatically create broad survivor-state transcription in this CRISPR assay.

The stronger neuronal adhesion comparators likewise support a zero prediction. Large extracellular synaptic organizers and contact molecules, including `Dscam`, `Nrxn2`, `Nrxn3`, `Lrrtm3`, `Lrrtm4`, `Ptprd`, `Ptprt`, `Ptprf`, and `Ptpro`, all had `n_degs = 0` in the same focal cell group. Several others had `n_degs = 1`, but for `Nrxn1`, `Nlgn3`, `Cntnap1`, `Cntnap2`, `Cadm2`, `Tenm3`, and `Ptprm` that one gene was only the targeted transcript. Because target-transcript log-fold change is not an editing-efficiency readout in this dataset, I did not require visible self-knockdown for `Pcdh15`; the point is narrower: even bona fide neuronal synaptic adhesion genes rarely propagated to downstream FDR-significant changes in the recovered `151 TH Prkcd Grin2c Glut` nuclei.

External `Pcdh15` brain evidence did not justify overriding the training analogs upward. Ye et al. linked `Pcdh15` to serotonin-transporter expression in midbrain 5-HT traits, but that was germline/background genetics and serotonergic biology rather than acute partial loss in thalamic glutamatergic neurons. Reiners et al. placed PCDH15 in photoreceptor Usher complexes, again outside the NeuN-enriched neuronal tissue sampled here. I therefore treated the expected direction as indeterminate for the thalamic transcriptional endpoint, with no candidate-specific reason to expect a broad nonzero DEG burden.

**Prediction:** `Pcdh15 = 0` DEGs. A self-only count of 1 is the main alternative if the `Pcdh15` transcript itself is sensitive to the gRNAs in this cell group, but the direct `Pcdh19` null and the many zero adhesion/synaptic-organizer perturbations make zero the better point estimate.

## Limits of the prediction

This is an extrapolation from imperfect within-dataset analogs. `Pcdh19` is the closest assayed protocadherin but is not a CDH23/USH1 tip-link partner; `Adgrv1` is an Usher-related hair-bundle protein but is in a different complex; and most of the other comparators are generic neuronal adhesion or synaptic-organization genes rather than PCDH15 pathway members. The true CDH23-PCDH15 mechanotransduction partners were absent from the training-count table, and no raw per-nucleus expression or guide-level outcome was available to estimate `Pcdh15` editing in the held-out perturbation. Finally, the endpoint is a BH-thresholded DEG count from recovered nuclei, so a prediction of zero means no expected FDR-significant transcriptional footprint under this assay and power, not absence of PCDH15 biology.
