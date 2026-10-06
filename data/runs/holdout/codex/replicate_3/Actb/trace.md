# Actb DEG-count forecast for `151 TH Prkcd Grin2c Glut`

## Target biology used

- Target: `Actb`.
- Requested endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `p < 0.05`.
- The exact focal expression bundle reports `feature_available=false` and `feature_status=not_in_expression_matrix` for Actb in this group, so the perturbed transcript itself cannot contribute a self-DEG to the requested measured-gene count. The focal contrast is available and was measured against 23,679 matched non-target control nuclei.
- The Actb biology bundle supports real functional engagement by P37-P44 rather than a permanently pre-installed product: beta-actin is a dynamic monomer/filament pool, and mouse conditional-loss evidence places beta-actin depletion on a days-to-weeks clock after recombination.
- The same bundle also argues against expecting a broad cell-state transcriptome by default in this assay: gamma-actin and other isoactins can partly preserve total actin, the closest CNS phenotype evidence is developmental rather than a P16 thalamic perturbation, the cellular reach inside the aggregated thalamic population is unresolved, and survivor-conditioned recovery may attenuate the profile.

## Training measurements used

The declared focal count table contains 1,674 training targets after withholding Actb. It is floor-heavy in this class:

- 1,205/1,674 targets have 0 DEGs.
- 1,481/1,674 have at most 1 DEG.
- 1,512/1,674 have at most 2 DEGs.
- The median is 0, the 75th percentile is 1, and the 90th percentile is 2.

I treated the cytoskeletal genes as the relevant quantitative scale for Actb rather than the screen-wide high tail from RNA processing, proteostasis, and nuclear housekeeping factors. In the focal Parquet rows:

| comparator | focal n_degs | interpretation |
|---|---:|---|
| `Actg1` | 1 | closest same-family cytoplasmic actin anchor; the only significant row was `Actg1` itself |
| `Actn4` | 0 | actin-crosslinking structural gene |
| `Cdc42` | 1 | Rho-family actin regulator; the only significant row was `Cdc42` itself |
| `Rac1` | 0 | Rho-family actin regulator |
| `Rho` | 0 | Rho-family actin regulator |
| `Add1` | 0 | actin/spectrin capping protein |
| `Add2` | 0 | actin/spectrin capping protein |
| `Add3` | 0 | actin/spectrin capping protein |
| `Cfl2` | 0 | actin-filament turnover regulator |

I also used core microtubule and neuronal structural comparators as a broader cytoskeleton boundary: `Tubb4b=1`, `Tubb5=1`, `Tuba4a=2`, and `Tuba1a=7`; the tubulin counts were dominated by the perturbed tubulin transcript and close tubulin isoform compensation rather than by a generic injury or death-state signature.

## Synthesis

Actb loss should eventually remove beta-actin-specific supply in edited cells, but the direct thalamic DEG-count expectation is low because:

- the closest measured isoform perturbation, `Actg1`, had a self-transcript-only response in this same class;
- Actb self loss is unobservable as a measured DEG because `Actb` is absent from the expression matrix;
- other actin/cytoskeletal training perturbations with comparable structural logic were mostly zero or self-only;
- isoactin compensation and survivor-conditioned sampling both make a strong recovered-nucleus transcriptional program uncertain rather than expected.

I therefore forecast that Actb will sit at the focal floor after removal of any impossible self-target contribution.

```tsv
target_name	predicted_n_degs
Actb	0
```
