# Max n_degs forecast

## Target and endpoint

- Held-out target: `Max`, from the one-row manifest and the endpoint-blind
  biology bundle.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
  in the focal population.

## Evidence used

- `Max` biology bundle
  `[local file: Max.json]`
  had SHA-256 `1baabf6a5754c46474abdfd81fdc2aae01217135471070ac5553b2205adee580`
  in the perturbation-characterization registry. The bundle states that no
  endpoint values were used in the biological cards.
- Exact focal expression reach for `Max` was nonzero but moderate:
  11,468 of 23,679 matched non-target nuclei expressed the feature
  (`48.431%`), with mean raw UMI `0.7300`, mean CP10K `0.4517`,
  and pseudobulk CPM `45.75`.
- The functional-stock card called MAX a renewable nuclear subunit of MYC- and
  repressor-containing DNA-binding heterodimers and judged functional stock at
  P37-P44 as likely substantially depleted after P16 editing. The same card and
  observability card also made the main uncertainty explicit: the protein-
  turnover and deletion evidence came from cultured cells or non-neural mouse
  B cells, and no matched postnatal thalamic-neuron loss model was identified.
- The declared training count table
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  contained 1,674 training targets and did not contain `Max`. In this focal
  class, 1,205 targets had `0` DEGs, 469 were positive, the median was `0`, the
  75th percentile was `1`, the 90th percentile was `2`, and the 95th percentile
  was `18`.
- Curated analog nomination over that exact 1,674-target universe placed `Myc`
  and `Mga` as the strongest exact-complex / projected-complex MAX-network
  candidates, with `Mycn` as a physical-interaction candidate. The directly
  measured focal counts for the closest MYC/MAX-side candidates were
  `Myc = 0`, `Mycn = 0`, `Mnt = 0`, `Mga = 2`, and `Tfdp1 = 2`.
  Adding nearby exact or direct candidates kept the center at a very sparse
  scale: `Ehmt1 = 4`, `Cdkn2a = 0`, and `Hdac5 = 0`.
- The declared Parquet for those same focal contrasts agreed with the scalar
  counts. In the nine-node MAX-neighbor profile comparison
  `[Myc, Mga, Mycn, Mnt, Tfdp1, Ehmt1, Sin3a, Cdkn2a, Hdac5]`, five nodes had
  no FDR-significant focal genes, three had 1-9, and only `Sin3a` exceeded 50.
- Same-experiment corpus Findings `Myc:F003` and `Mga:F005` interpret the
  represented MYC/MAX/MGA/MNT/E2F side as sparse, target-specific, and
  nonconvergent rather than as one shared postmitotic neuronal transcriptional
  module. I used these Findings only as packaged interpretation of the
  training perturbations, not as independent replication.

## Synthesis

MAX expression and the multi-week edit-to-harvest window make a realized lesion
plausible, so I did not use a pure dropout or unexpressed-gene null. The
quantitative scale, however, is governed by the observed MAX-network side of
the training table: direct and near-direct partners were flat or nearly flat in
`151 TH Prkcd Grin2c Glut`, and `Mga`/`Tfdp1` topped out at two DEGs. `Sin3a`
is a native Mad-Max complex member and had a 1,433-DEG focal response, but that
looks like a SIN3A chromatin-corepressor outlier rather than a transferable MAX
point estimate because the MYC/MGA/MNT side did not phenocopy it.

I therefore placed `Max` at the sparse but nonzero edge of the close-comparator
range instead of the exact zero median or the broad `Sin3a` branch.

Predicted `n_degs`: **2**
