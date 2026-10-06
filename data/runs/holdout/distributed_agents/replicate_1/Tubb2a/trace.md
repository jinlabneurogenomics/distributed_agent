# Held-out DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

The requested endpoint is the integer `n_degs` for each held-out perturbation in
`151 TH Prkcd Grin2c Glut`, the thalamic glutamatergic class marked by Prkcd and
Grin2c. I treated `n_degs` as the number of measured genes whose Wilcoxon
Benjamini-Hochberg adjusted p-value is below 0.05 in the focal cell group,
including the perturbed target transcript if it passed the same threshold. The
only requested target in `b0084.csv` is `Tubb2a`, and it is absent from both the
training count CSV and the differential-expression Parquet as a `gene_target`.

The held-out endpoint itself is therefore absent from the declared inputs. The
training count CSV is a direct observation of the same endpoint for 1,674
non-held-out targets; the Parquet is direct expression-signature evidence for
those same training targets and context-only evidence for genes, such as
`Tubb2a`, that appear as downstream measured genes. The selected internal corpus,
`perturbai-july-260713-sourceguard-1773-v1`, was used as same-experiment
packaged interpretation of tubulin comparators, not as independent replication.
I used PubMed literature for the external prior on tubulin isotype function and
TUBB2A disease biology.

## Computations over the declared data

I first summarized the focal training endpoint from
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`. It is highly sparse:

| summary | value |
|---|---:|
| training targets | 1,674 |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2,677 |

To verify the endpoint and inspect `Tubb2a` analogs, I filtered
`training_de_all_cell_groups.parquet` to
`group_name == "151 TH Prkcd Grin2c Glut"` and recomputed, for every
`gene_target`, `sum(pvals_adj < 0.05)`. The recomputed counts matched all rows
of the training count CSV exactly, so I used the CSV counts as the authoritative
calibrated endpoint and the Parquet rows to inspect expression patterns.

The biologically closest assayed structural-tubulin and microtubule perturbations
in the focal cell group were:

| training perturbation | `n_degs` | focal expression evidence |
|---|---:|---|
| `Tuba1a` | 7 | Self transcript down, and a coherent tubulin replacement signature up: `Tubb3`, `Tubb2a`, `Tuba4a`, `Tubb4a`, `Tubb4b`, and `Tubb5` all passed FDR 0.05. |
| `Tuba4a` | 2 | `Tuba4a` self down plus one weak non-tubulin singleton, `Mast1`; no multi-tubulin compensation. |
| `Tubb4b` | 1 | `Tubb4b` self down only; `Tubb5` was the nearest beta-tubulin row but did not pass FDR. |
| `Tubb5` | 1 | Strong `Tubb5` self down only; no alpha/beta-tubulin paralog induction. |
| `Map1b` | 1 | `Map1b` self down only; no downstream tubulin-code or axon-growth RNA module. |
| `Kif1a` | 1 | `Kif1a` self down only at FDR 0.05; several near misses but no broad motor-stress program. |
| `Kif5a` | 1 | `Kif5a` self down only; no detectable anterograde-transport stress program. |
| `Kif5c` | 1 | `Kif5c` self down only. |
| `Stmn2` | 1 | `Stmn2` self down only; the next tubulin row, `Tuba1a`, was a near miss. |
| `Mapt` | 1 | `Mapt` self down only. |
| `Spast` | 0 | No FDR 0.05 genes. |
| `Ttll5` | 0 | No FDR 0.05 genes. |

I also queried the focal-cell rows for the measured tubulin genes
`Tuba1a`, `Tuba4a`, `Tubb2a`, `Tubb3`, `Tubb4a`, `Tubb4b`, `Tubb5`, `Tbcd`,
`Stmn2`, `Map1b`, and `Tubg1` across every training perturbation. This showed
that `Tubb2a` can be a downstream part of broad states in this cell group: it
was up after `Cic`, `Tuba1a`, `Pura`, `Zbtb7a`, and `Nrf1`, and down after
`Gfpt1`, `Elp1`, `Thap11`, `Atp2a2`, `Rnpc3`, `Vps54`, `Cdc40`, `Rab7`,
`Atxn10`, and `Prpf6`. I did not treat chromatin, splicing, vesicle-trafficking,
and proteostasis perturbations such as `Cic` or `Gfpt1` as mechanistic analogs
for `Tubb2a` knockout, because in them `Tubb2a` is a downstream marker embedded
in hundreds of DEGs, not the initiating lesion.

The internal PerturbAI reports supported the same separation. The `Tuba1a`
report annotated the six-gene alpha/beta-tubulin induction module in `151 TH
Prkcd Grin2c Glut` and noted that direct `Tuba4a`, `Tubb4b`, and `Tubb5`
perturbations failed to reproduce it. The `Tubb5` and `Tubb4b` reports annotated
self-down, postnatal transcriptional buffering across assayed neuronal groups
and contrasted that with the Tuba1a-specific tubulin-paralog feedback signature.

## Biological transfer for `Tubb2a`

`Tubb2a` encodes beta-IIa tubulin, one of the beta-tubulin subunits that pairs
with alpha tubulin to form microtubule heterodimers. Mouse postnatal neurons
express multiple alpha- and beta-tubulin isotypes with partially specialized
temporal patterns, and microtubule behavior depends on isotype composition
(Hausrat et al., 2020, DOI 10.1002/dneu.22745; Vemu et al., 2017, DOI
10.1091/mbc.E17-02-0124). Human heterozygous TUBB2A missense variants cause a
tubulinopathy spectrum with epilepsy, developmental delay, and variably abnormal
cortical malformations (Brock et al., 2020, DOI
10.1136/jmedgenet-2019-106740); broader tubulinopathy reviews place TUBB2A
with TUBA1A, TUBB2B, and TUBB3 in the alpha/beta-tubulin genes where altered
heterodimer abundance, GTP binding, protofilament interactions, or motor/MAP
binding can perturb brain development (Maillard et al., 2022, DOI
10.1016/j.semcdb.2022.07.009). A newer Arg391 series further supports the
alpha/beta heterodimer interface as a disease-relevant mechanism for TUBB2A
(Di Pasquale et al., 2025, DOI 10.3389/fncel.2025.1664953).

The causal chain I applied was:

`Tubb2a` CRISPR loss of function -> reduced beta-IIa tubulin contribution to
alpha/beta heterodimer pools -> possible tubulin-isotype dosage feedback or
microtubule-state changes -> survivor-conditioned nuclear RNA changes after
3-4 weeks -> FDR-thresholded DEG count in thalamic glutamatergic neurons.

The sign and strength of transfer from each training perturbation were:

| comparator | expected transfer to `Tubb2a` |
|---|---|
| `Tubb5`, `Tubb4b` | Same broad molecular class and same beta-tubulin subunit side; they are the strongest direct priors that an acute beta-tubulin loss in postmitotic neurons usually leaves only the self transcript detectable. |
| `Tuba1a` | Partial same-outcome prior for tubulin dosage feedback, because `Tubb2a` itself was induced after `Tuba1a` loss. I downweighted it because it perturbs the major neuronal alpha-tubulin pool and, in the same responder cell group, the direct beta-tubulins did not trigger reciprocal multi-tubulin feedback. |
| `Tuba4a` | Same alpha/beta heterodimer assembly endpoint but weaker than `Tuba1a`; its observed focal response was self plus one singleton, which argues against a broad generic structural-tubulin state. |
| `Map1b`, `Mapt`, `Stmn2`, `Kif1a`, `Kif5a`, `Kif5c`, `Spast`, `Ttll5` | Mostly counterexamples: microtubule tracks, motors, MAPs, severing, and tubulin-code genes can affect axons or polymer function, but the postnatal snRNA-seq endpoint did not convert those perturbations into FDR-level nuclear RNA programs in the focal cell group. |

I therefore predicted a nonzero but very small count. The direct evidence for
`Tubb2a` being downstream of `Tuba1a` makes a complete zero less likely than for
a random training target. Conversely, the direct `Tubb5` and `Tubb4b` results,
both self-only in this exact cell group, argue that partial acute loss of one
beta-tubulin isotype is buffered and should not be promoted to the 7-DEG
`Tuba1a` pattern. My point estimate is `1`, corresponding to the expected
self-transcript call with no confident downstream paralog crossing FDR 0.05.

## Limits

The largest uncertainty is isotype specificity. `Tubb2a`, `Tubb3`, and `Tubb4a`
were not available as training perturbations, so the closest beta-tubulin
loss-of-function observations are `Tubb5` and `Tubb4b`, not a beta-II/III
neuronal paralog. The external TUBB2A literature is dominated by human dominant
missense tubulinopathies and developmental malformation, while this dataset is
a sparse P16 mouse CRISPR loss-of-function screen observed only in recovered
NeuN-positive nuclei at P37-P44. The assay can miss altered microtubule
polymerization, axonal transport, dendritic morphology, survivor depletion, or
developmental wiring phenotypes that do not leave a stable somatic nuclear RNA
signature. Finally, the `1` prediction relies on expected recovery of a
significant self-transcript decrease; target RNA loss is not a calibrated
editing-efficiency measure, but in the same focal group the represented tubulin
comparators with nonzero counts were self-driven.
