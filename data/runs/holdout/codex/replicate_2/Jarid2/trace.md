## Target

- Target: `Jarid2`
- Requested population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the count of measured genes with Wilcoxon BH-adjusted `p < 0.05`

## Evidence Used

### Target biology bundle

The canonical `Jarid2` biology bundle characterizes JARID2 as a non-core PRC2 accessory factor whose perturbation stops new JARID2 supply but does not instantly remove pre-existing JARID2 protein, PRC2 occupancy, or already-installed H3K27me3/locus states.

Material fields from the bundle:

- `operative_entity`: multiple functional pools spanning JARID2 protein in PRC2.2/chromatin complexes and downstream locus-specific chromatin states.
- `functional_stock_by_harvest`: `partially_depleted_or_leading_edge`, because 21-28 days should renew much of the protein/occupancy pool but not guarantee erasure of all chromatin memory.
- `renewal_demand`: `context_dependent`, with direct loss evidence mainly from embryonic/progenitor settings rather than postmitotic thalamic neurons.
- `redundancy`: `unknown`; MTF2/PRC2.1 is an alternative PRC2 recruitment axis in embryonic stem cells, but no matched thalamic-neuron compensation test is available.
- Exact in-assay reach for `Jarid2` in `151 TH Prkcd Grin2c Glut`: expression was measurable in 19,761 of 23,679 non-target cells, `83.45%` expressing, with mean raw UMI `2.118` and mean CP10k `1.337`.

Interpretation: `Jarid2` is present in the focal neurons, so the perturbation is not out of reach. The biology nevertheless points to a slow, buffered chromatin operation rather than acute collapse of an essential transcription or RNA-processing module.

### Training count table

The declared 151 TH training table contains 1,674 non-held-out perturbations. Its FDR `p_adj < 0.05` DEG counts are sparse and highly skewed:

- median: `0`
- 75th percentile: `1`
- 90th percentile: `2`
- 95th percentile: `18`
- 59 of 1,674 perturbations have at least 50 DE genes
- 15 of 1,674 perturbations have at least 500 DE genes

This makes a zero-to-single-digit response the default scale unless the target maps onto one of the large generic perturbation classes.

### Closest measured comparators

The count table did not contain the most direct PRC2 core or PRC2.2 comparators that would have bracketed JARID2 directly: `Eed`, `Ezh1`, `Ezh2`, `Suz12`, `Aebp2`, `Mtf2`, `Phf1`, `Phf19`, `Rbbp4`, and `Rbbp7` were absent from the training target list.

The closest represented H3K27/Polycomb-side perturbations were instead quiet:

| comparator | focal n_degs | bearing |
| --- | ---: | --- |
| `Kdm6b` | 0 | H3K27 demethylase; same-experiment Findings describe it as FDR-null in recovered neurons and selectively flat relative to other chromatin regulators that do respond in this thalamic group |
| `Mga` | 2 | PRC1.6/MAX-network repressor; same-experiment Findings describe only a tiny up-only 151 TH / 155 MB glutamatergic derepression response |

Broader chromatin regulators gave a split picture rather than a uniformly strong class:

| comparator | focal n_degs |
| --- | ---: |
| `Ep300` | 0 |
| `Kdm5b` | 0 |
| `Kat6a` | 0 |
| `Chd7` | 0 |
| `Arid1b` | 1 |
| `Crebbp` | 8 |
| `Kdm5c` | 18 |
| `Arid1a` | 22 |
| `Chd4` | 100 |
| `Setd1a` | 368 |
| `Sin3a` | 1433 |

The packaged same-experiment corpus also marks useful boundaries: `Ep300` was robustly null across measured neuronal groups, `Crebbp` produced only a small 151 TH-restricted response at the looser corpus FDR threshold, and `Kdm6b` was flat despite `Setd1a`, `Smarcc2`, `Kmt2a`, `Setdb1`, `Kdm5c`, `Crebbp`, and `Setd5` being detectable in the same thalamic context. Those records are interpretations of the same Perturb-seq experiment rather than independent replication.

### Profile check

I compared a 21-node chromatin cohort in the declared Parquet restricted to `group_name == "151 TH Prkcd Grin2c Glut"`. The small-count nodes stayed individually quiet in the exact profile table:

| node | significant features at `p_adj < 0.05` |
| --- | ---: |
| `Kdm6b` | 0 |
| `Mga` | 2 |
| `Ep300` | 0 |
| `Crebbp` | 8 |
| `Chd4` | 100 |

Whole-profile correlations among these quiet targets mostly involved nonsignificant rank structure, so I treated them only as a check that the chosen low-count examples were not hiding a shared strong FDR-supported module.

## Synthesis

`Jarid2` has high enough focal expression for an effect to be observed, and JARID2-specific PRC2.2 recruitment should be at least partly renewed by 21-28 days. That argues against an unreachable target and against an automatic hard zero.

The downward evidence is stronger for the FDR count scale. JARID2 is an accessory/recruitment factor, not the catalytic PRC2 subunit; pre-existing H3K27me3 and locus states can persist; PRC2.1/MTF2 can supply an alternative recruitment route; and the best available measured H3K27/Polycomb-side comparators in the same thalamic endpoint were `Kdm6b = 0` and `Mga = 2`. More general chromatin machinery can produce huge DEG burdens in this population, but those high-count examples are less operation-matched than the buffered repressive-chromatin comparators.

I therefore placed `Jarid2` in the same low, sparse band as `Kdm6b`/`Mga`/`Crebbp`, with a tiny derepression response rather than a broad chromatin-regulator response.

Predicted `n_degs`: `2`
