# DEG-count prediction trace

## Question and endpoint

The task asks for a point prediction of `n_degs` for each requested perturbation
held out from the supplied Perturb-seq differential-expression inputs.  The
requested manifest contains one target, `Ffar1`, and the endpoint is the number
of measured genes in `151 TH Prkcd Grin2c Glut` whose Wilcoxon
Benjamini-Hochberg adjusted p-value is below 0.05.  I treated the supplied
training count table as direct observations for the non-held-out perturbations
in the focal cell group and the all-cell differential-expression Parquet as the
source of the underlying signature and matched-nucleus context.  `Ffar1` itself
is absent from both training inputs, so its endpoint is absent from the declared
inputs rather than directly observed.

I resolved the cell label literally as an Allen atlas thalamic glutamatergic
class: `151` is a class identifier, `TH` means thalamus, `Prkcd` and `Grin2c`
are marker genes, and `Glut` denotes glutamatergic neurons.  I interpreted
`logfoldchanges` as perturbed versus matched control.  I did not use target RNA
loss as a guide-efficiency filter, because this mosaic CRISPR/snRNA design does
not make observed target-mRNA reduction a quantitative editing-efficiency
measure.

## Sources

- Declared endpoint counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared per-gene DE Parquet:
  `training differential-expression dataset`.
- Requested target manifest:
  `single-target request for Ffar1`.
- Run-local dataset portrait, task bindings, compact coverage, measurement
  registry, and capability manifest under `codex_runtime/pipeline`.
- The internal same-experiment semantic layer was the
  `perturbai-july-260713-sourceguard-1773-v1` corpus.  BioKG and Findings
  queries had no `Ffar1` node or Finding, so I used it only for represented
  training analogs such as `Ppara`, `Ppard`, `Pparg`, `Gnao1`, and `Gnas`.
- External mechanism priors came from PubMed-indexed FFAR literature:
  Kimura et al. 2019, Physiol Rev, doi:10.1152/physrev.00041.2018;
  Khan and He 2015, Neuropharmacology, doi:10.1016/j.neuropharm.2015.05.013;
  Psichas et al. 2017, Diabetologia, doi:10.1007/s00125-017-4420-2;
  Dragano et al. 2023, Mol Metab, doi:10.1016/j.molmet.2023.101840,
  PMID:38036170.  I also used the Reactome `PPARA activates gene expression`
  pathway, stable identifier `R-HSA-1989781`, as a curated external definition
  of the PPARA fatty-acid transcriptional regulon.

## Computation over the declared inputs

I first counted the requested manifest rows and confirmed that only `Ffar1` was
requested.  The training endpoint table contains 1,674 non-held-out perturbations
in the focal cell group.  Its count distribution is highly zero-inflated:
1,205/1,674 perturbations have `n_degs = 0`, the median is 0, the 75th percentile
is 1, the 90th percentile is 2, and the 95th percentile is 18.  The large upper
tail is driven mostly by chromatin regulators, RNA-processing factors,
proteostasis factors, and core neuronal regulators, with values such as
`Uba5 = 2677`, `Tpr = 1768`, `Sin3a = 1433`, and `Rnpc3 = 868`.

I then scanned the focal class in the Parquet and grouped by `gene_target`:

```sql
SELECT gene_target,
       sum(pvals_adj < 0.05)::INTEGER AS n_sig,
       min(pvals_adj) AS min_padj,
       max(n_pert_matched) AS n_pert,
       max(n_ctrl_matched) AS n_ctrl
FROM read_parquet(...)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
GROUP BY gene_target;
```

The grouped Parquet counts reproduced the CSV exactly for all 1,674 focal
targets.  Every focal comparison used the same 23,679 matched control nuclei;
the relevant analog perturbations had 109-315 matched perturbed nuclei, so their
zeros are not explained by a uniquely tiny recovered sample.

Relevant focal-cell counts were:

| training perturbation | reason inspected | n_degs in `151 TH Prkcd Grin2c Glut` |
|---|---|---:|
| `Ppara` | lipid/fatty-acid nuclear receptor and PPAR/RXR regulon | 0 |
| `Ppard` | brain-expressed PPAR/RXR lipid receptor | 0 |
| `Pparg` | PPAR/RXR lipid receptor | 0 |
| `Ppargc1a` | lipid/mitochondrial transcriptional coactivator | 0 |
| `Acsl4` | neuronal acyl-CoA/fatty-acid metabolism node | 1 |
| `Gnas` | GPCR G alpha s to cAMP/CREB transducer | 0 |
| `Gnal` | GPCR G alpha olf to cAMP transducer | 0 |
| `Gnao1` | neuronal GPCR G alpha o transducer | 1 |
| `Gnb5` | GPCR beta subunit/regulator | 0 |
| `Plcb1` | phospholipase C downstream of Gq | 0 |
| `Itpr1` | IP3/Ca2+ release downstream of PLC | 0 |
| `Prkca` | protein kinase C downstream of DAG/Ca2+ | 0 |
| `Prkcg` | protein kinase C isoform | 1 |
| `Adcy1` | Ca2+/calmodulin-regulated cAMP production | 0 |
| `Adcy3` | cAMP production | 0 |
| `Adcy5` | cAMP production | 0 |
| `Calm1` | calmodulin | 14 |
| `Calm2` | calmodulin | 0 |
| `Calm3` | calmodulin | 1 |
| `Camk2a` | Ca2+/calmodulin kinase | 0 |
| `Camk2b` | Ca2+/calmodulin kinase | 1 |
| `Camk2g` | Ca2+/calmodulin kinase | 0 |
| `Cnr1` | abundant Gi/o-coupled neuronal GPCR | 1 |
| `Chrm2`, `Chrm3` | muscarinic GPCRs | 0, 0 |
| `Cckar`, `Cckbr` | CCK GPCRs | 0, 0 |
| `Grm1`, `Grm5`, `Grm7` | metabotropic glutamate GPCRs | 1, 0, 1 |
| `Htr2a`, `Htr2c` | Gq-coupled serotonin GPCRs | 0, 0 |

I also inspected the internal corpus for these analogs.  The PPAR/RXR reports
state that `Ppara`, `Ppard`, and `Pparg` were whole-surface or near
whole-surface transcriptional nulls in this P16-to-P37/44 neuronal screen.
`Ppara` had zero downstream FDR<0.10 genes in 22 measured groups and its
literature-obvious comparators `Ppard`, `Pparg`, `Ppargc1a`, `Rxra`, and `Rxrg`
were also flat across their measured surfaces.  `Ppard` had zero downstream
FDR<0.10 genes in 23/23 recovered groups.  `Pparg` had no FDR-significant
downstream response in any of 20 recovered juvenile neuronal groups, and
canonical lipid/adipogenic, oxidative-stress, UPR/ISR, autophagy, and
immediate-early sentinel genes were not FDR-significant.  The same-experiment
`Gnas` and `Gnao1` reports make a similar point for ligand-gated GPCR
transduction: basal postnatal loss of upstream G-protein components was
overwhelmingly transcriptionally buffered and did not expose broad cAMP,
CREB, immediate-early, activity, or stress modules, even though downstream
CREB-family rewiring can be detected in the same Wilcoxon universe.

## Target-specific prediction

### Ffar1

`Ffar1`, also called `Gpr40` or FFAR1, encodes a rhodopsin-family receptor for
medium- and long-chain fatty acids.  FFAR1 can mobilize intracellular calcium
through Gq/PLC signaling in pancreatic or enteroendocrine models, and fatty-acid
sensing through this receptor is well established outside the brain
(Kimura et al. 2019; Psichas et al. 2017).  The brain literature supports real
neuronal functions, including reports that hypothalamic FFAR1 signaling in
POMC or AgRP neurons can affect feeding and energy balance and that GPR40 has
been studied in neurogenesis and pain contexts (Khan and He 2015; Dragano et al.
2023, PMID:38036170).

The causal transfer model is:

`Ffar1` CRISPR loss -> reduced fatty-acid-evoked FFAR1 signaling -> possible
changes in Gq/PLC/Ca2+, MAPK, lipid-sensing, or neuropeptide-state pathways ->
any chronic transcriptional program present 3-4 weeks later in recovered
postnatal `151 TH Prkcd Grin2c Glut` nuclei -> the count of genes crossing
FDR 0.05.

The strong link in that chain is the receptor identity and proximal ligand
signaling.  The weak link is conversion of a basal `Ffar1` loss-of-function
perturbation into a broad constitutive RNA program in this thalamic neuronal
class.  FFAR1 is not an obligate complex member of the PPAR/RXR transcriptional
machinery; PPARs are downstream nuclear receptors for lipid-metabolic states,
not required same-outcome partners.  Nevertheless, their measured behavior is
the best in-dataset falsifier for a large basal lipid-response program: `Ppara`,
`Ppard`, `Pparg`, and `Ppargc1a` were all zero in the focal class, and the
curated PPAR/RXR reports show that canonical fatty-acid regulons were broadly
absent in the neuronal screen.  The proximal second-messenger side also argues
against a multi-gene FFAR1 response: `Gnas`, `Gnal`, `Plcb1`, `Itpr1`, `Prkca`,
`Adcy1`, `Adcy3`, `Adcy5`, and most Ca2+/calmodulin/CaMK genes were zero in
the focal class; represented GPCRs with endogenous neuronal expression were
almost all zero or singleton responders.

I therefore predicted no FDR-significant genes for `Ffar1` in the focal group.
The decision is driven mainly by within-dataset evidence: the endpoint table
shows that receptor and lipid-signaling perturbations in this assay usually
land at exactly zero, while the Parquet confirms that these comparators are
focal-class nulls rather than missing rows.  External FFAR literature was used
only to choose mechanistically sensible comparators and to check for an obvious
reason that `Ffar1` should be an exception.  The main exception would have been
a POMC/AgRP-like hypothalamic nutrient-sensing state, but `151 TH Prkcd Grin2c
Glut` is thalamic, the experiment did not impose a fatty-acid or fasting
challenge, and the perturbation was an acute sparse CRISPR loss at P16 rather
than cell-type-specific hypothalamic knockdown under obesity or starvation.

Final prediction: `Ffar1 = 0`.

## Limits

This is an extrapolation because no `Ffar1`, `Ffar2`, `Ffar3`, or `Ffar4`
perturbation was present in the training endpoint table or July same-experiment
corpus.  A zero prediction does not mean FFAR1 lacks neuronal biology; it means
that a stable transcriptome-wide response is unlikely to cross BH FDR 0.05 in
this basal recovered thalamic class.  The screen would be poorly powered for a
rare hypothalamic subpopulation, for glial or peripheral FFAR1 functions, for
acute ligand-evoked calcium fluxes, and for changes that require fasting,
obesity, inflammation, pain, or dopaminergic injury.  The GPCR and PPAR
comparators are mechanistic analogs and counterexamples rather than obligate
same-outcome partners, so they support a low/zero count only through the
absence of a broader chronic lipid- or receptor-signaling RNA program in the
same assay.

