# Prediction task

I interpreted the task as a scalar hold-out prediction: for each requested
perturbation, predict the number of genes that would pass BH-adjusted Wilcoxon
FDR < 0.05 in `151 TH Prkcd Grin2c Glut` after the same P16 AAV-CRISPR,
P37-P44 NeuN+ snRNA-seq experiment. The endpoint is directly observed for
training perturbations in the supplied CSV, but `Zfp398` was withheld from both
the focal DEG-count table and the all-cell differential-expression Parquet.

There was one requested target, and I preserved the requested CSV order:

| target_name |
|---|
| Zfp398 |

# Sources used

- Declared PerturbAI training DEG-count table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared PerturbAI all-cell differential-expression Parquet:
  `training differential-expression dataset`.
- Run-local requested-target manifest:
  `single-target request for Zfp398`.
- Internal same-experiment interpretation corpus:
  PerturbAI July 260713 sourceguard 1773 v1, queried through the run-declared
  `corpus.calibration`, `corpus.findings`, and `corpus.report_evidence` style
  entrypoints. The corpus is a packaged interpretation of the same screen, not
  independent replication.
- External literature from PubMed for `Zfp398`/human `ZNF398`/`ZER6` and for
  the nearest visible SCAN-domain comparator `Zfp397`/human `ZNF397`.

# Dataset checks and computations

The requested manifest contained exactly one target, `Zfp398`. The visible
training set contained 1,674 unique perturbations in the focal-cell DEG-count
CSV. The empirical count distribution was highly zero-inflated: 1,205/1,674
visible perturbations had `n_degs = 0`, the median count was 0, the 75th
percentile was 1, the 90th percentile was 2, and the 95th percentile was 18.
This makes a zero or single-digit prediction the prior for an unannotated,
non-core zinc-finger transcription factor unless a close measured analog shows
a reproducible response in the focal thalamic cells.

I then queried the Parquet only for the focal group and visible perturbations
that were plausible analogs or counterexamples:

| visible target | focal `n_degs`, FDR<0.05 | reason for checking |
|---|---:|---|
| `Zfp397` | 0 | closest useful SCAN/C2H2 zinc-finger comparator represented in the experiment |
| `Zfp236` | 19 | KRAB-like zinc-finger factor with a weak focal-cell response |
| `Zfp148` | 8 | zinc-finger transcription factor with a sparse thalamus-only response |
| `Zfp423` | 150 | high-count zinc-finger developmental regulator, used as a counterexample |
| `Zbtb7a` | 841 | very high-count zinc-finger/BTB factor, used as a counterexample |
| `Yy1` | 720 | high-count zinc-finger transcription factor, used as a counterexample |
| `Thap11` | 478 | high-count DNA-binding factor, used as a counterexample |

`Zfp398` was absent as a `gene_target` in the Parquet, as expected. For the
closest visible anchors, the actual focal FDR<0.05 rows were:

- `Zfp397`: 0 genes.
- `Zfp148`: 8 genes, mostly a small down-regulated RNA/synaptic set
  (`Srrm2`, `Ypel4`, `Cacnb3`, `Plekhj1`, `Srsf9`, `Slitrk5`, `Ptprn`,
  `Rasgrp2`).
- `Zfp236`: 19 genes, led by `Ogt`, `Eif4a2`, `Gdi1`, `Phip`, `Cpt1c`,
  `Snrnp70`, `Kmt5b`, `Rreb1`, and `Ache`.

The internal corpus reported that visible `Zfp397` was a pan-neuronal null in
the same assay: it was recovered in 22 of 23 taxonomy groups and no measured
group had a downstream gene at FDR < 0.10. Its SCAN-family comparators
`Zkscan1` and `Zscan26` were also flat, while `Zkscan16` produced only two
isolated downstream events. The same corpus called `Zfp148` a sparse,
151-restricted response and `Zfp236` a weak, cell-state-limited
nutrient/translation response. Those target-specific surfaces were more
relevant than pooling all C2H2 or all zinc-finger perturbations, because the
high-count examples had distinct mechanisms: `Zbtb7a` rewired endomembrane,
lysosome, synaptic, and neurosecretory programs; `Zfp423` affected a
ZFP423/OAZ developmental cell-state and surface/glycoprotein program; `Thap11`
was much broader and dominated by replication and mitochondrial/proteostasis
features.

# Target-specific prediction

## Zfp398

`Zfp398`, also called `ZER6`/human `ZNF398`, encodes a C2H2 zinc-finger
transcription factor with a KRAB-containing p52 isoform and a longer p71
isoform. Conroy et al. cloned the isoforms and showed that they can bind DNA
and regulate a reporter, with isoform-specific repression by estrogen receptor
alpha through p52-ZER6 (Conroy et al., 2002, JBC, DOI
`10.1074/jbc.M107702200`, PMID 11779858). This supports the *modality* that a
loss-of-function could in principle have a transcriptional readout in snRNA-seq.
It does not identify a thalamic juvenile-neuron regulon.

The best direct within-dataset analog was not one of the famous broad zinc
finger factors, but `Zfp397`. The `Zfp397` perturbation was a complete focal
null in the training labels (`n_degs = 0`) and a null across the postmitotic
neuronal surface in the packaged PerturbAI report. `Zfp397` is not an obligate
partner of `Zfp398`, but it is a better calibration point than `Zfp423`,
`Zbtb7a`, `Yy1`, or `Thap11`: it is a narrow C2H2/SCAN zinc-finger factor
rather than an OAZ, BTB/POZ, YY1-complex, or THAP11 network hub. The external
ZNF397 literature likewise described a SCAN zinc-finger transcriptional
regulator and found mouse `Zfp397` to be non-essential in a knockout setting
(Wu et al., 2003, Gene, DOI `10.1016/s0378-1119(03)00551-1`, PMID 12801647;
Bailey et al., 2008, Chromosoma, DOI `10.1007/s00412-008-0155-7`, PMID
18369653).

`Zfp236` and `Zfp148` were small positive counterexamples. `Zfp236` had 19
focal DEGs and a coherent `Ogt`/`Eif4a2`/`Cpt1c` response, but the internal
report tied that response to a glucose and hexosamine-biosynthetic context
rather than to a generic KRAB-zinc-finger module. `Zfp148` had 8 focal DEGs and
no broad pan-neuronal response; its focal signature aligned with RNA-splicing
and synaptic genes. Neither is an obligate complex mate, paralog with a known
shared ZFP398 regulon, or upstream/downstream effector of ZFP398, so their
small positive counts are plausible upper-bound counterexamples rather than a
reason to move `Zfp398` into the 10-20 DEG range.

The most directly neuronal ZER6 study I found was in cultured neuronal cells:
Kwag et al. reported that p52-ZER6 can suppress `MT3` and increase ROS in
HT-22/SH-SY5Y models, with p52-ZER6 up and MT3 down in 5xFAD cortex (Kwag et
al., 2025, BBRC, DOI `10.1016/j.bbrc.2025.151316`, PMID 39809138). That is
useful evidence that the protein can regulate a neuronal redox gene, but it
studied overexpression/disease association rather than acute sparse
loss-of-function in recovered thalamic glutamatergic nuclei. Other ZER6 papers
place p52-ZER6 in tumor p53, G6PD, DAZAP1/SLC7A11, IGF1R/mitophagy, and
ferroptosis-resistance programs (Huang et al., 2019, DOI
`10.1016/j.ebiom.2019.08.070`, PMID 31521611; Tang et al., 2023, DOI
`10.1038/s41389-023-00464-4`, PMID 36977688; Li et al., 2024, DOI
`10.1038/s41388-024-03058-5`, PMID 38773262; Qiu et al., 2025, DOI
`10.1016/j.apsb.2025.02.013`, PMID 40486833). Those programs depend on
proliferating tumor states or ferroptosis stresses that are not sampled in this
NeuN-enriched P16-to-P37/44 experiment.

The causal transfer chain for a positive call therefore breaks at propagation
from `Zfp398` loss to a known limiting postmitotic thalamic program:

intervention, CRISPR loss of `Zfp398` -> direct loss of a poorly characterized
KRAB/C2H2 transcription factor -> possible release of isoform-specific targets
such as `MT3` or tumor-state p53/metabolic genes -> no visible measured
training perturbation establishes that this propagates into the strong
proteostasis, spliceosome, endomembrane, or ZFP423 thalamic programs -> the
endpoint is a BH-corrected single-cell DEG count in surviving
`151 TH Prkcd Grin2c Glut` nuclei.

I therefore predicted a genuine focal null, `0` DEGs. This is driven primarily
by the within-dataset `Zfp397` null and by the focal training distribution;
external ZER6 biology only weakly upgrades the possibility of a very small
effect, and not enough to justify a nonzero FDR<0.05 count.

# Limits

- No held-out `Zfp398` expression signature or DEG count was available; the
  prediction is extrapolation.
- `Zfp397` is an analog by domain class, not a paralog with a proven shared
  regulon, so its zero is only weak endpoint evidence.
- The average AAV-CRISPR mRNA knockdown in this experiment was modest and DNA
  indels were not sequenced. A flat downstream transcriptome would not prove
  absent editing.
- The ZER6 literature is mostly in cancer or cultured neuronal models. It
  establishes transcription-factor capacity and p52-specific targets, but it
  does not define a required postnatal thalamic-glutamatergic maintenance
  program.
- This assay samples recovered NeuN+ nuclei after P16 perturbation. It would
  miss earlier developmental, glial, tumor-proliferative, and pre-assay
  depletion phenotypes.
