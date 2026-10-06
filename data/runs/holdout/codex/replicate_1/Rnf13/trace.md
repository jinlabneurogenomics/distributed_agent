# Rnf13 direct n_degs forecast

## Declared target and endpoint

- Target: `Rnf13`.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- The active one-row manifest and the canonical biology bundle both identify `Rnf13`; `Rnf13` is absent from the 1,674-row training count table.

## Canonical biology-only target evidence

Evidence source: declared `Rnf13` biology bundle, SHA256 `05670e95a2e25458f00f03036e7fd6c9eb83c538008475c743096bdea4db7f8f`, retrieved through `characterization_bundle(view="biology")`.

- The focal-population expression reach is real: in non-target nuclei from `151 TH Prkcd Grin2c Glut`, `Rnf13` is detected in 16,324 of 23,679 nuclei, or 68.94%, with mean log1p CP10k 0.526 and mean raw UMI 1.413.
- Functional stock was adjudicated as `likely_substantially_depleted` by P37-P44 after P16 editing. The rationale is that RNF13 is an actively processed membrane/cytoplasmic PA-TM-RING E3 ubiquitin ligase rather than a permanently installed structural pool.
- Observability is weaker than stock depletion. Mouse Rnf13 loss has a documented adult hippocampal synaptic phenotype, but that evidence is constitutive, outside thalamus, and does not prove an acute P16-onward requirement in thalamic glutamatergic neurons. Related PA-TM-RING proteins, especially RNF167, are only a hypothetical redundancy signal.

I therefore treated Rnf13 as engaged and reachable in the assayed cells, but as more likely to produce a small synaptic/endosomal survivor-cell signature than a core proteostasis or lysosomal-collapse signature.

## Training endpoint scale

Evidence source: declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.

- The 1,674 measured training perturbations are heavily zero-inflated: 1,205 have 0 DEGs, 1,481 have at most 1 DEG, and the median count is 0.
- Count scale is very skewed in this cell class: the 90th percentile is 2, the 95th percentile is 18, the 99th percentile is 430, and the maximum is 2,677.

Selected same-endpoint training comparators were chosen from Rnf13's operation rather than from observed proximity to the held-out target:

| comparator set | observed `n_degs` in `151 TH Prkcd Grin2c Glut` | interpretation |
| --- | ---: | --- |
| RING / ubiquitin ligase controls: `Rnf216`, `Rnf220`, `Cblb`, `Ube3a` | all 0 | most measured E3 perturbations near this level do not create an FDR-significant survivor signature in the focal thalamic class |
| Synaptic-vesicle / SNARE comparators: `Stx1b`, `Nsf`, `Stxbp1`, `Syn1`, `Syn2`, `Syp` | 0, 0, 1, 1, 0, 1 | the closest measured functional readouts to the Rnf13 hippocampal snapin/SNARE story sit at zero-to-single-gene scale |
| Small Rab / vesicle-trafficking comparators: `Rab18`, `Rab27a`, `Rab3gap1`, `Rab3gap2` | all 0 | perturbing a vesicle-trafficking label alone is usually silent in the focal endpoint |
| Retromer / endosomal trafficking boundaries: `Vps35`, `Vps54`, `Rab7` | 17, 31, 501 | core endosomal machinery can be visibly transcriptional, but these losses are more central than Rnf13's documented E3/substrate-tuning role |

## Expression-parquet check

Evidence source: `training_de_all_cell_groups.parquet`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"` with `pvals_adj < 0.05` in `profile_compare`.

The matched profile comparison over 17 selected comparators reproduced the same scale in the expression table: 11 had no significant features, 3 had 1 to 9, 2 had 10 to 49, and only `Rab7` had at least 50. Exact focal counts from the profile table were:

- `Rnf216`, `Rnf220`, `Cblb`, `Ube3a`, `Stx1b`, `Nsf`, `Syn2`, `Rab18`, `Rab27a`, `Rab3gap1`, `Rab3gap2`: 0
- `Stxbp1`, `Syn1`, `Syp`: 1 each
- `Vps35`: 17
- `Vps54`: 31
- `Rab7`: 501

## Forecast

The empirical prior strongly favors 0, and the direct synaptic/E3 comparators argue against a broad response. I still placed Rnf13 just above zero because the target is expressed in most focal non-target cells and its functional protein pool should turn over within the 21-28 day window, making a self-transcript-scale or very small downstream signal more plausible than a strict null. The endosomal machinery positives were used only as upward boundaries: Rnf13 is too peripheral, potentially redundant, and context-mismatched to borrow their tens-to-hundreds of DEGs.

Predicted `n_degs`: **1**.
