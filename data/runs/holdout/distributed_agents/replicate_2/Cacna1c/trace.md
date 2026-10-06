# Cacna1c held-out DEG-count prediction

## Question and resolution of ambiguities

The requested held-out target list contains one mouse perturbation, `Cacna1c`.
I interpreted the requested value as the same endpoint stored in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: the number of measured genes
with `pvals_adj < 0.05` in the `151 TH Prkcd Grin2c Glut` contrast for that
target. That count includes the perturbed gene itself if its own transcript is
BH-significant. This matters because several weak channel-neighborhood training
rows have exactly one DEG, and that one DEG is only the self transcript.

I used the CSV counts as the authoritative endpoint for training targets and the
Parquet only to inspect which genes and directions created those counts. The
Distributed Agents same-experiment corpus often reports "downstream" counts at FDR<0.10,
excluding the target transcript, so I did not substitute those corpus counts for
the requested FDR<0.05, self-inclusive endpoint.

## Sources

- Supplied training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Supplied differential-expression Parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Requested-target CSV:
  `[local file: 026_Cacna1c.csv]`
- Distributed Agents same-experiment semantic corpus:
  `perturbai-july-260713-sourceguard-1773-v1`
- External biological literature from PubMed:
  Moosmang et al. 2005, DOI `10.1523/JNEUROSCI.1531-05.2005`;
  Zhang et al. 2006, DOI `10.1111/j.1460-9568.2006.04734.x`;
  Wheeler et al. 2008, DOI `10.1083/jcb.200805048`;
  Wang et al. 2017, DOI `10.1523/JNEUROSCI.2583-16.2017`;
  Ma et al. 2023, DOI `10.1038/s41583-023-00742-5`;
  Lee et al. 2013, DOI `10.1073/pnas.1320572110`.

## Computational checks

The held-out manifest has one row after the header:

```tsv
target_name
Cacna1c
```

The focal training endpoint has 1,674 non-held-out targets. Its distribution is
zero-inflated and heavy-tailed:

- `n_degs == 0`: 1,205 targets, 72.0%
- `1 <= n_degs < 10`: 363 targets, 21.7%
- `10 <= n_degs < 100`: 63 targets, 3.8%
- `n_degs >= 100`: 43 targets, 2.6%
- median `0`, 90th percentile `2`, 95th percentile `18`, maximum `2677`

I queried the focal Parquet rows for calcium-channel genes and selected
Ca2+/calmodulin/CREB comparators:

```sql
SELECT gene_target,
       sum(pvals_adj < 0.05) AS n_fdr05,
       sum(pvals_adj < 0.05 AND names <> gene_target) AS downstream_fdr05,
       sum(pvals_adj < 0.10) AS n_fdr10,
       min(CASE WHEN names = gene_target THEN pvals_adj END) AS self_fdr
FROM read_parquet('training_de_all_cell_groups.parquet')
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
GROUP BY gene_target;
```

The voltage-gated calcium-channel neighborhood in the focal cell group was:

| training perturbation | `n_degs` at FDR<0.05 | downstream DEGs at FDR<0.05 | focal pattern |
| --- | ---: | ---: | --- |
| `Cacna1a` | 0 | 0 | CaV2.1 pore; no self hit, minimum FDR 0.415 |
| `Cacna1d` | 0 | 0 | closest L-type CaV1.3 pore paralog; no self or downstream hit, minimum FDR 1.0 |
| `Cacna1e` | 0 | 0 | CaV2.3 pore; no self hit, minimum FDR 0.718 |
| `Cacna1g` | 12 | 11 | CaV3.1 T-type pore; self down plus `Ptprn` up, `Stmn4`, `Cpne7`, `Ly6e`, `Jun`, `Zdhhc22`, `Lrrc7`, `Irag1` down, `Iyd`, `Serpine2`, `Notum` up |
| `Cacna2d1` | 1 | 0 | only the self transcript |
| `Cacna2d2` | 0 | 0 | flat |
| `Cacnb2` | 0 | 0 | flat |
| `Cacnb4` | 1 | 0 | only the self transcript |
| `Cacng2` | 0 | 0 | flat |
| `Cacng3` | 0 | 0 | flat |

Other pathway rows that were useful for calibration:

| training perturbation | `n_degs` | downstream DEGs | focal pattern |
| --- | ---: | ---: | --- |
| `Calm1` | 14 | 13 | small thalamic module with `Rasgrp2`, `Peg3`, `Resp18`, `Vamp1`, `Coro6` up and `Atp2b1` down |
| `Calm2` | 0 | 0 | flat despite coding for the same calmodulin protein |
| `Calm3` | 1 | 0 | self transcript only |
| `Atp2b1` | 22 | 21 | activity/calcium-clearance-like genes, including `Fos`, `Nr4a1`, `Vgf`, `Cck`, and `Ptprn` |
| `Atp2b2` | 1 | 0 | self transcript only |
| `Atp2b3` | 1 | 0 | self transcript only |
| `Ppp3r1` | 9 | 8 | weak calcineurin-regulatory response, including `Pcsk1n`, `Ptprs`, `Atp2a2`, and `Coro6` |
| `Ppp3ca` | 4 | 3 | self plus `Iyd`, `Pik3r1`, `Ptpn3` |
| `Ppp3cc` | 0 | 0 | flat |
| `Camk2a` | 0 | 0 | flat |
| `Camk2b` | 1 | 0 | self transcript only |
| `Camk2g` | 0 | 0 | flat |
| `Creb1` | 10 | 9 | weak CRE-family compensation, headed by `Crem` up |
| `Crebbp` | 8 | 8 | weak and not Creb1-like |
| `Adcy1`, `Adcy3`, `Adcy5` | 0 each | 0 | flat proximal cAMP branches |
| `Grin1` | 89 | 88 | much broader NMDAR state in the focal `Grin2c+` thalamic class |

## Same-experiment corpus evidence

`Cacna1c` itself is fully absent from the Distributed Agents corpus graph:
`target_context(Cacna1c)` returned `target_found=false`, with zero findings,
claims, or explicit same-experiment references. I therefore used the corpus for
training analogs only.

Key Distributed Agents records used:

- The high-confidence CaV claim `claim:4a61b7cf2bb3e0766552` states that
  `Cacna1g` loss elicits a selective `151 TH Prkcd Grin2c Glut` response that is
  not a generic consequence of perturbing represented voltage-gated
  calcium-channel pore or auxiliary-subunit genes.
- `Cacna1g:F004` and evidence `Cacna1g:E024` specifically contrast the
  `Cacna1g` thalamic response against `Cacna1a`, `Cacna1d`, `Cacna1e`,
  `Cacna2d1`, `Cacna2d2`, `Cacnb2`, `Cacnb4`, `Cacng2`, and `Cacng3`, all of
  which had zero downstream FDR<0.10 genes in the same 151 group; the
  FDR<0.05 training endpoint agrees except that `Cacna2d1` and `Cacnb4` each
  contribute a self-transcript-only count of 1.
- `Cacna1d:F003` records the nearest measured L-type paralog as weak and
  divergent, with `Cacna1d:E018` showing 160 perturbed 151 nuclei, no
  significant self transcript, and no FDR<0.10 downstream genes in the focal
  class.
- `Calm1:F004` says represented CaM effector perturbations were mostly flat or
  divergent. This is important because a generic Ca2+/calmodulin pathway
  transfer would otherwise make `Calm1`, `Atp2b1`, `Ppp3r1`, and `Creb1` look
  like a single module; in the same experiment they produced different marker
  sets or no markers at all.
- `Creb1:F007` shows that represented PKA, CBP/p300, TrkB, CaMK, and MAPK
  perturbations did not phenocopy `Creb1`, again arguing against a simple linear
  CaV1.2 -> CaM/CaMK -> CREB count transfer.

## Biological interpretation for Cacna1c

`Cacna1c` encodes CaV1.2, an L-type high-voltage-activated calcium-channel
alpha1 pore. External literature makes it a plausible transcription-coupling
gene: Cav1.2 is required for hippocampal NMDA-receptor-independent late LTP,
MAPK activation, and CRE-dependent transcription in CA1 neurons in conditional
mouse knockouts (Moosmang et al. 2005), and local L-type Ca2+ channel activity
can be encoded by CaMKII to signal to nuclear CREB (Wheeler et al. 2008).
Densin-180 promotes Cav1.2 trafficking and nuclear signaling from excitatory
synapses (Wang et al. 2017), and a recent review places L-type channels and
NMDARs at the start of neuronal excitation-transcription coupling (Ma et al.
2023).

Those facts raised the prior that `Cacna1c` could have a nonzero response, but
the assay-specific comparisons pulled the expected count down:

1. The closest represented L-type pore, `Cacna1d`/CaV1.3, was completely silent
   in 151, including its self transcript. Zhang et al. 2006 showed that CaV1.2
   and CaV1.3 differ in surface targeting and pCREB coupling by stimulus level
   and neuronal type, so `Cacna1d` is not an interchangeable surrogate, but it
   is still the best same-family acute LoF comparator.
2. Other high-voltage CaV pores and auxiliary subunits were also flat or
   self-only. `Cacna1a`, `Cacna1e`, `Cacnb2`, `Cacna2d2`, `Cacng2`, and
   `Cacng3` had `n_degs=0`; `Cacna2d1` and `Cacnb4` had no downstream DEGs.
   Thus `151 TH Prkcd Grin2c Glut` is not generally converting CaV-subunit loss
   into an FDR-detectable nuclear program.
3. `Cacna1g` is the strong counterexample, but it is a low-voltage T-type
   Cav3.1 channel. Its thalamic role is closer to rebound burst excitability in
   thalamocortical neurons; CaV3.1 knockout alters thalamocortical firing and
   oscillatory behavior (Lee et al. 2013). The same-experiment corpus also shows
   that its 151 signature did not extend to HVA/L-type channel relatives. I
   therefore treated `Cacna1g=12` as evidence that the assay can see a
   channel-linked thalamic state, not as a quantitative predictor for CaV1.2.
4. Downstream calcium and CREB nodes gave weak, branch-specific signatures.
   `Atp2b1`, `Calm1`, `Ppp3r1`, and `Creb1` were nonzero, but their marker genes
   and signs were largely disjoint; `Calm2`, `Calm3`, `Camk2a/b/g`,
   `Ppp3cc`, `Adcy1`, `Adcy3`, and `Adcy5` were zero or self-only. This argues
   that partial acute perturbation of a Ca2+ signaling component is often
   buffered at basal snRNA-seq time scales.
5. `Grin1` produced a much larger 89-DEG focal response, but it is the obligate
   NMDAR subunit in a `Grin2c` marker class and remodeled synaptic and
   ion-channel transcripts broadly. The Distributed Agents corpus finds represented
   NMDAR subunits are themselves subunit- and cell-context-specific, so a broad
   `Grin1`-like response should not be assigned to an L-type channel by the
   shared fact of Ca2+ entry.

The point prediction is therefore the modal CaV-family outcome rather than the
`Cacna1g` thalamic exception:

```tsv
target_name	predicted_n_degs
Cacna1c	0
```

## Limits

- This is an extrapolation because the direct `Cacna1c` perturbation, its
  signature, and its same-experiment corpus report were all held out.
- `Cacna1d` is the closest assayed L-type paralog, but CaV1.2 and CaV1.3 differ
  in localization, gating range, and cell-type pCREB coupling; a true CaV1.2
  effect could be missed by transferring from CaV1.3.
- The most relevant missing channel comparators are `Cacna1b` and the T-type
  paralogs `Cacna1h` and `Cacna1i`.
- The assay was basal, juvenile, sparse, and mosaic. It did not apply a
  depolarizing or synaptic stimulus before harvest and did not measure Ca2+
  currents, channel protein, CREB phosphorylation, cell loss before recovery, or
  thalamic firing. A channel can have a strong electrophysiologic function while
  producing no durable basal nuclear RNA DEGs.
- Self-transcript significance for the held-out `Cacna1c` guide pool is
  unknowable from family membership. The closest HVA pore genes were not
  self-significant in the focal class, while several unrelated pathway genes
  were, so I did not add a predicted self-only DEG.
