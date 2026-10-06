# DEG-count prediction trace

## Question and resolved ambiguities

The held-out manifest for this run contains a single target:

```tsv
target_name
Tlx3
```

I therefore predicted one endpoint: the integer number of genes that would have
`pvals_adj < 0.05` in the held-out `Tlx3` perturbation in
`151 TH Prkcd Grin2c Glut` cells.  I treated the supplied per-gene parquet and
the focal training-count CSV as the only same-experiment quantitative evidence;
`Tlx3` itself is held out and I did not assume access to its signature or true
count.

## Sources used

- `[local file: training_de_all_cell_groups.parquet]`
  for same-experiment log2 fold changes and BH-adjusted Wilcoxon p values.
- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for the focal-cell observed training endpoint.
- `[local file: 241_Tlx3.csv]`
  for the requested target list and order.
- Distributed Agents same-experiment corpus MCP,
  `perturbai-july-260713-sourceguard-1773-v1`.  `Tlx3` was absent from this
  release, so I used it only to interpret training comparators that were present,
  chiefly `Tcf7l2` and `Rora`.
- Distributed Agents runtime `profile_neighbors`, comparing `Tcf7l2` and `Rora` signed
  151-class profiles against all 1,674 eligible training targets.
- PubMed literature for Tlx3/Lbx1/Ptf1a developmental biology:
  Cheng et al. 2004, Nature Neuroscience, DOI `10.1038/nn1221`, PMID
  `15064766`; Glasgow et al. 2005, Development, DOI `10.1242/dev.02167`,
  PMID `16291784`; Mizuguchi et al. 2006, Nature Neuroscience, DOI
  `10.1038/nn1706`, PMID `16715081`; Guo et al. 2012, Journal of
  Neuroscience, DOI `10.1523/JNEUROSCI.6301-11.2012`, PMID `22723691`; Dai et
  al. 2008, Journal of Comparative Neurology, DOI `10.1002/cne.21759`, PMID
  `18512225`; Monteiro et al. 2021, Frontiers in Cell and Developmental
  Biology, DOI `10.3389/fcell.2021.642697`, PMID `33996801`.

## Computation over the same-experiment data

The focal training counts are zero-inflated:

- training targets in the focal CSV: 1,674
- targets with `n_degs == 0`: 1,205
- targets with `n_degs > 0`: 469
- median `n_degs`: 0
- 75th/90th/95th percentiles: 1 / 2 / 18
- maximum: 2,677

I then enumerated candidate `Tlx3` comparators in the training-count CSV.  The
important focal counts were:

| comparator | `n_degs` | interpretation |
| --- | ---: | --- |
| `Lbx1` | 1 | close embryonic dorsal interneuron/Tlx3-lineage regulator, nearly silent here |
| `Ptf1a` | 0 | opposing inhibitory-vs-excitatory dorsal-horn fate regulator, silent here |
| `Gata3` | 0 | sensory/autonomic developmental TF, not active in this class |
| `Lmx1b` | 0 | expressed with Tlx3 in several excitatory hindbrain/dorsal-horn populations, silent here |
| `Pax2` | 0 | inhibitory dorsal-neuron TF downstream of Ptf1a, silent here |
| `Ebf1`, `Ebf2`, `Ebf3` | 0, 0, 0 | developmental TF controls, silent here |
| `Zic1`, `Sox2`, `Sox5` | 2, 2, 2 | weak developmental-TF counterexamples |
| `Tcf7l2` | 106 | true postnatal thalamic transcriptional response, but Wnt/TCF rather than Tlx3 biology |
| `Rora` | 278 | true postnatal thalamic nuclear-receptor response, but RORalpha rather than Tlx3 biology |

For the most relevant focal-cell profiles I filtered the parquet as:

```python
dataset.to_table(
    columns=["names", "gene_target", "logfoldchanges", "pvals_adj", "scores"],
    filter=((pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
            & pc.field("gene_target").isin(candidate_targets)),
)
```

This confirmed that the nonzero counts for the Tlx3-lineage comparators were
minimal: `Lbx1` had only `Vps35l` at FDR 0.05, while `Ptf1a`, `Lmx1b`, `Gata3`,
`Pax2`, and `Ebf1` had no focal DEGs.

The same query showed that `Tcf7l2` and `Rora` have real, broad 151-class
programs. `Tcf7l2` down-regulated `Ramp3`, `Spock3`, `Kcnc2`, `Pcsk2`, `Pcp4`,
`Plekhg1`, `Mmp15`, `Nexn`, and other thalamic neuronal genes, for 106
FDR-significant genes. `Rora` down-regulated `Prkcg`, `Adgrb1`, `Rasa4`,
`Tnnt1`, `Elmod1`, `Atp6ap2`, `Pcp4`, `Kcnc2`, `Nr1d1`, `Prkcd`, and many
other genes, for 278 FDR-significant genes. They shared 19 FDR<0.05 genes in
the focal class, including same-direction decreases of `Spock3`, `Kcnc2`,
`Pcp4`, `Atp6ap2`, `Prkcd`, and `Pcdh1`, but the overlap was partial and some
shared genes had opposite signs.

I also checked the measured `Tlx3` row across all 1,674 focal-cell training
targets. It never reached FDR 0.05 as a measured transcript; many of the largest
absolute log-fold changes had `pvals_adj = 1`, consistent with a very sparse or
undetected feature rather than a robust Tlx3-positive recovered state in the
151 matrix.

The Distributed Agents runtime profile of `Tcf7l2` and `Rora` against all focal training
targets found 203 same-cell neighbors across whole-vector and signed-tail views,
but the nearest neighbors were diffuse and not a Tlx3/dorsal-interneuron module.
I therefore used that profile only as evidence that the assay can recover broad
151-class transcriptional states; it did not supply a positive Tlx3 analog.

## Target-specific biological reasoning

### Tlx3

`Tlx3` is a homeobox selector for glutamatergic over GABAergic identity in
developing dorsal spinal neurons. Tlx1/Tlx3 loss removes dorsal glutamatergic
markers and de-represses Pax2/Gad/Viaat inhibitory markers, while ectopic Tlx3
can suppress GABAergic differentiation and promote a glutamatergic fate
(Cheng et al. 2004, DOI `10.1038/nn1221`). `Ptf1a` acts on the opposing branch:
Ptf1a-null dorsal horn precursors convert from inhibitory lineages toward
`Lmx1b`/`Tlx3` glutamatergic lineages (Glasgow et al. 2005, DOI
`10.1242/dev.02167`). `Gsh1/2` and `Ascl1` regulate the early choice between
`Tlx3`-positive excitatory and `Ptf1a`-positive inhibitory interneurons
(Mizuguchi et al. 2006, DOI `10.1038/nn1706`), and Tlx1/3 versus Ptf1a later
shape distinct receptor-gene programs in the dorsal horn (Guo et al. 2012, DOI
`10.1523/JNEUROSCI.6301-11.2012`). A direct ChIP/expression study further
showed that Tlx3 activates dILB excitatory-neuron genes and represses
alternative inhibitory dILA fate genes in embryonic dorsal spinal cord
(Monteiro et al. 2021, DOI `10.3389/fcell.2021.642697`).

The problem is that this biology maps to embryonic spinal/hindbrain sensory
circuits, not obviously to postnatal thalamic `Prkcd`/`Grin2c` glutamatergic
neurons. Dai et al. 2008 reported postnatal Lmx1b and Tlx3 colocalization in
parabrachial, nucleus of the solitary tract, medullary dorsal horn, and spinal
dorsal horn excitatory neurons, again pointing to hindbrain/spinal populations
rather than the thalamic class assayed here. In the training data, the direct
Tlx3-lineage controls agree with that context mismatch: `Lmx1b`, `Ptf1a`,
`Gata3`, `Pax2`, and the three `Ebf` targets were all zero in 151 cells, and
`Lbx1` had only a single marginal focal DEG.

The nonzero thalamic transcription factors do not rescue a positive call for
`Tlx3`. `Tcf7l2` and `Rora` prove that postmitotic, juvenile 151 cells can show
hundreds of DEGs after perturbing a maintained thalamic regulator. The internal
Distributed Agents corpus also annotated `Tcf7l2` as a sharply thalamic Wnt/TCF response
and `Rora` as a selective thalamic RORalpha response. But those are different
regulatory axes: the same corpus explicitly notes that the represented
`Tcf7l2`/`Rora` thalamic neighborhoods are only partially overlapping and are
not interchangeable phenocopies. Mechanistic transfer from either broad program
to `Tlx3` would therefore be an extrapolation unsupported by the measured
candidate controls.

I predict no FDR-significant focal genes for `Tlx3`: the prior over all training
genes is already dominated by zeros, the best mechanistic analogs from the
dorsal Tlx/Ptf1a/Lbx1 developmental network are null or singleton in the focal
class, and the broad thalamic `Tcf7l2`/`Rora` signatures are biologically
instructive counterexamples rather than a reason to expect a Tlx3 response.

Predicted `n_degs`: **0**.

## Limits of the reasoning

- `Tlx3` is absent from the training parquet, the focal training-count table,
  and the Distributed Agents same-experiment corpus, so there is no held-out signature
  to compare directly.
- The strongest external literature is embryonic and spinal/hindbrain-centered;
  applying it to a P16-to-P37/44 thalamic Perturb-seq assay is an inference
  from anatomical and developmental mismatch, not a direct experiment.
- A sparse CRISPR loss in an apparently Tlx3-low population could still produce
  a small off-axis or survivor-conditioned effect that rounds to one or a few
  DEGs. The focal training distribution makes such singleton effects common.
- `151 TH Prkcd Grin2c Glut` is a coarse cell group relative to named thalamic
  nuclei. A small Tlx3-dependent subpopulation inside that class would be
  diluted by the Wilcoxon test against all recovered matched nuclei.
- The prediction is a point estimate for an assay- and power-dependent FDR
  count, not a claim that Tlx3 is biologically unimportant in every neuronal
  lineage.
