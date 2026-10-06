# Stim1 direct n_degs forecast

## Target and endpoint

- Target: `Stim1`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the declared focal cell group.
- Point forecast: **0**

## Evidence used

### Declared target biology

The canonical `Stim1` biology bundle describes STIM1 as an ER-membrane Ca2+ sensor/channel-coupling protein that dynamically clusters with ORAI1 after store depletion and supports store-operated Ca2+ entry. The P16 edit should stop new STIM1 production, and a 21-28 day post-edit interval is long enough that a substantial fraction of this dynamic protein stock should turn over by harvest, but the evidence is partial because no STIM1 half-life was resolved for juvenile thalamic neurons.

The bundle's exact baseline measurement shows that `Stim1` is present in the focal population but not pan-cellular or abundant:

- `mean_raw_umi = 0.6518`
- `mean_cp10k = 0.4016`
- `pct_cells_expressing = 44.09`
- `10,441 / 23,679` non-target nuclei expressed the feature

The same biology bundle also flags partial same-context redundancy from `Stim2`: single `Stim1` loss in adult forebrain was much milder than combined `Stim1`/`Stim2` loss, so STIM-family overlap is a reason to attenuate the expected steady-state RNA response in thalamic neurons.

### Declared training count scale

The focal training table contains 1,674 observed perturbations. It is heavily zero-inflated for this exact endpoint:

- 1,205 / 1,674 training targets have `n_degs = 0`
- median = 0
- 75th percentile = 1
- 90th percentile = 2
- 95th percentile = 18

The relevant training perturbations around calcium signaling and neuronal Ca2+-dependent transcription were mostly flat in this same focal table:

| training target | focal `n_degs` |
|---|---:|
| `Itpr1` | 0 |
| `Ryr2` | 0 |
| `Ryr3` | 0 |
| `Cacna1a` | 0 |
| `Cacna1d` | 0 |
| `Cacna1e` | 0 |
| `Camk2a` | 0 |
| `Nfatc3` | 0 |
| `Camk2b` | 1 |
| `Calm3` | 1 |
| `Ppp3ca` | 4 |
| `Ppp3r1` | 9 |
| `Cacna1g` | 12 |
| `Calm1` | 14 |

The ER-quality-control comparators were much larger:

| training target | focal `n_degs` |
|---|---:|
| `Hspa5` | 5 |
| `Opa1` | 37 |
| `Dhdds` | 116 |
| `Atp2a2` | 187 |

I treated `Atp2a2`/SERCA2 as a positive bound for ER Ca2+ store depletion rather than as a direct quantitative analogue for `Stim1`: the profile query on the declared Parquet showed `Atp2a2` induced canonical UPR/ISR genes in this focal class (`Ddit3`, `Chac1`, `Xbp1`, `Herpud1`, `Hspa5`, `Asns`, amino-acid/one-carbon genes), while `Cacna1g`, `Ppp3ca`, and calcineurin/CaM/CaMK targets had small, specific, non-UPR signatures or only self-transcript hits.

### Same-experiment report layer

The packaged report layer, which is a curated same-experiment interpretation rather than independent replication, supported the same separation:

- `Atp2a2` was described as the training-table calcium/ER perturbation that generated a strong thalamic ER-stress ISR/UPR state.
- The `Atp2a2` report explicitly contrasted that state with represented ER release channels and isolated UPR arms: `Itpr1`, `Ryr3`, and `Atf6` did not reproduce the `Atp2a2` program.
- `Itpr1` was annotated as downstream-null across all recovered neuronal groups and as non-phenocopying `Atp2a2` in `151 TH Prkcd Grin2c Glut`.
- `Cacna1g` was the clearest represented voltage-gated channel response in the focal group, but it was only a 12-gene `pvals_adj < 0.05` footprint in the declared count table and lacked the broad UPR/ISR or immediate-early program expected from a generic Ca2+ stress response.

## Synthesis

`Stim1` loss is expected to be functionally realized enough that the endpoint is not dismissed as an unedited target. The quantitative question is whether loss of the STIM1 store-operated entry arm should look like a broad ER store-refilling failure, a small activity/calcium-plasticity perturbation, or no sustained nuclear RNA state in recovered juvenile thalamic neurons.

I weighted the `Itpr1`/`Ryr2`/`Ryr3`/`Atf6`/CaMK/calcineurin family more strongly than `Atp2a2` because STIM1 is a sensor for store-operated influx after depletion, not the pump that loads ER calcium at baseline. Removing SERCA2 directly depletes ER stores and triggers a robust UPR/ISR state; removing STIM1 should instead blunt one replenishment route, and `Stim2` can buffer part of the STIM operation. The exact expression reach, about 44% of focal non-target cells with low mean UMI, further argues against a broad class-wide response.

The focal class can reveal small calcium-linked responses, as `Cacna1g`, `Calm1`, `Ppp3r1`, and `Ppp3ca` show, but most similarly positioned store-release and downstream Ca2+-plasticity genes landed at 0 or 1. Given that prior and the mechanistic offset from direct ER depletion, the most likely integer is the zero bin, with one or a few self/local hits as the main uncertainty.

I therefore forecast:

```tsv
target_name	predicted_n_degs
Stim1	0
```
