# Ndufa13 DEG-count prediction

## Question and resolved ambiguity

The requested held-out perturbation list contains one target:

```text
Ndufa13
```

I treated the endpoint as the count of every measured gene with `pvals_adj < 0.05` in
`151 TH Prkcd Grin2c Glut`, exactly as in the supplied training count CSV. That count includes
the perturbation target's own transcript when the self-knockdown RNA is significant; in the focal
training table, many `Nduf*` perturbations with `n_degs = 1` are self-only calls.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for the observed focal-cell DEG counts of non-held-out targets.
- `[local file: training_de_all_cell_groups.parquet]`
  for focal-cell signed Wilcoxon scores, log2 fold changes, adjusted p-values, and matched perturbed/control
  counts for respiratory-chain analogs.
- `[local file: 145_Ndufa13.csv]`
  for the requested held-out target and order.
- Distributed Agents same-experiment corpus MCP, release
  `perturbai-july-260713-sourceguard-1773-v1`. `Ndufa13` had no target-context entries in the corpus,
  so I used the corpus entries for represented Complex I comparators, especially `Ndufs2`, `Ndufs8`,
  `Ndufv1`, `Ndufv2`, `Ndufa10`, and `Ndufa4`.
- Distributed Agents runtime profile tools. I made a run-local focal-cell table containing 42 mitochondrial
  and respiratory-chain targets and compared signed Wilcoxon-score profiles in
  `mito_profile_compare.json`; the inspection artifact `mito_profile_inspect_key.json` was used only
  through bounded `profile_table` reads.
- External bibliography, queried through Europe PMC/PubMed:
  Fearnley et al. 2001, J. Biol. Chem., DOI `10.1074/jbc.C100444200`, PMID `11522775`;
  Huang et al. 2004, Mol. Cell. Biol., DOI `10.1128/MCB.24.19.8447-8456.2004`, PMID `15367666`;
  Fiedorczuk et al. 2016, Nature, DOI `10.1038/nature19794`, PMID `27595392`.

Those external papers establish the biological prior that NDUFA13/GRIM-19 is a bona fide
mitochondrial respiratory Complex I subunit required for Complex I assembly/function; I used that
prior to select Complex I/NDUFAF analogs, not to inflate the expected snRNA-seq response above what
those analogs actually did in this screen.

## Computation over the supplied tables

I first confirmed that the manifest contains only `Ndufa13`, and that `Ndufa13` is absent from both
training inputs as a perturbation target.

From the focal training count table:

- There are 1,674 represented training perturbations.
- 469 have any focal-cell DEG; the median is 0, the 75th percentile is 1, and the 95th percentile is 18.
- The 23 represented `Nduf*` Complex I structural/assembly targets have a total of only 11 focal DEGs:
  12 are `0`, 11 are `1`, and the maximum is `1`.
- Adding `Timmdc1` gives the Complex I/assembly-like set I used most directly:

| target | `n_degs` |
|---|---:|
| Ndufa10 | 1 |
| Ndufa11 | 0 |
| Ndufa12 | 0 |
| Ndufa4 | 1 |
| Ndufa6 | 1 |
| Ndufa8 | 0 |
| Ndufa9 | 0 |
| Ndufaf2 | 0 |
| Ndufaf4 | 0 |
| Ndufaf5 | 0 |
| Ndufb10 | 1 |
| Ndufb11 | 1 |
| Ndufb3 | 0 |
| Ndufb7 | 0 |
| Ndufb8 | 1 |
| Ndufb9 | 1 |
| Ndufc2 | 1 |
| Ndufs2 | 1 |
| Ndufs4 | 0 |
| Ndufs7 | 0 |
| Ndufs8 | 1 |
| Ndufv1 | 0 |
| Ndufv2 | 1 |
| Timmdc1 | 0 |

I then filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` for the Complex I set plus
nearby respiratory-chain and mitochondrial comparators. This yielded 42 perturbations x 17,259 genes.
The operation was a direct row filter on `group_name` and `gene_target`; no expression values were
imputed or transformed before comparison.

The significant focal rows showed that the Complex I counts were almost always self-only:

- `Ndufa10`, `Ndufa4`, `Ndufa6`, `Ndufb10`, `Ndufb11`, `Ndufb8`, `Ndufb9`, `Ndufc2`, `Ndufs2`, and
  `Ndufs8` each had exactly one significant gene, their own transcript, with self log2 fold changes
  from about -0.43 to -0.86.
- `Ndufv2` had exactly one DEG, but it was `Cdc40` up rather than a significant `Ndufv2` self call.
- `Ndufa11`, `Ndufa12`, `Ndufa8`, `Ndufa9`, `Ndufaf2`, `Ndufaf4`, `Ndufaf5`, `Ndufb3`, `Ndufb7`,
  `Ndufs4`, `Ndufs7`, `Ndufv1`, and `Timmdc1` had no focal DEGs.

The runtime profile comparison reinforced that the sparse counts were not hiding a shared subthreshold
state. In the focal cell group, the core Complex I anchors `Ndufa10`, `Ndufs2`, `Ndufs8`, `Ndufv1`,
and `Ndufv2` had no FDR-gene intersections with the checked `Ndufa/Ndufb/Ndufs` peers, and their
whole-score Pearson/cosine values against same-pathway peers were near zero. For example, among the
50 inspected pairs from these five anchors to close `Nduf` peers, cosines ranged from about -0.048
to 0.109; the largest value was the still-small `Ndufs8`--`Ndufb10` cosine. The focal profile table
also showed that `Ndufa13` as a measured downstream gene was not reproducibly induced or repressed
by the represented Complex I perturbations; its adjusted p-value was 1.0 in the Complex I rows that
I checked.

I used `Opa1` as a boundary/positive-control mitochondrial comparator. In the same focal cell group
`Opa1` had 37 DEGs, including ISR/amino-acid stress genes such as `Asns`, `Mars1`, `Chac1`, `Ddit3`,
`Mthfd2`, and `Slc7a5`. That demonstrates that the assay can see a mitochondrial stress program,
but the Distributed Agents corpus and the direct focal counts agree that single nuclear Complex I subunit
perturbations usually did not cross that threshold. Other respiratory-chain comparators were also
sparse: `Coa8`, `Cox11`, `Cox4i1`, `Cox6a1`, `Cox7b`, `Cox8a`, `Uqcrb`, `Uqcrfs1`, `Uqcrh`,
`Lrpprc`, `Mff`, and `Gfm2` were all `0`, while `Cox5a`, `Sdha`, `Uqcrc2`, `Uqcrq`, and `Sod2`
were all `1`.

## Target-specific rationale

### Ndufa13

`Ndufa13` encodes GRIM-19 / NADH dehydrogenase [ubiquinone] 1 alpha subcomplex subunit 13. GRIM-19
was identified as a Complex I subunit by Fearnley et al. 2001, Huang et al. 2004 found that it is
needed for Complex I assembly and function, and the Fiedorczuk et al. 2016 mammalian Complex I
structure places NDUFA13 among the many nuclear accessory subunits of the enzyme.

The best in-dataset analogs are therefore the represented nuclear-encoded Complex I structural and
assembly factors, not `Opa1` or generic mitochondrial perturbations. In the focal count table,
those analogs form an exceptionally narrow 0/1 class. `Ndufs2`, `Ndufs8`, `Ndufv1`, `Ndufv2`,
`Ndufa10`, `Ndufa11`, `Ndufa12`, `Ndufa6`, `Ndufa8`, `Ndufa9`, `Ndufaf2`, `Ndufaf4`, `Ndufaf5`,
`Ndufb10`, `Ndufb11`, `Ndufb3`, `Ndufb7`, `Ndufb8`, `Ndufb9`, `Ndufc2`, `Ndufs4`, and `Ndufs7`
all remained at 0 or 1 DEG in the same cell type; `Timmdc1`, a Complex I assembly factor present in
the count table, was 0. The same-experiment Distributed Agents corpus makes the same point at the broader
all-cell-group level: represented NDUF/NDUFAF perturbations repeatedly had flat, sparse, near-zero
correlated signatures rather than a shared acute OXPHOS-stress transcriptional module.

The zero/nonzero decision is consequently driven mostly by the on-target transcript. I do not expect
an FDR-significant downstream Complex I/ISR module from `Ndufa13`, because none of the focal Complex I
analogs exceeded one DEG and `Opa1` is a different mitochondrial lesion. I nevertheless assign one
rather than zero because the NDUFA13 transcript should be expressed in these neurons and many same-
complex structural subunits with similar focal perturbed-cell counts contributed exactly one
significant self-depletion event. That puts the best integer prediction at a self-only response:

```text
Ndufa13 -> 1 DEG
```

## Limits

The largest uncertainty is target-gene engagement. The hidden `Ndufa13` guides, perturbed-cell count,
and focal self log fold change were not in the supplied data, and within the represented Nduf panel
self-RNA significance split almost evenly between 0 and 1. This makes `0` a plausible neighbor of the
chosen `1`.

The Complex I analogy is biochemical, not structural identity: NDUFA13 is one accessory subunit among
many, and a severe complete loss of GRIM-19 in other systems need not match acute sparse P16 neuronal
editing. Conversely, a missing transcriptional response in this endpoint does not prove that Complex I
activity was preserved; the screen did not measure indels, protein, oxygen consumption, ROS, ATP, or
loss of edited cells. The Distributed Agents corpus had no direct `Ndufa13` entry, so all same-experiment
reasoning for the held-out target is extrapolated from represented Complex I and respiratory-chain
neighbors.
