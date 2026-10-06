# Chrna5 DEG-count forecast

Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with
BH-adjusted Wilcoxon `p < 0.05`.

Target: `Chrna5`.

## Inputs used

- The one-row holdout manifest declares `Chrna5`.
- The declared `Chrna5` biology bundle supplies biology-only evidence and exact
  focal-population reach; it does not include the held-out differential
  expression signature or count.
- The `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table supplies exact
  training `n_degs` values for 1674 non-held-out targets.
- The declared all-cell-group Parquet was used only to inspect exact
  `151 TH Prkcd Grin2c Glut` FDR-significant rows for cholinergic receptor
  training perturbations.
- Packaged Findings for `Chrna3`, `Chrna4`, `Chrna7`, and `Chrnb2` were used as
  same-experiment semantic summaries of those training perturbations, not as an
  independent replication.

## Evidence

The exact target-reach measurement is extremely sparse in the requested
population: `Chrna5` is detected in 129 of 23,679 non-target `151` nuclei
(`0.5447865%`), with 180 total UMIs, mean raw UMI `0.0076017`, and
mean log1p CP10K `0.0028007`. That is the strongest quantitative reason to
expect little or no cell-autonomous nuclear RNA response after a sparse P16
edit: most recovered nuclei assigned to a `Chrna5` guide are unlikely to be
active `Chrna5`-expressing thalamic cells at baseline.

The biology bundle supports possible postnatal function but weak realization in
this exact assay window. Alpha5 is an accessory subunit of an assembled
heteromeric nicotinic receptor, adult mouse alpha5 loss has neural and thalamic
functional consequences, and alpha5-independent receptor complexes remain.
However, the edited P16 allele stops new alpha5 supply rather than disabling
pre-existing assembled receptors; the closest surface-receptor turnover proxy
supports persistence beyond two weeks, so the P37-P44 harvest is a
partial-depletion or leading-edge window rather than a complete receptor-loss
state.

The `151` endpoint is globally sparse in the training table. Of 1674 training
perturbations, 1205 have zero DEGs, 1481 have at most one DEG, and 1512 have at
most two; the median is 0, the 75th percentile is 1, and the 90th percentile is
2. The high-count tail is dominated by broad nuclear and proteostatic
regulators, not by ligand-gated channel subunits.

The most relevant measured perturbations, single nicotinic receptor subunits
and adjacent cholinergic receptor genes, were almost all null in this focal
class:

| training target set | exact `151` counts |
| --- | --- |
| `Chrna1`, `Chrna2`, `Chrna3`, `Chrna4`, `Chrna6`, `Chrna7` | `0, 0, 0, 2, 0, 0` |
| `Chrnb1`, `Chrnb2`, `Chrnb3` | `0, 1, 0` |
| `Chrnd`, `Chrne`, `Chrng` | `0, 0, 0` |
| `Chrm2`, `Chrm3`, `Ache` | `0, 0, 1` |

Among these 15 cholinergic receptor or degradation perturbations, the Parquet
has only four FDR<0.05 rows in `151`: `Ache` self, `Chrnb2` self, and for
`Chrna4` the self transcript plus `Cyp46a1`. Thus even genes with clearer
measured self-transcript depletion contributed no recurrent downstream
nicotinic program. The same-experiment Findings summarize the same boundary:
`Chrna3`, `Chrna7`, and `Chrnb2` were downstream-flat across recovered neuronal
groups, while `Chrna4` had only a one-gene thalamic downstream response that was
not phenocopied by `Chrnb2` or other represented receptor relatives.

The biology bundle names `Chrna3`, `Chrna4`, `Chrnb2`, and `Chrnb4` as receptor
context genes. In the training `151` count table, the available direct partners
are `Chrna3 = 0`, `Chrna4 = 2`, and `Chrnb2 = 1`; `Chrnb4` is not present. I
therefore weighted the available same-complex subunits over less specific ion
channels and treated their sparse counts as the main empirical analog set.

## Synthesis

`Chrna5` has credible receptor biology, but for this direct endpoint the
target is barely expressed in the exact assayed thalamic nuclei, acts through a
partly persistent assembled receptor stock, and belongs to a receptor-subunit
class that is transcriptionally buffered in the `151` training measurements.
Because `n_degs` includes the self transcript, the low exact `Chrna5`
expression also makes a one-DEG self-only call less likely than it was for
`Chrnb2` or `Chrna4`.

Point prediction: `0`.
