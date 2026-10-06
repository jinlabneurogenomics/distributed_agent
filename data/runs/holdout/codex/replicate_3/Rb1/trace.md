## Prediction trace

Target and endpoint:

- The declared one-row holdout manifest
  `[local file: Rb1.csv]`
  contains only `Rb1`.
- The endpoint is `n_degs` in `151 TH Prkcd Grin2c Glut`: the count of measured
  genes in that focal thalamic glutamatergic class with Wilcoxon
  `pvals_adj < 0.05`.
- `Rb1` has no rows in the declared training expression parquet
  `[local file: training_de_all_cell_groups.parquet]`;
  the target profile and the target DEG count were therefore not observed in
  the quantitative training inputs.

Biology used from the endpoint-blind `Rb1` bundle:

- The canonical biology bundle
  `[local file: Rb1.json]`
  adjudicates pRB as a dynamic Rb-E2F nuclear corepressor whose operative
  stock should be substantially depleted during the P16 to P37-P44 CRISPR
  window.
- The same bundle reports strong exact focal reach: in non-target nuclei from
  `151 TH Prkcd Grin2c Glut`, `Rb1` was detected in 17,384 of 23,679 nuclei
  (73.415%) with mean CP10K 0.946.
- The strongest loss-of-function prior in the bundle is acute adult mouse
  forebrain deletion: pRB was reduced by one week and cortical neuronal density
  was markedly reduced by four weeks. That supports real perturbation within
  the window, but it is cortical/adult and the requested readout is
  survivor-conditioned thalamic nuclear RNA.

Training measurements used:

- The declared focal training count table
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  has 1,674 training perturbations. I recomputed focal `pvals_adj < 0.05`
  counts from the parquet for all 1,674 focal targets and found zero
  mismatches with that CSV.
- The focal count distribution is very sparse: 1,205 / 1,674 training targets
  have 0 DEGs, the median is 0, the 75th percentile is 1, the 90th percentile
  is 2, and the 95th percentile is 18.
- Pocket-protein paralogs `Rbl1` and `Rbl2`, the cleanest direct biological
  comparators named in the `Rb1` bundle, are absent from the training count
  table. The assayed cell-cycle / E2F / p53-axis targets that were present were
  all focal-class nulls:

| training target | `n_degs` in 151 TH Prkcd Grin2c Glut |
| --- | ---: |
| `E2f1` | 0 |
| `Cdkn2a` | 0 |
| `Myc` | 0 |
| `Mycn` | 0 |
| `Trp53` | 0 |
| `Trp63` | 0 |
| `Trp73` | 0 |

- I also checked broad chromatin/corepressor targets from the same focal
  parquet query. `Sin3a`, a general corepressor scaffold and therefore an
  intentionally broad upper-bound comparator, had 1,433 focal DEGs; nearby but
  less Rb-specific chromatin regulators gave much smaller or null responses
  (`Crebbp` 8, `Ep300` 0, `Smarca4` 0).

Synthesis:

`Rb1` is expressed in a large fraction of the focal thalamic cells and pRB
should turn over by harvest, so I did not treat it as an unexpressed or
unrealized knockout. At the same time, the endpoint is measured only in nuclei
that survived and retained the focal annotation; strong Rb1 loss can be partly
converted into depletion rather than many recovered-cell DEGs. The most
operation-adjacent measured perturbations did not produce any BH-significant
gene in this class, and the one high-DEG corepressor example, `Sin3a`, is far
broader than Rb-E2F derepression. I therefore forecast a low single-digit
signature: above a hard null because of the bundle's high expression and
turnover support, but below the weak `Crebbp` chromatin response and far below
the broad `Sin3a` survivor state.

Point prediction: `Rb1` -> 4.
