# DEG-count prediction trace

## Question and endpoint

I interpreted the task as a scalar holdout prediction: estimate the number of
measured genes that would have had BH-adjusted Wilcoxon `pvals_adj < 0.05` after
acute AAV-CRISPR loss of `Eef1a2` in `151 TH Prkcd Grin2c Glut` neurons. The
requested target list contains exactly one held-out perturbation:

```tsv
target_name
Eef1a2
```

`Eef1a2` is absent from both supplied training inputs, so its DEG count and its
own expression signature are not directly observed. The endpoint itself is
directly observed for the non-held-out genes in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`; the all-cell-group Parquet
is the direct differential-expression table from which those counts were
derived and is the source for exact DEG identities and focal-cell matched
nucleus counts.

## Sources used

- Declared training DEG counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression Parquet:
  `training differential-expression dataset`.
- Requested-target CSV:
  `single-target request for Eef1a2`.
- Run-local metadata: `task_bindings.json`, `coverage.json`,
  `measurement_registry.json`, and `capabilities.json`.
- Same-experiment internal corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, using bounded Finding and
  Evidence/Reference lookups for measured translation-factor analogs. This
  corpus is an interpretation layer over the same Perturb-seq experiment, not
  an independent replicate.
- External literature from PubMed:
  Chambers et al. 1998, PNAS, DOI `10.1073/pnas.95.8.4463`, PMID `9539760`;
  Khalyfa et al. 2001, JBC, DOI `10.1074/jbc.M101011200`, PMID `11294870`;
  Newbery et al. 2007, JBC, DOI `10.1074/jbc.M703962200`, PMID `17640869`;
  Abbott et al. 2009, Biochemical Society Transactions, DOI
  `10.1042/BST0371293`, PMID `19909265`;
  Griffiths et al. 2012, PLoS One, DOI `10.1371/journal.pone.0041917`, PMID
  `22848658`; McLachlan et al. 2018, Human Mutation, DOI
  `10.1002/humu.23677`, PMID `30370994`; Mohamed and Klann 2023, PNAS, DOI
  `10.1073/pnas.2307704120`, PMID `37695913`; Davies et al. 2023, Molecular and
  Cellular Neuroscience, DOI `10.1016/j.mcn.2023.103879`, PMID `37429391`.

The run manifest marked the ranking workbench, ordering validator, and bounded
predictive graph review unavailable because this is a scalar count prediction
with no ranked supervision. I therefore did not use them.

## Computations over the declared data

I first checked the focal training distribution. It has 1,674 non-held-out
targets: 469 have a nonzero focal-cell DEG count and the distribution is highly
sparse and right-skewed, with median 0, 75th percentile 1, 95th percentile 18,
and mean 14.1 DEGs.

For mechanistic analogs, I queried the focal Parquet rows for the closest
represented translation elongation, initiation, and mTOR-axis perturbations.
The exact count was recomputed from the Parquet as:

```sql
SELECT gene_target,
       count(*) FILTER (WHERE pvals_adj < 0.05) AS n_degs_fdr05,
       count(*) FILTER (WHERE pvals_adj < 0.10) AS n_degs_fdr10,
       max(n_pert_matched) AS n_pert_matched,
       max(n_ctrl_matched) AS n_ctrl_matched
FROM parquet_scan($declared_parquet)
WHERE group_name='151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
GROUP BY gene_target;
```

The focal-cell comparator counts were:

```tsv
target_name	n_degs_fdr05	n_degs_fdr10	n_pert_matched
Elp1	645	830	153
Ufc1	572	846	175
Tsc2	86	128	177
Atxn10	52	74	193
Opa1	37	45	195
Eef2	9	10	87
Mtor	2	5	188
Eif4a2	2	2	135
Eif4g1	1	1	143
Eif4h	1	1	178
Eif5a	0	1	189
Eif2ak4	0	0	194
Rptor	0	0	235
```

The eEF1 exchange-factor subunits `Eef1b2`, `Eef1d`, `Eef1g`, the alpha paralog
`Eef1a1`, and `Vars` were not present as focal training perturbations.

I then inspected exact significant focal genes for the direct elongation analogs
and the same-experiment corpus interpretation around `Eef2` and `Eif4a2`.
`Eef2`, the closest represented elongation GTPase, had 9 genes at FDR 0.05:
`Ranbp2`, `Ufd1`, `Mul1`, `Prkcsh`, `Khdc4`, `Fbxo9`, `Atl1`, `Chd8`, and
`Tnfrsf12a`, with `Stk38` just below the task threshold at FDR 0.0865. The
FDR-significant genes point to a modest endomembrane/proteostasis and
nuclear/RNA-processing response, not a wholesale integrated-stress or ribosomal
transcriptional collapse in this thalamic class.

The internal Eef2 report provided two useful checks. First, across all Eef2
responder groups, obvious translation-factor comparators did not phenocopy
`Eef2`: `Eif2ak4` and `Eif4g1` had no downstream FDR 0.10 genes in any matched
group, `Eif5a`, `Eif4a2`, and `Eif4h` each had only two total downstream genes,
and none shared a same-direction FDR 0.10 downstream gene with `Eef2`. Second,
mTOR-side regulators were also not straightforward Eef2 phenocopies: `Mtor` and
`Rptor` were nearly flat, while `Tsc2` was broader but weakly and partly
oppositely related to the Eef2-restricted signature. That made broad mTOR,
initiation-factor, or generic protein-synthesis pathway membership too weak to
justify a large `Eef1a2` count.

I also kept broader stress perturbations as counterexamples. `Elp1`, `Ufc1`,
`Tsc2`, and `Opa1` showed tens to hundreds of focal DEGs, but their measured
programs were ISR, ubiquitin-folding, mTOR, or mitochondrial stress programs
rather than an Eef2-like elongation response. They show that the thalamic class
has power to detect broad postmitotic stress when it is engaged, but they are
not close causal analogs for the expected EEF1A2 lesion.

## Target-specific reasoning

### Eef1a2

`Eef1a2` encodes the neuron- and muscle-enriched eEF1A isoform that delivers
aminoacyl-tRNAs to the ribosome as the alpha subunit of the eEF1 elongation
complex. This is mechanistically upstream of peptide elongation, whereas the
measured `Eef2` perturbation hits the subsequent ribosomal translocation step.
That makes `Eef2` the only close measured analog in this training universe.

The external knockout literature argues against treating `Eef1a2` as a
redundant housekeeping target in postnatal neurons. The mouse wasted mutation is
a deletion that abolishes `Eef1a2` expression and is sufficient to cause
post-weaning wasting, motor-neuron degeneration, and death by roughly four weeks
(Chambers et al. 1998; Newbery et al. 2007). `Eef1a1` and `Eef1a2` show a
developmental switch: eEF1A1 declines in neuronal soma as eEF1A2 rises, so by
the postnatal window used here EEF1A2 is the dominant neuronal soma isoform
(Khalyfa et al. 2001; Davies et al. 2023). Human EEF1A2 missense variants cause
neurodevelopmental disease and epilepsy, and experimental patient variants
reduce translation elongation and perturb actin bundling in neurons (McLachlan
et al. 2018; Mohamed and Klann 2023), supporting a neuron-relevant requirement
for this factor.

Those biological facts support a nonzero prediction: a successful acute indel
in `Eef1a2` should impair a limiting elongation function in postnatal neurons,
and any surviving `151 TH Prkcd Grin2c Glut` nuclei should be able to mount a
secondary RNA response. I did not scale the prediction to hundreds of DEGs,
however, for three reasons. First, the same causal class was muted in the exact
focal endpoint: `Eef2` gave only 9 focal DEGs, even though EEF2 was much broader
in upper-layer cortical neurons in the same experiment. Second, multiple
measured translation-initiation or translation-regulatory perturbations were
flat or nearly flat in the focal class despite representing essential
translation machinery. Third, this experiment samples only recovered nuclei
3-4 weeks after sparse P16 editing; complete EEF1A2 loss can drive degeneration,
so the assayed population may be biased toward edited cells with enough residual
EEF1A2 protein or monoallelic/subthreshold disruption to survive.

The final estimate is therefore a small positive count, slightly above `Eef2`'s
9 DEGs to reflect the stronger postnatal neuronal requirement for EEF1A2 once
Eef1a1 has been replaced, but still within the low two-digit range established
by the focal-cell elongation-factor response rather than the 37-645 DEG stress
programs of mechanistically different perturbations.

Prediction: `Eef1a2 = 12` DEGs at BH FDR 0.05 in `151 TH Prkcd Grin2c Glut`.

## Limits and uncertainty

This is an extrapolation from one close measured elongation analog. The eEF1
exchange-factor subunits and `Eef1a1` were absent as training perturbations, so
I could not compare `Eef1a2` to a full eEF1 complex series. `Eef2` is a strong
mechanistic comparator for cytoplasmic elongation but not an obligate complex
member of EEF1A2, and the same-experiment `Eef2` report shows that many
translation-pathway lesions do not converge at the RNA level. The acute,
mosaic, sparse CRISPR assay also measures survivor-conditioned nuclear RNA, not
allelic editing, EEF1A2 protein abundance, ribosome occupancy, protein
synthesis, axonal translation, or pre-assay depletion. A much stronger
unrecovered-cell selection effect or a buffered residual-protein state would
both move the measured DEG count away from the point estimate.
