# Sec31a n_degs forecast

Target: `Sec31a`

Cell class: `151 TH Prkcd Grin2c Glut`

Predicted `n_degs`: `0`

## Endpoint

`n_degs` is the number of measured genes in this focal class with BH-adjusted
Wilcoxon `p < 0.05` for one perturbation versus its matched non-targeting
control.

## Sec31a biology used

- The canonical Sec31a biology bundle places SEC31A in the SEC13-SEC31 outer
  COPII coat at ER exit sites and in the COPII prebudding/vesicle-formation
  step with `Sec13`, `Sec23a/b`, and `Sec24a/b/c/d`.
- Exact focal-population expression is available and substantial:
  `mean_raw_umi = 2.0247`, `mean_log1p_cp10k = 0.7244`, and `82.30%` of
  `151 TH Prkcd Grin2c Glut` non-target cells express `Sec31a`.
- The functional-stock adjudication does not establish that SEC31A protein is
  gone by the P37-P44 harvest. Stopping new intact SEC31A synthesis should not
  immediately inactivate already synthesized SEC31A, SEC31A exchange at ER exit
  sites is not a degradation half-life, and no target-specific degradation or
  perturbation-to-loss clock was available.
- The available mouse loss phenotype is whole-animal embryonic lethality; it is
  not a postnatal thalamic-neuron timing anchor. `Sec31b` is a paralog but the
  bundle had no thalamic compensation test.

## Training measurements used

The declared focal-class count table contains 1,674 training perturbations.
Its distribution is extremely zero-heavy:

- `1205 / 1674` targets have `n_degs = 0`
- `276 / 1674` have `n_degs = 1`
- median `0`, 75th percentile `1`, 90th percentile `2`, 95th percentile `18`

I then used the declared training Parquet in the same cell class for
COPII/secretory-pathway perturbations that were present in training:

| training perturbation | focal `n_degs` | matched perturbation nuclei | min BH FDR |
|---|---:|---:|---:|
| `Sec23a` | 0 | 307 | 0.8735 |
| `Sar1b` | 0 | 112 | 0.1085 |
| `Tfg` | 0 | 118 | 1.0000 |
| `Copa` | 0 | 75 | 0.3644 |
| `Copg1` | 1 | 234 | 9.24e-17 |
| `Rab18` | 0 | 117 | 0.9123 |
| `Trappc10` | 0 | 142 | 0.8154 |
| `Trappc9` | 0 | 263 | 1.0000 |
| `Hspa5` | 5 | 47 | 0.00415 |

`Copg1`'s single DEG was only the self transcript. `Hspa5` was a looser
ER-stress comparator rather than a COPII structural analog; its five DEGs were
downstream ER-stress genes and it had only 47 matched perturbation nuclei.

The profile cohort over these nine training perturbations did not reveal a
coherent hidden ER-export program below the FDR line. Across the 36 pairwise
comparisons, median top-tail overlap was only 0.050 for positive tails and
0.0525 for negative tails, positive significant-program overlap was absent, and
the five significant `Hspa5` genes were not shared with the COPII/traffic
perturbations.

## Synthesis

`Sec31a` is expressed in the focal population and is part of an essential
secretory-pathway coat, so a small response or a single self-transcript hit is
plausible. I nevertheless put most weight on the task-matched training
evidence: the closest measured COPII component, `Sec23a`, had zero focal DEGs
despite 307 matched nuclei; `Sar1b` and `Tfg` were also zero; the broader
secretory-traffic set was dominated by zeros; and the one-count `Copg1`
example did not show a downstream program.

Because pre-existing SEC31A persistence through the harvest is unresolved and
the training analogs show little recurrent thalamic transcriptional response,
I forecast the modal quiet outcome.
