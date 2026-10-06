# Direct DEG-count forecast for Dlx5

## Target and endpoint

- Target: `Dlx5`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes in this focal class with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Point prediction: `0`

## Decisive biological evidence

The biology bundle supports target engagement in the narrow sense that DLX5 is a renewable nuclear homeobox transcription factor: an acute disruptive coding edit should stop new functional DLX5 synthesis, and a 21-28 day interval is likely long enough for much of the pre-existing free protein pool to turn over. That made a silent prediction depend mainly on focal-population reach rather than on persistence of pre-edit protein.

The exact in-assay reach, however, is extremely low in the requested thalamic glutamatergic population. Among `151 TH Prkcd Grin2c Glut` non-target nuclei, `Dlx5` had:

- `207 / 23679` nuclei expressing the target, or `0.874%`
- `259` total target UMIs
- `0.01094` mean raw UMIs per nucleus
- `0.6855` pseudobulk CPM

That is a near-absence signal for an aggregate glutamatergic class. The bundle's external evidence also points the same way: adult `Dlx5` expression is restricted to GABAergic interneuron classes rather than broadly to neurons, while the matched assay class is thalamic `Glut`. Sparse edited nuclei and a sub-1% target-expressing minority make a class-level FDR-significant program unlikely even if Dlx5 loss is realized in the few cells that contain it.

## Training measurements used

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 training perturbations. Its distribution is heavily concentrated at zero:

- 1,205 / 1,674 training targets had `n_degs = 0`
- median `n_degs = 0`
- 75th percentile `n_degs = 1`
- only 58 / 1,674 exceeded 50 DEGs

Curated mouse annotation/corpus analog nomination did not place `Dlx5` in a tight endpoint-matched module with strong responding `Dlx`-like perturbations. The one available paired-family target with a direct relationship, `Dlx6`, had `n_degs = 0`. The focal count table was also zero for nearby developmental or GABAergic/neural transcription-factor perturbations:

| training target | focal `n_degs` |
|---|---:|
| `Dlx6` | 0 |
| `Dlx3` | 0 |
| `Gata3` | 0 |
| `Pax6` | 0 |
| `Nkx2-1` | 0 |
| `Maf` | 0 |
| `Mafb` | 0 |
| `Neurod2` | 0 |
| `Satb2` | 0 |
| `Tbr1` | 0 |
| `Arx` | 0 |
| `Mef2c` | 1 |

Exact rows from the training Parquet confirmed that the closest `Dlx` neighbors were not near a broad response in this population: `Dlx6` and `Dlx3` each had 17,259 assayed rows in `151 TH Prkcd Grin2c Glut`, zero rows below BH 0.05, and minimum adjusted p-values of 1.0. Several generic chromatin/signaling candidates from broad fallback annotations did respond strongly in this class, for example `Sin3a = 1433`, `Ctnnb1 = 383`, and `Ctcf = 270`, but their effects falsify indiscriminate averaging over generic transcription/chromatin annotations rather than overriding the sparse-reach `Dlx5` prior.

## Synthesis

The strongest quantitative evidence is the exact target-expression reach: the requested population contains too little `Dlx5` RNA for many edited recovered nuclei to be Dlx5-dependent. Functional-stock depletion is biologically plausible by harvest, but only in cells with a DLX5 stock to deplete. The nearest available `Dlx` perturbation, the broader GABAergic/developmental transcription-factor comparators, and the zero-heavy focal training distribution all agree that the most likely count is at the floor.

Residual uncertainty is that `151 TH Prkcd Grin2c Glut` is an aggregate thalamic class and could contain a very small Dlx5-positive subpopulation. With under 1% observed non-target expression, that minority is unlikely to produce a BH-significant whole-class signature, so I predict no measured DEGs.
