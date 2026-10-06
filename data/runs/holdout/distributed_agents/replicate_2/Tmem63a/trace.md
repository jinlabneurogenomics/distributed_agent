# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and resolved ambiguities

The task is to predict `n_degs` for the held-out perturbation target in
`242_Tmem63a.csv`. The manifest contains one target:

| target_name |
|---|
| `Tmem63a` |

I treated `n_degs` as the number of measured genes, including the perturbed
target transcript if it passes threshold, with `pvals_adj < 0.05` in the focal
`151 TH Prkcd Grin2c Glut` class. The held-out `Tmem63a` perturbation itself is
absent from the parquet and from the training endpoint, so its count has to be
inferred from non-held-out perturbations and from target biology.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`, the exact endpoint for
  1,674 non-held-out perturbations in the focal cell group.
- `[local file: training_de_all_cell_groups.parquet]`, filtered to
  `group_name == "151 TH Prkcd Grin2c Glut"` for target-level expression
  signatures and per-gene `pvals_adj`.
- Distributed Agents same-experiment semantic corpus
  `perturbai-july-260713-sourceguard-1773-v1`. This release had no direct
  `Tmem63a` target context, but it did contain interpreted reports for the
  assayed paralogs `Tmem63b` and `Tmem63c`.
- Distributed Agents runtime profile tools, using focal-class `logfoldchanges` and
  `pvals_adj < 0.05`, to compare `Tmem63b` and `Tmem63c` against other
  measured ion-channel and Ca2+-handling perturbations.
- NCBI PubMed, via E-utilities, for OSCA/TMEM63 gene-function literature.

Key external citations:

- Murthy et al. 2018, eLife, doi:10.7554/eLife.41844, PMID:30382938:
  established OSCA/TMEM63 proteins from plants, flies, and mammals as an
  evolutionarily conserved family of mechanically activated ion channels.
- Zhao et al. 2016, Cell Biochemistry and Function, doi:10.1002/cbf.3185,
  PMID:27045885: cloned the three mouse Tmem63 paralogs and reported
  hyperosmolarity-activated currents when mouse TMEM63A/B/C were co-expressed
  in HEK293 cells.
- Zheng et al. 2023, Neuron, doi:10.1016/j.neuron.2023.07.006,
  PMID:37543036: showed that mammalian TMEM63 proteins, including TMEM63A and
  TMEM63B, are pore-forming, monomeric, high-threshold mechanosensitive
  channels.
- Li et al. 2024, Nature Cell Biology, doi:10.1038/s41556-024-01353-7,
  PMID:38388853: found Drosophila TMEM63 and mouse TMEM63A can act as
  lysosomal mechanosensory ion channels, with mouse TMEM63A mediating lysosomal
  mechanosensitivity in Neuro-2a cells.
- Yang et al. 2024, Cell Discovery, doi:10.1038/s41421-023-00628-x,
  PMID:38172113: identified TMEM63B as a hyperosmolarity sensor in excitatory
  subfornical-organ thirst neurons.
- Wang et al. 2025, Neuroscience Bulletin, doi:10.1007/s12264-024-01338-4,
  PMID:39982638: linked a human TMEM63A loss-of-function variant to
  hypomyelination and showed that Tmem63a knockout in mice delays early
  oligodendrocyte differentiation and myelination.

## Computational checks

The focal training endpoint is very sparse: among 1,674 non-held-out targets,
1,205 had `n_degs = 0`, 363 had 1-9 DEGs, 63 had 10-99 DEGs, and only 43 had
100 or more DEGs. The endpoint is therefore best treated as a zero-inflated
response-breadth measurement, not as a continuous phenotypic score.

I first pulled the exact counts for `Tmem63` family members and for nearby
channel/Ca2+-handling controls from the training-count CSV, then filtered the
parquet to the focal group and a hand-selected comparator set:

```python
import pyarrow.dataset as ds

d = ds.dataset(
    "[local file: 260901_predict]"
    "holdout_task/Inputs/training_de_all_cell_groups.parquet",
    format="parquet",
)
filt = (
    (ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & ds.field("gene_target").isin(targets)
)
tbl = d.to_table(
    columns=[
        "names", "scores", "logfoldchanges", "pvals_adj",
        "gene_target", "n_pert_matched", "n_ctrl_matched",
    ],
    filter=filt,
)
sig_count = (
    tbl.to_pandas()
    .groupby("gene_target")["pvals_adj"]
    .apply(lambda x: int((x < 0.05).sum()))
)
```

I also computed focal signed-profile neighborhoods for `Tmem63b` and `Tmem63c`
over all 1,674 training perturbations, using `logfoldchanges` as the signed
effect and `pvals_adj < 0.05` as the significance threshold. The closest
whole-profile neighbors of both paralogs were mostly zero-DEG perturbations.
Within a compact channel cohort (`Tmem63b`, `Tmem63c`, `Trpm3`, `Trpm7`,
`Pkd1`, `Itpr1`, `Kcnma1`), the `Tmem63b` versus `Tmem63c` top-tail overlaps
were only 0.08 on the positive tail and 0.11 on the negative tail, and neither
tail contained shared significant genes. I treated these signed-tail results,
plus the exact FDR counts, as more informative than high full-vector Pearson
similarities between raw nonsignificant log-fold-change vectors.

## Target-specific reasoning

### `Tmem63a`

`Tmem63a`, `Tmem63b`, and `Tmem63c` are the three mammalian members of the
OSCA/TMEM63 mechanically activated/osmosensitive channel family. That made the
two represented paralogs the most important dataset-local analogs, with
channel and Ca2+-homeostasis perturbations serving as counterexamples.

| training perturbation | focal `n_degs` | focal expression-pattern evidence | use for `Tmem63a` |
|---|---:|---|---|
| `Tmem63b` | 1 | The only focal FDR<0.05 gene was `Tmem63b` itself, log2FC = -0.701 and adjusted P = 4.16e-17, in 150 perturbed vs 23,679 control nuclei. | Strong paralog anchor. It shows the assay could detect Tmem63-family self-transcript loss, but acute `Tmem63b` loss did not generate a downstream focal transcriptional program. |
| `Tmem63c` | 0 | No focal gene reached FDR<0.05 in 243 perturbed vs 23,679 control nuclei. | Strong paralog anchor in the opposite direction: a TMEM63-family perturbation can be entirely FDR-null in this neuronal class. |
| same-experiment corpus `Tmem63b:F001`, `Tmem63c:F001-F004` | near-null across the atlas | The Distributed Agents corpus reported `Tmem63b` as near-null across 22 measured cell groups, with only two singleton downstream genes at FDR<0.10 outside the focal group, and `Tmem63c` as having 0 downstream FDR<0.10 genes in every measured group. The high-confidence claim `claim:301f58a6a168ac2f500c` states that `Tmem63b` and `Tmem63c` loss did not produce interchangeable postnatal neuronal transcriptomic surfaces despite family relatedness. | This broadens the focal 0/1 counts: the low focal counts are not hiding a strong TMEM63 module elsewhere in the postnatal neuronal atlas. |
| `Trpm3`, `Trpm7`, `Pkd1`, `Itpr1`, `Cacng3` | 0 each | All had zero focal DEGs. `Itpr1`, an ER Ca2+ release channel, had 0 significant genes in 203 perturbed nuclei. | These are not TMEM63 paralogs, but they argue that perturbing represented channel/osmotic/Ca2+-release machinery often leaves basal thalamic snRNA-seq at FDR null. |
| `Kcnma1` | 1 | Only `Kcnma1` itself passed FDR<0.05. | A Ca2+-activated channel loss can look self-only, similar to `Tmem63b`. |
| `Atp2a2`, `Atp2b1`, `Cacna1g` | 187, 22, 12 | `Atp2a2` induced a clear ER-stress/ISR program, starting with significant `Atp2a2`, `Cars`, `Ddit3`, `Shmt2`, `Chac1`, `Xbp1`, and `Hspa5`; `Atp2b1` and `Cacna1g` produced smaller but nonzero focal signatures. | Counterexamples. The prediction is not "all calcium/channel genes are zero"; broad or medium counts appear when loss engages a homeostatic program in this cell class. The TMEM63 paralogs did not show that behavior. |

The biological prior also points to a narrow or silent readout in this
experiment. TMEM63A is a high-threshold mechanosensitive cation channel, and
recent work places it at the plasma membrane or lysosome in stretch/osmotic
contexts rather than as a constitutive neuronal transcriptional regulator.
Known TMEM63A biology is prominent in organellar mechanosensing and in
oligodendrocyte/myelin phenotypes, while this screen sampled NeuN+ neuronal
nuclei after sparse P16 CRISPR in postmitotic cells and did not impose osmotic
or mechanical challenge. The positive TMEM63B thirst-neuron literature is also
not directly transferable to `151 TH Prkcd Grin2c Glut`: the training
`Tmem63b` perturbation itself was effectively self-only in the focal class.

I therefore made the zero/nonzero call from the within-dataset paralog counts:
`Tmem63b` was a one-gene self hit and `Tmem63c` was zero, and the most
mechanistically relevant follow-up evidence says represented TMEM63-family
loss is buffered at steady state in the postnatal neuronal atlas. Since the
endpoint uses an integer count and the direct paralog evidence centers between
0 and 1, I rounded toward the dominant sparse outcome and predicted
`Tmem63a = 0`.

## Limits

- There is no direct `Tmem63a` perturbation profile in the supplied parquet or
  in the Distributed Agents same-experiment corpus. `Tmem63a` expression level, guide
  cutting, and self-transcript depletion in the focal class are therefore
  unobserved.
- The difference between 0 and 1 is largely a self-transcript question in this
  neighborhood: `Tmem63b` contributed exactly one focal DEG and it was the
  target itself, whereas `Tmem63c` contributed none. A stronger `Tmem63a`
  self-transcript decrease could make the true endpoint one even without any
  downstream state.
- TMEM63A has disease and developmental roles in oligodendrocytes,
  peripheral sensory neurons, and organelles that are not assayed well by a
  NeuN-enriched, whole-brain-minus-hindbrain, postmitotic neuronal snRNA-seq
  design.
- Loss of a mechanosensitive/osmosensitive channel can change excitability,
  organellar mechanics, lipids, or stress responses without creating many
  nuclear mRNA changes at baseline, so a predicted zero should not be read as
  biological dispensability.
- `Atp2a2` and `Atp2b1` show that Ca2+ transporters can trigger medium or
  strong signatures in this exact focal class; I am extrapolating that
  `Tmem63a` behaves like its TMEM63 paralogs rather than like SERCA2/PMCA1.
