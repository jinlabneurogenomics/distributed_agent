# Direct `n_degs` forecast for `Vps13d`

## Declared target and endpoint

- **Target:** `Vps13d`, from the one-row holdout manifest at `[local file: Vps13d.csv]`.
- **Cell class:** `151 TH Prkcd Grin2c Glut`.
- **Endpoint:** number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- **Outcome-blind inputs used:** the declared biology bundle `biology_bundles/Vps13d.json`, the declared training count table `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, and focal training rows from `training_de_all_cell_groups.parquet`.
- The held-out `Vps13d` count was absent from the training count table; no `Vps13d` profile rows were used.

## Biology that set the direction

The structured `Vps13d` bundle makes a real neuronal perturbation plausible in this assay:

- In the exact assayed population, `Vps13d` was detected in `20,815 / 23,679` non-target nuclei: `87.9049%` expressing, mean raw UMI `2.5206`, mean CP10K `1.6016`, pseudobulk CPM `157.9742`.
- The functional-stock adjudication called VPS13D operative capacity **likely substantially depleted** by P37-P44 after P16 editing, but with partial evidence completeness because target-specific VPS13D protein half-life in juvenile thalamic neurons was unknown.
- The source card placed VPS13D at mitochondrial size/fission/clearance and peroxisome biogenesis through organelle contacts.
- Prior loss data supported postnatal neuronal observability in another mouse excitatory-neuron context: conditional Vps13d loss produced mitochondrial abnormalities and later neuronal loss in hippocampal/cortical excitatory neurons, while primary neurons showed dysfunction over a roughly 12-16 day scale.
- Two caveats kept the estimate low: pre-existing protein and organelles can persist after editing, and the single-nucleus readout is survivor-conditioned.

## Focal training measurements

The declared `151 TH Prkcd Grin2c Glut` training table contained `1,674` perturbations. It was sparse: `1,205` had `0` DEGs, the median was `0`, the 90th percentile was `2`, the 95th percentile was `18`, the 99th percentile was `430`, and the mean was `14.05`.

Closest functional training perturbations were mostly silent or tiny:

| group | focal counts |
|---|---|
| VPS13 paralogs | `Vps13a=0`, `Vps13b=0`, `Vps13c=0` |
| peroxisome | `Pex1=0`, `Abcd3=0`, `Acbd5=0`, `Pex14=1` |
| autophagy/mitophagy | `Atg5=0`, `Becn1=0`, `Map1lc3a=1`, `Park7=1`, `Sqstm1=1`, `Rb1cc1=4` |
| mitochondrial dynamics/transport | `Mff=0`, `Rhot1=0`, `Trak1=0`, `Yme1l1=0`, `Opa1=37` |
| broad organelle-stress context | `Nrf1=138`, `Rab7=501`, `Ufc1=572`, `Uba5=2677` |

I also compared 23 selected mitochondria/peroxisome/autophagy/VPS-family or stress-boundary targets in the focal group from the expression Parquet. The comparison had no missing profiles; among these 23 training perturbations, 13 had no significant genes, 5 had 1-9, 1 had 10-49, and 4 had at least 50. Pairwise tail overlap across the cohort was weak enough that the high-count `Rab7`, `Ufc1`, and `Uba5` signatures were treated as broad stress boundaries rather than scale donors for VPS13D.

## Packaged same-experiment context

The corpus reports matched the numeric split above:

- `Opa1` generated an ATF4/ISR-like mitochondrial response, but its closest FDR-confirmed neighbors were mostly noncanonical stress perturbations, and represented fission/OPA1-processing targets did not phenocopy it.
- `Pex14` was transcriptionally buffered, without broad downstream FDR signal across measured neuronal groups.
- `Vps13a` was buffered and `Vps13b` was a whole-transcriptome null; the represented VPS13 paralogs did not form a shared acute neuronal signature.
- `Rab7`, `Ufc1`, and `Uba5` carried strong lysosomal, UFMylation, or generic organelle-stress programs in this thalamic class, but those are more proximal and broader stress perturbations than VPS13D's organelle-contact maintenance defect.

## Point synthesis

I set the point above zero because `Vps13d` was broadly expressed in the exact thalamic focal population and its bundle supported loss of operative mitochondrial/peroxisomal maintenance during the P16-to-P37/P44 window. I kept it well below the `Opa1` count of 37 and far below `Rab7`/`UFC1`/`UBA5`-scale stress because most closer peroxisomal, VPS-family, mitophagy, and mitochondrial-dynamics perturbations were 0-4 DEGs in this same cell class, and the survivor-conditioned readout can miss cells that have progressed too far into VPS13D-dependent failure.

**Predicted `n_degs`: 12**
