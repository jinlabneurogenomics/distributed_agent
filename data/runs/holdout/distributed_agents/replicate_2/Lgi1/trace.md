# Lgi1 DEG-count prediction trace

## Question and resolved ambiguities

The requested held-out perturbation set contains one target, `Lgi1`. I interpreted
the endpoint as the exact training endpoint in
`151 TH Prkcd Grin2c Glut`: the count of measured genes with
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` after acute sparse
AAV-PHP.eB CRISPR-Cas9 loss of the target gene in postnatal NeuN+ mouse nuclei.
The count includes the targeted transcript itself if that row passes FDR, as in
the observed `Adam22`, `Dlg4`, `Cadm2`, `Nlgn3`, and `Nrxn1` training examples.

I treated the held-out `Lgi1` signature as unavailable. `Lgi1` was absent from
the training count CSV and from the parquet `gene_target` column, so I did not
use any `Lgi1` perturbation DE rows. I did inspect `Lgi1` as a measured
`names` feature in other, non-held-out perturbations to confirm that it is not
invisible to the focal-cell Wilcoxon test.

## Sources used

Inputs:

- `[local file: training_de_all_cell_groups.parquet]`
- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- `[local file: 125_Lgi1.csv]`

Internal same-experiment knowledge:

- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`.
  It had no direct `Lgi1` target context, but it did contain an `Adam22`
  context and same-experiment claims that represented AMPAR/TARP/scaffold
  perturbations, neurexin/LRRTM/neuroligin/CADM/GluD adhesion perturbations, and
  postsynaptic-scaffold perturbations are buffered or near-null in this basal
  postnatal snRNA-seq readout.
- Distributed Agents runtime profile tools over the focal-cell parquet slice. I compared
  `Adam22` against a hand-selected synaptic cohort containing represented
  AMPAR, TARP, PSD-scaffold, neurexin, neuroligin, LRRTM, CADM/GluD, IL1RAPL,
  and PTP-delta targets.

External mechanism evidence:

- NCBI PubMed via `bioeval_literature`.
- Fukata et al. 2010, PNAS, DOI `10.1073/pnas.0914537107`, PMID `20133599`:
  secreted LGI1 links the epilepsy-related ADAM22 and ADAM23 receptors in a
  trans-synaptic complex containing presynaptic potassium channels and
  postsynaptic AMPA-receptor scaffolds; Lgi1 loss in mice causes lethal
  epilepsy and reduced AMPAR-mediated hippocampal transmission.
- Ohkawa et al. 2013, Journal of Neuroscience, DOI
  `10.1523/JNEUROSCI.3506-13.2013`, PMID `24227725`: LGI1 autoantibodies can
  block the LGI1-ADAM22/23 interaction and reduce synaptic AMPAR clusters,
  supporting the same extracellular receptor/AMPAR axis in acquired LGI1
  autoimmunity and in the knockout mouse.

## Computation over the supplied data

The manifest has exactly one requested target:

| target_name |
| --- |
| Lgi1 |

The focal training count CSV has 1,674 non-held-out perturbations. Its count
distribution is heavily zero-inflated: 1,205/1,674 are zero, the median is 0,
the 75th percentile is 1, and the 95th percentile is 18. Thus the prior for a
typical synaptic or adhesion perturbation is a flat focal response unless a
nearby observed target shows otherwise.

For the biologically nominated comparators I read focal-cell rows from the
parquet with this filter:

```python
(group_name == "151 TH Prkcd Grin2c Glut")
& gene_target.isin(relevant_training_targets)
& (pvals_adj < 0.05)
```

I also used the small training-count CSV to retrieve exact `n_degs` for the
same targets. The most relevant observations were:

| training perturbation | focal `n_degs` | focal FDR-level rows seen in the parquet |
| --- | ---: | --- |
| `Adam22` | 1 | only `Adam22`, logFC -0.550, FDR 1.07e-9 |
| `Gria1` | 0 | none |
| `Gria2` | 0 | none |
| `Gria3` | 0 | none |
| `Cacng2` | 0 | none |
| `Cacng3` | 0 | none |
| `Dlg4` | 1 | only `Dlg4`, logFC -0.444, FDR 1.15e-8 |
| `Dlgap4` | 2 | `Dlgap4` and `Vgf` |
| `Homer2` | 0 | none |
| `Shank2` | 0 | none |
| `Lrrc7` | 0 | none |
| `Nrxn1` | 1 | only `Nrxn1`, logFC -0.518, FDR 2.67e-23 |
| `Nrxn2` | 0 | none |
| `Nrxn3` | 0 | none |
| `Nlgn3` | 1 | only `Nlgn3`, logFC -0.896, FDR 4.79e-11 |
| `Cadm2` | 1 | only `Cadm2`, logFC -0.757, FDR 6.47e-16 |
| `Grid2` | 0 | none |
| `Lrrtm3` | 0 | none |
| `Lrrtm4` | 0 | none |
| `Il1rap` | 0 | none |
| `Il1rapl1` | 0 | none |
| `Il1rapl2` | 0 | none |
| `Ptprd` | 0 | none |
| `Ptprt` | 0 | none |
| `Kcna1` | 0 | none |
| `Kcna2` | 0 | none |
| `Kcnq2` | 1 | not in the primary LGI1 complex; sparse channel counterexample |
| `Kcnq3` | 1 | not in the primary LGI1 complex; sparse channel counterexample |
| `Scn1a` | 1 | not in the primary LGI1 complex; sparse channel counterexample |
| `Scn2a` | 1 | not in the primary LGI1 complex; sparse channel counterexample |
| `Scn8a` | 1 | not in the primary LGI1 complex; sparse channel counterexample |
| `Cacna1a` | 0 | none |
| `Cacna1g` | 12 | detectable thalamic channel response, but mechanistically farther |

I ran a Distributed Agents runtime profile comparison for `Adam22` plus 23 represented
synaptic targets. The run wrote `lgi1_synaptic_compare.json` and reported 18/24
profiles with no significant features and 6/24 with only 1-9 significant
features. This confirmed that the local cohort is mostly flat in the exact
focal cell group. The continuous correlations among flat profiles were not used
to transfer a signed expression state because the leading log-fold-change tails
for `Adam22` were nonsignificant artifacts with FDR 1.0.

As a check on self-transcript detectability, I queried the measured `names ==
Lgi1` rows across all 1,674 observed perturbations in the focal cell group.
`Lgi1` was measured in all profiles and was significantly altered by four broad
regulatory perturbations, with adjusted p-values as low as 8.38e-4. That does
not leak the held-out knockout result, but it argues that `Lgi1` RNA is present
enough in this focal group that direct CRISPR-induced transcript loss could be
called, as it was for `Adam22` and several adhesion receptors.

## Target-specific biological reasoning

### `Lgi1`

LGI1 is a secreted antiepileptogenic ligand rather than an ion channel subunit.
Its closest direct loss-of-function analog in the training set is `Adam22`, one
of the receptors it bridges to `Adam23`. Fukata et al. showed that LGI1 forms an
extracellular ADAM22/ADAM23 trans-synaptic complex that organizes presynaptic
Kv1-family potassium channels with postsynaptic AMPAR scaffolds, and Ohkawa et
al. showed that blocking LGI1-ADAM22/23 reduces synaptic AMPAR clusters. The
best mechanistic transfer is therefore from `Adam22`, then from represented
Kv1/PSD/TARP/AMPAR neighbors as counterexamples.

`Adam22` had focal `n_degs = 1`, and that one row was `Adam22` itself. The
Distributed Agents corpus `Adam22:F003` and `Adam22:F004` findings state that `Adam22`
did not transcriptionally engage the expected AMPAR, MAGUK, TARP, Kv1,
immediate-early, ISR, or UPR modules; the represented direct complex or
receptor-subunit comparators did not phenocopy it, and `Lgi1`, `Adam23`, and
the other `Lgi` paralogs were absent as perturbation targets. The Distributed Agents
`Kcna1:F002` finding independently references the Kv1/LGI1 complex and reports
that represented `Kcna2`, `Kcnab2`, `Adam22`, and `Dlg4` surfaces were flat or
singleton-sized rather than a shared Kv1-like RNA module.

The AMPAR-side evidence points the same way. In the focal count table
`Gria1`, `Gria2`, `Gria3`, `Cacng2`, and `Cacng3` were all 0, while `Dlg4` was
only a self-transcript singleton. The high-confidence Distributed Agents AMPAR claim
`claim:a9367c3aeaad95bfae9c` summarizes the broader same-experiment pattern:
represented AMPAR-core and AMPAR-trafficking/scaffold perturbations were
transcriptionally buffered in basal juvenile neurons and did not form an
interchangeable AMPAR-loss nuclear RNA program.

The broader synaptic-adhesion counterexamples also argue against a large
response. `Nrxn1`, `Nlgn3`, and `Cadm2` were self-transcript singletons in the
focal group; `Nrxn2`, `Nrxn3`, `Lrrtm3`, `Lrrtm4`, `Il1rap`, `Il1rapl1`,
`Il1rapl2`, `Ptprd`, and `Ptprt` were zero. Distributed Agents
`claim:da426d57898fc5cde54d` and `claim:60396794c5493932dc07` generalize these
findings across represented neurexin/LRRTM/neuroligin/CADM/GluD and PSD
scaffold perturbations: local synapse and adhesion biology is often visible in
protein localization, spine, current, or circuit assays, but is usually off-axis
for this steady-state postnatal nuclear RNA assay.

This left a zero-versus-one decision. I predicted no downstream FDR-level
program for `Lgi1`, because the direct receptor `Adam22` and its Kv1/AMPAR/PSD
neighbors were flat after the same P16 sparse CRISPR modality. I nevertheless
predicted a nonzero count of exactly one because direct self-transcript loss is
the dominant event in the nearest nonzero training analogs: `Adam22`, `Dlg4`,
`Nrxn1`, `Nlgn3`, and `Cadm2` each contributed only their own mRNA in this focal
group. `Lgi1` mRNA was also detectable enough to be an FDR-level downstream row
under several unrelated regulatory perturbations, so a singleton `Lgi1` row is
more plausible than complete invisibility.

Final point prediction: `Lgi1 -> 1`.

## Limits and extrapolations

The strongest ligand-side tests were unavailable: `Lgi1`, `Lgi2`, `Lgi3`,
`Lgi4`, `Adam11`, and `Adam23` were not represented as training perturbations.
Thus the prediction extrapolates from `Adam22` and from downstream
Kv1/AMPAR/PSD neighbors rather than from another secreted LGI-family knockout.

The internal `Adam22` result is still an imperfect analog. LGI1 is secreted and
can act non-cell-autonomously, whereas this readout assigns perturbations to
single nuclei in a sparse mosaic. A secreted ligand can be buffered by LGI1
released from nearby unedited cells, which would make the downstream program
even flatter than a cell-autonomous receptor perturbation but says little about
protein-level synaptic rescue.

The assay was basal snRNA-seq, not electrophysiology, AMPAR/Kv1 localization,
or seizure monitoring. Fukata 2010 and Ohkawa 2013 make LGI1 a compelling
synaptic and epilepsy gene, but the training data show that such local synaptic
protein phenotypes frequently leave few or no FDR-level nuclear RNA changes in
this P16-to-P37/P44 Perturb-seq design.

Finally, the direct target transcript is only a probabilistic anchor. The hidden
`Lgi1` guides could have lower editing, a different number of recovered edited
nuclei, or a lower baseline detection rate than `Adam22`; any of those would
collapse the predicted singleton to zero. I therefore put the response at the
minimal nonzero value rather than borrowing counts from broader excitability or
channel perturbations such as `Cacna1g`.
