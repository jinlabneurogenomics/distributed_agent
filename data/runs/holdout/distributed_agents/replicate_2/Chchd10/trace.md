# Chchd10 prediction trace

## Question and resolved ambiguities

The requested manifest contains one held-out perturbation, `Chchd10`.  I interpreted
the requested value as the number of measured genes with `pvals_adj < 0.05` after
acute AAV-CRISPR loss of `Chchd10` in the focal `151 TH Prkcd Grin2c Glut`
population.  The count includes the perturbed target transcript itself if that
transcript is measured and passes the adjusted Wilcoxon threshold, because the
training endpoint was defined directly from all measured rows for the
perturbation.

I treated mouse `Chchd10` as a held-out target with no direct expression
signature in the supplied parquet.  Therefore the estimate below transfers from
training perturbations in the same focal cell group, with special weight on
`Chchd2` because it is the represented CHCHD2/CHCHD10 paralog.

## Sources used

- Input training DEG counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
  This supplied the observed `n_degs` values for non-held-out targets in
  `151 TH Prkcd Grin2c Glut`.
- Input differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
  I streamed the row groups whose `group_name` metadata overlapped
  `151 TH Prkcd Grin2c Glut`, filtered to the focal group, and extracted
  candidate mitochondrial perturbations plus mtISR sentinel genes.
- Requested-target manifest:
  `[local file: 037_Chchd10.csv]`.
- Distributed Agents same-experiment corpus,
  release `perturbai-july-260713-sourceguard-1773-v1`.  The corpus had no
  frozen `Chchd10` findings, so I used the `Chchd2` findings and their internal
  mitochondrial contrasts: `Chchd2:F002`, `Chchd2:F003`, and `Chchd2:F004`.
- Run-local Distributed Agents profile comparison over the focal expression profiles.  I
  compared `Chchd2` with `Opa1`, `Micos13`, `Cox4i1`, `Tomm40`, `Park7`,
  `Ndufs2`, `Uqcrq`, `Yme1l1`, and `Snca` using all-gene Wilcoxon `scores`,
  while retaining `pvals_adj < 0.05` as the FDR endpoint.
- PubMed-indexed literature:
  Bannwarth et al. 2014, DOI `10.1093/brain/awu138`, PMID `24934289`;
  Genin et al. 2016, DOI `10.15252/emmm.201505496`, PMID `26666268`;
  Zhou et al. 2019, DOI `10.1093/hmg/ddy413`, PMID `30496485`;
  Anderson et al. 2019, DOI `10.1007/s00401-019-01989-y`, PMID `30877432`;
  Liu et al. 2020, DOI `10.1093/hmg/ddaa077`, PMID `32338760`;
  Ruan et al. 2022, DOI `10.1038/s41419-022-04602-5`, PMID `35173147`;
  Nguyen et al. 2022, DOI `10.1093/hmg/ddab329`, PMID `34791217`.

## Computational calibration

The training-count distribution in the focal group is highly zero-inflated:
`469/1674` training targets had a nonzero count, the median was 0, the 75th
percentile was 1, and the 95th percentile was 18 DEGs.  A prediction of 1
therefore means "target transcript plus no reproducible downstream program", not
a large transcriptional phenotype.

The focal parquet slice confirmed that `Chchd10` is a measured transcript in the
focal group: a `names == "Chchd10"` row is present for all 1674 training
signatures.  That made it plausible for a held-out `Chchd10` perturbation to
produce one DEG through direct depletion of its own RNA.

Key observed training counts used for the Chchd10 comparison were:

| training target | focal n_degs | focal expression evidence |
| --- | ---: | --- |
| `Chchd2` | 1 | The only focal FDR gene was `Chchd2` itself: logFC -0.880, score -11.86, q=3.18e-28. mtISR markers such as `Asns`, `Ddit3`, `Chac1`, `Mars1`, and `Mthfd2` all had q=1. |
| `Micos13` | 0 | No focal FDR genes; the best adjusted p-values in the whole profile were q=1. |
| `Opa1` | 37 | Clear positive cristae-stress comparator. `Asns`, `Mars1`, `Chac1`, `Ddit3`, `Cars`, `Mthfd2`, `Slc7a5`, and `Slc7a1` were induced at q<0.05, and `Opa1` itself was depleted. |
| `Cox4i1` | 0 | No focal FDR genes; `Cox4i1` itself was depleted nominally but did not pass FDR, q=0.176. |
| `Cox5a` | 1 | One focal FDR gene, `Cox5a` itself. |
| `Cox6a1` | 0 | No focal FDR genes. |
| `Ndufs2` | 1 | One focal FDR gene, `Ndufs2` itself. mtISR markers were absent. |
| `Ndufs4` | 0 | No focal FDR genes. |
| `Ndufa4` | 1 | One focal FDR gene, `Ndufa4` itself. |
| `Ndufa9` | 0 | No focal FDR genes. |
| `Uqcrq` | 1 | One focal FDR gene, `Gpr180`, with no coherent mtISR marker induction. |
| `Tomm40` | 1 | One focal FDR gene, `Tomm40` itself. |
| `Park7` | 1 | One focal FDR gene, `Park7` itself. |
| `Snca` | 0 | No focal FDR genes. |
| `Yme1l1` | 0 | No focal FDR genes. |
| `Mff` | 0 | No focal FDR genes. |
| `Coa8` | 0 | No focal FDR genes. |
| `Gfm2` | 0 | No focal FDR genes. |
| `Sucla2` | 1 | One focal FDR gene. |
| `Aco2` | 0 | No focal FDR genes. |
| `Slc25a4` | 1 | One focal FDR gene, `Slc25a4` itself. |
| `Slc25a46` | 1 | One focal FDR gene, `Slc25a46` itself. |
| `Isca2` | 1 | One focal FDR gene, `Isca2` itself. |
| `Abcb7`, `Nfs1`, `Fars2`, `Rars2`, `Lars2`, `Lonp1`, `Afg3l2`, `Clpp`, `Clpx`, `Agk` | 0 | No focal FDR genes in this candidate slice. |

The focused profile comparison also rejected the idea that weak `Chchd2`
contains a hidden Opa1-like rank pattern in this cell group.  `Chchd2` had 1
significant feature, `Opa1` had 37, and `Chchd2`'s all-gene Pearson correlations
against the mitochondrial/Parkinson comparator panel ranged only from -0.0296
to 0.0362, with zero overlap of FDR-significant genes with every comparator.
`Opa1` was similarly near-orthogonal to the weak comparators, reinforcing the
Distributed Agents corpus claim that the Opa1 amino-acid/ATF4 state is not a generic
output of every mitochondrial perturbation in this assay.

## Target-specific reasoning for Chchd10

`Chchd10` and `Chchd2` encode homologous mitochondrial intermembrane-space CHCH
proteins.  CHCHD10 localizes near cristae junctions; CHCHD10 disease variants
were first linked to a mitochondrial myopathy with ALS/FTD-like features by
Bannwarth et al. 2014, and mutant patient fibroblasts showed respiratory-chain
and cristae abnormalities.  Genin et al. 2016 placed CHCHD10 with the MICOS
network containing mitofilin/IMMT, CHCHD3, and CHCHD6, and Zhou et al. 2019
showed that CHCHD2 mutations impair CHCHD10 binding, MICOS components, and
cristae structure.  Those facts make `Chchd2`, `Micos13`, `Tomm40`, respiratory
chain genes, and `Opa1` the right training perturbations to examine; the
comparison is mechanistic, not just family-name matching.

The decisive within-dataset analog is `Chchd2`.  In the same focal cells it
registered CRISPR depletion of its own transcript but no downstream mtISR or
cristae-stress program: the focal count was `n_degs = 1`, and the sole FDR gene
was `Chchd2`.  The Distributed Agents `Chchd2:F002/F003` findings independently reached
the same conclusion across the same experiment: Opa1 can induce an ISR-like
amino-acid and one-carbon program, but `Chchd2`, `Micos13`, `Ndufs2`, `Uqcrq`,
`Yme1l1`, `Cox4i1`, `Tomm40`, `Park7`, and `Snca` were weak or flat rather
than converging on that Opa1 state.  In the focal parquet rows I saw the same
split: `Opa1` induced `Asns`, `Mars1`, `Chac1`, `Ddit3`, `Cars`, `Mthfd2`, and
`Slc7a5`, whereas `Chchd2` and the other represented mitochondrial comparators
had q=1 for those markers.

External biology argues for keeping the estimate at a singleton instead of
promoting it toward the `Opa1` count.  CHCHD2 and CHCHD10 can regulate OMA1,
OPA1 processing, cristae morphology, and the mitochondrial ISR, but strong basal
stress is more evident in double CHCHD2/CHCHD10 loss or in disease-mutant
contexts than in an isolated partial loss.  Liu et al. 2020 found that combined
CHCHD2/CHCHD10 loss activated OMA1 and affected long OPA1, consistent with
partial redundancy; Ruan et al. 2022 reported stronger ISR activation when both
proteins were knocked down than after single CHCHD2 loss; and Anderson et al.
2019 found that a Chchd10 S55L ALS/FTD knock-in produced tissue-specific toxic
gain of function whereas Chchd10 ablation by itself did not induce the same
mtISR pathology.  Nguyen et al. 2022 similarly found that mouse midbrain
dopaminergic neurons survived Chchd2 loss, supporting the broader point that
CHCHD2/10 disease alleles are not faithfully modeled by a short, single-gene
loss-of-function transcriptome.

I therefore predict that an acute sparse `Chchd10` knockout in juvenile thalamic
glutamatergic neurons would be buffered at the level of broad nuclear RNA
output.  Because `Chchd10` is measured in this focal panel and the closest
expressed mitochondrial targets often contribute exactly their own knocked-down
transcript as the single FDR gene, the best point prediction is nonzero but
minimal: **1 DEG**.

## Limits

There was no direct `Chchd10` training signature and no `Chchd10` node in the
Distributed Agents same-experiment corpus, so the prediction extrapolates from `Chchd2`
and from same-organelle training targets.  That is biologically defensible but
imperfect: CHCHD10 and CHCHD2 are paralogous rather than identical, and
CHCHD10 may have cell-type-specific abundance or guide performance that differs
from `Chchd2`.

The most fragile part of the point estimate is the single self-transcript DEG.
If the held-out guide pool edits `Chchd10` inefficiently or if CHCHD10 RNA is
too sparse in the assayed nuclei, the realized count could be 0 even if the
downstream-state prediction is correct.  Conversely, a stronger-than-expected
single-gene Chchd10 loss could, in principle, cross the OMA1/OPA1/mtISR
threshold seen with `Opa1`, but that would be extrapolation away from the
observed `Chchd2`, `Micos13`, TOMM, Complex I, Complex IV, and stress-axis
comparators.
