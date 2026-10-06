# Direct `n_degs` forecast for Trpv4

Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with Wilcoxon BH-adjusted `p < 0.05`.

Prediction: `0`.

## Evidence used

- The held-out manifest target is `Trpv4`.
- The Trpv4 characterization bundle was served in the biology-only view: labeled-neighbor outcomes and the Trpv4 endpoint outcome were not exposed.
- The exact in-assay focal expression measurement for `151 TH Prkcd Grin2c Glut` was extremely low:
  - `n_cells_expressing = 167` of `23679` matched non-target nuclei.
  - `pct_cells_expressing = 0.705266%`.
  - `mean_raw_umi = 0.007475`, `mean_log1p_cp10k = 0.003355`, and `pseudobulk_cpm = 0.4685`.
- The biology card supports functional realization where Trpv4 is actually expressed: TRPV4 is a dynamic membrane cation channel, and the 21-28 day edit-to-harvest window should be long enough to deplete most functional channel stock in successfully edited expressing cells. The card also leaves the relevant thalamic neuronal phenotype, exact latency, and compensation unresolved.
- The focal training count table is dominated by null observations even though this is a high-yield class:
  - 1,205 / 1,674 training targets had `n_degs = 0`.
  - 276 / 1,674 had `n_degs = 1`.
  - Only 193 / 1,674 had at least 2 DEGs, 106 / 1,674 had at least 10, and 43 / 1,674 had at least 100.
  - Median `n_degs` was 0 and the 75th percentile was 1.
- I used the declared expression parquet in the same focal group to check a caller-selected training cohort of channel-like comparators. Structural/operation-adjacent channel perturbations were silent or nearly silent:
  - `Trpa1`: 0 DEGs
  - `Trpm3`: 0 DEGs
  - `Trpm7`: 0 DEGs
  - `Trpv1`: 0 DEGs
  - `Pkd1`: 0 DEGs
  - `Itpr1`: 0 DEGs
  - `Tmem63c`: 0 DEGs
  - `Tmem63b`: 1 DEG
- Positive calcium- or channel-associated counterexamples were present but biologically less transferable to a low-reach TRPV4 forecast:
  - `Grin1`: 89 DEGs
  - `Atp2a2`: 187 DEGs
  - `Calm1`: 14 DEGs
  - `Cacna1g`: 12 DEGs

## Reasoning

The strongest downward-bearing evidence was the exact focal reach. A perturbation of a Ca2+-permeable channel can be functional after a 21-28 day CRISPR window, but the direct target is expressed in only about 0.7% of recovered matched non-target nuclei in this aggregated thalamic glutamatergic class. Any cell-autonomous TRPV4 loss state is therefore diluted across a broad class in the Wilcoxon contrast. Low nuclear mRNA does not prove absence of protein in every nucleus, but here it agrees with the card-level prior that TRPV4 is low/restricted in neural tissue rather than broadly required in thalamic NeuN-positive neurons.

The same focal count table puts zero at the modal and median outcome, and the matched channel cohort keeps the relevant local scale near zero: TRP-family/mechanosensitive or intracellular cation-channel perturbations in training were 0 except for a one-gene `Tmem63b` footprint. Larger responses from `Grin1`, `Atp2a2`, `Calm1`, and `Cacna1g` show that calcium and channel biology is assay-visible when a perturbation hits broad neuronal machinery, so I did not treat "ion channel" as intrinsically null. I treated those positive cases as upper context rather than close scale donors because Trpv4 has much narrower measured reach and a more peripheral osmotic/mechanosensory operation in this focal population.

Synthesis: functional Trpv4 loss is plausible in the rare expressing cells, but the assayed aggregate gives it too little focal-population reach to move any measured gene past BH `p < 0.05`. The most likely integer count is therefore zero.
