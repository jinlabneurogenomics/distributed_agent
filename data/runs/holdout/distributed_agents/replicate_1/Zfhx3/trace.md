# Question and endpoint

The requested held-out perturbation is `Zfhx3`. I interpreted the output as a
point prediction of the number of focal-cell measured genes with
`pvals_adj < 0.05` after acute sparse AAV-CRISPR loss of `Zfhx3` in
`151 TH Prkcd Grin2c Glut` neurons. The requested readout was directly observed
for 1,674 non-held-out training perturbations in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`; `Zfhx3` was held out from
both that count table and the differential-expression Parquet, so all reasoning
below is transfer from other targets.

I used three source classes.

- Declared input data:
  `training differential-expression dataset`
  and
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Same-experiment internal corpus:
  the PerturbAI July `260713_sourceguard_1773_v1` Findings/report corpus,
  queried for target-specific reports on biologically selected training
  comparators.
- External literature through PubMed/NCBI E-utilities: Watanabe et al. 1996,
  DOI 10.1016/s0169-328x(96)00204-5, PMID 9013792; Ido et al. 1996,
  DOI 10.1016/0378-1119(95)00740-7, PMID 8654949; Parsons et al. 2015,
  DOI 10.1016/j.cell.2015.06.060, PMID 26232227; Wilcox et al. 2017,
  DOI 10.1177/0748730417722631, PMID 28816086; Wilcox et al. 2021,
  DOI 10.1016/j.isci.2021.103142, PMID 34632336; Nolan et al. 2023,
  DOI 10.1096/fj.202201829R, PMID 37713040; Perez Baca et al. 2024,
  DOI 10.1016/j.ajhg.2024.01.013, PMID 38412861; Komine et al. 2012,
  DOI 10.1371/journal.pone.0053114, PMID 23300874; Habib et al. 2018,
  DOI 10.1093/brain/awx326, PMID 29253101.

# Computations over the declared dataset

I recomputed the focal count endpoint from the Parquet as a consistency check:

```sql
select gene_target as target_name,
       cast(sum(pvals_adj < 0.05) as integer) as n_degs
from read_parquet(:training_de_all_cell_groups)
where group_name = '151 TH Prkcd Grin2c Glut'
group by gene_target
```

The recomputation produced 1,674 focal targets and matched the supplied
training-count CSV exactly. The held-out manifest contained only `Zfhx3`;
`Zfhx3` had zero rows as a `gene_target` in the training Parquet and was absent
from the count CSV.

The focal endpoint was very sparse: 1,205/1,674 training perturbations had
`n_degs = 0`, another 276 had `n_degs = 1`, and the median count was zero. I
therefore required a target-specific reason to move `Zfhx3` above zero rather
than treating its large transcription-factor annotation alone as predictive.

# Zfhx3 prediction

## Closest within-dataset paralog

The most relevant visible paralog was `Zfhx2`, the only ZFHX-family perturbation
available in the training endpoint table. In the exact focal class it had:

- `Zfhx2`: 203 perturbed nuclei versus 23,679 matched controls,
  `n_degs = 0`, minimum focal adjusted P value 1.0.

The same-experiment `Zfhx2` report was also essentially a negative report rather
than a hidden broad response: across 22 measured neuronal groups it had one
weak downstream hit at FDR 0.10 in `009 L2-3 IT PIR AON ENT Glut`, no focal
`151` response, and no acute mRNA compensation by `Zfhx3` or `Zfhx4`; both
paralog transcripts were measured in `Zfhx2` tests and had FDR 1.0 across all
22 measured groups. Komine et al. 2012 tied `Zfhx2` to differentiating neurons
and behavioral phenotypes in mice, and Habib et al. 2018 tied `Zfhx2` to
peripheral dorsal-root-ganglion pain programs. The internal report showed that
those DRG and monoaminergic programs displaced poorly into the sampled central,
postmitotic atlas. That makes `Zfhx2` a strong numeric anchor for this
platform, but not proof that `Zfhx3` is identically inert.

Given the requested endpoint, the important observation is directional: a close
ZFHX homeodomain/zinc-finger factor can be well powered in the focal group
without producing even a singleton DEG. This pulls the `Zfhx3` estimate toward
zero.

## Focal thalamic transcription-factor analogs

I checked whether other postmitotic thalamic transcription factors argue that a
Zfhx3 knockout should behave like a broad thalamic state perturbation:

- `Tcf7l2`: 111 perturbed nuclei, `n_degs = 106`.
- `Prox1`: 205 perturbed nuclei, `n_degs = 50`.
- `Zfp423`: 160 perturbed nuclei, `n_degs = 150`.

All three produced real focal signatures, but their report-level comparisons
are counterexamples to a generic "large neural transcription factor in
thalamus" rule. The `Tcf7l2` response recovered a mostly down-regulated
thalamic terminal excitability/synaptic program, including `Ramp3`, `Kcnc2`,
`Pcsk2`, `Grin2b`, `Gabbr2`, `Gabra4`, `Gabra1`, `Prkcd`, `Pcp4`, and `Cpe`.
`Prox1` had only seven overlaps with the 64-gene Prox1 FDR 0.10 signature when
compared with `Tcf7l2`, most in the opposite direction. `Zfp423` caused a
large thalamic subtype/surface-glycoprotein shift but did not phenocopy its
obvious EBF/BMP/RA molecular neighborhood.

In the exact focal Parquet rows, these training perturbations also did not
recruit `Zfhx3` as a downstream transcript: `Zfp423` gave the strongest among
them at `Zfhx3` log2FC -0.294 and FDR 0.302, while `Tcf7l2` and `Prox1` both
had `Zfhx3` FDR 1.0. Thus the visible thalamic TFs show that the assay can
detect transcription-factor dependencies in `151 TH Prkcd Grin2c Glut`, but
they do not place `Zfhx3` inside one of those focal DEG programs.

## Chromatin and zinc-finger counterexamples

Perez Baca et al. 2024 reported human ZFHX3 loss-of-function as a syndromic
intellectual-disability mechanism and found increased ZFHX3 abundance during
human neuronal differentiation, promoter-proximal binding near nervous-system
development genes, and interaction with BRG1/BRM-associated BAF complex
components and the cleavage/polyadenylation complex. That made BAF and other
chromatin-regulatory training perturbations useful as upper-bound
counterexamples rather than direct complex analogs.

The focal training counts for selected chromatin factors were:

- `Smarcc2`: 162 perturbed nuclei, `n_degs = 185`.
- `Arid2`: 170 perturbed nuclei, `n_degs = 56`.
- `Arid1a`: 316 perturbed nuclei, `n_degs = 22`.
- `Arid1b`: 173 perturbed nuclei, `n_degs = 1`.
- `Ep300`: 155 perturbed nuclei, `n_degs = 0`.
- `Kat6a`: `n_degs = 0`.
- `Kat6b`: `n_degs = 0`.
- `Chd7`: `n_degs = 0`.

The internal `Smarcc2` and `Arid2` reports showed that their focal effects were
not just a generic chromatin-damage signature: `Smarcc2` converged with
`Smarce1` and `Arid1a`, partially with `Arid2`, and not with several other
BAF-family targets; `Arid2` also separated from `Arid1a`, `Arid1b`,
`Bcl11a`, and `Bcl11b`. Because ZFHX3 is not an obligate BAF subunit, the
human protein-interaction prior is too broad to transfer the large `Smarcc2` or
moderate `Arid2` count to `Zfhx3`.

Other developmental zinc-finger or homeodomain-like training factors were
mostly null in the focal group:

- `Zfp462`: 283 perturbed nuclei, `n_degs = 0`.
- `Zfp521`: 194 perturbed nuclei, `n_degs = 0`.
- `Zfp536`: 196 perturbed nuclei, `n_degs = 0`.
- `Zhx3`: 110 perturbed nuclei, `n_degs = 0`.
- `Foxp2`: 245 perturbed nuclei, `n_degs = 0`.
- `Npas3`: 198 perturbed nuclei, `n_degs = 0`.

Those are weaker biological analogs than `Zfhx2`, but together they support the
idea that many neuronal developmental TF genes do not create a measurable FDR
0.05 footprint after a P16 mosaic knockout in this specific thalamic class.

## External Zfhx3 biology and endpoint alignment

ZFHX3/ATBF1 itself is a plausible neural regulator. Watanabe et al. 1996 showed
that mouse `Atbf1`/`Zfhx3` mRNA is highest at embryonic day 13-15, declines by
postnatal day 28, and is regionally enriched in basal telencephalon,
diencephalon, and mesencephalon with high expression in the inferior colliculus
and thalamus. Ido et al. 1996 similarly found high developing-brain and low
adult-tissue ATBF1 transcript levels. Perez Baca et al. 2024 showed that human
ZFHX3 haploinsufficiency causes syndromic neurodevelopmental disease.

The mouse functional literature is strongest outside the exact focal endpoint.
Parsons et al. 2015 found that the `Zfhx3(Sci/+)` allele alters an
AT-motif-driven neuropeptide axis in the suprachiasmatic nucleus. Wilcox et al.
2017 showed an adult conditional `Zfhx3` knockout changes circadian pace and
amplitude, again through SCN biology, and Wilcox et al. 2021 showed that
developing-hypothalamus deletion can ablate the SCN. Nolan et al. 2023 found
that `Zfhx3(Sci/+)` alters energy balance and arcuate-hypothalamus neuropeptide
expression.

Those data establish that ZFHX3 can drive large neuronal expression programs,
but the causal chain does not land cleanly in the requested cell group:

1. The requested perturbation is acute, sparse P16 CRISPR loss of function, not
   an embryonic deletion, a lifelong dominant missense allele, or a complete
   adult hypothalamic conditional excision.
2. The direct molecular consequence is expected loss of a nuclear TF in exposed
   postmitotic cells; it does not require a co-perturbation or obligate complex
   partner in the screen.
3. Published propagation is strongest through SCN clock/neuropeptide programs
   and ARC energy-balance transcripts. Those nuclei are hypothalamic and likely
   diluted or absent in the `151 TH Prkcd Grin2c Glut` thalamic group.
4. The measured endpoint is an FDR-thresholded snRNA-seq DEG count in recovered
   thalamic neurons, not a behavioral circadian readout, food-intake phenotype,
   retinal output, or embryonic diencephalic patterning phenotype.

I therefore treated the embryonic thalamic expression prior as a reason to avoid
an overconfident biological null, but not as sufficient evidence for a nonzero
focal FDR 0.05 count. Developmental expression has largely decayed by the
P37-P44 harvest window, and the closest same-platform ZFHX analog was silent in
the focal group.

# Final point estimate

I predict `Zfhx3` will have `0` DEGs at FDR 0.05 in
`151 TH Prkcd Grin2c Glut`.

The within-dataset evidence drives the numerical value: the focal count
distribution has a zero median, the closest measured paralog `Zfhx2` has zero
focal DEGs with 203 perturbed nuclei, and other developmental zinc-finger or TF
counterexamples are also zero. External literature prevents interpreting
`Zfhx3` as an unimportant gene, but it points mostly to embryonic
diencephalic/SCN/ARC biology rather than to a maintained P16-to-P37 thalamic
regulon of the sort directly counted here.

# Limits

- `Zfhx3` and `Zfhx4` were absent as training perturbations, so the single
  closest family member available was `Zfhx2`.
- `Zfhx2` is not a perfect analog: it has its own DRG and monoaminergic biology,
  and failure of `Zfhx2` in the focal group cannot prove failure of a
  `Zfhx3` knockout.
- The Watanabe et al. thalamic `Atbf1` expression data stop at P28, while the
  Perturb-seq endpoint was read at P37-P44 after P16 infection. That makes the
  thalamic prior directionally relevant but age-mismatched.
- SCN and arcuate-hypothalamus Zfhx3 programs are endpoint-mismatched. A real
  SCN/ARC effect could be invisible here because the screen asks about a broad
  thalamic glutamatergic class, not those nuclei.
- The acute AAV CRISPR design did not measure DNA indels or ZFHX3 protein, and
  target-RNA down-regulation should not be used as an editing-efficiency
  filter.
