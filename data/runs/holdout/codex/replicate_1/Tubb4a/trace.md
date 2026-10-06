# Tubb4a direct n_degs forecast

## Target and endpoint

- Target: `Tubb4a`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Requested endpoint: count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the focal class.
- Forecast: `1`

## Evidence used

### Canonical biology bundle

The declared biology-only bundle reports exact in-assay focal expression for
`Tubb4a`: 22,311 of 23,679 non-target nuclei expressed it in
`151 TH Prkcd Grin2c Glut` (`94.222729%`), with mean raw UMI `5.0623`,
mean CP10K `2.9816`, and pseudobulk CPM `317.27`. This makes the target
transcript measurable in the focal population, so a self-transcript DE row is
plausible.

The same bundle argues against a broad downstream transcriptional state.
`Tubb4a` encodes a beta-tubulin structural subunit; a disruptive edit blocks
new TUBB4A supply but does not directly inactivate TUBB4A already incorporated
into mixed-isotype microtubules. The functional-stock card adjudicates operative
microtubule stock as `likely_persists` through the P16-to-P37/P44 interval:
germline null mouse neural tissue preserved total beta-tubulin through other
beta-tubulin isotypes, with no detected neural phenotype through one year, while
acute thalamic compensation remains untested.

### Focal-class training counts

The 151-class training count table contained 1,674 perturbations. It was
strongly zero-inflated:

- `1205 / 1674 = 72.0%` had `n_degs = 0`
- `1481 / 1674 = 88.5%` had `n_degs <= 1`
- `1512 / 1674 = 90.3%` had `n_degs <= 2`

The biology-matched tubulin and microtubule perturbations were all in this very
low-count regime in the same endpoint:

| training target | n_degs in 151 |
| --- | ---: |
| `Tubb4b` | 1 |
| `Tubb5` | 1 |
| `Tuba4a` | 2 |
| `Tuba1a` | 7 |
| `Kif1a` | 1 |
| `Kif2a` | 0 |
| `Kif5a` | 1 |
| `Map1b` | 1 |
| `Mapt` | 1 |

Direct Parquet rows for these 151-class tubulin targets showed that `Tubb4b`
and `Tubb5` each contributed only the perturbed transcript itself at
`pvals_adj < 0.05`; `Tuba4a` contributed its self row plus only `Mast1`; and
only `Tuba1a` produced a small multi-tubulin compensation module. The local
corpus likewise described `Tubb4b`, `Tubb5`, `Tuba4a`, `Map1b`, `Mapt`,
`Kif2a`, and `Kif5a` as buffered or nearly null, and noted that direct
`Tuba4a`/`Tubb4b`/`Tubb5` beta-tubulin perturbations did not phenocopy the
`Tuba1a` compensation module.

### Profile comparison

I compared the observed 151-class signed profiles of
`Tuba1a`, `Tuba4a`, `Tubb4b`, `Tubb5`, `Kif1a`, `Kif2a`, `Kif5a`, `Map1b`, and
`Mapt`. The cohort had weak recurrence rather than a shared high-DEG state:
median signed-tail overlap was only `0.025` for the positive tail and `0.0325`
for the negative tail, and significant-program overlap was zero in every
reported direction.

## Synthesis

The exact focal expression of `Tubb4a` argues against complete invisibility of
the target transcript. However, the decisive biological and same-endpoint
training evidence point to buffering of beta-tubulin structural loss, not to a
large thalamic survivor-state program: the closest beta-tubulin training
perturbations were self-only or nearly self-only, the alpha-tubulin `Tuba1a`
compensation program did not transfer to beta-tubulin perturbations, and the
broader microtubule machinery cohort also stayed almost flat. I therefore
forecast one total significant row, corresponding to an expected self-transcript
call with no downstream genes passing BH `0.05`.
