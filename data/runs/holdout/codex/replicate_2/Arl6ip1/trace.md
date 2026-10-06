# Arl6ip1 forecast for `151 TH Prkcd Grin2c Glut`

## Endpoint and declared target

- Target: `Arl6ip1`.
- Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `p < 0.05`.
- The declared training count table has 1,674 perturbations and does not contain `Arl6ip1`.
- In this focal class, the training endpoint is sparse: 469/1,674 perturbations have a nonzero count, the median is 0, the 75th/85th percentiles are 1, the 90th percentile is 2, and the 95th percentile is 18.

## Biology used

The endpoint-blind Arl6ip1 characterization bundle identifies ARL6IP1 as an integral ER membrane-shaping component that promotes FAM134/Retreg-dependent ER remodeling and ER-phagy. Complete constitutive loss produces progressive mouse neural and neuromuscular phenotypes, so the gene is not a biologically inert neuronal target. Exact in-assay expression reach is also material: Arl6ip1 is detected in 15,296/23,679 matched non-target nuclei in this cell class, 64.60%, with mean log1p CP10K 0.465.

The same bundle leaves short-window functional realization unresolved. The P16 edit should stop new ARL6IP1 synthesis, but it need not immediately eliminate ER-embedded ARL6IP1 protein or already shaped ER structure, and no postmitotic-neuron ARL6IP1 turnover clock was available for the 21-28 day P16-to-harvest interval. This argues for possible activity, but with a small acute recovered-nucleus expression footprint rather than a high-confidence stress or degeneration state.

## Training perturbations used

I used typed analog nomination only to avoid a symbol-prefix search. It found no exact complex/paralog or narrow-module training match for `Arl6ip1`; the only higher-specificity training nominee was `Ssr4` through a STRING physical edge, and the rest of the ER nominees were broad ER/endoplasmic-reticulum-tubule annotations. The closest source-adjacent measured genes I retained were therefore ER-tubule/reticulophagy genes plus a few ER-phagy/autophagy boundary genes, interpreted by biological specificity:

| perturbation | relationship to Arl6ip1 biology | focal `n_degs` |
| --- | --- | ---: |
| `Retreg1` | FAM134B ER-phagy partner named in the Arl6ip1 bundle | 1 |
| `Atl1` | ER tubular network organization | 1 |
| `Atl3` | ER tubular network organization | 0 |
| `Reep1` | ER tubular network | 1 |
| `Reep2` | ER tubular network | 1 |
| `Rab18` | ER tubular network | 0 |
| `Spast` | ER tubular network | 0 |
| `Ssr4` | STRING physical / Sec61-translocon ER boundary | 1 |
| `Atg5`, `Becn1`, `Lamp2`, `Psen1`, `Trp53` | broader autophagy, lysosomal, ER, or stress context controls | 0 |
| `Map1lc3a`, `Ppt1`, `Bcap31` | broader autophagy/ER-membrane context controls | 1 |
| `Mtor` | broad autophagy regulator, off-axis for direct ARL6IP1 loss | 2 |
| `Hspa5` | ER stress chaperone boundary | 5 |

Profile comparison in the declared Parquet and exact `151 TH Prkcd Grin2c Glut` context found all 18 inspected analog/boundary nodes and no moderate or high response among them: 8/18 had zero significant features and the other 10 were in the 1-to-9 significant-feature bucket. The seven ER-tubule/reticulophagy-like nodes (`Atl1`, `Atl3`, `Reep1`, `Spast`, `Reep2`, `Rab18`, `Retreg1`) had five one-DEG profiles and two null profiles. They shared some weak negative-tail shape across continuous log-fold-change ranks, but their FDR-significant programs did not share any significant gene, so I treated them as low-scale local evidence rather than as a robust recurrent module.

## Forecast

The direct FAM134/ER-shaping evidence and 64.6% focal expression argue against rounding down to a confident null, but the available measured source-adjacent perturbations are overwhelmingly 0 or 1 DEG and the biology bundle gives no timing anchor showing that pre-existing ER membrane stock should be depleted enough by P37-P44 to trigger a larger recovered-cell response. I therefore set the point prediction at the upper edge of the closest local analogs, not at the off-axis ER-stress boundary.

`predicted_n_degs = 1`
