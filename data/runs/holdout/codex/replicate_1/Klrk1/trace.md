# Klrk1 `n_degs` forecast

## Target and endpoint

- Target manifest: `Klrk1`.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05` in this cell class.
- The target expression signature and target DEG count were withheld; the forecast below does not use a `Klrk1` outcome.

## Biology used

The declared biology bundle identifies Klrk1 as the mouse NKG2D immune receptor. The active protein is a surface homodimer that signals through DAP10 or DAP12 adaptors; CRISPR loss of function should deplete newly made receptor complexes by the P37-P44 harvest if the gene is actually expressed in an edited cell. The limiting issue is context, not stock persistence: the curated loss phenotypes are immune, tumor-surveillance, infection, or systemic neuroinflammatory phenotypes, and the bundle found no matched healthy thalamic neuron-autonomous requirement.

The exact focal-population reach was essentially absent:

- `n_non_target_cells = 23679`
- `n_cells_expressing = 6`
- `pct_cells_expressing = 0.0253389`
- `total_target_umi = 6`
- `pseudobulk_cpm = 0.0158808`

Self expression is not a quantitative editing-efficiency readout, but for a receptor whose established function requires the receptor itself to be present, six total UMIs across the matched non-target thalamic nuclei strongly argues against a broad NKG2D-dependent transcriptional state in `151 TH Prkcd Grin2c Glut`.

The same-experiment corpus had no `Klrk1` report, Finding, Claim, or explicit comparator reference, so there was no packaged Klrk1 profile evidence to use or to override the biology bundle.

## Training evidence used

The declared focal count table contained 1,674 training perturbations. Its empirical scale was sparse:

- `1205 / 1674` training targets had `n_degs = 0`.
- `1481 / 1674` had `n_degs <= 1`.
- `1546 / 1674` had `n_degs <= 5`.
- Median `n_degs` was `0`.

High counts existed in this high-yield class, but they concentrated in broadly expressed regulatory and cell-biological genes such as `Uba5`, `Tpr`, `Sin3a`, spliceosome/proteasome targets, and other essential machinery. `Klrk1` is biologically unlike those broad responders.

The nearest useful internal comparators were not exact NKG2D components, because `Hcst`, `Tyrobp`, and Klr-family receptors were not in the focal 1,674-target count table. The closest measured boundary was lymphocyte immunoreceptor machinery in the same neuronal assay:

| training target | focal `n_degs` |
| --- | ---: |
| `Cd247` | 0 |
| `Cd3d` | 0 |
| `Cd3e` | 0 |
| `Cd3g` | 0 |
| `Cd4` | 0 |
| `Cd79a` | 0 |
| `Cd79b` | 0 |
| `Fyn` | 0 |
| `H2-Eb1` | 0 |
| `Icos` | 0 |
| `Ptprc` | 0 |

Direct Parquet inspection in `151 TH Prkcd Grin2c Glut` confirmed that each of these profiles had 17,259 measured-gene rows and zero BH `p < 0.05` genes; matched perturbed-cell counts were 125-223 against 23,679 matched controls, so these were observed quiet perturbations rather than absent targets.

Packaged same-experiment interpretation supported using this cohort as a boundary: `Cd247` produced no FDR < 0.10 downstream gene in any of 22 measured NeuN-positive neuronal groups, `Cd4` was likewise pan-flat on the recovered neuronal transcriptomic axis, and the corpus Claim over `Cd247`, `Cd3d`, `Cd3e`, `Cd3g`, `Cd4`, `Cd79a`, and `Cd79b` summarized these TCR/CD3/BCR-related perturbations as flat, sparse, or nonconvergent rather than a latent shared immune-receptor RNA module in NeuN-positive nuclei.

## Forecast

The positive case for Klrk1 was only that a successful edit can deplete a dynamic receptor if it is present. The stronger endpoint-matched bearings were downward: exact in-assay expression was near zero, the known Klrk1 biology is immune-cell restricted, matched neuronal phenotypes were unresolved, same-assay lymphocyte receptor comparators were FDR-flat, and the focal count table's baseline expectation is already zero-inflated.

I therefore predict a literal null in this focal population:

`predicted_n_degs = 0`
