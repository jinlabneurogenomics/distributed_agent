# Dcx direct `n_degs` forecast

## Target and endpoint

- Held-out manifest target: `Dcx`.
- Cell group: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes in the focal perturbation contrast with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- The declared training count table contains 1,674 targets and omits `Dcx`.

## Evidence used

### Dcx biology bundle

The canonical `Dcx` bundle and runtime `characterization_bundle(target="Dcx", view="biology")` exposed only source biology and exact focal-population expression, with `target_outcome_exposed=false`.

The functional-stock card supports functional realization where `Dcx` is truly expressed and edited: DCX is a soluble, renewable microtubule-associated protein, and a DCX-Halo pulse-chase in primary neurons measured turnover on an hours scale, far shorter than the 21-28 day edit-to-harvest window.

The same bundle makes the matched adult thalamic consequence uncertain and probably weak. The strongest mouse loss phenotype is developmental hippocampal lamination; acute adult dentate-gyrus loss did not alter selected newborn-neuron survival, differentiation, or fate readouts; late postnatal/adult robust DCX signal is mainly in immature neurogenic populations rather than mature pan-thalamic neurons; and Dclk paralog redundancy was demonstrated only in developing hippocampus.

Exact non-target expression in the focal population is low but present:

- `mean_cp10k = 0.543707`
- `mean_raw_umi = 0.841210`
- `pct_cells_expressing = 46.733392`
- `n_cells_expressing = 11066 / 23679`

I treated this as enough reach for a possible self-transcript call, but not as evidence for a broad downstream state in mature thalamic neurons.

### Training endpoint scale

In `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`:

- rows: 1,674
- median `n_degs`: 0
- mean `n_degs`: 14.05
- zero-DEG targets: 1,205 / 1,674
- exactly-one-DEG targets: 276 / 1,674
- targets with `n_degs <= 1`: 1,481 / 1,674
- targets with `n_degs >= 100`: 43 / 1,674

So the same focal class has a heavy floor at 0-1 genes, with a long tail of rare broad responders.

### Cytoskeletal and migration comparators

I used the declared Parquet only for training targets in the same `151 TH Prkcd Grin2c Glut` context, retrieving rows for exact cytoskeletal, microtubule, or neuronal-migration candidates when either `pvals_adj < 0.05` or the measured gene was the perturbed target.

The closest microtubule-associated training genes were floor responses:

| comparator | count-table `n_degs` | exact focal interpretation |
|---|---:|---|
| `Map1b` | 1 | self-transcript only; `Map1b` p-adj `1.06e-05`, logFC `-0.358` |
| `Mapt` | 1 | self-transcript only; `Mapt` p-adj `1.43e-05`, logFC `-0.533` |
| `Map6` | 0 | no focal call; self transcript p-adj `0.330` |
| `Stmn2` | 1 | self-transcript only at the 0.05 threshold; `Stmn2` p-adj `1.58e-20`, logFC `-1.001` |
| `Tuba1a` | 7 | self plus reciprocal tubulin-paralog program |
| `Tubb5` | 1 | self-transcript only; `Tubb5` p-adj `7.71e-23`, logFC `-1.478` |

The selected same-experiment corpus Findings, used as interpretations of those training measurements rather than independent replication, agree that most MAP or tubulin-neighborhood losses are buffered in postnatal neuronal snRNA profiles:

- `Map1b` was transcript-self-only in `151` and `155`, with no non-`Map1b` FDR<0.10 downstream transcript in any group.
- `Map6` was a complete downstream transcriptomic null across all recovered groups.
- `Mapt` produced no FDR-resolved downstream transcriptional response in any measured neuronal group.
- `Tuba1a` was the exceptional structural tubulin with a small tubulin-paralog compensation program.

I also checked migration/reelin/PAK-Rac relatives in the same count table:

| comparator | `n_degs` in `151` |
|---|---:|
| `Dab1` | 0 |
| `Reln` | 0 |
| `Rac1` | 0 |
| `Pak1` | 1 |
| `Pak2` | 0 |
| `Pak3` | 0 |
| `Gsk3b` | 6 |
| `Ppp2r2b` | 0 |
| `Ppp2r5d` | 0 |

`Dctn1` was the main high-count cytoskeletal exception in this search (`n_degs = 75` in `151`), but its Parquet rows were a sterol/cholesterol and vesicle/lysosome response (`Insig1`, `Msmo1`, `Hmgcs1`, `Hmgcr`, `Fdft1`, `Ldlr`, etc.), and corpus Findings likewise tie it to dynactin/trafficking rather than generic microtubule binding. I did not treat it as a magnitude analogue for `Dcx`.

## Forecast

The point forecast is **1 DEG**.

My synthesis is that acute `Dcx` loss in P16-P44 thalamic neurons is much more likely to be a floor response than a broad state: the adult matched context is not a developmental migration state, close MAP/tubulin-neighborhood training perturbations are mostly null or self-only, and migration/reelin/PAK-Rac pathway targets are also flat in `151`.

I chose 1 rather than 0 because `Dcx` has measurable focal expression in nearly half of non-target nuclei, pre-existing DCX stock should not persist to harvest in edited expressing cells, and the best expressed MAP comparators in this assay often register exactly one DEG through their own knocked-down transcript while still producing no downstream program.
