# Question

The task asks for a point prediction of `n_degs` for the held-out `Nlgn1`
perturbation in `151 TH Prkcd Grin2c Glut` neurons.  I interpreted `n_degs` as
the total number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
in that focal cell group, including the target transcript when it was measured
and significant.  That convention matches the training CSV: in the parquet
slice for `151 TH Prkcd Grin2c Glut`, `Nlgn3`, `Nrxn1`, `Dlg4`, `Cadm2`, and
`Cntnap2` each have exactly one FDR<0.05 row, and the row is the perturbed gene
itself.

There was one requested target:

| held-out target | requested-order position |
|---|---:|
| Nlgn1 | 1 |

# Sources Used

- Direct endpoint table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  This is direct evidence for non-held-out training perturbations in the
  requested endpoint.
- Direct differential-expression parquet:
  `training differential-expression dataset`.
  I queried only `151 TH Prkcd Grin2c Glut` rows for biologically selected
  synaptic adhesion, postsynaptic-density, and glutamate-receptor comparators.
- Run-local requested-target manifest:
  `single-target request for Nlgn1`.
- Dataset portrait and measurement registry in `codex_runtime/pipeline`.
  These establish that the parquet and report corpus are same-experiment
  representations, that the readout is survivor-conditioned single-nucleus RNA,
  and that self-transcript loss is not an editing-efficiency score.
- Internal same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, using bounded
  `corpus.findings`, `corpus.report_evidence`, `corpus.calibration`, and
  `corpus.graph` for exact comparator identities in the packaged
  same-experiment reports.  The graph was used only to confirm which comparator
  genes were named in the `Nlgn3` report; relation count and topology were not
  used as candidate scores.
- External literature from NCBI PubMed E-utilities:
  Chubykin et al. 2007, Neuron, doi:10.1016/j.neuron.2007.05.029,
  PMID:17582332; Craig and Kang 2007, Current Opinion in Neurobiology,
  doi:10.1016/j.conb.2007.01.011, PMID:17275284; Reissner et al. 2013,
  Genome Biology, doi:10.1186/gb-2013-14-9-213, PMID:24083347; Jeong et al.
  2019, PNAS, doi:10.1073/pnas.1821775116, PMID:31138690; Szüber et al. 2024,
  Frontiers in Molecular Neuroscience, doi:10.3389/fnmol.2024.1359067,
  PMID:38813439.

# Quantitative Calibration

The focal training distribution is highly zero-inflated.  Among 1,674
non-held-out perturbations, 1,205 have `n_degs = 0`, the median is 0, the 75th
percentile is 1, the 90th percentile is 2, and the maximum is 2,677.  Therefore
the prior for an arbitrary held-out gene is 0 or a singleton unless its local
mechanistic neighbors are broad responders.

I queried the parquet for the 151-group rows of the most relevant represented
NLGN/NRXN/PSD/LRRTM/CADM/CNTP/glutamate-receptor perturbations and counted rows
with `pvals_adj < 0.05`:

| training perturbation | 151-group `n_degs` | FDR<0.05 rows in the focal group | reason for comparison to Nlgn1 |
|---|---:|---|---|
| Nlgn3 | 1 | `Nlgn3` down | closest measured neuroligin paralog; postsynaptic neurexin-binding adhesion molecule |
| Nrxn1 | 1 | `Nrxn1` down | presynaptic binding partner class for neuroligins |
| Nrxn2 | 0 | none | neurexin paralog counterexample |
| Nrxn3 | 0 | none | neurexin paralog counterexample |
| Dlg4 / PSD-95 | 1 | `Dlg4` down | NLGN1 binds PSD-95 through its PDZ ligand and depends on PSD-95 for synaptic localization |
| Shank2 | 0 | none | excitatory postsynaptic scaffold counterexample |
| Shank3 | 2 | `Shank3` down, `Uba5` up | excitatory postsynaptic scaffold; showed only a singleton downstream response |
| Dlgap4 | 2 | `Dlgap4` down, `Vgf` down | SHANK-associated PSD/GKAP family member; visible but still sparse |
| Lrrtm1 | 1 | `R3hdm2` up | neurexin-binding excitatory synapse organizer unrelated by family |
| Lrrtm3 | 0 | none | LRRTM counterexample |
| Lrrtm4 | 0 | none | LRRTM counterexample |
| Cadm2 | 1 | `Cadm2` down | immunoglobulin-family synaptic adhesion counterexample |
| Cntnap2 | 1 | `Cntnap2` down | disease-linked neuronal adhesion protein; self-only in the focal group |
| Gria1 | 0 | none | AMPA-receptor subunit counterexample |
| Gria2 | 0 | none | AMPA-receptor subunit counterexample |
| Grid1 | 1 | `Grid1` down | ionotropic glutamate receptor-family counterexample |
| Grid2 | 0 | none | ionotropic glutamate receptor-family counterexample |
| Grin2a | 1 | `Grin2a` down | NMDA receptor subunit counterexample |
| Grin2b | 2 | `Grin2b` down, `Pianp` down | NMDA receptor subunit counterexample |
| Grin1 | 89 | broad mixed up/down program | direct obligatory NMDAR-subunit perturbation showing that receptor loss can be visible |
| Magi2 | 0 | none | PSD scaffolding counterexample |
| Syngap1 | 0 | none | PSD signaling counterexample |

The local counts make `Nlgn3` and `Dlg4` the strongest quantitative anchors:
both affect proteins immediately adjacent to NLGN1 at excitatory postsynapses
and both produced one counted DEG, the self-transcript only.  The adhesion
neighborhood around those anchors is also sparse: `Nrxn1`, `Nrxn2`, `Nrxn3`,
`Lrrtm1`, `Lrrtm3`, `Lrrtm4`, `Cadm2`, and `Cntnap2` fell between 0 and 1 in the
same focal endpoint.  The SHANK/DLGAP neighborhood likewise stayed at 0-2.

I used `Grin1` as a counterexample rather than as the main anchor.  `NLGN1`
organizes excitatory synapses and interacts with NMDAR-containing PSDs, but it
is not itself the obligatory NMDA receptor channel subunit.  Direct `Grin1`
loss created 89 FDR<0.05 genes in the focal group, including `Scg2`, `Stmn4`,
`Kctd16`, `Gpm6a`, and `Tspan7`, showing that this cell group can mount a broad
NMDAR-loss transcriptional response.  `Nlgn3`, `Dlg4`, `Shank3`, and the other
PSD/adhesion perturbations did not copy that state.

# Same-Experiment Corpus Evidence

The July same-experiment corpus reinforced the direct parquet query rather than
replacing it.

- The `Nlgn3` report states that all 22 recovered neuronal groups had zero
  downstream FDR<0.10 genes after excluding `Nlgn3` itself.  In `151 TH Prkcd
  Grin2c Glut`, `Nlgn3` RNA decreased strongly but no non-self gene reached
  FDR<0.10.
- Its `Nlgn3:F002` cross-perturbation contrast explicitly compared `Nlgn3` with
  `Nrxn1`, `Nrxn2`, `Nrxn3`, `Dag1`, `Lrrtm1`, `Adam10`, `Dlg4`, `Shank2`,
  `Shank3`, and `Cntnap2`; those literature-obvious synaptic relatives were
  transcriptionally flat or sparse and had near-zero score correlations to
  `Nlgn3`.
- `Nlgn3:F004` used `Grin1`, `Grin2b`, and `Tsc2` as sensitivity controls:
  these perturbations produced many downstream FDR<0.10 genes in the same
  screen universe while `Nlgn3` stayed flat.  This argues against treating
  every synaptic gene as undetectable in the assay.
- The `Dlg4` report similarly called PSD-95 loss a globally downstream-flat
  event at the snRNA level; the only 151-group FDR<0.05 row in my direct query
  was `Dlg4` itself.
- The `Shank3`, `Lrrtm1`, and `Cntnap2` reports described small singleton or
  near-null surfaces, supporting the idea that canonical synaptic adhesion and
  scaffold phenotypes are displaced toward receptor localization, synaptic
  protein organization, and electrophysiology rather than a stable cell-body
  mRNA program.

# Biological Transfer to Nlgn1

The causal chain I used for transfer was:

`Nlgn1` CRISPR loss in postmitotic neurons -> reduced NLGN1 function at
postsynaptic excitatory synapses -> altered trans-synaptic neurexin adhesion,
PSD-95 coupling, and NMDAR/AMPAR balance -> local synapse and physiology
effects over 3-4 weeks -> surviving NeuN-positive thalamic glutamatergic nuclei
sampled by 10x Flex -> Wilcoxon DE count.

External literature makes `Nlgn1` a real synaptic gene but does not predict an
obligate broad nuclear transcriptional state.  Chubykin et al. showed that
neuroligin-1 overexpression selectively enhances excitatory responses and
potentiates NMDAR/AMPAR ratios, while Nlgn1 deletion selectively decreases the
NMDAR/AMPAR ratio.  Craig and Kang and Reissner et al. review neuroligin-
neurexin trans-synaptic adhesion and the broader NLGN/NRXN/LRRTM/Cbln synaptic
adhesion network.  Jeong et al. showed that the NLGN1/PSD-95 interaction is
phosphorylation-regulated and affects NLGN1 surface and synaptic localization.
Szüber et al. place TrkB-dependent NLGN1 tyrosine phosphorylation upstream of
PSD-95 accumulation in a cultured-neuron synaptogenic assay.  These mechanisms
operate at synaptic membranes and protein scaffolds, so the same-experiment
`Nlgn3`, `Dlg4`, `Shank3`, `Lrrtm1`, and `Nrxn` null/singleton results are
better endpoint analogs than the broad `Grin1` channel-subunit state.

# Prediction

For `Nlgn1`, I predict a nonzero but singleton response:

- The nonzero call is driven mainly by the self-transcript expectation.
  `Nlgn1` is an expressed excitatory postsynaptic gene, and the nearest
  self-only local anchors, `Nlgn3`, `Nrxn1`, `Dlg4`, `Cadm2`, and `Cntnap2`, all
  counted exactly their own transcript at FDR<0.05 in this focal group.
- I did not add a downstream DEG because the NLGN/NRXN/PSD/LRRTM/CADM/Cntnap2
  comparison set was overwhelmingly buffered.  `Nlgn3` is the closest measured
  paralog and had no non-self FDR<0.10 genes in any recovered neuronal class in
  the packaged report, despite detectable self-transcript depletion in the
  focal group.
- I kept the count far below `Grin1` because an NLGN1 adhesion/scaffold
  perturbation is upstream or adjacent to NMDAR physiology but is not an
  obligate loss of the receptor channel complex.  The direct channel/subunit
  perturbation is a boundary counterexample, not a phenocopy.

Point prediction: `Nlgn1 = 1`.

# Limits

- `Nlgn1`, `Nlgn2`, and `Nlgn4x` were not represented as non-held-out training
  perturbations, so the direct neuroligin-family anchor is `Nlgn3` rather than
  an exact NLGN1 paralog or an excitatory/inhibitory NLGN1-vs-NLGN2 contrast.
- The prediction is a count in one assay, not a statement that NLGN1 loss is
  biologically inert.  snRNA-seq did not measure PSD-95/NMDAR localization,
  NMDAR/AMPAR ratios, dendritic spines, neurexin splice isoforms, local
  translation, or synaptic currents.
- The held-out count can include the `Nlgn1` transcript itself; whether a
  self-row passes FDR depends on baseline focal-cell expression, gRNA recovery,
  and RNA destabilization of edited alleles.  The prediction of 1 assumes
  Nlgn1 behaves like the expressed `Nlgn3`, `Nrxn1`, `Dlg4`, `Cadm2`, and
  `Cntnap2` anchors in this group.
- The external literature is from hippocampal/cortical culture, knockout, and
  review settings rather than this exact P16 mosaic thalamic Perturb-seq
  design.  I used it only to decide which same-experiment perturbations are
  mechanistically appropriate analogs.
