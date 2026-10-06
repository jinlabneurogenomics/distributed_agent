# Direct forecast for Fus in 151 TH Prkcd Grin2c Glut

## Inputs used

- Target: `Fus` from the declared one-row manifest.
- Canonical prediction-safe biology bundle: `biology_bundles/Fus.json`, also
  read through `reference.perturbation_characterization` with
  `view=biology`; the served bundle reported
  `target_outcome_exposed=false` and `labeled_neighbors_exposed=false`.
- Target cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05` in
  the declared 151 TH count table.
- Training measurements: the declared 151 TH count table and filtered rows from
  `training_de_all_cell_groups.parquet` for RNA-binding and spliceosome
  comparators. The filtered table is same-experiment evidence, not independent
  replication of the count table.
- Same-experiment corpus target contexts for `Tardbp`, `Matr3`, `Hnrnpc`, and
  `Snrnp70`; these were used only for training perturbations.

## Biology bearing

The Fus bundle makes a true silent forecast unlikely:

- `Fus` RNA was detected in 23,569 of 23,679 non-target nuclei in the focal
  cell class, with 99.535% cells expressing, mean raw UMI 8.046, and
  pseudobulk CPM 504.3. Thus the perturbation targets a transcript that is
  broadly present in the assayed 151 TH population.
- FUS is a predominantly nuclear RNA/DNA-binding protein that couples
  transcription and RNA processing in dynamic RNP assemblies.
- The functional-stock card adjudicated FUS as
  `likely_substantially_depleted` by the P37-P44 harvest: disruptive editing
  stops new production, the operative FUS assemblies are continuously renewed,
  and direct primary-neuron shRNA experiments showed protein depletion and an
  RNA-regulatory consequence within 10 days, inside the 21-28 day experiment.
- Related FET-family proteins, EWSR1 and TAF15, can respond to Fus loss but do
  not appear completely redundant, so paralogy is a dampening uncertainty rather
  than a reason to forecast zero.

At the same time, FUS is not a core spliceosome subunit in this experiment.
The report layer for measured training perturbations repeatedly shows that
related RNA-binding or ALS/stress-granule genes do not form one interchangeable
module; therefore I used those targets to set a magnitude tier, not to assume
that Fus will phenocopy a specific profile.

## Training scale

The 151 TH count table contained 1,674 training perturbations. Its distribution
was extremely zero inflated:

- median `n_degs`: 0
- 75th percentile: 1
- 90th percentile: 2
- 95th percentile: 18
- 99th percentile: 436
- 1,205 / 1,674 targets had `n_degs = 0`

Filtered 151 TH rows from the declared Parquet gave the following exact DEG
counts for the comparators I used:

| target | n_degs |
|---|---:|
| Rnpc3 | 868 |
| U2af2 | 828 |
| Hnrnpu | 733 |
| Cdc40 | 624 |
| Prpf6 | 454 |
| Thoc1 | 303 |
| Snrnp70 | 213 |
| Tardbp | 210 |
| Matr3 | 149 |
| Hnrnpc | 122 |
| Atxn2 | 8 |
| Vcp | 2 |
| Sqstm1 | 1 |
| Fmr1 | 0 |
| Tia1 | 0 |

Those measurements separated three useful magnitude regimes.

1. Core or near-core splicing/RNA-biogenesis failures (`Rnpc3`, `U2af2`,
   `Cdc40`, `Prpf6`) were very large, 454-868 DEGs. The Hnrnpc and Snrnp70
   reports placed Hnrnpc/Snrnp70 near that process but explicitly below a full
   core-spliceosome-collapse state.
2. Strong single RBP perturbations had a moderate 151 TH footprint:
   `Tardbp` 210, `Matr3` 149, `Hnrnpc` 122, with `Snrnp70` at 213 as a nearby
   U1/RNP upper comparator.
3. Several RNA-granule or neurodegeneration-linked targets were weak or flat:
   `Atxn2` 8, `Vcp` 2, `Sqstm1` 1, `Tia1` 0, `Fmr1` 0. Reports for `Matr3`
   and `Tardbp` directly warned that ALS-linked or RBP-family membership alone
   did not imply a common juvenile-neuron loss-of-function transcriptomic
   module.

Pairwise score correlations among the moderate RBPs were low in the focal
Parquet slice (`Tardbp`/`Matr3` r = -0.0027,
`Tardbp`/`Hnrnpc` r = 0.030, `Matr3`/`Hnrnpc` r = -0.0013), while
`Matr3` and `Tardbp` still generated robust individual RNP-associated programs.
That argues against borrowing any single profile but supports an RBP-specific
count on the order of 10^2 DE genes.

## Numeric synthesis

I placed `Fus` just inside the moderate RBP tier:

- Upward relative to the zero-inflated training baseline because `Fus` is
  expressed in essentially all assayed 151 TH control nuclei and its operative
  RNA-bound stock should turn over within the P16-to-P37/P44 interval.
- Upward relative to the flat RNA-granule examples because FUS has direct
  nuclear RNA-processing biology and direct mouse-neuron depletion evidence.
- Downward relative to `Rnpc3`/`U2af2`/`Cdc40`/`Prpf6`/`Hnrnpu` because FUS is
  a dynamic RBP with FET-family partial redundancy, not an obligate core
  spliceosome or broad RNA-architecture dependency.
- Centered close to `Tardbp`, `Matr3`, and `Hnrnpc`, whose 151 TH counts were
  210, 149, and 122.

The resulting point prediction is `160` DEGs.
