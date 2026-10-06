# Trace

## Target and endpoint

- Target: `Tnfrsf1b`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Predicted `n_degs`: `0`

## Evidence used

The declared biology bundle for `Tnfrsf1b` reports an exact in-assay reach of only
120 expressing non-target nuclei out of 23,679 in `151 TH Prkcd Grin2c Glut`,
with 127 total target UMIs, `0.5068%` expressing cells, `0.00536` mean raw UMI
per cell, and `0.336` pseudobulk CPM. That is direct focal-population expression
evidence for very sparse baseline `Tnfrsf1b` RNA.

The same bundle adjudicates the edited TNFR2 receptor stock as likely
substantially depleted by the P37-P44 harvest after P16 editing, because TNFR2 is
a regulatable surface receptor/signaling component rather than a durable
installed structure. I therefore did not treat this as a case where long-lived
pre-edit material should make the perturbation inactive. The limiting evidence
is instead context reach: postnatal neuronal TNFR2 function is documented under
hippocampal excitotoxic challenge, while baseline healthy thalamic neuron demand
is unresolved and adult mouse thalamic regional RNA is low.

The declared focal training table has 1,674 measured training targets in this
cell class. Its count distribution is heavily zero-inflated: 1,205 targets
had `n_degs = 0`, the median was `0`, 1,512 targets had `n_degs <= 2`, and only
59 targets had `n_degs >= 50`.

I used TNF/TNFR/NF-kB-side training perturbations as the closest measured
biological comparators rather than the large core-process outliers in the upper
tail of the count distribution. In the declared `151 TH Prkcd Grin2c Glut`
count table:

| training perturbation | focal `n_degs` |
|---|---:|
| `Tnfrsf1a` | 0 |
| `Traf3` | 0 |
| `Nfkb1` | 0 |
| `Rel` | 0 |
| `Chuk` | 0 |

The declared expression parquet matched those count-table zeros in the exact
focal class. Directly filtering `training_de_all_cell_groups.parquet` to
`151 TH Prkcd Grin2c Glut` showed 17,259 measured genes for each of those five
perturbations, with zero genes at `pvals_adj < 0.05` and also zero genes at
`pvals_adj < 0.10`.

Packaged same-experiment Findings give the same biological interpretation, not
an independent replication. `Tnfrsf1a:F002` reports that basal `Tnfrsf1a`
perturbation did not induce a TNF/NF-kB immediate program and that intracellular
TNFR/NF-kB neighbors were flat. `Traf3:F004` reports that represented
TNFR/TLR/NF-kB relatives did not phenocopy `Traf3`, with `Cd40`, `Chuk`,
`Map3k7`, `Nfkb1`, `Rel`, `Tlr2`, `Tlr4`, and `Tnfrsf1a` all yielding
zero downstream FDR `< 0.10` genes on their own matched neuronal surfaces.

## Synthesis

The count-table base rate alone makes a zero or near-zero answer the default in
this focal thalamic class. The target-specific biology pulls further toward
zero: `Tnfrsf1b` is an inducible TNF-family receptor with extremely sparse
focal expression, and the represented receptor-side/TNF/TLR/NF-kB module is
measured as transcriptionally silent in the unchallenged postnatal neuronal
setting. Functional depletion of the receptor by harvest prevents me from
dismissing editing outright, but it is not enough to overcome the weak baseline
ligand/context evidence.

I therefore predicted no detectable downstream DE genes at BH-adjusted
Wilcoxon `p < 0.05`.
