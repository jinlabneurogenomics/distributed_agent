# Dock7 DEG-count prediction

## Question and endpoint

The requested target is `Dock7`, a held-out perturbation. I interpreted the
endpoint as the exact focal-cell readout used in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: the number of measured
genes with `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` after acute,
postnatal, sparse CRISPR loss of the target, counting any significant
self-transcript together with downstream genes. The held-out `Dock7` contrast is
absent by construction, so the prediction must transfer from visible training
perturbations and external Dock7 biology rather than reading a Dock7 row.

I treated the readout as directly observed for each non-held-out training
perturbation in the focal training CSV. Expression signatures in
`training_de_all_cell_groups.parquet` were direct same-experiment expression
evidence for those visible perturbations. The packaged July 260713
sourceguard-1773 same-experiment corpus was used only as an interpreted
same-experiment layer over those visible perturbations, not as independent
replication. External support came from PubMed-indexed primary literature and
reviews:

- Watabe-Uchida et al. 2006, DOI 10.1016/j.neuron.2006.07.020, PMID 16982419:
  DOCK7 activates Rac, polarizes nascent axons, and controls local
  stathmin/Op18 phosphorylation in developing hippocampal neurons.
- Tai et al. 2014, DOI 10.1016/j.celrep.2013.12.034, PMID 24440718: DOCK7 is
  required for chandelier-cell cartridge and bouton morphogenesis through
  ErbB4 activation in developing cortical interneurons.
- Perrault et al. 2014, DOI 10.1016/j.ajhg.2014.04.012, PMID 24814191:
  biallelic human DOCK7 truncating variants cause early-onset epileptic
  encephalopathy with cortical blindness and intellectual disability.
- Blasius et al. 2009, DOI 10.1073/pnas.0813208106, PMID 19202056: recessive
  mouse Dock7 truncations produced hypopigmentation on C57BL/6J backgrounds
  without an overt neurobehavioral requirement in vivo.
- Gadea and Blangy 2014, DOI 10.1016/j.ejcb.2014.06.003, PMID 25022758:
  DOCK-family exchange factors couple Rac/Cdc42-family GTPases to actin,
  adhesion, and migration biology.

## In-dataset calculations

From the focal training-count CSV I first inspected the scalar target
distribution. It contained 1,674 unique training targets; 1,205 had
`n_degs == 0`, the median was 0, the 75th percentile was 1, the 95th percentile
was 18, and the maximum was 2,677. Thus a held-out gene needed specific evidence
for an assay-visible broad state before it should be placed above the zero/one
baseline.

I then queried the training counts for biologically adjacent visible genes:
Dock-family, Rac/Cdc42, PAK, WAVE-regulatory-complex, GEF/GAP, stathmin,
ErbB4/Pcdh19, and Rab3gap1/Myo6 neighborhood targets. The focal counts were:

| comparator | focal `n_degs` | relationship to Dock7 |
|---|---:|---|
| `Dock3` | 0 | closest visible DOCK-family Rac GEF and axon/neurite cytoskeletal comparator |
| `Rac1` | 0 | immediate GTPase output for DOCK7 and other DOCK-family GEFs |
| `Cdc42` | 1 | adjacent Rho-family GTPase; the lone focal DEG was `Cdc42` self-RNA |
| `Pak1` | 1 | group-I Rac/Cdc42 effector kinase; the lone focal DEG was `Pak1` self-RNA |
| `Pak2` | 0 | group-I Rac/Cdc42 effector kinase |
| `Pak3` | 0 | neuronal group-I Rac/Cdc42 effector kinase |
| `Cyfip1` | 0 | WAVE-regulatory-complex subunit downstream of Rac signaling |
| `Cyfip2` | 1 | WAVE-regulatory-complex subunit; the lone focal DEG was `Cyfip2` self-RNA |
| `Kalrn` | 0 | neuronal Rac/Rho GEF |
| `Fgd4` | 0 | Cdc42 GEF |
| `Arhgap18` | 0 | Rho-family GAP |
| `Arhgap32` | 0 | Rho-family GAP |
| `Arhgef9` | 1 | neuronal Cdc42/Rho exchange-factor neighborhood; one self-RNA event |
| `Limk1` | 0 | PAK/cofilin cytoskeletal effector |
| `Cfl2` | 0 | cofilin-family actin effector |
| `Tiam1` | 0 | Rac GEF |
| `Myo6` | 0 | reported DOCK7 interactor in neurite outgrowth assays |
| `Erbb4` | 0 | DOCK7-linked receptor in chandelier-cell cartridge development |
| `Pcdh19` | 0 | reported proximity interactor of DOCK7 in the neuronal Pcdh19 network |
| `Rab3gap1` | 0 | ER/Golgi neurite-outgrowth factor reported to interact with DOCK7 |
| `Stmn2` | 1 | microtubule-dynamics/stathmin-family comparator; one self-RNA event |

I read the corresponding rows from the large Parquet after filtering to
`group_name == "151 TH Prkcd Grin2c Glut"` and these targets. Each visible
comparator had 17,259 measured genes and 69-282 matched perturbed nuclei in the
focal cell group. The Parquet confirmed that the sparse counts above were not
hiding a shared Dock/Rac expression pattern: `Dock3`, `Rac1`, `Pak2`, `Pak3`,
`Cyfip1`, `Kalrn`, `Limk1`, `Pcdh19`, `Rab3gap1`, and `Erbb4` had no
FDR-significant focal genes; `Cdc42`, `Pak1`, and `Cyfip2` crossed only on their
own transcripts. The Wilcoxon-score vector for `Dock3` in the focal group was
effectively uncorrelated with the plausible analogs: Pearson `r` was 0.037 to
`Cdc42`, -0.029 to `Rac1`, 0.049 to `Pak1`, -0.030 to `Pak2`, 0.035 to `Pak3`,
0.062 to `Cyfip1`, 0.024 to `Cyfip2`, and 0.009 to `Limk1`.

As a positive control for assay visibility, I checked visible RAF/MEK/MAPK
targets in the same focal cell group. `Braf` and `Map2k1` each had 4 focal DEGs
and shared the down-regulated `Vgf`/`Ptpn5`/`Unc13a` pattern, while `Gsk3b` had
6 and `Mtor` had 2. This shows that a small thalamic signaling response could be
seen by the assay, but Dock/Rac/PAK/WAVE perturbations did not project through
that nuclear module.

## Same-experiment corpus evidence

The internal same-experiment corpus had compact reports for `Dock3`, `Rac1`,
`Cdc42`, `Pak1`, and `Pak2`. Those reports agreed with the focal Parquet:

- `Dock3` produced no robust downstream snRNA-seq response in any recovered
  neuronal cell group; its represented Rac/WAVE/GSK3b comparators did not
  converge with it.
- `Rac1` was transcriptionally buffered in 21 of 22 measured cell groups; its
  only robust RNA event was a single Sst-restricted `Ranbp1` up-regulation, and
  represented Cdc42/PAK/WRC/GEF/GAP relatives did not phenocopy it.
- `Cdc42` had no robust downstream transcriptional response and no shared
  FDR-supported overlap with represented Rac1/PAK/LIMK/CYFIP/Kalrn/Dock3/Fgd4
  relatives.
- `Pak1` and `Pak2` were sparse or null, and the reports specifically cautioned
  that canonical PAK actin, cofilin, and MAPK biology is not well read out by
  this postnatal snRNA-seq endpoint.

These corpus summaries were not used as a graph score or independent
replication; they were used to cross-check that the raw focal rows were part of
a broader same-assay uncoupling of the Rac/Cdc42/PAK cytoskeletal branch from
steady-state nuclear RNA.

## Target-specific causal transfer for `Dock7`

`Dock7` sits upstream of local Rac activation, actin remodeling, and
microtubule regulation. The strongest direct external evidence is developmental
or morphological: DOCK7 knockdown blocks axon formation in cultured developing
hippocampal neurons by altering local stathmin phosphorylation
(Watabe-Uchida et al. 2006), DOCK7 modulates ErbB4-dependent chandelier-cell
cartridge formation during cortical interneuron development (Tai et al. 2014),
and human biallelic truncations are a cause of a congenital developmental and
epileptic encephalopathy syndrome (Perrault et al. 2014; Haberlandt et al. 2021,
DOI 10.1002/mgg3.1607, PMID 33471954).

The causal chain for the requested experiment is narrower:

`Dock7` sparse CRISPR loss after P16 -> reduced DOCK7 Rac-GEF/scaffolding
activity in already postmitotic thalamic glutamatergic neurons -> local Rac,
ErbB4, stathmin, actin, or microtubule consequences -> possible morphology or
synaptic effects among recovered nuclei after 3-4 weeks -> Wilcoxon
steady-state nuclear RNA in `151 TH Prkcd Grin2c Glut`.

The weak link is the transfer from local cytoskeletal/morphological biology to
the measured nuclear DEG-count endpoint. The direct visible Rac/Cdc42/PAK/WAVE
perturbations were essentially flat in exactly the focal cell group, and the
closest visible DOCK-family perturbation, `Dock3`, was a zero-DEG target with no
meaningful focal score-vector neighbor. `Erbb4`, `Pcdh19`, `Myo6`, and
`Rab3gap1`, although connected to reported Dock7 protein neighborhoods in other
systems, were also zero-DEG in the focal endpoint. Therefore the best
assay-matched prior for Dock7 is not the long-tailed high-response perturbation
class, but a null or self-only small-GTPase/cytoskeletal class.

I considered whether Dock7 should be predicted as one DEG rather than zero
because some null cytoskeletal perturbations have a significant self-transcript
and the requested count includes self-RNA. I did not add that single gene: Rac1,
Dock3, Pak2, Pak3, Kalrn, Limk1, Pcdh19, Rab3gap1, Myo6, and Erbb4 were zero in
the same endpoint, and the dataset portrait warns that measured target-RNA loss
is variable and should not be treated as target engagement. The more stable
integer point estimate for this family is consequently 0.

## Prediction and limits

`Dock7` is predicted to have `predicted_n_degs = 0`.

This is driven mainly by within-dataset evidence from the focal training counts
and Parquet signatures of Dock/Rac/Cdc42/PAK/WAVE analogs. External biology was
used to choose the analogs and to avoid treating `Dock7` as a generic quiet
gene: it is a real neurodevelopmental Rac-GEF, but its established endpoints are
axon specification, chandelier-cell morphology, and disease phenotypes that are
stage-, cell-type-, and modality-shifted from acute postnatal thalamic
single-nucleus RNA. The main uncertainty is that Dock7 itself is not Dock3, and
human complete biallelic DOCK7 deficiency is severe. If the P16 thalamic
perturbation happened to expose a Dock7-specific ErbB4 or stress branch, the
Rac/PAK comparisons would underpredict it; the supplied training perturbations
provide no focal evidence for such a branch.
