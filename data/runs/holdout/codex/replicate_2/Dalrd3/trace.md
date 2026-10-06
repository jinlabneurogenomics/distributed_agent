# Dalrd3 DEG-count forecast

Target and endpoint:

- Target: `Dalrd3`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`

## Biological reach

The declared biology bundle supports target reach but not a large endpoint by
itself. `Dalrd3` was detected in the matched non-target nuclei for the focal
class in 20,282 / 23,679 nuclei, with 85.65% of nuclei expressing the feature,
mean raw UMI 2.28, and pseudobulk CPM 142.63. Thus the target transcript was
available in the assayed thalamic neurons.

Functionally, DALRD3 is the substrate-targeting partner that routes selected
arginine tRNAs to METTL2 for m3C32 modification. The card adjudicated the
P16-to-P37/P44 perturbation window as `likely_substantially_depleted`: a CRISPR
edit should stop new DALRD3 production, residual targeting protein should fall
over a 21-28 day window, and newly made tRNA carriers should increasingly lack
the DALRD3-dependent mark. The card also leaves endpoint strength uncertain:
target-specific neuronal turnover is missing, mouse postnatal neural
loss-of-function evidence was not found, and the human phenotype evidence is
germline/developmental rather than an acute juvenile neuronal transcriptome.

## Training perturbations used

The count table for the same focal class is sparse: 1,205 / 1,674 training
targets had zero DEGs, the median was 0, the 75th percentile was 1, the 90th
percentile was 2, and only 43 training targets had at least 100 DEGs. A
nonzero molecular lesion therefore is not enough to predict a large
BH-significant nuclear-RNA response.

I treated the nearest interpretable measured class as tRNA-modification and
translation-adjacent perturbations:

| training target | `151 TH Prkcd Grin2c Glut` `n_degs` |
|---|---:|
| `Alkbh8` | 0 |
| `Cdkal1` | 0 |
| `Nsun2` | 0 |
| `Trmt1` | 0 |
| `Fars2` | 0 |
| `Lars2` | 0 |
| `Rars2` | 0 |
| `Eef2` | 9 |
| `Elp2` | 150 |
| `Elp1` | 645 |

The direct Parquet check for `Alkbh8`, `Nsun2`, and `Trmt1` in the focal class
confirmed that each had 17,259 measured genes and zero BH<0.05 hits, so their
zeros in the count table were not missing profiles. The packaged
same-experiment Findings further reported that `Alkbh8` had zero downstream
FDR<0.10 genes across the recovered neuronal panel, `Nsun2` had no significant
downstream mRNA signature in any measured neuronal group, `Trmt1` was nearly
flat with only three downstream FDR<0.10 gene-by-cell-group hits and no focal
class program, and `Cdkal1` was also almost transcriptionally silent.

I downweighted `Elp1` and `Elp2` despite their large responses. Same-experiment
Finding `Elp1:F003` explicitly separates the Elongator branch from a generic
tRNA-modification-null state: acute `Alkbh8`, `Nsun2`, and `Trmt1` loss did not
reproduce the `Elp1`/`Elp2` thalamic ATF4/amino-acid integrated-stress
response, and the Claim contribution including `Cdkal1` makes the same
Elongator-specific distinction. `Dalrd3` is a tRNA-Arg m3C32 targeting factor,
not an Elongator-core component or a U34 Elongator-pathway target, so the silent
direct methylation/demethylation perturbations were a closer endpoint prior
than the high-count Elongator ISR state.

## Point forecast

`Dalrd3` is likely engaged by the screen, but its closest assayed non-Elongator
tRNA-modification comparators were focal-class nulls. I therefore predicted
the modal sparse outcome:

```tsv
target_name	predicted_n_degs
Dalrd3	0
```
