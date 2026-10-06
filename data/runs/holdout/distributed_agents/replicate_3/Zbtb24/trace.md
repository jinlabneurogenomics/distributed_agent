# Reasoning trace

## Question and resolved ambiguities

The requested hidden endpoint is the number of genes with `pvals_adj < 0.05` after each held-out CRISPR loss-of-function perturbation in the focal cell group `151 TH Prkcd Grin2c Glut`. The manifest for this run contains one target:

| target_name |
| --- |
| Zbtb24 |

I interpreted zero as a prediction that no measured coding gene will pass the Scanpy Wilcoxon Benjamini-Hochberg cutoff in this focal group, not as a statement that the guide failed, that Zbtb24 is unimportant, or that methylation/repeat phenotypes would be absent.

## Sources used

- Differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Focal-cell training endpoint CSV: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Requested-target manifest: `[local file: 265_Zbtb24.csv]`.
- Distributed Agents same-experiment corpus: `perturbai-july-260713-sourceguard-1773-v1`. It had no direct `Zbtb24` target card, but did contain curated findings for relevant training perturbations including `Dnmt3a`, `Mbd2`, `Mecp2`, `Chd4`, `Setdb1`, and `Zbtb7a`.
- Independent literature from NCBI PubMed:
  - de Greef et al. 2011, DOI: `10.1016/j.ajhg.2011.04.018`, identified `ZBTB24` mutations as a cause of ICF2 syndrome.
  - Wu et al. 2016, DOI: `10.1093/hmg/ddw243`, showed that ZBTB24 directly activates `CDCA7` and that Cdca7 was the top down-regulated transcript in Zbtb24-mutant mESCs.
  - Ren et al. 2019, DOI: `10.1093/nar/gkz557`, defined the ZBTB24 DNA-binding motif, found motif instances including the `Cdca7` promoter, and showed ICF missense mutations can abolish sequence-specific DNA binding and `Cdca7` induction.
  - Velasco et al. 2018, DOI: `10.1093/hmg/ddy130`, compared ICF methylomes and separated the heterochromatin-biased methylation defects downstream of `ZBTB24`, `CDCA7`, and `HELLS` from the `DNMT3B` subtype.
  - Unoki et al. 2020, DOI: `10.1038/s41598-020-74636-2`, implicated the CDCA7/HELLS complex in recruitment of DNMT1/UHRF1 and suppression of DNA:RNA hybrids at pericentromeric repeats.
  - Unoki 2021, DOI: `10.1111/gtc.12850`, reviewed the ZBTB24-CDCA7-HELLS arm as a chromatin-remodeling route into maintenance DNA methylation and chromosome stability.

## Dataset calibration

I first restricted the DE parquet to `151 TH Prkcd Grin2c Glut`. That focal slice contains:

| quantity | value |
| --- | ---: |
| training perturbations | 1,674 |
| measured genes per perturbation | 17,259 |
| focal DE rows | 28,891,566 |
| total significant focal rows | 23,526 |

The observed endpoint distribution in the training CSV is very sparse:

| statistic | `n_degs` |
| --- | ---: |
| mean | 14.1 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| max | 2,677 |

Only 469 of 1,674 training perturbations had any FDR-significant genes in the focal group. This made the zero/nonzero decision a real part of the prediction rather than a rounding detail.

## Signature computations

I used training counts to identify in-assay analogs, then inspected their focal signatures in the parquet. Raw whole-vector log-fold-change correlations were misleading because all candidate vectors, even zero-DEG vectors, were positively correlated around `r = 0.6`. I therefore computed a feature-centered vector

`centered_lfc(gene, target) = logfoldchanges(gene, target) - mean_over_all_1674_targets(logfoldchanges(gene, target))`

for the 17,259 measured genes in the focal group before comparing candidate signatures. The important centered correlations were all near zero:

| pair | centered Pearson `r` | raw Pearson `r` |
| --- | ---: | ---: |
| `Zbtb7a` vs `Chd4` | 0.024 | 0.641 |
| `Zbtb7a` vs `Setdb1` | -0.030 | 0.627 |
| `Chd4` vs `Setdb1` | 0.000 | 0.651 |
| `Setdb1` vs `Mecp2` | 0.020 | 0.675 |
| `Dnmt3a` vs `Mbd2` | 0.005 | 0.669 |

The FDR-tail overlap agreed with the centered-vector result. `Setdb1` and `Chd4` shared only four FDR genes in this focal group (`Abhd12b`, `Ddo`, `Msra`, `Smtn`); `Setdb1` and `Zbtb7a` shared only `Smtn`; `Setdb1` and `Mecp2` shared only `Ptprm`. `Zbtb7a` and `Chd4` shared 34 FDR genes, but they were both larger, mechanistically distinct responses and still had near-zero centered correlation with nine significant direction conflicts.

## Zbtb24-specific analogs and boundaries

The exact axis downstream of ZBTB24 is poorly represented among the non-held-out perturbations. `Cdca7`, `Hells`, `Uhrf1`, `Dnmt1`, and `Dnmt3b` were absent from the focal training-count CSV, so no same-complex perturbation could be used directly.

| training perturbation | focal `n_degs` | expression-pattern evidence | relevance to `Zbtb24` |
| --- | ---: | --- | --- |
| `Dnmt3a` | 0 | Zero FDR genes in 151; the Distributed Agents corpus reports zero downstream FDR genes in every measured neuronal group and no meaningful positive or negative signature neighbor. | A DNA-methylation writer, but mostly a boundary: acute postnatal loss of a cumulative methylation enzyme was transcriptionally buffered. That supports caution about predicting a large mRNA response from `Zbtb24`'s methylation biology. |
| `Mbd2`, `Mbd5`, `Mecp2` | 0, 0, 16 | `Mecp2` had a small response; `Mbd2` and `Mbd5` were zero. The same-experiment corpus explicitly found that `Mecp2`, `Mbd2`, `Mbd5`, and `Dnmt3a` did not collapse into one methyl-CpG reader/writer signature. | Methyl-CpG readers are downstream of methylated DNA rather than the ZBTB24-CDCA7-HELLS maintenance machinery. Their low counts argue against a broad shared methylation-loss RNA state over this assay window. |
| `Setdb1` | 22 | Active but narrow: 17 up and 5 down FDR genes. The significant up genes included `Tasor`, `Atf7ip`, and clustered protocadherins, and overlapped `Chd4` at only four genes. | Best represented repeat/heterochromatin-repression proxy, but the signature was H3K9/HUSH/protocadherin-biased, not a generic ICF-like DNA-methylation program. I used it as an upper bound for a low, nonzero chromatin-maintenance response. |
| `Chd4` | 100 | The NuRD ATPase had a focal thalamic response with channel, calcium, matrix/adhesion, and redox branches. Centered `Chd4`-`Setdb1` correlation was approximately zero. | A chromatin remodeler and methylation-adjacent counterexample showing the focal cell group can respond to nuclear perturbations, but mechanistically distant from ZBTB24 because CHD4 is a NuRD ATPase rather than the CDCA7/HELLS maintenance axis. |
| `Zbtb16`, `Zbtb18`, `Zbtb20`, `Zbtb38` | 0, 5, 0, 1 | Most represented ZBTB-family losses were silent or nearly silent in 151. `Zbtb18` had only five FDR genes, including its own transcript and `Endou`. | Family membership alone did not imply a broad postnatal neuronal signature; these are better low-count boundaries than positive analogs. |
| `Zbtb7a` | 841 | Very broad, with endomembrane/lysosome, GPCR-sorting, glycolytic, and neuropeptide components in the Distributed Agents corpus. Its nearest FDR-backed neighbors were UFMylation/proteostasis perturbations rather than ZBTB-family genes or chromatin methylation factors. | Same BTB-zinc-finger superfamily, but a poor mechanistic analog. I treated this as a counterexample showing that a ZBTB factor can be highly active in 151, not as evidence that `Zbtb24` should get a high count. |

## Biological rationale and prediction

ZBTB24 is a sequence-specific transcription factor whose loss causes ICF2 syndrome. The best-established molecular route is activation of `CDCA7`; CDCA7 then works with the HELLS SNF2 ATPase in an ICF2/3/4 heterochromatin and DNA-methylation maintenance pathway. That places ZBTB24 near DNA methylation and pericentromeric/repetitive heterochromatin rather than near a fast membrane-trafficking or proteostasis response like the large `Zbtb7a` signature.

In this experiment, the most mechanistically relevant assayed methylation nodes were quiescent: `Dnmt3a`, `Mbd2`, and `Mbd5` all had `n_degs = 0`, and `Mecp2` had only 16. The nearest heterochromatin/repressive proxy, `Setdb1`, did respond, but only with 22 genes and with a clustered-protocadherin/HUSH pattern that was not shared by other chromatin regulators. The larger `Chd4` and `Zbtb7a` signatures look like different biology and therefore set only a loose detectability control, not a count prior for `Zbtb24`.

I therefore predicted that acute, sparse P16 `Zbtb24` loss would usually leave the 151 thalamic nuclear mRNA surface below the FDR threshold. If `Zbtb24` depletion reduced `Cdca7` enough in these postmitotic neurons, a handful of genes could pass; however, the exact `Cdca7`/`Hells` arm was absent from training, the RNA readout did not quantify repetitive elements or DNA methylation, and the focal response could be delayed or buffered on a 3-4 week timescale. My final point estimate is zero DEGs.

| target | predicted `n_degs` |
| --- | ---: |
| `Zbtb24` | 0 |

## Limits

- The strongest limitation is missing exact analogs: `Cdca7`, `Hells`, `Uhrf1`, `Dnmt1`, and `Dnmt3b` were not in the training endpoint table.
- DNA methylation, pericentromeric repeats, IAP/ERV transcripts, R-loops, and chromosomal instability were not the measured endpoint. A genuine ZBTB24 epigenomic phenotype could be invisible to the supplied coding-gene Wilcoxon count.
- `Dnmt3a` is a de novo/mCH methyltransferase rather than an ICF2/3/4 maintenance factor, and `Setdb1` is an H3K9 writer; both are imperfect boundaries.
- The perturbation is acute, mosaic, and postmitotic. Germline ICF disease and embryonic Zbtb24-mutant stem-cell phenotypes are useful for mechanism but likely overstate the transcriptional impact expected in P37-P44 neurons after partial AAV-CRISPR loss.
- Because the exact axis was not observed, the difference between zero and a very small count is extrapolative. I chose zero because the closest available methylation/ZBTB comparators were mostly at zero and the focal training set is strongly zero-inflated.
