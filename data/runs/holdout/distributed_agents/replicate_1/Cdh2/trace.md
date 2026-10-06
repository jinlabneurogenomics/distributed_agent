# Cdh2 held-out DEG-count prediction

## Question and endpoint

The requested prediction is the number of genes expected to satisfy `pvals_adj < 0.05` after `Cdh2` perturbation in `151 TH Prkcd Grin2c Glut` thalamic glutamatergic neurons. I treated this as the same endpoint represented in the training CSV: a Perturb-seq Wilcoxon DEG count in recovered, class-assigned nuclei, including the perturbed target transcript if that transcript itself passes the FDR threshold. The held-out `Cdh2` rows are absent from both supplied files, so the `Cdh2` count is absent from the declared inputs and had to be inferred from non-held-out perturbations.

Ambiguities I resolved:

- The `151` prefix is an Allen-style class identifier, not a cell count.
- The count endpoint is assay- and power-dependent and is not a direct readout of editing efficiency, viability, or synapse morphology.
- The matched recovered-nucleus counts were used only to check that analogs in `151` were not near-zero-cell outliers.
- Target-transcript loss in a comparator was interpreted only as part of the FDR count surface. I did not use self-knockdown magnitude as a quantitative editing-efficiency score.

## Sources

- Direct input counts: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Direct differential-expression rows: `training differential-expression dataset`.
- Held-out request manifest: `single-target request for Cdh2`.
- Dataset portrait and measurement registry in `codex_runtime/pipeline/`, which define the focal-cell label, row semantics, and absent quantities.
- Internal same-experiment semantic layer: `perturbai-july-260713-sourceguard-1773-v1` Findings/Evidence/Reference corpus. I used it as packaged interpretation of the same Perturb-seq experiment, not as an independent replicate. I used the BioKG graph only to find whether any visible Finding explicitly mentioned the held-out symbol `Cdh2`; its only hit was `Pcdh19:F003`, and the graph hit itself was not scored.
- External biology from PubMed and corpus-resolved references:
  - Seong, Yuan and Arikkath 2015, doi:10.4161/19336918.2014.994919 / PMID:25914083, reviewing classical cadherin/catenin functions in dendrite and synapse morphogenesis.
  - Valenta, Hausmann and Basler 2012, doi:10.1038/emboj.2012.150 / PMID:22617422, reviewing beta-catenin as both a cadherin-junction component and the nuclear effector of canonical Wnt signaling.
  - Togashi et al. 2002, doi:10.1016/s0896-6273(02)00748-1 / PMID:12123610, showing that cadherin blockade perturbs dendritic spine morphology and synaptic protein localization in cultured hippocampal neurons.
  - Tai et al. 2007, doi:10.1016/j.neuron.2007.05.013 / PMID:17553425, showing activity-regulated N-cadherin endocytosis controlled by beta-catenin.
  - Abe et al. 2004, doi:10.1038/nn1212 / PMID:15034585, showing that alphaN-catenin stabilizes dendritic spines and synaptic contacts.
  - Nikitczuk et al. 2014, doi:10.1002/hipo.22282 / PMID:24753442, showing that late postnatal conditional N-cadherin ablation in excitatory forebrain synapses changes synaptic molecular organization with limited gross spine-structure effects.

## Computation over the declared data

The requested CSV contained one held-out target:

| requested target |
| --- |
| Cdh2 |

In the focal training-count CSV there were 1,674 unique non-held-out targets. The endpoint was sparse: 1,205/1,674 targets had `n_degs = 0`, the median was 0, the 75th percentile was 1, the 95th percentile was 18, and the largest thalamic responders were rare outliers such as `Uba5` with 2,677 DEGs and `Ctnnb1` with 383 DEGs.

No classical `Cdh*` perturbation was available among the 1,674 training targets; the only cadherin-prefixed training target was `Pcdh19`. I therefore queried the training counts for cadherin/catenin, Wnt, and synaptic-adhesion analogs selected from known biology and from the July corpus. I then read the raw Parquet for row groups 546-580, the only row groups whose `group_name` statistics could contain `151 TH Prkcd Grin2c Glut`, and filtered them to the analog gene set to verify exact `151` FDR<0.05 and FDR<0.10 counts, top nominal rows, and matched nuclei.

### `151` analog counts

| training perturbation | `151` n_degs | `151` FDR<0.10 genes | matched perturbed nuclei | interpretation for `Cdh2` |
| --- | ---: | ---: | ---: | --- |
| `Ctnna2` | 0 | 0 | 223 | Direct cadherin-actin linker; best `151` row was its own transcript at FDR 0.146, with no downstream genes. |
| `Ctnna3` | 0 | 0 | 229 | Catenin paralog; no `151` DEG and no all-cell neuronal response in the corpus. |
| `Ctnnd2` | 1 | 1 | 221 | Neuronal delta-catenin; the one `151` DEG was `Ctnnd2` itself, not a downstream module. |
| `Pcdh19` | 0 | 0 | 137 | Protocadherin adhesion disease gene; all top `151` nominal rows had adjusted p-value 1. |
| `Nectin1` | 0 | 0 | 162 | Synaptic adhesion gene outside the classical cadherin complex; no focal FDR signal. |
| `Cadm2` | 1 | 1 | 167 | SynCAM-family synaptic adhesion molecule; the only `151` DEG was `Cadm2` itself. |
| `Actn4` | 0 | 0 | 199 | Actin-associated countercheck; flat in `151`. |
| `Dscam` | 0 | 1 | 124 | Surface recognition molecule; one FDR<0.10 near miss, zero FDR<0.05 genes. |
| `Nrxn1`/`Nrxn2`/`Nrxn3` | 1 / 0 / 0 | 1 / 0 / 1 | 253 / 281 / 175 | Synaptic adhesion receptors; at most a one-gene focal footprint. |
| `Nlgn3`, `Cntnap1`, `Cntnap2`, `Grid1`, `Grid2`, `Lrrtm1`, `Lrrtm3`, `Lrrtm4`, `Ptprt` | 0-1 each | 0-1 each | 94-283 | A broader synaptic-adhesion set was likewise sparse. |

I also checked the Wnt/beta-catenin branch because `Cdh2` physically binds beta-catenin and `Ctnnb1` is a strong thalamic responder.

| training perturbation | `151` n_degs | matched perturbed nuclei | reason kept as counterexample |
| --- | ---: | ---: | --- |
| `Ctnnb1` | 383 | 171 | Beta-catenin is both a cadherin-junction protein and the direct nuclear coactivator of Wnt/TCF targets. Its `151` signature was led by strong down-regulation of `Plekhg1`, `Gabra4`, `Ramp3`, `Nin`, `Rasgrp1`, `Synpo2`, `Chrna4`, and `L1cam`; it also reduced `Cdh2` itself, logFC -0.447, FDR 9.03e-05 in corpus evidence `Ctnnb1:E028`. |
| `Tcf7l2` | 106 | 111 | Downstream Wnt transcription-factor target, therefore mechanistically close to the Ctnnb1 nuclear program rather than to membrane `Cdh2`. |
| `Lrp6` | 4 | 120 | Upstream Wnt co-receptor with only six FDR<0.10 genes in `151`. |
| `Gsk3b` | 6 | 108 | Pathway regulator but opposite/indirect with respect to beta-catenin stabilization; weak focal response. |
| `Lrp5`, `Fzd2`, `Fzd4`, `Fzd6`, `Fzd9`, `Lgr4`, `Gpc6` | 0 each | 139-281 | Single Wnt receptors or modulators did not substitute for `Ctnnb1` in `151`. |

The July corpus records agreed with these raw counts. `Ctnna2:F002` reported that core cadherin/catenin, Arp2/3-actin, and `Lef1`/Wnt readouts never passed FDR<0.10 after `Ctnna2` loss across 22 measured groups. `Ctnna2:F003` and `Ctnna3:F003` reported that `Ctnna2`, `Ctnna3`, and `Ctnnd2` did not form a broad transcriptomic phenocopy. `Ctnnb1:F007` specifically rejected the naive family transfer: `Lrp6` and `Tcf7l2` partially converged with `Ctnnb1`, but `Lrp5`, `Gsk3b`, the single Frizzled perturbations, `Lgr4`, `Gpc6`, `Ctnna2`, `Ctnna3`, and `Ctnnd2` did not. `Pcdh19:F001-F003` reported no robust post-P16 neuronal downstream response for `Pcdh19`, despite literature links among PCDH19, N-cadherin and protocadherin adhesion codes.

## Causal transfer for `Cdh2`

The relevant chain is:

`Cdh2` CRISPR loss of function -> reduced N-cadherin at cadherin/catenin synaptic adhesions -> local effects on beta-catenin anchoring, synaptic adhesion, and receptor/scaffold organization -> possible homeostatic transcription in recovered thalamic neurons -> FDR-thresholded nuclear RNA DEGs at 3-4 weeks.

The same chain for `Ctnnb1` differs at the direct molecular consequence. `Ctnnb1` loss removes beta-catenin from both junctional cadherin complexes and the canonical Wnt nuclear coactivator pool. Valenta et al. define that dual function, and the Perturb-seq evidence showed a strong Wnt/TCF depression in `151`, including `Lef1`/`Axin2`-linked feedback genes in the same state as adhesion genes. Because `Cdh2` is an upstream membrane adhesion molecule, its loss can disturb local cadherin-catenin adhesion but is not expected to directly eliminate nuclear beta-catenin/TCF activity in the same way. The strong 383-DEG `Ctnnb1` result is therefore a counterexample to a generic "cadherin/catenin genes are all broad responders" rule, not a same-outcome prior for `Cdh2`.

`Ctnna2` is a better mechanistic analog at the synaptic complex stage: alphaN-catenin links cadherin adhesion to actin and stabilizes dendritic spines, but its perturbation had zero `151` DEGs and no detectable core cadherin/Arp/Wnt transcriptional echo across the measured cells. `Ctnnd2`, another neuronal cadherin/catenin protein, had only a one-gene focal count. `Pcdh19`, `Cadm2`, `Nectin1`, neurexins/neuroligin/CNTNAP/LRRTM/Grid/Ptprt, and `Dscam` gave the same qualitative message: perturbing synaptic or surface-adhesion architecture in this postnatal sparse CRISPR assay often produced no stable nuclear program and, when nonzero, usually produced a one-gene count driven by the target row itself.

External N-cadherin literature supports biological importance but not a large RNA cascade. Cadherin blockade and N-cadherin/beta-catenin trafficking alter spine and synaptic organization in neurons (Togashi et al.; Tai et al.; Seong et al.), and late postnatal forebrain N-cadherin ablation changes synaptic molecular composition and behavior (Nikitczuk et al.). Those are mainly protein-localization, structure, physiology, and circuit phenotypes. They do not require a broad cell-autonomous snRNA-seq response in recovered thalamic nuclei 3-4 weeks after mosaic P16 editing.

## Point prediction

I predict a nonzero but minimal focal footprint:

- The zero-count analogs make a broad `Cdh2` response unlikely.
- The one-count `Cadm2`, `Ctnnd2`, `Cntnap1`, `Cntnap2`, `Grid1`, `Lrrtm1`, `Nlgn3`, and `Nrxn1` cases show that structurally important adhesion perturbations frequently land at exactly one focal DEG in this endpoint.
- `Cdh2` itself was measurably regulated in `151` after `Ctnnb1` loss, so it is plausibly expressed and detectable in this group; direct `Cdh2` targeting may therefore contribute the one threshold-crossing row, but I do not project the 383-gene beta-catenin/Wnt response onto it.

Final point prediction: `Cdh2 = 1`.

## Limits and extrapolation

This is extrapolation because no `Cdh2`, `Cdh1`, `Cdh4`, `Cdh13`, `Pcdh1`, or `Pcdh9` perturbation was present in the training Parquet. The represented catenins and synaptic-adhesion genes are mechanistic neighbors, not obligate members of the same limiting molecular function as N-cadherin. The focal endpoint is also a discrete FDR count, so a prediction of 0 vs 1 can hinge on the target transcript's own adjusted p-value. The external N-cadherin studies measured culture, hippocampus, adult conditional synaptic deletion, or developmental adhesion phenotypes rather than acute AAV-CRISPR in postnatal thalamic neurons. I therefore place confidence in a very small response, but the exact one-gene call is less secure than the rejection of a large `Ctnnb1`-like Wnt/TCF footprint.
