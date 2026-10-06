# Six6 held-out DEG-count prediction

## Question and endpoint

The requested prediction is the integer number of genes expected to pass
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` after CRISPR loss of
`Six6` in the focal `151 TH Prkcd Grin2c Glut` neuronal group. The held-out
`Six6` perturbation itself is absent from both supplied inputs, so its own
signature and observed count were not used. I treated `151 TH Prkcd Grin2c
Glut` as a thalamic glutamatergic class; `TH` is the atlas thalamus token, not
tyrosine hydroxylase.

The observed endpoint is directly present for held-in perturbations in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`. The all-cell differential
expression Parquet is the direct source for exact subthreshold and cross-cell
patterns of candidate analogs. Literature and the July same-experiment corpus
were context for deciding which held-in perturbations were plausible analogs;
they are not independent Perturb-seq measurements.

## Sources used

- Declared focal training DEG counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
- Declared differential-expression Parquet:
  `training differential-expression dataset`
- Requested held-out list:
  `single-target request for Six6`
- Distributed Agents same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`; I queried direct comparator
  summaries for `Six3`, `Pax6`, and `Rax`, and found no `Six6` Finding or
  Claim story in the selected corpus.
- PubMed literature:
  Jean, Bernier, and Gruss 1999, PMID 10473118,
  DOI `10.1016/s0925-4773(99)00068-4`; Gallardo et al. 1999, PMID 10512683,
  DOI `10.1006/geno.1999.5916`; Lopez-Rios et al. 2003, PMID 12441302,
  DOI `10.1242/dev.00185`; Tetreault, Champagne, and Bernier 2008,
  PMID 19146846, DOI `10.1016/j.ydbio.2008.12.022`; Larder et al. 2011,
  PMID 21228153, DOI `10.1523/JNEUROSCI.1688-10.2011`.

## Quantitative calibration

The focal held-in distribution was extremely sparse: 469 of 1,674 training
perturbations had at least one DEG, the median was 0, the 75th percentile was
1, the 90th percentile was 2, and only the upper tail reached hundreds or
thousands of DEGs. A positive prediction for `Six6` therefore needed closer
evidence than membership in a developmental transcription-factor family.

I grouped the declared Parquet rows by `gene_target` and `group_name` and
counted `pvals_adj < 0.05` for eye-field, anterior forebrain, and Six6-network
genes present in the held-in universe. I also extracted the ten smallest
adjusted p-values for the key analogs in `151 TH Prkcd Grin2c Glut` to check
whether the zero counts were near misses.

## Six6 reasoning

### Held-in analogs and counterexamples

The most relevant held-in analog was `Six3`, the closest SIX-family paralog in
the Six3/Six6 subfamily. In the focal class, `Six3` had 167 matched perturbed
nuclei, `n_degs = 0`, and no near-threshold signal: its smallest focal adjusted
p-value was `1.0`. Its ten best focal rows had nominal p-values between
`8.7e-05` and `0.0023` but were all adjusted to `1.0`; the measured `Six6`
row within the `Six3` perturbation had `pvals_adj = 1.0`. Across all measured
cell groups in the declared Parquet, `Six3` produced only one corrected gene,
in `007 L2-3 IT CTX Glut`, not in the focal thalamic class. The July corpus
independently summarized the same-experiment pattern as a single `Slc6a6`
edge for `Six3` in `007 L2-3 IT CTX Glut` and no convergence among unbiased
signature neighbors or represented SIX/homeobox/Wnt-Hh relatives.

`Six5` was a more distant SIX-family counterexample, not a strong mechanistic
analog for `Six6`. It nevertheless checked whether SIX genes as a class were
active in this focal readout. `Six5` had 215 matched perturbed nuclei,
`n_degs = 0`, smallest focal adjusted p-value `1.0`, and no corrected DEGs in
any group found by the bounded scan.

Canonical retinal and anterior patterning regulators also argued for a null or
near-null point estimate in this postnatal thalamic population:

- `Pax6`: held-in focal `n_degs = 0`; in the Parquet, 138 focal perturbed
  nuclei and smallest adjusted p-value `1.0`. Tetreault et al. showed that
  Lhx2 and Pax6 activate `Six6` in retinal progenitors, so `Pax6` is upstream
  in the retinal Six6 program, but its own acute P16 perturbation was quiet in
  this focal thalamic cell group.
- `Rax`: held-in focal `n_degs = 0`; 209 focal perturbed nuclei and smallest
  adjusted p-value `0.649`. It had only a singleton corrected response in
  `001 L5-6 IT Glut` in the targeted scan, and the July corpus summarized
  that canonical RAX-network perturbations did not phenocopy its responder
  groups.
- `Otx2`: held-in focal `n_degs = 0`; 162 focal perturbed nuclei and smallest
  adjusted p-value `0.885`.
- `Hesx1`: held-in focal `n_degs = 0`; 222 focal perturbed nuclei and smallest
  adjusted p-value `1.0`.
- `Vsx2`: held-in focal `n_degs = 0`; 220 focal perturbed nuclei and smallest
  adjusted p-value `1.0`.
- `Pax2`, `Pax3`, `Pax4`, `Pax7`, and `Pax8` were all held in and all had
  `n_degs = 0` in the focal training-count file.
- Six6-cofactor genes `Tle1`/`Aes`, `Vax1`, and `Lhx2` were not available as
  held-in perturbations in the focal training table. `Peg3`, a reported HCRT
  neuron fate factor in lateral hypothalamus, had a single focal DEG and was
  not close enough to override the eye-field analogs.

### Biological transfer

Six6 is a homeodomain transcription factor closely related to Six3. Jean et al.
identified murine `Six6/Optx2` as a Six3-related gene expressed embryonically
in the presumptive pituitary/hypothalamic axis, ventral optic stalk, and neural
retina. Gallardo et al. mapped human `SIX6` into the chromosome 14 SIX1/SIX4
cluster and linked SIX6 hemizygosity to developmental eye and pituitary
anomalies. Lopez-Rios et al. showed that SIX6 and SIX3 use Groucho-family TLE
and AES cofactors in an eye-development network. Larder et al. established
that Six6-null mice have hypothalamic dysregulation and impaired fertility
through GnRH-neuron defects.

Those studies support Six6 as a real developmental regulator, but the
causal chain is imperfect for this assay: the strongest consequences were in
embryonic optic/pituitary/GnRH lineages, whereas the requested perturbation is
acute mosaic loss at P16, harvested 3 to 4 weeks later, in recovered NeuN+
whole-brain neuronal nuclei assigned to a thalamic Prkcd/Grin2c glutamatergic
class. A developmental requirement in retina or GnRH neurons does not imply
that residual Six6 function limits the transcriptome of postnatal thalamic
glutamatergic neurons. The same-experiment `Six3`, `Pax6`, `Rax`, `Otx2`,
`Hesx1`, and `Vsx2` results are a direct falsifier of a broad eye-field/homeobox
postnatal response in this cell group.

### Prediction

I predicted `Six6` to be below the focal FDR threshold, with a point estimate
of **0 DEGs**. This is driven mainly by the declared dataset: its closest
available paralog `Six3` and adjacent eye-field transcription factors were
all FDR-null in the focal class with sufficient matched nuclei and no
near-threshold adjusted p-values. External literature increases confidence
that those are the right comparators rather than unrelated homeobox factors,
but it does not supply evidence for a positive postnatal thalamic DEG burden.

## Limits

This is an extrapolation because the held-out `Six6` signature is absent by
design. `Lhx2`, `Vax1`, `Tle1`, and `Aes` would have been mechanistically
useful Six6-network perturbations but were not in the held-in focal count
table. Germline Six6-null and developmental organoid literature can reveal
lineage requirements that an acute partial postnatal CRISPR perturbation may
not reproduce. Conversely, a zero DEG prediction means no measured gene is
expected to pass this assay's FDR 0.05 threshold; it is not a claim that Six6
has no molecular role or that the guides would fail.
