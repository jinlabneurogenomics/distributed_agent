# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and resolved ambiguities

The requested readout is the integer number of genes with BH-adjusted Wilcoxon
`pvals_adj < 0.05` after each held-out CRISPR perturbation in `151 TH Prkcd
Grin2c Glut` neurons. The held-out target list contains one gene, `Actb`, and
`Actb` is absent as a training `gene_target` and absent from the training
`n_degs` CSV. I treated the supplied focal-cell `n_degs` table as the exact
endpoint for visible perturbations and the all-cell differential-expression
Parquet as the exact expression surface for analog checks.

The endpoint is the assay-specific FDR-significant gene count in recovered
single nuclei. It is not a cell-essentiality score, an editing-efficiency
measurement, or a morphological/synaptic endpoint. I therefore predicted a
count from same-assay transcriptional analogs first and used external biology
only to decide which visible perturbations were plausible analogs or
counterexamples.

## Sources used

- Declared training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
- Declared all-cell DE rows:
  `training differential-expression dataset`
- Requested target manifest:
  `single-target request for Actb`
- Internal same-experiment corpus: `perturbai-july-260713-sourceguard-1773-v1`,
  especially the bounded `Actg1` report and the BioKG relation index used only
  to find the Actg1 report that explicitly compared `Actb`.
- External literature from NCBI PubMed:
  Bunnell and Ervasti 2010, DOI `10.1002/cm.20467`, PMID `20662086`;
  Perrin, Sonnemann and Ervasti 2010, DOI `10.1371/journal.pgen.1001158`,
  PMID `20976199`; Bunnell, Burbach, Shimizu and Ervasti 2011,
  DOI `10.1091/mbc.E11-06-0582`, PMID `21900491`; Riviere et al. 2012,
  DOI `10.1038/ng.1091`, PMID `22366783`; Patrinostro et al. 2018,
  DOI `10.1073/pnas.1807895115`, PMID `30012594`; Sundby et al. 2022,
  DOI `10.1091/mbc.E22-02-0054`, PMID `35594181`; Wu et al. 2016,
  DOI `10.1016/j.neuron.2016.10.014`, PMID `27840001`; Klein et al. 2013,
  DOI `10.1073/pnas.1209811110`, PMID `23382180`.

## Computations over the declared data

I first summarized the visible focal-cell counts. The training endpoint has
1,674 perturbations; 1,205 have zero DEGs, the median is 0, the 75th percentile
is 1, and the mean is inflated to 14.1 by a small number of large responses
such as `Uba5`, `Tpr`, and `Sin3a`. Thus a one- or zero-DEG prediction is not a
special null assumption; it is the modal behavior in this focal cell class.

I then selected visible genes around the cytoplasmic actin network and checked
their exact focal-cell FDR 0.05 burdens. The non-obvious Parquet query was:

```sql
SELECT gene_target,
       COUNT(*) FILTER (WHERE pvals_adj < 0.05) AS n_fdr05,
       COUNT(*) FILTER (WHERE pvals_adj < 0.10) AS n_fdr10,
       COUNT(*) FILTER (WHERE pvals < 0.05) AS n_nominal,
       MIN(pvals_adj) AS min_fdr,
       MAX(n_pert_matched) AS n_pert,
       MAX(n_ctrl_matched) AS n_ctrl
FROM parquet_scan($training_parquet)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN $actin_related_training_targets
GROUP BY gene_target;
```

That query showed the closest and pathway-near perturbations were all tiny in
`151`: `Actg1` 1, `Actn4` 0, `Cfl2` 0, `Cyfip1` 0, `Cyfip2` 1, `Cdc42` 1,
`Rac1` 0, `Pak1` 1, `Pak2` 0, `Pak3` 0, `Limk1` 0, `Fmn1` 0, `Fmn2` 0,
`Diaph2` 0, `Tpm1` 0, `Tpm3` 0, `Myo5a` 1, `Myo6` 0, `Myo9a` 0, `Add1` 0,
`Add2` 0, and `Add3` 0. The one-hit calls for `Actg1`, `Cdc42`, `Cyfip2`,
`Myo5a`, and `Pak1` were their own targeted transcript rows, not a shared
downstream actin or stress program. For `Actg1` specifically in `151`, the
Parquet gave `Actg1` logFC `-0.824`, FDR `9.85e-16`, 227 perturbed nuclei and
23,679 controls; probed actin-neighbor transcripts such as `Cdc42`, `Cyfip1`,
`Cyfip2`, `Pak1`, `Rac1`, `Tuba1a`, `Tuba4a`, `Tubb4b`, and `Tubb5` all had
FDR `1.0`.

The July same-experiment Actg1 report independently packaged the same pattern
at a slightly looser FDR 0.10 reporting threshold: `Actg1` was measured in
22 of 23 cell groups, its transcript trended down in every measured group, but
only two downstream genes across all groups reached FDR 0.10, with zero
downstream FDR 0.10 genes in `151 TH Prkcd Grin2c Glut`. The report also
tested a literature-nominated actin set including `Rac1`, `Cdc42`, `Cyfip1`,
`Cyfip2`, `Mrtfa`, `Flnb`, `Fmn2`, `Pak1`, `Pak2`, `Pak3`, myosins, and
tropomyosins and found that these perturbations did not phenocopy the sparse
Actg1 responder classes.

I kept tubulin genes as counterexamples rather than as Actb analogs:
`Tuba1a`, `Tuba4a`, `Tubb4b`, and `Tubb5` had focal counts of 7, 2, 1, and 1.
Their signatures were dominated by tubulin self/paralog feedback, for example
`Tuba1a` down with induction of `Tubb3`, `Tubb2a`, `Tuba4a`, `Tubb4a`,
`Tubb4b`, and `Tubb5`. That is an autoregulatory microtubule response, not the
response seen after cytoplasmic actin or Rho/WAVE perturbation.

## Target-specific reasoning

### `Actb`

The most direct within-dataset analog is `Actg1`, the other nonmuscle
cytoplasmic actin. External evidence supports using it as the closest analog:
Actb/beta-actin and Actg1/gamma-actin proteins are 99% identical and differ by
four amino acids, and mouse gene-editing experiments showed that replacing the
Actb coding sequence with gamma-actin protein rescues the overt lethality and
fibroblast-proliferation phenotypes of Actb deletion, separating several
severe Actb-null phenotypes from loss of the beta-actin protein itself
(Patrinostro et al. 2018; Sundby et al. 2022). The analog is not perfect:
Actb-null embryos and Actb-null fibroblasts have stronger growth and migration
defects than Actg1-null models (Bunnell et al. 2011), while Actg1-null mice
show delayed embryonic growth and perinatal survival defects rather than the
earlier Actb-null lethality (Bunnell and Ervasti 2010). However, both sets of
strong phenotypes are mostly developmental, proliferative, or morphologic, not
obligate broad transcriptional responses in already postmitotic P16-P37/44
NeuN-positive neurons.

The causal transfer chain is therefore weak in exactly the direction needed for
the requested endpoint. An `Actb` guide should perturb a core actin subunit and
could alter F-actin, dendritic spine structure, synaptic vesicle endocytosis,
or neurite mechanics. Beta-actin mRNA localization and synaptic beta-actin
translation have been tied to excitatory synapse number (Klein et al. 2013),
and beta/gamma actin support synaptic endocytosis in knockout preparations
(Wu et al. 2016). Those observations predict cytoskeletal and synaptic
phenotypes if the perturbation is strong enough, but they do not require a
large nuclear RNA program by 3-4 weeks in surviving thalamic glutamatergic
nuclei.

The visible perturbations test this distinction in the focal cell group.
`Actg1` loss gave only the `Actg1` self-transcript hit and no FDR 0.10
downstream genes in `151`; `Cfl2`, `Rac1`, `Cyfip1`, `Limk1`, formins,
tropomyosins, `Pak2`, and `Pak3` were all FDR-zero; `Cdc42`, `Cyfip2`,
`Myo5a`, and `Pak1` again only counted their self rows. Thus the declared
screen is not seeing a broad SRF, immediate-early, Rho/WAVE, or cytoskeletal
compensation program after actin-network loss of function in this cell class.
Human ACTB/ACTG1 Baraitser-Winter syndrome further does not demand a high
count here, because the disease mutations reported by Riviere et al. were
mostly de novo missense alleles affecting development, while this experiment is
postnatal CRISPR loss of function.

I therefore predicted no FDR 0.05 downstream genes for `Actb`. I did not add
one for the self transcript: the Actg1 report notes that `Actb` was absent from
the Actg1 output-gene rows, so there was no direct evidence that `Actb` would
be one of the measured genes able to contribute an automatic self-knockdown
count in this Parquet-defined readout. The point estimate is `0` rather than
`1` because the closest transferable focal-cell evidence is Actg1 downstream
zero, not Actg1 total including its measured self row.

## Limits

The prediction is extrapolative because the exact `Actb` perturbation was held
out and no Actb-specific differential-expression rows were present in the
declared inputs. The strongest external Actb evidence comes from embryonic
knockouts, fibroblasts, hair cells, and synaptic physiology rather than the
same thalamic glutamatergic population, and the Perturb-seq assay is a partial,
sparse CRISPR perturbation read out in surviving nuclei rather than complete
protein depletion. A severe Actb hit could in principle cause selection,
morphology, or synapse defects without leaving many recoverable DEG calls.

The main quantitative uncertainty is the zero-versus-one boundary. If Actb was
both measured and significantly depleted in the held-out DE surface, the
endpoint could gain a single self row despite no downstream response. I treated
that as less likely than a downstream-zero count because the same-experiment
Actg1 report explicitly lacked `Actb` as an output gene and because the task
requires the Parquet-defined measured-gene count rather than a guaranteed
self-transcript assay.
