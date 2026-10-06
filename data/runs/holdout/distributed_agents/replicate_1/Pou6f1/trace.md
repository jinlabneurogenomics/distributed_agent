# DEG-count prediction for 151 TH Prkcd Grin2c Glut

## Question and endpoint

The held-out target set for this run contains one perturbation, `Pou6f1`. I
interpreted the task as a scalar prediction of the number of genes that would
pass `pvals_adj < 0.05` after acute AAV-CRISPR loss of `Pou6f1` in recovered
`151 TH Prkcd Grin2c Glut` nuclei, using the supplied non-held-out
differential-expression parquet and the matching training `n_degs` table as
the direct endpoint evidence. The held-out `Pou6f1` count and signature are
absent by construction; `Pou6f1` can still appear as a measured transcript in
other targets' rows.

The readout is response breadth after BH correction in a survivor-conditioned
single-nucleus DE test. I did not treat target-gene self knockdown as editing
efficiency or as the endpoint.

## Sources used

- Declared Parquet input:
  `training differential-expression dataset`.
  I queried the focal cell group for `pvals_adj < 0.05` and `< 0.10`, minimum
  adjusted p value, signed Wilcoxon-score leaders, and matched perturbed/control
  nucleus counts for represented POU genes and response-positive transcription
  factor counterexamples.
- Declared training-count input:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  This supplied exact visible-target counts in the focal cell group.
- Declared requested-target CSV:
  `single-target request for Pou6f1`.
  This supplied the single requested row, `Pou6f1`, and no ordering supervision.
- Internal same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`. I used the Pou6f2, Pou3f3,
  Pou3f4, and Pou2f1 Finding/Evidence/Reference records as packaged
  interpretation of the same Perturb-seq experiment, not as independent
  replication.
- External literature retrieved through PubMed:
  Okamoto et al., 1993, PMID:8463278; Cui and Bulleit, 1998,
  DOI:10.1002/(SICI)1097-4547(19980615)52:6<625::AID-JNR1>3.0.CO;2-A;
  Zhou et al., 1996, DOI:10.1523/JNEUROSCI.16-07-02261.1996; Drews et al.,
  2007, DOI:10.1007/s00335-007-9059-8; and Malik et al., 2018,
  DOI:10.1007/s00018-018-2748-5.

## Quantitative checks over the training data

The focal training table contains 1,674 non-held-out targets. Its distribution
is zero-inflated: the median `n_degs` is 0, the 75th percentile is 1, the 90th
percentile is 2, and 469/1,674 perturbations have a nonzero count. Thus a
single zero for a related gene is not automatically decisive, but a set of
nulls in the same family is meaningful.

The same-family POU perturbations represented in the focal class were all
transcriptionally quiet at the requested threshold:

| target | observed `n_degs`, FDR<0.05 | FDR<0.10 | matched perturbed nuclei | best focal-class adjusted p value |
| --- | ---: | ---: | ---: | ---: |
| `Pou1f1` | 0 | 0 | 208 | 1.000 |
| `Pou2f1` | 0 | 0 | 173 | 0.369 |
| `Pou2f2` | 0 | 0 | 166 | 1.000 |
| `Pou3f3` | 0 | 0 | 419 | 0.849 |
| `Pou3f4` | 0 | 0 | 220 | 0.759 |
| `Pou4f3` | 0 | 0 | 241 | 1.000 |
| `Pou5f1` | 0 | 0 | 143 | 1.000 |
| `Pou6f2` | 0 | 0 | 182 | 1.000 |

`Pou6f2` is the key anchor because it is the only visible class-VI paralog of
`Pou6f1`. In the focal class, no Pou6f2 row approached significance; its
lowest-ranked rows were `Top3b`, `Chmp1b`, `Sun2`, `Cdk5r2`, and `Pou2f1`, all
with FDR=1.0. The internal July report also summarized the complete Pou6f2
surface as 0 downstream genes at FDR<0.10 in all 23 measured neuronal cell
groups, with the 151-class comparison having 182 perturbed and 23,679 control
nuclei. The report's whole-surface score-neighbor calculation found only
near-zero correlations for Pou6f2, with the strongest positive neighbors
`Nkx6-2`, `Safe_target_62`, `Fmn1`, `Trim2`, and `Lrrc7` all at r <= 0.0289
and the strongest negative neighbors all near zero. That argues against a
hidden Pou6f2-like module elsewhere in the training set.

I also checked that this was not a generic failure of transcription-factor
perturbations in the focal class. `Prdm10`, `Tcf7l2`, and `Ctcf` had 52, 106,
and 270 focal-class DEGs respectively, each with very small adjusted p values.
The endpoint is therefore able to register transcriptional-regulator effects
in `151 TH Prkcd Grin2c Glut`; the null evidence is specific to the represented
POU factors under this postnatal, basal neuronal perturbation.

## Target-specific biological transfer

### Pou6f1

`Pou6f1` encodes a class-VI POU-domain transcription factor historically called
Brn-5 or Emb. Okamoto et al. cloned the murine gene as a CNS-predominant POU
factor, and Cui and Bulleit described Brn-5 protein expression as an early
postmitotic neuronal differentiation event across multiple developing and
mature CNS neuronal populations. Drews et al. later identified a predicted
Pou6f1/Brn5 site in a conserved Scn8a promoter element and showed that mutating
that site reduced promoter activity in transfected neuronal cells. Those
papers support neuronal regulatory potential, so `Pou6f1` should not be
treated as an arbitrary gene.

The causal transfer chain from the visible data is still weak for a broad
focal-class survivor transcriptome:

- Intervention: the experiment would acutely disrupt `Pou6f1` in sparse,
  postmitotic P16-to-P37/P44 thalamic glutamatergic neurons.
- Direct molecular consequence: loss of a DNA-binding POU factor. Malik et al.
  reviewed that POU factors share a bipartite DNA-binding architecture but have
  class- and chromatin-context-dependent target choice, so a generic POU-domain
  analogy is insufficient.
- Best same-function anchor: the class-VI paralog `Pou6f2/RPF-1`. Zhou et al.
  described `Pou6f2` as a restricted CNS/retinal POU factor, but the same
  screen found `Pou6f2` completely flat in the focal class and across all
  assayed neuronal groups.
- Broader family checks: the visible POU1, POU2, POU3, POU4, and POU5
  perturbations were also flat in `151 TH Prkcd Grin2c Glut`; the packaged
  Pou6f2 and Pou2f1 reports explicitly found no generic acute POU-family
  response.
- Propagation to endpoint: there is no represented obligate complex or
  pathway dependency saying that Pou6f1 loss should phenocopy a known
  high-burden visible target such as `Ctcf`, `Tcf7l2`, or `Prdm10`.
- Exposure and sampling: the best neuronal evidence for Brn-5 is broad
  developmental and promoter activity evidence, not a thalamic
  Prkcd/Grin2c-specific P37 maintenance requirement. The assay samples
  recovered neurons after an acute mosaic perturbation and will miss embryonic
  specification functions or rare retinal/GnRH-like lineages that are not
  present in this focal class.

The within-dataset evidence therefore points to a measured null. External
knowledge raises the prior above a completely unannotated gene because Pou6f1
is neuronal and can regulate neuronal promoters, but it does not supply a
candidate-specific reason to override the focal Pou6f2/POU-family nulls. I
predict that acute `Pou6f1` loss would produce no genes passing FDR 0.05 in the
held-out focal comparison:

`Pou6f1`: predicted `n_degs = 0`.

## Limits

The prediction is an extrapolation from paralogs and other POU-family
perturbations because `Pou6f1` itself is held out. `Pou6f2` is the closest
visible paralog, but POU6F1 and POU6F2 need not bind the same genomic sites in
the thalamic neurons assayed here. The Parquet contains DE summaries rather
than raw counts, chromatin occupancy, guide-level indels, or pre-assay survival
denominators, so I cannot test whether a quiet recovered signature hides
selection or compensatory survival. Literature on Pou6f1 emphasizes development
and promoter assays more than acute postmitotic loss in adult thalamic
glutamatergic neurons, making the zero call a dataset-driven estimate rather
than a statement that Pou6f1 has no neuronal function.
