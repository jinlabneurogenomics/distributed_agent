# Kcnq5 DEG-count prediction trace

## Question and resolved ambiguity

The requested held-out perturbation list contains one target:

```text
Kcnq5
```

I interpreted `n_degs` exactly as in the supplied training CSV: the count of measured genes with `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut`, including the perturbed target's own transcript if that self row passes FDR. This matters because the closest retained KCNQ perturbations in the focal group have a single strict DEG that is the self-transcript, while their non-self effects are absent or only just above the cutoff.

## Sources used

- Differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Focal training-count CSV:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Requested-target manifest:
  `[local file: 118_Kcnq5.csv]`
- Same-experiment semantic corpus: Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`
- Run-local profile analysis: Distributed Agents runtime `profile_neighbors` and `profile_compare` over the focal-cell Wilcoxon-score vectors, with the 1,674 training targets as the eligible universe
- Literature from PubMed:
  - Brown and Passmore 2009, British Journal of Pharmacology, DOI `10.1111/j.1476-5381.2009.00111.x`, PMID `19298256`
  - Cooper 2011, Seminars in Cell & Developmental Biology, DOI `10.1016/j.semcdb.2010.10.001`, PMID `20940059`
  - Gilling et al. 2013, Frontiers in Genetics, DOI `10.3389/fgene.2013.00054`, PMID `23596459`
  - Huang and Trussell 2011, Nature Neuroscience, DOI `10.1038/nn.2830`, PMID `21666672`
  - Fidzinski et al. 2015, Nature Communications, DOI `10.1038/ncomms7254`, PMID `25649132`
  - Soh et al. 2022, PNAS, DOI `10.1073/pnas.2117640119`, PMID `35320039`
  - Wei et al. 2022, Journal of Neurophysiology, DOI `10.1152/jn.00509.2021`, PMID `35583973`

## Computational checks

The manifest check found exactly one requested target, `Kcnq5`, and the focal
training-count file confirmed that `Kcnq5` was absent from the 1,674 training
targets.

The training-count distribution is sparse: 1,205/1,674 training perturbations
have `n_degs = 0`, 276 have `n_degs = 1`, the median is 0, and the 75th
percentile is 1. The Kv7 and potassium-channel neighborhood was similarly
sparse in `151 TH Prkcd Grin2c Glut`:

| training target | focal `n_degs` |
| --- | ---: |
| `Kcnq1` | 0 |
| `Kcnq2` | 1 |
| `Kcnq3` | 1 |
| `Kcna1`, `Kcna2`, `Kcnb1`, `Kcnb2`, `Kcnc1`, `Kcnd3`, `Kcnh1`, `Kcnh5`, `Kcnj6`, `Kcnn2`, `Kcnn3`, `Kcnt1`, `Kcnt2`, `Kctd16`, `Kctd8` | 0 |
| `Kcnab2`, `Kcnc2`, `Kcnc3`, `Kcnma1` | 1 |
| `Kctd1` | 2 |

Other excitability comparators were also usually 0 to 2 DEGs in the focal
group: `Scn1a`, `Scn2a`, `Scn8a`, `Gabra1`, `Gabrg2`, `Gabbr1`, `Gabbr2`,
`Hcn2`, `Cacnb4`, and `Grin2a` each had 1 or 2, while `Kcnb1`, `Cacna1a`,
`Cacna1d`, `Cacna1e`, `Hcn1`, `Gria1`, `Gria2`, and `Gria3` were 0. `Grin1`
was the main high-count channel counterexample at 89 DEGs, but its same-
experiment corpus report tied the 151 signature to a trafficking/stress axis
rather than to a Kv7-like channel-compensation program.

To inspect exact focal expression rows without scanning the full 616 million
row parquet, I read the Parquet footer, identified row groups whose
`group_name` min/max values bracketed `151 TH Prkcd Grin2c Glut`, and pulled
only row groups 546-580. In the focal rows:

- `Kcnq1`: `n_pert_matched = 280`, no significant row; the smallest Kcnq1
  focal adjusted p-values were all 1.0.
- `Kcnq2`: `n_pert_matched = 283`, `n_ctrl_matched = 23679`, exactly one
  strict FDR row:
  `Kcnq2` itself, log2FC `-0.775903`, Wilcoxon score `-11.896856`,
  `pvals_adj = 2.12096e-28`.
  The strongest non-self row was `Agap2`, log2FC `0.283634`, score `4.530136`,
  `pvals_adj = 0.05086725`, just above the requested `0.05` endpoint.
- `Kcnq3`: `n_pert_matched = 211`, `n_ctrl_matched = 23679`, exactly one
  strict FDR row:
  `Kcnq3` itself, log2FC `-0.379112`, Wilcoxon score `-5.061797`,
  `pvals_adj = 0.007168`.
  The strongest non-self rows, such as `Sv2b`, `Egr1`, and `Rimoc1`, had
  `pvals_adj = 0.86601001` or worse.

The runtime profile comparison used the focal Wilcoxon `scores` vector for
`Kcnq1`, `Kcnq2`, and `Kcnq3` and compared them with selected peers and the
full eligible 1,674-target training universe by whole-profile Pearson/cosine
and signed top-tail overlap. It found one significant feature for `Kcnq2` and
one for `Kcnq3`, matching the two self rows above, and no significant feature
for `Kcnq1`. Score-vector similarities around the KCNQ anchors were very weak:
for example, `Kcnq2` versus `Kcnq3` had Pearson `0.0409` and cosine `0.0444`;
`Kcnq2` versus its nearest selected broad peer, `Atp1a3`, had Pearson `0.0761`;
and `Kcnq3` versus `Atp1a3` had Pearson `0.0711`. Broad `Agap2`-linked
neighbors from the corpus, including `Rnpc3`, `Sin3a`, `Zbtb7a`, `Ctnnb1`,
`Psmb4`, `Psmc1`, `Elp1`, `Elp2`, and `Tpr`, have 80-1,768 focal DEGs and
near-zero KCNQ correlations, so I treated them as evidence that a single shared
near-threshold feature is not enough to transfer a large count to `Kcnq5`.

## Same-experiment biological analogs

### Primary analogs: `Kcnq2` and `Kcnq3`

`KCNQ5/Kv7.5` is in the neuronal Kv7/M-current channel family. Brown and
Passmore 2009 review the neuronal Kv7.2-Kv7.5 channels as noninactivating
voltage-gated K+ channels that control resting excitability through the
M-current, and Cooper 2011 describes the more specialized axonal targeting of
Kv7.2/Kv7.3 channels. KCNQ5 is mechanistically connected to both subunits:
Soh et al. 2022 showed that KCNQ2 and KCNQ5 can form native brain channel
complexes independent of KCNQ3, and Gilling et al. 2013 showed functional
KCNQ3/KCNQ5 heteromeric channels. These facts make the retained `Kcnq2` and
`Kcnq3` perturbations the best training analogs for a held-out `Kcnq5` LoF.

In the actual same-experiment data, both analogs were very narrow in the focal
cell type. `Kcnq2` and `Kcnq3` each produced exactly one focal DEG at
`pvals_adj < 0.05`, and that DEG was the target transcript itself. The
Distributed Agents corpus report for `Kcnq2` notes that across all 23 measured classes
there were only three non-self calls at FDR `< 0.10`, with the 151
`Agap2` response sitting at FDR `0.0509`. The `Kcnq3` report is even flatter:
only two downstream FDR `< 0.10` gene-by-cell-group calls across 22 recovered
classes, no recurrent immediate-early response, no ISR/UPR or heat-shock
module, and no voltage-gated channel compensation including no `Kcnq5`
compensation. In 151 specifically, `Kcnq3`'s only strict DEG was its own
transcript.

### Boundary analog: `Kcnq1`

`Kcnq1` is the Kv7.1 family member, but external literature places its major
roles in cardiac IKs, inner-ear, and epithelial physiology rather than in the
neuronal M-current branch. In the focal training data it had 0 DEGs, and the
same-experiment corpus reports a pan-neuronal null: 0 non-self genes at FDR
`< 0.10` across all 23 recovered cell groups. I therefore used `Kcnq1` only as
a family-specific negative boundary. Its null says the assay does not turn
every KCNQ-family perturbation into a transcriptional response, but it is less
biologically close to `Kcnq5` than `Kcnq2` or `Kcnq3`.

### Counterexamples

Some 151 signatures with a weak overlap to the `Kcnq2` `Agap2` feature were
large: `Atp1a3` had 80 DEGs in the supplied strict training endpoint, `Ctnnb1`
383, `Psmc1` 430, `Elp1` 645, `Psmb4` 742, `Zbtb7a` 841, `Rnpc3` 868,
`Sin3a` 1433, and `Tpr` 1768. These are RNA processing, proteostasis, Wnt, or
ion-gradient perturbations with broad focal transcriptional states. Because
their whole-profile correlations to `Kcnq2`/`Kcnq3` were near zero and their
counts are orders of magnitude above the KCNQ anchors, I rejected them as
quantitative predictors for `Kcnq5`.

`Grin1` is another counterexample: it is a neuronal ion-channel subunit and has
89 focal DEGs, but it is an obligatory NMDA receptor subunit and the corpus
links its 151 signature to Vps54/Rab7/Wdfy3-like membrane-trafficking or stress
states rather than to the Kv7 M-current channel family.

## Kcnq5 prediction

I predict a nonzero but minimal response: `1` DEG.

Within-dataset evidence dominates the count scale. The two closest represented
neuronal Kv7 perturbations, `Kcnq2` and `Kcnq3`, were both single-DEG events in
the focal class, with no strict FDR downstream genes. Their corpus summaries
also indicate sparse outputs across the whole screen rather than a stable
Kv7-family transcriptional module. The broader K-channel and voltage-channel
training rows were mostly zero or one DEG.

External biology pushes `Kcnq5` closer to `Kcnq2`/`Kcnq3` than to the
`Kcnq1` null. Kv7.5 is a neuronal M-current subunit with direct roles in
resting membrane potential and transmitter release in the rat calyx of Held
(Huang and Trussell 2011), hippocampal inhibition and network oscillations in
mouse Kcnq5 dominant-negative models (Fidzinski et al. 2015), documented
KCNQ2/KCNQ5 association in native brain channels (Soh et al. 2022), and
loss-of-function mouse seizure phenotypes in a human KCNQ5 developmental
encephalopathy study (Wei et al. 2022). That makes a completely invisible
perturbation less likely than one that at least scores the target transcript.

I did not predict any additional downstream DEGs because Kv7 perturbation
changed the nuclear RNA state very weakly in the assay that actually matches
the requested endpoint. In this sparse postnatal mosaic setting, channel loss
can alter excitability at the membrane without inducing a persistent resting
snRNA immediate-early, stress, or compensatory channel program three to four
weeks later.

## Limits

The main extrapolation is target expression. `Kcnq5` itself was held out, so the
training parquet and Distributed Agents corpus provide no `Kcnq5` perturbation row, no
on-target `Kcnq5` log fold change, and no recovered `Kcnq5` cell count. The
prediction of one DEG assumes that `Kcnq5` is expressed enough in the recovered
`151 TH Prkcd Grin2c Glut` nuclei for its own transcript to be reduced and pass
FDR, as happened for `Kcnq2` and `Kcnq3`. If Kv7.5 expression is lower in this
thalamic class, the true count could easily be 0. Conversely, if Kv7.5 has a
more central role than Kv7.2/Kv7.3 in these exact neurons, a small non-self
Agap2/Egr1-like response could push the count above 1. Nothing in the retained
same-experiment data supports a broad response comparable to `Grin1`,
proteasome, RNA-processing, or transcription-factor perturbations.
