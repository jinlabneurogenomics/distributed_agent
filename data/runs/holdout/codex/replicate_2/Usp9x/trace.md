# Usp9x n_degs forecast

Target: `Usp9x` in `151 TH Prkcd Grin2c Glut`.

Endpoint to predict: the number of measured genes with Wilcoxon `pvals_adj < 0.05` in the held-out `Usp9x` profile. The held-out `Usp9x` differential-expression rows were not used.

## Inputs used

- Declared biology bundle: `biology_bundles/Usp9x.json`.
- Declared focal-class training counts: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared non-held-out differential-expression Parquet: `training_de_all_cell_groups.parquet`.
- Same-experiment Finding summaries for measured training perturbations. These were used as interpretations of the declared experiment, not as independent replication.

## Quantitative anchor points

The focal count table is highly zero-inflated:

- `1674` training targets total.
- `1205` have `n_degs = 0`.
- median `n_degs = 0`; 75th percentile `= 1`; 90th percentile `= 2`; 95th percentile `= 18`.

The most relevant measured perturbations did not support a global proteasome-scale estimate:

| training target | focal `n_degs` | interpretation for Usp9x |
| --- | ---: | --- |
| `Usp48` | 10 | closest USP-family anchor; compact and specific 151 TH response |
| `Bap1` | 16 | another deubiquitinase, but chromatin/PR-DUB rather than USP9X-like substrate deubiquitinase |
| `Uchl1` | 1 | neuronal DUB with essentially no broad RNA response |
| `Otud7a` | 0 | neuronal DUB/synaptic target with no focal response |
| `Cyld` | 0 | DUB with no robust response in the assayed neuronal groups |
| `Vcp` | 2 | proteostasis-adjacent regulator with only two focal DEGs |
| `Shank3` | 2 | USP9X-linked postsynaptic substrate axis was transcriptionally tiny |
| `Ankrd11` | 20 | neurodevelopmental/synaptic chromatin regulator; upper local-scale reference |
| `Huwe1` | 158 | much broader E3-ligase response, kept as an upper biological contrast rather than a direct scale donor |
| `Psmb4` | 742 | core proteasome lesion with a pan-proteostasis program, not a single-DUB analogue |
| `Psmc1` | 430 | core proteasome lesion, not a single-DUB analogue |
| `Ufc1` | 572 | core ubiquitin-fold-conjugation machinery, not a USP9X-scale analogue |
| `Uba5` | 2677 | core ubiquitin-fold-activation machinery, not a USP9X-scale analogue |

Parquet checks across cell classes supported the same separation. `Usp48` was 151-specific in the declared measurements: 10 FDR<0.05 genes in `151 TH Prkcd Grin2c Glut` and 0 in every other queried group. `Bap1` had a small restricted surface: 16 genes in `151 TH Prkcd Grin2c Glut`, 4 in `052 Pvalb Gaba`, and none in the other queried groups. By contrast, `Psmb4` and `Psmc1` produced hundreds to thousands of DEGs across many classes, matching their core proteasome role and making them poor magnitude donors for a substrate-selective USP9X knockout.

## Biology interpretation

The Usp9x bundle argues that the perturbation should be functionally realized in this assay. Usp9x RNA is directly observed in `151 TH Prkcd Grin2c Glut` non-target cells with 93.79% of nuclei expressing it, and the measured USP9X protein half-lives of about 31-39 hours put a 21-28 day P16-to-harvest interval many half-lives beyond the starting enzyme pool. USP9X is a renewable deubiquitinase acting on selected neuronal substrates, and the declared card judged pre-edit stock likely substantially depleted by harvest.

That makes an exact zero less likely than for a random target, but the card's positive biology is not a reason to import the large proteasome count scale. The direct phenotypes for Usp9x come from developmental forebrain/neural conditional models rather than acute juvenile thalamic perturbation; USP9X loss perturbs substrate ubiquitination and synaptic scaffold proteostasis, which can remain mostly post-translational; and measured training perturbations along DUB, TGF-beta, ankyrin, and postsynaptic scaffold axes were quiet or single-digit in this focal class. The same-experiment corpus summaries were concordant: `Usp48` and `Bap1` had compact thalamic responses, while `Uchl1`, `Cyld`, `Otud7a`, `Vcp`, and `Shank3` lacked broad DUB/synaptic/proteostasis transcriptional programs.

## Forecast

I forecast a real but compact focal response, slightly above the 10-gene `Usp48` anchor because Usp9x is well expressed and should deplete by harvest, but below the `Bap1`/`Ankrd11` 16-20 gene range because the closest USP and substrate-axis observations are small and the developmental forebrain phenotypes are only partial context matches.

Point prediction: `12`.
