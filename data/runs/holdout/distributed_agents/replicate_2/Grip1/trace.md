# Grip1 held-out DEG-count prediction

## Question and resolved ambiguities

The requested target list contains one held-out perturbation, `Grip1`. I interpreted the endpoint as the exact `n_degs` used in `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: the number of rows for a target in `151 TH Prkcd Grin2c Glut` whose measured gene has `pvals_adj < 0.05` in the matched perturbed-versus-control Wilcoxon test. This includes the perturbed transcript itself when it is one of the measured genes and passes FDR. I therefore separated total significant rows from "downstream" rows with `names != gene_target` when judging analogs.

`Grip1` is completely held out, so I could not use a same-target expression signature or DEG count. I predicted by transferring from training perturbations in the same focal cell group, using external gene function only to decide which training genes were mechanistically comparable.

## Sources used

- Differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Focal training counts: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Requested target manifest: `[local file: 100_Grip1.csv]`.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`. I used it for bottom-up findings around represented AMPAR, PSD, and AMPAR-trafficking perturbations.
- NCBI PubMed literature queries for the biology of GRIP1 and AMPA-receptor trafficking.

Key literature:

- Dong et al. 1997, PMID 9069286, DOI `10.1038/386279a0`: identified GRIP as a seven-PDZ synaptic protein that binds the C termini of AMPA-receptor subunits.
- Wyszynski et al. 1999, PMID 10414981, DOI `10.1523/JNEUROSCI.19-15-06528.1999`: showed native GRIP1/GRIP2 association with GluR2/3 AMPARs in brain and localization at excitatory synapses, while also noting GRIP is not only an AMPAR-bound protein pool.
- Setou et al. 2002, PMID 11986669, DOI `10.1038/nature743`: showed GRIP1 can bind kinesin heavy chains and steer dendritic transport relevant to AMPAR trafficking.
- Hoogenraad et al. 2005, PMID 15965473, DOI `10.1038/nn1487`: found that GRIP1 knockdown in cultured hippocampal neurons mislocalized GluR2, EphB2, and KIF5 and impaired dendrite morphogenesis, supporting a transport/scaffold role.
- Takamiya et al. 2008, PMID 18509036, DOI `10.1523/JNEUROSCI.0654-08.2008`: showed functional redundancy of GRIP1 and GRIP2 in cerebellar LTD, with single deletion of either isoform sparing LTD.
- Tan et al. 2020, PMID 32948689, DOI `10.1073/pnas.2014827117`: showed neuronal GRIP1 is required for synaptic AMPAR accumulation during LTP and for normal hippocampal LTP and learning/memory.

## Dataset computations

The held-out manifest has exactly one target:

```tsv
target_name
Grip1
```

The focal training-count table has 1,674 non-held-out perturbations. Its response breadth is very zero-heavy: the median is 0, the 75th percentile is 1, the 90th percentile is 2, the 95th percentile is 18, and the maximum is 2,677.

The DE parquet is sorted by `group_name`; I identified row groups 546-580 as covering `151 TH Prkcd Grin2c Glut` and queried only this focal group. For each candidate analog I counted all FDR 0.05 rows and non-self FDR 0.05 rows:

```sql
select
  gene_target,
  count(*) as n_rows,
  sum(pvals_adj < 0.05) as n_fdr05,
  sum(case when names != gene_target and pvals_adj < 0.05 then 1 else 0 end)
    as n_downstream_fdr05
from read_parquet(...)
where group_name = '151 TH Prkcd Grin2c Glut'
  and gene_target in (...)
group by gene_target;
```

I also checked self-transcript rows, pathway transcripts such as `Grip1`, `Grip2`, `Gria1`, `Gria2`, `Gria3`, `Gria4`, `Dlg4`, `Dlgap4`, `Shank2`, `Shank3`, `Homer1`, `Homer2`, `Cacng2`, `Cacng3`, `Cnih2`, `Cnih3`, `Shisa6`, `Pick1`, and `Nsf`, and every focal row with `pvals_adj < 0.20` for the Grip1-neighborhood targets. Those rows are in `analog_focal_rows.tsv`.

Finally, I built a run-local focal profile comparison for a curated Grip1-relevant cohort:

`Gria1, Gria2, Gria3, Cacng2, Cacng3, Dlg4, Shank2, Shank3, Homer2, Syngap1, Nsf, Grin1, Dlgap4`

The profile comparison reported nine of these thirteen as having no significant focal features, three as having one to nine, and only `Grin1` as having at least fifty. In the compact inspection:

| target | focal FDR 0.05 rows | direction balance |
|---|---:|---|
| `Gria2` | 0 | 0 positive, 0 negative |
| `Dlg4` | 1 | 0 positive, 1 negative |
| `Shank3` | 2 | 1 positive, 1 negative |
| `Dlgap4` | 2 | 0 positive, 2 negative |
| `Grin1` | 89 | 40 positive, 49 negative |

The raw focal parquet rows show that `Dlg4`, `Grik5`, `Grin2a`, `Camk2b`, `Caskin1`, `Abhd12`, `Adam22`, and `Atad1` had self-transcript-only calls in this cell type; `Shank3` had its self row plus `Uba5`; `Dlgap4` had its self row plus `Vgf`; `Grin2b` had its self row plus `Pianp`; and `Grin1` had a broad 89-row response.

## Target-specific reasoning

### Grip1

**External mechanism.** `Grip1` encodes glutamate receptor-interacting protein 1, a multi-PDZ scaffold for GluA2/3-containing AMPARs (Dong et al. 1997; Wyszynski et al. 1999). Its literature phenotype is mainly local trafficking, anchoring, and synaptic plasticity rather than a direct transcription-factor or chromatin-regulator function. GRIP1 can couple cargo to kinesin motors for dendritic delivery (Setou et al. 2002), knockdown can disturb GluR2/EphB/KIF5 localization and dendrite morphology in developing hippocampal cultures (Hoogenraad et al. 2005), GRIP1 and GRIP2 show redundancy in cerebellar LTD assays (Takamiya et al. 2008), and neuronal Grip1 knockout impairs AMPAR accumulation during LTP (Tan et al. 2020).

**Most relevant represented perturbations.**

- `Gria1`, `Gria2`, `Gria3`: direct AMPAR pore-forming subunits and the closest receptor-side partners available in the training parquet. Each had `n_degs = 0` in `151 TH Prkcd Grin2c Glut`, with zero non-self rows. The same-experiment Distributed Agents corpus states that represented AMPAR-core subunits were nearly silent and did not form an interchangeable AMPAR-loss nuclear RNA program; its Gria2 finding in particular contrasted `Gria1`, `Gria3`, `Cacng2`, `Cacng3`, and `Dlg4` as shared near-null AMPAR-core/TARP/scaffold comparators.
- `Cacng2` and `Cacng3`: TARP auxiliary AMPAR-trafficking/scaffolding genes. Both had `n_degs = 0`. The Distributed Agents `Cacng2` finding summarized that `Cacng3`, `Dlg4`, and `Gria1/2/3` were flat or almost flat, supporting the view that this represented AMPAR trafficking/scaffolding axis is post-transcriptional or buffered in the juvenile basal snRNA readout.
- `Nsf`: part of AMPAR/GluA2 trafficking, and an internal counterexample to mapping all GluA2-trafficking biology to RNA. It had `n_degs = 0` in the focal group. The Distributed Agents `Atad1` finding noted that although ATAD1/Thorase biology touches GluA2/GRIP1 AMPAR trafficking, `Nsf` and `Gria1/2/3` did not phenocopy the active Atad1 thalamic signature.
- `Dlg4`, `Shank2`, `Shank3`, `Dlgap4`, `Homer2`, `Syngap1`: PSD scaffolds downstream or adjacent to glutamate receptors. `Dlg4` had `n_degs = 1`, but that one row was the `Dlg4` self-transcript only; `Shank2`, `Homer2`, and `Syngap1` had `n_degs = 0`; `Shank3` had `n_degs = 2`, comprising `Shank3` itself and `Uba5`; and `Dlgap4` had `n_degs = 2`, comprising `Dlgap4` itself and `Vgf`. The Distributed Agents `Dlg4` and `Shank3` findings both emphasize that represented postsynaptic scaffold and synaptic-adhesion perturbations mostly fail to induce a shared steady-state RNA module in this P16 screen.
- `Grik1`, `Grik3`, `Grik4`, `Grik5`: kainate receptor relatives. They are weaker analogs than AMPAR genes because GRIP1 is known for GluA2/3 AMPAR trafficking, but they still help calibrate glutamate-receptor subunit loss. The focal counts were `0, 0, 0, 1`, and the `Grik5` row was self only.
- `Grin1`, `Grin2a`, `Grin2b`: NMDAR subunit counterexamples. They show the assay can detect receptor-coupled nuclear changes in this focal class, but they are mechanistically less appropriate than AMPAR/PSD genes because NMDARs couple Ca2+ entry to transcription differently. `Grin1` was the clear positive control with `89` focal DEGs, whereas `Grin2a` had a self-only `1` and `Grin2b` had `2` rows. The Distributed Agents Gria and Dlg4 findings make the same contrast: NMDAR perturbations can be visible where AMPAR/scaffold perturbations are flat.
- Additional synaptic-neighborhood genes `Baiap2`, `Adam22`, `Abhd12`, and `Caskin1` were used as counterexamples against a generic synapse-gene effect: their focal counts were `0, 1, 1, 1`, respectively, and the three nonzero cases were self only.

**Decision.** I predicted `Grip1 = 0`.

The Grip1 prior is not "any glutamate receptor gene can respond." In this exact focal cell type, directly represented AMPAR subunits had zero calls, TARP/AMPAR trafficking genes had zero calls, and PSD scaffolds were either zero or one isolated downstream singleton. Grip1 sits on the buffered AMPAR-trafficking side of the internal boundary, not on the `Grin1` NMDAR side that produced 89 focal DEGs. The external biology also points to receptor localization, kinesin-dependent trafficking, and plasticity readouts; those are all poorly matched to a sparse, postmitotic, 3-4 week nuclear RNA endpoint unless the perturbation secondarily drives stress or activity-dependent transcription, which the AMPAR/TARP/PSD analogs did not.

The remaining question is whether the `Grip1` self-transcript alone would pass FDR. Across all 1,674 focal training perturbations only 319 of 1,642 measurable self rows were self-significant, and among the closest focal analogs the AMPAR genes `Gria1/2/3`, the TARPs `Cacng2/3`, `Nsf`, `Shank2`, `Homer2`, and `Syngap1` did not pass FDR for their own transcripts. `Dlg4` and `Shank3` did pass self with 273 and 280 perturbed nuclei, so a one-row outcome is possible. I nevertheless called zero because GRIP1 is a scaffolding/trafficking molecule with GRIP-family redundancy, GRIP1 protein loss was not directly measured, average mRNA depletion in this assay is modest, and the direct AMPAR subunits and TARP comparators most likely to share a local AMPAR-synapse response were self-flat in this same cell group.

## Limits and extrapolation

- `Grip1` itself and its paralog `Grip2` were absent from the training perturbations, so there is no same-gene or same-family count to copy.
- Several important AMPAR auxiliary or trafficking genes were also absent as perturbations, including `Gria4`, `Cnih2`, `Cnih3`, `Shisa6`, and `Pick1`; I could only check their mRNA values downstream of represented analogs.
- The predicted count is dominated by same-experiment negative evidence. It does not imply GRIP1 is biologically unimportant, only that sparse postnatal Grip1 loss is unlikely to generate a focal steady-state nuclear RNA program with one or more FDR 0.05 rows.
- Many profile similarities among zero-response genes are not mechanistic signatures; sparse profiles can look similar because most genes are nonsignificant. I used expression profiles to confirm the absence of shared FDR-level AMPAR/PSD programs, not to average arbitrary nearest neighbors into a numeric estimate.
- A prediction of `0` is most sensitive to the self-transcript row. If the held-out guide set happened to produce stronger Grip1 mRNA decay in this focal cell group, the true count could plausibly be `1` even while the downstream response remained zero.
