# DEG-count prediction for held-out Pax5

## Question and resolved ambiguities

The task is to predict, for each target in
`167_Pax5.csv`, the number of genes that would pass Benjamini-Hochberg FDR
0.05 after an acute AAV-CRISPR loss-of-function perturbation in
`151 TH Prkcd Grin2c Glut` neurons.  The manifest contains one target:
`Pax5`.  `Pax5` is absent from both the training count CSV and the parquet
as a perturbation target, so I treated all Pax5 observations as a fully
held-out endpoint and used only non-held-out targets as in-dataset evidence.

I interpreted `0` as the point prediction that no measured gene will have
`pvals_adj < 0.05` in the focal group, rather than as a claim that Pax5 has no
biological function in every context.  The estimate is for the assay-specific,
postnatal NeuN+ neuronal CRISPR readout.

## Sources used

- Requested targets:
  `[local file: 167_Pax5.csv]`.
- Focal training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
  The file contains 1,674 non-held-out targets; 1,205 have `n_degs = 0`,
  the median is 0, the 75th percentile is 1, and the mean is 14.1 because a
  small number of RNA-processing/proteostasis/chromatin targets produce broad
  responses.
- Full DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
  I filtered this table to `group_name = '151 TH Prkcd Grin2c Glut'` and
  inspected the FDR-significant counts, near-threshold counts, matched cell
  counts, and signed log-fold-change profiles for Pax, midbrain/hindbrain,
  paired-like homeobox, and B-lineage transcription-factor analogs.
- Distributed Agents corpus release
  `perturbai-july-260713-sourceguard-1773-v1`.
  Pax5 itself had no target-centered corpus finding in this release.
  Relevant corpus evidence came from `claim:a74e194700044572fe96`, which states
  that represented Pax/Otx/Pitx/En developmental-regulator perturbations do
  not recover canonical thyroid, retinal, or midbrain-hindbrain transcriptional
  programs in the sampled postnatal neuronal groups.  The claim is anchored by
  `Pax8:F002` and supported by `Pax2:F004`, `Otx2:F005`, `Pitx2:F004`, and
  `En1:F003`.
- Distributed Agents runtime expression-profile comparison.
  I compared `Pax2`, `Pax3`, `Pax6`, `Pax8`, `En1`, `Otx2`, `Pitx2`,
  `Pitx3`, `Lmx1b`, and `Foxa2` in the focal group using
  `logfoldchanges` as the signed value and `pvals_adj < 0.05` as the
  significance threshold.  The lossless artifact is
  `artifacts/pax_family_profile_compare.json`; the bounded inspection table is
  `artifacts/pax_family_profile_inspect.json`.
- External biology from PubMed/NCBI E-utilities and prior knowledge:
  Medvedovic et al. 2011, DOI `10.1016/B978-0-12-385991-4.00005-2`, reviewing
  Pax5 as a B-cell identity factor; Nutt and Kee 2007, DOI
  `10.1016/j.immuni.2007.05.010`, on E2A/EBF1/Pax5 control of B-cell
  commitment; Pridans et al. 2008, PubMed `18209069`, on Pax5 direct targets
  in early B-cell differentiation, including secondary B-lineage transcription
  factors; Bouchard et al. 2000, DOI `10.1242/dev.127.17.3703`, showing
  biochemical equivalence of Pax2 and Pax5 in several embryonic Pax2
  developmental domains; and Ye et al. 2001, DOI `10.1038/nn761`, showing
  Pax2 regulation of Pax5/8 and Fgf8 at the embryonic midbrain-hindbrain
  organizer.

## Computational checks

The core focal check was:

```sql
select gene_target,
       count(*) as n_rows,
       sum(pvals_adj < 0.05) as n_fdr05,
       sum(pvals_adj < 0.10) as n_fdr10,
       min(pvals_adj) as min_padj,
       any_value(n_pert_matched) as n_pert,
       any_value(n_ctrl_matched) as n_ctrl
from training_de_all_cell_groups
where group_name = '151 TH Prkcd Grin2c Glut'
  and gene_target in (...)
group by gene_target;
```

The same query over the full 17,259 measured genes per target showed no
FDR<0.05 and no FDR<0.10 genes for every mechanistic analog listed below.
Apparent extreme log-fold changes in the flat profiles all had adjusted
p-values far from significance, commonly exactly 1.0, so they were treated as
sparse-count artifacts rather than as coherent subthreshold programs.  The
profile-comparison nodes for `Pax2`, `Pax3`, `Pax6`, `Pax8`, `En1`, `Otx2`,
`Pitx2`, `Pitx3`, `Lmx1b`, and `Foxa2` all had
`response_activity_status = no_significant_features`.

## Target-specific reasoning

### Pax5

Prediction: `0` DEGs.

`Pax5` has two plausible external neighborhoods, and both point away from a
broad `151 TH Prkcd Grin2c Glut` response.

First, Pax5 belongs to the Pax2/Pax5/Pax8 subgroup.  Pax2, Pax5, and Pax8 act
in overlapping embryonic patterning contexts, including the
midbrain-hindbrain organizer; Pax2 can induce Fgf8 partly through Pax5/8 in
that embryonic tissue (Ye et al. 2001), and a Pax5 minigene can substitute
for Pax2 in multiple Pax2-dependent developmental contexts when driven from
the Pax2 locus (Bouchard et al. 2000).  The matched training data make this
neighborhood a negative analog in the postnatal neuronal screen:

| Training perturbation | why compared with Pax5 | observed `n_degs` in 151 TH Prkcd Grin2c Glut | focal signature evidence |
| --- | --- | ---: | --- |
| `Pax2` | closest developmental subgroup member and embryonic MHB relative | 0 | 251 perturbed vs 23,679 control nuclei; 0 genes at FDR<0.05, 0 at FDR<0.10, minimum adjusted p = 0.937 |
| `Pax8` | Pax2/Pax5/Pax8 subgroup member; corpus finding directly tested thyroid and MHB programs | 0 | 195 perturbed vs 23,679 controls; 0 genes at FDR<0.05, 0 at FDR<0.10, minimum adjusted p = 1.0 |
| `Pax3`, `Pax4`, `Pax6`, `Pax7` | broader Pax-family counterexamples; less mechanistically direct than Pax2/Pax8 | 0 each | all 0 genes at FDR<0.05 and FDR<0.10 in the focal group |
| `En1`, `En2`, `Otx2` | MHB/homeobox pathway comparators rather than Pax paralogs | 0 each | all 0 genes at FDR<0.05 and FDR<0.10 in the focal group |
| `Pitx2`, `Pitx3`, `Foxa2`, `Lmx1b` | dopaminergic/developmental transcription-factor comparators useful for testing a hidden postnatal midbrain-like module | 0 each | all 0 genes at FDR<0.05 and FDR<0.10 in the focal group |

The Distributed Agents corpus claim `claim:a74e194700044572fe96` generalizes the same
observation across the represented assay: Pax/Otx/Pitx/En developmental
regulators were absent, sparse, or nonconvergent and did not recover canonical
thyroid, retinal, Pax/Otx, or midbrain-hindbrain programs in P16-to-P37/P44
neuronal nuclei.  `Pax8:F002` explicitly included `151 TH Prkcd Grin2c Glut`
among the tested groups and noted that Pax8 loss did not recover a thyroid or
embryonic MHB program, including the expected `Pax2`, `Pax5`, `En1`, `En2`,
`Wnt1`, `Fgf8`, `Otx2`, and `Gbx2` targets.  `Pax2:F004` likewise found that
Pax8, Pax6, En1, En2, Otx2, Gata3, and Lbx1 failed to phenocopy Pax2 in the
screen, with Pax5 absent as a held-out perturbation.  This is direct
within-dataset evidence that developmental Pax-family relatedness does not
translate into a detectable acute signature in this juvenile postmitotic
neuronal context.

Second, Pax5 is a lineage-identity factor for B lymphopoiesis.  It activates
B-cell genes, represses non-B-lineage genes, and works with the E2A/EBF1
network to stabilize B-cell commitment (Nutt and Kee 2007; Medvedovic et al.
2011).  Pax5 can directly regulate secondary B-lineage factors and signaling
genes in pro-B cells (Pridans et al. 2008).  That external role is a poor fit
to the focal assay because the nuclei were NeuN-enriched brain neurons rather
than hematopoietic cells.  The available B-lineage and immune transcription
factor training perturbations also behaved as nulls in the focal group:

| Training perturbation | observed `n_degs` |
| --- | ---: |
| `Ebf1`, `Ebf2`, `Ebf3` | 0, 0, 0 |
| `Spi1`, `Ikzf3`, `Tcf3` | 0, 0, 0 |
| `Bcl11a`, `Bcl11b` | 0, 0 |
| `Irf1`, `Irf2`, `Irf3`, `Irf5`, `Irf8`, `Irf9` | 0, 0, 0, 0, 0, 0 |

Those are not strong positive analogs for Pax5 mechanism in B cells, but they
are relevant boundary conditions: canonical hematopoietic/B-cell transcription
factors did not show a thalamic glutamatergic neuronal response in the same
endpoint.

I therefore predicted a true zero rather than a small nonzero count.  A small
Pax5 effect cannot be excluded, but the most mechanistically grounded
measured analogs, including the closest Pax2/Pax8 subgroup members, are
exactly zero in the focal training counts, have no FDR<0.10 genes, and sit in
a corpus-supported class of embryonic regulators whose canonical programs are
not engaged by this acute postnatal neuronal perturbation.

## Limits and extrapolation

- Pax5 itself is completely held out; there is no direct Pax5 perturbation
  signature or DEG count in the supplied inputs and no Pax5-centered Distributed Agents
  corpus finding in the selected release.
- The closest in-dataset analogs are developmental subgroup members and
  pathway relatives, not Pax5 itself.  Pax2/Pax8 evidence is strong for
  ruling out an embryonic Pax2/5/8-like neuronal module in this assay, but it
  does not prove that Pax5 RNA or DNA editing would be absent in every assayed
  Pax5 guide cell.
- The external B-cell literature comes from hematopoietic contexts.  I used it
  mainly to decide that Pax5's best-known regulatory circuit should not be
  expected in NeuN+ thalamic glutamatergic neurons; this is a context-transfer
  argument, not a direct measurement.
- The endpoint is powered by the Wilcoxon/BH single-nucleus comparison.  A
  rare-cell or protein-level effect, a very small RNA shift, or an effect in
  unassayed non-neuronal cells could be real biology while still yielding
  `n_degs = 0` here.
