# Pik3ca held-out DEG-count prediction

## Question interpreted

The run asks for a point prediction of `n_degs` for each target in
`178_Pik3ca.csv`, where `n_degs` is the number of measured genes in
`151 TH Prkcd Grin2c Glut` nuclei with Benjamini-Hochberg-adjusted Wilcoxon
`pvals_adj < 0.05` after sparse postnatal CRISPR loss of the target gene.

The manifest contains one target:

| held-out target | predicted `n_degs` |
| --- | ---: |
| `Pik3ca` | 0 |

I treated the endpoint as an assay-specific breadth of the steady-state
snRNA-seq response, not as a direct statement about PIK3CA biochemical
importance, editing success, cell size, survival, or evoked phosphorylation.
The important ambiguity was pathway direction: activating `PIK3CA` alleles are
strong mTORopathy/overgrowth drivers, but this experiment assayed acute
loss-of-function in postmitotic P16-edited neurons.

## Sources used

Input data:

* `[local file: training_de_all_cell_groups.parquet]`
* `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
* `[local file: 178_Pik3ca.csv]`

Same-experiment internal resources:

* Distributed Agents corpus MCP, release
  `perturbai-july-260713-sourceguard-1773-v1`.
* Distributed Agents runtime profile comparison over the focal-cell Wilcoxon `scores`,
  written to `pik3ca_pathway_profile_compare.json` and inspected through
  `pik3ca_pathway_profile_inspect.json`.

External biology:

* Dornan and Burke 2018, Frontiers in Immunology, DOI
  `10.3389/fimmu.2018.00575`, PMID `29616047`: class IA PI3Ks contain p110
  catalytic subunits, including p110alpha/`PIK3CA` and p110beta/`PIK3CB`,
  bound to p85-family regulatory subunits and are activated downstream of
  cell-surface receptors.
* Fox, Mott and Owen 2020, Biochemical Society Transactions, DOI
  `10.1042/BST20190845`, PMID `32677674`: p85 regulatory subunits exist in
  excess over p110 catalytic subunits and can have p110-independent adaptor
  roles, a reminder that `Pik3r1`/`Pik3r2` loss is a close but imperfect proxy
  for catalytic `Pik3ca` loss.
* Huang and Manning 2009, Biochemical Society Transactions, DOI
  `10.1042/BST0370217`, PMID `19143635`: PI3K-AKT activates mTORC1 in part by
  phosphorylating and relieving TSC1/TSC2 inhibition of Rheb.
* Riviere et al. 2012, Nature Genetics, DOI `10.1038/ng.2331`, PMID
  `22729224`: de novo germline and postzygotic activating mutations in
  `AKT3`, `PIK3R2`, and `PIK3CA` cause related megalencephaly syndromes.
* Gerasimenko, Baldassari and Baulac 2023, Neurobiology of Disease, DOI
  `10.1016/j.nbd.2023.106144`, PMID `37149062`: cortical-malformation
  mTORopathies are dominated by activating mutations in `MTOR`, `AKT3`,
  `PIK3CA`, and `RHEB`, or loss of repressors such as `DEPDC5`, `TSC1`, and
  `TSC2`.

## Computation over the supplied dataset

I first verified that the manifest has exactly one requested row, `Pik3ca`, and
that the focal training-count CSV has 1,674 non-held-out perturbations with no
duplicates. The training distribution in this cell group is highly zero-heavy:
median 0, 90th percentile 2, 95th percentile 18, and maximum 2,677 DEGs.

For the pathway-specific comparison I loaded from the parquet only
`group_name == "151 TH Prkcd Grin2c Glut"` and a curated PI3K/AKT/mTOR/RAS
training set:

`Pik3cb`, `Pik3r1`, `Pik3r2`, `Akt3`, `Igf1r`, `Insr`, `Irs1`, `Rptor`,
`Mtor`, `Depdc5`, `Tsc2`, `Gsk3b`, `Mapk1`, `Strada`, and `Braf`.

This yielded 17,259 measured genes for each selected perturbation. Recomputing
`sum(pvals_adj < 0.05)` from the parquet exactly matched the training-count
CSV:

| training perturbation | focal `n_degs` | relevance to `Pik3ca` |
| --- | ---: | --- |
| `Pik3cb` | 0 | p110beta class IA catalytic paralog; closest represented catalytic PI3K neighbor |
| `Pik3r1` | 0 | p85alpha/p55alpha/p50alpha class IA regulatory subunits |
| `Pik3r2` | 0 | p85beta class IA regulatory subunit; human activating variants converge with `PIK3CA` and `AKT3` in megalencephaly genetics |
| `Akt3` | 0 | dominant brain AKT isoform, downstream of PI3K/PIP3 |
| `Igf1r` | 0 | receptor tyrosine kinase upstream of IRS/PI3K/AKT |
| `Insr` | 0 | receptor upstream of IRS/PI3K/AKT |
| `Irs1` | 0 | adaptor between insulin/IGF receptors and PI3K |
| `Rptor` | 0 | positive mTORC1 scaffold downstream of PI3K/AKT/TSC |
| `Strada` | 0 | LKB1/STRAD/mTOR-adjacent comparator |
| `Mapk1` | 0 | parallel receptor-to-MAPK branch comparator |
| `Mtor` | 2 | downstream kinase; weak loss-of-kinase signature |
| `Gsk3b` | 6 | AKT substrate and PI3K-adjacent kinase, but not class IA PI3K |
| `Braf` | 4 | parallel RAS/MAPK effector |
| `Depdc5` | 13 | GATOR1/mTORC1 negative regulator; positive control for mTORC1 de-repression |
| `Tsc2` | 86 | TSC complex mTORC1 negative regulator; broadest on-pathway positive control |

The raw expression patterns separated receptor-proximal PI3K perturbations from
the downstream mTORC1-repressor phenotype:

* `Pik3cb`, `Pik3r1`, and `Pik3r2` each had 0 significant genes in the focal
  group. Their leading signed Wilcoxon scores were all non-significant by
  adjusted p-value, and inspected mTOR/SREBP feedback genes such as `Cyp51`,
  `Hmgcs1`, `Insig1`, `Ldlr`, `Msmo1`, `Atp6v0b`, `Lamp2`, `Rragd`, `Pik3r1`,
  and `Pik3r3` had `pvals_adj == 1.0`.
* `Akt3`, `Igf1r`, `Insr`, `Irs1`, `Rptor`, `Mapk1`, and `Strada` were also
  flat at the FDR 0.05 endpoint, so the zero call is supported by more than the
  PI3K family itself.
* `Tsc2` loss produced 86 DEGs, including induced sterol/feedback markers
  `Cyp51`, `Pik3r3`, `Atp6v0b`, `Ldlr`, `Msmo1`, `Lamp2`, and `Pik3r1`.
  `Depdc5` loss produced 13 DEGs, including induced `Pik3r1`, `Ldlr`,
  `Pik3r3`, `Hmgcs1`, `Insig1`, and `Msmo1`. Thus the screen can detect the
  downstream mTORC1/SREBP-like state when a negative regulator is removed.
* `Mtor` loss gave only 2 DEGs and was negatively correlated with the
  derepressive `Tsc2` and `Depdc5` signatures, as expected for loss of a
  positive kinase rather than loss of an mTORC1 brake.

For signed pattern evidence, the runtime comparison used complete focal-cell
Wilcoxon score vectors and the same FDR column. Representative score-vector
Pearson correlations over 17,259 measured genes were:

| pair | Pearson `r` |
| --- | ---: |
| `Pik3cb` vs `Pik3r1` | -0.003 |
| `Pik3cb` vs `Pik3r2` | 0.024 |
| `Pik3r1` vs `Pik3r2` | 0.006 |
| `Pik3cb` vs `Tsc2` | 0.037 |
| `Pik3r1` vs `Tsc2` | 0.018 |
| `Pik3r2` vs `Tsc2` | -0.040 |
| `Depdc5` vs `Tsc2` | 0.288 |
| `Mtor` vs `Tsc2` | -0.195 |
| `Mtor` vs `Depdc5` | -0.151 |

These values make `Tsc2` and `Depdc5` useful boundary cases rather than direct
analogs for `Pik3ca`: their responses are in the expected same arm, but they
are induced by removing mTORC1 repressors downstream of AKT.

## Same-experiment corpus evidence

The Distributed Agents corpus contained no direct finding for held-out `Pik3ca`, but it
did contain relevant same-experiment findings for the represented neighbors:

* `Pik3cb:F001` and `Pik3cb:F002`: `Pik3cb` had no FDR-level downstream
  response across recovered neuronal classes; downstream `Tsc2` and weak
  `Mtor` signatures were detectable where `Pik3cb` and direct PI3K-core
  comparators were flat.
* `Pik3r1:F001`, `Pik3r1:F003`, and `Pik3r1:F004`: `Pik3r1` loss was
  pan-neuronally FDR-flat, `Pik3r2` and `Pik3cb` were equally buffered, and
  receptor/AKT/mTOR neighbors failed to converge on a `Pik3r1`-like signature.
* `Pik3r2:F001`, `Pik3r2:F003`, and `Pik3r2:F004`: `Pik3r2` loss was
  buffered across every recovered neuronal group, did not phenocopy human
  activating `PIK3R2` brain-overgrowth alleles, and was separated from the
  strong downstream `Tsc2` mTOR-axis transcriptional state.
* `Akt3:F003`: `Akt3`, `Pik3cb`, `Pik3r1`, `Pik3r2`, and `Rptor` were flat
  with near-zero score correlations, supporting a broader buffered class of
  upstream PI3K/mTOR nodes under basal sparse postnatal neuronal conditions.
* `Mtor:F005` and `Mtor:F006`, and `Depdc5:F005`: same-pathway membership was
  not interchangeable in this assay; negative regulators such as `Tsc2` and
  `Depdc5` exposed the detectable sterol/lysosomal program, whereas positive
  core or upstream nodes (`Pik3r1`, `Pik3cb`, `Rptor`, `Strada`) did not.

## Target-specific rationale

`Pik3ca` encodes p110alpha, a class IA PI3K catalytic subunit. In a wiring
diagram, loss of p110alpha could lower PIP3, reduce AKT activation, relieve
TSC2 repression, and dampen mTORC1. That is why I treated class IA regulatory
subunits, the p110beta catalytic paralog, receptor adaptors, `Akt3`, and the
TSC/mTOR/GATOR1 nodes as the relevant comparison set rather than using global
nearest neighbors.

The closest measured in-dataset analog is `Pik3cb`: like `Pik3ca`, it is a
p110 class IA catalytic gene, and its focal-cell count was 0. The two measured
regulatory-subunit perturbations were also 0, and they bound the same class IA
holoenzyme layer from the p85 side. The strongest in-assay counterexamples,
`Tsc2` and `Depdc5`, remove brakes downstream of PI3K/AKT and therefore force
mTORC1 in the opposite biochemical direction from `Pik3ca` loss. Their
existence shows that the dataset is not globally blind to mTOR-axis sterol
feedback, but they should not be transferred directly to an upstream positive
PI3K subunit.

External knowledge sharpens the direction call. Human `PIK3CA`,
`PIK3R2`, and `AKT3` neurodevelopmental overgrowth genetics are dominated by
activating, often mosaic, embryonic or developmental PI3K-AKT-mTOR activation.
The held-out perturbation instead removes `Pik3ca` in sparse postmitotic
neurons and is assayed weeks later by basal nuclear RNA. The represented
`Pik3r2` and `Akt3` loss-of-function perturbations already failed to reproduce
such overgrowth biology in this experimental context. I therefore predict that
`Pik3ca` will join the buffered upstream class IA/AKT group rather than the
`Tsc2`/`Depdc5` de-repressed mTORC1 group.

My point prediction is exactly zero DEGs, not just "small positive", because
all direct represented class IA components in the focal group were exactly
zero, the broader receptor-to-AKT neighborhood was exactly or nearly zero, and
the few subthreshold `Pik3cb`/`Pik3r1`/`Pik3r2` score excursions were not a
recurring sterol, lysosomal, immediate-early, or mTOR transcriptional module.

## Limits and uncertainty

The comparison is still extrapolative. `Pik3ca` itself was held out, and the
training parquet did not include `Pten`, `Tsc1`, `Rheb`, `Akt1`, `Akt2`,
`Pik3cd`, `Pik3r3`, or `Pdpk1` as focal perturbation targets, so redundancy
among catalytic isoforms and several direct PI3K branches could not be tested.
`Pik3cb` is a paralog, not an identical effector, and p85 regulatory-subunit
loss can have stoichiometric effects that differ from loss of p110alpha.

The assay also measures steady-state nuclear RNA only. A true change in PIP3,
pAKT, pS6, translation, autophagic flux, soma size, dendritic structure, or
evoked insulin/IGF responsiveness could occur without producing any FDR 0.05
DEGs. Finally, activating `PIK3CA` disease alleles act in a very different
direction and developmental context from this sparse postnatal CRISPR
loss-of-function screen, so those data were used to place boundaries around the
analogy, not to upweight a broad nonzero prediction.
