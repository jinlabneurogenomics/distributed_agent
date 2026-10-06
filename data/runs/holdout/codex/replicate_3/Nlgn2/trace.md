# Nlgn2 n_degs forecast

## Target and endpoint

- Target: `Nlgn2`.
- Cell group: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- Forecast: `1`.

## Evidence used

### Biology bundle

The declared Nlgn2 biology bundle supports real target engagement in the assay
window:

- NLGN2 is a postsynaptic adhesion component that organizes inhibitory
  synaptic transmission.
- In the exact assayed population, `Nlgn2` is detected in 22,782 of 23,679
  matched non-target nuclei, 96.2118%, with mean CP10K 3.0061.
- The expected functional-stock card adjudicates operative NLGN2 as
  `likely_substantially_depleted` by the P37-P44 harvest after a P16 edit:
  synaptic NLGN2 turns over on a days-long scale, and adult conditional loss
  made NLGN2 undetectable after about 2-3 weeks.
- The best matched loss-of-function physiology is thalamic, but it came from a
  constitutive knockout and from ventrobasal thalamic neurons; the same bundle
  marks 21-28 day transcriptional latency in the acute thalamic Perturb-seq
  window as unresolved.

I therefore treated `Nlgn2` as biologically reachable, but not as a broad
transcriptional regulator.

### Training count table

The declared 151-count training table is extremely sparse:

- 1,205 / 1,674 training perturbations have `n_degs = 0`.
- 276 / 1,674 have `n_degs = 1`.
- 1,512 / 1,674 are at `n_degs <= 2`.
- The median is 0 and the 90th percentile is 2.
- Of the 276 one-DEG perturbations, 237 are self-transcript-only in the
  matching expression Parquet.

The long upper tail is dominated by spliceosome, proteasome, chromatin, and
core cell-state regulators, not by single synaptic adhesion perturbations.

### Declared expression Parquet

I checked the matched Parquet rows for synaptic adhesion, inhibitory synapse,
and postsynaptic scaffold training perturbations in the same thalamic group.
The nearest functional comparators were almost all flat or self-only at
FDR < 0.05:

| target | n_degs in 151 TH Prkcd Grin2c Glut |
| --- | ---: |
| `Nlgn3` | 1 |
| `Nrxn1` | 1 |
| `Nrxn2` | 0 |
| `Nrxn3` | 0 |
| `Cntnap1` | 1 |
| `Cntnap2` | 1 |
| `Lrrtm1` | 1 |
| `Lrrtm3` | 0 |
| `Lrrtm4` | 0 |
| `Dlg4` | 1 |
| `Dlgap4` | 2 |
| `Shank2` | 0 |
| `Shank3` | 2 |
| `Syngap1` | 0 |
| `Gphn` | 0 |
| `Arhgef9` | 1 |

The Parquet rows showed that `Nlgn3`, `Nrxn1`, `Dlg4`, `Arhgef9`, `Cntnap1`,
`Cntnap2`, `Gabbr1`, `Gabbr2`, and `Gabra1` each had exactly one significant
feature and it was the perturbed transcript itself. `Gphn`, `Nrxn2`, `Nrxn3`,
and several related receptor or scaffold targets had no feature at FDR < 0.05.
`Grin1` was a clear exception with 89 DEGs, but it is an ionotropic glutamate
receptor core subunit whose thalamic perturbation produced a distinct activity
and homeostatic program rather than a generic synaptic-adhesion null.

### Same-experiment corpus checks

Packaged findings over the same experiment were consistent with this sparse
interpretation: `Nlgn3` had zero downstream genes at FDR < 0.10 across its
recovered cell groups, `Nrxn2` was downstream-null across 23 classes, `Nrxn1`
had only a Pvalb-restricted singleton downstream hit, `Dlg4` was globally flat
after removing its own transcript, and `Arhgef9` had no downstream genes at
FDR < 0.10 despite significant self-transcript depletion in this thalamic
class.

## Synthesis

`Nlgn2` has strong local expression and should lose renewable NLGN2 protein in
successfully edited cells, so a strict zero felt too low: a detectable
self-transcript change is plausible in a high-power thalamic group. The biology
does not, however, point to an acute nucleus-wide RNA state on the scale of the
high-count training tail. Its closest measured adhesion and inhibitory-synapse
neighbors mostly produced either zero DEGs or a single self-transcript DEG.

I therefore predicted that `Nlgn2` would land in the self-only / minimal
response regime and chose the integer point `1`.
