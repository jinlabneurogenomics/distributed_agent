# Question and resolved ambiguity

The task is to predict, for each target in `251_Tspan12.csv`, the hidden
`n_degs` endpoint in `151 TH Prkcd Grin2c Glut`: the number of measured genes
with Scanpy Wilcoxon Benjamini-Hochberg `pvals_adj < 0.05` after acute
postnatal AAV-CRISPR loss of the target.

The manifest contains one held-out target, `Tspan12`. `Tspan12` is absent as a
training `gene_target` and absent from the training endpoint CSV, so I treated
all rows for `Tspan12` itself as unobserved. The endpoint includes self rows
when the target transcript passes FDR, so the decision below includes both
downstream Wnt/Norrin biology and the possibility that `Tspan12` itself could
be the only hit.

# Sources used

Internal, same-experiment evidence:

- `[local file: 251_Tspan12.csv]`
- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- `[local file: training_de_all_cell_groups.parquet]`
- Distributed Agents same-experiment corpus, release
  `perturbai-july-260713-sourceguard-1773-v1`, queried for `Fzd4`, `Lrp5`,
  and `Lrp6` claims and findings around Wnt-receptor behavior in the screen.

External biological evidence:

- Junge et al. 2009, Cell, DOI `10.1016/j.cell.2009.07.048`, PMID 19837033:
  TSPAN12 enhances Norrin-, but not Wnt-, induced FZD4/beta-catenin signaling
  and Tspan12 loss phenocopies retinal vascular defects of `Ndp`, `Fzd4`, and
  `Lrp5` mutant mice.
- Nikopoulos et al. 2010, American Journal of Human Genetics, DOI
  `10.1016/j.ajhg.2009.12.016`, PMID 20159111, and Poulter et al. 2010,
  American Journal of Human Genetics, DOI `10.1016/j.ajhg.2010.01.012`,
  PMID 20159112: human `TSPAN12` mutations cause autosomal-dominant familial
  exudative vitreoretinopathy, tying the gene to the Norrin/FZD4/LRP5 pathway.
- Zhang et al. 2018, Arteriosclerosis, Thrombosis, and Vascular Biology,
  DOI `10.1161/ATVBAHA.118.311689`, PMID 30354230: endothelial loss of
  `Tspan12` impairs retinal vascular morphogenesis and blood-retina barrier
  formation/maintenance.
- Wang et al. 2018, PNAS, DOI `10.1073/pnas.1813217115`, PMID 30478038:
  Norrin and Wnt7a/Wnt7b systems cooperate in blood-brain and blood-retina
  barrier development and maintenance, with `Tspan12` acting as a Norrin
  coactivator.

# Dataset computations

I first read the held-out manifest and verified that it contains exactly:

```text
Tspan12
```

From the focal training endpoint there are 1,674 training perturbations:
1,205 have `n_degs = 0`, 363 have 1-9 DEGs, 63 have 10-99 DEGs, and 43 have
at least 100 DEGs. The median count is 0 and the 75th percentile is 1, so a
new target needs fairly direct evidence before being moved away from 0 in this
cell group.

For the parquet, I queried only `group_name == "151 TH Prkcd Grin2c Glut"`
and a curated set of Wnt/Norrin/tetraspanin comparators, then recomputed
`sum(pvals_adj < 0.05)` for each target. The only nontrivial operation was a
filtered Arrow scan:

```python
f = (
    (ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & ds.field("gene_target").isin(comparator_targets)
)
table = dataset.to_table(
    columns=["names", "gene_target", "logfoldchanges", "pvals_adj",
             "scores", "n_pert_matched", "n_ctrl_matched"],
    filter=f,
)
```

I also scanned all focal-cell rows where the measured `names` value was
`Tspan12`, `Fzd4`, `Lrp5`, `Lrp6`, `Ndp`, `Axin2`, `Ramp3`, `Plekhg1`, or
`Tspan7`. This verified that `Tspan12` is in the measured-gene set for the
focal class, but in the 1,674 visible training perturbations its own row never
approached FDR significance: the best adjusted p-value was 0.193 in `Tpr`;
the next were 0.491 in `Chd4` and 0.538 in `Atp2a2`.

# Target-specific reasoning

## `Tspan12`

`Tspan12` is not a generic thalamic neuronal regulator. The best-established
function of the protein is as a cell-surface coactivator in the
Norrin/FZD4/LRP5-or-LRP6 beta-catenin receptor complex, especially in retinal
vascular endothelial cells. Human genetics and mouse endothelial models place
the high-effect phenotypes in retinal angiogenesis and blood-retina barrier
maintenance rather than in postmitotic NeuN+ thalamic neurons.

The biologically closest perturbations represented in the training data were
therefore `Fzd4`, `Lrp5`, and `Lrp6`, not `Tspan7` simply because it is also a
tetraspanin. Their focal-cell endpoint behavior was:

| training target | `151 TH Prkcd Grin2c Glut` evidence |
| --- | --- |
| `Fzd4` | 188 perturbed nuclei; 0 genes at FDR<0.05; every focal row had `pvals_adj = 1.0`. |
| `Lrp5` | 230 perturbed nuclei; 0 genes at FDR<0.05; every focal row had `pvals_adj = 1.0`. |
| `Lrp6` | 120 perturbed nuclei; 4 genes at FDR<0.05: `Nrbp2`, `Nsmf`, `Atrnl1`, `Chgb`; the Wnt feedback gene `Axin2` was down with logFC -0.800 but missed 0.05 with FDR 0.073. |
| `Fzd2`, `Fzd6`, `Fzd9` | all 0 genes at FDR<0.05; min FDRs 1.0, 0.875, and 0.357, respectively. |
| `Ror1`, `Ror2`, `Ryk`, `Prickle1` | all 0 genes at FDR<0.05 in this focal group. |
| `Ctnnb1` | 383 genes at FDR<0.05, including strong decreases of `Plekhg1`, `Ramp3`, and Wnt-feedback genes such as `Axin2`. |
| `Tcf7l2` | 106 genes at FDR<0.05, overlapping the `Ctnnb1` thalamic state only partially. |
| `Gsk3b` | 6 genes at FDR<0.05, including the `Gsk3b` self row and weak noncanonical genes; the same-experiment corpus cautions that isolated `Gsk3b` loss did not simply induce canonical Wnt transcription. |
| `Tspan7`, `Cd81` | each had `n_degs = 1`, but in both cases the singleton was the self transcript, not a downstream membrane-scaffold program. |

The Distributed Agents corpus sharpened those raw counts. It contains no direct
`Tspan12` claim because `Tspan12` was held out, but its `Fzd4:F002` finding
states that `Fzd4`, `Fzd2`, `Fzd6`, and `Fzd9` did not converge with the
detectable `Ctnnb1`/`Lrp6` thalamic Wnt response. Its `Lrp5:F003` and
`Lrp6:F004` findings likewise separate `Lrp5` from the weak `Lrp6` branch:
`Lrp6`, not `Lrp5`, converged with `Ctnnb1`, while the represented
receptor-level relatives were flat. The release-level claims summarize the
same boundary: detectable beta-catenin/TCF output exists in this assay, but
single Frizzled receptors and `Lrp5` are mostly transcriptionally buffered.

That boundary is directly relevant to `Tspan12`. If the hidden perturbation
were acting through its canonical Norrin complex, it should most resemble
`Fzd4` and `Lrp5`, and both are complete focal-cell nulls. The only upstream
coreceptor with a visible effect, `Lrp6`, produced just 4 FDR<0.05 genes and
only a subthreshold `Axin2` response, so even moving `Tspan12` toward the
slightly active branch would predict at most a very small count. The self-row
case also points downward: unlike `Tspan7` or `Cd81`, `Tspan12` behaves as a
low, nonsentinel transcript in these thalamic neuronal nuclei, consistent
with its vascular-endothelial prior.

I therefore predict that acute `Tspan12` loss in recovered
`151 TH Prkcd Grin2c Glut` nuclei will have no measured gene passing
FDR 0.05:

```text
Tspan12 -> 0
```

# Limits

This is an extrapolation from same-complex training targets; the actual
`Tspan12` signature was fully held out. `Ndp` itself was a measured gene but
not a represented perturbation target, so the exact ligand side of the
Norrin/FZD4/TSPAN12 complex could not be tested. The screen is NeuN-enriched
and under-samples endothelial cells, where the external literature says the
strongest `Tspan12` biology lies; therefore the zero prediction is specific to
the assayed postnatal neuronal nuclei and should not be read as a vascular
or developmental null. Finally, the assay measures nuclear RNA, not FZD4
protein trafficking, barrier integrity, retinal angiogenesis, or local
neurite/synapse phenotypes.
