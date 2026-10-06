# DEG-count prediction trace

## Question and endpoint

The task is to predict `n_degs` for each requested held-out perturbation in
`151 TH Prkcd Grin2c Glut` cells. I interpreted `n_degs` exactly as the training
CSV does: the count of measured genes in the focal-cell Wilcoxon DE table with
Benjamini-Hochberg-adjusted `pvals_adj < 0.05`, using the assayed nuclear
RNA-seq contrast of perturbed versus matched non-targeting controls. The target
gene itself is included when its own transcript crosses FDR 0.05, because the
training counts agree with a direct count over the supplied parquet under that
rule.

The held-out manifest contains one requested target, `Camk4`, and it is absent
from the supplied training-count CSV, as expected.

## Sources

- Declared Perturb-seq DE parquet:
  `training differential-expression dataset`.
  I queried focal-cell rows for calcium/calmodulin, CaMKII, calcineurin, CREB,
  NMDAR, and calcium-channel training perturbations and used the adjusted
  p-value threshold requested by the task.
- Declared focal-cell training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Requested-target manifest:
  `single-target request for Camk4`.
- Run-local corpus and calibration: July 260713 sourceguard 1773 v1 Findings
  ledger, queried only for same-experiment summaries of the inspected training
  analogs. This corpus is a packaged interpretation layer over the same
  Perturb-seq experiment, not independent replication.
- Independent literature from PubMed:
  - Finkbeiner et al. 1997, Neuron, DOI `10.1016/s0896-6273(00)80395-5`,
    PMID `9390517`.
  - Ho et al. 2000, Journal of Neuroscience, DOI
    `10.1523/JNEUROSCI.20-17-06459.2000`, PMID `10964952`.
  - Wei et al. 2002, Nature Neuroscience, DOI `10.1038/nn0602-855`,
    PMID `12006982`.
  - Kokubo et al. 2009, Journal of Neuroscience, DOI
    `10.1523/JNEUROSCI.0040-09.2009`, PMID `19605628`.

## Computation

I first used the focal training-count CSV to find measured perturbations in or
near the calcium/calmodulin-to-transcription axis. I then used a filtered
DuckDB scan of the parquet restricted to `group_name = '151 TH Prkcd Grin2c
Glut'` and those targets to count `pvals_adj < 0.05` rows and list the actual
FDR genes. The direct counts matched the CSV:

| analog | observed 151-cell `n_degs` |
|---|---:|
| `Calm1` | 14 |
| `Cacna1g` | 12 |
| `Creb1` | 10 |
| `Ppp3r1` | 9 |
| `Ppp3ca` | 4 |
| `Camk2b` | 1 |
| `Calm3` | 1 |
| `Prkaca` | 1 |
| `Calm2` | 0 |
| `Camk2a` | 0 |
| `Camk2g` | 0 |
| `Ppp3cc` | 0 |

The exact focal-cell significant genes showed compact, mostly distinct
signatures rather than one shared calcium module:

- `Calm1`: 14 genes, including the self transcript and a small induced module
  containing `Rasgrp2`, `Peg3`, `Aifm3`, `Tuba1b`, `Resp18`, `Maged1`,
  `Coro6`, `Vamp1`, and the repressed calcium pump `Atp2b1`.
- `Creb1`: 10 genes, led by strong `Crem` induction and down-regulation of
  `Tmem181a`, `Txndc12`, `Chkb`, `Nceh1`, `Ppox`, `Rnf139`, and `Sez6l2`.
- `Ppp3r1`: 9 genes, led by `Pcsk1n` and `Ptprs` induction plus repression of
  `Atp2a2`, `Coro6`, `Septin4`, and `Slc6a17`.
- `Ppp3ca`: 4 genes, including the self transcript, `Iyd` and `Ptpn3` down,
  and `Pik3r1` up.
- `Cacna1g`: 12 genes, including self plus `Ptprn` up and `Stmn4`, `Cpne7`,
  `Jun`, `Zdhhc22`, `Lrrc7`, and `Irag1` down.
- `Camk2b`, `Calm3`, and `Prkaca`: each had only the perturbed transcript
  itself at FDR 0.05 in the focal class.
- `Camk2a`, `Camk2g`, `Calm2`, and `Ppp3cc`: no focal-cell FDR genes.

I also computed Pearson correlations between focal-cell Wilcoxon score vectors
for these analogs. These correlations were generally weak: the strongest was
the expected calcineurin catalytic/regulatory pair, `Ppp3ca` versus `Ppp3r1`,
at `r = 0.137`; `Calm1` versus `Creb1` was slightly anticorrelated
(`r = -0.028`), and the CaMKII paralogs were nearly uncorrelated with one
another and with the CREB/calmodulin/calcineurin nodes. I therefore used the
observed DEG counts as local scale calibration, not as proof that any one
measured analog is an expression phenocopy of `Camk4`.

## Target-specific reasoning

### Camk4

`Camk4` encodes CaMKIV, a Ca2+/calmodulin-regulated kinase classically linked
to nuclear CREB phosphorylation and Ca2+-dependent transcription in neurons.
Finkbeiner et al. showed that BDNF can activate CREB through a CaMKIV-regulated
calcium/calmodulin pathway in cultured neurons and hippocampal slices. Ho et
al. showed that Camk4/CaMKIV-deficient mice have impaired neuronal CREB
phosphorylation and Ca2+/CREB-dependent gene expression as well as synaptic
plasticity defects; Wei et al. found reduced or blocked CREB activation in
amygdala and cortical areas of CaMKIV-null mice during fear-memory assays; and
Kokubo et al. linked a CaMKK2/CaMKIV cascade to CREB phosphorylation and
`Bdnf` transcription in developing cerebellar granule cells. These external
data make a zero prediction less likely than for a generic buffered kinase:
Camk4 is in the Ca2+-to-nucleus branch rather than in the largely synaptic
CaMKII branch.

The best within-dataset scale analog is `Creb1`, because CREB1 is immediately
downstream of CaMKIV in the canonical transcriptional route. `Creb1` produced
10 focal-cell DEGs, driven by `Crem` induction and a small ER/lipid/lysosomal/
heme/membrane module rather than by a broad immediate-early program. A direct
Camk4 lesion should partially reduce CREB activation, but it is upstream of
CREB1 and therefore buffered by parallel CREB kinases such as PKA, RSK/MSK and
by Ras/MAPK routes; I therefore expect a response in the same low-count regime,
not a larger effect than `Creb1`.

`Calm1` is the principal upstream in-dataset positive analog. It caused 14
focal-cell DEGs with `Rasgrp2`, `Resp18`, `Vamp1`, cytoskeletal/lipid genes,
and `Atp2b1` down, but the July corpus specifically noted that `Calm1` did not
phenocopy represented CaM effectors and did not activate a classical
`Fos`/`Arc`/`Npas4`/`Egr` immediate-early module. `Calm2` and `Calm3`, which
encode the same calmodulin protein, had 0 and 1 DEG respectively. Those
training results argue that single acute CaM-axis perturbations in this assay
usually produce a narrow 151-cell RNA footprint even when the perturbed protein
is biologically central.

The represented CaMKII paralogs are counterexamples rather than direct Camk4
surrogates. `Camk2a`, `Camk2b`, and `Camk2g` had 0, 1, and 0 focal-cell DEGs,
and the same-experiment corpus reports that their full RNA signatures did not
converge despite their shared calcium/calmodulin regulation. CaMKII alpha/beta
complexes are synaptic plasticity enzymes, whereas CaMKIV is a CaMKK-activated
nuclear CREB kinase, so the CaMKII nulls lower confidence in a huge generic
CaMK transcriptome but should not force `Camk4` to zero.

Calcineurin perturbations give another small-effect Ca2+/CaM-to-transcription
calibration. Loss of the catalytic subunit `Ppp3ca` yielded 4 focal-cell DEGs;
loss of regulatory `Ppp3r1` yielded 9 and shared `Pcsk1n` induction with
`Ppp3ca`. The corpus interpretation was that the canonical NFAT, immediate-
early, and ISR/UPR programs were absent. This fits a small nonzero Camk4
prediction: calcium-regulated nuclear signaling can leave a detectable trace
in this thalamic population, but basal snRNA-seq at one postnatal time point is
not a robust reporter of every activity-dependent Ca2+ effector.

Finally, receptor and channel analogs set an upper bound. `Cacna1g`, a
thalamic T-type calcium-channel alpha subunit, caused a similarly small
12-gene focal-cell state. `Grin1`, the obligatory NMDAR subunit, caused 89
focal-cell DEGs, but its program contained broad synaptic and excitability
remodeling genes such as `Erc2`, `Homer2`, `Lrrc7`, `Kif17`, and `Kcnab2`.
The corpus reports that NMDAR subunit perturbations did not phenocopy CaMKII
or each other. Because NMDAR and Cav3.1 loss change membrane conductance,
calcium influx and synaptic state upstream of many effectors, I did not transfer
the 89-gene `Grin1` breadth to a single nuclear kinase.

Putting these together, I predict that acute mosaic Camk4 loss is not silent
but will be assay-sparse: lower than `Calm1`/`Creb1`/`Cacna1g` if alternative
CREB-activating routes compensate, higher than CaMKII or `Prkaca` because
CaMKIV has a more direct Ca2+-to-CREB transcriptional role. I used the small
Ca2+/CREB analog band and selected **8 DEGs** as the point estimate.

## Limits

The requested endpoint for `Camk4` is genuinely absent: neither the focal
`n_degs` nor the Camk4 expression signature is present in the training CSV or
DE parquet. The estimate is therefore a transfer from related perturbations,
not a measured value. The closest training perturbations are imperfect in
opposite ways: `Creb1` is downstream and integrates more than CaMKIV;
`Calm1-3` are upstream but affect all calmodulin effectors; calcineurin is a
parallel CaM effector with NFAT rather than CREB as its canonical transcription
branch; CaMKII kinases are same-family but more synaptic; and NMDAR/Cav3.1
targets perturb calcium entry itself. The July corpus and the focal parquet
both show that these signatures do not form a clean common module, so the point
estimate has high uncertainty around a low nonzero expectation.

