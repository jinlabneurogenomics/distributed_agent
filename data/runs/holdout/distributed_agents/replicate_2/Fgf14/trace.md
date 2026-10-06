# Trace: Fgf14

## Question and interpretation

The held-out target manifest contains one requested perturbation:
`Fgf14`.  I interpreted the requested endpoint as the number of rows for this
target and for `151 TH Prkcd Grin2c Glut` whose `pvals_adj < 0.05`, counting
the target transcript itself if it would have passed the same threshold.  That
matches the training count behavior: for example, `Fgf13` has two focal DEGs
and one of them is the `Fgf13` self-transcript.

I did not interpret a weak target-transcript log fold change in the screen as
failed editing, because the assay is mosaic AAV CRISPR in postmitotic neurons
and the readout is nuclear RNA, not indel or protein abundance.

## Sources

- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, the observed focal
  DEG counts for 1,674 non-held-out perturbations.
- `training_de_all_cell_groups.parquet`, filtered to
  `group_name == "151 TH Prkcd Grin2c Glut"` for target-specific adjusted
  p-values, fold changes, and matched cell counts.
- Distributed Agents corpus release
  `perturbai-july-260713-sourceguard-1773-v1`; the release had no
  `Fgf14` target-centered record, but it contained curated findings for
  `Fgf12`, `Fgf13`, `Scn1a`, `Scn1b`, `Scn2a`, `Scn8a`, `Kcnq2`, and `Ank2`.
- A run-local Distributed Agents `profile_neighbors` analysis over focal log-fold-change
  profiles, using all 1,674 training targets as eligible observed nodes.  I used
  the output as a falsification check for broad expression similarity, not as a
  substitute for biological relevance, because the FHF/Nav signatures are very
  sparse.
- External PubMed literature on intracellular fibroblast growth factors:
  Laezza et al. 2009, DOI: `10.1016/j.mcn.2009.05.007`; Goldfarb et al. 2007,
  DOI: `10.1016/j.neuron.2007.07.006`; Shakkottai et al. 2008,
  DOI: `10.1016/j.nbd.2008.09.019`; Xiao et al. 2013,
  DOI: `10.1016/j.mcn.2013.07.008`; Bosch et al. 2015,
  DOI: `10.1523/JNEUROSCI.2663-14.2015`; Ali et al. 2016,
  DOI: `10.1074/jbc.M115.703868`.

## Computations over the differential-expression tables

I read the held-out manifest and confirmed that `Fgf14` was not in the focal
training-count table.  The training endpoint is zero-inflated and sparse in
this cell group: among 1,674 training perturbations the median was 0 DEGs, the
75th percentile was 1 DEG, and only 469 targets had any DEG.

For mechanistic comparators I filtered the parquet to the focal cell group and
to FHF, voltage-gated sodium-channel, KCNQ, HCN, calcium-channel, and axon
initial segment scaffold targets.  The non-obvious part of the query was simply
predicate pushdown on `group_name` and `gene_target`, followed by counting
features whose adjusted p-value was below 0.05:

```python
import pyarrow.dataset as ds

dset = ds.dataset("training_de_all_cell_groups.parquet", format="parquet")
tbl = dset.to_table(
    columns=[
        "gene_target", "names", "logfoldchanges", "pvals_adj",
        "n_pert_matched", "n_ctrl_matched",
    ],
    filter=(
        (ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
        & ds.field("gene_target").isin(analog_targets)
    ),
)
```

I then compared focal DEG burdens and inspected the identities of the
significant genes.  The central focal-cell counts were:

| comparator | focal n_degs | focal expression evidence |
| --- | ---: | --- |
| `Fgf12` | 0 | no gene, including `Fgf12`, passed FDR 0.05 among 256 matched perturbed nuclei |
| `Fgf13` | 2 | `Fgf13` self down, q = 4.39e-12, and `Rell2` down, q = 0.0398, among 195 matched nuclei |
| `Fgf1` | 0 | canonical secreted FGF ligand, not an intracellular FHF; flat |
| `Fgfr1`, `Fgfr2`, `Fgfr3`, `Fgfrl1` | 0, 0, 0, 0 | receptor-family counterexamples; flat in the focal group |
| `Scn1a` | 1 | self-transcript only |
| `Scn1b` | 2 | `Scn1b` self down plus `Jun` up |
| `Scn2a` | 1 | self-transcript only |
| `Scn3a` | 0 | no focal DEG |
| `Scn8a` | 1 | self-transcript only |
| `Kcnq2` | 1 | self-transcript only at FDR 0.05; `Agap2` was just above the cutoff at q = 0.0509 |
| `Kcnq3` | 1 | self-transcript only |
| `Hcn1`, `Hcn2` | 0, 1 | `Hcn2` was self-transcript only; `Hcn1` was flat |
| `Ank1`, `Ank2` | 0, 0 | testable ankyrin/AIS-adjacent scaffolds were flat |
| `Cacna1a`, `Cacna1g` | 0, 12 | a useful boundary: not every ion-channel gene is forced to be null in this cell group |

The run-local `profile_neighbors` pass compared `Fgf12`, `Fgf13`,
`Scn1a`, `Scn2a`, `Scn8a`, `Kcnq2`, `Kcnq3`, and `Hcn2` against every training
target.  `Fgf12` had 0 significant features and `Fgf13` had only 2, and their
nearest whole-profile neighbors were null-like targets such as `Rars2`,
`Tenm4`, `Fgfr1`, `Grin2b`, and `Ephb4` rather than a coherent FHF/Nav module.
I therefore used this analysis to reject a hidden robust expression state, not
to average arbitrary nearest neighbors.

## Biology and target-specific reasoning

`Fgf14` is the fourth fibroblast-growth-factor homologous factor, also called
an intracellular FGF.  Unlike secreted `Fgf1` or FGFR receptors, FGF14 acts
inside neurons, localizes to the axon initial segment, and binds the
cytoplasmic C-tail of voltage-gated sodium channels.  Laezza et al. 2009 showed
that FGF14 splice variants differentially regulate Nav1.2/`Scn2a` and
Nav1.6/`Scn8a`, while Ali et al. 2016 mapped FGF14 surfaces required for the
FGF14-Nav1.6 complex.  Goldfarb et al. 2007 showed that FHFs control intrinsic
excitability through voltage-gated sodium-channel gating.  FGF14 loss in mice
strongly affects cerebellar firing and ataxia-related physiology
(Shakkottai et al. 2008; Bosch et al. 2015), and Xiao et al. 2013 placed FGF14
in the AIS/Nav1.6 protein-localization system.

Those mechanisms make `Fgf12` and `Fgf13` the best direct training analogs,
with sodium-channel subunits as pathway comparators.  The focal-cell data were
decisive about their RNA breadth: `Fgf12` was a complete zero and `Fgf13` was a
two-gene signature dominated by its own transcript.  The Distributed Agents corpus
separately curated the same boundary: represented FHF, Nav alpha/beta, and
FGFR perturbations do not produce a shared pan-FHF, pan-Nav, or FGF-family RNA
module in this assay.  In particular, `Fgf13` finding `F004` contrasts `Fgf12`,
`Fgf1`, `Fgfr1`, `Fgfr2`, `Fgfr3`, `Fgfrl1`, `Scn1a`, `Scn1b`, `Scn2a`,
`Scn3a`, and `Scn8a`; `Scn2a` and `Scn8a` corpus findings likewise describe
strong buffering and no shared sodium-channel transcriptional state.

I therefore rejected a broad nonzero count for `Fgf14`: its primary literature
phenotype is channel gating, AIS localization, and repetitive firing, none of
which is guaranteed to leave tens of steady-state nuclear DEGs after sparse
P16 CRISPR.  The proper focal prior is the small observed FHF/Nav distribution:
0 for `Fgf12`, 2 for `Fgf13`, and 0-2 for most directly represented sodium
channel subunits.

I also did not set `Fgf14` to a confident zero.  It is detectable as a measured
gene in the focal DE table: another broad perturbation, `Zbtb7a`, significantly
down-regulated `Fgf14` in `151 TH Prkcd Grin2c Glut` at q = 0.0365.  `Fgf13`,
`Scn1a`, `Scn1b`, `Scn2a`, `Scn8a`, `Kcnq2`, `Kcnq3`, and `Hcn2` all show that
for channel-complex genes in this assay the target transcript alone can account
for the entire count.  The most likely outcome for `Fgf14` is therefore a
barely nonzero, self-transcript-dominated result rather than an FDR-flat
response or a multi-gene FHF module.

## Point prediction

- `Fgf14`: `1` DEG.  This is driven mostly by within-dataset FHF/Nav sparsity
  and secondarily by external knowledge that the FGF14 lesion is proximal to
  Nav protein function instead of to a transcriptional pathway.  I expect at
  most the `Fgf14` transcript itself to pass FDR 0.05 in the focal class.

## Limits

The closest target, `Fgf14` itself, was held out and had no Distributed Agents
target-centered context in the selected release.  `Fgf11`, `Ank3`, and `Nfasc`
were not represented training perturbations, so some natural AIS comparators
could not be tested.  FGF14 literature is strongest in cerebellar and
heterologous Nav systems, whereas the prediction is for thalamic glutamatergic
neurons after mosaic P16 CRISPR.  Finally, the endpoint counts the nuclear RNA
state of recovered neurons; it can miss real changes in sodium current,
Nav1.6 localization, AIS organization, firing, or network compensation.
