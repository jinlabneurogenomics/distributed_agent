# Nalcn DEG-count prediction

## Question and endpoint

The run asks for a point prediction of `n_degs` for the held-out perturbation
`Nalcn` in `151 TH Prkcd Grin2c Glut` cells. I treated `n_degs` as the exact
task endpoint: the number of measured genes with Benjamini-Hochberg adjusted
Wilcoxon `pvals_adj < 0.05` in recovered nuclei from the focal thalamic
glutamatergic group.

The requested manifest contains one row:

| target_name |
|---|
| Nalcn |

`Nalcn` was not present in the supplied training DEG-count CSV and the
channelosome partners `Unc79`, `Unc80`, and `Fam155a` also had no focal-cell
training endpoint. Therefore the held-out endpoint is absent from the declared
inputs; the prediction below transfers from non-held-out perturbations of other
ion channels and uses external NALCN biology only to decide which transfers are
mechanistically plausible.

## Sources used

- Declared training endpoints:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  This CSV contains the directly observed `151 TH Prkcd Grin2c Glut` DEG count
  for 1,674 non-held-out perturbations.
- Declared differential-expression table:
  `training differential-expression dataset`.
  I used this for the focal-cell expression signatures, matched recovered-cell
  counts, and independent recomputation of FDR<0.05 gene counts for selected
  analogs. This is the same experiment as the CSV, not independent replication.
- Run-local dataset context and measurement registry under
  `codex_runtime/pipeline`, used for schema and measurement limits. In
  particular, target mRNA down-regulation was treated as QC context, not as a
  measure of editing efficiency.
- The July PerturbAI same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`; only the compact calibration
  summary and bounded `Cacna1g` Finding inventory were informative for this
  target. The corpus is an interpretation layer over the same Perturb-seq
  experiment and was not counted as a second dataset.
- PubMed literature for NALCN function and complex membership:
  - Lu et al., 2007, Cell, DOI `10.1016/j.cell.2007.02.041`, PMID `17448995`.
  - Lu et al., 2010, Neuron, DOI `10.1016/j.neuron.2010.09.014`, PMID
    `21040849`.
  - Chua et al., 2020, Science Advances, DOI `10.1126/sciadv.aaz3154`, PMID
    `32494638`.
  - Kang and Chen, 2022, Nature Communications, DOI
    `10.1038/s41467-022-30403-7`, PMID `35550517`.

The ranking feature workbench, ordering validator, and bounded predictive graph
review were not used because the capability manifest marks them unavailable for
this scalar count task without explicit ranked or partial-ranked supervision.

## Quantitative calibration from the declared dataset

I first counted direct FDR<0.05 hits in the focal cell group for visible
non-held-out perturbations that could plausibly bracket NALCN:

```sql
SELECT gene_target,
       count(*) AS measured,
       sum(CASE WHEN pvals_adj < 0.05 THEN 1 ELSE 0 END) AS n_sig,
       max(n_pert_matched) AS n_pert_matched,
       max(n_ctrl_matched) AS n_ctrl_matched
FROM read_parquet(training_de_all_cell_groups.parquet)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
GROUP BY gene_target;
```

The selected rows all had 17,259 measured genes and 23,679 matched controls in
the focal comparison; `n_pert_matched` ranged from 90 to 288 among the selected
channel targets. The counts below are FDR<0.05 counts from the Parquet and
match the training CSV.

| perturbation | focal `n_degs` | focal signature evidence |
|---|---:|---|
| `Cacna1g` | 12 | Small but real thalamic signature: `Cacna1g` itself was down and 11 other genes passed FDR<0.05, led by up-regulated `Ptprn`, `Iyd`, `Serpine2`, `Notum` and down-regulated `Stmn4`, `Cpne7`, `Ly6e`, `Zdhhc22`, `Jun`, `Lrrc7`, and `Irag1`. The same-experiment corpus reports that this footprint is narrowly thalamic and does not phenocopy other represented voltage-gated calcium-channel perturbations. |
| `Cacna1a`, `Cacna1d`, `Cacna1e` | 0, 0, 0 | No FDR<0.05 genes in the focal group. These are voltage-gated calcium-channel pore-forming genes but not the T-type thalamic channel `Cacna1g`. |
| `Cacna2d1`, `Cacnb4` | 1, 1 | The only significant gene was the perturbed transcript itself. |
| `Cacna2d2`, `Cacnb2`, `Cacng2`, `Cacng3` | 0, 0, 0, 0 | No FDR<0.05 focal response. |
| `Scn1a`, `Scn2a`, `Scn8a` | 1, 1, 1 | For each voltage-gated sodium-channel pore gene, the sole significant row was self-target down-regulation. |
| `Scn1b` | 2 | `Scn1b` itself and `Jun` were significant; this is still a near-null downstream response. |
| `Scn3a` | 0 | No significant focal response. |
| `Hcn1`, `Hcn2` | 0, 1 | `Hcn2` had only self-target down-regulation; `Hcn1` had none. |
| `Kcnq1`, `Kcnq2`, `Kcnq3` | 0, 1, 1 | `Kcnq2` and `Kcnq3` had only self-target down-regulation. |
| `Kcna1`, `Kcna2`, `Kcnb1`, `Kcnb2`, `Kcnt1`, `Kcnt2` | all 0 | No significant focal response. |
| `Grin1` | 89 | A broader synaptic-receptor counterexample, with `Grin1` down-regulation and induction of a downstream synaptic/activity signature. It is relevant to the same thalamic glutamatergic neurons but less causal-specific than resting leak conductances. |
| `Atp1a3` | 80 | A broader ionic-homeostasis counterexample. `Atp1a3` loss strongly changed its own transcript plus `Atp2a2`, `Ache`, `Prkcg`, `Rgs16`, `Notum`, `Srxn1`, and other genes. The ATPase is expected to disturb ion gradients directly, not just one depolarizing background conductance. |
| `Atp2a2`, `Atp2b1` | 187, 22 | Calcium-pump perturbations caused endoplasmic-reticulum or calcium-clearance signatures, including `Ddit3`, `Xbp1`, `Herpud1`, `Hspa5` for `Atp2a2` and immediate-early genes for `Atp2b1`. These were treated as high-side counterexamples rather than close NALCN analogs. |

This calibration argues against a broad stress or immediate-early prediction
for `Nalcn`. In the same postnatal mosaic assay, most channel genes that change
excitability directly produced zero or a single focal DEG. The one closest
thalamic channel response, `Cacna1g`, reached 12 FDR<0.05 genes, but the July
corpus and the raw signature both show a specific T-type calcium-channel
program rather than a pan-channel response.

## Target-specific reasoning

### Nalcn

**Biology.** NALCN is the pore-forming component of a nonselective Na+ leak
channel that helps set neuronal resting membrane potential. Mouse `Nalcn`
mutants lack a TTX- and Cs+-resistant background Na+ current in hippocampal
neurons, show reduced neuronal firing in brainstem-spinal-cord recordings, and
die neonatally with disrupted respiratory rhythm (Lu et al., 2007). Extracellular
Ca2+ control of that background Na+ leak current requires the
UNC79-UNC80-NALCN complex, and `nalcn` or `unc79` knockout neurons lose the
excitatory response to lowered extracellular Ca2+ (Lu et al., 2010). Later
reconstitution and structural work established that NALCN, FAM155A, UNC79, and
UNC80 form a channelosome: co-expression of UNC79, UNC80, and FAM155A is needed
for robust NALCN currents in heterologous cells (Chua et al., 2020), and
UNC79-UNC80 scaffold NALCN-FAM155A and regulate NALCN localization and
self-inhibition (Kang and Chen, 2022).

**Causal transfer model.** The perturbation is acute CRISPR loss of the NALCN
pore in postnatal neurons. The direct molecular effect should reduce the NALCN
depolarizing leak conductance in cells where enough alleles are disrupted. That
propagates to a more hyperpolarized resting potential and altered basal
excitability, then could secondarily change activity-regulated transcripts.
The measured endpoint is the survivor-conditioned nuclear RNA signature three
to four weeks later, so it is expected to be weaker than embryonic or germline
phenotypes and it will miss cells that are selected out before nuclei are
recovered.

**Within-dataset analogs.** The direct NALCN complex would have been the clean
comparison set, but `Unc79`, `Unc80`, and `Fam155a` lacked training DEG counts
in this input. Among visible pore-forming excitability genes, voltage-gated Na+
channels were near-null in the focal cell type: `Scn1a`, `Scn2a`, and `Scn8a`
each produced only a self-transcript DEG, `Scn1b` produced only two total DEGs,
and `Scn3a` produced zero. Other resting or subthreshold excitability
comparators also favored a null or self-only footprint: `Hcn1` was zero,
`Hcn2` was self-only at one DEG, and `Kcnq2`/`Kcnq3` were self-only at one DEG.
The represented voltage-gated Ca2+ channel family had the same pattern except
for `Cacna1g`: `Cacna1a`, `Cacna1d`, and `Cacna1e` were zero and the auxiliary
subunits were zero or self-only, whereas `Cacna1g` had a narrowly thalamic
12-gene signature. `Nalcn` is functionally closer to leak or background
excitability than to the broad `Atp1a3` ion-gradient and `Atp2a2` ER-stress
responses, so I used those pump perturbations only as high-side bounds.

**Prediction.** I predict a nonzero but minimal focal response, `1` DEG. The
nonzero call comes from NALCN being an obligate pore for an established neuronal
background Na+ conductance and the fact that `Nalcn`, `Unc79`, and `Unc80` are
measured in the focal Parquet rows. The very small count comes from the
declared training data: most acute channel knockouts in this thalamic group
produce zero or self-only FDR<0.05 calls, and the Cacna1g-specific 12-gene
program is the exception rather than the rule. I did not promote toward
`Grin1`, `Atp1a3`, or `Atp2a2` because those perturbations act through
receptor-mediated synaptic drive or ion-gradient/ER-calcium collapse and their
signatures contain downstream programs not expected from partial NALCN leak
reduction in recovered postnatal neurons.

## Final predicted count

| target_name | predicted_n_degs |
|---|---:|
| Nalcn | 1 |

## Limits

- The requested `Nalcn` signature is completely held out, and no direct
  NALCN-channelosome partner in the training CSV supplied an observed focal
  DEG count. The prediction therefore extrapolates from looser excitability
  analogs rather than from `Unc79`, `Unc80`, or `Fam155a`.
- The FDR<0.05 count is assay- and power-dependent. It includes self-transcript
  rows when those pass the statistical cutoff, but self-target down-regulation
  is not an editing-efficiency estimate in this mosaic CRISPR assay.
- Literature on NALCN establishes a membrane-current and excitability role, not
  a specific snRNA-seq DEG burden in postnatal `151 TH Prkcd Grin2c Glut`
  neurons. The external evidence supports a biologically non-null perturbation,
  while the approximate count is driven mainly by the within-dataset
  near-null behavior of other channel perturbations.
- Germline mouse lethality and heterologous channelosome reconstitution occur
  at different causal stages than this experiment. They support the direction
  from `Nalcn` loss to reduced NALCN current, but not broad transcriptional
  stress among recovered nuclei after sparse postnatal AAV editing.
