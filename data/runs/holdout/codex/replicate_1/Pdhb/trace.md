# Pdhb DEG-count prediction

## Target and endpoint

- The one-row holdout manifest names `Pdhb` as the target.
- The requested endpoint is `n_degs` in `151 TH Prkcd Grin2c Glut`: the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the focal thalamic glutamatergic population.

## Evidence used

### Canonical target biology

The declared `biology_bundles/Pdhb.json` bundle identifies PDHB as an obligate beta subunit of the mitochondrial pyruvate dehydrogenase E1 alpha2-beta2 heterotetramer. A disruptive edit is therefore biologically meaningful, with no located mouse same-context beta-subunit paralog. The exact in-assay expression measurement also supports target reach in the focal population: `Pdhb` was detected in 21,831 of 23,679 non-target nuclei, 92.20%, with pseudobulk CPM 216.95 and mean raw UMI 3.46.

The same bundle tempers that reach: editing stops new beta-subunit production but does not directly disable pre-existing E1 heterotetramers. PDHB protein can undergo proteasomal degradation, but the bundle found no matched P16-to-P37/P44 half-life or acute postmitotic thalamic loss clock, so the functional stock call is `partially_depleted_or_leading_edge` rather than substantially depleted at harvest.

### Training counts in the focal population

The declared training count table for `151 TH Prkcd Grin2c Glut` is very sparse: 1,205 of 1,674 training perturbations have `n_degs = 0`, 1,481 have `n_degs <= 1`, and the median is 0.

Biochemical neighbors of `Pdhb` that are present in the training table are all at the same near-null scale in the focal population:

| target | role | `n_degs` |
| --- | --- | ---: |
| `Pdha1` | PDH E1 alpha partner | 1 |
| `Dlat` | PDH E2 core | 1 |
| `Dld` | PDH / OGDH / BCKDH E3 subunit | 0 |
| `Mpc1` | mitochondrial pyruvate carrier | 0 |
| `Aco2` | TCA aconitase | 0 |
| `Dlst` | OGDH E2 core | 0 |
| `Ogdh` | OGDH E1 | 0 |
| `Idh3a` | TCA isocitrate dehydrogenase | 1 |
| `Mdh2` | TCA malate dehydrogenase | 1 |
| `Ndufs4` | complex I | 0 |
| `Sdha` | complex II / TCA | 1 |
| `Suclg1` | TCA succinyl-CoA ligase | 0 |
| `Sucla2` | TCA succinyl-CoA ligase | 1 |
| `Nfs1` | mitochondrial Fe-S biogenesis | 0 |
| `Isca2` | mitochondrial Fe-S biogenesis | 1 |

For the closer PDH/TCA subset that I checked directly in `training_de_all_cell_groups.parquet`, the only BH<0.05 rows were self-transcript hits. `Pdha1`, `Dlat`, `Idh3a`, `Ndufs2`, `Sdha`, and `Sucla2` each had one significant row, and in every case that row was `names == gene_target`; `Dld`, `Mpc1`, `Aco2`, `Dlst`, `Ogdh`, `Ndufv1`, and `Cox4i1` had no BH<0.05 row in the same exact focal context.

### Same-experiment corpus around measured analogs

The selected same-experiment Finding ledger supports interpreting those low counts as a pathway-local boundary rather than as a single anomalous target. `Pdha1:F004` reports that measured PDC comparators `Dlat`, `Dld`, and `Mpc1` were flat or nearly flat and that related TCA comparators were also sparse. `Dlat:F004` reports that expected PDC and adjacent mitochondrial-carbon comparators failed to phenocopy the `Dlat` singleton response in `151 TH Prkcd Grin2c Glut`. `Dld:F001` and `Dld:F003` report a buffered `Dld` perturbation and sparse/null DLD-pathway comparator responses. Those corpus records use the same experiment and a report-level FDR<0.10 downstream framing, so I used them only as qualitative context for the exact BH<0.05 counts above.

## Synthesis

`Pdhb` has better target reach than many silent genes, and as the PDH E1 beta subunit it is a direct counterpart of measured `Pdha1`; that argues against treating it like an unrelated zero-inflated prior draw. The functional-stock card weakens the case for a large response, however, because a P16 edit may only begin eroding pre-existing assembled E1 by the P37-P44 harvest.

Most importantly, the measured PDH axis in this focal population does not produce a downstream nuclear program at BH<0.05. The two closest present PDH subunits, `Pdha1` and `Dlat`, land at `n_degs = 1`, and the Parquet shows those counts are their own target transcripts rather than downstream stress or identity markers. I therefore predict that `Pdhb` will be similarly self-transcript-only, with no additional downstream DE genes crossing BH<0.05.

Point prediction: `1`
