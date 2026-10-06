# Direct forecast trace

## Target

- Manifest target: `Dnm1l`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: count of measured focal-population genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`

## Evidence used

### Declared Dnm1l biology bundle

- The focal non-target expression measurement for `Dnm1l` is available in the declared biology bundle: `Dnm1l` was detected in 22,992 of 23,679 focal non-target nuclei, `97.10%`, with mean raw UMI `4.81`, mean CP10k `3.015`, and mean log1p CP10k `1.308`.
- The same bundle adjudicates the functional stock as `likely_substantially_depleted` by the P37-P44 harvest. DRP1/DNM1L is a recurrent, dynamic mitochondrial/peroxisomal fission GTPase; its residual protein is expected to clear in this 21-28 day window because neuronal DNM1L protein has a roughly 3-day turnover estimate and adult forebrain conditional deletion reached maximal hippocampal depletion within 14 days.
- The observability card supports a postmitotic-neuron phenotype within the window but notes that the direct phenotype evidence is adult forebrain/hippocampus rather than this thalamic class and that survivor-conditioned single-nucleus RNA may miss some mitochondrial morphology or synaptic consequences.

### Declared focal training counts and expression Parquet

The focal count table contains 1,674 training perturbations and no `Dnm1l` row. Its distribution is very sparse:

- `1,205 / 1,674` training targets have `n_degs = 0`.
- The median count is `0`; the 75th percentile is `1`; the 95th percentile is `18`.
- Direct focal Parquet inspection showed that `319` training targets have a significant self-transcript row and that many one-DEG calls are self-only: `237 / 276` targets with `n_degs = 1` consist of their own transcript as the sole FDR-significant feature.
- After subtracting significant self-transcript rows from training targets where the self row is present, `1,442 / 1,674` have no significant downstream measured gene.

Training perturbations in the mitochondrial fission/dynamics and mitochondrial stress neighborhood were mostly silent or self-only in this exact focal class:

| training target | focal `n_degs` | interpretation from focal Parquet |
|---|---:|---|
| `Mff` | 0 | no self hit and no downstream hit |
| `Dnm1` | 1 | self-transcript only; classical dynamins are not DRP1 substitutes in the `Dnm1l` biology bundle |
| `Opa1` | 37 | 36 downstream hits plus self; the downstream genes include ISR/amino-acid-stress markers such as `Asns`, `Ddit3`, `Chac1`, `Slc7a5`, and aminoacyl-tRNA synthetases |
| `Rhot1` | 0 | no downstream hit |
| `Yme1l1` | 0 | no downstream hit |
| `Afg3l2` | 0 | no downstream hit |
| `Clpp` | 0 | no downstream hit |
| `Clpx` | 0 | no downstream hit |
| `Lrpprc` | 0 | no downstream hit |
| `Slc25a46` | 1 | self-transcript only |
| `Park7` | 1 | self-transcript only |
| `Sqstm1` | 1 | self-transcript only |
| `Atad1` | 1 | self-transcript only |

Other focal respiratory-chain/import comparators such as `Ndufs4`, `Ndufa10`, `Sdha`, `Cox5a`, `Uqcrc2`, `Timmdc1`, and `Tomm40` were likewise in the 0-1 range, with the nonzero calls dominated by the perturbed transcript itself.

## Synthesis

I treated a strong `Dnm1l` molecular lesion as likely realized because the target RNA is broadly present in the focal class and DRP1 protein should renew within the experimental window. I did not transfer the `Mff = 0` count directly: MFF is only one DRP1 recruitment route, so an upstream `Dnm1l` edit should be less buffered than `Mff` loss. I also downweighted the `Opa1 = 37` footprint because that profile has a clear inner-mitochondrial ISR-like downstream program, whereas most nearby fission, mitochondrial QC, and OXPHOS perturbations in the same focal data had no detectable downstream survivor-state RNA response.

That leaves the expected focal burden at the boundary between null and self/very-small. The exact focal expression of `Dnm1l` makes a significant targeted-transcript row plausible, while the training analogs make a tens-of-genes downstream program unlikely. My point prediction is therefore:

`predicted_n_degs = 1`
