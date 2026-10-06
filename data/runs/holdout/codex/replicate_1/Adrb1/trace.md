# Direct DEG-count forecast for Adrb1

## Target and endpoint

- Manifest target: `Adrb1`.
- Requested endpoint: `n_degs` for `151 TH Prkcd Grin2c Glut`, the number of measured genes with Wilcoxon BH-adjusted `p < 0.05`.
- `Adrb1` was absent from the declared focal-class training count table, so the target endpoint was not read from training rows.

## Biology used

- The canonical biology bundle identifies `Adrb1` as a catecholamine-responsive beta-1 adrenergic GPCR that signals through Gs/cAMP.
- The focal in-assay expression reach is real but partial: `Adrb1` was detected in 9,071 of 23,679 non-target nuclei in `151 TH Prkcd Grin2c Glut` (`38.308%`), with mean CP10K `0.3283`, pseudobulk CPM `33.789`, and mean raw UMI `0.5391`.
- Functional stock was adjudicated as likely substantially depleted by the 21-28 day harvest because editing stops new intact receptor synthesis, the only measured total-receptor half-life is much shorter than the perturbation interval, and a four-week postnatal neuronal deletion produced an Adrb1-dependent mPFC phenotype.
- The same bundle also leaves major reasons to expect a small transcriptional endpoint: the receptor is a neuromodulatory input rather than core expression machinery, available thalamic evidence establishes expression but not broad receptor dependence, and the mPFC and HeLa facts do not prove a juvenile thalamic steady-state nuclear RNA response.

## Training measurements used

The declared focal count table contains 1,674 observed training perturbations. It is strongly zero-inflated in this cell class:

- 1,205 / 1,674 targets have `n_degs = 0`.
- 1,481 / 1,674 have `n_degs <= 1`.
- The median and 75th percentile are 0 and 1; the 90th and 95th percentiles are 2 and 18.
- Only 59 / 1,674 have `n_degs >= 50`, with the large mean, 14.054, driven by a long tail up to 2,677.

The closest count-table entries to a beta-adrenergic Gs/cAMP perturbation were almost all silent in the same focal group:

- Beta/adrenergic receptors: `Adrb2 = 0`, `Adrb3 = 0`, `Adra1a = 0`, `Adra2a = 0`, `Adra2b = 0`.
- Immediate Gs/cAMP/Rapgef/PDE pathway entries: `Gnas = 0`, `Gnal = 0`, `Adcy1 = 0`, `Adcy3 = 0`, `Adcy5 = 0`, `Rapgef2 = 0`, `Rapgef4 = 0`, `Pde4b = 0`, `Pde4d = 0`.
- Other neuromodulatory GPCRs in the table were similarly quiet: `Drd2`, `Drd4`, `Drd5`, `Chrm2`, `Chrm3`, all assayed serotonin receptors, all assayed opioid receptors, all three assayed NPY receptors, and `Sstr5` were `0`.

I also compared 48 observed GPCR/cAMP-related perturbation profiles directly in the expression Parquet for `151 TH Prkcd Grin2c Glut`. Forty of the 48 had no BH-significant genes, and the remaining eight were only in the 1-9 significant-gene range. A focused Parquet inspection of `Adrb2`, `Gnas`, `Adcy1`, `Rapgef2`, and `Pde4d` confirmed that each had zero significant measured genes across 17,259 features in the exact focal profile.

## Forecast

The biology makes successful receptor loss plausible: `Adrb1` is expressed in a sizeable minority of the recovered focal nuclei and pre-edit receptor stock should not persist for the full 3-4 week interval. The quantitative scale, however, is dominated by the focal class's heavy zero mass and by the silence of the nearest receptor and Gs/cAMP training perturbations, including the related `Adrb2`.

I therefore forecast a null measured DEG burden rather than placing `Adrb1` in the sparse high-response tail.

`predicted_n_degs = 0`
