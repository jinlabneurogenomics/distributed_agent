# Foxg1 held-out DEG-count prediction

## Question and resolved ambiguities

The requested endpoint is a point prediction for the number of focal-cell differentially expressed genes after acute sparse CRISPR loss of `Foxg1`, with significance defined exactly as `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut`.

I treated this as a scalar assay-yield prediction rather than as a ranking. `Foxg1` is absent from both supplied input tables as a perturbation, so there is no direct measured `Foxg1` differential-expression profile available. I did not interpret weak target-gene self-repression as failed editing, and I did not transfer embryonic or germline Foxg1 phenotypes directly unless the same causal step should still operate in P16-to-P37/44 postmitotic thalamic neurons.

## Sources used

- Declared training endpoint CSV: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression Parquet: `training_de_all_cell_groups.parquet`.
- Run-local requested-target manifest: `b0142.csv`, containing only `Foxg1`.
- Dataset portrait `perturbai-atlas-v5` and task bindings in `codex_runtime/pipeline`.
- Internal same-experiment corpus `perturbai-july-260713-sourceguard-1773-v1`; I used bounded Finding inventories for comparator perturbations only as prepackaged interpretation of the same Perturb-seq experiment.
- External mechanism/expression priors:
  - Allen Mouse Brain Atlas, genome-wide adult mouse in situ expression resource; Lein et al. 2006, DOI 10.1038/nature05453, PMID 17151600.
  - Foxg1-Cre expression mapping; Hebert and McConnell 2000, DOI 10.1006/dbio.2000.9732, PMID 10837119.
  - FOXG1 dose and forebrain developmental review; Hettige and Ernst 2019, DOI 10.3389/fped.2019.00482, PMID 31824897.
  - FoxG1/Smad/FoxO interaction in telencephalic neuroepithelium; Seoane et al. 2004, DOI 10.1016/s0092-8674(04)00298-3, PMID 15084259.
  - Foxg1 and COUP-TFI/Nr2f1 in embryonic cortical projection-neuron specification; Hou et al. 2019, DOI 10.1038/s41467-019-11043-w, PMID 31395862.

## Dataset calculations

The requested-target CSV had one exact target, `Foxg1`. The focal training table contained 1,674 unique non-held-out perturbations; 1,205 had `n_degs = 0`, the median was 0, the 75th percentile was 1, and only 78 training targets exceeded 20 DEGs. Thus the calibrated prior for a held-out transcription factor in this focal thalamic class is no FDR hit unless there is a strong local analog with the right postnatal mechanism.

I first looked up focal `n_degs` for developmental transcriptional regulators, forkhead relatives, TGF-beta/SMAD pathway members, and broader chromatin/Wnt counterexamples in the supplied count table. I then queried the differential-expression Parquet with the exact focal `group_name` and that restricted `gene_target` set to recover the significant measured genes rather than only the count. The relevant focal rows were:

| training perturbation | focal `n_degs` | focal significant genes from the Parquet | interpretation for `Foxg1` |
| --- | ---: | --- | --- |
| `Foxp2` | 0 | none | Forkhead/neurodevelopmental TF; the internal corpus reports no FDR<0.10 downstream response in any measured neuronal group and no CNTNAP2/early FOXP axis in this juvenile assay. This is a negative analog, not a paralogous obligate effector. |
| `Foxa2`, `Foxk2` | 0, 0 | none | Forkhead family counterexamples; superficial family membership does not predict a broad thalamic footprint. |
| `Tbr1` | 0 | none | Telencephalic/cortical projection-neuron TF with known developmental links to FOXG1-region biology; in the focal thalamic class it produced no FDR<0.05 gene. |
| `Satb2` | 0 | none | Cortical projection-neuron identity factor; the same-experiment corpus reports a flat postnatal response and absence of the canonical Satb2 switch. |
| `Bcl11a`, `Bcl11b` | 0, 0 | none | Developmental cortical TFs; both were focal nulls, and the same-experiment corpus groups Bcl11a, Bcl11b, and Satb2 as buffered in this P16 acute assay. |
| `Pax6` | 0 | none | Embryonic neural patterning TF; the corpus reports complete transcriptional silence across recovered neuronal groups, again arguing that developmental TF importance is mostly off-window here. |
| `Sox11` | 0 | none | Immature-neuron SOXC factor; no focal response and no robust response across neuronal groups in the corpus. |
| `Tcf4` | 0 | none | Neurodevelopmental bHLH factor; the corpus reports only a small Pvalb response and no focal thalamic response. |
| `Meis2` | 0 | none | Forebrain/LGE patterning TF; no focal response and no postnatal MSN-like module. |
| `Nr2f1` | 2 | `Sorl1` up, `Sema7a` down | The closest named pathway counterexample because embryonic Foxg1 can repress COUP-TFI/Nr2f1 in cortex. The juvenile perturbation was nearly silent and did not recover the cortical arealization/projection-neuron marker program. |
| `Smad2`, `Smad3`, `Smad4` | 1, 0, 0 | only `Cpne7` down for `Smad2` | These test the TGF-beta/SMAD arm that Foxg1 can antagonize in neuroepithelium. Canonical SMAD signaling itself was absent or one-gene in recovered P16 neurons, so it is not a strong same-endpoint bridge. |
| `Arid1b` | 1 | `Arid1b` down | A broad ASD/chromatin regulator that was unexpectedly buffered in postmitotic neurons; included to avoid assuming every disease TF yields a large thalamic signature. |
| `Chd8` | 61 | 61 genes, led by `Pnisr`, `Tmem50a`, `Chd8`, `Man2c1`, `Usp11` | A moderate nonzero chromatin counterexample; its PNISR/USP11/DUS3L RNA-processing module is not a Foxg1 pathway. |
| `Ctnnb1` | 383 | Wnt/excitability/adhesion module, led by `Plekhg1`, `Gabra4`, `Ramp3`, `Rasgrp1`, `Chrna4`, `L1cam`, `Lef1`, `Axin2`, `Ctnnb1` and many synaptic/adhesion genes | A strong focal thalamic Wnt/adhesion effect. Foxg1 intersects Wnt/TGF-beta developmental patterning in telencephalon, but acute Foxg1 loss is not expected to impair beta-catenin's adhesion or Wnt-feedback functions directly in this thalamic survivor population. |

The exact focal-cell matched counts for the most relevant nulls were adequate for the assay: `Foxp2`, 245 perturbed nuclei; `Tbr1`, 288; `Satb2`, 236; `Bcl11a`, 203; `Bcl11b`, 206; `Pax6`, 138; `Sox11`, 324; `Tcf4`, 250; `Smad4`, 123. Their zeros are therefore not simply absent focal rows.

## Foxg1 rationale

`Foxg1` encodes a dosage-sensitive forkhead transcription factor central to telencephalon and neocortical development, and pathogenic FOXG1 loss causes a severe forebrain neurodevelopmental syndrome. That external biology raises its importance but places much of the known regulatory action in embryonic progenitors and cortical/striatal telencephalic lineages rather than in already specified thalamic glutamatergic neurons. The Foxg1-Cre mapping in Hebert and McConnell 2000 explicitly describes Foxg1 as telencephalic with other discrete head domains; the focal atlas class is a thalamic, diencephalic glutamatergic group. Allen Mouse Brain Atlas expression patterns likewise support Foxg1 as predominantly forebrain/telencephalic rather than a strong adult thalamic gene.

I mapped the causal chain as: AAV CRISPR delivered at P16 perturbs `Foxg1` in sparse recovered neurons -> any direct consequence requires Foxg1 protein to be present and nonredundantly regulating transcription in the edited focal thalamic neurons at P16-P37/44 -> embryonic Foxg1 targets would have to remain coupled to a postmitotic thalamic maintenance program -> the edited neurons must survive and be sampled -> a Wilcoxon FDR response must appear across nuclear RNA. The likely break is early in that chain: low or absent focal Foxg1 activity plus the off-window nature of the canonical telencephalic programs.

The within-dataset analogs reinforce that break. Acute postnatal loss of multiple developmental TFs with strong embryonic or cortical identities (`Pax6`, `Satb2`, `Bcl11a`, `Bcl11b`, `Meis2`, `Sox11`, `Foxp2`) was transcriptionally buffered in this assay and zero in the focal group. Known Foxg1-adjacent mechanisms do not rescue a nonzero call: the COUP-TFI/Nr2f1 axis was only a two-gene focal response, SMAD pathway perturbations were zero or one-gene in the focal class, and the strong `Ctnnb1` response reflects beta-catenin Wnt-feedback, excitability, and adhesion biology that is not an obligate downstream consequence of Foxg1 loss here.

I therefore predict `Foxg1` as an FDR-level non-responder in `151 TH Prkcd Grin2c Glut` and assign 0 DEGs rather than a low positive count. A one- or two-gene response like `Nr2f1`, `Sox2`, `Sox5`, or `Smad2` remains plausible, but the point prediction is zero because the closest postnatal in-dataset analogs were null.

## Limits

This is an extrapolation because the held-out `Foxg1` perturbation has no expression signature in the supplied dataset. The Parquet used here contains differential statistics, not unperturbed per-cell expression, so the low-focal-Foxg1 premise comes from external expression atlases and Foxg1-Cre literature rather than direct baseline measurement in the training file. The internal corpus summaries are curated interpretations of the same Perturb-seq experiment and are not independent replication. Finally, severe selection before the snRNA-seq readout could hide a direct Foxg1 effect in unsampled cells, although none of the close focal analogs suggests a broad survivor-state signature.
