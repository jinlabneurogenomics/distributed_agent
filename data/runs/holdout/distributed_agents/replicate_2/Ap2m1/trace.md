# Trace

## Question and interpretation

The task was to predict the held-out endpoint `n_degs` for the requested genetic
perturbations in `151 TH Prkcd Grin2c Glut` cells. I treated `n_degs` as exactly
the count of measured genes with Benjamini-Hochberg-adjusted Wilcoxon
`pvals_adj < 0.05` for the focal cell group, not as a generic measure of gene
essentiality, editing efficiency, or synaptic importance.

The held-out manifest
`[local file: 012_Ap2m1.csv]`
contained one requested target:

```text
Ap2m1
```

`Ap2m1` was absent from both the training count CSV and the differential
expression parquet as a perturbation target, so there was no direct `Ap2m1`
signature to interpolate from. I therefore used perturbations of related
adaptor, clathrin, dynamin, and synaptic-vesicle endocytic genes to set the
expected response scale.

## Sources used

Internal same-experiment sources:

- The supplied focal-cell endpoint table,
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- The supplied row-level differential-expression table,
  `[local file: training_de_all_cell_groups.parquet]`.
- Distributed Agents corpus MCP, release
  `perturbai-july-260713-sourceguard-1773-v1`. This release had no direct
  target context or findings for `Ap2m1`, but did contain 49 findings over the
  in-dataset analogs I inspected.
- Distributed Agents runtime profile comparison over the focal-cell `logfoldchanges`.

External biological sources:

- NCBI PubMed literature searches and full PubMed metadata for AP-2,
  clathrin-mediated endocytosis, and neuronal synaptic-vesicle recycling.
- Functional knowledge of the AP-2 clathrin adaptor complex as a plasma-membrane
  cargo adaptor whose medium `mu2` subunit is encoded by `AP2M1`/`Ap2m1`.

Key cited literature:

- Motley et al. 2006, Molecular Biology of the Cell,
  DOI `10.1091/mbc.e06-05-0452`, PMID `17035630`: the AP-2 complex is needed
  for cargo recognition and clathrin-coated vesicle formation, and mutating the
  `mu2` YXXPhi cargo-binding or phosphorylation site impairs AP-2-dependent
  uptake.
- Kim and Ryan 2009, Journal of Neuroscience,
  DOI `10.1523/JNEUROSCI.5639-08.2009`, PMID `19321783`: strong AP-2 knockdown
  in primary CNS neurons slows, but does not abolish, synaptic-vesicle protein
  endocytosis, with AP-1 able to partially substitute.
- Kim and Ryan 2009, Journal of Biological Chemistry,
  DOI `10.1074/jbc.M109.039149`, PMID `19762466`: AP-2 `mu2` contributes to
  sorting in synaptic-vesicle endocytosis through distributed interactions
  rather than one individually indispensable motif.
- Willox and Royle 2012, Current Biology,
  DOI `10.1016/j.cub.2012.05.048`, PMID `22727701`: Stonin 2 was a major
  adaptor in a neuronal synaptic-vesicle retrieval RNAi screen, whereas AP-2
  perturbation had a comparatively minor synaptic retrieval phenotype.
- Gu et al. 2013, eLife, DOI `10.7554/eLife.00190`, PMID `23482940`: genetic
  AP2 hemicomplex data in C. elegans support partial function of the remaining
  hemicomplex after loss of either alpha or mu2.
- Kononenko et al. 2014, Neuron, DOI `10.1016/j.neuron.2014.05.007`,
  PMID `24908483`: at central synapses, clathrin/AP-2 are important for
  synaptic-vesicle reformation from endosome-like vacuoles but are not essential
  for membrane retrieval itself.

## Computational checks

I read the focal training count table and found 1,674 non-held-out
perturbations. The endpoint is highly zero-inflated in this cell group:

- 1,205 of 1,674 training perturbations had 0 DEGs.
- 1,481 of 1,674 had at most 1 DEG.
- 1,512 of 1,674 had at most 2 DEGs.
- 1,527 of 1,674 had at most 3 DEGs.
- The median was 0, the 75th percentile was 1, and the maximum was 2,677.

I then scanned only the focal-cell row groups of the large parquet and projected
the columns needed to inspect analog signatures. The non-trivial part of the
operation was the predicate pushdown:

```python
import pyarrow.compute as pc
import pyarrow.dataset as ds

dset = ds.dataset(
    "[local file: Inputs]"
    "training_de_all_cell_groups.parquet",
    format="parquet",
)

filt = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(
        ["Ap1b1", "Ap1s2", "Ap3b1", "Ap4s1", "Cltc",
         "Dnm1", "Synj1", "Syp", "Syn1", "Syn2", "Bin1"]
    )
)

table = dset.to_table(
    columns=[
        "gene_target", "names", "logfoldchanges", "pvals_adj", "scores",
        "n_pert_matched", "n_ctrl_matched",
    ],
    filter=filt,
)
```

I also ran a Distributed Agents runtime profile comparison on `151 TH Prkcd Grin2c Glut`
`logfoldchanges` for `Ap1b1`, `Ap1s2`, `Ap3b1`, `Ap4s1`, `Cltc`, `Dnm1`,
`Synj1`, `Syp`, `Syn1`, and `Bin1`, with the 1,674 training perturbations as the
eligible universe and `pvals_adj < 0.05` as the significance threshold. That
comparison found that 7 of the 10 inspected endocytosis/adaptor analogs had only
1 to 9 significant features and 3 had none. Among the inspected pairs, the
whole-profile cosines were broad, about 0.65 to 0.75, but none of the focal
pairs shared significant FDR features. I used those profile observations as a
check against over-pooling these genes into a single response module.

## Target-specific reasoning

### Ap2m1

`Ap2m1` encodes the `mu2` medium subunit of the heterotetrameric AP-2 adaptor.
The AP-2 complex recruits cargo into clathrin-coated vesicles at the plasma
membrane; `mu2` binds tyrosine-based cargo motifs and its phosphorylation state
regulates AP-2 cargo recruitment. This is a direct clathrin-mediated
endocytosis perturbation, but it is at the adaptor/cargo-sorting tier rather
than the clathrin heavy-chain tier.

No AP-2 subunit was available as a training perturbation in the focal count
table:

- `Ap2a1`: absent
- `Ap2a2`: absent
- `Ap2b1`: absent
- `Ap2m1`: held out
- `Ap2s1`: absent

The closest in-sample focal-cell perturbations and their observed counts were:

| training target | observed `n_degs` in `151 TH Prkcd Grin2c Glut` | relevance to `Ap2m1` |
|---|---:|---|
| `Ap1b1` | 1 | AP-family adaptor subunit; intracellular adaptor rather than plasma-membrane AP-2 |
| `Ap1s2` | 0 | same AP-1 adaptor family; useful AP-family low-response boundary |
| `Ap3b1` | 0 | adaptor-complex subunit; AP-3 is synaptic/endolysosomal and not AP-2 |
| `Ap4s1` | 0 | adaptor-complex subunit; useful counterexample for AP-family disruption |
| `Cltc` | 3 | core clathrin heavy chain, upstream of many coated-vesicle pathways |
| `Dnm1` | 1 | vesicle scission GTPase downstream of coated-pit assembly |
| `Synj1` | 1 | phosphoinositide phosphatase needed for synaptic-vesicle uncoating |
| `Syp` | 1 | synaptic-vesicle cargo, not an AP-2 subunit |
| `Syn1` | 1 | synaptic-vesicle cycle gene; presynaptic but not clathrin cargo sorting |
| `Syn2` | 0 | presynaptic vesicle-cycle boundary |
| `Bin1` | 1 | membrane-curvature/endocytic adaptor, a weaker AP-2 comparator |

The FDR-level features for these analogs show that most of the nonzero counts
were target-transcript-only events rather than broad downstream states:

- `Ap1b1`: 1 DEG, `Ap1b1` itself, log2FC `-0.537`,
  adjusted P `3.99e-4`.
- `Dnm1`: 1 DEG, `Dnm1` itself, log2FC `-0.712`,
  adjusted P `4.09e-25`.
- `Synj1`: 1 DEG, `Synj1` itself, log2FC `-0.583`,
  adjusted P `3.11e-7`.
- `Syp`: 1 DEG, `Syp` itself, log2FC `-1.776`,
  adjusted P `7.95e-66`.
- `Syn1`: 1 DEG, `Syn1` itself, log2FC `-0.834`,
  adjusted P `1.59e-24`.
- `Bin1`: 1 DEG, `Bin1` itself, log2FC `-0.331`,
  adjusted P `2.89e-6`.
- `Cltc`: 3 DEGs: `Ero1b`, `Gabra4`, and `Rbms1`; `Cltc` itself was down by
  log2FC `-0.418` but did not pass FDR in this focal group.
- `Ap1s2`, `Ap3b1`, `Ap4s1`, and `Syn2`: 0 DEGs.

The Distributed Agents corpus reinforced the idea that the relevant in-dataset module is
sparse at the nuclear RNA level. In release
`perturbai-july-260713-sourceguard-1773-v1`, `Ap3b1` was annotated as
pan-transcriptionally buffered across the recovered NeuN+ neuronal atlas, and
`Ap4s1` as producing no downstream transcriptomic response in any recovered
neuronal cell group. The corpus also contained a high-confidence claim that
core `Cltc` perturbation can produce a cell-type-restricted neuronal nuclear
response that is not phenocopied by adaptor-tier, `Dnm1`, `Synj1`, or other
presynaptic/endocytic neighbors, and a high-confidence claim that acute sparse
`Dnm1` and `Synj1` perturbations can leave neuronal nuclear downstream programs
undetectably flat by FDR-based snRNA-seq.

These observations make `Cltc` the upper boundary rather than the central
estimate for `Ap2m1`. Complete AP-2 loss has clear vesicle-sorting consequences,
but external neuronal work shows that AP-2 removal slows or reshapes
synaptic-vesicle retrieval without abolishing it, with AP-1 or other adaptors
providing partial compensation. In this experiment the perturbation was acute,
sparse, and mosaic; it read out nuclear snRNA-seq several weeks after P16
editing rather than electrophysiology or vesicle morphology. That context favors
a near-zero somatic transcriptomic response.

I therefore predict a nonzero count only because the target transcript itself
is likely to be detectably reduced for a ubiquitously expressed AP-2 subunit,
analogous to the `Ap1b1`, `Dnm1`, `Synj1`, `Syp`, `Syn1`, and `Bin1` self-only
calls. I do not predict a broad secondary program because all AP-family
available counterexamples were 0 or 1 DEGs, and the strongest mechanistic
counterexample, `Cltc`, still reached only 3 DEGs in this focal group.

Final point prediction: `Ap2m1 = 1`.

## Limits and uncertainty

- There was no direct `Ap2m1` entry in the Distributed Agents corpus release and no AP-2
  subunit perturbation in the training DEG-count table, so the prediction is an
  extrapolation from adjacent adaptor and endocytic genes.
- AP-1, AP-3, AP-4, clathrin, dynamin, synaptojanin, synaptophysin, synapsin,
  and BIN1 are imperfect comparators. They bound the expected response breadth
  of a trafficking perturbation in this assay, but none is a one-for-one AP-2
  `mu2` replacement.
- Several external studies used siRNA, shRNA, germline mutants, or conditional
  knockout in cultured neurons or other species. Their vesicle-recycling
  phenotypes show pathway function, but they do not measure the same acute P16
  AAV CRISPR, postmitotic mouse snRNA-seq endpoint.
- The true held-out count can jump between 0 and 1 depending on target mRNA
  abundance, guide performance, and matched perturbed-cell count. A count of 0
  would be plausible if `Ap2m1` self-depletion misses FDR; a count of 2 to 3
  would be plausible if `Ap2m1` behaves closer to `Cltc`. The within-dataset
  calibration makes a large multi-hundred-DEG response unlikely.
