# Acox1 in 151 TH Prkcd Grin2c Glut

## Declared target and assay

The one-row holdout manifest names `Acox1`. The requested scalar is `n_degs` in `151 TH Prkcd Grin2c Glut`, counting measured genes with BH-adjusted Wilcoxon `p < 0.05`.

The prediction-safe `Acox1` biology bundle exposes focal-class target reach but no held-out outcome. In non-target `151 TH Prkcd Grin2c Glut` nuclei, `Acox1` was detected in 16,272 of 23,679 cells, 68.719%, with mean CP10k 0.827 and pseudobulk CPM 82.665. The functional-stock card classifies harvest-time ACOX1 capacity as `likely_substantially_depleted`: a disruptive edit stops new soluble peroxisomal ACOX1 supply, and 21-28 days should be enough for ordinary soluble protein turnover. The same bundle keeps acute transcriptional observability unresolved, because mouse knockout evidence is systemic/hepatic, the human biallelic neural phenotype is constitutional and chronic, ACOX1-specific neuronal turnover is not measured, and related Acox2/Acox3 enzymes are only partial biochemical relatives rather than a demonstrated thalamic compensation mechanism.

## Quantitative training evidence

The declared focal-class training count table contains 1,674 visible targets. It is zero-inflated: 1,205 targets have `n_degs = 0`, the median is 0, the 75th percentile is 1, the 90th percentile is 2, and the mean 14.05 is driven by a small high-burden tail.

The visible peroxisomal / lipid-catabolic comparators nearest the ACOX1 mechanism all sat at the bottom of that distribution in `151 TH`:

| target | focal `n_degs` |
|---|---:|
| `Abcd3` | 0 |
| `Acbd5` | 0 |
| `Aco2` | 0 |
| `Hsd17b4` | 0 |
| `Pex1` | 0 |
| `Agps` | 1 |
| `Acsl4` | 1 |
| `Cpt1c` | 1 |
| `Pex14` | 1 |
| `Far1` | 2 |

Direct Parquet inspection in `151 TH Prkcd Grin2c Glut` showed that the singleton calls for `Acsl4`, `Cpt1c`, and `Pex14` were self-transcript rows only:

| perturbation | significant focal rows at FDR < 0.05 |
|---|---|
| `Acsl4` | `Acsl4` |
| `Cpt1c` | `Cpt1c` |
| `Pex14` | `Pex14` |

`Agps` had one trans call, `Dhcr24`; `Far1` had its self row plus `Tial1`. Thus the ACOX1-like beta-oxidation/import/transport set provides no observed downstream focal-class module. Across all focal-class training self rows, 319 of 1,642 self transcripts were significant, and 237 of the 276 singleton `n_degs = 1` cases were just a significant self row, so a count of one would mostly reflect detectable target-transcript loss rather than a downstream state.

The same conclusion was present in the selected same-experiment corpus. Claim `claim:a3b54f2b17cb911aec15` states that represented peroxisome-linked perturbations do not converge on a shared acute neuronal transcriptomic module and are predominantly flat, sparse, or target-specific. The Hsd17b4 pathway-uncoupling Finding `Hsd17b4:F002` directly compared `Abcd3`, `Acbd5`, `Pex1`, and `Pex14` and found no phenocopy; the Pex14 contrast Finding `Pex14:F003` likewise found no Pex14-like state among represented peroxisome-linked comparators.

I also ran symmetric profile comparisons over the focal-class log-fold-change rows for the ACOX1-nearest lipid/peroxisome cohort and the exact Claim cohort. The ACOX1-nearest cohort had 5 of 8 targets with no FDR-significant feature and the Claim cohort had 4 of 7 with none; median positive top-tail overlap was only 0.075 in both, and significant-program overlap was effectively absent. Those profile diagnostics supported treating the sparse `Agps`/`Far1` calls as small target-specific exceptions, not as evidence for a broad hidden peroxisomal state that should transfer to `Acox1`.

## Forecast

I predict no focal-class downstream genes for `Acox1`. The exact baseline expression makes a self-transcript row possible, but self-knockdown is stochastic in this assay and the closest visible pathway genes split between no self call and self-only singleton calls. With beta-oxidation neighbor `Hsd17b4`, transporter `Abcd3`, tether `Acbd5`, and import factor `Pex1` all at zero, and with no coherent peroxisome program in the Parquet or corpus, the most likely count is the bottom bin:

`predicted_n_degs = 0`
