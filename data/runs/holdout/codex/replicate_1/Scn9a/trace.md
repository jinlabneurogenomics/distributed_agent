# Scn9a DEG-count forecast

## Target and endpoint

- Target: `Scn9a`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the count of measured genes with Wilcoxon BH-adjusted `p < 0.05`
- Forecast: `0`

## Evidence used

### Declared Scn9a biology bundle

The target bundle supports functional realization but only narrow in-assay
reach. Scn9a encodes Nav1.7, a pore-forming voltage-gated sodium-channel alpha
subunit. Adult mouse neural deletion data indicate that Nav1.7 protein decays
over weeks after intact transcript is removed, so P16 disruption can plausibly
substantially deplete channel stock by the P37-P44 harvest.

The same bundle makes the dilution risk substantial in this specific endpoint:

- exact feature availability for `Scn9a` in `151 TH Prkcd Grin2c Glut`: present
- non-target nuclei in this class: `23679`
- nuclei detectably expressing `Scn9a`: `2753`
- detectable expressing fraction: `11.6263%`
- mean raw UMI for `Scn9a`: `0.1606`
- mean log1p(CP10K): `0.0749`

Thus the operation is credible in Nav1.7-positive cells, but the screen measures
a broad recovered thalamic glutamatergic aggregate in which most nuclei do not
detectably express the target.

### Training count table in the matched 151 class

The supplied `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains
1,674 training perturbations and does not include the held-out `Scn9a` row.
It is strongly zero-heavy:

- median `n_degs`: `0`
- 75th percentile: `1`
- 90th percentile: `2`
- zero rows: `1205/1674`

I used the Nav-channel/FHF genes represented in the same-experiment Scn3a/Nav
corpus claim as the closest operation-level comparators and read their matched
151 counts:

| training target | n_degs in 151 |
| --- | ---: |
| `Scn1a` | 1 |
| `Scn1b` | 2 |
| `Scn2a` | 1 |
| `Scn3a` | 0 |
| `Scn8a` | 1 |
| `Fgf12` | 0 |
| `Fgf13` | 2 |

This closest cohort has a mean of `1` and a median of `1`, but even that slightly
overstates expected downstream response for `Scn9a`: in the exact Parquet rows
for this cell class, `Scn1a`, `Scn2a`, and `Scn8a` each had only the self-target
transcript below 0.05 FDR; `Scn3a` and `Fgf12` had no significant feature; and
the two-count cases were just self plus one isolated marker.

As a broader excitability check, other voltage-channel perturbations in the same
151 table were also mostly silent: `Cacna1a/Cacna1d/Cacna1e`, `Hcn1`,
`Kcna1/Kcna2`, `Kcnb1`, and `Kcnc1` all had zero DEGs; `Hcn2`, `Kcnq2`, and
`Kcnq3` had one DEG each. The larger excitability-channel responses,
`Cacna1g = 12` and `Grin1 = 89`, came from non-Nav channel biology and were not
treated as scale donors for Nav1.7.

### Matched profile comparison

I compared the 151 Wilcoxon-score profiles of
`Scn1a/Scn1b/Scn2a/Scn3a/Scn8a/Fgf12/Fgf13` in the declared Parquet. All 21
pairwise Pearson correlations were near zero, from `-0.0276` to `0.1144`, and
no pair shared a significant positive or negative FDR-level feature. The profile
cohort therefore supports the corpus interpretation that represented Nav-family
and FHF perturbations do not form a shared pan-Nav transcriptional module in
this assay.

### Same-experiment corpus context

The selected same-experiment corpus had no packaged `Scn9a` report, Finding,
Claim, or explicit same-experiment comparator record. It did contain a high
confidence Scn3a/Nav higher-order Claim stating that represented Nav alpha/beta
subunits and FHF modulators produce sparse, target- and cell-context-specific
RNA responses rather than a shared pan-Nav or Nav-complex transcriptional
module. That corpus interpretation was used only as a same-experiment semantic
summary over training profiles, not as independent validation.

## Synthesis

Three bearings determined the integer:

1. Upward: the Scn9a edit is expected to remove a renewable Nav1.7 conductance
   in the subset of target-expressing neurons by harvest.
2. Downward: exact 151 expression reach is low and anatomically restricted, so
   both the self row and any downstream electrophysiology-coupled RNA response
   are strongly diluted in the recovered aggregate.
3. Matched scale: the closest measured Nav/FHF perturbations in 151 sit at
   `0-2` DEGs, with no shared downstream channel-compensation or activity
   module and with most nonzero counts driven by self-target rows.

Because Scn9a should be less visible in the aggregate nuclear RNA endpoint than
the broadly represented self-detectable Nav alpha perturbations, I placed the
point at the lower edge of the Nav comparator range rather than at its median.
