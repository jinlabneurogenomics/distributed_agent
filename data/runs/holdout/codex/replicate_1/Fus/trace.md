## Target

- Exact manifest target: `Fus`
- Requested endpoint: number of genes with BH-adjusted Wilcoxon `p < 0.05` in `151 TH Prkcd Grin2c Glut`.
- Output is a direct held-out forecast. I did not inspect a `Fus` perturbation profile or count.

## Evidence Used

### Biology-only Fus bundle

The declared `Fus.json` bundle supports a real perturbation in the requested
focal population:

- `Fus` was measured in the exact focal non-target cells with
  `pct_cells_expressing = 99.535%`, `mean_cp10k = 5.121`, and
  `mean_raw_umi = 8.046`.
- The functional-stock card adjudicated FUS as
  `likely_substantially_depleted` by the P37-P44 harvest: FUS is a dynamic
  nuclear RNA/DNA-binding ribonucleoprotein regulator, and primary mouse-neuron
  shRNA experiments depleted protein and produced an RNA-regulatory consequence
  within 10 days, inside this assay's 21-28 day P16-to-harvest window.
- The observability card supports postnatal neuronal relevance outside
  thalamus, but keeps survivor conditioning unknown and notes EWSR1/TAF15
  relatedness as a partial-compensation uncertainty rather than full
  redundancy.

Interpretation: high in-assay expression and a turnover-compatible dynamic
RBP mechanism make a strict zero less likely than for a generic target, but
the bundle does not imply a core-spliceosome-scale whole-gene response.

### Training count table

The 151 TH training count table contains 1,674 perturbations. It is extremely
zero-heavy:

| statistic | value |
| --- | ---: |
| total training perturbations | 1,674 |
| zero-DEG perturbations | 1,205 |
| positive perturbations | 469 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| 97.5th percentile | 100 |
| 99th percentile | 430 |

The local RNA-processing and RNP comparators in the same count table split into
three useful regimes:

| comparator class | 151 TH `n_degs` |
| --- | --- |
| spliceosome / core RNA-processing stressors | `Rnpc3 868`, `U2af2 828`, `Cdc40 624`, `Prpf6 454`, `Tnpo3 618`, `Thoc1 303`, `Snrnp70 213` |
| broad nuclear RNP / ALS-linked RBPs | `Hnrnpu 733`, `Tardbp 210`, `Matr3 149`, `Hnrnpc 122` |
| weak ALS/RNP boundary cases | `Hnrnpa2b1 11`, `Atxn2 8`, `Vcp 2`, `Grn 1`, `Kif5a 1`, `Sqstm1 1`, `Stmn2 1`, `Sort1 0`, `Tia1 0` |

Interpretation: RNA metabolism is a high-response neighborhood in this cell
class, but ALS/RBP identity alone is not enough. FUS should be pulled upward
from the all-target prior and downward from the 400-900 DEG core-spliceosome
targets.

### 151 TH expression-profile analysis of training perturbations

I profiled a 21-node RNA-processing/RNP cohort directly from
`training_de_all_cell_groups.parquet` with `group_name =
"151 TH Prkcd Grin2c Glut"`, `gene_target` as the entity, `names` as
features, `logfoldchanges` as signed values, and `pvals_adj < 0.05` as the
significance definition.

The Parquet re-derived the exact same 151 TH DEG burdens for the focal analogs:

| target | 151 TH DEGs | perturbed nuclei |
| --- | ---: | ---: |
| `Rnpc3` | 868 | 149 |
| `U2af2` | 828 | 222 |
| `Hnrnpu` | 733 | 163 |
| `Cdc40` | 624 | 159 |
| `Prpf6` | 454 | 72 |
| `Thoc1` | 303 | 121 |
| `Snrnp70` | 213 | 135 |
| `Tardbp` | 210 | 153 |
| `Matr3` | 149 | 130 |
| `Hnrnpc` | 122 | 196 |
| `Hnrnpa2b1` | 11 | 124 |
| `Ddx3x` | 8 | 138 |
| `Hnrnph2` | 4 | 169 |
| `Hnrnpdl` | 1 | 206 |
| `Snrpn` | 1 | 214 |
| `Fmr1` | 0 | 178 |
| `Tia1` | 0 | 85 |

A cohort diagnostic over the 12 active RNP/splicing perturbations showed that
the active nodes are directionally related but not one narrow copy of the same
signature: across 66 selected pairs, median positive-tail overlap coefficient
was 0.142, median negative-tail overlap coefficient was 0.280, and median
significant-program overlap coefficients were 0.089 positive and 0.312
negative. The explicit `Tardbp`/`Matr3`/`Hnrnpu`/`U2af2`/`Rnpc3` inspection
likewise kept the large spliceosome and hnRNP signatures distinct from the
near-flat `Hnrnpa2b1`, `Ddx3x`, and `Fmr1` profiles despite superficial RBP
similarity.

Interpretation: the profile geometry supports treating FUS as a partial,
RNA-regulatory responder rather than borrowing the median of the very largest
spliceosome/proteostasis-like profiles.

### Same-experiment corpus context for training analogs

Packaged Findings for the measured analogs agreed with the quantitative split:

- `Tardbp` produced a real, uneven postmitotic neuronal response and its compact
  RNA-processing response was linked to expected TDP-43 biology, but the report
  also found that disease-family comparators such as `Matr3`, `Hnrnpa2b1`,
  `Atxn2`, `Tia1`, and `Vcp` were not interchangeable acute phenocopies.
- `Matr3` had its largest responses in 151 TH / 155 MB / 191 MB groups and
  partially converged with `Tardbp` and splicing factors, while still being much
  smaller than `U2af2`, `Prpf6`, and `Cdc40`.
- `Hnrnpu`, `U2af2`, and `Rnpc3` reports tied their large signatures to
  spliceosome/RNA-processing and secondary proteostasis or neuronal-effector
  states; the same reports explicitly separated core RNA-processing convergence
  from generic hnRNP-family membership.

Interpretation: `Tardbp` and `Matr3` are better upper analogs for FUS than
`Rnpc3`/`U2af2`, while `Hnrnpa2b1`/`Tia1`/`Atxn2` are lower boundary cases
showing that a disease-linked or RNP-associated target can be almost silent.

## Synthesis

I placed `Fus` above the global 95th percentile of the training table because
it is almost universally expressed in the focal population, should have lost
functional dynamic RNP stock by the harvest window, and sits in the same
nuclear RNA-processing biology that generated visible 151 TH responses for
`Tardbp`, `Matr3`, `Hnrnpu`, and splicing factors.

I placed it well below `Tardbp`/`Matr3` rather than at their 149-210 DEG scale
because the 3-prime whole-gene readout will miss direct FUS splicing/localization
defects, EWSR1/TAF15 provide a plausible buffer, and the training data show that
several ALS/RNP relatives are flat or only weakly significant even with adequate
151 TH cell recovery.

Balancing those bounds, my point forecast is a modest nonzero response:

`predicted_n_degs = 64`
