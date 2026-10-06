# DEG-count prediction for `Max`

## Question and endpoint

The requested prediction is the number of measured genes that would reach
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` after perturbing `Max`
in `151 TH Prkcd Grin2c Glut` neurons. `Max` was completely held out: it is not
present as a training `gene_target` in
`training_de_all_cell_groups.parquet` and it has no row in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.

I treated `n_degs` as an assay- and power-dependent response-breadth endpoint
for recovered postnatal neuronal nuclei, not as a direct measurement of target
engagement, cell survival, or absolute MYC/MAX biological importance. The
training DEG-count CSV is direct endpoint evidence for non-held-out
perturbations. The Parquet is direct evidence for those same perturbations'
gene-level DE signatures. Same-experiment corpus reports from
`perturbai-july-260713-sourceguard-1773-v1` are pre-interpreted summaries of
the same experiment, so I used them as a compact index and mechanistic
interpretation layer, not as independent replication.

## Sources used

- Declared training endpoint file:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared DE file:
  `training differential-expression dataset`.
- Requested-target manifest:
  `single-target request for Max`.
- Internal same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, especially the Findings and
  Evidence records for `Myc`, `Mycn`, `Mnt`, `Mga`, `Mlxip`, and `Chd8`.
- External literature:
  Carroll et al. 2018, Frontiers of Medicine, doi:10.1007/s11684-018-0650-z,
  PubMed 30054853; Prochownik and Wang 2022, Cells,
  doi:10.3390/cells11040747, PubMed 35203395; Wey et al. 2010, Cerebellum,
  doi:10.1007/s12311-010-0190-9; Knoepfler et al. 2002, Genes & Development,
  doi:10.1101/gad.1021202; Stielow et al. 2018, PLoS Genetics 14:e1007193,
  doi:10.1371/journal.pgen.1007193; Mochizuki et al. 2021,
  Nature Communications 12:7020, doi:10.1038/s41467-021-27345-x; Mathsyaraja
  et al. 2021, eLife 10:e64212, doi:10.7554/eLife.64212.

## Quantitative checks

I first read the requested-target CSV and confirmed it contains a single
target, `Max`, in that order.

From the 1,674-row focal training-count table, the endpoint distribution was
highly zero-inflated and skewed:

- median: 0 DEGs
- 75th percentile: 1 DEG
- 90th percentile: 2 DEGs
- 95th percentile: 18 DEGs
- nonzero perturbations: 469 of 1,674
- maximum: 2,677 DEGs for `Uba5`

I then compared `Max` with represented training perturbations in the
MYC/MAX/MLX network and PRC1.6/chromatin branch. For the focal cell group the
observed training counts were:

| training target | `151 TH Prkcd Grin2c Glut` `n_degs` | biological relationship to `Max` |
|---|---:|---|
| `Myc` | 0 | canonical MAX heterodimer partner and transcriptional activator |
| `Mycn` | 0 | MYC-family MAX partner |
| `Mnt` | 0 | MAX-binding E-box repressor and MYC antagonist |
| `Mlxip` | 0 | MLX partner in the extended MYC/MAX/MLX metabolic network |
| `Mga` | 2 | MAX-interacting PRC1.6/E-box repressor |
| `Setdb1` | 22 | indirect germline-silencing chromatin node, not a MAX partner |
| `Sin3a` | 1,433 | MNT-family corepressor scaffold, much broader than `Mnt` itself |
| `E2f1` | 0 | E2F/cell-cycle axis comparator |
| `E2f5` | 0 | E2F-family comparator |
| `Tfdp1` | 2 | E2F dimerization partner |
| `Tfdp2` | 0 | E2F dimerization partner |
| `Trp53` | 0 | apoptosis/cell-cycle stress comparator |
| `Fbxw7` | 1 | MYC protein regulator comparator |
| `Atoh1` | 0 | cerebellar granule precursor developmental comparator |
| `Sox2` | 2 | progenitor-state comparator |
| `Sox4` | 0 | neurodevelopmental comparator |
| `Sox11` | 0 | neurodevelopmental comparator |

The focal-cell DE rows for the closest targets showed:

- `Myc`, 210 perturbed nuclei: 0 FDR<0.05 genes. The strongest non-self rows
  were `Cdh2` at FDR 0.136, `Ywhah` at FDR 0.136, and `Unk` at FDR 0.136.
- `Mycn`, 320 perturbed nuclei: 0 FDR<0.05 genes. The strongest non-self rows
  were `Tardbp` at FDR 0.347 and `Tor1aip2` at FDR 0.347.
- `Mnt`, 226 perturbed nuclei: 0 FDR<0.05 genes. The strongest non-self row
  was `Per2`, FDR 0.708.
- `Mlxip`, 182 perturbed nuclei: 0 FDR<0.05 genes; every row had
  FDR 1.0.
- `Mga`, 82 perturbed nuclei: 2 FDR<0.05 genes, both upregulated:
  `Obscn`, log2FC 4.435, FDR 1.73e-8, and `Stag3`, log2FC 3.606,
  FDR 4.83e-5. `Tasor` was next, log2FC 0.577, FDR 0.0525.
- As an assay-capacity contrast, `Chd8` had 61 FDR<0.05 genes in the same cell
  group with 197 perturbed nuclei, including `Pnisr`, `Tmem50a`, `Chd8`,
  `Man2c1`, `Usp11`, `Csf2ra`, `Dus3l`, and `Luc7l3`.

The all-cell-group DE scan was important because a one-cell null could be a
power accident. The closest MYC/MAX/MLX represented targets were sparse across
the whole dataset:

- `Myc`: 0 genes at FDR<0.10 in every recovered cell group.
- `Mlxip`: 0 genes at FDR<0.10 in every recovered cell group.
- `Mycn`: 5 genes at FDR<0.10, restricted to `053 Sst Gaba`.
- `Mnt`: two one-gene FDR<0.05 signatures, `Trim2` in
  `009 L2-3 IT PIR AON ENT Glut` and `Preb` in
  `017 CA3 CA2-FC DG Glut`.
- `Mga`: the small `151 TH` `Obscn`/`Stag3`/`Tasor` FDR<0.10 signature plus
  `Stag3` in `155 MB Glut`.

The corresponding corpus records independently summarized the same pattern:
`Myc` and `Mlxip` were pan-neuronal FDR<0.10 nulls; `Mycn`, `Mnt`, and `Mga`
did not phenocopy each other or `Myc`; `Mga` had a narrow up-only
Stag3-centered signature in `151 TH` and `155 MB`; and `Mnt` did not reproduce
the broad `Sin3a` corepressor phenotype.

The SQL used for the focal signature extraction was:

```sql
SELECT gene_target, names, group_name, logfoldchanges, scores, pvals_adj,
       n_pert_matched, n_ctrl_matched
FROM read_parquet(?)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN ('Myc','Mycn','Mnt','Mga','Mlxip','Chd8','Trappc9')
ORDER BY gene_target, pvals_adj, ABS(scores) DESC;
```

## Target-specific biological reasoning

### `Max`

`Max` encodes the obligate bHLHZip partner through which MYC-family activators
and MNT/MXD-family repressors bind E-box DNA; the extended network also links
MNT to MLX-containing metabolic dimers. Reviews by Carroll et al. and
Prochownik and Wang describe this architecture, the temporal and tissue
restriction of many network outputs, and the fact that MYC/MAX/MXD/MNT/MGA
members are not interchangeable readouts of one constitutive transcriptional
program.

The causal transfer model for this assay is:

`Max` CRISPR loss -> reduced MYC/MAX and MNT/MAX/MGA/MAX bHLHZip function ->
possible loss of MYC-driven activation plus derepression from MNT/MGA-family
complexes -> transcriptional programs that are actually limiting in
postmitotic juvenile `151 TH` neurons -> recovery and survival of perturbed
nuclei -> Wilcoxon/FDR DEG calls.

The strongest same-complex analogs point to little or no constitutive MYC/MAX
activity in this cell group. `Myc` loss caused 0 DEGs in `151 TH` and was a
screen-wide FDR<0.10 null. `Mycn` also caused 0 in `151 TH`; its only
screen-wide signal was a five-gene FDR<0.10 `053 Sst Gaba` response that did
not involve the `151 TH` class. These are endpoint-aligned analogs for the
activator side because `Max` loss should impair MYC/MYCN-driven E-box
activation if such activation is basal and limiting. The lack of response in
acute postmitotic neurons is also biologically plausible: Knoepfler et al. and
Wey et al. place major c-Myc/N-Myc neural loss-of-function phenotypes in
progenitors and cerebellar development, whereas this screen perturbs already
postmitotic P16 neurons and assays surviving nuclei at P37-P44.

On the repressor side, `Mnt` is a direct MAX-binding MYC antagonist, but
`Mnt` perturbation produced 0 DEGs in `151 TH` and only two isolated
one-gene signatures elsewhere. This argues against a strong basal MNT/MAX
repression program in the focal thalamic cells. `Mnt` also failed to phenocopy
`Sin3a`: `Sin3a` had 1,433 DEGs in the focal class, showing that the experiment
could detect a broad chromatin-corepressor dependency, but MNT was not the
limiting input to that dependency in recovered postnatal neurons.

`Mga` is the main nonzero counterexample. MGA participates in ncPRC1.6, and
PRC1.6 can use MGA/MAX/E2F6-associated binding to repress meiotic or germline
targets such as `STAG3` in embryonic and proliferative systems
(Stielow et al.; Mochizuki et al.; Mathsyaraja et al.). In the training data,
`Mga` loss derepressed `Obscn` and `Stag3` in `151 TH`, exactly the kind of
upward leak that could occur if `Max` loss weakens an MGA/MAX repressive
complex. I therefore treated `Mga` as the strongest candidate for a nonzero
`Max` prediction. Two details kept the prediction at the null boundary rather
than at `Mga`'s count of 2. First, the same-experiment `Mga` report showed
that only four group-by-gene calls supported the entire positive surface
across the screen, and the broad expected PRC1.6 germline, EMT, and E2F/cycle
panels were otherwise absent except for `Stag3`. Second, `Max` is not
identical to `Mga`: losing `Mga` removes the PRC1.6 DNA-binding subunit itself,
whereas losing `Max` simultaneously disrupts opposite-sign MYC-family
activation and MNT/MGA-family repression and may only partially affect
MAX-independent PRC1.6 recruitment through E2F6-associated mechanisms.

`Mlxip` was a useful negative extended-network counterexample. It is not a
direct MAX partner, but its MLX-containing Mondo branch is connected to the
same bHLHZip growth and nutrient-responsive network. It had 0 focal DEGs and
was an FDR<0.10 null in every recovered group, while pathway controls such as
`Gfpt1`, `Srebf2`, and `Tsc2` generated metabolic or stress signatures in
overlapping neurons. That makes it less likely that `Max` loss will reveal a
large hidden MYC/MAX/MLX metabolic program in this basal postnatal condition.

Putting these together, the direct training analogs for `Max` in the focal
cell class are `Myc` 0, `Mycn` 0, `Mnt` 0, `Mlxip` 0, and `Mga` 2. The only
same-complex evidence for nonzero output is a very narrow `Mga` derepression
signal, and the stronger pattern is that acute perturbation of represented
MYC/MAX/MLX members is silent or nearly silent in postmitotic neurons. I
therefore predicted that `Max` will sit below the FDR<0.05 detection boundary
in this cell group.

Final point prediction:

- `Max`: 0 DEGs.

## Limits and uncertainty

`Max` itself was held out and its expression signature is absent, so the
prediction is an extrapolation from partners and pathway neighbors. Several
directly useful members, including `Mxd1`, `Mxd2`, `Mxd3`, `Mxd4`, `Mxi1`,
`Mycl`, `Mlx`, `Mlxipl`, `Pcgf6`, `L3mbtl2`, and `E2f6`, were also absent from
the training count table, limiting direct same-complex comparisons. The
Parquet reports recovered-nucleus transcription after 3-4 weeks, so it could
miss early, protein-level, or lethal MAX-dependent effects that fail to leave
surviving `151 TH` nuclei. Conversely, the dataset and corpus are two
representations of one Perturb-seq experiment rather than independent
replication. The exact integer is most uncertain around the 0-2 boundary
because `Mga` provides a plausible two-gene PRC1.6 leak, but the available
evidence does not justify predicting a broader response.
