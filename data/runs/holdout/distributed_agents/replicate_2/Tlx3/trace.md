# Trace

## Question and resolved scope

The held-out target set for this run contains one gene, `Tlx3`, from
`241_Tlx3.csv`. I predicted the focal endpoint
`n_degs = count(pvals_adj < 0.05)` in `151 TH Prkcd Grin2c Glut` after the
P16-to-P37/P44 sparse AAV CRISPR loss-of-function perturbation. `Tlx3` is absent
from both supplied training inputs, so I treated all `Tlx3` counts and
signatures as unobserved and transferred from represented genes.

I interpreted `151 TH` as an Allen-derived thalamic glutamatergic class, not
tyrosine-hydroxylase neurons. I also treated a flat target-transcript row in
analog perturbations as QC context only, not as a failed knockout call, because
the experiment uses mosaic indel-producing CRISPR.

## Sources used

- Supplied focal training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Supplied DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
  I used parquet metadata to localize the focal stripes and the Distributed Agents
  runtime profile tool to compare focal-cell signed Wilcoxon `scores` for
  selected represented targets with `pvals_adj < 0.05` as the significant-feature
  threshold.
- Distributed Agents corpus `perturbai-july-260713-sourceguard-1773-v1`, a curated
  same-experiment interpretation layer over the Perturb-seq DE tables.
- NCBI PubMed E-utilities for external developmental and thalamic literature.

## Dataset computations

The focal count CSV has 1,674 non-held-out targets; 469 have a nonzero 151 TH
count, the median is 0, the 75th percentile is 1, and the largest responses are
rare outliers. I therefore did not convert "transcription factor" status into
an automatic nonzero call.

The relevant represented focal counts were:

| training target | focal `n_degs` | reason for comparison |
| --- | ---: | --- |
| `Lbx1` | 1 | closest represented dorsal-spinal partner of Tlx3; both act in the spinal excitatory/inhibitory selector network |
| `Ptf1a` | 0 | opposing dorsal-horn inhibitory selector; Tlx3-positive excitatory neurons expand in `Ptf1a` mutants |
| `Lmx1b` | 0 | Tlx3 co-expressed excitatory neuronal factor in dorsal horn/brainstem sensory nuclei |
| `Pax2` | 0 | inhibitory fate comparator in the same embryonic dorsal-spinal switch |
| `Pax8` | 0 | Pax-family developmental comparator from the same postnatal flat network |
| `Atoh1`, `Neurod1`, `Neurod2`, `Neurog3` | 0 each | represented proneural/bHLH developmental comparators; none produced a 151 TH response |
| `Hoxa1`, `Hoxa13`, `Hoxa3`, `Hoxb8`, `Hoxd10`, `Hoxd13` | 0 each | represented homeobox developmental controls |
| `Tcf7l2` | 106 | a real maintained thalamic transcription-factor response and Wnt/TCF counterexample |
| `Rora` | 278 | a real maintained ROR alpha thalamic terminal-state response and nuclear-receptor counterexample |
| `Ctnnb1` | 383 | beta-catenin/Wnt positive control that converges with `Tcf7l2`, not with the Tlx3 analogs |

I then ran a focal profile comparison for
`Lbx1`, `Lmx1b`, `Ptf1a`, `Pax2`, `Tcf7l2`, `Rora`, and `Ctnnb1`, using each
training target's 17,259-gene Wilcoxon-score vector in
`151 TH Prkcd Grin2c Glut`.

Key profile observations:

- `Lbx1` had one significant 151 TH feature: `Vps35l` down
  (`score = -4.709`, `pvals_adj = 0.0430`).
- `Lmx1b`, `Ptf1a`, and `Pax2` each had 0 significant 151 TH features.
- Direct-developmental pair similarities were near zero: `Lbx1` vs `Lmx1b`
  cosine `-0.0009`, `Lbx1` vs `Ptf1a` `0.0106`, `Lbx1` vs `Pax2` `0.0375`,
  and `Lmx1b` vs `Ptf1a` `-0.0076`.
- The direct Tlx3 analog lane had no significant overlap with the broad thalamic
  TCF/Wnt or ROR programs: `Lbx1` shared 0 significant genes with `Tcf7l2`,
  `Rora`, or `Ctnnb1`; `Lmx1b`, `Ptf1a`, and `Pax2` had no significant genes to
  share.
- In contrast, the thalamic counterexample module is visible in the same focal
  matrix: `Tcf7l2` shared 40 same-direction FDR<0.05 genes with `Ctnnb1`
  in 151 TH. This makes a simple "homeobox and developmental TFs cannot be
  detected in this screen" explanation too strong; the better boundary is
  target and cell-state specificity.

The Distributed Agents corpus added broader same-experiment context:

- `Lbx1` produced exactly one robust downstream DEG across 22 measured neuronal
  groups, and its `Vps35l` event in 151 TH was not a reconstitution of the
  textbook dorsal-spinal `Lbx1`/`Ptf1a`/`Pax2` module; `Ptf1a`, `Pax2`, `Pax8`,
  and `Phox2b` did not respond in the 151 comparison.
- `Ptf1a` had no FDR<0.10 downstream genes in any of the 23 recovered neuronal
  groups; the represented PTF1/bHLH relatives did not expose a hidden postnatal
  neuronal module.
- `Lmx1b` was a pan-taxonomy transcriptional null at FDR<0.10 and did not
  converge with represented midbrain-dopamine network perturbations.
- `Pax2` had only a single weak FDR<0.10 event outside 151 and no canonical
  Pax/Otx/En/Gata/Lbx developmental signature.
- `Tcf7l2` and `Rora` were explicitly broad in 151 TH, but the corpus assigns
  them to maintained thalamic TCF/beta-catenin and ROR alpha terminal-state
  programs, not to dorsal-spinal Tlx/Lbx fate selection.

## Tlx3-specific biological reasoning

`Tlx3` is a homeobox selector for glutamatergic rather than GABAergic fate in
embryonic dorsal spinal cord. `Ptf1a` is required for GABAergic over
glutamatergic dorsal-horn fate, and `Ptf1a` loss transfates inhibitory
precursors toward `Lmx1b+;Tlx3+` excitatory neurons in mouse embryos
(Glasgow et al. 2005, doi:10.1242/dev.02167, PMID:16291784).
`Gsh1/2` and `Ascl1` regulate `Tlx3` during sensory interneuron specification
(Mizuguchi et al. 2006, doi:10.1038/nn1706, PMID:16715081). In dorsal spinal
cord, Tlx1/3 and Ptf1a also control different receptor gene batteries in
glutamatergic and GABAergic neurons (Guo et al. 2012,
doi:10.1523/JNEUROSCI.6301-11.2012, PMID:22723691), and ChIP/expression work
showed that Tlx3 directly activates many excitatory dILB genes while repressing
alternative inhibitory dILA genes (Monteiro et al. 2021,
doi:10.3389/fcell.2021.642697, PMID:33996801). Outside the spinal cord, Tlx3
combines with Runx1 during nociceptor, thermoceptor, and pruriceptor
development in dorsal-root ganglia (Lopes et al. 2012,
doi:10.1523/JNEUROSCI.1109-12.2012, PMID:22787056), and Lmx1b/Tlx3
co-expression persists in postnatal parabrachial, solitary-tract, and dorsal
horn excitatory neurons (Dai et al. 2008, doi:10.1002/cne.21759,
PMID:18512225).

Those priors predict a spinal/caudal sensory developmental circuit, not a broad
acute thalamic circuit in P37-P44 neurons. The represented genes most likely to
stand in for that biology are therefore `Lbx1`, `Ptf1a`, `Lmx1b`, and `Pax2`,
and all were zero or one-gene in 151 TH. The one `Lbx1` hit was `Vps35l`, not
`Slc17a6`, `Slc17a7`, `Gad1`, `Gad2`, `Lmx1b`, `Pax2`, receptor genes from the
Tlx/Ptf dorsal-horn literature, or any larger transmitter-fate module.

The broad 151 TH responses to `Rora`, `Tcf7l2`, and `Ctnnb1` are useful
counterexamples but not positive analogs. TCF7L2 is a thalamic terminal
selector/Wnt effector with postnatal thalamic ion-channel and synaptic targets
(Lee et al. 2017, doi:10.1016/j.ydbio.2017.02.010, PMID:28219675; Lipiec et al.
2020, doi:10.1242/dev.190181, PMID:32675279; Nagalski et al. 2012,
doi:10.1007/s00429-012-0474-6, PMID:23152144). ROR alpha has a postnatal,
cell-autonomous thalamic role in thalamocortical maturation (Vitalis et al.
2018, doi:10.1093/cercor/bhx262, PMID:29040410). Their strong counts show that
this cell group can report maintained transcription-factor biology, but they
also sharpen the negative inference for Tlx3: when a regulator owns a maintained
151 TH program, the training matrix and corpus recover a coherent signature.
The Tlx3-neighbor developmental network did not.

## Prediction

For `Tlx3`, I therefore predict `0` DEGs at BH-adjusted Wilcoxon FDR<0.05 in
`151 TH Prkcd Grin2c Glut`.

The decision is driven mainly by within-dataset evidence from `Lbx1 = 1`,
`Ptf1a = 0`, `Lmx1b = 0`, `Pax2 = 0`, the many additional zero homeobox/bHLH
developmental comparators, and the absence of profile overlap between these
targets and the real thalamic `Tcf7l2`/`Rora`/`Ctnnb1` responses. External
literature supplies the mapping from Tlx3 to the dorsal-spinal sensory
selector network and argues that it is a developmental, lineage-restricted
program rather than a generic thalamic maintenance factor.

## Limits

- `Tlx1` and `Tlx2`, the most direct Tlx-family paralogs, were not represented
  in the focal training-count table, so the comparison relies on pathway
  partners rather than a paralog knockout.
- The DE parquet does not provide absolute baseline expression; I did not use
  adult Tlx3 expression in the focal cell group as a quantitative feature.
- The `Lbx1` comparator is sparse rather than perfectly null. A one-gene
  `Tlx3` response is possible, but the task requires a point prediction and the
  best estimate rounds down to zero because none of the canonical Tlx genes
  appear in the Lbx1/Ptf1a/Lmx1b/Pax2 signatures.
- P16 sparse CRISPR cannot test embryonic cell-fate conversion or cell-abundance
  effects that would have happened before the assay; the prediction is only for
  the within-surviving-nucleus RNA endpoint requested here.
- The Distributed Agents corpus is derived from the same experiment, so it is
  interpretation and calibration evidence rather than independent replication.
