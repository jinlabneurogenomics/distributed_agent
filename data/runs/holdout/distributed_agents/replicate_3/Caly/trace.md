# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and interpretation

The requested manifest contains one held-out perturbation:

```text
Caly
```

I interpreted the task as predicting the focal endpoint `n_degs`: the number of
measured genes with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` in
the `151 TH Prkcd Grin2c Glut` cell group after sparse postnatal CRISPR loss of
the target.  The held-out target was absent from both the training count table
and the perturbation rows in the DE parquet, so I treated all Caly-specific DEG
or signature information as unknown and transferred from nearby training
perturbations.

The main ambiguity is whether to count an on-target transcript decrease as a
real DEG.  I did count it, because the supplied training endpoint counts every
measured gene with `pvals_adj < 0.05`, and many weak focal responses in the
training CSV are one-gene, self-transcript-only calls.

## Sources used

- Input focal training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
  I inspected parquet metadata and found that row groups 547-579 are entirely
  `151 TH Prkcd Grin2c Glut`, with the two boundary row groups 546 and 580
  partly overlapping, then read that restricted interval for candidate
  endocytic, AP-adaptor, synaptic, glutamate-receptor, and dopamine/GPCR
  perturbations.
- Requested-target manifest:
  `[local file: 028_Caly.csv]`.
- Distributed Agents corpus MCP, release
  `perturbai-july-260713-sourceguard-1773-v1`.  The corpus had no direct Caly
  claims, but it did contain a clathrin/endosomal cohort centered on `Cltc`,
  `Dnm1`, `Synj1`, `Bin1`, `Cd2ap`, `Dnajc5`, and `Sh3kbp1`, including the
  high-confidence claim that core `Cltc` perturbation is transcriptionally
  detectable while adaptor-tier, `Dnm1`, `Synj1`, `Bin1`-like, and
  presynaptic/endocytic neighboring perturbations are flat or sparse.
- Distributed Agents runtime `profile_neighbors`, used as a local sanity check on the
  observed focal signatures for `Cltc`, `Dnm1`, `Synj1`, and `Ap1b1` across the
  1,674 eligible training targets.  I did not use those raw whole-profile
  neighbors as mechanistic analogs because the focal surfaces of these anchors
  had only 1-3 significant features and the nearest full-surface matches were
  dominated by subthreshold ranks rather than by pathway-specific FDR overlap.
- PubMed literature:
  Xiao et al. 2006, *J. Biol. Chem.*, DOI `10.1074/jbc.M600265200`, PMID
  `16595675`; Davidson et al. 2009, *Eur. J. Neurosci.*, DOI
  `10.1111/j.1460-9568.2008.06563.x`, PMID `19120439`; Muthusamy et al. 2012,
  *J. Neurochem.*, DOI `10.1111/j.1471-4159.2012.07814.x`, PMID `22650988`;
  Ha et al. 2012, *J. Biol. Chem.*, DOI `10.1074/jbc.M112.370601`, PMID
  `22843680`.

## Focal-cell calibration

The focal training endpoint is very sparse:

- `1,674` non-held-out perturbations were present.
- `1,205 / 1,674`, or 72%, had `n_degs = 0`.
- The median was `0`; the 75th percentile was `1`; only 5% of perturbations had
  at least 18 DEGs.
- The largest responses were core RNA/proteostasis/chromatin perturbations
  such as `Uba5` with 2,677 DEGs, `Tpr` with 1,768, `Sin3a` with 1,433,
  `U2af2` with 828, `Psmb4` with 742, `Hnrnpu` with 733, and `Cdc40` with 624.

Within the focal parquet slice I compared Caly to training targets in three
mechanistic neighborhoods.

### Clathrin/endocytic and adaptor analogs

External work makes this the closest mechanistic neighborhood for CALY:
calcyon is a brain-enriched single-pass vesicular protein that binds clathrin
light chain and promotes clathrin-mediated endocytosis in neurons
(Xiao 2006), supports activity-dependent AMPA-receptor internalization and LTD
in hippocampal CA1 neurons (Davidson 2009), binds AP complex mu subunits and
particularly affects AP-3 cargo targeting in mouse brain (Muthusamy 2012), and
can help internalize dopamine D1 receptors through a PSD-95-containing complex
(Ha 2012).

The relevant focal training perturbations were uniformly small:

| training target | focal `n_degs` | focal expression evidence |
| --- | ---: | --- |
| `Cltc` | 3 | The only focal significant genes were `Rbms1`, `Ero1b`, and `Gabra4`, each with q = 0.042.  `Cltc` itself was not a focal DEG, although it is the corpus-positive counterexample showing that stronger core clathrin disruption can reach the nucleus in selected neuronal groups. |
| `Dnm1` | 1 | The sole focal DEG was `Dnm1` itself, log2FC -0.712, q = 4.09e-25; no downstream gene survived FDR 0.05. |
| `Synj1` | 1 | The sole focal DEG was `Synj1` itself, log2FC -0.583, q = 3.11e-07; no downstream endocytic or stress gene survived. |
| `Bin1` | 1 | The sole focal DEG was `Bin1` itself, log2FC -0.331, q = 3.1e-06. |
| `Cd2ap` | 0 | No gene passed FDR 0.05. |
| `Sh3kbp1` | 0 | No gene passed FDR 0.05. |
| `Dnajc5` | 1 | The sole focal DEG was `Dnajc5` itself, log2FC -0.480, q = 0.010. |
| `Ap1b1` | 1 | The sole focal DEG was `Ap1b1` itself, log2FC -0.537, q = 3.99e-04. |
| `Ap1s2` | 0 | No focal DEG. |
| `Ap3b1` | 0 | No focal DEG, even though AP-3 is the adaptor complex most directly connected to calcyon cargo targeting in Muthusamy 2012. |
| `Ap4s1` | 0 | No focal DEG. |
| `App` | 1 | The sole focal DEG was `App` itself; APP/endosomal AD-linked perturbations were not broad analogs of core `Cltc`. |
| `Prepl` | 1 | The sole focal DEG was `Prepl` itself. |
| `Ocrl` / `Inpp5k` | 0 / 0 | Endocytic phosphoinositide relatives were flat in this focal group. |

This strongly argues against a broad Caly downstream count.  Direct impairment
of vesicle fission (`Dnm1`), clathrin uncoating/phosphoinositide turnover
(`Synj1`), AP-1/AP-3/AP-4 adaptor components, and APP/clathrin accessory
scaffolds generally produced either zero DEGs or only the knocked-down target
itself.  `Cltc` and `Rab7` are useful counterexamples because they show
endosomal or coat perturbations can be large in this assay, but they are core
trafficking nodes; Caly is a neuronal accessory protein downstream of clathrin
light chain and AP-3 rather than the coat or late-endosome machinery itself.

### Synaptic-vesicle and receptor-scaffold comparators

CALY also touches synaptic receptor trafficking.  The focal training surface
again favored self-only or null responses:

| training target | focal `n_degs` | why it matters |
| --- | ---: | --- |
| `Syp` | 1 | Synaptic-vesicle membrane protein; only `Syp` itself was significant. |
| `Syn1` | 1 | Vesicle reserve-pool phosphoprotein; one focal DEG. |
| `Snca` | 0 | Presynaptic synuclein perturbation was flat. |
| `Sncb` | 1 | Only `Sncb` itself was significant. |
| `Nsf` / `Napb` | 0 / 0 | SNARE-cycle perturbations were flat. |
| `Stx1b` | 0 | Syntaxin-1B perturbation was flat. |
| `Vamp1` / `Stx16` | 1 / 1 | Both were self-only. |
| `Unc13a` / `Unc13b` | 0 / 0 | Vesicle-priming perturbations were flat. |
| `Dlg4` | 1 | PSD-95 scaffold; the only focal DEG was `Dlg4` itself, relevant because Ha 2012 links calcyon to dopamine D1 receptor trafficking through PSD-95. |
| `Drd2`, `Drd4`, `Drd5`, `Gnas`, `Gnal`, `Adcy3`, `Pde1c`, `Pde10a` | 0 each | Dopamine/GPCR/cAMP comparators did not expose a tonic receptor-signaling RNA module in this basal snRNA-seq context. |

The glutamate-receptor layer gave one major counterexample: `Grin1` produced 89
focal DEGs.  I treated that as a boundary rather than an analog because
`Grin1` removes the obligate NMDAR pore-forming subunit, whereas Caly modulates
activity-dependent AMPAR endocytosis and receptor trafficking.  The more
peripheral ionotropic glutamate receptor perturbations were small in the same
cell group: `Gria1` and `Gria2` had 0 DEGs, `Grin2a` had 1, and `Grin2b` had 2.

### Evidence for possible on-target detection

Although I did not predict downstream activation, I did not predict a hard
zero.  In the focal slice, `Caly` was a measured feature across all 1,674
training perturbations and was itself FDR-significant downstream of several
broad chromatin/RNA-binding perturbations (`Zbtb7a`, `Brd4`, `U2af2`,
`Hnrnpc`, `Ctcf`, `Wac`, and `Tardbp`).  That does not tell us Caly is easy to
knock down, but it does show that the transcript is present and detectable in
this cell type.  The closest Caly-like perturbations with detectable endpoint
counts were overwhelmingly one-gene self effects with on-target log2FC values
from roughly -0.33 to -0.71, which is the natural calibration for a weak
neuronal accessory endocytic target.

## Target prediction

### `Caly`: predicted `n_degs = 1`

The external biology puts CALY next to clathrin light chain, AP-3 sorting, AMPA
receptor internalization, and D1-receptor/PSD-95 trafficking, but the supplied
dataset shows that those local trafficking processes generally do not produce a
durable basal soma/nuclear transcriptomic module after sparse P16 CRISPR.  In
the exact focal cell group, the best analogs were either null (`Cd2ap`,
`Sh3kbp1`, `Ap3b1`, `Ap4s1`, `Snca`, `Nsf`, `Gria1`, `Gria2`, dopamine/GPCR
targets) or one-gene self hits (`Dnm1`, `Synj1`, `Bin1`, `Dnajc5`, `Ap1b1`,
`Dlg4`, `Syp`, `Vamp1`, `Stx16`).  The higher-count counterexamples, `Cltc`,
`Rab7`, and `Grin1`, are stronger core nodes and not good quantitative matches
for the accessory CALY branch.

I therefore expect no downstream DEG program but a reasonable chance that Caly
itself crosses FDR 0.05 as the single significant gene, giving a point estimate
of `1`.

## Limits

The most important limitation is that there is no direct Caly perturbation in
the parquet or in the Distributed Agents corpus.  CALY has no true paralog in the
training target set, and several of the most direct molecular partners were
absent as perturbations (`Clta`, `Cltb`, AP-2 subunits, neuronal AP-3 subunits,
`Grin2c`, `Snap25`, `Stx1a`, `Vamp2`, `Syt1`).  Existing Caly literature
measures transferrin uptake, AMPAR/D1 receptor internalization, LTD, and AP-3
cargo localization, none of which are the same as steady-state single-nucleus
RNA 3-4 weeks after mosaic CRISPR.

The predicted positive count is mostly an extrapolated on-target call.  If the
gRNA pool cuts poorly, if Caly protein loss is not coupled to mRNA decay, or if
Caly expression in `151 TH Prkcd Grin2c Glut` is too low in the exact matched
nuclei, the actual count could be `0`.  Conversely, a strong guide pool could
produce a `Cltc`-like stress response, but the training analogs make that less
likely than a null or self-only outcome.
