# Prediction trace for Dgkd

## Question and endpoint

The requested held-out perturbation list in `055_Dgkd.csv` contains one target:

```tsv
target_name
Dgkd
```

I interpreted the endpoint as the total number of measured genes with `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` after CRISPR perturbation of `Dgkd`, with the target transcript itself included if it passes FDR. This matters because several one-DEG training perturbations in this cell group are self-transcript-only events.

The requested target was absent from both the all-cell differential-expression parquet and the focal training-count CSV, so no `Dgkd` DE signature was used directly.

## Sources used

- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed FDR<0.05 DEG counts for 1,674 non-held-out training perturbations in the focal cell group.
- `training_de_all_cell_groups.parquet`: per-gene Wilcoxon differential-expression statistics. I filtered this table to `group_name == "151 TH Prkcd Grin2c Glut"` when checking analog signatures.
- Distributed Agents same-experiment corpus `perturbai-july-260713-sourceguard-1773-v1`, including target context and bottom-up findings for `Dgke` and lexical claims for PI/DAG/PKC, postsynaptic calcium, and PI3K/mTOR perturbation neighborhoods.
- Run-local Distributed Agents profile tools, used to compare observed focal expression surfaces among selected analogs.
- PubMed-indexed literature on DGK enzymology and DGKdelta function:
  - Sakane and Kanoh 1997, DOI `10.1016/s1357-2725(97)00037-x`: DGKs convert DAG to phosphatidic acid and DGKdelta belongs to the type II PH-domain-containing DGK class.
  - Shulga et al. 2013, DOI `10.1021/bi401178y`: DGKdelta and DGKepsilon have nonredundant lipid outputs in fibroblasts, with DGKdelta promoting lipogenesis while DGKepsilon loss did not produce the same defect.
  - Murakami et al. 2020, DOI `10.1074/jbc.RA119.012369`: DGKdelta can use saturated/monounsaturated DG species supplied by sphingomyelin synthase-related protein rather than the arachidonoyl DG species typical of PI turnover.
  - Lu et al. 2018, DOI `10.1016/j.bbrc.2018.02.165`; Lu et al. 2019, DOI `10.1016/j.bbalip.2019.158608`; Lu et al. 2020, DOI `10.1002/1873-3468.13765`: brain-specific DGKdelta knockout affects serotonergic biology and SERT protein turnover through DGKdelta/Praja-1 signaling.
  - Ding et al. 2017, DOI `10.1038/s41598-017-05680-8`: DGKdelta can support ER exit of IFT88-containing vesicles for primary-cilium/Shh signaling, illustrating that it has subcellular functions outside a simple PI-cycle DAG sink.

## Dataset calibration

The focal training endpoint is extremely sparse:

- 1,674 training targets.
- Mean `n_degs = 14.1`, median `0`, 75th percentile `1`.
- 1,205 of 1,674 targets, 72.0%, had `0` DEGs.
- Only 28.0% of targets had any FDR<0.05 gene.

I therefore treated a zero or singleton prediction as the default unless a held-out gene had a close assayed analog with a real multi-gene response in `151 TH Prkcd Grin2c Glut`.

I filtered `training_de_all_cell_groups.parquet` to the focal cell group and selected PI/DAG/PKC or PI3K/mTOR-relevant perturbations. The FDR<0.05 counts in the original row table matched the training count CSV:

| perturbation | focal `n_degs` | focal significant genes | interpretation for Dgkd |
| --- | ---: | --- | --- |
| `Dgke` | 1 | `Dgke` only, logFC -0.586, FDR 5.97e-8 | closest assayed DGK-family lipid kinase; supports no downstream steady-state RNA response |
| `Plcb1` | 0 | none | upstream PI-cycle DAG production did not trigger a detectable program when lost |
| `Prkca` | 0 | none | canonical DAG/PKC effector was flat |
| `Prkcg` | 1 | `Prkcg` only, logFC -0.567, FDR 2.21e-11 | another DAG/PKC branch perturbation reduced only its own transcript |
| `Kdr` | 0 | none | endothelial VEGF-neighbor comparator for `Dgke`; flat in this neuron group |
| `Nrp1` | 0 | none | VEGF/co-receptor and axon-guidance comparator; flat |
| `C3` | 0 | none | complement/endothelial-disease comparator; flat in NeuN+ neurons |
| `Pitpna` | 21 | `Pitpna`, `Prkcg`, `Atp2a2`, tubulin/cytoskeleton-associated genes | broader PI-transfer perturbation; counterexample showing this cell group can respond to lipid handling, but not a close DGKdelta phenocopy |
| `Pitpnm3` | 0 | none | PI-transfer-related negative comparator |
| `Mtor` | 2 | `Rims3`, `Tmed8` | core mTOR kinase loss was sparse |
| `Pik3cb` | 0 | none | receptor-proximal PI3K branch was buffered |
| `Pik3r1` | 0 | none | receptor-proximal PI3K branch was buffered |
| `Pik3r2` | 0 | none | receptor-proximal PI3K branch was buffered |
| `Akt3` | 0 | none | downstream PI3K/Akt node was buffered |
| `Depdc5` | 13 | cholesterol/tubulin-skewed sparse response | GATOR1 negative-regulator counterexample; broader than `Dgkd` but much weaker than `Tsc2` |
| `Tsc2` | 86 | sterol/mTOR-axis response | negative mTORC1 regulator; active but biologically too distal to transfer directly to DGKdelta |
| `Agk` | 0 | none | mitochondrial lipid kinase, weak boundary comparison |
| `Dnajc13` | 1 | `Dnajc13` only | near-null control found near `Dgke` in same-experiment corpus comparisons |

I also checked whether training perturbations with exactly one DEG tend to be self-transcript events. Among training targets whose own transcript was measured, 237 of 275 one-DEG perturbations, 86.2%, had the target transcript itself as significant. Thus `Dgke` and `Prkcg` are not broad pathway responses: they are the common self-only pattern.

The run-local profile comparison on the 18 selected observed profiles confirmed the activity classes above: 11 had no focal FDR<0.05 genes, 4 had 1 to 9, 2 had 10 to 49, and only `Tsc2` had at least 50. I did not transfer the high whole-profile Pearson/cosine values from that comparison because they were inflated by shared extreme log-fold changes for effectively absent genes; FDR-level DEG counts and mechanistically selected neighbors were more reliable for this endpoint.

## Same-experiment corpus evidence

The Distributed Agents corpus had no `Dgkd` target record, consistent with `Dgkd` being held out. It did have three `Dgke` findings:

- `Dgke:F001`, high confidence: acute postnatal mosaic `Dgke` loss produced no robust pan-neuronal transcriptional output. Across 23 recovered cell groups, including groups with significant `Dgke` self-transcript depletion, every group had zero non-`Dgke` genes at FDR<0.10.
- `Dgke:F002`, moderate confidence: whole-score-vector comparisons placed `Dgke` in no detectable convergence module. The nearest full-surface neighbors were near zero correlation, so the corpus interprets `Dgke` as a flat signature, not as a weak copy of another response.
- `Dgke:F003`, moderate confidence: represented PI-cycle/DAG/PKC and endothelial-disease neighbors did not phenocopy `Dgke`; full-surface correlations between `Dgke` and `Plcb1`, `Prkca`, `Prkcg`, `Kdr`, `Nrp1`, and `C3` were all near zero in the corpus DE surface.

The corpus also contained a high-confidence mGluR/Homer/IP3R/PKC/CaMK/PSD claim: single-gene perturbations of represented postsynaptic calcium-plasticity and scaffold components generally failed to form a shared steady-state RNA module. This supports treating `Plcb1`, `Prkca`, and `Prkcg` as negative DAG/PKC branch evidence rather than expecting a latent postsynaptic calcium program after `Dgkd`.

PI3K/mTOR claims in the corpus separated buffered upstream PI3K/Akt and positive mTORC1 nodes (`Pik3cb`, `Pik3r1`, `Pik3r2`, `Akt3`, `Mtor`) from distinguishable negative-regulator responses (`Depdc5`, `Tsc2`). Those are useful counterexamples: the assay can detect a basal lipid/growth response in this cell type, but only for particular mTORC1-repressive nodes, not for receptor-proximal lipid kinases in general.

## Target-specific prediction for Dgkd

`Dgkd` encodes DGKdelta, a DAG kinase that consumes diacylglycerol and generates phosphatidic acid, so `Dgke` is the most direct assayed family analog. The transfer is imperfect: DGKepsilon preferentially handles arachidonoyl DAG in the PI cycle, whereas DGKdelta is a type II enzyme with PH/SAM domains and evidence for saturated/monounsaturated DG handling and SMSr-associated PA production. DGKdelta also has protein-level functions in SERT turnover and ciliary vesicle trafficking that `Dgke` would not model.

Despite those differences, the external DGKdelta mechanisms do not point to a broad autonomous transcriptional program in `151 TH Prkcd Grin2c Glut` under this assay:

- The SERT/Praja-1 brain-knockout results are serotonergic and protein/lipid centered, while the focal cell group is thalamic glutamatergic and the Perturb-seq readout is basal nuclear mRNA 3-4 weeks after partial mosaic CRISPR.
- The myoblast, adipocyte, beta-cell, and cilium literature mostly involves dividing or peripheral cells, specialized ER/ciliary trafficking, or metabolic challenge. Those contexts are poorly matched to juvenile postmitotic NeuN+ thalamic neurons.
- The within-dataset PI-cycle and PKC readouts nearest to a DGK perturbation are flat or self-only in the exact focal context.

For the zero/nonzero decision, I predicted that `Dgkd` would not have downstream genes at FDR<0.05. I did, however, assign one DEG rather than zero because the endpoint includes the target transcript and the closest positive analogs, `Dgke` and `Prkcg`, each had exactly one focal DEG corresponding to the perturbed transcript itself. `Dgkd` is a measured gene in the focal DE table for every non-held-out perturbation, and other perturbations can move it detectably, so a direct guide-induced `Dgkd` RNA decrease could plausibly cross BH FDR even if no downstream program appears.

Predicted `n_degs`: **1**.

## Limits and extrapolation

- `Dgkd` itself was held out, so there is no direct same-experiment signature, guide performance estimate, or target-RNA depletion measurement for `Dgkd`.
- `Dgke` is the only direct DGK-family target in the training perturbation set. It calibrates DAG kinase buffering in the assay but differs from DGKdelta in domain structure, acyl-chain preference, localization, and disease biology.
- A one-DEG call depends on whether the `Dgkd` transcript itself crosses FDR. The training data show this is common for one-DEG perturbations, but it is still more guide/transcript-expression dependent than a downstream biological program.
- The assay measures steady-state snRNA in basal juvenile postmitotic neurons. It would miss acute lipid second-messenger changes, local PKC activity, PA species, receptor trafficking, SERT protein abundance, ciliary vesicle trafficking, evoked activity-dependent transcription, and peripheral or endothelial phenotypes.
- The broad `Tsc2` and smaller `Depdc5` responses show that PI3K/mTOR-related transcription can be detectable in this cell type, but they are negative mTORC1 regulators rather than close DGKdelta analogs; using them quantitatively would overpredict `Dgkd`.
