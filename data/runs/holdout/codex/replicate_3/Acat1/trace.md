# Acat1 n_degs forecast

## Declared endpoint and target

- Target: `Acat1`, the single row in the declared holdout manifest
  `[local file: Acat1.csv]`.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, counted as measured genes with Wilcoxon `pvals_adj < 0.05`.
- Training scalar source: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Training profile source: `[local file: training_de_all_cell_groups.parquet]`.
- Biology-only target bundle: `[local file: Acat1.json]`.

## Biology prior

The declared biology bundle makes Acat1 a reachable but not obviously
high-output postmitotic neuronal perturbation.

- Exact in-assay reach is strong: in non-target nuclei of
  `151 TH Prkcd Grin2c Glut`, `Acat1` is detected in 21,744 of 23,679 cells
  (`91.83%`), with mean raw UMI `3.36`, mean CP10k `2.10`, and pseudobulk
  CPM `210.66`.
- ACAT1 is a mitochondrial acetyl-CoA/acetoacetyl-CoA thiolase used in
  ketone-body and isoleucine metabolism. The bundle adjudicates the operative
  stock as a renewable mitochondrial catalytic protein and concludes that a
  P16 disruptive edit should likely deplete functional ACAT1 by the P37-P44
  harvest window.
- The phenotypic evidence is less matched to this assay: the closest loss
  phenotype is human biallelic ACAT1 deficiency with episodic systemic
  ketoacidosis and neurological injury. The bundle did not find a matched
  mouse postnatal thalamic neuron loss-of-function study, and it reports no
  direct evidence that the related cytosolic thiolase `Acat2` compensates for
  mitochondrial ACAT1 in this cell class.

I therefore treated Acat1 as likely edited in an expressing population but
with unresolved coupling between loss of this specific metabolic step and a
large survivor-conditioned thalamic snRNA-seq response.

## Training evidence

The focal training count table contains 1,674 non-held-out targets. Its
distribution is extremely sparse:

- median `n_degs`: `0`
- mean `n_degs`: `14.05`
- zero-DEG targets: `1205 / 1674`
- one-DEG targets: `276 / 1674`
- targets with `n_degs >= 20`: `80 / 1674`
- targets with `n_degs >= 100`: `43 / 1674`

I nominated available Acat1 comparators from curated mouse pathway and
functional annotations with the packaged gene-analog workflow and wrote the
full run-local record to `workbench/acat1_gene_analogs.jsonl`. Acat1 itself is
absent from the same-experiment ledger and BioKG projection in that record, so
the nominations came only from curated annotations. The record found no
training-available exact paralog or same-complex analog and 35
training-available narrow-module candidates, mostly in CoA/lipid, TCA,
pyruvate, fatty-acid, butanoate, and branched-chain amino-acid modules.

Those narrow candidates in the declared 151 count table were mostly silent:

- 22 of 35 had `n_degs = 0`.
- 11 of 35 had `n_degs = 1`.
- Only two had more than one DEG: `Mdh1` with 29 and `Dhdds` with 116.
- The most Acat1-proximal isoleucine or branched-chain amino-acid candidates
  were all zero: `Auh`, `Bckdhb`, `Bckdk`, `Ivd`, and `Pcca` each had
  `n_degs = 0`.

I then inspected the exact focal Parquet profiles of the 35 narrow nominees.
`workbench/narrow_analog_focal_metrics.csv` records derived 151-class metrics
from the Parquet, and the profile comparison/cohort artifacts are
`workbench/narrow_analog_profile_compare.json` and
`workbench/narrow_analog_profile_cohort.json`.

The Parquet check sharpened the count-table result:

- The one-DEG narrow analogs all had only their own target transcript as the
  significant feature in this cell class.
- Among all 1,674 training targets, 237 of the 276 one-DEG outcomes were also
  self-transcript-only.
- The five Acat1-proximal BCAA/isoleucine nominees had no genes at
  `pvals_adj < 0.10`, not merely no genes below 0.05.
- Pairwise profile topology across the 35 narrow candidates was weak: 595
  candidate pairs had median positive top-tail overlap `0.025` and median
  negative top-tail overlap `0.030`, so these metabolic perturbations did not
  define a coherent transferable downstream expression state.

`Mdh1` and `Dhdds` were therefore treated as submodule outliers rather than
scale-bearing Acat1 analogs: `Mdh1` is a cytosolic malate dehydrogenase and its
29-gene signature was largely outside the direct ketone/isoleucine thiolase
story, while `Dhdds` sits in terpenoid/dolichol biosynthesis and produced a
much broader stress-like expression program not shared by the BCAA-side
nominees.

## Forecast

The strongest training signal is that acute loss of nearby mitochondrial or
CoA-metabolism genes in this thalamic class usually yields no downstream
FDR-significant program. The exact Acat1 reach and the likely depletion of a
renewable mitochondrial enzyme argue against a pure assay-null prior, but the
matched analogs put the expected downstream count near zero.

I therefore placed Acat1 at the common self-transcript-only edge of the sparse
distribution: one significant measured gene total, not a multi-gene metabolic
state.

`predicted_n_degs = 1`
