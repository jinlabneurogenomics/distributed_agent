# Gad1 direct DEG-count forecast

## Target and endpoint

- Target from the declared one-row holdout manifest: `Gad1`.
- Requested focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- The declared training endpoint table contains 1,674 targets and does not contain `Gad1`.

## Evidence used

### Gad1 biology bundle

I used the canonical `Gad1` biology view only; it reported
`target_outcome_exposed=false` and `labeled_neighbors_exposed=false`.

The Gad1 source card makes a disruptive edit biologically meaningful in cells
that rely on GAD67: Gad1 encodes the 67-kDa glutamate decarboxylase that
converts glutamate to GABA, and the functional-stock adjudication calls
Gad1-encoded catalytic capacity `likely_substantially_depleted` by the
P37-P44 harvest if an expressing postmitotic neuron is successfully edited at
P16. That argues against treating Gad1 as an intrinsically inert perturbation.

The limiting evidence is reach in the requested focal class. The exact
non-target expression measurement for `151 TH Prkcd Grin2c Glut` was:

- `pct_cells_expressing = 12.2471`
- `n_non_target_cells = 23679`
- `n_cells_expressing = 2900`
- `mean_raw_umi = 0.1838`
- `mean_log1p_cp10k = 0.0684`
- `pseudobulk_cpm = 11.5189`

The same bundle explicitly supersedes qualitative thalamic expression claims
with this exact in-assay reach. Its literature-derived thalamic prior is also
restricted rather than broad: Gad1-positive/GABAergic cells are sparse in
mouse thalamocortical nuclei, not the dominant pan-thalamic population.

### Training endpoint table

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table is very
zero-skewed:

- 1,205 / 1,674 targets have `n_degs = 0`.
- 1,481 / 1,674 have `n_degs <= 1`.
- 1,542 / 1,674 have `n_degs <= 4`.
- The median is `0`; the 75th percentile is `1`.

This puts a low-reach metabolic neurotransmitter perturbation near a strong
floor even before target-specific interpretation.

### Task-matched GABA and inhibitory-neuron perturbations

I retained same-endpoint training perturbations by Gad1 mechanism and local
cell-state relevance rather than by global footprint:

| training target | reason for checking | `151 TH Prkcd Grin2c Glut` `n_degs` |
| --- | --- | ---: |
| `Gad2` | Gad1 paralog and GAD65/GABA synthesis buffer named in the Gad1 card | 0 |
| `Slc32a1` | vesicular GABA transporter | 0 |
| `Slc6a1` | GABA transporter | 0 |
| `Abat` | GABA catabolism | 0 |
| `Dlx6` | inhibitory-neuron developmental regulator in the training universe | 0 |
| `Gphn` | inhibitory synapse scaffold | 0 |
| `Reln` | inhibitory-neuron-associated marker in this nominated set | 0 |
| `Gabra1` | GABA-A receptor subunit | 1 |
| `Gabrb2` | GABA-A receptor subunit | 4 |

The direct profile comparison of 16 GABA/inhibitory training perturbations in
the matched `151 TH Prkcd Grin2c Glut` Parquet slice found that 11 / 16 had no
significant features and that every member of the cohort fell in the `0` to `9`
significant-feature bin. The four closest biochemical Gad1 comparators checked
above, `Gad2`, `Slc32a1`, `Slc6a1`, and `Abat`, each had exactly zero positive
and zero negative significant features in the focal slice.

## Synthesis

Gad1 knockout should deplete GAD67 in genuinely Gad1-expressing neurons during
the 21-28 day experimental window, so I did not score it as a molecular
no-operation. The requested class, however, is a thalamic glutamatergic
aggregate with low Gad1 reach: only about 12% of non-target nuclei expressed
Gad1 at a mean of 0.18 raw UMI. That makes the class-level CRISPR contrast
heavily diluted and only weakly coupled to the GABAergic biology in the source
card.

The measured training evidence in the same class supports that downward
placement. Directly adjacent GABA synthesis, packaging, transport, and
catabolism perturbations were all exact zeros, and the broader GABA receptor /
inhibitory marker cohort stayed almost entirely at the floor. Given that the
training distribution itself has a zero median, I forecast Gad1 at the modal
floor rather than adding a self-transcript or one-gene allowance.

Predicted `n_degs`: `0`.
