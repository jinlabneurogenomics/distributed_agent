# Predicting the held-out 151 TH Prkcd Grin2c Glut response for Apc

## Question and resolved ambiguities

The requested endpoint is the number of measured genes with `pvals_adj < 0.05`
after a held-out CRISPR loss-of-function perturbation in the focal
`151 TH Prkcd Grin2c Glut` class. In this Allen-style label, `TH` denotes
thalamus, not tyrosine hydroxylase; the focal class is therefore a thalamic
glutamatergic population. I used the training count CSV as the authoritative
definition of the FDR 0.05 scalar endpoint and used the parquet signatures only
for non-held-out perturbations. `Apc` was absent from both training inputs, as
expected from the manifest.

## Sources used

- `training_de_all_cell_groups.parquet`: non-held-out per-gene Wilcoxon
  differential-expression statistics. I filtered this to
  `group_name == "151 TH Prkcd Grin2c Glut"` for represented Wnt,
  beta-catenin, and pathway-boundary targets.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: exact training
  `n_degs` for the focal group.
- `015_Apc.csv`: the held-out target list; it contains only `Apc`.
- Distributed Agents same-experiment semantic corpus
  `perturbai-july-260713-sourceguard-1773-v1`: used for curated same-assay
  interpretations of `Ctnnb1`, `Tcf7l2`, `Lrp6`, `Gsk3b`, `Fzd4`, `Fzd6`,
  `Macf1`, and related Wnt receptor-layer perturbations.
- Distributed Agents runtime profile comparison: I compared signed 151-TH log-fold
  change profiles for `Ctnnb1`, `Tcf7l2`, `Lrp6`, `Gsk3b`, `Lrp5`, `Fzd2`,
  `Fzd4`, `Fzd6`, `Fzd9`, `Ctnnd2`, and `Macf1`, using
  `pvals_adj < 0.05` only to summarize robust overlaps.
- PubMed literature:
  - Stamos and Weis 2013, Cold Spring Harb Perspect Biol,
    DOI `10.1101/cshperspect.a007898`, PMID `23169527`.
  - Liu et al. 2002, Cell, DOI `10.1016/S0092-8674(02)00685-2`,
    PMID `11955436`.
  - Hinoi et al. 2000, J Biol Chem, DOI `10.1074/jbc.M003997200`,
    PMID `10906131`.
  - MacDonald, Tamai, and He 2009, Dev Cell,
    DOI `10.1016/j.devcel.2009.06.016`, PMID `19619488`.
  - Purro et al. 2008, J Neurosci,
    DOI `10.1523/JNEUROSCI.2320-08.2008`, PMID `18716223`.
  - Mohn et al. 2014, Mol Psychiatry, DOI `10.1038/mp.2014.61`,
    PMID `24934177`.

## Computational calibration

I read the held-out manifest and confirmed that the sole target is `Apc`. The
focal training table has 1,674 observed perturbations and is strongly
zero-inflated: 1,205 targets have 0 DEGs, 363 have 1-9, 63 have 10-99, and 43
have at least 100. A global median of 0 would therefore be a poor default for a
core pathway target in a pathway with a measured focal response.

I then filtered the parquet to 151 TH Prkcd Grin2c Glut for represented
canonical Wnt/beta-catenin and boundary targets and recomputed the exact
`pvals_adj < 0.05` counts:

| training target | 151 TH Prkcd Grin2c Glut `n_degs` | signed details |
|---|---:|---|
| `Ctnnb1` | 383 | 100 up, 283 down |
| `Tcf7l2` | 106 | 39 up, 67 down |
| `Lrp6` | 4 | 1 up, 3 down |
| `Gsk3b` | 6 | 1 up, 5 down |
| `Ctnnd2` | 1 | self-transcript only |
| `Lrp5`, `Fzd2`, `Fzd4`, `Fzd6`, `Fzd9`, `Macf1` | 0 | no FDR 0.05 genes |

The robust intersections also separated direct beta-catenin/TCF responses from
superficial family matches. `Ctnnb1` and `Tcf7l2` shared 44 FDR 0.05 genes in
151 TH, 40 in the same direction. All four `Lrp6` significant genes were in
the `Ctnnb1` signature and changed in the same direction; two were also in the
`Tcf7l2` signature. By contrast, `Gsk3b` shared only one significant gene with
`Ctnnb1`, the assayed Frizzled receptors had zero significant genes, and
`Macf1` was silent.

The sentinel genes matched the corpus interpretation. `Ctnnb1` loss decreased
canonical feedback and thalamic state genes: `Axin2` -0.943, `Lef1` -0.624,
`Notum` -1.187, `Wnt9b` -1.111, `Vangl1` -0.818, `Ramp3` -1.367, `Gabra4`
-0.758, `Spock3` -0.576, and `L1cam` -0.602 at FDR 0.05. `Tcf7l2` reproduced a
smaller same-direction terminal program, including `Lef1`, `Ramp3`, `Kcnc2`,
`Pcsk2`, `Cpe`, `Spon1`, and `Spock3`. `Lrp6` captured only a four-gene
Axin2-adjacent trace at FDR 0.05, and isolated `Gsk3b` loss did not induce
canonical Wnt output.

## Target-specific reasoning

### Apc

`Apc` encodes the adenomatous polyposis coli scaffold in the Axin/GSK3/CK1
beta-catenin destruction complex. CK1 first primes beta-catenin, GSK3 adds the
phosphodegron, and the APC/Axin complex promotes beta-catenin phosphorylation,
ubiquitylation, and proteasomal destruction; Wnt pathway activation or APC loss
therefore stabilizes beta-catenin and increases beta-catenin/TCF transcription
rather than phenocopying a `Ctnnb1` knockout in direction
(Hinoi et al. 2000; Liu et al. 2002; Stamos and Weis 2013; MacDonald et al.
2009). APC also has neuronal microtubule and synaptic roles: Wnt3a rapidly
redistributes APC at axonal microtubule plus ends in cultured neurons, and
forebrain APC conditional knockout increases beta-catenin and changes synaptic
structure/function in mouse hippocampus (Purro et al. 2008; Mohn et al. 2014).

The strongest within-dataset anchor is `Ctnnb1`, with 383 focal DEGs. Its
signature proves that this class can report beta-catenin-dependent Wnt genes
and a larger thalamic excitability/adhesion state. `Tcf7l2`, the downstream TCF
effector most convergent with `Ctnnb1`, had 106 DEGs and shared many of the
same down-regulated thalamic genes. These two targets are relevant because APC
loss should alter the abundance of the beta-catenin transcriptional coactivator
that acts through TCF/LEF proteins.

The near-null comparators set important upper and lower bounds. `Lrp6` is an
upstream co-receptor and was only a four-gene response despite same-direction
overlap with `Ctnnb1`; single Frizzled receptors and `Lrp5` were flat. Those
zeros are weak counterexamples for `Apc` because APC lies in the intracellular
core complex rather than in a redundant receptor layer. `Gsk3b` had only 6 DEGs
and no Axin2/Lef1/Notum induction, so loss of a single kinase was buffered away
from canonical Wnt output in this assay, probably because it is pleiotropic,
post-translational, and not the only kinase in the destruction complex. `Macf1`
and `Ctnnd2` were also poor analogs: the Distributed Agents corpus specifically
interprets `Macf1` as failing to activate the Wnt/beta-catenin program, and
`Ctnnd2` is an adhesion-family boundary rather than a destruction-complex
member.

The zero/nonzero call is therefore nonzero. The point estimate should not be
copied from `Ctnnb1`: `Ctnnb1` loss removes beta-catenin itself, including its
cadherin-associated and Wnt-transcription functions, whereas `Apc` loss should
stabilize beta-catenin and may be partially limited by negative feedback in
postmitotic neurons. It should, however, be far above `Lrp6`/`Gsk3b` because
APC is the direct destruction-complex scaffold whose loss is a canonical route
to beta-catenin accumulation. I assign `Apc` a low-strong response, close to the
`Tcf7l2` count and about one third of `Ctnnb1`.

Prediction: `Apc` -> `128` DEGs.

## Limits

`Apc` itself, Axin paralogs, Dishevelled paralogs, most TCF/LEF/TLE genes, and
`Apc2` were not represented as focal training perturbations, so the most direct
destruction-complex neighborhood is missing. The task only observes survivor
nuclear RNA 3-4 weeks after sparse P16 CRISPR editing; beta-catenin protein,
APC protein at microtubule plus ends, synapses, spines, and electrophysiology
were not measured. Directional expectations for `Apc` are biochemical
extrapolations from Wnt literature, while the count magnitude is calibrated to
same-experiment `Ctnnb1`/`Tcf7l2`/`Lrp6` responses. The exact 128 value is thus
a point prediction within a broad low-strong region, not a directly observed
quantity.
