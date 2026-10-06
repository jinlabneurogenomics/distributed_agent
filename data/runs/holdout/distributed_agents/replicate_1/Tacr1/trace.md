# Reasoning trace

## Question and endpoint

I interpreted the task as a scalar holdout prediction for one missing perturbation, `Tacr1`, in the focal `151 TH Prkcd Grin2c Glut` neuronal class. The requested value is `n_degs`: the number of measured genes whose Scanpy Wilcoxon test against matched controls had Benjamini-Hochberg adjusted `pvals_adj < 0.05`. `Tacr1` was absent from both supplied training inputs, so its own count and expression signature were not available. A zero prediction means that I expect no measured gene, including the target transcript itself, to pass FDR 0.05 under the acute sparse AAV CRISPR perturbation design.

## Sources used

- Direct endpoint data: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, containing 1,674 visible focal-cell training perturbations and their observed `n_degs`.
- Direct DE statistics: `training differential-expression dataset`, queried for `151 TH Prkcd Grin2c Glut` rows of tachykinin, neuromodulatory GPCR, G-protein, PLC, and PKC comparator perturbations.
- Run-local task metadata and measurement registry: `task_bindings.json`, `coverage.json`, `capabilities.json`, and `measurement_registry.json`.
- Same-experiment semantic corpus: `perturbai-july-260713-sourceguard-1773-v1`. I checked for packaged Tacr1/Tacr3 Claim or Finding coverage. The corpus contained no story for `Tacr1` or `Tacr3`, and a graph query found no visible Finding that reported `Tacr1` as a comparator; this was treated only as absence of packaged same-experiment interpretation, not as biological negative evidence.
- External PubMed literature on NK1R/Tacr1 biology:
  - Krause et al., 1992, DOI `10.1111/1523-1747.ep12462082`: tachykinin NK1/NK2/NK3 receptors are G-protein-coupled receptors and substance P/NK1R can couple to phospholipase C and inositol phospholipid hydrolysis.
  - Yan et al., 2009, DOI `10.1177/0269881108100255`: germline functional NK1R/Tacr1 loss changes mouse behavior and dopamine regulation, showing that Tacr1 loss can be physiologically active in the brain.
  - Simavli et al., 2015, DOI `10.1210/en.2014-2012`: substance P/NK1R regulates Kiss1/GnRH reproductive signaling in hypothalamic neuroendocrine circuitry.
  - Choi et al., 2020, DOI `10.1038/s41586-020-2860-1`, and Barik et al., 2021, DOI `10.7554/eLife.61135`: Tacr1 labels defined pain-related ascending spinal/parabrachial circuits, supporting cell-type-restricted rather than universal CNS action.

## Quantitative calibration from the training set

The supplied training counts were highly zero-inflated in the focal class:

| quantity | value |
| --- | ---: |
| training targets | 1,674 |
| targets with `n_degs = 0` | 1,205 |
| targets with `n_degs > 0` | 469 |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2,677 |

This means the default for an ordinary receptor perturbation in this cell class is no FDR-significant DEG. Low recovered-cell count alone did not force zero: among targets with 100 to 130 focal perturbed nuclei, the zero fraction was 0.751, but the same bin also contained strong responses such as `Tpr` with 1,768 DEGs at 114 nuclei, `Tnpo3` with 618 at 118 nuclei, `Wac` with 384 at 124 nuclei, and `Gfpt1` with 311 at 120 nuclei.

## Target-specific analogs and expression evidence

Among tachykinin-family genes, the only close visible perturbation in the focal training count table was `Tacr3`; `Tac1`, `Tac2`, `Tacr2`, `Gnaq`, `Gna11`, `Plcb4`, `Prkcd`, `Trpc3`, and `Gpr83` were not visible training targets. I therefore used `Tacr3` as the closest in-dataset paralog comparator and a broader set of neuromodulatory receptors and proximal signaling components as counterexamples.

| visible perturbation | relation to Tacr1 | focal perturbed nuclei | observed `n_degs` | focal expression-pattern evidence |
| --- | --- | ---: | ---: | --- |
| `Tacr3` | tachykinin NK3 receptor, closest visible tachykinin receptor | 115 | 0 | no gene at FDR 0.05; top absolute-score rows such as `Rap2b`, `Lpin1`, `Lmbrd2`, and `Nrxn1` all had `pvals_adj = 1` |
| `Htr2a` | Gq/11-coupled neuromodulatory receptor | 181 | 0 | no FDR DEG; minimum adjusted p-value was 0.8899 among inspected top rows |
| `Htr2b` | Gq/11-coupled neuromodulatory receptor | 138 | 0 | no FDR DEG; strongest inspected row `Tor1aip2` had `pvals_adj = 0.06296` |
| `Htr2c` | Gq/11-coupled neuromodulatory receptor | 126 | 0 | no FDR DEG; strongest rows all adjusted to 1 |
| `Grm5` | Gq/11-coupled metabotropic glutamate receptor | 164 | 0 | no FDR DEG |
| `Grm1` | Gq/11-coupled metabotropic glutamate receptor | 115 | 1 | the single DEG was `Grm1` itself, not a broad downstream signature |
| `Cckar`, `Cckbr` | Gq/11-coupled neuropeptide receptors | 223, 249 | 0, 0 | no FDR DEG |
| `Plcb1` | PLC effector downstream of many Gq receptors | 160 | 0 | no FDR DEG |
| `Prkca`, `Prkcg` | PKC pathway components downstream of PLC/Ca2+ signaling | 169, 175 | 0, 1 | no downstream FDR signature; `Prkcg`'s single DEG was `Prkcg` |

This set is a biologically appropriate comparison because Tacr1/NK1R is a neuromodulatory tachykinin GPCR whose canonical signaling enters Gq/PLC/Ca2+/PKC-like second messenger routes. The closest paralog, `Tacr3`, and several receptor-level analogs in the same signaling class were quiet in exactly the requested focal cell group. The single-DEG cases among `Grm1`, `Gnao1`, and `Prkcg` were target-transcript dominated rather than evidence for a recurrent transcriptional state.

## Tacr1 prediction

`Tacr1` encodes NK1R, the preferred substance P receptor. External data make it clear that complete Tacr1/NK1R loss can matter in selected circuits: it affects dopamine-dependent behavior in germline knockout mice, hypothalamic reproductive signaling, and pain-related spinal/parabrachial circuits. Those observations support a possible cell-state effect if the assayed thalamic glutamatergic neurons are Tacr1-positive and receive active tachykinin input during the P16 to P37/P44 perturbation window.

I did not project those papers as direct evidence for a broad `151 TH Prkcd Grin2c Glut` DEG burden. Most of the strongest Tacr1 literature is germline, pharmacological, hypothalamic, spinal, parabrachial, cortical interneuron, or non-neuronal; it is not sparse postnatal CRISPR in thalamic glutamatergic neurons. Acute partial receptor disruption is also more likely to change excitability or peptide responsiveness than to create a large homeostatic transcriptional footprint visible in recovered single nuclei.

The in-dataset prior is therefore stronger than the external pro-function prior for this endpoint. The most relevant visible tachykinin paralog, `Tacr3`, had `n_degs = 0`, and the wider in-dataset Gq/neuropeptide receptor panel was almost uniformly zero in the same focal class. The few one-DEG comparators did not show a broad analog signature. I predicted that `Tacr1` will likewise fall below the FDR threshold for every measured gene:

| target | zero/nonzero call | predicted `n_degs` |
| --- | --- | ---: |
| `Tacr1` | zero | 0 |

## Limits and uncertainty

The prediction is an extrapolation from receptor-family and signaling analogs because `Tacr1` itself was completely held out and no Tacr1-specific same-experiment Finding was available. `Tacr3` is the closest visible tachykinin receptor but is not an obligate complex partner; its ligand preference and anatomical expression differ from Tacr1. Broad Gq/PLC receptor silence is informative for response breadth in this assay, but it cannot exclude a thalamus-specific Tacr1 circuit effect. Conversely, germline and pharmacological NK1R studies demonstrate physiological roles of the receptor but overstate the expected effect of sparse juvenile CRISPR loss on survivor-state nuclear RNA. Because the endpoint is an FDR count, predictions near zero are especially threshold-sensitive: a weak Tacr1 self-transcript effect or a single downstream gene could move the true count from 0 to 1 without implying a qualitatively broad response.
