# Prediction trace for `151 TH Prkcd Grin2c Glut`

## Question

The requested held-out perturbation list in `013_Ap2s1.csv` contains exactly one mouse target:

```text
Ap2s1
```

I interpreted `n_degs` as the number of measured transcripts with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` in the `151 TH Prkcd Grin2c Glut` group after perturbing `Ap2s1`, using the same convention as the training count CSV. I did not exclude the target transcript itself, because the supplied endpoint table includes self-transcript calls such as `Dnm1`, `Synj1`, `Prepl`, and `Ap1b1` when those self rows pass FDR 0.05.

## Sources used

- Supplied endpoint table: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`; this gave exact observed `151` DEG counts for all 1,674 non-held-out training perturbations.
- Supplied DE parquet: `training_de_all_cell_groups.parquet`; I filtered this to `group_name == "151 TH Prkcd Grin2c Glut"` for AP/adaptor, clathrin, and synaptic endocytosis comparators and counted rows with `pvals_adj < 0.05`, then inspected which of those rows were self-transcripts versus downstream genes.
- Distributed Agents same-experiment corpus release `perturbai-july-260713-sourceguard-1773-v1`; I queried `target_context`, `search_claims`, and `candidate_set_topology` for `Ap2s1`, AP-adaptor, clathrin, Dnm1/Synj1, Hspa8, and adaptor-tier reports. The corpus had no direct `Ap2s1` target report, as expected for a held-out perturbation.
- Distributed Agents runtime `profile_neighbors`; I compared signed `logfoldchanges` in the focal `151` cell type across a 21-member AP/endocytosis cohort. The resulting artifact was `ap2s1_analogs_profile_neighbors.json`.
- External literature from PubMed, especially AP-2 structural and endocytic work and AP2S1 disease papers:
  - Matsui and Kirchhausen, 1990, DOI `10.1021/bi00500a011`
  - Nesbit et al., 2012, PubMed `23222959`, DOI `10.1038/ng.2492`
  - Kim and Ryan, 2009, PubMed `19321783`, DOI `10.1523/JNEUROSCI.5639-08.2009`
  - Kononenko et al., 2014, PubMed `24908483`, DOI `10.1016/j.neuron.2014.05.007`
  - Willox and Royle, 2012, PubMed `22727701`, DOI `10.1016/j.cub.2012.05.048`
  - Hannan et al., 2021, PubMed `33729479`, DOI `10.1093/hmg/ddab076`

## Computation over the supplied data

I used the training count CSV as the endpoint calibration table. The focal cell type is sparse and heavily zero-inflated: among 1,674 training perturbations, 469 were nonzero, the median was 0, the 75th percentile was 1, the 95th percentile was 18, and the mean of 14.1 was pulled upward by a small number of broad responders such as `Uba5`, `Tpr`, `Sin3a`, and `Psmb4`.

I then scanned only the focal group and a hand-built AP/endocytosis comparator set from the full parquet. The key operation was:

```python
f = (
    (ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & ds.field("gene_target").isin(candidate_targets)
)
table = dset.to_table(
    columns=[
        "names", "gene_target", "logfoldchanges",
        "pvals_adj", "n_pert_matched", "n_ctrl_matched"
    ],
    filter=f,
)
```

This gave exact focal-cell DEG identities rather than only the precomputed totals. Important `151` rows were:

| training perturbation | `151` count at FDR 0.05 | pattern in the parquet | relationship to `Ap2s1` |
|---|---:|---|---|
| `Ap1s2` | 0 | no `151` FDR gene | AP-family sigma subunit; nearest represented structural cousin but AP-1, not AP-2 |
| `Ap4s1` | 0 | no `151` FDR gene | AP-family sigma subunit; different compartment/cargo biology |
| `Ap3b1` | 0 | no `151` FDR gene | represented AP-3 complex subunit; no acute nuclear response |
| `Ap1b1` | 1 | only `Ap1b1` itself, logFC -0.537, FDR 0.000399 | AP-1 beta subunit; self-only in the focal group |
| `Dnm1` | 1 | only `Dnm1` itself, logFC -0.712, FDR 4.09e-25 | synaptic vesicle fission downstream of clathrin/AP-2 |
| `Synj1` | 1 | only `Synj1` itself, logFC -0.583, FDR 3.11e-7 | PI(4,5)P2 phosphatase and uncoating/endocytosis node |
| `Bin1` | 1 | only `Bin1` itself, logFC -0.331, FDR 3.1e-6 | BAR-domain endocytic/AD-linked comparator |
| `Prepl` | 1 | only `Prepl` itself, logFC -0.748, FDR 7.77e-10 | clathrin-adjacent PREPL/AP-1 biology |
| `Cd2ap` | 0 | no `151` FDR gene | clathrin-associated adaptor-tier comparator |
| `Sh3kbp1` | 0 | no `151` FDR gene | CIN85 adaptor-tier comparator |
| `Cltc` | 3 | `Gabra4`, `Rbms1`, `Ero1b`; no large thalamic stress signature at FDR 0.05 | core clathrin coat, broader and more disruptive than AP2S1 cargo selection |
| `Hspa8` | 9 | Hsp70/co-chaperone response including `Dnaja1`, `Hspa4l`, `Syt4`, `Hsp90aa1` | clathrin uncoating chaperone, but its `151` response is proteostasis-biased |
| `Stxbp1` | 1 | only `Stxbp1` itself | exocytic Munc18-1/SNARE-cycle positive control, not an AP-2 phenocopy |

The focal-profile comparison reinforced the split between these classes. In a 21-node cohort of AP/endocytic perturbations, `Cltc` and `Hspa8` did not behave as whole-profile neighbors of the mostly self-only AP/endocytosis nodes in `151`; `Cltc` was even isolated in the whole-profile Pearson/cosine layers of the runtime topology digest. I therefore used `Cltc` and `Hspa8` as detectability controls for trafficking and uncoating stress, not as direct numeric templates for `Ap2s1`.

## Same-experiment biological context

The Distributed Agents corpus returned no direct findings for `Ap2s1`, which is consistent with the target being completely held out.

For represented AP-adaptor perturbations, the corpus Claim `claim:97fd9a4f6d91daf7bdbb` summarized that focal responses to `Ap1b1`, `Ap1s2`, and `Ap4s1` were target-specific rather than a generic AP-family or clathrin-adjacent transcriptional state. `Ap1s2` had a single non-focal `Btbd8` event in `191 MB P MY GABA`, `Ap1b1` had a single non-focal `Napa` event in `027 NP-CT-L6b-OB Glut`, and `Ap4s1` was fully downstream-null. This lane is most directly relevant to `Ap2s1` because AP2S1 is the small sigma2 subunit of another heterotetrameric adaptor complex.

For clathrin/endocytic neighbors, the high-confidence Claim `claim:491c5c6eb002662cbefd` contrasted core `Cltc` disruption with adaptor-tier, APP-linked, `Dnm1`, `Synj1`, `Bin1`, `Cd2ap`, `Sh3kbp1`, and `Dnajc5` perturbations. The important conclusion was not that clathrin biology is invisible: `Cltc` produced a cell-type-restricted secondary response, but many AP-adjacent or endocytosis-adjacent nodes stayed flat or self-only. That argues against transferring even `Cltc`'s small `151` count of 3 onto the more cargo-adaptor-level `Ap2s1`.

For synaptic vesicle endocytosis, corpus findings for `Dnm1` and `Synj1` reported a shared FDR-based downstream-zero nuclear transcriptomic pattern in young postmitotic neuronal groups, even though those genes have severe physiological expectations. In the focal count table, both were nonzero only because their own target transcripts passed FDR 0.05. This is the strongest warning that a local vesicle-recycling defect need not become a broad nuclear DEG count in this assay.

## External biology and how it affected the prediction

AP-2 is a plasma-membrane clathrin adaptor whose core contains one alpha, beta2, mu2, and sigma2/AP2S1 subunit; the core stabilizes clathrin coats and links cargo membranes to clathrin (Matsui and Kirchhausen, 1990). Human AP2S1 Arg15 mutations disrupt recognition of dileucine-based CaSR cargo and cause familial hypocalciuric hypercalcemia type 3, and the Ap2s1 Arg15Leu mouse model showed impaired AP2 sigma2 interactions with CaSR and other AP-2 subunits while homozygotes died perinatally (Nesbit et al., 2012; Hannan et al., 2021).

Those data establish that AP2S1 matters for AP-2 function, but they do not imply a large basal somatic RNA signature after a sparse frameshift perturbation in recovered juvenile thalamic neurons. Synaptic AP-2 loss or knockdown can slow and mis-sort synaptic vesicle endocytosis without abolishing all recycling: AP-1 can partially substitute in cultured neurons, Stonin2 can dominate over AP-2 for synaptic vesicle retrieval in hippocampal synapses, and conditional AP-2 loss at CNS synapses can be bypassed for bulk membrane retrieval while clathrin/AP-2 reforms synaptic vesicles from endosome-like vacuoles (Kim and Ryan, 2009; Willox and Royle, 2012; Kononenko et al., 2014). That mechanistic displacement makes `Ap2s1` closer to the internally silent `Dnm1`/`Synj1`/AP-adaptor lane than to the `Rab7` late-endosome failure state.

## Target-specific decision

### `Ap2s1`

I predict that acute sparse `Ap2s1` loss will have no measured FDR 0.05 DEG in `151 TH Prkcd Grin2c Glut`.

The primary within-dataset analogs are the AP-family perturbations:

- `Ap1s2`: `n_degs = 0` in `151`.
- `Ap4s1`: `n_degs = 0` in `151`.
- `Ap3b1`: `n_degs = 0` in `151`.
- `Ap1b1`: `n_degs = 1`, but the only focal hit was the `Ap1b1` self-transcript.

The secondary pathway analogs were also weak in the focal group:

- `Dnm1`, `Synj1`, `Prepl`, `Bin1`, `Stxbp1`, `App`, `Cplx1`, `Sv2a`, and `Vamp1` each had a focal count of 1 driven by their own transcript rather than a downstream AP-2-like nuclear program.
- `Cd2ap`, `Sh3kbp1`, `Nsf`, `Psen1`, `Sorl1`, and `Abca7` had zero focal DEGs.
- `Cltc` had three focal downstream genes, but the all-surface corpus result places `Cltc` on a core-coat stress/downshifting axis that was not phenocopied by AP-adaptor or Dnm1/Synj1 nodes.
- `Hspa8` had nine focal genes from a cytosolic Hsp70/co-chaperone response, which is a chaperone counterinduction program rather than an AP-2 cargo-sorting program.
- `Rab7` and `Vps35` are positive controls for late endosomal/retromer disruption, not close AP-2 analogs; their `151` counts of 501 and 17 show that the assay can detect trafficking stress when it crosses the nuclear threshold.

That evidence led to a zero rather than a small nonzero count. I expect the direct cargo-sorting and synaptic-vesicle effects of AP2S1 loss to be mostly local, protein-level, or physiologic in this P16-to-P37/44 setting. The only realistic route to `n_degs = 1` would be a detectable `Ap2s1` self-transcript decrease, because I do not expect a downstream module. The three represented adaptor sigma/AP-complex comparators were not self-significant in `151`, so I did not add a point for the self row.

## Limits

No same-complex AP-2 alpha, beta2, or mu2 perturbation was present in the non-held-out training set, and the same-experiment corpus had no direct `Ap2s1` report. AP-1, AP-3, and AP-4 complexes differ in compartment and cargo specificity, so they are imperfect AP-2 surrogates.

The assay did not measure AP2S1 protein, AP-2 complex assembly, clathrin-coated-pit dynamics, cargo uptake, synaptic vesicle recycling, CaSR internalization, or electrophysiology. A zero DEG prediction is therefore only a prediction about the snRNA-seq FDR count in recovered `151` nuclei.

The 0-versus-1 boundary is fragile because the endpoint includes the target transcript. Many close negative perturbations have exactly one focal DEG solely because their own transcript passed FDR 0.05, and target self-depletion is not predictable from pathway biology alone in this sparse CRISPR design.

