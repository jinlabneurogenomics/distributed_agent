# Prediction trace for 151 TH Prkcd Grin2c Glut

## Question and scope

The requested held-out target list contains one perturbation, `Supt16`.
I interpreted `n_degs` as the count of measured genes in the `151 TH Prkcd Grin2c Glut`
cell group with Wilcoxon Benjamini-Hochberg adjusted `pvals_adj < 0.05`
after acute AAV-CRISPR loss of the target gene.

I resolved two ambiguities as follows.

- The hidden endpoint is a cell-group-specific count in this assay, not a
  direct measure of biological essentiality or the size of the primary edit.
- The useful training examples are therefore same-assay perturbations whose
  post-P16 neuronal RNA signatures bound the expected response of a FACT
  histone-chaperone perturbation. I did not treat all chromatin genes as
  equivalent analogs.

I verified that `Supt16` is absent from both training inputs: it has no row in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` and no `gene_target ==
"Supt16"` rows in `training_de_all_cell_groups.parquet`.

## Sources

- Held-out manifest:
  `[local file: 228_Supt16.csv]`.
- Training endpoint table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Training differential-expression table:
  `[local file: training_de_all_cell_groups.parquet]`.
- Same-experiment internal corpus: Distributed Agents corpus release
  `perturbai-july-260713-sourceguard-1773-v1`.
- Literature retrieved from PubMed:
  Wang et al. 2021, DOI 10.1080/15384101.2021.1881726 / PMID 33590780;
  Carvalho et al. 2013, DOI 10.1093/nar/gks1472 / PMID 23325844;
  Marciano et al. 2018, DOI 10.1074/jbc.RA117.000994 / PMID 29764934;
  Wang et al. 2023, DOI 10.1093/nar/gkad846 / PMID 37850662;
  Ma et al. 2023, DOI 10.1093/hmg/ddac259 / PMID 36255738.

## Computations over the training data

The focal training count table had 1,674 perturbations. Its endpoint distribution
was extremely zero-heavy: mean 14.05, median 0, third quartile 1, 90th percentile
2, 95th percentile 18, 99th percentile 436, and maximum 2,677. This made the
prior expectation zero or tiny unless there was target-specific evidence for a
broad 151-cell response.

I then filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and
to FACT-relevant or counterexample perturbations, counted `pvals_adj < 0.05`,
and inspected the top significant features. The filter used PyArrow dataset
predicate pushdown:

```python
flt = (
    ds.field("group_name") == "151 TH Prkcd Grin2c Glut"
) & ds.field("gene_target").isin(nodes)
table = dataset.to_table(
    columns=["gene_target", "names", "logfoldchanges", "pvals_adj"],
    filter=flt,
)
```

The most important focal-cell counts were:

| training perturbation | 151 TH Prkcd Grin2c Glut DEGs | why I used it |
| --- | ---: | --- |
| `Setd2` | 1 | H3K36me3 writer that recruits mammalian FACT to active genes in the Carvalho et al. model; closest measured upstream FACT proxy. |
| `Brd1` | 4 | Chromatin transcription cofactor with a tiny real 151-cell module; lower positive chromatin control. |
| `Setd5` | 9 | NDD-linked chromatin/transcription factor with a restricted thalamic module. |
| `Setdb1` | 22 | Active repressive-chromatin perturbation but still sparse in 151. |
| `Kmt2a` | 24 | H3K4 writer with a small 151 effect, contrasting with broad `Setd1a`. |
| `Chd2` | 34 | Measurable CHD remodeler response dominated by this thalamic group. |
| `Chd8` | 61 | Restricted postmitotic chromatin response, not a pan-neuronal shock. |
| `Chd4` | 100 | Largest member of the sparse-to-moderate chromatin analog band. |
| `Brd4` | 311 | Broad transcriptional coactivator/readout positive control; stronger than the FACT proxies. |
| `Setd1a` | 368 | Broad H3K4/COMPASS-related response, useful as a high chromatin counterexample. |
| `Sin3a` | 1,433 | Very broad chromatin/corepressor counterexample. |
| `Tpr` | 1,768 | Very broad nuclear transport stress counterexample. |
| `Uba5` | 2,677 | Maximal focal response, useful only as a scale anchor. |
| `Ep300`, `Bicra`, `Kmt2c`, `H2ac8`, `H3f3a`, `H4c11`, `Orc4`, `Orc6` | 0 each | Null controls showing that essential, chromatin, histone, or replication-related annotations alone do not imply a focal DEG response. |

`Setd2` had only one significant gene in the focal group, `Septin5`
(`log2FC = 0.458`, adjusted p = 1.63e-4). The histone genes `H2ac8`, `H3f3a`,
and `H4c11` were flat in the endpoint despite being nucleosomal substrates of
FACT, and the origin-recognition perturbations `Orc4` and `Orc6` were flat,
consistent with replication machinery being a poor predictor in postmitotic
neurons. Conversely, `Brd4`, `Setd1a`, `Sin3a`, and the RNA-processing or
proteostasis genes showed that the 151-cell assay had ample power to see broad
steady-state responses when acute loss produced one.

The Distributed Agents corpus had no Supt16-scoped findings or first-hop target paths,
which is expected for a completely held-out perturbation. I used it to audit
the candidate training analogs. Its Setd2 finding set reports a single robust
151-cell downstream gene and buffering of canonical SETD2 programs after sparse
P16 neuronal knockout. Its Brd4, Chd2, Chd4, Chd8, Setd5, Setdb1, Bicra,
Ep300, Kmt2c, and Chd7 findings repeatedly reject simple phenocopy by family,
chromatin domain, or complex-adjacent membership. For example, measured
KMT2/chromatin-disorder comparators did not phenocopy `Setd1a`, available
H3K4/enhancer and chromatin-NDD relatives did not phenocopy `Kmt2c`, `Bicra`
was flat despite BAF-sensitive responses from `Smarcc2`/`Arid2`/`Arid1a` in
the same cell class, and `Ep300` was flat in cell groups where other chromatin
regulators responded.

## Biology of Supt16

Mouse `Supt16` encodes the SPT16 large subunit of FACT, an obligate histone
chaperone complex with SSRP1. FACT binds histones and reorganizes nucleosomes
during transcription, replication, and DNA repair; SSRP1 heterodimerizes with
SPT16 in the complex and the complex binds H2A-H2B and H3-H4 histones
(Wang et al. 2021; Marciano et al. 2018). During replication, SPT16 also
interfaces with the MCM2-7 helicase to recycle parental histones, but that arm
is less directly relevant for postmitotic NeuN+ nuclei (Wang et al. 2023).

The strongest mechanistic bridge into the measured perturbation set was SETD2:
in mammalian cells, SETD2-dependent H3K36me3 supports FACT subunit loading on
active genes and transcription-coupled H2B exchange, and SETD2 depletion
reduces SPT16/SSRP1 loading (Carvalho et al. 2013). That makes `Setd2` more
relevant to `Supt16` than generic enhancer, H3K4, or BAF/NuRD comparators.
However, the bridge is indirect: SETD2 tunes FACT recruitment through an
H3K36me3-marked context, whereas `Supt16` directly removes the FACT large
subunit. Direct FACT disruption should be at least as likely to give a
detectable response as `Setd2`, but not necessarily a broad H3K4/BRD4-like
response.

Loss-of-function evidence also argues against a completely inert call. Human
SUPT16H partial loss-of-function variants are associated with developmental and
neurologic phenotypes, and Drosophila dre4/SUPT16H knockdown in neurons or glia
strongly impaired viability in a cell-autonomous fashion (Ma et al. 2023).
That evidence is not a direct DEG-count calibration for sparse juvenile mouse
postmitotic neurons, but it keeps Supt16 above the many development-only or
replication-only null expectations.

## Target-specific prediction

`Supt16` has no measured FACT paralog or SSRP1 partner in the training table.
The direct upstream FACT proxy, `Setd2`, was a one-DEG focal perturbation and
the Distributed Agents same-experiment summary calls its canonical H3K36 program
buffered. Null `Orc4` and `Orc6` argue that SPT16's replication-coupled
function should not be weighted much in this postmitotic assay. Null
`H2ac8`/`H3f3a`/`H4c11` argue that histone-core membership does not make a
chromatin response broad here. On the other hand, `Brd1 = 4`, `Setd5 = 9`,
`Setdb1 = 22`, `Kmt2a = 24`, `Chd2 = 34`, and `Chd8 = 61` show a band of real
but restricted 151-cell chromatin responses, and direct removal of SPT16 is
more central than SETD2 depletion alone.

I therefore predict a nonzero but very small response: larger than the
single-gene `Setd2` proxy, near the restricted `Setd5`/`Crebbp` range, and far
below `Brd4`, `Setd1a`, and broad RNA-processing or proteostasis perturbations.

Final point prediction:

| target_name | predicted_n_degs |
| --- | ---: |
| `Supt16` | 9 |

## Limits

The largest limitation is that no direct same-complex comparator was available:
`Ssrp1` is absent, and no `Supt16` expression signature exists in the parquet.
The `Setd2` analogy is mechanistically grounded through FACT recruitment, but
it is not a FACT-subunit knockout. FACT's replication and parental-histone
recycling literature comes mostly from dividing systems or yeast and is only a
weak guide in juvenile postmitotic neurons. Finally, the screen's sparse
AAV-CRISPR modality can buffer even essential chromatin genes through partial
mRNA depletion, protein stability, survival/dropout of strongly edited cells,
or redundant transcriptional states, so the integer 9 should be read as a
small-response calibrated point estimate rather than as a claim that exactly
nine genes are biologically downstream of Supt16.
