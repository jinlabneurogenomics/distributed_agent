# Minpp1 DEG-count forecast

## Target and endpoint

- Manifest target: `Minpp1`.
- Cell population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the 151-class perturbation contrast.
- Declared count table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Declared expression table: `[local file: training_de_all_cell_groups.parquet]`.
- The released same-experiment corpus has no `Minpp1` target entry: `target_context(target="Minpp1")` returned 0 Findings, 0 Claims, and 0 explicit target references. I therefore used corpus records only to interpret observed training perturbations, not as target outcome evidence.

## Biology used for the held-out target

The declared biology bundle reports broad direct reach in the exact focal population: `Minpp1` is detected in 16,758 of 23,679 matched non-target 151-class cells, or 70.77%, with pseudobulk CPM 91.89.

`Minpp1` encodes an ER-lumen inositol-polyphosphate phosphatase. Targeted-null mouse fibroblasts lacked Minpp1 activity and accumulated InsP5/InsP6 by 30-45%, arguing that the biochemical function can be limiting in some mouse cells. The functional-stock adjudication calls pre-edit activity `likely_substantially_depleted` by P37-P44 because the operative stock is a renewable ER enzyme acting on soluble metabolites, with a 14.7 h mouse epithelial protein half-life as the closest turnover anchor.

Those points made a true functional perturbation plausible in assayed 151-class neurons, but they did not establish a large postnatal thalamic RNA state. The positive neural phenotype evidence is germline/developmental, centered on P21 cortex and E14.5 neural progenitors, while an earlier null line was viable without gross defects. The bundle also flags redundancy as unresolved: no close Minpp1 paralog was reported, but tissue-specific alternative phosphatase activity exists and was not tested in thalamic neurons.

## Training response scale

The exact 151-class training count table is extremely zero-inflated:

| count range | training targets |
| --- | ---: |
| `n_degs = 0` | 1205 |
| `n_degs = 1` | 276 |
| `n_degs = 2` | 31 |
| `n_degs <= 2` | 1512 |
| `n_degs = 3..5` | 34 |
| `n_degs = 6..9` | 22 |
| `n_degs = 10..49` | 47 |
| `n_degs = 50..99` | 16 |
| `n_degs >= 100` | 43 |

Across all 1,674 training perturbations the median is 0, the 90th percentile is 2, the 95th percentile is 18, and the mean is 14.05 because a small high-response tail is very large. In the parquet rows for the low-count part of the same table, 237 of 276 one-DEG perturbations were self-target-only singleton calls, so `n_degs = 1` is still a near-null downstream forecast rather than a multi-gene response.

## Biological comparators from the count table and parquet

Counts below are exact `pvals_adj < 0.05` values in `151 TH Prkcd Grin2c Glut`.

| training target | 151-class `n_degs` | interpretation for `Minpp1` |
| --- | ---: | --- |
| `Inpp5k` | 0 | Phosphoinositide/ER-contact phosphatase comparator; acute P16 loss was a 22-cell-class neuronal transcriptional null at FDR<0.10 in the same-experiment corpus. |
| `Ocrl` | 0 | Phosphoinositide/endocytic phosphatase comparator; flat in 151. |
| `Plcb1` | 0 | PI-to-IP3 signaling comparator; flat in 151. |
| `Itpr1` | 0 | ER IP3 receptor/calcium-release comparator; flat in 151. |
| `Synj1` | 1 | Phosphoinositide/endocytic comparator; the only 151 DEG was `Synj1` itself. |
| `Mtor` | 2 | Metabolic-growth pathway node; almost flat in 151. |
| `Hspa5` | 5 | Direct ER chaperone perturbation with only a small 151 ERQC response. |
| `Manf` | 3 | ER stress-adjacent comparator with a small 151 response. |
| `Sec63` | 11 | ER client-handling comparator, modest compared with the major ER-calcium state. |
| `Pitpna` | 21 | PI-transfer comparator that can respond, but does not represent a generic PI/PLC/PKC module. |
| `Atp2b1` | 22 | PMCA calcium-pump response that is selective for that paralog. |
| `Tsc2` | 86 | Strong mTOR-complex regulator, mechanistically too broad for direct transfer. |
| `Dhdds` | 116 | Dolichol/glycosylation-linked ERQC stress boundary. |
| `Atp2a2` | 187 | SERCA2 perturbation with a selective ER-stress ISR/UPR state; direct 151 DE included `Ddit3`, `Xbp1`, `Herpud1`, `Hspa5`, `Asns`, and `Cars`. |

The same-experiment corpus supports treating the high-response calcium/ER stress genes as boundary cases. It reports that Atp2a2/SERCA2 loss selectively activates an ER-stress ISR/UPR neuronal transcriptional state not reproduced by assayed PMCA, SPCA1, calcium-release-channel, or isolated ATF6 perturbations. It also reports that represented membrane-associated phosphoinositide and endocytic pathway perturbations, including `Inpp5k`, `Ocrl`, and `Synj1`, do not produce an interchangeable neuronal transcriptional module.

I compared the handpicked 12-node training cohort (`Atp2a2`, `Atp2b1`, `Dhdds`, `Hspa5`, `Inpp5k`, `Mtor`, `Ocrl`, `Pitpna`, `Plcb1`, `Sec63`, `Synj1`, `Tsc2`) in the declared 151-class parquet with `profile_compare`, then summarized it with `profile_cohort` in `evidence/selected_training_profile_cohort.json`. Significant-program overlap across the selected pairs was weak, with median overlap coefficient 0 for both the positive and negative significant programs. This reinforced that the high DEG burdens from `Atp2a2`, `Dhdds`, and `Tsc2` should not be averaged into a single reusable inositol-phosphate prior for `Minpp1`.

## Synthesis

`Minpp1` should be expressed and depleted enough for the edit to matter, so I did not assign a structural zero. However, the best-matched postnatal neuronal training perturbations near phosphoinositide/inositol handling were flat or singleton in 151-class neurons, and the large ER-stress examples came from calcium-store or glycosylation perturbations that the corpus explicitly bounded as selective. The most likely measured state is therefore no recurrent downstream module with, at most, a singleton BH-significant gene.

Point prediction: `1`.
