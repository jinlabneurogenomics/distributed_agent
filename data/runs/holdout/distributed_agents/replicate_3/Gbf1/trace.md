# Gbf1 DEG-count prediction trace

## Question interpreted

The requested held-out target list contains one perturbation, `Gbf1`.  I need to
predict the integer number of genes that would pass `pvals_adj < 0.05` in
`151 TH Prkcd Grin2c Glut` after acute AAV-CRISPR loss of `Gbf1`.
The `Gbf1` rows themselves are held out, so I treated the supplied parquet and
the `151 TH Prkcd Grin2c Glut` training-count CSV as evidence only from other
perturbations.

The count being predicted is a screen endpoint, not a direct GBF1 activity,
protein, viability, or editing-efficiency measurement.  A zero prediction means
that no measured transcript is expected to survive Benjamini-Hochberg correction
at 0.05 in this focal cell group.

## Sources used

- Input manifest: `090_Gbf1.csv`; this established that the only held-out
  target for this run is `Gbf1`.
- Focal training counts:
  `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.  I used the observed
  `n_degs` for mechanistically related, non-held-out perturbations in the
  exact cell group to be predicted.
- Differential-expression parquet:
  `training_de_all_cell_groups.parquet`.  I used rows from
  `151 TH Prkcd Grin2c Glut` to compare the log-fold-change signatures of
  selected Golgi, ER-Golgi, COPI/COPII, COG/SNARE, GARP/retromer, and ER-stress
  perturbations.
- Distributed Agents same-experiment corpus release
  `perturbai-july-260713-sourceguard-1773-v1`.  This release has no held-out
  `Gbf1` context, but it does contain bottom-up findings and claims for the
  observed ER-Golgi/Golgi perturbations: `Copa`, `Copg1`, `Cog4`, `Cog5`,
  `Stx5a`, `Sar1b`, `Sec23a`, `Tmem165`, and `Trip11`.
- Distributed Agents runtime profile tools.  I used these to compute profile comparisons
  from the held-in focal-cell signatures; priors from gene function were not
  mixed into these observed profile calculations.
- External mechanism from PubMed-indexed literature:
  - Kawamoto et al. 2002, DOI `10.1034/j.1600-0854.2002.30705.x`: GBF1 is a
    cis-Golgi ARF guanine-nucleotide exchange factor involved in ARF/COPI
    membrane recruitment.
  - Garcia-Mata et al. 2003, DOI `10.1091/mbc.e02-11-0730`: GBF1 regulates
    ARF/COPI-dependent ER-Golgi intermediate formation, COPI recruitment, and
    Golgi integrity.
  - Szul et al. 2005, DOI `10.1111/j.1600-0854.2005.00282.x`, and Zhao et al.
    2006, DOI `10.1242/jcs.03173`: GBF1 dynamically cycles on early secretory
    membranes and supports sustained ARF activation/COPI recruitment.
  - Jackson 2014, DOI `10.4161/21592780.2014.943616`, and Bhatt et al. 2019,
    DOI `10.1091/mbc.E18-11-0711`: in the secretory pathway GBF1 activates ARF
    proteins at the cis-Golgi/Golgi continuum, thereby linking it upstream of
    COPI and other ARF effectors.

## Computational checks over the training data

The focal count file has 1,674 held-in targets.  It is sparse in the requested
cell group: 1,205 targets have `n_degs = 0`, the median is 0, the mean is 14.05,
and the maximum is 2,677.

I first pulled the focal `n_degs` for pathway neighbors selected from GBF1's
known role in cis-Golgi ARF/COPI recruitment and early secretory traffic:

| training perturbation | focal `n_degs` | interpretation for `Gbf1` |
| --- | ---: | --- |
| `Copa` | 0 | COPI coat subunit, direct downstream machinery for GBF1-ARF signaling |
| `Copg1` | 1 | second measured COPI coat subunit; only a singleton response |
| `Sec23a` | 0 | COPII ER-exit comparator |
| `Sar1b` | 0 | COPII-initiation comparator |
| `Tfg` | 0 | ER-exit/COPII-region comparator |
| `Stx5a` | 0 | ER-Golgi SNARE comparator |
| `Stx16` | 1 | Golgi/endosomal SNARE comparator |
| `Cog4` | 0 | COG Golgi tethering comparator |
| `Cog5` | 0 | COG Golgi tethering comparator |
| `Trip11` | 0 | cis-Golgi/GMAP-210 trafficking comparator |
| `Tmem165` | 0 | Golgi glycosylation-homeostasis comparator |
| `Dpm1` | 0 | glycosylation/CDG comparator |
| `Atp2c1` | 1 | Golgi Ca/Mn pump comparator |
| `Vps53` | 0 | GARP endosome-to-TGN comparator |
| `Vps35` | 17 | retromer counterexample showing some trafficking genes can score |
| `Vps54` | 31 | GARP counterexample with a larger but still non-COPI surface |
| `Cltc` | 3 | clathrin/adaptor counterexample, sparse in the focal group |
| `Vcp` | 2 | ERAD/proteostasis-adjacent counterexample, sparse here |
| `Hspa5` | 5 | direct ER chaperone perturbation; small UPR/proteostasis positive control |
| `Sec63` | 11 | ER-translocation perturbation; small ER-stress positive control |
| `Gfpt1` | 311 | strong hexosamine/UPR positive control |

I then asked Distributed Agents runtime to compare the focal log-fold-change signatures of
these 21 training perturbations in `151 TH Prkcd Grin2c Glut`.  Of this
hand-curated traffic/stress cohort, 11/21 profiles had no FDR-significant
features, 6/21 had 1-9, 3/21 had 10-49, and only `Gfpt1` had at least 50
significant features.  A direct inspection of five GBF1-relevant anchors
confirmed 0 significant features for `Copa`, `Cog4`, `Stx5a`, and `Sec23a`,
and one significant down feature for `Copg1`, across 17,259 measured genes.
Across the 50 comparisons between those five anchors and ten Golgi/COPII/UPR
peers, no pair shared an FDR-significant feature in the same direction.  Thus,
the apparent pathway cohort did not contain a recurring corrected COPI or
ER-Golgi stress signature.

The Distributed Agents corpus agreed with that direct profile check.  Its ER-Golgi claim
states that the represented ER-Golgi transport, COPI, COG, SNARE, and
Golgi/CDG perturbations "do not produce a shared broad secretory-pathway
transcriptional module in postmitotic neurons."  Specific same-experiment
findings for `Copa`/`Copg1` reported no shared COPI-collapse transcriptional
signature, for `Stx5a` reported that COG, COPI, `Sar1b`, `Vcp`, and `Stx16`
failed to phenocopy the two isolated `Stx5a` singleton genes, and for
`Trip11`, `Cog4`, `Tmem165`, `Sar1b`, and `Sec23a` reported pan-neuronal or
near-null profiles despite their secretory-pathway biology.

## Target-specific reasoning

### Gbf1

GBF1 is upstream of COPI coat recruitment: its Sec7 ARF-GEF activity activates
ARF proteins on early secretory/Golgi membranes, and active ARF recruits COPI.
A severe GBF1 block can therefore disrupt ER-to-Golgi intermediates, Golgi
architecture, secretion, and ARF-effector localization.  The direct biological
expectation before looking at this dataset is not that `Gbf1` is inert.

The focal training set, however, argues that this expectation usually does not
become a broad 3-4 week postnatal neuronal nuclear-RNA response.  The two
closest represented COPI coat perturbations are `Copa` and `Copg1`; they have
0 and 1 DEGs respectively in `151 TH Prkcd Grin2c Glut`, and the same-experiment
corpus specifically rejects a reproducible `Copa`/`Copg1` COPI-collapse
phenocopy.  The upstream/downstream early-secretory comparators are also flat in
the focal group: `Sec23a`, `Sar1b`, `Tfg`, `Stx5a`, `Cog4`, `Cog5`, `Trip11`,
and `Tmem165` all have 0 DEGs.  This matters more than a generic Golgi prior:
these are the observed outputs of the same AAV-CRISPR, postmitotic neuronal
assay and the same cell group or closely matched neuronal groups.

I treated `Vps35`, `Vps54`, `Gfpt1`, `Hspa5`, and `Sec63` as counterexamples,
not as the main analogs.  They show that trafficking or ER-proteostasis genes
can create nonzero focal responses, so the zero calls for COPI/COG/COPII nodes
are not due to a powerless DE pipeline.  They are weaker predictors of `Gbf1`,
because `Vps35`/`Vps54` operate more in retromer/GARP endosome-to-TGN traffic
and because `Gfpt1`, `Hspa5`, and `Sec63` are direct ER stress or glycosylation
stress perturbations rather than ARF/COPI recruitment factors.  If GBF1 loss in
the surviving nuclei produced a canonical UPR/ISR rebound, the profile should
look more like those nonzero controls; instead, its immediate COPI and early
Golgi analogs were flat or singleton-only.

Those observations make a broad GBF1 response unlikely.  A one-gene response
like `Copg1` or `Stx16` is possible, but there was no shared corrected feature
across the direct observed analogs, and the requested output is an integer point
estimate.  I therefore predict that no gene crosses FDR 0.05 for held-out
`Gbf1`.

Prediction: `Gbf1` -> `0`.

## Limits and extrapolation

- `Gbf1` itself, `Arf1`/`Arf3`/`Arf4`/`Arf5`, and the most direct BIG-family
  ARF-GEF comparisons were absent from the focal training counts I queried, so
  the prediction is transferred through COPI coat, COG/SNARE, and ER-exit
  neighbors rather than a measured ARF-GEF paralog.
- GBF1 sits upstream of multiple ARF effectors and can be more pleiotropic than
  knocking out one coatomer subunit.  A stronger, earlier, or non-neuronal
  GBF1 perturbation could induce Golgi collapse, UPR, or cell death that this
  sparse P16 NeuN+ screen would not report as a recovered-nucleus DEG count.
- The data measure nuclear RNA at one 3-4 week endpoint and do not measure
  indel burden, GBF1 protein, Golgi morphology, cargo flux, glycosylation, or
  transient stress.  A zero-DEG transcriptome is therefore compatible with a
  protein-level trafficking defect.
- The distinction between exactly 0 and a 1-gene singleton is inherently noisy
  in this assay.  I chose 0 because the closest training nodes in the focal
  group are dominated by strict zeros and their rare singletons were
  target-private rather than a recurrent GBF1/COPI signature.
