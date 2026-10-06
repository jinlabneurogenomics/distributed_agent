# Irf6 prediction trace

## Target and endpoint

- Target: `Irf6`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the focal population

## Evidence used

### Exact focal expression

The declared biology bundle reports direct non-target expression for `Irf6` in `151 TH Prkcd Grin2c Glut`:

- `n_non_target_cells = 23679`
- `n_cells_expressing = 13`
- `pct_cells_expressing = 0.05490096710165125`
- `total_target_umi = 13`
- `mean_raw_umi = 0.0005490096710165125`
- `mean_cp10k = 0.0004143554107701387`
- `pseudobulk_cpm = 0.0344083829386859`

This is the most decisive biology-side observation. `Irf6` is effectively unexpressed in the assayed focal thalamic glutamatergic nuclei, so an otherwise functional edit has almost no directly perturbed transcription-factor pool to remove in the aggregate population assayed by the Wilcoxon contrast.

### Functional stock and source-card biology

The same canonical bundle adjudicates IRF6 as a renewable intracellular IRF-family DNA-binding transcription factor, with no evidence for an installed long-lived postmitotic structure. Its functional stock was judged `likely_substantially_depleted` by the P37-P44 harvest in cells where the P16 edit successfully interrupts ongoing supply.

That makes lack of turnover a weak explanation for a quiet outcome, but the rest of the source card points away from a strong focal neuronal response: the strongest mouse loss phenotypes are germline/developmental and largely epithelial; the adult brain morphology observation was lifelong heterozygosity, not acute postnatal thalamic loss; and the neuronal evidence comes from injured embryonic cortical culture rather than healthy postnatal thalamic neurons.

### Training count table

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table is extremely zero-heavy:

- 1,674 training perturbations total
- 1,205 with `n_degs = 0` in this focal class
- 1,481 with `n_degs <= 1`
- median `n_degs = 0`
- 90th percentile `n_degs = 2`
- mean `n_degs = 14.05`, inflated by a small tail of broad RNA-processing, proteostasis, trafficking, and chromatin regulators

This empirical distribution makes a zero-count call a strong default unless the target is expressed and has training analogs with a large 151 signature.

### Chosen biological training perturbations

I interpreted the IRF-family and nearby immune/developmental transcription-factor perturbations as the most informative local controls for the biology card, then checked their focal counts:

| training target | focal `n_degs` |
|---|---:|
| `Irf1` | 0 |
| `Irf2` | 0 |
| `Irf3` | 0 |
| `Irf5` | 0 |
| `Irf8` | 0 |
| `Irf9` | 0 |
| `Trp63` | 0 |
| `Nfkb1` | 0 |
| `Rel` | 0 |
| `Stat1` | 1 |
| `Stat3` | 0 |

`Irf5` is the paralog called out in the source card, and the measured IRF-family perturbations were uniformly transcriptionally silent in the focal class.

### Parquet profile check

I queried the declared `training_de_all_cell_groups.parquet` for `group_name == "151 TH Prkcd Grin2c Glut"` and the same IRF-family peers. Each had 17,259 measured-gene rows in this class, matched-control depth of 23,679 nuclei, and no BH-significant genes:

| perturbation | measured genes | Parquet `n(padj < 0.05)` | minimum `pvals_adj` |
|---|---:|---:|---:|
| `Irf1` | 17,259 | 0 | 1 |
| `Irf2` | 17,259 | 0 | 1 |
| `Irf3` | 17,259 | 0 | 1 |
| `Irf5` | 17,259 | 0 | 0.788907 |
| `Irf8` | 17,259 | 0 | 0.121418 |
| `Irf9` | 17,259 | 0 | 1 |

This Parquet slice confirms that the family-level zero counts are not just barely missed DEG calls; the focal class shows no coherent IRF-loss signature among the observed training perturbations.

## Synthesis

The forecast rests on three aligned pieces of evidence: exact focal `Irf6` expression is nearly absent; acute postnatal thalamic biology for IRF6 is weak compared with developmental epithelial biology; and every measured IRF-family training perturbation is zero-DEG in this same high-yield focal class. Because only 13 of 23,679 non-target nuclei had any `Irf6` UMI, a population-level Wilcoxon signature would require a rare expressing subpopulation to carry an unusually large, synchronized downstream state. The training table shows that even this permissive class is usually silent unless the perturbed gene has broad focal-cell activity, which `Irf6` does not.

Predicted `n_degs`: `0`
