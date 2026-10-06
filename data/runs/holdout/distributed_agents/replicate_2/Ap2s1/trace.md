# DEG-count prediction for held-out Ap2s1

## Question and resolved ambiguities

The requested target manifest contained a single held-out perturbation,
`Ap2s1`. I interpreted the endpoint as the exact training-table endpoint:
the integer number of measured genes in `151 TH Prkcd Grin2c Glut` with
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05`. I counted the
perturbed target transcript itself when it would pass the cutoff, because the
training `n_degs` file does the same; in many vesicle-cycle controls below the
only DEG is the knocked-down target RNA.

## Sources used

- Training endpoint CSV:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Training differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest:
  `[local file: 013_Ap2s1.csv]`.
- The selected same-experiment Distributed Agents semantic corpus,
  `perturbai-july-260713-sourceguard-1773-v1`. It had no direct `Ap2s1`
  Finding, but did contain AP-family, `Cltc`, `Dnm1`, `Synj1`, `Bin1`, and
  `Syp` report summaries from this Perturb-seq experiment.
- NCBI PubMed literature retrieval for AP-2 and synaptic-vesicle endocytosis.

## Computation over the training data

The focal training counts are very sparse: among 1,674 visible training
perturbations, 1,205 have `n_degs = 0`, 363 have 1-9, 63 have 10-99, and only
43 have at least 100 DEGs. I therefore treated the endpoint as a
zero/very-weak/rare-strong count rather than as a normally distributed scalar.

I queried the focal-cell rows of the parquet for AP-complex, clathrin,
synaptic-vesicle, and presynaptic endocytic comparators, then counted
`pvals_adj < 0.05` and checked which genes were significant. The non-obvious
operation was filtering the large parquet by `group_name == "151 TH Prkcd
Grin2c Glut"` and a hand-declared mechanistic target set, then ranking each
target by adjusted p-value:

```python
f = (pc.field("group_name") == "151 TH Prkcd Grin2c Glut") & \
    pc.field("gene_target").isin(targets)
tab = dset.to_table(
    columns=[
        "names", "gene_target", "logfoldchanges",
        "pvals_adj", "scores", "n_pert_matched", "n_ctrl_matched",
    ],
    filter=f,
)
```

I also ran a Distributed Agents runtime profile comparison in the same focal group over
the signed log-fold-change vectors for `Ap1b1`, `Ap1s2`, `Ap3b1`, `Ap4s1`,
`Cltc`, `Dnm1`, `Synj1`, `Bin1`, `Syp`, and related vesicle genes. Tail
overlap was computed on the leading 200 positive and negative features. The
profile check was useful mainly as a falsification step: it did not reveal a
hidden AP/endocytosis transcriptional module. Among the AP-1/AP-3/AP-4 nodes
and `Cltc`, no pair shared a significant DEG in either direction at FDR 0.05,
and `Cltc` had no negative-tail overlap with `Ap1b1`, `Ap1s2`, or `Ap4s1`
within the leading 200 genes despite being the most proximal coated-vesicle
counterexample.

## Target-specific reasoning

`Ap2s1` encodes the sigma subunit of adaptor protein complex 2, the
plasma-membrane clathrin adaptor complex. Biochemically, AP-2 contains large
alpha and beta chains, the medium AP50/mu2 chain, and the small AP17/sigma2
chain, with the small and medium chains part of the AP-2 core retained in
clathrin coats (Matsui and Kirchhausen 1990, DOI:10.1021/bi00500a011;
Kirchhausen et al. 1989, DOI:10.1073/pnas.86.8.2612). AP-2 couples clathrin
coat assembly to cargo sorting during clathrin-mediated endocytosis
(Traub 2003, DOI:10.1083/jcb.200309175; Bonifacino and Traub 2003,
DOI:10.1146/annurev.biochem.72.121801.161800).

The closest training perturbations argue for a very small nuclear RNA
footprint in this focal thalamic glutamatergic class:

| training perturbation | focal `n_degs` | focal expression-pattern evidence | interpretation for `Ap2s1` |
| --- | ---: | --- | --- |
| `Ap1b1` | 1 | The one FDR<0.05 gene was `Ap1b1` itself; no downstream focal gene passed. The Distributed Agents corpus calls `Ap1b1` broadly buffered and without a robust whole-surface neighbor. | Same adaptor-protein family and vesicle-coat biology, but AP-1 is Golgi/endosomal rather than plasma-membrane AP-2. It supports buffering of adaptor-complex LOF but is not a positive AP-2 phenocopy. |
| `Ap1s2` | 0 | No focal DEG; same-experiment corpus reports 21 of 22 measured groups had no downstream FDR<0.10 genes, with only one `Btbd8` response elsewhere. | Small-subunit AP-family comparator; its near-pan-neuronal silence is a counterweight against predicting a broad AP small-subunit stress program. |
| `Ap3b1` | 0 | No focal DEG; the corpus reports complete downstream silence in all 18 measured groups and no meaningful profile neighbor. | Another adaptor complex used for vesicle and lysosome-related trafficking; its null surface shows that losing a neuronal trafficking adaptor did not automatically make a detectable nuclear state here. |
| `Ap4s1` | 0 | No focal DEG; the corpus reports no downstream response in any recovered neuronal group. | Small-subunit adaptor comparator; useful as a boundary because even a disease-relevant AP complex can be buffered after acute P16 CRISPR. |
| `Cltc` | 3 | Only `Gabra4`, `Rbms1`, and `Ero1b` passed FDR 0.05 in the focal group. The cross-target profile comparison found no shared FDR<0.05 genes with AP-family focal signatures. | `Cltc` is the most direct coated-vesicle counterexample; it proves the assay can detect a clathrin-related response, but in the exact focal group its effect was still weak. `Ap2s1` should be no broader than this unless AP-2 loss creates a more global defect than clathrin heavy-chain loss, which the literature does not suggest. |
| `Dnm1` | 1 | The one focal DEG was self `Dnm1`. Distributed Agents reports zero non-`Dnm1` downstream genes at FDR<0.10 in 22 neuronal groups. | Dynamin is core to vesicle fission and synaptic-vesicle endocytosis. Its transcriptomic buffering is a strong argument that impaired vesicle recycling can remain almost invisible in this nuclear assay. |
| `Synj1` | 1 | The one focal DEG was self `Synj1`. Distributed Agents reports zero downstream FDR<0.10 genes in all 21 recovered groups and no meaningful nearest neighbor. | `Synj1` is a canonical phosphoinositide turnover gene for clathrin-coated vesicle uncoating; it is a close pathway comparator and was effectively downstream-null. |
| `Bin1` | 1 | The one focal DEG was self `Bin1`; the corpus reports only two isolated downstream genes over the entire 23-group neuronal surface. | A BAR-domain endocytic comparator. It did not produce the expected calcium/activity/synaptic RNA program in the same postnatal assay. |
| `Syp`, `Syn1`, `Vamp1`, `Stxbp1`, `Cplx1`, `Cplx2`, `Syn2`, `Stx1b`, `Unc13a` | 0-1 | `Syp`, `Syn1`, `Vamp1`, `Stxbp1`, and `Cplx1` each had a single focal DEG and it was the self transcript; `Cplx2`, `Syn2`, `Stx1b`, and `Unc13a` had none. | These are less direct than AP-2 but form a functional presynaptic-vesicle boundary: many genes with obvious synaptic importance were transcriptionally quiet in this thalamic group. |

External biology points the same way. AP-2 is unquestionably part of neuronal
clathrin-mediated endocytosis, and AP-2-interacting machinery helps couple
PI(4,5)P2 production and cargo selection to synaptic-vesicle retrieval
(Nakano-Kobayashi et al. 2007, DOI:10.1038/sj.emboj.7601573; Diril et al.
2006, DOI:10.1016/j.devcel.2005.12.011). But AP-2 depletion in primary
neurons slows rather than abolishes uptake of major synaptic-vesicle proteins,
with partial substitution by AP-1 (Kim and Ryan 2009,
DOI:10.1523/JNEUROSCI.5639-08.2009); conditional AP-2 loss in central
synapses impairs synaptic-vesicle reformation from endosome-like vacuoles but
does not eliminate membrane retrieval itself (Kononenko et al. 2014,
DOI:10.1016/j.neuron.2014.05.007); and an optical adaptor screen found
Stonin 2 to be a major synaptic-vesicle retrieval adaptor with AP-2 playing a
minor role at small hippocampal synapses (Willox and Royle 2012,
DOI:10.1016/j.cub.2012.05.048). Those studies are not the same sparse,
postnatal, in-vivo CRISPR context, but they make a broad immediate AP-2-loss
RNA stress state less likely than the weak self-transcript-only behavior seen
for `Dnm1`, `Synj1`, and `Syp`.

My prediction is therefore nonzero but very small: one FDR-significant gene. I
expect the most likely FDR hit to be the target transcript `Ap2s1` itself, as
for many of the one-DEG synaptic and endocytic anchors, rather than a
secondary homeostatic program.

## Limits of the reasoning

The most important limitation is that every direct AP-2 complex subunit
(`Ap2a1`, `Ap2a2`, `Ap2b1`, `Ap2m1`) was absent from the training focal
endpoint, leaving only other adaptor complexes and neighboring endocytic genes
as analogs. `Cltc` is mechanistically close but removes the coat scaffold, not
a cargo adaptor subunit; `Dnm1` and `Synj1` act at fission and uncoating, not
at AP-2 cargo selection. The external AP-2 literature is mostly cultured
neuron, synapse, or biochemical evidence and does not determine whether a
small thalamic glutamatergic population sampled 3-4 weeks after mosaic AAV
CRISPR will retain or compensate AP-2 protein. Finally, the point value of 1
depends on `Ap2s1` self-transcript depletion passing FDR in the held-out
cells; the within-dataset evidence is stronger for "no broad downstream
program" than for that exact self-transcript p-value.
