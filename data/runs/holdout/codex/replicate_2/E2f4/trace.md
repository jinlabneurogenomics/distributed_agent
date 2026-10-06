# Direct E2f4 forecast for `151 TH Prkcd Grin2c Glut`

## Declared target and endpoint

- Target manifest row: `E2f4`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05`

I used the declared biology-only `E2f4` bundle, the declared
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table, and bounded Parquet
queries against `training_de_all_cell_groups.parquet`. I did not query the
held-out `E2f4` expression signature or same-experiment `E2f4` report.

## Biology

The exact in-assay expression slice says `E2f4` is reachable in this focal
population: 16,619 of 23,679 non-target nuclei expressed it
(`70.18%`; mean CP10k `0.855`). That removes low target reach as a simple reason
for a null forecast.

The perturbation card points in the opposite, dampening direction. E2F4 is a
DNA-binding DP/p107/p130 transcription-complex component; a disruptive genome
edit should stop new E2F4 supply, but p107/p130-bound E2F4 is stabilized and the
endogenous neuronal residence time of that protected pool is not known. The
functional-stock call was therefore
`partially_depleted_or_leading_edge`, not confident full loss by the P37-P44
harvest.

The phenotype evidence was also displaced from the assay context. The closest
neural loss evidence is embryonic ventral-telencephalon and precursor biology,
while adult selected-region NeuN staining establishes detection rather than a
postnatal thalamic requirement. E2F5 can overlap with E2F4/pocket-protein
function in non-neuronal genetic tests, so the represented `E2f5` perturbation
is a relevant, though incomplete, family anchor.

## Training measurements

The focal count table contains 1,674 training perturbations. Its distribution is
very sparse in this high-yield cell class:

- `1,205 / 1,674` training targets have `0` DEGs.
- The median is `0`; the 75th percentile is `1`; the mean is `14.05`, inflated
  by a small high-response tail.

The most local E2F/DP measurements were quiet:

| training target | n_degs in `151 TH Prkcd Grin2c Glut` |
|---|---:|
| `E2f1` | 0 |
| `E2f5` | 0 |
| `Tfdp1` | 2 |
| `Tfdp2` | 0 |

A direct Parquet check in this same class reproduced those counts. The only
FDR<0.05 genes among the DP targets were the two positive `Tfdp1` genes
`Cntrob` and `Dcaf15`; `E2f1`, `E2f5`, and `Tfdp2` had no significant measured
gene. Broader cell-cycle and transcriptional neighbors in the count table were
also mostly flat in this class: `Cdkn2a`, `Ep300`, `Mnt`, `Myc`, `Mycn`,
`Tfdp2`, and `Smarca4` each had `0`, and `Smarca2` had only its own transcript.

The packaged same-experiment findings agree with the measured anchors but are
not an independent replicate. `E2f5:F002`, `E2f1:F002`, `E2f1:F003`, and
`Tfdp1:F002` interpret the assayed E2F/DP family as lacking a coordinated
canonical G1/S, replication, mitotic, or apoptotic RNA program in postnatal
NeuN-positive neuronal nuclei; `Tfdp1:F003` reports that represented DP/E2F
relatives did not phenocopy the small two-gene `Tfdp1` thalamic response.

## Synthesis

High `E2f4` expression keeps a detectable response biologically possible, and
the P16 edit should deplete at least renewable free E2F4. The counterweights
are stronger for this endpoint: the stock card does not support complete
pocket-complex clearance within 21-28 days, the clearest loss phenotypes are
developmental rather than postnatal thalamic, and single perturbations of the
represented E2F/DP axis are empirically zero or nearly zero in the same
Perturb-seq class.

I therefore centered the forecast below one DEG and rounded to the nearest
non-negative integer:

`predicted_n_degs = 0`
