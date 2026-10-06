# Ppp2r1a n_degs forecast trace

## Target and endpoint

- Manifest target: `Ppp2r1a`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in that focal population.
- The target perturbation profile and target count were not used.

## Evidence used

### Ppp2r1a biology bundle

The declared biology-only bundle identifies Ppp2r1a as the PP2A A-alpha scaffold subunit. This is a shared dynamic-complex component rather than a single terminal transcription factor: A-alpha coordinates the catalytic C subunit with interchangeable B subunits across PP2A holoenzymes.

Exact same-assay target reach in `151 TH Prkcd Grin2c Glut` was high:

- `pct_cells_expressing = 94.0031`
- `mean_raw_umi = 4.3998`
- `mean_log1p_cp10k = 1.1938`
- `pseudobulk_cpm = 275.7488`

The functional-stock adjudication was also positive for realization by harvest. The card used PP2A holoenzyme remodeling plus a bulk thalamus Ppp2r1a protein `T50` of 5.7435 days; over the P16 to P37-P44 interval this spans about 3.66 to 4.88 half-lives, so a successful disruptive edit should substantially deplete pre-edit A-alpha. That argues against treating the P16 perturbation as too slow to matter.

The biology bundle also gives two dampening caveats that are directly relevant to a DEG-count forecast:

- Ppp2r1b/A-beta can provide partial scaffold reserve after A-alpha loss and is present in thalamus, although not as a complete equivalent.
- The strongest neural phenotype evidence comes from developmental forebrain excitatory-neuron conditional deletion, not an acute P16 thalamic time course, so it does not establish that a broad survivor RNA program must appear within 21 to 28 days.

### Training count table

The declared focal count table contains 1,674 training perturbations. Counts in this cell class are highly sparse:

- 1,205/1,674 have `n_degs = 0`.
- 276/1,674 have `n_degs = 1`.
- The median is 0, the 75th percentile is 1, the 90th percentile is 2, and the 95th percentile is 18.

The closest observed phosphatase and PP2A-related rows are all low:

| target | interpretation for Ppp2r1a forecast | n_degs |
|---|---:|---:|
| Ppp2r2b | PP2A B55 regulatory subunit, narrower than A-alpha scaffold | 0 |
| Ppp2r5d | PP2A B56 regulatory subunit, narrower than A-alpha scaffold | 0 |
| Ppp3ca | calcineurin catalytic subunit, phosphatase signaling control | 4 |
| Ppp3r1 | calcineurin regulatory subunit, phosphatase signaling control | 9 |
| Ppp3cc | calcineurin catalytic paralog, phosphatase signaling control | 0 |
| Ppm1g | serine/threonine phosphatase control | 3 |

Nearby Ca/calmodulin and kinase-signaling perturbations were also mostly in the 0 to 6 range, with only a few broader controls such as `Calm1` at 14, `Tsc2` at 86, and `Grin1` at 89. `Tsc2` and `Grin1` show that this thalamic class can report large signaling/receptor programs, but their mTOR and NMDA-receptor mechanisms are less directly scale-matched to PP2A A-alpha scaffold loss than the quiet PP2A/phosphatase rows.

### Same-context Parquet spot checks

The focal Parquet profiles agreed with the count table for the hand-selected PP2A/phosphatase cohort. In `151 TH Prkcd Grin2c Glut`, `Ppp2r2b` and `Ppp2r5d` each had 17,259 measured genes, 0 FDR-significant genes, and minimum adjusted p-values of 0.3617 and 0.4050. Their matched perturbed-cell counts were 151 and 141, comparable to other low but nonzero signaling controls such as `Ppm1g` with 182 perturbed cells and 3 DEGs.

The same query gave low single-digit significant counts for `Ppp3ca`, `Ppp3r1`, and `Ppm1g` and did not reveal a recurrent high-amplitude PP2A-like transcriptional program. A bounded profile comparison of 20 PP2A, phosphatase, Ca/calmodulin, MAPK, mTOR, and NMDA controls put six nodes in the `no_significant_features` bucket and eleven in the `1_to_9_significant_features` bucket; the broader `Grin1`/`Tsc2` controls were the only 50-plus DEG rows in that selected cohort.

## Forecast synthesis

The high focal expression and likely protein-stock clearance move `Ppp2r1a` above a hard-zero prediction: the perturbation should engage the A-alpha scaffold in this cell class if editing succeeds. Loss of A-alpha is also broader than loss of one observed B subunit, so the two zero PP2A-regulatory rows should be read as lower-scale boundaries, not as exact donors.

The downward evidence is stronger for scale. The two available PP2A holoenzyme-specific rows are exactly zero, calcineurin and PPM phosphatase rows sit at 0 to 9 DEGs, many CaM/CaMK rows are 0 or 1, and PP2A A-beta reserve plus survivor-conditioned sparse CRISPR should dilute a large acute stress program. No declared training measurement supplied an exact scaffold or catalytic-core PP2A donor with a large response.

I therefore used the low-single-digit phosphatase regime as the center, with a small upward adjustment from the zero PP2A B-subunit rows for Ppp2r1a's broader scaffold role and strong expression reach. The resulting point forecast is:

`predicted_n_degs = 3`
