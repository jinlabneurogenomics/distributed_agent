# Direct DEG-count forecast for Dync1h1

Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with
BH-adjusted Wilcoxon `p < 0.05`.

Prediction: `75`

## Evidence used

- The one-row holdout manifest names `Dync1h1`.
- The exact in-assay non-target expression card reports Dync1h1 expression in
  `151 TH Prkcd Grin2c Glut`: 23,457 / 23,679 non-target nuclei express the
  feature, 99.06% of cells, with mean raw UMI 8.17 and pseudobulk 511.80 cpm.
  This made lack of focal reach unlikely.
- The canonical biology card classifies DYNC1H1 as the force-generating heavy
  chain and scaffold of cytoplasmic dynein-1. A disruptive edit should stop
  synthesis of full-length motor-domain-containing heavy chain; old dynein-1
  pools can persist, but adult postmitotic photoreceptor deletion crosses into
  overt functional failure over a three-to-four-week interval. The card
  therefore calls functional stock by harvest likely substantially depleted, but
  with transfer uncertainty from retina to juvenile thalamic neurons.
- DYNC2H1 is a distinct ciliary dynein-2 heavy chain rather than a redundant
  cytoplasmic dynein-1 paralog; in the declared focal count table `Dync2h1` and
  `Dync2i1` both had 0 DEGs. I treated them as specificity boundaries, not as
  estimates for cytoplasmic dynein-1.
- Cytoplasmic dynein-1 cargo transport requires the dynein complex, dynactin,
  and an activating adaptor. The declared training target `Dctn1` encodes the
  p150/Glued dynactin subunit, making it the closest assayed dynein-1 transport
  perturbation in the count table (Reck-Peterson et al., PMID:29662141).

## Training measurements used

Declared focal count table:

| comparator set | focal `n_degs` |
| --- | --- |
| `Dctn1` | 75 |
| `Rab7` | 501 |
| `Vps54`, `Vps35` | 31, 17 |
| `Cltc`, `Htt` | 3, 3 |
| `Kif1a`, `Kif1b`, `Kif5a`, `Kif5c`, `Klc1`, `Klc2` | 0-1 |
| `Tuba1a`, `Tuba4a`, `Tubb4b`, `Tubb5`, `Map1b`, `Mapt`, `Actg1` | 1-7 |
| `Dync2h1`, `Dync2i1` | 0, 0 |

The full count distribution is sparse: 1,205 / 1,674 training targets are 0;
the median is 0, the 75th percentile is 1, the 95th percentile is 18, and
`Dctn1` at 75 is already at approximately the 97th percentile. `Rab7` is much
larger, but it is a late-endosome/lysosome GTPase and not a dynein-1 structural
subunit, so I used it as an upper biological warning rather than as the primary
scale donor.

From the declared Parquet in the same focal population, the main nonzero
transport comparators broke down as:

| target | total DEGs | up | down | matched perturbed nuclei |
| --- | ---: | ---: | ---: | ---: |
| `Rab7` | 501 | 311 | 190 | 215 |
| `Dctn1` | 75 | 49 | 26 | 182 |
| `Vps54` | 31 | 6 | 25 | 161 |
| `Vps35` | 17 | 8 | 9 | 133 |

A symmetric profile comparison of 24 training transport/cytoskeletal nodes in
the exact `151 TH Prkcd Grin2c Glut` context wrote
`evidence/transport_profile_compare.json` and
`evidence/transport_profile_cohort.json`. It did not show a tight reusable
transport module: the cohort was sparse except for `Rab7` and `Dctn1`, and
the lower-count kinesin, tubulin, tau, clathrin/SNARE, and dynein-2 controls
did not support a high count for generic microtubule or vesicle genes.

## Synthesis

The biology argues against a null: Dync1h1 is expressed in essentially the
entire assayed focal population, the edit should eliminate new functional
cytoplasmic dynein-1 heavy-chain supply, dynein-1 is not replaced by dynein-2,
and the declared three-to-four-week window is long enough for material
postmitotic motor-stock loss.

The quantitative scale argues for a focal count in the tens rather than
hundreds. The direct dynactin comparator `Dctn1` is the best measured local
anchor at 75 DEGs. `Rab7` shows that this population can mount a much larger
trafficking/lysosomal response, but Rab7 loss is not the same proximal lesion.
The ciliary dynein-2 and plus-end motor/cytoskeletal comparators are mostly
0-7 DEGs and keep the Dctn1 anchor from being lifted merely because the target
is a motor or microtubule-associated gene. Finally, survivor-conditioned nuclei
and persistence of pre-edit DYNC1H1 make complete dynein-1 failure by harvest
uncertain.

I therefore used `Dctn1` as the nearest scale-bearing perturbation and kept the
forecast at its observed focal burden:

`predicted_n_degs = 75`
