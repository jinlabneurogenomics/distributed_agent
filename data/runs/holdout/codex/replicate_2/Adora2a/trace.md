# Direct forecast trace

## Target and endpoint

- Target: `Adora2a`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes in this class with Wilcoxon `pvals_adj < 0.05`
- Point prediction: `0`

The `Adora2a` row is absent from
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, and the target contrast is
absent from `training_de_all_cell_groups.parquet`. The selected same-experiment
corpus also had no `Adora2a` Finding, Claim, or explicit comparator record, so
there was no packaged target signature to reuse.

## Evidence used

### Exact target biology

The biology-only `Adora2a.json` bundle reports exact non-target expression in
the focal population:

- 434 of 23,679 focal non-target nuclei expressed `Adora2a`
- `pct_cells_expressing = 1.8328476709320496`
- `mean_raw_umi = 0.03146247730056168`
- `mean_cp10k = 0.01604567840326096`
- `pseudobulk_cpm = 1.9718650222554612`

The same bundle favors functional A2A receptor depletion over the 21-28 day
CRISPR window in cells that are successfully edited and express the receptor,
because new receptor supply should stop and receptor pools are regulatable.
That realization prior does not overcome the exact reach measurement: in this
aggregated thalamic-glutamatergic class the transcript is near the floor and is
seen in fewer than 2% of control nuclei. The curated mouse loss phenotypes are
from forebrain or striatal neuronal contexts rather than matched juvenile
thalamus, and family compensation by other adenosine receptors is unresolved.

### Training endpoint distribution

The declared `151 TH Prkcd Grin2c Glut` training count table contains 1,674
observed targets:

- 1,205/1,674 have `n_degs = 0`
- 1,481/1,674 have `n_degs <= 1`
- median `n_degs = 0`
- 75th percentile `n_degs = 1`
- 90th percentile `n_degs = 2`

The mean count, 14.05, is not representative of the typical perturbation
because a small set of housekeeping or regulatory genes produces hundreds to
thousands of DEGs. `Adora2a` does not have that broad-regulator biology and is
expressed sparsely in the focal nuclei.

### Training analogs

I used the local gene-analog nomination skill with the declared training table
as the availability universe. Its priority index is a typed biological
inspection order rather than an endpoint score, so I interpreted the nominated
genes through their actual `151` counts and Parquet profiles.

Among the first 100 nominated training genes:

- 72 had `n_degs = 0`
- 24 had `n_degs = 1` or `2`
- 1 had `n_degs = 3` to `9`
- 3 had `n_degs >= 10`
- median `n_degs = 0`, 75th percentile `= 1`, 95th percentile `= 2`

The top 20 nominated genes were also mostly silent:

| gene | `n_degs` |
| --- | ---: |
| `P2ry12` | 0 |
| `Drd2` | 0 |
| `Pparg` | 0 |
| `Drd4` | 0 |
| `Fyn` | 0 |
| `Cacna1d` | 0 |
| `Grin1` | 89 |
| `Adra2a` | 0 |
| `Chrna7` | 0 |
| `Chrna3` | 0 |
| `Adcy1` | 0 |
| `Chrna4` | 2 |
| `Adcy5` | 0 |
| `Grin2b` | 2 |
| `Creb1` | 10 |
| `Chrnb2` | 1 |
| `Chrna2` | 0 |
| `Calm3` | 1 |
| `Grin2a` | 1 |
| `Grik1` | 0 |

The few outliers do not look like positive evidence for `Adora2a`. `Grin1`
is the obligatory NMDA receptor subunit in glutamatergic neurons and had an
89-gene profile in the Parquet; `Creb1` is a downstream transcription factor
with 10 DEGs. They are broader signaling machinery than a sparsely expressed
A2A GPCR. The nearer receptor and G-protein/cAMP perturbations were quiet:
`P2ry12`, `Drd2`, `Drd4`, `Adra2a`, `Adcy1`, `Adcy5`, and `Gnas` all had
`n_degs = 0`; other neurotransmitter GPCR families in the table were likewise
almost always zero or one.

The matched Parquet check confirmed that 13 of the first 20 nominated genes
had no significant feature at FDR 0.05 in `151`, five had only 1-9, one had
10-49, and one had at least 50. In the same 20-gene cohort, signed feature
overlap was weak rather than a coherent A2A-like module, so I did not average
the `Grin1` footprint into the receptor comparators.

## Synthesis

The forecast is dominated by three converging observations:

1. `Adora2a` has extremely sparse focal expression in the exact in-assay
   non-target nuclei, making an aggregate class-wide DE signature difficult to
   detect even if edited expressing cells lose receptor function.
2. The matched training endpoint has a large atom at zero: more than 70% of
   observed targets are silent in this cell class and the 75th percentile is
   only one DEG.
3. Training genes in receptor, purinergic, dopaminergic, adenylyl-cyclase, and
   G-protein neighborhoods are overwhelmingly silent; the nonzero analog
   outliers are broader synaptic or transcriptional regulators rather than
   sparse A2A receptor perturbations.

I therefore predict no BH-significant measured gene for `Adora2a` in
`151 TH Prkcd Grin2c Glut`.
