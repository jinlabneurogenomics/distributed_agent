# Pik3ca DEG-count forecast

## Target and endpoint

- Target: `Pik3ca`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Forecast: `0`

## Evidence used

### Outcome-blind target biology

The canonical `Pik3ca` bundle exposes in-assay reach but not the held-out differential-expression outcome. `Pik3ca` is expressed in this focal non-target population in `16402 / 23679` nuclei, or `69.27%`, with mean `1.34` raw UMI and pseudobulk `83.97` CPM. The bundle therefore supports target reach in the assayed thalamic population.

The same bundle describes `Pik3ca` as the p110-alpha catalytic subunit of class IA PI3K. Its functional-stock adjudication says the P16 disruptive edit should stop new p110-alpha supply and that the renewable catalytic stock is likely substantially depleted by the P37-P44 harvest, although the timing evidence is partial and not measured directly in juvenile thalamic neurons. Its observability card gives only low-confidence support for a postnatal neural phenotype from hypothalamic POMC/AgRP loss and leaves thalamic latency and compensation unresolved.

This made a silent response plausible rather than forcing a failed-edit interpretation: the perturbation is likely reachable, but p110-alpha loss can be buffered by PI3K isoforms/regulatory complexes or expressed as phosphoinositide and phosphorylation changes without a basal nuclear-RNA footprint.

### Training count table and PI3K-centered analogs

The `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains `1674` training perturbations. It is strongly zero-inflated: median `n_degs = 0`, only `469` targets have at least one DEG, and only `106` have at least `10`.

I nominated training-available analogs from typed curated relationships using `gene-analog-nomination-skill`, with the full count table as the training universe. The strongest close PI3K-core and immediate-pathway rows were almost all silent in the focal count table:

| training target | relationship to the PI3K axis | focal `n_degs` |
| --- | --- | ---: |
| `Pik3cb` | p110 catalytic isoform and close class IA PI3K module member | 0 |
| `Pik3r1` | p85 regulatory subunit in exact PI3K complexes | 0 |
| `Ptpn11` | receptor/MAPK/PI3K-adjacent module member | 0 |
| `Igf1r` | upstream receptor module member | 0 |
| `Insr` | upstream receptor module member | 0 |
| `Pik3r2` | p85 regulatory subunit in exact PI3K complexes | 0 |
| `Hras` | upstream Ras module member | 0 |
| `Irs1` | upstream insulin-receptor substrate module member | 0 |
| `Mapk1` | MAPK branch member | 0 |
| `Mtor` | downstream mTOR hub | 2 |
| `Akt3` | AKT branch member | 0 |
| `Rptor` | mTORC1 component | 0 |

Among the first 10 nominated training genes the total DEG count was `1`; among the first 20 it was only `7`, with `Mtor = 2` and `Map2k1 = 4` being the only clearly proximal nonzero rows. `Tsc2` had `86` DEGs, but it ranked lower as a downstream mTORC1 brake and is mechanistically an activating mTOR-state perturbation rather than a direct class IA PI3K catalytic loss comparator.

I checked the training parquet for these same rows in `151 TH Prkcd Grin2c Glut`; it exactly supported the count-table calls. `Pik3cb`, `Pik3r1`, `Pik3r2`, `Mapk1`, `Raf1`, `Akt3`, and `Rptor` had zero BH `< 0.05` genes. `Mtor` had only two genes, `Rims3` and `Tmed8`, below BH `0.05`; `Map2k1` had four, and `Gsk3b` had six.

### Same-experiment corpus context for training comparators

The selected same-experiment corpus, queried only for training genes, describes the direct PI3K core as broadly flat in this screen:

- `Pik3cb` had no FDR-level downstream transcriptional response in any of 22 recovered neuronal cell groups.
- `Pik3r1` was pan-neuronally FDR-flat.
- `Pik3r2` was transcriptionally buffered across recovered neuronal groups.
- `Akt3` was all-null, and a packaged comparison noted that `Pik3cb`, `Pik3r1`, `Pik3r2`, and `Rptor` were all flat PI3K/AKT/mTOR relatives.
- The `Mtor` report explicitly separated weak `Mtor` detectability from the flat direct pathway comparators: `Rptor`, `Akt3`, `Pik3cb`, `Pik3r1`, and `Pik3r2`.

Thus the same-experiment semantic layer did not supply a hidden `Pik3ca` outcome, but it did reinforce that class IA PI3K loss-of-function is commonly buffered in this P16-to-P37/P44 sparse neuronal snRNA endpoint.

### Observed profile check

I symmetrically compared a 16-node nominated PI3K/MAPK/mTOR cohort in the training parquet for the exact focal group. Twelve of the 16 biologically nominated nodes had `0` significant features; three had `1-9`; only `Tsc2` had at least `50`. In a bounded profile inspection, the focal direct PI3K-core nodes had:

| node | significant features |
| --- | ---: |
| `Pik3cb` | 0 |
| `Pik3r1` | 0 |
| `Pik3r2` | 0 |
| `Mtor` | 2 |
| `Tsc2` | 86 |

There was no recurrent significant PI3K-core feature set to transfer to `Pik3ca`; the only stronger response, `Tsc2`, reflected a more distal and directionally different mTOR-control state.

## Synthesis

`Pik3ca` is expressed in the focal thalamic nuclei, and p110-alpha should be depleted in successfully edited cells by harvest, so I did not treat a zero prediction as an editing-failure default. The quantitative endpoint, however, is steady-state survivor nuclear RNA, and every direct training proxy for basal class IA PI3K loss was silent: the p110-beta catalytic isoform, p85-alpha, p85-beta, AKT3, and RAPTOR all had `0` focal DEGs, with `Mtor` only barely nonzero.

The rare larger mTOR-axis response after `Tsc2` was not enough to move the forecast upward. `Tsc2` releases mTORC1 repression rather than removing a catalytic PI3K subunit, and the count/parquet/corpus evidence showed that direct PI3K-core perturbations did not phenocopy it. The biology bundle supplies reach and plausible stock depletion, but the training measurements say this axis is usually buffered or off the basal snRNA axis in the exact juvenile thalamic endpoint.

I therefore placed the point estimate at the mode of the closest measured analogs:

`predicted_n_degs = 0`
