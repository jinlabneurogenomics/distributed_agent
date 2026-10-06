# Question and setup

The requested held-out target was `Slitrk1`, from
`212_Slitrk1.csv`. I interpreted `n_degs` exactly as the focal-cell endpoint
used in the training count CSV: the number of measured genes with
`pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut`, counting the target
transcript itself when it is a measured, FDR-significant row.

The main ambiguity was whether to count a possible Slitrk1 self-transcript
drop as a positive effect. Several one-DEG training perturbations in this
neighborhood are self-only target RNA calls, whereas several similarly
surface/synaptic genes are zero even though their own transcript is measured.
I therefore treated "target self knockdown reaches FDR" and "the perturbation
drives a downstream cell-state program" as separate questions.

# Sources

Within-run data:

- Held-out manifest:
  `[local file: 212_Slitrk1.csv]`
- Focal-cell training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`

Internal same-experiment knowledge layer:

- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`.
  There was no direct `Slitrk1` target record, as expected for a held-out
  perturbation. I used corpus claims and target records for represented
  synaptic-adhesion neighbors including `Lrrtm3`, `Ptprd`, `Il1rapl1`,
  `Nrxn2`, and `Nlgn3`.
- I also ran a run-local profile comparison over focal-cell expression
  signatures for the candidate analogs
  `Ptprd, Il1rapl1, Il1rapl2, Lrrtm1, Lrrtm3, Lrrtm4, Nrxn1, Nrxn2, Nrxn3,
  Nlgn3, Cadm2, Grid2, Dlg4, Dlgap4, Homer2, Shank2, Shank3`.

External literature, via PubMed, used only to justify biological proximity:

- Yim et al. 2013, PNAS, DOI `10.1073/pnas.1209881110`, PMID `23345436`:
  Slitrk family proteins organize excitatory and inhibitory synapses through
  LAR receptor protein tyrosine phosphatases.
- Um et al. 2014, Nature Communications, DOI `10.1038/ncomms6423`, PMID
  `25394468`: structural basis for LAR-RPTP/Slitrk adhesion, including
  Slitrk1.
- Beaubien et al. 2016, Scientific Reports, DOI `10.1038/srep27343`, PMID
  `27273464`: Slitrk1 localizes to excitatory synapses and Slitrk1 reduction
  lowers excitatory synapse number in hippocampal neurons.
- Kang et al. 2016, Frontiers in Molecular Neuroscience, DOI
  `10.3389/fnmol.2016.00104`, PMID `27812321`: neuropsychiatric Slitrk1 and
  Slitrk-family missense variants can impair trafficking, PTPdelta binding,
  and synapse-inducing activity.
- Takahashi and Craig 2013, Trends in Neurosciences, DOI
  `10.1016/j.tins.2013.06.002`, PMID `23835198`: type-IIa receptor PTPs are
  presynaptic hubs for synapse organization.
- Schroeder et al. 2018, Neuron, DOI `10.1016/j.neuron.2018.06.026`, PMID
  `29983322`: LRR synaptic adhesion proteins, including Slitrk1 and LRRTM1,
  regulate input-specific excitatory synapse architecture.

# Computations over the training data

1. Loaded the manifest and found exactly one requested target, `Slitrk1`.
2. Loaded the focal-cell training count CSV. It has 1,674 non-held-out
   perturbations; 469 have nonzero `n_degs`, the median is 0, the 75th
   percentile is 1, and the 95th percentile is 18. This makes a zero or
   self-only response the local prior for genes without a strong transcriptional
   role.
3. Filtered the focal-cell parquet rows to literature- and corpus-nominated
   synaptic adhesion, receptor-PTP, neurexin/neuroligin/LRRTM, and PSD
   comparators. For each candidate I counted `pvals_adj < 0.05`, listed the
   significant genes, and inspected the row where `names == gene_target` to
   separate target self-RNA calls from downstream markers.
4. Queried whether Slitrk-family transcripts were measured in the focal group.
   `Slitrk1` through `Slitrk6`, `Ptprs`, and `Lrrc4b` are present as measured
   features, but none of those genes is a represented perturbation target.
   Thus a Slitrk1 self call is technically possible, but no exact Slitrk or
   PTPsigma perturbation calibrates its guide-specific transcript drop.
5. Compared the exact analog cohort profiles in the focal cell group. Ten of
   17 analogs had no FDR 0.05 features; the remainder had only 1-3 features.
   The pairwise significant-feature intersections were zero in the inspected
   core comparisons, so the cohort does not define a reusable signed multi-gene
   module.

# Slitrk1-specific analogs

| Training perturbation(s) | Focal `n_degs` | Expression evidence | Why relevant for Slitrk1 |
| --- | ---: | --- | --- |
| `Ptprd` | 0 | No focal FDR genes; the target row was weak and nonsignificant. | PTPdelta is the represented LAR-RPTP closest to the Slitrk adhesion machinery. The Distributed Agents `Ptprd:F002` finding reports that measured Ptprd relatives, including `Ptprf`, `Ptprm`, `Ptprt`, `Il1rapl1`, `Il1rapl2`, `Ntrk3`, and neurexin/neuroligin comparators, were flat, null, or singleton responders rather than a coherent FDR module. `Ptprs`, the PTPsigma paralog used by several Slitrk proteins for excitatory synaptogenesis, was not itself a training perturbation. |
| `Il1rap`, `Il1rapl1`, `Il1rapl2` | 0, 0, 0 | All were zero in `151 TH Prkcd Grin2c Glut`. | IL1RAPL proteins are postsynaptic organizers that also use PTPdelta-like receptor PTPs. The Distributed Agents high-confidence claim `claim:fea40917ad49d48e4705` says the represented IL1RAP/IL1RAPL/PTPdelta axis is not expressed as a shared postnatal neuronal mRNA module. This is a strong local counterexample to assuming a trans-synaptic adhesion protein will drive many nuclear DEGs. |
| `Lrrtm1`, `Lrrtm3`, `Lrrtm4` | 1, 0, 0 | `Lrrtm1` had only `R3hdm2` significant in the focal group; `Lrrtm3` and `Lrrtm4` had no focal DEGs, and neither had its own transcript significant. | LRRTMs are LRR postsynaptic adhesion genes, biologically close in cellular function though not paralogous to Slitrk1. Distributed Agents `Lrrtm3:F002` reports no hidden LRRTM-neurexin transcriptomic phenocopy among directly queryable paralogs and receptor-side comparators. |
| `Nrxn1`, `Nrxn2`, `Nrxn3`, `Nlgn3`, `Cadm2`, `Grid2` | 1, 0, 0, 1, 1, 0 | `Nrxn1`, `Nlgn3`, and `Cadm2` were self-transcript-only positives; `Nrxn2`, `Nrxn3`, and `Grid2` were zero. | These are alternative extracellular synaptic adhesion or ligand-side systems. Distributed Agents `claim:da426d57898fc5cde54d` summarizes the same-experiment result: represented neurexin, neuroligin, LRRTM, GluD, CADM, contactin-associated, and scaffold-near perturbations were mostly flat, singleton, or non-overlapping despite obvious synaptic relationships. |
| `Dlg4`, `Dlgap4`, `Homer2`, `Lrrc7`, `Shank2`, `Shank3` | 1, 2, 0, 0, 0, 2 | `Dlg4` was self-only; `Dlgap4` had target plus `Vgf`; `Shank3` had target plus `Uba5`; the rest were zero. | These are postsynaptic density/scaffold comparators. They show that even perturbing prominent postsynaptic structural genes generally stays below a broad steady-state RNA threshold in this P16/postmitotic assay. |
| `Ntrk2`, `Ntrk3` | 3, 0 | `Ntrk2` had target, `Atp2a2`, and `Vgf`; `Ntrk3` was zero. | Slitrks are "Slit and Trk-like" by domain architecture, not Trk receptors. The contrast helps bound the name-level analogy: an enzymatic TrkB receptor can produce a small focal response, but Ntrk3 is silent and Trk signaling is not the core Slitrk1 mechanism. |

# Biological interpretation

Slitrk1 is a neuronal transmembrane LRR protein concentrated at excitatory
postsynaptic sites. Slitrk-family proteins bind presynaptic type-IIa LAR-RPTPs
through extracellular LRR domains and organize synapse formation through local
adhesion and clustering. That makes `Ptprd` and the unrepresented `Ptprs`
mechanistically closer than transcription factors or generic neuronal disease
genes; `Lrrtm*`, `Nrxn*`, `Nlgn3`, `Cadm2`, and PSD scaffolds are useful
counterexamples because they perturb comparable extracellular or postsynaptic
synaptic architecture without producing a broad nuclear signature in this
dataset.

The same-experiment evidence was predominantly negative. In the focal group,
the strongest Slitrk1-neighbor perturbations were zero or target-only
singletons. The local corpus independently summarized the broader same-assay
surfaces as absence of a shared IL1RAP/IL1RAPL/PTPdelta module, absence of a
shared receptor-PTP module, and buffering of represented neurexin/neuroligin/
LRRTM/GluD/CADM/PSD-near perturbations at the postnatal snRNA level. This
matches the external biology: Slitrk1 loss is expected to affect synapse
number, input specificity, receptor localization, or electrophysiology more
than it is expected to acutely rewrite thousands of somatic mRNAs in sparse
postmitotic neurons.

I therefore predict that acute mosaic P16 CRISPR loss of `Slitrk1` will not
cross the FDR 0.05 threshold for a downstream transcriptional state in
`151 TH Prkcd Grin2c Glut`. Because no represented Slitrk paralog calibrates
self-transcript detection, and because the nearest LRR adhesion targets
`Lrrtm3` and `Lrrtm4` were zero rather than self-only in this focal cell group,
I also chose the conservative target-count decision: `Slitrk1` is predicted to
remain at zero significant genes rather than a one-gene self-only call.

# Limits

The prediction extrapolates from adjacent synaptic adhesion systems, not from
an exact Slitrk paralog or PTPsigma perturbation: `Slitrk1-6`, `Ptprs`, and
`Lrrc4b` were not training perturbations. The assay did not measure indels,
SLITRK1 protein, LAR-RPTP binding, synapse number, receptor currents, or
behavior, so a zero-DEG prediction should not be read as a prediction of no
synaptic phenotype. The endpoint is also powered by 10x nuclear detection and
target-specific guide efficacy; if the hidden Slitrk1 guide set happened to
produce a strong nonsense-mediated target RNA drop, the observed answer could
be a one-DEG self-transcript signature even in the absence of downstream
biology.

# Final point prediction

`Slitrk1`: 0 DEGs.
