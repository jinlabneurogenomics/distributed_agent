# Sdhb DEG-count forecast

Target: `Sdhb` in `151 TH Prkcd Grin2c Glut`

Predicted `n_degs`: `1`

## Evidence that determined the point

- The prediction-safe SDHB biology bundle identifies SDHB as the obligate
  iron-sulfur subunit of mitochondrial respiratory complex II, partnered with
  `Sdha`, `Sdhc`, and `Sdhd`. The same bundle records exact focal-population
  reach for `Sdhb`: 16,626 of 23,679 non-target nuclei expressed the transcript
  in `151 TH Prkcd Grin2c Glut` (70.214%), with pseudobulk CPM 88.289 and mean
  raw UMI 1.409. It also adjudicates the P16-to-P37/P44 loss as likely
  substantially depleting functional SDHB stock because a measured mouse
  thalamus protein half-life of about 12.82 days spans roughly 1.6-2.2
  half-lives over the experiment. The card leaves important uncertainty:
  residual assembled complex II, spare capacity, and survivor conditioning are
  not measured by the bundle.

- In the focal training count table, the only same-complex training subunit was
  `Sdha`, with `n_degs = 1`. Direct Parquet rows for
  `151 TH Prkcd Grin2c Glut` showed that the lone 5% FDR hit was `Sdha` itself
  (`logFC = -0.7809`, `p_adj = 2.11e-12`); the nearest downstream hit, `Edem2`,
  reached only `p_adj = 0.0646` and was outside the requested endpoint. The
  same-experiment Sdha report summarized this as a broadly buffered complex-II
  response with no broad HIF/pseudohypoxia, mitochondrial ISR/UPRmt, NRF2/redox,
  ER, or ISR transcriptional program.

- Other focal TCA and respiratory-chain measurements support the same scale.
  Among `Aco2`, `Dlat`, `Dld`, `Dlst`, `Idh3a`, `Mdh1`, `Mdh2`, `Ogdh`,
  `Pdha1`, `Sdha`, `Sucla2`, and `Suclg1`, eight of twelve had zero downstream
  DEGs at `p_adj < 0.05`, seven of those enzyme perturbations had counts of 0 or
  a self-transcript-only 1, and `Sdha` was in that self-only group. The larger
  `Mdh1` result was not used as a magnitude donor: it was 28 downstream DEGs in
  this endpoint, but the packaged report ties it to the cytosolic
  malate-aspartate-shuttle arm with partial `Got1` convergence, while
  mitochondrial MAS components and carriers such as `Mdh2`, `Got2`, and
  `Slc25a12` did not phenocopy it.

- The focal respiratory-chain training genes were likewise mostly flat. In the
  queried set of 38 represented Cox/Nduf/Uqcr/Timm/Tomm/Coa8/Lrpprc genes, the
  summed focal count was only 15; most nonzero counts were a single
  self-transcript hit, and many complex-I, III, and IV targets were zero.

## Synthesis

`Sdhb` is a real, well-expressed, obligate complex-II perturbation, so I did not
forecast a safe-target-like absence of any detectable effect. But the matched
training data put the closest assayed operation, `Sdha`, at exactly one focal
5% FDR gene and showed that this one gene was self-transcript loss rather than a
downstream stress response. The broader TCA/OXPHOS panel argues that acute
single-subunit mitochondrial enzyme loss in recovered postnatal thalamic
neurons is usually transcriptionally buffered in this assay, while the
`Mdh1/Got1` exception is a cytosolic MAS state, not a complex-II scale
analogue.

Because `Sdhb` is expressed in most focal non-target nuclei, the most likely
detectable feature is the target transcript itself. The point forecast is
therefore one DEG, with the main downward risk being no measurable `Sdhb`
self-transcript depletion and the main upward risk being a rare SDHB-specific
downstream crossing of the 5% FDR threshold.
