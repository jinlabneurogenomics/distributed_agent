# Zfp398 n_degs forecast

## Target and endpoint

- Manifest target: `Zfp398`
- Focal class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes in this focal class with Wilcoxon `pvals_adj < 0.05`
- Point prediction: `0`

## Evidence used

The biology-only Zfp398 bundle supports target accessibility but not a strong matched
thalamic-neuron response prior:

- Exact in-assay non-target expression is present in the focal class
  (`mean_cp10k = 1.0305`; 17,892 of 23,679 non-target nuclei expressing,
  75.56%).
- Zfp398 is annotated as a KRAB/C2H2 nuclear transcription regulator, so a
  disruptive P16 edit should stop new functional protein production rather than
  remove a stable installed structure.
- The functional-stock card judged the operative stock likely substantially
  depleted by the P37-P44 harvest, but only with partial, low-confidence kinetic
  evidence: no Zfp398-specific protein half-life, chromatin residence time, or
  matched post-edit clearance clock was found.
- No transferable postnatal thalamic-neuron loss phenotype was found. Adult
  thalamic expression establishes reach but not ongoing functional demand.

The declared training count table for this exact class is strongly zero-heavy:

- 1,674 visible training perturbations.
- 1,205/1,674 have `n_degs = 0`.
- Median `n_degs = 0`; 75th percentile = 1; 90th percentile = 2; 95th
  percentile = 18.
- The large upper tail is formed by high-impact nuclear transport, splicing,
  proteasome, ubiquitin, and chromatin regulators such as `Uba5`, `Tpr`,
  `Sin3a`, `Rnpc3`, `Zbtb7a`, and `U2af2`, which are not close analogs for the
  poorly characterized sequence-specific Zfp398 perturbation.

I used the visible `Zfp*` perturbations as the closest measured local family
check rather than fitting to the global long tail:

- 30 `Zfp*`/`Zfpm2` rows are present in the count table.
- 25/30 have `n_degs = 0`.
- The five nonzero cases are `Zfp612 = 1`, `Zfp692 = 1`, `Zfp148 = 8`,
  `Zfp236 = 19`, and the outlying `Zfp423 = 150`.
- Excluding the atypically broad `Zfp423` case, the local set has a mean of
  1.0 and a median of 0.

The endpoint Parquet confirmed the same class-specific counts for that Zfp
cohort. Each visible Zfp target had 17,259 measured features in
`151 TH Prkcd Grin2c Glut`, and their matched perturbed nuclei spanned 64-283
against 23,679 matched controls, so the local zero pattern is not just a missing
row artifact.

## Synthesis

Zfp398 is expressed and likely functionally depleted enough that a transcriptional
effect is plausible. The limiting evidence is biological demand: the bundle has
no matched postnatal neural loss phenotype, no known same-context target program,
and no close compensating paralog test. In the exact endpoint, most biological
targets are quiet and the measured Zfp-family perturbations overwhelmingly sit
at zero, with only single-digit to low-double-digit responses aside from one
atypical broad regulator.

I therefore placed Zfp398 at the local Zfp-family mode and global median rather
than assigning it to the high-DEG essential-machinery tail. A small response of
one or a few DEGs remains plausible, but the best integer forecast for the held
out `151 TH Prkcd Grin2c Glut` count is:

`predicted_n_degs = 0`
