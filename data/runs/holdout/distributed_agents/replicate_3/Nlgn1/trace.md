# Nlgn1 DEG-count prediction trace

## Question and resolved ambiguities

I interpreted the held-out readout as the focal-cell DEG count for each
requested perturbation, where `n_degs` is exactly the number of rows with
`pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` for that perturbed
target. The requested manifest contains one held-out target, `Nlgn1`.

Two details affected the count estimate:

- The endpoint counts the perturbed target gene itself when its guide-mediated
  RNA depletion passes FDR 0.05. Thus an `n_degs = 1` training example can mean
  "self transcript only" rather than one downstream response gene.
- The task is not asking whether NLGN1 has an important synaptic function. It is
  asking whether sparse P16 AAV CRISPR loss of `Nlgn1`, read out by NeuN+
  single-nucleus RNA-seq 3-4 weeks later, creates enough nuclear RNA shifts in
  this thalamic glutamatergic cell group to pass a Wilcoxon/BH threshold.

## Sources used

- Read-only training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Read-only per-gene DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Requested-target manifest:
  `[local file: 152_Nlgn1.csv]`
- Same-experiment Distributed Agents corpus release
  `perturbai-july-260713-sourceguard-1773-v1`, especially target contexts for
  `Nlgn3`, `Nrxn1`, `Nrxn2`, `Nrxn3`, `Lrrtm1`, `Dlg4`, and `Shank3`.
- Distributed Agents runtime profile comparison over the focal-cell parquet rows for a
  neuroligin/neurexin/LRRTM/PSD candidate cohort. The generated run-local
  artifacts were `nlgn1_synaptic_profile_compare.json`,
  `nlgn1_synaptic_profile_inspect_adhesion.json`, and
  `nlgn1_synaptic_profile_inspect_psd.json`.
- PubMed literature on neuroligin-1 and neurexin/LRRTM excitatory synapse
  organization.

## Dataset checks and computations

The requested CSV has one data row: `Nlgn1`. It is absent from the training
count CSV and from the training DE parquet as a `gene_target`, as expected for a
fully held-out perturbation.

I summarized the 1,674 training DEG counts for the focal cell group. They are
heavily zero-inflated: the median is 0, the 75th percentile is 1, and only 469
targets have any FDR 0.05 gene in `151 TH Prkcd Grin2c Glut`.

I then joined biological nomination with direct focal-cell observations:

| training perturbation | focal `n_degs` | FDR 0.05 genes in `151 TH Prkcd Grin2c Glut` |
|---|---:|---|
| `Nlgn3` | 1 | `Nlgn3` |
| `Nrxn1` | 1 | `Nrxn1` |
| `Nrxn2` | 0 | none |
| `Nrxn3` | 0 | none |
| `Lrrtm1` | 1 | `R3hdm2` |
| `Lrrtm3` | 0 | none |
| `Lrrtm4` | 0 | none |
| `Dlg4` | 1 | `Dlg4` |
| `Dlgap4` | 2 | `Dlgap4`, `Vgf` |
| `Shank2` | 0 | none |
| `Shank3` | 2 | `Shank3`, `Uba5` |
| `Homer2` | 0 | none |
| `Magi2` | 0 | none |
| `Cacng2` | 0 | none |
| `Gria1`, `Gria2`, `Gria3` | 0 each | none |
| `Grin2a` | 1 | `Grin2a` |
| `Grin2b` | 2 | `Grin2b`, `Pianp` |
| `Grin1` | 89 | broad NMDA-receptor response |

The exact focal-cell DE rows show that the one-count entries for `Nlgn3`,
`Nrxn1`, and `Dlg4` are pure self-transcript hits. `Nlgn3` was down in its own
perturbation with score -7.90 and adjusted p value `4.79e-11`;
`Nrxn1` was down with score -10.87 and adjusted p value `2.67e-23`;
`Dlg4` was down with score -7.19 and adjusted p value `1.15e-08`.
`Shank3` had a weaker self hit plus one downstream gene, and `Lrrtm1` had one
non-self singleton. By contrast, `Grin1` generated 89 DEGs in the same cell
group, so the thalamic cell group and DE test were capable of reporting a broad
synaptic-receptor response when the perturbation actually propagated to the
nucleus.

For expression-pattern evidence, I compared signed Wilcoxon-score profiles
across all 17,259 measured focal-cell genes for 20 synaptic candidates. In the
`Nlgn3`-anchored rows, Pearson correlations to LRRTM, neurexin, PSD-scaffold,
and NMDA controls were tiny: for example `Nlgn3` versus `Dlg4` was 0.0106,
versus `Lrrtm3` was 0.0203, versus `Lrrtm4` was 0.0282, versus `Shank3` was
0.0345, and versus `Nrxn1` was likewise near zero in the complete comparison.
The `Nlgn3` singleton did not overlap any peer's FDR 0.05 set. This argues that
the neuroligin/neurexin sector is not carrying a hidden low-amplitude signed
module in these cells.

## Nlgn1-specific biological reasoning

`Nlgn1` is the closest functional family member available only by external
biology, because the exact gene was held out and the training parquet contained
only `Nlgn3`, not `Nlgn1`, as a neuroligin perturbation. Neuroligin-1 is a
postsynaptic adhesion molecule concentrated at excitatory glutamatergic
synapses, binds presynaptic beta-neurexins, and links neurexin adhesion to
PSD-95, AMPA receptor trapping, NMDA receptor function, and LTP. Those
properties were established by Song et al. 1999
(`doi:10.1073/pnas.96.3.1100`), Levinson et al. 2005
(`doi:10.1074/jbc.M413812200`), Mondin et al. 2011
(`doi:10.1523/JNEUROSCI.6439-10.2011`), Soler-Llavina et al. 2011
(`doi:10.1073/pnas.1114028108`), Jiang et al. 2016
(`doi:10.1038/mp.2016.80`), Jeong et al. 2019
(`doi:10.1073/pnas.1821775116`), and Wu et al. 2019
(`doi:10.1016/j.neuron.2019.02.013`). More broadly, neurexins use alternative
splicing and multiple postsynaptic ligands, including neuroligins and LRRTMs, to
organize synapses rather than to drive a single linear transcriptional pathway
(Siddiqui and Craig 2010, `doi:10.1016/j.conb.2010.08.016`; Reissner et al.
2013, `doi:10.1186/gb-2013-14-9-213`).

The within-dataset analogs point in the same direction:

- `Nlgn3` is the direct measured neuroligin-family analog. In this focal group
  it had exactly one FDR 0.05 DEG, its own transcript. The Distributed Agents same-
  experiment corpus additionally reports that `Nlgn3` had zero downstream genes
  at FDR 0.10 across all recovered neuronal cell groups and no meaningful
  whole-signature neighbor.
- `Nrxn1`, `Nrxn2`, and `Nrxn3` are the presynaptic receptor family for
  neuroligins. Their focal counts were 1, 0, and 0. Corpus findings for `Nrxn2`
  and `Nrxn3` specifically describe this as shared absence of broad DE across
  neurexin-family and ligand-side perturbations rather than a missed thalamic
  submodule.
- `Lrrtm1`, `Lrrtm3`, and `Lrrtm4` are alternative postsynaptic neurexin
  ligands. They had 1, 0, and 0 focal DEGs, and `Lrrtm1`'s one gene was an
  idiosyncratic `R3hdm2` singleton rather than a neuroligin-like response.
- `Dlg4`, `Shank2`, `Shank3`, `Homer2`, `Magi2`, and `Dlgap4` are PSD
  scaffolding comparators that could have revealed a shared excitatory
  postsynaptic mRNA program. They all sat in the same 0-2 count band; `Dlg4`
  itself was a self-only singleton. The corpus finding for `Dlg4` explicitly
  summarizes shared transcriptional flatness among `Dlg4`, `Nlgn3`, `Nrxn2`,
  `Shank2`, `Homer2`, `Magi2`, and `Cacng2`.
- `Grin1`, `Grin2a`, and `Grin2b` are counterexamples, not direct phenocopies.
  Their activity shows that some glutamate receptor perturbations, especially
  `Grin1`, can generate a detectable focal nuclear RNA response. Their stronger
  counts therefore sharpen the negative comparison for an adhesion protein like
  `Nlgn1`: the screen is not blind to every synaptic gene, but it is largely
  blind to isolated neuroligin/neurexin/LRRTM and PSD scaffold losses.

The remaining question is zero versus one. I chose a nonzero singleton because
`Nlgn1` itself is present as a measured focal feature, neuroligin-1 is expected
to be expressed in excitatory neurons, and the two best self-RNA analogs in the
same focal group, `Nlgn3` and `Nrxn1`, crossed FDR 0.05 only for their own
transcripts. I did not add any extra downstream genes because neither the exact
paralog nor the trans-synaptic and PSD neighbors formed a shared downstream
program in the focal signatures.

Final point prediction for `Nlgn1`: `1`.

## Limits

This is an extrapolation from `Nlgn3` plus synaptic neighbors; the same-
experiment corpus contained no direct `Nlgn1` finding because `Nlgn1` is the
held-out target. `Nlgn1` is not identical to `Nlgn3`: NLGN1 is biased toward
excitatory synapses and has a well documented role in NMDA-receptor-dependent
LTP, so a real thalamic `Nlgn1` response could be slightly larger than the
`Nlgn3` self-only response. Conversely, the whole endpoint can be zero if the
`Nlgn1` self transcript is less abundant in this cell group or the pooled guides
deplete nuclear `Nlgn1` less cleanly than `Nlgn3`. Finally, the Perturb-seq
readout does not test protein loss, receptor nanodomains, dendritic spine
structure, presynaptic release, or electrophysiology; these are the assays in
which NLGN1 biology is strongest.
