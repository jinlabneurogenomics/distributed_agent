# Gria4 151 TH Prkcd Grin2c Glut forecast

## Target and endpoint

- Target: `Gria4`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Point forecast: `0`

## Evidence used

### Declared Gria4 biology bundle

- The canonical `Gria4` bundle exposed target biology and exact in-assay expression reach, with `target_outcome_exposed=false`.
- `Gria4` is directly reachable in the focal population: non-target `151 TH Prkcd Grin2c Glut` nuclei expressed `Gria4` in 23,472/23,679 cells, or 99.13%, with mean raw UMI 8.60 and mean log1p CP10K 1.786.
- The perturbation should be functionally realized by harvest when editing succeeds. The bundle adjudicates GluA4 as a dynamic AMPA-receptor pore-forming subunit whose pre-edit stock is `likely_substantially_depleted` by the P37-P44 harvest; its direct turnover evidence is a 23 +/- 8 h GluR4 half-life in cultured neurons, far shorter than the 21-28 d post-P16 interval.
- The strongest loss phenotype in the card is germline thalamocortical physiology, especially reticular-thalamic excitation. That supports a thalamic functional role but leaves the acute P16-to-P37/44 survivor-conditioned single-nucleus RNA effect in glutamatergic 151 TH neurons unresolved.

### Training endpoint table

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table has 1,674 training perturbations and is heavily zero-inflated for this exact endpoint:

- median `n_degs = 0`
- 1,205/1,674 training perturbations had `n_degs = 0`
- 1,481/1,674 had `n_degs <= 1`
- 1,512/1,674 had `n_degs <= 2`
- only 43/1,674 reached `n_degs >= 100`

Endpoint-matched counts for the most direct measured AMPA/core training analogs in 151 TH were at the floor:

| training target | 151 TH `n_degs` |
|---|---:|
| `Gria1` | 0 |
| `Gria2` | 0 |
| `Gria3` | 0 |
| `Cacng2` | 0 |
| `Cacng3` | 0 |
| `Dlg4` | 1 |

Nearby glutamate-receptor family members were also mostly flat or singleton-scale, while the assay could detect a thalamic response for the NMDA core subunit `Grin1`:

| training target | 151 TH `n_degs` |
|---|---:|
| `Grin1` | 89 |
| `Grin2a` | 1 |
| `Grin2b` | 2 |
| `Grin2d` | 0 |
| `Grin3a` | 0 |
| `Grid1` | 1 |
| `Grid2` | 0 |
| `Grik1` | 0 |
| `Grik3` | 0 |
| `Grik4` | 0 |
| `Grik5` | 1 |
| `Grm1` | 1 |
| `Grm5` | 0 |
| `Grm7` | 1 |
| `Grm8` | 0 |

### 151 TH expression-Parquet profile check

I compared the exact `151 TH Prkcd Grin2c Glut` rows in the declared training Parquet for 18 glutamate-receptor-family perturbations. The profile comparison used `scores` over measured genes with `pvals_adj < 0.05` marking significant features.

The focal AMPA paralogs had complete 151 TH profiles over 17,259 features and no significant features:

| node | significant features | positive | negative |
|---|---:|---:|---:|
| `Gria1` | 0 | 0 | 0 |
| `Gria2` | 0 | 0 | 0 |
| `Gria3` | 0 | 0 | 0 |

`Grin1` was the lone large responder in this 18-node receptor cohort, with 89 significant genes split 40 positive and 49 negative. It did not share any significant 151 TH features with the AMPA paralogs, which had none; whole-profile cosines between `Grin1` and `Gria1`, `Gria2`, and `Gria3` were -0.054, 0.015, and 0.072. This makes the NMDA-core response a detectability boundary, not a scale donor for `Gria4`.

### Same-experiment corpus interpretation

The selected corpus Findings are a semantic layer over the same Perturb-seq measurements, not independent replication. I used them to interpret why the endpoint-matched analogs were biologically relevant:

- `Gria2:F004` records that sampled AMPAR-core and AMPAR TARP/scaffold comparators were rejected as strong `Gria2` phenocopies because `Gria1`, `Gria3`, `Cacng2`, `Cacng3`, and `Dlg4` were all nearly downstream-null.
- `Gria3:F003` anchors the broader contrast that AMPAR-core and AMPAR-trafficking relatives were buffered like `Gria3`, whereas NMDA subunits such as `Grin1`, `Grin2a`, and `Grin2b` produced detectable DE in the same universe.

## Synthesis

`Gria4` has excellent transcript reach in 151 TH and its GluA4 protein stock is plausibly renewed within the experiment, so I did not treat the perturbation as unreachable. The decisive quantitative evidence was instead the endpoint behavior of its closest training analogs: all three measured AMPA pore-forming paralogs have `n_degs = 0` in the exact focal class, auxiliary AMPAR components are also 0-1, and the profile Parquet shows no hidden 151 TH significant module across `Gria1`, `Gria2`, or `Gria3`.

The high `Grin1` count proves that acute perturbation of a glutamate receptor can yield a 151 TH nuclear RNA program when the local biology couples to transcription, but its profile is an NMDA-specific boundary rather than an AMPA-family scale estimate. Because the best AMPA-core evidence sits at zero and the Gria4 biology does not supply a matched acute RNA phenotype that would override those measurements, the most likely integer count is the same 151 TH floor as `Gria1`/`Gria2`/`Gria3`: `0`.
