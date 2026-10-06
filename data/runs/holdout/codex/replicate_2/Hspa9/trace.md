# Hspa9 direct DEG-count forecast

## Requested endpoint

- Target: `Hspa9`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Point prediction: `1`

I treated the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` as
the observed training endpoint table and
`training_de_all_cell_groups.parquet` as the exact training DE surface. `Hspa9`
was absent from the visible 1,674-target count table, so no target signature or
target count was used.

## Biology used

The declared Hspa9 bundle identified HSPA9 as the mitochondrial HSP70
matrix chaperone for protein import, folding, assembly/quality control, and
iron-sulfur machinery. The focal thalamic population expressed `Hspa9`
detectably but not ubiquitously: 10,522 of 23,679 non-target nuclei
expressed it, with mean log1p CP10K 0.270 and 40.97 pseudobulk CPM.

The same bundle argued that a disruptive edit should stop new HSPA9 supply
while leaving pre-edit mitochondrial protein initially active. It retained
target-specific evidence for HSPA9 turnover through ClpXP but no transferable
juvenile-neuron half-life, and adjudicated the P37-P44 stock state as
`partially_depleted_or_leading_edge`. That made a very large, immediate stress
signature less likely than for short-lived essential RNA or proteasome factors.

## Training evidence

The 1,674 visible training targets in the focal class are highly sparse:
median `n_degs = 0`, third quartile `1`, 90th percentile `2`, 95th percentile
`18`, and only 106 targets had at least 10 DEGs.

Hspa9's most direct visible local analogs were quieter than the global
mean:

| comparator set | visible genes and `n_degs` | summary |
| --- | --- | --- |
| Matrix chaperone / Fe-S / matrix proteostasis / respiratory clients | `Aco2=0`, `Afg3l2=0`, `Clpp=0`, `Clpx=0`, `Dnajc19=0`, `Lonp1=0`, `Nfs1=0`, `Yme1l1=0` | 8/8 at zero |
| Slightly expanded mitochondrial import / Fe-S set | the genes above plus `Isca2=1`, `Tomm40=1` | median 0, mean 0.2 |
| Non-mitochondrial HSP70 chaperones | `Hspa5=5`, `Hspa8=9` | weak upward evidence, but different compartments |
| Mitochondrial dynamics upper boundary | `Opa1=37` | shows a mitochondrial perturbation can be visible, but is a different process |

I also compared thirteen selected mitochondrial/chaperone profiles
symmetrically in the declared Parquet under
`group_name = "151 TH Prkcd Grin2c Glut"`. Eight had no significant features,
four had 1-9 significant features, and only `Opa1` was in the 10-49 bin
with 37 DEGs. That supported using the direct matrix perturbations as the
scale center and treating `Hspa5`, `Hspa8`, and `Opa1` as only upward
boundaries.

## Synthesis

The direct analogs favored an outcome very near zero: Hspa9 loss converges
on mitochondrial import/folding and Fe-S biology, and the visible perturbations
nearest those processes were `0` to `1` in this exact population. I did not set
the point to zero because Hspa9 is expressed in a large minority of focal
nuclei, is broader than the visible single-client and ClpXP perturbations, and
has postnatal neural loss evidence in the biology bundle. The partial-stock
adjudication and quiet local mitochondrial training counts kept the estimate
below the ER/cytosolic HSP70 rows and far below the Opa1 boundary.

Balancing those bearings, the most defensible integer point is one significant
gene.
