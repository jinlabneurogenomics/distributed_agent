# Gatad1 prediction trace

## Question and resolved ambiguities

The requested prediction is the held-out `n_degs` for each target in
`089_Gatad1.csv`, restricted to `151 TH Prkcd Grin2c Glut` cells.  I treated
`n_degs` as the exact endpoint in the training CSV: the number of measured
genes with `pvals_adj < 0.05` in that focal cell group, including the targeted
gene itself if it passed the threshold.  I did not treat absence from the
training parquet as a failed perturbation; Gatad1 was held out by design.

The manifest contained a single target, in this order:

```tsv
target_name
Gatad1
```

## Sources used

Internal same-experiment data:

- Differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Focal training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Requested-target manifest:
  `[local file: 089_Gatad1.csv]`
- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`.
  `target_context(Gatad1)` had no Gatad1-specific report in the filtered
  same-experiment corpus, so I used corpus claims about represented NuRD/MBD
  and chromatin-repressor comparators rather than target-specific Gatad1
  findings.
- Distributed Agents runtime profile comparison over focal-cell log-fold-change vectors.

External literature from PubMed:

- Gatad1/ODAG was first described as a postnatal ocular-development-associated
  mouse gene that is down-regulated by P14 in the eye: Tsuruga et al. 2002,
  Gene, DOI `10.1016/s0378-1119(02)00563-2`, PMID `12062807`.
- GATAD1 can act as an epigenetic transcriptional repressor in neuroendocrine
  puberty timing by repressing `KISS1` and `TAC3` and reducing H3K4me2 through
  KDM1A recruitment: Lomniczi et al. 2015, Nature Communications,
  DOI `10.1038/ncomms10195`, PMID `26671628`.
- GATAD1 can directly bind and activate the `PTP4A3/PRL3` promoter in liver
  cancer cells: Sun et al. 2018, Hepatology, DOI `10.1002/hep.29750`,
  PMID `29266303`.
- GATAD1 has been connected to the EMSY/KDM5A/SIN3B/H3K4me3-associated
  complex in proteomic work: Varier et al. 2016, Journal of Biological
  Chemistry, DOI `10.1074/jbc.M115.701227`, PMID `26841866`.
- Phosphorylation of a disease-associated GATAD1 serine controls 14-3-3
  binding and is predicted to affect GATAD1 nuclear localization: Rrustemi et
  al. 2024, Nature Communications, DOI `10.1038/s41467-024-46794-8`,
  PMID `38605029`.
- Direct loss of Gatad1 in one differentiated lineage was weak: cardiomyocyte
  Gatad1 knockout mice were reported not to develop cardiomyopathy through
  aging or pressure overload: Pang et al. 2024, Journal of Molecular Histology,
  DOI `10.1007/s10735-024-10297-z`, PMID `39641830`.
- Mammalian NuRD architecture places CHD ATPases, MBD proteins, GATAD2
  proteins, HDAC1/2, MTA proteins, and RBBP4/7 in a biochemical complex:
  Kloet et al. 2014, FEBS Journal, DOI `10.1111/febs.12972`,
  PMID `25123934`.

## Computations over the focal dataset

I first used the training-count CSV as the calibrated endpoint distribution.
The focal group is zero-inflated: 1,205 of 1,674 training perturbations have
`n_degs = 0`; only 469 are nonzero; the median is 0 and the 75th percentile is
1.  The mean is 14.1, but the mean is dominated by a small high tail
(`Uba5 = 2677`, `Tpr = 1768`, `Sin3a = 1433`).

To inspect exact analog counts I joined selected chromatin candidates against
the endpoint CSV.  The most relevant rows were:

```tsv
target_name	n_degs
Gatad2b	1
Mbd2	0
Chd4	100
Sin3a	1433
Chd2	34
Chd8	61
Chd7	0
Kdm5b	0
Kdm5c	18
Hdac5	0
Hdac8	0
Arid1a	22
Arid1b	1
Smarca2	1
Smarca4	0
Setd1a	368
Zmynd8	74
```

I then filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and
`pvals_adj < 0.05` for the same candidates.  The exact filter was:

```python
(
    pc.field("group_name") == "151 TH Prkcd Grin2c Glut"
) & pc.field("gene_target").isin(targets) & (
    pc.field("pvals_adj") < 0.05
)
```

This confirmed that `Gatad2b` had only one significant feature, `Gatad2b`
itself (`logFC = -0.498`, `p_adj = 0.00348`), while `Mbd2` had no significant
features and `Chd4` had 100.  The leading Chd4 FDR hits were a mixed
up/downstream set, for example `Begain` up, `Cpne7` down, `Zfp467` up,
`Ramp3` down, `Pygm` up, `Sorbs1` down, `Tle2` up, and `Xylt2` down.

Finally, I compared full focal log-fold-change profiles over 17,259 measured
genes with the Distributed Agents runtime `profile_compare` tool.  `Gatad2b`, `Mbd2`,
and `Chd4` have moderately similar whole-vector background correlations to
many chromatin perturbations, but essentially no intersection of FDR-significant
genes with those larger signatures.  For example, `Gatad2b` vs `Chd4` had
Pearson `0.676` and cosine `0.735` across the whole vector but zero shared
positive FDR genes and zero shared negative FDR genes because the only
`Gatad2b` significant gene was its own transcript.  `Mbd2` similarly had
zero FDR genes.  This made the exact DEG counts more informative than broad
whole-profile correlations for Gatad1.

## Target-specific reasoning

### Gatad1

Biologically relevant training perturbations and counterexamples:

- `Gatad2b`, `n_degs = 1`.
  `Gatad2b` is the closest same-prefix measured target and a p66 beta NuRD
  subunit, but in the focal group its only FDR hit was the self-transcript.
  It therefore argues against treating the GATAD name or p66/NuRD adjacency as
  sufficient to predict a downstream thalamic program.
- `Mbd2`, `n_degs = 0`.
  MBD2 is a methyl-CpG/NuRD-associated cofactor.  Its flat focal profile is a
  second boundary for any hypothesis that loss of an MBD-GATAD-HDAC chromatin
  repressor necessarily creates a visible `151 TH Prkcd Grin2c Glut` RNA
  response.
- `Chd4`, `n_degs = 100`.
  CHD4 is the NuRD ATPase and shows that the same assay can detect a real NuRD-
  adjacent chromatin response in this cell group.  The same-experiment
  Distributed Agents claim `claim:85bada0191e4170beb10` summarizes the relevant
  boundary: represented NuRD/MBD-adjacent perturbations, including `Chd4`,
  `Gatad2b`, and `Mbd2`, do not collapse into a single neuronal loss-of-
  function mRNA signature.  `Chd4` is therefore a positive counterexample for
  assay sensitivity, not an estimator that should be transferred directly to
  Gatad1.
- `Sin3a`, `n_degs = 1433`, and H3K4-axis genes `Kdm5c = 18`, `Kdm5b = 0`,
  `Setd1a = 368`.
  Varier et al. connect GATAD1 to an EMSY/KDM5A/SIN3B complex, and Lomniczi et
  al. connect GATAD1 to KDM1A-dependent promoter repression.  The direct
  partners `Kdm1a`, `Kdm5a`, and `Sin3b` were absent from the training-count
  table, so the represented analogs are indirect.  Their training endpoints are
  heterogeneous rather than a monotone H3K4/SIN3 response, so I used the large
  `Sin3a` and `Setd1a` counts as evidence for possible detectability of core
  chromatin machinery but not for a large Gatad1 count.
- General zinc-finger and developmental transcription factors were mostly flat
  in this focal group (`Gata1 = 0`, `Gata3 = 0`, `Gata4 = 0`, `Gata6 = 0`,
  `Zkscan1 = 0`, `Zkscan16 = 0`, many `Zfp* = 0`).  These are weak analogs
  because their DNA-binding domains and regulons differ from Gatad1, but they
  reinforce that a promoter-binding repressor does not automatically generate
  focal thalamic DEGs after a sparse P16 loss-of-function perturbation.

External Gatad1 biology makes a strong nonzero prediction unlikely in this
specific context.  GATAD1 is capable of locus-specific transcriptional
regulation: it represses `KISS1` and `TAC3` in hypothalamic puberty circuitry
via KDM1A in Lomniczi et al., it binds the `PTP4A3/PRL3` promoter in liver
cancer, and it has a phosphorylation-dependent 14-3-3 interaction that can
control localization.  Those mechanisms point to promoter-specific regulation
rather than to an obligate core chromatin activity like CHD4 ATPase loss or
SIN3A loss.  They also come from hypothalamic/puberty, tumor, cardiac, or
endothelial systems rather than postnatal thalamic glutamatergic neurons.

I therefore predicted an exact zero rather than a broad or self-only response.
The internal part of the decision is that the closest measured NuRD/GATAD2B/MBD
comparators are focal-null or nearly focal-null, while the visible CHD4 and
SIN3A cases are biochemically more central and not phenocopies.  The external
part is that known GATAD1 functions are conditional, promoter-specific, and not
established as a constitutive requirement for juvenile postmitotic thalamic
neuronal RNA maintenance.

## Predicted value

```tsv
target_name	predicted_n_degs
Gatad1	0
```

## Limits

- Gatad1 itself was not in the same-experiment Distributed Agents corpus and was absent
  as a perturbation from both supplied training inputs, so there was no direct
  Gatad1 expression signature to compare.
- The best mechanistic partners for external GATAD1 knowledge were not direct
  training targets: `Kdm1a`, `Kdm5a`, `Sin3b`, and the MIER proteins were
  missing from the focal training-count file.
- `Gatad2b` and `Mbd2` are useful boundaries for NuRD-adjacent reasoning, but
  Gatad1 is not simply another core NuRD subunit.
- Whole-profile correlations among low-response perturbations were dominated
  by broad weak background structure and did not imply shared FDR-level DEGs.
- A prediction of zero is sensitive to a possible isolated Gatad1 self-
  transcript drop.  The dataset context warns that target-transcript loss is
  not a reliable functional readout, but it still contributes to this exact
  `n_degs` endpoint when significant.
