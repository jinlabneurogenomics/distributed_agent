# Direct forecast trace for Epha7

Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, counted as measured genes with BH-adjusted Wilcoxon `p < 0.05`.

Prediction target and declared-data checks:

- The one-row holdout manifest names `Epha7`.
- `Epha7` is absent from the declared training count table and had 0 rows in the declared training DE Parquet for `151 TH Prkcd Grin2c Glut`, so no held-out target outcome or target expression signature was used.
- The declared `151 TH Prkcd Grin2c Glut` count table contains 1,674 observed training targets. It is zero-inflated: 1,205/1,674 targets have `n_degs = 0`, the median is 0, the 75th percentile is 1, 276 targets have exactly 1 DEG, and only 106 targets have at least 10 DEGs.

Biology for `Epha7`:

- The canonical biology bundle reports broad focal-population transcript reach for `Epha7`: 19,764/23,679 non-target nuclei express it in `151 TH Prkcd Grin2c Glut` (`83.47%`; mean raw UMI 3.21; pseudobulk CPM 200.94).
- EphA7 is a cell-surface ephrin-A receptor with kinase-positive and kinase-negative functional pools. The stock card judged functional stock by harvest as `likely_substantially_depleted`, because a P16 edit should stop renewal of affected receptor isoforms across the 21-28 day interval, but with residual uncertainty from unknown EphA7 isoform turnover and unknown guide placement across isoforms.
- Loss evidence supports neural relevance but does not supply a matched acute transcriptomic effect: the postnatal phenotype is germline cortical loss at P10-P22, and the target-region evidence is embryonic thalamic patterning rather than juvenile thalamic loss after P16 editing.
- `Epha4` is the only explicitly related Eph-family comparator in the bundle; its reported overlap with `Epha7` is developmental thalamic coexpression/function, with no matched evidence that it compensates for juvenile `Epha7` loss.

Training measurements used for scale:

- Observed Eph-family receptor perturbations in the same `151 TH` count table were almost silent: `Epha10 = 0`, `Epha2 = 0`, `Epha3 = 0`, `Epha4 = 1`, `Epha5 = 0`, `Ephb1 = 0`, `Ephb2 = 0`, and `Ephb4 = 0`.
- The single `Epha4` DEG in the focal Parquet slice was the self-transcript row itself (`names = Epha4`, log fold-change `-1.0266`, adjusted `p = 7.88e-32`), so no observed Eph receptor supplied a downstream DEG in this thalamic population.
- A broader hand-defined axon-guidance/surface-receptor neighborhood was also low: 18 semaphorin/plexin/robo/slit/netrin/L1/Nrcam perturbations had mean `n_degs = 0.39`, median 0, and max 2; 14 surface receptor tyrosine kinases had mean `n_degs = 0.21`, median 0, and max 3.
- Self-transcript rows are not a reliable source of a guaranteed count: in the same focal Parquet slice, only 319/1,642 observed self-rows were significant, and seven of the eight observed Eph receptor self-rows were not significant.

Synthesis:

`Epha7` is not an absent or implausible target in this thalamic class: it is expressed in most focal nuclei, is a membrane receptor whose functional stock should be at least partly depleted by P37-P44, and has developmental/postnatal neural phenotypes. Those points keep the forecast above a strict biological null. They are outweighed for the exact `n_degs` endpoint by the measured training scale: the closest Eph receptor perturbations in the same class were 7/8 zeros, the only nonzero Eph receptor count was a self-transcript-only `Epha4` effect, and related guidance/receptor genes almost never exceeded one or two significant rows. Because an acute `Epha7` edit is more likely to produce either no BH-significant row or a lone self row than a broad recovered-nucleus state, and because self-row significance is not assured, I set the point forecast at the integer mode of this local evidence: 0.
