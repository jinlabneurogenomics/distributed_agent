## Target and endpoint

- Target: `Zbtb42`
- Forecasted endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, defined as the number of measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05`.
- Point prediction: `0`

## Evidence used

### Zbtb42 biology-only target bundle

Provenance: `[local file: Zbtb42.json]`, schema `expected-transcript-impact-agent-bundle-v1`, bundle sha256 `72358d2b9d737cb56622fb376aa48c25c8f455be541c39b57fc5a4f18d446875`.

- The exact in-assay expression measurement in non-target `151 TH Prkcd Grin2c Glut` nuclei was extremely low:
  - `n_cells_expressing = 31 / 23679`, or `0.13091769078086068%`;
  - `total_target_umi = 33`;
  - `mean_raw_umi = 0.0013936399341188395`;
  - `mean_log1p_cp10k = 0.0006930278972482208`;
  - `pseudobulk_cpm = 0.08734435669051036`.
- ZBTB42 is supported as a soluble nuclear BTB/POZ and C2H2 zinc-finger transcriptional regulator, so a real perturbation could in principle have direct transcriptomic consequences.
- The target-specific acute realization prior is weak. The bundle found no ZBTB42 half-life, chromatin-residence, or clearance measurement, and the broad neuronal-proteome turnover proxy spans less than 1 day to more than 20 days. Because the P16-to-P37/P44 window is 21-28 days, the target card leaves `functional_stock_by_harvest` indeterminate rather than depleted.
- The phenotype prior is also weak for this endpoint: decreased prepulse inhibition in homozygous constitutive mutants is a nervous-system phenotype, but it is neither assigned to 151 thalamic glutamatergic neurons nor timed after acute postnatal loss.

### Training counts in the focal population

Provenance: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`, declared visible training table with `Zbtb42` held out.

- The visible `151 TH Prkcd Grin2c Glut` endpoint is zero-heavy: among 1,674 training targets the median count is `0`, the 75th percentile is `1`, the 90th percentile is `2`, and only 106/1,674 targets have at least 10 DEGs.
- Within measured ZBTB-family perturbations:
  - `Zbtb10`, `Zbtb16`, `Zbtb20`, and `Zbtb21`: `0` focal DEGs;
  - `Zbtb38`: `1` focal DEG;
  - `Zbtb18`: `5` focal DEGs;
  - `Zbtb7a`: `841` focal DEGs.
- The one large ZBTB outlier, `Zbtb7a`, is not a good scale donor for Zbtb42. In the same-experiment corpus release `perturbai-july-260713-sourceguard-1773-v1`, the visible Zbtb7a report described a broad, graded postmitotic neuronal response across 22/23 measured groups, an endomembrane/lysosome and neurosecretory state, and nearest FDR-backed positive signatures with UFMylation/proteostasis perturbations rather than ZBTB paralogs. The same Zbtb7a report explicitly noted that canonical fetal-globin partners including `Bcl11a` and `Bcl11b` were essentially flat in neurons. This supports treating Zbtb7a as a distinct visible program, not as the default BTB-ZF prior.
- Corpus Findings for visible `Zbtb10`, `Zbtb16`, `Zbtb20`, and `Zbtb21` summarized genome-wide or all-neuronal-class flat responses; `Zbtb38` was sparse with a small thalamic up-signature; and `Zbtb18` had a narrow `Pxdn`/`Endou` extracellular-matrix marker response. Those reports are the semantic layer over the same Perturb-seq experiment, not an independent replicate.

### Training rows from the expression parquet

Provenance: `[local file: training_de_all_cell_groups.parquet]`, declared target-free training DE parquet.

For the focal `151 TH Prkcd Grin2c Glut` group, direct rows in the parquet matched the count table for selected visible BTB/NuRD-family comparators:

| gene_target | focal DEGs at BH < 0.05 | matched perturbed nuclei |
| --- | ---: | ---: |
| `Bcl11a` | 0 | 203 |
| `Bcl11b` | 0 | 206 |
| `Zbtb10` | 0 | 187 |
| `Zbtb16` | 0 | 180 |
| `Zbtb18` | 5 | 208 |
| `Zbtb20` | 0 | 185 |
| `Zbtb21` | 0 | 137 |
| `Zbtb38` | 1 | 199 |
| `Zbtb7a` | 841 | 282 |

The small nonzero ZBTB-family signatures were tiny: `Zbtb38` had only `Msra` significant in the focal group, while `Zbtb18` had `Endou`, `Pxdn`, `Clstn2`, `Man2a2`, and the `Zbtb18` transcript itself.

## Synthesis

I placed most weight on exact focal expression reach, because only 0.13% of matched non-target nuclei had detectable Zbtb42 RNA and the target contributed 33 UMIs total across 23,679 nuclei. A P16 edit of a gene this rarely expressed at the assayed P37-P44 state has little opportunity to create a population-level Wilcoxon signal in the aggregate 151 thalamic class unless ZBTB42 had an earlier postnatal effect that persisted broadly; the declared card found no matched evidence for that scenario and could not resolve residual protein stock at harvest.

The focal training distribution reinforced a zero prediction. The endpoint is sparse overall, and the visible ZBTB-family counts are mostly `0` with only `1` to `5` genes for the small responders. I did not transfer the 841-gene `Zbtb7a` burden because its measured state is a broad stress/endomembrane/proteostasis-like neuronal response rather than a generic BTB-ZF perturbation magnitude.

The resulting forecast is therefore the modal and biologically most compatible count, `0`. The main uncertainty is that Zbtb42 is still a nuclear transcriptional regulator with a constitutive nervous-system phenotype, so a small persistent postnatal program of one or a few genes would not be surprising; however, the exact target reach and the flat visible ZBTB comparators make a larger focal response unlikely.
