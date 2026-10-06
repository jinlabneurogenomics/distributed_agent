# Gbf1 forecast for `151 TH Prkcd Grin2c Glut`

## Target and endpoint

- Target: `Gbf1`, from the declared one-row holdout manifest `Gbf1.csv` and the canonical biology bundle `biology_bundles/Gbf1.json`.
- Endpoint: `n_degs`, the number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `p < 0.05`.
- Declared measured training surfaces used:
  - `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  - `[local file: training_de_all_cell_groups.parquet]`
- The count table and Parquet are two representations of the same PerturbAI experiment; they were used as direct training measurements, not as independent replication.

## Target biology

The biology-only `Gbf1` bundle supports reach and molecular realization but not a quantified large transcriptional response. `Gbf1` was detected in `20134 / 23679` non-target nuclei in the focal class, or `85.03%`, with mean `1.4225` CP10K and `2.2745` raw UMI. GBF1 is a cycling ARF guanine-nucleotide exchange factor at the cis-Golgi/ERGIC that supports ARF-dependent COPI recruitment and early secretory traffic. The functional-stock card adjudicated pre-edit GBF1 as likely substantially depleted by the 21 to 28 day harvest window because the available protein half-life evidence is on an hours scale, although the turnover evidence is not from edited postnatal thalamic neurons.

That makes `Gbf1` a biologically reachable secretory-traffic perturbation, not an absent-target case. The residual uncertainties cut the other way: the bundle did not identify a direct P16 thalamic-neuron loss experiment, BIG1/BIG2 compensation was untested, and the snRNA endpoint is survivor-conditioned rather than a Golgi morphology, traffic-flux, or cell-loss readout.

## Training measurements

The focal-class training count table is zero-inflated:

- `1674` training perturbations
- `1205` with `n_degs = 0`
- median `0`
- 75th percentile `1`
- 90th percentile `2`
- 95th percentile `18`

I therefore treated a low count as the base rate unless a close mechanistic neighborhood had a recurrent high-burden module.

The closest represented perturbations to GBF1's ER-Golgi/COPI branch were flat or nearly flat in the declared count table:

| training target | link to GBF1 decision | `n_degs` in `151` |
|---|---:|---:|
| `Copa` | core COPI coat subunit downstream of ARF activation | 0 |
| `Copg1` | core COPI coat subunit downstream of ARF activation | 1 |
| `Sec23a` | COPII/ER-exit branch of early secretory traffic | 0 |
| `Sar1b` | COPII initiation GTPase | 0 |
| `Stx5a` | ER-Golgi / intra-Golgi SNARE | 0 |
| `Cog4` | Golgi tethering / retrograde traffic | 0 |
| `Cog5` | Golgi tethering / retrograde traffic | 0 |
| `Stx16` | endosome-to-TGN SNARE comparator | 1 |

A run-local profile comparison on `training_de_all_cell_groups.parquet`, filtered exactly to `group_name = "151 TH Prkcd Grin2c Glut"`, gave the same picture at the expression-profile level. The inspected proximal nodes had `0` significant features for `Copa`, `Cog5`, `Sec23a`, and `Stx5a`, and `1` for `Copg1`, across `17,259` profiled genes. These flat profiles also had no same-direction FDR-significant overlap with stress-positive but less direct organelle comparators such as `Gfpt1`, `Rab7`, `Vps35`, and `Vps54`.

The high-count positive controls were useful mainly as boundaries:

- `Gfpt1` had `311` focal DEGs and marks a strong hexosamine/glycosylation-to-UPR/ISR state.
- `Rab7` had `501` focal DEGs and marks a broad endolysosomal/autophagy/ISR state.
- `Vps35` and `Vps54` had `17` and `31` focal DEGs, respectively.

Those responses show the thalamic population can mount an organelle-stress signature in this assay, but the response is branch-specific rather than shared across ER-Golgi traffic genes.

## Packaged same-experiment interpretation

`Gbf1` itself had no same-experiment Findings or Claims in the selected corpus release, so I used packaged context only for measured training comparators.

The most relevant Claim-level boundary was `claim:6a94b158a9de9a66a6c3`: represented ER-Golgi trafficking and Golgi glycosylation/homeostasis perturbations did not form a shared broad secretory-pathway module in postmitotic neurons. Its supporting Findings included `Copa:F004`, `Copg1:F003`, `Stx5a:F003`, `Cog4:F002`, and a `Trip11:F003` cross-comparison that explicitly grouped `Sec23a`, `Sar1b`, `Copa`, `Copg1`, `Stx5a`, `Cog4`, and `Cog5` as absent or nearly absent responders.

A second Claim, `claim:6ad7068adcc1a43c2bbe`, separated represented COPII/ER-exit nodes from ER stress: `Tfg`, `Sec23a`, and `Sar1b` were transcriptionally buffered, whereas `Sec63` elicited an ER-stress response. This argued against transferring the larger `Sec63`, `Gfpt1`, or `Rab7` burdens to every proximal trafficking perturbation.

## Synthesis

The target-side biology makes an edited `Gbf1` allele likely to matter molecularly by harvest, but the most endpoint-matched training evidence says that postnatal NeuN-positive neurons often do not convert single-node early-secretory disruption into a thresholded nuclear RNA program. Core COPI, COPII-initiation, COG, and ER-Golgi SNARE perturbations all landed at `0` or `1` DEG in the exact focal class, and the packaged reports interpret that as a real buffered ER-Golgi/secretory region of the screen rather than as a single failed target.

I therefore forecast a strict null or a one-gene edge case, with the point estimate rounded to the modal proximal outcome:

`predicted_n_degs = 0`
