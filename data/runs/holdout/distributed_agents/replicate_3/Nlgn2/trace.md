# DEG-count prediction trace

## Question and endpoint

The requested held-out target file contains one gene:

| target_name |
|---|
| Nlgn2 |

I interpreted the endpoint as the exact `n_degs` count used in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: the number of measured
genes with `pvals_adj < 0.05` in the `151 TH Prkcd Grin2c Glut` differential
expression contrast for that knockout.  The count includes the perturbed gene
itself if its transcript is significantly depleted; it is therefore possible for
a biologically buffered perturbation to have `n_degs = 1` because only the
self-transcript passes FDR.

`Nlgn2` was absent from both the training DEG-count table and the supplied
training DE parquet as a perturbation target, so no `Nlgn2` DEG count or
`Nlgn2` perturbation signature was used from the endpoint data.

## Sources

Same-experiment inputs:

- `training_de_all_cell_groups.parquet`: the per-gene Wilcoxon DE statistics for
  non-held-out perturbations.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: focal-cell DEG counts for
  the 1,674 non-held-out perturbations.
- Distributed Agents internal semantic corpus, release
  `perturbai-july-260713-sourceguard-1773-v1`: I used cards and claims for
  `Nlgn3`, `Nrxn1`, and `Gphn` to cross-check literature-aware interpretation of
  the same experiment.  The corpus had no `Nlgn2` card, which I treated as
  missing held-out coverage, not as a null biological statement.
- Distributed Agents run-local profile tools: I compared Wilcoxon-score profiles in the
  focal cell group for a declared synaptic-adhesion/inhibitory-synapse cohort.

External biological evidence:

- Varoqueaux, Jamain, and Brose 2004, DOI `10.1078/0171-9335-00410`,
  PMID `15540461`: neuroligin-2 is localized to inhibitory synapses.
- Poulopoulos et al. 2009, DOI `10.1016/j.neuron.2009.08.023`,
  PMID `19755106`: NLGN2 binds gephyrin, activates collybistin, and drives
  postsynaptic assembly at perisomatic inhibitory synapses.
- Li et al. 2017, DOI `10.1016/j.neuron.2017.10.003`, PMID `29107521`:
  NLGN2 and SLITRK3 cooperate in inhibitory synapse development.
- Ali, Marth, and Krueger-Burg 2020, DOI `10.1126/scisignal.abd8379`,
  PMID `33443230`: review of NLGN2 as an inhibitory-synapse organizer and
  neurexin-linked adhesion molecule.

## Computational steps

The focal training-count distribution was strongly zero-inflated:

- 1,674 training targets
- median `n_degs = 0`
- 75th percentile `n_degs = 1`
- 469/1,674 targets with any focal DEG
- 106/1,674 with at least 10 DEGs

I then loaded the focal `151 TH Prkcd Grin2c Glut` rows from the parquet for
mechanistic analogs of `Nlgn2`: `Nlgn3`; `Nrxn1`, `Nrxn2`, `Nrxn3`; `Gphn`,
`Arhgef9`, and GABA receptor/transport neighbors; LRRTM, CADM, CNTNAP, SHANK,
and DLG scaffold/adhesion genes; and NMDAR genes as sensitivity controls.  For
each perturbation I counted rows with `pvals_adj < 0.05` and inspected the
identity of the significant features.  This mattered because many one-DEG
signatures were self-only.

I also ran a focal Wilcoxon-score profile comparison over 15 synaptic analogs
using `scores` as the signed value and `pvals_adj < 0.05` as the activity
threshold.  Nine profiles had one to nine significant features and six had none.
Pairwise Pearson/cosine values among `Nlgn3`, `Nrxn1`, `Gphn`, `Arhgef9`, and
their synaptic peers were near zero; for example, `Nlgn3` versus `Nrxn2` was the
largest whole-profile Pearson within the `Nlgn3` view at only `0.046`, and
`Nlgn3` versus `Gabra1` was `-0.057`.  None of the inspected pairs shared an
FDR-significant feature in the same direction.  Thus the analog set supplied
sparse counts, not a broad common expression pattern to transfer quantitatively.

## Target-specific reasoning

### Nlgn2

`Nlgn2` encodes neuroligin-2, a postsynaptic adhesion molecule concentrated at
inhibitory synapses.  Mechanistically it binds presynaptic neurexins across the
cleft and helps assemble the gephyrin/collybistin postsynaptic scaffold that
clusters GABA(A) and glycine receptors.  That biology made three training
groups the most relevant.

1. Neuroligin and neurexin adhesion.

| training target | focal `n_degs` | focal FDR pattern | interpretation for `Nlgn2` |
|---|---:|---|---|
| `Nlgn3` | 1 | the only FDR<0.05 row was self-depletion, `Nlgn3` log2FC `-0.90`, q `4.79e-11` | The nearest assayed neuroligin paralog showed no downstream focal module.  NLGN3 is not inhibitory-specific like NLGN2, but the self-only result is the strongest evidence that an acute neuroligin knockout can be transcriptomically buffered in this assay. |
| `Nrxn1` | 1 | self-only, `Nrxn1` log2FC `-0.52`, q `2.67e-23` | Neurexin is the presynaptic NLGN binding family; a one-gene self-only result argues against a generic neurexin/neuroligin nuclear response. |
| `Nrxn2` | 0 | no FDR<0.05 genes | A direct neurexin-family counterexample with no focal self or downstream DEG. |
| `Nrxn3` | 0 | no FDR<0.05 genes; one q<0.10 row, `Vps4a`, q `0.0908` | Another neurexin-family counterexample; no broad downstream state. |

The internal Distributed Agents corpus supported the same interpretation.  The `Nlgn3`
card reported zero downstream genes at FDR<0.10 across all recovered neuronal
cell groups and stated that neurexin/neuroligin and scaffold neighbors were
near-zero correlated with `Nlgn3`.  The `Nrxn1` and `Nrxn2` cards likewise
described mostly flat or one-gene surfaces for represented neurexin-family and
ligand-side targets.  The selected corpus had no `Nlgn2` record, so this is an
extrapolation from paralog and binding-partner measurements.

2. Inhibitory postsynaptic scaffold and receptor-complex genes.

| training target | focal `n_degs` | focal FDR pattern | interpretation for `Nlgn2` |
|---|---:|---|---|
| `Gphn` | 0 | no FDR<0.05 genes in the focal group | GPHN is the central gephyrin scaffold recruited downstream of NLGN2; its null focal signature shows that disrupting the inhibitory postsynaptic scaffold does not necessarily produce focal nuclear DE. |
| `Arhgef9` | 1 | self-only, `Arhgef9` log2FC `-0.57`, q `3.70e-08` | Collybistin is activated by NLGN2 and controls gephyrin membrane clustering; the focal response was again just target depletion. |
| `Gabra1` | 1 | self-only, `Gabra1` log2FC `-1.13`, q `4.26e-18` | A GABA(A) receptor alpha-subunit perturbation did not induce GABA receptor compensation. |
| `Gabra2`, `Gabra3`, `Gabra5` | 0, 0, 0 | no FDR<0.05 genes | GABA(A) receptor subunit losses were mostly invisible to the focal snRNA endpoint. |
| `Gabbr1`, `Gabbr2` | 1, 1 | self-only for both targets | GABA(B) receptor subunits also stayed at the self-transcript-only scale. |

The `Gphn` corpus card specifically warned that the expected phenotype of
gephyrin loss is receptor clustering and inhibitory physiology, not necessarily
a change in nuclear abundance of `Gabra`, `Gabrb`, `Gabrg`, `Glra`, `Arhgef9`,
or `Nlgn` transcripts.  That is a close conceptual fit for NLGN2: the most
likely primary defect is local inhibitory-synapse organization rather than a
large somatic RNA program.

3. Other synaptic adhesion/scaffold controls and NMDAR counterexamples.

| training target | focal `n_degs` | focal FDR pattern | use as evidence |
|---|---:|---|---|
| `Lrrtm1` | 1 | one downstream gene, `R3hdm2`, q `0.0269` | LRRTMs are neurexin-linked adhesion proteins; the singleton response argues that neurexin-ligand perturbations need not give broad DE. |
| `Lrrtm3`, `Lrrtm4` | 0, 0 | no FDR<0.05 genes | Additional flat neurexin-ligand perturbations. |
| `Dlg4` | 1 | self-only, `Dlg4` q `1.15e-08` | A PSD scaffold gene with local synaptic function but no broad focal mRNA response. |
| `Shank2`, `Shank3` | 0, 2 | `Shank3` had self plus `Uba5`; `Shank2` had none | ASD/synaptic scaffolds are not generically high-DEG in this assay. |
| `Grin1` | 89 | self plus a multi-gene downstream program | Positive control: the same focal group and Wilcoxon workflow can detect broad receptor-coupled transcriptional changes. |
| `Grin2a`, `Grin2b`, `Grin2d`, `Grin3a` | 1, 2, 0, 0 | mostly self-only or sparse | Even among NMDAR subunits, large focal DEG counts are not automatic. |

These controls set the approximate scale.  `Grin1` shows that a broad response
is observable when present, but the NLGN/NRXN/GPHN/ARHGEF9/GABA receptor
neighborhood around NLGN2 sits at zero or one focal DEGs, usually just the
perturbed transcript itself.

## Prediction decision

I predict a nonzero count for `Nlgn2`, but only barely: `1`.

The external biology makes NLGN2 highly relevant for inhibitory synapse
structure in glutamatergic neurons, yet the same-experiment analogs show that
this class of acute, postmitotic synaptic-adhesion perturbation is largely
off-axis for the juvenile nuclear RNA endpoint.  I therefore did not transfer
the large `Grin1` response or any broad disease-gene prior to NLGN2.  The reason
for choosing `1` rather than `0` is that the endpoint counts self-target rows
and the closest expressed paralog, `Nlgn3`, was exactly a self-only one-DEG
signature in the focal group.  `Nrxn1`, `Gabra1`, `Gabbr1`, `Gabbr2`, `Arhgef9`,
`Dlg4`, `Cadm2`, `Cntnap1`, and `Cntnap2` reinforce that pattern: the target RNA
can be the only called DEG while downstream genes stay below FDR 0.05.

## Limits

This is an extrapolation because `Nlgn2`, `Nlgn1`, `Nlgn4`, `Slitrk3`, `Mdga1`,
and `Mdga2` were not available as direct training perturbations.  NLGN3 is a
paralog but is not functionally identical to inhibitory-specific NLGN2, and
neurexins are presynaptic multi-isoform hubs rather than postsynaptic NLGN2
substitutes.  The assay measures steady-state nuclear RNA in recovered NeuN+
nuclei; it does not measure GABAergic puncta, receptor localization, miniature
inhibitory currents, or survival before cell recovery.  The largest uncertainty
is the self-transcript call: if `Nlgn2` is not detectably expressed or not
significantly depleted in this focal class, the true count would likely be `0`;
if the perturbation leaks into a real homeostatic inhibitory-synapse RNA
response, a few downstream genes could pass FDR.  The same-experiment analogs
make either a broad response or dozens of focal DEGs unlikely.

