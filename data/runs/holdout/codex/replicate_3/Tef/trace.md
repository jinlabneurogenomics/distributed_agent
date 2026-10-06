# Direct forecast trace: Tef in 151 TH Prkcd Grin2c Glut

## Target and endpoint

- Target: `Tef`.
- Endpoint: `n_degs`, the count of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Declared training endpoint table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Declared training expression parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Canonical target biology bundle: `[local file: Tef.json]`, served with `target_outcome_exposed=false` and `labeled_neighbors_exposed=false`.

## Biology bearing

The biology-only `Tef` bundle supports target reach in the exact assayed class but predicts buffering of the single-gene lesion:

- `Tef` is expressed in the focal non-target nuclei: 20,305 of 23,679 nuclei, 85.75%, with mean raw UMI 2.41 and pseudobulk CPM 151.29.
- TEF is a renewed nuclear PAR-bZIP DNA-binding transcriptional activator, so a P16 disruptive edit is expected to stop new functional TEF production and to substantially deplete functional TEF by the P37-P44 harvest; the card marks this conclusion as sparse because no target-specific mouse neuronal TEF protein half-life was found.
- The strongest neural phenotype evidence is family-level. Postnatal epilepsy and mortality required combined `Dbp`/`Hlf`/`Tef` loss, and the card adjudicates DBP/HLF redundancy as same-context `full_compensation_same_context`, blocking a strong unqualified expectation for acute `Tef`-only loss.

I therefore treated `Tef` as an expressed transcription-factor perturbation with plausible on-target realization but a buffered endpoint, not as an unexpressed null and not as a broad lethal/core regulator.

## Held-in quantitative context

The focal training count table contains 1,674 held-in targets; `Tef`, `Dbp`, and `Hlf` are absent. Counts are strongly zero-inflated:

- 1,205 / 1,674 targets have `n_degs = 0`.
- Median `n_degs` is 0, mean is 14.05, the 90th percentile is 2, and the 95th percentile is 18.

I used the deterministic gene-annotation provider to define transcription factors in the perturbation universe and intersected them with the 151-class training counts. This produced 344 held-in TF targets:

- 284 / 344 held-in TFs have `n_degs = 0`.
- Median and 75th percentile are both 0; the 90th percentile is 2 and the 95th percentile is 15.

Because no specific TEF paralog or narrow complex analogue was present, I ran `gene-analog-nomination-skill` for `Tef` against the actual held-in count universe. It returned no `exact_complex_or_paralog`, no `bidirectional_corpus_comparator`, no `narrow_module`, and no `direct_interaction_or_dependency` candidates; all 1,273 available nominees were broad functional fallbacks. The leading broad DNA-binding TFs had focal counts `Creb1=10`, `Foxa2=0`, `Jund=0`, `Maf=0`, and `Neurod1=0`, which supports a very low scale but was too nonspecific to set the point by itself.

I also compared the observed 151-class expression profiles of core-clock/circadian and broad TF context genes from the declared expression parquet:

- Low direct clock-context counts: `Clock=3`, `Cry1=1`, `Cry2=3`, `Nr1d2=1`.
- Broader or less transferable circadian nuclear-regulator counts: `Bmal1=103`, `Nr1d1=116`, `Rora=278`.
- A quieter related nuclear receptor: `Rorc=0`.

The 13-node profile comparison over `Bmal1`, `Clock`, `Cry1`, `Cry2`, `Nr1d1`, `Nr1d2`, `Rora`, `Rorc`, `Creb1`, `Foxa2`, `Jund`, `Maf`, and `Neurod1` had no missing profiles in the exact 151-class parquet subset. Five of these had no significant features, four had 1-9 significant features, one had 10-49, and three had at least 50. The low `Clock`/`Cry`/`Nr1d2` scale was more transferable to a buffered single PAR-bZIP perturbation than the large `Bmal1`/`Nr1d1`/`Rora` signatures, because those are broader upstream or nuclear-receptor perturbations rather than single `Tef` loss.

## Synthesis

I placed `Tef` above 0 because focal expression is high and the operative TF stock is likely depleted within 21-28 days. I placed it near the floor because same-brain PAR-bZIP genetics argue for strong buffering of single `Tef` loss, the exact paralogs are absent from the held-in table, all deterministic available analogues are only broad TF fallbacks, and the held-in transcription-factor distribution has its 90th percentile at two DEGs.

The low direct clock-context values, `1, 1, 3, 3`, put the natural transferable center at two DEGs. I used that median as the integer point estimate while treating the high `Bmal1`, `Nr1d1`, and `Rora` counts as an upper-tail warning rather than scale-matched evidence.

Predicted `n_degs`: 2
