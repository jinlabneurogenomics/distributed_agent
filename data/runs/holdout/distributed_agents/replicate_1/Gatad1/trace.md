# DEG-count prediction trace

## Question and endpoint

I interpreted the task as a point prediction for the held-out perturbation
`Gatad1`: the requested number is the count of measured genes in
`151 TH Prkcd Grin2c Glut` with `pvals_adj < 0.05` after acute sparse AAV
CRISPR loss of Gatad1 from P16 to P37-P44. The count includes the perturbed
target transcript if that measured gene itself passes FDR. `151 TH Prkcd
Grin2c Glut` was treated as the exact Allen thalamic glutamatergic class in
the input dataset; `TH` was not interpreted as tyrosine hydroxylase.

The held-out endpoint is absent for Gatad1 by design. The direct quantitative
evidence is therefore the focal-cell training-count CSV for non-held-out
perturbations and the corresponding differential-expression rows in
`training_de_all_cell_groups.parquet`.

## Sources

Internal same-experiment sources:

- Declared training DEG counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared DE parquet:
  `training differential-expression dataset`.
- Requested-target manifest:
  `single-target request for Gatad1`.
- Dataset portrait and measurement registry in `codex_runtime/pipeline`.
- PerturbAI July 260713 sourceguard-1773 corpus v1 for bounded
  same-experiment summaries of Gatad2b, Mbd2, and Chd4 reports. I used it only
  as a packaged interpretation of the same Parquet experiment, not as
  independent replication.

External mechanism sources:

- EpiFactors, as cited by the PerturbAI Gatad2b report, for the curated NuRD
  complex definition: Medvedeva et al. 2015, `doi:10.1093/database/bav067`.
- Lomniczi et al. 2015 for hypothalamic GATAD1/ZNF transcriptional repression
  of `KISS1` and `TAC3` with KDM1A recruitment in puberty timing,
  `doi:10.1038/ncomms10195`, PMID 26671628.
- Varier et al. 2016 for interaction of GATAD1 with the
  EMSY/KDM5A/SIN3B histone-modifying complex, `doi:10.1074/jbc.M115.701227`,
  PMID 26841866.
- Tsuruga et al. 2002 for the original mouse Odag/Gatad1 description as a
  postnatal ocular-development associated gene, `doi:10.1016/s0378-1119(02)00563-2`,
  PMID 12062807.
- Yang et al. 2016 for a zebrafish gatad1 knockout model of GATAD1-associated
  adult cardiomyopathy, `doi:10.3390/jcdd3010006`, PMID 28955713.
- Pang et al. 2024 for mouse cardiomyocyte-specific Gatad1 knockout showing no
  cardiomyopathy through aging or pressure overload, `doi:10.1007/s10735-024-10297-z`,
  PMID 39641830.
- Rrustemi et al. 2024 for phosphorylation-dependent 14-3-3 binding to a
  cardiomyopathy-associated GATAD1 motif, `doi:10.1038/s41467-024-46794-8`,
  PMID 38605029.

## Dataset calculations

The requested-target manifest contained one row, `Gatad1`, with no duplicate
target. `Gatad1` was absent from the focal-cell training-count CSV, as required
for a held-out target.

I counted and summarized the supplied focal training counts over 1,674
non-held-out perturbations:

- 1,205/1,674 training perturbations had `n_degs = 0`.
- The median was 0, the 75th percentile was 1, and the 90th percentile was 2.
- Only a small heavy tail produced large DEG burdens; for example `Sin3a` had
  1433, `Chd4` had 100, `Setd1a` had 368, `Brd4` had 311, and `Ctcf` had 270.

I then queried the focal-cell Parquet rows for the closest represented
mechanistic comparators:

| training perturbation | focal `n_degs` | most relevant focal DE evidence |
|---|---:|---|
| `Gatad2b` | 1 | `Gatad2b` itself was the only FDR<0.05 gene: logFC -0.498, FDR 0.00348 in 162 perturbed nuclei; the top downstream candidate, `Rasgrp2`, was +0.596 but sub-threshold at FDR 0.1325. |
| `Mbd2` | 0 | No focal FDR<0.05 genes in 244 perturbed nuclei; the same-experiment report also found that Mbd2 was nearly flat across neuronal groups and did not show the expected broad MBD2/NuRD de-repression surface. |
| `Chd4` | 100 | A much broader focal thalamic signature with genes such as `Begain` logFC +1.001 and `Cpne7` logFC -1.064 at strong FDR, but same-experiment Gatad2b/Mbd2 comparisons showed that the Chd4 program was ATPase- or CHD4-complex-specific rather than a generic consequence of losing any NuRD-associated bridge subunit. |
| `Mbd5` | 0 | No focal response, arguing that loss of an MBD-family chromatin reader can be buffered in this assay. |
| `Pogz` | 0 | No focal response despite a chromatin-associated neurodevelopmental prior. |
| `Ywhae` | 0 | No focal response; GATAD1 has a phosphorylation-dependent 14-3-3/YWHA interaction in cardiomyopathy studies, but Ywhae loss is not an obligate same-direction proxy for Gatad1 loss in these neurons. |
| `Ywhag` | 1 | Minimal focal response for another 14-3-3-family perturbation. |
| `Ywhaz` | 1 | Minimal focal response; its only strong focal DE row was the Ywhaz transcript itself. |

## Target-specific reasoning

### Gatad1

Gatad1 has external evidence for transcriptional and chromatin-associated
roles, but those priors do not map to a single indispensable complex in the
P16-to-P37/P44 thalamic glutamatergic experiment. Lomniczi et al. showed that
GATAD1 can repress `KISS1` and `TAC3` through KDM1A recruitment in the
hypothalamic puberty network. Varier et al. placed GATAD1 with
EMSY/KDM5A/SIN3B at active H3K4me3-marked promoters in breast cancer cells.
Tsuruga et al. identified Odag/Gatad1 from early postnatal eye expression, and
cardiac literature links human GATAD1 to dilated cardiomyopathy, but the
zebrafish and cardiomyocyte mouse studies do not establish a broad neuronal
maintenance transcriptional program.

The direct within-dataset analogs are weak. Gatad2b is not Gatad1, but it is
the closest assayed GATA-domain chromatin/NuRD-adjacent perturbation. In the
focal cell group, Gatad2b produced only one FDR<0.05 gene, the target
transcript itself, with Rasgrp2 as a recurrent but sub-FDR thalamic downstream
hint. The PerturbAI Gatad2b report described Gatad2b loss as transcriptionally
buffered across postmitotic juvenile neurons: only two downstream FDR<0.10
events appeared across 371,796 downstream gene-by-cell-group tests. Mbd2, the
other assayed MBD/NuRD comparator, produced 0 focal FDR<0.05 genes and did not
phenocopy Gatad2b or Chd4. Chd4 is a counterexample showing that the cell group
can detect NuRD-linked chromatin disruption when a limiting ATPase is hit, but
the same-experiment Chd4 report explicitly found that Gatad2b and Mbd2 did not
reproduce the Chd4 thalamic program.

The causal transfer chain is therefore:

`Gatad1` CRISPR loss -> reduced GATAD1 transcription-factor/chromatin-adaptor
activity -> possible promoter-level effects through KDM1A or
EMSY/KDM5A/SIN3B, but no established obligate CHD4/MBD2 NuRD failure and no
strong prior for `KISS1`/`TAC3` biology in `151 TH Prkcd Grin2c Glut` ->
surviving postmitotic thalamic neurons -> FDR-level snRNA-seq readout.

That chain predicts a null or at most self-transcript-only DEG count. Because
the focal training set is zero-inflated, Mbd2 and Mbd5 were focal nulls,
Gatad2b was only self-significant, and the stronger external GATAD1 phenotypes
come from hypothalamus, eye, heart, endothelium, or transformed dividing cells
rather than thalamic postmitotic neurons, I chose the lower side of this
0-or-1 band and predicted 0 DEGs for Gatad1.

## Limits

This is an extrapolation from nearby perturbations; Gatad1 itself is not in the
training Parquet or the training count table. The assay did not include Kdm1a,
Kdm5a, Sin3b, EMSY, Gatad2a, Chd3, Mbd3, Hdac1/2, Mta1/2/3, or Rbbp4/7 as
training perturbations in this focal table, so the exact GATAD1-associated
complexes could not be tested directly. The prediction also depends on the
screen's acute, sparse, survivor-conditioned postnatal design; it could miss
early developmental, glial/endothelial, cardiac, retinal, or low-abundance
neuronal phenotypes and it gives no guide-level indel measurement. Finally, a
count of 0 means only that I expect no gene to cross this experiment's
single-cell Wilcoxon FDR threshold, not that Gatad1 biology is absent.
