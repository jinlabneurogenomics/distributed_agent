# Rab28 n_degs forecast

Target and endpoint:

- Manifest target: `Rab28`.
- Cell group: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the number of measured genes in this focal group with BH-adjusted Wilcoxon `p < 0.05`.

Prediction-safe Rab28 biology:

- The declared biology bundle is `biology_bundles/Rab28.json`, checksum `c3ff69c95aae39634e9dab3754cc9eca9f251774c760a4d700192ffcd6347371`, with `endpoint_values_used=false`.
- Rab28 is present in the assayed focal population: `20,462 / 23,679` non-target nuclei express it, `pct_cells_expressing = 86.4141`, `mean_log1p_cp10k = 0.8061`, and `mean_raw_umi = 2.3088`.
- The functional-stock card predicts that P16 disruptive editing should likely substantially deplete the dynamic Rab28 protein pool by the P37-P44 harvest, because new farnesylated Rab28 production stops and the best available mature-neuronal proteome proxy favors turnover on a days scale.
- The endpoint-coupling evidence is weak for thalamic nuclear RNA. The direct mammalian phenotype is in postnatal retina and cone outer-segment shedding; the related C. elegans evidence connects RAB-28 to IFT/BBSome ciliary trafficking; adult mouse thalamic cellular demand remains unresolved.

Training measurements used:

- The declared training count table contains 1,674 targets for this cell class. Its empirical distribution is highly zero-inflated: 1,205 targets have `n_degs = 0`; 1,481 have `n_degs <= 1`; the median is 0; the 75th percentile is 1.
- The close represented ciliary/BBSome/IFT training perturbations were flat or singleton in the count table:

| target | `n_degs` |
| --- | ---: |
| `Bbs5` | 0 |
| `Cep290` | 0 |
| `Dync2h1` | 0 |
| `Dync2i1` | 0 |
| `Ift43` | 0 |
| `Ift81` | 0 |
| `Ift88` | 0 |
| `Kif3b` | 0 |
| `Lztfl1` | 0 |
| `Rpgrip1l` | 0 |
| `Ttc21b` | 0 |
| `Ttc8` | 1 |

- The `dataset.candidate_profile_review` comparison over the declared Parquet and exact `151 TH Prkcd Grin2c Glut` context found the same pattern. Among `Bbs5`, `Cep290`, `Dync2h1`, `Dync2i1`, `Ift43`, `Ift81`, `Ift88`, `Lztfl1`, `Ttc8`, and `Ttc21b`, 45/45 pairwise profile comparisons were available, no pair had any significant-program overlap, the positive top-tail overlap coefficient had median `0.04`, and the negative top-tail overlap coefficient had median `0.05`.
- The same profile comparison kept `Arl3` and `Rab7` as small-GTPase boundaries. `Arl3` had only one significant gene in this class. `Rab7` had 501, but I treated it as an endolysosomal high-response boundary rather than a Rab28 analogue because its large survivor signature is not the ciliary Rab28/BBSome/IFT operation.

Same-experiment corpus context:

- Training-target corpus findings, which are another view of the same experiment rather than independent replication, support the count-table interpretation.
- `Ift88:F003` contributed to claim `claim:78305cab7c1c7b98458d`: represented ciliary transport, BBSome, transition-zone, ciliary-GPCR, and Hedgehog-adjacent perturbations were largely buffered at the basal postnatal NeuN+ nuclear-RNA level.
- `Cep290:F003` made the same point in a transition-zone context: expected ciliary GPCR, BBSome/IFT, and Hedgehog-effector transcription was absent or nearly absent after perturbing `Cep290` and represented pathway components.
- `Ttc8:F003` reported no robust shared transcriptional module across `Bbs5`, `Ift43`, `Ift81`, `Ift88`, `Kif3b`, `Dync2h1`, `Lztfl1`, `Rpgrip1l`, `Ttc21b`, and `Cep290`.
- `Bbs5:F003` reported that represented BBSome/ciliary relatives did not phenocopy `Bbs5`; `Ttc8`, `Lztfl1`, and `Ift88` lacked robust downstream modules in matched neuronal contexts.

Synthesis:

Rab28 is expressed and its edited protein pool should not be dismissed as unreached. The limiting issue is endpoint projection: the card places Rab28 in a specialized ciliary/photoreceptor trafficking axis, and the available postnatal neuronal training analogues for ciliary trafficking are almost all FDR-null in this focal thalamic group. The exact closest mechanistic partners `Ift27` and `Pde6d` are absent from the training table, so I left room for a singleton, but the mode, median, and log-space center of the represented ciliary cohort all round to zero. I therefore forecast a near-null BH-significant footprint:

`predicted_n_degs = 0`.
