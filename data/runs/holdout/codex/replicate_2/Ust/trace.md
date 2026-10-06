# Ust direct `n_degs` forecast

## Target

- Held-out target: `Ust`
- Focal cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`

The one-row manifest declares `Ust`, and the run-local characterization bundle is the biology-only bundle for `Ust`. The selected same-experiment corpus had no `Ust` Findings, Claims, or explicit comparator references, so it provided no endpoint-bearing `Ust` report evidence.

## Evidence Used

### Ust biology and in-assay reach

The canonical bundle describes Ust as a Golgi uronyl 2-O-sulfotransferase that installs 2-O-sulfate on chondroitin/dermatan glycosaminoglycan chains. The operative species is therefore a durable sulfated carrier state rather than free Ust enzyme. The card adjudicates harvest-time functional stock as `likely_substantially_depleted`, but with `partial` evidence completeness because Ust protein turnover, juvenile mouse thalamic carrier kinetics, and stable extracellular-matrix persistence were not measured directly.

Exact focal-population expression was present but sparse:

- `mean_log1p_cp10k = 0.09746016797335329`
- `mean_raw_umi = 0.22340470459056547`
- `pct_cells_expressing = 16.563199459436632`
- `n_cells_expressing = 3922 / 23679` non-target nuclei

The bundle's prior neural evidence is supportive but not tightly matched: embryonic neocortical Ust knockdown altered migration, a germline mouse predicted-null allele had postnatal startle/preweaning annotations, and regional adult mouse thalamic RNA is detected. None of those are a P16-to-P37/P44 thalamic postmitotic-neuron transcriptome measurement.

### Training-count background

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 visible training perturbations:

- 1,205 / 1,674 have `n_degs = 0`
- median `n_degs = 0`
- 75th percentile `n_degs = 1`
- 90th percentile `n_degs = 2`
- mean `n_degs = 14.05`, inflated by a long upper tail

Thus the focal-class endpoint is sparse; most visible biological knockouts are measured as zero even before adding any Ust-specific concerns about expression reach and matrix-product persistence.

### Visible glycan and proteoglycan analogs

I used the closest visible perturbations in the training count table for extracellular glycan/proteoglycan biology:

| target | focal `n_degs` |
|---|---:|
| `Adamts17` | 0 |
| `B3gat3` | 0 |
| `Ext1` | 0 |
| `Ext2` | 0 |
| `Glce` | 0 |
| `Gpc6` | 0 |
| `Hs6st2` | 0 |
| `Xylt1` | 0 |

These cover glycosaminoglycan linkage synthesis (`Xylt1`, `B3gat3`), heparan-sulfate polymerization or modification (`Ext1`, `Ext2`, `Glce`, `Hs6st2`), a proteoglycan coreceptor (`Gpc6`), and extracellular proteoglycan remodeling (`Adamts17`). They are not same-reaction Ust paralogs, but they are the most interpretable visible neighbors for a Golgi/extracellular sulfated-GAG perturbation.

### Matched profile check

I projected those eight anchors into the declared training Parquet in the exact `151 TH Prkcd Grin2c Glut` context using `gene_target`, `names`, `logfoldchanges`, and `pvals_adj < 0.05`. All eight had available 17,259-gene focal profiles and all eight had:

```text
significant_feature_count = 0
positive_significant_feature_count = 0
negative_significant_feature_count = 0
response_activity_status = no_significant_features
```

Their first-hop profile neighborhoods were broad and weak rather than a tight nonzero state: the 8 anchors touched a 350-node bounded nearest-neighbor union, too large for the tool to compute an all-pairs topology digest. I treated that as a check that these zero labels were not hiding an obvious recurrent active module in the matched Parquet.

## Synthesis

Ust loss is biologically credible within 21-28 days because the enzyme's product is renewed, Ust lacks a close same-reaction paralog in the bundle's bounded search, and exact in-assay expression confirms some target-positive focal nuclei. Those points argue against dismissing the perturbation as impossible.

The quantitative bearing is still downward. Ust RNA reaches only about one sixth of non-target focal nuclei, its strongest prior phenotypes are developmental or whole-animal rather than postmitotic thalamic single-nucleus RNA, and the best task-matched visible extracellular-GAG/proteoglycan perturbations are uniformly null in the same cell class. Since the count table itself is heavily zero-inflated, this leaves no reason to move away from the all-zero analog cohort.

Point prediction: `0`.
