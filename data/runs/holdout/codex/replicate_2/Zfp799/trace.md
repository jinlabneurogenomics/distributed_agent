# Direct forecast trace

## Target and endpoint

- Target: `Zfp799`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`

## Evidence used

1. **Declared target bundle**

   The one-row holdout manifest and canonical biology bundle both identify the held-out perturbation as `Zfp799`; no target expression signature or target DEG count was exposed.

   In the exact focal population, `Zfp799` was a measured, well-detected transcript in matched non-targeting nuclei: 19,788 of 23,679 nuclei expressed the gene, 83.57% of the population, with mean expression 2.13 raw UMI and 1.37 CP10k.

2. **Biology prior for the perturbation**

   The bundle annotates ZFP799 as a nuclear KRAB/C2H2 zinc-finger protein predicted to regulate RNA polymerase II transcription. A disruptive edit should stop new protein supply, and the P16-to-P37/P44 interval is long enough that a soluble nuclear protein could substantially turn over. That makes the perturbation biologically plausible in recovered neurons.

   The same bundle did not find a Zfp799-specific postnatal neural loss phenotype, a thalamic perturbation study, a tested compensating paralog, or a ZFP799-specific half-life / DNA-residence measurement. Thus expression and plausible stock depletion do not establish that thalamic postmitotic neurons have an ongoing high-scope requirement for ZFP799.

3. **Training-count base rate in the exact cell group**

   I used the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table, which contains 1,674 held-in perturbations.

   - 1,205 / 1,674 training targets, 72.0%, had `n_degs = 0`.
   - 1,481 / 1,674, 88.5%, had `n_degs <= 1`.
   - The median was 0; the 75th percentile was 1; the 90th percentile was 2.
   - A small tail of broad responses dominated the mean: 58 / 1,674 targets had more than 25 DEGs.

4. **Held-in zinc-finger comparators in the expression parquet**

   I queried the declared training Parquet in the `151 TH Prkcd Grin2c Glut` context for the held-in `Zfp*` targets, retaining significant rows plus each self row. The count table and Parquet agreed that the closest simple family slice was mostly null:

   - 25 / 30 `Zfp*` held-in targets had 0 DEGs.
   - 2 / 30 had exactly 1 DEG: `Zfp612`, `Zfp692`.
   - Two had modest but still sparse signals: `Zfp148` with 8 and `Zfp236` with 19.
   - One was a clear outlier: `Zfp423` with 150 in the BH<0.05 count table.

   The packaged same-experiment report for `Zfp423` treats its 151 thalamic response as a specific developmental / identity and surface-remodeling program, with no phenocopy from obvious relatives such as `Zfp521`, EBF/BMP-SMAD/RA/Zic-pathway perturbations, or `Chd4`. I therefore used `Zfp423` as evidence that the assay can detect large zinc-finger-linked thalamic responses, but not as a close quantitative analogue for a poorly characterized KRAB/C2H2 regulator.

## Synthesis

The endpoint prior in this cell group is sharply zero-inflated. `Zfp799` is genuinely expressed in the focal thalamic nuclei and should be perturbable by P37-P44, so I did not treat it as an unavailable or failed perturbation. However, the biology bundle leaves its postnatal thalamic requirement unresolved, and the observed held-in `Zfp*` perturbations are overwhelmingly at zero with only rare named outliers. That combination supports a near-null expectation.

I assign a one-gene point rather than a broad response: one DEG keeps the forecast above a pure expression-absent null while staying at the floor of the observed nonzero zinc-finger and whole-training distributions.

Predicted `n_degs`: `1`
