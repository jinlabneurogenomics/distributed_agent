# Rhobtb2 DEG-count prediction

## Question and endpoint

The task is to predict, for each held-out perturbation, the integer `n_degs` that would have been observed in `151 TH Prkcd Grin2c Glut` cells if the perturbation had not been withheld from the PerturbAI differential-expression inputs. `n_degs` is the count of measured mouse genes with Wilcoxon Benjamini-Hochberg `pvals_adj < 0.05` in the focal thalamic glutamatergic class.

There is only one requested target:

| target_name | predicted_n_degs |
|---|---:|
| Rhobtb2 | 0 |

I treated `151 TH Prkcd Grin2c Glut` as a thalamic glutamatergic neuronal class, not as a tyrosine-hydroxylase-positive dopamine class. The supplied Parquet and training-count CSV are direct observations for non-held-out perturbations and contain no `Rhobtb2` endpoint or `Rhobtb2` expression signature. The held-out endpoint is therefore absent from the declared inputs and must be predicted by transfer from visible perturbations plus external gene-function evidence.

## Sources and computations

### Declared run metadata

I read:

- `task.md`
- `codex_runtime/pipeline/dataset_context.md`
- `codex_runtime/pipeline/task_bindings.json`
- `codex_runtime/pipeline/coverage.json`
- `codex_runtime/pipeline/capabilities.json`
- `codex_runtime/pipeline/measurement_registry.json`

The capability manifest made the ranking workbench and `synthesis.ordering_validate` unavailable because this is a scalar count-prediction task with no ranked or partially ranked gene supervision, so I did not invoke them. I also did not invoke `corpus.predictive_graph_review`: it was unavailable for the same reason and is intended for ranked predictions, not one-gene DEG-count prediction. The same-experiment corpus was used only for compact interpretations of visible training perturbations; it is not independent replication of the Parquet.

### Focal DEG counts

I read `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` to calibrate the scalar endpoint in the focal cell class. The training endpoint is heavily zero-inflated:

- 1,674 training perturbations.
- Median `n_degs = 0`; mean `14.1`.
- 1,205/1,674 perturbations have `n_degs = 0`.
- The 75th, 90th, 95th, and 99th percentiles are 1, 2, 18, and about 436 DEGs.

This means the default expectation for a target without a close broad-responder analog is no FDR-significant focal response.

### Focused Parquet query

I queried the declared Parquet with DuckDB only for focal-cell rows for visible genes in the `Rhobtb2` functional neighborhood: Rho/Rac/Cdc42-axis perturbations, Ral/Rap regulators, BTB/KCTD/KLHL adaptors, and ZBTB-family counterexamples. For each target I exported all focal rows satisfying any of:

```sql
pvals_adj < 0.05
OR names IN (
  'Rhobtb2','Cdc42','Rac1','Rala','Btbd9','Kctd1','Kctd16','Kctd8',
  'Klhl20','Klhl7','Resp18','Cluap1','Pxdn','Endou','Clstn2','Man2a2'
)
OR row_number() over the target by adjusted p-value <= 5
```

The focal observed counts among the biologically relevant visible perturbations were:

| comparator | focal n_degs | focal expression evidence |
|---|---:|---|
| `Btbd9` | 0 | No gene reached `pvals_adj < 0.05`; no shared focal BTB/KCTD/KLHL module. |
| `Kctd1` | 2 | Only `Resp18` up and `Cluap1` down reached FDR 0.05. |
| `Kctd16` | 0 | No focal FDR 0.05 genes. |
| `Kctd8` | 0 | No focal FDR 0.05 genes. |
| `Klhl20` | 0 | No focal FDR 0.05 genes. |
| `Klhl7` | 0 | No focal FDR 0.05 genes. |
| `Cdc42` | 1 | Only the `Cdc42` target transcript reached FDR 0.05. |
| `Rac1` | 0 | No focal FDR 0.05 genes. |
| `Rala` | 0 | No focal FDR 0.05 genes. |
| `Arhgef9` | 1 | Only the `Arhgef9` target transcript reached FDR 0.05. |
| `Arhgap18` | 0 | No focal FDR 0.05 genes. |
| `Arhgap32` | 0 | No focal FDR 0.05 genes. |
| `Rapgef2` | 0 | No focal FDR 0.05 genes. |
| `Rapgef4` | 0 | No focal FDR 0.05 genes. |

I treated `Rab7` and `Zbtb7a` as counterexamples, not analogs. They have large focal responses, 501 and 841 DEGs respectively, but they measure different biology: `Rab7` is a core late endosome/autophagy-lysosome GTPase, while `Zbtb7a` is a zinc-finger BTB transcription factor with a broad regulatory footprint. Their large count shows that the focal class has power for strong endolysosomal or TF perturbations, but neither transfers to `Rhobtb2` by obligate complex membership or directional dependence.

### Same-experiment corpus

I used the July 260713 sourceguard 1773 v1 PerturbAI corpus through:

- `corpus.calibration`, to verify that Findings are atomic same-experiment interpretations and relation counts are not endpoint scores.
- `corpus.findings`, for compact `Btbd9`, `Kctd1`, `Cdc42`, `Rac1`, `Rala`, and `Zbtb18` Findings.
- `corpus.direct_evidence`, for unranked summary-first comparison records around `Btbd9`, `Kctd1`, `Cdc42`, `Rac1`, and `Rala`.
- `corpus.report_evidence`, to resolve material evidence and reference records for `Btbd9:F003`, `Cdc42:F003`, `Rac1:F001`, and `Rala:F001`.

Important same-experiment interpretations were:

- `Btbd9` produced no FDR 0.10 downstream DE genes in any recovered neuronal class, and represented BTB/Kelch relatives `Kbtbd7`, `Klhl7`, and `Klhl20` had either null or very small response surfaces rather than a shared proteostasis, ISR, UPR, or autophagy signature. Candidate CUL3-BTBD9 substrate genes and stress markers were also absent from the `Btbd9` response. This is directly relevant because RHOBTB2 and BTBD9 are both substrate-adaptor-like BTB proteins, but it argues that loss of one such adaptor is usually not amplified into broad nuclear RNA remodeling in this assay.
- `Kctd1` was a tiny responder: the corpus described only sparse one- or two-gene responses, and the represented KCTD-family perturbations `Kctd8` and `Kctd16` did not phenocopy it. This supports a zero-to-tiny rather than broad expectation for another non-core BTB/KCTD-like adaptor.
- `Cdc42` generated no robust downstream program across recovered neuronal classes despite being a well-established actin/spine regulator; represented `Rac1`, `Pak1`, `Pak2`, `Pak3`, `Limk1`, `Cfl2`, `Cyfip1`, `Cyfip2`, `Tiam1`, `Dock3`, `Fgd4`, `Arhgap18`, `Arhgap32`, and `Arhgef9` did not form a shared transcriptomic module. This is relevant because `Rhobtb2` is an atypical Rho GTPase, but most of the nearby small-GTPase cytoskeletal circuitry is post-translational and weak at the snRNA-seq DEG-count endpoint.
- `Rac1` and `Rala` were focal nulls. `Rala` was downstream-null at FDR 0.10 in every recovered neuronal class, even though RalA is involved in AMPAR trafficking, polarity, and exocyst biology; this is a counterweight against assuming that a neuronal GTPase disease association implies a broad steady-state RNA response.

### External biological knowledge

External evidence was used to decide which visible perturbations are mechanistically meaningful:

- Straub et al. 2017, DOI `10.1016/j.ajhg.2017.11.008`, established de novo BTB-domain `RHOBTB2` missense variants as a cause of developmental and epileptic encephalopathy, found increased abundance of mutant RHOBTB2 in HEK293 transfection consistent with impaired proteasomal degradation, and showed that altered Drosophila RhoBTB levels affect seizure susceptibility, locomotion, and dendritic arborization.
- Langhammer et al. 2023, DOI `10.1016/j.gim.2023.100885`, expanded `RHOBTB2` genotype-phenotype correlations: BTB-domain missense variants impair proteasomal degradation and associate with severe DEE, GTPase-domain variants are more variable, and biallelic truncating or splice variants can cause neurodevelopmental phenotypes. This supports biological relevance of loss, but also shows that dominant BTB missense disease is not a simple acute heterozygous loss-of-function model.
- Langhammer et al. 2025, DOI `10.1093/hmg/ddae183`, found ion-channel enrichment in fly-head RNA-seq after RhoBTB overexpression and a functional interaction with `paralytic`; in human iPSC-derived mature neurons, altered excitability was clear for BTB-domain missense variants but not for homozygous frameshift loss or GTPase-domain missense variants. This pushes the requested CRISPR loss-of-function toward a weaker transcriptional expectation than RHOBTB2 gain/stabilization.
- Manjarrez et al. 2014, DOI `10.1371/journal.pone.0090054`, and Choi et al. 2016, DOI `10.1038/onc.2016.441`, support the molecular framing of RHOBTB2/DBC2 as an atypical Rho-family BTB protein that can assemble a CUL3 E3 ligase complex and act as a substrate adaptor. These studies are cancer/cell-line contexts, so they support domain function rather than predicting thalamic neuronal DEG burden.
- Gao et al. 2022, PMID `35449961`, identified candidate BTBD9 ubiquitination substrates in SH-SY5Y cells. I used that only through the internal `Btbd9` comparison to ask whether a related BTB adaptor perturbation induces substrate/stress marker RNAs in the screen; it did not.
- Govek et al. 2005, DOI `10.1101/gad.1256405`, Reactome R-HSA-442586, Han et al. 2009, DOI `10.1371/journal.pbio.1000187`, Lalli 2009, DOI `10.1242/jcs.044339`, and Das et al. 2014, DOI `10.1242/jcs.145037`, establish the Rho/Rac/Cdc42 and Ral/exocyst branches as real neuronal cytoskeletal and trafficking circuits. The screen shows that those circuits generally do not manifest as broad P16-to-P37/P44 focal nuclear RNA programs.

## Rhobtb2-specific reasoning

`Rhobtb2` has two plausible routes to a transcriptional response: an atypical Rho-GTPase route and a BTB/CUL3-adaptor route.

For the Rho-GTPase route, the causal chain is:

`Rhobtb2` CRISPR loss -> altered atypical Rho-family protein or CUL3-adaptor function -> possible effects on local cytoskeletal, trafficking, ubiquitination, or excitability processes -> survivor-conditioned thalamic neurons 3 to 4 weeks later -> Wilcoxon nuclear RNA endpoint.

The visible Rho/Rac/Cdc42/Ral comparators break mainly between propagation and nuclear RNA measurement. `Cdc42`, `Rac1`, and `Rala` are closer to canonical neuronal small-GTPase signaling than `Rhobtb2`, but `Cdc42` had only a self-transcript hit in the focal class, while `Rac1` and `Rala` had zero focal FDR 0.05 DEGs. Rho/Rac/Cdc42-axis regulators and effectors in the count CSV were also focal-null or singleton targets: `Pak1` 1, `Pak2` 0, `Pak3` 0, `Limk1` 0, `Cyfip1` 0, `Cyfip2` 1, `Tiam1` 0, `Dock3` 0, `Fgd4` 0, `Arhgap18` 0, `Arhgap32` 0, `Arhgef9` 1, `Rapgef2` 0, and `Rapgef4` 0. The analogous intervention is expected to have the same weak-or-null direction at the requested endpoint because local GTPase state, actin remodeling, and receptor trafficking are not broad steady-state mRNA programs in this postmitotic CRISPR setting.

For the BTB/CUL3 route, the causal chain is:

`Rhobtb2` CRISPR loss -> loss of a specific CUL3-adaptor-like substrate-recognition function -> altered abundance of a small set of protein substrates -> possible compensatory stress or pathway response -> survivor nuclear RNA.

The best visible analogs again favor zero. `Btbd9` is the closest measured BTB-adaptor-like comparison and had `n_degs = 0` in the focal class and no downstream FDR 0.10 response in any recovered neuronal class. `Kctd1` had only two focal genes, while `Kctd8`, `Kctd16`, `Klhl7`, and `Klhl20` had zero focal DEGs. The causal link is same-direction only at the broad domain level, not at an obligate substrate or complex level, because RHOBTB2-specific partners and direct scaffolds such as `Cul3` and `Rbx1` were not perturbation targets in the training count CSV. This makes the BTB evidence a weak but negative proxy: represented substrate adaptors were generally not amplified into a detectable stress, ubiquitin, proteasome, autophagy, or UPR transcriptome.

The external RHOBTB2 literature prevents calling the gene biologically inert: patient BTB missense variants and fly RhoBTB overexpression are neuroactive, and complete human loss can be pathogenic. But most severe dominant disease is associated with missense variants that stabilize or otherwise dysregulate RHOBTB2 protein, not with the exact P16 acute mosaic loss tested here. The 2025 iPSC result, in which BTB-domain missense variants but not homozygous frameshift loss altered mature-neuron excitability, is a particularly important direction-specific prior against a broad loss-of-function RNA response.

I therefore predict that `Rhobtb2` will behave like the focal-null `Btbd9`/`Kctd8`/`Kctd16`/`Klhl` adaptors and the focal-null `Rac1`/`Rala` small-GTPase perturbations, not like `Rab7` or `Zbtb7a`. The point estimate is zero FDR 0.05 genes.

## Limits and uncertainty

The prediction is an extrapolation because no direct `Rhobtb2`, `Rhobtb1`, `Rhobtb3`, `Cul3`, `Rbx1`, or `Kctd13` perturbation was visible in the focal training endpoint. The training analogs cover broad BTB-domain and Rho-family logic, but none is an obligate RHOBTB2 complex member or a known same-substrate adaptor. The endpoint is a sparse, survivor-conditioned nuclear RNA count; it can miss dendritic arborization, channel gating, trafficking, ubiquitination, seizure liability, protein abundance, and early selection. Conversely, a single self-transcript hit could make the observed count 1 even when there is no downstream response, as happened for `Cdc42` and `Arhgef9`; I did not try to infer `Rhobtb2` editing efficiency from its mRNA because the dataset portrait warns that self-RNA loss is not a reliable engagement measure.
