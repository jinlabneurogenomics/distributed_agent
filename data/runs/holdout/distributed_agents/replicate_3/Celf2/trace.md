# Prediction trace for `034_Celf2`

## Question and resolved ambiguities

The held-out manifest contains one perturbation target:

| target | requested prediction |
| --- | --- |
| `Celf2` | number of genes in `151 TH Prkcd Grin2c Glut` with Wilcoxon BH-adjusted `pvals_adj < 0.05` after acute AAV CRISPR loss of function |

I interpreted `n_degs` exactly as a gene-level count in the focal cell group, not as a splicing, isoform, viability, or developmental-phenotype score. The held-out `Celf2` signature is absent from the supplied DE parquet and from the training `n_degs` CSV, so the estimate has to be transferred from non-held-out perturbations.

## Sources used

- Local endpoint table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Local DE matrix: `[local file: training_de_all_cell_groups.parquet]`.
- Distributed Agents same-experiment corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`. I queried the `Celf2` target neighborhood; this release had no direct Celf2 Claim/Finding edges.
- Distributed Agents runtime profile tools. I compared RNA-binding and spliceosome-related observed signatures in `151 TH Prkcd Grin2c Glut` using `logfoldchanges` with `pvals_adj < 0.05` as the significant-feature threshold.
- NCBI PubMed through the BioEval Literature MCP for external CELF2/CELF-family biology:
  - Dasgupta & Ladd 2011, DOI `10.1002/wrna.107`, PMID `22180311`.
  - Suzuki et al. 2012, DOI `10.1186/1471-2091-13-6`, PMID `22433174`.
  - Syed et al. 2026, DOI `10.1007/s12035-026-05933-6`, PMID `42189331`.

## Computation over the supplied data

I first read the focal training count CSV and checked the endpoint distribution. It contains 1,674 non-held-out targets; the endpoint is sparse in this cell group:

| statistic | `n_degs` |
| --- | ---: |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| 99th percentile | 436 |
| maximum | 2677 |

I then filtered the parquet to the focal group and a manually chosen RNA-processing comparator set using pyarrow row filters:

```python
ds.dataset(path).to_table(
    columns=["names", "gene_target", "logfoldchanges", "pvals_adj"],
    filter=(ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
           & ds.field("gene_target").isin(comparators),
)
```

That gave 17,259 measured genes per retrieved comparator. No CELF paralog was present as a non-held-out training perturbation, so I used observed spliceosome and neuronal/RNA-binding proteins as analogs and counterexamples.

I also pulled the focal `names == "Celf2"` row for all 1,674 training perturbations. `Celf2` itself was significantly changed by 6 perturbations; the strongest same-experiment hits were `U2af2` (`log2FC = -0.308`, `p_adj = 1.8e-6`) and `Snrnp70` (`log2FC = -0.239`, `p_adj = 0.017`). That puts `Celf2` downstream of some high-response RNA-splicing states, but it is not evidence that Celf2 loss phenocopies those core factors.

For expression-pattern evidence among the analogs, the Distributed Agents runtime pairwise comparison used signed `logfoldchanges` across the 17,259 focal measured genes. It found that the RNA-processing candidates share broad negative-tail structure more than a single tight positive program; across a 15-node RBP/splicing cohort the mean top-tail overlap coefficient was 0.128 for negative features versus 0.074 for positive features. That supported keeping the spliceosome-collapse phenotypes separate from weaker, more target-specific RBP phenotypes.

## Celf2 reasoning

### Biological prior

`Celf2` encodes a CELF/CUGBP RNA-binding protein. CELF proteins regulate pre-mRNA alternative splicing and other post-transcriptional processes, including editing, deadenylation, mRNA decay, and translation (Dasgupta & Ladd 2011). CUGBP2/CELF2 itself has alternatively spliced isoforms with different RNA-recognition behavior and different effects on model splicing reporters (Suzuki et al. 2012). A constitutive mouse `Celf2` knockout disrupts cortical architecture and neuronal maturation, with bulk RNA-seq showing widespread transcriptional dysregulation and splicing analyses showing altered exon inclusion in neurodevelopmental transcripts; `Camk2a` was highlighted as a CELF2-regulated transcript (Syed et al. 2026).

Those reports make a zero-effect prediction less attractive than for an arbitrary receptor or cytoskeletal target. However, they are imperfectly matched to this Perturb-seq endpoint. The experiment here is acute, sparse, juvenile/postmitotic, and produces modest average target-RNA depletion; the readout is 3-prime snRNA gene abundance rather than exon usage. CELF2 should therefore be weaker than knockout of a constitutive spliceosome component, because much of its direct biology can be isoform-level or translational and buffered at total-gene abundance.

### Relevant training perturbations

`Celf2` had no assayed CELF paralog in the 1,674-target training endpoint table. I therefore used three observed groups.

| group | focal training targets and `n_degs` | expression-pattern evidence | interpretation for `Celf2` |
| --- | --- | --- | --- |
| Core spliceosome / splicing execution factors | `U2af2` 828, `Rnpc3` 868, `Cdc40` 624, `Prpf6` 454, `Snrnp70` 213 | These all had hundreds of significant genes. `U2af2` and `Snrnp70` also significantly reduced the measured `Celf2` transcript in the focal cell group. In profile comparison they were connected to the broad RBP/splicing neighborhood mostly through shared downregulated tails, not through a CELF-like target-specific positive program. | They prove that the assay can detect large RNA-processing perturbations, but they are high-side counterexamples. CELF2 is a sequence-specific post-transcriptional regulator, not a U2AF heterodimer subunit, a minor spliceosome factor, or a PRP19 complex component. |
| Broad hnRNP / nuclear RBP stress responses | `Hnrnpu` 733, `Tardbp` 210, `Matr3` 149, `Hnrnpc` 122 | These produced tens to hundreds of up- and downregulated significant features. For example, `Hnrnpc` had 77 positive and 45 negative significant genes; `Tardbp` had 131 positive and 79 negative; their whole-profile Pearson correlation was 0.667, but their significant intersections were small, showing related stress neighborhoods with target-specific cores. | These are mechanistically closer than core spliceosome factors because they are RBPs rather than catalytic spliceosome parts. They still likely overestimate Celf2 because HNRNPC/HNRNPU/TARDBP/MATR3 are abundant nuclear RBPs with broad RNA-processing and chromatin/RNA-organizing functions. |
| Weak or near-null RNA-binding counterexamples | `Hnrnpa2b1` 11, `Hnrnph2` 4, `Hnrnpdl` 1, `Fmr1` 0, `Fxr1` 0, `Snrpb` 0, `Snrpn` 1, `Rbm28` 0 | Several RBPs retained smooth whole-profile correlations with strong RBP signatures but had essentially no significant program of their own. Example endpoint counts: `Hnrnpa2b1` had 7 positive and 4 negative DEGs; `Hnrnph2` had 2 positive and 2 negative; `Fmr1` and `Fxr1` had zero. | These are the lower anchor for a non-core RNA-binding target in this assay. CELF2 has stronger published developmental RNA-regulatory evidence than the zero calls, but the sparse endpoint table warns that most RBPs do not clear many gene-level FDR hits after partial acute perturbation. |

### Count choice

The zero/nonzero decision was driven mostly by external CELF2 biology: CELF2 is a neuronal RNA regulator with knockout evidence for broad transcriptome changes, so I expect at least a small focal response rather than exactly zero. The magnitude was driven mostly by the within-dataset calibration: all core spliceosome and high-abundance hnRNP analogs were too broad, while weaker RBPs in the same focal cells landed at 0 to 11 DEGs. I therefore put `Celf2` just above the weak-RBP anchors and far below `Hnrnpc`/`Matr3`/`Tardbp`.

Final point prediction: **12 DEGs**.

## Limits

- There was no direct `Celf2` expression signature, no non-held-out CELF paralog, and no Distributed Agents same-experiment corpus Claim/Finding for `Celf2`; the prediction is a cross-mechanism extrapolation.
- The best literature support includes constitutive knockout and developmental phenotypes. Those can overstate the effect of mosaic juvenile CRISPR perturbation with partial target-RNA reduction.
- Gene-level 3-prime snRNA differential expression is likely insensitive to many direct CELF2 consequences, especially exon choice, UTR regulation, mRNA localization, and translation.
- The selected RBP analogs are imperfect: `Tardbp`, `Matr3`, and hnRNP genes have ALS/stress and nuclear-architecture functions not specific to CELF2, whereas `Fmr1`/`Fxr1` are largely translational regulators and may understate a splicing regulator.
- Cell recovery and guide performance for the held-out target are unobserved here; both can shift an endpoint count near the zero/nonzero boundary.
