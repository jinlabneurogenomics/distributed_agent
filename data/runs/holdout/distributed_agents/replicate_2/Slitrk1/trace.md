# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and interpretation

The held-out manifest contains one target, `Slitrk1`. I interpreted the endpoint
as the exact count, in `151 TH Prkcd Grin2c Glut` neurons, of measured genes with
`pvals_adj < 0.05` in the perturbation-vs-control Wilcoxon test. I counted the
target transcript itself as eligible for this endpoint when it would have passed
FDR, because the supplied training count table does the same.

`Slitrk1` was completely held out, so neither its focal DEG count nor any
`Slitrk1` perturbation signature was available for transfer.

## Sources

- Training endpoint: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Training DE statistics: `[local file: training_de_all_cell_groups.parquet]`.
- Requested targets: `[local file: 212_Slitrk1.csv]`.
- Internal semantic layer: Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`. This release had no `Slitrk1` target-context entry, but it did contain Ptprd, Il1rapl1, Lrrtm3/Lrrtm4, Nrxn1, and Lrfn2 Findings that summarize same-experiment synaptic-adhesion comparisons.
- Same-experiment profile tooling: Distributed Agents runtime `profile_compare` and `profile_cohort` over a manually nominated focal synaptic-adhesion cohort.
- External literature found through PubMed:
  - Yim et al. 2013, PNAS, DOI `10.1073/pnas.1209881110`, PMID `23345436`.
  - Um et al. 2014, Nature Communications, DOI `10.1038/ncomms6423`, PMID `25394468`.
  - Beaubien et al. 2016, Scientific Reports, DOI `10.1038/srep27343`, PMID `27273464`.
  - Valnegri et al. 2011, Human Molecular Genetics, DOI `10.1093/hmg/ddr418`, PMID `21926414`.
  - Takahashi et al. 2012, Nature Neuroscience, DOI `10.1038/nn.3040`, PMID `22286174`.
  - Takahashi and Craig 2013, Trends in Neurosciences, DOI `10.1016/j.tins.2013.06.002`, PMID `23835198`.
  - Han et al. 2018, Journal of Neuroscience, DOI `10.1523/JNEUROSCI.0672-18.2018`, PMID `29934346`.

## Computational checks

The focal training table contained 1,674 non-held-out biological targets. Its
counts were highly concentrated at zero: 1,205/1,674 had no DEG, the median was
0, the 75th percentile was 1, and only 5% of training targets exceeded 18 DEGs.

For the mechanistically nominated Slitrk1-neighborhood genes, I queried only
`group_name = '151 TH Prkcd Grin2c Glut'` from the DE Parquet and then summed
`pvals_adj < 0.05` by `gene_target`. The focal Parquet slice had 17,259 measured
features per queried target. I also pulled the actual focal FDR genes so that a
count of 1 caused by guide-visible self-depletion was not mistaken for a broad
downstream state.

The same 32-gene cohort was passed to Distributed Agents runtime `profile_compare`. In
the focal cell group, 19/32 analogs had no FDR-significant feature and the other
13 had only one or two. The comparison did not reveal a shared multi-gene FDR
module among the LAR-RPTP, IL1RAPL, LRRTM, neurexin/neuroligin, postsynaptic
scaffold, latrophilin/FLRT/UNC5, or teneurin comparators.

## Biological comparison for `Slitrk1`

Slitrk1 is a postsynaptic leucine-rich repeat adhesion molecule. SLITRK family
proteins bind presynaptic type IIa/LAR receptor tyrosine phosphatases to promote
synapse organization; Slitrk1 is itself localized to excitatory synapses and
Slitrk1 reduction in hippocampal culture reduces excitatory synapse number
(Yim 2013; Um 2014; Beaubien 2016). PTPdelta, PTPsigma, and LAR act as hub
presynaptic receptors for this and related postsynaptic adhesion codes
(Takahashi and Craig 2013; Han 2018).

The closest exact controls had important gaps: `Slitrk2`-`Slitrk6` were not in
the training count table, and `Ptprs`, the PTPsigma receptor that is prominent
for excitatory Slitrk signaling, was also absent. I therefore used receptor-side
LAR-RPTPs, PTPdelta partners, and the broader synaptic adhesion machinery as
imperfect but assay-matched analogs.

| Training perturbation | Focal `n_degs` | FDR genes in `151 TH Prkcd Grin2c Glut` | Why it was relevant |
|---|---:|---|---|
| `Ptprd` | 0 | none | Direct PTPdelta/LAR-RPTP side of the Slitrk and IL1RAPL trans-synaptic network. The Distributed Agents Ptprd Finding also reports no shared FDR module across represented LAR-RPTP and synaptic-adhesion relatives. |
| `Ptprf` | 0 | none | LAR paralog of Ptprd/Ptprs; no focal response and no Ptprd-like transcriptional state. |
| `Ptprt` | 0 | none | Receptor-PTP family boundary; corpus Ptprt/Ptprd claims describe represented receptor-PTPs as flat or singleton responders rather than a coherent neuronal RNA module. |
| `Ptprm` | 1 | `Ptprm` down | Type IIB receptor-PTP counterexample; the one focal hit was its own transcript. |
| `Il1rapl1` | 0 | none | Postsynaptic PTPdelta-binding organizer of excitatory synapses; a same-receptor analog to Slitrks (Valnegri 2011). |
| `Il1rapl2` | 0 | none | Il1rapl1 paralog and PTPdelta binder; focal null. |
| `Lrrtm1` | 1 | `R3hdm2` up | LRRTM/neurexin synaptic adhesion family; the only focal hit was an isolated non-recurrent transcript. |
| `Lrrtm3` | 0 | none | LRRTM family member; Distributed Agents calls it pan-measured FDR-null and non-convergent with LRRTM/neurexin comparators. |
| `Lrrtm4` | 0 | none | LRRTM family member; corpus evidence shows it did not recruit the expected neurexin/HSPG/AMPAR RNA program. |
| `Nrxn1` | 1 | `Nrxn1` down | Core presynaptic adhesion hub. The single focal hit was self-target depletion. |
| `Nrxn2` | 0 | none | Neurexin family analog; focal null. |
| `Nrxn3` | 0 | none | Neurexin family analog; focal null. |
| `Nlgn3` | 1 | `Nlgn3` down | Postsynaptic neurexin ligand; the only focal hit was self-target depletion. |
| `Ntrk3` | 0 | none | Postsynaptic LAR-RPTP ligand in the TrkC/PTPsigma branch; focal null. |
| `Lrfn2` | 0 | none | SALM postsynaptic organizer near PSD/NMDAR biology; no focal response. |
| `Dlg4` | 1 | `Dlg4` down | PSD-95 scaffold; singleton self-depletion and no Slitrk-like downstream program. |
| `Shank2` | 0 | none | PSD scaffold boundary; focal null. |
| `Shank3` | 2 | `Shank3` down, `Uba5` up | PSD scaffold boundary; only two focal hits, one being self. |
| `Cadm2` | 1 | `Cadm2` down | Synaptic adhesion comparator used as a broader CAM boundary; singleton self-depletion. |
| `Grid1` | 1 | `Grid1` down | GluD receptor adhesion/scaffold comparator; singleton self-depletion. |
| `Grid2` | 0 | none | GluD receptor comparator; focal null. |
| `Gria1` | 0 | none | AMPAR subunit downstream of several synaptic organizers; focal null. |
| `Gria2` | 0 | none | AMPAR subunit boundary; focal null. |
| `Flrt3` | 0 | none | LRR adhesion/guidance molecule in the latrophilin/UNC5 axis; focal null and non-convergent in the Distributed Agents Flrt3 comparison. |
| `Adgrl1` | 1 | `Adgrl1` down | Latrophilin adhesion receptor; singleton self-depletion. |
| `Adgrl2` | 1 | `Adgrl2` down | Latrophilin paralog; singleton self-depletion. |
| `Adgrl3` | 1 | `Adgrl3` down | Latrophilin paralog; singleton self-depletion. |
| `Unc5c` | 1 | `Unc5c` down | FLRT/UNC5 guidance partner; singleton self-depletion. |
| `Unc5d` | 0 | none | UNC5 paralog; focal null. |
| `Tenm3` | 1 | `Tenm3` down | Teneurin synaptic adhesion family; singleton self-depletion. |
| `Tenm4` | 0 | none | Teneurin paralog; focal null. |
| `Dcc` | 0 | none | Axon guidance/adhesion boundary; focal null. |

This set puts Slitrk1 into the quietest part of the focal calibration. Across
these 32 perturbations the total number of focal FDR genes was only 14; 12 of
the 14 were the perturbed gene itself, and only two focal downstream genes
remained after ignoring self-depletion. Even the direct Slitrk receptor-side
perturbations `Ptprd` and `Ptprf` were 0 in the focal cell type.

There are stronger transcriptional responses elsewhere in synaptic biology:
for example `Grin1` had 89 focal DEGs. I treated those as counterexamples rather
than analogs. An acute loss of an NMDAR pore-forming subunit can directly alter
calcium-dependent transcription, whereas Slitrk1 is an extracellular adhesion
organizer whose best-characterized readouts are presynaptic differentiation,
synapse density, and circuit physiology. In this training set, perturbing
adhesion molecules, receptor PTP partners, PSD scaffolds, or AMPAR/GluD
receptor-near controls did not mimic the broad `Grin1` state.

## Prediction

I predict that `Slitrk1` loss will not yield an FDR-resolved focal nuclear RNA
response. The nonzero alternative would be a single FDR hit from direct
`Slitrk1` mRNA depletion, because isolated self-depletion was visible for some
surface and scaffold genes in the same focal class. I still chose zero because
many equally relevant PTPdelta/LAR-RPTP and LRR adhesion genes had no focal
self-hit or downstream hit, `Slitrk1` was in the measured feature universe but
not perturbed in training, and the Distributed Agents/PubMed evidence points to a
structural synapse organizer rather than to a cell-autonomous transcription
factor, splicing factor, or proteostasis regulator.

Final point prediction: `Slitrk1` -> `0`.

## Limits

- Exact `Slitrk` paralog perturbations and `Ptprs` were held out or absent from
  the training endpoint, so the closest possible in-family transfer was not
  available.
- The external Slitrk1 literature is mostly culture, hippocampus, germline or
  early-developmental synapse biology. It does not directly assay a sparse P16
  CRISPR loss in thalamic `Prkcd`/`Grin2c` glutamatergic neurons.
- The Parquet contains DE statistics, not raw expression, protein abundance,
  indel rates, spine counts, or synaptic physiology. A zero DEG prediction is
  therefore only a prediction about the FDR-level nuclear RNA endpoint.
- If `Slitrk1` happens to be expressed highly enough in the focal thalamic
  class for CRISPR-mediated transcript depletion to pass BH correction, the
  true count could be 1 even without a downstream program.
