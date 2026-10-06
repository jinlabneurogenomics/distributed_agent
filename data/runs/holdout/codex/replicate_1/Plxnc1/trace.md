# Plxnc1 n_degs forecast

## Requested target

- Cell class: `151 TH Prkcd Grin2c Glut`.
- Target: `Plxnc1`, from the declared one-row holdout manifest and matching canonical biology bundle.
- Endpoint: number of measured genes in the held-out `Plxnc1` contrast with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

## Evidence used

### Target biology

The prediction-safe Plxnc1 biology bundle was used in `biology` view only; it explicitly did not expose labeled neighbors or the target outcome. It reports:

- Exact in-assay reach in the focal non-target population: `Plxnc1` was detected in `13,830 / 23,679` nuclei, `58.406%`, with mean `1.231` raw UMI and pseudobulk `77.162` CPM. This supersedes the qualitative adult-thalamus expression ambiguity and means a Plxnc1 edit is at least reachable in the assayed thalamic population.
- Plexin-C1 is a single-pass Sema7A receptor with neural roles in synapse formation, dendrite selection, and synapse elimination.
- The perturbation should stop production of new functional receptor but should not directly inactivate receptor molecules already on the membrane.
- The functional-stock adjudication calls operative stock by P37-P44 `likely_substantially_depleted`, with partial evidence: receptor turnover was inferred from a same-family neuronal proxy and sub-month Plxnc1 RNAi phenotype, but no Plxnc1-specific thalamic half-life or P16 thalamic depletion series was found.
- Functional observability is supported in other postnatal mouse neural contexts, especially neonatal olfactory bulb and postnatal cerebellar climbing fibers, while exact P16-P44 thalamic latency and Itgb1/Sema7A buffering remain unresolved.

### Training DEG counts

The 1,674-row training count table for `151 TH Prkcd Grin2c Glut` is highly sparse:

- median `n_degs = 0`
- 1,205 / 1,674 targets had `0`
- 1,546 / 1,674 had `<= 5`
- the mean, `14.05`, is driven by a short tail of very large nuclear programs rather than by a typical receptor-like response.

I focused on perturbations available in the training table that are biologically close to Plxnc1 by family, Sema/co-receptor relationships, or neighboring developmental guidance receptor biology:

| target | 151 TH `n_degs` |
| --- | ---: |
| `Itgb1` | 0 |
| `Nrp1` | 0 |
| `Nrp2` | 0 |
| `Plxna1` | 0 |
| `Plxna2` | 1 |
| `Plxna4` | 0 |
| `Plxnd1` | 0 |
| `Dcc` | 0 |
| `Ryk` | 0 |
| `Robo1` | 1 |
| `Robo2` | 0 |
| `Slit2` | 0 |
| `Sema4d` | 0 |
| `Sema5a` | 1 |
| `Unc5c` | 1 |
| `Unc5d` | 0 |
| `Epha4` | 1 |
| `Ntrk2` | 3 |

Those 18 analogs sum to 8 FDR-significant genes; their arithmetic mean is `0.444`, their `log1p` mean back-transforms to `0.309`, and their median is `0`. The exact Parquet rows for the same 18 genes in `151 TH Prkcd Grin2c Glut` gave no missing profiles, 12 targets with no significant gene, and the remaining 6 in the 1-9 significant-feature bin, confirming that the tabulated low counts match the held-in expression signatures.

### Packaged same-experiment context

I queried the same-experiment Finding inventory only for held-in analogs, not for `Plxnc1`. The released interpretations supported the same local calibration:

- `Itgb1` was called a pan-measured FDR-null transcriptional perturbation, and other represented integrins mostly phenocopied that null.
- `Nrp1`, `Dcc`, and `Plxnd1` were described as complete or broad postnatal neuronal nulls.
- `Plxna1`, `Plxna2`, and `Plxna4` had only isolated one-gene or two-gene effects outside most cell groups, with represented plexin/neuropilin/semaphorin relatives failing to converge.
- `Robo1` did not yield a broad Slit/Robo/actin transcriptional program.

## Synthesis

Plxnc1 is measurably expressed and the 21-28 day window is probably long enough to deplete a renewable Plexin-C1 receptor pool, so I did not treat the target as unreachable. The expected endpoint, however, is not receptor engagement; it is an FDR<0.05 nuclear RNA program in recovered thalamic neurons. The biology card places the known Plxnc1 loss phenotypes in olfactory and cerebellar developmental circuits rather than in this thalamic population, and the closest held-in Sema/plexin/co-receptor perturbations are almost all transcriptionally silent in this same cell class.

The count table therefore provides a tighter scale prior than the broad observation that the target is expressed: the selected receptor/guidance cohort has median `0` and log-scale center near `0.3` DEGs, with no profile-level evidence for a shared stronger subthreshold program. I predict that Plxnc1 will land on the same local null surface.

Predicted `n_degs`: `0`.
