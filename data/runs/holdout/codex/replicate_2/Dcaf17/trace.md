# Dcaf17 n_degs forecast for `151 TH Prkcd Grin2c Glut`

## Declared target and endpoint

- Target: `Dcaf17`, the single row in the declared holdout manifest.
- Focal population: `151 TH Prkcd Grin2c Glut`, resolved exactly to thalamic glutamatergic neurons.
- Endpoint: number of measured genes in that class with Wilcoxon `pvals_adj < 0.05` after `Dcaf17` perturbation.
- No `Dcaf17` observed profile or DEG count was used.

## Biology prior from the held-out bundle

The declared biology bundle reports exact focal-population reach for the held-out
target: `Dcaf17` was detected in 8,578 of 23,679 non-target nuclei
(`36.226%`) with mean raw UMI `0.480`, pseudobulk `30.113` CPM, and
mean log1p CP10K `0.212` in `151 TH Prkcd Grin2c Glut`. This makes the
transcript measurable in the assayed population but not broadly high.

The functional-stock card was the main downward modifier. DCAF17 is only
assigned a putative nuclear/nucleolar DDB1-CUL4 substrate-receptor role; its
physiologic substrate and neuron-specific reaction are unresolved. A disruptive
edit should stop new intact DCAF17 synthesis, but the bundle found no
target-specific DCAF17 protein half-life, CRL4-DCAF17 residence time, or
postmitotic neuronal persistence measurement. The card therefore adjudicated
`functional_stock_by_harvest = indeterminate` for the P16 to P37-P44 interval.

Human biallelic DCAF17 disease and the postnatal mouse testis phenotype support
that DCAF17 loss can matter biologically, and the bounded paralog search found
no close named mouse paralog. Those facts did not outweigh the assay mismatch:
the direct mouse loss phenotype is non-neural, the human phenotype is chronic
congenital disease, and neither establishes a 21-28 day thalamic neuronal RNA
response.

Primary provenance: declared `biology_bundles/Dcaf17.json`, served again by
`characterization_bundle(target="Dcaf17", view="biology")`.

## Training measurements used

The declared class-specific count table contained 1,674 observed training
perturbations. Its empirical distribution was zero-heavy:

- 1,205 of 1,674 perturbations had `n_degs = 0`.
- Median = 0; 75th percentile = 1; 90th percentile = 2; 95th percentile = 18.
- The mean was inflated to 14.05 by a very small high-yield tail headed by
  core RNA/proteostasis/transcriptional regulators.

`Dcaf17` was absent from the table. The bundle-named core CRL4 genes
`Ddb1`, `Cul4a`, and `Cul4b` were also absent, so I used the declared mouse
annotation nominator against the exact 1,674-gene training universe rather
than matching by gene-symbol pattern.

That nomination found only four available specific
`direct_interaction_or_dependency` candidates for `Dcaf17`; their focal-class
counts were:

| candidate | typed relationship to Dcaf17 | `n_degs` |
| --- | --- | ---: |
| `Dcaf8` | STRING physical + broad CUL4/DCAF annotations | 0 |
| `Ddb2` | STRING physical + broad CUL4-DDB1 annotations | 0 |
| `Arih1` | STRING physical + ubiquitination/nuclear annotations | 7 |
| `Crbn` | STRING physical + protein-ubiquitination annotations | 0 |

The best broader ubiquitination fallback with matched assay coverage,
`Fbxo11`, had `n_degs = 1`; another Cul4/neddylation fallback, `Nfe2l2`,
had `n_degs = 0`. These six nodes were then re-read from the declared
Parquet in `151 TH Prkcd Grin2c Glut`, where the significant-feature counts
matched the count table exactly: four had no significant features and the two
nonzero examples remained in the `1_to_9_significant_features` activity bucket.

The signed expression profiles of this CUL4/ubiquitination set did not form a
coherent high-response state. Across all 15 available selected pairs, the mean
top-tail overlap coefficient was only `0.075` for positive tails and `0.117`
for negative tails. There was no positive significant-program overlap; the
single negative significant-program comparison had overlap coefficient `0`.

Primary provenance: declared
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, declared
`training_de_all_cell_groups.parquet`,
`workbench/dcaf17_analog_nominations.jsonl`,
`workbench/profile_compare_cul4_ubiquitination.json`, and
`workbench/profile_cohort_cul4_ubiquitination.json`.

## Forecast

I used the local CRL4/DCAF and ubiquitination measurements as the quantitative
anchor because they best match the putative DDB1-CUL4 substrate-receptor
operation while remaining observed in the same focal population. Their
endpoint median is 0, three of the four most specific candidates are exactly
0, and the nonzero specific candidate, `Arih1`, is still only 7 DEGs. The
broader fallbacks were also 0 or 1.

The target-specific biology did not justify shifting upward from that local
zero: `Dcaf17` is expressed but in a minority of non-target nuclei, the
CRL4-DCAF17 substrate map in thalamic neurons is unknown, and residual
pre-edit protein or downstream modified substrates could persist through the
21-28 day post-edit window. Those uncertainties make a large high-tail count
unlikely and make the point estimate favor the exact-zero mode of the matched
training analogs.

Predicted `n_degs`: **0**.
