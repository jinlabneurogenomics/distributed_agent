# Direct forecast for Pdhx

Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

## Declared target biology

- Target: `Pdhx`.
- Exact focal expression from the canonical biology bundle: `Pdhx` was detected in 16,772 of 23,679 non-target nuclei, `70.8307%`, with mean CP10K `0.86995`. That makes focal-population reach plausible and argues against a zero forecast based on absence of expression.
- Molecular role: PDHX/E3BP is a noncatalytic pyruvate dehydrogenase complex core component that anchors E3/DLD. Loss stops synthesis of replacement PDHX-containing PDC rather than instantly removing pre-edit complex.
- Functional-stock prior: the bundle adjudicates PDHX stock as `likely_substantially_depleted` by the P16 to P37-P44 harvest window, but only with partial evidence because PDHX-specific turnover in postmitotic thalamic neurons was not measured.
- Observability residuals: PDHX human disease evidence is constitutional and developmental; the bundle did not find a matched postnatal mouse thalamic-neuron phenotype or a matched redundancy test.

## Training measurements used

The focal count table has 1,674 training perturbations:

- 1,205 have `n_degs = 0`
- 276 have `n_degs = 1`
- median = 0
- 75th percentile = 1
- 90th percentile = 2
- mean = 14.05, reflecting a small high-count tail

Counts for biologically selected PDC, mitochondrial carbon-flux, and mitochondrial carrier analogs in the same focal class:

| target | n_degs |
|---|---:|
| Dlat | 1 |
| Pdha1 | 1 |
| Dld | 0 |
| Aco2 | 0 |
| Dlst | 0 |
| Ogdh | 0 |
| Idh3a | 1 |
| Mdh2 | 1 |
| Mpc1 | 0 |
| Sdha | 1 |
| Slc25a12 | 1 |
| Slc25a4 | 1 |

The declared Parquet rows for these 12 training perturbations showed that the seven FDR-significant calls were all self-target transcript calls:

| target | significant measured gene |
|---|---|
| Dlat | Dlat |
| Pdha1 | Pdha1 |
| Idh3a | Idh3a |
| Mdh2 | Mdh2 |
| Sdha | Sdha |
| Slc25a12 | Slc25a12 |
| Slc25a4 | Slc25a4 |

The other five selected targets had no significant genes. In a focal-class profile comparison over the same 12 nodes, all profiles were available, seven were in the `1_to_9_significant_features` bucket, five were in the `no_significant_features` bucket, and significant-program overlap across the 66 selected pairs was empty. This supports a shared near-null downstream regime rather than a recurrent PDC/TCA stress program.

## Synthesis

The nearest measured PDC donors, `Dlat`, `Pdha1`, and `Dld`, argue strongly against a broad thalamic survivor-state transcriptome after direct PDC impairment: their counts are `1`, `1`, and `0`, and the nonzero calls are self knockdown only. The broader mitochondrial carbon-flux set remains in the same sparse regime. `Pdhx` is therefore unlikely to join the RNA-processing, proteostasis, or transcriptional-regulator tail with hundreds of DEGs.

The remaining decision is whether to predict no significant genes or one self-target call. I used `1` because the exact expression bundle shows `Pdhx` is present across most focal nuclei, the closest direct PDC perturbations often registered a single self transcript, and the endpoint includes the perturbed transcript. I did not treat target-transcript reduction as evidence of functional knockout strength; it only affects the integer count here because the assay's DEG count includes that row. The main downward uncertainty is that some structurally similar metabolic genes had self log-fold changes that did not pass BH correction, so an outcome of zero would not be surprising if `Pdhx` nuclear RNA is buffered or weakly depleted.

Predicted `n_degs`: `1`.
