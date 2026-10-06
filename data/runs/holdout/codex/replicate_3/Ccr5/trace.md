# Ccr5 DEG-count forecast

## Declared target and endpoint

- Target: `Ccr5`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Point prediction: `0`

The target was the one row in the declared `Ccr5.csv` manifest. The endpoint
count table available for `151 TH Prkcd Grin2c Glut` contained 1,674 training
perturbations and excluded the held-out Ccr5 outcome.

## Target biology used

The biology-only Ccr5 bundle supports functional realization of an edit in
cells that use CCR5: CCR5 is a dynamically trafficked cell-surface chemokine
GPCR, pre-edit receptor stock is expected to clear on the 21-28 day P16-to-
P37/P44 interval, and adult mouse hippocampal/cortical perturbations show that
CCR5 can matter in postnatal neural settings.

The same bundle made the focal-population reach extremely narrow:

- `pct_cells_expressing = 0.32095949997888423`
- `n_cells_expressing = 76` of `23679` non-target nuclei
- `total_target_umi = 86`
- `mean_raw_umi = 0.003631910131340006`
- `pseudobulk_cpm = 0.22762468713284517`

I therefore treated Ccr5 as biologically editable but nearly absent in the
assayed thalamic NeuN-positive population. A large class-wide nuclear RNA
program would require either an effect in many Ccr5-undetected neurons or a
strong indirect signal, not simply loss of a receptor in the small fraction of
detected Ccr5-positive nuclei.

## Training evidence used

The focal count table was dominated by tiny responses:

- 1,205 / 1,674 training perturbations had `n_degs = 0`
- 1,481 / 1,674 had `n_degs <= 1`
- 1,546 / 1,674 had `n_degs <= 5`

The closest target named by the Ccr5 biology card is the curated paralog
`Ccr2`; it had `n_degs = 0` in the focal count table. The represented
chemokine-GPCR comparators in the same table, `Cx3cr1` and `Cxcr4`, also had
`n_degs = 0`.

The declared differential-expression Parquet confirmed the row-level focal
counts for those comparators:

| target | measured genes in `151 TH Prkcd Grin2c Glut` | BH<0.05 genes | BH<0.10 genes | minimum BH p |
| --- | ---: | ---: | ---: | ---: |
| `Ccr2` | 17,259 | 0 | 0 | 1.0 |
| `Cx3cr1` | 17,259 | 0 | 0 | 1.0 |
| `Cxcr4` | 17,259 | 0 | 1 | 0.06722883626445451 |

Packaged same-experiment Ccr2 findings, used as interpretation of these same
Perturb-seq measurements rather than independent replication, also pointed to
a flat neuronal chemokine-receptor axis: Ccr2 was a pan-measured neuronal null
at FDR<0.10, its score vector had no substantive positive or negative neighbor,
and Cx3cr1/Cxcr4 did not reveal a generic chemokine-GPCR neuronal response.

## Synthesis

The strongest upward evidence was that functional CCR5 protein should be gone
by harvest in successfully edited Ccr5-expressing neurons and that CCR5 has
documented postnatal neural effects outside this exact context. That evidence
did not overcome three downward bearings for this exact scalar endpoint:

- Ccr5 transcript was detected in only 0.32% of the focal non-target nuclei.
- NeuN-positive neuronal sampling omits or under-samples the immune/myeloid
  compartments where chemokine receptors often act.
- The closest available training perturbations around chemokine receptors were
  all zero-count in the focal class, with Ccr2 null across its neuronal surface.

I therefore assigned the most likely BH<0.05 DEG count for Ccr5 in
`151 TH Prkcd Grin2c Glut` to the zero-count mode: `0`.

I did not use the withheld Ccr5 expression signature, the Ccr5 target outcome,
labeled-neighbor outcomes, calibrated response probabilities, scalar priors, or
relationship/branch/terminal prediction review artifacts.
