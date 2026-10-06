# Direct `n_degs` prediction for `Fcgr2b`

## Endpoint

- Target: `Fcgr2b`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Requested prediction: held-out `n_degs`; the target signature itself was not queried or used.

## Evidence used

### Exact Fcgr2b reach in the focal population

The declared biology bundle places the target transcript at the floor of the
assayed TH neuronal population:

- `n_non_target_cells`: 23,679
- `n_cells_expressing`: 105
- `pct_cells_expressing`: 0.4434%
- `total_target_umi`: 119 across `377,814,907` total non-target RNA UMIs
- `mean_raw_umi`: 0.0050
- `mean_cp10k`: 0.0031
- `pseudobulk_cpm`: 0.3150

Thus a sparse CRISPR loss in NeuN-positive TH nuclei is expected to edit mostly
cells with little or no Fcgr2b RNA to remove. The card still favors realized
protein depletion in cells that truly use the receptor by P37-P44:
`functional_stock_by_harvest = likely_substantially_depleted`; this is a
renewable membrane receptor whose new supply stops after editing. That
realization prior does not by itself overcome the extremely small exact
population reach.

### Biology of the perturbed gene

The canonical card describes Fcgr2b as a low-affinity IgG Fc receptor with an
ITIM-mediated inhibitory function and immune-complex uptake roles. Its direct
mouse neural evidence is outside the requested context: germline/systemic adult
seizure phenotypes, amyloid-beta stress models, and microglial Fc-receptor
biology. The same card specifically records that normal-brain atlas evidence
places FCGR2B primarily in CNS macrophage, leukocyte, and vascular-associated
smooth-muscle clusters, with mouse primary evidence for microglial expression,
not broad baseline expression in healthy juvenile thalamic neurons.

I therefore treated Fcgr2b as a likely real perturbation in Fcgr2b-positive
immune or disease-induced neuronal states, but as a poor-match perturbation for
healthy `151 TH Prkcd Grin2c Glut` nuclei.

### Training-count scale

The declared focal-population training table contains 1,674 held-in targets.
Its response distribution is strongly zero-inflated:

- `n_degs = 0`: 1,205 / 1,674 = 72.0%
- `n_degs <= 1`: 1,481 / 1,674 = 88.5%
- median: 0
- 75th percentile: 1
- 90th percentile: 2
- 95th percentile: 18
- maximum: 2,677

The large responses were dominated by core neuronal housekeeping, RNA
processing, and proteostasis perturbations such as `Uba5`, `Tpr`, `Sin3a`,
`Rnpc3`, `Zbtb7a`, `U2af2`, and `Psmb4`. Fcgr2b does not share that broad
cell-autonomous machinery logic.

### Held-in immune/Fc comparators

I used the count table to check a receptor/immune stratum that is closer to
Fcgr2b's expected biology than the high-response housekeeping tail. In the same
`151 TH Prkcd Grin2c Glut` endpoint, all of these held-in perturbations had
`n_degs = 0`:

`Fcgr4`, `Csf1r`, `Cx3cr1`, `Cd14`, `Cd36`, `Cd40`, `Cd80`, `H2-Eb1`, `Spi1`,
`Irf1`, `Irf2`, `Irf3`, `Irf5`, `Irf8`, and `Irf9`.

The declared Parquet confirmed that those 15 perturbations contributed 258,885
focal-population measured-gene rows, 17,259 per target, with zero rows at
`pvals_adj < 0.05`. Their matched perturbed counts ranged from 123 to 258
against 23,679 matched controls. Fourteen of the fifteen had best
`pvals_adj = 1.0`; the most active was still nonsignificant
(`Irf8`, best `pvals_adj = 0.1214`).

## Synthesis

Fcgr2b has enough receptor-turnover biology that loss can matter where the
gene is expressed, but its exact baseline reach in the assayed TH neurons is
only 105 / 23,679 nuclei. The endpoint is a BH-thresholded transcriptional
signature among recovered NeuN-positive thalamic nuclei, and the local training
data show that both the screen overall and same-compartment immune receptor
perturbations are usually silent at this threshold.

The best point prediction is therefore the zero mode of the held-in
distribution, with the Fc/immune comparator subset supporting zero rather than
rounding to one.

Predicted `n_degs`: `0`
