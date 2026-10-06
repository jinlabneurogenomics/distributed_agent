# DEG-count holdout prediction

## Question and resolved ambiguities

The requested held-out perturbation set for this run contains one mouse target,
`Epha6`. I interpreted the endpoint as the exact training CSV endpoint:

```
n_degs = count of measured genes with pvals_adj < 0.05
```

in `151 TH Prkcd Grin2c Glut` nuclei after sparse P16 AAV CRISPR loss of
function, including a target's own transcript if it passes the same FDR
threshold. The requested `Epha6` perturbation was completely held out from the
DE Parquet and the focal-cell training-count CSV, so I did not have an
`Epha6` loss-of-function signature. I treated the Parquet/training counts as
the primary endpoint evidence and used external biology only to decide which
visible training perturbations were mechanistically comparable.

## Sources used

- Declared input counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression table:
  `training differential-expression dataset`.
- Declared held-out manifest:
  `single-target request for Epha6`.
- Run-local task bindings, coverage, capability manifest, and PerturbAI atlas
  dataset portrait in `codex_runtime/pipeline`.
- Internal same-experiment semantic corpus
  `perturbai-july-260713-sourceguard-1773-v1`, queried through
  `corpus.calibration`, `corpus.findings`, `corpus.report_evidence`, and the
  July BioKG graph only as semantic navigation over comparator mentions.
- External literature:
  Kullander and Klein 2002, Nat Rev Mol Cell Biol, PMID:12094214; Pasquale
  2005, Nat Rev Mol Cell Biol, PMID:15928710; Bevins et al. 2011, J Neurosci,
  doi:10.1523/JNEUROSCI.1652-11.2011; Das et al. 2016, Cell Biosci,
  doi:10.1186/s13578-016-0115-5; Sudarsanam et al. 2025, J Neurosci,
  doi:10.1523/JNEUROSCI.0201-25.2025.

## Quantitative calibration from the focal training endpoint

The one requested gene was not a ranking task, so the ranking-only feature
workbench and predictive graph review were not policy-available. I queried the
training count CSV and the declared Parquet directly.

In the focal count CSV there were 1,674 visible biological training targets.
The distribution was sparse:

- 1,205/1,674 targets had `n_degs = 0`.
- The median was 0.
- The 75th, 90th, 95th, and 99th percentiles were 1, 2, 18, and 430 DEGs.
- Large nuclear responses were detectable in this same cell group, for
  example `Uba5` 2,677, `Tpr` 1,768, `Sin3a` 1,433, `Rnpc3` 868, and
  `Zbtb7a` 841.

I then checked the Eph-family and proximal pathway perturbations represented in
the same focal endpoint:

| training target | focal `n_degs` | non-self focal DEGs |
| --- | ---: | ---: |
| `Epha10` | 0 | 0 |
| `Epha2` | 0 | 0 |
| `Epha3` | 0 | 0 |
| `Epha4` | 1 | 0 |
| `Epha5` | 0 | 0 |
| `Ephb1` | 0 | 0 |
| `Ephb2` | 0 | 0 |
| `Ephb4` | 0 | 0 |
| `Adam10` | 0 | 0 |
| `Chn1` | 0 | 0 |
| `Fyn` | 0 | 0 |
| `Kalrn` | 0 | 0 |
| `Pak1` | 1 | 0 |
| `Pak2` | 0 | 0 |
| `Psen1` | 0 | 0 |
| `Ptpn11` | 0 | 0 |
| `Rac1` | 0 | 0 |

The focal `Epha4` singleton was `Epha4` itself
(`logfoldchanges = -1.027`, `pvals_adj = 7.88e-32` in 184 perturbed nuclei vs
23,679 controls), not a downstream EphA transcriptional program. `Pak1` and
`Cdc42` behaved similarly: their lone focal DEGs were their self-transcripts.
The strongest Eph/NMDAR counterexamples were `Grin1`, with 89 focal DEGs
including 88 non-self genes, and `Grin2b`, with 2 focal DEGs including one
non-self gene; `Ephb1`, `Ephb2`, `Ephb4`, and `Fyn` did not transfer that
NMDAR-proximal biology into a broad nuclear response.

The Parquet query for this distinction was:

```sql
SELECT gene_target,
       SUM(pvals_adj < 0.05) AS deg05,
       SUM(CASE WHEN names <> gene_target
                THEN CAST(pvals_adj < 0.05 AS INTEGER)
                ELSE 0 END) AS downstream_deg05,
       MIN(CASE WHEN names <> gene_target THEN pvals_adj ELSE NULL END)
         AS min_downstream_fdr
FROM read_parquet($training_parquet)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN ($eph_and_pathway_targets)
GROUP BY gene_target;
```

As QC context only, the focal measured-gene universe did contain an `Epha6`
row for all 1,674 visible training perturbations, and two unrelated broad
perturbations changed `Epha6` at FDR 0.05 (`Uba5`, q=0.0044; `Smarcc2`,
q=0.0141). That confirms `Epha6` was not absent from the measured gene table,
but it does not predict whether the hidden `Epha6` perturbation would have a
self-transcript DEG.

## Same-experiment interpretation of visible analogs

The July same-experiment corpus contained reports for the visible Eph receptors
`Epha2`, `Epha3`, `Epha4`, `Epha5`, `Epha10`, `Ephb1`, `Ephb2`, and `Ephb4`.
I used the BioKG comparator graph only to find which Eph/ephrin records to read;
graph topology and comparator multiplicity did not order the prediction.

Those reports were consistent with the raw focal counts:

- `Epha2` was pan-neuronally buffered: all 23 measured neuronal groups had zero
  downstream genes at FDR < 0.10. Its same-experiment report contrasted
  related Eph receptors plus `Adam10`, `Fyn`, `Ptpn11`, `Rac1`, `Sos1`,
  `Mapk1`, `Mapk9`, and PI3K subunits and found no hidden EphA2-like nuclear
  module.
- `Epha3` had zero non-self downstream genes at FDR < 0.10 in all 22 recovered
  groups. The report tested Eph-family receptors and the ADAM10/PSEN1,
  Src-family, CHN1, Rac, MAPK, and PAK neighborhood and again found
  non-convergence at the transcriptome level.
- `Epha4` showed significant self-transcript depletion in five neuronal groups,
  including `151 TH Prkcd Grin2c Glut`, but no downstream genes in those five
  groups. Its only non-self FDR < 0.10 event was `Tmsb10` up in `053 Sst Gaba`.
- `Epha5`, the closest visible biological analog for `Epha6`, had a single
  FDR < 0.10 downstream hit across the whole measured surface: `Lnpep` down in
  `012 MEA LA CA1 DG Glut`. It had zero DEGs in the focal thalamic group.
  Represented Eph-family perturbations did not phenocopy this one-gene
  `Epha5` event.
- `Epha10`, `Ephb1`, `Ephb2`, and `Ephb4` likewise had at most an isolated
  off-focal hit or were fully flat. EphB/NMDAR records explicitly showed that
  direct `Grin1`, `Grin2a`, and `Grin2b` perturbations were detectable, whereas
  EphB receptor and `Fyn` perturbations were not NMDAR-like in the snRNA-seq
  endpoint.

## Biological transfer to `Epha6`

`Epha6` encodes an EphA receptor and is mechanistically closer to `Epha5` and
other EphA-family receptors than to the broad splicing, proteasome, and
chromatin perturbations that dominate the high-count tail of the focal
training endpoint. Eph/ephrin signaling is membrane-contact-dependent,
frequently bidirectional, and is well known for local growth-cone, axon
guidance, target-map, spine, and synapse effects rather than for requiring a
large persistent stress-like nuclear RNA program in every postmitotic neuron
(Kullander and Klein 2002; Pasquale 2005).

`Epha5` is the most informative within-dataset analog because Das et al. 2016
studied EphA5 and EphA6 together and reported abnormal Golgi staining and spine
morphology after their deletion. That is a same-direction prior for local
neuronal structural consequences of EphA6 loss, but it is weak endpoint
evidence for `n_degs`: the endpoint here is survivor-conditioned nuclear RNA
at P37-P44 after sparse P16 AAV editing. The `Epha5` training perturbation
produced zero focal DEGs and only one off-focal downstream gene across all
groups, arguing that EphA5/EphA6-like structural signaling is usually
transcriptionally buffered in this assay.

EphA6 also participates in retinal EphA gradients with EphA4/EphA5-like
relative signaling logic (Bevins et al. 2011), and recent cortical work places
EphA6 downstream of postnatal MEF2C in callosal axon targeting through
Ephrin-A5 repulsion (Sudarsanam et al. 2025). Both links point to spatially
restricted axon-targeting or repulsion roles. They do not supply a reason that
EphA6 should differ from visible `Epha4` and `Epha5` by inducing many FDR 0.05
genes in thalamic `Prkcd`/`Grin2c` glutamatergic nuclei.

The causal transfer model is therefore:

`Epha6` CRISPR loss -> reduced EphA6 receptor function -> weaker
ephrin-A/contact-dependent local cytoskeletal and targeting signals -> possible
spine or wiring changes in receptive neurons -> recovered P37-P44 thalamic
nuclei assayed by Wilcoxon DE.

The direct molecular and local cytoskeletal stages transfer from the EphA5/A4
literature in the same loss-of-function direction. The link to the requested
endpoint breaks at propagation from local membrane/cytoskeletal signaling to a
large steady-state nuclear RNA state: every visible single Eph receptor in the
focal training endpoint sat at zero downstream DEGs, and the only visible
EphA-family focal count was an `Epha4` self-transcript. Because target
self-depletion is an unreliable editing-strength measure in this platform and
because comparable `Epha5` did not score its own transcript in the focal group,
I did not add a self-transcript DEG for hidden `Epha6`.

## Prediction

I predict `Epha6` will have no measured genes below BH-adjusted Wilcoxon
FDR 0.05 in `151 TH Prkcd Grin2c Glut`:

| target | predicted `n_degs` | rationale |
| --- | ---: | --- |
| `Epha6` | 0 | The focal within-dataset EphA/EphB receptor neighborhood is all zero or self-only; the closest visible analog `Epha5` is zero in the focal group; external EphA6 biology supports local axon/spine or retinotopic/callosal targeting functions rather than a broad P37 thalamic nuclear RNA program. |

## Limits

This is an extrapolation because `Epha6` itself was held out, ephrin-A ligands
were not available as visible perturbation anchors, and the Parquet does not
contain DNA indel rates, protein loss, synaptic morphology, electrophysiology,
or axon-targeting phenotypes. A true `Epha6` self-transcript hit would move the
endpoint from 0 to 1 even if all downstream genes remained null; the visible
training data are not enough to predict that with confidence. The prediction
also assumes that thalamic `151 TH Prkcd Grin2c Glut` neurons behave more like
the visible postmitotic EphA receptor perturbations than like the developing
retina or cortical callosal systems where EphA6 has a clearer wiring role.
