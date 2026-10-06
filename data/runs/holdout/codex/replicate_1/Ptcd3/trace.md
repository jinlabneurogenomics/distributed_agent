# Ptcd3 forecast trace

## Endpoint

- Target: `Ptcd3`, the one row in the declared holdout manifest.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Quantity predicted: measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- The visible training count table has 1,674 perturbations and does not contain `Ptcd3`.

## Biology used

The canonical biology bundle identifies PTCD3 as the mitochondrial small-ribosomal-subunit protein mS39, an rRNA-binding component required for mitochondrial translation (`ptcd3-operation-mitoribosomal-ms39`). PTCD3 depletion is target-proximal to mitochondrial protein synthesis and respiratory capacity (`ptcd3-operation-translation-respiration`), so a realized acute knockout could plausibly matter in neurons.

That prior was tempered by two timing and buffering uncertainties. A P16 edit should block new intact PTCD3, but it would not directly remove the mS39 already installed in assembled mitoribosomes, and the curated bundle found no PTCD3 protein half-life, mS39 exchange time, or post-edit neuronal time-to-loss measurement for the 21-28 day window (`ptcd3-turnover-unknown`). `Ptcd3` itself is clearly in reach in the focal population: 20,854 of 23,679 non-target nuclei expressed it, for 88.07% expression, mean 2.707 raw UMIs and mean log1p(CP10K) 0.884. That argues against a simple absence-of-expression null but does not quantify editing strength or downstream response.

## Training measurements used

The focal count table is extremely sparse overall: median `n_degs` is 0; 1,205/1,674 targets have 0 DEGs; the 90th percentile is 2 DEGs; and the 95th percentile is 18 DEGs.

The nearest visible mitochondrial-translation or mitochondrial-RNA maintenance perturbations were quiet in the same cell class:

| target | 151 TH Prkcd Grin2c Glut `n_degs` | minimum BH-adjusted p in the 151 Parquet rows | matched perturbed nuclei |
| --- | ---: | ---: | ---: |
| `Fars2` | 0 | 1.000 | 180 |
| `Gfm2` | 0 | 1.000 | 190 |
| `Lars2` | 0 | 0.952 | 256 |
| `Lrpprc` | 0 | 0.174 | 111 |
| `Rars2` | 0 | 1.000 | 165 |

A broader sanity check of 31 visible `Cox*`, `Nduf*`, `Coa8`, and `Lrpprc` respiratory-chain targets was also low-yield: 19 had 0 DEGs, 12 had 1 DEG, none had more than 1, and 11/12 of the one-DEG cases were explained by a significant self-transcript decrease. The direct Parquet rows therefore did not show a broad 151 thalamic transcriptional state for this mitochondrial axis.

## Synthesis

I treated Ptcd3 as an expressed, biologically real mitochondrial-translation target, but the training perturbations closest to that process were zero-DEG examples and the stock card left the amount of functional mS39/mitoribosome depletion by harvest unresolved. Because the residual nonzero case looked most likely to be a lone self-transcript effect, and self-target transcript loss is not predictable from the biology bundle, I rounded down to the quiet-state point forecast.

Predicted `n_degs`: 0
