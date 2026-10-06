# DCAF17 DEG-count prediction

## Question and resolved ambiguities

The requested held-out target list contained one gene, `Dcaf17`. I interpreted the task as a point prediction of the number of assayed genes that would have `pvals_adj < 0.05` for acute AAV-CRISPR loss of `Dcaf17` in `151 TH Prkcd Grin2c Glut` neurons, under the same Wilcoxon/BH procedure used for the supplied focal training table.

Two ambiguities were resolved explicitly:

- A prediction of `0` means no measured downstream gene is expected to cross FDR 0.05 in this specific sparse, postnatal neuronal assay. It is not a claim that DCAF17 is biologically inert, dispensable in germline loss, or poorly edited.
- Self-transcript fold change was not used as a pass/fail editing score. In this dataset several active perturbations have weak target-RNA changes in one cell group, so I based the call on downstream FDR counts, mechanistic analogs, and the external role of DCAF17.

## Sources used

- Input DE matrix: `[local file: training_de_all_cell_groups.parquet]`.
- Focal training endpoint: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Requested-target manifest: `[local file: 051_Dcaf17.csv]`.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`, queried for `Dcaf17`, `Dcaf8`, `Ddb2`, and `Wdr26`.
- PubMed literature searches for `C2orf37`, `DCAF17`, and Woodhouse-Sakati syndrome.

Key literature and external facts:

- `DCAF17` was originally identified as `C2orf37`, a nucleolar protein whose loss-of-function mutations cause Woodhouse-Sakati syndrome; the index study emphasized that its molecular function was still unknown (Alazami et al., 2008, PMID: 19026396, DOI: 10.1016/j.ajhg.2008.10.018).
- Human Woodhouse-Sakati cases are chronic, recessive, multisystem developmental/neuroendocrine disease rather than an acute cell-autonomous neuronal RNA phenotype. Reviews and cohorts report alopecia, hypogonadism, diabetes, hearing loss, cognitive involvement, extrapyramidal signs, basal-ganglia iron, and white-matter lesions with high phenotypic variability (Abusrair et al., 2018, PMID: 30409855, DOI: 10.3174/ajnr.A5879; Kohil et al., 2023, PMID: 36721231, DOI: 10.1186/s13023-023-02614-8; Ali et al., 2021, PMID: 34590781, DOI: 10.1002/ajmg.a.62501).
- Published WSS variant work describes DCAF17 as a nucleolar DDB1/CUL4-associated substrate receptor and modeled pathogenic truncation as removing residues important for DDB1 interaction (Ali et al., 2016, PMID: 26612766, DOI: 10.1111/cge.12700). That makes CRL4/DCAF-family perturbations reasonable analogs, but not enough to assume that every DCAF receptor has the same neuronal transcriptome.

## Computations over the Perturb-seq inputs

I first validated that the manifest was exactly one held-out row:

```text
target_name
Dcaf17
```

I then loaded only `group_name == "151 TH Prkcd Grin2c Glut"` from the 616,253,184-row parquet with PyArrow dataset filtering. The focal slice contained 28,891,566 rows: 1,674 training targets times 17,259 assayed genes. I recomputed the endpoint as:

```python
focal_count = (
    focal.groupby("gene_target")["pvals_adj"]
    .apply(lambda x: int((x < 0.05).sum()))
)
```

This matched the supplied focal count CSV. The training distribution was highly zero-inflated: 469/1,674 non-held-out targets had a positive focal DEG count, the median was 0, the 75th percentile was 1, and only the top 5% exceeded 18 DEGs.

For the DCAF17 decision I also computed exact focal counts and FDR genes for same-family, ubiquitin-system, WD-repeat, DNA-repair, and chromatin counterexamples, and I used the Distributed Agents runtime profile comparison on `logfoldchanges` with `pvals_adj < 0.05` to inspect whether `Dcaf8`, `Ddb2`, `Wdr26`, `Wdr48`, or `Fbxo11` shared a robust adjusted-gene module. The comparison returned three no-FDR profiles (`Dcaf8`, `Ddb2`, `Wdr48`), one single-DEG profile (`Fbxo11`), and one 13-DEG profile (`Wdr26`). Because the largest raw log-fold-change ranks in these small perturbation groups often had `pvals_adj = 1`, I treated all-gene rank overlap as a weak negative-control diagnostic and relied most heavily on FDR-level genes.

## Target-specific reasoning

### `Dcaf17`

There was no DCAF17 entry in the same-experiment Distributed Agents corpus: `target_context("Dcaf17")` returned no claims, findings, or explicit references. Thus no prior same-experiment finding directly measured or summarized DCAF17. The estimate had to be transferred from raw focal signatures and from genes with related molecular roles.

The closest represented analogs were CRL4/DDB1-associated or DCAF-like targets:

| training target | focal `n_degs` | matched perturbed nuclei | expression-pattern evidence and interpretation |
| --- | ---: | ---: | --- |
| `Dcaf8` | 0 | 165 | The only measured `Dcaf*` perturbation in the focal count table. It had no focal FDR genes. Distributed Agents `Dcaf8:F001` reported no downstream genes at FDR 0.10 in any of 22 recovered neuronal groups, and `Dcaf8:F004` found that directly measured CRL4/chromatin comparators did not phenocopy `Dcaf8`: `Ddb2` and `Dnmt3a` were flat while `Setdb1` had a distinct narrow response. |
| `Ddb2` | 0 | 215 | A DDB1-CUL4 substrate receptor in the same broad CRL4 receptor class, but wired to UV-damage/global-genome NER rather than to the unknown DCAF17 nucleolar function. It had no focal FDR genes. Distributed Agents `Ddb2:F001` reported a basal pan-neuronal null across all measured groups, arguing that DDB1-CUL4 receptor loss alone did not create tonic p53, stress, or DNA-repair transcription in these postmitotic nuclei. |
| `Dnmt3a` | 0 | 209 | A chromatin comparator used by the corpus to bound DCAF8-related surfaces; it had no focal FDR genes. This is a counterexample against assigning DCAF17 a broad nuclear/chromatin response only because it is nuclear. |
| `Setdb1` | 22 | 113 | An active nuclear counterexample. It induced a narrow protocadherin/Atf7ip/Tasor-biased state in this focal group, with `Tasor`, `Ccdc84`, `Pmvk`, `Atf7ip`, `Pcdhga8`, and related genes crossing FDR 0.05. This proves the focal group can detect a small chromatin/nuclear response, but the corpus explicitly separated that response from `Dcaf8`, `Ddb2`, and `Dnmt3a`, so it is not a good direct predictor for DCAF17. |

Broader ubiquitin and WD-repeat comparators were mostly also silent:

| training target | focal `n_degs` | matched perturbed nuclei | expression-pattern evidence and interpretation |
| --- | ---: | ---: | --- |
| `Wdr26` | 13 | 112 | The strongest WD-repeat/ubiquitin-ligase-adaptor-like comparator in this focal group. Its significant genes included down-regulated `Grin2b`, `Cyc1`, `Hnrnpu`, `Peg3`, `Kcna2`, `Abca7`, `Gabra4`, and `R3hdm2` plus up-regulated `Stk25`, `Calb1`, `Pde1b`, and `Smtn`. Distributed Agents showed that `Wdr26` is a CTLH-adaptor state with RNA-processing, proteostasis, synaptic, metabolic, and Tsc2/mTOR-proximal structure. That is informative as a positive counterexample but mechanistically distant from DCAF17. |
| `Wdr48` | 0 | 129 | A WD-repeat UAF1/USP1 cofactor linked to Fanconi/homologous-recombination biology, but no focal FDR genes. Distributed Agents `Wdr48:F002` noted that WDR48's canonical replicative genome-maintenance branch did not appear as a Fanconi, p53, or DNA-damage DE program in postmitotic neurons. |
| `Wdr37` | 0 | 221 | WD-repeat comparator with no focal response. |
| `Fbxo11` | 1 | 57 | F-box substrate adaptor with one focal FDR gene, `Ppib` down. Distributed Agents treated the related restricted signature as subthreshold and not a reproducible module. |
| `Fbxo38` | 0 | 194 | E3-ligase substrate-adaptor comparator with no focal response. |
| `Ube3a` | 0 | 84 | Neuronally important E3 ligase, but no focal FDR genes after acute sparse perturbation. |
| `Ube2e2` | 0 | 124 | Ubiquitin-conjugating enzyme comparator with no focal response. |
| `Trim2` | 2 | 236 | E3 ligase associated with axonopathy; only two focal DEGs, and Distributed Agents `Trim2:F004` found that E3-ligase and neuropathy comparators, including `Dcaf8` and `Ube3a`, did not phenocopy the Trim2 thalamic signature. |

Large ubiquitin/proteostasis responses did exist, but were poorer mechanistic analogs. `Psmb4` produced 742 focal DEGs and `Psmc1` produced 430, with broad synaptic and proteasome-associated shifts; `Tsc2` produced 86. These show that the assay has power to detect proteostasis and mTOR-adjacent remodeling in `151 TH Prkcd Grin2c Glut`, and they prevent a blanket "all ubiquitin genes are silent" rule. DCAF17 is not a core proteasome subunit and has no literature-supported reason to create the WDR26/TSC2 module or a proteasome-subunit failure state after 3-4 weeks of mosaic postnatal loss.

My zero/nonzero decision for `Dcaf17` was therefore:

- Within-dataset evidence strongly favored a null or near-null response. The closest focal DCAF/CRL4 measurements, `Dcaf8` and `Ddb2`, were both zero; related WD-repeat and E3 adaptors clustered at 0-1 DEGs except for the distinct `Wdr26` CTLH biology.
- External biology did not supply a reason to override that null. DCAF17 is a nucleolar DDB1/CUL4-associated factor with an incompletely defined function; WSS phenotypes are chronic, recessive, multisystem, and include endocrine, myelin/white-matter, basal-ganglia iron, and extrapyramidal features that are poorly represented by acute sparse CRISPR in NeuN-positive juvenile mouse nuclei.
- The focal cell group has many strong responses to RNA-processing, proteasome, and core chromatin genes, so a DCAF17 response in the hundreds would require extrapolating far beyond both its DCAF analogs and its known biology.

I rounded the expectation down to exactly zero FDR genes rather than a tiny positive number. That is calibrated to the focal training set, where the median perturbation is zero and mechanistic neighbors with no coherent FDR module usually land at 0 rather than 1-5.

## Limits and extrapolation

- `Dcaf17` itself was held out from both the DE parquet and the focal count table, and the Distributed Agents corpus had no DCAF17-centered same-experiment finding. The prediction is transfer, not direct observation.
- The nearest CRL4 core genes, `Ddb1`, `Cul4a`, `Cul4b`, `Rbx1`, and most DCAF paralogs were not available as focal training perturbations. `Dcaf8` and `Ddb2` are appropriate family-level anchors but not same-substrate or same-complex replacements for DCAF17.
- Human WSS is germline and chronic; it may involve endocrine organs, auditory cells, oligodendrocyte/myelin biology, or basal-ganglia vulnerability that this NeuN-enriched, postnatal, whole-brain-minus-hindbrain Perturb-seq screen cannot assay.
- The experiment measures nuclear RNA abundance only. A DCAF17 effect on nucleolar morphology, ribosome assembly, substrate ubiquitination, protein stability, or long-timescale survival could occur without producing many BH-significant snRNA-seq genes in `151 TH Prkcd Grin2c Glut`.
- The point estimate has threshold risk: a single weak gene crossing FDR would move the endpoint from 0 to 1 even if the qualitative conclusion of a buffered response remained the same.

## Final point prediction

`Dcaf17`: **0** DEGs at BH-adjusted Wilcoxon `p < 0.05` in `151 TH Prkcd Grin2c Glut`.
