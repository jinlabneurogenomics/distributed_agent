# Question and interpretation

The held-out manifest for this run contains one perturbation, `Camk4`. I
interpreted the requested endpoint as the integer number of measured genes with
`pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` after acute P16 AAV
CRISPR loss of `Camk4`, using the same single-nucleus Wilcoxon/BH procedure
used for the supplied training rows.

I treated zero as a literal prediction that no assayed gene, including the
target transcript, will cross FDR 0.05. A positive singleton prediction means I
expect only a very small effect, most likely the target transcript itself, to
cross the threshold. I did not treat developmental germline CaMKIV knockout,
dominant drug perturbation, or acutely stimulated phospho-CREB results as
quantitative DEG-count evidence, because this screen measures a sparse,
postmitotic, unstimulated loss-of-function state 3-4 weeks after AAV delivery.

# Sources

* Training endpoints: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
* Training signatures: focal rows of
  `training_de_all_cell_groups.parquet`, queried with DuckDB for
  `group_name = '151 TH Prkcd Grin2c Glut'` and mechanistically nominated
  targets.
* Distributed Agents corpus `perturbai-july-260713-sourceguard-1773-v1`. `Camk4` itself
  was not a corpus target in this release, so the corpus was used only for
  in-dataset training-target summaries around `Creb1`, `Mef2a`, `Calm1`, MEF2
  paralogs, calmodulins, CaMKII subunits, calcineurin subunits, and `Ntrk2`.
* PubMed literature on CaMKIV biology, especially:
  * Matthews et al. 1994, DOI `10.1128/mcb.14.9.6107-6116.1994`: CaMKIV, but
    not CaMKII, entered the nucleus and activated CREB-dependent transcription.
  * Shieh et al. 1998, DOI `10.1016/s0896-6273(00)81011-9`: cortical-neuron
    BDNF exon III calcium response included a CREB-dependent arm driven by
    CaMKIV.
  * Anderson and Kane 1998, DOI `10.1023/a:1009276932076`, and Soderling 1999,
    DOI `10.1016/s0968-0004(99)01383-3`: reviews placing CaMKIV downstream of
    Ca2+/calmodulin and CaMKK and upstream of nuclear CREB signaling.
  * See et al. 2001, DOI `10.1096/fj.00-0106com`: CaMKIV/CREB supported
    survival of depolarized cerebellar granule neurons.
  * Song et al. 2015, DOI `10.1007/s11427-014-4781-4`: CaMKIV knockout mice
    had behavioral phenotypes, but NMDA/depolarization induction of CREB and
    BDNF remained intact in cortical neurons, illustrating redundancy of this
    kinase for some activity-regulated transcriptional outputs.
  * Arrazola et al. 2009, DOI `10.1002/jcp.21902`: Wnt/beta-catenin can induce
    CaMKIV expression in hippocampal neurons. I used this only as a possible
    upstream relation to reject, not as evidence that `Camk4` loss should
    phenocopy `Ctnnb1` loss.

# Focal training calibration

I first read the held-out CSV and confirmed that the only requested target was
`Camk4`. I then read the training count CSV to calibrate the focal-cell
distribution: 1205 of 1674 non-held-out targets had `n_degs = 0`, the median was
0, the 75th percentile was 1, the 90th percentile was 2, and the 95th
percentile was 18. Broad responses were rare and dominated by global
RNA/protein-homeostasis or transcriptional regulators such as `Uba5`, `Tpr`,
`Sin3a`, `Rnpc3`, `Zbtb7a`, and proteasome targets.

The query over the focal parquet rows selected a CaMKIV neighborhood rather
than all 28.9 million rows in the cell group: CaMKII subunits, calmodulins,
CREB/CBP, MEF2 factors, calcineurin, TrkB, voltage-gated calcium channels,
NMDAR/PSD genes, PKA/MAPK neighbors, and the Wnt/beta-catenin counterexample.
For each nominated training perturbation I compared the supplied
`n_degs < 0.05` count with the actual focal FDR genes and signs.

# `Camk4` reasoning

## Direct calcium/calmodulin and CaMK paralogs

`Camk4` is a nuclear Ca2+/calmodulin- and CaMKK-activated kinase that can
phosphorylate CREB and couple calcium entry to transcription. The closest
represented CaMK family perturbations in the training set were not broad in
`151 TH Prkcd Grin2c Glut`:

* `Camk2a`: `n_degs = 0`. The target transcript was measured but its focal
  self log2 fold change was only `-0.16` with BH FDR 1.0.
* `Camk2b`: `n_degs = 1`, consisting of the target transcript itself
  (`Camk2b -0.44`, FDR `1.3e-10`).
* `Camk2g`: `n_degs = 0`, despite a negative self log fold change.

The Distributed Agents corpus independently summarized this as non-convergence among
measured CaMKII paralogs and absence of a robust CaMKII transcriptomic module.
This is the most important same-family calibration: a calcium/CaM kinase label
alone did not produce a durable basal RNA response in this cell group.

Single calmodulin-locus perturbations also argued for buffering rather than a
shared Ca2+/CaM collapse:

* `Calm1`: `n_degs = 14`, with `Calm1` down and a small
  Rasgrp2/Peg3/Resp18/Vamp1/Tuba1b/Atp2b1 homeostatic module.
* `Calm2`: `n_degs = 0`.
* `Calm3`: `n_degs = 1`, the direct `Calm3` transcript.

The corpus notes that `Calm1`, `Calm2`, and `Calm3` did not phenocopy each other
or the represented CaM effectors. It also reports that `Calm1` loss did not
turn on a Fos/Junb/Arc/Npas4/Egr/Nr4a activity-dependent program. Thus even a
more proximal perturbation to all CaMKs gave sparse, branch-specific outputs.

## Downstream CREB, CBP, MEF2, and calcineurin readouts

CaMKIV's canonical nuclear substrates are closer to the measurable readout than
CaMKIV itself. Those targets were detectable but still small in the focal
group:

* `Creb1`: `n_degs = 10`, centered on strong `Crem` induction and a few
  down-regulated organelle/lipid/lysosomal genes. The Distributed Agents summary
  specifically notes that this was the broadest `Creb1` group but was not a
  basal `Bdnf/Fos/Arc/Npas4` immediate-early program.
* `Crebbp`: `n_degs = 8`, without a clear same-direction phenocopy of `Creb1`.
* `Mef2a`: `n_degs = 4` at the stricter FDR 0.05 threshold
  (`Gpr4`, `Prkcg`, `Ogt`, `Sez6`). Distributed Agents describes the FDR 0.10 signature
  as a tiny 151-only thalamic response embedded partly in `Ctnnb1`, not as the
  canonical Arc/synapse-elimination arm.
* `Mef2c`: `n_degs = 1` in the focal group; its larger cortical IT response did
  not generalize to 151.
* `Mef2d`: `n_degs = 0`.
* `Ppp3ca`, `Ppp3cc`, `Ppp3r1`: `n_degs = 4`, `0`, and `9`, respectively.
  Corpus MEF2 summaries note that these calcineurin perturbations did not
  phenocopy the tiny `Mef2a` response.
* `Hdac5`, a represented class-IIa HDAC corepressor neighbor, had `n_degs = 0`.

This pattern makes a multi-dozen `Camk4` count unlikely. If loss of the
transcription factors themselves or of CREB coactivator input is only 1-10 DEGs
in this cell group, then loss of one upstream kinase, in a family with known
redundancy, should be weaker.

## Rejected broader pathway analogs

I considered several broader calcium or synaptic perturbations as upper-bound
counterexamples and rejected them as quantitative analogs.

`Grin1` had `n_degs = 89`, but `Grin2a`, `Grin2b`, `Grin2d`, and `Grin3a`
had 1, 2, 0, and 0 DEGs in the same focal group, and the CaMKII and calmodulin
targets did not converge with NMDA receptor loss in the corpus summaries.
`Grin1` is therefore a receptor-core perturbation, not a good proxy for loss of
one nuclear CaM kinase.

Voltage-gated calcium-channel perturbations were also mostly self-only or flat:
`Cacna1a`, `Cacna1d`, and `Cacna1e` were 0; `Cacna2d1` and `Cacnb4` were 1; and
`Cacna1g` was 12 with a T-type-channel-specific mix. These bound `Camk4` in the
same sparse range as the direct CaM/CaMK/CREB neighborhood.

Finally, `Ctnnb1` had 383 focal DEGs and the corpus describes a large Wnt,
adhesion, excitability, and neuropeptide response. Wnt/beta-catenin can induce
`Camk4` expression in hippocampal neurons, but in this screen the `Ctnnb1`
signature is far broader than one Wnt-regulated kinase. I did not transfer the
`Ctnnb1` count to `Camk4`.

## Point estimate

The within-dataset evidence is stronger than the external literature for the
count scale. The literature says CaMKIV can drive CREB-dependent transcription
after calcium signals, while Song et al. 2015 shows that some
NMDA/depolarization-induced CREB/BDNF responses persist in CaMKIV-null cortical
neurons. The training set says that, under the actual basal P16 sparse-CRISPR
assay, CaMKII, calmodulin, CREB, MEF2, calcineurin, PKA/MAPK, and TrkB nodes
mostly produce 0-10 focal DEGs, often just their own transcript.

I therefore predict a sparse nonzero response for `Camk4`: one DEG. The single
gene is most likely direct `Camk4` mRNA depletion rather than a propagated
CREB/MEF2 module. `Camk4` is present in the measured focal gene set and was
itself BH-significant as a downstream gene of five broad training perturbations
(`Bmal1`, `Nr1d1`, `Rab7`, `Psmb4`, and `Hnrnpu`), so it is expressed enough to
be detectable in this cell class. I still kept the count to 1 because every
mechanistically close pathway comparison argues against a broader stable RNA
state.

# Limits

The weakest part of the prediction is the direct target-transcript call. Guide
cutting and nonsense-mediated decay for held-out `Camk4` are not measured in the
inputs, and several expressed training targets, including `Camk2a`, failed to
show significant self-depletion in 151. If the `Camk4` guides are inefficient or
the transcript is too sparse, the true count could be 0.

The MEF2 literature used here is partly non-neuronal, and the Wnt relation was
shown in hippocampal neurons rather than thalamic `Prkcd/Grin2c` neurons.
Those mechanisms were therefore used only to nominate in-dataset comparators.
The final scale is driven by the same-experiment training signatures, not by
assuming that acute calcium stimulation phenotypes will persist for weeks in
resting NeuN-positive nuclei.
