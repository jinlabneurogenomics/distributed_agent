# DEG-count prediction trace

## Question and interpretation

The held-out target manifest for this run contains one gene:

```text
Cdh2
```

I interpreted the task as: predict how many measured genes will have
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` after acute AAV/CRISPR
loss of `Cdh2` in the Allen `151 TH Prkcd Grin2c Glut` neuronal cell group.
`Cdh2` itself was absent from both the parquet differential-expression table and
the focal training count CSV, so any predicted count has to be transferred from
held-in perturbations and from external biology.

The endpoint is the assay-specific number of called DEGs, not a score for the
importance of N-cadherin at synapses. I therefore treated postnatal
loss-of-function phenotypes in hippocampus/neocortex as evidence for what
`Cdh2` does biologically, but gave the highest weight to held-in single-gene
Perturb-seq behavior in the same `151 TH Prkcd Grin2c Glut` population.

## Sources

- Training endpoint table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Training DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Requested-target manifest:
  `[local file: 033_Cdh2.csv]`
- Distributed Agents corpus MCP, release
  `perturbai-july-260713-sourceguard-1773-v1`. Exact `Cdh2` target context was
  absent, as expected for this held-out target. Lexical corpus search was still
  useful for synthesized claims about represented cadherin/catenin, Wnt/catenin,
  protocadherin, and synaptic adhesion perturbations in the same experiment.
- Distributed Agents runtime profile comparison over the supplied parquet, filtered to
  `group_name == "151 TH Prkcd Grin2c Glut"`.
- PubMed literature for cadherin/catenin neuronal synapse biology.

## Dataset computations

I first read the requested manifest and confirmed that the only target, in output
order, is `Cdh2`.

From the focal training-count CSV I computed the endpoint distribution across
the 1,674 non-held-out targets in this cell group. The distribution is strongly
zero-inflated:

- median: `0` DEGs
- 75th percentile: `1` DEG
- 90th percentile: `2` DEGs
- 95th percentile: `18` DEGs
- 99th percentile: about `436` DEGs
- maximum: `2677` DEGs

I then enumerated held-in genes in the same broad mechanistic space: classical
cadherin/catenin relatives, protocadherins, neurexin/neuroligin/LRRTM adhesion
genes, DSCAM, integrins, FGF receptors, and Wnt/catenin pathway members. The
key observed counts in `151 TH Prkcd Grin2c Glut` were:

| held-in perturbation | observed n_degs | relevance to Cdh2 |
| --- | ---: | --- |
| `Ctnna2` | 0 | alpha-N-catenin; direct cadherin-actin scaffold partner |
| `Ctnna3` | 0 | alpha-T-catenin paralog; related cadherin/cytoskeletal adaptor |
| `Ctnnd2` | 1 | delta-catenin; neuronal cadherin-associated p120-family catenin |
| `Pcdh19` | 0 | cadherin superfamily/synaptic adhesion comparator |
| `Nrxn1` | 1 | synaptic adhesion comparator |
| `Nrxn2` | 0 | synaptic adhesion comparator |
| `Nrxn3` | 0 | synaptic adhesion comparator |
| `Nlgn3` | 1 | synaptic adhesion comparator |
| `Lrrtm1` | 1 | synaptic adhesion comparator |
| `Lrrtm3` | 0 | synaptic adhesion comparator |
| `Lrrtm4` | 0 | synaptic adhesion comparator |
| `Dscam` | 0 | neuronal IgSF adhesion comparator |
| `Ctnnb1` | 383 | beta-catenin; cadherin partner but also a nuclear Wnt/TCF effector |
| `Lrp6` | 4 | Wnt/beta-catenin co-receptor |
| `Tcf7l2` | 106 | Wnt/TCF transcription factor |
| `Gsk3b` | 6 | Wnt/beta-catenin pathway kinase |
| `Lrp5` | 0 | Wnt co-receptor counterexample |

For a narrower signature check, I used `profile_compare` on 17 held-in profiles:
`Ctnna2`, `Ctnna3`, `Ctnnd2`, `Ctnnb1`, `Pcdh19`, `Nrxn1`, `Nrxn2`, `Nrxn3`,
`Nlgn3`, `Lrrtm1`, `Lrrtm3`, `Lrrtm4`, `Dscam`, `Lrp5`, `Lrp6`, `Tcf7l2`, and
`Gsk3b`. The runtime compared signed `logfoldchanges` vectors across 17,259
measured genes in the focal cell group and used `pvals_adj < 0.05` only to count
FDR-level shared programs.

The profile call reproduced the endpoint counts for the cadherin/catenin
neighbors:

- `Ctnna2`: 0 significant features
- `Ctnna3`: 0 significant features
- `Ctnnd2`: 1 significant feature
- `Pcdh19`: 0 significant features
- `Ctnnb1`: 383 significant features

A direct filtered read of the parquet for the most relevant targets showed that
the single `Ctnnd2` FDR hit was the perturbed gene itself:

| perturbation | significant measured gene | log2 fold change | adjusted p-value |
| --- | --- | ---: | ---: |
| `Ctnnd2` | `Ctnnd2` | -0.456 | 2.61e-4 |

Thus the best same-complex precedent for a weak nonzero call is a singleton
self-knockdown call rather than an induced downstream state.

I also used `profile_cohort` on the 12 cadherin/synaptic-adhesion profiles
excluding the Wnt factors. Across 66 pairwise comparisons, the mean overlap
coefficient among each node's 100 most positive features was `0.041`, the mean
overlap among the 100 most negative features was `0.071`, and no pair shared a
significant positive or negative FDR-level program. This supports the corpus
claim that represented synaptic adhesion and receptor-scaffold perturbations are
largely buffered or off-axis in the postnatal neuronal nuclear transcriptome.

`Ctnnb1` was treated as a boundary case, not as the main predictor. It is part
of the cadherin complex, but the corpus contained same-experiment Wnt/catenin
claims showing that the broad `Ctnnb1` thalamic response converges with
`Tcf7l2` and the Wnt co-receptor `Lrp6`. In the focal cell group, `Ctnnb1`
shared 40 FDR-level features with `Tcf7l2` and all 4 FDR-level `Lrp6` features,
whereas it shared no FDR-level features with `Ctnna2`, `Ctnna3`, `Ctnnd2`, or
`Pcdh19`. I therefore did not transfer the 383-DEG `Ctnnb1` endpoint to `Cdh2`.

## Biological interpretation for Cdh2

`Cdh2` encodes N-cadherin, a calcium-dependent classical cadherin that forms
adhesive complexes with catenins at neuronal contacts. Cadherin/catenin
complexes regulate synaptogenesis, dendritic spine shape, and synaptic
stability; these roles have been reviewed by Goda, 2002
(`doi:10.1016/S0896-6273(02)00765-1`) and Takeichi and Abe, 2005
(`doi:10.1016/j.tcb.2005.02.002`). Postnatal N-cadherin loss in excitatory
hippocampal neurons impairs persistent LTP-associated spine enlargement
without changing baseline synapse number or baseline neurotransmission
(Bozdagi et al., 2010, `doi:10.1523/JNEUROSCI.1223-10.2010`), and late
postnatal N-cadherin ablation changes the molecular organization of adult
hippocampal synapses, including PSD95/GluA1 and inhibitory marker balance,
without gross changes in dendrite or spine number (Nikitczuk et al., 2014,
`doi:10.1002/hipo.22282`).

The held-in catenin neighbors map onto this biology. Alpha-N-catenin stabilizes
dendritic spines and links cadherins to actin (Abe et al., 2004,
`doi:10.1038/nn1212`), and delta-catenin modulates spine and synapse
morphogenesis downstream of cadherin/cytoskeletal signaling (Arikkath et al.,
2009, `doi:10.1523/JNEUROSCI.0835-09.2009`). Those are mechanistically closer
to N-cadherin than TCF/Wnt transcription factors are, and they produced 0, 0,
and 1 DEGs in this same focal group. The single `Ctnnd2` hit was self, which
argues for little or no downstream nuclear RNA program even when target RNA
knockdown is detectable.

The Wnt/beta-catenin branch sets an important upper boundary but is a poor
positive analog. Beta-catenin participates in cadherin complexes at synapses,
for example in presynaptic cadherin/catenin/p140Cap spine stabilization
(Li et al., 2017, `doi:10.1016/j.neuron.2017.05.022`), yet `Ctnnb1`,
`Lrp6`, and `Tcf7l2` responses in this dataset reflect a Wnt/TCF-associated
thalamic transcriptional state rather than generic cadherin adhesion loss.
`Cdh2` perturbation should remove a cell-surface adhesion component and reduce
cadherin-associated beta-catenin locally, but it is not expected to phenocopy
loss of nuclear beta-catenin or TCF7L2.

## Target-specific prediction

### Cdh2

**Decision:** predict `0` DEGs.

**Within-dataset evidence.** The closest assayed scaffold/cadherin analogs were
flat: `Ctnna2` had 0 DEGs, `Ctnna3` had 0, `Ctnnd2` had only its own transcript,
and `Pcdh19` had 0. Wider synaptic adhesion comparators were also almost all
zero or singleton: `Nrxn1` 1, `Nrxn2` 0, `Nrxn3` 0, `Nlgn3` 1, `Lrrtm1` 1,
`Lrrtm3` 0, `Lrrtm4` 0, and `Dscam` 0. This pattern is stronger evidence than
the large `Ctnnb1` count because the latter belonged to the Wnt/TCF boundary
module shared with `Tcf7l2`, not to the nontranscriptional cadherin scaffold
neighbors.

**External biology.** N-cadherin is important for synapse and spine stability,
but the strongest published phenotypes after postnatal loss are structural,
plasticity, or protein-composition phenotypes. Those need not become a broad
steady-state snRNA-seq response three to four weeks after sparse mosaic CRISPR
in postmitotic neurons. That expectation matches the held-in adhesion genes.

**Approximate count.** The only plausible nonzero mode is a singleton `Cdh2`
self-DEG analogous to `Ctnnd2`; however, two alpha-catenin scaffold partners and
`Pcdh19` did not even reach a self-hit in the same cell group. I therefore chose
the modal count among the closest analogs, `0`, rather than rounding up to a
rare singleton.

## Limits and extrapolations

- No exact `Cdh2` profile or DEG count was available in the supplied training
  data or the Distributed Agents perturbation-centered corpus. The prediction is an
  extrapolation from cadherin/catenin and synaptic adhesion neighbors.
- `Ctnna2`, `Ctnna3`, and `Ctnnd2` are intracellular adaptors, not a direct
  extracellular classical cadherin receptor. They are the best represented
  complex-adjacent perturbations, but they are imperfect analogs.
- Postnatal conditional mouse knockouts and in vitro knockdown papers often
  assay hippocampus or cortex with structural/electrophysiological endpoints,
  while the requested readout is a sparse, acute, thalamic single-nucleus RNA
  count. I used those papers to interpret mechanism, not to infer DEG counts
  directly.
- `Ctnnb1` demonstrates that this focal cell group can produce a broad
  catenin-related transcriptional response, but it also demonstrates the risk of
  conflating adhesive catenin biology with Wnt/TCF nuclear signaling.
- A prediction of zero does not mean N-cadherin is irrelevant or unedited. It
  means I do not expect any measured transcript, including `Cdh2` itself, to
  survive BH correction at FDR 0.05 in this assay.

