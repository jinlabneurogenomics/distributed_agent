# Nr1h3 n_degs prediction trace

## Target and safe biology

- **Held-out target:** `Nr1h3`, from the one-row manifest `Nr1h3.csv`.
- **Requested context:** `151 TH Prkcd Grin2c Glut`.
- **Endpoint:** number of measured genes in that context with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- **Safe target bundle used:** `[local file: Nr1h3.json]`, also served through `characterization_bundle(target="Nr1h3", view="biology")` with `target_outcome_exposed=false`.

The target card made `Nr1h3` a plausible but weakly expressed acute postnatal neuronal perturbation. LXR-alpha is an RXR-heterodimerizing transcription factor, and a P16 disruptive edit should block new intact receptor production; because the 21-28 day edit-to-harvest interval is longer than the 9-day adult mouse brain average protein lifetime, the bundle adjudicated operative stock as likely substantially depleted by harvest. The main negative bearings were endpoint reach and demand: direct single-gene `Nr1h3` loss evidence was hepatic/systemic rather than neural, LXR-beta/Nr1h2 could buffer the pathway, no matched postnatal thalamic latency evidence was available, and exact focal expression was very sparse: 843 of 23,679 matched non-target nuclei expressed `Nr1h3` RNA, or 3.560%, with mean raw UMI 0.0381 and pseudobulk 2.39 CPM.

## Training measurements used

I used the declared focal count table:

`[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`

This table contains 1,674 visible target counts for `151 TH Prkcd Grin2c Glut`. Its empirical distribution was sparse:

- 1,205 / 1,674 targets had `n_degs = 0`;
- median = 0, 75th percentile = 1, 90th percentile = 2;
- only 83 / 1,674 targets exceeded 50 DE genes.

The hand-selected LXR/RXR and lipid-axis rows were:

| visible training target | `n_degs` |
|---|---:|
| `Nr1h2` | 0 |
| `Rxra` | 0 |
| `Rxrb` | 0 |
| `Rxrg` | 0 |
| `Abca1` | 0 |
| `Srebf1` | 0 |
| `Hmgcr` | 0 |
| `Srebf2` | 7 |
| `Thra` | 3 |
| `Nr3c1` | 0 |
| `Rora` | 278 |
| `Nr1d1` | 116 |

I then checked the declared training Parquet,

`[local file: training_de_all_cell_groups.parquet]`,

for those same targets in the focal group. Each selected target had 17,259 measured-gene rows. The direct LXR/RXR controls were all FDR-flat in `151`: `Nr1h2`, `Rxra`, `Rxrb`, `Rxrg`, `Abca1`, and `Srebf1` had zero genes at `pvals_adj < 0.05`; `Srebf2` had 7, and its leading significant rows were the expected negative sterol-biosynthesis features, including `Dhcr24`, `Insig1`, `Hmgcs1`, and `Msmo1`. Thus the table can detect a neuronal sterol module in this class, but single loss of the LXR-beta paralog, RXR partners, or an efflux target did not engage it.

## Corpus and profile interpretation

The same-experiment corpus reports used only visible training perturbations:

- `Nr1h2:F001-F003`: `Nr1h2` produced no downstream FDR<0.10 gene in any of the 23 measured groups, expected LXR cholesterol-efflux and sterol-regulatory transcripts were absent, and represented LXR/RXR perturbations did not reveal a hidden juvenile neuronal LXR/RXR module.
- `Rxra:F001-F003`: `Rxra` produced no robust downstream neuronal transcriptome in any of the 23 groups and lacked the expected neuronal LXR/RXR `Apoe-Abca1` cholesterol axis.
- `Srebf2:F001-F002`: direct `Srebf2` loss down-regulated a compact sterol-biosynthesis mRNA module, proving that this snRNA-seq surface is not generically blind to cholesterol transcription when the transcriptional driver is engaged.
- `Rora:F001-F005`: `Rora` produced a large, selective `151` thalamic signature, whereas `Rorb` and `Rorc` failed to phenocopy it; this made the `Rora`/`Nr1d1` high-count nuclear-receptor cases poor donors for `Nr1h3`.

I also compared 17 visible nuclear-receptor/lipid profiles in the focal Parquet. The profile audit found 13/17 with no significant focal features, two with 1-9 significant features, and only `Rora` plus `Nr1d1` in the >=50-feature class. Whole-profile cosines between `Srebf2` or the active `Rora`/`Nr1d1` controls and the LXR/RXR rows were near zero: for example, `Rxra`-`Srebf2` cosine was 0.006, `Nr1h2`-`Srebf2` was 0.043, and `Rora`-`Rxrg` was -0.081. I therefore treated `Srebf2`, `Rora`, and `Nr1d1` as assay-positive boundaries rather than magnitude donors for `Nr1h3`.

## Forecast

The upward case is that `Nr1h3` encodes a renewable transcription factor and the edit-to-harvest window should be long enough to deplete LXR-alpha protein. That was outweighed by focal evidence that the target is expressed in only a small minority of the matched thalamic nuclei, by lack of matched postnatal neuronal demand evidence, and most importantly by the measured silence of the closest visible `Nr1h2`/`Rxra`/`Rxrb`/`Rxrg` single perturbations under the same acute neuronal assay. The best point estimate is therefore the direct-analogue mode rather than a small SREBP2-like sterol response.

**Predicted `Nr1h3` `n_degs`: 0**
