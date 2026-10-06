# Trpv4 held-out DEG-count prediction

## Question interpreted

The requested scalar is the number of genes that would pass
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` after acute AAV-CRISPR
loss of the held-out gene in `151 TH Prkcd Grin2c Glut` thalamic
glutamatergic nuclei.

The manifest for this run contains one target:

```text
Trpv4
```

`Trpv4` was absent from both the training differential-expression parquet and
the focal training count CSV, so no `Trpv4` endpoint count or expression
signature was used.

One typo-like ambiguity was resolved by the dataset context: `TH` in
`151 TH Prkcd Grin2c Glut` is thalamus, not tyrosine hydroxylase, and the group
is a glutamatergic neuronal class.

## Sources

Internal same-experiment inputs and tools:

- `training_de_all_cell_groups.parquet`: focal and cross-perturbation
  log-fold-change and adjusted-p-value profiles for non-held-out perturbations.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed `n_degs` for
  1,674 non-held-out perturbations in the focal class.
- Distributed Agents runtime profile-comparison tools:
  `profile_neighbors`, `profile_compare`, and `profile_inspect`, run only on
  visible non-held-out expression signatures.
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`, used for qualitative reports on
  the trained TRP-channel perturbations. This corpus is a curated semantic
  layer over the same Perturb-seq experiment; it is not independent
  replication.
- Distributed Agents mouse gene-annotation analog store, used to nominate
  training-available genes related to `Trpv4` through Reactome, Gene Ontology,
  KEGG, STRING physical v12.0, and local functional-class annotations.

External biological references:

- Reactome mouse pathway `R-MMU-3295583`, "TRP channels", grouped `Trpv4` with
  trained TRP-channel analogs including `Trpv1`, `Trpa1`, `Trpm3`, and
  `Trpm7`.
- Gene Ontology terms in the local annotation store, especially
  `GO:0005261` monoatomic cation channel activity and `GO:0005262` calcium
  channel activity.
- Liedtke et al. 2000, Cell, DOI `10.1016/S0092-8674(00)00143-4`,
  PMID `11081638`: cloned VR-OAC/TRPV4 as a hypotonicity-gated cation channel
  expressed in osmosensory neurosensory cells.
- Strotmann et al. 2000, Nature Cell Biology, DOI `10.1038/35036318`,
  PMID `11025659`: independently described OTRPC4/TRPV4 as a
  Ca2+-permeable nonselective cation channel activated by extracellular
  osmolarity decreases.
- Plant and Strotmann 2007, Handbook of Experimental Pharmacology,
  DOI `10.1007/978-3-540-34891-7_11`, PMID `17217058`: reviewed TRPV4 as a
  homotetrameric, outwardly rectifying, Ca2+-permeable cation channel activated
  by swelling, heat, mechanical stimulation, endocannabinoids, arachidonic-acid
  metabolites, and phorbol esters.
- Filosa et al. 2013, Journal of Cardiovascular Pharmacology,
  DOI `10.1097/FJC.0b013e318279ba42`, PMID `23107877`: reviewed that brain
  TRPV4 is prominent in astrocytic endfeet around vessels and can regulate
  vascular tone.
- Shibasaki et al. 2015, Biochemical and Biophysical Research Communications,
  DOI `10.1016/j.bbrc.2015.01.087`, PMID `25637662`: showed developmentally
  regulated postsynaptic clustering of TRPV4 in hippocampal neurons, supporting
  neuronal roles but in a different neuronal population from the thalamic focal
  class assayed here.

## Computational calibration

### Training count distribution

The focal training count CSV contained 1,674 perturbations:

- 1,205 / 1,674 had `n_degs = 0`.
- median = 0.
- 75th percentile = 1.
- 90th percentile = 2.
- 95th percentile = 18.
- maximum = 2,677.

Thus a zero prediction is common in this endpoint, and a target needs either a
strong direct analog or a stronger biological reason to leave the zero/one
background.

### Relevant counts

The closest direct TRP-channel perturbations in the trained endpoint were all
zero in the focal cell group:

| target | focal n_degs | role |
| --- | ---: | --- |
| `Trpv1` | 0 | closest trained vanilloid TRP-channel member |
| `Trpa1` | 0 | sensory TRP channel in the same Reactome TRP module |
| `Trpm3` | 0 | calcium-permeable TRP channel in the same Reactome TRP module |
| `Trpm7` | 0 | TRP channel in the same Reactome TRP module |

Osmotic and calcium-channel boundaries were also quiet:

| targets | focal n_degs |
| --- | ---: |
| `Pkd1`, `Osmr` | 0, 0 |
| `Kcnn2`, `Kcnn3`, `Kcnma1` | 0, 0, 1 |
| `Kcnq1`, `Kcnq2`, `Kcnq3` | 0, 1, 1 |
| `Cacna1a`, `Cacna1d`, `Cacna1e`, `Cacna1g`, `Cacna2d1`, `Cacna2d2`, `Cacnb2`, `Cacnb4`, `Cacng2`, `Cacng3` | 0, 0, 0, 12, 1, 0, 0, 1, 0, 0 |
| `Gria1`, `Gria2`, `Gria3` | 0, 0, 0 |
| `Grin1`, `Grin2a`, `Grin2b`, `Grin2d`, `Grin3a` | 89, 1, 2, 0, 0 |

`Grin1` and, much more weakly, `Cacna1g` demonstrate that ion-channel
perturbations can be visible in `151 TH Prkcd Grin2c Glut`. They are not good
point donors for `Trpv4`, though: `Grin1` is the obligatory NMDA receptor
subunit and had its own curated Grin-subunit non-phenocopy report in the
Distributed Agents corpus, while `Cacna1g` was singled out by the same corpus as a
narrow thalamic exception whose response did not phenocopy other voltage-gated
calcium-channel perturbations.

### Focal parquet slice

I filtered the parquet to the focal group and selected the closest analogs and
counterexamples:

```python
filter = (
    field("group_name") == "151 TH Prkcd Grin2c Glut"
) & field("gene_target").isin(
    ["Trpv1", "Trpa1", "Trpm3", "Trpm7", "Pkd1",
     "Cacna1a", "Cacna1g", "Grin1", "Grin2b", "Kcnma1", "Kcnq2"]
)
columns = [
    "names", "gene_target", "logfoldchanges",
    "pvals_adj", "n_pert_matched", "n_ctrl_matched",
]
```

This pulled 189,849 focal rows, 17,259 genes for each of 11 perturbations.
Matched perturbed nucleus counts were adequate for a sparse call in this
endpoint: `Trpv1` 187, `Trpa1` 191, `Trpm3` 154, `Trpm7` 81, `Pkd1` 136,
`Cacna1g` 264, and `Grin1` 247, all against 23,679 matched controls.

The `Trpv1`, `Trpa1`, and `Trpm7` focal profiles had minimum adjusted p-values
of exactly 1.0; `Trpm3` had a best adjusted p-value of 0.1458. `Pkd1` was also
flat with best adjusted p-value 1.0. In the same filtered read, the positive
controls recovered the expected significant genes: `Cacna1g` had 12
FDR-significant features and `Grin1` had 89.

### Profile-space inspection

I compared 13 visible profiles with `profile_compare` in exactly the focal
context:

```text
Trpv1, Trpa1, Trpm3, Trpm7, Pkd1,
Kcnn2, Kcnn3, Kcnma1, Kcnq2, Cacna1a, Cacna1g, Grin1, Grin2b
```

The comparison used `logfoldchanges` over the focal profiles with
`pvals_adj < 0.05` as the significance call. Eight of the 13 anchors had zero
significant features; `Kcnma1`, `Kcnq2`, and `Grin2b` had one to two; `Cacna1g`
had 12; and `Grin1` had 89.

Among the direct TRP anchors and `Pkd1`, every pair had zero significant genes
on both sides and therefore no FDR-overlap evidence. Their whole-profile
Pearson correlations sat in a narrow moderate band, about 0.66 to 0.69 between
the TRP anchors, which is consistent with a shared low-signal baseline but not
with a distinctive reproducible TRP tail. The top raw log-fold-change tails of
the zero-DEG TRP perturbations were dominated by non-significant, often
idiosyncratic genes with adjusted p-values of 1.0, so I did not use them as
directional biological evidence.

The eligible-neighbor pass over all 1,674 training profiles likewise did not
find a tight TRP-specific expression module: the nearest whole-profile
neighbors for `Trpv1` and `Trpa1` were unrelated genes such as `Tcf12`,
`Ttll5`, `Eif4g1`, `Mest`, and `Cd46`, while the same-experiment corpus had
already curated these TRP nearest-neighbor relationships as near-zero,
nonconvergent neighborhoods.

## Target-specific reasoning

### `Trpv4`

`Trpv4` encodes a Ca2+-permeable, nonselective TRP vanilloid channel activated
by hypotonicity, swelling/mechanical stimuli, warm temperature, endogenous
lipids, and phorbol ester agonists. The outside literature makes it a plausible
signaling channel, but the signaling is stimulus- and cell-state-dependent:
classic TRPV4/VR-OAC work tied it to osmotic and mechanosensory Ca2+ entry
rather than to constitutive transcription-factor or chromatin regulation
(Liedtke et al. 2000; Strotmann et al. 2000; Plant and Strotmann 2007).

The most local in-dataset analogs point to no focal response:

- Reactome `R-MMU-3295583`, "TRP channels", nominated trained `Trpv1`,
  `Trpa1`, `Trpm3`, and `Trpm7` as the strongest `Trpv4` analogs.
- All four had `n_degs = 0` at FDR 0.05 in `151 TH Prkcd Grin2c Glut`.
- The filtered parquet showed no near-threshold focal effect for those four
  genes: `Trpv1`, `Trpa1`, and `Trpm7` had best adjusted p-value 1.0, and
  `Trpm3` had best adjusted p-value 0.1458.
- In the Distributed Agents same-experiment corpus, `Trpa1` was a corrected null in
  every recovered central neuronal group; `Trpm3` was nearly blank across 22
  groups; `Trpm7` produced a single robust hit outside the focal thalamic
  group; and `Trpv1` produced only two corrected downstream genes over 22
  groups. Corpus Claims further summarized that represented TRP-channel and
  nociceptor-associated perturbations did not form a shared basal
  central-neuron transcriptional module.

The broader counterexamples did not justify lifting the prediction above zero.
`Pkd1` was an osmo-/mechanosensory calcium-channel comparator and had
`n_degs = 0`; the Pkd1 corpus report called it fully buffered across the
postnatal neuronal atlas. `Kcnma1`, `Kcnn2`, `Kcnn3`, `Kcnq2`, and `Kcnq3`
tested links from Ca2+ entry to calcium-activated or cationic excitability
control and were zero or singleton. Voltage-gated calcium-channel alpha and
auxiliary subunits were also mostly zero or singleton; `Cacna1g = 12` was a
clear exception, but the same-experiment corpus explicitly reported that it
did not phenocopy other represented voltage-gated calcium-channel
perturbations. Finally, `Grin1 = 89` confirms that thalamic glutamatergic cells
can mount a channel-loss transcriptome, but the NMDA receptor is a core
synaptic coincidence detector, and the corpus reported that other
Grin-subunit knockouts did not phenocopy `Grin1`.

The experimental context also pushes toward a null call. Many well-established
TRPV4 functions are in vascular cells, astrocytic endfeet, peripheral sensory
neurons, kidney, and other non-neuronal or non-brain contexts; the supplied
assay used NeuN-enriched brain nuclei and under-samples vascular and glial
cells. Shibasaki et al. showed neuronal postsynaptic TRPV4 in hippocampal
neurons, so I am not assuming that TRPV4 is absent from all neurons. I am
instead assuming that an acute, mosaic, 3- to 4-week partial loss in an
unstimulated postnatal thalamic glutamatergic population is unlikely to
produce a stable FDR-significant transcriptome when the trained TRP-channel
perturbations did not.

Prediction: `Trpv4` should have no measured genes passing FDR 0.05 in this
focal class, so the point estimate is `0`.

## Limits

- There is no held-out `Trpv4` expression signature in the input data, so the
  prediction extrapolates from trained TRP and calcium-channel perturbations.
- `Trpv1`, `Trpa1`, `Trpm3`, and `Trpm7` are analogs by pathway and channel
  class, not true redundant paralogs of `Trpv4`. TRPV4 has distinct gating and
  tissue biology, especially osmo-/mechanosensory and vascular/astrocytic
  roles.
- The TRP-channel training signatures are transcriptionally flat. Flat
  profiles calibrate response breadth well for this endpoint, but they cannot
  reveal what a small, real, sub-FDR TRPV4 module would look like.
- `Trpm7` had only 81 matched perturbed nuclei in the focal class, so its
  individual zero is somewhat less powered than the others; the prediction does
  not rest on `Trpm7` alone.
- External TRPV4 studies often use germline knockouts, pharmacological agonists
  or antagonists, peripheral neurons, astrocytes, vascular cells, kidney, or
  injury/osmotic stimulation. Those contexts are informative about function but
  are imperfect proxies for sparse postmitotic CRISPR loss in recovered
  NeuN-positive thalamic nuclei.
- DEG count is power- and assay-dependent. A prediction of zero means no gene
  is expected to pass this screen's FDR 0.05 threshold, not that TRPV4 is
  biologically irrelevant or unedited.
