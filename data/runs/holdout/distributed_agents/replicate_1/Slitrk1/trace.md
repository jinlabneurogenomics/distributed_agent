# DEG-count prediction trace

## Question and endpoint

The requested held-out perturbation is `Slitrk1`. I interpreted the task as a
point prediction of `n_degs` in `151 TH Prkcd Grin2c Glut`, where `n_degs` is
the number of measured genes with Wilcoxon Benjamini-Hochberg FDR < 0.05 in
perturbed nuclei versus the matched non-targeting control. The held-out
`Slitrk1` perturbation has no rows in the supplied differential-expression
Parquet and no entry in the focal training-count CSV, so the endpoint is
directly observed for training perturbations and absent for `Slitrk1`.

I treated significant self-target transcript changes as part of `n_degs`,
because the training CSV exactly matches a count of all focal `pvals_adj < 0.05`
rows in the Parquet. I did not use self-target log fold change as an editing
efficiency score; the dataset portrait notes that self RNA loss is not a
reliable readout of functional CRISPR disruption in this sparse AAV-Cas9
screen.

## Sources used

- Differential-expression Parquet:
  `training differential-expression dataset`.
  I queried only `151 TH Prkcd Grin2c Glut` rows for measured analog targets
  and Slitrk-family readout genes.
- Focal training endpoint CSV:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  This supplied the observed focal DEG counts for the non-held-out genes.
- Requested-target CSV:
  `single-target request for Slitrk1`.
  This contained exactly one requested target, `Slitrk1`.
- Run-local dataset portrait, task bindings, coverage, capability manifest, and
  measurement registry in `codex_runtime/pipeline`.
- Internal same-experiment semantic corpus
  `perturbai-july-260713-sourceguard-1773-v1`, specifically `Lrrtm1` and
  `Tenm3` Finding/Evidence records. This corpus is a packaged interpretation of
  the same Perturb-seq experiment, not independent replication.
- External PubMed literature, used only for gene-function priors:
  Abelson et al. 2005, Science, DOI `10.1126/science.1116502`, PMID
  `16224024`; Aruga and Mikoshiba 2003, Molecular and Cellular Neuroscience,
  DOI `10.1016/s1044-7431(03)00129-5`, PMID `14550773`; Yim et al. 2013,
  PNAS, DOI `10.1073/pnas.1209881110`, PMID `23345436`; Linhoff et al. 2009,
  Neuron, DOI `10.1016/j.neuron.2009.01.017`, PMID `19285470`;
  Soler-Llavina et al. 2011, PNAS, DOI `10.1073/pnas.1114028108`, PMID
  `21953696`; Monavarfeshani et al. 2018, eLife, DOI `10.7554/eLife.33498`,
  PMID `29424692`.

## Quantitative calibration

The training response breadth in the focal thalamic class was highly sparse:
among 1,674 training perturbations, 1,205 had `n_degs = 0`; the median was 0,
the 75th percentile was 1, the 90th percentile was 2, and the 95th percentile
was 18. Thus a generic postmitotic neuronal target needs strong local evidence
to predict a nonzero FDR count.

For analogs, I counted FDR < 0.05 rows in the focal Parquet after filtering
`group_name = '151 TH Prkcd Grin2c Glut'` and the selected `gene_target`
values, and inspected any rows with `pvals_adj < 0.10` to see whether the
training count was a self-transcript call or a broader downstream state.

Key focal analog counts were:

| training perturbation | observed focal `n_degs` | focal expression-pattern evidence |
| --- | ---: | --- |
| `Lrrtm1` | 1 | one non-self hit, `R3hdm2` up, log2FC 0.283, FDR 0.0269; 200 perturbed nuclei |
| `Lrrtm3` | 0 | no focal FDR < 0.10 rows among 17,259 measured genes; 195 perturbed nuclei |
| `Lrrtm4` | 0 | no focal FDR < 0.10 rows; 114 perturbed nuclei |
| `Flrt3` | 0 | no focal FDR < 0.10 rows; 168 perturbed nuclei |
| `Ptprd` | 0 | no focal FDR < 0.10 rows; 169 perturbed nuclei |
| `Ptprf` | 0 | no focal FDR < 0.10 rows; 237 perturbed nuclei |
| `Nlgn3` | 1 | only the `Nlgn3` self transcript was significant; log2FC -0.896, FDR 4.8e-11 |
| `Nrxn1` | 1 | only the `Nrxn1` self transcript was significant; log2FC -0.518, FDR 2.7e-23 |
| `Nrxn2` | 0 | no focal FDR < 0.10 rows; 281 perturbed nuclei |
| `Nrxn3` | 0 | no FDR < 0.05 rows; the only FDR < 0.10 row was `Vps4a` up, FDR 0.0908 |
| `Dlg4` | 1 | only the `Dlg4` self transcript was significant; log2FC -0.444 |
| `Shank2` | 0 | no focal FDR < 0.10 rows |
| `Shank3` | 2 | a sparse signal: `Shank3` self transcript and `Uba5` |
| `Adgrl1`, `Adgrl2`, `Adgrl3` | 1, 1, 1 | each count was a self-transcript call |
| `Tenm3`, `Tenm4`, `Dscam`, `Unc5c`, `Unc5d` | 1, 0, 0, 1, 0 | the nonzero calls were self transcripts |

These are imperfect but informative counterexamples. `Slitrk1` encodes a
cell-surface leucine-rich-repeat synapse organizer rather than a transcription
factor, spliceosome/proteasome component, or global chromatin regulator. In the
same focal assay, measured perturbations of LRRTM/neurexin/neuroligin/PSD
synapse organizers and related adhesion receptors were concentrated at zero or
at a single self transcript. The lone `Lrrtm1` non-self DEG did not generalize:
the internal `Lrrtm1` report found one downstream FDR < 0.10 gene across
371,796 downstream tests in 22 measured neuronal groups, and a targeted
immediate-early, AMPA/NMDA, postsynaptic-scaffold, neurexin, and synaptic-vesicle
panel had 0 FDR < 0.10 genes after `Lrrtm1` perturbation. Its literature-chosen
comparators `Lrrtm3`, `Lrrtm4`, `Nrxn1`, `Nrxn2`, `Nrxn3`, `Nlgn3`, `Dlg4`,
`Shank2`, and `Shank3` were themselves all null or singleton-sparse at the
whole-surface level in the internal corpus.

I also checked whether Slitrk-family transcripts themselves were a recurrent
module in `151`. `Slitrk1` was significantly changed by only three high-burden,
global regulators in the training focal rows: `Ctcf`, `Uba5`, and `Sin3a`.
`Slitrk2` was never significant. `Slitrk3`, `Slitrk4`, `Slitrk5`, and `Slitrk6`
were sporadically altered downstream of high-burden chromatin/proteostasis
perturbations such as `Tcf7l2`, `Ctcf`, `Tpr`, `Uba5`, `Zbtb7a`, `Ufc1`, and
`Cic`. That pattern supports Slitrk genes as occasional downstream state
markers, not as a focal single-gene SLITRK loss signature already exposed by
analogous membrane-protein knockouts.

## Target-specific biological transfer

### `Slitrk1`

External biology predicts a synaptic and neurite-morphology phenotype, but not
a broad constitutive nuclear RNA phenotype. Aruga and Mikoshiba defined Slitrk1
as one of six neural Slit- and Trk-like LRR transmembrane proteins and showed
Slitrk1 can promote unipolar neurite outgrowth in culture, with an intracellular
domain distinct from Slitrk2-6. Abelson et al. associated rare human `SLITRK1`
variants with Tourette syndrome and showed a Tourette frameshift mutant failed
to enhance dendritic growth in primary neurons. Yim et al. showed SLITRK family
members act with LAR receptor protein tyrosine phosphatases to organize
excitatory or inhibitory synapse formation in an isoform-dependent way.

The causal chain I used was:

`Slitrk1` CRISPR loss in P16 postmitotic mosaic neurons -> loss of a
postsynaptic LRR adhesion protein -> local changes in neurite/synapse
organization and possible PTPRD/PTPRF/PTPRS-dependent adhesion signaling ->
compensation by other adhesion organizers and pathway divergence across Slitrk
isoforms -> recovered P37-P44 `151 TH Prkcd Grin2c Glut` nuclei -> Wilcoxon
DEG count in nuclear RNA.

At the direct-molecular and local-synapse stages, the prior for a phenotype is
real. SLITRKs are synapse organizers, LRRTMs are excitatory synapse organizers
identified in the same broad class of LRR transmembrane adhesion proteins, and
LRRTMs/neuroligins/neurexins can have both overlapping and divergent synaptic
functions in vivo. At the endpoint stage, however, the assayed analogs show
that this class is strongly buffered in the P16-P37/44 snRNA-seq endpoint:
single perturbations of `Lrrtm1`, `Lrrtm3`, `Lrrtm4`, `Nrxn1`, `Nrxn2`,
`Nrxn3`, `Nlgn3`, `Dlg4`, `Shank2`, `Shank3`, `Flrt3`, `Ptprd`, and `Ptprf` did
not trigger a multi-gene `151` transcriptome. The same-experiment `Tenm3`
report makes the same point for a neighboring cell-surface adhesion axis:
teneurin, latrophilin, FLRT, LRRTM, neurexin, Dscam, and Unc5 comparators were
null or singleton-sparse as single-gene transcriptional modules, even though
their proteins have established wiring or synaptic roles.

The strongest case for a nonzero `Slitrk1` count would be a significant
self-transcript knockdown or an isolated idiosyncratic hit like `Lrrtm1`'s
`R3hdm2`. I discounted that to below 0.5 genes as a point estimate because
`Lrrtm1` itself was FDR=1.0 in the focal class despite 200 perturbed nuclei, the
LAR-RPTP analogs `Ptprd` and `Ptprf` were full zeroes, and the held-out endpoint
asks for BH-significant genes in coarse survivor nuclei rather than synapse
density, dendritic morphology, AMPA/NMDA receptor localization, or tics.

Prediction: `Slitrk1` -> 0 DEGs.

## Limits and uncertainty

This is an extrapolation from related but not identical proteins. No Slitrk
paralog was available as a training perturbation, and the external SLITRK1
literature mostly measures dendrites, synapses, or disease genetics rather than
P16 sparse CRISPR in thalamic glutamatergic neurons. The focal atlas class may
dilute a small Slitrk1-positive subpopulation, and the Parquet lacks indel
rates, protein abundance, synaptic structure, electrophysiology, and pre-assay
survival. A one-gene result, especially a self-transcript call, would not be
surprising; a broad DEG count would require a secondary stress or activity
state that the measured synaptic-adhesion analogs did not show.
