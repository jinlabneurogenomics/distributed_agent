# Notch3 direct n_degs forecast

Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, defined as the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.

## Target and assay reach

- The holdout manifest contains one target, `Notch3`.
- The canonical Notch3 biology bundle indicates that a P16 disruptive edit should substantially deplete Notch3 functional stock by the P37-P44 harvest in cells that actually express Notch3: ligand-responsive surface receptor is continually supplied, the active intracellular effector is degradable, and the 21-28 day post-edit interval is several-fold longer than the broad mouse-brain proteome turnover scale. This supports target engagement as biologically plausible rather than excluding the perturbation on persistence grounds.
- The same bundle gives the decisive context limitation: Notch3 is essentially absent from the assayed NeuN-positive thalamic neuronal population. In the exact focal non-target nuclei, Notch3 had `61 / 23679` expressing cells, `pct_cells_expressing = 0.2576122302462097`, `mean_raw_umi = 0.003040668947168377`, and `pseudobulk_cpm = 0.19056950550656807`.
- The source-card evidence also places mouse neural-tissue Notch3 expression and loss phenotypes in vascular mural cells, not thalamic postmitotic neurons. Therefore the expected realized lesion in the assayed nuclei is heavily diluted or absent even though Notch3 is consequential in vascular compartments outside this FACS-enriched neuronal assay.

## Training perturbations used

The focal-class training count table contains 1,674 non-held-out targets and is sparse: 1,205 have `n_degs = 0`, the median is `0`, and 1,481 have at most one DEG.

I treated visible Notch-family and core Notch-node perturbations as the most relevant direct training comparators because they test whether acute CRISPR loss of related receptor/protease/ligand-side Notch machinery can produce a postnatal thalamic neuronal signature in this assay.

| training target | `n_degs` in `151 TH Prkcd Grin2c Glut` | use in forecast |
|---|---:|---|
| `Notch1` | 0 | Notch receptor-family boundary |
| `Notch2` | 0 | closest documented Notch3 paralog in the bundle |
| `Notch4` | 0 | Notch receptor-family boundary |
| `Adam10` | 0 | canonical receptor-cleavage node |
| `Dll1` | 0 | canonical ligand-side node |
| `Psen1` | 0 | gamma-secretase node |
| `Hesx1` | 0 | Notch-adjacent transcription-factor boundary |
| `Mib1` | 27 | weak positive Notch-adjacent exception |

I then checked the declared Parquet for these same targets in the exact focal class. `Notch1`, `Notch2`, `Notch4`, `Adam10`, `Dll1`, `Psen1`, and `Hesx1` each had 17,259 measured-gene rows and no gene even at `pvals_adj < 0.10`; the minimum adjusted p-values for `Notch1`, `Notch2`, `Adam10`, `Psen1`, and `Hesx1` were all `1.0`, and were `0.4901981894` for `Notch4` and `0.6775600159` for `Dll1`. The `Mib1` Parquet rows reproduced the small nonzero count, with 27 genes at FDR<0.05.

Same-experiment corpus context made the `Mib1` exception non-projectable to `Notch3`: the Mib1 report calls the response an SREBF2-like sterol/cholesterol module and explicitly states that it is uncoupled from canonical Notch transcription, does not reproduce the Dll1/Notch/ADAM10/presenilin perturbations, and lacks HES/HEY/Nrarp/Dtx1 induction or repression.

## Forecast

The quantitative and biological evidence both point below the detection boundary. Notch3 has far less exact neuronal reach than would be needed for a robust aggregated thalamic RNA response; measured loss of the other Notch receptors and several core Notch nodes is flat in the same cell class; and the one weak Notch-adjacent positive case is a Mib1-specific sterol state rather than a receptor-family Notch program.

I therefore forecast the modal zero outcome:

`predicted_n_degs = 0`
