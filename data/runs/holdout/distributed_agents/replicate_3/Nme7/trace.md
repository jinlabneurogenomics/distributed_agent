# Reasoning trace

## Question interpreted

The held-out target list for this run contains one perturbation, `Nme7`. I treated the requested endpoint as the exact training-count definition: in `151 TH Prkcd Grin2c Glut` thalamic glutamatergic neurons, count all measured mouse genes, including the perturbed target if present, whose Wilcoxon `pvals_adj` is below 0.05 after acute sparse AAV-CRISPR loss of function. `Nme7` itself is absent from both the per-gene DE parquet and the focal-cell training count CSV, so the prediction has to be transferred from other perturbations.

I resolved the main ambiguity in favor of the supplied postnatal neuronal assay rather than germline or developmental knockout phenotypes. `Nme7` has strong published ciliary phenotypes, including hydrocephalus and situs phenotypes, but the Perturb-seq experiment assayed NeuN+ postmitotic nuclei 3-4 weeks after P16 editing and did not include ependymal, choroid plexus, respiratory, nodal, or retinal endpoints.

## Sources used

- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed `n_degs` for 1,674 non-held-out perturbations in the focal cell group.
- `training_de_all_cell_groups.parquet`: focal-cell per-gene Wilcoxon statistics, queried for ciliary, Hedgehog, centrosomal, microtubule, and retinal/ciliopathy comparators.
- Distributed Agents same-experiment corpus `perturbai-july-260713-sourceguard-1773-v1`: no direct `Nme7` Claim/Finding was present, but ciliary Claims and Findings around `Ift88`, `Kif3b`, `Dync2i1`, `Arl3`, and `Cep290` summarized the same atlas' internal comparisons.
- PubMed literature for `NME7` biology:
  - Lai et al. 2011, DOI `10.1091/mbc.E10-07-0596`, PMID `21289087`.
  - Liu et al. 2014, DOI `10.1091/mbc.E13-06-0339`, PMID `24807905`.
  - Vogel et al. 2010, DOI `10.1177/0300985809353553`, PMID `20080492`.
  - Reish et al. 2016, DOI `10.1002/humu.22998`, PMID `27060491`.
  - Sedova et al. 2021, DOI `10.3390/ijms22083810`, PMID `33916973`.
  - Ji et al. 2025, DOI `10.26508/lsa.202402933`, PMID `39824631`.

## Dataset computations

I read the requested-target manifest and confirmed that `Nme7` is the sole held-out row. I then queried the training count CSV by symbol prefix and by hand-curated ciliary/Hedgehog comparator sets. To inspect expression-pattern evidence rather than just counts, I scanned only the focal cell group and selected training targets from the parquet with an Arrow predicate:

```python
expr = (ds.field("group_name") == "151 TH Prkcd Grin2c Glut") & pc.field("gene_target").isin(targets)
table = dataset.to_table(
    columns=["names", "gene_target", "logfoldchanges", "scores",
             "pvals_adj", "n_pert_matched", "n_ctrl_matched"],
    filter=expr,
)
```

For each selected training perturbation I recomputed `sum(pvals_adj < 0.05)` in the focal group, compared it with the count CSV, inspected the minimum adjusted p-value and top adjusted hits, and correlated the signed Wilcoxon-score vectors among the selected perturbations to check whether FDR-flat ciliary genes nevertheless shared a below-threshold transcriptional state.

The focal class is responsive in the experiment overall: 469 of 1,674 training perturbations have at least one DEG and strong positive controls such as `Uba5`, `Tpr`, `Sin3a`, `Psmb4`, and `Psmc1` produce hundreds to thousands of focal DEGs. The relevant ciliary neighborhood was different. Core ciliary transport and transition-zone genes had zero focal DEGs with no coherent top genes:

| comparator | rationale | observed focal `n_degs` | focal expression evidence |
|---|---|---:|---|
| `Alms1` | basal-body/BBS-related ciliary target | 0 | min q = 1.0; 110 perturbed vs 23,679 control nuclei |
| `Bbs5` | BBSome comparator | 0 | min q = 0.220 |
| `Cep290` | ciliary transition-zone gate | 0 | min q = 0.650 |
| `Cfap69` | cilium/axonemal comparator represented in corpus Claims | 0 | min q = 1.0 |
| `Dync2h1` | dynein-2 retrograde IFT motor | 0 | min q = 0.348 |
| `Dync2i1` | dynein-2 intermediate chain, close to `Dync2h1` | 0 | min q = 1.0 |
| `Ift43` | IFT-A | 0 | min q = 0.847 |
| `Ift81` | IFT-B | 0 | min q = 0.391 |
| `Ift88` | IFT-B and classic ciliary/Hedgehog component | 0 | min q = 1.0 |
| `Kif3b` | kinesin-2 anterograde IFT motor | 0 | min q = 1.0 |
| `Lztfl1` | BBSome trafficking regulator | 0 | min q = 0.196 |
| `Ttc21b` | IFT-A retrograde trafficking | 0 | min q = 0.459 |
| `Ttc8` | BBSome | 1 | the only DEG was the target transcript itself, `Ttc8`, q = 3.07e-05 |

The downstream cilium-to-Hedgehog arm was also silent:

| comparator | observed focal `n_degs` | focal expression evidence |
|---|---:|---|
| `Cdon` | 0 | min q = 1.0 |
| `Gli1` | 0 | min q = 1.0 |
| `Gli2` | 0 | min q = 1.0 |
| `Gpr161` | 0 | min q = 1.0 |
| `Ptch1` | 0 | min q = 1.0 |
| `Ptch2` | 0 | min q = 1.0 |
| `Smo` | 0 | min q = 1.0 |

Retinal/ciliopathy and ARL3-cycle comparators were likewise flat in the same focal group:

| comparator | observed focal `n_degs` | focal expression evidence |
|---|---:|---|
| `Arl2bp` | 0 | min q = 1.0 |
| `Arl3` | 1 | the only DEG was `Arl3` itself, q = 0.018 |
| `Armc9` | 0 | min q = 1.0 |
| `B9d1` | 0 | min q = 1.0 in this focal class |
| `Cspp1` | 0 | min q = 1.0 |
| `Iqcb1` | 0 | min q = 1.0 |
| `Rpgr` | 0 | min q = 0.648 |
| `Rpgrip1l` | 0 | min q = 0.184 |
| `Spata7` | 0 | min q = 0.116 |

The score-vector check supported these as true near-nulls rather than the same weak module failing a hard q-value threshold. The closest ciliary-neighborhood correlations in the focal rows were tiny: `Ift43` to `Ift81` was Pearson r = 0.123, `Ift88` to `Ptch2` was r = 0.127, most best neighbors for `Alms1`, `Cep290`, `Dync2i1`, `Kif3b`, `Ttc21b`, and `Arl3` were around |r| = 0.03-0.08, and no pair shared a focal downstream DEG set. Microtubule cytoskeleton perturbations provided a useful counterexample: the assay can see a focused microtubule RNA response when it exists (`Tuba1a`, 7 DEGs led by `Tuba1a`, `Tubb3`, `Tubb2a`, `Tuba4a`, `Tubb4a`; q as low as 2.8e-20), but centrosome/cilium-adjacent genes such as `Cep120`, `Kif2a`, `Nin`, `Nek1`, `Nek9`, `Rfx3`, and `Ulk4` had 0 focal DEGs.

The Distributed Agents corpus agreed with this direct parquet read. The high-confidence ciliary Claim `claim:78305cab7c1c7b98458d` states that acute perturbation of represented ciliary trafficking and ciliary signaling genes in postnatal NeuN+ neurons is largely buffered at the basal nuclear RNA level rather than forming a shared ciliary transcriptional module, with `Alms1`, `Cep290`, `Cfap69`, `Dync2i1`, `Ift43`, `Ift88`, `Kif3b`, `Ttc21b`, and `Ttc8` as target genes. `Ift88:F003`, `Kif3b:F002`, `Dync2i1:F002`, and `Cep290:F003` specifically contrasted flat IFT, dynein-2, BBSome, transition-zone, PTCH/SMO/GLI, and ciliary GPCR surfaces with large non-ciliary responses such as proteasome perturbations. The corpus also reported that the biochemical `Arl3`/`Arl2bp` ciliary relationship and retinal/ciliary-gate disease relationships did not translate to shared postnatal brain-neuron DE signatures in this atlas (`Arl3:F003`; Claims `claim:1852264399a3b66af6a8` and `claim:23e9053d61771b0c8274`).

## Target-specific rationale for `Nme7`

`Nme7` encodes a nucleoside diphosphate kinase family protein that sits at the centrosome/basal body/cilium interface rather than an RNA-binding, chromatin, proteasome, or transcription-factor node. In cultured ciliary assays, `NME7` perturbation affects ciliary cargo transport and Hedgehog readouts: Lai et al. found `Arl3`, `Nme7`, and `Ssna1` siRNA hits with ciliary transport defects without a gross cilium-length phenotype, Liu et al. identified NME7 as a gamma-tubulin ring complex component that facilitates centrosome-based microtubule nucleation, and Ji et al. reported that NME7 localizes at centrosomes/basal bodies and supports primary cilium assembly, ciliary microtubule stability, and SMO-dependent Hedgehog signaling. Whole-animal null data reinforce that this is biologically real ciliary machinery: Nme7 knockout mice show situs inversus and hydrocephalus, human NME7 mutation was linked to situs inversus totalis, and CRISPR Nme7 knockout rats had semilethality, hydrocephalus, situs inversus, postnatal growth retardation, and sterility.

Those mechanisms made the core comparators the represented cilium genes above, especially IFT motors/components (`Ift43`, `Ift81`, `Ift88`, `Kif3b`, `Dync2h1`, `Dync2i1`), transition-zone/ciliopathy genes (`Cep290`, `Rpgrip1l`, `B9d1`, `Armc9`, `Cspp1`), the BBSome (`Bbs5`, `Ttc8`, `Lztfl1`), the ARL3 cargo-localization axis (`Arl3`, `Arl2bp`), and the downstream cilium-Hedgehog circuit (`Smo`, `Ptch1`, `Ptch2`, `Gli1`, `Gli2`, `Gpr161`, `Cdon`). They are better analogs than NME-family paralogs, because no `Nme1`-like paralog was represented in the focal training count table and most other NME proteins do not share `Nme7`'s established basal-body/ciliary role.

The within-dataset analogs overwhelmingly point to a zero or, at most, a target-transcript-only singleton. Out of the closest represented ciliary perturbations in the focal cell group, nearly all had zero DEGs. The two singletons, `Arl3` and `Ttc8`, were not downstream ciliary modules; they were self-transcript decreases. Given that self-transcript decreases are inconsistent in this CRISPR/snRNA modality and `Nme7` itself had no direct training measurement, I did not add a self-hit. The public ciliary phenotypes are strongest in embryonic node, ependymal/multiciliated, respiratory, retinal, reproductive, and cultured proliferative cell contexts, all displaced from recovered P37-P44 NeuN+ thalamic glutamatergic nuclei. The best point prediction for the number of FDR<0.05 focal DEGs is therefore `0`.

## Limits

This is an extrapolation because the exact `Nme7` CRISPR rows were held out and the corpus had no `Nme7`-specific Finding. There were also no direct same-complex gamma-tubulin ring complex subunits such as `Tubg1`, `Tubgcp2`, or `Tubgcp3` in my focal comparator set, and no NME paralog with the same ciliary role in the training count table. The flat ciliary training perturbations establish that the postnatal NeuN+ nuclear RNA readout is usually insensitive to basal ciliary transport loss, but they do not prove that Nme7 editing leaves primary cilia, SMO trafficking, or neuronal physiology normal. Finally, a low-count self-transcript-only hit is possible whenever the target mRNA is expressed and falls enough for the Wilcoxon test; I treated that as less likely than zero because the closest downstream biology was uniformly FDR-flat.
