# Direct DEG-count forecast for Ergic1

## Requested endpoint

- Target: `Ergic1`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Point forecast: `0`

## Evidence used

### Target-side biology

The declared Ergic1 biology bundle identifies ERGIC1 as a cycling ER-Golgi intermediate compartment membrane protein that interacts with and stabilizes ERGIC3/hErv46. The exact in-assay focal population has broad Ergic1 RNA reach: `22288 / 23679` non-target nuclei express Ergic1, `94.1256%` expressing, with mean raw UMI `3.9690`, mean CP10K `2.4693`, and pseudobulk CPM `248.7541`.

That expression makes the target accessible in the assayed cells, but the functional-stock card left the 21-28 day post-edit realization unresolved. A disruptive edit should stop new ERGIC1 synthesis, while already installed ERGIC/ER/Golgi membrane protein may persist; no Ergic1 protein half-life, residence-to-degradation measurement, or perturbation-to-clearance clock was established. The source phenotype evidence was constitutive/systemic, not an acute postnatal thalamic-neuron loss phenotype, and related ERGIC2/ERGIC3 family evidence did not establish compensation or lack of compensation in the focal context.

### Training count table

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` count table contains 1,674 training perturbations. It is strongly zero-inflated in this focal class:

- `1205 / 1674` targets have `n_degs = 0`.
- The median is `0`.
- The mean is `14.05`, dominated by a small heavy tail.
- The 75th, 80th, 90th, 95th, and 99th percentiles are `1`, `1`, `2`, `18`, and `430`.

The deterministic gene-analog nomination run used the actual 1,674-gene training universe. Ergic1 itself was not in that universe. Among 765 available nominees, no candidate had exact-complex/paralog, reciprocal same-experiment comparator, narrow-module, or direct-interaction evidence for Ergic1; every nominee was a broad-functional-fallback candidate. The leading available ERGIC/early-secretory transport nominees therefore provided only broad process-level calibration, not exact molecular substitution.

The best ER/ERGIC-adjacent transport nominees and their observed focal counts were:

| candidate | relationship cue from nomination | `n_degs` |
|---|---:|---:|
| `Copa` | Golgi-to-ER retrograde and ER-to-Golgi vesicle transport | 0 |
| `Lman2l` | ER-to-Golgi vesicle transport; COPII-coated ER-to-Golgi vesicle | 0 |
| `Sec23a` | ER-to-Golgi vesicle transport; COPII-coated ER-to-Golgi vesicle | 0 |
| `Bcap31` | ER-to-Golgi vesicle transport; ERGIC membrane | 1 |
| `Copg1` | ER-to-Golgi vesicle transport; ERGIC | 1 |
| `Cog4` | Golgi-to-ER retrograde transport; Golgi membrane | 0 |
| `Stx5a` | ER-to-Golgi vesicle transport; ERGIC membrane | 0 |
| `Trip11` | ER-to-Golgi vesicle transport; ERGIC | 0 |
| `Sar1b` | ER-to-Golgi vesicle transport; ER membrane | 0 |
| `Tfg` | ER-to-Golgi vesicle transport | 0 |
| `Spast` | ER-to-Golgi vesicle transport; ER membrane | 0 |
| `Vcp` | ER-to-Golgi vesicle transport; ER membrane | 2 |
| `Hspa5` | ERGIC; ER membrane | 5 |

In the strictest early-secretory subset above, the median `n_degs` was `0` and the back-transformed mean of `log1p(n_degs)` was `0.17`; after also keeping the more general Vcp/Hspa5 stress/proteostasis comparators, the median remained `0` and the back-transformed `log1p` mean was `0.39`.

### Parquet check

I queried the declared `training_de_all_cell_groups.parquet` for the high-priority nominees in the exact focal `group_name`. Each available profile had 17,259 measured genes in this class. The Parquet-derived significant-gene counts matched the count table:

- `Copa`, `Lman2l`, `Sec23a`, `Cog4`, `Stx5a`, `Trip11`, `Sar1b`, `Spast`, `Tfg`, `Cog5`, `Trappc9`, and `Trappc6b`: `0` DEGs.
- `Bcap31`: `1` DEG, and it was the self transcript `Bcap31`.
- `Copg1`: `1` DEG, and it was the self transcript `Copg1`.
- `Vcp`: `2` DEGs, `Rasgef1b` and `Nsmf`.
- `Hspa5`: `5` DEGs, including ER-stress/protein-quality-control genes such as `Hsp90b1`, `Nfe2l1`, `Pdia4`, and `Derl3`.

Thus, the nearest ERGIC/early-secretory perturbations do not show a propagated thalamic transcriptional program. The only one-DEG calls in close COP/ERGIC-adjacent nodes were self-transcript effects, which are explicitly not reliable measures of functional knockout strength in this dataset.

### Same-experiment corpus topology

The release graph audit over the 13 leading early-secretory candidates found one connected explicit-Finding-reference component: 23 connected pairs among 78 possible pairs, with 5 reciprocal and 18 one-sided report-derived links. The largest fully connected subset was `Copa`, `Copg1`, `Stx5a`, and `Trip11`. This supported treating the candidates as a loose same-experiment ER/Golgi transport neighborhood, but the topology is a report-derived view of the same experiment rather than independent replication, and it supplied no exact Ergic1 endpoint analogue.

## Synthesis

Ergic1 is broadly expressed in the focal neurons, so lack of target presence is not the main reason to choose a small value. The downward evidence is instead quantitative and mechanistic:

- the 21-28 day effective depletion of a pre-installed cycling ERGIC membrane protein is unresolved;
- exact ERGIC2/ERGIC3-family or ERGIC1-complex training analogues were absent;
- the best available COP/ERGIC/ER-to-Golgi transport perturbations were almost all measured at `0` in this same cell class;
- the two one-DEG close analogues were self-transcript-only hits rather than propagated response programs; and
- the small Hspa5/Vcp signals reflect broader ER stress or protein-homeostasis lesions that are not justified as equal-scale proxies for Ergic1.

Those observations put the expected Ergic1 focal DEG burden below one measured gene. I therefore rounded the forecast to the nearest non-negative endpoint count:

`predicted_n_degs = 0`
