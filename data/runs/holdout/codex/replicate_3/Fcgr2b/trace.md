# Fcgr2b forecast

## Declared target and endpoint

- Target: `Fcgr2b`, the single row in the declared holdout manifest.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the number of measured genes in this focal class with Wilcoxon `pvals_adj < 0.05`.

## Biology used

The prediction-safe Fcgr2b biology bundle supports target engagement but weak focal reach:

- Fcgr2b is a low-affinity IgG Fc receptor with inhibitory ITIM signaling and immune-complex uptake functions characterized mainly in B cells, myeloid cells, and microglia.
- The receptor is a renewable membrane/recycling-pool protein, so a P16 disruptive edit can plausibly deplete new supply by the P37-P44 harvest, although endogenous mouse neuronal receptor turnover is not directly known.
- Prior neural phenotypes come from adult systemic knockout or amyloid-beta/disease models, not from an acute healthy thalamic-neuron loss setting.
- Exact focal-population expression is extremely sparse: 119 Fcgr2b UMIs across 23,679 matched non-target `151 TH Prkcd Grin2c Glut` nuclei, with 105 expressing nuclei, `0.443%` expressing, mean raw UMI `0.00503`, and pseudobulk `0.315` cpm.

Thus I treated Fcgr2b as biologically real where Fc receptor signaling is installed, but mostly outside the assayed NeuN-positive thalamic glutamatergic population. The dominant bearing for this endpoint was therefore loss of population reach, not uncertain receptor persistence.

## Training measurements used

The held-out target itself is absent from the focal training count table. In the 1,674 available `151 TH Prkcd Grin2c Glut` training perturbations, 1,205 had zero DEGs; the median was `0`, the 90th percentile was `2`, and only 128 perturbations exceeded five DEGs. This cell class can show very large responses for broadly used neuronal or housekeeping targets, but its count distribution is still strongly zero-inflated.

I then checked focal Parquet rows for training perturbations chosen before looking at their row-level signatures because they share immune, microglial, Fc-receptor-family, or leukocyte-associated biology with Fcgr2b rather than broad thalamic neuronal function:

| training target | focal `n_degs` | Parquet rows in focal class | BH < 0.05 rows |
|---|---:|---:|---:|
| `Axl` | 0 | 17,259 | 0 |
| `Cd14` | 0 | 17,259 | 0 |
| `Cd36` | 0 | 17,259 | 0 |
| `Csf1r` | 0 | 17,259 | 0 |
| `Cx3cr1` | 0 | 17,259 | 0 |
| `Fcgr4` | 0 | 17,259 | 0 |
| `H2-Eb1` | 0 | 17,259 | 0 |
| `Irf8` | 0 | 17,259 | 0 |
| `Lgals3` | 0 | 17,259 | 0 |
| `P2ry12` | 0 | 17,259 | 0 |
| `Ptprc` | 0 | 17,259 | 0 |
| `Spi1` | 0 | 17,259 | 0 |

The all-zero measurements for this preselected immune/microglial group outweighed generic low-count uncertainty. Their recovered perturbed-cell counts were within the same order as the assay's sparse design, so the result is not evidence of impossibility, but it is the most endpoint-matched evidence for this biology in this focal neuronal class.

## Point synthesis

Fcgr2b loss is likely molecularly realized in rare cells that genuinely express the receptor by harvest, but Fcgr2b has almost no focal baseline expression, its strongest priors are non-neuronal or disease/stress-dependent, and available immune/microglial training perturbations do not produce any BH-significant genes in the same thalamic glutamatergic Parquet slice. I therefore forecast no detectable population-level survivor transcriptional response in `151 TH Prkcd Grin2c Glut`.

Predicted `n_degs`: `0`
