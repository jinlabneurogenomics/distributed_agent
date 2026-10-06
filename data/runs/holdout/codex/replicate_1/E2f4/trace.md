# Evidence and reasoning

## Target and endpoint

- Target manifest: `E2f4`.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, defined as the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- The same-experiment Parquet and corpus were treated as different representations of the same Perturb-seq experiment, not as independent replication. I did not query or use an E2f4 same-experiment DE profile, E2f4 report, or any withheld E2f4 outcome.

## Training count table

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` has 1,674 training targets and does not contain E2f4.

Its distribution is strongly zero-inflated:

| quantity | value |
|---|---:|
| targets with 0 DEGs | 1,205 |
| targets with 1 DEG | 276 |
| targets with 2 DEGs | 31 |
| fraction with <=2 DEGs | 0.903 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |

The closest directly measured E2F/DP training perturbations are all at the floor or near it in the focal class:

| training target | focal 151-class `n_degs` |
|---|---:|
| E2f1 | 0 |
| E2f5 | 0 |
| Tfdp1 | 2 |
| Tfdp2 | 0 |

Adjacent cell-cycle/MYC/E2F-side comparators were also flat or tiny in the focal count table: `Cdkn2a=0`, `Myc=0`, `Mycn=0`, `Trp53=0`, `Mnt=0`, `Mlxip=0`, `Mga=2`, and `Foxk2=0`.

## Row-level Parquet checks

I checked the declared training DE Parquet directly for `151 TH Prkcd Grin2c Glut` and the four measured E2F/DP analogs. Each analog had 17,259 measured rows in this class:

| gene_target | rows | `pvals_adj < 0.05` | minimum `pvals_adj` |
|---|---:|---:|---:|
| E2f1 | 17,259 | 0 | 1.000000 |
| E2f5 | 17,259 | 0 | 1.000000 |
| Tfdp1 | 17,259 | 2 | 0.011383 |
| Tfdp2 | 17,259 | 0 | 1.000000 |

The two Tfdp1 151-class DE genes were `Cntrob` and `Dcaf15`; the next Tfdp1 gene had adjusted `p = 0.118`. Across all assayed groups for these four E2F/DP targets, only Tfdp1 had any gene passing either `pvals_adj < 0.05` or `pvals_adj < 0.10`, and those were exactly the two 151-class genes.

## Packaged same-experiment interpretation

The same-experiment Findings for E2f1, E2f5, Tfdp1, and Tfdp2 support interpreting the measured counts as a buffered postmitotic E2F/DP surface rather than as four unrelated noisy nulls:

- The high-confidence Claim over E2f1, E2f5, Tfdp1, and Tfdp2 states that single perturbations of represented E2F/DP family members do not engage a coordinated canonical G1/S replication, mitotic, or apoptotic nuclear transcriptomic program in settled postnatal neurons.
- E2f5 F002 reports absent canonical E2F/DREAM G1/S derepression after E2f5 perturbation and notes that E2f4 and pocket-protein perturbations were not directly represented there.
- Tfdp1 F002/F003 report that its two-gene thalamic response is not a canonical E2F/DP G1-S program and is not phenocopied by Tfdp2, E2f1, or E2f5.
- E2f1 and Tfdp2 are reported as broadly FDR-null, including absence of canonical G1/S and DNA-replication output.

## E2f4 biology bundle

The canonical E2f4 biology bundle gives two opposing bearings:

- Upward / reach-bearing: E2f4 is available in the exact focal population, with 16,619 of 23,679 non-target nuclei expressing it, `70.18%` expressing, mean log1p(CP10K) `0.528`, mean CP10K `0.855`, and pseudobulk CPM `84.4`. Low focal reach therefore should not be the dominant reason to call zero.
- Downward / buffering-bearing: E2F4 functions as a DP- and pocket-protein-associated transcription factor; the functional-stock card calls the expected P37-P44 state `partially_depleted_or_leading_edge`, because free E2F4 should turn over after editing but p107/p130-bound pools can be stabilized. The source card also documents E2F5 overlap outside this neuronal context, and the observability card marks postnatal neuronal requirement, latency, and thalamic compensation as unresolved.

## Numeric synthesis

The count distribution alone has a zero median and a 90th percentile of only 2, so a training target needs a strong reason to leave the floor. E2f4 is not a generic high-yield nuclear essential comparable to the large 151-class tails such as `Uba5`, `Tpr`, or `Sin3a`; its closest measured E2F/DP paralog and partner perturbations are 0, 0, 0, and 2 DEGs, with no hidden near-threshold tails for the zeros and no pan-neuronal E2F/DP module outside Tfdp1's two focal genes.

The exact E2f4 expression prevents demoting the target all the way to a technical no-reach null, but the postmitotic E2F/DP evidence and the partially persistent p107/p130-bound stock make the most likely outcome another floor or near-floor focal signature. Because the closest measured analog set has median 0, because E2f5 is the direct E2f4-overlap paralog and is completely FDR-null, and because Tfdp1's two hits do not mark a general E2F program, I assign the integer point forecast:

`predicted_n_degs = 0`
