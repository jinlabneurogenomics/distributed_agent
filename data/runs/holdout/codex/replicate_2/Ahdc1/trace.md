# Ahdc1 forecast for `151 TH Prkcd Grin2c Glut`

## Declared target and endpoint

- Target manifest: `Ahdc1`.
- Endpoint: `n_degs`, the number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- The focal training table `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]` contained 1,674 training perturbations and no `Ahdc1` row.
- The matched Parquet operations below used only training perturbations; no `Ahdc1` differential-expression profile or outcome was queried.

## Biology of Ahdc1

Evidence came from the declared biology bundle
`[local file: Ahdc1.json]`
and the equivalent `distributed_agents_runtime.characterization_bundle(target="Ahdc1", view="biology")` record.

- Exact same-assay expression reach is high but not complete: in matched non-target nuclei from `151 TH Prkcd Grin2c Glut`, `Ahdc1` was detected in 15,863/23,679 nuclei, or 66.99%, with mean log1p CP10k 0.499. This makes the target transcript present in the assayed focal population but does not by itself measure editing efficiency or response size.
- The functional operation is chromatin-associated regulation: AHDC1/Gibbin binds enhancer/promoter chromatin and regulatory partners and maintains gene-specific enhancer-promoter contacts in stem-cell differentiation and epithelial/mesodermal systems.
- The functional-stock adjudication called the P16-to-P37/44 lesion `partially_depleted_or_leading_edge`, because a disruptive edit should stop new full-length AHDC1 supply, but existing nuclear protein and previously installed chromatin states could persist and Ahdc1-specific neuronal half-life/residence measurements were absent.
- Biological consequence is real but temporally mismatched: mouse Ahdc1 loss evidence is mainly embryonic morphogenesis or post-weaning systemic physiology, and human AHDC1 truncations cause a neurodevelopmental syndrome. None of those directly times an acute loss response in postmitotic juvenile thalamic neurons.
- Redundancy evidence was weakly favorable: the card found no close mouse `Ahdc1` paralog after a bounded search, reducing the chance of simple one-paralog buffering while leaving generic chromatin-network compensation unresolved.

## Training-count scale

The requested focal count table was extremely zero-inflated.

- 1,205/1,674 training perturbations had `n_degs = 0`.
- 469/1,674 were positive.
- The median was 0, the 75th percentile was 1, and the 90th percentile was 2.
- The mean was 14.05 because a small number of targets had hundreds to thousands of DE genes.

This makes a prediction in the 0-2 range the natural baseline for a perturbation without a tight high-response analog.

## Ahdc1 analogs

I used `gene-analog-nomination-skill` against the actual 1,674-gene training universe and wrote the typed nomination record to
`workbench/ahdc1_analog_nominations.jsonl`.

- `Ahdc1` was not represented in the training universe or in the selected same-experiment corpus ledger.
- The nominator returned no exact complex/paralog, bidirectional corpus comparator, narrow-module, direct-interaction, or dependency candidates.
- All 899 nominated available genes were `broad_functional_fallback`, so their retrieval priority is useful for bounding inspection but not a mechanistic weight.
- The highest-specificity functional community was `GO:0140585` promoter-enhancer loop anchoring activity. The training-available direct members were:
  - `Zic1`: `n_degs = 2`
  - `Zic2`: `n_degs = 0`
  - `Msl2`: `n_degs = 0`
- The first 8 broad Ahdc1 nominees had counts `[2, 0, 0, 0, 0, 2, 0, 1]`: median 0, mean 0.625, max 2.
- The first 20 nominees had mean 0.45 and max 2; the first 50 had mean 0.46 and max 3. Higher broad-fallback outliers such as `Bmal1`, `Rora`, and `Ctnnb1` appeared only after the immediate loop-anchor/developmental set and were connected by broad annotations or graph-supported communities rather than a source-like operation.

## Same-experiment corpus checks

I queried the selected same-experiment Findings/Claims corpus with `target_context`.

- `Ahdc1` had `target_found = false`, no Findings, no Claims, and no explicit comparator references in the released corpus, so no packaged `Ahdc1` interpretation was available.
- `Msl2`, the nearest chromatin-loop/NSL-like comparator in the analog table, had a high-confidence corpus Finding reporting zero downstream FDR<0.10 genes in all 20 measured neuronal cell groups after P16 CRISPR loss. That is the same experiment rather than independent replication, but it supports the count-table observation that a developmental chromatin regulator can be transcriptionally buffered in this acute postnatal readout.
- `Zic1` and `Zic2` were sparse in the focal class and divergent from each other. `Zic1` had a tiny focal signature, while `Zic2` was effectively near-null at the requested stricter BH < 0.05 threshold and its packaged FDR<0.10 report was a single weak `Rap1gap` event. The corpus also noted that represented Zic paralogs were not interchangeable acute postmitotic neuronal regulators.

## Matched profile check

I compared 14 selected broad Ahdc1 analogs in the declared Parquet, restricted to
`group_name = "151 TH Prkcd Grin2c Glut"`, using Wilcoxon `scores` as signed
profiles and `pvals_adj < 0.05` as the activity threshold:

- Lossless comparison: `workbench/ahdc1_broad_analog_profile_compare.json`
- Loop-anchor inspection: `workbench/ahdc1_loop_anchor_profile_inspect.json`
- Caller-declared cohort diagnostic: `workbench/ahdc1_broad_analog_profile_cohort.json`

The three direct promoter-enhancer-loop candidates were exactly the low-count nodes from the count table:

| node | positive DEGs | negative DEGs | total DEGs |
| --- | ---: | ---: | ---: |
| `Zic1` | 1 | 1 | 2 |
| `Zic2` | 0 | 0 | 0 |
| `Msl2` | 0 | 0 | 0 |

Across the 14-node broad analog cohort, the directional cohesion medians were only 0.02 for the positive top tail and 0.02 for the negative top tail. Pairwise checks from `Zic1`, `Zic2`, and `Msl2` to the broader high-response outliers had low whole-profile correlations and almost no shared significant DE genes. For example, `Zic1` versus `Rora` had Pearson 0.120 and one shared positive significant gene, while `Zic2` and `Msl2` had zero significant-gene intersections with `Rora`, `Ctnnb1`, `Bmal1`, `Wdr26`, and the other inspected broader peers. I therefore treated those high-count broader fallbacks as context for the existence of strong thalamic TF/chromatin responses, not as scale analogs for `Ahdc1`.

## Synthesis

The count-table prior and the closest source-like training perturbations both point to a null or one-/two-gene focal response. `Ahdc1` is not simply absent: it is expressed in two thirds of focal nuclei, lacks a known close paralog, and probably begins to lose renewable AHDC1 protein during the 21-28 day window. Those facts moved the point above a strict zero. The counterweight is that AHDC1 is a chromatin-establishment/developmental regulator with uncertain postmitotic renewal demand and possible persistence of installed chromatin states, and the closest measured loop-anchor/developmental comparators were sparse or silent rather than hundreds-of-DEG perturbations.

I therefore placed the forecast at the upper edge of the closest analog mean but still inside the zero-inflated local regime:

`predicted_n_degs = 1`
