# DEG-count prediction trace

## Question

The held-out target list contains one mouse perturbation, `Zfhx4`.  I interpreted the requested value as the integer number of measured genes expected to pass Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` in the `151 TH Prkcd Grin2c Glut` differential-expression contrast after acute AAV-CRISPR loss of function.  The readout is the statistical breadth of the recovered single-nucleus transcriptional response, not developmental essentiality, viability, target-RNA knockdown, or a raw effect-size sum.

`151 TH Prkcd Grin2c Glut` was used as an exact focal group label denoting thalamic glutamatergic neurons.  I did not treat the numeric prefix as a count or use fuzzy cell-type matches.

## Sources

- Direct endpoint: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Direct expression evidence: `training differential-expression dataset`, queried only for the focal cell group and mechanistically relevant visible perturbations.
- Run-local manifests: `task_bindings.json`, `coverage.json`, `measurement_registry.json`, and the PerturbAI atlas dataset portrait in `dataset_context.md`.
- PubMed literature found through NCBI E-utilities:
  - Nogami et al. 2005, J. Comp. Neurol., DOI `10.1002/cne.20382`, PMID `15612017`.
  - Perez Baca et al. 2025, Am. J. Hum. Genet., DOI `10.1016/j.ajhg.2025.04.008`, PMID `40367947`.
  - Komine et al. 2012, PLoS ONE, DOI `10.1371/journal.pone.0053114`, PMID `23300874`.
  - Ishii et al. 2003, J. Comp. Neurol., DOI `10.1002/cne.10807`, PMID `12926016`.
  - Jung et al. 2005, Development, DOI `10.1242/dev.02098`, PMID `16251211`.

The selected same-experiment PerturbAI July corpus was present, but the pre-decision coverage had no Zfhx4-specific Finding or report hit.  I therefore used the Parquet and focal training counts as the internal experimental evidence and did not use corpus graph topology, comparator multiplicity, or Finding summaries to order the prediction.

## Calibration From The Training Endpoint

The focal training endpoint has 1,674 visible biological perturbations.  It is very sparse:

| Statistic | Value |
|---|---:|
| minimum | 0 |
| median | 0 |
| 75th percentile | 1 |
| mean | 14.05 |
| maximum | 2,677 |
| targets with 0 DEGs | 1,205 |
| targets with >= 1 DEG | 469 |
| targets with >= 10 DEGs | 106 |
| targets with >= 100 DEGs | 43 |

Thus, for a target with no close visible positive analog, the empirical baseline is zero or at most one DEG.  I used direct focal counts for candidate analogs, then inspected their focal Parquet rows to distinguish true FDR-supported expression patterns from uninformative all-`pvals_adj = 1` rows.

## Target-Specific Evidence

### Zfhx4

**External function.** Zfhx4 encodes a very large zinc-finger homeobox transcription factor.  Nogami et al. cloned rat `Zfh4`, showed that the 390 kDa protein is structurally close to ATBF1/Zfhx3, and found expression in many developing postmitotic neurons with high neonatal signal in midbrain and diencephalon and lower expression after birth (Nogami 2005, DOI `10.1002/cne.20382`).  Perez Baca et al. established human ZFHX4 haploinsufficiency as a neurodevelopmental disorder gene and reported increased expression during human brain development and neuronal differentiation, ZFHX4 promoter binding near embryonic, neuronal, and axonal development genes, and craniofacial/behavioral defects in zebrafish `zfhx4` crispants (Perez Baca 2025, DOI `10.1016/j.ajhg.2025.04.008`).  Those data argue that ZFHX4 is biologically real in neural development, but they do not by themselves show that a partial, postnatal, mosaic knockout in already differentiated thalamic glutamatergic neurons should generate many FDR-significant survivor-state genes three to four weeks later.

**Closest within-screen analogs.**

| Visible perturbation | Relationship to Zfhx4 | `151 TH Prkcd Grin2c Glut` `n_degs` | Focal expression-pattern evidence |
|---|---|---:|---|
| `Zfhx2` | Same zinc-finger homeobox family; Komine et al. describe `Zfhx2` as another multi-homeodomain/multi-zinc-finger transcription factor expressed mainly in differentiating neurons in mouse brain (Komine 2012, DOI `10.1371/journal.pone.0053114`). | 0 | 203 matched perturbed nuclei and 23,679 controls; no measured gene passed FDR 0.05 and the adjusted p-value vector had no nominally small tail. |
| `Zfp423` | Neural zinc-finger transcription factor, but not a ZFHX paralog and not an obligate partner. | 150 | Strong outlying focal response, led by `Grid2ip`, `Cd47`, `Ntsr1`, `Kcnab3`, `Syt13`, and `Cnnm1` with FDR support.  This is a positive counterexample showing that some developmental zinc-finger regulators are visible, not a direct transfer because its biology is not the same as ZFHX4. |
| `Zeb1` / `Zeb2` | Zinc-finger E-box/homeobox regulators; broader transcription-factor analogs rather than direct paralogs. | 15 / 0 | `Zeb1` had a small but real focal signature headed by `Stxbp2`, `Ap1m2`, `F11r`, and `Cdc42bpg`; `Zeb2` was completely quiet.  The split argues against propagating response breadth by homeobox or zinc-finger class alone. |
| `Tcf4`, `Zbtb20`, `Bcl11a`, `Bcl11b`, `Foxp2`, `Meis1`, `Meis2`, `Pbx1` | Developmental neuronal transcription factors with roles in identity or differentiation programs, used as postmitotic TF counterexamples. | all 0 | None produced FDR 0.05 DEGs in the focal class.  Several all-null signatures contained huge log-fold changes paired with `pvals_adj = 1`; I treated those as sparse-expression/pseudocount artifacts, not evidence of a real large response. |
| `Arid1a`, `Arid1b`, `Arid2` | Chromatin-remodeling comparators, included because ZFHX4/ZFHX3 IP-MS studies implicate chromatin-associated binding partners. | 22 / 1 / 56 | These BAF/PBAF perturbations can yield low-to-moderate focal signatures, but they are complex subunits rather than ZFHX4 paralogs or downstream effectors. |
| `Mef2a`, `Mef2c`, `Mef2d`, `Sox5` | Neuronal activity/development TF comparators. | 4 / 1 / 0 / 2 | Low endpoint counts despite clear neural roles. |

I considered the intervention-to-readout chain as: acute CRISPR disruption of `Zfhx4` in juvenile thalamic glutamatergic neurons -> loss of one sequence-specific nuclear transcription factor -> altered target-gene regulation if ZFHX4 is expressed and nonredundant in these postmitotic cells -> recovered nuclei sampled at P37-P44 -> Wilcoxon DE against pooled controls.  The weak point in that chain is not target engagement but endpoint propagation.  The strongest direct analog, `Zfhx2`, did not cross FDR in the same focal class, and most homeobox/neurodevelopmental TFs in training were also zero.  `Zfp423`, `Zeb1`, and `Arid2` demonstrate that the class is capable of reporting TF/chromatin perturbations, but none supplies an obligate same-outcome prior for Zfhx4.

**Prediction.** I therefore predict no genes pass FDR 0.05 for `Zfhx4`: the final point estimate is `0`.  The prediction is driven mainly by within-dataset endpoint counts for ZFHX/homeobox/neurodevelopmental TF comparators; external ZFHX4 literature prevents treating the gene as a generic null target, but it supports an embryonic and neuronal-differentiation role more strongly than an acute broad transcriptomic requirement in the recovered juvenile thalamic neuron population.

## Limits

The requested Zfhx4 contrast itself is absent, so the answer is an extrapolation from visible analogs.  `Zfhx2` is the closest assayed paralog-like comparator but is not an experimentally established obligate partner of ZFHX4 in thalamic glutamatergic neurons.  Several visible developmental TFs were silent in this endpoint despite important developmental roles, which is informative for assay calibration but also highlights that zero DEG counts can reflect focal cell expression, postnatal timing, perturbation strength, sampling power, or survivor conditioning rather than absence of biology.  The ZFHX4 literature is richer in human/zebrafish developmental and rat embryonic/neonatal expression evidence than in acute mouse thalamic loss-of-function transcriptional profiling, so it was used as a prior about gene function rather than as a direct measurement of the requested endpoint.
