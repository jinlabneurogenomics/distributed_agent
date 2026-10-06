# Thoc2 DEG-count forecast

## Target and endpoint

- Target manifest: `Thoc2`.
- Requested endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, the number of measured genes with Wilcoxon BH-adjusted `p < 0.05`.
- Declared training count table: 1,674 targets; `Thoc2` is absent.
- Declared expression table: `training_de_all_cell_groups.parquet`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"` for matched training profiles.

## Biology used

The declared Thoc2 bundle supports functional realization in the assayed window:

- THOC2 is a core THO/TREX mRNA-processing and nuclear-export component.
- A P16 disruptive edit should mainly stop new intact THOC2 supply; pre-edit THOC2 is a renewable protein stock rather than an irreversible installed structure.
- Measured THOC2 half-lives in primary nondividing mouse neurons were about 43-45 h, far shorter than the 21-28 d P16-to-P37/P44 interval.
- The card therefore adjudicates pre-edit functional stock as likely substantially depleted by harvest.
- Exact in-assay reach is high in the focal population: Thoc2 RNA was detected in 20,186 / 23,679 non-target 151-class nuclei, or 85.25%, with mean raw UMI 2.225 and mean log1p CP10k 0.784.

That makes a recovered transcriptional response biologically plausible despite survivor-conditioning. It does not make the response automatically as large as every RNA-processing target, because the mouse phenotype evidence is developmental/hypomorphic rather than an acute thalamic null, and Thoc2l is an annotated related gene with unknown buffering capacity.

## Training measurements that set the scale

The 151-class training count distribution is very zero-heavy:

- 1,205 / 1,674 training targets have `n_degs = 0`.
- The median is 0 and the 90th percentile is 2.
- Only 59 / 1,674 training targets have at least 50 DEGs.
- The moderate/high tail begins sharply: among counts at least 100, the median is 368.

Named RNA-processing/export comparators from the declared training count table:

| training target | 151-class n_degs |
|---|---:|
| Ddx39b | 0 |
| Hnrnpa2b1 | 11 |
| Hnrnpc | 122 |
| Thoc1 | 303 |
| Prpf6 | 454 |
| Cdc40 | 624 |
| Hnrnpu | 733 |
| U2af2 | 828 |
| Rnpc3 | 868 |
| Tpr | 1768 |

Direct Parquet aggregation for those same nodes confirmed the count-table values over 17,259 measured genes in `151 TH Prkcd Grin2c Glut`; for example, `Thoc1` had 303 DEGs split 233 up / 70 down with 121 matched perturbed nuclei, while `Ddx39b` had 0 DEGs with 48 matched perturbed nuclei.

## Profile evidence

A symmetric comparison of the 10 RNA-processing/export nodes in the 151-class Parquet showed that the non-null comparators share a broad signed profile rather than being count-only coincidences.

- `Thoc1` had whole-profile Pearson correlations of 0.687 with `Tpr`, 0.685 with `Hnrnpu`, 0.677 with `Cdc40`, 0.647 with `Prpf6`, 0.621 with `Rnpc3`, and 0.606 with `U2af2`.
- The high-count nodes spanned the same response-activity family in the profile topology.
- `Ddx39b` stayed at 0 significant features, so mRNA export annotation alone is not enough to force a nonzero call.

## Synthesis

The closest measured perturbation is `Thoc1`, the only measured THO-subcomplex subunit in the declared 151-class count table, at 303 DEGs. I treated `Tpr` and the spliceosome factors as upper-scale evidence for what a strong RNA-biogenesis/export stress state can look like in this high-yield cell class, but not as direct magnitude donors for THOC2. I treated `Ddx39b` as a real lower boundary because it is RNA-export machinery yet quiet in this endpoint, but discounted it relative to `Thoc1` because DDX39B is not the THO structural core and its 48 matched perturbed nuclei leave it a weak scale anchor.

Given the high focal expression reach and predicted protein-stock depletion, I forecast a real but moderate 151-class response centered on the same-complex `Thoc1` anchor rather than on the dataset-wide zero mode or on the 800-1,800 DEG upper tail.

Predicted `n_degs`: **300**
