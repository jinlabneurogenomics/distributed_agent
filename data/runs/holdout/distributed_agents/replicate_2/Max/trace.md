# Question and resolved ambiguities

The requested held-out target list in
`[local file: 132_Max.csv]`
contains one perturbation, `Max`. I interpreted the task as a point prediction
of how many genes would have `pvals_adj < 0.05` after `Max` loss of function in
`151 TH Prkcd Grin2c Glut` nuclei, using the supplied training perturbations
only. `0` means that no measured transcript is expected to pass the
Benjamini-Hochberg FDR threshold in that cell group.

The supplied count table contained 1,674 non-held-out perturbations. The focal
cell group is strongly zero-inflated: 1,205/1,674 perturbations have `n_degs =
0`, the median is 0, the 75th percentile is 1, and only the top 5% exceed 18
DEGs. Therefore I treated a few-gene result as a materially different call from
a broad chromatin or proteostasis response.

# Sources used

Primary in-dataset evidence:

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for observed `n_degs` in the focal group.
- `[local file: training_de_all_cell_groups.parquet]`
  for focal differential-expression rows and for the actual top genes in the
  comparator signatures.
- Local Distributed Agents runtime `profile_neighbors`, run on `Myc`, `Mycn`, `Mga`,
  `Mnt`, `Mlxip`, and `Usf1` in `151 TH Prkcd Grin2c Glut`, to check whether
  any observed focal signatures recurred as a robust Myc/Max-like state.

Internal annotation and corpus evidence:

- Distributed Agents corpus MCP release
  `perturbai-july-260713-sourceguard-1773-v1`.
  `target_context(Max)` returned no direct frozen claims or findings for `Max`,
  so the corpus was used only for represented comparators.
- Distributed Agents corpus findings for `Myc`, `Mycn`, `Mnt`, `Mga`, and `Mlxip`,
  especially claim `claim:e0f08892a4e37698b91a`, which states that represented
  MYC/MAX-network and adjacent E2F/Mondo/metabolic perturbations do not form a
  shared postmitotic neuronal transcriptomic module in this assay.
- Distributed Agents corpus evidence `Mnt:E030`-`Mnt:E033`, which specifically records
  that `Myc`, `Mycn`, `Mga`, `Mlxip`, `E2f1`, `E2f5`, and `Trp53` did not
  converge on `Mnt`, and that `Max`, `Mlx`, and `Mxd1`-`Mxd4` were absent as
  perturbation targets in the model-visible parquet.
- Local gene annotation parquet tables derived from CORUM v5.0 and STRING
  v12.0: CORUM contains MYC-MAX, Mad-Max-Sin3, and MondoA-MLX complexes; STRING
  records high-confidence physical edges among `Mlx`/`Mlxip` and many MAX/MGA
  cofactors.

External biological knowledge:

- `Max` encodes the bHLH leucine-zipper partner that permits sequence-specific
  DNA binding by MYC-family proteins (Blackwood and Eisenman 1991,
  PMID:2006410, DOI:10.1126/science.2006410).
- MXD/MAD proteins also heterodimerize with MAX and antagonize MYC-family
  transcriptional activation (Ayer, Kretzner and Eisenman 1993, PMID:8425218,
  DOI:10.1016/0092-8674(93)90661-9).
- MNT is a MAX-interacting MYC antagonist that uses a Sin3-interaction domain
  and can suppress MYC-dependent transcription (Hurlin, Queva and Eisenman
  1997, PMID:9308234, DOI:10.1007/978-3-642-60801-8_11; Yang and Hurlin 2017,
  PMID:28230739, DOI:10.3390/genes8020083).
- MGA is a PRC1.6-associated MAX-network repressor, with MGA/L3MBTL2/E2F6
  involved in targeting noncanonical PRC1.6 to repressed loci including
  germline-related programs (Stielow et al. 2018, PMID:29381691,
  DOI:10.1371/journal.pgen.1007193).
- MLXIP/MondoA acts with MLX, rather than MAX, in glucose-responsive
  transcription through targets such as `Txnip`, which makes it an adjacent
  E-box metabolic branch rather than a direct MAX dimer (Stoltzman et al. 2008,
  PMID:18458340, DOI:10.1073/pnas.0712199105; Peterson et al. 2010,
  PMID:20385767, DOI:10.1128/MCB.01613-09).

# Computation

I filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and either
counted `pvals_adj < 0.05` per `gene_target` or loaded targeted comparator
profiles:

```python
table = dataset.to_table(
    columns=["gene_target", "names", "logfoldchanges", "pvals_adj"],
    filter=(ds.field("group_name") == focal)
           & ds.field("gene_target").isin(comparator_genes),
)
```

The focal slice has 28,891,566 rows: exactly 17,259 measured genes for each of
1,674 training perturbations. The computed significant-gene counts matched the
training count CSV.

# Target-specific reasoning

## Max

Relevant observed perturbations in `151 TH Prkcd Grin2c Glut`:

| comparator | observed `n_degs` | focal expression evidence | relevance |
|---|---:|---|---|
| `Myc` | 0 | No gene passed FDR 0.05; the smallest focal adjusted p-value was 0.136 (`Ywhah`, `Unk`, `Cdh2`). | Direct MAX activator partner. Its complete focal null is the closest observed test of the activator arm that would be reduced by MAX loss. |
| `Mycn` | 0 | No FDR-significant focal genes; smallest adjusted p-value 0.347. | N-MYC also requires MAX. The null argues that a second MYC-family activator is not maintaining a broad basal program in this thalamic/midbrain glutamatergic group. |
| `Mnt` | 0 | No focal FDR-significant genes; top adjusted p-value 0.708. | Direct MAX-network repressor and MYC antagonist. Its flat response argues against a strong derepression arm after removing an individual MNT/MAX complex. |
| `Mga` | 2 | Only `Obscn` and `Stag3` passed FDR 0.05; the next gene, `Tasor`, was just above threshold at 0.0525. | MAX/PRC1.6-associated repressor. This is the only direct MAX-network comparator with a focal hit, but the response was a tiny up-only MGA-specific derepression signature, not a broad MYC/MAX program. |
| `Mlxip` | 0 | No FDR-significant focal genes. | MondoA uses MLX rather than MAX, so it is a metabolic E-box counterexample. Its null supports quiescence of the related Mondo/MYC nutrient branch. |
| `Usf1` | 1 | Only `Gaa` passed FDR 0.05. | E-box bHLH-LZ factor that is independent of MAX. The singleton response is a negative control for "E-box TF" as a sufficient predictor of broad DE. |
| `Cdkn2a` | 0 | No focal FDR-significant genes. | Tests a p53/cell-cycle-adjacent stress/apoptosis route downstream of proliferative MYC biology; flat in this postmitotic focal group. |
| `Ogt` | 4 | Four focal DEGs. | A metabolic/chromatin boundary case connected to nutrient signaling rather than to obligate MAX dimers. It remained small. |
| `Kmt2a` | 24 | A histone-methyltransferase cofactor present in MAX/MGA annotation neighborhoods. Its modest signature shows that a shared chromatin-neighborhood annotation edge does not translate into a MAX-like signature. |
| `Chd8` | 61 | A chromatin remodeler present in MAX/MGA annotation neighborhoods. Its modest response is larger than the direct MYC/MAX members but still far below broad stress/chromatin responders. |
| `Sin3a` | 1433 | Broad focal response with ER quality-control, RNA-processing, lipid/lysosomal, and ciliary arms in the Distributed Agents corpus. | `Sin3a` is recruited by MNT/MXD repressors, but the corpus explicitly separates broad SIN3A-dependent neuronal transcription from `Mnt`; this is an assay-positive counterexample rather than a reason to make `Max` broad. |

The Distributed Agents runtime nearest-neighbor scan of the six direct or adjacent
`Myc`/`Max`/`Mlx` anchors did not find a hidden high-count, mechanistically
coherent focal analog. Whole-logFC correlations in this sparse setting ranked
many unrelated zero-count perturbations; direct FDR overlap among the network
members was absent or consisted of `Mga`'s two genes only. Signed top-200
overlap among direct anchors was also shallow; for example `Myc` versus `Mnt`
shared 14 positive-tail and 31 negative-tail genes out of 200, and `Myc` versus
`Mga` shared only 13 positive-tail and 5 negative-tail genes.

The mechanistic prior for `Max` is stronger than the individual `Myc`, `Mycn`,
or `Mnt` priors because a MAX edit can simultaneously impair MYC-family
activators plus MXD/MNT/MGA repressors. In a proliferating cell this centrality
could be dramatic. In this P16 to P37/P44 NeuN-enriched perturbation, however,
the direct represented arms themselves are essentially silent in the focal
group: activator loss is zero, MNT loss is zero, MGA loss is only two genes, and
adjacent MLXIP/USF/E2F/p53 comparisons are flat or singleton-like in the
corpus. Since `Max` loss removes opposing transcriptional arms, the weak MGA
derepression signal is not enough evidence to push the prediction above
threshold.

Prediction: `Max` -> 0 DEGs.

# Limits and extrapolation

The prediction is mostly within-dataset driven. The direct held-out `Max`
signature was unavailable in the training parquet, and the internal corpus has
no `Max` target context. The most obvious same-family repressors,
`Mxd1`-`Mxd4`, `Mxi1`, `Mlx`, `Mlxipl`, and core PRC1.6 subunits such as
`L3mbtl2`, `Pcgf6`, and `E2f6`, were also not represented as training
perturbations in this focal endpoint. A full MAX protein-null could have a
larger or different effect than an acute sparse AAV-CRISPR perturbation with
modest mean target-RNA downregulation, and snRNA-seq at this single chronic
endpoint can miss protein-only, electrophysiological, activity-dependent, or
early transient MYC/MAX effects. The exact boundary between 0 and a 1-2 gene
MGA-like singleton response is therefore the weak spot; I chose 0 because every
closest observed direct arm was 0 except `Mga`, and `Mga`'s two focal genes
look target-specific rather than like a generic MAX-network response.
