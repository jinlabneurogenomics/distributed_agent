# Acat1 DEG-count prediction

## Question interpreted

The requested target list contains one held-out perturbation:

- `Acat1`

I interpreted `n_degs` exactly as in the supplied focal-cell endpoint: the number
of measured genes with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05`
for the perturbation in `151 TH Prkcd Grin2c Glut`, inclusive of the targeted
transcript if the target RNA itself passes FDR. `Acat1` was confirmed absent from
both the focal training-count CSV and the parquet as a `gene_target`, so no
measured `Acat1` knockout signature was used.

One ambiguity I resolved was nomenclature. Mouse `Acat1` is mitochondrial
acetyl-CoA acetyltransferase 1, also called mitochondrial acetoacetyl-CoA
thiolase or beta-ketothiolase/T2. I treated it as a ketone-body and isoleucine
catabolic enzyme, not as the cholesterol-esterification enzyme often called
ACAT1 in older pharmacology papers; the latter is `Soat1` in mouse.

## Sources used

- The supplied focal training-count table
  `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`. This set the assay scale:
  1,205 of 1,674 non-held-out perturbations had `n_degs = 0`, the median was 0,
  the 75th percentile was 1, the 95th percentile was 18, and only the long tail
  reached hundreds to thousands of genes.
- The supplied parquet
  `training_de_all_cell_groups.parquet`. I queried the `151 TH Prkcd Grin2c
  Glut` rows for candidate metabolic analogs and inspected the FDR support and
  self-transcript rows for each analog.
- Distributed Agents same-experiment corpus release
  `perturbai-july-260713-sourceguard-1773-v1`. `target_context(Acat1)` returned
  no bottom-up claims, findings, or explicit references, so the internal corpus
  did not contain direct `Acat1` evidence. I used the corpus contexts for
  `Bckdhb`, `Dld`, `Pdha1`, `Hmgcr`, and `Mdh1` to interpret the represented
  BCAA/organic-acid and mitochondrial carbon-metabolism comparators.
- Distributed Agents run-local profile tools. I built
  `acat1_candidate_profiles.tsv` from focal-cell parquet rows for 24 selected
  metabolic/lipid/OXPHOS candidates, ran a signed log-fold-change comparison in
  `acat1_candidate_profile_compare.json`, inspected it in five chunks, and
  projected the principal organic-acid/TCA cohort to
  `acat1_primary_metabolic_cohort.json`.
- Literature on ACAT1/T2 deficiency and isoleucine catabolism: Fukao et al.
  2018, DOI 10.1038/s10038-018-0524-x, PMID 30393371; Abdelkreem et al. 2019,
  DOI 10.1002/humu.23831, PMID 31268215; Korman 2006, DOI
  10.1016/j.ymgme.2006.07.010, PMID 16950638; Paquay et al. 2017, DOI
  10.1007/s10545-017-0021-y, PMID 28255778; Grunert and Sass 2020, DOI
  10.1186/s13023-020-01357-0, PMID 32345314.

## Computations over the parquet

I first searched the focal training list for exact or nearby `Acat1` biochemical
analogs. Exact ketone-body/acetoacetyl-CoA comparators such as `Acat2`, `Bdh1`,
`Bdh2`, `Oxct1`, `Oxct2a`, `Oxct2b`, `Hmgcl`, `Hmgcs1`, `Hmgcs2`, `Acaa1a`,
`Acaa1b`, and `Acaa2` were absent from the training perturbations. The available
training evidence therefore came from adjacent mitochondrial organic-acid,
branched-chain amino-acid, pyruvate dehydrogenase, TCA, and OXPHOS genes.

For each candidate, I read the rows satisfying:

```python
group_name == "151 TH Prkcd Grin2c Glut"
gene_target in candidate_genes
```

and retained `names`, `gene_target`, `logfoldchanges`, `pvals_adj`, `scores`,
`n_pert_matched`, and `n_ctrl_matched`. That produced 414,216 focal-cell
gene-by-perturbation rows across 24 candidates. For each candidate I then
checked:

- the observed `n_degs` in the training-count CSV;
- whether the target transcript itself was FDR-significant;
- the minimum `pvals_adj` in the signature, to distinguish a true zero from a
  self-transcript-only count of one;
- signed log-fold-change similarity among all candidate profiles.

The key focal-cell results were:

| training perturbation | observed `n_degs` | target self row in 151 | relevance to `Acat1` |
|---|---:|---|---|
| `Bckdhb` | 0 | Bckdhb logFC -0.645, FDR 1 | BCKDH subunit upstream of the isoleucine/branched-chain catabolic neighborhood |
| `Bckdk` | 0 | Bckdk logFC -0.676, FDR 1 | BCKDH regulatory kinase; pathway counterexample |
| `Ivd` | 0 | Ivd logFC -0.163, FDR 1 | mitochondrial leucine organic-acid catabolism |
| `Auh` | 0 | Auh logFC -0.295, FDR 1 | mitochondrial leucine catabolism near HMG-CoA/acetoacetate chemistry |
| `Pcca` | 0 | Pcca logFC -0.256, FDR 1 | propionyl-CoA carboxylase for Val/Ile/Met/Thr odd-chain catabolism |
| `Etfa` | 0 | Etfa logFC -0.562, FDR 1 | electron-transfer flavoprotein, fatty-acid/amino-acid oxidation |
| `Dld` | 0 | Dld logFC -0.398, FDR 1 | E3 subunit shared by BCKDH, PDH, and OGDH complexes |
| `Dlst` | 0 | Dlst logFC -0.342, FDR 1 | OGDH E2 subunit |
| `Ogdh` | 0 | Ogdh logFC -0.385, FDR 0.564 | TCA alpha-ketoglutarate dehydrogenase E1 |
| `Aco2` | 0 | Aco2 logFC -0.103, FDR 1 | mitochondrial TCA enzyme |
| `Dlat` | 1 | Dlat logFC -0.674, FDR 2.8e-7 | PDH E2; one DEG was the target transcript itself |
| `Pdha1` | 1 | Pdha1 logFC -1.039, FDR 1.3e-6 | PDH E1 alpha; one DEG was the target transcript itself |
| `Idh3a` | 1 | Idh3a logFC -0.817, FDR 9.3e-11 | mitochondrial NAD-IDH subunit; self-transcript-only in 151 |
| `Mdh2` | 1 | Mdh2 logFC -0.840, FDR 7.4e-5 | mitochondrial malate dehydrogenase; self-transcript-only in 151 |
| `Sdha` | 1 | Sdha logFC -0.781, FDR 2.1e-12 | succinate dehydrogenase; self-transcript-only in 151 |
| `Mdh1` | 29 | Mdh1 logFC -1.059, FDR 1.6e-22 | a useful counterexample: the cytosolic malate-aspartate-shuttle arm can respond in 151 |
| `Hmgcr` | 0 | Hmgcr logFC -0.300, FDR 1 | sterol/mevalonate counterexample, not a direct ACAT1 analog |

The Distributed Agents profile comparison of the 24 candidate signatures found 13
candidates with no FDR-significant features, 10 with only 1-9 significant
features, and only `Mdh1` in the 10-49 bin. In the exact 15-node BCAA,
organic-acid, and TCA cohort, the top-tail overlap was small and no pair had a
nonzero overlap coefficient for an FDR-supported significant program. That is,
the relevant metabolic nodes had weakly correlated full logFC surfaces at the
rank level but no shared, recurrent, FDR-level downstream gene set in 151.

## Same-experiment analogs and corpus interpretation

`Acat1` itself had no entry in the Distributed Agents corpus, so the within-dataset
evidence is entirely by transfer.

The closest available analog group was the BCAA/organic-acid set
`Bckdhb`, `Bckdk`, `Ivd`, `Auh`, `Pcca`, `Etfa`, and `Dld`. Every member had
`n_degs = 0` in 151. Distributed Agents claims for `Bckdhb` and `Dld` explicitly state
that represented mitochondrial BCAA/leucine and organic-acid catabolic nodes
were transcriptionally buffered in the acute postnatal neuronal screen:
`Bckdhb:F001` found no downstream response across recovered neuronal groups;
`Bckdhb:F002` showed measured BCKDH-axis relatives `Bckdk` and `Dld` were also
flat; `Dld:F003` tied the DLD pathway to a broader sparse/null carbon-entry and
TCA surface. This is the best mechanistic lane for `Acat1`, because ACAT1/T2
cleaves 2-methylacetoacetyl-CoA in isoleucine degradation and also handles
acetoacetyl-CoA in ketone-body utilization.

The next comparison set, `Dlat`, `Pdha1`, `Dlst`, `Ogdh`, `Aco2`, `Idh3a`,
`Mdh2`, and `Sdha`, asked whether a mitochondrial matrix carbon enzyme tends to
make a generic mitochondrial or ISR-like nuclear state in this focal cell type.
It did not: `Dlst`, `Ogdh`, and `Aco2` were zero, while `Dlat`, `Pdha1`,
`Idh3a`, `Mdh2`, and `Sdha` were singletons dominated by self-transcript
detection. The corpus contexts for `Pdha1` and `Dld` reached the same conclusion
at a broader brain-wide level: represented PDC, DLD-linked, TCA, and adjacent
mitochondrial perturbations were mostly flat or sparse and did not form a
coherent postmitotic neuronal PDH/TCA module.

`Mdh1` is a counterexample rather than a predictor. It produced 29 DEGs in the
same 151 cell group, and the Distributed Agents corpus links it to a cytosolic
`Mdh1`/`Got1` malate-aspartate-shuttle response. That argues the cell type and
Wilcoxon pipeline can detect a metabolic response when an edited node crosses a
transcriptional threshold, but it also argues against pooling all metabolic
enzymes: mitochondrial `Mdh2`, `Got2`, and `Slc25a12` did not phenocopy the
cytosolic `Mdh1`/`Got1` state.

I considered `Hmgcr` only as a boundary. It had `n_degs = 0` in 151 and the
Distributed Agents corpus reports an almost flat sterol/mevalonate perturbation surface,
but it is not chemically close to `Acat1`. It mostly confirms that the run should
not be redirected toward the unrelated cholesterol-esterification ACAT1/`Soat1`
literature.

## Biological rationale for `Acat1`

ACAT1/T2 loss is a real mitochondrial metabolic defect: beta-ketothiolase
deficiency impairs both ketone-body utilization and isoleucine catabolism
(Fukao et al. 2018; Abdelkreem et al. 2019; Korman 2006). The human disease is
classically intermittent ketoacidosis, often during fasting or infection; several
series report that many patients are neurologically normal between crises or
after appropriate management, while a subset develops basal-ganglia or
extrapyramidal sequelae (Paquay et al. 2017; Grunert and Sass 2020). That
fits an enzyme whose most severe consequences depend on systemic ketogenic
stress and metabolite accumulation rather than a constitutive, cell-autonomous
nuclear RNA program in every neuron.

The Perturb-seq context further weakens the case for a broad response. The
experiment perturbed sparse postmitotic neurons on a normal in vivo background
from P16 to P37-P44 and used nuclear RNA from surviving NeuN-positive nuclei.
There was no fasting, ketogenic diet, infection, metabolomics readout, or
non-neuronal compartment in which liver/astrocyte ketone supply or systemic
organic acidemia could be established. Direct BCAA and organic-acid analogs that
should have exposed basal amino-acid-catabolism stress if it were easy to see in
this assay were all zero in 151.

The main reason to choose 1 rather than 0 would be target-transcript capture:
`Dlat`, `Pdha1`, `Idh3a`, `Mdh2`, and `Sdha` each reached one DEG because the
perturbed enzyme RNA itself was significantly reduced. I did not up-call
`Acat1` to 1, because the most pathway-matched BCAA/organic-acid genes
`Bckdhb`, `Bckdk`, `Ivd`, `Auh`, `Pcca`, `Etfa`, and `Dld` all had no
self-transcript FDR signal in the same focal cell group, even when their nominal
log-fold changes were negative. ACAT1 is more analogous to that organic-acid
catabolic group than to the abundant core PDH/TCA/OXPHOS genes. I therefore
predict no gene, including the target transcript, will pass FDR 0.05.

## Prediction

| target_name | predicted_n_degs | zero/nonzero decision |
|---|---:|---|
| `Acat1` | 0 | zero |

## Limits and extrapolations

- There was no `Acat1` signature in the parquet and no direct `Acat1` entry in
  the Distributed Agents corpus, so the prediction transfers from neighboring
  mitochondrial organic-acid and carbon-metabolism perturbations.
- The closest ketone-body genes, especially `Oxct1`, `Bdh1`, `Hmgcl`, and
  `Acat2`, were absent from the training perturbation set. `Bckdhb`, `Ivd`,
  `Auh`, and `Pcca` are mechanistic neighbors and stress counterexamples, not
  exact substitutes for mitochondrial acetoacetyl-CoA thiolase.
- A zero DEG prediction does not imply that ACAT1 protein, ketone flux,
  isoleucine metabolites, or edited-allele fractions would be unchanged. The
  assay measures steady-state nuclear RNA in surviving neurons, and the endpoint
  is heavily affected by expression, guide efficiency, cell counts, and
  Benjamini-Hochberg correction.
- The external disease literature involves biallelic germline human ACAT1
  deficiency and systemic metabolic crises. That is informative for pathway
  placement but imperfect for a sparse juvenile mouse CRISPR knockout under
  basal feeding conditions.
