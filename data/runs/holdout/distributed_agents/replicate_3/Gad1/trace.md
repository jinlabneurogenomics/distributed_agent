# Held-out prediction for `151 TH Prkcd Grin2c Glut`

## Question and resolved ambiguities

The held-out manifest contains one target, `Gad1`. I interpreted the endpoint as the exact focal-cell count of measured genes satisfying `pvals_adj < 0.05` in the supplied Wilcoxon differential-expression table, not an FDR 0.10 count and not a cross-cell-type aggregate. I preserved the manifest order and made one non-negative integer point prediction.

`Gad1` itself is absent from the released training endpoint as a target to predict. It can still appear as a measured transcript in other perturbations, and I treated those rows only as evidence about comparator signatures, not as a direct `Gad1` perturbation readout.

## Sources used

- Input training counts: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Input differential-expression parquet: `training_de_all_cell_groups.parquet`.
- Same-experiment Distributed Agents corpus, release `perturbai-july-260713-sourceguard-1773-v1`.
  - `Gad2:F001-F005`: Gad2 was self-only in inhibitory neurons, flat in glutamatergic neurons, and had no robust whole-universe phenocopy.
  - `Slc32a1:F001-F005`: vesicular GABA transporter loss was pan-null downstream and was a transmitter-mismatch negative outside GABAergic cells.
  - `Slc6a1:F001-F006`: GABA transporter perturbation was transcriptionally buffered, with only one FDR<0.10 downstream event across the universe and none in this focal group.
  - `Abat:F001-F004`: GABA-catabolic perturbation was flat in this glutamatergic context and did not yield a robust phenocopy.
  - `Dlx6:F001-F005`: a measured GABAergic developmental regulator was all-null after postnatal Dlx6-only coding perturbation.
- Public biology:
  - Erlander et al. 1991, Neuron, DOI `10.1016/0896-6273(91)90077-d`, PMID `2069816`: mammalian `Gad1` and `Gad2` encode the distinct GAD67 and GAD65 glutamate decarboxylases that synthesize GABA.
  - Martin and Rimvall 1993, Journal of Neurochemistry, DOI `10.1111/j.1471-4159.1993.tb03165.x`, PMID `8419527`: GAD67 and GAD65 differ in regulation and localization, with GAD67 contributing a more generally distributed basal GABA-synthetic pool and GAD65 enriched for terminal, demand-responsive synthesis.
  - Asada et al. 1997, PNAS, DOI `10.1073/pnas.94.12.6496`, PMID `9177246`: germline GAD67 loss severely reduces neonatal cortical GABA content, confirming `Gad1` as a real GABA-synthesis enzyme rather than a passive marker.
  - Yao et al. 2023, Nature, DOI `10.1038/s41586-023-06812-z`, PMID `38092916`: the Allen Brain Cell Atlas whole-mouse-brain taxonomy separates glutamatergic and GABAergic transcriptomic identities, which is the basis for treating a `Glut` thalamic class as the wrong transmitter context for a GABA-synthetic enzyme.

## Computations over the training data

I used DuckDB to aggregate the focal DE rows by `gene_target` and count rows with `pvals_adj < 0.05`; this reproduces the endpoint definition directly from the parquet. The focal training set had 1,674 observed targets: 1,205 were zeros, 469 were nonzero, and the smallest nonzero count was 1 DEG.

For biologically selected comparators in the focal cell group, I also recorded the minimum FDR and matched perturbed nuclei:

| Perturbation | Mechanistic relation to Gad1 | focal `n_degs` | min FDR | `n_pert_matched` |
| --- | --- | ---: | ---: | ---: |
| `Gad2` | paralogous GAD65 GABA-synthesis enzyme | 0 | 1 | 178 |
| `Slc32a1` | vesicular GABA transporter, downstream GABA packaging | 0 | 1 | 268 |
| `Slc6a1` | presynaptic/plasma-membrane GABA uptake | 0 | 1 | 220 |
| `Abat` | GABA catabolism | 0 | 0.831 | 188 |
| `Gls` | glutaminase, upstream glutamate supply | 0 | 0.0989 | 103 |
| `Dlx6` | forebrain GABAergic program regulator | 0 | 1 | 294 |
| `Arx` | interneuron developmental regulator | 0 | 0.346 | 269 |

The same set had no significant movement in immediate-early/activity genes or GABA identity genes in the focal group. For example, under `Gad2` perturbation the focal rows for `Fos`, `Npas4`, `Nr4a1`, `Vgf`, `Gad1`, `Slc32a1`, and `Slc6a1` all had FDR = 1.

As a positive control, several postsynaptic GABA-A receptor subunits were detectable in the same focal group:

| Perturbation | focal `n_degs` | significant focal genes |
| --- | ---: | --- |
| `Gabra1` | 1 | `Gabra1` |
| `Gabrb2` | 4 | `Gabrb2`, `Nr4a1`, `Vgf`, `Nalf1` |
| `Gabrd` | 2 | `Gabrd`, `Cttnbp2` |
| `Gabrg2` | 1 | `Gabrg2` |

These are counterexamples rather than analogs: receptor subunits can act in the thalamic glutamatergic neuron being sequenced, while `Gad1` acts in GABA synthesis and should mostly matter in GABA-releasing cells.

I additionally ran `profile_neighbors` on the focal signatures of `Gad2`, `Slc32a1`, `Slc6a1`, `Abat`, and `Dlx6`, using the 1,674 focal training targets as the eligible universe and ranking by whole-profile correlation plus positive/negative signed-tail overlap. Every one of these anchors had `significant_feature_count = 0`, and the top neighbors were unrelated genes with weak top-50 signed-tail overlaps, not a GABA-synapse module. I therefore used the profile search as negative evidence against an occult focal GABA module, not as a pooled prediction rule.

## Target-specific reasoning

### `Gad1`

`Gad1` encodes GAD67, one of the two glutamate decarboxylases that synthesize GABA from glutamate. The closest assayed paralog is `Gad2`/GAD65. In the focal `151 TH Prkcd Grin2c Glut` group, `Gad2` CRISPR yielded `n_degs = 0`, with the best FDR equal to 1.0 despite 178 matched perturbed nuclei. Even in `052 Pvalb Gaba`, a canonical inhibitory comparator, `Gad2` produced only its own transcript as an FDR 0.05 hit; no downstream transcriptional state accompanied the edit.

The same focal-cell null held for mechanistically adjacent presynaptic GABA perturbations: `Slc32a1` for vesicular GABA loading, `Slc6a1` for GABA uptake, and `Abat` for GABA degradation all had `n_degs = 0`. In `052 Pvalb Gaba`, `Slc32a1`, `Slc6a1`, and `Abat` likewise had one significant self or near-self event each at FDR 0.05, showing target engagement in a better-matched inhibitory class without a broad transcriptional response.

Upstream identity regulators gave the same boundary. `Dlx6` was null in the focal group and, according to the same-experiment Distributed Agents corpus, all-null across measured groups after this P16 mosaic coding perturbation. `Arx` was also null in `151 TH Prkcd Grin2c Glut`; its limited same-experiment response was confined to inhibitory neuron groups. These observations argue that a postmitotic acute perturbation of one GABAergic identity or synthesis gene did not convert the focal glutamatergic state into an FDR-detectable alternative transcriptome.

The sparse nonzero GABA-A receptor signatures (`Gabrb2`, `Gabrd`, `Gabrg2`, `Gabra1`) do not override that conclusion. They point to a local postsynaptic receptor effect in `Prkcd/Grin2c` glutamatergic cells, whereas `Gad1` is presynaptic and biosynthetic. Losing GAD67 in a `Glut` cell group that lacks a focal `Gad2` response is more analogous to the measured `Gad2`/`Slc32a1`/`Slc6a1` nulls than to a receptor subunit knockout.

**Prediction:** `Gad1` should be an exact zero in the focal endpoint: `predicted_n_degs = 0`.

## Limits

The prediction is still an extrapolation because `Gad1` itself was held out and no direct `Gad1` target row was available. `Gad1` and `Gad2` are close but not redundant: GAD67 and GAD65 have different localization and regulation, so the `Gad2` result is a strong analog but not a biochemical identity. The perturbation is also sparse, acute CRISPR in postnatal neurons with partial mRNA knockdown; it should not be conflated with germline Gad67 loss, which has severe developmental GABA phenotypes. Finally, a zero prediction means no genes pass this assay's single-nucleus Wilcoxon/BH threshold; it does not imply that GAD67 has no physiological role in GABAergic neurons.
