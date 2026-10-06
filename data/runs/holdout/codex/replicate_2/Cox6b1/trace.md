# Cox6b1 direct DEG-count forecast

## Target and endpoint

- Target from the declared one-row manifest: `Cox6b1`.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- The selected same-experiment corpus has no `Cox6b1` target Findings or Claims, and the training count table does not contain `Cox6b1`, so the forecast below uses the Cox6b1 biology bundle plus non-Cox6b1 training measurements.

## Biology that mattered

The Cox6b1 bundle identifies Cox6b1 as a nuclear-encoded cytochrome-c-oxidase, complex-IV, subunit whose operative material is already installed in mitochondrial complex IV by the P16 perturbation. The functional-stock card judged Cox6b1 stock likely substantially depleted by P37-P44 because new subunit supply should stop and COX6B1 is in a shorter-lived primary-neuron mitochondrial-protein class, but it also preserved uncertainty from pre-existing complex IV and a supercomplex-stabilized tail.

Exact target reach supports that the gene is measurable but not abundant in the focal class: non-target `151 TH Prkcd Grin2c Glut` nuclei had `Cox6b1` expression in 9,769 of 23,679 nuclei, `41.256%`, with mean raw UMI `0.591` and mean log1p CP10K `0.245`. That is enough for possible self-transcript detection, but not a reason by itself to expect a large downstream nuclear RNA response.

## Training measurements

The full `151 TH Prkcd Grin2c Glut` training count table is sparse: 1,205 of 1,674 perturbations have `n_degs = 0`; the median is 0, the 75th percentile is 1, and the 90th percentile is 2. I therefore treated "severe mitochondrial biology" as insufficient unless nearby measured respiratory-chain perturbations broke out of that null background.

The direct complex-IV and adjacent OXPHOS analogs did not break out:

| target | `151` `n_degs` |
|---|---:|
| `Coa8` | 0 |
| `Cox11` | 0 |
| `Cox4i1` | 0 |
| `Cox5a` | 1 |
| `Cox6a1` | 0 |
| `Cox7b` | 0 |
| `Cox8a` | 0 |
| `Ndufa4` | 1 |
| `Ndufs4` | 0 |
| `Uqcrfs1` | 0 |
| `Uqcrc2` | 1 |
| `Timmdc1` | 0 |
| `Opa1` | 37 |

Direct Parquet rows showed that the singleton cases in this set were self-transcript hits, not broad stress responses: `Cox5a` contributed only `Cox5a`, `Ndufa4` only `Ndufa4`, and `Uqcrc2` only `Uqcrc2` at FDR < 0.05 in `151`. `Opa1` was the exception, with a 37-gene amino-acid/ISR-like program, so I used it as a boundary showing that the assay could detect mitochondrial stress but did not use it as a scale donor for an individual complex-IV structural subunit.

Packaged report Findings, as a same-experiment interpretation layer over those rows, matched the direct measurements: Cox4i1, Cox5a, Cox6a1, Cox11, Coa8, Ndufa4, Ndufs4, and Uqcrfs1 were reported as flat or uncoupled from canonical ATF4/ISR, UPRmt, redox, mitophagy, or OXPHOS-compensation programs rather than as a recurrent complex-IV stress module.

I also profiled the 13-node OXPHOS cohort above in the declared Parquet restricted to `151 TH Prkcd Grin2c Glut`. Nine nodes had no significant features, three had only 1-9 significant features, and only `Opa1` was in the 10-49 bucket. The cohort diagnostic had near-zero positive-tail sharing across all 78 pairs, with mean positive top-tail overlap coefficient `0.037`, reinforcing that these perturbations did not form a shared induced response whose scale should be transferred to Cox6b1.

## Synthesis

Cox6b1 is a plausible real complex-IV perturbation by harvest, so I did not score it as a failed edit or as biologically irrelevant. The decisive quantitative point, though, is that the measured structural and assembly perturbations around complex IV were almost all null in this exact cell class and mostly differed only in whether the perturbed transcript itself crossed FDR. The expected downstream count is therefore approximately zero, with a one-gene self hit as the main upward risk. Because zero was the mode and median of the closest complex-IV set and of the broader curated mitochondrial set, I round the forecast to:

`predicted_n_degs = 0`
